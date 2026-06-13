---
type: skill
name: website-design
version: 1.0
description: >
  Design a custom-coded page (or site) from brand inputs + teardown/reference + content, producing a
  single-file HTML mockup with inline CSS, deliberate typography, and conversion plumbing — ready for
  implementation as Next.js components. The design pillar of the website-factory program. Takes the
  output of `seo-site-teardown` (research) and feeds `design-emulation-verify` (QA). Use whenever a
  Keelworks client or prospect needs a designed page concept before the full Next.js build begins.
  Triggers: "design a homepage for <client>", "mockup <page> for <client>", "create a design concept
  for <client>", "what should <client>'s site look like", "run the design skill on <client>",
  "design a page from the teardown". Produces a self-contained HTML mockup + design-notes doc capturing
  all reasoning for reuse. Composes with seo-site-teardown (upstream) and design-emulation-verify
  (downstream).
status: active
created: 2026-06-12
updated: 2026-06-12
extracted-from: east-coast-furniture-services mockup v1 (Fable subagent, 2026-06-11)
depends-on: []
composes-with: [seo-site-teardown, design-emulation-verify]
tags: [skill, website-design, website-factory, design, mockup, fable, reusable]
---

# Website Design (v1.0)

> **v1.0 (2026-06-12)** — Extracted from the East Coast Furniture Services homepage mockup (the first
> dogfood run). Fable subagent produced the v1 mockup; design reasoning captured in
> `east-coast-furniture-services/mockup-homepage-v1-design-notes.md`. This skill codifies the
> repeatable process so site #2, #3, #4 get faster and more consistent.

## What this skill is

A repeatable process for turning {brand inputs + teardown/reference + content} into a **designed page
concept** — a self-contained HTML mockup with deliberate visual design decisions, not just a functional
scaffold. The output is the design layer between research (what to build) and implementation (building
it in Next.js).

**Why this exists separately from the build.** Design decisions (palette, typography, layout rhythm,
copy voice, imagery strategy) compound across every page of a site. Making them deliberately in a
mockup phase — and capturing the reasoning — means the full build inherits a coherent design system
rather than accumulating ad-hoc choices page by page.

**Core principle — design argues the brand's claim.** Every visual choice (color, type, layout, copy)
should argue the client's positioning. Navy + brass for institutional authority. Serif headlines for
30-year-firm gravitas. A floorplan SVG instead of stock photography. The design is not decoration — it
is the brand's argument made visual.

## When to use

Trigger this skill when:

- A new client or prospect needs a homepage concept before the full Next.js build
- A specific page type (service page, location page, landing page) needs a design concept
- The team wants to test a design direction before committing to full implementation
- A teardown has been completed and the next step is "what should our version look like"

Do NOT use this skill for:

- WordPress page builds (those use the Core 30 SOP's existing templates)
- Minor CSS tweaks to an existing site (just edit the code directly)
- Full Next.js implementation (that's `custom-html-build` / [WF-6])

## Inputs

### Required

1. **Client brief** — business identity, services, positioning, certifications, scale claims,
   service area, target buyer. Source: `prospect-intake` output or `client-fact-research` output.
   At minimum: who they are, what they do, who buys, what makes them credible.

2. **Content inventory** — the actual content for the page: service descriptions, stats/proof points,
   portfolio items, team/founder info, testimonials, CTAs, contact info. Can be extracted from the
   existing site, provided by the client, or drafted from the brief.

3. **Design direction** — at least ONE of:
   - A teardown dossier from `seo-site-teardown` (design tokens, patterns, layout conventions)
   - A reference site URL with specific patterns to emulate
   - Explicit brand guidelines (colors, fonts, logo, imagery style)
   - A positioning statement that implies visual direction ("government-grade + premium contractor")

### Optional

4. **Existing brand assets** — logo files, brand colors, existing photography, style guides.
   When absent, the skill derives a palette and typography from the positioning (see Technique 2).

5. **Page scope** — which page to design. Default: homepage. Can be any page type.

6. **Imagery constraints** — what imagery is available or allowed. Options:
   - Client has photography → use it
   - No photography, AI generation allowed → plan Higgsfield/Midjourney hooks
   - No photography, no AI → use the constraint-as-asset technique (see Technique 1)

7. **Reference patterns** — specific patterns from `design-emulation-verify`'s catalog or from
   the teardown's "patterns worth emulating" section to include in the design.

## Output contract

Two artifacts per design run:

### 1. The mockup — single-file HTML

Location: `04_projects/clients/<_prospects|_active>/<client>/mockup-<page>-v<N>.html`

Requirements:
- **Self-contained** — inline CSS, Google Fonts link only, minimal JS (mobile nav toggle at most).
  No external dependencies, no build step. Opens in any browser.
- **Responsive** — works on desktop AND mobile. Use CSS Grid + Flexbox + clamp() for fluid sizing.
- **Section-complete** — every section the page needs is present with real or realistic content
  (no "Lorem ipsum" except where explicitly flagged as placeholder for client photography).
- **Conversion-plumbed** — sticky CTA, clickable phone, form placeholder, CTAs at every scroll depth.
- **Semantically correct** — proper heading hierarchy, nav/main/footer, alt text placeholders.
- **Design-quality CSS** — not utility-class soup. CSS custom properties for the design system
  (palette, typography, spacing, shadows, radii). Organized by section.

### 2. The design notes — companion markdown

Location: `04_projects/clients/<_prospects|_active>/<client>/mockup-<page>-v<N>-design-notes.md`

Frontmatter: `type: design-notes`, `status: draft`, `client:`, `designer:` (model used).

Sections:
- **The mockup** — section inventory (what's on the page, top to bottom)
- **Design reasoning** — numbered list of every deliberate design decision with rationale.
  This is the reusable knowledge. Capture verbatim.
- **Reusable takeaways** — patterns extracted from this run that generalize to other clients.
  Feed these back into the skill's `references/` over time.
- **Open follow-ups** — what needs operator review, what changes on signing, what the next
  iteration should address.

## The design process — step by step

### Step 1 — Absorb the inputs

Read the client brief, content inventory, and design direction. Extract:

- **The buyer** — who is the target buyer? What do they care about? What are they afraid of?
- **The credibility proof points** — the 3-4 hardest facts (years, revenue, certifications,
  brand partnerships) that establish trust.
- **The positioning claim** — what does this business want the buyer to believe about them?
- **The current gaps** — what does the existing site get wrong? (Misspellings, broken images,
  underselling, wrong channel, etc.)

### Step 2 — Derive the design system

Before writing any HTML, lock these decisions:

**Palette (3-5 colors):**
- Use Technique 2 (palette-as-positioning): pick colors that *argue* the brand's claim.
- Derive from the positioning, not from the client's current palette (which is often weak).
- Dark primary for authority, warm accent for premium/action, neutral for body, paper for backgrounds.
- The accent color is for CTAs and proof-point highlights only — sparingly used reads premium.

**Typography (2 fonts max):**
- Display font for headlines (serif = gravitas/authority; geometric sans = modern/clean).
- Body font for text and UI (always a clean sans-serif: Inter, Manrope, DM Sans, etc.).
- Lock sizes with clamp() for fluid scaling. Eyebrow labels: uppercase, letter-spaced, small.

**Spacing + rhythm:**
- Section padding: 80-100px vertical. Consistent rhythm = designed; irregular = template.
- Dark/light section alternation for visual pacing (dark primary → white → paper → dark primary).
- Max content width: 1100-1200px. Generous side padding (24-32px).

**Imagery strategy:**
- If no photography: use Technique 1 (constraint-as-asset) — domain-native SVG artifacts.
- If AI generation planned: note Higgsfield hooks with subject/style/aspect requirements.
- If client has photos: plan crops, aspect ratios, overlay treatments.

**Shadow + radius:**
- Consistent card radius (12-16px). Consistent shadow scale (sm/md/lg).
- Cards should feel lifted, not flat. But not skeuomorphic — modern elevation.

### Step 3 — Structure the page

Map the page sections top-to-bottom. Standard homepage structure (adapt per client):

1. **Sticky nav** — logo + links + phone + primary CTA
2. **Hero** — badge/eyebrow + headline (speaks to buyer's fear/desire) + sub-headline +
   dual CTAs + proof line (condensed stats) + hero visual (photography/SVG/gradient)
3. **Stats spine** — full-width dark bar with 4-5 proof points (the numbers that matter)
4. **Services grid** — 3-6 service cards with icons + brief descriptions + learn-more links
5. **Portfolio/projects** — 3-4 project cards with images + operational detail captions
6. **Credibility section** — brand-partner wall, certification badges, key credential callout (e.g., MBE/GSA)
7. **Verticals/industries** — who they serve (with icons or cards)
8. **Service area** — geographic coverage (map or city grid)
9. **Quote/contact form** — pre-modeled fields that coach qualified inquiries
10. **Footer** — NAP, links, social, legal

Not every client needs all sections. The brief determines which sections earn their spot.

### Step 4 — Write the copy

Copy is part of the design, not separate from it. Apply Technique 4:

- **Headlines speak to the buyer's risk, not the feature list.** Identify the #1 fear
  (schedule slip, budget overrun, quality gap, unreliable contractor) and write to it.
- **Proof points at escalating depth.** The hardest credibility facts appear 3x: hero proof
  line (condensed) → stats bar (full numbers) → dedicated section (full context + seal/badge).
- **Portfolio captions carry operational detail** — not "Office Project" but "47 workstations
  installed overnight, zero business-day disruption." Make placeholders feel lived-in.
- **CTAs are specific and action-oriented** — "Request a Quote" not "Contact Us";
  "Call (555) 123-4567" not "Phone".

### Step 5 — Build the mockup

Write the single-file HTML with inline CSS. Follow the design system from Step 2.

**Build order within the file:**
1. CSS custom properties (`:root` block with all tokens)
2. Base reset + body styles + utility classes (`.wrap`, `.eyebrow`, `.btn-*`)
3. Section-by-section CSS (nav → hero → stats → services → ... → footer)
4. Responsive breakpoints (`@media` at the end)
5. HTML body: semantic structure, section by section
6. Minimal JS (mobile nav toggle only, at the bottom)

**Quality checks during build:**
- Every section has an eyebrow label (consistent editorial hierarchy)
- Every dark section has proper light-text colors (check contrast)
- Every CTA uses the accent color (visual consistency)
- The page has visual rhythm (dark-light-dark alternation)
- Mobile nav collapses properly
- No horizontal scroll at any viewport width

### Step 6 — Write the design notes

Capture every design decision and its rationale in the companion markdown. This is the knowledge
that makes the next mockup faster. Be specific — "deep primary + warm accent for institutional authority" not
"picked some colors."

### Step 7 — Verify with design-emulation-verify (if reference exists)

If the design was based on a teardown/reference, run `design-emulation-verify` to diff the mockup
against the reference. Close structural and pattern gaps; stylistic differences that serve the
client's brand are intentional, not gaps.

**If design-emulation-verify is not yet implemented** (current state: spec only), do a manual
3-axis check:
- **Structural:** Does the mockup have the same section types and order as the reference?
- **Stylistic:** Are the typography scale, spacing rhythm, and color usage in the same ballpark?
- **Pattern:** Are the key patterns from the reference present (FAQ accordion, pricing transparency,
  founder presence, etc.)?

## Reusable design techniques

These techniques generalize across clients. Extracted from real mockup runs.

### Technique 1 — Constraint-as-asset

When stock imagery is unavailable or risky, build **domain-native SVG artifacts** instead:
- A floorplan for a furniture installer
- A wiring diagram for an electrician
- A route map for a mover
- A building cross-section for an HVAC company

These beat generic placeholders AND signal domain fluency to the buyer. The constraint becomes
a credibility asset.

**Implementation:** Inline SVG in the HTML, styled with the design system's colors. Use
`repeating-linear-gradient` for textures (blueprint grid, panel texture). Floating stat chips
anchor proof points on the visual.

### Technique 2 — Palette-as-positioning

Pick colors that **argue the brand's claim**, not that "look nice":
- Navy (#0a1521) = institutional/government-grade → for a GSA-certified contractor
- Brass (#c79a4b) = premium, not decorative → for a high-end installer
- Forest green = reliability/growth → for a landscaping company
- Deep red + silver = urgency + precision → for an emergency electrician

Explicitly invert the client's weak current palette. A washed-out blue-grey becomes a commanding
navy. A generic red-and-black becomes a sophisticated palette with intention.

### Technique 3 — Proof-point spine

Repeat the 3-4 hardest credibility facts at **escalating depth** rather than once:
1. **Hero proof line** — condensed (e.g., "[revenue] · [years] · [certification]")
2. **Full stats bar** — full-width dark section with big numbers + labels
3. **Dedicated section** — e.g., certification "seal card" with full explanation + transactional framing

Repetition is intentional, not redundant. Each repetition adds context the previous one couldn't.

### Technique 4 — Copy to the buyer's risk

Identify the buyer's #1 fear and write headlines to it:
- **Office furniture buyer** → "The schedule holds" (fear: project delays)
- **Homeowner hiring an electrician** → "Fixed right the first time" (fear: callbacks)
- **Facilities manager** → "Zero business-day disruption" (fear: operational impact)

This is more effective than feature-listing ("We install furniture" → nobody cares).

### Technique 5 — Dark/light section rhythm

Alternate section backgrounds for visual pacing:
- Hero (dark navy) → Stats (dark) → Services (light/white) → Portfolio (paper/warm) →
  Credibility (dark) → Verticals (light) → Service Area (paper) → Form (dark) → Footer (darkest)

The alternation creates a reading rhythm. Three light sections in a row feels flat; three dark
sections in a row feels oppressive. Alternate.

### Technique 6 — Conversion plumbing everywhere

Don't concentrate CTAs in one spot. Distribute:
- Sticky nav CTA (always visible)
- Hero dual CTAs (primary + secondary/ghost)
- End of each major section (contextual CTA)
- Dedicated form section (pre-modeled fields)
- Footer phone + form link
- Mobile: sticky bottom bar with phone + quote

**Form fields should coach qualified inquiries** — not just "Name / Email / Message" but fields
that pre-model the kind of information the business needs (project type, timeline, facility size).

## Model selection — Fable vs default

**Evidence from the first dogfood (East Coast Furniture, 2026-06-11):**

Fable (Anthropic's design-strong model) produced the v1 mockup. Findings:

- **Fable strengths:** Deliberate palette reasoning (navy + brass as trust argument), sophisticated
  typography pairing (Fraunces serif + Manrope sans), the constraint-as-asset SVG floorplan move,
  dark/light rhythm, proof-point escalation structure, editorial hierarchy (eyebrow labels).
- **Fable approach:** Used as a subagent with `model: "fable"` parameter. Single prompt with full
  brief + audit + design constraints. Produced ~1000-line single-file HTML on first pass.

**Recommendation:** Use Fable for the initial design concept (Step 5) when available. The default
model can execute the same process using the techniques documented here, but Fable's design
intuitions (particularly palette-as-positioning and constraint-as-asset) are stronger out of the box.

**Comparison completed (2026-06-12, code-read-only — no render evidence yet).** Default model
(Claude Opus 4.6) produced v2 on the same ECFS brief. Full analysis in
`references/fable-vs-default-comparison.md`. Summary: Fable wins on palette reasoning, typography,
hero visual, and page architecture. Tie on copy quality and conversion plumbing. Verdicts are
provisional pending browser render at 4 viewports. **Recommendation: use Fable for initial
concepts when available; the default model is fully capable using the documented techniques.**

## Higgsfield imagery hook

When the design calls for AI-generated imagery (photography-style images of people, locations,
or scenarios):

1. **During mockup:** Use CSS gradient + texture placeholders with descriptive comments
   (`<!-- HIGGSFIELD: Owner portrait, professional headshot, navy suit, office setting -->`).
2. **After approval:** Generate via Higgsfield CLI/MCP with the Soul Character (if trained)
   for consistent likeness. Aspect ratios and crop specs noted in the mockup comments.
3. **Integration:** Replace placeholder with the generated image. Run design-emulation-verify
   to confirm the image treatment matches the reference bar.

This is a hook, not a full integration. The imagery pipeline has its own skill
(`imagery-automation-pivot` when shipped); this skill provides the spec of what's needed.

## Composition with other skills

### Upstream: seo-site-teardown

The teardown produces the design inputs this skill consumes:
- Design tokens (palette, typography from `design-tokens.md`)
- Layout patterns and section conventions
- Content templates and language patterns
- What actually ranks (so design serves SEO, not fights it)

**Contract:** This skill reads the teardown dossier's design-fingerprint sections. It does NOT
re-run the teardown. If no teardown exists for the client's niche, either run one first or
provide an explicit design direction (Input #3).

### Downstream: design-emulation-verify

The verification skill diffs the mockup against the reference:
- Structural gaps (sections missing or out of order)
- Stylistic gaps (typography, color, spacing differences)
- Pattern gaps (expected patterns absent)

**Contract:** This skill produces a mockup that design-emulation-verify can consume. The mockup
must be viewable at a URL (localhost, preview deploy, or opened as a local file). The design-notes
document serves as the "composition doc" that tells the verifier what was intentional.

### Downstream: custom-html-build ([WF-6])

The full Next.js build consumes the design system (palette, typography, component patterns) from
this skill's mockup. The mockup's CSS custom properties map directly to Tailwind theme tokens.
The section structure maps to Next.js components.

**Contract:** The mockup's `:root` CSS custom properties (canonical `--primary-*`/`--accent-*`
naming) are the design system. The build skill maps them to Tailwind v4 `@theme` CSS-variable
tokens. See `references/pillar-composition-contract.md` Contract 4 for the mapping.

## Quality gates

The mockup must:

- Open in a browser and render correctly at 1440px, 1024px, 768px, and 375px widths
- Have no horizontal scroll at any viewport
- Pass a basic contrast check (dark text on light, light text on dark — no grey-on-grey)
- Have every section populated with real or realistic content (no Lorem ipsum)
- Include at least 3 CTAs at different scroll depths
- Have a sticky nav that works
- Use semantic HTML (h1 once, h2 per section, proper nav/main/footer)
- Use canonical token naming (`--primary-*`, `--accent-*`, `--ink`, `--slate-*`, `--paper-*`)
  per `references/design-system-template.md` — no per-client color names in `:root`

## Trigger phrases

- "Design a homepage for [client]"
- "Mockup [page] for [client]"
- "What should [client]'s site look like"
- "Create a design concept"
- "Run the design skill"
- "Turn the teardown into a design"
- "Design a page from the brief"

## Related

- [[seo-site-teardown]] — upstream (research front-end)
- [[design-emulation-verify]] — downstream (verification QA)
- [[custom-html-build]] — downstream (full Next.js implementation)
- [[strategy-custom-coded-nextjs-via-ai-with-competitor-inspiration]] — the 3-pillar strategy
- [[tactic-emulate-competitor-design-patterns-with-ai]] — the methodology this skill operationalizes
- [[decision-2026-06-11-website-factory-program-locked-decisions]] — locked stack + hosting decisions

## Decision archaeology

- 2026-06-12 [created] — Skill extracted from the East Coast Furniture Services homepage mockup
  (Fable subagent, 2026-06-11). Handoff: [[handoff-2026-06-11-website-design-skill-and-mockup]].
  Techniques 1-6 captured from the live run's design reasoning. Fable-vs-default comparison
  completed same session — code-read-only verdicts, render evidence pending
  (see `references/fable-vs-default-comparison.md`). Second-config proof pending [T2-DAD1].
