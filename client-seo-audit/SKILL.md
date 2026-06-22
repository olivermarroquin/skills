---
name: client-seo-audit
version: 1.0
status: active
created: 2026-06-22
updated: 2026-06-22
description: One-command SEO audit skill. Reads per-client config (domain, target keywords, competitors), calls seo-data-wrapper for live DataForSEO data, composes with prioritization + competitor-deep-research + report template, and produces a client-ready findings doc. Zero hardcoded client values.
compose-targets:
  - seo-data-wrapper (cost-guarded DataForSEO data layer)
  - market-intelligence-engine (arena schema for scoring)
  - competitor-deep-research (competitor column format)
  - prioritization (issue ranking)
triggers:
  - "audit <client>"
  - "run SEO audit for <client>"
  - "client-seo-audit on <slug>"
  - "generate SEO findings for <client>"
  - "run a full SEO audit on <client-slug>"
tags: [skill, seo, audit, client, dataforseo, local-seo, growth-program, productization]
---

# client-seo-audit — One-command client SEO audit

## Purpose

`audit <client>` reads a per-client config file, pulls live SEO data through the `seo-data-wrapper` (cost-guarded DataForSEO layer), and produces a **client-ready findings doc** containing:

1. **Ranking snapshot** — where the client ranks for target keywords (organic + local pack)
2. **Competitor teardown** — how competitors compare across key metrics
3. **Prioritized issue list** — what to fix, ranked by impact
4. **Content-brief recommendations** — what to publish next, based on keyword gaps

All from config alone. Zero hardcoded client values.

## Config

Per-client configs live in `skills/client-seo-audit/configs/<client-slug>.yaml`:

```yaml
# === Client identity (REQUIRED) ===
client:
  slug: ""                    # e.g. "acme-plumbing"
  name: ""                    # e.g. "Acme Plumbing Co."
  domain: ""                  # e.g. "acmeplumbing.com"
  gbp_name: ""                # e.g. "Acme Plumbing Co." (for local pack matching)

# === Target keywords (REQUIRED, ≥3) ===
target_keywords:
  - "plumber springfield va"
  - "drain cleaning springfield"
  - "emergency plumber near me"

# === Competitors (REQUIRED, ≥1) ===
competitors:
  - domain: "competitorone.com"
    name: "Competitor One"
  - domain: "competitortwo.com"
    name: "Competitor Two"

# === Location (REQUIRED for local-SEO) ===
location:
  name: "Springfield,Virginia,United States"  # DataForSEO location_name format (city,region,country)
  language_code: "en"

# === Budget (REQUIRED) ===
budget_usd: 2.00              # per-audit spend cap passed to seo-data-wrapper

# === Operations (OPTIONAL — defaults to full_audit) ===
operations:
  - ranking_snapshot
  - keyword_serps
  - backlink_profile
  - competitor_overview
  - keyword_research
  - on_page_audit

# === Output (OPTIONAL) ===
output_dir: ""                # defaults to skills/client-seo-audit/_state/<slug>/
```

### Config validation rules

1. `client.slug`, `client.name`, `client.domain` must be non-empty strings
2. `target_keywords` must have ≥3 entries
3. `competitors` must have ≥1 entry with a non-empty `domain`
4. `budget_usd` must be > 0
5. `location.name` must be non-empty
6. **Zero hardcoded values** — every client-specific value comes from this file

If validation fails → HALT with a clear error naming the missing/invalid fields.

## Execution steps

### Step 1: Load and validate config

Read `configs/<client-slug>.yaml`. Validate per rules above. If the file doesn't exist, HALT with: `Config not found: configs/<client-slug>.yaml — create it from the template in configs/_template.yaml`.

### Step 2: Check state / resumability

Read `_state/<client-slug>/last-run.json` if it exists. If a prior run exists from today with `status: partial`, offer to resume (reuse cached data, skip completed operations).

### Step 3: Invoke seo-data-wrapper

For each operation in `config.operations`, call `seo-data-wrapper` with:
- `client_slug` and `client_domain` from config
- `budget_usd` from config
- `location_name` and `language_code` from config
- The specific operation name

**Operations and their wrapper calls:**

#### 3a. `ranking_snapshot`
- `domain_rank_overview` for client domain → V1 organic metrics
- `ranked_keywords` for client domain (limit 20, sorted by rank asc) → top keyword positions

#### 3b. `keyword_serps`
- `serp_organic_live_advanced` for each target keyword at client's location → client rank + local pack detection (V2)
- **Cost: $0.002 × number of target keywords**

#### 3c. `backlink_profile`
- `backlinks_summary` for client domain → A1 authority metrics
- **Cost: ~$0.02**

#### 3d. `competitor_overview`
- `domain_rank_overview` for each competitor domain → V1 comparison
- `backlinks_summary` for each competitor (bulk if ≤10) → A1 comparison
- **Cost: ~$0.04 × number of competitors**

#### 3e. `keyword_research`
- `keyword_overview` for target keywords → search volume + intent
- `keywords_for_site` for client domain → additional keyword opportunities
- **Cost: ~$0.07**

#### 3f. `on_page_audit`
- `on_page_instant_pages` for client homepage → on-page SEO health
- **Cost: ~$0.01**

If the spend guard halts mid-run → log which operations completed, which were skipped, and the spend total. Produce a partial findings doc from available data.

### Step 4: Compose — competitor teardown

If `skills/competitor-deep-research/SKILL.md` exists on disk:
- Map the competitor data from Step 3d onto the competitor-deep-research 15-column format (columns populated by DataForSEO; others marked `[data-source-needed]`)
- Produce a per-competitor summary

If `skills/competitor-deep-research/SKILL.md` does NOT exist:
- **Graceful degrade:** log `competitor-deep-research-unavailable`, produce a simplified competitor comparison table from raw wrapper data. Do NOT block.

### Step 5: Compose — prioritize issues

Collect all findings into a candidate set:
- Missing/thin organic rankings (from Step 3a/3b)
- Keywords where competitors outrank client (from Step 3b + 3d)
- Backlink gap vs competitors (from Step 3c + 3d)
- On-page issues (from Step 3f)
- Local pack absence for target keywords (from Step 3b)
- Content gaps (keywords with volume but no client page — from Step 3e)

If `skills/prioritization/SKILL.md` exists on disk:
- Feed candidates to prioritization with criteria: `impact` (search volume × rank gap), `effort` (content vs technical vs link-building), `quick_win` (already ranking 11-20 → push to page 1)
- Output: ranked issue list

If `skills/prioritization/SKILL.md` does NOT exist:
- **Graceful degrade:** log `prioritization-unavailable`, sort issues by search volume × rank gap descending. Do NOT block.

### Step 6: Generate findings doc

Write the findings doc to `<output_dir>/<client-slug>-seo-audit-<YYYY-MM-DD>.md` using the report template (see `references/report-template.md`).

Sections:
1. **Executive summary** — 3-5 bullet overview of where the client stands
2. **Ranking snapshot** — table of target keywords with client rank, search volume, local pack status
3. **Competitor teardown** — comparison table (client vs each competitor across V1/V2/A1 metrics)
4. **Prioritized issues** — ranked list with issue, impact, recommended action
5. **Content-brief recommendations** — top 3-5 keyword gaps to target with new content
6. **Technical findings** — on-page issues from the audit
7. **Spend report** — DataForSEO API cost for this audit run
8. **Data sources and freshness** — which endpoints were called, cache hits, timestamps

### Step 7: Update state

Write to `_state/<client-slug>/`:
- `last-run.json` — run metadata (date, status, operations completed, spend, output path)
- `audit-history.json` — append-only log of all audit runs for this client

### Step 8: Report

Output to the operator:
- Path to the findings doc
- Spend summary (total cost, budget remaining, cache hit rate)
- Any skipped operations or graceful-degrade activations
- Suggested next action (e.g., "review findings doc and share with client" or "run competitor-deep-research for deeper profiles")

## Graceful degrade summary

| Compose target | If absent | Behavior |
|---|---|---|
| `seo-data-wrapper/SKILL.md` | HALT | Cannot proceed without data layer |
| `competitor-deep-research/SKILL.md` | Degrade | Simplified comparison table from raw data |
| `prioritization/SKILL.md` | Degrade | Sort by volume × rank gap instead |
| `market-intelligence-engine/SKILL.md` | Degrade | Skip arena scoring, report raw metrics |
| DataForSEO MCP connection | HALT | Cannot proceed without connector |

## Per-client state layout

```
skills/client-seo-audit/
├── SKILL.md                          # this file
├── configs/
│   ├── _template.yaml                # blank template
│   ├── ev-electric-services.yaml     # EV client config
│   ├── s-and-h-contracting.yaml      # S&H client config
│   └── <any-client-slug>.yaml        # any future client
├── _state/
│   ├── ev-electric-services/
│   │   ├── last-run.json
│   │   └── audit-history.json
│   └── s-and-h-contracting/
│       ├── last-run.json
│       └── audit-history.json
└── references/
    ├── report-template.md
    └── issue-categories.md
```

## Zero hardcoded values — enforcement

The skill reads ALL client-specific values from `configs/<slug>.yaml`. The skill code (this SKILL.md and the operator's execution of it) contains:
- NO domain names
- NO keyword lists
- NO competitor names
- NO location strings
- NO GBP names

The only client-specific content in this skill directory is inside `configs/` files, which the operator creates per client.

## Phase 3 deferred — multi-vendor aggregator

> **DEFER until:** (a) concepts 1+2 prove on a real pilot client AND (b) a second vetted data source passes strict-gate AND (c) pilot audits show DataForSEO-only gaps that corroboration would close.

When activated, the audit skill adds a second data source alongside `seo-data-wrapper` and reconciles conflicting signals (e.g., DataForSEO says rank 5, second source says rank 8 → report both with confidence note).
