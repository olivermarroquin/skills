---
type: template
status: active
created: 2026-06-16
updated: 2026-06-16
skill: design-fingerprint
tags: [template, design-fingerprint, dossier, light-depth, design-only]
---

# Light dossier template (design-only note)

> Used by the `design-fingerprint` skill at `depth: light`. Brevity is correct here —
> a 200-word note with good patterns is better than a 2,000-word note that isn't actionable.
> Matches the format spec in `03_domains/website-design/inspiration/design-only/_README.md`.

---

## Output filename

`inspiration-{{site_slug}}.md`

## Frontmatter

```yaml
---
type: design-inspiration
status: captured
created: {{date}}
updated: {{date}}
domain: {{domain}}
sector: {{sector}}          # optional
archetype: {{archetype}}    # optional
capture-engine-version: {{engine_version}}
tags: [design-inspiration, {{sector}}, {{archetype}}]
---
```

## Template

```markdown
# {{site_name}} — design reference

**Domain:** {{domain}}
**Captured:** {{capture_date}} via site-capture-engine v{{engine_version}}

## Patterns worth lifting

### {{pattern_name_1}}
{{pattern_description_1}}
→ `catalog/{{category_1}}/{{pattern_slug_1}}`

### {{pattern_name_2}}
{{pattern_description_2}}
→ `catalog/{{category_2}}/{{pattern_slug_2}}`

[2-5 patterns total — each named, described, with a catalog/ landing pointer]

## Visible tooling / libraries

- **Framework:** {{framework}}
- **CSS:** {{css_framework}}
- **Fonts:** {{fonts}}
- **Motion:** {{motion_libraries | "None / pure CSS"}}
- **Other:** {{other_tooling}}

## Why this matters

{{one_paragraph_why_this_matters}}
```

**Rules:**
- 2-5 named liftable patterns, no more
- Every pattern carries a `→ catalog/` landing pointer
- One paragraph for "why this matters" — what this reference teaches that isn't already in the catalog
- Trait sidecar (`_traits-{{site_slug}}.yaml`) is STILL emitted alongside the light note
