---
name: service-seo-research
description: Produce a Tier-1 service base brief — cross-client, cross-city, per domain — that downstream Phase 3a scaffolders consume to author 2000-word service pages. Triggers on phrases like "research the panel-upgrade service," "produce a service base brief for X," "run service SEO research on Y," "write the Tier-1 brief for Z service," "do a service-level competitor synthesis for [service],", "what's the SERP look like for [service]," or any time the operator wants a service-level (not client-level, not city-level) research output. One argument: the service name. Optional second argument: domain qualifier (e.g. residential-electrical, plumbing, hvac). Output: a single markdown file at second-brain/05_shared-intelligence/research-briefs/services/<service-slug>.md following the locked template at second-brain/05_shared-intelligence/research-briefs/_template-service-brief.md.
---

# Service SEO Research

A reusable workflow for producing Tier-1 service base briefs. The
briefs sit at `second-brain/05_shared-intelligence/research-briefs/services/`
and feed every Phase 3a scaffolder run for every client in the same
domain.

This skill was authored on 2026-05-26 as part of Phase 2a of the
[[client-seo-onboarding-automation]] blueprint. The first brief
produced from it is the panel-upgrade brief — refer to it when this
skill's instructions are unclear; it's the worked example.

This skill is a **sibling** to [[competitor-deep-research]], not an
extension of it. The two have different shelf locations, different
output shapes, and different consumers. This skill calls the
competitor-deep-research workflow as a research subprocess; it doesn't
replace it.

---

## When to use

Trigger this skill when the operator wants service-level (not
client-level, not city-level) intelligence about a specific service in
a specific domain. Typical triggers:

- "Research the panel-upgrade service"
- "Produce a service-base brief for [service]"
- "Write the Tier-1 brief for [service]"
- "What's the SERP look like for [service]?"
- "Do a service-level competitor synthesis for [service]"
- "Run service SEO research on [service]"

Do **not** use this skill for:

- Per-client competitive research (use [[competitor-deep-research]])
- Per-city research (use Phase 2b city-base research engine — TBD)
- Per-(service × city) research (use Phase 2c intersection research
  engine — TBD)
- Per-client fact gathering (use Phase 2d client-fact research engine
  — TBD)
- One-tool surveys (use [[seo-tooling-landscape-research]])

---

## Inputs the skill needs

Confirm these with the operator before researching. Present as plain
text — do not use AskUserQuestion (it's been glitching in Cowork per
Oliver's standing feedback memory).

1. **Service name and slug.** What's the service? What's the slug it
   will be stored under? (Examples: `panel-upgrade`, `troubleshooting`,
   `ev-charger-installation`.) Slug should be lowercase kebab-case,
   no plural.

2. **Domain.** Residential electrical? Plumbing? HVAC? Roofing? The
   domain qualifier matters because the same service name can mean
   different things across domains (e.g. "installation" in roofing
   vs. electrical). Default to `residential-electrical` for Keelworks
   work in 2026.

3. **SERP scope.** National (default) or regional? National is the
   right scope for most service briefs — the brief stays
   cross-client and cross-city. Regional makes sense only when the
   service has materially different competitive landscapes by region
   (e.g. solar installation in the Sun Belt vs. the Northeast).

4. **Existing-research carry-overs.** Has a competitor-deep-research
   run for a relevant client already happened? (E.g. the EV Electric
   enhanced competitor synthesis from 2026-06-03 covers Tier-1 deep
   dives on AJ Long, Mr. Electric, Absolute, Kolb + Tier-2 light-scan
   rows for 6 additional competitors + cross-competitor structural
   pattern for residential electrical in Fairfax County.) Carrying
   those findings forward avoids re-research. If yes, name the
   synthesis file so the skill reads it instead of re-fetching the
   competitors.

   **Prefer the most recent enhanced synthesis** (produced via the
   2026-06-03+ enhanced `competitor-deep-research` skill which
   includes the Tier-2 light-scan table in §1.5 + per-page deep
   audit data inside each Tier-1 brief + cross-competitor
   structural pattern in §4.5). The enhanced shape feeds materially
   more service-brief sections than the legacy Tier-1-only synthesis:
   §2 (Top-10 SERP analysis), §5 (Schema patterns), §6 (Content
   depth norms), §7 (FAQ patterns), §9 (Internal-linking
   observations), §11 (Pricing visibility), §12 (Trust and
   authority signal norms) all pull from the enhanced data when
   available. If only a legacy Tier-1-only synthesis exists, the
   service brief still works but Section §2 + §6 + §11 carry
   wider gaps that the brief's methodology should name.

5. **Output folder.** Default:
   `~/workspace/second-brain/05_shared-intelligence/research-briefs/services/`.
   Override only if the operator wants the brief written somewhere
   else (rare).

6. **Time budget.** Useful to know up-front. Typical budget for a
   service brief from scratch: 60–90 minutes (top-10 SERP fetch +
   AI-search across 4 surfaces + schema audit + FAQ mining +
   synthesis). With a competitor-deep-research carry-over: 30–45
   minutes.

If any input is missing, ask the operator before researching.
Underspecified inputs are the most common failure mode for this
skill.

---

## Pre-flight: read the canonical exemplar and template

Before producing anything new, read:

1. The locked template:
   `~/workspace/second-brain/05_shared-intelligence/research-briefs/_template-service-brief.md`
   — every section, every "What this feeds" line, every consumption
   contract with the Phase 3a scaffolder.

2. The worked example:
   `~/workspace/second-brain/05_shared-intelligence/research-briefs/services/panel-upgrade.md`
   — what a finished brief looks like.

3. The scaffolder data shape:
   `~/workspace/repos/ai-agency-core/scripts/data/services/troubleshooting.json`
   — the JSON contract the brief feeds.

4. The folder conventions:
   `~/workspace/second-brain/_meta/conventions.md` — frontmatter and
   naming rules.

5. The plain-language conventions:
   `~/workspace/second-brain/_meta/plain-language-conventions.md`.

If the template has moved or been renamed, search the vault by
filename (Glob `_template-service-brief.md`). If not found, the
template's content is described inline in this SKILL.md below — fall
back to that.

---

## High-level workflow

The skill runs in nine phases. Phases 1-7 produce the brief sections
the Phase 3a scaffolder consumes; Phase 8 surfaces knowledge-growth
extensions; Phase 9 is an optional Perplexity refinement pass on the
finished brief. Don't skip Phases 1-7 — the scaffolder depends on every
section. Phase 8 is operator-default-on. Phase 9 is operator-opt-in.

1. **Confirm inputs** (above).
2. **Top-10 SERP fetch** — pull the live top 10 organic results for
   the head keyword.
3. **Keyword and question mining** — Google search + AI-search across
   Perplexity, ChatGPT, Claude, Gemini, Google AI Overviews + GSC
   regex query mining if client GSC is connected.
4. **Schema and content depth audit** — for the top 5, audit JSON-LD,
   word counts, FAQ patterns, pricing-visibility patterns.
5. **Image and trust-signal audit** — for the top 5, audit imagery
   and authority signals.
6. **Internal-linking map** — for the top 5, capture how their
   service pages link to each other and to city pages.
7. **Synthesis and write-up** — assemble the brief from sections 1–14,
   following the locked template exactly. AI-citation-hardening
   checklist (§4.5 of the template) must be verified before declaring
   done.
8. **Knowledge-growth hooks** — propose primer/tactic/pattern
   extensions based on what was learned. Hand off to
   [[meta-document-primer]] or [[multi-source-synthesis]] as the
   operator confirms.
9. **Optional Perplexity refinement** — offer to run
   [[perplexity-refinement]] on the brief to close the AI-search gaps
   flagged in §4 and §14c. Operator-opt-in; default-recommended depth
   is `deep`.

Mark each phase as a task in the operator's task list so they can see
progress.

---

## Phase 1 — Confirm inputs

Present the input list as plain text. Wait for the operator's
answers before proceeding. Underspecified inputs ruin the output.

If the operator carries forward a competitor-deep-research synthesis,
read that file first and capture the findings that apply at the
service level (not the city level). Most of the top-10 SERP audit
work, schema audit, and content-depth audit may already be done.

**Enhanced-synthesis consumption map** (when the carried-forward
synthesis was produced via the 2026-06-03+ enhanced
`competitor-deep-research` skill):

| Service brief section | Enhanced synthesis source |
|---|---|
| §2 Top-10 SERP analysis | §1.5 Tier-2 light-scan table — rebuild as service-specific Top-10 SERP table (re-fetch only for results not already in the Tier-2 set) |
| §5 Schema patterns | §1.5 schema-types column + §4.5 schema-types row (universal-gap finding lands cleanly into the brief's recommendations) |
| §6 Content depth norms | §4.5 word-count-band trait + per-Tier-1-brief Section 3.5 (per-page deep audit) — the median + 25/75 distribution is derivable from the Tier-1 audited-page rows |
| §7 FAQ patterns | §1.5 FAQ-count column + §4.5 inline-FAQ-embedding trait + per-Tier-1-brief Section 3.5 |
| §9 Internal-linking observations | §4.5 internal-link-density trait + per-Tier-1-brief Section 9 |
| §11 Pricing visibility | §4.5 transparent-pricing trait |
| §12 Trust and authority signals | §4.5 hero-treatment + named-neighborhood + permit-references traits |

For each section, the service brief should cite the enhanced
synthesis section it sourced from (e.g.,
`[source: [[../../04_projects/clients/_active/ev-electric-services/admin-extracts/competitor-research/synthesis-2026-06-03-enhanced|enhanced synthesis]] §4.5 on 2026-06-03]`).

---

## Phase 2 — Top-10 SERP fetch

**Default path (enhanced-synthesis carry-over):** if Phase 1 named
an enhanced `competitor-deep-research` synthesis (with §1.5 Tier-2
light-scan table), START by reading the §1.5 rows directly. The
Tier-2 set is already the top-10-shape; the only fetch work
remaining is verifying the rows are service-specific (a
Tier-2 row captured at the client level is general; the service
brief needs it scoped to the head-keyword SERP). Re-fetch only the
rows that don't already cover the head-keyword (typically 2–4 of
the 10).

**Full-fetch path (no enhanced synthesis available):**
Run `WebSearch` for the head keyword (e.g. `panel upgrade`,
`electrical troubleshooting`, `ev charger installation`). Capture the
top 10 organic results, excluding directories (Yelp, BBB, Angi,
Checkbook, Houzz, Thumbtack, Yellow Pages, Nextdoor).

For each result, use `mcp__workspace__web_fetch` to pull the page.
Capture:

- Domain, page title, URL pattern
- Word count (use `scripts/count_words.py` in the
  `competitor-deep-research` skill for hard counts; the
  enhanced-skill workflow assumes hard counts, not estimates)
- Whether JSON-LD schema is present (search for
  `application/ld+json`); list the `@type` values
- Whether FAQs are present on-page; hard count
- Whether pricing is visible

Build the **Top-10 SERP table** (Section 2 of the template).

**SPA fallback.** If `web_fetch` returns empty content for a result,
the site is client-rendered. Escalate to
`mcp__Claude_in_Chrome__navigate` + `mcp__Claude_in_Chrome__get_page_text`
if available; otherwise flag the result in the methodology section as
"blocked — JS-rendered" and move on. Don't fake the audit.

---

## Phase 3 — Keyword and question mining

This phase populates Sections 3 (Google) and 4 (AI search) of the
template.

### 3a. Google keyword mining

Tools to use, ranked by preference (programmatic first, then free
browser-driven, then free-with-caps):

**Programmatic (preferred for Claude-Code workflows):**

- **DataForSEO API** — `keywords_data/google_ads/search_volume`
  endpoint returns monthly volume + competition score per keyword.
  `dataforseo_labs/google/keyword_ideas` returns long-tail
  variants. `dataforseo_labs/google/keyword_difficulty` returns
  difficulty scores. Pay-as-you-go (~$0.0005-0.005 per query).
  Set API credentials from tier-3 vault (`DATAFORSEO_LOGIN`,
  `DATAFORSEO_PASSWORD`). Use this as the primary path for
  precise volume + difficulty numbers — substitutes for Ahrefs
  Pro / SEMrush Pro in this workflow.

**Browser-driven (via Claude in Chrome):**

- **Ahrefs free Keyword Generator** (`ahrefs.com/keyword-generator`)
  — navigate via `mcp__Claude_in_Chrome__navigate`, query, extract
  text. Free tier shows top 100 keyword ideas with monthly volume
  and difficulty for one query per IP per few hours.
- **AlsoAsked** (`alsoasked.com`) — 3 free queries per day. Best
  visualization of the People-Also-Ask tree. Navigate via Chrome,
  query, capture the tree.
- **AnswerThePublic** (`answerthepublic.com`) — 2 free queries per
  day. Question-form keyword visualization. Browser-drive same way.
- **Keyword Surfer Chrome extension** — overlays volume + competition
  on Google SERP. If Oliver has installed it, the data shows up
  inline when navigating Google search.

**Free-with-caps fallbacks:**

- **Google "People also ask"** — manual scroll of the SERP via
  Chrome navigation.
- **Ubersuggest free** — limited free queries per day.

Build the three keyword buckets (head + variants, long-tail,
questions) per the template's Section 3. Cite the tool inline per
the brief's source-attribution convention.

**Order of operations for a typical brief:**

1. Run DataForSEO API for head-keyword + 5-10 close variants → get
   precise volume + difficulty numbers
2. Run AlsoAsked + AnswerThePublic via Chrome for the question
   tree
3. Cross-check with Ahrefs free Keyword Generator if DataForSEO
   data feels off
4. Aggregate into Section 3a/3b/3c tables in the brief

### 3b. AI-search question mining

**Primary tool: Claude in Chrome.** All AI surfaces below are
browser-reachable in Oliver's signed-in session via
`mcp__Claude_in_Chrome__navigate` → `mcp__Claude_in_Chrome__get_page_text`.
Confirm a connected browser via
`mcp__Claude_in_Chrome__list_connected_browsers` before starting.
If empty, ask Oliver to install / launch the Claude in Chrome
extension and re-invoke.

Run the head query through each surface and capture answer shape +
citations:

- **Google AI Overviews** — navigate to Google search for the head
  query. Capture whether an AI Overview block renders and what
  sources it cites. Quote the Overview's structure verbatim — it's
  the outline the page needs to satisfy to be citation-worthy. If
  no Overview renders, note it; some queries don't trigger one.
- **Perplexity** (`perplexity.ai`) — run the head query. Capture
  sources cited and the answer's natural-language form. Perplexity
  cites the most aggressively of any AI surface; the source list
  is gold.
- **ChatGPT** (`chat.openai.com`) — run the head query in a chat with
  web browsing enabled. Capture cited sources + the answer pattern.
- **Claude** (`claude.ai`) — run the head query. Capture answer
  shape and citation pattern.
- **Gemini** (`gemini.google.com`) — run the head query. Capture
  answer shape and citation pattern.

For each surface, the brief's §4a-4c should record:
- The exact query run
- The first 200-300 words of the answer (or the entire answer if
  shorter)
- The source list (URLs, in order shown)
- Notable answer structure (bullet-heavy vs paragraph-heavy,
  with/without comparison tables, with/without code/data blocks)

### 3b.1 — Mandatory Otterly.ai integration (when configured)

**This is not optional when Otterly is set up.** Otterly.ai
tracks the same surfaces (ChatGPT, Perplexity, AI Overviews,
Copilot) DAILY across the client's configured prompts. The brief
benefits enormously from pulling the latest Otterly data into the
research process. Specifically:

1. **Per-prompt brand coverage** — Otterly's Brand Coverage % per
   prompt tells you which AI surfaces our brand appears in, which
   competitors appear, and at what frequency. Use this to validate
   or contradict the manually-run Phase 3b Perplexity / ChatGPT
   queries. If the manual queries show one competitor dominating
   but Otterly's 14-day trend shows a different pattern, the brief
   should flag the discrepancy and weight Otterly higher (it's
   time-averaged across daily scans).

2. **Citation share + domain coverage** — Otterly's Citations data
   shows which URLs the AI engines actually cite. This goes into
   the brief's §9 (Internal-linking observations) as
   "what URLs do AI engines preferentially cite from each competitor."

3. **Newly-surfaced competitor brands** — Otterly detects ALL
   brands mentioned per prompt, not just the configured ones. New
   competitors that surface this way feed §2 (Top-10 SERP analysis)
   as additional research targets. The brief's §15 (Methodology)
   should record any Otterly-surfaced competitor that wasn't in
   the original competitor-deep-research synthesis.

4. **Sentiment scores** — Otterly captures sentiment polarity per
   brand. If a competitor has negative sentiment markers, flag in
   the brief's §13c (Defensive moves) as "this competitor's
   reputation may be vulnerable — watch for them losing share."

**Practical:** export Otterly's CSV snapshots when running each
brief; reference the most recent snapshot's data points inline
in the brief. Citation format: `[source: otterly.ai snapshot
YYYY-MM-DD]`.

**If Otterly isn't yet configured for this client**, the brief
runs without this data and the methodology section notes the
limitation. When Otterly comes online later, the brief gets
refreshed.

### 3b.2 — Mandatory Watchdog integration (when configured)

**Watchdog (heytony.ca)** tracks weekly competitor change reports
for the configured 3 sites. The brief consumes Watchdog data in two
ways:

1. **As a brief-refresh trigger** — when Watchdog reports surface
   "major changes" on a tracked competitor's site (new service
   page launched, schema added, content overhaul), the brief
   should be considered for refresh. The brief's §15 (Methodology)
   should reference the most recent Watchdog scan and any changes
   noted since the last brief refresh.

2. **As a §2 (SERP analysis) input** — Watchdog's weekly digest
   surfaces new pages competitors publish. These are research
   targets for the brief's §2: have they added a panel-upgrade
   page in a new city? A new service-line page? The brief should
   audit these additions and either reflect them in the top-10
   SERP table (if they're ranking) or flag them as competitive
   moves to monitor.

**Cross-referencing the automated workflow**: per the
[[../../second-brain/_meta/handoffs/handoff-2026-05-26-competitor-deep-research-enhancements|2026-05-26
competitor-deep-research enhancements handoff]], a future Cowork
workflow will parse Watchdog weekly emails and auto-file analysis
notes per change. When that workflow is live, this brief's §2
research can incorporate those analysis notes directly via
wikilinks rather than re-deriving from scratch.

**Citation format**: `[source: watchdog.heytony.ca weekly report
YYYY-MM-DD]`.

Distill the "questions our page must answer" list — 8–12 questions
that appear in at least two AI surfaces' answer structures. Format
per the template's Section 4d.

### 3c. GSC regex query mining (verification layer)

If the client's GSC is connected to the agent (Ahmad: yes since
2026-05-22), run the GSC regex queries per
[[tactic-gsc-regex-query-mining-for-ai-search-discovery]]:

1. Navigate to GSC via Chrome:
   `https://search.google.com/search-console/performance/search-analytics?resource_id=<URL>`
2. Set date range to "Last 16 months"
3. Add a Query filter with Custom (regex):
   - `(\b\w+\b\s){7,}` for 7+ word conversational queries
   - Then run additional passes with each companion pattern from
     the tactic note (question-form, near-me, urgency,
     comparison, decision-stage)
4. Sort by Impressions descending; capture top 30-50 entries per
   pattern
5. Cross-reference with the brief's §3c (PAA-derived questions) and
   §4d (AI-surface questions). Verified queries are higher-priority
   for the scaffolder than purely hypothesized ones.

The brief's §4e captures the GSC-regex output in a structured table
with Action column (rewrite existing page / add new page / add to
FAQ / add as attribute).

---

## Phase 4 — Schema and content depth audit

For the top 5 SERP results, run the schema audit:

- Search the fetched HTML for `application/ld+json`. If present,
  capture the `@graph` structure: which `@type` values, how
  `LocalBusiness` and `Service` relate, whether `Service.offers`
  carries a real `Offer.price` or a `termsOfService` string.
- Run each top-5 URL through the Google Rich Results Test
  (`search.google.com/test/rich-results`) if browser tools are
  available, or note the schema only from the HTML.

For each, capture content depth:

- Median page word count across the top 10
- Section-by-section paragraph counts for the median page
- Paragraph length distribution
- Tone (corporate-formal, contractor-folksy, technical, consultative)
  — quote 2–3 sentences from the top-ranking page as the voice anchor.

Populate Sections 5 and 6 of the template.

---

## Phase 5 — FAQ, image, trust, and pricing audit

For the top 5, capture:

- **FAQ patterns** (Section 7) — which 6–10 Q&As recur. For each:
  canonical wording, how many of the top 5 pages have it, average
  answer length, notes. Identify the "no competitor answers this
  well" gap.
- **Image-style observations** (Section 8) — hero treatment, imagery
  type, color palette, composition norms, alt-text norms, owner-face
  presence. Recommend a Higgsfield prompt direction for the service.
- **Pricing-visibility norms** (Section 11) — published-pricing
  pattern vs. estimate-only pattern. Pattern distribution across the
  top 10. Median pricing range if published-pricing dominates.
  Tone of pricing transparency.
- **Trust and authority signals** (Section 12) — license, insurance,
  years in business, review count + rating, owner face, awards.
  Which are universal (table-stakes), which are differentiation
  opportunities.

For Section 11 specifically: per the
[[decision-2026-05-26-no-pricing-on-residential-contractor-core-30-pages]]
decision, the default for Keelworks residential contractor clients
is the **estimate-only pattern**. Capture what competitors do
honestly, then recommend the estimate-only pattern unless the
operator overrides for a specific service or client.

---

## Phase 6 — Internal-linking map

For the top 5, capture the internal-link patterns (Section 9):

- Service-to-service links — how many, where on the page, anchor-text
  patterns
- Service-to-city links — how many, presentation, anchor-text
- Service-to-category-hub links — does a hub exist; how does this
  page link up to it
- Link density — average cross-links per page

Recommend a `related_cards` set for the service — 4–6 sibling
services in topical-adjacency order. This feeds the Phase 4b
internal-linking automation directly.

---

## Phase 7 — Synthesis and write-up

Open the locked template
(`~/workspace/second-brain/05_shared-intelligence/research-briefs/_template-service-brief.md`)
and produce a brief at
`~/workspace/second-brain/05_shared-intelligence/research-briefs/services/<service-slug>.md`
following the template exactly.

**Before declaring done, verify §4.5 — the AI-citation-hardening
checklist.** Every checkbox should pass. If any fail, flag in §15
(Methodology) and let the operator decide whether to accept or
remediate. The checklist is the brief's gate to the scaffolder; an
unchecked brief produces a weaker page.

Apply these rules:

### File structure and frontmatter

```yaml
---
type: research-brief
brief-tier: service
status: draft
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
service-slug: <service-slug>
domain: <domain>
research-date: <YYYY-MM-DD>
researcher: service-seo-research-skill
tools-used: [<list of tools actually consulted>]
sources-cited: <integer>
tags: [research-brief, tier-1, service, <domain>]
---
```

Filename: `<service-slug>.md` — no `brief-` prefix (these are
descriptive cross-domain reference docs, like the SEO tools
inventory files).

### Required sections

All 15 sections from the locked template, in order:

1. Service identity and naming
2. Top-10 SERP analysis
3. Keyword and question targets — Google search
4. Keyword and question targets — AI search
5. Schema patterns competitors use
6. Content depth norms
7. FAQ patterns
8. Image-style observations
9. Internal-linking observations
10. Problem and process patterns
11. Pricing-visibility norms
12. Trust and authority signal norms
13. Competitive moat assessment
14. Sources cited
15. Methodology

Each section opens with the template's **What this feeds** line so
the Phase 3a scaffolder reader knows which JSON fields the section
serves.

### Source-attribution requirement

Every claim in the brief must trace to a competitor page fetch, a
keyword-tool query, an AI-search run, or an existing vault note.
Inline citation format:

```
[source: <type> <reference> on YYYY-MM-DD]
```

Examples:

- `[source: webfetch https://example.com/services/panel-upgrade/ on 2026-05-26]`
- `[source: alsoasked.com query "panel upgrade" on 2026-05-26]`
- `[source: perplexity.ai query "what does a panel upgrade cost" on 2026-05-26]`
- `[source: rich results test https://example.com/services/panel-upgrade/ on 2026-05-26]`
- `[source: [[../../04_projects/clients/_active/ev-electric-services/admin-extracts/competitor-research/synthesis-2026-05-23|EV Electric Fairfax synthesis]] on 2026-05-23]`

Section 14 (Sources cited) is the roll-up of all inline citations,
grouped by source type. The brief's `sources-cited:` frontmatter
field is the count of distinct sources in that roll-up.

### Plain-language requirement

Per [[plain-language-conventions]], write the brief in plain
language. Gloss SEO and schema jargon inline the first time it
appears. The brief is read by Oliver (operator) and by the Phase 3a
scaffolder — neither benefits from dense whitepaper voice.

### Honest-assessment requirement

Per Oliver's standing preferences captured across multiple memories:
call out hype, lock-in, and feature gaps explicitly. Don't
sugarcoat. If a competitor is strong, say so. If the top-10 SERP is
dominated by directory-style pages and only one real-business page
ranks well, call that out — it means the moat is "have a real
business page" and the recommendation is "ship one."

### Wikilink rules

Slug-only wikilinks for files with unique filenames:
`[[panel-upgrade]]`, `[[plain-language-conventions]]`. Path-based
wikilinks for ambiguous filenames like project READMEs:
`[[ev-electric-services/README]]`.

Every brief must link to:

- The parent folder README (`[[_README]]` or
  `[[services/_README]]`)
- The locked template (`[[_template-service-brief]]`)
- The blueprint (`[[client-seo-onboarding-automation]]`)
- Any client-side competitor-research synthesis the brief carried
  findings from
- The plain-language conventions
- The SEO primer ([[primer|seo/primer]]) for terminology and
  operational layer references

---

## Phase 8 — Knowledge-growth hooks

This phase is what makes the research engine **compounding**
rather than one-off. After producing the brief in Phase 7, the
skill scans for primer/tactic/pattern extension opportunities and
offers them to the operator as a numbered list.

The skill never writes to primers/tactics/patterns without
explicit operator confirmation. Default behavior: surface
extensions; let the operator approve.

### 8a. Scan for new vocabulary

Read the brief's body and compare against the SEO primer's
Appendix A. Flag any term used in the brief that isn't already
defined either in the SEO primer or in the marketing primer's
Appendix A.

For each flagged term:
- Surface to operator with a 1-sentence proposed gloss
- Ask "Add to SEO primer Appendix A?"
- On confirmation, invoke [[meta-document-primer]] in
  `extend-and-write` mode against the SEO primer

### 8b. Scan for tactical patterns

Read the brief's §2 (Top-10 SERP), §5 (Schema), §6 (Content depth),
§8 (Image), §9 (Internal-linking), §11 (Pricing), §12 (Trust
signals). Identify any pattern observed in 3+ competitor pages
that isn't already named as a tactic in `seo/tactics/`.

For each candidate:
- Surface to operator with the observed mechanism and the 3+
  source citations from the brief
- Ask "Promote to a new tactic note?" or "Add as cluster-recorded
  observation under an existing tactic?"
- On confirmation, write the tactic note per the conventions
  (frontmatter + capture date + mechanism + cluster math)

### 8c. Scan for pattern-promotion candidates

Read the brief alongside any other recent service briefs (last 30
days). If the same pattern surfaces in 2+ briefs, that's a
2/3-promotion candidate. If 3+, that's 3/3-promotion-ready.

For each candidate:
- Surface to operator with the brief citations
- Ask "Hand off to [[multi-source-synthesis]] for pattern
  promotion?"
- On confirmation, the multi-source-synthesis skill takes over

### 8d. Scan for synthesis-readiness

Invoke [[synthesis-readiness-scan]] on the SEO domain scope.
The scan checks for ready clusters (3+ source notes converging on
the same pattern) and surfaces them. Any cluster that crossed
threshold this run gets offered.

### 8e. Update the SEO primer's Section D tactics list

If a new tactic note was created in step 8b, update the SEO
primer's Section D bulleted list to include it. This is the only
direct primer write the skill does — it's a one-line addition that
keeps the primer's tactics list current.

### 8f. Update the consumption-contract table in the template

If the brief surfaced JSON-field additions (e.g., the
`tldr_paragraph` or `key_takeaways` fields proposed 2026-05-26),
flag for operator: "Should these be added to the Phase 3a
scaffolder's JSON shape?" The brief template's bottom table is
the single source of truth for the consumption contract; updating
it stays a manual operator step until the Phase 3a scaffolder
ships and the new fields are validated end-to-end.

### Output of Phase 8

A numbered list of proposed extensions, each with:
- What it is (vocab gloss / tactic mechanism / pattern observation)
- Where it would land (primer Appendix A / new tactic note /
  pattern promotion / synthesis invocation)
- Source citations from the brief
- A one-sentence "why this is worth capturing"

The operator picks `all`, `none`, or specific numbers. The skill
executes only the confirmed picks.

---

## Phase 9 — Optional Perplexity refinement (added 2026-05-27)

After the brief is written (Phase 7) and knowledge-growth hooks are
processed (Phase 8), the skill MAY offer to run a Perplexity refinement
pass on the new brief via the [[perplexity-refinement]] skill. This
step is **operator-opt-in**, not automatic — the brief is complete and
shippable to the Phase 3a scaffolder without Phase 9.

### Why Phase 9 exists for service briefs specifically

The brief template's §4 (Keyword and question targets — AI search) and
§14c (Sources cited — AI-search surfaces) routinely flag Perplexity,
ChatGPT, Claude, and Gemini as **not reachable from the original Cowork
invocation**. The first panel-upgrade brief (2026-05-26) carried four
explicit Perplexity-shaped gaps:

- §4a: AI Overview structure — inferred, not directly observed
- §4b: Perplexity citation set — blocked from session
- §4c: ChatGPT / Claude / Gemini answer patterns — assumed from training data
- §14c: AI-search surfaces section — wholesale flagged for operator follow-up

Phase 9 is the standing way to close those gaps. Running perplexity-refinement
on a freshly written brief is the highest-ROI use of the Perplexity Pro
subscription for service-research work.

### When to offer (auto-rec upgrade 2026-05-27)

Service briefs are treated as **tier-1-equivalent** for refinement purposes — the
brief carries 12-15 high-tier factual claims as a rule, the §4 / §14c
AI-search gaps are explicitly waiting to be closed, and the brief feeds
every Phase 3a scaffolder run for every client in the domain. Stakes are
high enough that refinement is the strong default.

**Auto-rec rule:** Phase 9 runs an automatic Phase-1 parse on the new
brief (cheap; no queries yet) and always surfaces a calibrated
recommendation. Default depth is `deep` for first refinement of any new
brief. Operator can override.

Skip the offer only if:

- The operator already ran Perplexity manually during Phase 3b (AI-search
  question mining) and pasted answers into the brief — refinement would
  duplicate that work
- The operator explicitly says "skip refinement" or "we'll come back to
  this"

### How to offer

After Phase 8 completes and the Phase-1 parse runs, the executor says:

> "Brief written and knowledge-growth hooks processed. Phase-1 parse on
> the brief found [N] high-tier claims, [M] medium-tier, [K] low-tier.
> The brief flagged [N] explicit AI-search gaps in §4 / §14c.
>
> **Recommendation: run perplexity-refinement at `deep` depth, `append`
> mode.** Reason: first refinement of a new brief; deep depth closes the
> AI-search gaps and validates the load-bearing claims in one pass.
>
> Picks: yes (default) / light / medium / deep / sister-file / skip"

If the operator just says "yes" or doesn't reply within the chat flow,
proceed with the recommended depth and mode.

Recommend `deep` for first refinement of any new brief; the brief
carries 12-15 high-tier claims and `medium`'s cap of 7 would leave most
unrefined.

### What the perplexity-refinement skill does from here

See `[[perplexity-refinement]]/SKILL.md`. Briefly: Phase 1 parses the
brief and tiers claims; Phase 2 runs Pro Search queries via Claude in
Chrome; Phase 3 synthesizes findings into six buckets; Phase 4 writes
back per mode; Phase 5 surfaces follow-ups.

The refinement output lands inside the brief (append mode) or as a sister
file at
`05_shared-intelligence/research-briefs/services/<service-slug>-perplexity-refined-YYYY-MM-DD.md`.
The brief's frontmatter gets `perplexity-refined: YYYY-MM-DD`.

### What this does NOT change about the brief

- Section ordering, "What this feeds" lines, and JSON-shape compatibility
  are unchanged. The Phase 3a scaffolder reads the brief sequentially;
  refinement appended at the bottom doesn't interfere.
- The brief's `status: draft` is unaffected by refinement. Refinement
  may surface that the brief is ready to promote to `status: validated`
  once enough claims are externally backed, but that's an operator
  decision after reviewing the refinement output.
- The brief's `sources-cited:` count gets updated to reflect any new
  sources surfaced via refinement (Phase 5a candidates that get
  ingested through VIS-extraction).

### Refresh-trigger relationship

The brief's §15 methodology names a 6-month default refresh trigger.
After 6 months, re-running perplexity-refinement at `medium` or `deep`
depth with Template 6 (find-updated-info) as the dominant query shape is
the standing refresh path. The refinement output becomes the bulk of
the refresh work; rewrites of the brief body happen only where
refinement surfaces material changes.

---

## Closing step — Auto-invoke output-quality-loop

After the brief is written, refresh-record updated, and any post-brief perplexity-refinement step has resolved, emit the standard auto-invoke block per `~/workspace/skills/output-quality-loop/references/auto-invoke-convention.md` and `~/workspace/second-brain/_meta/conventions.md` § "Output quality". This is the closing step every artifact-producing skill emits before declaring the chat done. Convention shipped Phase 5 of the output-quality-loop project (2026-05-28).

**Artifact list for this skill.** Always include: the service brief itself (e.g., `~/workspace/second-brain/05_shared-intelligence/research-briefs/services/<service-slug>--brief.md`). Optionally include (when this run produced them): the per-service refresh-record entry update if extracted as its own file, any sister "perplexity refinement" file produced by the post-brief refinement step.

**The block to emit (verbatim):**

````markdown
## Auto-invoke output-quality-loop

This skill produced the following artifact(s):
- `<service-brief-path>`

[output-quality-loop:eval] — for each artifact, run output-quality-loop in EVALUATE mode. If PASS, declare the chat done. If NEEDS REVISION or FAIL, ingest the revision prompt as if it were operator input and regenerate the artifact, then re-invoke output-quality-loop. Cap at 3 iterations; on the 3rd FAIL, escalate to the operator with the evaluation report.
````

Required-element discipline per the convention spec: heading text matches verbatim (`## Auto-invoke output-quality-loop`); one bullet per artifact with full path in backticks; directive opens with `[output-quality-loop:eval]` and includes the iteration-cap discipline language.

**Iterate or declare done.** All PASS → declare done. Any NEEDS REVISION (minor / substantive) → Mode 2 auto-fires a revision prompt; ingest as operator input, apply fixes to the brief (tighten a section, add a missing citation, fix a frontmatter field, fill a gap the evaluator flagged), re-emit the block, loop. Any FAIL → revision prompt includes root-cause analysis; address the root cause (often: missing required section, no AI-citation hardening checklist applied, low citation density, voice drift), regenerate, re-emit, loop.

**Iteration cap (3 max).** Track count via the folder-quality-log's per-artifact section before each regeneration. If three iteration entries exist and the verdict is still not PASS, **escalate** to the operator with the evaluation report and stop. Don't run a fourth iteration — that's the load-bearing cost-control discipline.

**Operator bypass.** Include `--bypass-quality-loop` (or "skip the quality loop") in the original brief request to skip the block for that invocation. The bypass records to the closest folder's `_quality-log.md` under `### Bypassed (manual override)`.

---

## Vault stewardship

Per the [[vault-stewardship-principles]]:

1. **Check folder structure before writing.** The brief lives at
   `second-brain/05_shared-intelligence/research-briefs/services/<service-slug>.md`.
   The folder exists; the `_README.md` exists. Don't write the brief
   anywhere else.

2. **Update the folder `_README.md` if needed.** If the folder
   `_README.md` doesn't list new sibling services that have been
   produced recently, propose an edit. Non-destructive — never
   overwrite existing content.

3. **Cross-reference related notes.** The brief's "Related" section
   must wikilink to peer briefs, the parent folder, and the
   template.

4. **Subfolder creation = README update.** If the brief produces
   sub-artifacts (e.g. a Higgsfield prompt log), they live in a
   sibling folder with its own `_README.md`.

---

## Verification — before declaring done

1. **Frontmatter check** — frontmatter is valid YAML, has all
   required fields (`type`, `status`, `created`, `updated`,
   `service-slug`, `domain`, `research-date`, `researcher`,
   `tools-used`, `sources-cited`, `tags`).

2. **Section completeness** — all 15 template sections present, each
   opens with its "What this feeds" line.

3. **Source-attribution check** — every claim has an inline
   citation. Run a grep for sentences with numbers (volumes, word
   counts, link counts) and confirm each has a `[source: …]` tag.

4. **Wikilink check** — extract wikilinks via grep and confirm peer
   links resolve.

5. **Plain-language scan** — scan for unglossed jargon. SERP, schema,
   FAQPage, LCP, CWV, AggregateRating, JSON-LD, etc. should be
   defined inline on first use.

6. **JSON-shape compatibility check** — walk the "How the scaffolder
   consumes this brief" table at the bottom of the template and
   confirm the brief surfaces data for every JSON field in
   `data/services/troubleshooting.json` (or whatever the current
   scaffolder template's JSON shape is). Any gap is a brief defect.

7. **Plain-language pass on a sample paragraph.** Pick the densest
   paragraph in the brief and confirm it reads as plain language.
   If not, run the [[plain-language-translation]] skill on the brief
   retroactively.

---

## Reporting back to the operator

End with a terse summary (per `feedback_terse_completion_reports.md`):

- Brief written to `<path>`
- Top 3 surprises from the research
- Top recommendation for the scaffolder per the competitive-moat
  section
- Blocked questions if any (e.g. "Perplexity wasn't reachable from
  this invocation; please run the head query manually and paste the
  answer")

Use bullets, not paragraphs. Don't restate the brief content —
Oliver can read the file.

---

## Working principles

These are the rules of the road. They shaped the first invocation
(panel-upgrade on 2026-05-26) and should shape every future use.

1. **Cross-client by design.** A Tier-1 brief lives forever. Once
   panel-upgrade is researched, it serves Ahmad, Mohammad, and every
   future electrician client. Don't bake client-specific facts into
   a Tier-1 brief — those go in the Tier-3 intersection brief or the
   client-fact brief.

2. **Source every claim.** No unsourced numbers, no unsourced
   patterns, no unsourced recommendations. The brief is only as
   trustworthy as its weakest claim.

3. **Plain language.** The brief is read by humans and by the
   scaffolder. Both benefit from conversational prose. No jargon
   walls.

4. **Honest about what you couldn't research.** Section 15
   (Methodology) names every research dimension that couldn't be
   completed, with the reason. The brief's credibility comes from
   admitting its gaps, not pretending they don't exist.

5. **Locked template.** Don't restructure the template per
   invocation. The Phase 3a scaffolder reads briefs sequentially —
   if the section order or naming drifts, the scaffolder breaks. If
   the template needs an update, propose it as a separate change,
   then update every existing brief in lockstep.

6. **Quote specifics, avoid hand-waving.** "AJ Long's panel-upgrade
   page is around 2,800 words with a 5-step process and 6 FAQs"
   beats "AJ Long has detailed service pages." Specifics let the
   scaffolder make calibrated decisions; hand-waving doesn't.

7. **Free tools by default.** Don't ask Oliver to sign up for Ahrefs
   Pro mid-research. Use free tools first. If a paid tool would
   genuinely unlock something free tools can't reach, surface that
   as a recommendation.

---

## Reference files

When you need them, read these:

- `~/workspace/second-brain/05_shared-intelligence/research-briefs/_template-service-brief.md`
  — the locked template
- `~/workspace/second-brain/05_shared-intelligence/research-briefs/_README.md`
  — folder index explaining the three-tier model
- `~/workspace/second-brain/05_shared-intelligence/research-briefs/services/panel-upgrade.md`
  — the worked example
- `~/workspace/repos/ai-agency-core/scripts/data/services/troubleshooting.json`
  — the JSON shape the brief's data feeds
- `~/workspace/skills/competitor-deep-research/SKILL.md` — the
  per-client sibling skill this skill calls as a subprocess
- `~/workspace/skills/seo-tooling-landscape-research/SKILL.md` —
  tells which tools to use

---

## Maintenance notes

### M1: Template path dependency (added 2026-05-26, v1.0)

**The issue:** This skill references the canonical template at
`second-brain/05_shared-intelligence/research-briefs/_template-service-brief.md`
by literal path in multiple places. If that file is moved or
renamed, this skill will fail on Pre-flight.

**How to fix:** Search the vault by filename (Glob
`_template-service-brief.md`). Update the paths in this SKILL.md
once the new location is confirmed.

**Why it wasn't designed away:** Single canonical instance is the
simplest design. If the template moves more than once, refactor to
dynamic discovery.

### M2: AI-search reachability from Cowork (added 2026-05-26, v1.0)

**The issue:** Cowork sessions can't always sign into Perplexity,
ChatGPT, Claude.ai, or Gemini. Phase 3b's AI-search question mining
needs human-in-the-loop in those cases.

**How it surfaces:** Phase 3b runs into an authentication wall or
returns empty content.

**How to fix:**

1. Surface the limitation to the operator the first time you hit it
   in a given invocation.
2. Ask the operator to run the head query manually in each
   reachable AI surface and paste the answer back.
3. Capture the manual answers in the brief with citation:
   `[source: perplexity.ai query "<phrase>" on YYYY-MM-DD, operator-pasted]`.

The skill is honest about what it can't reach. Don't fake AI-search
data.

### M3: SERP volatility (added 2026-05-26, v1.0)

**The issue:** The top-10 SERP changes over time. A brief written
in May 2026 may have stale rankings by November 2026.

**How it surfaces:** Phase 3a scaffolder produces pages that compete
against a SERP composition the brief assumed but no longer matches.

**How to fix:** Refresh trigger in the brief's Methodology section.
Default: re-research when the top 3 SERP results materially change,
or once per 6 months, whichever comes first. Quarterly refresh per
active service is a reasonable cadence for the maintenance loop
once the system is live.

---

## How to add a new maintenance note

When the skill errors or produces a calibration miss in production,
add a new entry following the pattern: **Issue → How it surfaces →
How to fix → Why it wasn't designed away.** Date-stamp the entry.
This is how future-Claude learns from past failures without
re-hitting the same wall.

---

## See also (inside the vault)

- `[[client-seo-onboarding-automation]]` — the roadmap this skill
  serves
- `[[_template-service-brief]]` — the locked template
- `[[_README]]` — research-briefs folder index
- `[[services/_README]]` — Tier-1 services folder index
- `[[competitor-deep-research]]` — the per-client research skill
- `[[seo-tooling-landscape-research]]` — informs tool selection
- `[[plain-language-conventions]]` — voice rules
- `[[conventions]]` — KOS naming and frontmatter rules
- `[[plain-language-translation]]` — for retroactive translation
  passes

---

## Peer-reviewer dispatch (GPR-9, gate-peer-reviewer v3.3)

**Gate type:** G-service-brief (closing gate — Check 6 KCA applies).
**Fires after:** Phase 8 knowledge-growth hooks + AI-citation checklist §4.5, before closing.
**Dispatch shape:** Orchestrator spawns the peer-reviewer as a Task sub-agent after the brief is authored and before the closing protocol completes.

**Per-gate dispatch block (Claude Code substrate):**

```
## Peer-reviewer dispatch

Gate type: G-service-brief
Orchestrator: service-seo-research
Project: <client-slug>
Wave: null

Context paths for the Task sub-agent:
- Gate output: <path to authored brief>
- Gate-type registry: ~/workspace/skills/gate-peer-reviewer/references/gate-type-registry.md
- Check spec: ~/workspace/skills/gate-peer-reviewer/references/check-spec.md
- Facts profiles: ~/workspace/skills/gate-peer-reviewer/references/facts-profiles/
- Lesson files: ~/workspace/second-brain/05_shared-intelligence/lessons/ (most recent for this skill)

Task instruction: Read the gate-type registry entry for G-service-brief. Run Check 1 satisfaction targets.
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
gate-id: G-service-brief
orchestrator: service-seo-research
```

Then proceed to close with the skip noted. Skipping is acceptable as long as it's tracked; silently dropping the review step is not.
