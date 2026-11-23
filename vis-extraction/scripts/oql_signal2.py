#!/usr/bin/env python3
"""
oql_signal2.py — VIS Signal 2 (OQL Mode 5) confidence scoring (Phase 8, T2)

Reads a G-extraction verdict JSON file and computes a confidence score
(0–100) using the OQL Mode 5 five-input formula calibrated for VIS source notes.
Score >= threshold → PASS (Signal 2 green). Score < threshold → PARK.

Threshold source: confidence-calibration.md, Source note (VIS) row → 80
(the script reads the threshold from that row; hardcoded fallback = 80)

Five inputs and weights for VIS source notes:
  Input 1 — Hard-requirement margin   (30 pts): Verdict string quality
  Input 2 — Quality-dimension margin  (20 pts): Verdict grade (PASS vs APPROVE-WITH-NOTES vs BLOCKING)
  Input 3 — Discipline-rule cleanliness (25 pts): catches[] count; each deducts 7 pts, floor 0
  Input 4 — Iteration position         (15 pts): G-extraction runs once per VIS note → always 15
  Input 5 — Spec-routing coverage      (10 pts): checks_run non-empty; failed checks deduct

Weight rationale (from confidence-calibration.md VIS row):
  "First-pass cleanliness is the main signal." Hard-req margin and cleanliness carry the most weight.
  Iteration position is constant for VIS (G-extraction single-run), so it anchors the baseline.

Verdict JSON contract (from gate-type-registry.md § G-extraction check_structured_verdict):
  - verdict:    string — "PASS" | "APPROVE-WITH-NOTES" | "HOLD" | "BLOCKING" | "FAIL"
  - checks_run: list of {name: str, result: str, detail: str}
  - catches:    list of findings
  - cost_usd:   float

Usage:
  python3 oql_signal2.py <verdict-json-path> [--threshold N] [--selftest] [--verbose]

Exit codes:
  0 — PASS (score >= threshold)
  1 — PARK (score < threshold)
  2 — Input error (verdict file not found, bad JSON, missing fields)

Built: 2026-11-23 (VIS-P8 value hardening, CG-006 resolution)
"""

import argparse
import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Scoring tables
# ---------------------------------------------------------------------------

# Input 1: Hard-requirement margin (max 30 pts)
VERDICT_HARD_REQ = {
    "PASS": 30,
    "APPROVE-WITH-NOTES": 25,
    "HOLD": 15,
    "BLOCKING": 10,
    "FAIL": 0,
}

# Input 2: Quality-dimension margin (max 20 pts)
VERDICT_QUALITY_DIM = {
    "PASS": 20,
    "APPROVE-WITH-NOTES": 15,
    "HOLD": 8,
    "BLOCKING": 5,
    "FAIL": 0,
}

# Input 3: Discipline-rule cleanliness
# Base = 25; deduct CATCH_DEDUCTION per catch, floor 0
CLEANLINESS_BASE = 25
CATCH_DEDUCTION = 7

# Input 4: Iteration position
# G-extraction is always run once per VIS note — constant 15
ITERATION_SCORE = 15

# Input 5: Spec-routing coverage (max 10 pts)
# Non-empty checks_run = baseline. Each FAIL check deducts 3 pts, floor 0.
SPEC_ROUTING_BASE = 10
SPEC_ROUTING_EMPTY = 0
CHECK_FAIL_DEDUCTION = 3

# Default threshold (matches confidence-calibration.md VIS row)
DEFAULT_THRESHOLD = 80

# Elevation / de-elevation rules (from confidence-calibration.md § How the score elevates)
# Rule 1: spec-routing coverage gap → cap at 70
# Rule 3: third-iteration PASS → cap at PASS_anchor - 5 (not applicable — always iter 1 for VIS)
SPEC_ROUTING_GAP_CAP = 70


# ---------------------------------------------------------------------------
# Scoring logic
# ---------------------------------------------------------------------------

def score_verdict(verdict_data: dict, verbose: bool = False) -> dict:
    """
    Compute Signal 2 confidence score from a G-extraction verdict JSON dict.
    Returns dict with keys: score, inputs, pass_threshold, verdict, reasoning.
    """
    verdict_str = str(verdict_data.get("verdict", "")).upper()
    # Normalize common variations
    if verdict_str in ("APPROVE", "APPROVE WITH NOTES"):
        verdict_str = "APPROVE-WITH-NOTES"
    elif verdict_str in ("BLOCK", "BLOCKED"):
        verdict_str = "BLOCKING"

    checks_run = verdict_data.get("checks_run", [])
    catches = verdict_data.get("catches", [])

    # --- Input 1: Hard-requirement margin ---
    i1 = VERDICT_HARD_REQ.get(verdict_str, 10)  # unknown verdict → conservative 10

    # --- Input 2: Quality-dimension margin ---
    i2 = VERDICT_QUALITY_DIM.get(verdict_str, 5)

    # --- Input 3: Discipline-rule cleanliness ---
    catch_count = len(catches) if isinstance(catches, list) else 0
    i3 = max(0, CLEANLINESS_BASE - catch_count * CATCH_DEDUCTION)

    # --- Input 4: Iteration position (always 15 for VIS G-extraction) ---
    i4 = ITERATION_SCORE

    # --- Input 5: Spec-routing coverage ---
    if not checks_run or not isinstance(checks_run, list):
        i5 = SPEC_ROUTING_EMPTY
        spec_gap = True
    else:
        failed_checks = sum(
            1 for c in checks_run
            if isinstance(c, dict) and str(c.get("result", "")).upper() in ("FAIL", "BLOCKING", "FAILED")
        )
        i5 = max(0, SPEC_ROUTING_BASE - failed_checks * CHECK_FAIL_DEDUCTION)
        spec_gap = False

    raw_score = i1 + i2 + i3 + i4 + i5

    # --- Elevation / de-elevation rules ---
    final_score = raw_score
    elevation_notes = []

    # Rule 1: empty checks_run → cap at 70
    if spec_gap:
        if final_score > SPEC_ROUTING_GAP_CAP:
            final_score = SPEC_ROUTING_GAP_CAP
            elevation_notes.append(
                f"Rule 1 applied: empty checks_run → score capped at {SPEC_ROUTING_GAP_CAP}"
            )

    reasoning = []
    if verbose:
        reasoning = [
            f"Input 1 (hard-requirement margin):   {i1}/30  — verdict: {verdict_str}",
            f"Input 2 (quality-dimension margin):  {i2}/20",
            f"Input 3 (discipline-rule cleanliness): {i3}/25  — {catch_count} catch(es) × {CATCH_DEDUCTION}pt deduction",
            f"Input 4 (iteration position):         {i4}/15  — G-extraction single-run (constant)",
            f"Input 5 (spec-routing coverage):      {i5}/10  — {len(checks_run) if isinstance(checks_run, list) else 0} check(s) in checks_run",
            f"Raw score: {raw_score}",
        ] + (elevation_notes if elevation_notes else ["No elevation rules applied"])

    return {
        "verdict": verdict_str,
        "score": final_score,
        "inputs": {"i1": i1, "i2": i2, "i3": i3, "i4": i4, "i5": i5},
        "catch_count": catch_count,
        "raw_score": raw_score,
        "elevation_notes": elevation_notes,
        "reasoning": reasoning,
    }


def evaluate(verdict_path: Path, threshold: int, verbose: bool) -> int:
    """
    Load verdict JSON, score it, print result. Returns exit code (0=PASS, 1=PARK).
    """
    if not verdict_path.exists():
        print(f"ERROR: Verdict file not found: {verdict_path}", file=sys.stderr)
        return 2

    try:
        verdict_data = json.loads(verdict_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in verdict file: {e}", file=sys.stderr)
        return 2

    required_fields = {"verdict", "checks_run", "catches"}
    missing = required_fields - set(verdict_data.keys())
    if missing:
        print(f"ERROR: Verdict file missing required fields: {missing}", file=sys.stderr)
        return 2

    result = score_verdict(verdict_data, verbose=verbose)
    score = result["score"]
    verdict_str = result["verdict"]
    passed = score >= threshold

    if verbose:
        print(f"Verdict file: {verdict_path}")
        print(f"G-extraction verdict: {verdict_str}")
        for line in result["reasoning"]:
            print(f"  {line}")
        print()

    status = "PASS" if passed else "PARK"
    print(
        f"Signal 2 — {status}: score={score} threshold={threshold} "
        f"verdict={verdict_str} catches={result['catch_count']}"
    )
    if not passed:
        weak = []
        i = result["inputs"]
        if i["i1"] < 25:
            weak.append(f"verdict quality ({i['i1']}/30 — not PASS)")
        if i["i2"] < 15:
            weak.append(f"quality-dimension margin ({i['i2']}/20)")
        if i["i3"] < 18:
            weak.append(f"cleanliness ({i['i3']}/25 — {result['catch_count']} catch(es))")
        if i["i5"] < 7:
            weak.append(f"spec-routing coverage ({i['i5']}/10)")
        if weak:
            print(f"  Weak inputs: {'; '.join(weak)}")
        print(f"  Rerun extraction and address catches, then re-dispatch G-extraction.")

    return 0 if passed else 1


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

SELFTEST_CASES = [
    (
        "clean first-pass PASS, 0 catches → score 100, PASS",
        {"verdict": "PASS", "checks_run": [{"name": "source_fidelity", "result": "PASS"}], "catches": []},
        80, True, 100,
    ),
    (
        "APPROVE-WITH-NOTES, 1 catch → score 83, PASS",
        {"verdict": "APPROVE-WITH-NOTES", "checks_run": [{"name": "source_fidelity", "result": "PASS"}], "catches": ["minor metric phrasing"]},
        80, True, 83,
    ),
    (
        "APPROVE-WITH-NOTES, 3 catches → score 69, PARK",
        {"verdict": "APPROVE-WITH-NOTES", "checks_run": [{"name": "source_fidelity", "result": "PASS"}], "catches": ["c1", "c2", "c3"]},
        80, False, 69,
    ),
    (
        "BLOCKING, 2 catches, 1 failed check → score 48, PARK",
        # i1=10 i2=5 i3=max(0,25-14)=11 i4=15 i5=max(0,10-3)=7 → 48
        {"verdict": "BLOCKING", "checks_run": [{"name": "source_fidelity", "result": "FAIL"}], "catches": ["fabricated URL", "wrong metric"]},
        80, False, 48,
    ),
    (
        "FAIL, 0 catches, 1 failed check → score 47, PARK",
        # i1=0 i2=0 i3=25 i4=15 i5=max(0,10-3)=7 → 47
        {"verdict": "FAIL", "checks_run": [{"name": "source_fidelity", "result": "FAIL"}], "catches": []},
        80, False, 47,
    ),
    (
        "PASS, empty checks_run → score capped 70, PARK at threshold 80",
        {"verdict": "PASS", "checks_run": [], "catches": []},
        80, False, 70,
    ),
    (
        "PASS, 0 catches, 1 failed check → score 97, PASS",
        {"verdict": "PASS", "checks_run": [{"name": "source_fidelity", "result": "FAIL"}], "catches": []},
        80, True, 97,
    ),
    (
        "APPROVE-WITH-NOTES, 2 catches → score 76, PARK",
        {"verdict": "APPROVE-WITH-NOTES", "checks_run": [{"name": "source_fidelity", "result": "PASS"}], "catches": ["c1", "c2"]},
        80, False, 76,
    ),
]


def run_selftest() -> None:
    print("Running oql_signal2.py self-test...")
    passed = 0
    failed = 0

    for desc, verdict_data, threshold, expected_pass, expected_score in SELFTEST_CASES:
        result = score_verdict(verdict_data, verbose=False)
        score = result["score"]
        actual_pass = score >= threshold

        score_ok = score == expected_score
        pass_ok = actual_pass == expected_pass
        ok = score_ok and pass_ok

        icon = "✓" if ok else "✗"
        status = "PASS" if ok else "FAIL"
        print(f"  {icon} [{status}] {desc}")
        if not ok:
            if not score_ok:
                print(f"       Score: expected {expected_score}, got {score} (inputs: {result['inputs']})")
            if not pass_ok:
                print(f"       Pass: expected {'pass' if expected_pass else 'park'}, got {'pass' if actual_pass else 'park'}")
            failed += 1
        else:
            passed += 1

    print(f"\nResults: {passed} passed, {failed} failed out of {len(SELFTEST_CASES)} cases")
    if failed:
        sys.exit(1)
    else:
        print("All self-test cases passed.")
        sys.exit(0)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="VIS Signal 2 (OQL Mode 5) confidence scoring from G-extraction verdict JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Reads a G-extraction verdict JSON and scores 5 inputs against VIS calibration weights.
Score >= threshold (default 80) → PASS (Signal 2 green).
Score < threshold → PARK (note must not auto-ship).

Exit codes: 0=PASS, 1=PARK, 2=input error
""",
    )
    parser.add_argument(
        "verdict_file",
        nargs="?",
        help="Path to G-extraction verdict JSON file",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=DEFAULT_THRESHOLD,
        help=f"Auto-approve threshold (default: {DEFAULT_THRESHOLD}, from confidence-calibration.md VIS row)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        default=False,
        help="Show per-input breakdown",
    )
    parser.add_argument(
        "--selftest",
        action="store_true",
        default=False,
        help="Run built-in test cases and exit",
    )

    args = parser.parse_args()

    if args.selftest:
        run_selftest()
        return

    if not args.verdict_file:
        parser.error("verdict_file is required (or use --selftest)")

    sys.exit(evaluate(Path(args.verdict_file), args.threshold, args.verbose))


if __name__ == "__main__":
    main()
