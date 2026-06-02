# RESUME — decomposition diagram text rendering

Mode 5 renders the project's wave dependency graph as indented ASCII. This reference defines the markers, the indentation rules, the cycle-detection check, and the rendering algorithm.

## Status markers

Each wave node in the diagram gets a status marker derived from `state_file.waves[<wave_id>].status` (or `planned_remaining_waves[]` for un-started waves):

| Marker | Status | Source |
|---|---|---|
| `[✓]` | closed | `waves[<wave_id>].status: closed` or `closed-with-spawned-blockers` |
| `[~]` | in-progress | `waves[<wave_id>].status: in-progress` |
| `[•]` | ready | wave is in `planned_remaining_waves[]` AND all `blocks_on[]` deps are closed-or-cleared |
| `[✗]` | blocked | wave is in `planned_remaining_waves[]` AND at least one `blocks_on[]` dep is un-closed |
| `[!]` | superseded | `waves[<wave_id>].status: superseded` — wave was closed-as-superseded by a strategic decision |

The marker comes first; the wave_id + scope summary follows.

## Indentation + edge rules

Waves with dependencies indent under their dependency, connected by `↓` (down-arrow). Linear chains render as a single column:

```
[✓] wave-A — scope A
     ↓
[•] wave-B — scope B
     ↓
[•] wave-C — scope C
```

Fan-outs (one wave blocks multiple downstream waves) render with branching arrows:

```
[✓] wave-A — scope A
     ↓
     ├──→ [•] wave-B1 — scope B1
     ├──→ [•] wave-B2 — scope B2
     └──→ [•] wave-B3 — scope B3
```

Joins (one wave waits on multiple upstreams) render with converging arrows from each upstream:

```
[✓] wave-A1 ──┐
              ↓
[✓] wave-A2 ──┼──→ [•] wave-B — scope B
              ↓
[✓] wave-A3 ──┘
```

For deeply nested graphs (>5 levels), Mode 5 keeps the column-of-arrows shape and adds a short legend at the bottom rather than fighting the ASCII rendering.

## Algorithm (high level)

1. Build a wave node list from `state_file.waves[]` (closed + in-progress waves) plus `state_file.planned_remaining_waves[]` (pending waves).
2. Build edge list from each wave's `blocks_on[]` array (edges point from blocker to blocked).
3. Run cycle detection (see next section).
4. Topologically sort the node list. Ties broken by `wave_id` lexical order.
5. Walk the sorted list. For each wave, render the marker + summary line, then render `↓` if the next wave depends on it (linear) OR render branching `├──→` / `└──→` if multiple downstreams depend on it.
6. Render the diagram in a fenced code block (so the markers + arrows preserve in markdown).

The full algorithm is straightforward; Mode 5's job at runtime is to produce the rendering, not to implement a graph library. For >10 waves, falling back to a "wave_id → dependencies" table is acceptable per the legibility-over-prettiness rule.

## Cycle detection

Waves should never have circular dependencies. But if they do (operator hand-edited `planned_remaining_waves[].blocks_on` and introduced a cycle, or a state file got corrupted), Mode 5 catches it at read-time rather than spawn-time.

**Detection.** Run a standard depth-first-search cycle detection on the wave graph. If any back-edge is found (a child node pointing to an ancestor in the DFS path), record the offending edge.

**Output on cycle.** Render the diagram preceded by a banner:

```
⚠️ CIRCULAR DEPENDENCY DETECTED in wave graph

The following waves form a cycle:
- wave-X depends on wave-Y
- wave-Y depends on wave-X

This is almost certainly an operator hand-edit mistake or state-file corruption.
Mode 5 recommends: edit `planned_remaining_waves[].blocks_on` to remove the cycle
before resuming any wave. The diagram below shows the graph as-is — affected waves
flagged.
```

Then render the diagram normally with affected waves additionally tagged `⚠️` after their marker:

```
[•]⚠️ wave-X — scope X (cycle with wave-Y)
     ↓
[•]⚠️ wave-Y — scope Y (cycle with wave-X)
```

Cycle detection runs even on graphs with zero cycles — it's cheap, and the absence of the warning banner is itself the signal that the graph is well-formed.

## Legend (rendered with every diagram)

The diagram always renders with a one-line legend below the code fence so the operator doesn't have to remember marker semantics:

```
Legend: [✓] closed · [~] in-progress · [•] ready · [✗] blocked · [!] superseded · ⚠️ cycle
```

## Worked examples

### Linear chain (S&H wave structure as of 2026-06-02)

After Mode 5 reads S&H state + applies stale-state reconciliations (both blockers cleared), the diagram renders:

```
S&H Contracting wave decomposition (post-reconciliation):

[✓] wave-A1 — emergency-electrician service brief + spot-check
     ↓
[•] wave-A2 — ev-charger + light-fixture service briefs (1.5h)
     ↓
[•] wave-A3 — Woodbridge + Lake Ridge + Dale City city briefs (1.5h)
     ↓
[•] wave-A4 — Manassas + Lorton + Springfield city briefs (1.5h)
     ↓
[•] wave-A5 — Burke + Alexandria + Stafford city briefs (1.5h)
     ↓
[•] wave-A6 — 4 Woodbridge intersection briefs (1.5h)

Legend: [✓] closed · [~] in-progress · [•] ready · [✗] blocked · [!] superseded · ⚠️ cycle
```

If Mode 5 had NOT applied the reconciliations (operator confirms "no, state file is correct"), wave A2 would render as `[✗]` with the blocker name parenthesized.

### Fan-out + join (hypothetical EV pages 06-12 PROVISION decomposition)

When PROVISION fires for EV pages 06-12 and produces 6-8 sub-chats (4 service briefs + 2 city briefs + scaffold + per-page publish waves), the diagram could render:

```
EV pages 06-12 wave decomposition (post-PROVISION):

[•] wave-svc-1 — service brief A ──┐
[•] wave-svc-2 — service brief B ──┤
[•] wave-svc-3 — service brief C ──┼──→ [✗] wave-scaffold — scaffold + build-order (blocked on svc + city briefs)
[•] wave-svc-4 — service brief D ──┤                            ↓
[•] wave-city-1 — city brief E   ──┤                           [✗] wave-publish — per-page publish waves
[•] wave-city-2 — city brief F   ──┘

Legend: [✓] closed · [~] in-progress · [•] ready · [✗] blocked · [!] superseded · ⚠️ cycle
```

The 6 brief waves are independent and parallel-safe; the scaffold wave joins on all 6; the publish wave is linear after scaffold. Mode 5 detects this shape from `blocks_on[]` arrays.

### Cycle case (defensive — should never fire in practice)

If `planned_remaining_waves` somehow included `wave-X.blocks_on: [wave-Y]` AND `wave-Y.blocks_on: [wave-X]`:

```
⚠️ CIRCULAR DEPENDENCY DETECTED in wave graph

The following waves form a cycle:
- wave-X depends on wave-Y
- wave-Y depends on wave-X

This is almost certainly an operator hand-edit mistake or state-file corruption.
Mode 5 recommends: edit `planned_remaining_waves[].blocks_on` to remove the cycle
before resuming any wave. The diagram below shows the graph as-is — affected waves
flagged.

[•]⚠️ wave-X — scope X (cycle with wave-Y)
     ↓
[•]⚠️ wave-Y — scope Y (cycle with wave-X)

Legend: [✓] closed · [~] in-progress · [•] ready · [✗] blocked · [!] superseded · ⚠️ cycle
```

The defensive surface gives the operator a clear repair path rather than spawning chats that block on themselves.

## Fallback for >10 waves

If the project has >10 waves, the ASCII diagram becomes hard to read. Mode 5 falls back to a table:

```
| Wave | Status | Scope | Blocks on |
|---|---|---|---|
| wave-A1 | [✓] closed | emergency-electrician brief | (none) |
| wave-A2 | [•] ready | ev-charger + light-fixture briefs | (A1) |
| wave-A3 | [•] ready | Woodbridge + Lake Ridge + Dale City briefs | (A2) |
| ... | ... | ... | ... |
```

The table preserves all the information; the visual graph isn't worth losing legibility for. Mode 5 picks the rendering at runtime — diagram for ≤10 waves, table above.

## Related

- [[SKILL]] § "Mode 5 — RESUME" Step 7 (compute wave graph)
- [[resume-output-shape]] § "Section 4 — Decomposition diagram"
- [[resume-input-sources]] § "State file" — where `planned_remaining_waves[].blocks_on` comes from
- [[../../multi-chat-coordination/SKILL|multi-chat-coordination SKILL]] § "DECOMPOSE Step 3" — the dependency-graph text shape this mirrors
