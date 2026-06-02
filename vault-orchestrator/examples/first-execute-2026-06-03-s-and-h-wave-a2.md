---
type: report
status: draft
created: 2026-06-03
updated: 2026-06-03
project: s-and-h-contracting
wave: wave-A2
mode: execute
skill: vault-orchestrator
skill-version: v1.2
substrate-documented-for: cowork-agent-tool
fire-status: paper-dispatch-no-live-fire
tags: [report, vault-orchestrator, execute, s-and-h-contracting, wave-a2, worked-example, first-real-run, paper-dispatch]
---

# EXECUTE DISPATCH PLAN — S&H Contracting (`s-and-h-contracting`) wave A2 — 2026-06-03

First real-use worked example of vault-orchestrator v1.2 Mode 6 EXECUTE. Run against the S&H wave A2 handoff (queued + promoted to Ready at v1.1 close 2026-06-02). This file documents the dispatch plan + per-sub-agent dispatch prompts THAT WOULD FIRE — it does NOT fire them per the kickoff DO NOT directive. Live dispatch happens during the actual S&H wave A2 run (which the operator may spawn manually via Cowork paste OR via Mode 6 EXECUTE composition from a future chat).

## Substrate label — explicit

**This worked example documents the dispatch plan for the Cowork Agent tool substrate.** Substrate detection probe trace:

- Probe 1 (Task tool availability): the live Mode 6 chat runs in a Cowork sandbox; Task tool is NOT in the runtime tool inventory; Probe 1 returns negative.
- Probe 2 (filesystem mount paths): working directory is `/sessions/<id>/mnt/workspace/`; matches the Cowork sandbox pattern. Probe 2 resolves: substrate = `cowork-agent-tool`.
- Probe 3 (Hermes-harness MCP): skipped — Probe 2 already resolved.

**On Cowork Agent tool substrate, sub-agents execute SEQUENTIALLY** even when the edit-zone conflict detector flags them as parallel-OK. This is the substrate constraint named in [[../references/sub-agent-dispatch-contract|sub-agent-dispatch-contract.md]] § "Substrate matrix" + lesson D-07. The dispatch plan below documents the PARALLEL INTENT (operator should see the conflict-flag table accurately) but the EXECUTION SHAPE for Cowork is sequential.

When this same wave runs from a Claude Code Task tool substrate (future possibility — operator may opt in), the dispatch plan stays identical; only the execution shape flips to parallel. The total wall-clock is the dominant operator-visible difference.

## Section 1 — Wave header

| Field | Value |
|---|---|
| Wave ID | `wave-A2` |
| Project slug | `s-and-h-contracting` |
| Source handoff | `~/workspace/second-brain/_meta/handoffs/handoff-2026-06-01-s-and-h-wave-a2-service-briefs.md` (status: queued → promoted to Ready at v1.1 close 2026-06-02 pass-85) |
| Substrate detected | `cowork-agent-tool` (Probe 2 resolved) |
| Execution shape | **sequential** (Cowork constraint; parallel intent documented but execution serializes) |
| Estimated wall-clock | ~1.5-2.5h sequential on Cowork (per the handoff body estimate); alt: ~45-60 min parallel on Claude Code Task tool |
| Estimated API cost | ~$0.30-$0.90 wave-total. **Always-fires per artifact:** $0.001-0.003 × 2 = $0.002-$0.006 (OpenAI + Gemini + Claude direct citation comparison on §4c). **Conditional per artifact (Sonar Mode 4 ceiling):** $0.30-$0.45 × 2 = $0.60-$0.90 (worst case 3 iterations). **Expected per the project's first-brief quality_log signal:** emergency-electrician landed NEEDS REVISION minor with 1 Mode 4 iteration at ~$0.06 → expect ~$0.06-$0.15 per artifact in practice → wave-expected ~$0.12-$0.30. Operator sees: floor $0.002-$0.006 (always); expected $0.12-$0.30 (per project signal); ceiling $0.60-$0.90 (worst case). |
| Sub-agent count | 2 |
| Parallel-safe per detector | 2 (both — see Section 3) |
| Serialized per detector | 0 |

## Section 2 — Sub-agent fan-out

Two sub-agents, one per Tier-1 service brief named in the wave A2 handoff scope. Slugs derive from the artifact path per the contract's collision-prevention rule.

| # | Sub-agent slug | Artifact path | Artifact type | Spec source | Est. minutes | Edit-zone declaration |
|---|---|---|---|---|---|---|
| 1 | `sub-agent-ev-charger-installation` | `05_shared-intelligence/research-briefs/services/ev-charger-installation.md` | Tier-1 service brief | `service-seo-research` skill spec + `research-briefs/services/_README.md` (template) + `output-quality-loop` Mode 1 routing for research-brief spec | 25 min produce + 5-10 min quality loop (per `per-artifact-sizing.md`) | writes: artifact path. state_keys: `quality_log.step-2.ev-charger-installation`. append_only: `waves.wave-A2.outputs`, `failures`. |
| 2 | `sub-agent-light-fixture-installation` | `05_shared-intelligence/research-briefs/services/light-fixture-installation.md` | Tier-1 service brief | same as #1 | 25 min produce + 5-10 min quality loop | writes: artifact path. state_keys: `quality_log.step-2.light-fixture-installation`. append_only: `waves.wave-A2.outputs`, `failures`. |

Both sub-agents implement the same four-substep quality loop contract from `client-seo-onboarding` v1.1 SKILL.md § "Per-step quality loop contract." Each produces ONE artifact end-to-end (Produce → Mode 1 EVALUATE → Mode 4 AUTO-RESEARCH if needed → Mode 5 AUTO-APPROVE-AND-ESCALATE).

## Section 3 — Conflict-flag table

Output of Phase 4 edit-zone conflict detector applied at sub-agent granularity per [[../references/parallel-safe-coordination|parallel-safe-coordination.md]]:

| Pair | Shared path | Severity | Resolution |
|---|---|---|---|
| ev-charger / light-fixture | `state.waves.wave-A2.outputs` (append-only) | parallel-OK-with-note | Both sub-agents append concurrency-safe; disjoint `quality_log` keys; disjoint artifact paths. On Claude Code Task tool: dispatch concurrently. **On Cowork Agent tool: dispatch sequentially per substrate constraint; the parallel-OK verdict is informational.** |
| ev-charger / light-fixture | `state.failures` (append-only) | parallel-OK-with-note | Same as above — append-only arrays are concurrency-safe by construction. |

No `serial-required` or `self-conflict` rows fire. The detector's verdict is clean.

## Section 4 — Polling cadence + operator-gate routing

| Field | Value |
|---|---|
| Operator-gate file path | `~/workspace/second-brain/04_projects/clients/_active/s-and-h-contracting/_pending-operator-decisions.md` |
| Gate file status | absent at dispatch start; orchestrator creates at Step 8 init |
| Polling cadence | N/A — Cowork sequential substrate doesn't poll; orchestrator reads sub-agent return value directly after each blocking Agent call |
| Sub-agent call ordering | sub-agent-ev-charger-installation → sub-agent-light-fixture-installation (alphabetical when no edit-zone-detector serialization required) |
| Gate types that may fire (per [[../references/operator-gate-routing|operator-gate-routing.md]]) | `quality-loop-3-iter-stall` (if a sub-agent stalls); `ambiguous-decision-archaeology` (rare on research briefs); `escalated-from-sub-skill` (Mode 5 hard-escalation from output-quality-loop) |
| Gate types that will NOT fire on this wave | `higgsfield-variant-pick` (no imagery work at wave A2); `schema-validation-failure` (no data file authoring); `external-write-confirm` (no WP REST API writes; no GSC submits; no git pushes — research briefs only) |

## Section 5 — Wave-close conditions

The orchestrator closes wave A2 when:

- Both sub-agents return `verdict: PASS at threshold` (PASS at confidence ≥ 85 per the per-step quality loop's brief-type threshold), OR
- All gate-file rows have non-pending operator responses (e.g., operator accepts a `light-escalate` on one brief; that brief still counts as wave-close-eligible).

On wave-close:

- Write `waves["wave-A2"].status: "closed"` + `closed_at: <ISO UTC>` to state file.
- Append `wave_log[]` entry with summary (which briefs landed at what verdicts), key_artifacts (both brief paths), spawned_handoffs (likely empty — wave A2 doesn't spawn new handoffs by design; subsequent waves A3-A6 are drafted at the close per the source handoff's "Subsequent waves" section).
- Remove `wave-A2` from `planned_remaining_waves[]`.
- Set `current_wave: null`.
- Append event-log row via `append_event_log.sh`.

If either sub-agent stalls + the operator-gate response is `--defer`, the wave does NOT close. The orchestrator stops + surfaces the wave-open state for operator decision.

## Section 6 — Substrate-adapted wall-clock estimate

Sequential on Cowork: ~85 min (sub-agent 1: ~30 min produce + 5-10 min quality loop = ~35-40 min; sub-agent 2: ~35-40 min) + ~5 min coordination overhead = **~1.5h (lower bound) to ~2.5h (upper bound with one Mode 4 escalation per brief)**.

Parallel on Claude Code Task tool: ~max(sub-agent 1 wall-clock, sub-agent 2 wall-clock) + ~5 min coordination = **~40-60 min** (when both briefs PASS first iteration) up to **~1-1.5h** (when one or both briefs need a Mode 4 escalation).

Operator-fatigue advisory: this wave's queue impact = ~1.5-2.5h on Cowork. Combined with vault total queue at wave A2 promote-time (cleared at v1.1 close), this is well below the 10h ceiling. No advisory warning fires.

## Per-sub-agent dispatch prompts (rendered verbatim)

These are the actual prompts the orchestrator would send if invoked. They are NOT fired in this worked example.

### Dispatch prompt for sub-agent-ev-charger-installation

```
You are a sub-agent dispatched by vault-orchestrator Mode 6 EXECUTE
on behalf of project s-and-h-contracting, wave wave-A2.

Your single artifact: ~/workspace/second-brain/05_shared-intelligence/research-briefs/services/ev-charger-installation.md
Artifact type: service-brief (Tier-1)
Spec source:
  - skill: ~/workspace/skills/service-seo-research/SKILL.md
  - template: ~/workspace/second-brain/05_shared-intelligence/research-briefs/services/_README.md
  - quality-loop routing: ~/workspace/skills/output-quality-loop/references/spec-routing-table.md
    § "Research brief"

Edit-zone: this sub-agent owns the following file paths during execution:
  - ~/workspace/second-brain/05_shared-intelligence/research-briefs/services/ev-charger-installation.md
  - state-file key: quality_log["step-2"]["ev-charger-installation"]
  - references it may update: none

Other concurrent sub-agents are working on:
  - sub-agent-light-fixture-installation (writing
    services/light-fixture-installation.md;
    parallel-OK-with-note per edit-zone detector — both sub-agents append
    to state.waves.wave-A2.outputs which is concurrency-safe;
    NOTE: substrate is Cowork Agent tool today, so this sub-agent runs
    BEFORE the light-fixture sub-agent in serial order).

Per-step quality loop contract: run the four sub-steps in order.

  1. Produce — invoke the service-seo-research sub-skill to author
     the Tier-1 service brief for "ev-charger-installation" covering
     all S&H confirmed cities (woodbridge-va, lake-ridge-va,
     dale-city-va, manassas-va, lorton-va, springfield-va, burke-va,
     alexandria-va, stafford-va) per the build-order matrix.
     Cover all 15 template sections. §4 (AI-search question mining)
     must route through Sonar (Perplexity) + OpenAI gpt-4o + Gemini
     gemini-2.5-flash + Claude sonnet-4-6 per the AI-surface
     reachability matrix at
     ~/workspace/skills/client-seo-onboarding/references/ai-surface-reachability-matrix.md.
     §5 must cover canonical Schema.org Electrician subtype + Service
     node + Offer.priceSpecification estimate-only + areaServed City
     over GeoCircle per the emergency-electrician wave A1 brief's §5
     pattern.

  2. Auto-evaluate — invoke output-quality-loop Mode 1 (EVALUATE) on
     the artifact path. Record verdict + confidence + iteration count
     in quality_log["step-2"]["ev-charger-installation"]. Verdict
     types: PASS / NEEDS REVISION (minor) / NEEDS REVISION
     (substantive) / FAIL. PASS threshold per research-brief spec: 85.

  3. Auto-elevate (if verdict ≠ PASS at threshold) — invoke
     output-quality-loop Mode 4 (AUTO-RESEARCH) via
     perplexity-refinement → Sonar. Cap at 3 iterations. On 3rd FAIL,
     stop + escalate via the operator-gate file at
     ~/workspace/second-brain/04_projects/clients/_active/s-and-h-contracting/_pending-operator-decisions.md
     with gate-type "quality-loop-3-iter-stall".

  4. Auto-decide — invoke output-quality-loop Mode 5
     (AUTO-APPROVE-AND-ESCALATE) with the per-type threshold (85)
     from references/confidence-calibration.md.

State writes — this sub-agent writes to the project state file at
~/workspace/second-brain/04_projects/clients/_active/s-and-h-contracting/_state/onboarding.json
ONLY at these per-key locations:
  - quality_log["step-2"]["ev-charger-installation"] — one entry per iteration
  - waves["wave-A2"].outputs — append the artifact path on PASS at threshold
  - failures[] — append on catastrophic stop (3-iter FAIL or sub-skill error)

You do NOT write any other state-file fields.

Operator gates — when you hit any of these, write a row to
~/workspace/second-brain/04_projects/clients/_active/s-and-h-contracting/_pending-operator-decisions.md
and stop:
  - quality-loop-3-iter-stall (3rd Mode 4 iteration hit FAIL)
  - ambiguous-decision-archaeology (state contradiction you can't resolve)
  - escalated-from-sub-skill (any composed sub-skill that escalates its own gate)

This wave will NOT trigger:
  - higgsfield-variant-pick (no imagery)
  - schema-validation-failure (no data-file authoring)
  - external-write-confirm (no WP REST API writes; no GSC submits; no
    git pushes — research briefs only land in the vault)

Return contract — when your artifact lands at PASS at threshold OR
you escalate via the gate file, return a single structured response:

  {
    "verdict": "<PASS | NEEDS REVISION (minor) | NEEDS REVISION (substantive) | FAIL | ESCALATED>",
    "confidence": <integer 0-100>,
    "iteration_count": <integer>,
    "artifact_path": "~/workspace/second-brain/05_shared-intelligence/research-briefs/services/ev-charger-installation.md",
    "failures": [<failure rows if any>],
    "gate_file_rows_written": [<row IDs if any>]
  }
```

### Dispatch prompt for sub-agent-light-fixture-installation

```
You are a sub-agent dispatched by vault-orchestrator Mode 6 EXECUTE
on behalf of project s-and-h-contracting, wave wave-A2.

Your single artifact: ~/workspace/second-brain/05_shared-intelligence/research-briefs/services/light-fixture-installation.md
Artifact type: service-brief (Tier-1)
Spec source:
  - skill: ~/workspace/skills/service-seo-research/SKILL.md
  - template: ~/workspace/second-brain/05_shared-intelligence/research-briefs/services/_README.md
  - quality-loop routing: ~/workspace/skills/output-quality-loop/references/spec-routing-table.md
    § "Research brief"

Edit-zone: this sub-agent owns the following file paths during execution:
  - ~/workspace/second-brain/05_shared-intelligence/research-briefs/services/light-fixture-installation.md
  - state-file key: quality_log["step-2"]["light-fixture-installation"]
  - references it may update: none

Other concurrent sub-agents are working on:
  - sub-agent-ev-charger-installation (writing
    services/ev-charger-installation.md;
    parallel-OK-with-note per edit-zone detector — both sub-agents append
    to state.waves.wave-A2.outputs which is concurrency-safe;
    NOTE: substrate is Cowork Agent tool today, so this sub-agent runs
    AFTER the ev-charger sub-agent returns).

Per-step quality loop contract: run the four sub-steps in order.

  1. Produce — invoke the service-seo-research sub-skill to author
     the Tier-1 service brief for "light-fixture-installation" covering
     S&H light-fixture build-order cells (slots 04, 08, 12, 16 = 4 cells
     in the build-order; cities woodbridge-va, lake-ridge-va, dale-city-va,
     manassas-va per the build-order matrix). Cover all 15 template
     sections. §4 (AI-search question mining) must route through Sonar
     (Perplexity) + OpenAI gpt-4o + Gemini gemini-2.5-flash + Claude
     sonnet-4-6 per the AI-surface reachability matrix. §5 schema:
     residential-electrical light-fixture scope; same Service node
     pattern as the ev-charger brief.

  2. Auto-evaluate — invoke output-quality-loop Mode 1 (EVALUATE) on
     the artifact path. Record verdict + confidence + iteration count
     in quality_log["step-2"]["light-fixture-installation"]. Verdict
     types: PASS / NEEDS REVISION (minor) / NEEDS REVISION
     (substantive) / FAIL. PASS threshold per research-brief spec: 85.

  3. Auto-elevate (if verdict ≠ PASS at threshold) — invoke
     output-quality-loop Mode 4 (AUTO-RESEARCH) via
     perplexity-refinement → Sonar. Cap at 3 iterations. On 3rd FAIL,
     stop + escalate via the operator-gate file at
     ~/workspace/second-brain/04_projects/clients/_active/s-and-h-contracting/_pending-operator-decisions.md
     with gate-type "quality-loop-3-iter-stall".

  4. Auto-decide — invoke output-quality-loop Mode 5
     (AUTO-APPROVE-AND-ESCALATE) with the per-type threshold (85)
     from references/confidence-calibration.md.

State writes — this sub-agent writes to the project state file at
~/workspace/second-brain/04_projects/clients/_active/s-and-h-contracting/_state/onboarding.json
ONLY at these per-key locations:
  - quality_log["step-2"]["light-fixture-installation"] — one entry per iteration
  - waves["wave-A2"].outputs — append the artifact path on PASS at threshold
  - failures[] — append on catastrophic stop (3-iter FAIL or sub-skill error)

You do NOT write any other state-file fields.

Operator gates — when you hit any of these, write a row to
~/workspace/second-brain/04_projects/clients/_active/s-and-h-contracting/_pending-operator-decisions.md
and stop:
  - quality-loop-3-iter-stall (3rd Mode 4 iteration hit FAIL)
  - ambiguous-decision-archaeology (state contradiction you can't resolve)
  - escalated-from-sub-skill (any composed sub-skill that escalates its own gate)

This wave will NOT trigger:
  - higgsfield-variant-pick (no imagery)
  - schema-validation-failure (no data-file authoring)
  - external-write-confirm (no WP REST API writes; no GSC submits; no
    git pushes — research briefs only land in the vault)

Return contract — when your artifact lands at PASS at threshold OR
you escalate via the gate file, return a single structured response:

  {
    "verdict": "<PASS | NEEDS REVISION (minor) | NEEDS REVISION (substantive) | FAIL | ESCALATED>",
    "confidence": <integer 0-100>,
    "iteration_count": <integer>,
    "artifact_path": "~/workspace/second-brain/05_shared-intelligence/research-briefs/services/light-fixture-installation.md",
    "failures": [<failure rows if any>],
    "gate_file_rows_written": [<row IDs if any>]
  }
```

## Stale-state reconciliations — operator confirmation already cleared

Mode 5 RESUME against S&H 2026-06-02 surfaced two stale-state reconciliations (v1.1 SKILL rewrite blocker apparently cleared; API keys blocker apparently cleared) per the worked example at `examples/first-resume-2026-06-02-s-and-h.md` § Section 5. Both reconciliations cleared with operator "yes" at Mode 5's Gate 3.

At Mode 6 dispatch time today (2026-06-03), the orchestrator re-reads the state file + the event log delta + confirms:

- State file `blocked_on[]` still names the two blockers (state file `updated_at: 2026-06-01 16:30 UTC` — not updated since Mode 5 reconciled; this is expected per Mode 5's read-only discipline).
- Event log rows confirm both blockers cleared (v1.1 SKILL rewrite shipped 2026-06-02 14:56:15 pass-84; API keys wiring shipped 2026-06-02 09:15:00 to 09:22:00).
- Master tracker shows wave A2 row in Ready-to-spawn at pass-85.

The Mode 6 dispatch plan proceeds on the reconciled state. If the operator wants Mode 6 to surface the same reconciliations again at dispatch time (defense in depth), they can chain via "resume s-and-h then execute wave A2" — Mode 5 runs first + emits its reconciliation surface, Mode 6 reads the post-reconciliation state.

## Honest framing — what's NOT in this dispatch plan

1. **Live fire is deliberately omitted.** Per the v1.2 Mode 6 build kickoff's DO NOT directive. The dispatch prompts above are paper artifacts; no Cowork Agent call has been made. The real S&H wave A2 dispatch happens during the actual wave A2 run (which the operator may spawn either manually or via Mode 6 EXECUTE composition).
2. **Cost estimates use the project's first-brief signal.** Emergency-electrician (wave A1) landed at NEEDS REVISION minor with 1 Mode 4 iteration. Wave A2's expected-cost range assumes a similar distribution. If the next briefs hit PASS first iteration, actual cost will be ~$0.002-$0.006 wave-total (just the validation calls). If they hit the worst case (3 iterations each), ~$0.90 wave-total.
3. **Substrate label is single-instance.** This worked example documents Cowork-sequential only. A future operator running Mode 6 against the same wave from Claude Code Task tool would see the same Section 2-5 + a different Section 6 wall-clock + the conflict-flag verdict drives actual concurrent dispatch. The plan SHAPE is substrate-agnostic; only execution shape adapts.
4. **No state-schema migration assumed.** S&H state file schema_version is `"1.0"`. The v1.1 schema fields (`waves[]`, `wave_log[]`, `planned_remaining_waves[]`, `blocked_on[]`, `quality_log`, `current_wave`) are present anyway (S&H's state file is "v1.0 with v1.1 fields ahead of formal migration" per Mode 5's read). Mode 6 reads the present fields; doesn't bump `schema_version`. Migration is the owning skill's responsibility per the v1.1 SKILL.md migration contract.
5. **Worked example is not yet validated against real-use.** This dispatch plan is theory until wave A2 actually runs. The first real-use run will surface any contract gaps; lesson D-rows (D-10+) will capture them in the v1.2 Mode 6 lesson file. Until then this document is a paper artifact + reference.

## What the operator does next

Operator has three substrate paths for actually firing S&H wave A2:

- **Path A — manual Cowork paste.** Operator pastes the wave A2 handoff prompt directly into a fresh Cowork window; `client-seo-onboarding` v1.1 runs its plan-bullet + 11-step machine. Simpler today; no Mode 6 dependency. Estimated cost ~$0.12-$0.30 wave-expected; wall-clock ~1.5-2.5h. This was the operator's baseline path before Mode 6 shipped.
- **Path B — Mode 6 EXECUTE composition from a Cowork chat.** Operator opens a fresh Cowork window, runs Mode 6 EXECUTE on wave A2 (with this worked example as the dispatch-plan reference). Mode 6 fires 2 sub-agents sequentially per the substrate constraint. Same cost surface as Path A. Same wall-clock as Path A. The advantage: the orchestrator manages state-file writes + operator-gate routing centrally rather than running it inline through `client-seo-onboarding`.
- **Path C — Mode 6 EXECUTE composition from a Claude Code Task tool chat.** Operator opens a Claude Code session, runs Mode 6 EXECUTE on wave A2. Mode 6 fires 2 sub-agents in parallel via concurrent Task calls. Wall-clock drops to ~40 min - 1.5h depending on Mode 4 escalation count. Cost surface identical (cost is per-artifact, not per-time). The advantage: actual parallelism.

The three paths land the same artifacts in the vault. Path selection is operator preference based on substrate availability + tolerance for the orchestrator overhead.

## See also

- [[../SKILL|vault-orchestrator SKILL.md]] § "Mode 6 — EXECUTE" — the spec this example demonstrates
- [[../references/sub-agent-dispatch-contract|sub-agent-dispatch-contract.md]] — the per-sub-agent contract this example renders
- [[../references/parallel-safe-coordination|parallel-safe-coordination.md]] — the conflict-detector reuse that resolved parallel-OK-with-note
- [[../references/operator-gate-routing|operator-gate-routing.md]] — the gate-file contract this example would use if a gate fired
- [[../references/inter-agent-coordination-via-state-file|inter-agent-coordination-via-state-file.md]] — the polling contract (Claude Code substrate only — irrelevant here)
- [[first-resume-2026-06-02-s-and-h|first-resume-2026-06-02-s-and-h.md]] — Mode 5 RESUME's first-run example against the same project
- `~/workspace/second-brain/_meta/handoffs/handoff-2026-06-01-s-and-h-wave-a2-service-briefs.md` — the source handoff this dispatch plan operates against
- `~/workspace/second-brain/04_projects/clients/_active/s-and-h-contracting/_state/onboarding.json` — the state file this dispatch plan reads + writes
- `~/workspace/skills/client-seo-onboarding/SKILL.md` § "Per-step quality loop contract" — the four-substep contract the dispatch prompts encode
- `~/workspace/skills/client-seo-onboarding/per-artifact-sizing.md` — the source of per-artifact minute estimates the cost surface aggregates from
