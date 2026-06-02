# Research budget per artifact type

Cost discipline for Mode 4 (AUTO-RESEARCH) in the output-quality-loop skill. Mode 4 composes with `perplexity-refinement`, which after the 2026-05-28 Phase 2 fix routes through Perplexity Pro (Path A: Claude in Chrome → Path B: Sonar API → refusal; silent Cowork `WebSearch` fallback is structurally forbidden). Every external query in auto-research mode therefore consumes either Pro credits (Path A, drawing on the operator's ~4,000-credits/month allocation) or pay-per-query Sonar billing (Path B, ~$0.005-$0.02 per query).

This file is the single source for "how many queries is auto-research allowed to run per artifact type, and which gaps does it prioritize." When the calibration drifts (a type's auto-research consistently under- or over-spends), update the table here once and Mode 4 picks up the change.

## The default caps

| Artifact type | Max queries per auto-research run | Top-N gaps researched | Notes |
|---|---|---|---|
| Core 30 page draft | **8** | top 5 | The highest-stakes artifact type; per-page rank + AI-citation outcomes compound over months. Compose with `competitor-deep-research` if shipped — its own Perplexity queries count against this cap. |
| Perplexity-refinement output | **6** | top 5 | Recursive composition with `perplexity-refinement` for deeper triangulation on the gaps. The recursive call inherits its own caps (3 / 7 / 15) — pick `light` (3) by default for recursive depth so the combined run stays under 9 queries total. |
| Cluster synthesis | **6** | top 5 | Compose with `multi-source-synthesis` review-agent mode. Queries target cluster claims with fewer than 3 sources cited (the premature-abstraction edge). |
| Cross-cluster synthesis | **8** | top 5 | Higher cap than cluster — cross-cluster synthesis spans more topics and more anchor questions need triangulation. |
| Research brief (any tier) | **5** | top 3 | Briefs already came out of a research-heavy skill (`service-seo-research`, `city-base-research`, `intersection-research`, `client-fact-research`); auto-research targets sections marked "operator follow-up pending" or "AI surfaces not reachable from Cowork" since those gaps are now reachable through Perplexity Sonar. |
| SKILL.md | **4** | top 3 | Targets rare or absent patterns ("what skills in this space do X better?"). Skill-design literature + agent-skill conventions + related work queries. Low default cap because skill-design queries return diminishing returns past ~4. |
| Source note (VIS ingestion) | **3** | top 3 | The source note is already the operator's distillation of one piece of content — auto-research should triangulate the 2-3 highest-tier extracted claims, not redo the whole VIS pass. For deeper refinement, the operator invokes `perplexity-refinement` directly with `medium` or `deep` depth, which is its own contract. |
| Blueprint | **8** | top 5 | Same cap as Core 30 — blueprints are high-leverage architectural artifacts. Queries target components whose mechanism is asserted without primary-source backing. |
| Tactic / tool / pattern / lesson note | **3** | top 2 | Small artifacts. If the tactic note has only 1-2 cited sources, auto-research surfaces 2-3 candidates for additional citation. Don't over-research; if more queries are warranted, the operator promotes to a full `perplexity-refinement` run. |

## Why these specific numbers

**Cap = 8 hard ceiling regardless of type.** A single artifact running auto-research consumes at most 8 Pro credits. That keeps a heavy month (50 evaluations × 8 queries = 400 credits) inside ~10% of monthly budget — auto-research can run on every evaluation without budget pressure.

**Top-N gaps researched is the soft ceiling.** The cap is what the artifact type is *allowed* to spend; the top-N is what it *will* spend by default. Most evaluations surface fewer gaps than the cap; auto-research only spends queries on real flagged gaps, not on filling the budget.

**Higher-stakes types get higher caps.** Core 30 pages, cross-cluster syntheses, and blueprints are the artifacts whose downstream impact compounds (a wrong fact on a published page erodes ranking; a wrong claim in a blueprint propagates into every system built from it). The cap follows the stakes.

**Recursive composition with `perplexity-refinement` is capped at `light` (3) by default.** Mode 4 invoking `perplexity-refinement` on a gap is recursive research — the same skill is asked to research the gaps in its own output. Without a low default depth, the recursive call could easily 2-3x the per-artifact budget. The operator can override to `medium` for specific high-value gaps; the default stays conservative.

## Configuration overrides

If a project consistently needs a higher or lower cap for a given type, override per-project in the skill's config (location TBD when the config layer ships; for v1 the operator overrides per-invocation):

- **Per-invocation override.** "Quality-check `<artifact>` with auto-research max=12" raises the cap to 12 for that single run. Surfaces in the folder log entry.
- **Per-artifact-type override.** When the same type warrants a different default across projects (e.g., S&H Core 30 pages may need fewer queries than EV's because S&H has thinner vault material to compare against), the override lives in the artifact-type's row of this file.

When you override, update the **Notes** column in the table above so future-Claude knows why the deviation happened.

## Cache reuse rules

Auto-research within the same loop iteration caches research results. If two gaps trigger the same query (e.g., "what's the strongest version of the capsule-content technique in current published work?" surfaces for both a Core 30 page evaluation AND a brief evaluation in the same chat), run the query once and reuse the answer for both gaps.

**Cache scope.** One loop iteration on one artifact. Caching across iterations on the same artifact (iteration 1 → iteration 2) is also allowed when the same gap reappears unchanged; it surfaces in the folder log as "Query cached from iteration N." Caching across separate artifacts is **not** allowed within v1 — the gap shapes differ enough that reusing a query would silently drop attribution discipline.

**Cache miss.** If the gap's wording differs but the underlying research question is the same, Mode 4 reformulates the question and runs a fresh query. The cache is keyed by the query text Mode 4 emits to `perplexity-refinement`, not by the gap.

## Termination rules (when to stop auto-research within a single run)

Even within the cap, auto-research stops early if:

1. **Top-5 gaps already covered.** If the EVALUATE pass surfaced only 3 gaps, auto-research runs only 3 queries (one per gap, plus any composed-skill queries each gap triggers). Don't pad the run to hit the cap.
2. **Three consecutive `inconclusive` query results.** The artifact's gaps may not be researchable through Perplexity Sonar (e.g., proprietary internal knowledge, vault-internal patterns, operator-discipline observations). Stop and surface that in the folder log under "External research" as "Stopped early: 3 inconclusive queries — gaps may not be externally researchable."
3. **Perplexity Sonar unavailable.** If `perplexity-refinement` returns the refusal message (Sonar API path missing), Mode 4 surfaces the gap to the operator and stops. Don't fall back to vault-internal research and pretend it filled the external benchmark — the audit trail breaks. (Historical note: pre-2026-06-01 versions referenced `no Path A, no Path B`. Path A was removed 2026-06-01.)
4. **Operator override during run.** If the operator intervenes mid-run ("skip the rest of the queries"), stop, log what was run, and proceed to the synthesis phase with whatever was collected.

## Tracking and audit

Every auto-research run writes to the folder log under the artifact's per-artifact section, in a sub-section titled `External research (Mode 4)`. The shape:

```markdown
### External research (Mode 4) — YYYY-MM-DD

**Path used:** Sonar API (`sonar-pro` or `sonar`)
**Queries run:** N of cap N (top M of top-5 gaps researched; K gaps skipped per termination rule)
**Cost incurred:** ~$X.XX

**Per-gap queries:**

1. **Gap:** <one-line gap from EVALUATE>
   - **Query:** "<query as run>"
   - **Verdict:** validates / partially-validates / contradicts / inconclusive
   - **Strongest source surfaced:** [URL]
   - **Elevation suggestion:** <what the revision prompt should add — one sentence>
2. ...

**Cache hits:** N (queries reused from earlier in this iteration)
**Termination reason:** "Top-N gaps covered" | "3 inconclusive results" | "Perplexity Sonar unavailable" | "Operator override"
```

The path-naming line is non-optional (same convention as `perplexity-refinement`'s cost-receipt line — see `~/workspace/skills/perplexity-shared/references/perplexity-cost-rules.md` § "Cost-receipt discipline"). Without it the operator can't audit Sonar spend across Mode 4 runs.

## Heavy-month warning thresholds

When monthly Path-A usage from auto-research alone exceeds **1,000 queries in the current calendar month (~25% of budget)**, Mode 4 surfaces a tally before the next run and asks whether to proceed. The router skill (`perplexity-research-suite`) tracks total monthly usage across the whole Perplexity suite per `perplexity-cost-rules.md` — Mode 4's local warning is additive, not a replacement.

## See also

- `~/workspace/skills/output-quality-loop/SKILL.md` § Mode 4 — the runtime behavior these caps govern
- `~/workspace/skills/output-quality-loop/references/evaluation-heuristics-by-type.md` § "Auto-research strategy" subsections — per-type research-question shapes that Mode 4 uses
- `~/workspace/skills/perplexity-shared/references/perplexity-cost-rules.md` — suite-wide cost rules; this file inherits its two-path priority + structural-refusal contract
- `~/workspace/skills/perplexity-refinement/SKILL.md` — the skill Mode 4 composes with as its research subroutine
