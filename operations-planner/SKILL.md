---
name: operations-planner
version: 0.1.0
status: active
created: 2026-06-14
updated: 2026-06-14
description: Walks the handoff tree, builds the reverse-dependency graph, computes gate-opening leverage scores, and emits an ordered operations plan. The "chief of operations" brain.
triggers:
  - operator asks "what should I spawn next based on leverage"
  - operator asks "run the operations planner"
  - operator asks "show me the dependency graph"
  - operator asks "what unblocks the most work"
  - scheduled invocation from [OP-3] (future)
composes-with:
  - prioritization (scoring contract + profile shape — reimplemented inline, not invoked at runtime)
  - vault-orchestrator (reads edit-zone conflict tables from cluster _READMEs — not invoked at runtime)
  - multi-chat-coordination (blocker-cleared logic reimplemented as set-membership test — not invoked at runtime)
tags: [skill, operations-planner, leverage, reverse-dependency, compose-dont-duplicate]
---

# `operations-planner` skill v0.1.0

The planning brain of the chief-of-operations system. Reads every handoff in the
tree, inverts their `depends-on` edges into a reverse-dependency graph, and scores
each spawnable handoff by **gate-opening leverage** — how many downstream handoffs
it unblocks (directly + transitively), weighted by depth decay.

## Purpose

Many handoffs sit in Ready-to-spawn, but not all are equal. This skill answers:
"which handoff, if shipped now, would unblock the most downstream work?" That's
the gate-opening leverage signal — the one thing the existing skills don't compute.

## What it produces

An `operations_plan` object (JSON + human-readable markdown) containing:

- `ready_now[]` — handoffs with all dependencies resolved to `done`
- `ordered_ready_to_spawn[]` — ready handoffs ranked by weighted leverage score
- `parallel_sets[]` — groups of ready handoffs safe to run concurrently
- `waiting_on{}` — handoffs blocked on upstream dependencies, with blocker labels
- `critical_path[]` — the longest dependency chain in the graph
- `cluster_next_up{}` — the ★ top-ranked handoff per cluster
- `in_flight[]` — currently active handoffs
- `session_budget_hours` — total estimated hours across all ready items
- `fatigue_flag` — true if session budget exceeds 40h
- Warnings: cycles, unmapped statuses, unresolved dependencies

## How to run

```bash
python3 ~/workspace/skills/operations-planner/analyze.py [--verbose]
```

Output lands in `skills/operations-planner/runs/op-plan-YYYY-MM-DD.json` and `.md`.

## Composition contract (honest scoping)

This skill **composes** three existing skills at the **contract level** (same
profile shape, same status normalization, same edit-zone severity model) but
**not at the runtime level** (no cross-process calls in v0.1). This is the right
trade-off for a v1 analyzer — runtime composition becomes real when [OP-3] wires
the scheduled loop.

### prioritization

`analyze.py` reimplements weighted-sum scoring inline. The profile at
`references/operations-planner-profile.md` follows the exact prioritization skill
profile spec so a future caller could hand it to the prioritization skill.

Criteria: `gate_opening_leverage` (0.40), `effort_hours` (0.20),
`reuse_multiplier` (0.15), `operator_priority` (0.25).

### vault-orchestrator

`analyze.py` reads edit-zone conflict tables from each cluster's `_README.md`
(the markdown tables under `## Edit-zone conflicts`). It parses pre-authored human
judgments for severity (serial-required, parallel-OK, etc.). Where a cluster
`_README` has no edit-zone table, parallel grouping defaults to "parallel-safe."

### multi-chat-coordination

`analyze.py` reimplements the blocker-cleared check as a simple set-membership
test: is every `depends_on` in the `done` column? This is NOT the full six-factor
evaluation from NEXT-MOVE mode. Calendar-gate, cognitive-load, file-collision, and
operator-priority factors are out of scope for v0.1.

## Leverage formula

```
leverage_score(node) = sum(1 / (1 + depth) for each transitive downstream node)
```

- Depth 0 (direct unblock): weight 1.0
- Depth 1 (one hop away): weight 0.5
- Depth 2: weight 0.33
- And so on — diminishing returns for distant downstream nodes

## Status normalization

See `references/status-normalization-map.md` for the full mapping from raw
`status:` values to the four canonical columns (`done`, `in_flight`, `next`,
`queued`). The tracker's Active/in-flight section **overrides** frontmatter for
non-done statuses — the tracker is the canonical runtime state.

## What this skill does NOT do

- It does not edit handoff files or the tracker (read-only analysis)
- It does not invoke skills as sub-agents (v0.1 is self-contained)
- It does not render a kanban board (that's [OP-2])
- It does not run on a schedule (that's [OP-3])
- It does not add `unblocks:` or `spawn-gates:` frontmatter (out of scope)
- It does not make judgment calls about what to spawn (it ranks; the operator picks)

## Related

- `[[operations-planner/_README|operations-planner cluster README]]`
- `[[reference-operations-data-contract|data contract]]`
- `[[prototype-kanban-mission-control.html|kanban prototype]]`
- `skills/prioritization/SKILL.md` — scoring contract shape
- `skills/vault-orchestrator/SKILL.md` — edit-zone conflict tables
- `skills/multi-chat-coordination/SKILL.md` — blocker-cleared logic
