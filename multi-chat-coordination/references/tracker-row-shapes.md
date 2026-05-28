# Tracker Row Shapes — Data Contract

The active-chats tracker at `~/workspace/second-brain/_meta/handoffs/_active-chats-tracker.md` has **six tables plus a "Hot decisions" bulleted list**. Each table has a fixed column shape. This file is the data contract the multi-chat-coordination skill uses when reading existing rows and writing new ones. Match these shapes exactly — Dataview queries elsewhere in the vault may depend on the column order.

## Table 1 — Active / in-flight chats

```markdown
## Active / in-flight chats

| Started | Chat name | Handoff file | Status | Expected duration | Notes |
|---|---|---|---|---|---|
| YYYY-MM-DD | <human-readable name> | [[<handoff-wikilink>\|<short-label>]] | ⏳ In-flight | ~Nh | <free-form notes> |
```

**Cell rules:**
- `Started`: ISO date the chat opened.
- `Chat name`: short human-readable label. Match the handoff's purpose; don't restate it.
- `Handoff file`: wikilink to the handoff. Use the slug-only form for standalone handoffs (`[[handoff-YYYY-MM-DD-<slug>|<label>]]`) or the project-prefixed form for handoffs inside a project folder (`[[<project-slug>/phase-N-<short>|<label>]]`). Escape the pipe inside the wikilink with `\|` so the table renders.
- `Status`: always `⏳ In-flight` while listed here. Other statuses migrate to other tables.
- `Expected duration`: rough estimate ("~2h", "~half day", "~1 session"). Honest is better than precise.
- `Notes`: optional free-form. Often used for concurrency callouts ("running alongside Phase 3a") or scope-creep flags.

**Empty-state row** (when nothing in-flight):
```markdown
| (none currently in flight) | | | | | |
```

## Table 2 — Recently closed chats

```markdown
## Recently closed chats

| Closed | Chat name | Handoff | Outcome |
|---|---|---|---|
| YYYY-MM-DD | <human-readable name> | [[<handoff-wikilink>\|<label> (consumed)]] | ✅ **Completed YYYY-MM-DD.** <full outcome paragraph> |
```

**Cell rules:**
- `Closed`: ISO date the chat closed (usually the day it shipped).
- `Outcome`: starts with `✅ **Completed YYYY-MM-DD.**` followed by a substantive paragraph naming the deliverables (with wikilinks), decisions made, pattern candidates surfaced, downstream unblocks. This is the canonical post-mortem cell — the audit trail.
- The handoff wikilink label conventionally includes `(consumed)` so the file's status is visible at a glance.

This table is intentionally verbose. Long outcome paragraphs are correct.

## Table 3 — Ready to spawn next (blockers cleared)

```markdown
## Ready to spawn next (blockers cleared)

| Chat name | Handoff file | Why now |
|---|---|---|
| <human-readable name> | [[<handoff-wikilink>\|<label>]] | <one-paragraph reason — what cleared, what this unblocks, dependencies satisfied> |
```

**Cell rules:**
- `Why now`: the load-bearing cell. Names the blocker that just cleared (with date), the dependencies satisfied, and what spawning this unblocks downstream.
- Strike-through rows that have already moved to In-flight or Recently closed STAY in this table with the chat name and handoff wikilink wrapped in `~~strikethrough~~` and the `Why now` cell rewritten as a pointer (see "Strike-through promotion convention" below).

## Table 4 — Queued — Tier 2

```markdown
## Queued — Tier 2 (spawn after Tier 1 lands, within ~1 week)

| Chat name | Handoff file | Trigger to spawn |
|---|---|---|
| <human-readable name> | [[<handoff-wikilink>\|<label>]] | <what condition needs to be true before spawning — usually a sibling chat shipping> |
```

**Cell rules:**
- `Trigger to spawn`: the condition that promotes this to Ready-to-spawn. Often "after Phase X lands" or "no blockers — spawn whenever bandwidth allows."

## Table 5 — Queued — Tier 3

```markdown
## Queued — Tier 3 (wait for explicit triggers, do NOT spawn yet)

| Chat name | Handoff file | Trigger to wait for |
|---|---|---|
| <human-readable name> | [[<handoff-wikilink>\|<label>]] | <hard gate — calendar date, external dependency, multi-prerequisite chain> |
```

**Cell rules:**
- `Trigger to wait for`: the hard gate. Calendar gates ("DataForSEO unlocks 2026-06-03"), multi-prerequisite chains ("after Phase 2a/b/c/d + Phase 3a/b/c/d ship"), or external-system events ("after first Watchdog report arrives") all count.

## Table 6 — Scheduled Cowork tasks

```markdown
## Scheduled Cowork tasks (background work, automated)

These are not "chats" Oliver spawns — they fire automatically.

| Fires | Task ID | What it does | State |
|---|---|---|---|
| YYYY-MM-DD HH:MM ET | `<task-id-slug>` | <one-line description> | Armed / Fired / Cancelled |
```

**Cell rules:**
- `Fires`: ISO date plus time-of-day in ET. Cron expressions also valid (e.g., `0 9 1 * *` for monthly).
- `Task ID`: kebab-case slug, wrapped in backticks. Should match the actual scheduled-task identifier in the Cowork scheduler.
- `State`: typically `Armed` (waiting to fire), `Fired` (already ran), `Cancelled` (manually killed before firing).

## Table 7 — Recently completed (past 7 days)

```markdown
## Recently completed (past 7 days)

| Date | Chat name | Handoff/source | Outcome |
|---|---|---|---|
| YYYY-MM-DD | <human-readable name> | [[<handoff-wikilink>\|<label>]] OR n/a (operator-driven) | <one-paragraph outcome — terser than Table 2's "Recently closed" cell> |
```

**Cell rules:**
- This is a rolling 7-day window. Rows older than 7 days move out (typically pruned during a tracker pass).
- `Outcome`: a shorter version of Table 2's outcome paragraph — names key deliverables and pattern candidates, omits the deep audit-trail prose.
- `Handoff/source`: `n/a (operator-driven)` is valid for chats that didn't have a pre-filed handoff (e.g., ad-hoc audits the operator opened directly).

## Bulleted list — Hot decisions sitting on Oliver's plate

Not a table. A numbered list of decisions deferred to the operator with one-line context per item. The skill never edits this list automatically — it's operator territory. The skill MAY surface a candidate for inclusion ("you might want to add X to Hot decisions") but does not write the row itself.

```markdown
## Hot decisions sitting on Oliver's plate

Captured YYYY-MM-DD so they don't get lost between chats:

1. **<decision label>** — <one-line context including any calendar gate>
2. ...
```

## Strike-through promotion convention

When a row is moved from Tier-3 or Tier-2 into Ready-to-spawn, OR promoted further from Ready-to-spawn into In-flight, OR shipped from In-flight into Recently closed, the **original row stays in its queue table** as a pointer:

- Wrap the `Chat name` cell in `~~strikethrough~~`
- Wrap the `Handoff file` wikilink in `~~strikethrough~~`
- Rewrite the right-hand cell (`Why now` / `Trigger to spawn` / `Trigger to wait for`) as a pointer:
  - To Ready-to-spawn: `✅ **Blocker cleared YYYY-MM-DD.** <what cleared>. Promoted to Tier-1 spawnable — see "Ready to spawn next" above.`
  - To In-flight: `⏳ **In-flight YYYY-MM-DD.** See "Active / in-flight chats" above.`
  - To Recently closed: `✅ **Shipped YYYY-MM-DD.** See "Recently closed chats" above.`

This keeps the historical trail visible while ensuring the live row appears in only one place. **The skill must understand this convention so it doesn't add duplicate rows or treat struck-through rows as still-pending.**

When auditing, a struck-through row is informational only — never count it as an open candidate. When recommending the next move, exclude struck-through rows from the candidate set.

## YAML frontmatter at the top of the tracker

```yaml
---
type: tracker
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
last-change: '<free-form prose describing the most recent update — wrap in single quotes>'
tags: [meta, handoffs, active-chats, coordination, state-of-play]
---
```

**Critical:** `last-change:` MUST be wrapped in single quotes. The value almost always contains colon-space sequences (`shipped: ...`, `used in this chat: 0`) that break YAML parsing if unquoted. This trap has bitten the file at least four times. Single quotes treat everything as literal except `''` (escape internal apostrophes by doubling them). Backticks, em-dashes, and colons inside the quoted value are all safe.

The skill verifies YAML parses cleanly after every tracker edit via:

```bash
python3 -c "import yaml; yaml.safe_load(open('_meta/handoffs/_active-chats-tracker.md').read().split('---')[1]); print('OK')"
```

Expected output: `OK`. Any other output is a frontmatter error to fix before declaring the edit complete.

## Wikilink conventions inside tracker cells

- **Standalone handoff:** `[[handoff-YYYY-MM-DD-<slug>\|<short label>]]`
- **Project-folder handoff:** `[[<project-slug>/phase-N-<short>\|<short label>]]`
- **Execution log:** `[[<path>/execution-log-YYYY-MM-DD-<topic>\|<short label>]]`
- **Always escape the pipe** inside the wikilink with `\|` so Markdown tables render correctly. The unescaped `|` would close the table cell prematurely.

Cross-reference: `~/workspace/second-brain/_meta/conventions.md` has the broader slug-only wikilink rule. The tracker follows it.

## Section ordering

The skill preserves the existing section order when editing the tracker:

1. Frontmatter
2. `# Active chats tracker` (H1)
3. `## How to use this file`
4. `## Active / in-flight chats`
5. `## Recently closed chats`
6. `## Ready to spawn next (blockers cleared)`
7. `## Queued — Tier 2`
8. `## Queued — Tier 3`
9. `## Scheduled Cowork tasks`
10. `## Recently completed (past 7 days)`
11. `## Hot decisions sitting on Oliver's plate`
12. `## Update protocol`
13. `## Related`

Never reorder these sections. Never collapse them. If a section becomes empty (e.g., zero in-flight chats), keep the section header and add the empty-state row.
