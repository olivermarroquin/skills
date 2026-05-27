---
name: city-base-research
description: Produce a Tier-2 city base brief — cross-client, cross-service — that downstream Phase 3b scaffolders consume to author the city-universal half of `data/cities/<city-slug>.json`. Triggers on phrases like "research the city of Vienna VA," "produce a city base brief for X," "run city SEO research on Y," "write the Tier-2 brief for Z city," "do a city-level base brief for [city]," "what's the local context look like for [city]," "city-research [slug]," or any time the operator wants a city-level (not service-level, not client-level, not service-by-city) research output. One argument: the city slug with state suffix (e.g. `vienna-va`, `bethesda-md`). Output: a single markdown file at second-brain/05_shared-intelligence/research-briefs/cities/<city-slug>.md following the locked template at second-brain/05_shared-intelligence/research-briefs/_template-city-brief.md.
---

# City Base Research

A reusable workflow for producing Tier-2 city base briefs. The
briefs sit at
`second-brain/05_shared-intelligence/research-briefs/cities/` and
feed every Phase 3b scaffolder run for every client serving that
city, across every service.

This skill was authored on 2026-05-27 as part of Phase 2b of the
[[client-seo-onboarding-automation]] blueprint. The first brief
produced from it is the Vienna VA brief — refer to it when this
skill's instructions are unclear; it's the worked example.

This skill is a **sibling** to [[service-seo-research]] and
[[competitor-deep-research]], not an extension of either. The three
have different shelf locations, different output shapes, and
different consumers:

- `service-seo-research` outputs `services/<service>.md` —
  cross-client, cross-city, per service
- `city-base-research` outputs `cities/<city-slug>.md` —
  cross-client, cross-service, per city
- `competitor-deep-research` outputs to
  `<client>/admin-extracts/competitor-research/` — per-client,
  cross-service

The three skills sit at the three corners of the (client × service ×
city) cube. Each focuses on one dimension and crosses the other two.

---

## When to use

Trigger this skill when the operator wants city-level (not
client-level, not service-level, not service-by-city) intelligence
about a specific city. Typical triggers:

- "Research the city of Vienna VA"
- "Produce a city base brief for [city]"
- "Write the Tier-2 brief for [city]"
- "Run city SEO research on [city]"
- "Do a city-level base brief for [city]"
- "What's the local context look like for [city]?"
- "City-research [slug]" (terse form when invoking by slug)

Do **not** use this skill for:

- Per-client competitive research (use [[competitor-deep-research]])
- Per-service research (use [[service-seo-research]])
- Per-(service × city) research (use Phase 2c intersection research
  engine — TBD)
- Per-client fact gathering (use Phase 2d client-fact research
  engine — TBD)

---

## Inputs the skill needs

Confirm these with the operator before researching. Present as
plain text — do not use AskUserQuestion (it's been glitching in
Cowork per Oliver's standing feedback memory).

1. **City name and slug.** What's the city, and what slug does it
   live under? Slug must include the two-letter state suffix
   (e.g. `vienna-va`, `bethesda-md`, `silver-spring-md`). The
   state suffix isn't optional — it prevents collisions across
   the dozens of duplicate-named US cities.

2. **County and state context.** Confirm the county the city sits
   in. Some cities span multiple counties or have ambiguous
   jurisdiction (e.g. City of Fairfax vs. Fairfax County — they're
   distinct jurisdictions sharing the name).

3. **Existing-research carry-overs.** Has a competitor-deep-
   research synthesis already covered this city's competitive
   layer? Has a sibling city brief already covered a neighbor
   that shares utility / county / AHJ context? Carry forward what
   you can — the utility-company section, the AHJ section, and
   the climate-quirks section are often shared across neighboring
   cities in the same county.

4. **Output folder.** Default:
   `~/workspace/second-brain/05_shared-intelligence/research-briefs/cities/`.
   Override only if the operator wants the brief written
   somewhere else (rare).

5. **Time budget.** Useful to know up-front. Typical budget for a
   city brief from scratch: 60-90 minutes (Census ACS lookup +
   neighborhood directory crawl + utility/AHJ identification +
   infrastructure-quirks audit + Google Trends pass + synthesis).
   With a neighboring-city brief already done: 30-45 minutes
   (most of utility/AHJ/county quirks carry forward).

If any input is missing, ask the operator before researching.
Underspecified inputs are the most common failure mode for this
skill.

---

## Pre-flight: read the canonical template and worked example

Before producing anything new, read:

1. The locked template:
   `~/workspace/second-brain/05_shared-intelligence/research-briefs/_template-city-brief.md`
   — every section, every "What this feeds" line, every
   consumption contract with the Phase 3b scaffolder.

2. The worked example (when it exists):
   `~/workspace/second-brain/05_shared-intelligence/research-briefs/cities/vienna-va.md`
   — what a finished brief looks like.

3. The scaffolder data shape:
   `~/workspace/repos/ai-agency-core/scripts/data/cities/vienna-va.json`
   and `~/workspace/repos/ai-agency-core/scripts/data/cities/fairfax-va.json`
   — the JSON contract the brief feeds. Both files exist because
   different cities frame the HQ-distance relationship differently
   (Vienna = "10-15 min away," Fairfax = "around the corner").

4. The folder conventions:
   `~/workspace/second-brain/_meta/conventions.md` — frontmatter
   and naming rules.

5. The plain-language conventions:
   `~/workspace/second-brain/_meta/plain-language-conventions.md`.

If the template has moved or been renamed, search the vault by
filename (Glob `_template-city-brief.md`). If not found, the
template's content is described in the template file linked above —
fall back to that.

---

## High-level workflow

The skill runs in seven phases. Each phase produces a section of
the final brief; don't skip phases — the Phase 3b scaffolder and
the downstream Phase 2c intersection briefs depend on every
section.

1. **Confirm inputs** (above).
2. **Administrative + geographic basics** — name, slug, county,
   ZIPs, AHJ, utilities.
3. **Demographics + neighborhoods** — ACS data, neighborhood
   inventory, housing-stock decade buckets.
4. **Infrastructure quirks** — utility coordination norms, code
   adoption, HOA prevalence, climate.
5. **Local ecosystem + search behavior** — chamber, BBB,
   directories, branded city search volume, Google Trends curve,
   AI-search city representation.
6. **City-universal positioning facts** — EV adoption, solar
   density, home-age distribution, seasonal patterns.
7. **Synthesis and write-up** — assemble the brief from sections
   1-12 of the locked template, in order.

Mark each phase as a task in the operator's task list so they can
see progress.

---

## Phase 1 — Confirm inputs

Present the input list as plain text. Wait for the operator's
answers before proceeding. Underspecified inputs ruin the output.

If the operator carries forward a sibling city brief from a
neighbor in the same county, read that file first and capture the
findings that apply (utility, AHJ, climate, code adoption). Most
of those sections can be lifted with light edits.

---

## Phase 2 — Administrative + geographic basics

This phase populates Sections 1 (city identity + administrative
basics) and 2 (geographic anchor) of the template.

### 2a. Identity + ZIPs + jurisdiction

Tools:

- **city.gov** site — the city's own website is the authoritative
  source for incorporation type, founding year, official ZIP
  list. Use `mcp__workspace__web_fetch` first; escalate to
  `mcp__Claude_in_Chrome__navigate` + `get_page_text` if the
  site is client-rendered.
- **County GIS / zoning lookup** — confirms the county
  jurisdiction and identifies overlapping ZIP boundaries.
- **USPS ZIP lookup** (`tools.usps.com/zip-lookup`) — confirms the
  ZIPs that serve the city.
- **data.census.gov city profile** — confirms population, land
  area, incorporated-place status.

### 2b. AHJ for permits

Tools:

- **County government site** — for most US suburbs, residential
  electrical permits are county-level. Find the building / land-
  development division.
- **City government site** — some incorporated towns add a city-
  level review on top of the county permit. Confirm or rule out.
- **NEC / IRC adoption ordinance** — locate the most recent
  adoption ordinance to confirm which code year is in effect.

Note the office name, URL, online-filing support, typical
turnaround, and any city-level layering.

### 2c. Utility companies

Tools:

- **State public utility commission** (e.g. Virginia SCC) — lists
  utility service areas by jurisdiction.
- **Utility company sites** (Dominion Energy, Washington Gas,
  Pepco, etc.) — confirm service area coverage.
- **City government site** — sometimes the city runs its own
  water + sewer; sometimes the county runs it.

Capture every utility serving the city (electric, gas, water,
sewer, trash, internet) with name + service-area note + URL.

### 2d. Geographic anchor

Tools:

- **Google Maps** — boundary visualization, drive times to
  reference cities.
- **City government site** — official boundary descriptions.
- **Wikipedia** — neighborhood-anchor descriptions, major road
  list.

Draft the 2-4 sentence geographic-anchor paragraph in the template's
shape, ready to drop into the JSON.

---

## Phase 3 — Demographics + neighborhoods

This phase populates Sections 3 (neighborhoods inventory), 4
(demographics), and 5 (housing stock patterns) of the template.

### 3a. Demographics — Census ACS pass

Tools (ranked):

- **data.census.gov** — the authoritative source. ACS 5-year
  estimates have the most demographic depth at the city/town
  level. Pull median household income, income bracket
  distribution, owner-occupancy rate, median home value, age
  distribution, household composition, educational attainment,
  occupational segments, languages spoken, commute pattern.
- **City government site demographic profile** — often has a
  prettied-up version of the ACS data plus interpretation.
- **niche.com / areavibes.com** — useful for cross-validation but
  not authoritative; cite the Census, not these.

The Census Bureau's lookup hierarchy can be confusing. The right
geography is usually "place" (incorporated places like cities and
towns) rather than "tract" or "block group." For unincorporated
communities, use the CDP (Census Designated Place) profile if
one exists; otherwise fall back to the county-subdivision level
and note the proxy in §12 (Methodology).

### 3b. Neighborhoods inventory

Tools (ranked):

- **City government site** — sometimes has an official neighborhood
  list with descriptions.
- **realtor.com / redfin.com neighborhood pages** — the realtor
  data is curated and named with the names locals use.
- **Wikipedia** — most US cities have a "Neighborhoods" section
  on the Wikipedia page.
- **Local newspaper coverage** — for the housing-stock decade
  breakdown per neighborhood, local news coverage is often the
  best source.
- **Patch.com city page** — covers neighborhood news; useful for
  identifying named neighborhoods locals actually reference.

For each neighborhood, fill in name + blurb + dominant housing
decade + approximate boundaries + notable features + demographic
tilt. Aim for 6-12 entries.

### 3c. Housing-stock patterns

Per Section 5 of the template, group housing into 2-4 decade
buckets. For each bucket, fill in title + neighborhood examples +
context paragraph. **Leave the `symptoms` field as `<TBD by
intersection brief>`** — it's service-specific and gets filled in
by Phase 2c.

Anchor the context paragraph to the era's real construction
conventions (panel size, wiring, plumbing, HVAC, insulation) per
the reference points in the template's Section 5.

---

## Phase 4 — Infrastructure quirks

This phase populates Section 6 of the template.

Tools:

- **Utility-company tariffs and operations pages** — for the
  electric utility's disconnect-coordination norms, the gas
  utility's residential-service policies, etc. These are the
  authoritative sources, not contractor blogs.
- **AHJ webpage** — for permitting quirks, inspection turnaround,
  any city-vs-county layering.
- **County code adoption ordinance** — for which NEC / IRC / IPC
  versions are in effect.
- **HOA prevalence proxy** — the realtor sites usually note "HOA
  community" in neighborhood profiles; cross-tabulate with
  Section 3 to estimate HOA prevalence.
- **NWS climate data** (`weather.gov`) — for the climate /
  weather quirks (freeze risk, storm history, flooding zones).

Capture electrical, plumbing, HVAC, permitting, code-adoption,
HOA, and climate quirks. Each fact gets a primary-source citation.

**Don't source infrastructure facts from contractor blogs** —
contractor blogs restate what AHJs and utilities publish, with no
added value and a higher risk of drift.

---

## Phase 5 — Local ecosystem + search behavior

This phase populates Sections 7 (local competitor business
landscape, generic) and 8 (local search behavior) of the template.

### 5a. Local ecosystem

Tools:

- **Chamber of Commerce** site — confirm existence, count
  members, evaluate signal strength.
- **BBB site** (`bbb.org`) — confirm city-level accredited-
  business count and regional signal strength.
- **Patch.com city page** — useful for confirming which directories
  locals actually use.
- **Yelp / Google Business Profile** — sanity check on directory
  usage in the city.
- **Local newspaper** — identify the dominant local news outlet
  for content-outreach planning.

### 5b. Search behavior

Tools (ranked):

- **DataForSEO API** — `keywords_data/google_ads/search_volume`
  for branded city queries. Pay-as-you-go (~$0.0005-0.005 per
  query). Set credentials from tier-3 vault.
- **Google Trends** (`trends.google.com`) — 5-year interest curve
  for the city name. Free. Navigate via Claude in Chrome if
  programmatic access is blocked.
- **Ahrefs free Keyword Generator** (`ahrefs.com/keyword-generator`)
  — light keyword lookups, free 1 query per few hours.
- **Manual Google search** — autocomplete suggestions reveal
  what locals type. Useful for identifying common misspellings
  and state-abbreviation usage.

### 5c. AI-search city representation

Tools:

- **Google AI Overviews** — search "what's <city> known for" and
  capture the Overview if it renders.
- **Perplexity** (`perplexity.ai`) — run the same query, capture
  sources cited and the natural-language answer.
- **ChatGPT** (`chat.openai.com`) — run the query in a chat with
  web browsing enabled. Capture the answer.

Per the [[service-seo-research]] skill's AI-search subsection,
escalate to manual operator-paste if AI surfaces aren't reachable
from the current Cowork session. Don't fake the data.

---

## Phase 6 — City-universal positioning facts

This phase populates Section 10 of the template.

For each fact you want to capture (EV adoption, solar density,
home-age distribution, new-construction trajectory, income
concentration, seasonal demand, city-government initiatives),
identify the primary source:

- **EV adoption** — state DMV registration data (e.g. Virginia
  DMV publishes EV registration by ZIP), or
  `afdc.energy.gov/vehicle-registration` (federal aggregate),
  or the utility's EV-tariff filings.
- **Solar density** — Department of Energy LBNL "Tracking the
  Sun" report, the utility's solar-interconnection reports.
- **Home-age distribution** — Census ACS housing variables
  (B25034 = year structure built).
- **New-construction trajectory** — Census Building Permits
  Survey, county recorder filings, city planning department.
- **Income concentration** — Census ACS B19001 (income brackets)
  + B19083 (Gini index).
- **Seasonal demand** — NWS climate normals + insurance industry
  data (often public via FEMA flood maps, NWS storm history).
- **City initiatives** — city sustainability dashboards,
  city-council resolutions, state energy office programs.

Each fact gets a 1-2 sentence framing ready for Phase 2c briefs to
pull verbatim.

**Don't cite contractor blogs for these facts.** They restate the
primary source with no added value and break the brief's
authority.

---

## Phase 7 — Synthesis and write-up

Open the locked template
(`~/workspace/second-brain/05_shared-intelligence/research-briefs/_template-city-brief.md`)
and produce a brief at
`~/workspace/second-brain/05_shared-intelligence/research-briefs/cities/<city-slug>.md`
following the template exactly.

Apply these rules:

### File structure and frontmatter

```yaml
---
type: research-brief
brief-tier: city
status: draft
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
city-slug: <city-slug-with-state>
city-name: <City Name>
state: <STATE_ABBR>
county: <County Name>
research-date: <YYYY-MM-DD>
researcher: city-base-research-skill
tools-used: [<list of tools actually consulted>]
sources-cited: <integer>
tags: [research-brief, tier-2, city, <state-abbr>]
---
```

Filename: `<city-slug>.md` — no `brief-` prefix (these are
descriptive cross-domain reference docs, like the service briefs).
Slug always includes the two-letter state.

### Required sections

All 12 sections from the locked template, in order:

1. City identity and administrative basics
2. Geographic anchor
3. Neighborhoods inventory
4. Demographics
5. Housing stock patterns
6. Local infrastructure quirks
7. Local competitor business landscape (generic)
8. Local search behavior + general search trends
9. Service-area neighbors
10. City-universal positioning facts
11. Sources cited
12. Methodology

Plus the "How the scaffolder consumes this brief" table at the
bottom (lift from template — same for every brief).

Each section opens with the template's **What this feeds** line so
the Phase 3b scaffolder reader knows which JSON fields the section
serves.

### Source-attribution requirement

Every claim in the brief must trace to a primary source —
government data, utility document, AHJ webpage, mapping service,
or keyword/trends tool. Inline citation format:

```
[source: <type> <reference> on YYYY-MM-DD]
```

Examples:

- `[source: data.census.gov ACS 5-year 2018-2022 for Vienna town,
  VA on 2026-05-27]`
- `[source: webfetch fairfaxcounty.gov/landdevelopment/ on
  2026-05-27]`
- `[source: dominionenergy.com tariff for VA on 2026-05-27]`
- `[source: trends.google.com "Vienna, VA" 5-year on 2026-05-27]`

Section 11 (Sources cited) is the roll-up of all inline citations,
grouped by source type. The brief's `sources-cited:` frontmatter
field is the count of distinct sources in that roll-up.

**Don't cite contractor blogs as primary sources for city facts.**
They restate what authoritative sources publish.

### Plain-language requirement

Per [[plain-language-conventions]], write the brief in plain
language. Gloss jargon inline the first time it appears (AHJ,
ACS, NEC, IRC, HOA, CDP, etc.). The brief is read by Oliver
(operator) and by the Phase 3b scaffolder — neither benefits from
dense whitepaper voice.

### Honest-assessment requirement

Per Oliver's standing preferences captured across multiple
memories: call out when a city's data is thin, when an AHJ's
turnaround is unusually slow, when a utility's coordination
overhead changes service economics. Don't sugarcoat.

### Wikilink rules

Slug-only wikilinks for files with unique filenames:
`[[vienna-va]]`, `[[plain-language-conventions]]`. Path-based
wikilinks for ambiguous filenames like project READMEs:
`[[ev-electric-services/README]]`.

Every brief must link to:

- The parent folder README (`[[_README]]` or `[[cities/_README]]`)
- The locked template (`[[_template-city-brief]]`)
- The blueprint (`[[client-seo-onboarding-automation]]`)
- Any sibling city briefs in the same county (they often share
  AHJ + utility + climate context)
- The plain-language conventions

---

## Vault stewardship

Per the [[vault-stewardship-principles]]:

1. **Check folder structure before writing.** The brief lives at
   `second-brain/05_shared-intelligence/research-briefs/cities/<city-slug>.md`.
   The folder exists; the `_README.md` exists. Don't write the brief
   anywhere else.

2. **Update the folder `_README.md` if needed.** When the brief
   adds the first or second city to the folder, propose an
   edit to `cities/_README.md` to list it. Non-destructive —
   never overwrite existing content.

3. **Cross-reference related notes.** The brief's "Related"
   section must wikilink to peer briefs in the same county, the
   parent folder, and the template.

---

## Verification — before declaring done

1. **Frontmatter check** — frontmatter is valid YAML, has all
   required fields (`type`, `brief-tier`, `status`, `created`,
   `updated`, `city-slug`, `city-name`, `state`, `county`,
   `research-date`, `researcher`, `tools-used`, `sources-cited`,
   `tags`).

2. **Section completeness** — all 12 template sections present,
   each opens with its "What this feeds" line.

3. **Source-attribution check** — every claim has an inline
   citation. Run a grep for sentences with numbers
   (demographic stats, drive times, ZIP codes, monthly volume)
   and confirm each has a `[source: …]` tag.

4. **Wikilink check** — extract wikilinks via grep and confirm
   peer links resolve.

5. **Plain-language scan** — scan for unglossed jargon. AHJ,
   ACS, NEC, IRC, HOA, CDP, GSC should be defined inline on
   first use.

6. **JSON-shape compatibility check** — walk the "How the
   scaffolder consumes this brief" table at the bottom of the
   template and confirm the brief surfaces data for every JSON
   field in `data/cities/vienna-va.json` (the reference shape).
   Any gap that isn't explicitly deferred to Phase 2c is a
   brief defect.

7. **Plain-language pass on a sample paragraph.** Pick the
   densest paragraph in the brief and confirm it reads as
   plain language. If not, run the [[plain-language-translation]]
   skill on the brief retroactively.

---

## Reporting back to the operator

End with a terse summary (per `feedback_terse_completion_reports.md`):

- Brief written to `<path>`
- Top 3 surprises from the research
- Top recommendation for the Phase 2c intersection briefs per
  the city-universal positioning facts (§10)
- Blocked questions if any (e.g. "Perplexity wasn't reachable
  from this invocation; please run the head query manually and
  paste the answer")

Use bullets, not paragraphs. Don't restate the brief content —
Oliver can read the file.

---

## Working principles

These are the rules of the road. They shaped the first invocation
(Vienna VA on 2026-05-27) and should shape every future use.

1. **Cross-client by design.** A Tier-2 brief lives forever.
   Once Vienna is researched, it serves Ahmad (electrician),
   Mohammad (electrician), a future plumber, a future HVAC
   contractor — every Keelworks client serving Vienna. Don't
   bake client-specific or service-specific facts into a Tier-2
   brief. Service-specific stuff goes in Tier 3
   intersection briefs; client-specific stuff goes in client-fact
   briefs.

2. **Primary sources only.** City facts come from
   `data.census.gov`, utility tariffs, AHJ webpages, official
   city/county sites, NWS climate data, and similar
   authoritative sources. **Contractor blogs are not primary
   sources** — they restate the authoritative source with no
   added value and a higher risk of drift.

3. **Plain language.** The brief is read by humans and by the
   scaffolder. Both benefit from conversational prose. No jargon
   walls.

4. **Honest about what you couldn't research.** Section 12
   (Methodology) names every research dimension that couldn't
   be completed, with the reason. The brief's credibility comes
   from admitting its gaps, not pretending they don't exist.

5. **Locked template.** Don't restructure the template per
   invocation. The Phase 3b scaffolder reads briefs sequentially
   — if the section order or naming drifts, the scaffolder
   breaks. If the template needs an update, propose it as a
   separate change, then update every existing brief in
   lockstep.

6. **Defer service-specific facts.** Anything keyed by service
   (electrical symptoms, plumbing symptoms, HVAC symptoms;
   service-specific keyword volume; service-specific
   competitors) goes to Phase 2c. The city brief captures the
   city-universal fact that the intersection brief will pull
   from (e.g. EV adoption density is city-universal; the
   electrical-page phrasing about EV-charger circuits is
   service-specific).

7. **Quote specifics, avoid hand-waving.** "Vienna's median
   household income is $169,381 per ACS 2018-2022" beats
   "Vienna is wealthy." Specifics let the scaffolder make
   calibrated decisions; hand-waving doesn't.

8. **Carry forward where possible.** Neighboring cities in the
   same county share utility, AHJ, climate, and code-adoption
   context. When briefing a second city in a county that
   already has one, read the neighbor's brief first and lift
   the shared sections with light edits.

---

## Reference files

When you need them, read these:

- `~/workspace/second-brain/05_shared-intelligence/research-briefs/_template-city-brief.md`
  — the locked template
- `~/workspace/second-brain/05_shared-intelligence/research-briefs/_README.md`
  — folder index explaining the three-tier research model
- `~/workspace/second-brain/05_shared-intelligence/research-briefs/cities/_README.md`
  — Tier 2 cities folder README
- `~/workspace/second-brain/05_shared-intelligence/research-briefs/cities/vienna-va.md`
  — the worked example
- `~/workspace/repos/ai-agency-core/scripts/data/cities/vienna-va.json`
  and `~/workspace/repos/ai-agency-core/scripts/data/cities/fairfax-va.json`
  — the JSON shape the brief's data feeds
- `~/workspace/skills/service-seo-research/SKILL.md` — the
  Tier 1 sibling skill
- `~/workspace/skills/competitor-deep-research/SKILL.md` — the
  per-client sibling skill that the city skill calls as a
  research input (for the local-competitor-ecosystem section)

---

## Maintenance notes

### M1: Template path dependency (added 2026-05-27, v1.0)

**The issue:** This skill references the canonical template at
`second-brain/05_shared-intelligence/research-briefs/_template-city-brief.md`
by literal path in multiple places. If that file is moved or
renamed, this skill will fail on Pre-flight.

**How to fix:** Search the vault by filename (Glob
`_template-city-brief.md`). Update the paths in this SKILL.md
once the new location is confirmed.

**Why it wasn't designed away:** Single canonical instance is the
simplest design. If the template moves more than once, refactor
to dynamic discovery.

### M2: Census ACS staleness (added 2026-05-27, v1.0)

**The issue:** The 5-year ACS estimates update annually but
trail real-time by ~2 years. A brief written using
ACS 2018-2022 reflects mid-pandemic data; ACS 2019-2023 (when
it lands) will reflect the post-pandemic shift. Income
brackets, owner-occupancy, and commute patterns moved
materially in many cities.

**How it surfaces:** A brief's demographic claims feel stale to
locals who know the city has changed.

**How to fix:** Refresh trigger in the brief's Methodology
section. Default: when the ACS releases a new 5-year vintage,
re-pull §4 of every brief that's older than 12 months. The
re-pull is cheap (Census lookup only).

### M3: AHJ + utility changes are rare but high-impact (added 2026-05-27, v1.0)

**The issue:** A city changes its building department's online
system, or a utility merges / spins off and the service-area
boundaries shift, or the city adopts a new NEC year. These
events are rare (1-2 per city per decade) but make the brief
materially wrong when they happen.

**How it surfaces:** A Phase 3b scaffolder run produces a page
that references the wrong AHJ URL or the wrong utility name.

**How to fix:** Annual refresh check on §1 (administrative
basics) and §6 (infrastructure quirks). If anything moved, the
brief gets a focused update; the rest of the brief stays.

---

## How to add a new maintenance note

When the skill errors or produces a calibration miss in
production, add a new entry following the pattern:
**Issue → How it surfaces → How to fix → Why it wasn't designed
away.** Date-stamp the entry. This is how future-Claude learns
from past failures without re-hitting the same wall.

---

## See also (inside the vault)

- `[[client-seo-onboarding-automation]]` — the roadmap this skill
  serves (Phase 2b)
- `[[_template-city-brief]]` — the locked template
- `[[_README]]` — research-briefs folder index
- `[[cities/_README]]` — Tier 2 cities folder index
- `[[service-seo-research]]` — the Tier 1 sibling skill
- `[[competitor-deep-research]]` — the per-client research skill
- `[[plain-language-conventions]]` — voice rules
- `[[conventions]]` — KOS naming and frontmatter rules
- `[[plain-language-translation]]` — for retroactive translation
  passes
