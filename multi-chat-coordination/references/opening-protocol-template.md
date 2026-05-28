---
type: reference
status: canonical
created: 2026-05-28
updated: 2026-05-28
applies-to: multi-chat-coordination
tags: [reference, multi-chat-coordination, opening-protocol, handoff-convention, tracker-discipline]
---

# Opening protocol — template for handoff generators

This is the canonical Opening Protocol section that every handoff DECOMPOSE mode generates must include verbatim. Place it inside the prompt fence, immediately after `--- start prompt ---` and BEFORE any work description (before "What you're building," before "Read these in order," before everything else the chat is supposed to do).

The protocol exists because operators have had to manually tell every prior chat: "go to the tracker and move your row to in-flight before doing anything." This automates that instruction.

## Canonical text — copy verbatim into every generated handoff

Place this block right after `--- start prompt ---`:

```markdown
## Opening protocol (RUN FIRST — before any other work)

This protocol is **mandatory**. Do not do any of the work described below until every step here has been executed. The operator has had to instruct prior chats to update the tracker manually — this section closes that friction.

**Step 1 — Read the active-chats tracker.**

Open `~/workspace/second-brain/_meta/handoffs/_active-chats-tracker.md`. Read the frontmatter and every section. Understand what else is in flight, what shipped recently, and what's blocked on what.

**Step 2 — Confirm this handoff is not already in-flight.**

Search "Active / in-flight chats" for this handoff's name. If a row already exists with status `⏳ In-flight`, STOP. Surface to the operator: "This handoff is already in-flight in another chat. Are you sure you want to start a duplicate?" Wait for explicit confirmation before continuing.

**Step 3 — Move this handoff's row to Active / in-flight.**

Find the row in its current section (Ready to spawn next, Tier-2 queue, or Tier-3 queue). **Remove** it from that section entirely — no strikethrough pointer left behind. The destination section is the canonical location.

Add a new row to the "Active / in-flight chats" section with:
- `Started:` today's date (YYYY-MM-DD)
- `Chat name:` matching the handoff
- `Handoff file:` wikilink to this handoff
- `Status:` `⏳ In-flight`
- `Expected duration:` from the handoff's Status section
- `Notes:` short paragraph describing what this chat is producing

**Step 4 — Bump frontmatter `last-change` (single-quote wrapper).**

Update the `last-change:` value to note the spawn. Keep the single quotes around the value — they protect against unquoted-colon-space YAML parse errors per the file's own discipline rules.

**Step 5 — Verify YAML still parses.**

Run from the second-brain repo root:

```
python3 -c "import yaml, re; m = re.match(r'^---\\n(.*?)\\n---\\n', open('_meta/handoffs/_active-chats-tracker.md').read(), re.DOTALL); yaml.safe_load(m.group(1)); print('OK')"
```

Expected output: `OK`. If it errors, the most common cause is an unquoted colon-space inside the `last-change` value — re-wrap in single quotes.

**Step 6 — Now begin the work described below.**

Only after the tracker reflects this chat's in-flight status may you proceed with the actual prompt instructions.
```

## Where this fits in the handoff body

The full handoff body structure with both protocols:

```
## Prompt to paste into a new chat

--- start prompt ---

## Opening protocol (RUN FIRST — before any other work)
... (the template above, verbatim)

## What you're building
... (the actual chat work)

[remaining handoff content — Files to create, Out of scope, Status, etc.]

## Closing protocol (RUN BEFORE TELLING THE OPERATOR THE CHAT IS DONE)
... (closing-protocol-template.md content, verbatim)

--- end prompt ---
```

Opening Protocol bookends the prompt at the top; Closing Protocol bookends at the bottom. The actual work sits between them.

## Why this protocol exists

Three sources of friction it closes:

1. **Manual operator instruction.** Pre-protocol, the operator had to remind every spawned chat: "update the tracker before you do anything." Adding this section automates the instruction.

2. **Tracker drift.** Pre-protocol, chats forgot to move themselves to in-flight, and the tracker would show the row still in queued state while work was actively happening. AUDIT mode caught this drift repeatedly.

3. **Duplicate spawns.** Pre-protocol, an operator could accidentally paste the same handoff into two chats without realizing the work was already in flight. Step 2 of the Opening Protocol catches this.

## Discipline rules the Opening Protocol enforces

- **Move, don't strikethrough.** Per the tracker's own "Move, don't strikethrough" convention — when a row leaves a queue section, it leaves entirely. No strikethrough'd pointer.
- **One canonical location per row.** A row exists in exactly one section at a time.
- **YAML safety on last-change.** Single-quote wrapping is non-negotiable — the colon-space trap inside the free-form prose value breaks parsing repeatedly without it.

## Related

- [[closing-protocol-template]] — the sibling protocol that runs at chat END
- [[tracker-row-shapes]] — the six section row shapes the Opening Protocol moves rows between
- [[handoff-frontmatter-spec]] — the handoff frontmatter the Opening Protocol does NOT touch (that's the Closing Protocol's job)
