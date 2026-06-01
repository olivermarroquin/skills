---
name: competitor-deep-research
description: Deep competitive intelligence research on a client's direct competitors, producing structured per-competitor briefs and a cross-competitor synthesis that feeds page-build and SEO strategy. Use this skill whenever the user asks to research competitors, do a "competitive analysis," "competitive deep dive," "competitor landscape," "competitive intelligence," or "competitor audit" for a specific client — and any time the user names 2 or more competitors and wants them profiled side-by-side. Also use when the user mentions wanting to feed competitor findings into a Core 30 / page-build / SEO foundation strategy, or when they ask "who else is ranking for [keyword]" and wants more than a list. The skill writes per-competitor markdown briefs and a synthesis file into the client's vault folder under admin-extracts/competitor-research/.
---

# Competitor Deep Research

A reusable workflow for doing competitive intelligence on a client's direct competitors. Produces per-competitor briefs and a cross-competitor synthesis that grounds page-build and SEO strategy in real data, not assumptions.

This skill was distilled from the 2026-05-23 EV Electric Services Fairfax County competitive research session. The full case study lives at `~/workspace/second-brain/04_projects/clients/_active/ev-electric-services/admin-extracts/competitor-research/` — refer to it when something in this skill is unclear; the synthesis file there shows what a finished output looks like.

---

## When to use

Trigger this skill when the user wants to understand a client's competitive landscape in enough depth to make page-build and SEO decisions. Typical triggers:

- "Research competitors for [client]"
- "Do a competitive deep dive on [client's competitors]"
- "Who's ranking for [keyword] and what are they doing?"
- "I need a competitor analysis to feed the Core 30 strategy"
- "Profile these 3 competitors and tell me where the gaps are"

Do **not** use this skill for:

- Generic "is X a competitor" lookups (use a web search instead)
- One-competitor profiles (the synthesis value comes from comparison; if there's only one, just write a single brief without invoking the full skill)
- Pricing-only or product-feature-only comparisons (this skill is shaped for SEO + content + positioning; not for product teardowns)

---

## Inputs you need from the operator

Ask for these before starting. Don't guess — wrong inputs produce wrong briefs.

1. **Client identity.** Business name, domain, owner name if relevant.
2. **Service area.** Primary geography, secondary geographies, explicit avoid list if there is one (some clients reject certain regions for revenue or strategic reasons).
3. **Top competitors (3–5).** Either the operator names them, or there's an existing ranking source to pull from (BrightLocal scan, Ahrefs export, a prior audit). If the operator only knows 1–2, supplement by running a Google search for the target head-keyword and picking the rest from the top organic results.
4. **Existing data the operator can hand over.** A BrightLocal scan, GBP audit, Ahrefs report, the client's own README — anything that grounds the research in numbers you don't have to re-derive.
5. **Output folder.** Default to `<client-vault-path>/admin-extracts/competitor-research/` if the client lives in the Knowledge OS vault. The operator can override.
6. **Time budget.** Useful to know up-front. Typical budget: 90 min for two primaries + 30 min each for secondaries + 30 min for synthesis = ~3 hours.

If any input is missing, ask the operator before researching. Bad inputs waste research budget.

---

## High-level workflow

The skill runs in four phases. Don't skip phases — each one feeds the next.

1. **Identify the competitor list** — confirm the primaries (operator-named or ranking-source-derived) and add 2–3 secondaries from the live Google search.
2. **Research each competitor** — for each one, follow the per-competitor research sequence below and produce a brief at `<output-folder>/<competitor-slug>.md`.
3. **Write the cross-competitor synthesis** — read all the briefs, extract patterns, and write the synthesis at `<output-folder>/synthesis-YYYY-MM-DD.md`.
4. **Maintain folder hygiene** — write a `_README.md` for the new folder if one doesn't exist, and update the parent folder's `_README.md` to list the new child (per the vault stewardship principle that subfolder creation and README maintenance are one atomic action).

Mark each phase as a task in the operator's task list so they can see progress.

---

## Phase 1: Identify the competitor list

Two sources of competitor names: the operator's prior data and a fresh Google search.

**Prior-data source (preferred when available):** BrightLocal Local Search Grid reports, Ahrefs exports, prior audit notes. Pull the top-ranking competitors for the keywords the client cares about. If a BrightLocal report exists, the operator has done some of this work already — use it.

**Live Google search:** Run `WebSearch` for the target head keyword (e.g., "electrician Fairfax VA"). Pick from the top 5 organic results, excluding directories (Yelp, BBB, Angi, Checkbook, Houzz, Thumbtack). The cross-source confirmation matters — competitors that appear in both BrightLocal AND organic Google are more strategically important than competitors that appear in only one.

**Primary vs secondary classification:**

- **Primary (full deep-dive brief):** The 2 highest-ranking competitors for the client's most important keyword, OR the operator's named-must-include competitors. Cap at 2.
- **Secondary (lighter-touch brief):** 2–3 additional competitors that round out the picture — typically the next-ranking organic results plus any operator-flagged-but-not-must-have names. Cap at 3.

Total: 4–5 competitors. More than 5 dilutes the synthesis; fewer than 3 doesn't give enough cross-competitor patterns to surface.

---

## Phase 2: Per-competitor research sequence

For each competitor, run the same sequence. Mechanizing the sequence is what makes the briefs comparable.

### Step 1: Fetch the homepage

Use the workspace `mcp__workspace__web_fetch` tool to pull the competitor's homepage. Read the returned markdown plus all meta tags. Capture:

- Business name, domain, tagline, phone, address, displayed licenses
- Years in business (if shown anywhere)
- Service area claimed
- Top services listed in the nav
- Whether reviews are linked or embedded

### Step 2: Fetch one service page and one location page

Pick the service page that matches the client's headline service (if the client leads with panel upgrades, fetch the competitor's panel-upgrade page). Pick the location page that matches the client's primary geography (if the client is in Fairfax, fetch the competitor's Fairfax page if they have one).

These two pages tell you how deep the competitor's content actually goes. Read for: word count (estimate), neighborhood mentions, permit references, transparent pricing, FAQs embedded inline, schema markup in the meta block, internal-linking density.

### Step 3: Fingerprint the tech stack

This is one of the most important findings in every brief. Use these signals:

- **HTTP headers via `curl -sI <domain>`** — `server:` reveals Netlify, WP Engine, Cloudflare, etc. `x-powered-by:` sometimes reveals PHP versions or framework. `cache-status:` reveals CDN behavior.
- **URL patterns** — `/wp-content/` confirms WordPress. `.html` extensions in sitemap suggest static site generator. `/us/en-us/_assets/` patterns suggest enterprise CMS (often .NET or Java-based).
- **Meta tags** — `meta-generator:` outright names the tool sometimes (e.g., `NitroPack`, `WordPress`, `Hugo`). Old-school `meta-keywords` and `meta-ICBM` tags hint at the era and origin of the site's SEO setup.
- **Image format** — `.webp` and `.avif` indicate a modern pipeline; `.png` and `.jpg` indicate it isn't.
- **Schema markup** — search the fetched HTML for `application/ld+json`. If present, note what type (LocalBusiness, AggregateRating, Service, FAQPage). If absent, that's a gap.
- **Agency credits** — many small-to-mid contractors outsource websites. Look for footer credits like "Website by [agency]" — common ones in home services are RYNO Strategic Solutions and ProIQ. The agency name tells you who's actually executing their SEO.

The reference file `references/patterns-to-watch.md` has a fuller fingerprint table — read it for any competitor whose stack isn't immediately obvious.

### Step 4: Count indexed pages via sitemap

Bash-run `curl -s <domain>/sitemap.xml | grep -c "<loc>"` to get a total URL count. Then `grep -oP '(?<=<loc>)[^<]+' | awk -F'/' '{print $4}' | sort | uniq -c | sort -rn | head -20` to see the URL-path-tier breakdown. This is how you quantify the content moat — AJ Long Electric had 274 pages indexed (62 VA cities + 67 service pages + 44 blog posts) while Mr. Electric of Fairfax had ~30 Fairfax-specific pages.

If the sitemap is missing or blocked, fall back to the visible navigation. Less precise, but acceptable.

### Step 5: Cross-reference any prior data

If the operator handed over a BrightLocal scan, Ahrefs report, or prior audit, pull the relevant numbers for this competitor — review count, rating, link count, authority score, average map rank for the tracked keywords. These numbers ground the brief's claims.

### Step 6: Write the brief

Use the template at `references/per-competitor-brief-template.md`. The template has 9 sections in a fixed order — keeping the order consistent across briefs is what makes the synthesis writable later.

Each brief should:

- Open with the basic identity facts (name, domain, address, phone, license, years in business)
- Cover tech stack with concrete fingerprints, not vague impressions
- Estimate page count from sitemap, not guess from nav
- Quote specific page snippets when calling out generic-vs-localized content
- End with a "what's NOT working" section that lists exploitable gaps — flaws the client can credibly out-execute

Briefs typically run 1,500–3,000 words for primaries and 800–1,500 words for secondaries. Don't pad. Each bullet should earn its place.

### Step 7: Handle SPA-rendered sites

If `web_fetch` returns empty content, the site is likely a client-rendered single-page app (JavaScript renders the content after the page loads). Don't keep retrying — escalate to a browser-rendered tool. In Cowork, that's `mcp__Claude_in_Chrome__navigate` + `mcp__Claude_in_Chrome__get_page_text`. If browser tools aren't available in the current session, flag the competitor as "blocked for re-audit" in the synthesis's "blocked questions" section and move on. Don't fake the analysis.

---

## Phase 3: Cross-competitor synthesis

After all briefs are written, write the synthesis at `<output-folder>/synthesis-YYYY-MM-DD.md`. Use the template at `references/synthesis-template.md`.

The synthesis is where the strategic value lands. Per-competitor briefs are inputs; the synthesis is the deliverable that operators will refer to when planning the client's Core 30 build or SEO foundation. Don't shortcut it.

Required sections:

1. **Quick-reference comparison table** — one row per competitor, with reviews, rating, links, authority, tech stack, page count, and top-keyword rank. The table is what operators screenshot and paste into client decks. Make it scannable.

2. **The headline finding** — the single most important pattern in the data. In the EV Electric case it was "content depth beats domain authority in this niche" (Mr. Electric's 53/100 authority losing to AJ Long's 11/100). Every market will have its own headline finding; surface it explicitly.

3. **Common patterns** — what ALL the competitors do. These are table stakes — the client can't differentiate by doing them, only lose by skipping them.

4. **Differentiation opportunities** — what NOBODY does well. These are the gaps the client can exploit. Make each one concretely actionable.

5. **Keyword targets ranked by competitiveness** — four tiers (hard, moderate, easy, defensive). Each tier names specific keywords and explains why they're at that difficulty level.

6. **Tech stack patterns: the "winning stack"** — what the data shows about which infrastructure choices correlate with ranking outcomes.

7. **Top 10 recommendations for the client's page build** — ordered by impact-to-effort ratio. Each recommendation should map to a specific finding from the briefs.

8. **Top 3 risks if the client doesn't act** — what happens if they delay.

9. **Blocked questions / follow-up research** — anything that couldn't be confirmed in this round. Honesty about gaps matters more than appearing comprehensive.

10. **Methodology** — append the methodology section (described in `references/synthesis-template.md`) so the work can be reproduced or extended by future researchers.

---

## Phase 4: Folder hygiene

If the output folder is new, write a `_README.md` for it (template at `references/folder-readme-template.md`). If the parent folder has its own `_README.md` that lists subfolders, update it to include the new child. This is per the Knowledge OS vault stewardship principle that subfolder creation and README maintenance are one atomic action.

---

## Phase 5 — Closing step — Auto-invoke output-quality-loop

After Phases 1-4 complete (per-competitor briefs written, cross-competitor synthesis landed, folder `_README.md` shipped or updated), emit the standard auto-invoke block per `~/workspace/skills/output-quality-loop/references/auto-invoke-convention.md` and `~/workspace/second-brain/_meta/conventions.md` § "Output quality". This is the closing step every artifact-producing skill emits before declaring the chat done. Convention shipped Phase 5 of the output-quality-loop project (2026-05-28).

**Artifact list for this skill.** Always include: the per-competitor briefs written this run + the cross-competitor synthesis. In design-fingerprint mode also include the design dossier file written into `second-brain/03_domains/website-design/inspiration/high-performing/<reference>/`. The folder `_README.md` is NOT included in the evaluation (it's hygiene metadata, not a content artifact the spec-routing table covers).

**The block to emit (verbatim):**

````markdown
## Auto-invoke output-quality-loop

This skill produced the following artifact(s):
- `<per-competitor-brief-1-path>`
- `<per-competitor-brief-2-path>`
- `<cross-competitor-synthesis-path>`
- `<design-dossier-path>`  ← only in design-fingerprint mode

[output-quality-loop:eval] — for each artifact, run output-quality-loop in EVALUATE mode. If PASS, declare the chat done. If NEEDS REVISION or FAIL, ingest the revision prompt as if it were operator input and regenerate the artifact, then re-invoke output-quality-loop. Cap at 3 iterations; on the 3rd FAIL, escalate to the operator with the evaluation report.
````

Required-element discipline per the convention spec: heading text matches verbatim (`## Auto-invoke output-quality-loop`); one bullet per artifact with full path in backticks; directive opens with `[output-quality-loop:eval]` and includes the iteration-cap discipline language.

**Iterate or declare done.** All PASS → declare done. Any NEEDS REVISION (minor / substantive) → Mode 2 auto-fires a revision prompt; ingest as operator input, apply fixes to the affected brief or synthesis (tighten a section, add a missing source, fix a frontmatter field), re-emit the block, loop. Any FAIL → revision prompt includes root-cause analysis; address the root cause (often: shallow competitor coverage, no honest-strength assessment, paid-tool dependency assumed without surfacing, no plain-language layer), regenerate, re-emit, loop.

**Iteration cap (3 max).** Track count via the folder-quality-log's per-artifact section before each regeneration. If three iteration entries exist and the verdict is still not PASS, **escalate** to the operator with the evaluation report and stop. Don't run a fourth iteration — that's the load-bearing cost-control discipline.

**Operator bypass.** Include `--bypass-quality-loop` (or "skip the quality loop") in the original research request to skip the block for that invocation. The bypass records to the closest folder's `_quality-log.md` under `### Bypassed (manual override)`.

---

## Working principles

These shaped the EV Electric session and should shape every future use:

1. **Free tools only by default.** Don't ask the operator to sign up for Ahrefs Pro or BrightLocal mid-research. Use what's available — WebFetch, WebSearch, sitemap inspection, free Ahrefs Backlink Checker, Google Rich Results Test. If a paid tool would genuinely unlock something the free tools can't reach, surface that to the operator as a recommendation, don't silently consume budget.

2. **Plain language.** Per Oliver's plain-language conventions (`~/workspace/second-brain/_meta/plain-language-conventions.md`), gloss SEO jargon inline. "Schema markup (a tagging format that tells Google what's on the page so it can show rich results like review stars)" is better than just "schema markup" the first time it appears in a brief. Don't assume the operator's client knows the jargon.

3. **Be honest about competitor strength.** If a competitor is genuinely strong, say so. Don't sugarcoat the picture to make the client feel better. The whole point of competitive research is to give the client a realistic picture so they can make good decisions.

4. **Quote specifics; avoid hand-waving.** "AJ Long's panel-upgrade page is around 2,800 words with a 5-step process, 6 FAQs, and 4 named case studies" beats "AJ Long has detailed service pages." Specifics let the reader verify; hand-waving doesn't.

5. **Source-attribute every claim.** When a brief says "1,200 reviews," it should be clear whether that came from the BrightLocal scan, the competitor's homepage, or a Google search. Operators need to know which signals to trust if numbers conflict later.

6. **Capture exploitable gaps, not all gaps.** A flaw a competitor has that the client can't credibly out-execute isn't worth listing. Stay focused on what the client can actually do with the finding.

7. **Don't run formal evals every time.** This skill came out of a single proven session; the methodology is the eval. If a future invocation finds a market where the methodology breaks down, document it in the relevant brief and propose a methodology revision via the methodology section of the synthesis.

---

## Reference files

When you need them, read these:

- `references/per-competitor-brief-template.md` — full template with all 9 sections, frontmatter, and example phrasing
- `references/synthesis-template.md` — full synthesis template with all 10 sections plus the methodology block
- `references/patterns-to-watch.md` — tech stack fingerprints, content depth heuristics, common winning + losing patterns observed in home-services niches
- `references/folder-readme-template.md` — `_README.md` template for the output folder

Scripts:

- `scripts/count_words.py` — pipe a fetched page through this to get hard word counts instead of estimates. Optional; brief-readability doesn't require it but the synthesis's quantitative claims are stronger with it.

---

## Worked example

The EV Electric Services session is the canonical worked example. Files to refer to:

- `~/workspace/second-brain/04_projects/clients/_active/ev-electric-services/admin-extracts/competitor-research/aj-long-electric.md` — primary deep-dive brief
- `~/workspace/second-brain/04_projects/clients/_active/ev-electric-services/admin-extracts/competitor-research/mr-electric-fairfax.md` — primary deep-dive brief
- `~/workspace/second-brain/04_projects/clients/_active/ev-electric-services/admin-extracts/competitor-research/absolute-electric.md` — secondary lighter-touch brief
- `~/workspace/second-brain/04_projects/clients/_active/ev-electric-services/admin-extracts/competitor-research/kolb-electric.md` — secondary lighter-touch brief
- `~/workspace/second-brain/04_projects/clients/_active/ev-electric-services/admin-extracts/competitor-research/synthesis-2026-05-23.md` — synthesis with methodology section

When in doubt about format, voice, depth, or section structure, read the worked example. It's the source of truth.

---

## Refinement — design-fingerprint mode (added 2026-05-23)

**Status:** spec only. Implementation TBD as a follow-up project.

### Why this mode exists

The base `competitor-deep-research` skill is shaped for SEO + content + positioning analysis. The output is a per-competitor brief and a cross-competitor synthesis useful for page-build strategy.

After the 2026-05-23 pivot to custom-coded Next.js sites built by emulating proven high-performing reference sites (see [[decision-2026-05-23-pivot-to-custom-coded-websites-via-nextjs]]), the skill also needs to produce a **design dossier** suitable for filing in `second-brain/03_domains/website-design/inspiration/high-performing/`. The base skill captures most of what a design dossier needs but is missing four things:

1. **Color palette extraction** — hex codes for primary, secondary, accent, neutral, text colors
2. **Typography extraction** — font family names + weights + size scale + line-height patterns
3. **Layout pattern detection** — hero composition, section conventions, FAQ shape, CTA style, footer pattern
4. **Performance scores** — Core Web Vitals (LCP, INP, CLS) from PageSpeed Insights API; not just lab data but real-user data when available

The refinement adds a `--mode design-fingerprint` flag (or equivalent invocation pattern in skill-speak) that produces a dossier in the format spec'd at `second-brain/03_domains/website-design/inspiration/high-performing/_README.md`.

### Trigger phrases for design-fingerprint mode

In addition to the base skill's triggers, also use this mode when:

- "Fingerprint the design of [site]"
- "Add [site] to the design catalog"
- "Build a design dossier for [site]"
- "Run a design-emulation prep on [site]"
- "Capture the visual fingerprint of [site]"
- Any time a site is being prepared for emulation by Claude Code per the [[tactic-emulate-competitor-design-patterns-with-ai|emulate competitor patterns tactic]]

### Inputs (in addition to the base skill's inputs)

- **Reference site URL** — required. Single URL, not a list.
- **Output mode** — `design-dossier` (default for this mode), or `dossier-plus-brief` (also writes the standard competitor brief)
- **Target catalog folder** — defaults to `second-brain/03_domains/website-design/inspiration/high-performing/`
- **Performance data source** — `lab` (Lighthouse), `field` (real-user CrUX), or `both` (preferred)

### Output contract — the design dossier format

Spec'd at `second-brain/03_domains/website-design/inspiration/high-performing/_README.md`. Reproduced here for skill-spec purposes:

```
dossier-<site-slug>.md

Frontmatter:
- type: design-dossier
- status: verified | provisional
- created, updated, domain, niche, geography
- performance-verified-date
- tags

Content sections (in order):
1. Business identity
2. Why it performs (rankings + CWV + content + conversion proxies)
3. Tools / code / framework fingerprint  ← base skill already covers this
4. Visual design fingerprint            ← NEW; the refinement's main addition
5. Patterns worth emulating
6. Patterns to skip
7. How we emulate without copying assets
8. Verification notes
```

### New procedure for the visual design fingerprint section

Beyond the base skill's tech-stack fingerprinting:

#### A. Color palette extraction

Procedure:

1. Pull all CSS files referenced from the page via `web_fetch`
2. Extract all hex codes via regex (`#[0-9a-fA-F]{3,6}`)
3. Also extract rgb()/rgba() values and convert to hex
4. Count frequency of each color; the top 5-7 most-used colors are usually the palette
5. Cross-check against any explicit CSS custom properties (`--color-primary`, `--brand-blue`, etc.)
6. Group by role: primary brand, secondary, accent, neutral background, neutral text
7. Write the palette as a code block with each role + hex value

Edge case: if the site uses Tailwind, palette colors often appear inline in the HTML as `bg-blue-500` etc. — convert to hex equivalents using a Tailwind palette reference.

#### B. Typography extraction

Procedure:

1. Pull all `@font-face` declarations from CSS
2. Pull all `font-family` declarations and count frequency
3. Identify the primary font (most common in body), secondary (often headings), and any display font
4. For each font, extract: weights used (300, 400, 500, 600, 700, etc.), sizes used (px, rem, em values; build a size scale), line-heights, letter-spacing
5. Check whether fonts are loaded via Google Fonts, self-hosted, or a service like Typekit
6. Write typography as: font name + weight + size scale + line-height pattern per role (body, headings, display, accent)

#### C. Layout pattern detection

Procedure:

1. Parse the rendered DOM (via Claude in Chrome if available, or via web_fetch's returned HTML if JS-light)
2. Identify the major sections of the home page in order: hero, services, about, testimonials, FAQ, footer, etc.
3. For each section, capture: HTML structure (which tags / classes), visual position (above-fold, below-fold), content density (text-heavy, image-heavy, mixed), CTA presence and style
4. Compare against an internal taxonomy of known section patterns (see `references/patterns-to-watch.md` — extend this file when new section patterns emerge)
5. Write layout patterns as a list of section conventions with examples

#### D. Performance scores

Procedure:

1. Call Google PageSpeed Insights API for both mobile and desktop variants of the site
2. Capture both lab data (Lighthouse synthetic) AND field data (real-user CrUX) where available
3. Capture all three Core Web Vitals: LCP, INP, CLS
4. Capture additional metrics: FCP, Speed Index, Total Blocking Time
5. Note whether each metric is "Good," "Needs Improvement," or "Poor" per Google's thresholds
6. Write performance scores as a table with each metric, lab + field values, and the Good/NI/Poor classification

#### E. Image format inventory

Procedure:

1. Extract all `<img>` `src` and `<source>` `srcset` attributes from the page
2. Count format distribution: AVIF, WebP, PNG, JPG, SVG, GIF
3. Note whether the site uses responsive images (`srcset`, `sizes`, `<picture>`)
4. Note whether Next.js Image component is in use (often visible from `_next/image?url=` patterns in URLs)
5. Modern format prevalence (AVIF + WebP) is a Pillar 2 SEO signal (image weight correlates with LCP)
6. Write image format inventory as a short table

### When to use base skill vs design-fingerprint mode

| User intent | Mode |
|---|---|
| Understand competitor landscape for SEO strategy | Base skill |
| Profile a competitor for client positioning | Base skill |
| Lift design patterns from a high-performing reference | Design-fingerprint mode |
| Build a catalog entry in `inspiration/high-performing/` | Design-fingerprint mode |
| Cross-competitor synthesis for Core 30 build | Base skill |
| Cross-reference synthesis for design catalog | Design-fingerprint mode |

If both are needed for the same site, run base skill first, then design-fingerprint mode. They produce sibling files (one in `admin-extracts/competitor-research/`, one in `website-design/inspiration/high-performing/`).

### Future implementation notes

When this refinement gets implemented:

- The color palette + typography extraction steps lend themselves to scripts (`scripts/extract_palette.py`, `scripts/extract_typography.py`) that take a URL and emit structured output
- The layout pattern detection is harder to automate; likely stays as a Claude-driven analysis with a reference taxonomy that grows over time
- The PageSpeed API call is a single HTTP request; cheap to wrap
- Image format inventory is parseable from `web_fetch`'s returned HTML
- Add a new template file `references/design-dossier-template.md` that mirrors the format spec'd in the website-design domain's `inspiration/high-performing/_README.md`
- Add a new patterns file `references/visual-patterns-taxonomy.md` cataloging known section conventions (hero variants, services-grid variants, FAQ shapes, footer styles)

The implementation work is a follow-up project. This spec captures what the refinement should produce.

### Related

- [[decision-2026-05-23-pivot-to-custom-coded-websites-via-nextjs]] — the canonical decision triggering this refinement
- [[strategy-custom-coded-nextjs-via-ai-with-competitor-inspiration]] — the strategy the refinement supports
- [[tactic-emulate-competitor-design-patterns-with-ai]] — the tactic that consumes design dossiers
- `~/workspace/skills/design-emulation-verify/SKILL.md` — sister skill that verifies our build against the reference's dossier

---

## Refinement — link-map mode (added 2026-05-31)

**Status:** spec + worked example shipped 2026-05-31 in the Phase 4b internal-linking session. Implementation lives alongside this SKILL.md; outputs go to `second-brain/05_shared-intelligence/research-briefs/link-maps/`.

### Why this mode exists

The base skill captures Section 9 ("Internal-linking observations") inside each per-competitor brief, but the data sits buried among the rest of the SEO/positioning analysis. Phase 4b of the [[client-seo-onboarding-automation]] blueprint needs a denser, standalone deliverable: a **link map** — a structured picture of how a competitor's pages link to each other — that downstream consumers can read without wading through 3,000 words of unrelated brief.

The link map feeds two consumers:

1. **A synthesis recommendation** — "this is what our site's link graph should look like." One per client domain. Lives at `link-maps/_synthesis-<client-slug>.md`.
2. **The internal-linking inserter script** (`repos/ai-agency-core/scripts/insert-internal-links.py`) — reads the synthesis and proposes/inserts cross-links into the client's published page corpus.

Treat link-map mode the same way design-fingerprint mode is treated: a focused dimension that can run alongside the base skill (`dossier-plus-brief` equivalent) or on its own.

### Trigger phrases for link-map mode

In addition to the base skill's triggers, also use this mode when:

- "Map the internal links on [site]"
- "Run a link-map on [site]"
- "Analyze [site]'s internal-linking architecture"
- "Build a reference architecture for [client]'s link graph"
- "What does the link graph look like on [top competitor]"
- Any time a site is being prepared for the internal-linking inserter described in [[client-seo-onboarding-automation]] Phase 4b

### Inputs (in addition to the base skill's inputs)

- **Competitor URL list** — required. The homepage URL plus at least one service page and one location page per competitor. Three competitors per (service, city) cell is the default cap.
- **Client slug** — required when writing a synthesis. The synthesis filename is `_synthesis-<client-slug>.md`.
- **Output folder** — defaults to `second-brain/05_shared-intelligence/research-briefs/link-maps/`. One file per competitor + one synthesis per client.
- **Source for the competitor list** — pull from the relevant Tier 3 intersection brief if one exists (per Phase 2c); otherwise from the Phase 1 competitor identification step.

### Output contract — the link-map dossier format

Spec'd at `second-brain/05_shared-intelligence/research-briefs/link-maps/_README.md`. Reproduced here:

```
<competitor-slug>.md

Frontmatter:
- type: link-map
- status: draft | verified
- created, updated
- competitor-slug, competitor-domain
- source-pages-audited: [list of URLs]
- tags: [link-map, internal-linking, <client-slug>, <niche>]

Content sections (in order):
1. Identity (one paragraph — name, domain, what this map covers)
2. Top-level navigation
   - 2a. Main nav structure (with anchor text + destination)
   - 2b. Mega-menu depth (if applicable)
   - 2c. Mobile nav variations
3. Footer link blocks
   - 3a. Services column
   - 3b. Locations column
   - 3c. Support / legal column
   - 3d. Social block
4. Breadcrumb structure (pattern + depth)
5. In-body link patterns
   - 5a. Link density per page type (homepage, service page, city page, blog)
   - 5b. Anchor-text conventions (bare slug, full title, action phrase, sentence-embedded)
   - 5c. Link-graph between service pages, city pages, and hubs (mermaid diagram)
6. Related-content sections (end of page) — shape, count, ordering
7. Patterns worth emulating (3-5 specific patterns the client should adopt)
8. Patterns to skip (anti-patterns)
9. Sources audited
```

### New procedure for link-map extraction

Beyond the base skill's Section 9:

#### A. Nav and footer extraction

Procedure:

1. `mcp__workspace__web_fetch` the homepage. Extract the `<nav>` and `<footer>` blocks.
2. For each `<a href>` in those blocks, capture: anchor text, destination URL, destination type (service page / city page / hub / external / utility), nesting depth in the menu.
3. Group destinations by type. Note total count per type.
4. If the nav is a mega-menu (multi-column dropdown), capture the column structure. Mega-menus expose more links per page-impression and are a known ranking signal.
5. Note whether the same nav serves every page or whether contextual nav variants exist.

#### B. Breadcrumb extraction

Procedure:

1. Fetch a service page and a city page. Search for `<nav aria-label="breadcrumb">`, `<ol class="breadcrumb">`, schema.org `BreadcrumbList` markup, or visually-styled breadcrumb divs near the top of the main content area.
2. Capture: depth (Home > Category > Service vs. Home > Service), separator character, whether the current page is linked or plain text, schema markup presence.
3. Note whether breadcrumbs appear on every page type or only some.

#### C. In-body link density and anchor-text patterns

Procedure:

1. Pull the main content area of a service page (excluding nav/footer/sidebar).
2. Count `<a href>` tags inside that content area. Compute link density (links per 100 words) using the brief's word-count estimate.
3. Categorize each link's anchor text: bare slug (`/panel-upgrade/`), full title (`Electrical Panel Upgrades in Vienna VA`), action phrase (`See our EV charger installation page`), or sentence-embedded (`our panel-upgrade work in Vienna`).
4. Repeat on a city page and a blog post. The density and anchor-text mix often differ by page type.
5. Surface the dominant anchor-text style. Sentence-embedded links score higher with Google because they read like editorial, not navigation.

#### D. Link-graph mapping

Procedure:

1. From the service page, list every internal link destination (excluding nav/footer/utility links).
2. From the city page, do the same.
3. Build a directed graph: nodes are page types (homepage, service hub, service page, city page, neighborhood page, blog, FAQ); edges are link directions with frequency.
4. Render the graph as a mermaid diagram inside the brief. Reading the diagram tells the operator at a glance whether the site is a star (everything links to the homepage), a web (service pages link to city pages link to neighborhoods), or a hub-and-spoke (category hubs absorb link equity from leaf pages).
5. The graph shape is the reference architecture the client's site should match.

#### E. Related-content section audit

Procedure:

1. Look for sections labelled "Related Services," "You might also like," "Other electrical services we offer," etc. at the bottom of service and city pages.
2. Capture: card count, ordering logic (alphabetical, topical adjacency, popularity), link style (card, list, inline paragraph).
3. Note whether related-content selection is hand-curated or template-driven. Template-driven sets that always show the same five siblings are easy to reproduce; hand-curated sets are harder but read more natural.

### How this folds back into the base skill

When running the base skill in `link-map` mode alongside the standard competitor brief:

- The base skill's Section 9 ("Internal-linking observations") shrinks to a one-paragraph summary with a wikilink to the dossier: `Full link map: [[link-maps/<competitor-slug>]]`.
- The dossier carries the detailed evidence; the brief carries the strategic implication for the client's SEO and content plan.
- If running link-map mode standalone (no full brief), skip the brief and write only the dossier.

### When to use base skill vs link-map mode

| User intent | Mode |
|---|---|
| Full competitive landscape for SEO + content strategy | Base skill |
| Cross-page link architecture only | Link-map mode |
| Prepare input for the internal-linking inserter | Link-map mode + synthesis |
| Compare nav/footer/breadcrumb patterns across competitors | Link-map mode on each, then synthesis |
| Audit the client's own site against a reference architecture | Link-map mode on the client's site, compared against the synthesis |

If both base skill and link-map mode are needed, run base skill first, then link-map mode. They produce sibling files (the brief in `admin-extracts/competitor-research/`, the dossier in `research-briefs/link-maps/`).

### Synthesis output — the reference architecture recommendation

After running link-map mode on the top 2-3 competitors for the same (service, city) cell or the same client, write a synthesis at `<output-folder>/_synthesis-<client-slug>.md`. Use this shape:

```
Frontmatter:
- type: link-map-synthesis
- status: draft | promoted
- client-slug, client-domain
- competitors-mapped: [list]
- created, updated, tags

Content sections:
1. Headline finding (one paragraph: the strongest pattern across the link maps)
2. Reference architecture
   - 2a. Homepage links to: <concrete list>
   - 2b. Service hub links to: <concrete list>
   - 2c. Service-city page links to: <concrete list>
   - 2d. City page links to: <concrete list>
   - 2e. Category hub links to: <concrete list>
3. Anchor-text conventions to adopt (3-5 rules)
4. Link density targets per page type (table)
5. Patterns to skip (anti-patterns the competitors do but we won't)
6. Mermaid diagram of the recommended link graph
7. Mapping to the data-driven layer (`related_cards` recommendations per service)
8. Mapping to the semantic layer (where the AI inserter should add contextual links)
9. Verification checklist (what to confirm after the inserter has run a pass)
```

The synthesis is what `insert-internal-links.py` reads. The script's `--reference-architecture <path>` flag points at this file.

### Future implementation notes

- The nav/footer extraction lends itself to a script (`scripts/extract_nav_footer.py`) that takes a URL and emits structured output. Defer until 3+ link maps exist.
- Anchor-text classification can be partially automated with a regex/heuristic pass; full classification stays a Claude-driven analysis.
- Mermaid generation can be templated once the page-type taxonomy is stable.
- Cross-link the synthesis to the relevant Tier 1 service briefs' Section 9 — the `related_cards` recommendations should agree.

### Related

- [[client-seo-onboarding-automation]] — the blueprint Phase 4b serves
- `~/workspace/repos/ai-agency-core/scripts/insert-internal-links.py` — the script that consumes the synthesis
- `~/workspace/repos/ai-agency-core/scripts/README-insert-internal-links.md` — operator-facing docs
- [[_template-service-brief]] — Section 9 (internal-linking observations) feeds into link-map mode
- [[execution-log-2026-05-31-internal-linking-automation]] — the build session that shipped this refinement
