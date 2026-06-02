# Confidence calibration (Mode 5)

How the quality loop turns a verdict into a confidence score, and how that score maps to an auto-approve decision.

This file is the source of truth for two things:
1. **Per-artifact-type confidence multipliers** — how reliable a verdict of this shape is at predicting what the operator would have decided
2. **Per-artifact-type auto-approve thresholds** — the score above which a PASS verdict ships without operator review

Updated quarterly as more real-use data accumulates. The next scheduled refresh is **2026-08-28** (three months from Phase 6 ship). Add a row to the "Calibration history" table at the bottom every time the file is updated.

---

## What is a confidence score?

A number from 0 to 100 attached to every verdict the loop emits. It says: "of the verdicts that looked like this one — same artifact type, same verdict, same pattern of pass/fail across the checklist — what fraction did the operator agree with?"

A PASS at 95 confidence means: in the calibration set, 95% of PASS verdicts on this artifact type were artifacts the operator shipped without further edit. A PASS at 60 confidence means: only 60% of comparable PASS verdicts survived operator review — the other 40% needed at least one round of edits before they shipped.

Confidence is per-type, not global. A PASS on a refinement output is not the same evidence as a PASS on a Core 30 page — different specs, different risk, different cost of being wrong. Phase 6 keeps the math separate.

---

## How the score is computed

Five inputs, weighted per type.

1. **Hard-requirement margin.** How comfortably did the artifact clear the hard requirements? All-clear at first iteration is stronger evidence than all-clear after two regenerations.
2. **Quality-dimension margin.** How far above the verdict's quality-dimension threshold is this artifact? 95% is stronger evidence than 86% for a PASS verdict.
3. **Discipline-rule cleanliness.** Zero violations is stronger evidence than two minor violations that didn't elevate the verdict.
4. **Iteration position.** First-iteration PASS is stronger evidence than third-iteration PASS. By the third iteration, the producing chat has been retrained against the spec and may be passing on form rather than substance.
5. **Spec-routing coverage.** All routed spec sources loaded cleanly is stronger evidence than two of seven sources flagged "stale" or "missing."

Weights live in the calibration table below per artifact type. The five inputs compose into a single 0-100 score using a weighted average, rounded to the nearest integer.

The score is **written into two places**:

1. **The artifact's own frontmatter**, alongside `last-verdict:`:

   ```yaml
   last-confidence-score: 95
   ```

2. **The folder-level `_quality-log.md`**, in the per-artifact section's Latest line and in the iteration metadata block:

   ```markdown
   **Latest:** PASS (2026-05-28) — iteration 1 of 3 — confidence 95
   ```

Mode 5's auto-approve gate reads the score from the artifact's frontmatter. The folder log holds the archaeology.

---

## Per-artifact-type calibration

The table below is the starting calibration for Phase 6 ship (2026-05-28). It anchors on conservative defaults from the handoff plus the small real-use dataset described in "Real-use data backing this calibration" below.

| Artifact type | Auto-approve threshold | PASS-confidence anchor | REVISION-confidence anchor | FAIL-confidence anchor | Weight notes |
|---|---|---|---|---|---|
| Refinement output | **80** | 75 | 70 | 70 | Low-stakes, revertible. Margin matters less; first-pass cleanliness matters most. |
| Cluster synthesis | **90** | 80 | 70 | 75 | Downstream tactic-promotion blast radius. Spec-routing coverage weighted high. |
| Core 30 page draft | **95** | 70 | 65 | 75 | Highest-stakes, ships to client site. Iteration position weighted high (1st-iter PASS is rare; mid-iter PASS warrants distrust). |
| SKILL.md | **90** | 70 | 65 | 75 | Permanent system component. Body changes propagate everywhere. Hard-requirement margin weighted high. |
| Tactic note | **85** | 75 | 70 | 70 | Affects vault graph. Discipline-rule cleanliness weighted high (citation discipline). |
| Tool note | **85** | 75 | 70 | 70 | Same shape as tactic. |
| Pattern note | **85** | 75 | 70 | 70 | Same shape, slightly higher promotion threshold (3+ observed instances rule). |
| Lesson note | **85** | 75 | 70 | 70 | Same shape as pattern. |
| Source note (VIS) | **80** | 80 | 70 | 70 | Low downstream radius. First-pass cleanliness is the main signal (matches Phase 1 Jono regression where PASS confidence sat high on first iteration). |
| Research brief | **85** | 75 | 70 | 75 | Feeds downstream scaffolders. Spec-routing coverage weighted high. |
| Cross-cluster synthesis | **90** | 75 | 70 | 75 | Same shape as cluster synthesis. |
| Blueprint | **90** | 70 | 65 | 75 | High blast radius — blueprints feed multiple downstream initiatives. |
| Scaffolded data file (service/city/client JSON) | **90** | 80 | 70 | 75 | Schema-validity-sensitive; FILL-placeholder detection load-bearing. Downstream scaffolders + publish pipeline depend on correctness. Added 2026-06-02 (v1.1 client-seo-onboarding Step 3). |
| Imagery-prompt log | **80** | 75 | 70 | 70 | Mid-stakes; operator still picks variants downstream so prompt imperfection is recoverable. Higgsfield prompt-craft is fast-moving; lower anchor reflects external-knowledge dependence. Added 2026-06-02 (v1.1 client-seo-onboarding Step 6). |
| Internal-link proposals + dead-link audit | **85** | 75 | 70 | 70 | Affects corpus graph + crawl behavior; per-axis completeness matters. Audit accuracy is binary (file exists or doesn't). Added 2026-06-02 (v1.1 client-seo-onboarding Step 10). |
| Onboarding final report | **85** | 80 | 70 | 70 | Aggregate summary; cross-checks state vs report. Most gaps are arithmetic mismatches; first-pass cleanliness is the main signal. Added 2026-06-02 (v1.1 client-seo-onboarding Step 11). |

**Reading the table:**

- **Auto-approve threshold** is the score above which a PASS verdict ships without operator review. A PASS at 94 on a Core 30 page does NOT auto-ship — Core 30 needs 95+. The artifact goes to light escalation.
- **PASS-confidence anchor** is the starting point for PASS verdicts on this type before the five-input weighting fires. A new artifact-type with no calibration history defaults to the anchor.
- **REVISION-confidence anchor** is the starting point for NEEDS REVISION verdicts. Below this anchor, the revision prompt is probably weak — the producing chat may regenerate without addressing the real gap.
- **FAIL-confidence anchor** is the starting point for FAIL verdicts. High FAIL confidence is itself a quality signal: a high-confidence FAIL means the artifact is genuinely broken, not borderline.

**The thresholds are deliberately conservative for Phase 6 ship.** Phase 6's calibration data is sparse (n=3 PASS verdicts, 1 BYPASS event — all known-good test artifacts). Conservative thresholds mean more low-confidence PASS verdicts land in light escalation, which the operator can ship-or-revise; nothing auto-ships on a thin signal. Tune downward when the calibration history shows the operator agreeing with low-margin PASS verdicts at high rates.

---

## Real-use data backing this calibration

As of 2026-05-28, the dataset is small. Phase 6 ships early (operator green-lit before the original 2-week-wait gate); calibration matures with use.

**Verdicts recorded across `_quality-log.md` files vault-wide:**

| Folder | Artifact | Type | Verdict | Iteration | Operator-accepted? |
|---|---|---|---|---|---|
| `03_domains/seo/` | cluster-synthesis-ai-era-seo-cluster-2026-05-27 | cluster synthesis | PASS | 1 of 3 | Yes (shipped 2026-05-27) |
| `03_domains/seo/insights/` | source-2026-04-26-jono-catliff-claude-code-seo-50000-clicks-per-month-masterclass | refinement output | PASS | 1 of 3 | Yes (operator hand-eval matched skill verdict) |
| `05_shared-intelligence/research-briefs/intersections/` | panel-upgrade--vienna-va | research brief (intersection) | PASS | 1 of 3 | Yes (handoff named as "high-quality reference artifact") |
| `04_projects/clients/_active/ev-electric-services/website-archive/new/core-30/02-panel-upgrade-vienna-va/` | panel-upgrade-vienna-va (Core 30 page) | Core 30 page draft | (BYPASSED) | n/a | n/a — operator overrode the gate rather than running the loop |

**Aggregate signals:**

- 3 PASS verdicts emitted, 3 operator-accepted (100%)
- 0 NEEDS REVISION or FAIL verdicts
- All 3 PASS verdicts landed at iteration 1 (no loop required)
- 1 publish bypass on the highest-stakes artifact type (Core 30 page) — the operator chose to skip the loop rather than run it

**What this calibration set can and can't tell us:**

It can tell us that on known-good test artifacts hand-picked as regression cases, the skill's PASS verdicts agree with the operator at 100%. That's a floor signal, not a ceiling signal — these are the easiest cases.

It can't tell us anything about NEEDS REVISION calibration (no real data), FAIL calibration (no real data), or how iteration position correlates with operator agreement (no iteration-2 or iteration-3 verdicts exist yet).

It tells us the bypass path is the most-used path for highest-stakes artifacts. Phase 6 treats `--bypass-quality-loop` as a first-class audit-trail event, not as an edge case.

**Why ship Phase 6 now anyway:** the operator named the trade-off explicitly. Conservative thresholds mean more escalations during the early-data window; the cost is operator review time on borderline cases, which is exactly what the operator wants to see. As the dataset grows, thresholds tune; the quarterly refresh at the top of this file is when that happens.

---

## When to recalibrate

**Quarterly refresh — every 90 days.** Pull the last 90 days of `_quality-log.md` entries vault-wide; for each verdict, mark whether the operator agreed (shipped without edit on PASS, accepted the revision on NEEDS REVISION, agreed regeneration was needed on FAIL); recompute per-type confidence anchors. Update the table above; add a row to the calibration history.

**Triggered refresh — any of these.** Skip the quarterly cadence and recalibrate now if:

1. **Operator overrides cross 10% on any type.** If the operator manually escalates or manually approves PASS-below-threshold verdicts on a type more than 1 in 10 times, the threshold is wrong.
2. **Auto-shipped artifacts produce post-ship corrections.** If a Core 30 page ships at 96 confidence and gets reverted within 48 hours, the auto-approve gate let through something it shouldn't have. Lower the threshold on that type until the dataset says it's safe to raise it again.
3. **A new artifact type appears in the routing table.** Phase 5 surfaced 6 emerging types (plain-language-companion, invoice-vault-record, bridge-note, reading-guide, citation-history-snapshot, design-dossier). When any of these gain a routing-table row, add a calibration row here with conservative anchors (60 PASS / 60 REVISION / 70 FAIL / 90 auto-approve threshold) and tune from there.

**Operator-initiated refresh.** The operator can edit this file directly at any time. The auto-approve gate reads the table fresh on every run; changes apply immediately. See `operator-controls.md` for the workflow.

---

## How the score elevates or de-elevates

These rules fire before the auto-approve gate reads the score. Apply in order; first match wins.

1. **Spec-routing coverage gap → score capped at 70.** If any routed spec source was unreachable (file moved, link broken, external URL down) during Mode 1 Phase 2, the verdict was built on incomplete evidence. Confidence is capped at 70 regardless of the weighted average, which keeps the artifact below every auto-approve threshold in the table.

2. **High-stakes dimension fail elevates the verdict but does not elevate the score.** A high-stakes-dimension fail flips a PASS to NEEDS REVISION via the existing rollup. The resulting NEEDS REVISION carries the de-elevated confidence (revision anchor for the type, adjusted by the same five inputs) — not the PASS anchor.

3. **Third-iteration PASS verdicts are capped at the PASS-confidence anchor minus 5.** By iteration 3, the producing chat has seen the spec multiple times and may be passing on form. Cap protects against trained-to-the-test artifacts auto-shipping.

4. **Mode 4 auto-research that returned "validates" on every gap adds 5 to the score.** External benchmark confirmed every flagged gap is at parity with the strongest published work. Cap at 100.

5. **Mode 4 auto-research that returned "inconclusive" on 3+ gaps subtracts 10.** Gaps that aren't externally researchable might be genuinely novel or genuinely fabricated. Honest discount until the operator confirms.

These elevation rules are the load-bearing piece of the calibration. The base score from the weighted average is the rough cut; rules 1-5 shape it against the verdict's actual evidence quality.

---

## Calibration history

Every update to this file appends a row here.

| Date | Author | Change | Trigger |
|---|---|---|---|
| 2026-05-28 | Phase 6 ship | Initial table; conservative anchors; n=3 real-use verdicts + n=1 bypass event backing the calibration | Phase 6 build |
| 2026-06-02 | client-seo-onboarding v1.1 | Added 4 new rows: Scaffolded data file (90), Imagery-prompt log (80), Internal-link proposals + dead-link audit (85), Onboarding final report (85). Conservative-by-default; calibration data sparse until v1.1 first real use. | v1.1 SKILL rewrite (per-step quality loop integration needs per-type thresholds for the artifacts the orchestrator produces) |
| (next: 2026-08-28) | quarterly refresh | TBD | TBD |

---

## See also

- `../SKILL.md` § Mode 5 — AUTO-APPROVE-AND-ESCALATE — how the score gates auto-ship
- `operator-controls.md` — how the operator overrides, manually escalates, adjusts thresholds, clears escalations
- `verdict-rollup-thresholds.md` — the verdict assignment rules the confidence score derives from
- `folder-quality-log-shape.md` — where the score is written in the folder log
- `evaluation-heuristics-by-type.md` — the per-type heuristic source the calibration weights against
