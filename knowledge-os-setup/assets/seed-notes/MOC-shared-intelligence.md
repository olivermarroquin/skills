---
type: MOC
status: canonical
created: <% tp.date.now("YYYY-MM-DD") %>
tags: [MOC, shared-intelligence]
---

# MOC: Shared Intelligence

> The compounding layer. Knowledge that survives projects.

## Patterns

```dataview
TABLE WITHOUT ID
  file.link as "Pattern",
  times-observed as "× Observed",
  confidence as "Confidence",
  domains as "Domains"
FROM "05_shared-intelligence/patterns"
SORT times-observed DESC
```

## Lessons

```dataview
TABLE WITHOUT ID
  file.link as "Lesson",
  category as "Category",
  severity as "Severity"
FROM "05_shared-intelligence/lessons"
SORT updated DESC
```

## Blueprints

```dataview
TABLE WITHOUT ID
  file.link as "Blueprint",
  maturity as "Maturity",
  domains as "Domains"
FROM "05_shared-intelligence/blueprints"
SORT updated DESC
```

## Tools

```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  category as "Category",
  status as "Status",
  my-stack as "In stack?"
FROM "05_shared-intelligence/tools"
SORT updated DESC
```

## Workflows

```dataview
TABLE WITHOUT ID
  file.link as "Workflow",
  times-run as "× Run",
  status as "Status"
FROM "05_shared-intelligence/workflows"
SORT times-run DESC
```

## Systems

```dataview
TABLE WITHOUT ID
  file.link as "System",
  layer as "Layer",
  maturity as "Maturity"
FROM "05_shared-intelligence/systems"
SORT updated DESC
```

## Promotion velocity

```dataview
TABLE WITHOUT ID
  rows.file.folder as "Type",
  length(rows) as "Promoted (last 30 days)"
FROM "05_shared-intelligence"
WHERE updated >= date(today) - dur(30 days)
GROUP BY split(file.folder, "/")[1]
```
