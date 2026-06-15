---
type: reference
status: active
skill: website-design
description: 3-pillar composition contract — how teardown, design, and verify work together
created: 2026-06-12
updated: 2026-06-12
tags: [reference, website-design, composition, website-factory, pillar]
---

# 3-pillar composition contract

The website-factory program's design methodology has three pillars that compose in sequence.
Each pillar is a separate skill with clean boundaries. This document defines the contracts
between them.

## The flow

```
site-capture-engine          website-design           design-emulation-verify
(Pillar 2: SEO)     →     (Pillar 1: Design)    →  (Pillar 3: Verification)
                    →                             →
teardown dossier    →     mockup HTML             →  gap report
design tokens       →     design notes            →  iteration targets
patterns list       →     CSS custom properties   →  pattern presence check
```

## Contract 1: teardown → design

**Producer:** `site-capture-engine`
**Consumer:** `website-design`

The teardown produces a dossier. The design skill reads these sections:

| Dossier section | What the design skill extracts |
|---|---|
| Design tokens (palette, typography) | Reference bar for palette + type decisions |
| Layout patterns + section conventions | Section structure and ordering guidance |
| Content templates | Copy patterns and section shapes |
| "Patterns worth emulating" | Specific patterns to include |
| "Patterns to skip" | Patterns to deliberately NOT include |
| What actually ranks | Which pages/patterns drive traffic (design serves SEO) |
| Conversion/UX system | CTA patterns, form design, capture paths |

**If no teardown exists:** The design skill can run with explicit design direction (brand
guidelines, reference URL, positioning statement) instead. The teardown makes the design
better-informed but is not a hard blocker.

**The design skill NEVER re-runs the teardown.** If teardown data is missing or stale,
ask the operator to run `site-capture-engine` first.

## Contract 2: design → verify

**Producer:** `website-design`
**Consumer:** `design-emulation-verify`

The design skill produces two artifacts the verify skill consumes:

| Artifact | What the verify skill uses it for |
|---|---|
| Mockup HTML (viewable at a URL) | The "build" side of the structural/stylistic/pattern diff |
| Design notes (markdown) | The "composition doc" — tells the verifier which patterns were intentionally emulated vs deliberately different |

**The design notes are critical.** Without them, the verifier treats every difference from the
reference as a gap. With them, the verifier can distinguish intentional brand differentiation
from accidental drift.

**The mockup's `:root` CSS custom properties** are the canonical design system. The verify
skill uses them as the "build's design tokens" for the stylistic diff.

## Contract 3: verify → design (iteration loop)

**Producer:** `design-emulation-verify`
**Consumer:** `website-design` (iteration pass)

The verify skill produces a gap report. The design skill closes gaps:

| Gap report section | Design skill action |
|---|---|
| Structural gaps | Add missing sections, reorder if needed |
| Stylistic gaps (outside policy) | Adjust CSS properties to close |
| Stylistic gaps (within policy) | No action — intentional brand differentiation |
| Pattern gaps | Add missing patterns or explain intentional omission |
| Asset carryover flags | Remove any verbatim reference content (legal boundary) |

**Iteration terminates when:** Zero structural gaps, all stylistic gaps either closed or
explained, all expected patterns present, zero asset carryover.

## Contract 4: design → custom-html-build

**Producer:** `website-design`
**Consumer:** `custom-html-build` ([WF-6])

The build skill extracts the design system from the mockup:

| Mockup artifact | Build artifact |
|---|---|
| `:root` CSS custom properties | Tailwind v4 `@theme` CSS-variable tokens |
| Section HTML structure | Next.js component boundaries |
| Responsive breakpoints | Tailwind responsive utilities |
| Typography scale | `@theme` font-size tokens |
| Button/card/nav patterns | Shared component library |

**The mockup is the single source of truth for visual design.** The build skill does not
re-derive palette, typography, or layout decisions — it implements what the mockup established.

### Canonical token naming convention

Mockup `:root` custom properties MUST use the `--primary-*` / `--accent-*` / `--ink` / `--slate-*`
/ `--paper-*` naming from `design-system-template.md`. This is the canonical vocabulary. Per-client
color names (e.g., `--navy-*`, `--brass-*`, `--slate-*`, `--copper-*`) are NOT canonical — they
leak client identity into what should be a portable design system.

**Mapping to Tailwind v4 `@theme`:** The locked stack (decision #3) is Tailwind CSS v4, which uses
`@theme` blocks in CSS (no `tailwind.config.ts` file). The mapping is:

```css
@theme {
  --color-primary-950: var(--primary-950);
  --color-primary-900: var(--primary-900);
  /* ... through the scale */
  --color-accent-500: var(--accent-500);
  --color-accent-400: var(--accent-400);
  --color-accent-600: var(--accent-600);
  --font-family-display: var(--font-display);
  --font-family-body: var(--font-body);
}
```

Then in templates: `bg-primary-950`, `text-accent-500`, `font-display`, etc.

**Note:** The v2 default-model mockup (`mockup-homepage-v2-default-model.html`) predates this
convention and uses `--slate-*`/`--copper-*` naming. It has NOT been regenerated — the comparison
verdicts remain valid for their purpose (code-read design quality assessment).

## When pillars can be skipped

| Scenario | Skip | Rationale |
|---|---|---|
| No reference site in the niche | Skip verify (or run in structural-only mode) | No reference to diff against |
| Client has strong brand guidelines | Teardown is optional (design direction from guidelines) | The guidelines ARE the design direction |
| Quick mockup for a sales call | Skip verify entirely | The mockup is a concept, not a build |
| Full build from approved mockup | Design already done — go straight to build | Don't re-run design |
