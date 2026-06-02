# Spawn-queue shape

The substrate-agnostic shape of `~/workspace/second-brain/_meta/handoffs/_spawn-queue.md`. The file is the audit trail for every chat the orchestrator has provisioned, regardless of how the spawn actually fires (Claude Code Task tool, Cowork paste, future Hermes-harness). PROVISION writes to it; the operator consumes it; future automation reads it.

Why substrate-agnostic matters: today Cowork has no chat-creation API, so spawning is operator-pasted. Tomorrow the spawn might be Claude Code Task tool, the day after a host-machine harness. Each consumer reads the same queue file — only the "how to deliver the prompt" step differs. The queue shape stays stable across substrate evolution.

## Frontmatter

```yaml
---
type: spawn-queue
status: active
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
last-change: '<YYYY-MM-DD> — <5-15 word summary of what this pass did> — see [[_active-chats-tracker-changelog]]'
tags: [meta, spawn-queue, vault-orchestrator, substrate-agnostic]
---
```

- `type: spawn-queue` — distinguishes from `tracker`, `tracker-changelog`, `handoff`
- `status: active` — queue is in use; rarely flipped (the file persists across PROVISION runs)
- `created` / `updated` — standard
- `last-change` — single-quoted free-form prose, parsed for the "what just changed" hover; full prose lives in the tracker changelog
- `tags` — discovery; include the orchestrator + substrate-agnostic marker

## Body sections (in order)

```
# Chat spawn queue
<2-3 paragraph framing — what this file is, how operator approves a spawn (either substrate), what makes it substrate-agnostic>

## How to use
<6-step numbered list — read summary, verify substrate, check conflicts, spawn via Task or paste, mark consumed, repeat>

## Operator-fatigue ceiling
<10-hour ceiling description + current queue total>

## 🔵 Queued (ready to spawn)
<empty-state message OR table of rows. Schema in comment.>

## 🟢 Recently spawned (past 7 days)
<empty-state message OR table of rows. Schema in comment.>

## ⚠️ Conflict flags
<empty-state message OR table of rows. Schema in comment.>

## See also
<wikilinks to skill, references, master tracker, handoffs README>
```

## Row schemas

### Queued row

| Field | Content |
|---|---|
| `#` | Row number, monotonic per PROVISION run; renumbered if rows reorder |
| Chat name | Human-scannable name; matches the master-tracker "Chat name" cell that this row will become when spawned |
| Handoff pointer | `[[path/to/handoff\|short-label]]` wikilink |
| Substrate rec | `claude-code` \| `cowork` \| `either`; matches the handoff's `preferred-substrate:` frontmatter |
| Estimated time | Range from handoff body (e.g., `~3-4h`) |
| Conflicts | `none` OR `flagged → see conflict table` (the link goes to a specific row in the Conflict flags table) |
| Prompt | `<details><summary>Click to expand</summary>\n\n```\n<verbatim prompt body, paste-ready for either substrate>\n```\n\n</details>` — the prompt is exactly what the operator would paste into a Cowork window OR exactly what Claude Code Task tool sees as the sub-agent's instructions |

The prompt cell is wrapped in `<details>` so the table stays scannable when collapsed. Expanding shows the full prompt for copy-paste.

### Recently spawned row

| Field | Content |
|---|---|
| Spawned | `YYYY-MM-DD` of the spawn event |
| Chat name | Matches the Queued row that was spawned |
| Handoff | Wikilink to the handoff (same as Queued row) |
| Substrate used | `claude-code-task` \| `cowork-paste` \| `hermes-harness`; the actual substrate, not the recommendation |
| Outcome | One-line outcome: `still in-flight`, link to closed-chat row in master tracker, or short failure note |

Recently-spawned rows are kept for 7 days. Older rows archive to `_spawn-queue-archive.md` quarterly per existing cleanup discipline.

### Conflict flag row

| Field | Content |
|---|---|
| Conflicts with | Pair description: `Row N (queued) ↔ "Chat X" (in-flight, started YYYY-MM-DD)` |
| Shared file | Path to the file both chats touch |
| Suggested resolution | `serialize` \| `split-handoff` \| `accept-risk (operator override required)` — see [[edit-zone-conflict-detection]] for severity scoring |

## Invariants

These hold across every PROVISION write. Violating any of them is a contract bug and should fail the write.

**1. Append-only at the bottom of "Queued".** PROVISION never inserts in the middle of the Queued table (renumbering existing rows is allowed when the operator explicitly asks for a reorder). New rows go at the bottom with the next row number.

**2. Move-don't-strikethrough on spawn.** When a row spawns, it MOVES from Queued to Recently spawned. No strikethrough left behind. Same discipline as the master tracker — destination section is canonical.

**3. Conflict-flag table is regenerated, not appended.** Each PROVISION run rebuilds the Conflict flags table from current Queued + in-flight handoff file-sets. Stale flags don't accumulate.

**4. Substrate rec matches handoff frontmatter.** The `preferred-substrate:` field on the drafted handoff is the source of truth. If the queue row diverges, the queue row is wrong (re-render the queue from the handoff).

**5. Prompt body is verbatim.** The prompt inside `<details>` is exactly what the operator would paste — no abbreviation, no "...", no editorial summary. The prompt includes the full Opening Protocol (mandatory) and Closing Protocol (mandatory) per the closing-protocol-template.

**6. Empty states have explicit messages.** When Queued / Recently spawned / Conflict flags are empty, render the empty-state message ("No queued chats. Run vault-orchestrator PROVISION mode..."), not an empty table. Empty tables look broken; empty-state messages are honest.

**7. YAML parses after every write.** Standard regex YAML check applies. The `last-change` line uses single-quote wrapping because the prose often contains colons.

**8. The queue is the audit trail.** Once a row lands in Recently spawned, it stays until quarterly archive. Audit means audit — no silent deletes.

## Why this shape

**Substrate-agnostic by design.** Each row carries a recommended substrate but the prompt itself is paste-ready for either Cowork or Claude Code. The harness-future operator can read the queue and route via any substrate without re-rendering the queue.

**One file, three tables.** Queue activity is naturally three-phase (queued → spawned → conflict-noted). Three tables in one file keeps the audit trail local; splitting into three files would fragment.

**Hand-editable.** The operator can reorder rows, edit prompts before pasting, add conflict-override frontmatter to a handoff, and the queue regenerates correctly on the next PROVISION run. Nothing in the shape requires a tool to author.

**Compatible with the master tracker.** Row shape mirrors the master tracker's "Ready to spawn" row shape (Chat name + Handoff pointer + Why now) so when a row spawns, the operator's mental model carries over without re-learning.

## Mapping to master tracker

When a queued row spawns and the chat starts, the chat's Opening Protocol moves a corresponding row from "Ready to spawn next" to "Active / in-flight chats" in the master tracker. The spawn-queue row moves to Recently spawned with substrate-used noted. The two records are kept in sync:

- Queue is the **provisioning audit trail** (what PROVISION drafted, when, with what conflicts)
- Master tracker is the **execution state** (what's actively running, what's queued at the tracker level, what's closed)

PROVISION writes to both atomically per run: drafts handoff → writes queue row → adds tracker row. If any of the three writes fails, all three roll back (handoff written but tracker row missing is a contract violation; PROVISION's closing protocol verifies).

## See also

- [[../SKILL|vault-orchestrator SKILL.md]] — PROVISION mode writes to this shape
- [[edit-zone-conflict-detection|edit-zone-conflict-detection reference]] — how the Conflict flags table is built
- [[checkpoint-integration|checkpoint-integration reference]] — what gets baked into long-running handoff prompts
- [[../../../second-brain/_meta/handoffs/_spawn-queue|_spawn-queue.md]] — the live queue file
- [[../../../second-brain/_meta/handoffs/_active-chats-tracker|master tracker]] — execution state companion
