---
type: skill
name: wordpress-to-custom-html
version: 0.9.0
status: draft
created: 2026-06-12
updated: 2026-06-12
author: wf4-ev-nextjs-build-202606121800
instance-1: ev-electric-services (WF-4, in-flight)
tags: [skill, migration, wordpress, nextjs, website-factory]
---

# Skill: WordPress → Custom HTML Migration

**Purpose:** Extract content, URLs, schema, and internal links from a live WordPress site, producing a migration-ready data package that a custom build (Next.js or other) can consume. Zero risk to the live site (read-only extraction). Produces a parity verification checklist for cutover safety.

**Status:** v0.9.0 — all steps (1-7) validated through staging on EV Electric ([WF-4]). Step 8 (cutover) documented but gated (~Aug). v1.0 promotion gated on S&H second-client from-config-alone proof ([WF-12]). 4 standing rules, 3 gotchas.

**Changelog:**
- v0.9.0 (2026-06-13): Steps 1-7 validated through staging. Steps 4b, 5, 6, 7 filled with instance data. 4 standing rules added (provenance, extraction scope, value-level diffs, conservative grading). 3 gotchas (whitespace-tolerant schema, slug mismatches, duplicate data files). Cutover runbook (Step 8) written. References/ populated with extraction-output-shape-sample.json.
- v0.1.0 (2026-06-12): Initial draft. Steps 1-4 scaffolded with EV instance data.

---

## Steps (validated during EV build)

### Step 1: Sitemap Crawl → URL Inventory
- Fetch `sitemap_index.xml` → identify page sitemaps vs non-page sitemaps (e.g., Elementor template sitemaps)
- Fetch the page sitemap → extract all URLs with `lastmod`
- Document exclusions with rationale (e.g., `elementskit_template-sitemap.xml` = Elementor internals)
- Output: `data/wp-extraction/live-sitemap-urls.json` with tier classification (core_static, core_index, service_hubs, service_city_leaves)
- **Validation:** URL count matches expectation; no duplicates

**Instance 1 (EV):** 41 URLs from `page-sitemap.xml`. `elementskit_template-sitemap.xml` excluded. Validated 2026-06-12.

### Step 2: Per-Page Content + Schema Extraction
- For each URL: fetch page, extract title, meta description, OG tags, canonical, H1, JSON-LD blocks, internal links, breadcrumb
- **Important:** WordPress sites may have MULTIPLE JSON-LD blocks (e.g., one from AIOSEO plugin, one injected by custom scaffolder into page content). Extract ALL blocks and tag their source.
- Output: `data/wp-extraction/pages/<slug>.json` per page

**Instance 1 (EV):** Sample extracted (electrical-troubleshooting-vienna-va). TWO JSON-LD blocks found: Block 1 = AIOSEO (BreadcrumbList/Organization/WebPage/WebSite), Block 2 = scaffolder-injected (LocalBusiness/Service/FAQPage with AggregateRating).

### Step 3: Slug Mapping (data slugs → URL slugs)
- Data layer file names often differ from live URL slugs (e.g., `troubleshooting.json` → `/electrical-troubleshooting/`)
- Build a first-class `data/slug-map.json` mapping data_slug → url_slug → leaf_template
- Document exclusions (test files, duplicate data files serving different clients, services without live pages)
- **Critical:** Route generation MUST consume the slug map, not raw data file names

**Instance 1 (EV):** 6 services mapped, 3 with slug mismatches. ev-charger.json vs ev-charger-installation.json resolved (different client variants). vienna-va-test.json excluded. emergency-electrician.json excluded (no live page).

### Step 4: Build-Time Route Validation
- Generate the route set from the slug map + sitemap inventory
- Compare against the extracted URL inventory
- FAIL the build if any live URL lacks a route (missing page at cutover) or any route lacks a live URL (new URL = ranking risk)
- Output: validation script at `scripts/validate-routes.ts`

**Instance 1 (EV):** 41/41 PASS — perfect URL parity.

### Step 4b: Live → Data Layer Harvest (FILL Backfill)
When the data layer has FILL placeholders where hand-authored content exists only on the live site, backfill the authored copy into client-scoped service overlays before Phase C rendering.

Full SOP: `[[pattern-migration-live-to-data-layer-harvest]]`

Key sequence:
1. Backup all data files to timestamped dir
2. Record baseline FILL counts
3. Confirm "N services, not M pages" model (cross-service comparison)
4. Harvest from the canonical page per service (WebFetch, read-only)
5. Parameterize all city-variable text as `{tokens}` — zero hardcoded city names
6. Write to client-scoped overlay (`data/services/<client-slug>/<service>.json`)
7. Verify: FILL count → 0, hardcoded-city grep → empty, sitemap lastmod unchanged

**Instance 1 (EV):** 4 services needed backfill (panel-upgrade: 31→0 FILLs, ev-charger: 23→0, light-fixture: 23→0, smoke-alarm: 23→0). 2 services already complete (troubleshooting: 0, outlet-installation: 0). Overlay dir: `data/services/ev-electric-services/`. Harvested from Vienna pages (canonical). Live site untouched (lastmod verified).

### Step 5: Internal Link Graph (Phase A — complete)
- Extracted outbound internal links from all 41 pages during Phase A extraction
- Built link graph: `data/wp-extraction/link-graph.json` (41 pages, 736 unique outbound links, 18 avg/page)
- Link integrity verified at build time: all internal links on rendered pages resolve to real routes (0 broken)
- Related-card links filtered against `getAllDynamicSlugs()` — links to non-existent services silently dropped

**Instance 1 (EV):** 736 links across 41 pages. Link integrity PASS (17 links on sample page, 0 broken).

### Step 6: Redirect Map + SEO Artifacts (Phase D — complete)
- **Redirect map:** `data/redirect-map.json` — first-class artifact. Currently empty (same-URL cutover = zero redirects). If URL changes arise during iteration, they land here. At cutover, generates Netlify `_redirects` file (not next.config.ts — incompatible with static export per C-07).
- **Split sitemaps:** `scripts/generate-sitemaps.ts` → `public/sitemap.xml` (index) + `sitemap-core.xml` (5 URLs) + `sitemap-hubs.xml` (6 URLs) + `sitemap-leaves.xml` (30 URLs). Parameterized — reads from slug-map + sitemap inventory.
- **llms.txt:** `public/llms.txt` — AI-crawler-friendly summary of the site (services, areas, contact, sitemap link). Day-one ship per AJ Long benchmark.
- **Production robots.txt:** `data/robots-production.txt` — allows all crawlers + explicit AI-crawler allow-list. NOT deployed during staging (staging robots.txt has `Disallow: /`). Swapped in at cutover per WF-5 Step 8.
- **Schema:** JSON-LD emitted on all leaf pages (2 blocks: BreadcrumbList/Organization/WebPage/WebSite + LocalBusiness/Service/FAQPage/AggregateRating). Value-level diff against live = IDENTICAL on all ranking-significant fields. AggregateRating emitted with review_count_source provenance (148 cross-platform, operator-confirmed).

**Instance 1 (EV):** 0 redirects needed (same URLs). 3 sitemaps (41 total URLs). llms.txt deployed. Schema value-level diff PASS.

### Step 7: Parity Verification Checklist (Phase E — exercised)

**What was verified:**
1. **Full render sweep:** all routes return 200 (node sweep, not spot-check) — 41/41 PASS
2. **Route validation:** generated routes ↔ live sitemap inventory — 41/41 PASS
3. **Link integrity:** internal links on rendered pages resolve to real routes — 0 broken
4. **Body parity (leaf):** rendered section list matches live (12 sections, headings aligned per C-16)
5. **Specificity:** Dominion Energy / Fairfax County in VA pages, PEPCO / Montgomery County in MD pages — PASS
6. **Schema value-level diff:** LocalBusiness, Service, FAQPage, AggregateRating field values IDENTICAL to live
7. **Hardcode scan:** zero client-specific values in src/ or scripts/ (only CLIENT_SLUG in config.ts)
8. **SEO elements:** title, meta desc, h1, JSON-LD, lang, viewport all present
9. **Accessibility landmarks:** nav (aria-label), main, footer all present

**What is deferred to operator:**
- Numeric Lighthouse scores (Chrome DevTools — PSI API quota exhausted)
- Rich Results Test (browser-based tool)
- Mobile visual rendering inspection (CSS classes correct, visual confirmation needed)
- Home page visual review (new design, no WP parity baseline)

**Instance 1 (EV):** All automated checks PASS. Operator checks deferred. Staging at `ev-electric-staging.netlify.app` (noindexed, live untouched).

### Step 8: Cutover Runbook (gated — do NOT execute until ranking gate met)
Pre-cutover:
- [ ] Verify 15+ pages ranking with observable impressions (the gate)
- [ ] Content-freeze the live WP site (no new content after this point)
- [ ] Final parity verification pass (Step 7) against the frozen state

Cutover:
- [ ] DNS cutover: evelectric.pro → Netlify
- [ ] **CRITICAL: Remove staging noindex** — delete the `X-Robots-Tag: noindex, nofollow` header from `netlify.toml` AND replace `public/robots.txt` with a production version (allow crawling, point to sitemap). Both were added at staging time (C-09) and MUST be removed at cutover or the production site will be invisible to search engines.
- [ ] Verify redirect-map covers any URL changes (expect zero for same-slug)
- [ ] Deploy with production robots.txt + no X-Robots-Tag header

Post-cutover verification:
- [ ] **Verify noindex is GONE:** `curl -sI https://evelectric.pro/ | grep -i x-robots` must return nothing. `curl -s https://evelectric.pro/robots.txt` must NOT contain `Disallow: /`.
- [ ] GSC: Request indexing of the home page
- [ ] GSC: Submit the sitemap
- [ ] Monitor GSC Coverage report for 2 weeks
- [ ] Spot-check 5 ranking pages in SERP: still appearing, correct URL

**Why this step exists (C-09):** Staging-noindex-left-on-at-launch is a classic migration killer. The staging site was correctly noindexed to prevent duplicate-content competition with the live WP site during the ranking stabilization window. Forgetting to remove it at cutover makes the production site invisible. This runbook step + post-cutover verification is the guard.

---

## Standing Rules (learned from EV instance)

### AggregateRating counts must carry documented provenance
Google's review-snippet policy restricts self-serving AggregateRating. Any `reviewCount` emitted in JSON-LD schema must have a `review_count_source` field in the client config documenting:
- The platform breakdown (e.g., "Google 83 + HireNimbus + others = 148")
- Who confirmed it and when (e.g., "operator-confirmed 2026-06-12")
- Whether the count is Google-only or cross-platform aggregate

**Why:** EV's config said 148 while GBP showed 83. Both are true (148 = cross-platform total). Without provenance, every future reviewer re-litigates the discrepancy. The client config is the single source of truth for review numbers; it must explain itself.

**Instance 1 (EV):** Resolved 2026-06-12 — `review_count_source` added to `client-ev-electric-services.json`.

### Extraction scope is URL/schema/link/meta — NOT body content
The WP extraction (Steps 1–4) captures metadata: page titles, meta descriptions, JSON-LD schema blocks, internal link graphs, breadcrumbs, and URL structure. It does NOT extract body copy (the 10–20KB of unique local content per page: symptom checklists, housing-pattern blocks, scenario sections, FAQ answers, pricing notes).

**Why this matters:** If the live pages were built from a single-sourced data layer (as with EV's Core-30 scaffolder), the body is already in the data files — extracting it from the rendered HTML would be re-deriving what already exists. The data layer is the body-parity source, not the extraction. The extraction's job is to capture everything that ISN'T in the data layer: URLs, schema structure, link topology, and meta tags.

**How to apply:** When building Phase E parity verification, the body comparison reconstructs pages from the data layer and diffs against the live rendered body. It does NOT compare extraction JSON against the live page (the extraction never held the body). Scope the extraction checklist and any parity-pass labels accordingly — "metadata parity" is not "content parity."

**Instance 1 (EV):** C-10 — extraction parity table incorrectly labeled "all content fields match — PASS" when only meta/schema/links were compared. Corrected: extraction covers metadata parity; body parity requires a separate data-layer reconstruction diff.

### Parity verification diffs VALUES, not presence-flags or counts
Schema parity means the emitted JSON-LD values match (business name, address, FAQ question text, rating numbers), not just that both pages have `has_local_business: true`. Body parity means the rendered text matches section-by-section, not that both pages have an H1. Link parity means every outbound link target and anchor text matches, not just that both pages have "19 links."

**Why:** Presence-flag verification catches missing schema types or dropped sections. It cannot catch wrong values (a stale review count, a swapped city name, a missing FAQ question). Value-level diffing is the only verification that catches substitution errors — the class that actually breaks rankings and user trust.

**How to apply:** Every parity check in Step 7 must operate at the value level:
- Schema: parse both JSON-LD graphs, diff field-by-field (not type-count)
- Body: reconstruct from data layer, diff rendered text section-by-section against live
- Links: compare sorted `(href, text)` tuples, not counts
- Meta: compare exact title/description strings, not "both have a title"

**Instance 1 (EV):** C-11 — parity table reported "Schema @types 19 EXACT" (a count match, not a value comparison). Corrected as a standing rule.

### "Parameterized" means tokenized-from-data, not stripped-to-generic
When parameterizing harvested content, every specific term on the live page (utility name, county name, neighborhood name) must be replaced with a **data-layer token** (`{utility_provider}`, `{county}`, etc.), NOT with a generic fallback ("the utility", "the county"). Stripping to generic is a content-parity regression — the live page is more specific, and specificity is an SEO + local-trust signal.

**Why:** A hardcode-grep returning CLEAN is necessary but not sufficient. The grep and the parity regression can be the same edit seen from opposite sides: removing "Dominion Energy" passes the hardcode-grep AND loses specificity. Both checks must run together.

**How to apply:** Pair two checks on every overlay:
1. **Hardcode-grep** — `grep -rinE "<city-names>|<utility-names>"` excluding metadata lines. Must return empty. (Prevents hardcoded values.)
2. **Specificity-loss check** — for every term present on the live page but generic in the overlay (e.g., "Dominion Energy" → "the utility"), verify the term is available as a data-layer token. If it is, use the token. If it isn't, add the field to the data layer first, then tokenize. Never ship a generic where the live page has a specific.

**The rule:** If the live page says "Dominion Energy" and the data layer has a `utility_provider` field, the overlay must say `{utility_provider}`. If the data layer lacks the field, add it (to the city JSON or client config) before writing the overlay. The overlay is never less specific than the live page.

**Instance 1 (EV):** C-13 — 4 overlays shipped with "the utility" (7× in panel-upgrade, 1× in ev-charger) where live pages said "Dominion Energy." Fixed: added `utility_provider` to all 21 city JSONs (VA = Dominion Energy, MD/DC = PEPCO, Stafford = Dominion + NOVEC/REC note), then re-tokenized overlays to `{utility_provider}`. Reconstruction now produces "Dominion Energy" for Vienna and "PEPCO" for Rockville — 10/10 full specificity.

### Parity verdicts: grade conservatively — "EXACT" means identical, not close
When comparing rendered output against live pages, grade each field honestly:
- **IDENTICAL** — byte-for-byte match (headings, body text, link targets)
- **IMPROVED** — our version is better with a stated reason (added keyword, fixed grammar, more specific)
- **DIFFERS** — our version is different with a stated reason and a judgment (acceptable divergence vs. regression)
- **REGRESSION** — our version is worse (dropped keyword, lost specificity, removed content)

Never grade "EXACT" when the text differs. Never grade "minor refinement" when specificity decreased. A section heading that drops a keyword ("Specific panel scenarios" → "Specific situations") is a REGRESSION, not a refinement — headings are ranking signals. When in doubt, grade "DIFFERS" and state the difference so a reviewer can judge.

**Why:** C-10 (metadata-as-content labeled PASS), C-13 ("the utility" labeled "minor refinement"), C-16 (four heading drifts graded EXACT) — three optimistic self-grades in one build. The build content is consistently strong; it's the grading that runs hot. Conservative grading makes PASS verdicts trustworthy without a reviewer re-checking each field.

**Instance 1 (EV):** C-16 — four headings drifted from live (dropped "electrical", "panel scenarios", "home needs", singular→plural). Fixed by adding live-matching heading templates to the EV overlay. Standing rule added to prevent the class.

---

## Dependencies
- Live WP site must be accessible (read-only)
- Data layer files must exist (for slug mapping)
- `[WF-2]` site-capture-engine skill (competitor benchmark context)

## Composes With
- `[WF-6]` custom-html-build (consumes the extraction output)
- `[WF-3]` website-design (design system feeds the build)
- `[WF-2]` site-capture-engine (benchmark comparison)

---

## Gotchas / Failure Modes (captured during EV build)

### G-1: Schema greps must be whitespace-tolerant — multiple JSON-LD blocks per page
**Symptom:** A grep for `"LocalBusiness"` in a page's HTML returns no match, leading to the conclusion that the page has no LocalBusiness schema.
**Root cause:** WordPress pages can have MULTIPLE `<script type="application/ld+json">` blocks injected by different sources: (a) SEO plugin (AIOSEO, Yoast) emits minified JSON on one line; (b) custom scaffolder/theme injects pretty-printed JSON with newlines and indentation. A grep tuned to the minified format (e.g., `"@type":"LocalBusiness"` without spaces) misses the pretty-printed block (e.g., `"@type": "LocalBusiness"` with a space after the colon, on a separate line).
**Fix:** (a) Extract ALL `<script type="application/ld+json">` blocks and parse each as JSON — don't grep for type strings in raw HTML. (b) If grepping, use whitespace-tolerant patterns: `@type.*LocalBusiness` rather than exact-match. (c) Tag each extracted block by its likely source (plugin-generated vs content-injected) since they serve different purposes and may need different handling at migration.
**Instance:** EV Phase A. Peer reviewer grep missed the scaffolder-injected block (pretty-printed, Block 2 of 2) containing LocalBusiness + Service + FAQPage + AggregateRating. Led to incorrect C-04 claim that live pages had no LocalBusiness schema. Corrected after WebFetch extraction returned both blocks.

### G-2: Slug mismatches between data files and live URLs are the norm, not the exception
**Symptom:** Route generation uses data file slugs (`troubleshooting`, `smoke-alarm`) and produces URLs that don't match the live site (`/electrical-troubleshooting/`, `/smoke-alarm-installation/`). Silently changes URLs at cutover — the exact thing the migration must prevent.
**Root cause:** Data files are named for internal clarity; live URLs are optimized for SEO. The mapping is arbitrary and must be explicit.
**Fix:** Build a first-class `slug-map.json` (data_slug → url_slug → leaf_template) BEFORE any route generation. Route generation consumes the slug map, never raw filenames. Build-time validation compares generated routes against the extracted sitemap inventory and fails on any mismatch.
**Instance:** EV Phase A, C-05. 3 of 6 services had slug mismatches; hub-vs-leaf URL patterns also diverged for ev-charger.

### G-3: Duplicate data files serving different clients look like errors but aren't
**Symptom:** `ev-charger.json` and `ev-charger-installation.json` both exist in `services/` with the same service name ("EV Charger Installation"). Appears to be a duplicate.
**Root cause:** The shared data layer serves multiple clients. `ev-charger.json` is the EV Electric variant (matching EV's live URL slug `ev-charger-{city}`); `ev-charger-installation.json` is the S&H Contracting variant (matching S&H's slug `ev-charger-installation-{city}`). Both are canonical for their respective clients.
**Fix:** Document the duality in the slug map's `services_excluded` section. Never delete without operator approval. The slug map must make clear which file each client build uses.
**Instance:** EV Phase A, C-05.
