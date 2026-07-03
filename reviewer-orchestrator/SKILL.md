---
name: reviewer-orchestrator
version: 3.0
description: Separate-session control plane that auto-dispatches independent peer-reviewers in parallel for producer chats, removing manual reviewer-spawning while preserving true session-independence. Phase 1 = operator-triggered dispatch; Phase 2 = auto-watch event-log polling; Phase 3 deferred. v3.0 adds deterministic completeness pre-checks (RGH-18/19 + PR-1 DoD) and structured producer-reply generation via event-log handoff-bus.
created: 2026-06-22
updated: 2026-07-03T00:00Z
status: active
depends-on: [gate-peer-reviewer, independent-reviewer-mandate]
tags: [skill, review-gate, rgh, rgh-9, reviewer-orchestrator, parallel-review, automation, independent-review]
---

# Reviewer Orchestrator (v3.0)

> **v3.0 changelog (2026-07-03)** — [RGH-16/RO-FIX]: completeness audit + producer-reply. Two new capabilities:
> 1. **Deterministic completeness pre-checks (Step 2):** Before dispatching LLM reviewers, the orchestrator runs `rgh18-build-correctness.py` + `rgh19-doc-completeness.py` on each full-tier manifest item. If either returns BLOCKING, that item is flagged DETERMINISTIC-BLOCKED and the LLM reviewer is skipped (the deterministic checks already found the problems). For Productize-tier runs, RGH-19's OC-20 enforces PR-1's B1-B6 DoD. This makes the orchestrator INVOKE the completeness checks, not just trust the reviewer to run them.
> 2. **Structured producer-reply (Step 9):** After all reviews complete, the orchestrator generates a structured reply per producer: verdict + per-finding table (severity/what/where/fix) + deterministic pre-check results + exact next action. Written to `.review-gate/state/reply-<session>-<timestamp>.md` and announced via `handoff-back` event-log row. The operator is no longer the manual copy/paste message bus.
> 3. **Operator-in-loop guarantees (Step 8):** BLOCKING verdicts + capability-gap decisions are surfaced as drafts — the orchestrator NEVER auto-applies side-effectful outcomes (tracker updates, CG-register entries, handoff status flips). Operator ratifies.
> Built by [RGH-16/RO-FIX]. Composes [RGH-18]+[RGH-19]+[PR-1]. Reuses fleet-orchestration handoff-bus contract.

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

### Step 2 — Run deterministic completeness pre-checks (RGH-18/19)

Before dispatching any LLM reviewer, run the deterministic completeness checks on each manifest item. These are CODE checks — not a reviewer self-report.

**For each manifest item with `gate_tier = full`:**

1. Run RGH-18 (build-correctness):
```bash
python3 ~/workspace/repos/ai-agency-core/scripts/mandatory-review-gate/rgh18-build-correctness.py \
  --session <producer_session> \
  --state-dir ~/workspace/.review-gate/state \
  --workspace-root ~/workspace \
  --handoff <handoff_path> \
  --tier <run_tier>
```

2. Run RGH-19 (doc/knowledge-completeness):
```bash
python3 ~/workspace/repos/ai-agency-core/scripts/mandatory-review-gate/rgh19-doc-completeness.py \
  --session <producer_session> \
  --state-dir ~/workspace/.review-gate/state \
  --workspace-root ~/workspace \
  --handoff <handoff_path> \
  --tier <run_tier>
```

3. Parse JSON output from each. Record the results per item:
   - `rgh18_verdict`: PASS or BLOCKING (with catches list)
   - `rgh19_verdict`: PASS or BLOCKING (with catches list)

4. **Gate logic:**
   - If EITHER returns BLOCKING → mark the manifest item as `DETERMINISTIC-BLOCKED`
   - If BOTH return PASS → mark as `DETERMINISTIC-PASS` (proceed to LLM reviewer dispatch)

5. **For Productize-tier runs:** verify that RGH-19's `checks_run` includes `OC-20` (PR-1 B1-B6 DoD). If OC-20 is absent or SKIP, flag as `DETERMINISTIC-BLOCKED` with reason "Productize-tier requires OC-20 (PR-1 DoD) — not found in RGH-19 output."

**For `fast-path` tier items:** skip this step (RGH-18/19 already run inside `independent-reviewer-dispatch.py` at the per-file level during the LLM review).

**Include deterministic results in the dispatch plan (Step 4)** so the operator sees which items are blocked before LLM dispatch.

### Step 3 — Pre-allocate CR ID ranges

To prevent CR-### collisions when multiple reviewers write to `_review-gate-catch-register.md` concurrently:

1. Read the current highest CR-### ID from the catch register
2. Allocate a range per reviewer: reviewer 1 gets CR-(N+1) through CR-(N+20), reviewer 2 gets CR-(N+21) through CR-(N+40), etc.
3. Include the allocated range in each reviewer's dispatch prompt

### Step 4 — Render the dispatch plan

For each manifest item, render one row:

| # | Producer chat | Session | Files | Tier | Handoff | CR range | Deterministic |
|---|---|---|---|---|---|---|---|

The **Deterministic** column shows the Step 2 result:
- `PASS` — both RGH-18 + RGH-19 passed; LLM reviewer will be dispatched
- `BLOCKED (N catches)` — deterministic checks found problems; LLM reviewer SKIPPED
- `—` — fast-path tier (deterministic pre-checks not run at orchestrator level)

For DETERMINISTIC-BLOCKED items, render the blocking catches below the table:
```
⛔ <chat_id> — DETERMINISTIC-BLOCKED:
  RGH-18: <verdict> — <catch summary>
  RGH-19: <verdict> — <catch summary>
```

Plus:
- **Dispatch shape:** parallel (all DETERMINISTIC-PASS reviewers fire concurrently via Agent tool; BLOCKED items skipped)
- **Edit-zone analysis:** verdict files are per-session-namespaced (no collision); firing-tracker rows are append-only (low collision, but reviewers must use their allocated CR range); catch-register uses pre-allocated CR-### ranges (no collision)
- **Estimated wall-clock:** ~5-15 min per review (parallel, so total ≈ slowest reviewer)

### Step 5 — Operator confirms the dispatch plan

Operator says `approve` / `edit` / `abort`. No reviewers fire until approved.

For DETERMINISTIC-BLOCKED items, the operator can:
- `approve` — accept the block; those items go straight to the producer-reply (Step 9) with the deterministic findings
- `override <item>` — force LLM dispatch despite the deterministic block (rare — e.g., if a deterministic check is a known false-positive)
- `abort` — cancel everything

### Step 6 — Dispatch reviewers in parallel

For each DETERMINISTIC-PASS manifest item (and any DETERMINISTIC-BLOCKED items the operator overrode), fire an Agent sub-agent with the dispatch prompt from `references/dispatch-contract.md`. All items dispatch in a single message (parallel Agent tool calls). DETERMINISTIC-BLOCKED items (not overridden) are skipped.

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

### Step 7 — Collect results + render summary

As each reviewer completes, collect its result. Merge with deterministic pre-check results from Step 2. Render a summary table:

| # | Producer | Deterministic | LLM Review | Final Verdict | Passes | Catches | CR IDs | Gate cleared? |
|---|---|---|---|---|---|---|---|---|

**Final verdict logic:**
- DETERMINISTIC-BLOCKED (not overridden) → BLOCKING (deterministic catches only)
- DETERMINISTIC-PASS + LLM PASS → PASS
- DETERMINISTIC-PASS + LLM BLOCKING → BLOCKING (LLM catches)
- Overridden DETERMINISTIC-BLOCKED + LLM result → use LLM result (but note the override)

### Step 8 — Surface BLOCKING verdicts + operator-in-loop gate

If any item has a BLOCKING final verdict (deterministic or LLM): surface the findings to the operator with the specific catches and the producer chat that needs fixes.

**Operator-in-loop guarantees (non-negotiable):**

1. **BLOCKING ratification:** The orchestrator surfaces BLOCKING verdicts and their findings. It does NOT auto-resolve. The operator decides: accept the block (producer must fix) or override (rare, with justification).

2. **Capability-gap (CG) decisions:** If any finding involves a capability gap (e.g., "this check can't verify X because the tool doesn't exist"), the orchestrator DRAFTS a CG-register entry (`_meta/handoffs/_capability-gap-register.md`) but does NOT write it. Present the draft to the operator; operator confirms or edits before the write.

3. **Side-effectful outcomes:** The orchestrator NEVER auto-applies:
   - Handoff status flips (e.g., `status: consumed`)
   - Tracker row moves (e.g., Active → _recently-closed)
   - CR-register entries for capability gaps
   - Any write outside the review-gate edit zone

   These are DRAFTED in the producer-reply (Step 9) as recommended actions. The operator or producer executes them.

### Step 9 — Generate producer-reply

For each reviewed producer, generate a structured reply that the operator can forward (or that the producer's auto-watch picks up via the handoff-bus).

**Reply format:**

```markdown
═══ REVIEWER → PRODUCER: {{chat_id}} ═══

**Verdict:** PASS / BLOCKING
**Producer session:** {{producer_session}}
**Reviewed by:** reviewer-orchestrator v3.0 (session {{orchestrator_session}})
**Deterministic pre-checks:** RGH-18 {{rgh18_verdict}} / RGH-19 {{rgh19_verdict}}

## Findings

| # | Source | Severity | What | Where | Fix |
|---|---|---|---|---|---|
| 1 | RGH-18 | blocking | ... | file:line | ... |
| 2 | RGH-19 | blocking | ... | file:line | ... |
| 3 | LLM-R1 | blocking | ... | file:line | ... |
| 4 | LLM-R1 | advisory | ... | file:line | ... |

**Source** column: `RGH-18` / `RGH-19` = deterministic check; `LLM-R<N>` = LLM reviewer pass N.

## Next action

[If PASS]:
- Close out. Run session-end protocol. Propose commits.
- Firing-tracker rows + catch-register entries already written by the reviewer.

[If BLOCKING]:
- Fix the {{N}} blocking finding(s) above.
- Re-run: post a new `ready-for-review` event-log row after fixes land.
- The orchestrator will re-dispatch on the next tick (Phase 2) or manual trigger (Phase 1).

═══ END REPLY ═══
```

**Delivery:**

1. **Write reply file:** `~/workspace/.review-gate/state/reply-{{producer_session}}-{{timestamp}}.md`

2. **Append handoff-bus event to `_event-log.md`:**
```
<timestamp> | .review-gate/state/reply-{{producer_session}}-{{timestamp}}.md | handoff-back | {{orchestrator_chat_id}} | [RGH-16] Reviewer-orchestrator reply for {{producer_chat_id}}: verdict {{verdict}}, {{N}} findings ({{M}} blocking). Reply at .review-gate/state/reply-{{producer_session}}-{{timestamp}}.md. Orchestrator session {{orchestrator_session}} ≠ producer session {{producer_session}}.
```

3. **Render the reply inline** in the orchestrator session so the operator can see it immediately. The operator can:
   - Forward it to the producer (paste or voice)
   - Let the producer's auto-watch pick it up via the `handoff-back` event (when producer-side auto-watch is implemented per fleet-orchestration design)

### Step 10 — Append event-log rows

For each completed review, append an event-log row (in addition to the handoff-bus row from Step 9):

```
<timestamp> | <files> | reviewer-orchestrator-dispatched-review | <orchestrator-chat-id> | [RGH-9] Independent review dispatched by reviewer-orchestrator: <producer_chat_id> verdict <PASS|BLOCKING>, <N> passes, <M> catches. Deterministic pre-checks: RGH-18 <verdict> / RGH-19 <verdict>. Reviewer session <orchestrator_session> ≠ producer session <producer_session>.
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

### Step W4 — Dispatch flow (reuses Phase 1 Steps 2–10)

This is the same as Phase 1:

1. **Step 2** — Run deterministic completeness pre-checks (RGH-18/19).
2. **Step 3** — Pre-allocate CR ID ranges.
3. **Step 4** — Render the dispatch plan (includes deterministic results).
4. **Step 5** — **Operator confirms the dispatch plan.** No reviewers fire until approved. This is the no-silent-dispatch guarantee.
5. **Step 6** — Dispatch reviewers in parallel (Agent tool). DETERMINISTIC-BLOCKED items skipped.
6. **Step 7** — Collect results + render summary (merged deterministic + LLM).
7. **Step 8** — Surface BLOCKING verdicts + operator-in-loop gate.
8. **Step 9** — Generate producer-reply (write reply file + handoff-bus event).
9. **Step 10** — Append event-log rows.

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

Phase 3 wires into vault-orchestrator Mode 6's Step 10 wave-close: when a wave closes with all sub-agents PASS, Mode 6 posts a `ready-for-review` event-log row and the reviewer-orchestrator auto-dispatches the independent review. The operator's only gate is the dispatch-plan confirmation (Step 5). Deterministic pre-checks (Step 2) and producer-reply (Step 9) run automatically.

## Honest limits

1. **Independent of producers, not of each other.** Dispatched reviewers share the orchestrator's session context. They are independent of each producer (different session), but not of each other. The strongest isolation (separate processes) is RGH-3/Hermes territory — complementary, not replaced by this.

2. **Runs on Claude Code (Agent tool).** This does NOT make Hermes unattended runs trustworthy — that's RGH-3's job. This automates the operator's manual reviewer-spawning workflow on Claude Code.

3. **Verdict file is model-authored.** Until the reviewer runs as an isolated process (RGH-3 Phase 2/3), the verdict file is model-authored. The operator remains the integrity backstop — spot-check verdict files in `.review-gate/state/`.

4. **CR range pre-allocation is an estimate.** If a reviewer finds >20 catches (the default range size), it must stop at the range boundary and report "CR range exhausted" — the orchestrator re-allocates and re-dispatches. This is unlikely in practice (median catch count is 3-5 per review).

5. **Agent sub-agents may produce shallower reviews than full separate-session reviewers.** The Agent tool dispatches a sub-agent with a single prompt — it runs autonomously without operator paste-back loops. This ensures session-independence (the mechanism) but not review depth (the adversarial rigor). For high-stakes artifacts, a full separate-session running review (operator relays each producer output, reviewer disk-verifies step-by-step per mandate Phase R) remains the gold standard. The orchestrator-dispatched review is best suited for: re-verification of already-reviewed artifacts, fast-path tier files, and parallel batch reviews where mechanism-independence matters more than maximum adversarial depth.

6. **Session ID inheritance is version-dependent.** Confirmed on CC v2.1.85 (2026-06-12). Re-verify after Claude Code upgrades — if Agent tool stops inheriting parent session_id, the independence mechanism breaks silently. The `log-review-pass.py` rejection check is the safety net (it will reject same-session attempts), but the orchestrator becomes unable to clear the gate.

7. **Watcher is session-scoped, not a daemon (Phase 2).** The polling loop only runs while the Claude Code session is active. If the operator closes the session or the conversation compresses past the watcher state, the loop stops. Background/unattended watching is RGH-3/Hermes territory. The watcher is best suited for: operator working sessions where multiple producers are in flight and reviews should be dispatched as they land.

8. **Watcher deduplication is per-session (Phase 2).** The `dispatched_sessions` set prevents re-dispatching within a single watch session. If the orchestrator session restarts, it re-scans from scratch — but the cross-check against `.review-gate/state/` markers prevents duplicate reviews (items with existing PASS markers are skipped). The only gap: if a reviewer was dispatched but hasn't yet written its marker, a new orchestrator session could re-dispatch. Mitigated by the operator dispatch-plan gate (Step 4) — the operator sees "already dispatched by prior session" context.

9. **Deterministic pre-checks enforce presence and structure, not insight quality (v3.0).** RGH-18 verifies build outputs exist and pass structural checks (placeholder sweep, leak audit, staging audit). RGH-19 verifies documentation completeness (exec-log substantiveness, evidence-per-DoD-item, pattern tracking, catches referenced, no silent deferrals, knowledge-capture audit, spec-vs-registry cross-check, Productize-DoD). Neither checks whether the *content* is correct, insightful, or well-written — that remains the LLM reviewer's job. The deterministic checks are a floor, not a ceiling.

10. **Producer-reply is model-authored (v3.0).** The structured reply (Step 9) is generated by the orchestrator model, not a deterministic script. The findings table faithfully reproduces deterministic and LLM outputs, but the "Next action" section is model-composed. The operator should review the reply before forwarding to the producer if the findings are complex or ambiguous.

11. **Handoff-bus is one-way until producer-side auto-watch ships (v3.0).** The `handoff-back` event-log row is written, but the producer doesn't auto-detect it yet — the operator still forwards the reply manually (or the producer greps the event log). Full bidirectional auto-watch is fleet-orchestration territory (see `_meta/handoffs/fleet-orchestration/`).

## Related

- `[[independent-reviewer-mandate]]` — the fixed instruction set each dispatched reviewer loads
- `[[gate-peer-reviewer]]` — the skill that defines gate types and review procedures
- `log-review-pass.py` — the gate-clearing script with the independence check (lines 99-119)
- `rgh18-build-correctness.py` — deterministic build-correctness gate (Step 2, [RGH-18])
- `rgh19-doc-completeness.py` — deterministic doc/knowledge-completeness gate (Step 2, [RGH-19])
- `[[handoff-2026-06-22-reviewer-orchestrator-mode7]]` — the originating handoff (RGH-9)
- `[[handoff-2026-06-24-rgh16-reviewer-orchestrator-completeness-and-reply]]` — completeness + reply handoff (RGH-16)
- `[[handoff-2026-06-09-phase-3-hermes-daemon-enforcement]]` — RGH-3, the complementary isolated-process reviewer
- `_meta/handoffs/fleet-orchestration/` — handoff-bus design (producer-reply delivery mechanism)
- vault-orchestrator Mode 6 — the wave-execution control plane (Phase 3 binds into its wave-close)
