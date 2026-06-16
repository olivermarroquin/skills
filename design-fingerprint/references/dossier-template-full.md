---
type: template
status: active
created: 2026-06-16
updated: 2026-06-16
skill: design-fingerprint
tags: [template, design-fingerprint, dossier, full-depth]
---

# Full dossier template (8 sections)

> Used by the `design-fingerprint` skill at `depth: full`. Each `{{placeholder}}` is filled from
> the capture package analysis. Sections marked *(contextual)* may be abbreviated or marked
> "Not assessed" when the relevant input data is not provided.

---

## Output filename

`dossier-{{site_slug}}.md`

## Frontmatter

```yaml
---
type: design-dossier
status: draft
created: {{date}}
updated: {{date}}
domain: {{domain}}
sector: {{sector}}          # optional — omit if not provided
archetype: {{archetype}}    # optional — omit if not provided
niche: {{niche}}            # optional — omit if not provided
geography: {{geography}}    # optional — omit if not provided
performance-verified-date: {{perf_date}}  # optional — omit if no performance data
capture-engine-version: {{engine_version}}
tags: [dossier, {{sector}}, {{archetype}}]
---
```

## Section 1 — Business / artifact identity

```markdown
## 1. Business / artifact identity

- **Name:** {{business_name}}
- **Domain:** {{domain}}
- **Niche:** {{niche | "Not specified"}}
- **Geography:** {{geography | "Not specified"}}
- **Framework:** {{framework}} ({{framework_details}})
- **Business model:** {{business_model | "Not assessed"}}
- **Years in business:** {{years | "Unknown"}}
```

## Section 2 — Why it performs *(contextual)*

```markdown
## 2. Why it performs

{{#if performance_data}}
### Rankings
{{ranking_evidence}}

### Core Web Vitals
| Metric | Mobile | Desktop | Source |
|---|---|---|---|
| LCP | {{lcp_mobile}} | {{lcp_desktop}} | {{cwv_source}} |
| INP | {{inp_mobile}} | {{inp_desktop}} | {{cwv_source}} |
| CLS | {{cls_mobile}} | {{cls_desktop}} | {{cwv_source}} |

### Content depth
{{content_depth_evidence}}

### Conversion proxies
{{conversion_proxy_evidence}}
{{else}}
*Not assessed — no performance data provided. This dossier captures design patterns only.
To upgrade to a verified high-performing reference, provide ranking data, CWV scores, and
review counts from authoritative sources.*
{{/if}}
```

**Rule:** Performance claims MUST cite evidence with source + date. Never fabricate.

## Section 3 — Tech + framework fingerprint

```markdown
## 3. Tech + framework fingerprint

- **CMS / framework:** {{framework}}
- **CSS framework:** {{css_framework}} ({{css_version}})
- **JS libraries:** {{js_libraries}}
- **Hosting / CDN:** {{hosting}}
- **Font loading:** {{font_loading_method}}
- **Schema types:** {{schema_types | "None detected"}}
- **Analytics:** {{analytics}}
- **Agency credit:** {{agency | "None visible"}}
```

## Section 4 — Visual-design fingerprint

```markdown
## 4. Visual-design fingerprint

### Palette
| Role | Hex | Usage | Notes |
|---|---|---|---|
| {{role}} | `{{hex}}` | {{usage_count}} | {{notes}} |

**Look:** {{palette_personality}}

### Typography
- **Primary font:** {{primary_font}} ({{font_loading}})
- **Secondary font:** {{secondary_font | "None"}}
- **Type scale:** {{type_scale_summary}}

| Role | Font | Weight | Size | Line-height |
|---|---|---|---|---|
| {{role}} | {{font}} | {{weight}} | {{size}} | {{line_height}} |

### Layout patterns
{{layout_description}}

### Spacing system
- **Base unit:** {{spacing_base}}
- **Dominant values:** {{dominant_spacing}}

### Border-radius
- **Strategy:** {{radius_strategy}}
- **Values:** {{radius_values}}

### Shadows
- **Strategy:** {{shadow_strategy}}

### Motion design
- **Libraries:** {{motion_libraries | "None / pure CSS"}}
- **Keyframe animations:** {{keyframes}}
- **Transition density:** {{transition_density}}
- **Motion personality:** {{motion_personality}}

### Image treatment
{{image_treatment}}
```

## Section 5 — Patterns worth lifting

```markdown
## 5. Patterns worth lifting

### {{pattern_name}}
{{pattern_description}}
→ `catalog/{{category}}/{{pattern_slug}}`

### {{pattern_name_2}}
{{pattern_description_2}}
→ `catalog/{{category_2}}/{{pattern_slug_2}}`

[repeat for each liftable pattern]
```

**Rule:** Every pattern MUST have a `→ catalog/` landing pointer.

## Section 6 — Patterns to skip

```markdown
## 6. Patterns to skip

### {{skip_pattern_name}}
{{why_skip}}

[repeat for each pattern to skip]
```

## Section 7 — How we emulate without copying assets

```markdown
## 7. How we emulate without copying assets

**What we lift (patterns — not copyrightable):**
- Color palette structure (hex values, role assignments, contrast ratios)
- Typography scale (font sizes, weights, line-heights — using our own licensed fonts)
- Layout patterns (section order, grid structure, spacing rhythm)
- Motion patterns (transition timing, animation types, interaction triggers)
- Component patterns (hero composition, CTA placement, card layouts)

**What we NEVER copy:**
- Photography, illustrations, or custom artwork
- Logos, brand marks, or iconography
- Copywriting, taglines, or marketing text
- Custom illustrations or character art
- Proprietary fonts (we license our own or use open-source equivalents)

**The line:** We emulate the *decisions* (dark background + bold accent + split-image hero),
not the *assets* (their specific photos, their specific copy, their specific logo).
{{site_specific_notes}}
```

**Rule:** This section is MANDATORY. Never omit it.

## Section 8 — Verification notes

```markdown
## 8. Verification notes

- **Capture date:** {{capture_date}}
- **Capture engine:** site-capture-engine v{{engine_version}}
- **Analysis date:** {{analysis_date}}
- **Analysis skill:** design-fingerprint v1.0
- **Viewports analyzed:** {{viewports}}
- **Caveats:** {{caveats | "None"}}
```
