---
name: issue-categories
description: Taxonomy of SEO issues that the client-seo-audit skill can detect and prioritize
type: reference
created: 2026-06-22
updated: 2026-06-22
tags: [reference, seo-audit, issues, prioritization]
---

# SEO Issue Categories

Used by Step 5 (prioritize issues) to classify findings before ranking them.

## Categories

### RANK — Ranking deficits
Issues where the client is underperforming in search rankings.

| Issue type | Detection source | Impact signal |
|---|---|---|
| Not ranking for target keyword | `keyword_serps` — client absent from top 100 | search_volume of keyword |
| Ranking below page 1 (pos 11-20) | `keyword_serps` — client rank 11-20 | search_volume × (rank - 10) |
| Ranking below page 2 (pos 21+) | `keyword_serps` — client rank 21+ | search_volume |
| Competitor outranks on target keyword | `keyword_serps` — competitor rank < client rank | search_volume × rank_gap |

### LOCAL — Local pack issues
Issues specific to local-SEO / Google Maps visibility.

| Issue type | Detection source | Impact signal |
|---|---|---|
| Not in local 3-pack for target keyword | `keyword_serps` — no local_pack entry for client | search_volume (local intent keywords are high-conversion) |
| Competitor in 3-pack, client not | `keyword_serps` — competitor in pack, client absent | search_volume × competitor_count_in_pack |

### AUTHORITY — Backlink/domain authority gaps
Issues where the client's link profile is weaker than competitors.

| Issue type | Detection source | Impact signal |
|---|---|---|
| Referring domains gap | `backlink_profile` vs `competitor_overview` | gap_size × competitor_rank |
| Low domain rank | `backlink_profile` — rank < 20 | inverse of rank |
| Competitor backlink advantage | `competitor_overview` — competitor has ≥2× more referring domains | ratio × search_volume_overlap |

### CONTENT — Content gaps
Issues where the client lacks content for rankable keywords.

| Issue type | Detection source | Impact signal |
|---|---|---|
| High-volume keyword with no page | `keyword_research` — keyword has volume, no client URL ranking | search_volume |
| Thin content vs competitor | `competitor_overview` — competitor has page, client doesn't | competitor_rank × search_volume |
| Missing service-city page | `keyword_serps` — "[service] [city]" not covered | search_volume × local_intent_multiplier |

### TECHNICAL — On-page technical issues
Issues with the client's website technical SEO.

| Issue type | Detection source | Impact signal |
|---|---|---|
| Missing or short title tag | `on_page_audit` — title_length < 30 or > 60 | page_importance |
| Missing meta description | `on_page_audit` — description empty or < 50 chars | page_importance |
| Missing H1 | `on_page_audit` — h1_count == 0 | page_importance |
| Multiple H1 tags | `on_page_audit` — h1_count > 1 | low (usually cosmetic) |
| Images without alt text | `on_page_audit` — images_without_alt > 0 | count × accessibility_weight |
| Low internal linking | `on_page_audit` — internal_links_count < 5 | page_importance |

## Priority scoring

When prioritization skill is available, issues are ranked using:

1. **Impact** = search_volume × rank_gap_or_absence_penalty
2. **Effort** = estimated work to fix (content > technical > on-page tweak)
3. **Quick win** = already ranking 11-20 (push to page 1 with less effort)

When prioritization skill is NOT available (graceful degrade):
- Sort by `impact` descending
- Group by category
- Flag quick wins (rank 11-20) at the top regardless of impact score
