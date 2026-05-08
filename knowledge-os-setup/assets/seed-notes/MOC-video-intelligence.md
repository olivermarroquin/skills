---
type: MOC
status: canonical
created: <% tp.date.now("YYYY-MM-DD") %>
domain: video-intelligence
tags: [MOC, video-intelligence]
---

# MOC: Video Intelligence

> The frontier monitoring and external content extraction system.

## What lives here
- Source notes for processed videos and articles
- Extracted tactics, tools, workflows
- Pattern candidates (3+ sources)
- Opportunities and content ideas surfaced from external content

## Entry points
- [[workflow-video-extraction|Workflow: video extraction]]
- [[workflow-knowledge-promotion|Workflow: knowledge promotion]]
- [[conventions|Naming & linking conventions]]

## Recently processed sources

```dataview
TABLE WITHOUT ID
  file.link as "Source",
  creator as "Creator",
  category as "Category",
  tier as "Tier"
FROM "03_domains/video-intelligence" OR "00_inbox"
WHERE type = "source"
SORT ingested DESC
LIMIT 15
```

## High-actionability sources (score ≥ 4)

```dataview
TABLE creator, category
FROM "03_domains/video-intelligence" OR "00_inbox"
WHERE type = "source" AND actionability-score >= 4
SORT actionability-score DESC
```

## Tools surfaced

```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  category as "Category",
  status as "Status"
FROM "05_shared-intelligence/tools"
SORT updated DESC
LIMIT 20
```

## Patterns discovered

```dataview
TABLE WITHOUT ID
  file.link as "Pattern",
  times-observed as "× Observed",
  confidence as "Confidence"
FROM "05_shared-intelligence/patterns"
WHERE contains(domains, "video-intelligence") OR contains(file.outlinks, "source-")
SORT times-observed DESC
```

## Opportunities surfaced

```dataview
TABLE WITHOUT ID
  file.link as "Opportunity",
  opportunity-type as "Type",
  status as "Status"
FROM "00_inbox/decisions-pending" OR "03_domains/video-intelligence"
WHERE type = "opportunity"
SORT created DESC
```

## Recent syntheses

```dataview
LIST
FROM "_meta/dashboards"
WHERE type = "synthesis"
SORT created DESC
LIMIT 5
```

## Tier definitions
- **Tier 1** — directly relevant to current build/business goals, act on now
- **Tier 2** — adjacent opportunity worth saving and revisiting
- **Tier 3** — interesting signal, low-priority
- **Tier 4** — hype/noise, archive after extraction
