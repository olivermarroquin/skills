---
name: seo-data-wrapper
version: 1.0
status: active
created: 2026-06-22
updated: 2026-06-22
description: Cost-guarded, vault-aware wrapper around the official DataForSEO MCP connector. Adds spend cap, response cache, and market-intelligence schema mapping. COMPOSES the official connector — does NOT fork it.
compose-targets:
  - dataforseo MCP (official, Apache-2.0, local stdio)
  - market-intelligence-engine (arena schema)
triggers:
  - "pull SEO data for <client>"
  - "get SERP data for <keywords>"
  - "run SEO data pull with budget $X"
  - "fetch backlinks for <domain>"
  - invoked programmatically by client-seo-audit skill
tags: [skill, seo, dataforseo, cost-guard, cache, wrapper, local-seo, growth-program]
---

# seo-data-wrapper — Cost-guarded DataForSEO wrapper

## Purpose

A thin composition layer over the official DataForSEO MCP connector that adds three capabilities the raw connector lacks:

1. **Spend guard** — per-run budget cap in USD. Tracks estimated cost per API call using DataForSEO's published per-endpoint pricing. Halts execution when the next call would exceed the cap. Logs cumulative spend to `_state/`.
2. **Response cache** — file-based cache keyed on `(endpoint, params_hash, date)`. Reuses cached responses within a configurable freshness window (default: 24 hours). Avoids re-billing for identical queries.
3. **Schema mapping** — maps raw DataForSEO JSON responses onto the `market-intelligence-engine` arena schema fields (V1, V2, A1, etc.) and the `competitor-deep-research` 15-column format, so downstream consumers get structured data, not raw JSON.

## Architecture: compose, never fork

All data calls go through the official DataForSEO MCP tools (`mcp__dataforseo__*`). This skill adds cost tracking, caching, and mapping around those calls. It does NOT reimplement any DataForSEO API logic.

```
caller (client-seo-audit)
  → seo-data-wrapper (this skill)
    → [cache check] → hit? return cached
    → [spend check] → would exceed cap? HALT with spend report
    → [MCP call] → dataforseo MCP tool
    → [cache write] → store response
    → [schema map] → return structured data
```

## Config

```yaml
# Required — provided by the caller (client-seo-audit or operator)
client_slug: ""          # e.g. "acme-plumbing"
client_domain: ""        # e.g. "acmeplumbing.com"

# Spend guard
budget_usd: 2.00         # per-run cap in USD; HALT when next call would exceed
warn_at_pct: 75          # log a warning when spend reaches this % of budget

# Cache
cache_dir: ""            # defaults to skills/seo-data-wrapper/_cache/
cache_freshness_hours: 24 # reuse cached responses younger than this

# Location (for local-SEO — city-level when available)
location_name: "United States"  # DataForSEO location_name format
language_code: "en"

# Output
output_dir: ""           # where to write mapped results; caller sets this
```

Validation: refuses to start if `client_slug`, `client_domain`, or `budget_usd` are empty/zero.

## Endpoint cost table

Estimated costs per DataForSEO API call (from published pricing, conservative):

| Endpoint tool | Cost per call | Used for |
|---|---|---|
| `serp_organic_live_advanced` | $0.002 | SERP rankings per keyword |
| `dataforseo_labs_google_ranked_keywords` | $0.05 | Domain's ranked keywords |
| `dataforseo_labs_google_domain_rank_overview` | $0.02 | Domain organic/paid overview |
| `dataforseo_labs_google_keyword_overview` | $0.02 | Keyword search volume + CPC |
| `dataforseo_labs_google_serp_competitors` | $0.05 | SERP competitor domains |
| `dataforseo_labs_google_keywords_for_site` | $0.05 | Keywords relevant to domain |
| `backlinks_summary` | $0.02 | Backlink profile overview |
| `backlinks_bulk_pages_summary` | $0.02 | Bulk backlink check |
| `backlinks_referring_domains` | $0.04 | Referring domain list |
| `on_page_instant_pages` | $0.01 | On-page SEO audit |
| `on_page_content_parsing` | $0.01 | Page content structure |
| `kw_data_google_ads_search_volume` | $0.05 | Google Ads search volume |

**These are estimates.** Actual billing may vary. The spend guard uses these as upper-bound estimates; if actual cost is lower, the guard is conservative (safe side).

## Spend guard protocol

1. Before each MCP call, look up the endpoint in the cost table.
2. Add the estimated cost to the running total.
3. If `running_total + estimated_cost > budget_usd`: **HALT**. Do NOT make the call.
   - Log: `SPEND_GUARD_HALT: would exceed budget ($X.XX of $Y.YY used). Remaining calls skipped.`
   - Return partial results collected so far + the spend report.
4. If `running_total / budget_usd >= warn_at_pct / 100`: log warning.
5. After each successful call, record the call in the spend log:
   ```json
   {"timestamp": "ISO-8601", "endpoint": "tool_name", "params_hash": "sha256_prefix", "estimated_cost_usd": 0.05, "cumulative_usd": 0.12}
   ```
6. At run end, write the full spend log to `_state/<client_slug>-spend-log-<date>.json`.

## Cache protocol

1. Compute cache key: `sha256(endpoint + sorted_params_json + date_YYYY-MM-DD)[:16]`
2. Cache file: `<cache_dir>/<endpoint>/<cache_key>.json`
3. On read: if file exists AND `mtime` < `cache_freshness_hours` → return cached, cost = $0.00.
4. On miss: make the MCP call, write response to cache file, charge the cost.
5. Cache is date-partitioned (the date in the key ensures daily freshness at minimum).

## Schema mapping

Raw DataForSEO responses are mapped onto two output schemas:

### 1. Market-intelligence arena fields

| Arena | DataForSEO source | Mapped field |
|---|---|---|
| V1 (organic) | `domain_rank_overview` → `organic.count`, `organic.etv` + `ranked_keywords` top-10 | `v1_organic_keywords`, `v1_organic_traffic`, `v1_top_keywords[]` |
| V2 (local pack) | `serp_organic_live_advanced` → items where `type == "local_pack"` | `v2_local_pack_present`, `v2_local_pack_position` |
| A1 (authority) | `backlinks_summary` → `backlinks`, `referring_domains`, `rank` | `a1_backlinks`, `a1_referring_domains`, `a1_domain_rank` |

### 2. Competitor-deep-research columns (subset)

| Column | DataForSEO source |
|---|---|
| Top 5 keywords | `ranked_keywords` top-5 by rank |
| Total backlinks | `backlinks_summary.backlinks` |
| Domain rank | `backlinks_summary.rank` |
| Avg rank for head keyword | `serp_organic_live_advanced` → client position |
| Local-pack flag | `serp_organic_live_advanced` → `local_pack` presence |

### 3. Raw pass-through

For endpoints not in the mapping tables, the wrapper returns the raw DataForSEO response as-is (still subject to spend guard + cache).

## Invocation

This skill is invoked by the `client-seo-audit` skill or directly by the operator. It is NOT a standalone audit — it is the data layer.

### Available operations

| Operation | Endpoints called | Typical cost |
|---|---|---|
| `ranking_snapshot` | `domain_rank_overview` + `ranked_keywords` (limit 20) | ~$0.07 |
| `keyword_serps` | `serp_organic_live_advanced` × N keywords | ~$0.002 × N |
| `backlink_profile` | `backlinks_summary` | ~$0.02 |
| `competitor_overview` | `domain_rank_overview` × N competitors | ~$0.02 × N |
| `keyword_research` | `keyword_overview` + `keywords_for_site` | ~$0.07 |
| `on_page_audit` | `on_page_instant_pages` | ~$0.01 |
| `full_audit` | all of the above | ~$0.50-1.50 |

### Operation dispatch

The caller specifies which operations to run:
```yaml
operations:
  - ranking_snapshot
  - keyword_serps
  - backlink_profile
  - competitor_overview
  - on_page_audit
```

Or `operations: [full_audit]` to run all.

## State

Per-client spend logs are written to:
- `skills/seo-data-wrapper/_state/<client_slug>-spend-log-<YYYY-MM-DD>.json`
- `skills/seo-data-wrapper/_state/<client_slug>-last-run.json` (summary: total spend, calls made, cache hits, halted?)

Cache files are written to:
- `skills/seo-data-wrapper/_cache/<endpoint_name>/<cache_key>.json`

## Graceful degrade

- **DataForSEO MCP not connected:** HALT immediately with `CONNECTOR_UNAVAILABLE`. Do not attempt fallback.
- **Individual endpoint fails:** Log the error, skip that operation, continue with remaining operations. Return partial results + error report.
- **Cache dir not writable:** Proceed without caching (every call hits the API). Log warning.

## Phase 3 deferred — multi-vendor aggregator

> **DEFER until:** (a) concepts 1+2 prove on a real pilot client AND (b) a second vetted data source passes strict-gate AND (c) pilot audits show DataForSEO-only gaps that corroboration would close.

When Phase 3 activates, this wrapper becomes the DataForSEO adapter inside a multi-vendor aggregator that reconciles across sources. The wrapper's cache + spend guard + schema mapping remain; the aggregator adds cross-source reconciliation.
