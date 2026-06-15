---
type: skill
name: custom-html-build
version: 0.9.0
status: draft
created: 2026-06-12
updated: 2026-06-12
author: wf4-ev-nextjs-build-202606121800
instance-1: ev-electric-services (WF-4, in-flight)
tags: [skill, build, nextjs, website-factory, tailwind]
---

# Skill: Custom HTML Build (Next.js + Tailwind)

**Purpose:** Build a custom Next.js site from a single-sourced data layer + design system + AJ-Long-benchmarked teardown. Produces a staged, non-live site with schema, internal links, and render verification — ready for a gated cutover.

**Status:** v0.9.0 — all steps (1-7) validated through staging on EV Electric ([WF-4]). v1.0 promotion gated on S&H second-client from-config-alone proof ([WF-12]). 7 key decisions, 6 gotchas.

**Changelog:**
- v0.9.0 (2026-06-13): Steps 1-7 validated through staging. Step 4 (data layer) fully documented with architecture + token catalog + script links. Step 5 (design) consumed WF-3 v1.0. Step 6 (templates) filled with full 4-tier table + 13-section leaf breakdown. Step 7 (verification) filled with complete results + honest limits. 7 key decisions, 6 gotchas. References/ populated with merged-data-shape-sample.json.
- v0.1.0 (2026-06-12): Initial draft. Steps 1-3 scaffolded with EV instance data.

---

## Steps (validated during EV build)

### Step 1: Project Scaffold
- Initialize Next.js 15+ App Router with Tailwind CSS v4
- Static export (`output: "export"`) for Netlify compatibility without serverless
- `trailingSlash: true` to match WordPress URL convention
- Inter font (matches AJ Long benchmark)
- **Do NOT fork the data layer** — import existing JSON files by path from the shared data repo

**Instance 1 (EV):** Next.js 16.2.9 + React 19.2.4 + Tailwind v4. Scaffolded at `repos/ev-electric-services/`. Build produces 44 static pages (41 real + _not-found + infrastructure). Validated 2026-06-12.

### Step 2: Route Structure from Slug Map
- Dynamic `[slug]` route for service hubs + service×city leaf pages
- Explicit routes for core pages (/, /about/, /contact/, /services/, /service-areas/)
- `generateStaticParams()` driven by the live sitemap inventory (not theoretical matrix)
- Build-time validation: generated routes must exactly match the 41-URL inventory

**Instance 1 (EV):** 36 dynamic slugs (6 hubs + 30 leaves) + 5 explicit routes = 41 total. Route validation PASS.

### Step 3: Netlify Staging Deploy
- Static export to `out/` directory
- `netlify.toml` with `publish = "out"`
- Deploy to auto-generated staging subdomain (NOT the live domain)
- Verify HTTP 200 on home + sample leaf page

**Instance 1 (EV):** Deployed to `iridescent-sorbet-6f7d6a.netlify.app`. HTTP 200 confirmed on home and leaf pages. Q-02 (stack combo unproven) resolved: Next.js 16.2.9 + Tailwind v4 + Netlify returns 200.

### Step 4: Data Layer Consumption (Phase B — exercised)

**Architecture:** Client-scoped overlay pattern (same as cities). Three-layer merge at load time:
```
shared base (data/services/<service>.json)
  + client overlay (data/services/<client-slug>/<service>.json)
  + city data (data/cities/<city>.json + data/cities/<client-slug>/<city>.json)
  + client config (data/client-<client-slug>.json)
  → token-substituted rendered content
```

**Data loaders (to implement in the Next.js project):**
- `loadServiceData(serviceSlug, clientSlug)` — reads base JSON, merges client overlay if exists (overlay fields win)
- `loadCityData(citySlug, clientSlug)` — reads base city JSON, merges client overlay if exists
- `loadClientConfig(clientSlug)` — reads client config JSON
- `substituteTokens(text, context)` — replaces `{city_name}`, `{county}`, `{utility_provider}`, `{owner_name}`, etc. from the merged context

**Token catalog** (used in service overlays):
- `{city_name}`, `{city_name_with_state}`, `{county}` — from city JSON
- `{utility_provider}` — from city JSON (added Phase B; e.g., "Dominion Energy", "PEPCO")
- `{owner_name}`, `{owner_first_name}`, `{license_state}`, `{license_issuer}` — from client config
- `{client_name}`, `{review_count_phrase}`, `{review_pitch}` — from client config
- `{phone_display}`, `{phone_tel}`, `{final_cta_response_promise}` — from client config

**Data shape reference:** See `skills/custom-html-build/references/merged-data-shape-sample.json` for a complete example of what the merge produces for one page.

**Scripts:**
- Route validator: `repos/ev-electric-services/scripts/validate-routes.ts` (parameterized — reads slug-map + sitemap inventory)
- Backfill harvest: see `[[pattern-migration-live-to-data-layer-harvest]]` (manual process, to be scripted at [WF-12])

**Instance 1 (EV):** 4 client overlays written (panel-upgrade, ev-charger, light-fixture, smoke-alarm). 2 services already complete in base (troubleshooting, outlet-installation). Reconstruction verified: Vienna = Dominion Energy / Fairfax County, Rockville = PEPCO / Montgomery County. 10/10 full specificity.

### Step 5: Design System (TODO — Phase B3)
- Consume [WF-3] website-design skill v1.0 (shipped pass 168) for component patterns
- Brand tokens from client config (primary blue #0871bc, navy #123075, accent yellow #f5b400)
- Component library: Header, Footer, Hero, ServiceCard, CTABar, etc.
- Mobile-first responsive
- AJ Long benchmark: sticky sidebar conversion, symptom checklists, minimal forms
- Note where [WF-3] drove decisions vs. where diverged

### Step 6: Page Templates (Phase C — exercised)

**4 tiers, all rendering from the data layer:**

| Tier | Template | Route | Sections | Pages |
|---|---|---|---|---|
| Core static | `app/page.tsx`, `about/page.tsx`, `contact/page.tsx` | Explicit routes | Hero + services grid + areas + CTA | 3 |
| Core index | `services/page.tsx`, `service-areas/page.tsx` | Explicit routes | Service cards / service×city matrix | 2 |
| Service hub | `[slug]/page.tsx` → `HubPage.tsx` | Dynamic | Hero + what-it-means + city grid + CTA | 6 |
| Service×city leaf | `[slug]/page.tsx` → `LeafPage.tsx` | Dynamic | 12 sections (see below) | 30 |

**Leaf page template sections (LeafPage.tsx):**
1. Breadcrumb (Home → Hub → This page)
2. Hero (eyebrow + H1 + subheading + dual CTA + review proof)
3. What it means (3 paragraphs)
4. Quick reference (6 symptom/situation cards)
5. Housing patterns (3 era-based cards with neighborhoods + symptoms)
6. Specific scenarios (7-8 problem cards)
7. Process steps (5-6 numbered steps)
8. Pricing (intro + bullet items + closing note)
9. About owner (3 paragraphs with review count)
10. Neighborhoods (city-specific list from city JSON)
11. Related services (filtered to pages that exist — non-existent service links dropped)
12. FAQ (8 questions with accordion)
13. Final CTA (heading + paragraph + dual buttons)

**Key implementation details:**
- `data-loader.ts`: three-layer merge (base + overlay + city) with `subAll` token substitution
- `page-resolver.ts`: resolves URL slug → service data slug + city slug from live sitemap inventory
- `{city_slug}` token added to context for related-card `href_slug` resolution
- Related cards filtered against `getAllDynamicSlugs()` — links to non-existent services (whole-house-rewire, generator-installation) silently dropped instead of generating broken links
- Hub pages substitute owner/client tokens but leave city tokens empty (hub is city-agnostic)

**Instance 1 (EV):** 41 pages rendered. Route validation 41/41 PASS. Link integrity PASS (17 links on sample page, 0 broken). Full specificity confirmed: Vienna=Dominion Energy/Fairfax County (14/10 occurrences), Rockville=PEPCO/Montgomery County (18/12). Schema wired for Phase D (SchemaJsonLd component present, not populated yet).

### Step 7: Render Verification (Phase E — exercised)

**Full render sweep:**
- All 41 routes return HTTP 200 on staging (node https.get sweep, not spot-check)
- Build produces 44 static pages (41 real + _not-found + infrastructure), zero errors
- Route validation: 41/41 PASS (generated routes ↔ live sitemap inventory)
- Link integrity: 17 internal links on sample page, 0 broken

**Full-page token + FILL sweep (PERMANENT STANDING CHECK — added from quality audit):**
```bash
# Must return 0 for both before any staging deploy or parity claim
grep -roh '{[a-z_]\+}' out/ --include="*.html" | grep -v '{}' | wc -l  # → 0
grep -rl "FILL" out/ --include="*.html" | wc -l                         # → 0
```
This catches unresolved `{tokens}` and leaked FILL placeholders across ALL rendered HTML — body, meta tags, and RSC payload. Run AFTER every build, BEFORE every deploy. A non-zero result means a token mapping is missing from `buildTokenContext` or a FILL field wasn't overridden in the client overlay.

**Why this is a standing check (not optional):** Issues 1 + 2 from the quality audit — 7 unresolved token types and 16 pages with FILL meta descriptions shipped to staging and passed section-level parity reviews. Only a full-page grep caught them. Section-level checks (headings, body text, schema values) are necessary but not sufficient.

**Lighthouse-equivalent audit (local — PSI API quota exceeded, numeric scores deferred to operator Chrome DevTools run):**
- SEO: all critical elements present (title, meta desc, h1, schema, lang, viewport, heading hierarchy)
- Accessibility: all landmarks present (nav with aria-label, main, footer), 0 images without alt, valid heading hierarchy
- Performance: static HTML (99KB leaf, 25KB home), self-hosted Inter font (preloaded woff2), single Tailwind stylesheet, no render-blocking JS, no images yet
- Best Practices: HTTPS, no mixed content, valid doctype
- **Honest limit:** numeric Lighthouse scores not produced — operator must run Chrome DevTools Lighthouse on `ev-electric-staging.netlify.app` for the numbers. Architecture guarantees 90+ but the assertion is unproven until run.

**Schema validation:**
- 2 JSON-LD blocks per leaf page (BreadcrumbList/Organization/WebPage/WebSite + LocalBusiness/Service/FAQPage)
- Value-level diff vs live: all ranking-significant fields IDENTICAL (LocalBusiness name/address/phone, AggregateRating 5.0/148, Service name, FAQ questions, Breadcrumb items)
- 2 acceptable differences: Organization.description truncated at first period (design choice, not bug — full description is on LocalBusiness), WebPage.datePublished/Modified omitted (unavailable at static-export build time)
- MD page (Rockville): correctly resolves PEPCO/Montgomery County, zero VA bleed
- **Rich Results Test: deferred to operator** (requires browser-based tool). JSON-LD structure is valid JSON, both blocks have @context, peer reviewer confirmed valid nesting.

**Hardcode scan (reuse gate):**
- `grep` across `src/` and `scripts/` for client-specific values: CLEAN
- Only client identifier is `CLIENT_SLUG` in `src/lib/config.ts` — the single config point
- 3 CSS/JSX comments reference the project by name (design reasoning) — acceptable, not rendered

**Mobile render check:**
- Sticky mobile CTA bar (`StickyMobileCTA.tsx`): `fixed bottom-0`, visible below `md:` breakpoint, call + quote buttons
- Header nav collapses on mobile (links hidden below `md:`)
- Hero gradient renders full-width on narrow viewports
- **Honest limit:** visual verification deferred to operator (I can confirm the CSS/responsive classes are correct; I cannot render and inspect a viewport)

**Operator review items:**
- Home page: new design (WP home was Elementor), highest-impression page, no parity baseline → flagged for Oliver's visual review
- Numeric Lighthouse scores: run from Chrome DevTools
- Rich Results Test: run from `search.google.com/test/rich-results`
- Mobile rendering: inspect from Chrome DevTools mobile view

**Instance 1 (EV):** 41/41 pages, all 200, schema value-level PASS, hardcode scan CLEAN, link integrity PASS. Staging at `ev-electric-staging.netlify.app` (noindexed). Live site untouched.

---

## Key Decisions (captured during build)

1. **Static export over serverless** — all 41 pages are SSG; no runtime needed. Eliminates Netlify auth/function requirements for staging. Can switch to ISR later for freshness. Decision doc: `repos/ev-electric-services/.kos/execution-logs/execution-log-2026-06-12-static-export-decision.md`.
2. **Serverless should be a positive decision, not a default.** Any client marketing site with fully static content should default to static export. The decision to use serverless (ISR, API routes, runtime data) must be a positive choice with a named reason — not just "Next.js defaults to it." Revisit at scale-out ([WF-11]) where build time or content freshness may justify the switch.
3. **Slug map is first-class** — data file names ≠ URL slugs. Route generation consumes `slug-map.json`, never raw filenames.
4. **Live sitemap inventory drives route generation** — the exact 30 leaf URLs from the sitemap, not a theoretical 6×13 matrix. Some service×city combos don't exist as pages yet.
5. **Schema is preserve + enhance** (corrected: live pages DO have LocalBusiness/Service/FAQPage/AggregateRating from the Core-30 scaffolder, in addition to BreadcrumbList/Organization/WebPage/WebSite from AIOSEO). Phase D preserves all existing schema and adds SpeakableSpecification/HowTo.
6. **Staging must be noindexed from first deploy.** Both `X-Robots-Tag: noindex, nofollow` header (netlify.toml) and `robots.txt Disallow: /` (public/). Removal is an explicit cutover-runbook step with post-cutover verification (see WF-5 Step 8). Staging-noindex-left-on-at-launch is a classic migration killer.

## Dependencies
- `[WF-5]` wordpress-to-custom-html (extraction feeds this build)
- `[WF-7]` data-model spec (schema definitions)
- `[WF-3]` website-design (design system)
- `[WF-2]` site-capture-engine (AJ Long benchmark)

## Composes With
- `[WF-5]` extraction → `[WF-6]` build → parity verification → cutover

---

## Gotchas / Failure Modes (captured during EV build)

### G-1: Anonymous Netlify deploy fails on serverless functions
**Symptom:** `npx netlify deploy --allow-anonymous` errors with "serverless functions require authentication" even when deploying `--dir=out`.
**Root cause:** `@netlify/plugin-nextjs` (or a prior build's `.netlify/` cache) bundles Next.js server routes as Netlify Functions. Anonymous deploys can't deploy functions.
**Fix:** (a) Use `output: "export"` for static sites — eliminates functions entirely. (b) Remove `@netlify/plugin-nextjs` if not needed. (c) Authenticate first (`npx netlify login`) if serverless IS needed.
**Instance:** EV Phase A, first deploy attempt.

### G-2: `.netlify/` state directory poisons deploy retries
**Symptom:** After switching from serverless to static export, `netlify deploy --dir=out` still tries to bundle functions from the cached `.netlify/` directory. Deploy fails with the same auth error even though the code no longer has functions.
**Root cause:** `.netlify/` caches the prior build's function bundles and deploy state. It doesn't auto-clean when the build mode changes.
**Fix:** `rm -rf .netlify` before retrying after any build-mode change (serverless → static, or different site link).
**Instance:** EV Phase A, second deploy attempt.

### G-3: `netlify` vs `npx netlify` — PATH gotcha
**Symptom:** Operator runs `! netlify login` → `command not found: netlify`.
**Root cause:** Netlify CLI is installed as a project devDependency or via npx, not globally. Bare `netlify` isn't on PATH.
**Fix:** Always use `npx netlify <command>`. Document this in any SOP that asks the operator to run Netlify commands.
**Instance:** EV Phase A, operator auth step.

### G-4: `sites:create` doesn't auto-link the repo
**Symptom:** `npx netlify sites:create --name foo` creates the site but the repo stays linked to a previously-linked site (visible in `.netlify/state.json`).
**Root cause:** `sites:create` and `link` are separate operations. Creating a site doesn't re-link the repo.
**Fix:** After `sites:create`, run `npx netlify unlink` then `npx netlify link --id <new-site-id>`.
**Instance:** EV Phase A, new site was created but repo still pointed at anonymous drop site.

### G-5: `create-next-app` refuses to scaffold into a non-empty directory
**Symptom:** `npx create-next-app . --typescript --tailwind` errors listing existing files (`.kos/`, `data/`).
**Root cause:** Scaffold command checks for any existing files and refuses to overwrite.
**Fix:** Scaffold in a temp directory, then copy config + src files into the real repo. Or scaffold first, then add non-conflicting directories.
**Instance:** EV Phase A, `repos/ev-electric-services/` already had `.kos/` and `data/`.

### G-6: Staging site indexable by default — no noindex protection
**Symptom:** Deployed staging site has no robots.txt (404), no `<meta name="robots">`, no `X-Robots-Tag` header. Search engines can index it, creating a crawlable duplicate of the live site's URL structure during the ranking stabilization window.
**Root cause:** Neither Next.js nor Netlify add noindex by default. It must be explicit.
**Fix:** Add BOTH (a) `X-Robots-Tag: noindex, nofollow` via `netlify.toml [[headers]]` and (b) `public/robots.txt` with `Disallow: /`. Removal is a cutover-runbook step (WF-5 Step 8).
**Instance:** EV Phase A, C-09.

### G-7: Unresolved {tokens} pass section-level parity checks
**Symptom:** Rendered pages contain literal `{city_distance_phrase}`, `{county_short}`, `{license_state_full}`, `{response_promise}`, etc. as visible text. Section-level parity reviews (checking headings, body paragraphs, schema values) don't catch these because they focus on content meaning, not raw output.
**Root cause:** `buildTokenContext` didn't map all token types used in the service JSONs. 7 tokens had data sources in the city/client JSONs but weren't wired. Service-keyed tokens (`city_most_common_problem_paragraph`, `city_ev_neighborhood_phrase`) need the service slug passed as a parameter.
**Fix:** (a) Add ALL token types to `buildTokenContext` including the service-keyed ones. (b) Run the full-page token sweep (`grep -roh '{[a-z_]+}' out/`) after EVERY build. (c) Make the sweep a standing check in Step 7, not optional.
**Instance:** EV quality audit — 7 unresolved token types across ALL 41 leaf pages, caught only by grep, not by any review.

### G-8: FILL placeholders in base service JSONs leak through overlays
**Symptom:** Pages render "FILL: Meta description (≤155 chars)..." in the `<meta name="description">` tag — visible in search results.
**Root cause:** The EV overlay has authored body content but missed `aioseo_meta_description_template`. The base JSON's FILL placeholder passes through the overlay merge untouched. Also affected: `hero_subheading_template` (light-fixture, smoke-alarm), `why_city_closing_note_template` (smoke-alarm).
**Fix:** (a) The harvest SOP must explicitly list ALL fields that the base marks as FILL, not just body content. (b) Run the FILL sweep (`grep -rl "FILL" out/`) after every build. (c) Add `aioseo_meta_description_template`, `hero_subheading_template`, `why_city_closing_note_template` to the harvest field checklist.
**Instance:** EV quality audit — 16 of 41 pages had FILL in meta description; 5 had FILL in hero subheading / closing note. Fixed by adding the fields to overlays.

### G-9: HTML entities in data JSONs double-encode in React
**Symptom:** Rendered text shows literal `&amp;` where `&` should appear (e.g., "W&amp;OD trail" instead of "W&OD trail"). Affects housing-pattern titles, neighborhood blurbs, and any text with ampersands.
**Root cause:** City/service JSONs were authored for WordPress HTML injection and stored `&amp;` (HTML entity). React JSX auto-escapes text content, turning the already-encoded `&amp;` into `&amp;amp;` (double-encoded).
**Fix:** Store plain `&` in JSON data files, not HTML entities. The data layer serves a React app, not WordPress. Run `sed -i 's/&amp;/\&/g'` on all city + service JSONs. Added `decodeHTMLEntities` + `decodeAllStrings` to data-loader as defense-in-depth.
**Instance:** EV QA3 — 22 city JSONs + 7 service JSONs had `&amp;` entities. 11 pages showed double-encoded text. Fixed by replacing entities in source data.

### G-10: Slug-map alias needed when data slug differs from sitemap service key
**Symptom:** Breadcrumb links to `/ev-charger/` (404) instead of `/ev-charger-installation/` (the real hub page).
**Root cause:** The sitemap inventory uses the `slug` field inside the JSON file (`ev-charger`) as the service key. The slug-map was keyed only by the filename (`ev-charger-installation`). When the page resolver looked up `ev-charger`, it found no entry and fell back to using the raw slug as the URL — producing a broken link.
**Fix:** Add an alias entry in the slug-map: `"ev-charger": { "data_slug": "ev-charger", "url_slug": "ev-charger-installation", ... }`. The slug-map must have entries for BOTH the filename-based key AND the internal-slug key when they differ.
**Instance:** EV QA3 — 5 ev-charger leaf pages had broken breadcrumb links. Fixed by adding the alias entry.
