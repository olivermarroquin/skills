---
type: reference
status: shipped
created: 2026-06-15
updated: 2026-06-15
version: "2.1"
tags: [reference, design-capture, site-capture-engine, package-contract, downstream-binding]
---

# Design-capture package contract (v2.1)

> **Downstream skills bind to this contract, not to individual file paths or internal assumptions.**
> [DI-2] design-fingerprint, [DI-3] reference-library, [DI-4] design-emulation-verify, and any
> future consumer reads the `design-capture-manifest.json` to discover what was captured and where
> each artifact lives. If the internal layout changes, the manifest absorbs the change — consumers
> never break.

## When the design-capture context fires

The design-capture output context activates when **either** condition is true:

1. **Path auto-detect:** the output folder matches `03_domains/website-design/inspiration/...` or
   any path containing `design-reference/` or `design-capture/`.
2. **Explicit flag:** `--design-capture` is passed to the capture scripts.

Design-capture runs **on top of** the universal capture — it is additive. The restoration-package
and teardown-analysis contexts are unaffected and produce identical output regardless of whether
design-capture also runs.

## Artifact inventory

All paths are relative to the capture output directory (e.g., `<out-dir>/<YYYY-MM-DD>/`).

### 1. Rendered screenshots (multi-breakpoint)

| Viewport | Width | Naming pattern |
|---|---|---|
| Desktop | 1440px | `<tier>__desktop__fold.png`, `<tier>__desktop__full.png` |
| Tablet | 768px | `<tier>__tablet__fold.png`, `<tier>__tablet__full.png` |
| Mobile | 390px | `<tier>__mobile__fold.png`, `<tier>__mobile__full.png` |

**Per-section crops:** `sections/<tier>__<viewport>__section-<N>.png` — one per detected major
section (header, hero, service grid, FAQ, CTA block, testimonial, footer, etc.). The fold line
is recorded in the screenshot manifest (pixel offset from top).

**Scroll-stop captures:** `scroll-stops/<tier>__<viewport>__scroll-<N>.png` — captures at each
viewport-height scroll interval, recording scroll-triggered animation reveals. Capped at 10 per
page×viewport.

**Component screenshots:** `components/<tier>__<component-type>.png` — bounding-box crop of each
detected recurring component (desktop viewport). Types: `hero`, `primary-nav`, `footer`,
`card-grid`, `cta-block`, `testimonial`, `faq-accordion`.

**Screenshot manifest:** `screenshot-manifest.json` — indexes every screenshot with metadata:

```json
{
  "capturedAt": "ISO-8601",
  "engineVersion": "2.1",
  "domain": "https://example.com",
  "viewports": [
    { "name": "desktop", "width": 1440, "height": 900 },
    { "name": "tablet", "width": 768, "height": 1024 },
    { "name": "mobile", "width": 390, "height": 844 }
  ],
  "pages": [{ "tier": "home", "path": "/", "url": "https://example.com/" }],
  "screenshots": [
    {
      "file": "home__desktop__fold.png",
      "type": "fold | full-page | section-crop | scroll-stop | component",
      "viewport": "desktop",
      "page": "home",
      "url": "https://example.com/",
      "section": { "index": 1, "tag": "section", "className": "hero", "belowFold": false },
      "scrollY": 0,
      "component": "hero"
    }
  ],
  "totals": {
    "standard": 6,
    "sectionCrops": 12,
    "scrollStops": 15,
    "components": 5
  }
}
```

### 2. Computed-style design tokens

| File | Format | Description |
|---|---|---|
| `design-tokens.json` | JSON | Machine-readable: palette (hex + count + role), typography (per role), spacing (histogram + base unit), border-radius set, shadow set |
| `design-tokens.md` | Markdown | Human-readable summary matching the established dossier format (palette table, type scale, spacing, radius, shadows, motion, reproduction note) |

**Key contract points:**
- Tokens are extracted via `getComputedStyle` on the live rendered DOM, not from source CSS.
- Colors are deduplicated and ranked by usage frequency with inferred roles (page-background,
  primary-text, brand/accent, secondary-accent, border).
- Typography is grouped by semantic role (h1–h6, body, button, caption, link, label).
- Spacing histogram infers a base unit (typically 4px or 8px).

### 3. Motion / interaction inventory

| File | Format |
|---|---|
| `motion-inventory.json` | JSON |

Contents:
- `libraries`: detected animation libraries (Framer Motion, GSAP, AOS, Lottie, Intersection Observer)
- `keyframes`: CSS `@keyframes` rules found in accessible stylesheets (name + keyframe count)
- `transitions`: elements with CSS transitions (element selector + transition value, up to 50)
- `animations`: elements with CSS animations (element selector + animation name/duration/timing, up to 50)

### 4. Component inventory

| File | Format |
|---|---|
| `component-inventory.json` | JSON |

Contents:
- Array of detected components, each with:
  - `type`: one of `hero`, `primary-nav`, `footer`, `card-grid`, `cta-block`, `testimonial`, `faq-accordion`
  - `selector`: CSS-like selector of the detected element
  - `bounds`: bounding rectangle `{ top, left, width, height }`
  - `childCount` (card-grid): number of child cards
  - `count` (CTA/testimonial/FAQ): instance count
  - `samples` (CTA): up to 5 CTA text + href pairs

### 5. A11y / contrast snapshot

| File | Format |
|---|---|
| `a11y-snapshot.json` | JSON |

Contents:
- `headingHierarchy`: ordered list of headings with level (1–6) and text
- `altText`: total images, with-alt, without-alt, decorative (empty alt), coverage percent
- `contrastPairs`: up to 20 foreground/background pairs, sorted worst-first, each with:
  - `foreground`, `background` (hex)
  - `ratio` (rounded to 2 decimal places)
  - `passAA` (≥4.5:1), `passAAA` (≥7:1), `passAALarge` (≥3:1)

### 6. Design-capture manifest

| File | Format |
|---|---|
| `design-capture-manifest.json` | JSON |

The **top-level index** that downstream skills read first. Structure:

```json
{
  "capturedAt": "ISO-8601",
  "engineVersion": "2.1",
  "url": "https://example.com",
  "title": "Example Site",
  "viewports": ["desktop-1440", "tablet-768", "mobile-390"],
  "artifacts": {
    "designTokens": { "json": "design-tokens.json", "md": "design-tokens.md" },
    "screenshots": { "manifest": "<date>/screenshot-manifest.json", "dir": "<date>/" },
    "motionInventory": "motion-inventory.json",
    "componentInventory": "component-inventory.json",
    "a11ySnapshot": "a11y-snapshot.json"
  },
  "captureConfig": {
    "designCapture": true,
    "scrollStopsPerPage": 10,
    "maxSectionsPerPage": 20,
    "tokenExtractionMethod": "getComputedStyle (live DOM)"
  }
}
```

## Legal boundary (carried from site-capture-engine v2.0)

The design-capture context captures **patterns and measurements** from publicly rendered pages:
- Color values, font metrics, spacing values, contrast ratios — these are facts, not copyrightable.
- Screenshots are captured for **internal reference only** — not for redistribution.
- No auth-walled content is captured without explicit operator authorization.
- Asset files (photos, logos, custom illustrations) are **never** redistributed. The capture
  documents what exists; the reproduction uses original assets per the client's brand.

## Versioning

This contract version matches the engine version in `SKILL.md`. When the contract changes:
1. Bump `engineVersion` in all emitted manifests.
2. Update this file.
3. Downstream skills check `engineVersion` and surface a warning if they encounter an unknown version.

## Producing scripts

| Script | What it produces |
|---|---|
| `scripts/capture_screenshots.mjs --design-capture` | All screenshot artifacts + `screenshot-manifest.json` |
| `scripts/extract_design_tokens.mjs` | `design-tokens.json`, `design-tokens.md`, `motion-inventory.json`, `component-inventory.json`, `a11y-snapshot.json` |

Both scripts are idempotent — re-running overwrites previous output in the same dated directory.
