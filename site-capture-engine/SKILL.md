---
name: site-capture-engine
version: 2.1
description: >
  Universal site capture engine with context-aware output. Captures any website's complete state — HTML,
  screenshots, schema, assets, SingleFile per page, redirect map, broken links, meta-data audit,
  internal-link graph, form/embed/pixel inventories, DNS/WHOIS/SSL snapshots — then auto-detects output
  context from the folder path. Three output contexts: (1) Client site (website-archive/old/) → restoration
  package. (2) Competitor site (competitor-research/*-teardown/) → 6-pass forensic teardown + blueprint.
  (3) Design reference (website-design/inspiration/ or --design-capture) → design-capture package:
  multi-breakpoint screenshots (1440/768/390px), computed-style design tokens, motion/component inventory,
  a11y/contrast snapshot, design-capture-manifest.json. Capture is universal; output is context-aware. No
  modes — path determines output. --force-restore / --force-teardown / --design-capture escape hatches.
  Triggers: "capture <site>", "archive <client>'s site", "tear down <competitor>", "snapshot <site> before
  cutover", "reverse-engineer <site>", "blueprint <site>", "capture design tokens from <site>", "design
  capture <site>". 7 v1.1 plugin hooks ship as no-ops (Lighthouse, axe-core, GA4, GSC, GBP, DataForSEO
  backlinks, cookies) — credentials gate, not code gate. Composes with client-onboarding-automation Phase 5
  as Step A.5; feeds website-factory rebuilds; baseline for design-emulation-verify; feeds [DI-2]
  design-fingerprint, [DI-3] reference-library, [DI-4] design-emulation-verify.
composes-with: [competitor-deep-research, website-design, design-emulation-verify, client-onboarding-automation, website-factory, design-fingerprint, reference-library]
---

# Site Capture Engine (v2.1)

> **v2.1 changelog (2026-06-15)** — [DI-1] design-capture context extension. (1) **Third output context:
> design-capture** — auto-detects from `website-design/inspiration/` or `design-reference/` paths, or via
> `--design-capture` flag. Additive to universal capture — restoration and teardown contexts unchanged.
> (2) **Multi-breakpoint rendered screenshots** — desktop (1440px), tablet (768px), mobile (390px) — each
> with full-page + fold + per-major-section crops + scroll-stop captures + component bounding-box
> screenshots. `screenshot-manifest.json` maps every image. (3) **Computed-style design tokens** — extracted
> via `getComputedStyle` on the live rendered DOM (not source CSS): deduped color palette (hex + frequency +
> inferred role), type scale per semantic role (h1–h6/body/button/caption), spacing histogram + inferred base
> unit, border-radius set, shadow set. Output: `design-tokens.json` + `design-tokens.md`. (4) **Motion /
> interaction inventory** — CSS transitions, keyframe animations, library detection (Framer Motion / GSAP /
> AOS / Lottie / Intersection Observer). `motion-inventory.json`. (5) **Component inventory** — structural
> heuristic detection of hero, nav, card grid, FAQ accordion, CTA block, testimonial, footer. Bounding
> screenshot + descriptor per component. `component-inventory.json`. (6) **A11y / contrast snapshot** — WCAG
> contrast ratios on top text/background pairs (pass/fail AA+AAA), heading hierarchy outline, alt-text
> coverage %. `a11y-snapshot.json`. (7) **Design-capture manifest** (`design-capture-manifest.json`) — stable
> downstream contract; [DI-2]/[DI-3]/[DI-4] bind to this. (8) **Package contract reference** at
> `references/design-capture-package-contract.md`. New scripts: `extract_design_tokens.mjs` (token
> extractor). Extended: `capture_screenshots.mjs` (`--design-capture` flag).

> **v2.0 changelog (2026-06-14)** — Renamed from `seo-site-teardown`. (1) **Context-detection output
> layer:** capture is universal; output auto-detects from folder path — `website-archive/old/` → restoration
> package, `competitor-research/*-teardown/` → teardown analysis + reproduction blueprint. `--force-restore`
> / `--force-teardown` escape hatches. (2) **12 universal capture extensions:** SingleFile CLI per page,
> asset capture loop (images/fonts/videos/media), 301/308 redirect map, broken-link inventory, meta-data
> audit per page (title/meta/OG/canonical), internal-linking graph (per-page in/out + anchor text), form
> inventory, embed inventory (iframes/YouTube/maps/social), pixel/tracking script inventory
> (GTM/GA4/FB/Hotjar), DNS records snapshot, WHOIS snapshot, SSL certificate snapshot. (3) **WP-cli
> database export sister-step** (if WP credentials provided). (4) **Restoration package output** (SingleFile
> + restore-README.md + zipped archive) for client context. (5) **7 v1.1 plugin hooks** as empty no-ops with
> "credentials missing → skipped" log lines. (6) **Main orchestrator script** `scripts/capture_site.py`.
> (7) **v1.1 roadmap** at `references/v1.1-roadmap.md`. (8) **Compose-with-Phase-5** documentation for
> client-onboarding-automation Step A.5. All v1.1 teardown content (6 passes, tells catalog, DataForSEO
> endpoints, dossier template, questions bank) preserved intact.

> **v1.1 changelog (2026-06-11)** — Peer-reviewed + second-target validated via [WF-2] skill-build
> chat. (1) **Decoder rewrite:** `extract_nextjs.py` now supports 3 extraction paths — Next.js RSC
> (`self.__next_f.push`, App Router 13+), Next.js `__NEXT_DATA__` (Pages Router ≤12), and HTML
> fallback (WordPress, Hugo, GoDaddy, any non-Next.js site). Auto-detects framework. Platform
> fingerprinting for WordPress/Hugo/Jekyll/Gatsby/GoDaddy/Wix/Squarespace/Nuxt/Svelte. Validated
> on 3 real sites. (2) **6 peer-review fixes:** frontmatter pass count corrected (4→6), checklist
> Pass 6 (Blog) added (8 items), internal-linking architecture step added to Pass 1 + checklist,
> "reverse-engineered machine" synthesis section made explicit in deliverables + checklist,
> framework-artifact sitemap exclusion note added (tcb_symbol, elementor_library), "matrix absent"
> handling for sites without service×city cross-product. (3) **3 new reference files:**
> `tells-catalog.md` (47 tells across 6 passes), `dataforseo-endpoints.md` (4 endpoints with
> costs/fallbacks), `teardown-dossier-template.md` (28-section template). (4) **Second-target
> validation:** Root Electric (rootelectric.com) — WordPress/Thrive, 159 content pages, 947 ranked
> keywords, full 6-pass teardown with dossier at
> `s-and-h-contracting/admin-extracts/competitor-research/root-electric-teardown/`. DataForSEO
> $0.126. Key finding: Root Electric's 159 pages outperform AJ Long's 1,018 pages on every
> ranking metric (73 top-3 vs 2, $10.5K vs $516 ETV) — quality+authority beats quantity.

> Distilled from the 2026-06-04/05 AJ Long Electric teardown (the canonical worked example):
> `~/workspace/second-brain/04_projects/clients/_active/ev-electric-services/admin-extracts/competitor-research/aj-long-teardown/`.
> When anything here is unclear, read that folder — the `teardown-*.md`, `blueprint-website-factory.md`,
> and the `raw/`+`extracted/`+`data/` artifacts show exactly what a finished teardown-context run produces.

---

## What this skill is

A **universal site capture engine** that archives any website's complete state and produces context-appropriate
output. Capture runs the same every time — every page, every asset, every structural extract. Output
auto-detects what to produce from the folder path.

**Three contexts, one capture:**

| Output folder pattern | Context | Auto-produces | Skips |
|---|---|---|---|
| `.../website-archive/old/...` | **Restoration** | SingleFile per page + restore-README.md + zipped archive. Uses GSC for ranking data when credentials present. | DataForSEO ranking queries; reproduction blueprint; design-capture |
| `.../competitor-research/...-teardown/...` | **Teardown** | 6-pass forensic teardown analysis + reproduction blueprint. Uses DataForSEO for ranking data (optional, paid). | Restoration package; WP-cli DB export; design-capture |
| `.../website-design/inspiration/...` or `.../design-reference/...` or `.../design-capture/...` | **Design-capture** | Multi-breakpoint screenshots (1440/768/390px) + computed-style design tokens + motion inventory + component inventory + a11y/contrast snapshot + design-capture-manifest.json. | Restoration package; teardown analysis; DataForSEO |

`--force-restore` / `--force-teardown` / `--design-capture` exist as operator escape hatches. `--design-capture` can stack with restoration or teardown (additive).

**Core principle — retain everything.** Save every sitemap, every decoded page, every schema graph, every
data file. Modern SEO sites are usually Next.js/React and embed their **full content in the HTML** as
JSON-LD + RSC flight data — so a capture can recover the real FAQs, pricing, local facts, and structure
**without a browser**. Never summarize away the raw; future phases consume it.

## When to use

- **Client onboarding (Step A.5):** capture the client's current site at `website-archive/old/captured-YYYY-MM-DD/` before any changes. Produces a restoration package — "plug in this USB, your site is back."
- **Pre-rebuild snapshot:** capture immediately before a Next.js rebuild kicks off, so the rebuild seeds from current state.
- **Quarterly re-capture:** scheduled every 90 days for active clients.
- **Competitor teardown:** before building a custom client site, to blueprint the strongest competitor.
- **Competitor watchdog:** when a change alert fires, re-run to diff against the prior snapshot.
- **Design reference capture:** capture any site's visual design system — tokens, motion, components, a11y — for the inspiration library or as a design direction input for a client build.
- Any time the operator says "capture/archive/snapshot <site>", "tear down/reverse-engineer <site>", or "capture design tokens from <site>."

Do **not** use for: a quick "who ranks for X" lookup (web search), a positioning-only brief (use
`competitor-deep-research`), or writing a structured design dossier from captured data (use
`design-fingerprint` skill, [DI-2] — this skill captures; [DI-2] interprets). Compose with those —
this skill is the deepest, build-oriented capture tier.

## Inputs

1. **Target site** (one domain).
2. **Output folder** — context auto-detected from path (see table above).
3. **WP credentials** (optional) — if the target is a WordPress site with admin access, provide `--wp-url`, `--wp-user`, `--wp-pass` for database export.
4. **DataForSEO availability** (teardown context only) — confirm the tier-3 wrapper probes clean. Pass 3 needs Labs. ~$0.03–0.50 total.
5. **Client context** (teardown context only) — who we're building for, their geography + service set.

## Host prerequisites

```bash
# Playwright (screenshots)
npm install playwright && npx playwright install chromium

# SingleFile CLI (self-contained HTML per page)
npm install -g single-file-cli

# WP-CLI (WordPress database export — optional)
brew install wp-cli   # or: curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
```

The capture engine runs on the **host** (Mac via Claude Code or CI worker), not the Cowork sandbox. Playwright's ~185MB Chromium download can't finish in the sandbox's short command window.

---

## Universal capture set (runs for any context)

These run every time, regardless of whether the output is restoration or teardown:

### Existing captures (from v1.0/v1.1)
- Sitemap enumeration (sitemap.xml → robots.txt → recursive same-origin crawl with depth cap)
- Per-page raw HTML capture (curl-based)
- Per-page rendered HTML (Playwright post-JS DOM — via `capture_screenshots.mjs`)
- Per-page screenshots (desktop 1440×900 + mobile iPhone 13; above-fold + full-page)
- Schema.org / JSON-LD graph extraction
- CSS files capture
- JS files capture
- Next.js / RSC content extraction (when applicable — via `extract_nextjs.py`)
- `robots.txt` + `llms.txt` capture
- Sitemap manifest + per-page metadata JSON

### v2.0 capture extensions
1. **SingleFile CLI per page** — self-contained .html that opens correctly in any browser standalone. The killer feature for restoration: one file = one page, fully offline, CSS/images/fonts inlined.
2. **Asset capture loop** — images, fonts, videos, linked media (extends v1's CSS-only asset capture). Files >50MB are metadata-only by default; `--include-large-media` for explicit opt-in.
3. **301/308 redirect map extraction** — critical for WP→Next.js migration. Follow each URL, record the chain.
4. **Broken-link inventory** — operator-facing punchlist of internal 4xx/5xx links.
5. **Meta-data audit per page** — title, meta description, OG tags, canonical URL, JSON-LD types. Per-page JSON output.
6. **Internal-linking graph** — per-page in/out links + anchor text. JSON graph output.
7. **Form inventory** — location, fields, POST target, field count. Surfaces conversion touchpoints.
8. **Embed inventory** — iframes, YouTube, Google Maps, Vimeo, social embeds. Typed classification.
9. **Pixel/tracking script inventory** — GTM, GA4, FB Pixel, Hotjar, Clarity, Segment, HubSpot, etc. ID extraction where exposed.
10. **DNS records snapshot** — A/AAAA/CNAME/MX/TXT/NS via `dig`.
11. **WHOIS snapshot** — registrar, expiry, creation date, transfer-lock state.
12. **SSL certificate snapshot** — issuer, expiry, subject, SANs, key info.

### v1.1 plugin hooks (no-op — fire once, log skip)
7 hooks ship as empty no-ops. Each logs "credentials missing → skipped." v1.1 fills the bodies once credentials are wired — no rework, just credential gates:

1. **Lighthouse / PageSpeed snapshot per page** — `hook_lighthouse()` — TODO v1.1
2. **axe-core accessibility audit per page** — `hook_axe_accessibility()` — TODO v1.1
3. **GA4 historical traffic snapshot per URL** — `hook_ga4_traffic()` — TODO v1.1
4. **GSC indexed-pages snapshot** — `hook_gsc_indexed_pages()` — TODO v1.1
5. **GBP listing snapshot per location** — `hook_gbp_listing()` — TODO v1.1
6. **DataForSEO backlink-profile snapshot** — `hook_dataforseo_backlinks()` — TODO v1.1
7. **Cookie inventory** — `hook_cookie_inventory()` — TODO v1.1

See `references/v1.1-roadmap.md` for insertion points, credential prereqs, and regression test plans.

---

## WP-cli database export (restoration context, optional)

For WordPress clients with credentials provided. Strongest restoration fidelity.

```bash
python3 capture_site.py https://example.com <out-dir> \
  --wp-url https://example.com/wp-admin \
  --wp-user admin --wp-pass <pass>
```

Exports: posts table, media library metadata, plugin config, options table. Skip if no WP credentials — the HTML + SingleFile captures are the fallback.

---

## Restoration package output (client context only)

When context = restoration (output folder matches `website-archive/old/`):

1. **SingleFile per page** — one self-contained .html per captured URL
2. **restore-README.md** — plain-language recovery instructions: "Open `pages/home.singlefile.html` in any browser — your site is back exactly as it was"
3. **Zipped archive** — `restoration-package-YYYY-MM-DD.zip` containing SingleFile pages + assets + restore-README

This is the "plug in this USB" artifact. A non-technical client can open any page in a browser and see their site.

---

## Design-capture output (design-reference context or `--design-capture`)

When context = design-capture (output folder matches `website-design/inspiration/`, `design-reference/`,
`design-capture/`, or `--design-capture` flag), the design-capture package is produced on top of the
universal capture. This is **additive** — `--design-capture` can stack with restoration or teardown.

**Produced artifacts:**

1. **Multi-breakpoint screenshots** — desktop (1440px), tablet (768px), mobile (390px). Each gets
   full-page + above-the-fold + per-major-section crops + scroll-stop captures. Component bounding-box
   screenshots (desktop). All indexed in `screenshot-manifest.json`.
2. **Computed-style design tokens** — `design-tokens.json` + `design-tokens.md`. Extracted from the live
   rendered DOM via `getComputedStyle` (not source CSS). Palette (hex + frequency + inferred role), type
   scale (per semantic role), spacing (histogram + base unit), border-radius, shadows.
3. **Motion / interaction inventory** — `motion-inventory.json`. CSS transitions, keyframe animations,
   detected libraries (Framer Motion, GSAP, AOS, Lottie).
4. **Component inventory** — `component-inventory.json`. Detected: hero, primary nav, card grid, FAQ
   accordion, CTA block, testimonial, footer. Bounding rect + descriptor per component.
5. **A11y / contrast snapshot** — `a11y-snapshot.json`. WCAG contrast ratios (top 20 pairs, pass/fail
   AA+AAA), heading hierarchy outline, alt-text coverage %.
6. **Design-capture manifest** — `design-capture-manifest.json`. Top-level index for all design-capture
   artifacts. Downstream skills ([DI-2]/[DI-3]/[DI-4]) bind to this manifest, not to file paths.

**Full contract:** `references/design-capture-package-contract.md`.

**Scripts:** `scripts/extract_design_tokens.mjs <url> <out-dir>` +
`scripts/capture_screenshots.mjs <domain> <out-dir> [urls.txt] --design-capture`.

---

## Teardown passes (competitor-research context)

When context = teardown, the 6-pass forensic analysis runs on top of the universal capture. Each pass sees what the previous one couldn't. The depth compounds — do not collapse passes.

### PASS 1 — Forensic structure (map the machine)

Goal: the page-tier taxonomy, the content templates, the per-entity data layer, and the language.

1. **Page inventory from the sitemap.** Fetch `sitemap.xml`; if it's a sitemap index, fetch every nested
   sitemap and count `<loc>` each. Record the true page count and the per-type breakdown. This is the
   ground truth — never trust a third-party "page count." **Exclude framework artifact sitemaps** from the
   content count (e.g., Thrive Architect `tcb_symbol-sitemap`, Elementor `elementor_library-sitemap`,
   WordPress `wp_template-sitemap`) — these are reusable template fragments, not pages visitors see.
2. **Identify the page tiers.** Group URLs by pattern into tiers (core/conversion, service hubs,
   **service×city matrix**, city/location, neighborhood, problem/symptom, guide, blog). Note counts.
   Not all sites have a matrix — many use flat service pages + flat city pages without cross-product.
   Record "matrix absent" explicitly (this is a finding, not a gap in the teardown).
3. **Decode representative pages (≥1 per tier).** Fetch full HTML, run `extract.py` to pull JSON-LD schema
   + RSC content. For each tier capture: section order, FAQ Q&As (verbatim), pricing, the **data points
   fused** (see below), word/heading counts, internal links.
4. **Map the per-entity data layer (the moat).** For the matrix pages, list every per-city/per-entity fact
   fused into the template: neighborhoods, housing era, permit authority + portal, utility, code/regulation
   specifics, brand/condition prevalence, year-stamped pricing, ZIP codes, population, cross-sells. THIS is
   what's expensive to research and what we must reproduce — templates are cheap.
5. **Read the language / craft ladder.** Premium tier (money pages) vs light tier (long-tail) — note the
   voice difference and the trust devices (certs, reviews, warranty, verifiable claims, local specificity).
6. **Map the internal-linking architecture.** From decoded pages, trace the full linking topology:
   hub→leaf (service hub → service×city pages), breadcrumb chains, cross-sell sidebar links, blog→service
   funneling, footer/nav link surfaces. Note: is linking template-driven (automatic) or hand-curated? How
   deep is the longest path from homepage? What's the orphan risk?

**Gate 1:** report the structure + page count + headline. Get operator confirmation before the deep passes.

---

### PASS 2 — Gap-fill (find what you didn't know to look for)

Goal: the things Pass 1 structurally can't see.

1. **`robots.txt` + `llms.txt` + AI-crawler posture.** Look explicitly for an AI-crawler allow-list
   (GPTBot, OAI-SearchBot, PerplexityBot, ClaudeBot, Google-Extended, Applebot-Extended, CCBot, Bytespider)
   and an `llms.txt` site index.
2. **Image pipeline.** Check for `/_next/image`, `.webp`/`.avif`, `srcset`.
3. **Matrix gap grid.** Compute which (service × city) cells are built vs not.
4. **Per-entity research seed — extract ALL of them.** Fetch every city/location page, decode, build the
   research seed mapping each entity → its data fields.
5. **Full inventories.** Save clean slug lists for blog/neighborhoods/problems/guides + the service taxonomy.

---

### PASS 3 — Tech/tools fingerprint + what ACTUALLY ranks

Goal: make **every tool explicit** and confirm what truly performs.

1. **Response headers** (`curl -I`): hosting/CDN, framework, ISR, security headers.
2. **Framework + build:** Next.js RSC, Turbopack, Tailwind, self-hosted fonts, image optimization.
3. **Third-party tools** — grep all payloads for external domains + script tags. Name each tool + its
   account token if exposed.
4. **Trust/cert mining** — license numbers, insurance, manufacturer certifications.
5. **DataForSEO — what actually ranks** (Labs subscription):
   - `ranked_keywords/live` → total ranked keywords, est. visits/value, which URLs rank.
   - `historical_rank_overview/live` → 6–12 months of keyword count + etv + position bands.

**Gate 2:** the ranked-keywords finding usually reframes strategy — report before Pass 4.

---

### PASS 4 — Conversion/UX + history + archaeology (traffic → money)

Goal: how they turn rankings into booked jobs, plus the migration + history.

1. **Conversion/CTA system.** Persistent header CTAs, per-page conversion sidebar, symptom checklists,
   24/7 booking layer. Map the full funnel.
2. **Migration playbook.** Check whether old URLs 301/308-redirect to new ones.
3. **Old-page archaeology.** Recover proven winners via Wayback Machine.
4. **Conversion + authority gap.** Reconcile with Pass-3 history.

**Gate 3 (closing):** dossier + blueprint updates.

---

### PASS 5 — Design system, strategic intent & money mechanics

Goal: the visual layer, WHY they built what they built, and the conversion levers HTML hides.

1. **Design tokens (from CSS).** Extract palette, CSS custom properties, font families.
2. **Visual composition** (REQUIRES screenshots). Hero layout, section rhythm, CTA design, mobile sticky-CTA.
3. **Strategic intent.** Read sitemap `<lastmod>` dates for programmatic scaling events.
4. **Money mechanics.** Financing, sticky mobile CTA, click-to-call density, form friction, call-tracking.

**Screenshots — automate, don't hand-capture.** Use `scripts/capture_screenshots.mjs`.

---

### PASS 6 — Blog deep-analysis (for the reusable blog engine)

If the site has a blog, tear it down for the blog engine. Sample ≥6 posts across topic types. Capture
writing style, structure, depth signals, topic engineering, internal linking, what actually ranked.

---

## Indexing & publishing lesson (answer the "200/day" question)

**Sitemap publishing has NO per-URL limit** — Google discovers on its own schedule. The **~200/day cap is on
manual/API priority-indexing requests**. Winning play: mass-publish via split sitemaps + GSC submission, then
selectively ACCELERATE highest-value pages via Indexing API (~200/day) / Bing IndexNow (up to 10k/day).

---

## Change tracking (before/after — every capture is a baseline)

Every capture is a dated snapshot. Structure the folder so re-runs diff cleanly:
- `raw/sitemaps/`, `raw/payloads/`, `raw/screenshots/<YYYY-MM-DD>/` — dated where it changes.
- On a change alert, re-run, save into a new dated capture, and write `changes-<YYYY-MM-DD>.md`.

### Re-capture cadence
- **Onboarding capture** — fires once at Step A.5, baseline at `captured-YYYY-MM-DD/`
- **Quarterly re-capture** — scheduled task fires every 90 days for active clients
- **On-demand re-capture** — operator can fire anytime ("capture-now <slug>")
- **Pre-rebuild re-capture** — fired automatically right before a Next.js rebuild kicks off

Latest snapshot wins for any downstream use (rebuild input, restoration package, GSC comparison).

---

## Quality gates (MANDATORY)

1. **`gate-peer-reviewer`** — gate each major artifact at its produce-step.
2. **`house-voice-rewrite` Mode 2** (conditional — client-facing artifacts only).
3. **`output-quality-loop` (EVALUATE mode)** — closing eval. Cap 3 iterations; escalate on 3rd FAIL.

---

## Deliverables

### Universal (every run)
1. **Retained raw** — `html/` (raw HTML per page), `meta/` (per-page meta JSON), `screenshots/`, `css/`, `assets/`
2. **Structured extracts** — `sitemap.json`, `internal-link-graph.json`, `redirect-map.json`, `broken-links.json`, `form-inventory.json`, `embed-inventory.json`, `tracking-pixels.json`, `dns-records.json`, `whois.txt` + `whois-summary.json`, `ssl-certificate.json`
3. **robots.txt** + **llms.txt**
4. **capture-manifest.json** — engine version, timestamp, page count, context, skip log
5. **Folder `_README.md`** + parent update

### Restoration context (client path)
6. **SingleFile per page** — self-contained .html per URL
7. **restore-README.md** — plain-language recovery instructions
8. **restoration-package-YYYY-MM-DD.zip**
9. **WP-cli database export** (if credentials provided)

### Teardown context (competitor path)
6. **Teardown dossier** — `teardown-YYYY-MM-DD-full-build-analysis.md`
7. **Reproduction blueprint** — `blueprint-website-factory.md`
8. **`extracted/`** (decoded content + schema per page via `extract_nextjs.py`)
9. **`data/`** (inventories, matrices, research seed, DataForSEO pulls)

### Design-capture context (design-reference path or `--design-capture`)
6. **Multi-breakpoint screenshots** — desktop/tablet/mobile full-page + fold + section crops + scroll-stops + component screenshots + `screenshot-manifest.json`
7. **`design-tokens.json`** + **`design-tokens.md`** — computed-style palette, type scale, spacing, radius, shadows
8. **`motion-inventory.json`** — transitions, keyframe animations, library detection
9. **`component-inventory.json`** — detected recurring visual components with bounding rects
10. **`a11y-snapshot.json`** — WCAG contrast ratios, heading hierarchy, alt-text coverage
11. **`design-capture-manifest.json`** — top-level index for all design-capture artifacts (downstream binding surface)

---

## The "tells" catalog

Codified so future runs don't miss them. Look for each; note present/absent:

- **Next.js RSC** (`self.__next_f`) → full content recoverable from HTML without a browser.
- **Sitemap index** split by type → count every nested sitemap.
- **Service×city matrix** → the page-count engine; compute the gap grid.
- **Per-entity research data layer** fused into templates.
- **Craft ladder** — premium money pages vs slot-filled long-tail.
- **Comprehensive JSON-LD graph** incl. `FAQPage`, `Offer`, `AggregateRating`, `BreadcrumbList`, `HowTo`, `SpeakableSpecification`.
- **AI-crawler allow-list** in robots.txt + `llms.txt`.
- **Tool stack** — every tool named.
- **Multi-GBP** local strategy + manufacturer certs.
- **Conversion sidebar** + symptom checklists + multiple capture paths + 24/7 voice booking.
- **Recent rebuild?** → old URLs 301/308-redirect to new + indexation lag + breadth-vs-position gap.
- **Single-day mass-generation** → programmatic scaling event.
- **Design tokens** → palette, font stack, motion.
- **Money/close-rate levers** → financing, sticky mobile CTA, minimal forms.

---

## Working principles

1. **Capture is universal; output is context-aware.** Same capture every time. Path determines the package.
2. **Multi-pass for teardowns.** The biggest findings come in passes 3–4.
3. **Retain everything; summarize nothing away.** Raw HTML + decoded text + data files all stay.
4. **Free/fetch tools first, then cheap DataForSEO.**
5. **Confirm what RANKS, not just what's built.**
6. **Conversion is half the answer.**
7. **Be honest about gaps.** Name what you couldn't capture.
8. **Plain language.**
9. **Every capture feeds downstream.** Restoration feeds recovery; teardown feeds the website-factory build.

---

## Reference files & scripts

- `scripts/capture_site.py` — **main orchestrator** (v2.0). Universal capture + context detection + all 12 extensions + v1.1 hooks. Entry point.
- `scripts/extract_nextjs.py` — multi-path content decoder: Next.js RSC, `__NEXT_DATA__`, HTML fallback. Auto-detects framework.
- `scripts/capture_screenshots.mjs` — Playwright host script for automated screenshots (desktop+mobile, fold+full, dated folders). With `--design-capture`: adds tablet (768px) viewport, per-section crops, scroll-stop captures, component bounding-box screenshots, `screenshot-manifest.json`. **Requires:** `npm install playwright` + `npx playwright install chromium`.
- `scripts/extract_design_tokens.mjs` — Playwright computed-style token extractor (v2.1). Extracts palette, type scale, spacing, radius, shadows from live rendered DOM via `getComputedStyle`. Also captures motion inventory, component inventory, a11y/contrast snapshot. **Requires:** Playwright.
- `references/teardown-checklist.md` — per-pass concrete checklist (teardown context).
- `references/questions-bank.md` — psychology/strategy probes.
- `references/tells-catalog.md` — 47 tells across 6 passes.
- `references/dataforseo-endpoints.md` — API calls, parameters, costs, fallbacks.
- `references/teardown-dossier-template.md` — 28-section template for new teardown runs.
- `references/v1.1-roadmap.md` — each v1.1 hook + insertion point + credential prereq + regression test plan.
- `references/design-capture-package-contract.md` — stable output contract for the design-capture context (v2.1). Downstream skills ([DI-2]/[DI-3]/[DI-4]) bind to this.
- **Worked examples:**
  - AJ Long teardown (teardown context): `ev-electric-services/admin-extracts/competitor-research/aj-long-teardown/`
  - Root Electric teardown (teardown context): `s-and-h-contracting/admin-extracts/competitor-research/root-electric-teardown/`
  - EV post-Core-30 capture (restoration context): `ev-electric-services/website-archive/old/post-core-30/`

## Registration

This skill is registered by **convention**: the presence of `SKILL.md` at
`~/workspace/skills/site-capture-engine/` makes it loadable by any Claude Code session or Cowork
chat. The toolkit-reuse-map at `second-brain/05_shared-intelligence/tools/_toolkit-reuse-map.md` tracks
the version and reusability classification.

## Composition

- **client-onboarding-automation Phase 5** — site-capture-engine is **Step A.5** of the orchestrator chain. Fires post-BOOTSTRAP, pre-Phase 2d client-fact research. Captured artifacts feed Phase 2d as primary source.
- **competitor-deep-research** — run first for the landscape (who ranks); then this skill on the one site to out-build.
- **design-emulation-verify** — captured snapshot becomes the "before" baseline for any subsequent rebuild verification.
- **website-design** — **downstream**: consumes the teardown dossier's design-fingerprint sections as design direction inputs.
- **website-factory program** — consumes the blueprint + structured extracts as rebuild seed.
- **output-quality-loop** — closing eval on produced artifacts.
- **gate-peer-reviewer** — gates each major artifact at produce-step.
- **[DI-2] design-fingerprint** — **downstream**: consumes the design-capture package (design-tokens.json + screenshots + motion inventory) to produce structured design dossiers with normalized trait vocabulary.
- **[DI-3] reference-library** — **downstream**: consumes design-capture manifest to populate the curated reference library + candidates registry.
- **[DI-4] design-emulation-verify** — **downstream**: consumes design-capture tokens + screenshots as build-vs-reference diff baseline.

## Failure modes + recovery

- **SingleFile CLI fails on JS-heavy SPA pages** → fall back to raw rendered HTML + screenshot pair; log gap in sitemap.json
- **WP-cli auth fails despite credentials provided** → fall back to wp-content/uploads + posts table via direct SQL; if both fail, log gap and proceed
- **Playwright Chromium download exceeds disk quota** → operator-side prerequisite; skill refuses with clear error if absent
- **Large media files (>50 MB videos)** blow up archive size → metadata-only by default; `--include-large-media` for opt-in
- **Anti-bot Cloudflare blocks Playwright** → fall back to Claude in Chrome manual capture; flag in sitemap.json
- **AJ Long regression mismatches existing teardown** → block ship until investigated
- **Context-detection misfires** → `--force-restore` / `--force-teardown` available; surface for review
