---
type: profile
status: active
created: 2026-06-14
updated: 2026-06-14
skill: prioritization
profile-name: operations-planner
scoring-mode: weighted-sum
tags: [profile, prioritization, operations-planner, leverage]
---

# Prioritization profile: operations-planner

Weighted-sum profile for ranking spawnable handoffs by gate-opening leverage
plus effort, reuse, and operator priority. Designed for the operations-planner
skill's `ordered_ready_to_spawn[]` output.

## Scoring mode

`weighted-sum`

## Criteria

| Name | Label | Weight | Direction | Values | Description |
|---|---|---|---|---|---|
| `gate_opening_leverage` | Gate-opening leverage | 0.40 | higher-is-better | 0.0–∞ (continuous) | Transitive unblocks count, depth-decayed. A node that opens five gated handoffs outranks an equal-effort node that opens none. Computed by `analyze.py` as `sum(1 / (1 + depth))` over all transitive downstream nodes. |
| `effort_hours` | Estimated effort | 0.20 | lower-is-better | 0.5–20.0 (continuous) | Midpoint of the handoff's "Estimated effort" range. Lower effort = can ship sooner = unblocks downstream sooner. Missing values default to 4.0 (median). |
| `reuse_multiplier` | Reuse multiplier | 0.15 | higher-is-better | 1–5 (discrete) | How many future projects/clients/skills this deliverable feeds. 1 = single-use, 5 = foundational infrastructure reused everywhere. Inferred from tags and handoff body heuristics. |
| `operator_priority` | Operator priority | 0.25 | higher-is-better | 1–5 (discrete) | Match against MEMORY.md `project_priority_*` entries and recent strategic signals. 5 = explicit operator top priority, 1 = no signal. |

Weights sum to 1.00.

## Default constraints

Dependencies are enforced via topological sort after scoring, per the
prioritization skill's Step 4 contract. Circular dependencies are surfaced
as errors.

## Domain context

Items are handoff files from `second-brain/_meta/handoffs/`. Each item's
`id` is its `[TAG]` bracket (e.g., `OP-1`, `WF-7`, `DI-1`). Attributes
are parsed from handoff frontmatter and body sections.
