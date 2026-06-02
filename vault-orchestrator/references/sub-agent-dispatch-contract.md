# Sub-agent dispatch contract

How Mode 6 EXECUTE spawns sub-agents to produce artifacts on behalf of a project's next-wave handoff. Names what a sub-agent is, the prompt shape, the return contract, and how the orchestrator adapts the dispatch model to the runtime substrate.

This is the per-sub-agent layer. For how multiple sub-agents coordinate via the state file, see [[inter-agent-coordination-via-state-file]]. For how parallelism is bounded by edit-zone conflict detection, see [[parallel-safe-coordination]]. For how operator-visible gates surface, see [[operator-gate-routing]].

## What a sub-agent is

A sub-agent is a narrowly-scoped per-artifact worker. It receives a prompt that names exactly one artifact to produce (one service brief, one city brief, one data file, one scaffolded page) plus the spec source for that artifact type plus the per-step quality loop contract. It produces that artifact end-to-end — runs the four-substep loop (Produce → Auto-evaluate Mode 1 → Auto-elevate Mode 4 if needed → Auto-decide Mode 5) — and returns a verdict + confidence + iteration count + artifact path + any failures.

**A sub-agent is NOT a full orchestrator-from-scratch invocation of `client-seo-onboarding`.** See lesson D-01 for the architectural rationale. The orchestrator's job is coordination; the sub-agent's job is one artifact. If a wave needs four artifacts, the orchestrator dispatches four sub-agents (sequenced or parallel per the substrate).

**A sub-agent is NOT human-judgment-heavy work.** Final report tone, escalation reasoning, ambiguous decision archaeology, Higgsfield variant pick — those stay operator-attended per `Mode 6 — out of scope`. Sub-agents can SURFACE these (route to the operator-gate file per [[operator-gate-routing]]) but they don't resolve them.

## The dispatch prompt shape

When Mode 6 spawns a sub-agent, it produces a prompt with these load-bearing parts:

```
You are a sub-agent dispatched by vault-orchestrator Mode 6 EXECUTE
on behalf of project <project-slug>, wave <wave-id>.

Your single artifact: <absolute artifact path on disk>
Artifact type: <service-brief | city-brief | intersection-brief | client-fact-brief | data-file | scaffolded-page | imagery-prompts | internal-link-proposals | final-report>
Spec source: <path to the spec the artifact must satisfy>

Edit-zone: this sub-agent owns the following file paths during execution:
- <artifact path>
- state-file key: quality_log["<step>"]["<artifact-name>"]
- references it may update: <list or "none">

Other concurrent sub-agents are working on:
- <other sub-agent artifacts, if any — parallel-safe per edit-zone detector>

Per-step quality loop contract: run the four sub-steps in order.
  1. Produce — author the artifact per the spec source.
  2. Auto-evaluate — invoke output-quality-loop Mode 1 (EVALUATE) on
     the artifact path. Record verdict + confidence + iteration count.
  3. Auto-elevate (if verdict ≠ PASS at threshold) — invoke
     output-quality-loop Mode 4 (AUTO-RESEARCH) via perplexity-refinement
     → Sonar. Cap at 3 iterations. On 3rd FAIL, stop + escalate via
     the operator-gate file.
  4. Auto-decide — invoke output-quality-loop Mode 5
     (AUTO-APPROVE-AND-ESCALATE) with the per-type threshold from
     references/confidence-calibration.md.

State writes — this sub-agent writes to the project state file
(<state-file path>) ONLY at these per-key locations:
  - quality_log["<step>"]["<artifact-name>"] — one entry per iteration
  - waves[<wave-id>].outputs — append the artifact path on PASS at threshold
  - failures[] — append on catastrophic stop (3-iter FAIL or sub-skill error)

You do NOT write any other state-file fields. The orchestrator owns the
rest (current_wave, planned_remaining_waves, blocked_on, ingest block,
research_status, etc.).

Operator gates — when you hit any of these, write a row to
<gate-file path> and stop:
  - Higgsfield variant pick (Step 7 work)
  - Schema validation failure on a data file
  - 3-iter quality-loop stall (per Auto-elevate cap)
  - Any external write (WP REST API, GSC submit, git push, tier-3
    mutation) — see lesson D-06

Return contract — when your artifact lands at PASS at threshold OR you
escalate via the gate file, return a single structured response:
  {
    "verdict": "<PASS | NEEDS REVISION (minor) | NEEDS REVISION (substantive) | FAIL | ESCALATED>",
    "confidence": <integer 0-100>,
    "iteration_count": <integer>,
    "artifact_path": "<absolute path>",
    "failures": [<failure rows if any>],
    "gate_file_rows_written": [<row IDs if any>]
  }
```

The prompt is verbatim — the sub-agent treats it as its operating instructions. The orchestrator does not paraphrase or summarize at dispatch time.

## Substrate-adaptive dispatch

Mode 6 detects the runtime substrate at dispatch time and adapts the dispatch model accordingly. See lesson D-07 for the precipitating refinement.

### Substrate detection

The orchestrator checks (in order):

1. **Operator-stated substrate** — if the operator names it explicitly ("dispatch via Cowork Agent tool" / "fire from Claude Code Task tool"), use that and skip the probes.
2. **Tool availability probes** — concrete probes the orchestrator runs in this order:
   - **Probe 1 — Task tool availability.** Check whether the Claude Code `Task` tool appears in the runtime's tool list AND can be called without an "unknown tool" error. If yes → Claude Code Task tool substrate. Detect by inspecting the system-prompt tool inventory OR by attempting a dry-run Task call wrapped in error handling.
   - **Probe 2 — filesystem mount paths.** Inspect the runtime's working directory and known workspace root. Path matching `/sessions/<id>/mnt/workspace/` indicates Cowork sandbox; path matching `/Users/<user>/workspace/` (or `~/workspace/` resolved by the Mac shell) indicates Mac Terminal (Claude Code). If Probe 1 was ambiguous + filesystem signals are clean, Probe 2 resolves the substrate.
   - **Probe 3 (future) — Hermes-harness MCP server registration.** Check the MCP registry for a registered `hermes-harness` server. If present + reachable, that's Hermes substrate. Not live today; reserved for the post-Hermes-shipping era.
   - **Probe order:** 1 → 2 → 3 → default. The first probe to resolve a substrate wins; subsequent probes don't run.
3. **Fallback** — Cowork sandbox is the default when all probes are ambiguous; renders the dispatch plan with the sequential adaptation. Operator can override with `--substrate <name>` if the default is wrong.

When operators report substrate mis-detection, the debug path is: which probe resolved the substrate? If Probe 1 returned a false positive (Task tool listed but actually unreachable), the runtime tool inventory may be stale — surface the diagnostic + ask operator to confirm.

### Substrate matrix

| Substrate | Status (2026-06-03) | Dispatch model | State-file writes | Polling cadence |
|---|---|---|---|---|
| Cowork Agent tool | Available today | Sequential one-shot. One Agent call per sub-agent; orchestrator blocks until the call returns; writes state between calls; next call spawns when prior returns. | Between calls (orchestrator does the write, not the sub-agent). | N/A — calls block until return. |
| Claude Code Task tool | Available today | True parallel. Multiple Task calls in one message fan out concurrently; sub-agents write `quality_log` keys mid-run; orchestrator polls state file at configurable cadence. | Mid-run, per-key (each sub-agent owns its `quality_log[<step>][<artifact-name>]` key per [[inter-agent-coordination-via-state-file]]). | Default 10s, configurable via `--polling-cadence Ns`. |
| Hermes-harness | Future (Phase 1 prework still queued; substrate not live yet) | Long-lived sub-agents with bidirectional messaging; full polling model with low-latency state propagation; sub-agents can be paused + resumed. | Mid-run + push notifications via Hermes channels. | Push-driven (no polling needed) once Hermes ships. |

### How the orchestrator names the substrate up front

At the dispatch plan's top, Mode 6 emits an explicit substrate label so the operator sees the actual execution shape + cost surface before any work fires:

```
Dispatching wave <wave-id> for <project-slug> via <substrate-name> substrate.

Execution shape: <parallel | sequential | push-driven>
Estimated wall-clock: <hours range — adapted to substrate>
Estimated API cost: ~$<total> across <N> sub-agents
  (Sonar Mode 4 calls ~$<per-artifact-Sonar> per artifact × <N> = $<Sonar-subtotal>
   + OpenAI/Gemini/Claude pre-fire validation calls ~$<per-artifact-validation> per artifact × <N> = $<validation-subtotal>
   — pre-fire validation always fires; Sonar Mode 4 fires only on NEEDS REVISION verdicts)
Sub-agent count: <N>
Parallel-safe per edit-zone detector: <count> sub-agents
Serialized per edit-zone detector: <count> sub-agents
```

Honest framing prevents the trust erosion lesson D-07 named: an operator who sees "parallel-OK-with-note" on a Cowork dispatch shouldn't think they're getting concurrent execution they aren't. The cost surface is similarly honest — operator sees the pre-fire surface PLUS the conditional Mode 4 escalation surface, not just one or the other.

### Cost estimation aggregated from per-artifact-sizing

Mode 6 reads `~/workspace/skills/client-seo-onboarding/per-artifact-sizing.md` § "Quality-loop overhead per artifact" + the standing per-call costs the operator's wrapper scripts have logged. For each planned sub-agent, the orchestrator estimates:

- **Always-fires per artifact (pre-fire validation calls):** Mode 1 EVALUATE runs the spec walk but doesn't typically hit external APIs; the v1.1 per-step quality loop also runs OpenAI / Gemini / Claude direct citation comparisons on §4c for research briefs (per `client-seo-onboarding` v1.1's AI-surface reachability matrix). Estimate: ~$0.001-0.003 per artifact for the three validation calls (combined cost of OpenAI gpt-4o + Gemini gemini-2.5-flash + Claude sonnet-4-6 small queries). Aggregate `validation-subtotal = per_artifact_validation × N`.
- **Conditional per artifact (Mode 4 Sonar escalation):** fires only when Mode 1 returns NEEDS REVISION. Per `per-artifact-sizing.md` § "Quality-loop overhead," a single Mode 4 iteration adds ~$0.06-$0.15 (3-5 Sonar queries). Worst case (3 iterations to PASS) = ~$0.30-$0.45 per artifact. Estimate at ~$0.10-$0.20 per artifact on average + name the worst-case explicitly.
- **Total per sub-agent:** validation-always + Sonar-conditional. Aggregate across N sub-agents for the wave-level estimate.

The dispatch plan renders the conditional surface honestly: "Sonar Mode 4 fires only on NEEDS REVISION verdicts" — operator sees that the total is a CEILING, not a deterministic spend. On a wave where all artifacts PASS first iteration, actual cost ≈ validation-subtotal only.

When the project's `state-file.quality_log` history shows past PASS-rate signal, the orchestrator may name an expected-cost range (e.g., "first S&H brief landed at NEEDS REVISION minor with 1 Mode 4 iteration → expect ~$0.06-$0.12 per artifact in practice"). If no signal exists, the orchestrator names the wide range + leaves the expected to the operator's read.

Cost line discipline: ALL surface costs are inline + named per surface; no opaque totals; no "approximately $X" without naming what's in $X. Per the standing plain-language convention + lesson D-07's framing rule.

### Why this matters for time estimates

Sequential dispatch on Cowork: total wall-clock ≈ sum of all sub-agent durations. A wave with two 90-minute briefs runs ~3h.

Parallel dispatch on Claude Code Task tool: total wall-clock ≈ duration of the slowest sub-agent (plus dispatch + return overhead). Two 90-minute briefs in parallel run ~1.5-2h.

The dispatch plan names BOTH numbers when the substrate could change between drafting + firing.

## Return contract

Every sub-agent returns a structured response (the shape in the prompt template above). The orchestrator:

1. Parses the response.
2. Verifies the artifact exists on disk at the named path.
3. Verifies state-file writes happened (cross-checks `quality_log[<step>][<artifact-name>]` for the verdict + confidence + iteration count).
4. On `verdict: PASS at threshold`, marks the sub-agent done in its dispatch log.
5. On `verdict: ESCALATED`, surfaces the gate-file row to the operator + pauses dispatch.
6. On `verdict: FAIL after 3 iterations`, escalates per [[operator-gate-routing]] § "3-iter quality stall."

If the sub-agent returns malformed (no JSON, missing fields, or "I couldn't do that"), the orchestrator marks the sub-agent as failed in its dispatch log + escalates via the gate file rather than silently dropping the failure.

## Sub-agent failure modes

| Failure | Detection | Orchestrator response |
|---|---|---|
| Sub-agent didn't write the artifact file | Step 2 verification fails | Mark sub-agent failed; surface as gate-file row; pause wave. |
| Sub-agent wrote state to a forbidden key (e.g., mutated `confirmed_services`) | State-file diff vs. allowed-write key set | Mark sub-agent failed; surface contract violation; require operator review before resuming the wave. |
| Sub-agent return is malformed | JSON parse fails OR required fields missing | Re-prompt the sub-agent once with the contract template; on second failure, escalate. |
| Sub-agent hits a real-world action gate | `verdict: ESCALATED` + gate-file row written | Surface the gate row + pause; resume on operator confirmation. |
| Sub-agent times out (long-running) | Substrate-specific timeout fires | Mark sub-agent timed-out; escalate via gate file with the sub-agent's last-known state. |

## Composition with `client-seo-onboarding`

Mode 6 dispatches sub-agents per the artifact types named in `client-seo-onboarding` v1.1 SKILL.md § "Per-step quality loop contract." The dispatch prompt reuses that skill's per-step quality loop language verbatim — the sub-agent's contract is the same contract the orchestrator chat would run if it executed inline.

The composition contract: Mode 6 does NOT reimplement the per-step quality loop. It dispatches sub-agents whose contract IS the per-step quality loop. The sub-agent's spec source is the spec the `client-seo-onboarding` step would route to via `output-quality-loop/references/spec-routing-table.md`.

## See also

- [[../SKILL|vault-orchestrator SKILL.md]] § "Mode 6 — EXECUTE" — the orchestrator entry point that invokes this contract
- [[inter-agent-coordination-via-state-file]] — how parallel sub-agents coordinate without colliding
- [[operator-gate-routing]] — the gate-file contract sub-agents use to escalate
- [[parallel-safe-coordination]] — the Phase 4 edit-zone conflict detection reuse
- [[resume-input-sources]] — what Mode 5 reads; Mode 6 consumes Mode 5's output as input
- [[resume-output-shape]] — Mode 5's Section 2 (Available next-wave handoffs) IS Mode 6's "what to dispatch" input
- `~/workspace/skills/client-seo-onboarding/SKILL.md` § "Per-step quality loop contract" — the canonical four-substep contract sub-agents implement
- `~/workspace/skills/output-quality-loop/references/spec-routing-table.md` — sub-agents read this to find the right spec for their artifact type
