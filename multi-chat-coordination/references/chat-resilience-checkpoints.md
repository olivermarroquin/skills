# Chat-resilience checkpoints — Optional convention

When a Cowork chat does long-running work and the operator wants resilience against mid-work death (chat crashes, sandbox loss, context-window exhaustion), the chat can periodically append a `### Checkpoint` block to its row in the active tracker. A fresh chat opened later can read the checkpoint and resume from intermediate state instead of restarting from the original handoff.

Phase 1 of the vault-orchestrator project (2026-05-30) shipped this convention. Checkpoints are **optional** — most short chats (under ~1 hour, single-file deliverable) skip them entirely. The convention exists for long-running work where resuming-from-zero is expensive.

## When to checkpoint

A chat should consider checkpointing when:

- Estimated duration > 2 hours OR
- Work spans multiple sessions (operator may close the chat and come back later) OR
- Deliverables include >5 files (resuming-from-zero rebuilds a lot) OR
- The chat is mid-research and has accumulated significant context the operator would lose if the chat died

Skip checkpointing when:

- The chat is short and the deliverable is single-file (just rerun the handoff)
- The work is fully captured in the per-task execution log (which already serves as a checkpoint of sorts)

## Where the checkpoint lives

The checkpoint block lives in the **Notes cell of the chat's row in the tracker's "Active / in-flight chats" table**. Both the master tracker and per-project trackers (per [[project-chat-tracker-shape]]) accept checkpoint blocks in the same place.

Example row with a checkpoint:

```markdown
| 2026-05-30 | vault-orchestrator Phase 1 | [[vault-orchestrator/phase-1-per-project-chat-tracker-shape\|Phase 1 handoff]] | ⏳ In-flight | 2-3 hours | Building per-project tracker shape spec. ### Checkpoint 2026-05-30 14:30 — Last completed step: project-chat-tracker-shape.md written + project-status-digest-shape.md written. Next step: write chat-resilience-checkpoints.md (this file). Open files: skills/multi-chat-coordination/references/project-status-digest-shape.md. Outstanding tool calls: none. Resume-prompt: "Resume vault-orchestrator Phase 1 from checkpoint 2026-05-30 14:30. Read ~/workspace/second-brain/_meta/handoffs/vault-orchestrator/phase-1-per-project-chat-tracker-shape.md for full context. Two reference files already shipped: project-chat-tracker-shape.md + project-status-digest-shape.md. Pick up at: write chat-resilience-checkpoints.md per the shape in §3 of the handoff." |
```

The Notes cell becomes longer with a checkpoint but stays parseable. Markdown tables tolerate long cells; the line wraps in editors but the rendered table is intact.

**Alternative for very long checkpoints:** if the checkpoint exceeds ~500 characters and the Notes cell becomes awkward, write the checkpoint into a sister file at `_meta/handoffs/<project-slug>/_checkpoint-<chat-slug>-YYYY-MM-DD-HHMM.md` and put a wikilink in the Notes cell: `### Checkpoint — see [[<project-slug>/_checkpoint-<chat-slug>-2026-05-30-1430]]`. The sister-file path is opt-in; inline checkpoints are the default.

## Checkpoint shape

```markdown
### Checkpoint <YYYY-MM-DD HH:MM>

Last completed step: <one-line — what just finished>
Next step: <one-line — what to do next>
Open files: <comma-separated list of paths the chat was editing>
Outstanding tool calls: <list of in-flight calls, or "none">
Resume-prompt: "<verbatim text the operator pastes into a new chat to resume>"
```

Field rules:

- **`<YYYY-MM-DD HH:MM>`** — timestamp of the checkpoint, ISO date + 24h time. Lets the operator see how stale a checkpoint is at a glance.
- **`Last completed step:`** — one line describing what was just finished. Specific, not vague. "Wrote project-chat-tracker-shape.md" beats "made progress on specs."
- **`Next step:`** — one line describing what to do next. Specific, not vague. "Write chat-resilience-checkpoints.md per §3 of the handoff" beats "continue the work."
- **`Open files:`** — comma-separated list of files the chat was actively editing or had open in context. Helps a fresh chat know which files to re-read first.
- **`Outstanding tool calls:`** — list of tool invocations that were in-flight when the checkpoint was written (e.g., "WebSearch for 'X'", "perplexity-refinement on Y"). If none, write `none`. Helps a fresh chat decide whether to retry or skip.
- **`Resume-prompt:`** — the load-bearing field. The verbatim text the operator pastes into a fresh Cowork chat to resume. Should be self-contained — include enough context that the resuming chat can pick up without re-reading the entire prior chat. References to the original handoff are encouraged; don't restate the handoff in the resume-prompt.

## When to update a checkpoint

Append-only is the default — multiple `### Checkpoint <timestamp>` blocks stacked in the Notes cell as the chat progresses. The freshest one wins; older checkpoints serve as audit trail of progress within the chat. A fresh chat reading the row reads the bottommost (most recent) checkpoint and resumes from there.

Lighter discipline alternative: overwrite the prior checkpoint when writing a new one — single checkpoint in the cell, always reflects current state. Trade-off: loses progress history within the chat, but keeps the Notes cell compact. Either pattern is valid; the chat picks one and stays consistent.

## When a checkpoint isn't needed (and shouldn't be added)

- **Single-step chats** — if the chat's whole deliverable is one file, a checkpoint mid-way adds noise without value. Just finish or rerun.
- **Chats with strong execution logs** — if the chat is already writing a detailed execution log per `~/workspace/CLAUDE.md` Knowledge Capture Protocol, the execution log IS the checkpoint. Don't double-write.
- **Recently-started chats** — the original handoff already serves as the "start here" instructions. No checkpoint needed within the first hour.

Checkpoints exist to bridge mid-work death — they're not progress reports. Don't gamify them.

## Composition with the Closing Protocol

When a chat ships, the Closing Protocol moves the row from "Active / in-flight" to "Recently closed". The checkpoint history in the Notes cell typically gets discarded at that point (the "Outcome" cell in Recently closed replaces it with the shipped-state summary). If the checkpoint history is worth preserving as audit trail, the closing-protocol run optionally appends it to the handoff body under a `## Checkpoint history` H2 before flipping the handoff to consumed. Most chats won't need this; long-running multi-session chats might.

## Composition with chat-resumption

When the operator pastes the `Resume-prompt:` into a fresh chat, the resuming chat:

1. Reads the prompt verbatim.
2. Re-reads the original handoff file (named in the prompt).
3. Re-reads the `Open files:` listed in the checkpoint.
4. Decides whether to retry `Outstanding tool calls:` or skip them (case-by-case judgment).
5. Picks up at the `Next step:` line and continues.

The resuming chat does NOT need to re-run the Opening Protocol (the row is already in "Active / in-flight" — that's why this is a resume, not a fresh spawn). It DOES need to bump the tracker's `last-change:` to note the resumption and append a fresh `### Checkpoint` block reflecting the new state.

## Lightweight pattern: silent resumption

A chat that dies and is resumed by the same operator within the same session often doesn't need a formal checkpoint. The operator opens a new chat, says "I was working on X, resume from Y" in conversational language, and the fresh chat picks up. The formal `### Checkpoint` convention exists for harder cases — multi-day gaps, multi-operator scenarios, automated future resumption (Phase 3+ orchestrator may auto-resume based on checkpoints).

## See also

- [[project-chat-tracker-shape]] — the per-project tracker the Notes-cell checkpoint lives in
- [[tracker-row-shapes]] — the master tracker's Notes-cell shape (same convention)
- [[closing-protocol-template]] — how a chat closes when checkpointed (may preserve checkpoint history in the handoff body)
- `~/workspace/CLAUDE.md` § Knowledge Capture Protocol — execution logs (the per-task log substrate; checkpoints complement, don't replace)
- `~/workspace/second-brain/_meta/handoffs/vault-orchestrator/phase-3-orchestrator-v1-survey-and-next-moves.md` — Phase 3 may auto-detect checkpoints during SURVEY mode and surface them in the state-of-vault report
