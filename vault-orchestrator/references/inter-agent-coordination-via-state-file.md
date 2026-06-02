# Inter-agent coordination via the state file

How Mode 6's sub-agents coordinate with the orchestrator and (when truly parallel) with each other, using the project state file as the only coordination primitive. No IPC, no signal handlers, no shared memory. See lesson D-02 for the precipitating decision.

This reference applies most directly to the true-parallel substrate (Claude Code Task tool). The Cowork sequential one-shot substrate doesn't need polling — the Agent call blocks until return — but the per-key write isolation rules apply there too (the orchestrator writes between calls; the rules below describe which keys belong to which actor).

## Why the state file (and not something else)

`04_projects/clients/_active/<slug>/_state/onboarding.json` is already the source-of-truth contract for `client-seo-onboarding` v1.1. Sub-agents owe the orchestrator a per-artifact verdict + confidence + iteration count; the state file already has the `quality_log` field for exactly that. Reusing the existing contract surface means zero new schema work + zero new file types.

Compare alternatives that the build rejected:

| Alternative | Why rejected |
|---|---|
| Shared in-memory queue | No infrastructure today; would require a vault-side daemon. |
| Message-passing / IPC | Same. Also: cross-substrate hostile (Cowork sandbox vs. Mac terminal). |
| Per-sub-agent log files | Adds N new files per wave; harder to query; doesn't compose with the existing `quality_log` aggregation in `client-seo-onboarding` resume contract. |
| Database with transactions | Way more contract surface than the problem needs. |

The state file wins on contract simplicity + zero new surface. Trade-off: polling is inefficient compared to push notifications, but at single-digit sub-agent fanout the inefficiency is invisible.

## Per-key write isolation

Each actor owns a deterministic set of state-file keys. Concurrent writes never collide because no two actors write the same key at the same time.

| Actor | Owns these keys (write) | Reads (read-only) |
|---|---|---|
| Orchestrator (Mode 6) | `current_wave`, `waves[<wave-id>].status`, `waves[<wave-id>].started_at`, `waves[<wave-id>].closed_at`, `wave_log[]` (append at wave-close), `planned_remaining_waves` (edit at wave-close), `blocked_on` (edit at wave-close), `operator_gates_pending[]` (if used) | Everything else |
| Sub-agent (per-artifact) | `quality_log[<step>][<artifact-name>]` (one entry per iteration), `waves[<wave-id>].outputs` (append on PASS at threshold), `failures[]` (append on catastrophic stop) | Everything else |
| Operator (manual edit) | Anything per `state-schema.md` § "Manual operator overrides" — typically `blocked_on`, `planned_remaining_waves`, `quality_log[<step>][<artifact-name>].decision` overrides | n/a |

`quality_log` is keyed by `(step, artifact-name)` pairs. Artifact names are globally unique within a wave (each sub-agent has a unique artifact path). Concurrent sub-agents writing different `(step, artifact-name)` keys never collide. `waves[<wave-id>].outputs` is append-only; append operations from different sub-agents don't overwrite each other.

The orchestrator does not write `quality_log` keys directly. The sub-agent's contract says it writes its own iteration entries. The orchestrator reads `quality_log` at every poll to determine sub-agent status.

## Append-only conventions

Two state-file arrays are append-only:

- `waves[<wave-id>].outputs` — sub-agents append the artifact path on PASS at threshold.
- `wave_log[]` — orchestrator appends one entry at wave-close.

Append-only means: never delete, never reorder, never edit existing entries. Append-only arrays are concurrency-safe by construction (last writer wins on the append, both entries persist).

`failures[]` is also append-only in practice (sub-agents append on catastrophic stop; the orchestrator may flip an entry's `operator_action` field but doesn't remove rows).

## Polling cadence (parallel substrate only)

When the orchestrator is on a true-parallel substrate (Claude Code Task tool), it polls the state file at a configurable cadence. Default 10 seconds.

Polling cycle:

```
1. Sleep for <polling-cadence-seconds>.
2. Read the state file.
3. For each in-flight sub-agent:
   a. Check quality_log[<step>][<artifact-name>] for a new iteration entry since last poll.
   b. If verdict == PASS at threshold → mark sub-agent done in dispatch log.
   c. If verdict == ESCALATED → check operator-gate file for a new row; pause that sub-agent.
   d. If verdict == FAIL after 3 iterations → escalate via gate file.
   e. If sub-agent hasn't written anything since last poll AND has been silent for > <silence-threshold> → mark stalled + investigate.
4. If all sub-agents in the wave have status == done OR escalated:
   → run wave-close protocol (write waves[<wave-id>].status: closed, append wave_log entry, clear current_wave).
5. Else loop back to step 1.
```

Polling is cheap (one file read per cycle). The state file is small (single-digit KB typically). 10s default fits comfortably in a Claude Code session timeout.

### Polling cadence flags

- `--polling-cadence Ns` (default `10s`) — interval between polls.
- `--silence-threshold Ns` (default `300s` = 5 min) — flag a sub-agent as stalled if no `quality_log` entry lands in this window.
- `--max-poll-iterations N` (default `360` = 1 hour at 10s cadence) — stop polling and escalate if no sub-agent completes within this window.

## Sequential dispatch coordination (Cowork substrate)

When the substrate is Cowork Agent tool (one-shot sub-agents), no polling is needed. The orchestrator:

1. Dispatches sub-agent A via a single Agent call.
2. Blocks until the call returns with sub-agent A's structured response.
3. Reads sub-agent A's response. Writes the corresponding `quality_log[<step>][<artifact-name>]` key + appends `waves[<wave-id>].outputs` if PASS at threshold.
4. Dispatches sub-agent B via the next Agent call.
5. Repeats until all sub-agents in the wave have run.
6. Runs wave-close protocol.

The state-file writes happen between calls. Per-key isolation still applies (the orchestrator only writes `quality_log` keys for the sub-agent that just returned; it doesn't touch other sub-agents' keys).

The wave's parallel-OK-with-note conflict-flag status is informational on Cowork — the orchestrator records the parallelism intent in the dispatch log + names the substrate constraint, but executes sequentially.

## Concurrent-write risks + mitigations

| Risk | Mitigation |
|---|---|
| Two sub-agents both writing `failures[]` (append) at the same instant | Append is concurrency-safe; both entries land. |
| A sub-agent writes `quality_log[<step>][<artifact-name>]` while the orchestrator reads | Read sees either pre-write or post-write state; never partial. JSON.parse on partial content would throw → orchestrator catches + retries on next poll. |
| Two sub-agents accidentally write the same `quality_log[<step>][<artifact-name>]` key (e.g., sub-agent IDs collide) | Sub-agent IDs MUST be artifact-path-derived, not random. Collision is a contract violation; the orchestrator detects + escalates. |
| Operator manually edits the state file mid-run | The orchestrator reads on every poll; an operator edit appears on the next poll cycle and may resolve a gate or change `planned_remaining_waves`. Manual edits are first-class per `state-schema.md` § "Manual operator overrides." |
| State file corruption (malformed JSON from a botched write) | Each write happens via read-modify-write with a pre-write JSON.parse validation. If a sub-agent's intended write would corrupt the file, the sub-agent stops + escalates via the gate file. The orchestrator periodically (every 10 polls) verifies the file parses cleanly + escalates if not. |

## Worked example — 2 sub-agents writing 2 briefs (parallel substrate)

S&H wave A2: ev-charger-installation brief + light-fixture-installation brief. Both target the services folder; no edit-zone conflict (different artifact paths).

```
T=0s:   Orchestrator detects Claude Code Task tool substrate.
T=0s:   Orchestrator writes current_wave: "wave-A2", waves["wave-A2"].status: "in-progress".
T=0s:   Orchestrator dispatches sub-agent ev-charger via Task call.
T=0s:   Orchestrator dispatches sub-agent light-fixture via Task call (same message).
T=0s:   Both sub-agents start executing.
T=10s:  Orchestrator polls state file. quality_log["step-2"] is empty. No status change.
T=20s:  Orchestrator polls. Still no entries.
...
T=45m:  ev-charger sub-agent finishes iteration 1 of Mode 1 EVALUATE. Verdict: NEEDS REVISION minor. Writes quality_log["step-2"]["ev-charger-installation"] = {iteration: 1, verdict: "NEEDS REVISION (minor)", confidence: 80, ...}.
T=45m:  Orchestrator polls. Sees the new entry. Logs in dispatch log. Sub-agent enters Mode 4 auto-elevate.
T=50m:  light-fixture sub-agent finishes iteration 1. Verdict: PASS. Writes quality_log["step-2"]["light-fixture-installation"] = {iteration: 1, verdict: "PASS", confidence: 87, ...} + appends waves["wave-A2"].outputs.
T=50m:  Orchestrator polls. Sees light-fixture PASS at threshold. Marks sub-agent done.
T=55m:  ev-charger sub-agent finishes iteration 2. Verdict: PASS. Writes quality_log["step-2"]["ev-charger-installation"] = {iteration: 2, verdict: "PASS", confidence: 88, ...} + appends waves["wave-A2"].outputs.
T=55m:  Orchestrator polls. Both sub-agents done. Runs wave-close protocol.
T=55m:  Orchestrator writes waves["wave-A2"].status: "closed", closed_at, appends wave_log entry, clears current_wave.
T=55m:  Wave A2 closed. Total wall-clock: ~55 minutes (limited by the slower sub-agent).
```

The same wave on Cowork substrate would take ~1h45m (45 min ev-charger sequential + 50 min wait + ~10 min coordination overhead) — the operator-visible difference between substrates lesson D-07 names.

## Worked example — operator gate firing mid-dispatch

ev-charger sub-agent hits a 3-iter quality stall. Writes `quality_log["step-2"]["ev-charger-installation"] = {iteration: 3, verdict: "FAIL", confidence: 65}` + writes a row to `_pending-operator-decisions.md`. Returns `verdict: ESCALATED`.

Orchestrator polls. Sees the FAIL verdict + the gate row. Marks ev-charger sub-agent paused (NOT failed — escalation is recoverable). Continues to poll for other sub-agents (e.g., light-fixture). When the operator responds to the gate file row, the orchestrator reads the response + decides whether to re-dispatch ev-charger (with operator-supplied context) or to close the wave with ev-charger marked stalled in `wave_log`.

The state file's `failures[]` does NOT get an entry on escalation. Per `state-schema.md` § "failures vs quality_log semantic distinction" — quality-loop verdict transitions go in `quality_log`; catastrophic stops (sub-skill error, contract violation, malformed return) go in `failures`. An escalation is the former.

## See also

- [[../SKILL|vault-orchestrator SKILL.md]] § "Mode 6 — EXECUTE" — the dispatch entry point
- [[sub-agent-dispatch-contract]] — what each sub-agent sees + how it writes
- [[operator-gate-routing]] — how escalations surface to the operator
- [[parallel-safe-coordination]] — how Mode 6 decides if sub-agents CAN run in parallel
- `~/workspace/skills/client-seo-onboarding/state-schema.md` — the state file's canonical schema; `quality_log` + `waves` + `wave_log` + `failures` shapes live there
- `~/workspace/skills/client-seo-onboarding/state-schema.md` § "failures vs quality_log — semantic distinction" — the rule for which array a sub-agent writes to
