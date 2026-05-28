# Verdict rollup thresholds

Mode 1 Phase 5 takes the per-item evaluation (hard requirements + quality dimensions + discipline rules) and rolls it up to one of four verdicts. This file defines the thresholds.

## The four verdicts

| Verdict | Hard requirements | Quality dimensions | Discipline rules | What happens next |
|---|---|---|---|---|
| **PASS** | All met | ≥85% at threshold | 0 violations | Artifact ships. Folder log records the PASS; counter increments. |
| **NEEDS REVISION (minor)** | All met | 70-84% at threshold | ≤2 minor violations | Mode 2 emits a punch-list revision prompt. Producing chat applies edits, re-evaluates. |
| **NEEDS REVISION (substantive)** | All met | 50-69% at threshold | OR 3+ violations of any severity | Mode 2 emits a revision prompt with root cause. Producing chat redrafts sections or regenerates. |
| **FAIL** | Any miss | <50% at threshold | OR severe discipline-rule violation | Mode 2 emits a full diagnostic prompt. Producing chat regenerates from scratch. |

## Hard-requirement scoring

Hard requirements are binary: pass or fail. There's no "partial credit" on a hard requirement.

**Single miss on a hard requirement = FAIL.** No exceptions. Hard requirements are the floor; if the floor isn't there, nothing above it matters.

If a hard requirement is genuinely not applicable to the artifact (e.g., "schema validation" doesn't apply to a tactic note), mark it `not-applicable` with a one-line explanation. Don't mark items not-applicable to keep the verdict from dropping — that's gaming the rollup.

## Quality-dimension scoring

Each quality dimension scores as:

- **pass** — at or above threshold; full weight toward PASS verdict
- **partial** — above floor but below bar; half weight toward PASS verdict
- **fail** — below floor; zero weight toward PASS verdict
- **not-applicable** — excluded from both numerator and denominator (rare; use sparingly)

The threshold percentage is calculated as:

```
threshold_pct = (passes + 0.5 * partials) / (passes + partials + fails)
```

`not-applicable` dimensions don't appear in the denominator.

Edge case: when a quality dimension is high-stakes (the heuristics file flags it as load-bearing — e.g., "every claim has a citation" for refinement outputs, or "cross-creator attributions are accurate" for cluster syntheses), a fail on that single dimension elevates the verdict regardless of overall percentage:

- High-stakes dimension at fail + everything else PASS → NEEDS REVISION (substantive)
- High-stakes dimension at fail + ≥1 other dimension fail → FAIL

The high-stakes flag is documented in the per-type heuristics file.

## Discipline-rule scoring

Discipline rules score as:

- **pass** — rule honored
- **fail** — rule violated, no severity tier
- **fail (severe)** — rule violated AND the violation is load-bearing (e.g., a non-destructive violation that silently rewrote operator content; a fabricated citation; a promotion-math escalation that wasn't supported)

**Severity tiers:**

- 0 violations → no impact on verdict
- 1 minor violation → no impact on verdict (still PASS-eligible)
- 2 minor violations → verdict can still be PASS, but borderline
- 3+ violations of any severity → verdict elevates to NEEDS REVISION (substantive) at minimum
- 1 severe violation → verdict elevates to NEEDS REVISION (substantive) at minimum; possibly FAIL depending on what else is broken

Severe violations include:

- Non-destructive default violated (the producing chat silently rewrote existing content)
- Fabricated citation (a source is cited but the source doesn't actually say what's claimed)
- Premature-abstraction (a pattern's definition was stretched mid-synthesis to make math read clean)
- Promotion-math misstatement (2/3 claimed as 3/3, or vice versa)
- Silent fallback to a forbidden source (e.g., Cowork WebSearch when Perplexity Pro is the contract)

## Verdict examples

These examples show how the rollup works in practice. They're not actual evaluations — they're illustrative.

### Example 1: clean PASS

- Hard requirements: 8/8 pass
- Quality dimensions: 6 pass, 1 partial, 0 fail (6.5 / 7 = 93%)
- Discipline rules: 0 violations

→ **PASS**

### Example 2: NEEDS REVISION (minor)

- Hard requirements: 8/8 pass
- Quality dimensions: 4 pass, 2 partial, 1 fail (5 / 7 = 71%)
- Discipline rules: 1 minor violation (slug-only wikilink rule missed)

→ **NEEDS REVISION (minor)**. The punch list: bump the 1 fail to partial-or-pass, sharpen the 2 partials, fix the wikilink format.

### Example 3: NEEDS REVISION (substantive) via percentage

- Hard requirements: 8/8 pass
- Quality dimensions: 3 pass, 1 partial, 3 fail (3.5 / 7 = 50%)
- Discipline rules: 1 minor violation

→ **NEEDS REVISION (substantive)**. Several sections need redrafting; surface-level edits won't cut it.

### Example 4: NEEDS REVISION (substantive) via discipline rules

- Hard requirements: 8/8 pass
- Quality dimensions: 6 pass, 1 partial (6.5 / 7 = 93%)
- Discipline rules: 3 minor violations

→ **NEEDS REVISION (substantive)**. The percentage would have landed PASS, but the discipline-rule violations are the load-bearing concern.

### Example 5: NEEDS REVISION (substantive) via high-stakes dimension

- Hard requirements: 8/8 pass
- Quality dimensions: 6 pass, 0 partial, 1 fail (where the fail is "every claim has a citation" for a refinement output, flagged as high-stakes) — overall percentage 86%
- Discipline rules: 0 violations

→ **NEEDS REVISION (substantive)**. The single high-stakes dimension at fail is the verdict driver, regardless of the overall percentage.

### Example 6: FAIL via hard requirement

- Hard requirements: 7/8 pass, 1 fail (frontmatter missing required field)
- Quality dimensions: 6 pass, 1 partial (93%)
- Discipline rules: 0 violations

→ **FAIL**. One hard-requirement miss = FAIL, no matter how strong the rest looks.

### Example 7: FAIL via severe discipline rule

- Hard requirements: 8/8 pass
- Quality dimensions: 6 pass, 1 partial (93%)
- Discipline rules: 1 severe violation (fabricated citation)

→ **FAIL**. A severe discipline-rule violation is sufficient cause for FAIL when paired with any other quality concern (here, the 1 partial).

## Why these thresholds

The numbers (85%, 70%, 50%) are calibration anchors derived from the Jono refinement evaluation Oliver did manually on 2026-05-27. That evaluation landed on "strong work, no critical gaps" — which in this rubric is PASS at the ~85-90% quality-dimension level.

The thresholds bias slightly conservative: a 70% quality score doesn't ship; it gets a revision prompt. The reasoning is that revision prompts are cheap (Mode 2 is free), so the cost of a false-positive revision prompt is small, while the cost of a false-positive PASS is meaningful (a flawed artifact ships and starts being referenced by downstream artifacts).

The thresholds are deliberately not "scientific" — they're calibration anchors that maintenance note M3 in the SKILL.md says to re-check when verdict drift appears.

## Calibration check (built into Mode 1)

After every 10 evaluations on a given artifact type, the skill compares its verdict distribution against the expected shape:

- Roughly 60-70% PASS for established artifact types (refinement outputs, source notes)
- Roughly 30-40% PASS for high-bar artifact types (Core 30 pages, cluster syntheses)
- Roughly 50% PASS for new-skill SKILL.md evaluations (these tend to land borderline)

If the actual distribution skews dramatically off these expectations, surface a calibration warning in the folder log's frontmatter and propose a heuristics review.

## Update path

The thresholds in this file are the single source of truth for verdict rollup. When the thresholds change (after a calibration review), update this file first, then the maintenance note in the SKILL.md.

Per-type adjustments live in `evaluation-heuristics-by-type.md`'s threshold notes — those override the defaults here only when the heuristics file says so explicitly.
