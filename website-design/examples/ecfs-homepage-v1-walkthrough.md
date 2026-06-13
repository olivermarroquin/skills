---
type: example
status: active
skill: website-design
description: Worked example — East Coast Furniture Services homepage v1 (Fable, 2026-06-11)
created: 2026-06-12
updated: 2026-06-12
client: east-coast-furniture-services
designer: fable (subagent)
tags: [example, website-design, ecfs, fable, worked-example]
---

# Worked example — East Coast Furniture Services homepage v1

The first dogfood run of the website-design skill. Mockup and design notes live at:
- `04_projects/clients/_prospects/east-coast-furniture-services/mockup-homepage-v1.html` (~1000 lines)
- `04_projects/clients/_prospects/east-coast-furniture-services/mockup-homepage-v1-design-notes.md`

## Inputs provided

| Input | Source | Content |
|---|---|---|
| Client brief | `prospect-intake` → `analysis/brief.md` | B2B commercial office furniture, $1B+ installed, 30 yrs, MBE, 8 brand partners, GoDaddy brochure site |
| Content inventory | Extracted from existing site + brief | 4 service lines, brand partner list, vertical list, NAP, scale claims |
| Design direction | Positioning: "government-grade + premium contractor" + audit gap list (misspelled name, broken logos, empty portfolio) |
| Imagery constraints | No photography available, no AI generation in mockup phase → constraint-as-asset |

## Design system derived (Step 2)

| Token | Value | Reasoning |
|---|---|---|
| Primary | Navy (#0a1521 → #2a4d70 scale) | Institutional/government-grade — inverts client's washed-out blue-grey |
| Accent | Brass (#c79a4b) | Premium contractor, not decorative — sparingly used for CTAs and eyebrows |
| Display font | Fraunces (optical size serif) | 30-year-firm authority an all-sans page wouldn't convey |
| Body font | Manrope | Clean, modern, excellent weight range |
| Imagery | Inline SVG — installation floorplan on blueprint grid | Constraint-as-asset: speaks the buyer's language (facilities/PM) |

## Techniques applied

| # | Technique | How it manifested |
|---|---|---|
| 1 | Constraint-as-asset | Inline-SVG installation floorplan (workstation pods, conference oval, privacy booths, dashed glass-wall callout) on a blueprint grid background. Floating stat chips anchor proof points. |
| 2 | Palette-as-positioning | Navy = institutional; brass = premium. Explicit inversion of client's washed-out #c0ccd0. |
| 3 | Proof-point spine | $1B / 30 yrs / MBE / 8 brands at 3 depths: hero proof line → full stats bar → MBE seal card |
| 4 | Copy to buyer's risk | "The schedule holds" — office furniture buyers' #1 fear is project delay. Portfolio captions: "nights/weekends phasing, GSA asset tracking, semester-break turnaround" |
| 5 | Dark/light rhythm | Nav (dark) → Hero (dark gradient) → Stats (dark) → Services (white) → Partners (paper-warm) → Portfolio (paper) → MBE (dark) → Verticals (white) → Area (paper) → Form (dark) → Footer (darkest) |
| 6 | Conversion plumbing | Sticky quote button + clickable phone in nav + brass CTA at each scroll depth + pre-modeled quote form (project type, timeline, facility size) |

## Page structure (Step 3 output)

1. Sticky nav — logo (gradient mark + text) + 5 links + phone + "Request a Quote" CTA
2. Hero — MBE badge + "Your furniture. Installed on schedule. *Every time.*" + sub + dual CTAs + proof line + SVG floorplan
3. Stats spine — $1B+ / 30+ Years / MBE / 8 Partners (full-width dark bar)
4. Services — 4 cards: Installation / Asset Management / Relocation / Architectural Walls
5. Brand partners — 8 partner logos (Fraunces text treatment since logos broken on current site)
6. Portfolio — 3 project cards with CSS gradient "images" + line-icon glyphs + operational captions
7. MBE/Credibility — seal card with transactional framing ("one subcontract, two boxes checked")
8. Verticals — 6 vertical cards (GSA/Gov, Legal, Education, Healthcare, Finance, Commercial)
9. Service area — MD/DC/DE/VA with city-grid text
10. Quote form — pre-modeled fields (name, company, phone, email, project type, timeline, details)
11. Footer — NAP + links + copyright (name spelled correctly)

## What Fable did well

- Palette reasoning was the strongest design choice — the navy/brass system argues "government-grade premium" without a word of copy
- The SVG floorplan was not prompted — Fable generated the constraint-as-asset move independently when told "no stock imagery"
- Typography pairing (Fraunces + Manrope) was sophisticated — the serif carries authority the body sans alone wouldn't
- Eyebrow label system (uppercase, letter-spaced, brass-colored, with a leading line) created consistent editorial hierarchy across all sections
- Copy was buyer-fear-oriented without being prompted for it — "the schedule holds" was Fable's choice

## What needed iteration

- Portfolio "images" are CSS gradient + texture approximations — they read as architecture but are obviously not photographs. On signing, real project photos replace these.
- Form is a visual placeholder (no backend) — needs wiring for the build
- Mobile breakpoints were present but could be tighter (some section padding too generous on 375px)
- No JSON-LD schema in the mockup — intentional (mockup ≠ production), but the build must add it

## Reusable patterns extracted → skill references

1. **Constraint-as-asset** → Technique 1 in SKILL.md
2. **Palette-as-positioning** → Technique 2 + derivation guide in `design-system-template.md`
3. **Proof-point spine** → Technique 3 in SKILL.md
4. **Copy to buyer's risk** → Technique 4 in SKILL.md
5. **Dark/light rhythm** → Technique 5 + section rhythm template in `design-system-template.md`
6. **Conversion plumbing everywhere** → Technique 6 in SKILL.md
7. **CSS custom properties as design system** → `design-system-template.md` (extractable to Tailwind)
