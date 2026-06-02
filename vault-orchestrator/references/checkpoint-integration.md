# Checkpoint integration

How PROVISION bakes the chat-resilience checkpoint convention into drafted handoffs so long-running chats can resume mid-work after a crash, sandbox loss, or context-window exhaustion.

The checkpoint convention itself lives in [[../../multi-chat-coordination/references/chat-resilience-checkpoints]] (Phase 1 of the vault-orchestrator project). This reference covers what PROVISION does with that convention during decomposition — when to include a checkpoint reminder, where it lands in the handoff body, and what it asks the spawning chat to do.

## When PROVISION includes the checkpoint reminder

PROVISION adds a "Chat-resilience checkpoint reminder" section to a drafted handoff when **any** of these triggers fire:

| Trigger | Threshold |
|---|---|
| Estimated build time | > 2 hours (matches the chat-resilience convention's default threshold) |
| Number of deliverables | > 5 distinct files (resuming-from-zero rebuilds a lot) |
| Multi-session shape | Handoff body names "across sessions" or "operator-paced" or includes operator gates (Higgsfield gate, manual approvals, calendar holds) |
| Research-heavy shape | Handoff body names "deep research" or "many sources" or "synthesis" (accumulated context is expensive to lose) |

For handoffs that miss every trigger (short, single-deliverable, no operator gates), PROVISION skips the checkpoint reminder. Adding the reminder to a 30-minute handoff is noise.

The decision is recorded inline in the PROVISION output: "Included checkpoint reminder in Phases 2, 3, 4 (each >2h); skipped Phase 1 (45min, single-file)."

## What the checkpoint reminder section looks like

PROVISION inserts the following section into the handoff prompt body, placed **between the work description and the Closing Protocol**:

```markdown
## Chat-resilience checkpoint reminder

This handoff is estimated at <range>h, which crosses the chat-resilience checkpoint threshold. If you are still working after ~90 minutes of focused execution, append a `### Checkpoint` block to this chat's row in the tracker's Active table.

Checkpoint shape (from [[../../skills/multi-chat-coordination/references/chat-resilience-checkpoints|chat-resilience convention]]):

- `### Checkpoint <YYYY-MM-DD HH:MM>` heading
- `Last completed step:` <one-line, specific>
- `Next step:` <one-line, specific>
- `Open files:` <comma-separated list>
- `Outstanding tool calls:` <list or "none">
- `Resume-prompt:` "<verbatim text a fresh chat would paste to resume>"

Skip checkpointing if you finish within ~90 minutes — the deliverable itself is the checkpoint.

If a checkpoint exceeds ~500 characters, write it to a sister file at `_meta/handoffs/<project-slug>/_checkpoint-<chat-slug>-YYYY-MM-DD-HHMM.md` and put a wikilink in the Notes cell instead.
```

The section is self-contained — the chat reads it and decides whether to checkpoint without needing to re-read the convention spec.

## Why this is part of PROVISION rather than the closing protocol

The closing protocol runs at chat **end** (flip status, move rows, propose git commits). Checkpoints exist for chat **mid-flight** — between the opening and closing. They're an orthogonal discipline, not a closing-protocol step.

Baking the reminder into the handoff body (above the closing protocol) means the chat reads about checkpoints early, decides whether the work fits the trigger, and integrates the discipline into its execution flow. Leaving it to the closing protocol would be too late — by closing time, the chat is shipping; the value of a checkpoint is when the chat might die before then.

## What PROVISION does NOT do for checkpoints

- It does not write the checkpoint itself. The chat writes its own checkpoint mid-flight.
- It does not enforce checkpointing. The chat can ignore the reminder if the work shape doesn't fit.
- It does not modify the chat-resilience convention. Convention edits belong to the multi-chat-coordination skill, not the orchestrator.
- It does not add reminders to short handoffs (≤2h, single-deliverable). Convention noise is its own failure mode.

## How PROVISION decides the threshold value per handoff

PROVISION reads the drafted handoff's `## Status` section for the `Estimated build time:` line. Parsing rules:

- "~2-3 hours" → midpoint = 2.5h → above threshold → include reminder
- "~30-45 minutes" → midpoint = 37.5min → below threshold → skip reminder
- "3-4 hours" without "~" → midpoint = 3.5h → above threshold → include reminder
- "1-2 hours" → midpoint = 1.5h → below threshold → skip reminder unless other trigger fires (deliverable count, multi-session, research-heavy)

If the estimate is missing or malformed, PROVISION includes the reminder by default (err toward more discipline, not less).

## Integration with the closing protocol

The closing protocol (inserted verbatim from `references/closing-protocol-template.md` in the multi-chat-coordination skill) sits **after** the checkpoint reminder section. Order inside the prompt body:

```
1. Opening Protocol (verbatim from opening-protocol-template)
2. Read these in order (handoff-specific context)
3. What you're building (handoff-specific work)
4. Out of scope (handoff-specific)
5. Files to edit (handoff-specific)
6. Files to create (handoff-specific)
7. Status (estimated time, blockers)
8. Chat-resilience checkpoint reminder (inserted by PROVISION if triggered)
9. What's next to spawn after this ships (handoff-specific)
10. Closing Protocol (verbatim from closing-protocol-template)
```

Sections 8 and 10 are both inserted by PROVISION — 8 conditionally based on triggers, 10 always.

## Examples

**Example 1 — Reminder included.** Drafted handoff "EV blog content calendar Phase 2: research + scoring rubric" estimated at 3-4 hours, produces 6 files (research brief + scoring rubric + 4 source notes), research-heavy. Triggers: time > 2h, deliverables > 5, research-heavy. PROVISION includes the reminder.

**Example 2 — Reminder skipped.** Drafted handoff "EV blog content calendar Phase 1: pick the content pillars" estimated at 45-60 minutes, produces 1 file (`pillars.md`), single decision focus. No triggers fire. PROVISION skips the reminder.

**Example 3 — Reminder included via multi-session shape.** Drafted handoff "S&H first-real-run orchestrator test" estimated at 5-8 hours autonomous + operator-attended Higgsfield gate. Time > 2h AND multi-session (operator gate). Both triggers fire. PROVISION includes the reminder.

**Example 4 — Reminder included via missing estimate.** Drafted handoff body has no `Estimated build time:` line (operator pasted a goal too quickly during DECOMPOSE). PROVISION defaults to including the reminder and adds a note in the PROVISION output: "Phase 2 missing time estimate; checkpoint reminder included by default."

## See also

- [[../SKILL|vault-orchestrator SKILL.md]] — PROVISION mode invokes this logic during handoff drafting
- [[../../multi-chat-coordination/references/chat-resilience-checkpoints|chat-resilience convention spec]] — the convention itself
- [[../../multi-chat-coordination/references/closing-protocol-template|closing-protocol template]] — what sits below the checkpoint reminder
- [[../../multi-chat-coordination/references/opening-protocol-template|opening-protocol template]] — what sits at the top of the same handoff body
- [[spawn-queue-shape|spawn-queue-shape reference]] — where the drafted handoff with reminder lands
- [[edit-zone-conflict-detection|edit-zone-conflict-detection reference]] — orthogonal discipline (conflicts catch race conditions; checkpoints catch mid-flight death)
