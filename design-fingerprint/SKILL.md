---
name: design-fingerprint
version: 1.0
description: >
  Turns a site-capture-engine design-capture package into a structured design dossier — the analytical
  layer between raw capture and a curated reference library. Produces a human-readable dossier (full
  8-section or light design-only) + a machine-readable YAML trait sidecar keyed to a controlled
  vocabulary, so downstream skills ([DI-3] reference-library, [DI-4] design-emulation-verify, [DI-6]
  cross-site synthesis) can parse traits without re-reading prose. Domain-agnostic: works on any
  captured visual artifact (website, app screen, static mock) — niche, geography, and why-it-performs
  are optional fields, not required. Use this skill whenever someone says "fingerprint the design of
  [site]," "build a design dossier for [site]," "add [site] to the design catalog," "run a design
  fingerprint on [site]," "capture the visual fingerprint of [site]," or any time a site-capture-engine
  design-capture package exists and needs to be turned into a structured reference. Also triggers when
  preparing a site for emulation per the emulate-competitor-design-patterns tactic, or when populating
  the reference library via [DI-3].
composes-with: [site-capture-engine, reference-library, design-emulation-verify, design-pattern-synthesis, competitor-deep-research]
---

# Design Fingerprint (v1.0)

> **v1.0 (2026-06-16)** — Initial build. Extracted from the unvalidated `--mode design-fingerprint`
> sub-section that was buried inside `competitor-deep-research` (spec-only, zero dossiers produced).
> Now a standalone general-purpose skill with config-driven templates, two-depth output, normalized
> trait vocabulary for cross-site analysis, machine-readable trait sidecar, and domain-agnostic design.
> Validated on AJ Long Electric (in-niche) + a 2nd out-of-niche instantiation.

A reusable skill that reads a [DI-1] design-capture package and produces a **structured design
dossier** — the analytical bridge between raw capture data and a curated reference library. The
dossier documents what makes a site's design work (palette, typography, layout, motion, patterns)
in enough detail that another builder can emulate the patterns without copying assets.

**Composes with:**
- **Upstream:** `site-capture-engine` (v2.1+) — produces the capture package this skill reads
- **Downstream:** `reference-library` ([DI-3]) — ingests dossiers into the curated library;
  `design-emulation-verify` ([DI-4]) — uses the dossier as the comparison baseline;
  `design-pattern-synthesis` ([DI-6]) — reads the machine trait sidecar for cross-site analysis
- **Sibling:** `competitor-deep-research` — landscape-tier competitive intelligence; this skill
  handles the design-depth dimension. Compose them: landscape first, then fingerprint the winner.

---

## When to use

Trigger this skill when someone wants to turn a captured site into a structured design reference.
Typical triggers:

- "Fingerprint the design of [site]"
- "Build a design dossier for [site]"
- "Add [site] to the design catalog"
- "Run a design fingerprint on [site]"
- "Capture the visual fingerprint of [site]"
- "What design patterns does [site] use?"
- Any time a site-capture-engine design-capture package exists and needs analysis
- Any time a site is being prepared for emulation per the
  [[tactic-emulate-competitor-design-patterns-with-ai|emulate competitor patterns tactic]]

Do **not** use this skill for:

- Capturing a site (use `site-capture-engine` first — this skill reads the capture, not the live site)
- SEO/competitive landscape analysis (use `competitor-deep-research`)
- Verifying a build against a reference (use `design-emulation-verify`)
- Cross-corpus pattern synthesis (use `design-pattern-synthesis` / [DI-6])

---

## Inputs

### Required

1. **Capture package path** — path to a directory containing a `design-capture-manifest.json` (the
   [DI-1] contract). The manifest indexes all artifacts: design tokens, screenshots, motion inventory,
   component inventory, a11y snapshot.

### Optional (config-driven)

2. **Depth** — `full` (default) or `light`.
   - `full`: 8-section dossier per `references/dossier-template-full.md`
   - `light`: design-only note per `references/dossier-template-light.md`
3. **Output path** — where to write the dossier + trait sidecar. Defaults to the capture package
   directory. For library ingestion, typically
   `second-brain/03_domains/website-design/inspiration/high-performing/` (full) or
   `../design-only/` (light).
4. **Sector** — free tag for cross-sector analysis (e.g., `electrical-services`, `hvac`, `saas`,
   `fintech`, `agency`). Written into frontmatter `sector:` field. Optional — omit for pure-design
   references where sector is irrelevant.
5. **Archetype** — free tag for design archetype classification (e.g., `dark-hero-cta`,
   `light-minimal`, `dashboard-dense`, `editorial`). Written into frontmatter `archetype:` field.
   Optional.
6. **Template override** — path to a custom template file. Overrides the depth-selected default.
7. **Site slug** — short kebab-case identifier for the site (e.g., `aj-long-electric`). Used in
   output filenames. If omitted, derived from the domain in the manifest.
8. **Niche** — domain/industry of the site (e.g., `electrical-services`). Optional.
9. **Geography** — primary service area or market (e.g., `Fairfax County, VA`). Optional.
10. **Performance data** — external performance evidence (CWV scores, ranking data, review counts).
    Optional — only used to populate the "Why it performs" section in full dossiers. If omitted, that
    section is marked "No performance data provided" rather than fabricated.

---

## Output contract

The skill produces **two files** per the two-file artifact split pattern:

### 1. Human-readable dossier

**Full depth:** `dossier-<site-slug>.md` — 8 sections per `references/dossier-template-full.md`:

1. **Business / artifact identity** — name, domain, niche, geography, framework, business model
2. **Why it performs** — rankings, CWV, content depth, conversion proxies. *Contextual:* present
   for high-performing references with performance data provided; marked "Not assessed" for
   pure-design references. Performance claims MUST cite evidence (rankings/CWV/review counts),
   not vibes — per `feedback_verify_stats_against_source_retractions`.
3. **Tech + framework fingerprint** — CMS, framework, libraries, hosting, CDN, schema types,
   analytics, agency credit
4. **Visual-design fingerprint** — palette (hex + roles), typography scale, layout patterns,
   spacing system, border-radius, shadows, motion design, image treatment
5. **Patterns worth lifting** — each named, described, tagged with a `catalog/` landing pointer
   (e.g., `→ catalog/heroes/dark-hero-split-image`). This is the actionable section for builders.
6. **Patterns to skip** — what NOT to emulate and why. Avoids treating every reference choice as good.
7. **How we emulate without copying assets** — the legal boundary, explicit. What we lift (patterns,
   measurements, structure) vs what we never copy (photos, logos, custom illustrations, copywriting).
   This section is **mandatory** on every full dossier.
8. **Verification notes** — when/how the analysis was done, capture engine version, any caveats

**Light depth:** `inspiration-<site-slug>.md` — design-only note per
`references/dossier-template-light.md`:

- Identity (name, domain)
- 2-5 named liftable patterns (each with `catalog/` pointer)
- Visible tooling/libraries
- One-paragraph "why this matters"

### 2. Machine-readable trait sidecar

`_traits-<site-slug>.yaml` — structured trait record keyed to `references/trait-vocabulary.md`.

The sidecar uses the **same site-slug prefix** as the dossier (shared naming convention). It contains
normalized trait values that [DI-6] cross-site synthesis can parse and count without re-reading prose.
See `references/trait-record-template.yaml` for the full schema.

**Key contract points:**
- Every trait key comes from `trait-vocabulary.md` — no free-form keys
- Values use the controlled value buckets defined in the vocabulary
- The sidecar is emitted for BOTH depth levels (full and light)
- `_traits-` prefix ensures the file sorts adjacent to the dossier but is clearly machine-facing

---

## Procedure

### Step 0 — Locate and validate the capture package

1. Read `design-capture-manifest.json` at the provided capture package path.
2. Verify `engineVersion` is `2.1` or later. If unknown version, warn but proceed.
3. Confirm required artifacts exist on disk:
   - `design-tokens.json` (required)
   - `design-tokens.md` (required)
   - `motion-inventory.json` (required)
   - `component-inventory.json` (required)
   - `a11y-snapshot.json` (optional — degrade gracefully)
   - Screenshot directory (optional — dossier can be written without screenshots)

### Step 1 — Extract and interpret design tokens

Read `design-tokens.json` and apply the interpretation rules in
`references/visual-token-interpretation.md`:

1. **Palette:** Map raw hex values + usage counts to semantic roles (brand/accent, primary-text,
   background, surface, border, semantic-status). Group by role, not by frequency alone.
2. **Typography:** Map font instances to a type scale (h1→body→caption). Identify the primary font
   family, secondary/display if present, loading method (self-hosted, Google Fonts, system).
3. **Spacing:** Infer the base unit from the spacing histogram. Identify the dominant spacing values.
4. **Border-radius:** Classify the radius strategy (sharp, slightly-rounded, rounded, pill).
5. **Shadows:** Classify the shadow strategy (flat, subtle-elevation, pronounced-depth).

### Step 2 — Analyze motion and interaction

Read `motion-inventory.json`:

1. Identify animation libraries (Framer Motion, GSAP, AOS, Lottie, etc.) or "none/pure CSS."
2. Classify keyframe animations by purpose (loading, attention, transition, decorative).
3. Assess transition density (sparse, moderate, rich) and dominant timing functions.
4. Summarize the motion personality (minimal, subtle-functional, expressive, cinematic).

### Step 3 — Analyze component inventory

Read `component-inventory.json`:

1. Map detected components to pattern categories (hero, navigation, card-grid, CTA, testimonial,
   FAQ, footer).
2. Note structural details: card count in grids, CTA text/placement, FAQ item count.
3. Cross-reference with screenshots (if available) for visual context.

### Step 4 — Identify liftable patterns

Synthesize Steps 1-3 into named patterns:

1. Name each pattern concretely (e.g., "Dark split-image hero with gradient overlay," not "Hero").
2. Describe what makes it effective (layout, contrast, hierarchy, motion).
3. Tag each pattern with its `catalog/` landing pointer — where it would live in the verified
   catalog after graduation (e.g., `→ catalog/heroes/dark-hero-split-image`).
4. Identify patterns to SKIP — anything outdated, inaccessible, or not worth emulating.

### Step 5 — Assess accessibility and contrast

Read `a11y-snapshot.json` (if available):

1. Note heading hierarchy quality (proper nesting, semantic use).
2. Note alt-text coverage.
3. Flag worst contrast pairs (below AA threshold).
4. Patterns with accessibility issues get noted in "Patterns to skip" with the reason.

### Step 6 — Write the dossier

Select template based on `depth` parameter:
- `full` → read `references/dossier-template-full.md`
- `light` → read `references/dossier-template-light.md`
- custom → read the template override path

Fill the template with findings from Steps 1-5. Key rules:

- **Performance claims require evidence.** If `performance-data` input was provided, cite it with
  source and date. If not provided, write "Not assessed — no performance data provided" in the
  Why-it-performs section. Never fabricate rankings or CWV scores.
- **Legal boundary is mandatory** (full depth). Section 7 is never omitted.
- **Patterns carry catalog pointers** (both depths). Every pattern in section 5 (full) or the
  patterns list (light) includes a `→ catalog/<category>/<pattern-name>` pointer.
- **Frontmatter includes sector and archetype** if provided.

Write the dossier to `<output-path>/dossier-<site-slug>.md` (full) or
`<output-path>/inspiration-<site-slug>.md` (light).

### Step 7 — Write the trait sidecar

Read `references/trait-record-template.yaml` and `references/trait-vocabulary.md`.

Map dossier findings to the controlled vocabulary:

1. For each trait category in the vocabulary, select the matching value bucket.
2. Record the raw evidence (hex values, font names, pixel values) alongside the normalized trait.
3. Record all liftable pattern names as `patterns_worth_lifting` entries.
4. Record sector and archetype tags.

Write to `<output-path>/_traits-<site-slug>.yaml`.

### Step 8 — Self-check

Before declaring the dossier complete:

1. Verify the dossier has all required sections for its depth level.
2. Verify every pattern in section 5 has a `catalog/` pointer.
3. Verify the legal-boundary section (section 7) is present and non-empty (full depth).
4. Verify the trait sidecar YAML is valid and all keys exist in `trait-vocabulary.md`.
5. Verify the trait sidecar's `site_slug` matches the dossier filename.
6. Cross-check: at least 3 palette entries, at least 1 font family, at least 1 named pattern.

---

## Config-driven design

The skill is domain-agnostic by design. All domain-specific content comes from inputs, not hardcoded
assumptions:

| What | Where it comes from | NOT hardcoded |
|---|---|---|
| Dossier sections | Template file (selectable) | Section list |
| Output path | `output-path` parameter | `inspiration/high-performing/` |
| Sector/niche | `sector` parameter | `electrical-services` |
| Archetype | `archetype` parameter | Any specific archetype |
| Performance evidence | `performance-data` parameter | Rankings, CWV scores |
| Pattern catalog structure | `catalog/` pointers in patterns | Category taxonomy |
| Trait normalization | `trait-vocabulary.md` reference | Any specific trait values |

To fingerprint a SaaS landing page, an app screen, or an out-of-niche reference: provide a capture
package + the appropriate sector/archetype tags. No code changes needed.

---

## Reference files

| File | Purpose |
|---|---|
| `references/dossier-template-full.md` | 8-section full dossier template |
| `references/dossier-template-light.md` | Design-only light note template |
| `references/trait-record-template.yaml` | Machine-readable trait sidecar schema |
| `references/trait-vocabulary.md` | Controlled vocabulary for cross-site trait normalization |
| `references/visual-token-interpretation.md` | How to turn raw [DI-1] tokens into roles/decisions |

---

## Upstream contract

This skill reads the [DI-1] design-capture package as specified in
`site-capture-engine/references/design-capture-package-contract.md` (v2.1). The manifest
(`design-capture-manifest.json`) is the entry point — the skill never assumes internal file paths
directly; it reads them from the manifest's `artifacts` map.

If the capture package was produced by a different engine version, the skill checks `engineVersion`
and warns on unknown versions but does not refuse to run.

---

## Downstream consumers

| Consumer | What it reads | How |
|---|---|---|
| [DI-3] `reference-library` | The dossier `.md` file | Ingests into the curated library as a reference entry |
| [DI-4] `design-emulation-verify` | The dossier `.md` file | Uses as the comparison baseline for build verification |
| [DI-6] `design-pattern-synthesis` | The `_traits-*.yaml` sidecar | Parses normalized traits for cross-site counting and ranking |
| Manual use | The dossier `.md` file | Human reads the dossier for design inspiration and pattern lifting |

---

## Related

- [[site-capture-engine]] — upstream capture engine (v2.1+)
- [[competitor-deep-research]] — sibling landscape skill (composes; design dossiers moved here)
- [[design-emulation-verify]] — downstream build-vs-reference diff
- [[tactic-emulate-competitor-design-patterns-with-ai]] — the tactic this skill feeds
- [[strategy-custom-coded-nextjs-via-ai-with-competitor-inspiration]] — the strategy this supports
- `second-brain/03_domains/website-design/inspiration/high-performing/_README.md` — dossier format origin
- `second-brain/03_domains/website-design/inspiration/design-only/_README.md` — light note format origin
