---
name: competitor-deep-research
version: 1.1
description: Deep competitive intelligence research on a client's direct competitors, producing structured per-competitor briefs AND a Tier-2 light scan AND a cross-competitor synthesis (with cross-competitor structural pattern table) that feeds page-build and SEO strategy. Use this skill whenever the user asks to research competitors, do a "competitive analysis," "competitive deep dive," "competitor landscape," "competitive intelligence," or "competitor audit" for a specific client — and any time the user names 2 or more competitors and wants them profiled side-by-side. Also use when the user mentions wanting to feed competitor findings into a Core 30 / page-build / SEO foundation strategy, or when they ask "who else is ranking for [keyword]" and wants more than a list. The 2026-06-03 v1.1 enhancements (Tier-2 light scan + per-page deep audit + cross-page top-5-trafficked-pages pattern detection) are default-on; they produce the "stalker-level" depth downstream service-research-engine and Phase 3a scaffolders consume. The skill writes per-competitor markdown briefs and a synthesis file into the client's vault folder under admin-extracts/competitor-research/.
---

# Competitor Deep Research (v1.1)

> **v1.1 changelog (2026-06-03)** — Three default-on enhancements per `handoff-2026-05-26-competitor-deep-research-enhancements`. (1) Combined Tier-1 deep-dive (4–5 competitors) + Tier-2 light scan (top 10 competitors) in one invocation — no separate modes; the synthesis carries both. (2) Per-page deep audit (Step 8) — structured 15-column stats row per audited page on every Tier-1 brief, captured into brief-template §3.5. (3) Cross-page pattern detection (Step 9) — top-5-trafficked-pages structural fingerprint per Tier-1 competitor at ≥80% page-share threshold, captured into brief-template §7.5 and rolled up into synthesis §4.5 across competitors. Phase numbering grew from 4 → 6 (Phase 2 Tier-2 light scan inserted, Phase 5 folder hygiene + Phase 6 closing). DataForSEO + free-toolkit paths documented side-by-side per enhancement. Brief template + synthesis template files updated in lockstep. Worked example: `synthesis-2026-06-03-enhanced.md` in the EV Electric vault folder, demonstrating the enhancements applied to the 2026-05-23 evidence base at $0.00 paid-API cost via the free-toolkit fallback. Deliberate evolution per `feedback_check_folder_structure_before_writing` discipline — the 2026-05-23 worked example is preserved untouched; v1.1 extends rather than replaces. Self-applying-spec lessons in `05_shared-intelligence/lessons/lesson-competitor-deep-research-v1.1-enhancements-2026-06-03.md`.

A reusable workflow for doing competitive intelligence on a client's direct competitors. Produces per-competitor briefs and a cross-competitor synthesis that grounds page-build and SEO strategy in real data, not assumptions.

This skill was distilled from the 2026-05-23 EV Electric Services Fairfax County competitive research session. The full case study lives at `~/workspace/second-brain/04_projects/clients/_active/ev-electric-services/admin-extracts/competitor-research/` — refer to it when something in this skill is unclear; the synthesis file there shows what a finished output looks like. The 2026-06-03 enhanced synthesis at the same path shows what the v1.1 default-on output looks like.

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
6. **Time budget.** Useful to know up-front. Typical budget for the **full enhanced run** (Tier-1 deep dives + Tier-2 light scan + per-page audit + top-5-pages pattern): 3–4 hours per Tier-1 primary, 60–90 minutes per Tier-1 secondary, 10–15 minutes per Tier-2 row, plus 60 minutes for synthesis. For a typical 2-primary + 2-secondary + 6-Tier-2 run that lands roughly **12–16 hours** end-to-end. Single-chat runs cap there cleanly; bigger fan-outs decompose via the vault-orchestrator (one sub-chat per Tier-1 competitor, parallel substrate). Without the enhancements, the legacy 2-primary + 2-secondary + synthesis budget was ~3 hours; the enhanced run is roughly 4–5× that for materially more thorough output.

7. **DataForSEO availability.** Confirm before starting. If the wrapper script (`~/workspace/second-brain-tier3/automation/scripts/dataforseo_query.py`) probes clean and the balance covers the spec'd queries (roughly $0.30–$0.50 for a full Tier-2 light scan + per-page audit using paid endpoints), use the **DataForSEO path** below. If the balance is short or operator wants to defer cost, use the **free-toolkit fallback** explicitly — every enhancement has both paths documented side-by-side. Don't silently mix; pick per-invocation and annotate the methodology section.

If any input is missing, ask the operator before researching. Bad inputs waste research budget.

---

## High-level workflow

The skill runs in five phases. Don't skip phases — each one feeds the next. **The Tier-2 light scan, per-page deep audit, and cross-page pattern detection are default-on as of the 2026-06-03 enhancements** — they are not optional modes. They produce the "stalker-level" depth the downstream service-research-engine and Phase 3a scaffolder consume.

1. **Identify the competitor list** — confirm the 4–5 Tier-1 competitors (operator-named primaries + secondaries from the live Google search) AND the broader Tier-2 set (top 10 organic + ranking-source competitors, including the Tier-1 set).
2. **Tier-2 light scan** — for the 10 Tier-2 competitors (which include the Tier-1 set), produce a structured row of metrics per competitor. Fast; ~10–15 minutes per row.
3. **Per-competitor Tier-1 research** — for each of the 4–5 Tier-1 competitors, follow the per-competitor research sequence below — including the new per-page deep audit (Step 8) and top-5-pages pattern detection (Step 9) — and produce a brief at `<output-folder>/<competitor-slug>.md`.
4. **Write the cross-competitor synthesis** — read all the Tier-1 briefs + the Tier-2 light-scan rows, extract patterns at the SITE level AND the cross-competitor structural pattern at the PAGE level, and write the synthesis at `<output-folder>/synthesis-YYYY-MM-DD.md`.
5. **Maintain folder hygiene** — write a `_README.md` for the new folder if one doesn't exist, and update the parent folder's `_README.md` to list the new child (per the vault stewardship principle that subfolder creation and README maintenance are one atomic action).

Mark each phase as a task in the operator's task list so they can see progress.

**Why the enhancements are default-on.** Oliver's 2026-05-26 direction: "I would want the competitor-deep-dive to do both tier 1 and tier 2, not have them as separate modes, I want all the data we can get at once" + "stalker like with all the details we can get so we know the actual stats of stuff and really understand their website." Tier-2 cross-validates that Tier-1 findings are representative across the broader competitive set rather than idiosyncratic to the 4–5 deepest competitors. Per-page audit makes the brief-template's §4.5 (AI-citation hardening checklist) verifiable at the scaffolder gate — every checkbox can be checked against real data, not assumptions. Top-5-pages pattern surfaces the WINNING STRUCTURE inside each competitor's site, which is what the Phase 3a scaffolder reproduces.

---

## Phase 1: Identify the competitor list

Two sources of competitor names: the operator's prior data and a fresh Google search. After the 2026-06-03 enhancements, **two tiers** of competitors get identified up-front — the deep-dive Tier 1 (4–5 names) AND the broader Tier 2 (the rest of the top 10 + ranking-source competitors).

**Prior-data source (preferred when available):** BrightLocal Local Search Grid reports, Ahrefs exports, prior audit notes. Pull the top-ranking competitors for the keywords the client cares about. If a BrightLocal report exists, the operator has done some of this work already — use it. The top-10 ranking-source competitors usually map cleanly to the Tier-2 set.

**Live Google search:** Run `WebSearch` for the target head keyword (e.g., "electrician Fairfax VA"). Pick from the top 10 organic results, excluding directories (Yelp, BBB, Angi, Checkbook, Houzz, Thumbtack, Yellow Pages, Nextdoor). The cross-source confirmation matters — competitors that appear in both BrightLocal AND organic Google are more strategically important than competitors that appear in only one.

**Tier 1 — full deep-dive briefs (4–5 competitors total):**

- **Primaries (2):** The 2 highest-ranking competitors for the client's most important keyword, OR the operator's named-must-include competitors. These get the full 9-section brief + per-page deep audit (Step 8) + top-5-pages pattern (Step 9).
- **Secondaries (2–3):** Additional competitors that round out the picture — typically the next-ranking organic results plus any operator-flagged-but-not-must-have names. Lighter-touch briefs (full 9 sections but fewer per-page audit rows, and top-5-pages pattern is optional).

Tier 1 cap is 4–5 because each Tier-1 competitor consumes 3–4 hours with the per-page audit + top-5-pages pattern work. More than 5 crosses a natural single-chat ceiling. If broader Tier-1 coverage is genuinely needed, decompose via the vault-orchestrator (one sub-chat per Tier-1 competitor in parallel).

**Tier 2 — light-scan rows (10 competitors total, INCLUDING the Tier-1 set):**

The Tier-2 set is the top 10 competitors for the head keyword. The 4–5 Tier-1 names appear as Tier-2 rows too (the structured row is a strict subset of the deep brief; producing both costs nothing extra in research time, and the same row format keeps the synthesis table consistent). The remaining 5–6 Tier-2-only competitors come from positions 5–10 in the ranking-source plus any organic Google top-10 not already named.

Each Tier-2 row is the structured metric set spec'd in Phase 2 below (~10–15 minutes per row). The Tier-2 light scan validates that the Tier-1 deep-dive findings are representative — patterns the deep dives surfaced should also appear in the broader scan, and patterns that surface only in deep dives but not in the light scan are flagged in the synthesis as Tier-1-specific (potentially idiosyncratic) rather than market-wide.

If the head-keyword SERP has fewer than 10 real-business results (e.g., directories dominate the top 10), expand the search to adjacent variants (head keyword + closest 1–2 long-tail variants) until 10 real-business results are identified. The methodology section names the expansion if it happened.

---

## Phase 2: Tier-2 light scan (run before per-competitor Tier-1 research)

For each of the 10 Tier-2 competitors, produce a structured row. Don't write a brief — the row IS the deliverable. Rows go into the synthesis as Section 1.5 (Tier-2 light-scan table) once all are collected.

Run the light scan BEFORE Tier-1 deep dives. Doing the broader-but-shallower pass first surfaces market patterns that sharpen the Tier-1 questions ("which Tier-1 competitor matches the market median vs which is the outlier?"). It also catches Tier-2 competitors who turn out to deserve Tier-1 promotion (e.g., a previously-unscanned operator surfaces as the #1 organic ranker with content depth nobody else has).

### Tier-2 row columns (one row per competitor)

Capture these 10 columns. Each cell cites the source inline.

1. **Domain** — canonical root domain.
2. **Page count** — total URLs in `sitemap.xml`. Bash: `curl -s <domain>/sitemap.xml | grep -c "<loc>"`. Fall back to the parent sitemap index if the top-level lists sub-sitemaps.
3. **Tech stack fingerprint** — CMS (WordPress / static SSG / enterprise CMS / Wix/Squarespace), hosting (HTTP `server:` header), schema present/absent (grep the homepage HTML for `application/ld+json`). One short line per cell, e.g. `WordPress + WP Engine; schema absent`.
4. **Top 5 keywords ranked for** — populated from DataForSEO Labs (preferred) or free Ahrefs Site Explorer / free Ahrefs Backlink Checker. List the top 5 by traffic; include the rank if available.
5. **Total backlink count** — from BrightLocal (if a scan exists), free Ahrefs Backlink Checker, or DataForSEO Backlinks Summary. Cite the source + date.
6. **Domain Authority** — Moz DA (or Ahrefs DR / SEMrush AS; specify which). Free Moz Link Explorer covers ~10 free queries/month; DataForSEO does not expose Moz DA directly.
7. **Average rank for the head keyword** — from the ranking-source PDF (BrightLocal Local Search Grid) or DataForSEO SERP `rank_absolute`. Cite source + date.
8. **Word count of one sampled service page** — pick the service page that matches the client's headline service (e.g., panel upgrade for an electrician). Use the existing `scripts/count_words.py` for a hard count; do not estimate. Cite the URL fetched.
9. **FAQ count on the sampled page** — hard count of question-answer pairs in the page body. Often visible as `<details>` / `<summary>` or as accordion section headings ending in `?`.
10. **Schema types on the sampled page** — list the `@type` values found in `application/ld+json` blocks (`LocalBusiness`, `Service`, `FAQPage`, `AggregateRating`, `BreadcrumbList`, etc.). Note "none visible in source" explicitly when absent.

### Method (DataForSEO path)

For the keyword + backlink + rank columns, use the wrapper at `~/workspace/second-brain-tier3/automation/scripts/dataforseo_query.py`. Endpoint cheat-sheet:

| Column | Endpoint | Typical cost |
|---|---|---|
| Top 5 keywords ranked for | `dataforseo_labs/google/ranked_keywords/live` (POST) | $0.005–$0.05 per target |
| Total backlink count | `backlinks/summary/live` (POST) | $0.0005–$0.005 per target |
| Average rank for head keyword | `serp/google/organic/live/regular` (POST) | $0.0006 per keyword |
| Page count (cross-check) | `dataforseo_labs/google/relevant_pages/live` (POST) | $0.005 per target |

Run each as a batched call where possible (multiple targets per request). Budget for 10 competitors × the 4 paid endpoints lands around $0.30–$0.50. The wrapper reports `tasks[*].cost` on stderr so the methodology section can record actuals.

### Method (free-toolkit fallback)

When DataForSEO is unavailable or the operator wants to defer cost:

- **Top 5 keywords ranked for** — use free Ahrefs Site Explorer ("top organic keywords" tab; shows top 5 free), or free Ubersuggest (top 5 free per IP per day). For ranking-source-PDF sources (e.g., BrightLocal), cite the keywords the scan tracked rather than re-deriving.
- **Total backlink count** — use free Ahrefs Backlink Checker (`ahrefs.com/backlink-checker`; shows count + top 100 links per domain per day per IP). Cite the date + source.
- **Domain Authority** — use free Moz Link Explorer (10 queries/month free). Or accept the ranking-source value if BrightLocal/Ahrefs scan exists.
- **Average rank for head keyword** — accept the ranking-source PDF value. If none exists, run a manual Google search for the head keyword from an incognito browser in the target geography and record the position.
- **Word count + FAQ count + schema types** — these are all derivable from `mcp__workspace__web_fetch` on the sampled page + `scripts/count_words.py`. No tool dependency.

Annotate each row with the source path actually used. The synthesis methodology section names which path the run used.

### When to escalate a Tier-2 row to Tier-1

If a Tier-2 row reveals:

- A competitor with 3× the page count of any Tier-1 primary AND ranking position better than 5
- A competitor with content-depth signals (word count 2,500+, FAQ count 5+, schema present) AND no current Tier-1 brief

…flag to the operator: "Tier-2 row N looks Tier-1-worthy. Promote and run a full deep dive?" The operator decides; don't auto-promote.

### SPA fallback

Same as Step 7 in Phase 3 below. If `web_fetch` returns empty, the site is client-rendered. Escalate to `mcp__Claude_in_Chrome__navigate` + `mcp__Claude_in_Chrome__get_page_text` when available; otherwise mark the row `[SPA — needs browser-rendered fetch]` and proceed. Don't fake values.

---

## Phase 3: Per-competitor Tier-1 research sequence

For each Tier-1 competitor, run the same sequence. Mechanizing the sequence is what makes the briefs comparable. Steps 1–7 are the legacy procedure; Steps 8 and 9 are the 2026-06-03 enhancements (per-page deep audit + top-5-pages pattern detection).

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

### Step 8: Per-page deep audit (2026-06-03 enhancement)

This is the "stalker-level" detail layer Oliver asked for. For each audited page on every Tier-1 competitor, capture a structured stats row. Don't substitute prose impressions — the table makes patterns visible at a glance and feeds the brief-template's §4.5 AI-citation hardening checklist directly.

**Pages to audit per Tier-1 primary (5 minimum):**

1. Homepage
2. Service page matching the client's headline service
3. City page matching the client's primary geography
4. A second service page (the client's #2 priority service)
5. A second city page (a near-primary geography)

For Tier-1 secondaries, 2–3 pages is fine (homepage + the service or city page).

**Columns to capture per page:**

| Column | What it is | How to capture |
|---|---|---|
| URL | The page audited | Direct |
| Page type | homepage / service / city / service×city / FAQ / blog / hub | Visual classification |
| Word count | Hard count of body text (excluding nav/footer/sidebar) | `scripts/count_words.py` against fetched HTML |
| Sentence count | Hard count of sentences in the body | Same script; `--mode sentences` flag |
| Paragraph count | Hard count of `<p>` tags inside main content | Same script; `--mode paragraphs` flag |
| H1 / H2 / H3 counts | Counts of each heading level | grep for `<h1`, `<h2`, `<h3` in the fetched HTML |
| Image count | Count of `<img>` tags in the body | grep `<img` |
| Alt-text quality | Proportion of `<img>` tags with descriptive alt vs empty/generic | grep `alt=""` for empty; manual sample of remaining alts |
| Schema types emitted | List of `@type` values inside `application/ld+json` | grep + JSON parse |
| FAQ count | Hard count of Q&A pairs in body | Visual count (often `<details>` / `<summary>` or accordion headings ending in `?`) |
| Internal-link count (in-body) | Count of `<a href>` inside main content, excluding nav/footer | Bash: extract main content block + grep |
| External-link count | Count of `<a href>` with hostnames different from the page | Same + filter |
| Page load time | Total time to load | PageSpeed Insights API or Lighthouse |
| LCP / INP / CLS | Core Web Vitals — Largest Contentful Paint (how long until the biggest visible element renders), Interaction to Next Paint (input responsiveness), Cumulative Layout Shift (how much the page jumps as it loads) | PageSpeed Insights API field data preferred, lab data fallback |
| Pricing published | Yes / No — does the page display real numbers? | Visual inspection |

**Method (DataForSEO path):**

For Core Web Vitals + page-load metrics, use the DataForSEO On-Page API:

- `on_page/pagespeed/google/live` — runs Google PageSpeed Insights against the URL. Returns LCP / INP / CLS / Speed Index + lab and field data when available. Cost ~$0.005 per URL.

For schema validation:

- `on_page/instant_pages` — fetches the page with browser rendering (handles SPAs) and returns parsed structured data among the response payload. Cost ~$0.005 per URL.

For 5 pages × 4–5 Tier-1 competitors that's roughly $0.10–$0.15 per competitor on the on-page audit alone.

**Method (free-toolkit fallback):**

- **Word / sentence / paragraph counts** — `scripts/count_words.py` (extend as needed; pure-Python, no API).
- **CWV + page load** — Google PageSpeed Insights free web UI (`pagespeed.web.dev`). Run each URL manually; capture LCP / INP / CLS / Speed Index from the report. Field data when available, lab data otherwise. Rate-limited but free.
- **Schema validation** — Google Rich Results Test (`search.google.com/test/rich-results`). Run each URL; capture which schema types pass validation. Definitive verdict per URL.
- **Heading / image / link counts** — grep against the fetched HTML.

Annotate each page row in the brief with the method actually used.

**Cross-page patterns become visible in the table.** Once 5 pages × 5 competitors = 25 rows exist, scan the columns vertically: do all 5 of AJ Long's audited city pages share a 3,500–4,000 word count? A 6-tile why-choose-us section? 5 named neighborhoods? That observation IS the seed for Step 9.

### Step 9: Top-5-pages cross-page pattern detection (2026-06-03 enhancement)

For each Tier-1 primary (Tier-1 secondaries: optional), identify the 5–10 highest-trafficked pages on the competitor's site and characterize their shared structural traits. This surfaces the WINNING STRUCTURE inside each competitor's site — not "what they do on the panel page" but "what their BEST pages systematically do that their worse pages don't."

**Method (DataForSEO path):**

- `dataforseo_labs/google/relevant_pages/live` — returns the top-trafficked pages on a domain ranked by organic traffic estimate. Cost ~$0.005 per target.
- Take the top 5–10 results. For each, fetch with `mcp__workspace__web_fetch` and apply the Step 8 audit columns.
- Look for traits present in 4+ of the 5 (or 5+ of the 10) audited pages — these are the structural patterns.

**Method (free-toolkit fallback):**

Three sources, pick the best available:

- **SimilarWeb free** (`similarweb.com/website/<domain>`) — surfaces the top-trafficked pages on a domain. Free tier shows top 5 pages with ~3-month-stale traffic data. Sufficient for pattern detection.
- **Sitemap + nav-heuristic** — read `sitemap.xml` and identify the page-types-most-linked-from-the-homepage-or-mega-nav as the proxy for "most-trafficked." Less precise than SimilarWeb but free and always available. For a 274-URL sitemap (AJ Long), the top-cluster pages are typically the city × headline-service combos.
- **Operator-named** — when the operator already knows the competitor's high-trafficked URLs (e.g., from a prior Ahrefs Pro export), use that list directly.

**Pattern detection rule:**

A structural trait counts as a pattern if it's present in **4 of 5** (or **5 of 10**, or proportional ≥80%) of the audited top-trafficked pages. Lower thresholds inflate noise. Higher thresholds miss real patterns. Document the trait + the page-share count + a one-line "what the pattern looks like in practice" in the brief's Section 7.5 (Top-5-pages pattern).

Examples of the kinds of traits that count:

- Word count band ("4 of 5 are 3,500–4,000 words")
- Structural section presence ("5 of 5 have a 6-tile why-choose-us section")
- Named-content density ("5 of 5 name 5+ specific neighborhoods")
- FAQ count ("4 of 5 have exactly 5 FAQs")
- Case-study placement ("5 of 5 embed 1 case study mid-page")
- Schema types ("5 of 5 emit LocalBusiness + Service; 0 of 5 emit FAQPage")
- Internal-link density to specific page-types ("5 of 5 link to ≥10 sibling city pages in-body")
- Image-treatment patterns ("4 of 5 use a hero photo of a real technician on a job site")

**Cross-validation with the per-page audit.** The Step 8 audit captured 5+ pages per competitor; some of those overlap the top-5 detected here. When a Step 8 audited page IS one of the top-5 trafficked pages, cite the row directly rather than re-fetching. Reduces fetch budget and keeps the data lineage clean.

The synthesis (Phase 4 below) rolls Step 9's per-competitor patterns into a cross-competitor "what does winning content in THIS niche look like at the structural level" — see Section 4.5 in the synthesis template.

---

## Phase 4: Cross-competitor synthesis

After all Tier-1 briefs are written AND the Tier-2 light-scan rows are collected, write the synthesis at `<output-folder>/synthesis-YYYY-MM-DD.md`. Use the template at `references/synthesis-template.md`.

The synthesis is where the strategic value lands. Per-competitor briefs and Tier-2 rows are inputs; the synthesis is the deliverable that operators will refer to when planning the client's Core 30 build or SEO foundation. Don't shortcut it.

Required sections (in order):

1. **Quick-reference comparison table** — one row per Tier-1 competitor, with reviews, rating, links, authority, tech stack, page count, and top-keyword rank. The table is what operators screenshot and paste into client decks. Make it scannable.

1.5. **Tier-2 light-scan table** *(2026-06-03 enhancement)* — one row per Tier-2 competitor (the 10 rows from Phase 2), using the 10-column structured format. Tier-1 competitors appear here too with their full data; Tier-2-only competitors get the same row shape. Sort by average rank for the head keyword. This is the cross-validation layer for the Tier-1 findings: patterns that surface in both tiers are market-wide; patterns that surface only in Tier-1 are flagged in the next section as Tier-1-specific (potentially idiosyncratic).

2. **The headline finding** — the single most important pattern in the data. In the EV Electric case it was "content depth beats domain authority in this niche" (Mr. Electric's 53/100 authority losing to AJ Long's 11/100). Every market will have its own headline finding; surface it explicitly. Triangulate with the Tier-2 table: does the headline finding hold across the broader 10-competitor set?

3. **Common patterns** — what ALL the competitors do (Tier 1 + Tier 2). These are table stakes — the client can't differentiate by doing them, only lose by skipping them. Distinguish "all Tier-1" from "all Tier-1 + Tier-2" when the difference matters.

4. **Differentiation opportunities** — what NOBODY does well across BOTH tiers. These are the gaps the client can exploit. Make each one concretely actionable.

4.5. **Cross-competitor structural pattern** *(2026-06-03 enhancement)* — roll up the per-competitor top-5-pages findings (from each Tier-1 brief's Section 7.5) into one cross-competitor view. Answers: "what does winning content in THIS niche look like at the page structural level?" Format: a table of structural traits × cross-competitor presence (e.g., "4,000-word city pages: 3 of 4 Tier-1 / 5 of 6 top-trafficked across competitors"). Surfaces the structural blueprint the Phase 3a scaffolder should reproduce.

5. **Keyword targets ranked by competitiveness** — four tiers (hard, moderate, easy, defensive). Each tier names specific keywords and explains why they're at that difficulty level.

6. **Tech stack patterns: the "winning stack"** — what the data shows about which infrastructure choices correlate with ranking outcomes. Validate against the Tier-2 table (does the "winning stack" stay winning when the lens widens?).

7. **Top 10 recommendations for the client's page build** — ordered by impact-to-effort ratio. Each recommendation should map to a specific finding from the briefs OR the cross-competitor structural pattern.

8. **Top 3 risks if the client doesn't act** — what happens if they delay.

9. **Blocked questions / follow-up research** — anything that couldn't be confirmed in this round. Honesty about gaps matters more than appearing comprehensive.

10. **Methodology** — append the methodology section (described in `references/synthesis-template.md`) so the work can be reproduced or extended by future researchers. Specify which path the run used (DataForSEO / free-toolkit / mixed) per enhancement.

---

## Phase 5: Folder hygiene

If the output folder is new, write a `_README.md` for it (template at `references/folder-readme-template.md`). If the parent folder has its own `_README.md` that lists subfolders, update it to include the new child. This is per the Knowledge OS vault stewardship principle that subfolder creation and README maintenance are one atomic action.

---

## Phase 6 — Closing step — Auto-invoke output-quality-loop

After Phases 1-5 complete (Tier-2 light-scan rows collected, per-competitor Tier-1 briefs written, cross-competitor synthesis landed including the Tier-2 table + cross-competitor structural pattern, folder `_README.md` shipped or updated), emit the standard auto-invoke block per `~/workspace/skills/output-quality-loop/references/auto-invoke-convention.md` and `~/workspace/second-brain/_meta/conventions.md` § "Output quality". This is the closing step every artifact-producing skill emits before declaring the chat done. Convention shipped Phase 5 of the output-quality-loop project (2026-05-28).

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

---

## Peer-reviewer dispatch (GPR-9, gate-peer-reviewer v3.3)

**Gate type:** G-competitor-brief (closing gate — Check 6 KCA applies).
**Fires after:** Per-competitor deep dives + cross-competitor synthesis, before closing.
**Dispatch shape:** Orchestrator spawns the peer-reviewer as a Task sub-agent after the synthesis is authored and before the closing protocol completes.

**Per-gate dispatch block (Claude Code substrate):**

```
## Peer-reviewer dispatch

Gate type: G-competitor-brief
Orchestrator: competitor-deep-research
Project: <client-slug>
Wave: null

Context paths for the Task sub-agent:
- Gate output: <paths to per-competitor briefs + cross-competitor synthesis>
- Gate-type registry: ~/workspace/skills/gate-peer-reviewer/references/gate-type-registry.md
- Check spec: ~/workspace/skills/gate-peer-reviewer/references/check-spec.md
- Lesson files: ~/workspace/second-brain/05_shared-intelligence/lessons/ (most recent for this skill)

Task instruction: Read the gate-type registry entry for G-competitor-brief. Run Check 1 satisfaction targets.
Run Checks 2-5 per check-spec.md skip logic. This IS a closing gate — run Check 6 (KCA).
Classify each catch severity per return-contract.md § Severity tiers.
Return the structured JSON verdict per references/return-contract.md.
```

**What the orchestrator does with the verdict:**

- `APPROVE` + `verdict_severity: advisory` → proceed to close. No operator review needed.
- `APPROVE-WITH-NOTES` + `verdict_severity: advisory` → proceed to close; notes logged for awareness.
- `APPROVE-WITH-NOTES` + `verdict_severity: blocking` → surface to operator with catches. Operator decides.
- `REJECT-AND-REDO` → fix the catch, re-run the step, re-dispatch peer-reviewer. Cap at 2 iterations; on 3rd REJECT, escalate to operator.
- `ESCALATE-AMBIGUOUS` → surface to operator with the peer-reviewer's ambiguity framing.

**Graceful degradation.** If peer-reviewer dispatch fails (skill unavailable on substrate), log:

```
event-type: peer-reviewer-skipped
reason: skill not available on <substrate>
chat-id: <id>
gate-id: G-competitor-brief
orchestrator: competitor-deep-research
```

Then proceed to close with the skip noted.
