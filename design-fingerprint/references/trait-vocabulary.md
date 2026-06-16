---
type: reference
status: active
created: 2026-06-16
updated: 2026-06-16
skill: design-fingerprint
consumers: [design-fingerprint, design-pattern-synthesis]
tags: [reference, design-fingerprint, trait-vocabulary, controlled-vocabulary, cross-site-analysis]
---

# Trait vocabulary (controlled)

> The canonical controlled vocabulary for cross-site trait normalization. Every `_traits-*.yaml`
> sidecar produced by the `design-fingerprint` skill uses ONLY keys and value buckets defined here.
> [DI-6] `design-pattern-synthesis` reads this file to know what traits exist and how to count them.
>
> **Adding new traits:** Append to the relevant category below. Never remove a trait that existing
> sidecars use — deprecate by adding `deprecated: true` and a migration note. Bump the vocabulary
> version when adding traits.

**Vocabulary version:** 1.0

---

## Category: palette_structure

Describes the site's color system at a structural level.

| Trait key | Value buckets | Description |
|---|---|---|
| `theme` | `dark`, `light`, `mixed` | Overall page background lightness |
| `brand_color_count` | `single-accent`, `dual-accent`, `multi-accent` | How many non-neutral brand colors dominate |
| `brand_hue_family` | `red`, `orange`, `yellow`, `green`, `cyan`, `blue`, `purple`, `pink`, `neutral-only` | Hue family of the primary brand color |
| `contrast_strategy` | `high-contrast`, `medium-contrast`, `low-contrast` | Brand-on-background contrast level |
| `semantic_colors` | `present`, `absent` | Whether red/green/amber status colors are used |
| `palette_size` | `minimal` (≤4), `standard` (5-7), `extended` (8+) | Total distinct intentional colors |

## Category: type_family

Describes typography choices.

| Trait key | Value buckets | Description |
|---|---|---|
| `font_system` | `single-font`, `dual-font`, `multi-font` | How many distinct font families are used |
| `primary_font_class` | `geometric-sans`, `humanist-sans`, `neo-grotesque`, `serif`, `slab-serif`, `mono`, `display`, `system-stack` | Classification of the primary body font |
| `heading_font_class` | (same buckets as primary) | Classification of the heading font (if different from body) |
| `font_loading` | `self-hosted`, `google-fonts`, `typekit`, `system-stack` | How fonts are loaded |
| `weight_range` | `narrow` (1-2 weights), `standard` (3-4), `wide` (5+) | How many font weights are used |

## Category: type_scale

Describes the sizing system for text.

| Trait key | Value buckets | Description |
|---|---|---|
| `scale_spread` | `tight`, `standard`, `generous`, `display-heavy` | h1-to-body size ratio classification |
| `h1_size_bucket` | `small` (≤36px), `medium` (37-48px), `large` (49-72px), `display` (73px+) | Absolute h1 size |
| `body_size` | `compact` (≤14px), `standard` (15-16px), `generous` (17-18px), `large` (19px+) | Body text size |

## Category: layout_grid

Describes layout and grid patterns.

| Trait key | Value buckets | Description |
|---|---|---|
| `layout_type` | `single-column`, `sidebar`, `multi-column`, `asymmetric`, `full-bleed-sections` | Dominant page layout structure |
| `hero_style` | `full-bleed-image`, `split-image-text`, `text-only`, `video-background`, `slider-carousel`, `gradient-overlay`, `illustration`, `none` | Above-the-fold hero pattern |
| `section_density` | `sparse` (≤5 sections), `standard` (6-10), `dense` (11+) | Number of distinct sections on the primary page |
| `card_grid_columns` | `2-col`, `3-col`, `4-col`, `masonry`, `none` | Dominant card grid column count |
| `cta_placement` | `hero-only`, `hero-and-sections`, `sticky`, `floating`, `inline-distributed` | Where primary CTAs appear |
| `navigation_style` | `fixed-top`, `sticky-top`, `static-top`, `sidebar`, `hamburger-only`, `mega-menu` | Primary navigation pattern |
| `footer_style` | `minimal` (1 row), `standard` (2-3 columns), `mega-footer` (4+ columns), `none` | Footer complexity |

## Category: spacing_system

Describes the spacing and rhythm approach.

| Trait key | Value buckets | Description |
|---|---|---|
| `spacing_base` | `4px`, `8px`, `other` | Inferred spacing base unit |
| `spacing_personality` | `tight`, `balanced`, `generous` | Dominant spacing feel |
| `content_width` | `narrow` (≤800px), `standard` (801-1200px), `wide` (1201px+) | Max content container width |

## Category: shape_and_depth

Describes border-radius and shadow strategies.

| Trait key | Value buckets | Description |
|---|---|---|
| `radius_strategy` | `sharp`, `slightly-rounded`, `rounded`, `very-rounded`, `pill`, `hybrid` | Dominant border-radius approach |
| `shadow_strategy` | `flat`, `subtle-elevation`, `pronounced-depth`, `layered` | Shadow usage pattern |

## Category: motion_type

Describes animation and interaction patterns.

| Trait key | Value buckets | Description |
|---|---|---|
| `motion_personality` | `minimal`, `subtle-functional`, `expressive`, `cinematic` | Overall motion design approach |
| `animation_source` | `none`, `css-only`, `tailwind-defaults`, `gsap`, `framer-motion`, `aos`, `lottie`, `custom-css`, `multi-library` | What drives the animations |
| `transition_density` | `sparse` (≤10), `moderate` (11-30), `rich` (31+) | Number of elements with CSS transitions |
| `scroll_animation` | `none`, `fade-in`, `slide-in`, `parallax`, `reveal-on-scroll`, `complex` | Scroll-triggered animation type |

## Category: cta_pattern

Describes call-to-action design patterns.

| Trait key | Value buckets | Description |
|---|---|---|
| `primary_cta_style` | `solid-button`, `outline-button`, `ghost-button`, `link-style`, `pill-button`, `gradient-button` | Visual style of the primary CTA |
| `cta_urgency` | `none`, `subtle` (color only), `moderate` (pulse/glow), `high` (animation + color + urgency text) | How urgently CTAs demand attention |
| `cta_count_above_fold` | `0`, `1`, `2`, `3+` | CTAs visible without scrolling |

## Category: trust_device

Describes trust and credibility patterns.

| Trait key | Value buckets | Description |
|---|---|---|
| `review_display` | `none`, `star-rating`, `testimonial-cards`, `carousel`, `video-testimonials`, `aggregate-badge` | How reviews/testimonials are displayed |
| `trust_badges` | `none`, `license-badges`, `association-logos`, `award-badges`, `certification-seals`, `mixed` | Trust badge types present |
| `social_proof` | `none`, `review-count`, `customer-count`, `case-studies`, `logos-strip` | Social proof mechanisms |

## Category: schema_type

Describes structured data and SEO markup.

| Trait key | Value buckets | Description |
|---|---|---|
| `primary_schema` | `none`, `LocalBusiness`, `Organization`, `WebSite`, `Product`, `SoftwareApplication`, `other` | Primary JSON-LD schema type |
| `schema_breadth` | `none`, `basic` (1-2 types), `moderate` (3-5), `rich` (6+) | How many schema types are used |

## Category: tooling_and_libraries

Describes the technical stack as visible from the frontend.

| Trait key | Value buckets | Description |
|---|---|---|
| `framework` | `nextjs`, `gatsby`, `nuxt`, `remix`, `astro`, `wordpress`, `webflow`, `squarespace`, `custom`, `unknown` | Frontend framework |
| `css_framework` | `tailwind`, `bootstrap`, `bulma`, `material-ui`, `chakra`, `styled-components`, `css-modules`, `vanilla`, `unknown` | CSS framework |
| `image_optimization` | `next-image`, `cloudinary`, `imgix`, `native-responsive`, `unoptimized` | Image delivery strategy |

---

## Versioning

When adding new trait keys:
1. Append to the relevant category (never reorder existing keys).
2. Bump vocabulary version at the top of this file.
3. Existing sidecars remain valid — new keys are simply absent in older sidecars.
4. [DI-6] handles missing keys gracefully (counts as "not measured," not "absent").

When deprecating a trait key:
1. Add `(deprecated v1.x — use {{replacement}} instead)` to the description.
2. Do NOT remove the row — old sidecars still reference it.
3. [DI-6] maps deprecated keys to their replacements during ingestion.
