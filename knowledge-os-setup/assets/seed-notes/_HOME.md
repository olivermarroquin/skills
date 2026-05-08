---
type: dashboard
status: canonical
created: <% tp.date.now("YYYY-MM-DD") %>
tags: [dashboard, home]
cssclass: dashboard
---

# Knowledge OS — Home

> Daily entry point. Surfaces drift, decisions, and compounding intelligence.

---

## 🔴 Decisions waiting

```dataview
TABLE WITHOUT ID
  file.link as "Decision",
  opportunity-type as "Type",
  estimated-effort as "Effort",
  estimated-value as "Value",
  tier as "Tier"
FROM "00_inbox/decisions-pending"
WHERE type = "opportunity" AND status = "surfaced"
SORT tier ASC, estimated-value DESC
LIMIT 10
```

---

## 📥 Inbox — sources pending extraction

```dataview
TABLE WITHOUT ID
  file.link as "Source",
  creator as "Creator",
  category as "Category",
  ingested as "Ingested"
FROM "00_inbox/sources-pending"
WHERE type = "source"
SORT ingested ASC
LIMIT 10
```

> If this list grows past 10, slow down ingestion. Backlog = passive consumption.

---

## 🟢 Recent ingestion (last 7 days)

```dataview
TABLE WITHOUT ID
  file.link as "Source",
  creator as "Creator",
  tier as "Tier",
  actionability-score as "Action"
FROM "03_domains" OR "00_inbox"
WHERE type = "source" AND ingested >= date(today) - dur(7 days)
SORT actionability-score DESC
```

---

## 🧠 Promoted to shared-intelligence (last 14 days)

```dataview
TABLE WITHOUT ID
  file.link as "Promoted note",
  type as "Type",
  updated as "Updated"
FROM "05_shared-intelligence"
WHERE updated >= date(today) - dur(14 days)
SORT updated DESC
LIMIT 15
```

> Target cadence: 2–4 per week. Two weeks of zero = drift.

---

## 🚨 Orphans (no incoming or outgoing links)

```dataview
LIST
FROM ""
WHERE length(file.inlinks) = 0 AND length(file.outlinks) = 0 AND !contains(file.path, "_meta/templates")
LIMIT 20
```

> These notes are isolated. Link them or archive them.

---

## ⚠️ Sources without extracted artifacts (>7 days old)

```dataview
LIST
FROM "03_domains" OR "00_inbox/sources-pending"
WHERE type = "source" 
  AND ingested <= date(today) - dur(7 days)
  AND length(file.outlinks) < 3
LIMIT 10
```

> Sources should produce 3+ artifacts (tactics, opportunities, content ideas, tool notes). If not, the system is just summarizing.

---

## 🔁 Pattern candidates

Tactics observed in 3+ sources but not yet promoted to a pattern:

```dataview
TABLE WITHOUT ID
  file.link as "Tactic",
  length(sources) as "× Sources",
  domain as "Domain"
FROM "03_domains"
WHERE type = "tactic" AND length(sources) >= 3 AND status != "promoted"
SORT length(sources) DESC
```

---

## 📊 Domain activity (last 30 days)

```dataview
TABLE WITHOUT ID
  rows.file.folder as "Domain",
  length(rows) as "Notes added"
FROM "03_domains"
WHERE created >= date(today) - dur(30 days)
GROUP BY split(file.folder, "/")[1]
SORT length(rows) DESC
```

---

## 📝 Active projects

```dataview
TABLE WITHOUT ID
  file.link as "Project",
  status as "Status",
  client as "Client?",
  sensitivity as "Tier"
FROM "04_projects"
WHERE type = "project-readme" AND status = "active"
```

---

## 🗓️ Latest synthesis

```dataview
LIST
FROM "_meta/dashboards"
WHERE type = "synthesis"
SORT created DESC
LIMIT 3
```

---

## Quick links

- [[conventions|🧭 Naming & linking conventions]]
- [[workflow-knowledge-promotion|♻️ Promotion workflow]]
- [[MOC-video-intelligence|🎬 Video Intelligence MOC]]
- [[MOC-shared-intelligence|🧠 Shared Intelligence MOC]]
- [[master-system-map|🗺️ Master System Map]]

---

## Dashboard health

If any of these are red, address before doing anything else:

- [ ] Inbox sources pending < 10
- [ ] At least 1 promotion in the last 14 days
- [ ] Orphan count < 10
- [ ] No sources older than 7 days without artifacts
