---
name: competitor-architecture-diff
version: 1.0
status: active
created: 2026-06-19
updated: 2026-06-19
substrate: claude-code
reusability: reusable-as-is
domains: [content-strategy, competitive-analysis]
composes-with: [content-coverage-audit, prioritization, site-capture-engine, competitor-deep-research]
tags: [skill, competitor-mining, content-architecture, expansion-backlog, DA-sprint]
---

# Skill: Competitor Architecture Diff

**Purpose:** Given competitor teardown data (URL inventories, extracted schemas,
content samples) and our current output set, classify what structural surfaces
(page types, section types, content formats, schema patterns) the competitor
has that we don't, and emit a ranked expansion backlog.

**DA-sprint origin:** Created as [DA3] — the AJ-Long teardown's URL inventories
are a content-architecture map of how a winning competitor structures their site.
We were mining it only for keywords/volumes, leaving structural surface area on
the table.

## Cross-project reusability

The engine is **domain-agnostic**. All SEO/electrical/Core-30 specifics live in
a **profile**. Given any competitor teardown (produced by `site-capture-engine` /
`competitor-deep-research`) + a description of our current output set, the engine
diffs architectures and emits expansion candidates. The profile specifies:

- Where the competitor teardown data lives
- How to classify competitor URLs into page types
- What our current output set looks like (page types + section types)
- Ranking criteria for expansion candidates
- Which prioritization profile to use for sequencing

## Inputs

| Input | Source | Required |
|---|---|---|
| `profile` | `references/profiles/<name>.yaml` | Yes |
| `teardown_base` | Directory containing competitor teardown data | Yes |
| `our_output_set` | Description of our current page/section types | In profile |
| `data_sources` | Paths to our city/service data for supportability check | In profile |

## Procedure

### Step 1: Parse competitor content architecture

Read the competitor's URL inventories from the teardown directory:
- `urls-services.txt` → service pages (base + city variants)
- `urls-problems.txt` → problem/symptom pages
- `urls-neighborhoods.txt` → neighborhood pages
- `urls-guides.txt` → guide/educational pages
- `urls-core.txt` → core site pages (about, contact, etc.)
- `urls-blog.txt` → blog content (if present)
- `urls-locations.txt` → location pages (if present)
- `service-city-presence-grid.tsv` → service×city matrix

For each URL inventory:
1. Count total URLs
2. Extract the page-type taxonomy (URL path structure → page type classification)
3. Parse any extracted `schema.json` + `content.txt` files to identify:
   - On-page modules (FAQ, HowTo, pricing tables, review blocks, etc.)
   - Schema types emitted per page type
   - Content sections visible in the content extraction

Output: a **competitor architecture map** — a structured dict of page types,
each with: count, URL pattern, schema types, on-page modules, sample URLs.

### Step 2: Map our current output set

From the profile's `our_output_set` definition, build a structured map of what
we currently produce:
- Page types (e.g., service×city landing pages)
- Section types per page (e.g., hero, quick-ref, pattern-cards, FAQ, pricing)
- Schema types per page (e.g., LocalBusiness, Service, FAQPage)
- Content formats (e.g., single HTML page, no blog, no guides)

### Step 3: Diff architectures

Compare the two maps. For each competitor surface, classify as:

- **`we-have`** — we produce this surface (page type, section type, or schema)
- **`we-lack-supportable`** — competitor has it, we don't, BUT our existing
  data sources could support building it (e.g., we have neighborhood data that
  could power dedicated neighborhood pages)
- **`we-lack-new-data`** — competitor has it, we don't, AND we'd need new data
  or research to build it (e.g., problem-specific symptom research we haven't done)
- **`not-applicable`** — competitor surface that doesn't apply to our model
  (e.g., careers page, AI assistant)

For `we-lack-supportable`, check the profile's `data_sources` to verify the
data actually exists. Don't claim supportable without evidence.

### Step 4: Emit expansion backlog

Two categories:

**A. New SECTION types for existing pages** (supportable from current data):
- Identify sections/modules the competitor uses within page types we already
  have (service×city pages) that we don't include
- Check if our data sources can populate them
- Examples: problem-cluster Q&A blocks, neighborhood-specific problem sections,
  issues-by-home-era sections, HowTo schema blocks

**B. Candidate new PAGE types** (net-new page categories):
- Identify page types the competitor has that we lack entirely
- For each, note: demand signal (URL count, implied search intent),
  data availability (what we'd need), effort estimate, reuse potential
- Examples: problem pages, neighborhood pages, guide pages

Each candidate gets:
- `name` — descriptive name
- `type` — `new-section` or `new-page-type`
- `competitor_evidence` — what the competitor has (URL count, sample URLs, schema)
- `our_data_status` — `supportable` or `needs-new-data`, with specifics
- `demand_signal` — evidence of search demand (URL count, keyword presence)
- `effort` — `low` / `medium` / `high`
- `reuse_potential` — `high` / `medium` / `low` (can other clients use this?)
- `rationale` — why this matters

### Step 5: Rank and sequence

Pass the expansion backlog to the `prioritization` skill with the profile
specified in `ranking_profile`. The prioritization skill sequences it alongside
existing build items. Don't invent a bespoke ranker.

### Step 6: Feed DA1

Emit the architecture-diff output in a format the `content-coverage-audit`
skill can consume for its L3 "competitor-axis expansion" lens:
- A structured JSON file at the profile's `cca_feed_path` with the diff results
- The CCA profile's `competitor_architecture.inventory_source` points to this

### Step 7: Output

Two files:
- `<output_dir>/architecture-diff-<competitor>-<date>.md` — human-readable report
- `<output_dir>/architecture-diff-<competitor>-<date>.json` — machine-readable findings

The JSON follows this shape:
```json
{
  "competitor": "<slug>",
  "profile": "<profile-id>",
  "generated": "YYYY-MM-DD",
  "competitor_architecture": {
    "<page-type>": {
      "count": N,
      "url_pattern": "...",
      "schema_types": [],
      "on_page_modules": [],
      "sample_urls": []
    }
  },
  "our_architecture": {
    "<page-type>": { ... }
  },
  "diff": {
    "we_have": [],
    "we_lack_supportable": [],
    "we_lack_new_data": [],
    "not_applicable": []
  },
  "expansion_backlog": {
    "new_sections": [ ... ],
    "new_page_types": [ ... ]
  },
  "cca_feed": { ... }
}
```

## Acceptance criteria (per invocation)

1. Architecture diff covers every URL inventory file in the teardown
2. ≥3 new section types identified (supportable from current data)
3. ≥2 candidate new page types identified (with demand + effort notes)
4. Each candidate has rationale tied to a competitor surface we lack
5. Backlog is sequenced via the prioritization skill (not a bespoke ranker)
6. CCA feed file emitted for L3 composition
7. Architecture-diff is reusable from config on a different client's teardown

## Profiles

Profiles live in `references/profiles/`. Each profile specifies:

```yaml
profile_id: <name>
competitor_slug: <slug>
teardown_base: <path to teardown data/>
our_output_set:
  page_types:
    - name: <type>
      sections: [...]
      schema: [...]
  section_types: [...]
data_sources:
  - name: <source>
    path: <glob or dir>
    provides: [<what fields/data>]
ranking_profile: <prioritization profile name>
cca_feed_path: <output path for CCA L3 feed>
output_dir: <where to write reports>
```

## Composition

- **Upstream:** `site-capture-engine` / `competitor-deep-research` produce the
  teardown data this skill consumes
- **Downstream:** `content-coverage-audit` L3 lens consumes the CCA feed;
  `prioritization` sequences the backlog
- **Parallel:** runs alongside DA2 (depth-parity) and DA4 (verify-page)

## Quality gates

- `output-quality-loop` on both output files
- `gate-peer-reviewer` with `G-default` gate type
