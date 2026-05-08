# Conventions Update — Source Note Naming

This document describes a change to the source-note naming convention introduced with Phase 2.

## What's changing

**Old convention:**
```
source-<creator-or-topic>.md
```
Example: `source-greg-isenberg-agent-builders.md`

**New convention:**
```
source-YYYY-MM-DD-<channel-or-author-slug>-<topic-slug>.md
```
Examples:
- `source-2026-05-03-nate-herk-claude-code-skills-six-best.md`
- `source-2025-08-25-anthropic-piloting-claude-in-chrome.md`
- `source-2026-04-15-greg-isenberg-niche-onboarding-agents.md`

## Why

You can scan a folder of these and immediately see who, when, what — without opening any files. Critical for clustering and triage at 10+ sources/week.

## Date semantics

- Use the source's **publish date** if known (yt-dlp surfaces it; trafilatura sometimes does)
- Fall back to **ingestion date** (today) if publish date is unknown
- Format: ISO YYYY-MM-DD, no exceptions

## Slug guidelines

- **Channel/author slug:** kebab-case, max 25 characters
- **Topic slug:** kebab-case, max 35 characters
- Total filename should stay under ~80 characters

## What this does NOT change

Supporting note naming stays as-is — they don't get date prefixes, because they're *about* the topic, not a snapshot in time:
- `tactic-schema-first-agent-design.md` (stays same)
- `tool-claude-code.md` (stays same)
- `opportunity-niche-onboarding-agent-service.md` (stays same)

Pattern notes, lessons, blueprints, workflows, and systems stay as-is.

## Existing source notes

The one sample source note created during Phase 1 (`source-example-onboarding-agent.md`) does NOT need to be retroactively renamed. New sources from Phase 2 onward use the new convention. Old ones stay where they are; if you ever revisit, you can rename then.

## Where this gets enforced

- The VIS extraction skill's prompt uses the new convention when creating source notes
- The QuickAdd "VIS: New source" macro should be updated to default to the new pattern (the user does this manually in Obsidian settings; QuickAdd config can't be auto-modified)

## QuickAdd update

To update the QuickAdd macro:
1. Open Obsidian Settings → QuickAdd
2. Find the "VIS: New source" choice
3. Click the gear icon
4. Change "File Name format" from:
   `source-{{VALUE:source slug}}`
   to:
   `source-{{DATE:YYYY-MM-DD}}-{{VALUE:channel and topic slug}}`

The `{{DATE:YYYY-MM-DD}}` is a QuickAdd macro that inserts today's date in the right format.
