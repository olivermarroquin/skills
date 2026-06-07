---
type: reference
skill: gate-peer-reviewer
skill-version: 3.3
created: 2026-06-07
updated: 2026-06-07
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

## Standing fixtures (v3.2 seed suite)

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
