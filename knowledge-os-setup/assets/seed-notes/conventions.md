---
type: meta
status: canonical
created: <% tp.date.now("YYYY-MM-DD") %>
tags: [meta, conventions, enforcement]
---

# KOS naming and linking conventions

These rules are non-negotiable. They make Dataview queries reliable and the graph view useful. Break them and the system stops compounding.

## File naming

All files use **kebab-case**, lowercase, no spaces.

### Required prefixes

| Prefix | Used for | Example |
|---|---|---|
| `source-` | Source notes (videos, articles) | `source-greg-isenberg-agent-builders.md` |
| `pattern-` | Reusable patterns | `pattern-three-tier-prompt-architecture.md` |
| `lesson-` | Extracted lessons | `lesson-never-skip-spec-validation.md` |
| `blueprint-` | System/architecture blueprints | `blueprint-vis-mvp.md` |
| `tool-` | Tool tracking notes | `tool-claude-code.md` |
| `workflow-` | Repeatable workflows | `workflow-video-extraction.md` |
| `system-` | System spec notes | `system-execution-control.md` |
| `tactic-` | Extracted tactics | `tactic-hooks-via-contradiction.md` |
| `opportunity-` | Surfaced opportunities | `opportunity-onboarding-saas-for-coaches.md` |
| `content-` | Content ideas | `content-why-most-agents-fail.md` |
| `spec-` | Specifications (project-level) | `spec-resume-saas-mvp.md` |
| `scope-` | Implementation scopes | `scope-resume-saas-auth.md` |
| `synthesis-` | Weekly/monthly synthesis | `synthesis-2026-w18.md` |
| `MOC-` | Maps of content (index notes) | `MOC-video-intelligence.md` |

### Filename rules

1. Start with the prefix
2. Use kebab-case for the rest
3. Date-stamped notes: append `-YYYY-MM-DD` at the end
4. Maximum 80 chars
5. No special characters except `-`

## Frontmatter rules

Every note must have YAML frontmatter with at minimum:

```yaml
---
type: <one of: source, pattern, lesson, blueprint, tool, workflow, system, tactic, opportunity, content-idea, spec, scope, synthesis, MOC>
status: <one of: draft, ingested, extracted, surfaced, promoted, validated, archived>
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [<type>, ...]
---
```

Notes without frontmatter break Dataview. They are invalid.

## Linking rules (ENFORCED)

Every note must link to:

1. **Parent context** — the domain, MOC, or system it belongs to
2. **At least one related artifact** — pattern, source, project, etc.
3. **Where it's used or referenced** (when applicable)

Notes with zero outgoing links are flagged as orphans by the home dashboard. Orphans must be either linked or archived.

## Tag rules

Tags are minimal and structural, not topical (use frontmatter `domains:` for topical).

Required tags by type:
- All notes: include `type` value as a tag
- Source notes: also tag `source` and source format (`video`, `article`, `tutorial`)
- Synthesis: tag `weekly`, `monthly`, `quarterly`

## Folder placement

The folder a note lives in is part of its identity. Don't fight the structure.

| Note type | Folder |
|---|---|
| Fresh capture, unprocessed | `00_inbox/captures/` |
| Source pending extraction | `00_inbox/sources-pending/` |
| Decision needed | `00_inbox/decisions-pending/` |
| Extracted source (kept) | `03_domains/<domain>/insights/` |
| Pattern (cross-source) | `05_shared-intelligence/patterns/` |
| Lesson (cross-project) | `05_shared-intelligence/lessons/` |
| Tool tracking | `05_shared-intelligence/tools/` |
| Workflow definition | `05_shared-intelligence/workflows/` |
| Blueprint | `05_shared-intelligence/blueprints/` |
| System spec | `01_ai-operating-system/` or `05_shared-intelligence/systems/` |
| Project artifacts | `04_projects/<area>/<project>/` (symlinked from repo `.kos/`) |
| Personal thinking | `02_core/thinking/` |
| Strategy | `02_core/strategy/` |
| Synthesis | `_meta/dashboards/syntheses/` |

## Drift checks

The system fails when:
- Notes have no frontmatter (Dataview breaks)
- Files don't follow naming convention (search and templates break)
- Notes are orphaned (graph view becomes useless)
- Two notes claim to be the same pattern (duplication)
- Lessons stay stuck in projects (no compounding)
- Sources never produce extracted artifacts (passive consumption trap)

The home dashboard surfaces these as drift indicators.
