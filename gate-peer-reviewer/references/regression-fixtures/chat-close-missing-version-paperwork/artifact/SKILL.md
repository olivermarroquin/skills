---
name: fixture-skill
version: 1.0
status: active
created: 2026-01-01
updated: 2026-01-01
description: Synthetic skill for regression testing G-chat-close OC-10.
tags: [skill, fixture]
---

# `fixture-skill` v1.0

A synthetic skill. The fixture simulates a chat that added a new reference file
and updated this index but did NOT bump version, write a changelog entry, or
append an event-log row.

## Reference files (index)

- `references/existing-reference.md` — The original reference.
- `references/new-reference-added-by-chat.md` — Added by the fixture chat (THIS is the edit that should have triggered a version bump).

## Version history

- **v1.0 (2026-01-01)** — Initial ship.
