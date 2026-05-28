---
name: intersection-research
description: Produce a Tier-3 service × city intersection brief — per-(service, city) cell, cross-client — that downstream Phase 3b scaffolders consume to fill the service-keyed slots inside `data/cities/<city-slug>.json` (quick_ref_localized_items, most_common_problem_paragraph, specific_problems_neighborhood_phrase, ev_charger_homes_phrase, and the per-pattern symptoms field). Triggers on phrases like "intersection-research panel-upgrade vienna-va," "run the Tier 3 brief for {service} in {city}," "produce an intersection brief for {service}--{city}," "city-specific competitor research for {service} in {city}," "what does the SERP look like for {service} in {city}," "research the {service} × {city} cell," "Phase 2c on {service} {city}," or any time the operator wants per-(service, city) intelligence (not Tier 1 service base, not Tier 2 city base, not per-client). Two required arguments: service-slug and city-slug-with-state. Output: a single markdown file at second-brain/05_shared-intelligence/research-briefs/intersections/<service-slug>--<city-slug>.md following the locked template at second-brain/05_shared-intelligence/research-briefs/_template-intersection-brief.md.
---

# Intersection Research

A reusable workflow for producing Tier-3 service × city intersection
briefs. The briefs sit at
`second-brain/05_shared-intelligence/research-briefs/intersections/`
and feed every Phase 3b scaffolder run for every client serving that
specific (service, city) cell.

This skill was authored on 2026-05-27 as part of Phase 2c of the
[[client-seo-onboarding-automation]] blueprint. The first brief
produced from it is the `panel-upgrade × vienna-va` brief — refer to
it when this skill's instructions are unclear; it's the worked
example.

This skill is a **sibling** to [[service-seo-research]],
[[city-base-research]], and [[competitor-deep-research]] — not an
extension of any of them. The four sit at the four corners of the
research model:

- `service-seo-research` → Tier 1, cross-client, cross-city, per
  service. Output: `services/<service-slug>.md`.
- `city-base-research` → Tier 2, cross-client, cross-service, per
  city. Output: `cities/<city-slug>.md`.
- `intersection-research` (this skill) → Tier 3, cross-client,
  per (service, city) cell. Output:
  `intersections/<service-slug>--<city-slug>.md`.
- `competitor-deep-research` → per-client, cross-service. Output:
  `<client>/admin-extracts/competitor-research/`.

Each skill stays disjoint by tier. This skill **calls**
`competitor-deep-research` as a subprocess when the per-cell top 3
overlaps with an already-researched competitor (carry the findings
forward instead of re-researching); it does not replace
`competitor-deep-research`.

---

## When to use

Trigger this skill when the operator wants per-(service, city)
intelligence — the local, time-sensitive layer that Tier 1 and Tier
2 can't carry. Typical triggers:

- "Intersection-research panel-upgrade vienna-va"
- "Run the Tier 3 brief for panel-upgrade in Vienna"
- "Produce an intersection brief for panel-upgrade--vienna-va"
- "What does the SERP look like for panel upgrade in Vienna VA?"
- "City-specific competitor research for {service} in {city}"
- "Research the {service} × {city} cell"
- "Phase 2c on panel-upgrade vienna-va"

Do **not** use this skill for:

- Tier 1 service research (use [[service-seo-research]])
- Tier 2 city research (use [[city-base-research]])
- Per-client competitive research (use [[competitor-deep-research]])
- Per-client fact gathering (use Phase 2d client-fact research
  engine — TBD)

---

## Inputs the skill needs

Confirm these with the operator before researching. Present as plain
text — do not use AskUserQuestion (it's been glitching in Cowork per
Oliver's standing feedback memory).

1. **Service slug.** Must match an existing Tier 1 service brief at
   `services/<service-slug>.md`. If the Tier 1 brief doesn't exist
   yet, stop and tell the operator: "The Tier 1 service brief for
   `<service-slug>` doesn't exist. Run `service-seo-research` first."
   Examples: `panel-upgrade`, `troubleshooting`, `ev-charger`,
   `whole-house-rewire`.

2. **City slug (with two-letter state suffix).** Must match an
   existing Tier 2 city brief at `cities/<city-slug>.md`. If the
   Tier 2 brief doesn't exist yet, stop and tell the operator:
   "The Tier 2 city brief for `<city-slug>` doesn't exist. Run
   `city-base-research` first." Examples: `vienna-va`,
   `bethesda-md`, `fairfax-va`.

3. **Existing-research carry-overs.** Has a `competitor-deep-research`
   synthesis already covered any of the city-tied competitors for
   this service? (E.g. the EV Electric 2026-05-23 Fairfax County
   synthesis covered AJ Long, Mr. Electric, Absolute, and Kolb for
   residential electrical.) Carry findings forward. If yes, name
   the synthesis file so the skill reads it instead of re-fetching
   the competitors.

4. **Output folder.** Default:
   `~/workspace/second-brain/05_shared-intelligence/research-briefs/intersections/`.
   Override only rarely.

5. **Time budget.** Useful to know up-front. Typical budget for an
   intersection brief from scratch: 45-75 minutes (live SERP for
   the head query + audit top 3 + localized keyword volume + AI-
   chat questions across reachable surfaces + PAA + Google Maps
   review mining). With a competitor-deep-research carry-over:
   25-40 minutes.

If any input is missing, ask the operator before researching.
Two-arg invocations ("`intersection-research panel-upgrade
vienna-va`") are fine; if either slug doesn't exist as a parent
brief, surface the dependency.

---

## Pre-flight: read the canonical template, both parent briefs, and the worked example

Before producing anything new, read:

1. **The locked template:**
   `~/workspace/second-brain/05_shared-intelligence/research-briefs/_template-intersection-brief.md`
   — every section, every "What this feeds" line, every consumption
   contract with the Phase 3b scaffolder.

2. **The Tier 1 service brief:**
   `~/workspace/second-brain/05_shared-intelligence/research-briefs/services/<service-slug>.md`.
   This brief is your authoritative source for what the service IS,
   how it's named, what the universal FAQ patterns are, what the
   universal symptom patterns are, what the universal pricing-
   visibility norms are. You will NOT re-derive any of this — the
   intersection brief layers city-specific findings on top of the
   service-universal layer the Tier 1 brief already established.

3. **The Tier 2 city brief:**
   `~/workspace/second-brain/05_shared-intelligence/research-briefs/cities/<city-slug>.md`.
   This brief is your authoritative source for what the city IS:
   neighborhoods, housing stock distribution, infrastructure
   quirks, AHJ, utility companies, demographics, the city-universal
   positioning facts in §10. You will pull from §10 in particular
   when filling §2's "specific local angles hit" column and the
   `specific_problems_neighborhood_phrase` slot.

4. **The worked example** (when it exists):
   `~/workspace/second-brain/05_shared-intelligence/research-briefs/intersections/panel-upgrade--vienna-va.md`.

5. **The scaffolder data shape:**
   `~/workspace/repos/ai-agency-core/scripts/data/cities/vienna-va.json`
   — the JSON contract the brief's service-keyed slots feed.

6. **Folder conventions:**
   `~/workspace/second-brain/_meta/conventions.md`.

7. **Plain-language conventions:**
   `~/workspace/second-brain/_meta/plain-language-conventions.md`.

If either parent brief (Tier 1 service or Tier 2 city) is missing,
STOP and surface the dependency to the operator. The intersection
brief layers on top of the parents; without them it has no
foundation.

---

## High-level workflow

The skill runs in seven phases. Each phase produces a section of the
final brief; don't skip phases — the Phase 3b scaffolder depends on
every section.

1. **Confirm inputs and read parents** (above).
2. **Live SERP capture for the head query** — top 3 contractor
   service-pages for "{service} in {city, state}".
3. **Per-competitor audit** — for each of the top 3, fetch the
   ranking page and capture the cell-specific competitor card.
4. **Localized keyword volume** — head term + 5-10 long-tail variants
   tied to this cell.
5. **AI-chat question mining** — head query through every reachable
   AI surface; capture answer shape and cited sources.
6. **Localized FAQ themes** — Google "People also ask" expansion +
   the AI-surface answers from Phase 5; distill the 6-10 questions
   the city page must answer.
7. **Google Maps review mining + write-up** — pull the top 3
   competitors' Google Maps reviews, mine for praise + complaint
   themes; assemble the brief.

Mark each phase as a task in the operator's task list so they can
see progress.

---

## Phase 1 — Confirm inputs and read parents

Present the input list as plain text. Wait for the operator's answers
before proceeding. Both parent briefs MUST exist — confirm by Glob /
Read before continuing.

If the operator carries forward a `competitor-deep-research` synthesis,
read that file first and capture the cell-tied findings. Most of the
§2 per-competitor audit work may already be done if the synthesis
already audited city-overlapping competitors.

---

## Phase 2 — Live SERP capture for the head query

Run `WebSearch` for the head query: `<service> in <city>, <state>`
(use the city's natural-language form, e.g. "panel upgrade in
Vienna, VA"). Also run the 2-3 close variants from the Tier 1
brief's §3a (e.g. "electrical panel upgrade Vienna VA", "200 amp
panel upgrade Vienna").

For each search, capture the top 10 organic results. From those,
identify the top 3 that are:

- Real contractor service-pages (not directories, not editorial)
- Specifically targeting the cell — either dedicated city-pages
  ("Panel Upgrade in Vienna, VA") or service-pages that explicitly
  list Vienna as a service area

Exclude:

- Directories: Yelp, BBB, Angi, Checkbook, Houzz, Thumbtack,
  Yellow Pages, Nextdoor
- Editorial / informational pages: This Old House, Homewyse, Angi
  editorial, Rewiring America, contractor-blog aggregators
- The client's own pages (note separately as §2.5 "where the
  Keelworks client currently ranks")

If fewer than 3 real contractor pages appear in the top 10 for the
head query, broaden to the top 20 OR include service-pages from
nearby cities (e.g. a Fairfax panel-upgrade page that lists Vienna
in service-area). Flag the broadening in §7 (Methodology).

Build the §2 top-3 list. Number them by SERP rank for the head
query as of the research date.

**SPA fallback.** If `mcp__workspace__web_fetch` returns empty
content for a result, the site is client-rendered. Escalate to
`mcp__Claude_in_Chrome__navigate` + `mcp__Claude_in_Chrome__get_page_text`
if available; otherwise flag in §7 as "blocked — JS-rendered" and
move on. Don't fake the audit.

---

## Phase 3 — Per-competitor audit (top 3)

For each of the top 3 from Phase 2, run the §2 audit:

### Step 1: Fetch the ranking page

Use `mcp__workspace__web_fetch` to pull the exact page ranking for
the head query. Capture:

- Domain, page URL, page title
- Estimated word count (from the fetched markdown)
- Image style (stock / branded composite / real on-site / AI /
  owner-face-visible)
- Pricing transparency (published $-ranges / estimate-only / mixed)

### Step 2: Audit the schema

Search the fetched HTML for `application/ld+json`. Capture the
`@type` values present (LocalBusiness, Service, FAQPage,
AggregateRating, BreadcrumbList, etc.) or note "none detected." If
the page is JS-rendered, escalate to Claude in Chrome for a
rendered fetch.

### Step 3: Domain authority lookup

Free tools first:

- Ahrefs free Backlink Checker (`ahrefs.com/backlink-checker`) —
  shows Domain Rating (DR) for free, 1-3 queries per IP per day
- Moz Link Explorer free — shows DA (Domain Authority)

Cite which tool was used. If neither was reachable, skip and note
in §7.

### Step 4: Extract local angles

Read the page's body. Identify every city-specific or local angle:

- Named neighborhoods the page mentions
- Named local landmarks (e.g. Wolf Trap, the W&OD trail)
- Named utility companies (e.g. Dominion Energy)
- Named permit offices (e.g. Town of Vienna, Fairfax County LDS)
- Named brands of equipment the page calls out (e.g. Federal
  Pacific, Zinsco) — these often have local prevalence patterns
- Named regulations (e.g. "Virginia adopted the 2020 NEC in 2024")
- Named ZIPs (e.g. 22180, 22182)

The Phase 3b scaffolder uses this list to voice the
`specific_problems_neighborhood_phrase` and the localized
`most_common_problem_paragraph` slots. The more specific local
angles surface across competitors, the stronger the consensus
signal for what to include in the Keelworks page.

### Step 5: Capture in-body phrasing for the head query

Quote the top 3 in-body phrases the page uses to refer to the
service in this city — verbatim, in quotes. These are the exact
phrases the buyer searched and the SERP rewarded.

### Step 6: Write the competitor card

Use the §2 card structure from the template — table of fields plus
2-4 sentence prose summary in plain language. Cite every claim
inline.

### Step 7: Cross-competitor synthesis

After all three cards are written, write the §2 "Cross-competitor
synthesis" subsection. 3-5 sentences. Lead with:

- What's universal across all three (table-stakes — every page does
  this; doing it doesn't differentiate)
- What gaps NONE of the three fill (moat opportunities — the local
  angles, the schema, the FAQ depth, the imagery style, the
  voicing)

This subsection is what the Phase 3b scaffolder uses to voice
`most_common_problem_paragraph[<service-slug>]`. The synthesis is
the load-bearing strategic deliverable in the brief.

---

## Phase 4 — Localized keyword volume

This phase populates §3 of the template.

### 4a. Head term + close variants — precise numbers when available

Tools, ranked by preference:

**Programmatic (preferred):**

- **DataForSEO API** — `keywords_data/google_ads/search_volume`
  for the head query and 3-5 close variants. Pay-as-you-go
  (~$0.0005-0.005 per query). Set credentials from tier-3 vault
  (`DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD`).

**Browser-driven (via Claude in Chrome):**

- **Ahrefs free Keyword Generator** — limited free queries per IP
- **Keyword Surfer Chrome extension** — overlays volume + competition
  on Google SERP when navigating Google search

**Free-with-caps fallbacks:**

- **Manual Google autocomplete** — captures the long-tail variants
  buyers actually type; volume is unknown but the phrase is real
- **Ubersuggest free** — limited free queries per day

If DataForSEO isn't configured yet, use the free path and ship the
brief with directional volume signals + a flagged Methodology gap.
Don't fabricate volume numbers.

### 4b. Long-tail variants tied to this cell

Mine for 5-10 long-tail variants from:

- The Tier 1 service brief's §3b (long-tail commercial keywords) —
  swap `{city}` for the actual city
- Google autocomplete on the head query plus 2-3 close variants
- Tier 1 brief's §3c (PAA questions) — convert each question into
  a city-tied phrase
- Local industry-specific phrases the §2 competitor cards surfaced
  in their in-body language

Each entry gets the phrase + volume (if known) + source.

### 4c. PAA for the head query

Run a Google search for the exact head query in a Chrome session.
Capture the PAA box's 3-5 questions verbatim. These directly seed
§5.

---

## Phase 5 — AI-chat question mining

This phase populates §4 of the template.

Use Claude in Chrome to navigate the AI surfaces. Confirm a
connected browser via `mcp__Claude_in_Chrome__list_connected_browsers`
before starting. If empty, ask the operator to install / launch the
Claude in Chrome extension and re-invoke.

Run the head query (and 1-2 close variants) through each reachable
surface:

### 5a. Google AI Overviews

Navigate to a Google search for the head query. Capture whether an
AI Overview renders and what sources it cites. Quote the Overview's
structure verbatim — the structure is the outline our city page
needs to satisfy to be citation-worthy.

### 5b. Perplexity

Navigate to `perplexity.ai`. Run the head query. Capture sources
cited (list of URLs in order) and the answer's natural-language
form (first 200-300 words). Perplexity cites most aggressively;
the source list is gold.

### 5c. ChatGPT

Navigate to `chat.openai.com`. Run the head query in a chat with
web browsing enabled. Capture cited sources and answer pattern.

### 5d. Claude (claude.ai) and Gemini (gemini.google.com)

Same procedure. Capture answer shape and citation pattern.

### 5e. Distill the "questions our city-page must answer" list

Aggregate across all surfaces and the PAA capture (§4c). The 6-10
questions that appear in at least two surfaces get the §4d table.

**If any AI surface is unreachable from the session**, flag in §7
Methodology and recommend operator-paste follow-up. Don't fake the
data.

---

## Phase 6 — Localized FAQ themes

This phase populates §5 of the template.

### 6a. Universal PAA themes for this cell

For each of the 3-5 PAA questions from §4c, capture:

- Canonical wording (as PAA shows it)
- Average answer length when PAA expands (50-120 words typical)
- Whether the answer is city-anchored or generic

### 6b. The "no competitor answers this well" gap

Of the §4c PAA questions plus the §5e distilled list, identify
which 1-2 questions appear in AI search or PAA but are NOT well
answered by any of the §2 top 3 competitor pages. These are the
competitive-moat FAQs to include in the city page.

Cite each finding inline.

---

## Phase 7 — Google Maps review mining + write-up

### 7a. Google Maps review mining

For each of the top 3 competitors (§2), navigate to their Google
Business Profile (search the business name + city in Google Maps
via Claude in Chrome). Capture:

- Total review count + average rating (as of the research date)
- Sample 20-30 reviews per competitor across the rating
  distribution (5-star, 4-star, 3-star, 2-star, 1-star)
- Recurring praise themes (what locals consistently call out as
  positive)
- Recurring complaint themes (what locals consistently call out
  as negative)
- Service-specific themes — reviews that explicitly mention this
  service (panel upgrade, EV charger, etc.)

### 7b. Cross-competitor review synthesis

- What locals consistently want from this service in this city (3-5
  attributes universal across the top 3's positive reviews)
- What locals consistently complain about (2-3 recurring negative
  themes across the top 3's one-and-two-star reviews)
- What's not said — gaps in the review corpus that the Keelworks
  page can highlight

**If Google Maps review mining is blocked from the session**, flag
in §7 Methodology and ship the brief with §6 as a "to-be-completed"
placeholder. Browser-driven extraction via Claude in Chrome is the
primary path; if neither path works, recommend operator-paste
follow-up.

### 7c. Assemble the brief

Open the locked template
(`~/workspace/second-brain/05_shared-intelligence/research-briefs/_template-intersection-brief.md`)
and produce a brief at
`~/workspace/second-brain/05_shared-intelligence/research-briefs/intersections/<service-slug>--<city-slug>.md`
following the template exactly.

Apply these rules:

#### File structure and frontmatter

```yaml
---
type: research-brief
brief-tier: intersection
status: draft
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
service-slug: <service-slug>
city-slug: <city-slug-with-state>
city-name: <City Name>
state: <STATE_ABBR>
research-date: <YYYY-MM-DD>
researcher: intersection-research-skill
tools-used: [<list of tools actually consulted>]
sources-cited: <integer>
tags: [research-brief, tier-3, intersection, <service-slug>, <state-abbr>]
---
```

Filename: `<service-slug>--<city-slug>.md` — double hyphen separates
the two slugs (the convention is locked in
`intersections/_README.md`).

#### Required sections

All 8 sections from the locked template, in order:

1. Intersection identity and head query
2. Top 3 city-specific competitors
3. Localized keyword volume
4. AI-chat questions for this cell
5. Localized FAQ themes
6. Localized review themes
7. Methodology
8. Sources cited

Plus the "How the scaffolder consumes this brief" table at the
bottom (lift from template — same for every brief).

Each section opens with the template's **What this feeds** line so
the Phase 3b scaffolder reader knows which JSON slots the section
serves.

#### Source-attribution requirement

Every claim must trace to a live SERP capture, a competitor page
fetch, an AI-search run, a keyword tool query, a Google Maps
reviews extraction, or an existing vault note. Inline citation
format:

```
[source: <type> <reference> on YYYY-MM-DD]
```

Examples:

- `[source: webfetch https://ajlongelectric.com/panel-upgrade-vienna-va/ on 2026-05-27]`
- `[source: WebSearch query "panel upgrade in Vienna, VA" on 2026-05-27]`
- `[source: perplexity.ai query "best panel upgrade contractor Vienna VA" on 2026-05-27]`
- `[source: google maps reviews AJ Long Electric sample of 25 reviews on 2026-05-27]`
- `[source: [[panel-upgrade|Tier 1 panel-upgrade brief]] on 2026-05-26]`

Section 8 is the roll-up. The brief's `sources-cited:`
frontmatter field is the count of distinct sources in that
roll-up.

#### Plain-language requirement

Per [[plain-language-conventions]], gloss SEO and code jargon
inline the first time it appears. The brief is read by Oliver
(operator) and by the Phase 3b scaffolder — neither benefits from
dense whitepaper voice.

#### Honest-assessment requirement

Per Oliver's standing preferences: call out hype, name AI-surface
gaps explicitly, name review-mining gaps explicitly, don't
sugarcoat competitor strength. If a competitor's Vienna page is
genuinely strong, say so. If only 1 of the 3 has a dedicated
Vienna page and the other 2 just list Vienna in service-area,
call that out — it changes what "top 3" means in this cell.

#### Wikilink rules

Slug-only wikilinks for files with unique filenames:
`[[panel-upgrade]]`, `[[vienna-va]]`, `[[plain-language-conventions]]`.
Path-based wikilinks for ambiguous filenames like project READMEs:
`[[ev-electric-services/README]]`.

Every brief must link to:

- The parent folder README (`[[intersections/_README]]`)
- The locked template (`[[_template-intersection-brief]]`)
- The Tier 1 service brief (`[[<service-slug>]]`)
- The Tier 2 city brief (`[[<city-slug>]]`)
- Any client-side competitor-research synthesis the brief carried
  findings from
- The plain-language conventions

---

## Closing step — Auto-invoke output-quality-loop

After the intersection brief is written and the cross-link back to parent service + city briefs has been added, emit the standard auto-invoke block per `~/workspace/skills/output-quality-loop/references/auto-invoke-convention.md` and `~/workspace/second-brain/_meta/conventions.md` § "Output quality". This is the closing step every artifact-producing skill emits before declaring the chat done. Convention shipped Phase 5 of the output-quality-loop project (2026-05-28).

**Artifact list for this skill.** The intersection brief itself (e.g., `~/workspace/second-brain/05_shared-intelligence/research-briefs/intersections/<service>--<city>.md`). If a sibling-client positioning addendum was added during this run (per the Phase-1 spot-check pattern from 2026-05-28), the brief is still one artifact — the addendum is a section, not a separate file.

**The block to emit (verbatim):**

````markdown
## Auto-invoke output-quality-loop

This skill produced the following artifact(s):
- `<intersection-brief-path>`

[output-quality-loop:eval] — for each artifact, run output-quality-loop in EVALUATE mode. If PASS, declare the chat done. If NEEDS REVISION or FAIL, ingest the revision prompt as if it were operator input and regenerate the artifact, then re-invoke output-quality-loop. Cap at 3 iterations; on the 3rd FAIL, escalate to the operator with the evaluation report.
````

Required-element discipline per the convention spec: heading text matches verbatim (`## Auto-invoke output-quality-loop`); one bullet per artifact with full path in backticks; directive opens with `[output-quality-loop:eval]` and includes the iteration-cap discipline language.

**Iterate or declare done.** All PASS → declare done. Any NEEDS REVISION (minor / substantive) → Mode 2 auto-fires a revision prompt; ingest as operator input, apply fixes to the brief (tighten a SERP-comparison section, add a missing review-mined customer-phrase, fix an AI-overview citation, fill a gap the evaluator flagged), re-emit the block, loop. Any FAIL → revision prompt includes root-cause analysis; address the root cause (often: parent brief not actually loaded, top-3-competitor coverage incomplete, no AI-citation hardening checklist applied, voice drift), regenerate, re-emit, loop.

**Iteration cap (3 max).** Track count via the folder-quality-log's per-artifact section before each regeneration. If three iteration entries exist and the verdict is still not PASS, **escalate** to the operator with the evaluation report and stop. Don't run a fourth iteration — that's the load-bearing cost-control discipline.

**Operator bypass.** Include `--bypass-quality-loop` (or "skip the quality loop") in the original brief request to skip the block for that invocation. The bypass records to the closest folder's `_quality-log.md` under `### Bypassed (manual override)`.

---

## Vault stewardship

Per the [[vault-stewardship-principles]]:

1. **Check folder structure before writing.** The brief lives at
   `second-brain/05_shared-intelligence/research-briefs/intersections/<service-slug>--<city-slug>.md`.
   The folder exists; the `_README.md` exists. Don't write the
   brief anywhere else.

2. **Update the folder `_README.md` if needed.** When the brief
   adds the first or second intersection to the folder, propose an
   edit to `intersections/_README.md` to list it. Non-destructive
   — never overwrite existing content.

3. **Cross-reference related notes.** The brief's "Related"
   section must wikilink to both parent briefs, the parent folder,
   and the template.

---

## Verification — before declaring done

1. **Frontmatter check** — frontmatter is valid YAML, has all
   required fields (`type`, `brief-tier`, `status`, `created`,
   `updated`, `service-slug`, `city-slug`, `city-name`, `state`,
   `research-date`, `researcher`, `tools-used`, `sources-cited`,
   `tags`).

2. **Section completeness** — all 8 template sections present, each
   opens with its "What this feeds" line. Plus the consumption-
   contract table at the bottom.

3. **Top 3 named** — the §2 top 3 are real, named businesses with
   live URLs. No generic placeholders. If only 2 cleared the
   contractor-page filter, that's the §7 Methodology disclosure;
   don't pad to 3 with directory pages.

4. **Source-attribution check** — every claim has an inline
   citation. Run a grep for sentences with numbers (volumes, word
   counts, review counts, ratings) and confirm each has a
   `[source: …]` tag.

5. **Wikilink check** — extract wikilinks via grep and confirm
   peer links resolve. Both parent briefs MUST link.

6. **Plain-language scan** — scan for unglossed jargon. SERP,
   schema, FAQPage, PAA, AI Overview, LocalBusiness, AggregateRating
   should be defined inline on first use.

7. **JSON-shape compatibility check** — walk the "How the scaffolder
   consumes this brief" table at the bottom of the template and
   confirm the brief surfaces enough data for the Phase 3b
   scaffolder to populate every service-keyed slot in
   `data/cities/<city-slug>.json`:
   - `quick_ref_localized_items[<service-slug>][]` (6-8 entries)
   - `most_common_problem_paragraph[<service-slug>]`
   - `specific_problems_neighborhood_phrase[<service-slug>]`
   - `ev_charger_homes_phrase` (electrical-domain only)
   - `housing_patterns[].symptoms` per pattern in the Tier 2 brief

   Any gap is a brief defect.

8. **Plain-language pass on a sample paragraph.** Pick the densest
   paragraph in the brief and confirm it reads as plain language.
   If not, run [[plain-language-translation]] on the brief
   retroactively.

---

## Reporting back to the operator

End with a terse summary (per `feedback_terse_completion_reports.md`):

- Brief written to `<path>`
- Top 3 named competitors and their SERP ranks for the head query
- The 1-2 moat opportunities the §2 synthesis surfaced
- Top recommendation for the Phase 3b scaffolder per the
  service-keyed slot contracts
- Blocked questions if any (AI surfaces, Google Maps reviews,
  DataForSEO)

Use bullets, not paragraphs. Don't restate the brief content —
Oliver can read the file.

---

## Working principles

These shape every invocation. They mirror the working principles of
the sibling Tier 1 and Tier 2 skills, adapted for the cell layer.

1. **Cross-client by design.** A Tier-3 brief lives forever. Once
   `panel-upgrade × vienna-va` is researched, it serves Ahmad,
   Mohammad, and every future electrician client serving Vienna.
   Don't bake client-specific facts into the intersection brief —
   client-specific stuff goes in the client-fact brief (Phase 2d).

2. **Layer on top of parents, don't re-derive.** The Tier 1 brief
   already established the service identity, schema patterns,
   content depth norms, FAQ patterns at the universal level. The
   Tier 2 brief already established the city's neighborhoods,
   housing stock, AHJ, utilities, demographics. This brief
   layers cell-specific findings on top. If you find yourself
   re-deriving anything in the Tier 1 or Tier 2 brief, stop and
   reference the parent instead.

3. **Top 3 must be real contractor pages.** No directories, no
   editorial pages, no generic placeholders. If only 2 cleared
   the filter, surface that fact in §7 Methodology and ship with
   2 — don't pad with directories.

4. **Source every claim.** No unsourced numbers, no unsourced
   patterns, no unsourced AI-search answers. The brief is only as
   trustworthy as its weakest claim.

5. **Plain language.** The brief is read by humans and by the
   scaffolder. Both benefit from conversational prose.

6. **Honest about what you couldn't research.** §7 (Methodology)
   names every research dimension that couldn't be completed,
   with the reason. The brief's credibility comes from admitting
   its gaps, not pretending they don't exist.

7. **Locked template.** Don't restructure the template per
   invocation. The Phase 3b scaffolder reads briefs sequentially
   — if the section order or naming drifts, the scaffolder
   breaks. If the template needs an update, propose it as a
   separate change, then update every existing brief in lockstep.

8. **Quote specifics, avoid hand-waving.** "AJ Long's
   panel-upgrade Vienna page leads with 'Vienna's older homes were
   built for a different electrical world'" beats "AJ Long has a
   localized Vienna page." Specifics let the scaffolder make
   calibrated decisions; hand-waving doesn't.

9. **Carry forward where possible.** When this brief targets a
   cell already partially covered by a `competitor-deep-research`
   synthesis (e.g. Fairfax County electrician work covered by the
   2026-05-23 synthesis), read the synthesis first and lift the
   cell-overlapping findings. Re-deriving wastes budget.

10. **Free tools by default.** Don't ask the operator to sign up
    for Ahrefs Pro mid-research. Use what's available. If a paid
    tool would genuinely unlock something free tools can't reach,
    surface that as a recommendation, don't silently consume
    budget.

---

## Reference files

When you need them, read these:

- `~/workspace/second-brain/05_shared-intelligence/research-briefs/_template-intersection-brief.md`
  — the locked template
- `~/workspace/second-brain/05_shared-intelligence/research-briefs/_README.md`
  — folder index explaining the three-tier research model
- `~/workspace/second-brain/05_shared-intelligence/research-briefs/intersections/_README.md`
  — Tier 3 folder index
- `~/workspace/second-brain/05_shared-intelligence/research-briefs/intersections/panel-upgrade--vienna-va.md`
  — the worked example
- `~/workspace/repos/ai-agency-core/scripts/data/cities/vienna-va.json`
  — the JSON shape the brief's service-keyed slots feed
- `~/workspace/skills/service-seo-research/SKILL.md` — Tier 1
  sibling
- `~/workspace/skills/city-base-research/SKILL.md` — Tier 2
  sibling
- `~/workspace/skills/competitor-deep-research/SKILL.md` —
  per-client sibling; called as a subprocess when a client-side
  synthesis covers cell-overlapping competitors

---

## Maintenance notes

### M1: Template path dependency (added 2026-05-27, v1.0)

**The issue:** This skill references the canonical template at
`second-brain/05_shared-intelligence/research-briefs/_template-intersection-brief.md`
by literal path in multiple places. If that file is moved or
renamed, this skill will fail on Pre-flight.

**How to fix:** Search the vault by filename (Glob
`_template-intersection-brief.md`). Update the paths in this
SKILL.md once the new location is confirmed.

**Why it wasn't designed away:** Single canonical instance is the
simplest design. If the template moves more than once, refactor
to dynamic discovery.

### M2: Parent-brief dependency (added 2026-05-27, v1.0)

**The issue:** This skill requires both the Tier 1 service brief
and the Tier 2 city brief to exist before producing the Tier 3
intersection brief. If either is missing, the brief has no
foundation.

**How it surfaces:** Pre-flight fails on parent-brief Read.

**How to fix:** Surface the missing dependency to the operator
and recommend running `service-seo-research` or `city-base-research`
first. Don't try to derive missing parent facts inline — that
violates the three-tier separation.

**Why it wasn't designed away:** The three-tier model is the
architectural choice. Skipping a tier produces brittle briefs
that fail on Phase 3b consumption.

### M3: Top-3 sufficiency (added 2026-05-27, v1.0)

**The issue:** Some (service, city) cells have fewer than 3 real
contractor pages ranking. Padding to 3 with directories or
editorial pages weakens the brief.

**How it surfaces:** Phase 2 SERP capture returns <3 contractor
pages after directory + editorial filtering.

**How to fix:** Broaden to the top 20 OR include service-pages
from nearby cities (e.g. a Fairfax page listing Vienna in
service-area). Flag the broadening in §7 (Methodology). If the
broadening still doesn't yield 3, ship with 2 and disclose.

**Why it wasn't designed away:** The "real contractor pages only"
filter is load-bearing — diluting it would defeat the brief's
purpose.

### M4: AI-search reachability from Cowork (added 2026-05-27, v1.0)

**The issue:** Cowork sessions can't always sign into Perplexity,
ChatGPT, Claude.ai, or Gemini. Phase 5 needs human-in-the-loop in
those cases.

**How it surfaces:** Phase 5 runs into an authentication wall or
returns empty content.

**How to fix:** Same playbook as the sibling Tier 1 skill's M2 —
surface to operator, ask for manual paste-back, cite
`[source: perplexity.ai query "<phrase>" on YYYY-MM-DD,
operator-pasted]`. Don't fake AI-search data.

### M5: Google Maps review extraction (added 2026-05-27, v1.0)

**The issue:** Google Maps review mining via web_fetch is
typically blocked (JS-rendered + sign-in required). Claude in
Chrome via a signed-in browser is the recommended path; without
it, §6 can't be filled.

**How it surfaces:** Phase 7a returns empty or partial data.

**How to fix:** Confirm a connected browser via
`mcp__Claude_in_Chrome__list_connected_browsers` before Phase 7a.
If no connected browser, surface to operator, ask for the
browser to be opened, and re-invoke. If the operator can't run
Claude in Chrome, ship the brief with §6 flagged for operator-
paste follow-up — don't fake review themes.

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
  serves (Phase 2c)
- `[[_template-intersection-brief]]` — the locked template
- `[[_README]]` — research-briefs folder index
- `[[intersections/_README]]` — Tier 3 folder index
- `[[service-seo-research]]` — Tier 1 sibling skill
- `[[city-base-research]]` — Tier 2 sibling skill
- `[[competitor-deep-research]]` — per-client sibling skill
- `[[plain-language-conventions]]` — voice rules
- `[[conventions]]` — KOS naming and frontmatter rules
- `[[plain-language-translation]]` — for retroactive translation
  passes
