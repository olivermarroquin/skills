---
name: reviewer-orchestrator
version: 1.0
description: Separate-session control plane that auto-dispatches independent peer-reviewers in parallel for producer chats, removing manual reviewer-spawning while preserving true session-independence. Phase 1 = operator-triggered on an explicit ready-for-review list; Phase 2/3 deferred.
created: 2026-06-22
updated: 2026-06-22
status: active
depends-on: [gate-peer-reviewer, independent-reviewer-mandate]
tags: [skill, review-gate, rgh, rgh-9, reviewer-orchestrator, parallel-review, automation, independent-review]
---

# Reviewer Orchestrator (v1.0)

> **v1.0 changelog (2026-06-22)** — Initial build. Phase 1: operator-triggered dispatch of independent peer-reviewers in parallel. Composes RGH-5's independent-reviewer-dispatch + the gate's session-independence check. Standalone skill (not vault-orchestrator Mode 7 — see Design Decisions). Dispatched reviewers inherit the orchestrator's session_id (≠ each producer's session_id), passing the `log-review-pass.py` independence check (CR-045 / RGH-8). Built by [RGH-9].

A **separate-session control plane** that auto-dispatches independent peer-reviewers in parallel. The operator no longer needs to manually paste reviewer prompts into fresh sessions — the orchestrator does it, reliably and concurrently, while preserving the session-independence that makes the review trustworthy.

**The hard constraint it respects:** the review gate (`log-review-pass.py`) rejects any reviewer whose session equals the producer's session (CR-045 / RGH-8). A reviewer dispatched by this orchestrator inherits the **orchestrator's** session — which is ≠ each producer's session — so it passes the independence check. That's the core mechanism.

## When to trigger

### Direct triggers

- "Review these producers"
- "Dispatch reviewers for the ready-for-review items"
- "Run the reviewer-orchestrator"
- "Auto-review [list of sessions/handoffs]"
- "Review what's ready"

### Indirect triggers

- Operator pastes a list of `ready-for-review` event-log rows
- Operator says "review BTF-1 and G13" (names specific producer chats)
- A Mode 6 wave-close signals `ready-for-review` (Phase 3 — deferred)

## Design decisions

### Standalone skill, not vault-orchestrator Mode 7

The handoff proposed Mode 7 as cleanest, but:
1. **Mode 7 is already claimed** by [T2-3] "drift detector / pre-sweep digest" (Tier-3 queue, `vault-orchestrator/phase-7-mode-7-drift-detector-pre-sweep-digest.md`).
2. **Different purpose.** vault-orchestrator manages vault state; this enforces review integrity — fundamentally different concerns.
3. **Composes WITH, not inside.** Fires AFTER producers complete; a peer of vault-orchestrator, not a sub-mode.
4. **SKILL.md size.** vault-orchestrator is ~1560 lines; adding review-dispatch would make it unwieldy.

Decision approved at Gate 1 (plan + design review, 2026-06-22).

### Independence mechanism

```
Producer session:     abc123  ← writes artifacts, posts ready-for-review
Orchestrator session: xyz789  ← THIS session (separate from all producers)
Reviewer sub-agent:   inherits xyz789 (Claude Code Agent tool inherits parent session_id)

log-review-pass.py --session abc123 --reviewer-session xyz789 → PASS  (xyz789 ≠ abc123)
log-review-pass.py --session abc123 --reviewer-session abc123 → REJECTED (same session)
```

Sub-agents dispatched via Claude Code's Agent tool inherit the parent's `session_id` (confirmed by real-runner evidence 2026-06-12, CC v2.1.85). This is the structural guarantee.

## Input format (Phase 1)

The operator provides a review manifest — a list of producer items to review. Each item needs:

| Field | Required | Source | Description |
|---|---|---|---|
| `producer_session` | Yes | Event-log `ready-for-review` row | The producer's session ID |
| `files` | Yes | Event-log row or dirty ledger | Files to review |
| `handoff_path` | Yes (build chats) | Event-log row or handoff frontmatter | Path to the originating handoff |
| `gate_tier` | Yes | Event-log row | `full` or `fast-path` |
| `gate_id` | No (default: `G-independent`) | Event-log row | Gate type |
| `chat_id` | Yes | Event-log row | Producer's chat ID (for firing-tracker) |

**Shorthand:** the operator can also just say "review the `ready-for-review` items in the event log" and the orchestrator will scan `_event-log.md` for unreviewed `ready-for-review` rows, cross-check against `.review-gate/state/` for existing markers, and build the manifest automatically.

## Step-by-step (Phase 1)

### Step 1 — Build the review manifest

If the operator provides explicit items, parse them into the manifest. If the operator says "review what's ready," scan `_event-log.md`:

1. Grep for `ready-for-review` rows
2. For each, extract: chat_id, producer_session, files, gate_tier, handoff_path
3. Cross-check against `.review-gate/state/<producer_session>-reviewed.jsonl` — skip items that already have a PASS marker with `reviewer_type: independent`
4. Present the manifest to the operator for confirmation

### Step 2 — Pre-allocate CR ID ranges

To prevent CR-### collisions when multiple reviewers write to `_review-gate-catch-register.md` concurrently:

1. Read the current highest CR-### ID from the catch register
2. Allocate a range per reviewer: reviewer 1 gets CR-(N+1) through CR-(N+20), reviewer 2 gets CR-(N+21) through CR-(N+40), etc.
3. Include the allocated range in each reviewer's dispatch prompt

### Step 3 — Render the dispatch plan

For each manifest item, render one row:

| # | Producer chat | Session | Files | Tier | Handoff | CR range |
|---|---|---|---|---|---|---|

Plus:
- **Dispatch shape:** parallel (all reviewers fire concurrently via Agent tool)
- **Edit-zone analysis:** verdict files are per-session-namespaced (no collision); firing-tracker rows are append-only (low collision, but reviewers must use their allocated CR range); catch-register uses pre-allocated CR-### ranges (no collision)
- **Estimated wall-clock:** ~5-15 min per review (parallel, so total ≈ slowest reviewer)

### Step 4 — Operator confirms the dispatch plan

Operator says `approve` / `edit` / `abort`. No reviewers fire until approved.

### Step 5 — Dispatch reviewers in parallel

For each manifest item, fire an Agent sub-agent with the dispatch prompt from `references/dispatch-contract.md`. All items dispatch in a single message (parallel Agent tool calls).

Each dispatched reviewer:
1. Loads `independent-reviewer-mandate.md` from disk (hardcoded path, non-negotiable)
2. Reads the producer's dirty ledger + handoff
3. Runs the full review protocol (Phases A→E from the mandate)
4. Writes verdict JSON to `.review-gate/state/verdict-independent-<producer_session>-<timestamp>.json`
5. Authors firing-tracker rows (using the orchestrator's chat ID prefix)
6. Authors catch-register rows (using pre-allocated CR range)
7. Calls `log-review-pass.py` with:
   - `--session <producer_session>`
   - `--reviewer-session <orchestrator_session>` (inherited from this orchestrator)
   - `--reviewer-type independent`
   - `--run-id <chat_id>`
   - `--verdict-file <path>`
   - `--tier <gate_tier>`
   - `--gate-id G-independent`
   - `--files <file1> <file2> ...`
8. Returns structured result: verdict, catch count per pass, convergence status

### Step 6 — Collect results + render summary

As each reviewer completes, collect its result. Render a summary table:

| # | Producer | Verdict | Passes | Catches | CR IDs | Gate cleared? |
|---|---|---|---|---|---|---|

### Step 7 — Surface any BLOCKING verdicts

If any reviewer returns BLOCKING: surface the findings to the operator with the specific catches and the producer chat that needs fixes. The orchestrator does NOT auto-resolve — operator drives.

### Step 8 — Append event-log rows

For each completed review, append an event-log row:

```
<timestamp> | <files> | reviewer-orchestrator-dispatched-review | <orchestrator-chat-id> | [RGH-9] Independent review dispatched by reviewer-orchestrator: <producer_chat_id> verdict <PASS|BLOCKING>, <N> passes, <M> catches. Reviewer session <orchestrator_session> ≠ producer session <producer_session>.
```

## Phase 2 — Auto-watch event-log (DEFERRED)

**Trigger to build:** Phase 1 proves on ≥2 real producers with zero mechanism failures.

Phase 2 adds a polling loop: the orchestrator watches `_event-log.md` for new `ready-for-review` rows on a configurable cadence (default: check every 60s while active). When it finds unreviewed items, it builds the manifest and dispatches — still with operator confirmation at the dispatch-plan gate (Step 4).

## Phase 3 — Bind to Mode 6 wave-close (DEFERRED)

**Trigger to build:** Phase 2 stable for ≥1 week of real use.

Phase 3 wires into vault-orchestrator Mode 6's Step 10 wave-close: when a wave closes with all sub-agents PASS, Mode 6 posts a `ready-for-review` event-log row and the reviewer-orchestrator auto-dispatches the independent review. The operator's only gate is the dispatch-plan confirmation (Step 4).

## Honest limits

1. **Independent of producers, not of each other.** Dispatched reviewers share the orchestrator's session context. They are independent of each producer (different session), but not of each other. The strongest isolation (separate processes) is RGH-3/Hermes territory — complementary, not replaced by this.

2. **Runs on Claude Code (Agent tool).** This does NOT make Hermes unattended runs trustworthy — that's RGH-3's job. This automates the operator's manual reviewer-spawning workflow on Claude Code.

3. **Verdict file is model-authored.** Until the reviewer runs as an isolated process (RGH-3 Phase 2/3), the verdict file is model-authored. The operator remains the integrity backstop — spot-check verdict files in `.review-gate/state/`.

4. **CR range pre-allocation is an estimate.** If a reviewer finds >20 catches (the default range size), it must stop at the range boundary and report "CR range exhausted" — the orchestrator re-allocates and re-dispatches. This is unlikely in practice (median catch count is 3-5 per review).

5. **Agent sub-agents may produce shallower reviews than full separate-session reviewers.** The Agent tool dispatches a sub-agent with a single prompt — it runs autonomously without operator paste-back loops. This ensures session-independence (the mechanism) but not review depth (the adversarial rigor). For high-stakes artifacts, a full separate-session running review (operator relays each producer output, reviewer disk-verifies step-by-step per mandate Phase R) remains the gold standard. The orchestrator-dispatched review is best suited for: re-verification of already-reviewed artifacts, fast-path tier files, and parallel batch reviews where mechanism-independence matters more than maximum adversarial depth.

6. **Session ID inheritance is version-dependent.** Confirmed on CC v2.1.85 (2026-06-12). Re-verify after Claude Code upgrades — if Agent tool stops inheriting parent session_id, the independence mechanism breaks silently. The `log-review-pass.py` rejection check is the safety net (it will reject same-session attempts), but the orchestrator becomes unable to clear the gate.

## Related

- `[[independent-reviewer-mandate]]` — the fixed instruction set each dispatched reviewer loads
- `[[gate-peer-reviewer]]` — the skill that defines gate types and review procedures
- `log-review-pass.py` — the gate-clearing script with the independence check (lines 99-119)
- `[[handoff-2026-06-22-reviewer-orchestrator-mode7]]` — the originating handoff (RGH-9)
- `[[handoff-2026-06-09-phase-3-hermes-daemon-enforcement]]` — RGH-3, the complementary isolated-process reviewer
- vault-orchestrator Mode 6 — the wave-execution control plane (Phase 3 binds into its wave-close)
