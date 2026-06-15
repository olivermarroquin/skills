---
type: reference
status: active
created: 2026-06-14
updated: 2026-06-14
topic: operations-planner
tags: [reference, operations-planner, status-normalization]
---

# Status normalization map

Maps every known handoff `status:` value to one of the four canonical columns
defined in `reference-operations-data-contract.md`.

## Canonical columns

| Column | Meaning |
|---|---|
| `done` | Work has landed — no further action |
| `in_flight` | Work is actively being executed right now |
| `next` | Ready to spawn — all blockers cleared |
| `queued` | Waiting on upstream dependencies or external triggers |

## Normalization table

| Raw `status:` value | → Column | Notes |
|---|---|---|
| `consumed` | `done` | Standard completion status |
| `shipped` | `done` | Alias used in some older handoffs |
| `complete` | `done` | Alias |
| `promoted` | `done` | Artifact promoted to shared-intelligence |
| `locked` | `done` | Spec locked, no further edits |
| `staging-complete` | `done` | Deployed to staging, cutover pending (treat as done for dependency purposes) |
| `active` | context-dependent | See below |
| `open` | `in_flight` | Alias for active |
| `submitted` | `in_flight` | Awaiting review |
| `active-with-wf4` | `in_flight` | Active with a specific workflow dependency |
| `queued` | `queued` | Standard queued status |
| `draft` | `queued` | Draft handoff, not yet ready |
| `draft-for-build` | `queued` | Drafted but build not started |
| `stub` | `queued` | Placeholder handoff |
| `ready` | `next` | Explicitly marked ready |
| `ready-to-spawn` | `next` | Alias |
| `cancelled` | `done` | No longer relevant — treat as resolved for graph purposes |

## `active` mapping

`active` maps to `in_flight`. The handoff is live — someone is (or was) working
on it. The tracker may further refine this (e.g., if the tracker has the row in
Ready-to-spawn, the tracker override wins with `next`), but the default without
tracker info is `in_flight`, not `queued`. A node with `status: active` should
never appear in `ready_now` — it's already being worked.

## Unmapped statuses

Any `status:` value not in this table is surfaced in the operations plan output
under `unmapped_statuses[]` with the file path. The analyzer does NOT silently
bucket unknown statuses — it flags them for operator review.
