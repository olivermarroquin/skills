---
type: reference
status: active
skill: website-design
description: Template for the CSS custom properties design system — copy and fill per client
created: 2026-06-12
updated: 2026-06-12
tags: [reference, website-design, design-system, css, template]
---

# Design system template — CSS custom properties

Copy this `:root` block into the mockup and fill in per-client values. These properties become the
Tailwind theme tokens when the mockup graduates to a Next.js build.

```css
:root {
  /* ===== PALETTE ===== */
  /* Primary: the authority/trust color (dark, commanding) */
  --primary-950: ;  /* darkest — nav bg, hero bg, dark sections */
  --primary-900: ;  /* dark — headings, footer */
  --primary-800: ;  /* medium-dark — card backgrounds on dark sections */
  --primary-700: ;  /* hover states on dark elements */
  --primary-600: ;  /* lighter accent on dark backgrounds */

  /* Accent: the action/premium color (warm, used sparingly) */
  --accent-500: ;   /* primary CTA bg, eyebrow text, highlights */
  --accent-400: ;   /* hover state, on-dark text accent */
  --accent-600: ;   /* darker accent for body text accents */

  /* Neutrals */
  --ink: ;          /* body text color */
  --slate-600: ;    /* secondary text */
  --slate-400: ;    /* tertiary text, captions */
  --line: ;         /* borders, dividers */
  --paper: ;        /* light section backgrounds */
  --paper-warm: ;   /* alternate light backgrounds (warmer) */
  --white: #ffffff;

  /* ===== TYPOGRAPHY ===== */
  --font-display: ;  /* e.g., "Fraunces", Georgia, serif */
  --font-body: ;     /* e.g., "Manrope", system-ui, -apple-system, sans-serif */

  /* ===== SPACING ===== */
  --radius: 14px;           /* card border-radius */
  --section-pad: 96px;      /* vertical section padding */
  --wrap-max: 1180px;       /* max content width */
  --wrap-pad: 28px;         /* horizontal content padding */

  /* ===== SHADOWS ===== */
  --shadow-sm: 0 1px 2px rgba(0,0,0,.06), 0 2px 8px rgba(0,0,0,.05);
  --shadow-md: 0 4px 14px rgba(0,0,0,.08), 0 12px 32px rgba(0,0,0,.10);
  --shadow-lg: 0 24px 60px rgba(0,0,0,.22);
}
```

## Palette derivation guide

| Client positioning | Primary | Accent | Why |
|---|---|---|---|
| Government-grade + premium | Deep navy (#0a1521) | Warm brass (#c79a4b) | Navy = institutional; brass = premium contractor |
| Emergency/urgent service | Deep charcoal (#1a1a2e) | Electric amber (#f59e0b) | Dark = serious; amber = urgency |
| Eco/sustainable | Forest green (#1b4332) | Warm gold (#d4a843) | Green = growth/nature; gold = quality |
| Modern/tech-forward | Cool slate (#0f172a) | Bright blue (#3b82f6) | Slate = sophistication; blue = trust/tech |
| Warm/community | Rich brown (#3c1518) | Terracotta (#c2703e) | Brown = warmth; terracotta = earth/craft |
| Clean/medical/precision | Pure white bg + navy text | Teal (#0d9488) | White = clinical; teal = care + precision |

## Typography pairing guide

| Client type | Display (headlines) | Body | Why |
|---|---|---|---|
| Established / authority | Serif (Fraunces, Playfair, Lora) | Sans (Manrope, Inter, DM Sans) | Serif = gravitas; sans = readability |
| Modern / startup | Geometric sans (Plus Jakarta, Outfit) | Sans (Inter, Geist) | Both modern; weight contrast separates |
| Craft / artisan | Slab serif (Bitter, Zilla Slab) | Humanist sans (Source Sans, Nunito) | Slab = handmade; humanist = approachable |
| Professional services | Classic serif (Merriweather, Libre Baskerville) | System sans (system-ui) | Classic = trust; system = fast-loading |

## Font size scale (clamp-based)

```css
h1 { font-size: clamp(38px, 5.4vw, 62px); }
h2 { font-size: clamp(30px, 4vw, 42px); }
h3 { font-size: clamp(22px, 2.5vw, 28px); }
.eyebrow { font-size: 12px; font-weight: 800; letter-spacing: .22em; text-transform: uppercase; }
body { font-size: 16px; line-height: 1.6; }
.section-lede { font-size: 17.5px; }
```

## Section rhythm template

Standard dark/light alternation:

| Section | Background | Text |
|---|---|---|
| Nav (sticky) | `--primary-950` (translucent + blur) | White |
| Hero | `--primary-900` → `--primary-950` gradient | White + accent highlights |
| Stats | `--primary-950` | White |
| Services | `--white` | `--ink` |
| Portfolio | `--paper-warm` | `--ink` |
| Credibility | `--primary-900` | White |
| Verticals | `--white` or `--paper` | `--ink` |
| Service area | `--paper` | `--ink` |
| Form | `--primary-950` | White |
| Footer | `--primary-950` (darkest) | Muted white |
