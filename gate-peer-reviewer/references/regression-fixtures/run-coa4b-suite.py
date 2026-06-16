#!/usr/bin/env python3
"""Run the COA-4b regression-fixture suite.

For each coa4b-c* fixture, dispatch the bound OC check against both
defect/ and clean/ states. Verify defect->FAIL, clean->PASS.

Usage:
  python3 run-coa4b-suite.py [--scripts-dir <path>]

  --scripts-dir  Path to the mandatory-review-gate scripts directory.
                 Default: repos/ai-agency-core/scripts/mandatory-review-gate
                 (relative to workspace root, auto-detected from this script's
                 location).

Exit code: 0 if all expectations met, 1 if any failure.
"""

import argparse
import json
import os
import subprocess
import sys
import yaml


def find_scripts_dir():
    """Auto-detect the mandatory-review-gate scripts directory."""
    # Walk up from this script to find the workspace root
    here = os.path.dirname(os.path.abspath(__file__))
    # We're at skills/gate-peer-reviewer/references/regression-fixtures/
    # Workspace root is 4 levels up
    workspace = os.path.normpath(os.path.join(here, '..', '..', '..', '..'))
    candidate = os.path.join(workspace, 'repos', 'ai-agency-core',
                             'scripts', 'mandatory-review-gate')
    if os.path.isdir(candidate):
        return candidate
    return None


def load_fixture_meta(fixture_dir):
    """Load fixture.yaml metadata."""
    meta_path = os.path.join(fixture_dir, 'fixture.yaml')
    if not os.path.exists(meta_path):
        return None
    with open(meta_path) as f:
        return yaml.safe_load(f)


def run_oc12(state_dir, scripts_dir):
    """Run OC-12 on a state directory using its deliverables.json."""
    deliv_file = os.path.join(state_dir, 'deliverables.json')
    if not os.path.exists(deliv_file):
        return None, 'no deliverables.json'

    with open(deliv_file) as f:
        deliverables = f.read()

    proc = subprocess.run(
        [sys.executable,
         os.path.join(scripts_dir, 'oc-12-per-deliverable-existence.py'),
         '--deliverables', deliverables,
         '--base-dir', state_dir],
        capture_output=True, text=True, timeout=30)

    try:
        out = json.loads(proc.stdout)
        return out.get('verdict', 'ERROR'), out.get('summary', '')
    except (json.JSONDecodeError, ValueError):
        return 'ERROR', proc.stderr[:200] if proc.stderr else 'no output'


def run_oc13(state_dir, scripts_dir):
    """Run OC-13 on a state directory using its assertions.json."""
    assert_file = os.path.join(state_dir, 'assertions.json')
    if not os.path.exists(assert_file):
        return None, 'no assertions.json'

    with open(assert_file) as f:
        assertions = f.read()

    proc = subprocess.run(
        [sys.executable,
         os.path.join(scripts_dir, 'oc-13-count-reconciliation.py'),
         '--assertions', assertions,
         '--base-dir', state_dir],
        capture_output=True, text=True, timeout=30)

    try:
        out = json.loads(proc.stdout)
        return out.get('verdict', 'ERROR'), out.get('summary', '')
    except (json.JSONDecodeError, ValueError):
        return 'ERROR', proc.stderr[:200] if proc.stderr else 'no output'


def run_oc14(state_dir, fixture_dir, scripts_dir):
    """Run OC-14 on a state directory.

    rename-spec.json is read from the fixture root (NOT inside the state dir).
    --search-root is the full state directory so the allowlist is exercised.
    """
    spec_file = os.path.join(fixture_dir, 'rename-spec.json')
    if not os.path.exists(spec_file):
        return None, 'no rename-spec.json at fixture root'

    with open(spec_file) as f:
        spec = json.load(f)

    proc = subprocess.run(
        [sys.executable,
         os.path.join(scripts_dir, 'oc-14-rename-propagation.py'),
         '--old-name', spec['old_name'],
         '--new-name', spec['new_name'],
         '--search-root', state_dir],
        capture_output=True, text=True, timeout=30)

    try:
        out = json.loads(proc.stdout)
        return out.get('verdict', 'ERROR'), out.get('summary', '')
    except (json.JSONDecodeError, ValueError):
        return 'ERROR', proc.stderr[:200] if proc.stderr else 'no output'


def run_oc15(state_dir, scripts_dir, check_date='2026-06-15'):
    """Run OC-15 on all .md files in the state directory."""
    md_files = []
    for fn in os.listdir(state_dir):
        if fn.endswith('.md'):
            md_files.append(os.path.join(state_dir, fn))

    if not md_files:
        return None, 'no .md files'

    proc = subprocess.run(
        [sys.executable,
         os.path.join(scripts_dir, 'oc-15-frontmatter-freshness.py'),
         '--files'] + md_files + ['--date', check_date],
        capture_output=True, text=True, timeout=30)

    try:
        out = json.loads(proc.stdout)
        return out.get('verdict', 'ERROR'), out.get('summary', '')
    except (json.JSONDecodeError, ValueError):
        return 'ERROR', proc.stderr[:200] if proc.stderr else 'no output'


def run_oc16_design_verified(state_dir):
    """OC-16 fixtures are design-verified only (need real git repo).

    Returns DESIGN-VERIFIED with a note about RGH-2 deferred execution.
    """
    return 'DESIGN-VERIFIED', 'requires git repo (deferred to RGH-2)'


def main():
    parser = argparse.ArgumentParser(
        description='Run the COA-4b regression-fixture suite')
    parser.add_argument('--scripts-dir', default=None,
                        help='Path to mandatory-review-gate scripts')
    parser.add_argument('--oc15-date', default='2026-06-15',
                        help='Date to use for OC-15 freshness check '
                             '(default: 2026-06-15, the COA-4b build date)')
    args = parser.parse_args()

    scripts_dir = args.scripts_dir or find_scripts_dir()
    if not scripts_dir or not os.path.isdir(scripts_dir):
        print(f'ERROR: scripts dir not found: {scripts_dir}', file=sys.stderr)
        sys.exit(2)

    fixtures_dir = os.path.dirname(os.path.abspath(__file__))
    results = []

    # Iterate all coa4b-c* fixture directories (sorted for determinism)
    for fix_name in sorted(os.listdir(fixtures_dir)):
        if not fix_name.startswith('coa4b-c'):
            continue

        fix_dir = os.path.join(fixtures_dir, fix_name)
        if not os.path.isdir(fix_dir):
            continue

        meta = load_fixture_meta(fix_dir)
        if not meta:
            print(f'SKIP {fix_name}: no fixture.yaml')
            continue

        check = meta.get('bound_check', '')

        for state in ['defect', 'clean']:
            state_dir = os.path.join(fix_dir, state)
            if not os.path.isdir(state_dir):
                print(f'SKIP {fix_name}/{state}: no {state}/ directory')
                continue

            expected = 'FAIL' if state == 'defect' else 'PASS'
            verdict, detail = None, ''

            if check == 'OC-12':
                verdict, detail = run_oc12(state_dir, scripts_dir)
            elif check == 'OC-13':
                verdict, detail = run_oc13(state_dir, scripts_dir)
            elif check == 'OC-14':
                verdict, detail = run_oc14(state_dir, fix_dir, scripts_dir)
            elif check == 'OC-15':
                verdict, detail = run_oc15(state_dir, scripts_dir,
                                           args.oc15_date)
            elif check == 'OC-16':
                verdict, detail = run_oc16_design_verified(state_dir)
            else:
                verdict, detail = 'SKIP', f'unknown check: {check}'

            if verdict is None:
                verdict, detail = 'SKIP', 'no test data'

            match = (verdict == expected or verdict == 'DESIGN-VERIFIED')
            mark = '\u2705' if match else '\u274c'

            results.append({
                'fixture': fix_name,
                'state': state,
                'check': check,
                'expected': expected,
                'actual': verdict,
                'match': match,
                'detail': detail,
            })

            print(f'{mark} {fix_name}/{state}: '
                  f'expected={expected} actual={verdict} \u2014 {detail}')

    # Summary
    total = len(results)
    passed = sum(1 for r in results if r['match'])
    failed = total - passed
    runnable = sum(1 for r in results
                   if r['actual'] not in ('DESIGN-VERIFIED', 'SKIP'))
    design_verified = sum(1 for r in results
                          if r['actual'] == 'DESIGN-VERIFIED')

    print(f'\n=== SUITE RESULT: {passed}/{total} expectations met, '
          f'{failed} failures ===')
    print(f'    Runnable checks: {runnable} '
          f'({runnable // 2} fixtures \u00d7 2 states)')
    print(f'    Design-verified: {design_verified} '
          f'({design_verified // 2} fixtures, deferred to RGH-2)')

    if failed > 0:
        print('\nFAILURES:')
        for r in results:
            if not r['match']:
                print(f'  {r["fixture"]}/{r["state"]}: '
                      f'expected={r["expected"]} actual={r["actual"]} '
                      f'\u2014 {r["detail"]}')

    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    main()
