# Operator-gate routing via `_pending-operator-decisions.md`

How Mode 6 surfaces sub-agent-blocking gates to the operator and resumes paused sub-agents on operator decision. See lesson D-03 for why this is a separate file from the state file's `operator_decisions_pending` field.

## Why a separate file from state-file `operator_decisions_pending`

The state file's `operator_decisions_pending` array holds project-scoped decisions that persist across waves (e.g., S&H's "research-scope-staging" decision from wave A1 — surfaced 2026-06-01, may persist for days or weeks until the operator resolves it). Mode 6's gates are sub-agent-scoped + transient — typically resolved in minutes, not hours.

Mixing the two pollutes the state file with ephemera. Operator gate rows in `_pending-operator-decisions.md` get cleared as the operator responds; they don't accumulate as a long-running decision log. The state file stays lean for the persistent decision shape.

The two surfaces coexist:

- **Persistent project decisions** → `state-file.operator_decisions_pending[]`
- **Transient sub-agent gates** → `_pending-operator-decisions.md` (this file)

## File location

`04_projects/clients/_active/<slug>/_pending-operator-decisions.md` (or the project's parallel path under `_active` / `_private` / `personal/`).

One file per project. Mode 6 creates it if absent at the first gate; cleans it up (truncates to header only) after wave-close if all gates are resolved.

## File shape

```markdown
---
type: operator-gate-log
status: active
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
project: <slug>
tags: [operator-gate, vault-orchestrator, mode-6-execute, <slug>]
---

# Operator gates — pending decisions for <project-slug>

This file surfaces sub-agent gates that need the operator's call before
the orchestrator can resume dispatch. One row per outstanding gate.
Respond by editing the row's "Operator response" cell inline. The
orchestrator polls this file alongside the state file.

## Open gates

| ID | Surfaced at (UTC) | Sub-agent | Artifact | Gate type | Decision needed | Operator response |
|---|---|---|---|---|---|---|
| <gate-id-1> | <ISO timestamp> | <sub-agent slug> | <artifact path> | <gate type> | <one-paragraph context + the decision the orchestrator needs> | _(pending)_ |

## Closed gates (this wave)

| ID | Closed at (UTC) | Decision | Resumed sub-agent? |
|---|---|---|---|

## See also

- [[../../_meta/handoffs/handoff-2026-06-01-vault-orchestrator-mid-project-resume-capability|v1.2 handoff]]
- `~/workspace/skills/vault-orchestrator/references/operator-gate-routing.md` — this contract
```

The "Closed gates (this wave)" section preserves an audit trail for the current wave; older closed gates archive at wave-close (orchestrator moves them to a per-wave subsection or deletes per project preference — default: delete after wave-close).

## Gate row schema

Each row in "Open gates" has these fields:

| Field | Content |
|---|---|
| ID | `gate-<wave-id>-<artifact-slug>-<short-hash>` — globally unique within the project. The orchestrator computes the hash from the artifact path + gate type + timestamp so re-runs produce stable IDs. |
| Surfaced at (UTC) | ISO 8601 timestamp from `date -u +"%FT%T"`. |
| Sub-agent | The sub-agent's slug (typically the artifact name). |
| Artifact | Absolute path to the artifact in question. |
| Gate type | One of the enum values below. |
| Decision needed | One paragraph + the concrete decision the orchestrator needs (typically yes/no, or a one-word value). Plain language; never expects the operator to read code or YAML to understand the gate. |
| Operator response | `_(pending)_` until the operator edits it. Acceptable responses: a one-word answer (`yes` / `no` / a value) OR `--defer` to come back later OR `--abort` to stop the wave. |

## Gate types (enum)

| Gate type | When it fires | Typical operator response |
|---|---|---|
| `higgsfield-variant-pick` | Sub-agent reached Step 7 imagery generation and Higgsfield offered N variants; sub-agent surfaces a thumbnail summary + needs the operator's pick | one of the variant IDs (`v1` / `v2` / `v3` / `regenerate`) |
| `schema-validation-failure` | Sub-agent's produced data file fails JSON schema check (extra field, missing required, wrong type) | `proceed-with-fix` (sub-agent auto-fixes per a named patch) / `manual-fix` (operator hand-edits) / `regenerate` / `abort-step` |
| `quality-loop-3-iter-stall` | Sub-agent ran 3 Mode 4 auto-elevate iterations and still hit FAIL on Mode 1 evaluate | `accept-fail` (proceed with FAIL audit trail) / `manual-revise` (operator hand-edits then resume) / `escalate-to-hard` (writes to `_meta/escalations/`) / `defer` |
| `external-write-confirm` | Sub-agent is about to fire a real-world action (WP REST API write, GSC submit, git push, tier-3 mutation per D-06) | `fire` / `defer` / `abort` |
| `ambiguous-decision-archaeology` | Sub-agent encountered a state contradiction it can't resolve (e.g., two execution logs disagree on what shipped); surfaces the contradiction + asks for the operator's call | free-text resolution per the surfaced ambiguity |
| `escalated-from-sub-skill` | A composed sub-skill (e.g., `output-quality-loop` Mode 5 hard-escalation) surfaced its own gate; sub-agent forwards it | depends on the composed skill's contract |

## How the orchestrator polls + resumes

The orchestrator's polling cycle (per [[inter-agent-coordination-via-state-file]] § "Polling cadence") reads the gate file alongside the state file:

```
On every poll:
1. Read state file. Process per-sub-agent quality_log entries as
   described in inter-agent-coordination-via-state-file.md.
2. Read _pending-operator-decisions.md. Parse the "Open gates" table.
3. For each row:
   a. If "Operator response" cell is still _(pending)_ → leave the
      sub-agent paused.
   b. If "Operator response" cell has a value → process the response:
      - For `yes`/`fire`/a specific value: orchestrator emits the
        resume signal to the sub-agent (next-poll dispatch with the
        operator-supplied value as additional context).
      - For `--defer`: orchestrator marks the sub-agent deferred;
        wave does NOT close until either the sub-agent resumes or the
        operator says `--abort`.
      - For `--abort`: orchestrator marks the sub-agent failed; closes
        the wave with the gated artifact missing; appends a wave_log
        entry naming the abort.
   c. On non-pending responses, move the row from "Open gates" to
      "Closed gates (this wave)" with the operator's decision + a
      timestamp + whether the sub-agent resumed.
4. Continue polling other sub-agents.
```

The orchestrator never auto-resolves a gate. The operator's response is the only source of truth for resolution.

## Worked example — quality-loop hard escalation routing through gate file

Sub-agent producing `services/ev-charger-installation.md` runs the four-substep loop. Iteration 1 verdict: NEEDS REVISION (substantive). Iteration 2 verdict: NEEDS REVISION (minor). Iteration 3 verdict: FAIL at confidence 65.

Sub-agent stops + writes:

```
state-file quality_log["step-2"]["ev-charger-installation"] = {
  iteration: 3,
  verdict: "FAIL",
  confidence: 65,
  decision: "hard-escalate",
  ...
}
```

Sub-agent appends a row to `_pending-operator-decisions.md`:

```markdown
| gate-wave-A2-ev-charger-installation-a4f7 | 2026-06-03T15:42:18Z | ev-charger-installation | 05_shared-intelligence/research-briefs/services/ev-charger-installation.md | quality-loop-3-iter-stall | Sub-agent ran 3 Mode 4 auto-elevate iterations on the ev-charger service brief and still hit FAIL at confidence 65. Top remaining gap (per Mode 1 eval): §4c OpenAI/Gemini direct citation comparison — sub-agent's Mode 4 queries returned generic results instead of cited synthesis. Suggest one of: `accept-fail` (proceed with the artifact at FAIL; light-escalate row added to folder log), `manual-revise` (operator hand-edits §4c then sub-agent re-runs Mode 5), `escalate-to-hard` (writes to `_meta/escalations/` + master tracker row + pauses wave), or `defer` (mark sub-agent deferred; wave doesn't close until resolved). | _(pending)_ |
```

Sub-agent returns `verdict: ESCALATED`. The orchestrator polls + sees the gate row. Marks ev-charger sub-agent paused.

Operator reads the row + responds inline:

```markdown
| gate-wave-A2-ev-charger-installation-a4f7 | 2026-06-03T15:42:18Z | ev-charger-installation | ... | quality-loop-3-iter-stall | ... | manual-revise |
```

Orchestrator polls + sees the non-pending response. Moves the row to "Closed gates" + writes:

```markdown
| gate-wave-A2-ev-charger-installation-a4f7 | 2026-06-03T15:51:33Z | manual-revise | yes (waiting for operator hand-edit; sub-agent re-dispatches on operator's "ready" signal) |
```

Orchestrator pauses the sub-agent in `manual-revise-waiting` mode. Operator edits the brief by hand. Operator returns to chat + says "ready" or similar. Orchestrator re-dispatches the ev-charger sub-agent with the manual-revise flag, which sends it directly to Mode 5 Auto-decide on the hand-edited artifact (skipping a fresh Mode 1 iteration).

## File cleanup at wave-close

At wave-close, the orchestrator:

1. Verifies all "Open gates" are empty (no row should be `_(pending)_` at wave-close; if any are, the wave didn't actually close).
2. Truncates the "Closed gates (this wave)" section per project preference:
   - Default: clear the section (the wave-close audit is in `wave_log`).
   - On `--preserve-gate-history`: leave the closed gates in the file as a per-wave archive subsection.
3. Updates the frontmatter `updated:` field.
4. Leaves the file in place for the next wave's gates.

If a project's `_pending-operator-decisions.md` is empty (no open gates + no closed history) for >30 days, the orchestrator can prune it. Default: leave in place (the file's existence isn't expensive).

## Composition with mission-control-dashboard (future)

Once `mission-control-dashboard` ships (currently Phase 0 stack research complete; implementation queued), the dashboard reads `_pending-operator-decisions.md` files across projects + surfaces a "gates needing your call" view. Today's contract anticipates this: the file shape is the dashboard's source-of-truth schema. Don't rename fields without updating the dashboard's reader.

## See also

- [[../SKILL|vault-orchestrator SKILL.md]] § "Mode 6 — EXECUTE" — the dispatch entry point
- [[sub-agent-dispatch-contract]] — the sub-agent contract that names gate-file writes
- [[inter-agent-coordination-via-state-file]] — the polling cycle that reads this file
- `~/workspace/skills/client-seo-onboarding/state-schema.md` § "Manual operator overrides" — the parallel operator-edit surface on the state file
- `~/workspace/second-brain/_meta/handoffs/mission-control-dashboard/_README.md` — the future dashboard that consumes this file
