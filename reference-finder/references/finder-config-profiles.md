---
type: reference
status: active
created: 2026-06-23
updated: 2026-06-23
skill: reference-finder
tags: [reference, config-profiles, reference-finder, design-inspiration-system]
---

# Config profiles — reference-finder v1.0

Each profile defines the full configuration for a reference-finder instantiation. The engine
reads the active profile and uses its values for all lane activation, source selection,
threshold evaluation, and output routing. No hardcoded values in the skill — everything comes
from here.

---

## Profile schema

```yaml
profile_name: string           # unique identifier
description: string            # one-line purpose

# Library routing
library_root: path             # root folder of the target library
registry_file: path            # candidates registry (relative to library_root)
queue_file: path               # ingestion queue
taste_profile: path            # taste profile file (relative to library_root)
rejection_log: path            # rejection log file (relative to library_root)

# Source catalog
source_catalog: path           # shared source catalog to read for Lane 2
source_catalog_feeds_filter: string  # filter value for catalog Feeds column ("design" / "product" / "both")

# Lane activation
active_lanes: [int]            # which lanes to run (1-6); Lane 5 always available

# Upstream skills
capture_skill: string          # skill name for pre-screen capture
fingerprint_skill: string      # skill name for design-quality scoring
competitor_skill: string       # skill name for performance-led lane (Lane 1)

# Performance checks
cwv_method: string             # "pagespeed-api" | "lighthouse-cli" | "none"
visibility_method: string      # "dataforseo" | "free-toolkit" | "none"

# Inclusion bars
inclusion_bars:
  design_quality_min: int      # minimum design-quality score (1-10)
  cwv_min: string              # "good" | "needs-improvement" | "none"
  visibility_min_keywords: int # minimum organic keywords for high-performing (0 = skip)
  content_depth_required: bool # whether content-depth check is applied

# Ranking
ranking_weights:
  design_quality: float        # default 0.4
  performance: float           # default 0.3
  novelty: float               # default 0.2
  taste_fit: float             # default 0.1
shortlist_cap: int             # maximum candidates in the shortlist (default 10)

# Sectors (for coverage map + Lane 1 seed queries)
sectors: [string]              # tracked sectors

# Lane-specific config
lane_1_seed_queries: map       # sector → [query templates with {geo} placeholder]
lane_3_prompts: [string]       # Sonar prompt templates with {sector} placeholder
```

---

## Profile 1: `website-design` (default)

The primary instantiation — website-design inspiration library.

```yaml
profile_name: website-design
description: Discover and vet reference sites for the website-design inspiration library

# Library routing
library_root: second-brain/03_domains/website-design/inspiration
registry_file: candidates-registry.md
queue_file: ../insights/_ingestion-queue.md
taste_profile: _taste-profile.md
rejection_log: _rejection-log.md

# Source catalog
source_catalog: second-brain/05_shared-intelligence/discovery-sources/_source-catalog.md
source_catalog_feeds_filter: design  # also includes "both" rows

# Lane activation
active_lanes: [1, 2, 3, 4, 5, 6]

# Upstream skills
capture_skill: site-capture-engine
fingerprint_skill: design-fingerprint
competitor_skill: competitor-deep-research

# Performance checks
cwv_method: pagespeed-api
visibility_method: dataforseo

# Inclusion bars
inclusion_bars:
  design_quality_min: 7
  cwv_min: good
  visibility_min_keywords: 100
  content_depth_required: true

# Ranking
ranking_weights:
  design_quality: 0.4
  performance: 0.3
  novelty: 0.2
  taste_fit: 0.1
shortlist_cap: 10

# Sectors
sectors:
  - electrical-services
  - hvac
  - plumbing
  - roofing
  - landscaping
  - restaurant
  - saas
  - fintech
  - agency
  - consumer-electronics
  - ai-dev-tools
  - data-analytics
  - website-builder
  - creative-portfolio
  - digital-security

# Lane 1 — seed queries per sector
lane_1_seed_queries:
  electrical-services:
    - "electrician {geo}"
    - "electrical contractor {geo}"
    - "emergency electrician {geo}"
  hvac:
    - "hvac contractor {geo}"
    - "ac repair {geo}"
    - "heating and cooling {geo}"
  plumbing:
    - "plumber {geo}"
    - "plumbing contractor {geo}"
    - "emergency plumber {geo}"
  roofing:
    - "roofing contractor {geo}"
    - "roof repair {geo}"
    - "roofer near me {geo}"
  landscaping:
    - "landscaping company {geo}"
    - "lawn care service {geo}"
    - "landscape design {geo}"
  restaurant:
    - "best restaurant {geo}"
    - "restaurant website design examples"
    - "restaurant online ordering {geo}"
  saas:
    - "best saas landing pages 2026"
    - "saas website design examples"
    - "highest-converting saas websites"
  # Add more sectors as the library grows

# Lane 3 — Sonar prompt templates
lane_3_prompts:
  - "What are the best-designed {sector} websites in 2026?"
  - "Which {sector} companies have the highest-converting websites?"
  - "Most innovative {sector} website designs"
  - "Best {sector} website examples for small businesses"
```

---

## Profile 2: `copywriting-swipe` (2nd-corpus proof)

Proves the engine works for a non-website reference library from config alone. This profile
discovers and vets high-quality copywriting examples for a copywriting swipe file.

```yaml
profile_name: copywriting-swipe
description: Discover and vet copywriting examples for the copywriting swipe library

# Library routing
library_root: second-brain/03_domains/content-systems/swipe-file
registry_file: candidates-registry.md
queue_file: _ingestion-queue.md
taste_profile: _taste-profile.md
rejection_log: _rejection-log.md

# Source catalog
source_catalog: second-brain/05_shared-intelligence/discovery-sources/_source-catalog.md
source_catalog_feeds_filter: product  # copywriting examples come from product/SaaS sites

# Lane activation — no SERP/CWV (Lane 1), no expansion yet (Lane 4), no meta-list (Lane 6)
active_lanes: [2, 3, 5]

# Upstream skills — different capture/fingerprint for copy (not visual design)
capture_skill: site-capture-engine   # captures the page content
fingerprint_skill: null              # no design fingerprint — copy quality is assessed differently
competitor_skill: null               # no SERP lane

# Performance checks — not relevant for copywriting quality
cwv_method: none
visibility_method: none

# Inclusion bars — copy-specific
inclusion_bars:
  design_quality_min: 0              # not applicable — replaced by copy-quality assessment
  cwv_min: none
  visibility_min_keywords: 0
  content_depth_required: false
  # Copy-specific bars (engine interprets these):
  copy_quality_min: 7                # assessed manually or via LLM evaluation
  specificity_required: true         # must have specific numbers/claims, not vague

# Ranking — copy-specific weights
ranking_weights:
  design_quality: 0.0                # not applicable
  performance: 0.0                   # not applicable
  novelty: 0.5                       # diversity of copy styles valued
  taste_fit: 0.5                     # Oliver's copy preferences drive selection
shortlist_cap: 10

# Sectors (copy categories)
sectors:
  - saas-landing-page
  - email-sequence
  - cold-outreach
  - product-description
  - case-study

# Lane 2 — copy-specific gallery sources (not from the shared catalog)
lane_2_override_sources:
  - name: Swipe File
    url: swipefile.com
    crawl: web_fetch
  - name: Swiped.co
    url: swiped.co
    crawl: web_fetch
  - name: Good Email Copy
    url: goodemailcopy.com
    crawl: web_fetch
  - name: Really Good Emails
    url: reallygoodemails.com
    crawl: Chrome
  - name: Email Love
    url: emaillove.com
    crawl: web_fetch

# Lane 3 — copy-specific Sonar prompts
lane_3_prompts:
  - "Best SaaS landing page copy examples 2026"
  - "Highest-converting email sequences for SaaS"
  - "Best cold outreach email examples B2B"
  - "Most effective product description copy"
```

### What this proves

The `copywriting-swipe` profile demonstrates that the reference-finder engine handles a
non-website corpus from config alone:

1. **Different sources** — copy-specific galleries (swipefile.com, swiped.co) instead of design
   galleries (Awwwards, Godly)
2. **Different bars** — copy quality replaces design quality; no CWV, no SERP visibility
3. **Different ranking** — novelty and taste-fit dominate instead of design + performance
4. **Different sectors** — copy categories (email-sequence, cold-outreach) instead of industries
5. **Same pipeline shape** — discover → dedup → vet → classify → rank → operator triage

No SKILL.md changes needed. The engine reads the profile and adapts.

---

## Adding a new profile

1. Copy the profile schema above.
2. Fill in all fields for the target library.
3. If the library folder doesn't exist yet, create it with a `_README.md` + the registry +
   queue + taste-profile + rejection-log files.
4. Run the finder with `--profile <profile_name>` to activate.

---

## Related

- [[discovery-lanes]] — lane specs that consume profile config
- [[vetting-rubric]] — threshold values from profile `inclusion_bars`
- [[reference-library]] — the library engine whose config shapes the bars
- `second-brain/05_shared-intelligence/discovery-sources/_source-catalog.md` — shared source catalog
