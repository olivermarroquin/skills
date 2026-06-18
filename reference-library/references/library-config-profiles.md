---
type: reference
status: active
created: 2026-06-18
updated: 2026-06-18
skill: reference-library
tags: [reference, reference-library, config-profiles, reuse]
---

# Library config profiles

> Each profile instantiates the `reference-library` engine for a specific domain. The engine
> reads the active profile and routes all operations (dedup, filing, queue, graduation) through
> the profile's paths and bars. To create a new library: add a profile below and create the
> folder structure — no skill code changes needed.

---

## Profile schema

```yaml
profile_name: <string>          # unique identifier
display_name: <string>          # human-readable name
description: <string>           # one-line purpose

# Folder structure (all paths relative to second-brain/)
library_root: <path>            # root folder for this library
high_performing_dir: <path>     # subfolder for high-performing entries
design_only_dir: <path>         # subfolder for design-only / swipe entries
catalog_dir: <path>             # graduation destination
queue_file: <path>              # standing ingestion queue
registry_file: <path>           # candidates registry (intake funnel)

# Upstream skills
capture_skill: <skill-name>     # skill that produces the raw capture
fingerprint_skill: <skill-name> # skill that produces the dossier/note

# Templates (paths relative to the fingerprint skill's references/)
full_template: <filename>       # 8-section full dossier template
light_template: <filename>      # design-only light note template

# Inclusion bars (high-performing lane)
inclusion_bars:
  - name: <string>
    description: <string>
    evidence_required: <string>
  # ... one entry per bar

# Design-only bar
design_only_bar: <string>       # one-line description of the visual quality threshold

# Cross-sector tag defaults
default_sector: <string|null>   # pre-filled sector tag (null = must be specified per entry)
```

---

## Profile 1 — Website-design inspiration (DEFAULT)

```yaml
profile_name: website-design
display_name: Website-Design Inspiration Library
description: >
  Curated reference sites for the website-design methodology. High-performing references
  have verified rankings + CWV + content depth + visual quality. Design-only references
  have visual quality only. Patterns graduate to the catalog after build-use or verification.

library_root: 03_domains/website-design/inspiration
high_performing_dir: 03_domains/website-design/inspiration/high-performing
design_only_dir: 03_domains/website-design/inspiration/design-only
catalog_dir: 03_domains/website-design/catalog
queue_file: 03_domains/website-design/insights/_ingestion-queue.md
registry_file: 03_domains/website-design/inspiration/candidates-registry.md

capture_skill: site-capture-engine
fingerprint_skill: design-fingerprint

full_template: dossier-template-full.md
light_template: dossier-template-light.md

inclusion_bars:
  - name: Rankings
    description: >
      Top 5 organic results for high-intent local-commercial queries in its niche,
      or comparable visibility (top-of-AI-overview, maps pack, citation density).
    evidence_required: Specific queries + positions, sourced and dated.
  - name: Core Web Vitals
    description: >
      "Good" range — LCP < 2.5s, CLS < 0.1, INP < 200ms. Real-user data preferred;
      lab data acceptable if flagged.
    evidence_required: PageSpeed Insights report or equivalent, dated.
  - name: Content depth
    description: >
      Service pages, location pages, FAQs, schema markup all present in some form.
    evidence_required: Page counts, content types observed.
  - name: Visual quality
    description: >
      At or above the bar we'd be comfortable shipping to a Keelworks client.
    evidence_required: Operator judgment (subjective but real).

design_only_bar: >
  Visual design at or above the bar we want to lift patterns from, regardless of
  SEO performance. The site looks great — that's the only criterion.

default_sector: null  # must be specified per entry (electrical-services, hvac, saas, etc.)
```

**Folder structure on disk:**
```
second-brain/03_domains/website-design/
├── inspiration/
│   ├── _README.md              (canonical — do not rewrite)
│   ├── high-performing/
│   │   ├── _README.md          (canonical — do not rewrite)
│   │   ├── dossier-*.md        (filed high-performing dossiers)
│   │   └── _traits-*.yaml      (trait sidecars)
│   ├── design-only/
│   │   ├── _README.md          (canonical — do not rewrite)
│   │   ├── inspiration-*.md    (filed design-only notes)
│   │   └── _traits-*.yaml      (trait sidecars)
│   └── candidates-registry.md  (intake funnel for [DI-7])
├── catalog/
│   ├── _README.md              (canonical — do not rewrite)
│   └── pattern-*.md            (graduated patterns)
└── insights/
    └── _ingestion-queue.md     (standing queue)
```

---

## Profile 2 — Copywriting swipe file (design proof only — execution proof deferred)

> **Design proof only.** This profile demonstrates that the engine is genuinely config-driven
> at the design level — all paths, bars, templates, and upstream skills are parameterized. The
> folder structure (`03_domains/content-systems/copywriting/swipe-file/`) does not yet exist
> on disk and no intake cycle has been run through this profile. **Execution proof is deferred
> to the first real 2nd-library instantiation** (CR-028). A copywriting swipe file uses the
> same intake/dedup/queue/graduation infrastructure with different folders, different bars,
> different upstream skills, and different templates.

```yaml
profile_name: copywriting-swipe
display_name: Copywriting Swipe File
description: >
  Curated collection of great copy — landing pages, cold emails, ad copy, headlines,
  CTAs — organized by type and effectiveness. High-performing entries have conversion
  data or A/B test results. Swipe entries are "this reads well" without performance proof.

library_root: 03_domains/content-systems/copywriting/swipe-file
high_performing_dir: 03_domains/content-systems/copywriting/swipe-file/proven
design_only_dir: 03_domains/content-systems/copywriting/swipe-file/inspiration
catalog_dir: 03_domains/content-systems/copywriting/patterns
queue_file: 03_domains/content-systems/copywriting/swipe-file/_ingestion-queue.md
registry_file: 03_domains/content-systems/copywriting/swipe-file/candidates-registry.md

capture_skill: null  # no automated capture — copy is pasted manually or via VIS extraction
fingerprint_skill: null  # no fingerprint skill — the swipe note IS the artifact

full_template: null  # custom template (would live at copywriting skill's references/)
light_template: null  # custom template

inclusion_bars:
  - name: Conversion evidence
    description: >
      Has measurable conversion data — A/B test results, revenue attribution,
      click-through rates, or credible case-study numbers.
    evidence_required: Specific metrics, sourced.
  - name: Copy quality
    description: >
      At or above the bar we'd want to emulate — clear value prop, strong hooks,
      effective CTAs, good voice.
    evidence_required: Operator judgment.

design_only_bar: >
  The copy reads well and teaches a technique worth remembering. No performance
  proof required — just quality writing that demonstrates a reusable pattern.

default_sector: null  # could be saas, ecommerce, b2b, services, etc.
```

**To activate this profile:**
1. Create the folder structure under `03_domains/content-systems/copywriting/swipe-file/`
2. Write `_README.md` files for `proven/` and `inspiration/` subfolders
3. Create the `_ingestion-queue.md` with Wave 1 items
4. Create copywriting-specific templates (or use the generic ones)
5. Invoke the skill with `--profile copywriting-swipe`

No changes to `SKILL.md` or the engine's intake/dedup/queue/graduation logic are needed.
The same `reference-library` skill routes through whichever profile is active.

---

## How to add a new profile

1. **Define the profile** in this file following the schema above.
2. **Create the folder structure** on disk (library root + high-performing + design-only +
   catalog + queue + registry).
3. **Write `_README.md` files** for each subfolder defining the inclusion bars and file formats.
4. **Create or reference templates** for the dossier/note formats.
5. **Set up the queue** with initial items.
6. **Invoke with `--profile <profile_name>`** — the engine handles the rest.

The engine reads the profile at invocation time. Multiple profiles can coexist — each operates
on its own folder tree with no cross-contamination.
