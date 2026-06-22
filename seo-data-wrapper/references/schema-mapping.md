---
name: schema-mapping
description: Maps DataForSEO MCP response fields onto market-intelligence-engine arena schema and competitor-deep-research columns
type: reference
created: 2026-06-22
updated: 2026-06-22
tags: [reference, schema, mapping, dataforseo, market-intelligence, competitor-deep-research]
---

# DataForSEO → Vault schema mapping

This reference defines how raw DataForSEO MCP tool responses are transformed into structured data consumable by the `market-intelligence-engine` arena model and `competitor-deep-research` column format.

## Market-intelligence arena mappings

### V1 — Google organic

**Source endpoints:**
- `dataforseo_labs_google_domain_rank_overview` → `metrics.organic`
- `dataforseo_labs_google_ranked_keywords` → top items by rank

**Mapped output:**
```json
{
  "arena": "V1",
  "score": null,
  "metrics": {
    "organic_keywords_count": "metrics.organic.count",
    "organic_etv": "metrics.organic.etv",
    "organic_keywords_top_10": "metrics.organic.pos_1 + pos_2_3 + pos_4_10",
    "top_keywords": [
      {
        "keyword": "items[].keyword_data.keyword",
        "position": "items[].ranked_serp_element.serp_item.rank_group",
        "search_volume": "items[].keyword_data.keyword_info.search_volume",
        "url": "items[].ranked_serp_element.serp_item.relative_url"
      }
    ]
  },
  "source": "DataForSEO Labs",
  "proxy": false
}
```

**Score derivation (V1, 0-5):**
- 5 = ≥50 top-10 organic keywords + ETV ≥1000
- 4 = ≥20 top-10 keywords + ETV ≥500
- 3 = ≥10 top-10 keywords + ETV ≥100
- 2 = ≥5 top-10 keywords
- 1 = some organic presence but <5 top-10
- 0 = no organic rankings found

### V2 — Local pack / Maps

**Source endpoint:**
- `serp_organic_live_advanced` with `location_name` set to city level

**Detection:** scan `items[]` for `type == "local_pack"`. Within `local_pack.items[]`, check if client domain or GBP name appears.

**Mapped output:**
```json
{
  "arena": "V2",
  "score": null,
  "metrics": {
    "local_pack_present": true,
    "client_in_local_pack": false,
    "client_position": null,
    "total_local_pack_results": 3
  },
  "source": "DataForSEO SERP",
  "proxy": false
}
```

**Score derivation (V2, 0-5):**
- 5 = in 3-pack position 1 for ≥50% of target keywords
- 4 = in 3-pack for ≥50% of target keywords
- 3 = in 3-pack for some target keywords
- 2 = appears in maps but not 3-pack for target keywords
- 1 = GBP exists but not ranking for any target keywords
- 0 = no local pack presence detected

### A1 — Topical authority + E-E-A-T

**Source endpoint:**
- `backlinks_summary`

**Mapped output:**
```json
{
  "arena": "A1",
  "score": null,
  "metrics": {
    "total_backlinks": "backlinks",
    "referring_domains": "referring_domains",
    "referring_domains_nofollow": "referring_domains_nofollow",
    "domain_rank": "rank",
    "broken_backlinks": "broken_backlinks",
    "referring_ips": "referring_ips"
  },
  "source": "DataForSEO Backlinks",
  "proxy": false
}
```

**Score derivation (A1, 0-5):**
- 5 = ≥350 referring domains + rank ≥50
- 4 = ≥150 referring domains + rank ≥30
- 3 = ≥50 referring domains
- 2 = ≥20 referring domains
- 1 = <20 referring domains but some backlinks
- 0 = no backlink data found

## Competitor-deep-research column mappings

These map onto the 15-column Tier-2 light scan defined in `competitor-deep-research` v1.4.

| Column # | Column name | DataForSEO endpoint | Field path |
|---|---|---|---|
| 1 | Domain | (input) | — |
| 4 | Top 5 keywords | `ranked_keywords` | `items[0:5].keyword_data.keyword` (sorted by `rank_group` asc) |
| 5 | Total backlinks | `backlinks_summary` | `backlinks` |
| 6 | Domain rank | `backlinks_summary` | `rank` |
| 7 | Avg rank for head keyword | `serp_organic_live_advanced` | client's `rank_group` in results |
| 12 | Local-pack flag V2 | `serp_organic_live_advanced` | `items[].type == "local_pack"` → client position |
| 14 | Review velocity M1 | (not from DataForSEO — from GBP/external) | — |

Columns 2, 3, 8, 9, 10, 11, 13, 15 require non-DataForSEO sources (sitemap crawl, Chrome, Sonar) and are NOT populated by this wrapper. The audit skill fills those from other compose targets or marks them `[data-source-needed]`.

## Keyword research output

For `keyword_research` operations, the wrapper returns:

```json
{
  "target_keywords": [
    {
      "keyword": "string",
      "search_volume": 0,
      "cpc": 0.00,
      "competition": 0.0,
      "competition_level": "LOW|MEDIUM|HIGH",
      "search_intent": "informational|transactional|navigational|commercial",
      "monthly_searches": [{"year": 2026, "month": 6, "search_volume": 0}]
    }
  ],
  "related_keywords": [],
  "keywords_for_site": []
}
```

## On-page audit output

For `on_page_audit` operations:

```json
{
  "url": "string",
  "meta": {
    "title": "string",
    "description": "string",
    "h1": "string",
    "canonical": "string"
  },
  "checks": {
    "title_length": 0,
    "description_length": 0,
    "h1_count": 0,
    "images_without_alt": 0,
    "internal_links_count": 0,
    "external_links_count": 0
  },
  "performance": {
    "size_bytes": 0,
    "time_to_interactive_ms": null
  }
}
```
