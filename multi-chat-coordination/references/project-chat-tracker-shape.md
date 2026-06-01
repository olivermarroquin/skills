# Per-project chat-tracker shape — Data contract

The data contract for `_chat-tracker.md` files. One lives at the root of every active project folder under `~/workspace/second-brain/04_projects/`. The per-project tracker is the **project-scoped mirror** of the master tracker at `~/workspace/second-brain/_meta/handoffs/_active-chats-tracker.md` — same visual conventions, same row shapes, same Opening/Closing protocol discipline, but scoped to one project.

Phase 1 of the vault-orchestrator project (2026-05-30) shipped this shape. Every row shape mirrors the master tracker spec at [[tracker-row-shapes]] exactly — DECOMPOSE-generated handoffs register cleanly into either level.

## Why this exists

The master tracker grows past one-tracker-can-hold-it-all as the system scales: 4+ active projects, 30+ closed chats, multiple skill-build initiatives in parallel. Per-project trackers split the load — each project owns its chat state — and the Phase 2 aggregator rolls per-project trackers up into a generated section of the master tracker. Until Phase 2 ships, per-project trackers are read-only placeholders the operator can scan; the master tracker remains the editing surface.

Companion file: every per-project tracker has a `_chat-status.md` digest beside it — the machine-readable contract Phase 2's aggregator parses. Spec at [[project-status-digest-shape]].

## File location

```
~/workspace/second-brain/04_projects/<area>/<active>/<project-slug>/_chat-tracker.md
~/workspace/second-brain/04_projects/<area>/<active>/<project-slug>/_chat-status.md
```

For example:

```
04_projects/clients/_active/ev-electric-services/_chat-tracker.md
04_projects/clients/_active/ev-electric-services/_chat-status.md
04_projects/personal/<project-slug>/_chat-tracker.md
04_projects/personal/<project-slug>/_chat-status.md
```

Filename rule: literal `_chat-tracker.md` and `_chat-status.md`. The underscore prefix sorts them above content folders in directory listings, matching the existing project `_README.md` / `_status.md` / `_intel-inbox.md` discipline.

**Naming collision note.** Some existing projects already have a `_status.md` file holding project-wide status prose (EV-Electric does, last updated 2026-05-22). To preserve that file non-destructively per the Knowledge OS rules, the chat-coordination digest uses `_chat-status.md` — not `_status.md`. The `_chat-` prefix on both files (`_chat-tracker.md` + `_chat-status.md`) signals their purpose: chat-coordination state, not project-wide status.

## Frontmatter

```yaml
---
type: project-chat-tracker
project: <project-slug>
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
last-change: 'YYYY-MM-DD (pass N) — short topic — see [[_chat-tracker-changelog]] (if a changelog exists for this project)'
tags: [meta, chat-tracker, <project-slug>, coordination]
---
```

**Field rules:**

- `type:` — always `project-chat-tracker`. Distinguishes from the master `type: tracker` so Dataview queries can target one or the other.
- `project:` — kebab-case slug matching the parent folder name.
- `status:` — `active` while the project is active; `archived` when the project moves to `_archive/`.
- `last-change:` — same single-quote-wrap rule as the master tracker (the value contains colon-space sequences that break YAML if unquoted). Apostrophes inside the quoted value must be doubled. After every edit, verify YAML parses with the regex-based check from the master tracker convention.
- `tags:` — always includes `chat-tracker` so cross-project Dataview queries can collect every per-project tracker in one query.

## Section order (canonical)

Mirrors the master tracker's section order with the same visual conventions (emoji prefix on header + Obsidian callout on next line). Update the count line whenever rows move in or out of the section.

1. `## How to use this file` (project-scoped — short pointer to the master tracker conventions)
2. `## 🟡 Active / in-flight chats` (yellow `[!warning]`)
3. `## 🔵 Ready to spawn next (blockers cleared)` (blue `[!info]`)
4. `## 🔵 Queued (project-scoped)` (blue `[!note]`) — Tier-2 and Tier-3 collapse into one queue at project scale; the master tracker still tiers them
5. `## 🟡 Open decisions / blockers` (yellow `[!question]`)
6. `## 🟢 Recently closed chats` (green `[!success]`)
7. `## 🟢 Recently completed (past 7 days)` (green `[!success]`)

**Why tiers collapse at project scope.** At master-tracker scale, Tier-2 (within ~1 week) versus Tier-3 (gated on external triggers) is load-bearing — Tier-1 promotion timing matters across the whole vault. At project scope, the same row already lives in the master tracker at its correct tier; duplicating the tier split inside one project's queue just adds maintenance burden without surfacing new signal. One `Queued (project-scoped)` table per project; the master tracker keeps the tier discipline.

Sections that are project-irrelevant are intentionally absent: no `## Scheduled Cowork tasks` (scheduled tasks live in the master tracker; they don't belong to any one project), no `## Hot decisions sitting on Oliver's plate` (vault-wide decision surface stays at the master).

## Table 1 — Active / in-flight chats

```markdown
## 🟡 Active / in-flight chats

> [!warning] N chats currently in flight

| Started | Chat name | Handoff file | Status | Expected duration | Notes |
|---|---|---|---|---|---|
| YYYY-MM-DD | <human-readable name> | [[<handoff-wikilink>\|<short-label>]] | ⏳ In-flight | ~Nh | <free-form notes — optional checkpoint block lives here, see [[chat-resilience-checkpoints]]> |
```

Cell rules match Table 1 in [[tracker-row-shapes]]. Wikilink targets are vault-relative: standalone handoffs at `[[handoff-YYYY-MM-DD-<slug>|<label>]]`; project-folder handoffs at `[[<project-slug>/phase-N-<short>|<label>]]`. Escape the pipe inside wikilinks with `\|`.

**Checkpoint blocks live in the Notes cell.** When a chat is long-running and the operator wants resilience against mid-work death, the chat can append a `### Checkpoint <YYYY-MM-DD HH:MM>` block to the Notes cell. Convention spec at [[chat-resilience-checkpoints]]. Checkpoints are optional; most short chats skip them.

**Empty-state row** (zero in-flight):

```markdown
| (none currently in flight) | | | | | |
```

## Table 2 — Ready to spawn next (blockers cleared)

```markdown
## 🔵 Ready to spawn next (blockers cleared)

> [!info] N chats ready to spawn

| Chat name | Handoff file | Why now |
|---|---|---|
| <human-readable name> | [[<handoff-wikilink>\|<label>]] | <one-paragraph reason — what cleared, what this unblocks, dependencies satisfied> |
```

Cell rules match Table 3 in [[tracker-row-shapes]]. `Why now` is the load-bearing cell.

## Table 3 — Queued (project-scoped)

```markdown
## 🔵 Queued (project-scoped)

> [!note] N chats queued

| Chat name | Handoff file | Trigger to spawn |
|---|---|---|
| <human-readable name> | [[<handoff-wikilink>\|<label>]] | <condition that promotes to Ready-to-spawn — usually a sibling phase shipping or an external dated trigger> |
```

Cell rules match Tables 4 and 5 in [[tracker-row-shapes]] (one combined table at project scope).

## Table 4 — Open decisions / blockers

```markdown
## 🟡 Open decisions / blockers

> [!question] N open items

Captured YYYY-MM-DD so they don't get lost between chats:

1. **<decision or blocker label>** — <one-line context including any calendar gate or waiting-on entity>
2. ...
```

Same bulleted-list shape as the master tracker's "Hot decisions sitting on Oliver's plate" section, scoped to this project. Items here are project-specific (waiting on a client confirmation, blocked on a permit, awaiting a stakeholder approval). Vault-wide decisions still live in the master tracker.

## Table 5 — Recently closed chats

```markdown
## 🟢 Recently closed chats

> [!success] N chats completed (full detail audit trail)

| Closed | Chat name | Handoff | Outcome |
|---|---|---|---|
| YYYY-MM-DD | <human-readable name> | [[<handoff-wikilink>\|<label> (consumed)]] | ✅ **Completed YYYY-MM-DD.** <full outcome paragraph> |
```

Cell rules match Table 2 in [[tracker-row-shapes]]. Long outcome paragraphs are correct. This is the audit trail.

## Table 6 — Recently completed (past 7 days)

```markdown
## 🟢 Recently completed (past 7 days)

> [!success] N entries

| Date | Chat name | Handoff/source | Outcome |
|---|---|---|---|
| YYYY-MM-DD | <human-readable name> | [[<handoff-wikilink>\|<label>]] OR n/a (operator-driven) | <one-paragraph terser outcome> |
```

Cell rules match Table 7 in [[tracker-row-shapes]]. Rolling 7-day window; older rows prune during a tracker pass.

## Visual conventions

Same emoji + Obsidian callout pattern as the master tracker. The mapping table from [[tracker-row-shapes]] applies verbatim — yellow `[!warning]` for active, blue `[!info]` for spawnable, blue `[!note]` for queued, yellow `[!question]` for open decisions, green `[!success]` for closed/completed. Update the count line on every row move.

## Move-don't-strikethrough rule

Same rule as the master tracker. When a row leaves its section (chat spawns, ships, or promotes between tiers), MOVE it — never leave a strikethrough'd pointer. The destination section is the canonical location.

## Opening / Closing Protocol at project scope

A chat that operates inside one project optionally also runs the per-project tracker's Opening/Closing Protocol — same shape as the master tracker, scoped to the project file. Today (pre-Phase-2 aggregator) the operator uses the master tracker as the editing surface, so per-project Opening/Closing Protocols are **optional secondary writes**. Once the Phase 2 aggregator ships, the per-project tracker becomes the primary editing surface for project-scoped chats and the master tracker becomes the aggregated view.

When a chat does run the per-project Opening Protocol, the steps mirror the master:

1. Read the per-project tracker fully.
2. Confirm the handoff is not already in "Active / in-flight chats".
3. Move the row into "Active / in-flight chats" with today's date.
4. Bump frontmatter `last-change` (single-quoted).
5. Verify YAML parses.
6. Begin work.

Closing Protocol mirrors the master Closing Protocol's seven steps — flip handoff frontmatter to consumed, add "Actual deliverable" blockquote, move row to "Recently closed chats", add one-liner to "Recently completed", bump `last-change`, verify YAML, propose git commands. Both protocols additionally update the companion `_chat-status.md` digest (see [[project-status-digest-shape]] for the digest contract).

## YAML safety

Same single-quote-wrap rule as the master. The skill verifies parses with:

```bash
python3 -c "import yaml, re; m = re.match(r'^---\n(.*?)\n---\n', open('04_projects/<area>/<active>/<project>/_chat-tracker.md').read(), re.DOTALL); yaml.safe_load(m.group(1)); print('OK')"
```

Expected output: `OK`. Any other output is a frontmatter error to fix before declaring the edit complete.

## Wikilink conventions

Same as the master tracker — slug-only form for standalone handoffs (`[[handoff-YYYY-MM-DD-<slug>|<label>]]`); project-prefixed form for handoffs inside a project folder (`[[<project-slug>/phase-N-<short>|<label>]]`); always escape the pipe inside wikilinks with `\|`. Per [[../../../second-brain/_meta/conventions]] § slug-only-wikilinks rule.

## How this composes with the master tracker

**Phase 1 (today):** Per-project trackers are scaffolded by hand at project-creation time (or retroactively by the operator for existing projects). The master tracker remains the operator's primary editing surface. Per-project trackers serve as project-scoped reading views — useful when a chat operates entirely inside one project and the operator wants the project's chat state in one file.

**Phase 2 (aggregator skill):** The master-tracker-aggregator skill walks every `_chat-status.md` digest in the vault (read-only), rolls them up into a generated section of the master tracker, and produces a vault-wide state-of-play view. At that point, per-project trackers become the project-scoped editing surface; the aggregator keeps the master view in sync.

**Phase 3+ (orchestrator):** The vault-orchestrator skill calls the aggregator on every SURVEY invocation, ranks spawnable candidates from the rollup, and (Phase 4) drafts handoffs that auto-register into the right per-project tracker.

Until Phase 2 ships, treat per-project trackers as read-only-by-aggregator placeholders. Operators continue to edit the master tracker; per-project trackers are scaffolded once + lightly maintained as project state evolves.

## See also

- [[tracker-row-shapes]] — master-tracker row contract (this spec is the project-scoped mirror)
- [[project-status-digest-shape]] — companion `_chat-status.md` digest the Phase 2 aggregator parses
- [[chat-resilience-checkpoints]] — optional `### Checkpoint` block convention for the Notes cell
- [[handoff-frontmatter-spec]] — handoff frontmatter contract (referenced by every tracker row)
- [[closing-protocol-template]] — closing-protocol baked into every DECOMPOSE-generated handoff; at Phase 2+ this updates both the master tracker AND the per-project tracker + digest
- `~/workspace/second-brain/_meta/conventions.md` — vault-wide naming and frontmatter rules
- `~/workspace/second-brain/_meta/handoffs/_active-chats-tracker.md` — the master tracker this spec mirrors
- `~/workspace/second-brain/_meta/handoffs/vault-orchestrator/_README.md` — the project that produced this spec
