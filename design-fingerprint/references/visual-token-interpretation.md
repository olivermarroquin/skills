---
type: reference
status: active
created: 2026-06-16
updated: 2026-06-16
skill: design-fingerprint
tags: [reference, design-fingerprint, design-tokens, interpretation-rules]
---

# Visual token interpretation rules

> How to turn raw [DI-1] computed-style tokens into semantic roles and design decisions.
> The design-fingerprint skill applies these rules in Step 1 of its procedure.

## 1. Palette interpretation

### Role assignment algorithm

Given the palette array from `design-tokens.json` (sorted by usage frequency):

1. **Primary text:** The most-used color on text elements. Usually `#ffffff` (dark themes) or
   `#000000` / `#1a1a1a` (light themes).
2. **Page background:** The most-used color on background properties. Usually opposite of primary
   text — `#1e1e1e`/`#0a0a0a` (dark) or `#ffffff`/`#f5f5f5` (light).
3. **Brand / accent:** The highest-frequency NON-neutral color (not white, black, or gray). This is
   the color that "owns" CTAs and interactive elements. Threshold: if the top non-neutral color has
   ≥50 uses, it's the brand color; if <50, the site may lack a dominant accent.
4. **Surface / card:** A color close to but distinct from the page background, used on cards/panels.
   Often 1-2 shades lighter (dark theme) or darker (light theme) than the background.
5. **Border:** Low-opacity or gray values used on border properties. Usually neutral.
6. **Semantic colors:** Red/green/amber/blue used for status indicators, warnings, success states.
   Identified by hue, not by usage frequency.

### Neutral detection

A color is "neutral" if its saturation (in HSL) is ≤10% OR it is within the set:
`#000`, `#111`–`#eee`, `#fff`, and their 6-digit equivalents. This prevents white/black/gray
from being classified as the brand color.

### Theme detection

- **Dark theme:** page-background lightness ≤30% (HSL L value)
- **Light theme:** page-background lightness ≥70%
- **Mixed:** neither clear threshold, or multiple background colors span both

### Palette personality (human-readable summary)

Template: `"{theme} theme ({background_hex}) + {brand_personality} {brand_color_name} ({brand_hex})
accent + {text_color} text. {energy_assessment}."`

Energy assessment:
- High-contrast brand on dark = "High-contrast, high-energy"
- Muted brand on light = "Refined, understated"
- Multiple bright accents = "Playful, multi-accent"

## 2. Typography interpretation

### Font role assignment

From the `design-tokens.json` typography array (instances per role):

1. **Primary body font:** The font-family on `body` role elements. This is the site's reading font.
2. **Heading font:** The font-family on `h1`/`h2` roles. Same as body = single-font system; different
   = dual-font system.
3. **Display / accent font:** Any third font-family used on ≤5 elements. Rare.
4. **Mono font:** Any monospace font — usually for code or technical UI.

### Loading method detection

From the capture package context (not in tokens directly — infer from the capture):
- `next/font` self-hosted woff2 → "Self-hosted via next/font (optimal)"
- Google Fonts `<link>` → "Google Fonts (external dependency)"
- `@font-face` local files → "Self-hosted (@font-face)"
- System fonts only → "System font stack (no external fonts)"

### Type scale classification

Map the size values from typography roles to a scale:

| Classification | Characteristic |
|---|---|
| Tight | h1 ≤ 36px, small body (14px) |
| Standard | h1 36-48px, body 16px |
| Generous | h1 48-72px, body 16-18px |
| Display-heavy | h1 ≥ 72px, large size jumps between levels |

## 3. Spacing interpretation

### Base unit inference

The `design-tokens.json` reports an "inferred base unit" from the spacing histogram.

- **4px base:** The Tailwind/standard web convention. Most common.
- **8px base:** Material Design convention.
- **2px base:** Mathematically valid but usually means the base unit is actually 4px or 8px with
  half-step subdivisions.
- **Other:** Custom system. Note the value.

### Spacing personality

- **Tight:** dominant values ≤16px, dense layouts
- **Balanced:** mix of 16-32px dominant values
- **Generous:** dominant values ≥24px, airy/spacious layouts

## 4. Border-radius interpretation

### Strategy classification

| Dominant radius | Classification | Personality |
|---|---|---|
| 0px (no radius) | Sharp | Technical, editorial, brutalist |
| 2-4px | Slightly rounded | Professional, subtle |
| 8-12px | Rounded | Friendly, modern |
| 16-24px | Very rounded | Soft, approachable |
| ≥9999px or very large | Pill | Playful, button-focused |
| Mix of sharp + pill | Hybrid | Cards sharp, buttons pill |

### Handling extreme values

Values like `3.35544e+07px` (≈`border-radius: 9999px`) are the CSS pill trick — classify as "pill"
and normalize to `9999px` in the dossier rather than showing the scientific notation.

## 5. Shadow interpretation

### Strategy classification

| Shadow presence | Classification |
|---|---|
| All `0px 0px 0px` or transparent | Flat (no elevation) |
| Present but subtle (≤4px blur, low opacity) | Subtle elevation |
| Pronounced (≥8px blur, visible) | Pronounced depth |
| Multiple shadow layers | Layered / neumorphic |

### Handling truncated values

The tokens file often truncates long shadow values. If the shadow string ends in `…`, classify based
on visible parameters. If all visible shadow values are `rgba(0,0,0,0)`, the site is effectively flat.

## 6. Motion interpretation

### Motion personality matrix

| Libraries | Keyframes | Transitions | Classification |
|---|---|---|---|
| None | ≤2 | ≤10 | Minimal |
| None | 3-5 | 10-30 | Subtle-functional |
| None or 1 library | ≥5 | ≥30 | Expressive |
| GSAP/Framer/Lottie | Any | Any | Cinematic (library-driven) |

### Standard Tailwind keyframes

`spin`, `ping`, `pulse`, `bounce` are Tailwind defaults — note them but don't overweight. These
indicate Tailwind usage, not custom animation design. Custom keyframe names indicate intentional
motion design.
