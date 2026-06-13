---
type: reference
status: active
skill: website-design
description: Fable vs default model (Claude Opus 4.6) comparison on the same ECFS homepage brief
created: 2026-06-12
updated: 2026-06-12
test-subject: east-coast-furniture-services
tags: [reference, website-design, fable, model-comparison, evidence]
---

# Fable vs default model comparison — ECFS homepage

Both models received the same brief (East Coast Furniture Services, B2B commercial office furniture,
$1B+, MBE, no photography) and produced a single-file HTML homepage mockup.

> **Method caveat:** All verdicts in this comparison are **code-read-only** — the assessor read the
> HTML/CSS source and evaluated design decisions from the code. Neither mockup was rendered in a
> browser at the 4 required viewport widths (1440/1024/768/375px) during the comparison. Visual
> quality claims (palette recognizability, headline hierarchy richness, SVG legibility, responsive
> behavior) are **provisional pending render evidence**. To finalize: open both files in a browser,
> capture screenshots at all 4 widths, and re-evaluate. Render evidence should be saved to the
> prospect folder alongside the mockups.

## Test conditions

| | Fable (v1) | Default / Opus 4.6 (v2) |
|---|---|---|
| Date | 2026-06-11 | 2026-06-12 |
| Substrate | Cowork (Fable subagent) | Claude Code (agent) |
| Brief | Prospect-intake brief + audit | Same brief (condensed) |
| Line count | ~1004 | ~1050 |
| File | `mockup-homepage-v1.html` | `mockup-homepage-v2-default-model.html` |

## Head-to-head comparison

### Palette

| | Fable | Default |
|---|---|---|
| Primary | Deep navy (#0a1521–#2a4d70) | Slate-charcoal (#0c1222–#1e293b) |
| Accent | Warm brass (#c79a4b) | Copper/terracotta (#c2703e) |
| Rationale | Navy = institutional/government; brass = premium | Charcoal = serious/contemporary; copper = materiality/craft |
| **Verdict** | **Stronger.** Navy + brass is more immediately recognizable as "government-grade premium" — the exact positioning ECFS needs for GSA/institutional buyers. | Valid alternative. More contemporary but less immediately coded for the B2B government niche. |

### Typography

| | Fable | Default |
|---|---|---|
| Display | Fraunces (optical-size serif) | DM Serif Display |
| Body | Manrope | Inter |
| Rationale | Fraunces = editorial gravitas + warmth | DM Serif = institutional/plain authority |
| **Verdict** | **Stronger for brand differentiation.** Fraunces's optical size variation creates a richer headline hierarchy. DM Serif is safer/plainer. | More conventional — safer choice, less distinctive. |

### Hero imagery (no-photography constraint)

| | Fable | Default |
|---|---|---|
| Approach | Detailed inline SVG — specific floorplan with workstation pods, conference oval, privacy booths, glass-wall callout, blueprint grid | CSS grid pattern + div-based architectural shapes, more atmospheric/ambient |
| **Verdict** | **Stronger.** The SVG floorplan is a specific, legible artifact that speaks the buyer's language. The CSS approach is more mood than substance. | The CSS approach is easier to produce but less impactful. |

### Proof-point structure

| | Fable | Default |
|---|---|---|
| Approach | Proof-point spine at 3 escalating depths (hero line → stats bar → MBE seal card) | Stats bar as separate section + credibility section later |
| **Verdict** | **Stronger.** The 3-depth spine is architecturally more interesting and reinforces credibility through repetition. | The separated approach is more conventional/scannable but less architecturally cohesive. |

### Copy voice

| | Fable | Default |
|---|---|---|
| Register | Editorial/luxury — "The schedule holds" | Institutional/direct — "Your project opens on schedule. Period." |
| Portfolio captions | Operational detail: "nights/weekends phasing, GSA asset tracking" | Similar operational detail with CSS-drawn project visualizations |
| **Verdict** | **Tie.** Both are buyer-fear-oriented. Fable is more polished; default is more direct. Both work for this audience. Client preference decides. |

### Conversion plumbing

| | Fable | Default |
|---|---|---|
| Approach | Sticky quote button + phone in nav, brass CTA at every depth, pre-modeled form | Similar: sticky nav, dual CTAs, form with Target Completion Date field, mobile sticky bottom bar |
| **Verdict** | **Tie.** Both are well-plumbed. Default's "Target Completion Date" form field is a nice qualifying touch. |

### Unique strengths

**Fable-only wins:**
- The constraint-as-asset SVG floorplan — this was generated independently (not prompted), demonstrating Fable's design intuition
- Eyebrow label system with leading-line decorators — more polished editorial hierarchy
- MBE "transactional framing" ("one subcontract, two boxes checked") — stronger for the buyer

**Default-only wins:**
- Concentric-ring credibility visual — interesting alternative to Fable's seal card
- "Target Completion Date" form field — better lead qualification
- Mobile sticky bottom CTA bar — explicit mobile conversion optimization

## Summary verdict

| Axis | Winner | Margin |
|---|---|---|
| Palette | Fable | Moderate — navy+brass is more niche-coded for B2B government |
| Typography | Fable | Slight — Fraunces is more distinctive; DM Serif is safer |
| Hero visual | Fable | Clear — inline SVG floorplan vs atmospheric CSS patterns |
| Page structure | Fable | Slight — proof-spine vs conventional stats bar |
| Copy quality | Tie | Both buyer-fear-oriented, different registers |
| Conversion | Tie | Both well-plumbed with different form innovations |
| Overall | **Fable** | Fable produces a more design-forward, distinctive mockup. Default produces a solid, conventional mockup. |

## Recommendation for the skill

**Use Fable for initial design concepts when available.** Fable's design intuitions — particularly
the constraint-as-asset move, palette-as-positioning, and the proof-point spine structure — are
stronger out of the box. The default model can produce a high-quality mockup using the techniques
documented in SKILL.md, but Fable demonstrates stronger first-pass design creativity.

**The default model is fully capable when Fable is unavailable.** The techniques extracted from
Fable's run (Techniques 1-6 in SKILL.md) serve as the playbook that brings the default model's
output closer to Fable's level. The skill documentation exists precisely to codify what Fable does
intuitively so any model can follow the process.

**Both models benefit from the skill's input contract.** Neither model produced a bad mockup — the
quality floor is high when the inputs are structured. The input contract + design system template
do more for quality than model selection.
