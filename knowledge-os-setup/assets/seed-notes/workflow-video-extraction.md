---
type: workflow
status: canonical
created: <% tp.date.now("YYYY-MM-DD") %>
domains: [video-intelligence, knowledge-os]
tools-required: [yt-dlp, claude, obsidian]
inputs: [video-url]
outputs: [source-note, tactics, opportunities, content-ideas, tool-notes]
estimated-time: "10-25 min per source"
times-run: 0
tags: [workflow, vis]
---

# Workflow: video extraction

The end-to-end loop from URL to structured outputs landing in the right folders.

## Goal
Convert one video into:
- 1 source note (canonical, in `03_domains/video-intelligence/insights/`)
- N tactic notes (one per non-trivial tactic)
- 0–N opportunity notes (only if real)
- 0–N content idea notes
- 0–N tool notes (only for tools worth tracking)

## When to run
- Anytime a high-signal source is queued in `00_inbox/sources-pending/`
- Triage gate: only process sources you'd be comfortable spending 15+ minutes on

## Tools required
- [[tool-yt-dlp]] — transcript pull
- [[tool-claude-cowork]] — extraction against templates
- Obsidian — review and link

## Steps

### 1. Triage (60 seconds)
Before processing, decide tier. If Tier 4 (hype/noise), don't process — archive.

- **Tier 1** — directly relevant to current goals → process today
- **Tier 2** — adjacent, worth saving → process this week
- **Tier 3** — interesting → process or batch
- **Tier 4** — noise → archive

### 2. Pull the transcript
```bash
yt-dlp --write-auto-sub --skip-download --sub-lang en --convert-subs srt "<URL>"
```

Or for sources that already have a transcript (articles, docs), skip this step.

### 3. Initial source note
Use the QuickAdd command "VIS: New source" to create a source note in `00_inbox/sources-pending/` from `template-source-video`. Fill frontmatter:
- title, creator, url, published, category, tier, domains

### 4. Hand to Cowork
Open Cowork against your second-brain folder. Paste the transcript and prompt:

> Process this transcript using the VIS skill. Source note is at `00_inbox/sources-pending/<filename>`. Extract per the source template, then create the supporting notes (tactics, opportunities, tool entries, content ideas) in their correct folders with bidirectional links.

### 5. Review (5 minutes)
- Skim the populated source note
- Check confidence labels — anything marked `inferred` should make sense
- Verify links resolve (no red links in graph view)
- Set `actionability-score` (0–5)

### 6. Move out of inbox
Once reviewed:
- Move the source note from `00_inbox/sources-pending/` to `03_domains/video-intelligence/insights/`
- Update `status: ingested` → `status: extracted`

### 7. Decision gate
For each opportunity note created:
- Pursue, park with conditions, or kill
- If pursue: link to relevant project or create one

### 8. Pattern check
- Are 3+ tactics now pointing to the same underlying mechanism?
- If yes, create a pattern note in `05_shared-intelligence/patterns/`

## Outputs
- Source note moved to insights
- N supporting notes created
- All links bidirectional
- `_HOME.md` shows the new content under "Recent ingestion"

## Validation
- [ ] Source note has 3+ outgoing links
- [ ] No orphans created
- [ ] Frontmatter is valid (Dataview can read it)
- [ ] At least one of: tactic, opportunity, content idea, tool

## Failure modes
- **Tier 4 sources sneaking through** — be ruthless at step 1
- **Inferred treated as explicit** — the template requires labeling, use it
- **Notes without links** — reject the extraction if Cowork didn't link
- **One-source patterns** — patterns require 3+, never promote a singleton

## Time budget
- Tier 1 source: 20-25 min total (worth it)
- Tier 2 source: 10-15 min
- Tier 3 source: 5-10 min (or batch)
- If you're spending more than this, scope is wrong
