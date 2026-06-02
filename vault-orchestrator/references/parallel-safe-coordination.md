# Parallel-safe coordination — reusing Phase 4 edit-zone conflict detection

How Mode 6 decides whether sub-agents can run in parallel (true-parallel substrate) or must serialize (any substrate where two sub-agents would race on a shared file). The decision logic is Phase 4's edit-zone conflict detection, applied to the sub-agent set instead of the handoff set. See lesson D-04 for the precipitating decision.

## What gets compared

Phase 4's [[edit-zone-conflict-detection|detector]] takes a list of handoffs with declared `## Files to edit` + `## Files to create` sections and produces a conflict-flag table. Mode 6 reuses the same detector with a smaller input shape — each sub-agent declares an edit-zone instead of a handoff body, and the detector operates on the sub-agent set.

### Sub-agent edit-zone declaration

When the orchestrator builds the dispatch plan, it computes each sub-agent's edit-zone as:

- **The artifact path** the sub-agent will write (one path per sub-agent — the per-artifact contract).
- **The state-file `quality_log` key** the sub-agent will write to (`quality_log[<step>][<artifact-name>]`).
- **The state-file append-only arrays** the sub-agent may append to (`waves[<wave-id>].outputs`, `failures[]`).
- **Any reference files** the sub-agent will update inline (rare — most sub-agents only write the artifact + state file).

For most sub-agents the edit-zone is exactly two writes: the artifact + the corresponding `quality_log` key.

### Detector input shape

Mode 6 hands the detector a list shaped like:

```yaml
sub_agents:
  - id: sub-agent-ev-charger-installation
    edit_zone:
      writes:
        - 05_shared-intelligence/research-briefs/services/ev-charger-installation.md
      state_keys:
        - quality_log.step-2.ev-charger-installation
      append_only:
        - waves.wave-A2.outputs
        - failures
  - id: sub-agent-light-fixture-installation
    edit_zone:
      writes:
        - 05_shared-intelligence/research-briefs/services/light-fixture-installation.md
      state_keys:
        - quality_log.step-2.light-fixture-installation
      append_only:
        - waves.wave-A2.outputs
        - failures
```

The detector compares pairwise + emits the same four severity levels Phase 4 produces:

| Severity | Trigger condition for sub-agents | Dispatch action |
|---|---|---|
| **serial-required** | Two sub-agents both write the same artifact path OR the same `quality_log` key | Reject the dispatch plan; surface to operator. (Shouldn't happen — sub-agent IDs are artifact-path-derived; collision is a contract violation per [[sub-agent-dispatch-contract]].) |
| **parallel-OK-with-note** | Sub-agents write different artifacts + different `quality_log` keys, but both append to the same `waves[<wave-id>].outputs` array | Dispatch in parallel (append is concurrency-safe by construction); surface the parallel-append intent in the dispatch plan for audit. |
| **warning-only** | Sub-agents both touch the same reference file inline (rare) | Dispatch in parallel; sub-agents must use idempotent appends (the detector flags this for operator awareness). |
| **self-conflict** | A sub-agent's edit-zone names a path the orchestrator owns (e.g., `current_wave`, `planned_remaining_waves`) | Reject the dispatch plan; the sub-agent's contract is malformed; surface to operator. |

The detector errs toward **serial-required** when ambiguous, same as Phase 4. Better a false positive (operator overrides to parallel) than a silent race.

## What changes from Phase 4 detector usage

| Phase 4 input | Mode 6 input | Difference |
|---|---|---|
| Handoff `## Files to edit` + `## Files to create` sections | Sub-agent `edit_zone.writes` + `edit_zone.state_keys` | Per-artifact granularity; smaller surface |
| Section qualifiers ("edit the 'Ready to spawn' section") | State-key qualifiers (`quality_log.<step>.<artifact-name>`) | Keys are inherently scoped; no section parsing needed |
| Conflict flag table in `_spawn-queue.md` | Conflict-flag column in the dispatch plan | Dispatch plan is the audit trail (Mode 6 doesn't write to `_spawn-queue.md`) |
| Operator approval at the review gate | No separate review gate — dispatch plan IS the proposal | Operator confirms the dispatch plan; conflict flags are part of the confirmation surface |

The detection algorithm is otherwise identical — the same severity-scoring + resolution-path logic Phase 4 ships.

## Substrate interaction

The detector's output applies the same way across substrates, but the actual execution differs:

- **Cowork sequential substrate:** the detector's `parallel-OK-with-note` verdict is informational. The dispatch plan records the parallelism intent + names the substrate constraint, but execution serializes per [[sub-agent-dispatch-contract]] § "Substrate matrix." Operator sees "parallel-OK but Cowork serializes" in the dispatch plan.
- **Claude Code Task tool substrate:** the detector's verdict drives the actual dispatch. `parallel-OK-with-note` sub-agents fire concurrently via multiple Task calls in one message. `serial-required` sub-agents fire in order (one Task call per message, blocking until return).
- **Hermes-harness substrate (future):** same as Claude Code Task tool for parallelism semantics; Hermes adds push-driven coordination on top.

## When `serial-required` fires within Mode 6

If two sub-agents collide on the same artifact path (the contract-violation case named above), Mode 6 does NOT silently serialize and proceed. The collision means the dispatch plan is malformed — two sub-agents shouldn't be producing the same artifact. The orchestrator stops + surfaces the contract violation to the operator + names the resolution (split the wave so each artifact has one sub-agent; OR fix the dispatch plan's sub-agent slug computation).

This differs from Phase 4 where `serial-required` is a normal output (operator serializes via queue order). At sub-agent granularity, `serial-required` is almost always a bug.

## When `parallel-OK-with-note` fires within Mode 6

This is the common case for a multi-artifact wave (e.g., S&H wave A2's 2 service briefs). Both sub-agents write disjoint artifacts + disjoint `quality_log` keys; both append to the same `waves.<wave-id>.outputs` (which is concurrency-safe).

The "note" in the dispatch plan surfaces the parallel-append for operator awareness. On Claude Code Task tool the orchestrator fires both via one multi-call message. On Cowork the orchestrator serializes (substrate constraint) but records the parallel intent.

## When `warning-only` fires within Mode 6

Rare. Triggers when two sub-agents both update a shared reference inline (e.g., both adding a row to the same skill-local index file). The detector flags it; sub-agents must use idempotent appends; the orchestrator surfaces the shared touch in the dispatch plan.

If this becomes common, the detector's pattern table needs a Mode 6 addition for the new shared-touch surface. Track in Mode 6's maintenance notes (skill-level note 16 or higher).

## What the detector does NOT do (same as Phase 4)

- It does not run live diffs against current file content. Conflicts are predicted from sub-agent edit-zone declarations, not from speculative diff resolution.
- It does not block any dispatch. The operator always sees the conflict flag + decides whether to override.
- It does not detect conflicts within a single sub-agent's own writes.
- It does not detect semantic conflicts (two sub-agents writing different artifacts that are nonetheless contradictory — e.g., two service briefs that take incompatible positions on a shared question). That's a [[../SKILL|Mode 6]] decision-research call when surfaced, or an operator review at wave-close.
- It does not track tier-3 vault files (Cowork can't read tier-3, and tier-3 writes are operator-driven by definition).

## Worked example — 2 service briefs (parallel-OK-with-note)

S&H wave A2 dispatches two sub-agents:

- sub-agent-ev-charger-installation → `05_shared-intelligence/research-briefs/services/ev-charger-installation.md`
- sub-agent-light-fixture-installation → `05_shared-intelligence/research-briefs/services/light-fixture-installation.md`

Both write to `waves.wave-A2.outputs` (append-only).

Detector output:

| Pair | Shared path | Severity | Resolution |
|---|---|---|---|
| ev-charger / light-fixture | `state.waves.wave-A2.outputs` (append-only) | parallel-OK-with-note | Dispatch in parallel; both appends are concurrency-safe; sub-agents own disjoint quality_log keys + disjoint artifact paths. |

On Claude Code Task tool: both fire concurrently in one message.

On Cowork Agent tool: they serialize (substrate constraint). The dispatch plan names: "Substrate is Cowork; parallel-OK-with-note conflicts execute sequentially. Estimated wall-clock: ~3-4h (vs. ~1.5-2h on Claude Code Task tool)."

## Worked example — sub-agent that mutates a reference file (warning-only)

A future sub-agent type might both produce an artifact AND update a shared index file (e.g., `05_shared-intelligence/research-briefs/services/_index.md` listing all service briefs). If wave A2's two sub-agents both want to add their row to this index, the detector emits:

| Pair | Shared path | Severity | Resolution |
|---|---|---|---|
| ev-charger / light-fixture | `05_shared-intelligence/research-briefs/services/_index.md` | warning-only | Sub-agents use idempotent appends (read index → append row only if absent → write); dispatch in parallel; the index file may briefly have both rows interleaved but both lands cleanly. |

The contract requires idempotent appends in the sub-agent prompt for any `warning-only` shared file.

## What happens if the detector misses a real conflict (false negative)

False negatives are not silent — they surface at execution time as either:

- A state-file write that fails (orchestrator sees stale content; retries on next poll).
- An artifact file with malformed content (Mode 1 evaluate fails the artifact).
- A wave-close that can't proceed (the orchestrator surfaces "unable to close wave because: <reason>").

Each of these escalates via the gate file. The operator resolves; the detector's pattern table gets a maintenance update (Mode 6 maintenance note for shared-file pattern drift).

## See also

- [[../SKILL|vault-orchestrator SKILL.md]] § "Mode 6 — EXECUTE" — the dispatch entry point that calls this detector
- [[edit-zone-conflict-detection|Phase 4 edit-zone-conflict-detection]] — the canonical detector this reference reuses
- [[sub-agent-dispatch-contract]] — the per-sub-agent contract that names the edit-zone declaration
- [[inter-agent-coordination-via-state-file]] — the polling contract that resolves runtime conflicts the detector missed
- [[operator-gate-routing]] — the gate-file contract that surfaces runtime conflicts
- `~/workspace/skills/multi-chat-coordination/SKILL.md` — DECOMPOSE produces the original handoff bodies Phase 4's detector consumes
