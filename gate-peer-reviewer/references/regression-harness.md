---
type: reference
skill: gate-peer-reviewer
skill-version: 3.7
created: 2026-06-07
updated: 2026-06-16
tags: [reference, regression-harness, testing, planted-defects, GPR-14]
---

# Regression harness — standing planted-defect suite

**Purpose.** Repeatable test suite run at every reviewer version bump to verify that known-caught defect classes remain caught. Prevents silent regression (D-12 partially regressed into the meta field; this harness would have caught it at the version bump that introduced the regression).

**When to run.** MUST run green before any version bump is committed. If any fixture goes red, the version bump is blocked until the regression is fixed.

---

## Architecture

The harness is a set of **test fixtures** — each fixture is a minimal artifact with one or more planted defects of a known class. The reviewer is dispatched against each fixture with a known gate type. The expected outcome (catch class, severity, verdict) is declared in the fixture metadata. Pass = reviewer catches the defect with correct severity. Fail = reviewer misses the defect OR misclassifies severity.

**Engine-level.** Fixtures are project-agnostic. They use synthetic data (fake client slugs, fake city names, fake service names) so they don't depend on any real project's data directory. The harness tests the PROCEDURE logic, not the domain data.

---

## Fixture format

Each fixture is a directory under `references/regression-fixtures/` with:

```
<fixture-slug>/
├── fixture.yaml          # metadata: gate_type, expected_catches, expected_verdict, expected_severity
├── artifact.*            # the planted-defect artifact (HTML, JSON, markdown — depends on gate type)
├── ground-truth/         # fake data files the reviewer would load (for value-cross-check fixtures)
│   └── *.json
└── README.md             # human-readable explanation of what's planted and why
```

### fixture.yaml schema

```yaml
fixture_id: <kebab-case unique ID>
description: <one-line description of what's being tested>
gate_type: <G-data | G-scaffold | G-publish | G-service-brief | G-extraction | ...>
defect_class: <D-10 | D-11 | D-12 | D-13 | PR-04 | PR-15 | PR-16 | PR-19a | meta-only | ...>
planted_defects:
  - surface: <body | meta-description | og:title | og:description | json-ld | frontmatter>
    defect_type: <placeholder | source-client-leak | wrong-value | missing-value>
    description: <what's wrong>
    expected_catch_severity: <blocking | nit | calibration | follow-up>
expected_verdict: <REJECT-AND-REDO | APPROVE-WITH-NOTES>
expected_verdict_severity: <blocking | advisory>
procedures_that_must_fire:
  - <full-placeholder-family-sweep | source-client-leak-audit | ground-truth-value-cross-check | live-rendered-cache-busted-verification>
introduced_at_version: <skill version when this fixture was added>
regression_for: <D-row or PR number this prevents regressing>
```

---

## Standing fixtures (v3.2 seed suite + v3.6 G-chat-close + v3.7 COA-4b corpus)

### Fixture 1: `meta-only-placeholder`

**Tests:** GPR-12 (meta-description missed THREE times before GPR-12).
**Gate type:** G-publish
**Planted defect:** Body text is clean. `<meta name="description">` contains `FILL: service description for {city_name}`. All other surfaces clean.
**Expected:** `full-placeholder-family-sweep` catches it on surface 3 (meta-description). Severity: blocking. Verdict: REJECT-AND-REDO.
**Regression for:** Alexandria / Springfield / Burke-Lorton meta-description misses.

### Fixture 2: `og-title-source-client-leak`

**Tests:** GPR-12 (leak audit must cover og:title, not just body).
**Gate type:** G-scaffold
**Planted defect:** Body text uses correct client name. `<meta property="og:title">` contains source client's business name ("EV Electric Services" on a non-EV artifact).
**Expected:** `source-client-leak-audit` catches it on layer D (og:title). Severity: blocking. Verdict: REJECT-AND-REDO.
**Regression for:** PR-04 class extended to metadata layers.

### Fixture 3: `jsonld-wrong-value`

**Tests:** GPR-10/RQ1 (value-correctness layer catches wrong value in JSON-LD).
**Gate type:** G-publish
**Planted defect:** Body text has correct city name ("Stafford"). JSON-LD `areaServed.name` has wrong city ("Fairfax"). Ground-truth JSON says "Stafford".
**Expected:** `ground-truth-value-cross-check` catches MISMATCH on `city_name` fact, surface `jsonld_schema`. Severity: blocking. Verdict: REJECT-AND-REDO.
**Regression for:** D-10 (Fairfax areaServed on Stafford page).

### Fixture 4: `body-clean-meta-wrong-dispatch-time`

**Tests:** GPR-10 + GPR-12 combined (value wrong in meta but correct in body).
**Gate type:** G-scaffold
**Planted defect:** Body says "15-minute response time" (correct per ground-truth). Meta-description says "45-minute response time" (wrong — the dangerous default). Ground-truth JSON says `dispatch_time: "15-minute"`.
**Expected:** `ground-truth-value-cross-check` catches MISMATCH on `dispatch_time` fact, surface `meta_description`. Severity: blocking. Verdict: REJECT-AND-REDO.
**Regression for:** D-12 (45-min dispatch on 15-mi city), specifically the meta-field regression.

### Fixture 5: `unrendered-template-brace-in-schema`

**Tests:** GPR-12 (placeholder sweep covers JSON-LD).
**Gate type:** G-publish
**Planted defect:** Body text is clean. JSON-LD `description` field contains `{phone_display}` (unrendered template brace).
**Expected:** `full-placeholder-family-sweep` catches `\{[a-z_]+\}` on surface 6 (JSON-LD/schema). Severity: blocking. Verdict: REJECT-AND-REDO.
**Regression for:** PR-16 ({phone_display} leaked) extended to schema surface.

### Fixture 6: `research-brief-wrong-county` (non-SEO proof)

**Tests:** GPR-10 value-correctness on a NON-page-build artifact.
**Gate type:** G-city-brief
**Planted defect:** Research brief claims "Located in Fairfax County" for a city that ground-truth says is in "Stafford County".
**Expected:** `ground-truth-value-cross-check` (research-brief profile) catches MISMATCH on `city_county_alignment`. Severity: blocking. Verdict: REJECT-AND-REDO.
**Regression for:** D-10 class on non-SEO artifact type. Proves engine-level applicability.

### Fixture 7: `advisory-only-nit` (severity tier proof)

**Tests:** GPR-13 (advisory catches don't force operator review).
**Gate type:** G-service-brief
**Planted defect:** Research brief has slightly inconsistent capitalization in section header ("Key considerations" vs template's "Key Considerations"). No blocking issues.
**Expected:** Check 1 flags as `nit` severity. `verdict_severity: advisory`. Verdict: APPROVE-WITH-NOTES.
**Regression for:** Severity tier classification — ensures advisory tier works and doesn't over-escalate.

### Fixture 8: `chat-close-missing-exec-log` (v3.6 — G-chat-close OC-1)

**Tests:** OC-1 — multi-step build chat with no execution log at close.
**Gate type:** G-chat-close
**Chat profile:** build
**Planted defect:** No `execution-log-*.md` exists in any expected path. OC-1 `ls` finds nothing.
**Expected:** OC-1 fires → BLOCKING. Gate prevents close until exec log is written.
**Regression for:** WF-1 gap #1 (exec log rationalized away at close); S&H wave A2 (same class).

### Fixture 9: `chat-close-missing-version-paperwork` (v3.6 — G-chat-close OC-10)

**Tests:** OC-10 — skill-build chat edits SKILL.md without version bump, changelog, or event-log row.
**Gate type:** G-chat-close
**Chat profile:** skill-build
**Planted defect:** SKILL.md edited (new reference added) but: version field not bumped, no changelog entry, no event-log row. All three paperwork elements missing.
**Expected:** OC-10 fires → BLOCKING. Gate prevents close until all three paperwork elements present.
**Regression for:** competitor-deep-research v1.1 close (missing version paperwork, 06-03). Also proves the skill-build profile works independently of the WF-1/COA-4b seed corpora (acceptance criterion A2).

---

## COA-4b replay corpus (v3.7 — 16 fixtures, 12 runnable + 4 design-verified)

> Added by [RGH-FIN] (`rgh-fin-coa4b-fixtures-reconnect-202606151430`). Source:
> `[[../../second-brain/_meta/handoffs/review-gate-hardening/evidence-2026-06-15-coa4b-25-catch-replay-corpus|COA-4b evidence]]`.
> These are the **deterministic** catches from the COA-4b site-capture-engine build
> (25 total, 15 deterministic) — each reconstructed as a synthetic fixture with
> `defect/` (pre-fix condition) and `clean/` (post-fix condition) states.
> Suite result: **32/32 expectations met, 0 failures, 0 false positives.**

### OC-12 fixtures (per-deliverable existence)

#### Fixture 10: `coa4b-c11` — Fabricated SingleFile (OC-12)

**Tests:** OC-12 — deliverable reported as produced but absent on disk.
**Bound check:** OC-12 (`oc-12-per-deliverable-existence.py`)
**Planted defect:** `deliverables.json` lists `singlefile/*.html` as non-stub; `defect/` has no `singlefile/` directory. Manifest claims 43 captured.
**Expected:** OC-12 FAIL on defect (path does not exist); PASS on clean (real SingleFile HTML present).
**Regression for:** COA-4b C-11 — fabricated 9.9MB SingleFile artifact; self-verdict PASS'd ground-truth-cross-check.

#### Fixture 11: `coa4b-c18` — Missing deliverable (OC-12)

**Tests:** OC-12 — deliverable required by spec but never produced.
**Bound check:** OC-12
**Planted defect:** `deliverables.json` lists `tracker/v1.1-row.md`; `defect/` has no `tracker/` directory.
**Expected:** OC-12 FAIL on defect; PASS on clean (tracker row present).
**Regression for:** COA-4b C-18 — v1.1 Tier-3 tracker row criterion unmet, unflagged.

### OC-13 fixtures (count-reconciliation vs source)

#### Fixture 12: `coa4b-c12` — Font completeness 0/9 (OC-13)

**Tests:** OC-13 — count assertion fails when 0 of 9 required fonts downloaded.
**Bound check:** OC-13 (`oc-13-count-reconciliation.py`)
**Planted defect:** `assertions.json` requires `count == 9` for `assets/font/*`; `defect/` has empty font dir.
**Expected:** OC-13 FAIL on defect (0 != 9); PASS on clean (9 woff2 files).
**Regression for:** COA-4b C-12 — "60 downloaded" (true, incomplete framing).

#### Fixture 13: `coa4b-c13` — Sampled denominator 10/43 (OC-13)

**Tests:** OC-13 — count assertion fails when only 10 of 43 pages checked.
**Bound check:** OC-13
**Planted defect:** `count == 43` for `broken-links/*.json`; `defect/` has only 10 files.
**Expected:** OC-13 FAIL on defect (10 != 43); PASS on clean (43 files).
**Regression for:** COA-4b C-13 — `broken_links: 0` implies full coverage; actually sampled 10/43.

#### Fixture 14: `coa4b-c15` — Manifest/disk contradiction (OC-13)

**Tests:** OC-13 manifest-matches-disk — manifest says wp_export skipped but export files exist on disk.
**Bound check:** OC-13
**Planted defect:** `capture-manifest.json` records `file_count: 0` + status `skipped`; 2 wp-export files present.
**Expected:** OC-13 FAIL on defect (manifest 0 != disk 2); PASS on clean (manifest 2 == disk 2).
**Regression for:** COA-4b C-15 — manifest says skipped, export exists.

#### Fixture 15: `coa4b-c16` — Incomplete presented complete 35/43 (OC-13)

**Tests:** OC-13 — count assertion fails when only 35 of 43 pages present.
**Bound check:** OC-13
**Planted defect:** `count == 43` for `pages/*.html`; `defect/` has only 35 files.
**Expected:** OC-13 FAIL on defect (35 != 43); PASS on clean (43 files).
**Regression for:** COA-4b C-16 — completeness 35/43, presented complete.

#### Fixture 16: `coa4b-c17` — Count exceeds source 84/43 (OC-13)

**Tests:** OC-13 — count assertion fails when captured exceeds source (duplication).
**Bound check:** OC-13
**Planted defect:** `count <= source_count` with source 43; `defect/` has 84 files.
**Expected:** OC-13 FAIL on defect (84 > 43); PASS on clean (43 files).
**Regression for:** COA-4b C-17 — 84 of 43 pages, "cosmetic" mislabel.

### OC-14 fixtures (rename-propagation completeness)

#### Fixture 17: `coa4b-c03` — Dead path after rename (OC-14)

**Tests:** OC-14 — live handoff still references old skill path after rename.
**Bound check:** OC-14 (`oc-14-rename-propagation.py`)
**Planted defect:** `live/program-handoff.md` references `seo-site-teardown` (old name).
**Expected:** OC-14 FAIL on defect (1 live straggler); PASS on clean (updated to `site-capture-engine`).
**Regression for:** COA-4b C-03 — dead path in program handoff, BLOCKING.

#### Fixture 18: `coa4b-c04` — Stale registry entry (OC-14)

**Tests:** OC-14 — coverage matrix still lists old skill name after rename.
**Bound check:** OC-14
**Planted defect:** `live/coverage-matrix.md` lists `seo-site-teardown 1.0`.
**Expected:** OC-14 FAIL on defect; PASS on clean.
**Regression for:** COA-4b C-04 — stale registry entry.

#### Fixture 19: `coa4b-c05` — Stale live forward-refs batch (OC-14)

**Tests:** OC-14 — multiple live docs name old skill in compose lists / future-spawn instructions.
**Bound check:** OC-14
**Planted defect:** 3 live files reference `seo-site-teardown`; 1 historical file (exempt).
**Expected:** OC-14 FAIL on defect (3 live stragglers); PASS on clean (all updated).
**Regression for:** COA-4b C-05/C-08/C-09/C-10 — stale live forward-refs.

#### Fixture 20: `coa4b-c02` — Version-string inconsistency (OC-14)

**Tests:** OC-14 — UA strings still reference old version after bump.
**Bound check:** OC-14
**Planted defect:** 3 occurrences of `site-capture-engine/1.0` in `capture_site.py` (should be 2.0).
**Expected:** OC-14 FAIL on defect (3 live stragglers); PASS on clean (all 2.0).
**Regression for:** COA-4b C-02 — "fixed (2 places)" but 3 remained.

### OC-15 fixtures (frontmatter freshness)

#### Fixture 21: `coa4b-c24` — Stale updated: frontmatter (OC-15)

**Tests:** OC-15 — files edited on 2026-06-15 still carry stale `updated:` dates.
**Bound check:** OC-15 (`oc-15-frontmatter-freshness.py`)
**Planted defect:** 3 files with `updated: 2026-06-04` / `2026-06-06` (stale).
**Expected:** OC-15 FAIL on defect (3 stale); PASS on clean (all `2026-06-15`).
**Regression for:** COA-4b C-24 — incomplete staleness sweep (QC fixed 2/5, missed 3).

### OC-16 fixtures (commit-staging audit — design-verified, deferred to RGH-2)

> OC-16 requires a real git repository to test `git status` vs dirty-ledger reconciliation.
> These fixtures contain the dirty-ledger JSONL and expected-finding descriptions.
> True execution testing deferred to [RGH-2]'s conformance suite (git-hook integration).

#### Fixture 22: `coa4b-c07` — Build artifact committed (OC-16)

**Tests:** OC-16 — `__pycache__/` staged for commit.
**Bound check:** OC-16 (`oc-16-commit-staging-audit.py`)
**Design-verified:** dirty-ledger + expected finding documented; needs git repo to execute.
**Regression for:** COA-4b C-07.

#### Fixture 23: `coa4b-c21` — Foreign files staged (OC-16)

**Tests:** OC-16 — another chat's deliverables staged in this chat's commit.
**Bound check:** OC-16
**Design-verified:** dirty-ledger + expected finding documented; needs git repo to execute.
**Regression for:** COA-4b C-21 — staged MI-1's deliverables.

#### Fixture 24: `coa4b-c22` — Artifact omitted from commit (OC-16)

**Tests:** OC-16 — peer-review log produced but not staged.
**Bound check:** OC-16
**Design-verified:** dirty-ledger + expected finding documented; needs git repo to execute.
**Regression for:** COA-4b C-22 — omitted review log.

#### Fixture 25: `coa4b-c23` — Rename deletions unstaged (OC-16)

**Tests:** OC-16 — old directory deletions not staged after rename.
**Bound check:** OC-16
**Design-verified:** dirty-ledger + expected finding documented; needs git repo to execute.
**Regression for:** COA-4b C-23 — rename deletions unstaged.

---

## Running the harness

### Manual run (at version bump)

For each fixture:

1. Read `fixture.yaml` to know expected outcomes.
2. Read `artifact.*` as the gate output.
3. Read `ground-truth/*.json` if the fixture has them (for value-cross-check).
4. Dispatch the peer-reviewer against the artifact with the declared `gate_type`.
5. Compare actual verdict, catches, and severity against `fixture.yaml` expectations.
6. Report: PASS (all expectations met) or FAIL (specific expectation violated + what happened instead).

### Automated run (future — when Hermes-harness ships)

The harness becomes a pre-commit hook: `scripts/run-regression-harness.sh` iterates fixtures, dispatches the reviewer via Task sub-agent per fixture, compares outputs, exits non-zero on any FAIL. Blocks the version-bump commit.

---

## Adding new fixtures

When a D-row is written for a new defect class:

1. Create `references/regression-fixtures/<fixture-slug>/`.
2. Write `fixture.yaml` with the expected outcomes.
3. Create a minimal `artifact.*` with ONLY the planted defect (keep fixtures small — test one thing per fixture).
4. Add `ground-truth/*.json` if the fixture needs value-cross-check data.
5. Write `README.md` explaining what's planted and why.
6. Run the harness to verify the fixture goes green against current reviewer version.
7. (Optional) Deliberately reintroduce the fixed defect and verify the fixture goes red.

### Naming convention

`<defect-surface>-<defect-type>[-<qualifier>]`

Examples: `meta-only-placeholder`, `og-title-source-client-leak`, `jsonld-wrong-value`, `body-clean-meta-wrong-dispatch-time`.

---

## Relationship to acceptance tests

The regression harness is NOT a substitute for the acceptance tests documented in check-spec.md worked examples (PR-01, PR-07, PR-15, PR-16, PR-17, PR-19a, PR-19b reproductions). Those test the reviewer against REAL production artifacts. The regression harness tests against SYNTHETIC fixtures to catch regressions at version-bump time without needing real project data.

Both must pass. Regression harness is fast (synthetic, no external dependencies). Acceptance tests are thorough (real data, real complexity). Run regression harness at every bump; run acceptance tests at major version bumps (x.0).
