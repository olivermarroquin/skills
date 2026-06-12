---
name: seo-site-teardown
version: 1.1
description: >
  Multi-pass forensic teardown of a high-performing SEO website, top to bottom, to produce a
  reproduction blueprint — the inputs a custom Next.js client-site build needs. Use this whenever the
  goal is to deeply understand HOW a winning site is built (not just "who ranks") so we can duplicate
  and beat it: page-tier taxonomy, the per-entity research data layer, content templates and language,
  full JSON-LD schema graph, internal-link architecture, the complete tech/tools stack (framework,
  hosting, booking/CRM, analytics, AI agent, AI-crawler strategy), what ACTUALLY ranks and the traffic
  history (via DataForSEO), and the conversion/UX system that turns traffic into booked jobs. Triggers:
  "tear down <site>", "reverse-engineer <site>", "study <competitor>'s whole build", "how is <site>
  built", "blueprint <site> so we can replicate it", "deep teardown for the website factory",
  "what is <site> doing that's working and how do we copy it". Runs in 6 escalating passes with operator
  gates, retains ALL raw data, and emits a teardown dossier + a reproduction blueprint. This is the
  research front-end of the website-factory program — run it on every reference site before a client
  Next.js build. Distinct from `competitor-deep-research` (SEO/positioning briefs); this is a full-build
  reproduction teardown. Compose them: competitor-deep-research for the landscape, seo-site-teardown for
  the one site you intend to out-build.
---

# SEO Site Teardown (v1.1)

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
> and the `raw/`+`extracted/`+`data/` artifacts show exactly what a finished run produces.

## What this skill is

A repeatable, **multi-pass** process for reverse-engineering a winning site's **entire build** so we can
reproduce and out-execute it for a client. The output is not a competitor opinion — it is a concrete
**reproduction blueprint**: the data model, page templates, tech stack, schema, internal-linking, AND the
conversion layer, grounded in retained raw evidence and in what actually ranks.

**Why multi-pass.** Each pass sees what the previous one couldn't. Pass 1 maps the structure; Pass 2 fills
the gaps you didn't know were there; Pass 3 makes every tool explicit and checks what truly ranks; Pass 4
finds the conversion machinery and the history. The depth compounds — do not collapse it into one pass.
The canonical run found its single most important fact (the new pages weren't ranking yet) only in Pass 3,
and the "make money not just pages" insight only in Pass 4.

**Core principle — retain everything.** Save every sitemap, every decoded page, every schema graph, every
data file. Modern SEO sites are usually Next.js/React and embed their **full content in the HTML** as
JSON-LD + RSC flight data — so a teardown can recover the real FAQs, pricing, local facts, and structure
**without a browser**. Never summarize away the raw; future build phases consume it.

## When to use

- Before building (or pitching) a custom Next.js client site, to blueprint the strongest competitor.
- When a competitor watchdog flags a big change (page-count jump, rebuild) and you need to know exactly
  what changed and what it means.
- Any time the operator says "study/teardown/reverse-engineer <site>" or "blueprint it so we can replicate."

Do **not** use for: a quick "who ranks for X" lookup (web search), a positioning-only brief (use
`competitor-deep-research`), or a pure visual-design dossier (use competitor-deep-research design-fingerprint
mode). Compose with those — this skill is the deepest, build-oriented tier.

## Inputs

1. **Target site** (one domain — this is a single-site deep teardown, not a landscape).
2. **Client context** — who we're building for, their geography + service set (so the teardown maps the
   reference's data layer onto the client's footprint).
3. **Output folder** — default `<client-vault>/admin-extracts/competitor-research/<slug>-teardown/`.
4. **DataForSEO availability** — confirm the tier-3 wrapper (`~/workspace/second-brain-tier3/automation/
   scripts/dataforseo_query.py`) probes clean and which subscriptions are active (Labs vs Backlinks). Pass 3
   needs Labs. ~$0.03–0.50 total for the ranked-keywords + historical + pagespeed calls.
5. **Time budget** — a full 4-pass run is ~6–12h of agent work. Single-chat-friendly; decompose by pass
   if needed.

## Setup

Create the folder skeleton and run all fetches from the sandbox (curl) — Next.js content is in the HTML:

```
<slug>-teardown/
  raw/        sitemaps/  payloads/  cities|entities/  extra/  robots.txt  llms.txt
  extracted/  (decoded content + schema per page)
  data/       (inventories, matrices, research seed, DataForSEO pulls)
  teardown-YYYY-MM-DD-full-build-analysis.md
  blueprint-website-factory.md   (or reference the program blueprint)
  _README.md
  extract.py  (copy scripts/extract_nextjs.py)
```

Always write a folder `_README.md` and update the parent's (vault stewardship). Retain raw HTML by default
(offer a `.gitignore` for `raw/**/*.html` if repo size matters).

---

## PASS 1 — Forensic structure (map the machine)

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
   deep is the longest path from homepage? What's the orphan risk? (Canonical run: §8 found hub-spoke +
   breadcrumbs + sidebar cross-sell + blog→service funneling — all template-driven, max 3 clicks.)

**Pass-1 questions to answer:** What are the tiers and counts? What's the matrix (services × cities)? What
per-entity data is fused? Is there a craft ladder (premium vs templated)? What's the internal-linking
topology? What's the headline finding?

**Gate 1:** report the structure + page count + headline. If a watchdog signal triggered this, this is
where you confirm "real vs artifact." Get operator confirmation before the deep passes.

---

## PASS 2 — Gap-fill (find what you didn't know to look for)

Goal: the things Pass 1 structurally can't see.

1. **`robots.txt` + `llms.txt` + AI-crawler posture.** Fetch both. **Look explicitly for an AI-crawler
   allow-list** (GPTBot, OAI-SearchBot, PerplexityBot, ClaudeBot, Google-Extended, Applebot-Extended,
   CCBot, Bytespider) and an `llms.txt` site index. These are a deliberate answer-engine play and the
   cheapest highest-leverage thing to copy. (Canonical run: AJ Long allow-listed all of them + shipped llms.txt.)
2. **Image pipeline.** Check for `/_next/image`, `.webp`/`.avif`, `srcset` — is the modern-format gap open
   or closed?
3. **Matrix gap grid.** Compute which (service × city) cells are built vs not. Saturation tells you their
   frontier and whether any cell is unclaimed.
4. **Per-entity research seed — extract ALL of them.** Fetch every city/location page (not just samples),
   decode, and build a `<entities>-research-seed.md` mapping each entity → its data fields. This is the
   direct reproduction seed for the client's `cities.json`. Watch for **demographic-aware variation** (the
   "common issues" line shifting by city wealth/age — a tell of genuine research).
5. **Full inventories.** Save clean slug lists for blog/neighborhoods/problems/guides + the service taxonomy
   (often grouped into categories in the mega-menu — capture the category IA).

**Pass-2 questions:** AI-crawler strategy? Image pipeline? Where's the build frontier? What's the full
per-entity data layer? What's the service-category IA?

---

## PASS 3 — Tech/tools fingerprint + what ACTUALLY ranks

Goal: make **every tool explicit** (so we can duplicate or beat it) and confirm what truly performs.

1. **Response headers** (`curl -I`): hosting/CDN (`server:`, `x-nf-request-id`=Netlify, `via`/`x-vercel`=
   Vercel), framework (`x-nextjs-*`), **ISR** (`x-nextjs-stale-time`), security headers, `Permissions-Policy`
   (microphone=self ⇒ a voice agent).
2. **Framework + build:** `self.__next_f` (Next.js RSC), `turbopack-*` chunk (Next 15+), Tailwind utility
   classes, `next/font` self-hosted woff2, `/_next/image`.
3. **Third-party tools — grep all payloads for external domains + script tags.** Concretely look for:
   **booking/CRM** (HousecallPro `online-booking.housecallpro.com`, ServiceTitan, Jobber, Calendly),
   **analytics** (GTM, GA4), **voice/chat AI** (ElevenLabs, Vapi, Retell, GPT/OpenAI), **review widgets**
   (Birdeye, Podium, NiceJob — or none = custom), **auth/forms/CDN**. Name each tool + its account token if
   exposed. (Canonical run: Netlix+Next.js+ISR · Tailwind · HousecallPro · GTM · ElevenLabs+GPT voice agent ·
   custom schema · llms.txt.)
4. **Trust/cert mining** (`/about/credentials` or equiv.): license numbers (+ how to verify them),
   insurance, **manufacturer certifications** (these are trust + keyword surfaces).
5. **DataForSEO — what actually ranks** (Labs subscription):
   - `dataforseo_labs/google/ranked_keywords/live` (target=domain, order_by etv desc) → total ranked
     keywords, est. visits/value, **and which URLs rank**. Critically: **are the NEW programmatic URLs
     ranking, or the OLD ones?** (Canonical run: only ~395 kw/~516 visits, all on OLD URLs that
     301/308-redirect to new — the 1,018 new pages weren't ranking yet.)
   - `dataforseo_labs/google/historical_rank_overview/live` → 6–12 months of keyword count + etv +
     position bands. **Watch breadth (kw count) vs position (top-3).** Breadth rising + top-3 flat = pages
     rank but on page 2; revenue needs position, not just pages.
   - Note which subscriptions are NOT active (e.g. Backlinks) and fall back to the BrightLocal/Ahrefs baseline.

**Pass-3 questions:** What's the full toolchain (every tool named)? Is it off-the-shelf-reproducible? What
actually ranks — new pages or old? Is the page bet paying off yet (history trend)? Where's the position gap?

**Gate 2:** the ranked-keywords finding usually reframes strategy — report it before Pass 4.

---

## PASS 4 — Conversion/UX + history + archaeology (traffic → money)

Goal: how they turn rankings into booked jobs, plus the migration + history.

1. **Conversion/CTA system.** From payloads + (if available) screenshots, capture: persistent header CTAs
   (click-to-call + Book Online), the **per-page conversion sidebar** (Need-Help-Now + Request-Quote +
   response-time reassurance; a Service-Area-Information card with county/population/ZIPs; an Other-Services
   cross-sell), in-body **symptom checklists** ("Signs You Need…"), and the **24/7 booking layer** (voice AI
   that books real jobs after hours). Map the full funnel: organic/local-pack → hyper-local page → qualify →
   trust stack → multi-path CTAs → booking.
2. **Migration playbook.** Check whether old URLs 301/308-redirect to new ones (equity preservation). If
   the site recently rebuilt, this is the client's WordPress→Next.js migration template — enumerate the
   old→new redirect map.
3. **Old-page archaeology.** The old high-ranking URLs (from Pass-3 ranked_keywords) are the proven winners.
   Their bodies are usually replaced (redirects), but recover them via the **Wayback Machine**
   (`web.archive.org` CDX API + snapshots) to study what earned the rankings. If archive.org is down, defer
   to a retry.
4. **Conversion + authority gap.** Reconcile with Pass-3 history: breadth is easy, position needs the
   authority layer (reviews velocity, **multi-GBP** count, backlinks, quality) + the conversion layer. State
   plainly that more pages ≠ more money without these.

**Pass-4 questions:** How do they convert? What are the CTAs and the funnel? Is there a 24/7 booking agent?
Did they migrate with redirects (our playbook)? What did the old winning pages look like? What's the
authority/conversion gap between breadth and revenue?

**Gate 3 (closing):** dossier + blueprint updates, framed strategy questions, closing protocol.

---

## PASS 5 — Design system, strategic intent & money mechanics

Goal: the visual layer, WHY they built what they built, and the conversion levers HTML hides.

1. **Design tokens (from CSS).** Fetch the `/_next/static/chunks/*.css`; extract the hex palette (by
   frequency), CSS custom properties (`--color-*`, `--container-*`, `--blur-*`, `--animate-*`), and font
   families. Output `data/design-tokens.md`: primary brand color, dark/light theme surfaces, semantic
   colors, font stack, framework (Tailwind vN), and motion (pulse/ping/glow). Re-themeable per client.
2. **Visual composition (REQUIRES pixels — name the gap).** The analyst reads HTML, not pixels. Get
   **screenshots per page-tier** (operator-provided or Claude-in-Chrome render), desktop + mobile,
   above-the-fold + full, saved to `raw/screenshots/`. Then write a visual-composition section: hero
   layout, section rhythm, CTA design/contrast/placement, trust-signal placement, imagery art-direction,
   mobile sticky-CTA, motion. Above-the-fold composition decides conversion — always capture it.
3. **Strategic intent — WHY they scaled.** Read sitemap `<lastmod>` dates: were the matrix/long-tail pages
   **mass-generated on a single day** (programmatic scaling event) vs. grown organically? Map each invested
   attribute (matrix, neighborhoods, schema/llms.txt, voice agent, multi-GBP, certs, pricing) to the
   **lead-generation lever** it serves. Answer: why scale, why these attributes, how recent (window size).
4. **Money mechanics (the close-rate levers).** Grep payloads for: **financing** (Synchrony, Wisetack,
   Hearth, GreenSky, Sunbit, Affirm), **sticky/fixed-bottom mobile CTA**, click-to-call density (`tel:`),
   **form friction** (count `<form>` + fields — minimal = good), call-tracking (CallRail/CTM). These are
   what turn traffic into booked calls and are easy to miss.

**Pass-5 questions:** What's the design token set (copyable)? What does it actually LOOK like (need
screenshots)? Was the page count a single-day mass-generation event (when)? Why those attributes — which
lever does each serve? What close-rate levers (financing, sticky mobile CTA, low-friction booking) are
present? Are we copying both ends of the funnel (pages + conversion), not just the pages?

**Screenshots — automate, don't hand-capture.** Use `scripts/capture_screenshots.mjs` (Playwright host
script: `node capture_screenshots.mjs <domain> <out-dir> [urls.txt]`). It captures every tier, desktop +
mobile, fold + full-page, into a **dated** folder. Run on the host/CI (the Cowork sandbox can't finish
Chromium's ~185MB download in its short command window). If Claude-in-Chrome is connected, it can also
capture live in-session — check `list_connected_browsers` first. Never block the teardown on manual
screenshots; capture the tokens from CSS now, queue the visual-composition pass when shots land.

---

## PASS 6 — Blog deep-analysis (for the reusable blog engine)

If the site has a blog, tear it down too — not for the current client, but to build the **blog engine for
all future clients.** Sample ≥6 posts across topic types (comparison/decision, symptom/emergency,
code-explainer, seasonal, buyer-stage, positioning). Decode each. Capture:
- **Writing style/voice** — authoritative + calm + specific? non-alarmist? (AJ Long: "Do not panic —
  millions of homes have it.") Quote real examples.
- **Structure** — intro → why it matters → context → identify → code → options+prices → local/insurance
  angle → action steps → soft CTA → authoritative sources → FAQ schema.
- **Depth signals** — code citations (NEC §), real price ranges, authority links (CPSC/NFPA/ESFI), local
  specificity, word count.
- **Topic engineering** — geo-tagged? seasonal? county-data? decision-stage? Map the topic taxonomy.
- **Internal linking** — does the post funnel informational traffic to service/city pages?
- **What actually worked** — cross-reference DataForSEO: which posts rank, for what, at what position.
  (AJ Long lesson: the blog is *excellent* but ranks page-2 — great content ≠ position without authority.
  So the model is worth copying; the position lesson is "content alone isn't enough.")

Output: a `blog-analysis` section + a reusable "what good blog content looks like" spec for the engine.

---

## Indexing & publishing lesson (answer the "200/day" question)

A recurring question: *if indexing is limited to ~200/day, why publish 1,000 pages at once?* Because the
two are different. **Sitemap publishing has NO per-URL limit** — you list every URL; Google discovers and
crawls on its own schedule (days→months for large sets; this is the indexation lag we measure). The
**~200/day cap is on manual/API priority-indexing requests** (Google Indexing API quota; GSC "Request
Indexing" is even lower). So the winning play, and what to build into the pipeline: **mass-publish the full
matrix via split sitemaps (no limit) + GSC sitemap submission, then selectively ACCELERATE the highest-value
money pages via the Indexing API (~200/day) / Bing IndexNow (up to 10k/day) + strong internal links.** Don't
expect launch-day rankings; do prioritize which pages get the scarce fast-track requests.

---

## Change tracking (before/after — every teardown is a baseline)

Every teardown is also a dated snapshot. Structure the folder so re-runs diff cleanly:
- `raw/sitemaps/`, `raw/payloads/`, `raw/screenshots/<YYYY-MM-DD>/` — dated where it changes.
- On a competitor-watch alert (e.g. HeyTony "site changed"), **re-run the relevant passes**, save into a
  new dated capture, and write a `changes-<YYYY-MM-DD>.md` diffing: page count, new/removed page types,
  schema, tech, CTAs, pricing, design. Then run the **CHANGE block of `references/questions-bank.md`** to
  reverse *why* they changed it and what they're betting on. This turns the watchdog alerts into a
  compounding intelligence timeline per competitor, not one-off snapshots. Use this same folder/organization
  for **every** site we tear down.

---

## Quality gates (MANDATORY — like every vault tool)

Every output of this skill is gated before it's considered done. Optimization to "best we can get," not
"good enough," is the standard.
1. **`gate-peer-reviewer`** — gate each major artifact (the teardown dossier, the blueprint, the blog spec)
   at its produce-step: disk-verify claims against the retained raw, check no placeholder/assumption text,
   confirm every "tell" was checked (present/absent), confirm the DataForSEO + conversion + visual layers
   are covered. Address findings before proceeding.
2. **`house-voice-rewrite` Mode 2 (conditional — client-facing artifacts)** — when the operator indicates
   the teardown dossier or blueprint will be shared with a client, invoke `house-voice-rewrite` Mode 2 on
   those artifacts before the `output-quality-loop` step. Use the client personality file at
   `second-brain/04_projects/clients/_active/<client-slug>/_state/personality-<client-slug>.md`. If no
   personality file exists for the client, skip the rewrite and note in the closing report:
   "House-voice rewrite skipped — no personality file found at `…/<client-slug>/…`."
3. **`output-quality-loop` (EVALUATE mode)** — closing: run on the teardown + blueprint (+ blog spec). On
   PASS, done. On NEEDS REVISION/FAIL, ingest the revision prompt, regenerate, re-run. Cap 3 iterations;
   escalate on the 3rd FAIL.
Emit the standard auto-invoke block at closing (see `output-quality-loop` convention).

---

## Deliverables (every run)

1. **Retained raw** — `raw/` (all sitemaps, representative + all-entity payloads, robots.txt, llms.txt),
   `extracted/` (decoded content + schema), `data/` (inventories, matrix + gap grid, research seed,
   DataForSEO pulls). Plus `extract.py`.
2. **Teardown dossier** — `teardown-YYYY-MM-DD-full-build-analysis.md`: the page-tier taxonomy, per-template
   anatomy, data-fusion layer, language, schema architecture, internal linking, **full tech/tools stack
   table**, service taxonomy, **DataForSEO reality-check** (what ranks + history), **conversion/UX system**,
   quality tells/inconsistencies, what-changed-vs-prior, and a dedicated **"reverse-engineered machine"
   synthesis** section that explains how all the pieces compound into the site's competitive advantage
   (canonical: §10 — one page showing structure + data + schema + conversion + authority as a system).
3. **Reproduction blueprint** — the 5-object data model (+ population/ZIP), tiered templates, build/render
   layer, research fan-out, the math to ~N pages, the **conversion + authority layer**, the migration
   redirect playbook, and a phased program decomposition mapping to existing tools.
4. **Non-destructive dossier/synthesis updates** if a prior competitor brief exists.
5. **Folder `_README.md`** + parent update.
6. **Closing:** if client-facing, `house-voice-rewrite` Mode 2 on the dossier + blueprint; then auto-invoke
   `output-quality-loop` on the teardown + blueprint; event-log row; git staged by name (no push).

## The "tells" catalog — concrete things to look for (from the canonical run)

Codified so future runs don't miss them. Look for each; note present/absent:

- **Next.js RSC** (`self.__next_f`) → full content recoverable from HTML without a browser.
- **Sitemap index** split by type → count every nested sitemap.
- **Service×city matrix** (`/services/<svc>/<city>`) → the page-count engine; compute the gap grid.
- **Per-entity research data layer** fused into templates (permit authority, utility, code dates,
  neighborhoods, housing era, brand prevalence, year-stamped price, population, ZIPs).
- **Craft ladder** — premium money pages vs slot-filled long-tail.
- **Comprehensive JSON-LD graph** incl. `FAQPage`, `Offer`/`PriceSpecification`, `AggregateRating`,
  `BreadcrumbList`, `HowTo`, **`SpeakableSpecification`** (voice/AI-answer bet).
- **AI-crawler allow-list in robots.txt + `llms.txt`** → answer-engine optimization.
- **Tool stack:** Next.js+Turbopack+Tailwind+ISR · Netlify/Vercel · HousecallPro (booking) · GTM/GA4 ·
  ElevenLabs+GPT voice agent · Next.js Image (WebP/AVIF) · self-hosted fonts.
- **Multi-GBP** local strategy + manufacturer certs as trust+keyword surfaces.
- **Conversion sidebar** (Need-Help-Now / Request-Quote / Service-Area-Info / Other-Services) + **symptom
  checklists** + **4 capture paths** + **24/7 voice booking**.
- **Recent rebuild?** → old URLs **301/308-redirect** to new (migration playbook) + **indexation lag** (new
  pages not ranking yet) + **breadth-vs-position** gap in the history.
- **Single-day mass-generation** → sitemap `<lastmod>` shows hundreds of pages built on one date = a
  deliberate programmatic scaling event (the machine in action); blog grown organically = predates it.
- **Design tokens** → dark theme + bold brand-color CTAs, Tailwind vN tokens, self-hosted font, pulse/glow
  motion on live/CTA elements. (Visual *composition* needs screenshots — name that gap.)
- **Money/close-rate levers** → financing (Synchrony/Wisetack/etc.), **sticky mobile CTA bar**, click-to-call
  everywhere, minimal forms (route to booking, not forms).
- **Both ends of the funnel** → pages (top: get found) + conversion/authority (bottom: financing, sticky CTA,
  voice booking, multi-GBP, reviews). Copying only the pages gets traffic without bookings.

## Working principles

1. **Multi-pass, always.** The biggest findings come in passes 3–4. Don't stop at structure.
2. **Retain everything; summarize nothing away.** Raw HTML + decoded text + data files all stay.
3. **Free/fetch tools first, then cheap DataForSEO.** Sitemaps/payloads/robots/llms are free. DataForSEO
   ranked_keywords + historical (~$0.03) are the cheapest highest-value confirmations — always run them in
   Pass 3 if Labs is live. Don't assume Backlinks is subscribed.
4. **Confirm what RANKS, not just what's built.** Page count is a leading indicator; rankings + history are
   the truth. Always ask "new URLs or old?" and "breadth vs position?".
5. **Conversion is half the answer.** A teardown that omits the CTA/funnel/booking layer can't explain how
   the site makes money. Always run Pass 4.
6. **Be honest about gaps.** Name what you couldn't capture (e.g. CWV behind a quota, Wayback offline) and
   itemize it for a follow-up — don't fake it.
7. **Plain language.** Gloss SEO/tech jargon inline (per the plain-language conventions).
8. **Every teardown feeds the build.** This is the research front-end of the website-factory program — the
   blueprint must be concrete enough to PROVISION into build phases.

## Reference files & scripts

- `references/teardown-checklist.md` — the per-pass concrete checklist (copy into the run's task list).
- `references/questions-bank.md` — the "why did they do that?" psychology/strategy questions to run on every
  page, dataset, and before/after change. Add good new questions as they arise.
- `scripts/extract_nextjs.py` — multi-path content decoder: Next.js RSC (App Router), `__NEXT_DATA__`
  (Pages Router), and HTML fallback (WordPress, Hugo, any non-Next.js site). Auto-detects framework.
  JSON-LD extraction works on all paths.
- `scripts/capture_screenshots.mjs` — Playwright host script for automated tier screenshots (desktop+mobile,
  fold+full, dated folders for before/after). Run on host/CI, not the sandbox. **Requires:**
  `npm install playwright` + `npx playwright install chromium` on the host machine.
- `references/tells-catalog.md` — expanded per-pass catalog of concrete things to look for.
- `references/dataforseo-endpoints.md` — exact API calls, parameters, costs, and fallbacks.
- `references/teardown-dossier-template.md` — copy this section structure when starting a new run.
- `references/questions-bank.md` — psychology/strategy probes to run on every page and dataset.
- Worked example: the AJ Long teardown folder (path at top) — the canonical finished output.
- Second-target validation: Root Electric (rootelectric.com) — WordPress/Thrive, 159 content pages,
  Rank Math SEO, llms.txt present. Validated generalization beyond Next.js.

## Registration

This skill is registered by **convention**: the presence of `SKILL.md` at
`~/workspace/skills/seo-site-teardown/` makes it loadable by any Claude Code session or Cowork
chat. There is no separate "Settings > Capabilities" registration step — skills are discovered
by the SKILL.md convention. The toolkit-reuse-map at
`second-brain/05_shared-intelligence/tools/_toolkit-reuse-map.md` tracks the version and
reusability classification.

## Composition

- `competitor-deep-research` — run first for the landscape (who ranks); then this skill on the one site to
  out-build.
- `output-quality-loop` — closing eval on the teardown + blueprint.
- The **website-factory program** consumes the blueprint; `vault-orchestrator` PROVISIONs the build phases;
  `scaffold-core-30-page.py` + `insert-internal-links.py` generate pages; `gate-peer-reviewer` reviews.
