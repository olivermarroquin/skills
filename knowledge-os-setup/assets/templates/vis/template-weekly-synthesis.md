---
type: synthesis
status: draft
created: <% tp.date.now("YYYY-MM-DD") %>
period: "<% tp.date.now('YYYY-[W]ww') %>"
sources-processed: 0
tags: [synthesis, weekly]
---

# Weekly synthesis: <% tp.date.now("YYYY-MM-DD") %>

## Period
Week of <% tp.date.now("YYYY-MM-DD", -7) %> → <% tp.date.now("YYYY-MM-DD") %>

## Sources processed this week

```dataview
TABLE creator, tier, category, actionability-score
FROM "00_inbox/sources-pending" OR "03_domains/video-intelligence"
WHERE type = "source" AND ingested >= date(today) - dur(7 days)
SORT actionability-score DESC
```

---

## Top 5 tools that surfaced

```dataview
TABLE category, status, length(sources) as "× sources"
FROM "05_shared-intelligence/tools" OR "03_domains"
WHERE type = "tool" AND updated >= date(today) - dur(7 days)
SORT length(sources) DESC
LIMIT 5
```

Notes:
- 

---

## Top tactics extracted

```dataview
LIST
FROM "03_domains"
WHERE type = "tactic" AND created >= date(today) - dur(7 days) AND actionability >= 3
SORT actionability DESC
```

Notes:
- 

---

## Opportunities surfaced

```dataview
TABLE opportunity-type, estimated-effort, estimated-value, tier
FROM "00_inbox/decisions-pending" OR "03_domains"
WHERE type = "opportunity" AND created >= date(today) - dur(7 days)
SORT tier ASC
```

### Decision queue (this week)
- [ ] [[ ]] — pursue / park / kill
- [ ] [[ ]] —

---

## Patterns becoming visible
Tactics or tools showing up across 3+ sources this month.

- 

If 3+ confirmed → create pattern note in `05_shared-intelligence/patterns/`.

---

## Content ideas

```dataview
TABLE format, platform
FROM "03_domains/content-systems"
WHERE type = "content-idea" AND created >= date(today) - dur(7 days)
```

---

## Build ideas
Things that should exist that don't yet.

- 

---

## Signal vs noise reflection
Was this week's intake high-signal? If not, what should be filtered next week?

- 

## Dropped from watchlist
Sources/creators that consistently produce noise — archive or stop following.

- 

## Next week's priorities
- 
- 
- 
