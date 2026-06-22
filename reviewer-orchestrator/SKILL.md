---
name: reviewer-orchestrator
version: 2.0
description: Separate-session control plane that auto-dispatches independent peer-reviewers in parallel for producer chats, removing manual reviewer-spawning while preserving true session-independence. Phase 1 = operator-triggered on an explicit ready-for-review list; Phase 2 = auto-watch event-log polling loop with operator dispatch-plan gate; Phase 3 deferred.
created: 2026-06-22
updated: 2026-06-22T19:00Z
status: active
depends-on: [gate-peer-reviewer, independent-reviewer-mandate]
tags: [skill, review-gate, rgh, rgh-9, reviewer-orchestrator, parallel-review, automation, independent-review]
---

# Reviewer Orchestrator (v2.0)

> **v2.0 changelog (2026-06-22)** — Phase 2: auto-watch event-log polling loop. The orchestrator now watches `_event-log.md` for new `ready-for-review` rows on a configurable cadence (default 60s). Each tick: grep → cross-check markers → report. When unreviewed items are found, builds the dispatch manifest and presents the dispatch plan — operator confirmation at Step 4 still required (no silent auto-dispatch). Per-tick sleep model with operator intervention points between every cycle. Only runs while the Claude Code session is active (not a daemon — that's RGH-3/Hermes). Built by [RGH-9-P2].

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
- "Watch for reviews" / "Start watching" (Phase 2 — starts the polling loop)
- "Watch every 30s" / "Watch every 5m" (Phase 2 — starts with custom cadence)

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

### Per-tick sleep model (Phase 2)

The polling loop uses **conversational turns, not a monolithic Bash loop script.** Each tick is a discrete cycle:

1. **Grep** `_event-log.md` for `ready-for-review` rows.
2. **Cross-check** against `.review-gate/state/` for existing PASS markers.
3. **Report** findings (or "nothing new") to the operator.
4. If items found → present the dispatch plan (Step 4 gate fires). Operator approves/edits/aborts.
5. If nothing found → issue a single `sleep <cadence>` Bash call. When it returns, run the next tick.

This means:
- The operator has a **natural intervention point between every cycle** — they can say "stop watching," change the cadence, or give other instructions.
- **Ctrl+C on the sleep** also works as an immediate interrupt.
- The watcher is **not a daemon** — it only runs while the Claude Code session is active. Background/unattended watching is RGH-3/Hermes territory.

Decision approved at Gate 2 (design review, 2026-06-22).

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

## Phase 2 — Auto-watch event-log (SHIPPED v2.0)

**Trigger met:** Phase 1 proved on ≥2 real producers (BTF-1 session 835d38fb + WF session 5e76d787) with zero mechanism failures (v1.0 shipped + closed pass 300).

Phase 2 adds a polling loop: the orchestrator watches `_event-log.md` for new `ready-for-review` rows on a configurable cadence (default: check every 60s while active). When it finds unreviewed items, it builds the manifest and dispatches — still with operator confirmation at the dispatch-plan gate (Step 4). See "Per-tick sleep model" in Design Decisions for the execution mechanism.

### Step W1 — Enter watch mode

The operator says "watch for reviews" (or a variant — see triggers). Optionally specify a cadence: "watch every 30s," "watch every 5m." Default: 60s.

Announce entry:
```
Watcher active. Cadence: <N>s. Checking _event-log.md for ready-for-review rows.
Say "stop watching" to exit. Say "watch every <N>s" to change cadence.
```

Initialize watcher state:
- `cadence_seconds` — polling interval (default 60)
- `tick_count` — starts at 0
- `last_seen_line_count` — line count of `_event-log.md` at watcher start (optimization: only grep new lines on subsequent ticks)
- `dispatched_sessions` — set of producer sessions already dispatched this watch session (prevents re-dispatch within the same loop)

### Step W2 — Tick: scan for unreviewed items

Each tick runs the same logic as Phase 1 Step 1 (build the review manifest), with these additions:

1. **Grep** `_event-log.md` for rows matching the tab-delimited pattern `\tready-for-review\t` (exact field match — avoids false positives from rows like `peer-review-started` that contain the substring `ready-for-review` in prose).
2. For each match, extract: `chat_id`, `producer_session`, `files`, `gate_tier` (default `full`), `handoff_path` (if present).
3. **Cross-check** against `.review-gate/state/<producer_session>-reviewed.jsonl` — skip items that already have a PASS marker with `reviewer_type: independent`.
4. **Skip** items whose `producer_session` is in `dispatched_sessions` (already dispatched this watch session).
5. **Result:** a list of unreviewed items (may be empty).

**Optimization:** on ticks after the first, only scan lines added since `last_seen_line_count` (use `tail -n +<last_seen_line_count>` before grepping). Update `last_seen_line_count` to the current line count after each tick.

### Step W3 — Report tick result

**If no unreviewed items:**
```
Tick <N>: no new ready-for-review items. Next check in <cadence>s.
```
Then proceed to Step W5 (sleep).

**If unreviewed items found:**
```
Tick <N>: found <M> unreviewed item(s):
- <chat_id_1> (session <session_1>, <file_count> files, tier <tier>)
- <chat_id_2> (session <session_2>, <file_count> files, tier <tier>)
...
Building dispatch plan.
```
Then proceed to Step W4 (dispatch flow).

### Step W4 — Dispatch flow (reuses Phase 1 Steps 2–8)

This is the same as Phase 1:

1. **Step 2** — Pre-allocate CR ID ranges.
2. **Step 3** — Render the dispatch plan.
3. **Step 4** — **Operator confirms the dispatch plan.** No reviewers fire until approved. This is the no-silent-dispatch guarantee.
4. **Step 5** — Dispatch reviewers in parallel (Agent tool).
5. **Step 6** — Collect results + render summary.
6. **Step 7** — Surface any BLOCKING verdicts.
7. **Step 8** — Append event-log rows.

After dispatch completes (or if the operator says `abort` at Step 4), add the relevant producer sessions to `dispatched_sessions`. This prevents re-detecting the same items on the next tick — both dispatched and explicitly aborted items are suppressed for the remainder of this watch session. Then proceed to Step W5 (sleep for the next tick).

### Step W5 — Sleep and loop

Issue a single Bash call:
```bash
sleep <cadence_seconds>
```

When the sleep completes, increment `tick_count` and return to Step W2.

**Operator intervention points:**
- During the sleep, the operator can interrupt (Ctrl+C) — the orchestrator sees the interruption and asks: "Sleep interrupted. Stop watching, change cadence, or continue?"
- Between any tick, the operator can say:
  - `"stop watching"` → exit the loop, announce: "Watcher stopped after <N> ticks."
  - `"watch every <M>s"` / `"slow down to 2m"` / `"speed up to 30s"` → update `cadence_seconds`, acknowledge, continue.
  - Any other instruction → pause the loop, handle the instruction, then ask: "Resume watching?"

### Step W6 — Exit watch mode

When the operator says "stop watching" (or the session ends naturally):

```
Watcher stopped after <N> ticks. Summary:
- Ticks completed: <N>
- Items dispatched: <M> (sessions: <list>)
- Items still unreviewed: <K> (if any remain)
```

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

7. **Watcher is session-scoped, not a daemon (Phase 2).** The polling loop only runs while the Claude Code session is active. If the operator closes the session or the conversation compresses past the watcher state, the loop stops. Background/unattended watching is RGH-3/Hermes territory. The watcher is best suited for: operator working sessions where multiple producers are in flight and reviews should be dispatched as they land.

8. **Watcher deduplication is per-session (Phase 2).** The `dispatched_sessions` set prevents re-dispatching within a single watch session. If the orchestrator session restarts, it re-scans from scratch — but the cross-check against `.review-gate/state/` markers prevents duplicate reviews (items with existing PASS markers are skipped). The only gap: if a reviewer was dispatched but hasn't yet written its marker, a new orchestrator session could re-dispatch. Mitigated by the operator dispatch-plan gate (Step 4) — the operator sees "already dispatched by prior session" context.

## Related

- `[[independent-reviewer-mandate]]` — the fixed instruction set each dispatched reviewer loads
- `[[gate-peer-reviewer]]` — the skill that defines gate types and review procedures
- `log-review-pass.py` — the gate-clearing script with the independence check (lines 99-119)
- `[[handoff-2026-06-22-reviewer-orchestrator-mode7]]` — the originating handoff (RGH-9)
- `[[handoff-2026-06-09-phase-3-hermes-daemon-enforcement]]` — RGH-3, the complementary isolated-process reviewer
- vault-orchestrator Mode 6 — the wave-execution control plane (Phase 3 binds into its wave-close)
