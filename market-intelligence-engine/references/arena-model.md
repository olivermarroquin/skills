---
type: skill-reference
skill: market-intelligence-engine
created: 2026-06-16
updated: 2026-06-16
tags: [skill-reference, market-intelligence, arena-model, scoring]
---

# Arena model — `market-intelligence-engine`

Restructured from the spec §3 flat-7 into **5 visibility arenas + 2 cross-cutting multipliers +
1 authority/depth axis** (operator-confirmed 2026-06-14). Maps directly to the Root Electric lesson:
Root didn't win a new place — it won organic + reviews + topical-authority depth across multiple arenas.

---

## Visibility arenas (where you show up) — scored 0-5 each

| # | Arena | What it measures | Primary data source / tool | Scoring anchors |
|---|---|---|---|---|
| V1 | **Google organic** | Ranked keywords, top-3 count, ETV, SERP-feature ownership, content depth | DataForSEO `domain_rank_overview` + `ranked_keywords` + `competitor-deep-research` Tier-2 | 5 = arena leader (e.g. 916kw / 73 top-3 / $10.5K ETV); 3 = competitive presence; 0 = no rankings |
| V2 | **Local pack / Maps** | Geo-grid rank, GBP completeness, categories, proximity weighting | Local Falcon geo-grid + BrightLocal + DataForSEO SERP `local_pack` + Google Maps | 5 = city-center 3-pack owner with review volume; 3 = appears in some packs; 0 = invisible (must be defended) |
| V3 | **AI answer engines** | Citation/visibility in ChatGPT / Perplexity / Gemini / Google AI Overviews for head terms | Otterly / Profound / Peec + Perplexity Sonar probes + manual probes + HubSpot AEO Grader | 5 = cited #1 across ≥2 engines for head terms; 3 = cited in some; 0 = absent across ≥3 engines |
| V4 | **Paid / LSA** | Google Ads presence, Local Services Ads, "Google Guaranteed" badge, ad density | Google Ads Transparency Center (Chrome) + live SERP sweep (mobile+desktop × geos) + Meta Ad Library | 5 = 27+ live ads with geo-targeting; 3 = active but thin; 0 = no ads (must be defended via TC + breadth SERP) |
| V5 | **Social / video** | YouTube/TikTok/IG presence, content cadence, engagement, video-in-SERP | Competitor site embeds + direct channel visits (IG/TikTok/YT/FB) | 5 = weekly cadence + distribution + engagement; 3 = present; 0 = searched ≥3 platforms, none found |

## Cross-cutting multipliers (multiply every visibility arena) — scored 0-5 each

| # | Multiplier | What it measures | Primary data source / tool | Scoring anchors |
|---|---|---|---|---|
| M1 | **Reviews / reputation** | Count, **velocity** (the durable lever), rating, response rate, platform spread | DataForSEO `my_business_info` + BrightLocal Reputation + SERP `local_pack` rating + Yelp/Angi/BBB | 5 = count leader OR velocity leader (distinguish — AJ Long 1,147 count vs Absolute 12.8/mo velocity); 0 = n/a |
| M2 | **Conversion / offer** | CTA system, financing, booking/voice AI, forms, sticky mobile, offer strength | `site-capture-engine` homepage capture + PageSpeed + BuiltWith/Wappalyzer tech detection | 5 = full stack (booking + financing + voice/chat AI + sticky mobile CTA); 3 = partial; 0 = n/a |

## Authority / depth axis — scored 0-5

| Axis | What it measures | Primary data source / tool | Scoring anchors |
|---|---|---|---|
| **A1 Topical authority & E-E-A-T** | Backlink profile + authority, topical depth/coverage, real expertise signals (owner voice, credentials, years), entity/knowledge-graph presence | DataForSEO `backlinks/summary` + `referring_domains` + content-depth audit + Google Knowledge Panel + Wikidata | 5 = 350+ locally-earned ref-domains + entity presence; 3 = moderate backlink profile; 0 = near-zero ref-domains |

---

## Composite scoring

**Composite = sum of 8 arena scores (max 40).** Rank competitors by composite.

Every cell must show:
- The **inline metric** (the number that justifies the score).
- The **source** (the pull/observation that produced the metric).
- **Proxy label** if the metric is estimated, not directly measured.

A cell scored 0 must be a **defended zero** per the no-undefended-zero guard (SKILL.md Phase 5).

---

## Electrician-field calibration (from [MI-3b] §9 V4-corrected final)

| Rank | Competitor | V1 | V2 | V3 | V4 | V5 | M1 | M2 | A1 | Composite |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Root Electric | 5 | 3 | 5 | 5 | 2 | 3 | 4 | 5 | 32 |
| 2 | PRO Electric | 4 | 3 | 4 | 4 | 1 | 4 | 4 | 4 | 28 |
| 3t | Absolute Electric | 3 | 3 | 3 | 2 | 1 | 5 | 5 | 4 | 26 |
| 3t | Kolb Electric | 3 | 2 | 3 | 4 | 1 | 3 | 5 | 5 | 26 |
| 3t | AJ Long Electric | 5 | 4 | 3 | 0 | 1 | 5 | 5 | 3 | 26 |
| 6 | Mr. Electric (franchise) | 3 | 3 | 3 | 2 | 2 | 3 | 3 | 1 | 20 |

This table is **reference calibration only** — not hardcoded into the skill. Each new run produces
its own scorecard from data.
