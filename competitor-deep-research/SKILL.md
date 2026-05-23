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
