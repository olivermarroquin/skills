---
name: reference-finder
version: 1.0
status: active
created: 2026-06-23
updated: 2026-06-23
description: >
  The discovery top-of-funnel for the reference-library pipeline. Runs multi-lane discovery
  (performance-led SERP rankers, design-led gallery/award pulls, AI-answer-led Sonar queries,
  expansion from existing keepers, operator manual-add, meta-list harvesting) over a sector,
  vets candidates through automated pre-screen + quality thresholds, classifies survivors as
  high-performing-candidate or design-only-candidate, and surfaces a ranked shortlist with
  evidence for operator triage. Approved candidates land in the candidates registry with status
  vetted→queued, which [DI-3] reference-library then captures/fingerprints/files. Profile-driven:
  website-design inspiration is the default profile; any future reference library (copywriting
  swipe, app-UI swipe) is created from a config profile alone, no skill changes. Use this skill
  when the operator says "find reference sites," "source inspiration for [sector]," "what are the
  best-designed [sector] sites," "add this site to the library," "run the finder," "scan
  [gallery] for candidates," or any time the discovery pipeline needs to feed the reference
  library.
triggers:
  - operator wants to GO FIND reference sites in a sector (not ingest one known URL — that is reference-library)
  - phrases like "find reference sites for [sector]," "source inspiration," "what are the best-designed [sector] sites," "scan for design references," "run the finder"
  - operator drops a URL or gallery link for evaluation (manual-add lane)
  - operator says "harvest [meta-list]" or "expand the source catalog"
  - any reference-library run that starts from discovery rather than a handed-down URL
composes-with:
  - reference-library ([DI-3]) — the engine this feeds; vetted candidates land in its candidates registry and flow through its intake pipeline
  - site-capture-engine ([DI-1]) — lightweight capture for pre-screen (not full design-capture)
  - design-fingerprint ([DI-2]) — light fingerprint for design-quality scoring during vetting
  - competitor-deep-research (v1.4) — the performance-led lane reuses its Tier-2 light scan for SERP ranker discovery; compose, don't duplicate
  - design-pattern-synthesis ([DI-6]) — reads the coverage map to surface sector gaps as sourcing worklists
  - _source-catalog.md (05_shared-intelligence/discovery-sources/) — the design-led lane's seed list; this skill reads it, writes yield data back
  - Perplexity Sonar (perplexity_sonar.py at tier-3) — AI-answer-led lane
  - web_fetch + Claude-in-Chrome — gallery/directory fetching per source catalog's Crawl column
  - gate-peer-reviewer + output-quality-loop — quality gates on produced artifacts
tags: [skill, reference-finder, discovery, vetting, website-finder, intake-registry, design-galleries, source-catalog, profile-driven, general-purpose, reusable-engine, design-inspiration-system]
---

# `reference-finder` skill v1.0 — the discovery & vetting top-of-funnel

> **v1.0 (2026-06-23)** — Initial build. The top-of-funnel that feeds [DI-3] reference-library.
> Multi-lane discovery (6 lanes) + automated vetting pipeline + operator review gate + candidates
> registry integration. Design-led lane reads the shared `_source-catalog.md` (34 sources);
> meta-list harvester proposes new catalog rows (operator-gated). Profile-driven: website-design
> is profile #1; a 2nd-corpus instantiation is documented as proof of reuse. Mirrors the
> `opportunity-finder` discover→vet→register shape applied to reference curation.

This skill **discovers** candidate reference sites across a sector, **vets** them through
automated pre-screen + quality thresholds, **classifies** survivors (high-performing-candidate
or design-only-candidate), and surfaces a **ranked shortlist with evidence** for operator triage.
Approved candidates update the candidates registry (`candidate→vetted→queued`), which [DI-3]
`reference-library` then captures, fingerprints, and files.

**It does NOT capture, fingerprint, or file.** Discovery + vetting + a ranked shortlist to decide
"add to library?" is the whole job. The capture ([DI-1]), fingerprint ([DI-2]), filing ([DI-3]),
and cross-site synthesis ([DI-6]) all live in their respective skills — this skill hands vetted
candidates over and stops.

## What's genuinely new here vs. reused

| Capability | Owned by | This skill's job |
|---|---|---|
| Multi-lane discovery shape, candidate registry, source-weighting | `opportunity-finder` pattern (documented + shipped) | **Instantiate the shape for reference curation** (`references/discovery-lanes.md`) |
| **Vetting rubric + classification (NEW)** | **this skill** | `references/vetting-rubric.md` — the quality gate before registry, no equivalent exists |
| **Taste-profile + rejection-log (NEW)** | **this skill** | Bias future filtering toward Oliver's aesthetic; learn from rejections |
| **Meta-list harvester (NEW)** | **this skill** | Crawl a "directory of directories" → propose new `_source-catalog.md` rows |
| Performance-led SERP discovery | `competitor-deep-research` v1.4 Tier-2 light scan | Call it with sector + geo; consume the top-ranker URLs |
| Design-led gallery pulls | `_source-catalog.md` + web_fetch/Chrome | Fetch listings from cataloged sources; parse candidate URLs |
| AI-answer-led queries | `perplexity_sonar.py` (tier-3) | Call with lane prompt template; consume candidate URLs |
| Lightweight pre-screen capture | `site-capture-engine` ([DI-1]) | Quick capture for design-quality assessment (not full design-capture) |
| Light fingerprint scoring | `design-fingerprint` ([DI-2]) | depth: light → design-quality score for vetting |
| CWV performance check | PageSpeed Insights API | Quick performance posture for high-performing classification |
| Quality gates | `gate-peer-reviewer` + `output-quality-loop` | Dispatch on SKILL.md + rubric + first shortlist |

**Do NOT use this skill for:**
- Ingesting a specific known URL into the library (use `reference-library` [DI-3])
- Capturing a site's design (use `site-capture-engine` [DI-1])
- Building a design dossier (use `design-fingerprint` [DI-2])
- Per-client SEO competitor discovery (use `competitor-deep-research` or `market-intelligence-engine`)
- Cross-corpus pattern synthesis (use `design-pattern-synthesis` [DI-6])

---

## Invocation modes

| Mode | When | What it does |
|---|---|---|
| `discover` | operator says "find references for [sector]" | Run the active profile's lanes over the sector → dedup → vet → ranked shortlist → operator triage. The default. |
| `manual-add` | operator drops a URL or gallery link | Run the vetting pipeline on the specific URL(s) → same classification + scoring → operator decision. The VIS-style fast path. |
| `expand` | operator points at a keeper in the library | Run Lane 4 (expansion) from that keeper → adjacent/similar candidates → same vet + shortlist. |
| `harvest` | operator says "harvest [meta-list]" | Crawl a meta-list from `_source-catalog.md` → propose new catalog source rows (operator-gated). |

All modes end at the **operator-triage shortlist** (or the proposed catalog rows for `harvest`).
The engine **proposes; the operator disposes** — nothing is ever auto-admitted to the library
without the review gate. (Auto-admit only on explicit `--review auto`.)

---

## The pipeline (one pass)

```
pick profile + sector
   → run active lanes — each emits candidate URLs + provenance notes
   → DEDUP against THREE stores:
       (1) the library itself (grep library-root for domain)
       (2) the candidates registry (grep for domain)
       (3) the ingestion queue (grep for domain)
   → VET each surviving candidate:
       (a) lightweight [DI-1] capture (quick, not full design-capture)
       (b) [DI-2] light fingerprint → design-quality score
       (c) PageSpeed CWV check → performance posture
       (d) DataForSEO visibility check (if performance-led lane) → ranking evidence
   → CLASSIFY against library bars:
       high-performing-candidate (all 4 bars) / design-only-candidate (visual bar only) / reject
   → RANK survivors by composite score (design-quality + performance + novelty)
   → APPLY taste-profile bias (boost/penalize per learned preferences)
   → SURFACE ranked shortlist (cap configurable, default 10) with:
       per-candidate evidence card (scores, screenshots, provenance, classification)
   → OPERATOR TRIAGE:
       approve → registry status candidate→vetted (this skill)
       reject → rejection-log entry with reason (this skill)
       defer → stays candidate, noted for re-evaluation
   → YIELD DATA: record per-source/per-lane hit rates → feed source-quality weighting
```

---

## Discovery lanes

Six lanes, each with a distinct discovery method. Full specs in `references/discovery-lanes.md`.

### Lane 1 — Performance-led (SERP rankers)

**Method:** Compose `competitor-deep-research` v1.4 Tier-2 light scan for high-intent queries
in the target sector + geography. Extract the top-ranking domains.

**Source:** DataForSEO SERP data (paid) or free-toolkit Google search fallback.

**Provenance:** `performance-led / competitor-deep-research / [query] / [geo] / [date]`

**When to run:** Always — performance evidence is the strongest signal for high-performing classification.

### Lane 2 — Design-led (galleries + awards)

**Method:** Fetch listings from design galleries and award sites cataloged in
`05_shared-intelligence/discovery-sources/_source-catalog.md`. Parse candidate URLs from
listings. Respect each source's `Crawl` column (web_fetch vs Chrome).

**Source:** The `_source-catalog.md` design-feed rows (Awwwards, Land-book, Godly, SiteInspire,
Httpster, Lapa Ninja, Mobbin, The FWA, CSS Design Awards, One Page Love, SaaS Landing Page,
Site of Sites + any rows added later).

**Provenance:** `design-led / [source-name] / [listing-url] / [date]`

**When to run:** Always for design-quality candidates. The highest-yield lane for design-only references.

**ToS/robots discipline:** Respect each gallery's terms. web_fetch restrictions honored. No
auth-walled content. No bulk scraping — fetch recent/featured listings, not full archives.

### Lane 3 — AI-answer-led (Perplexity Sonar)

**Method:** Query Perplexity Sonar API with sector-specific prompts:
"best-designed [sector] websites [year]," "highest-converting [sector] sites,"
"most innovative [sector] web design." Parse cited URLs from responses.

**Source:** `perplexity_sonar.py` at the tier-3 carve-out.

**Provenance:** `ai-answer-led / sonar / [query] / [date]`

**When to run:** Useful for cross-referencing what AI surfaces recommend. Lower yield than
direct gallery pulls but surfaces sites that appear in AI training/citation.

### Lane 4 — Expansion-led (from existing keepers)

**Method:** From a high-performer already in the library:
(a) Run its domain through `competitor-deep-research` to find its direct competitors.
(b) Identify the building agency (from tech fingerprint) → find their portfolio.
(c) Check AlternativeTo or similar-site services for adjacent domains.

**Source:** Existing library dossiers + competitor-deep-research + agency portfolios.

**Provenance:** `expansion-led / [seed-domain] / [method] / [date]`

**When to run:** After the library has ≥3 high-performing entries. Compounds the collection.

### Lane 5 — Manual-add (VIS-style operator intake)

**Method:** Operator drops a URL (or a gallery link that fans out to its listed sites) →
same vetting pipeline → registry. The fast path for human-sourced finds.

**Source:** Operator input.

**Provenance:** `manual-add / operator / [date]`

**When to run:** Any time. Always available.

### Lane 6 — Meta-list harvester

**Method:** Crawl a meta-list source from `_source-catalog.md` (e.g., toools.design 100-list,
awesome-saas-directories). Parse the listed galleries/directories. For each, propose a new
`_source-catalog.md` row (name, URL, feeds tag, crawl method, yield guess). Operator approves
which rows to add.

**Source:** `_source-catalog.md` meta-list rows.

**Provenance:** `meta-list-harvest / [meta-list-name] / [date]`

**When to run:** Periodically (quarterly) or when the operator wants to grow the source catalog.
Highest leverage for expanding discovery surface area.

**Operator gate:** New catalog rows are PROPOSED, never auto-added. The operator reviews each
proposed source before it enters the catalog.

---

## Vetting pipeline

Full rubric in `references/vetting-rubric.md`. Summary:

### Step 1 — Dedup

Grep three stores for the candidate's domain:
1. Library root (`inspiration/high-performing/` + `inspiration/design-only/`)
2. Candidates registry (`candidates-registry.md`)
3. Ingestion queue (`_ingestion-queue.md`)

If found → surface to operator: "Already exists at [path]. Skip / update / re-evaluate?"
Never silently re-surface what's already tracked.

### Step 2 — Automated pre-screen

Run in parallel where possible:

| Check | Tool | Output | Cost |
|---|---|---|---|
| Lightweight capture | `site-capture-engine` (quick mode) | Fold screenshot + basic tokens | ~10s per site |
| Light fingerprint | `design-fingerprint` (depth: light) | Design-quality score (1-10) | ~30s per site |
| CWV check | PageSpeed Insights API | LCP, CLS, INP scores + Good/Needs-Improvement/Poor | Free |
| Visibility check | DataForSEO ranked_keywords (if perf-led) | Estimated organic keywords + traffic | ~$0.01-0.02 |

### Step 3 — Classification

Score against the library's inclusion bars (from `reference-library` config profile):

| Classification | Criteria | Registry lane |
|---|---|---|
| `high-performing-candidate` | ALL: (1) top-5 organic OR strong visibility evidence, (2) CWV Good range, (3) visible content depth, (4) design-quality score ≥ 7/10 | high-performing |
| `design-only-candidate` | Design-quality score ≥ 7/10, performance not verified or below bar | design-only |
| `reject` | Design-quality score < 7/10 OR site is broken/inaccessible | logged in rejection-log with reason |

### Step 4 — Ranking

Composite score: `(design-quality × 0.4) + (performance × 0.3) + (novelty × 0.2) + (taste-fit × 0.1)`

- **design-quality** — from the light fingerprint (1-10 scale)
- **performance** — from CWV + visibility (1-10 normalized)
- **novelty** — sectors/archetypes underrepresented in the library score higher (coverage map)
- **taste-fit** — boost/penalty from the taste profile (see below)

### Step 5 — Operator triage

Surface the ranked shortlist (default cap: 10) with per-candidate evidence cards:

```
## [rank]. domain.com — [classification] — score [N]/10

**Provenance:** [lane] / [source] / [date]
**Design quality:** [score]/10 — [1-line summary from fingerprint]
**Performance:** CWV [Good/NI/Poor] — LCP [N]s, CLS [N], INP [N]ms
**Visibility:** [N] organic keywords, ~[N] monthly traffic (or "not checked")
**Sector:** [sector] — [coverage: new/existing]
**Screenshot:** [fold screenshot path or "capture pending"]

**Recommendation:** [high-performing-candidate / design-only-candidate]
**Taste-fit note:** [any taste-profile match/mismatch]
```

Operator actions per candidate: **approve** (→ vetted) / **reject** (→ rejection-log) / **defer**.

---

## Taste profile

Location: `<library-root>/_taste-profile.md` (per library profile).

A lightweight preferences file that biases the ranking step. Starts with operator-seeded
preferences; refines over time from approval/rejection patterns.

**Structure:**

```yaml
# Boosted traits (operator likes these → rank higher)
boost:
  - dark-hero-cta           # Oliver likes bold dark heroes
  - cinematic-motion         # appreciates scroll-driven animation
  - split-image-layout       # likes asymmetric hero compositions
  - minimal-typography       # clean type hierarchies

# Penalized traits (operator dislikes → rank lower, don't auto-reject)
penalize:
  - stock-photo-heavy        # prefers custom/generated imagery
  - generic-template         # dislikes obvious template sites
  - cluttered-navigation     # prefers clean nav patterns
  - slow-render              # penalize sites that feel sluggish

# Neutral (no bias either way)
neutral:
  - light-palette
  - dark-palette
```

Traits use the `design-fingerprint` controlled vocabulary (`references/trait-vocabulary.md`)
so the taste profile composes with the trait sidecar.

**Learning loop (v1.1):** Analyze rejection-log entries for recurring rejected traits →
propose taste-profile updates to the operator. Never auto-update.

---

## Rejection log

Location: `<library-root>/_rejection-log.md` (per library profile).

Every rejected candidate is logged with:

```markdown
| Domain | Date | Lane | Reason | Design score | Perf score | Rejected by |
|---|---|---|---|---|---|---|
| example.com | 2026-06-23 | design-led / Awwwards | Below design bar (4/10), stock-heavy | 4 | N/A | operator |
```

**Why log rejections:**
- Prevents re-surfacing the same site from different lanes
- Feeds the taste-learning loop (v1.1) — recurring rejection reasons reveal preference patterns
- Source-quality weighting — lanes/sources that produce mostly rejects get downweighted

---

## Sector coverage map

A derived view (not a separate file — computed at runtime) showing:

| Sector | High-performing | Design-only | Total | Gap? |
|---|---|---|---|---|
| electrical-services | 1 | 0 | 1 | — |
| consumer-electronics | 0 | 1 | 1 | — |
| hvac | 0 | 0 | 0 | **gap** |
| ... | | | | |

Sources: library dossier/note frontmatter `sector:` tags + candidates registry entries.

**Novelty scoring** uses this map — underrepresented sectors get a ranking boost.

When [DI-6] ships its thin-sector flags, those feed directly into this map as a sourcing
worklist: "DI-6 says we have 0 HVAC references → run performance-led + design-led for HVAC."

---

## Source-quality weighting

Per-source yield tracking, mirroring `opportunity-radar/discovery/_source-yield.md`:

| Source | Runs | Surfaced | Vetted | Approved | Yield % | Weight |
|---|---|---|---|---|---|---|
| Awwwards | 1 | 8 | 5 | 3 | 37.5% | 1.0 |
| Land-book | 1 | 12 | 4 | 2 | 16.7% | 0.8 |
| ... | | | | | | |

Updated after every discovery run. Sources with consistently low yield get deprioritized
(lower fetch priority, not removed from catalog). Sources with high yield get run first.

**Writes back to `_source-catalog.md`:** After accumulating ≥3 runs of yield data, append a
`yield-rating:` note to the catalog row (e.g., "high / medium / low"). The catalog is the
shared registry; yield data enriches it for all consumers.

---

## Config-driven design

The skill is domain-agnostic. All domain-specific content comes from a **config profile**. See
`references/finder-config-profiles.md` for the full profile schema and instantiated profiles.

| What | Where it comes from | NOT hardcoded |
|---|---|---|
| Target library | Profile `library_root` | `inspiration/` |
| Registry file | Profile `registry_file` | `candidates-registry.md` |
| Queue file | Profile `queue_file` | `_ingestion-queue.md` |
| Taste profile | Profile `taste_profile` | `_taste-profile.md` |
| Rejection log | Profile `rejection_log` | `_rejection-log.md` |
| Inclusion bars | Profile `inclusion_bars` | The 4-bar test |
| Source catalog | Profile `source_catalog` | `_source-catalog.md` |
| Active lanes | Profile `active_lanes` | `[1,2,3,4,5,6]` |
| Sector list | Profile `sectors` | `[electrical-services, hvac, ...]` |
| Upstream capture skill | Profile `capture_skill` | `site-capture-engine` |
| Upstream fingerprint skill | Profile `fingerprint_skill` | `design-fingerprint` |
| CWV check method | Profile `cwv_method` | `pagespeed-api` |
| Visibility check method | Profile `visibility_method` | `dataforseo` |

To instantiate a 2nd reference library (e.g., an app-UI swipe collection): create a new profile
in `finder-config-profiles.md` with the appropriate sources, lanes, bars, and taste profile.
No skill changes needed.

### 2nd-corpus proof: copywriting swipe file

Documented in `references/finder-config-profiles.md` as profile `copywriting-swipe`. Uses:
- Lane 2 sources: copywriting-specific galleries (swipefile.com, swiped.co, goodemailcopy.com)
- Lane 3 prompts: "best SaaS landing page copy," "highest-converting email sequences"
- Different inclusion bars: no CWV check, no SERP visibility — quality is copy effectiveness
- Different taste profile: boost `clear-value-prop`, `specific-numbers`, `social-proof-dense`
- Same vetting pipeline shape, same registry status flow, same operator gate

This proves the engine works for non-website corpora from config alone.

---

## Reference files

| File | Purpose |
|---|---|
| `references/discovery-lanes.md` | Full lane specs: method, source, prompt templates, provenance format, ToS notes |
| `references/vetting-rubric.md` | Pre-screen checks, scoring, classification thresholds, ranking formula |
| `references/finder-config-profiles.md` | Config profiles: website-design default + copywriting-swipe 2nd-corpus proof |

---

## Upstream dependencies

| Skill | Version | What this skill calls |
|---|---|---|
| `site-capture-engine` | v2.1+ | Quick-mode capture for pre-screen (not full design-capture) |
| `design-fingerprint` | v1.0+ | depth: light for design-quality scoring |
| `competitor-deep-research` | v1.4+ | Tier-2 light scan for performance-led lane (compose, don't duplicate) |
| `reference-library` | v1.0+ | Reads its config for inclusion bars; writes to its candidates registry |

---

## Downstream consumers

| Consumer | What it reads | How |
|---|---|---|
| [DI-3] `reference-library` | Candidates registry (vetted entries) | Picks up `status: queued` entries for capture + filing |
| [DI-6] `design-pattern-synthesis` | Sector coverage map | Flags thin sectors as sourcing worklists |
| `_source-catalog.md` | Yield data (appended by this skill) | Enriches source rows for all catalog consumers |
| Operator | Ranked shortlists | Reviews evidence cards, makes approve/reject/defer decisions |

---

## Related

- [[reference-library]] — downstream filing engine ([DI-3])
- [[site-capture-engine]] — upstream capture ([DI-1])
- [[design-fingerprint]] — upstream fingerprint ([DI-2])
- [[design-emulation-verify]] — sibling verification ([DI-4])
- [[design-pattern-synthesis]] — downstream synthesis ([DI-6])
- [[competitor-deep-research]] — performance-led lane muscle
- [[opportunity-finder]] — sibling skill; same discover→vet→register shape for opportunities
- [[vis-extraction]] — VIS-style operator-add intake pattern (manual-add lane mirrors this)
- `second-brain/05_shared-intelligence/discovery-sources/_source-catalog.md` — design-led lane seed list
- `second-brain/03_domains/website-design/inspiration/candidates-registry.md` — intake registry
- `second-brain/03_domains/website-design/inspiration/_taste-profile.md` — taste preferences
- `second-brain/03_domains/website-design/inspiration/_rejection-log.md` — rejected candidates log
