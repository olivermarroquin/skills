---
type: reference
status: active
created: 2026-06-23
updated: 2026-06-23
skill: reference-finder
tags: [reference, discovery-lanes, reference-finder, design-inspiration-system]
---

# Discovery lanes — reference-finder v1.0

Six lanes for sourcing candidate reference sites. Each lane has a distinct method, source,
and provenance format. Lanes run in parallel where possible. The profile's `active_lanes`
list controls which lanes fire on a given run.

**Key principle:** the design-led lane reads the shared `_source-catalog.md` as its seed
list — it does NOT hardcode galleries. The catalog is the living registry; this file documents
how each lane consumes it.

---

## Lane 1 — Performance-led (SERP rankers)

### Method

Compose `competitor-deep-research` v1.4 Tier-2 light scan. Provide:
- **Sector:** from the profile (e.g., `electrical-services`)
- **Geography:** from the profile or operator input (e.g., `Fairfax County, VA`)
- **Seed queries:** high-intent queries for the sector (e.g., `electrician fairfax va`,
  `electrical contractor northern virginia`, `emergency electrician [city]`)

Extract the top-ranking domains from the Tier-2 scan results. Each domain becomes a candidate
with ranking evidence attached.

### Source

- **Primary:** DataForSEO SERP data via `competitor-deep-research` (paid, ~$0.10-0.20 per scan).
- **Fallback:** Free-toolkit Google search (WebSearch tool) for the seed queries, excluding
  directories (Yelp, BBB, Angi, Thumbtack, Yellow Pages, Nextdoor, Houzz, Checkbook).

### Provenance format

```
performance-led / competitor-deep-research / [query] / [geo] / [YYYY-MM-DD]
```

### Prompt templates (seed queries)

Per sector, the profile defines 3-5 seed queries. Examples for `electrical-services`:

```yaml
seed_queries:
  - "electrician {geo}"
  - "electrical contractor {geo}"
  - "emergency electrician {geo}"
  - "residential electrician near me {geo}"
  - "commercial electrical services {geo}"
```

`{geo}` is replaced at runtime with the geography parameter.

### ToS / cost notes

- DataForSEO cost: ~$0.02-0.05 per SERP query. Budget ~$0.10-0.20 per sector scan.
- Free-toolkit fallback: $0 but lower precision (no traffic estimates, no keyword counts).
- Respect DataForSEO rate limits. Batch queries where possible.

### When to run

Always — performance evidence is the strongest signal for high-performing classification.
This lane is the primary source for high-performing-candidate classification.

---

## Lane 2 — Design-led (galleries + awards)

### Method

1. Read `05_shared-intelligence/discovery-sources/_source-catalog.md`.
2. Filter to rows where `Feeds` includes `design` or `both`.
3. For each source, respect the `Crawl` column:
   - `web_fetch` → use the web_fetch tool (server-rendered, works from sandbox)
   - `Chrome` → escalate to Claude-in-Chrome (JS-rendered galleries)
4. Fetch the source's recent/featured listings page. Parse candidate site URLs from the listings.
5. Each extracted URL becomes a candidate with the gallery as provenance.

### Source

The `_source-catalog.md` design-feed rows. As of 2026-06-23 (34 sources):

**Design galleries (11):** Site of Sites, Awwwards, Land-book, Godly, SiteInspire, Httpster,
Lapa Ninja, Mobbin, The FWA, CSS Design Awards, One Page Love

**Both-feed sources (4):** Land-book, Lapa Ninja, One Page Love, SaaS Landing Page (saaslandingpage.com)

**Listicles (4):** Wisepops, Adobe, Lovable, SpinX (static, lower leverage)

The catalog grows over time — this lane automatically picks up new `design`/`both` rows.

### Provenance format

```
design-led / [source-name] / [listing-url-or-page] / [YYYY-MM-DD]
```

### Fetching discipline

- **Recent/featured only.** Fetch the homepage or "latest" / "featured" / "winners" page of
  each gallery. Do NOT attempt to scrape full archives.
- **Pagination:** Follow at most 2-3 pages of results per source per run. Diminishing returns
  beyond that.
- **Rate limiting:** 2-3 second delay between requests to the same domain.
- **robots.txt:** Check and respect. If robots.txt blocks the listings page, skip the source
  and note it in the run log.
- **Gallery links fan-out:** If the operator drops a gallery URL in manual-add mode, the lane
  fetches that page and extracts all candidate site URLs from it (a gallery link becomes N
  candidate URLs).

### When to run

Always for design-quality candidates. Highest yield lane for design-only references. Lower
yield for high-performing candidates (galleries curate for aesthetics, not SEO performance).

---

## Lane 3 — AI-answer-led (Perplexity Sonar)

### Method

Query Perplexity Sonar API (`perplexity_sonar.py` at the tier-3 carve-out) with sector-specific
prompts. Parse cited URLs from responses. Each cited URL becomes a candidate.

### Source

Perplexity Sonar API. The only programmatic Perplexity surface — the full search product is
not available via API.

### Prompt templates

```yaml
prompts:
  - "What are the best-designed {sector} websites in 2026?"
  - "Which {sector} companies have the highest-converting websites?"
  - "Most innovative {sector} website designs"
  - "Best {sector} website examples for small businesses"
```

`{sector}` replaced at runtime. Queries are intentionally broad to surface diverse candidates.

### Provenance format

```
ai-answer-led / sonar / [query-slug] / [YYYY-MM-DD]
```

### Yield expectations

Lower yield than direct gallery pulls. Sonar citations tend toward well-known sites rather than
hidden gems. Useful for cross-referencing: a site that appears in BOTH Sonar results AND gallery
listings has stronger signal.

### Cost

~$0.005-0.01 per query (Sonar pricing). Budget ~$0.03-0.05 per sector scan (3-5 queries).

### When to run

Useful as a cross-reference signal. Run alongside Lane 1 + Lane 2 but weight results lower
in the composite ranking unless cross-confirmed by another lane.

---

## Lane 4 — Expansion-led (from existing keepers)

### Method

From a high-performer already in the library:

**(a) Competitive adjacency:** Run the keeper's domain through `competitor-deep-research` to
find its direct competitors. Each competitor becomes a candidate.

**(b) Agency portfolio:** From the keeper's dossier tech fingerprint, identify the building
agency or developer. Find their portfolio page → extract other sites they built. Each becomes
a candidate.

**(c) Similar-site services:** Check the keeper's domain on `alternativeto.net` (in the
`_source-catalog.md` as a product directory) or similar services for adjacent domains.

### Source

Existing library dossiers (high-performing lane) + `competitor-deep-research` + agency portfolios.

### Provenance format

```
expansion-led / [seed-domain] / [method: competitive|agency|similar] / [YYYY-MM-DD]
```

### Prerequisites

Library must have ≥3 high-performing entries for this lane to produce meaningful results.
Below that threshold, the seed pool is too small.

### When to run

After the library has sufficient high-performing entries. Best used in `expand` mode when the
operator points at a specific keeper. Also runs automatically in `discover` mode when the
library meets the prerequisite threshold.

---

## Lane 5 — Manual-add (VIS-style operator intake)

### Method

Operator drops a URL → run through the full vetting pipeline (dedup → pre-screen → classify →
score). No discovery step — the human IS the discovery.

If the operator drops a **gallery link** (detected by matching against `_source-catalog.md`
source URLs), fan out: fetch that gallery page, extract listed site URLs, and vet each as a
separate candidate.

### Source

Operator input. This lane is always available regardless of profile configuration.

### Provenance format

```
manual-add / operator / [YYYY-MM-DD]
```

### When to run

Any time the operator has a URL to evaluate. Zero-friction intake path.

---

## Lane 6 — Meta-list harvester

### Method

1. Read `_source-catalog.md` meta-list rows (currently 4: toools.design 100-list,
   awesome-saas-directories, saasconsult 40+ directories, Duhan 100 free platforms).
2. Fetch the meta-list page (respecting `Crawl` column).
3. Parse the listed galleries/directories/sources.
4. For each discovered source, draft a proposed `_source-catalog.md` row:
   - Name, URL, Feeds tag (design/product/both), Crawl method (web_fetch/Chrome),
     Yields/notes (one-line guess), Provenance.
5. **Surface the proposed rows to the operator for approval.** Never auto-add.
6. Approved rows are appended to `_source-catalog.md` by the operator (or by this skill
   after explicit approval).

### Source

`_source-catalog.md` meta-list rows.

### Provenance format (for proposed rows)

```
meta-list-harvest / [meta-list-name] / [YYYY-MM-DD]
```

### Operator gate

This lane is ENTIRELY operator-gated. It proposes; the operator reviews each source and decides
what enters the catalog. This is deliberate — the catalog is a curated registry, not a dump.

### When to run

Periodically (quarterly suggested cadence) or on-demand when the operator says "harvest
[meta-list]" or "grow the source catalog." Highest leverage for expanding discovery reach —
each meta-list can surface 10-100 new potential sources.

---

## Lane activation per profile

The `active_lanes` field in the config profile controls which lanes fire:

| Profile | Active lanes | Notes |
|---|---|---|
| `website-design` (default) | `[1, 2, 3, 4, 5, 6]` | All lanes active |
| `copywriting-swipe` (2nd-corpus) | `[2, 3, 5]` | No SERP/CWV (Lane 1), no expansion (Lane 4, no library yet), no meta-list (Lane 6, sources are hardcoded in profile) |

Lane 5 (manual-add) is always available regardless of the `active_lanes` list.

---

## Cross-lane dedup

A candidate URL may be surfaced by multiple lanes (e.g., a site appears in both Awwwards AND
the SERP top-5). This is signal, not noise:

- **Multi-lane confirmation boosts ranking.** A candidate discovered by 2+ lanes gets a
  novelty bonus in the composite score (it's validated from independent angles).
- **Dedup is against the REGISTRY, not between lanes.** If Lane 1 and Lane 2 both surface
  `example.com`, it appears ONCE in the shortlist with provenance from both lanes noted.

---

## Related

- [[_source-catalog]] — the shared source registry this reads
- [[vetting-rubric]] — the quality gate after discovery
- [[finder-config-profiles]] — per-profile lane activation + source overrides
- [[opportunity-finder]] — sibling skill, same lane shape for product opportunities
