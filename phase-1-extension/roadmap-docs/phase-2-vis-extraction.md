---
type: roadmap-item
status: active
created: 2026-05-04
updated: 2026-05-04
phase: 2
priority: critical
estimated-effort: "2-3 working days"
depends-on: ["[[phase-1-knowledge-os]]"]
related-domains: [video-intelligence, knowledge-os]
tags: [roadmap, active, phase-2]
---

# Phase 2: Video Intelligence System — Extraction MVP

## Hypothesis
Reduce the friction of converting a YouTube URL or article into a structured source note (plus supporting notes) from "30+ minutes of manual work" to "paste URL, review output, file." The judgment stays with the human; the typing and structure are automated.

## Why this matters
At the user's intake goal of 10+ sources/week, manual extraction is the bottleneck that kills the system. Phase 2 removes the bottleneck while preserving the judgment that makes the system valuable.

## Why not Phase 1
We needed the structure, schema, templates, and folder layout to exist as a target before automating against them. Phase 1 was the foundation; Phase 2 is the workflow on top.

## Scope (what's IN this phase)

### Core extraction pipeline
- Paste URL (YouTube or article) → transcript or text retrieved
- Claude/Cowork extracts against the source-video template
- Notes land in `00_inbox/sources-pending/` with frontmatter populated and structured sections drafted
- Bidirectional links to existing tools, patterns, and domain notes auto-created where confident

### Supporting note creation
- Tactics extracted as separate notes in `03_domains/<domain>/insights/`
- Opportunities surfaced go to `00_inbox/decisions-pending/` for triage
- Content ideas to `03_domains/content-systems/`
- Tool notes to `05_shared-intelligence/tools/` (or updated if exists)

### Intelligent slug generation
- No more manually inventing slugs
- Slugs are URL-safe, descriptive, deduplicated against existing notes

### Weekly synthesis
- Friday afternoon ritual
- Dataview-driven aggregation of the week's tools, tactics, opportunities, content ideas
- Top 5 of each surfaced
- Pattern candidate detection (3+ tactics converging on the same mechanism)

### MVP exit conditions (from VIS spec)
After 5-10 sources processed, the system must produce:
- At least 1 implementation plan
- At least 1 content idea
- At least 1 product/service idea
- At least 1 reusable pattern note

If we can't hit these in 2 weeks of real use, the system is too fluffy; re-architect.

## Scope (what's OUT — see [[phase-3-plus-queue]])
- Intelligent auto-routing to domain folders (Phase 3+ item #1)
- Cross-domain idea synthesis (item #2)
- YouTube channel monitoring (item #3)
- Pivot detector (item #4)
- Specialized agent teams (item #5)
- Web automation / SOP generation (item #6)
- Learning & retention system (item #7)

## Dependencies
- Phase 1 complete ✓
- yt-dlp or equivalent for transcript pull
- Cowork or Claude for extraction against templates
- Existing template library (already installed)

## Pushback / what I might be wrong about
The risk in Phase 2 is the same risk Phase 1 navigated: over-scoping. Specifically:
- "Auto-extract" can mean a button or it can mean a full pipeline; we're scoping as "Cowork-driven workflow," not "fully automated daemon"
- Quality of extraction is a function of the source quality, the template, and Claude's judgment — not infrastructure complexity. Don't add tooling to fix a quality problem that's actually a content problem.
- The user's instinct toward "constant monitoring and ideation" is being deferred for good reason. Resist scope creep here.

## Re-evaluation trigger
After 10 real sources processed: are MVP exit conditions met? If yes, ship. If no, what specifically is failing — the extraction quality, the workflow ergonomics, or the underlying judgment?

## Decision log
- 2026-05-04 — scoped after Phase 1 ships
