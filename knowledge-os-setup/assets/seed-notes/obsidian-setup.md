---
type: meta
status: canonical
created: <% tp.date.now("YYYY-MM-DD") %>
tags: [meta, setup, obsidian]
---

# Obsidian setup

Required configuration for the KOS to function. Run this once after installing.

## Required plugins (Community Plugins)

Install these from Settings → Community plugins:

1. **Templater** — runs the templates with date macros and inheritance
2. **Dataview** — powers every dashboard query
3. **QuickAdd** — one-keystroke note creation against templates
4. **Omnisearch** (optional but recommended) — full-text search beyond Obsidian's default

## Templater config

Settings → Templater:

- **Template folder location:** `_meta/templates`
- **Trigger Templater on new file creation:** ON
- **Folder Templates:**
  - `00_inbox/sources-pending` → `_meta/templates/vis/template-source-video`
  - `00_inbox/decisions-pending` → `_meta/templates/vis/template-opportunity`
  - `03_domains/video-intelligence/insights` → `_meta/templates/vis/template-source-video`
  - `05_shared-intelligence/patterns` → `_meta/templates/kos/template-pattern`
  - `05_shared-intelligence/lessons` → `_meta/templates/kos/template-lesson`
  - `05_shared-intelligence/blueprints` → `_meta/templates/kos/template-blueprint`
  - `05_shared-intelligence/tools` → `_meta/templates/kos/template-tool`
  - `05_shared-intelligence/workflows` → `_meta/templates/kos/template-workflow`
  - `05_shared-intelligence/systems` → `_meta/templates/kos/template-system`

## Dataview config

Settings → Dataview:

- **Enable JavaScript Queries:** ON (some queries on the home dashboard use this)
- **Enable Inline JavaScript Queries:** ON
- **Render Null As:** `—`
- **Refresh Interval:** 2500ms

## QuickAdd config

Settings → QuickAdd → Manage Macros. Add these commands:

### "VIS: New source"
- Type: Template
- Template path: `_meta/templates/vis/template-source-video`
- Folder: `00_inbox/sources-pending`
- File name: `source-{{VALUE:source slug}}`
- Hotkey: `Cmd+Shift+V`

### "KOS: New tactic"
- Type: Template
- Template: `_meta/templates/vis/template-tactic`
- Folder: prompts you for which domain → `03_domains/{folder}/insights`
- File name: `tactic-{{VALUE:tactic name}}`

### "KOS: New pattern"
- Type: Template
- Template: `_meta/templates/kos/template-pattern`
- Folder: `05_shared-intelligence/patterns`
- File name: `pattern-{{VALUE:pattern name}}`
- Hotkey: `Cmd+Shift+P`

### "KOS: New lesson"
- Type: Template
- Template: `_meta/templates/kos/template-lesson`
- Folder: `05_shared-intelligence/lessons`
- File name: `lesson-{{VALUE:lesson name}}`

### "KOS: New opportunity"
- Type: Template
- Template: `_meta/templates/vis/template-opportunity`
- Folder: `00_inbox/decisions-pending`
- File name: `opportunity-{{VALUE:opportunity name}}`

### "VIS: Weekly synthesis"
- Type: Template
- Template: `_meta/templates/vis/template-weekly-synthesis`
- Folder: `_meta/dashboards`
- File name: `synthesis-{{DATE:YYYY-[W]ww}}`

## Files & Links settings

Settings → Files & Links:

- **Default location for new notes:** In the folder specified below
- **Default folder:** `00_inbox/captures`
- **Use [[Wikilinks]]:** ON
- **New link format:** Shortest path when possible
- **Detect all file extensions:** ON

## Excluded Files (for Tier 2 client privacy)

Settings → Files & Links → Excluded files:

Add patterns:
- `04_projects/clients/_private/`
- `_archive/`

This excludes them from quick switcher, link suggestions, and Omnisearch by default.

## Hotkeys (recommended)

- `Cmd+O` — Quick switcher
- `Cmd+Shift+F` — Search in all files
- `Cmd+Shift+V` — VIS: New source (set above)
- `Cmd+Shift+P` — Pattern (set above)
- `Cmd+E` — Toggle reading/edit
- `Cmd+G` — Open graph view

## Graph view config

When you open the graph (Cmd+G):

- Filter: hide `_meta/templates/`
- Color groups:
  - `tag:#source` → blue
  - `tag:#pattern` → orange
  - `tag:#lesson` → green
  - `tag:#opportunity` → red
  - `tag:#tool` → purple

## Verification

After setup, open `_HOME.md`. You should see:
- The dashboard renders without errors
- "Recent ingestion" shows the sample source
- "Decisions waiting" shows the sample opportunity
- Quick links resolve

If any of these are broken: Templater is probably the culprit — check that the template folder path is correct.
