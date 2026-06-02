---
type: reference
status: v1.1
created: 2026-06-02
updated: 2026-06-02
skill: client-seo-onboarding
tags: [skill-reference, sizing, scope-estimation, multi-chat-decomposition]
---

# Per-artifact sizing table

Companion to [[SKILL]]. The canonical per-artifact minute estimates the scope-estimation gate uses to compute total run hours + chat count + wave decomposition.

**Sourced from:** real-use data from the EV Electric build (2026-05) and the S&H first-real-run (2026-06-01) plus the v1.0 SKILL.md's informal per-step sizing language. Calibrate this table as more real-use signal lands.

## Per-artifact minute table

| Artifact | New (no reuse) | Reused (already exists) | Notes |
|---|---|---|---|
| Tier-1 service brief | 25 min | 0 min | Via `service-seo-research`; covers all cities for one service |
| Tier-2 city brief | 20 min | 0 min | Via `city-base-research`; covers all services for one city |
| Tier-3 intersection brief | 15 min | 0 min | Via `intersection-research`; one cell per brief; highest volume in Core 30 |
| Client-fact brief | 30 min | 0 min | Via `client-fact-research`; one per client; meeting notes + intake form synthesis |
| `client-<slug>.json` data file | 5 min | 0 min | Via `scaffold-client-data.py` |
| `services/<slug>.json` data file | 5 min | 0 min | Via `scaffold-service-data.py`; one per confirmed service |
| `cities/<slug>.json` data file | 7 min | 0 min | Via `scaffold-city-data.py`; one per confirmed city; intersection-brief threading adds time |
| WP REST API verification | 5 min | n/a | One-time per client; no reuse semantics |
| Scaffold one Core 30 page | 2 min | n/a | Via `bulk-scaffold-pages.py` per page; bulk run is faster per-page |
| Imagery prompts per page | 3 min | n/a | Via `generate-imagery-prompts.py` per page |
| Higgsfield variant pick (operator) | 5-10 min | n/a | Operator-attended; per page |
| Wire + publish per page | 4 min | n/a | Via `wire-page-images.py` per page |
| Per-page GSC indexing | 1 min | n/a | Auto-submitted by `publish-core-30-page.py` |
| Internal-link proposals (corpus) | 15 min | n/a | One pass per corpus via `insert-internal-links.py` |
| Operator review of link proposals | 20 min | n/a | Operator-attended; per corpus |
| Apply approved diffs + republish | 30 min | n/a | Per corpus; scales with number of pages with links to add |
| Dead-link audit | 5 min | n/a | One pass per corpus via `audit-published-links.py` |
| Final report | 15 min | n/a | One per client |

## Quality-loop overhead per artifact

Per the v1.1 per-step quality loop contract, every artifact-producing step adds quality-loop runtime on top of the produce time above. Empirical estimates (calibrate as data lands):

| Quality-loop mode | Typical added time per artifact | Notes |
|---|---|---|
| Mode 1 (EVALUATE) only — PASS first iteration | +2-3 min | Reads artifact + walks spec sources + writes folder log |
| Mode 1 + Mode 4 (one iteration) | +5-8 min | Adds 3-5 Sonar queries (~$0.06-$0.15) plus regeneration time |
| Mode 1 + Mode 4 (3 iterations to PASS) | +20-30 min | Worst-case path before stall |
| Mode 5 escalation routing | +1 min | Light or hard escalation file writes |

**Budget rule:** when computing total run hours, add `+15%` to the base per-artifact minutes for quality-loop overhead. This is a rough average across the verdict distribution; tune as real data lands.

## Scope-estimation formula

```
total_hours = (
  sum(new_artifacts × per_artifact_minutes) +
  sum(operator_attended_minutes)
) × 1.15  # quality-loop overhead

estimated_chat_count = ceil(total_hours / per_chat_budget_hours)
```

Defaults:
- `per_chat_budget_hours` = 3-4 (autonomous waves can be lower; operator-attended waves tend to land at 3)

## Wave-shape recommendations

Three wave shapes cover most Core 30 runs:

### Research wave (3-6 hours each; can decompose into 2-3 sub-waves if total >6h)

- Service briefs (Tier-1)
- City briefs (Tier-2)
- Intersection briefs (Tier-3)
- Client-fact brief

Decompose by tier or by batch when the full set exceeds ~6 hours. Example: at Core 30 with 3 services + 9 cities + 30 intersections, the math is `(3×25) + (9×20) + (30×15) + 30 = 735 min ≈ 12h`, which decomposes into ~3 research waves (e.g., wave-A1 services-and-half-cities + wave-A2 rest-of-cities-and-15-intersections + wave-A3 final-15-intersections).

### Scaffold wave (1-2 hours)

- Data file authoring (client + services + cities)
- WP auth verification
- Bulk scaffold all pages
- Imagery prompts per page

Single wave for most Core 30 runs.

### Publish waves (2-3 hours each per 5 pages; operator-attended)

- Higgsfield variant pick
- Wire + publish + indexing

Decompose by page batches of 5 for operator-attention budgets. Core 30 = 6 publish waves of 5 pages each.

## How this table updates

When real-use data lands:

1. Capture actual minutes for each artifact type in the run's execution log
2. After 3+ real runs of the same artifact type, update the table's median estimate
3. Tune the quality-loop overhead multiplier (`+15%`) based on the verdict distribution

Maintain the calibration history below.

## Calibration history

| Date | Author | Change | Trigger |
|---|---|---|---|
| 2026-06-02 | v1.1 ship | Initial table from v1.0 SKILL.md language + EV / S&H first-run data | v1.1 rewrite |
| (next) | TBD | TBD | After 3+ real Core 30 runs land |

## Related

- [[SKILL]] — the orchestrator skill that reads this table
- [[state-schema]] — the `planned_remaining_waves` field uses `estimated_hours` per wave
- [[../../second-brain/05_shared-intelligence/patterns/pattern-orchestrator-multi-chat-decomposition|orchestrator multi-chat pattern]] — the architectural rationale
