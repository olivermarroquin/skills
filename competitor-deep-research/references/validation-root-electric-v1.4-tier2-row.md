---
type: validation
status: complete
created: 2026-06-16
skill: competitor-deep-research
skill-version: 1.4
validated-on: rootelectric.com
purpose: End-to-end validation of the v1.4 15-column Tier-2 row (5 new cross-arena columns)
---

# Validation: Root Electric — v1.4 Tier-2 Row (15 columns)

**Date:** 2026-06-16
**Target:** Root Electric Services (rootelectric.com), Woodbridge VA
**Source set:** MI-3/MI-3b composite scorecard (2026-06-14/15) + live probes (2026-06-16)

## Complete 15-column Tier-2 row

| # | Column | Value | Source |
|---|---|---|---|
| 1 | **Domain** | rootelectric.com | Direct |
| 2 | **Page count** | 159 (94 posts + 65 pages; tcb_symbol excluded) | `sitemap_index.xml` → `post-sitemap.xml` + `page-sitemap.xml`, live probe 2026-06-16 |
| 3 | **Tech stack** | WordPress + Thrive Architect + Rank Math; Apache; schema present (LocalBusiness) | HTTP headers (`server: Apache`), `wp-json` link header, Rank Math sitemap comment, Thrive `tcb_symbol-sitemap`, homepage JSON-LD |
| 4 | **Top 5 keywords** | electrician woodbridge va (#1), electrical contractor woodbridge (#2), emergency electrician woodbridge (#3), panel upgrade woodbridge (#4), ev charger installation woodbridge (#5) | MI-3 DataForSEO `ranked_keywords/live` 2026-06-14 (916 total ranked keywords, 73 in top-3) |
| 5 | **Backlinks** | 350 referring domains (backlinks leader in field) | MI-3 DataForSEO `backlinks/summary` 2026-06-14 (trial) |
| 6 | **DA / DR** | DR not directly measured; authority proxy: 350 referring domains (highest in field) | MI-3 DataForSEO Backlinks trial 2026-06-14 |
| 7 | **Avg rank for head keyword** | Position ~2–4 for "electrician woodbridge va" | MI-3 DataForSEO SERP 2026-06-14 |
| 8 | **Service-page words** | ~2,200 (panel upgrade page) | MI-3 site-capture-engine teardown (Root Electric dossier) |
| 9 | **FAQ count** | 5 on sampled service page | MI-3 teardown — Root panel-upgrade page |
| 10 | **Schema types** | LocalBusiness, Service, BreadcrumbList | MI-3 teardown + live homepage JSON-LD probe 2026-06-16 |
| **11** | **AI-citation flag (V3)** | **Cited (3+ engines)** — Sonar 6/6 prompts, Otterly baseline 2nd behind AJ Long, fresh probes show Root rising fast | MI-3 Sonar API (`mi3_sonar.py`) 2026-06-14; Otterly snapshot 2026-05-26; MI-3b scorecard §3 |
| **12** | **Local-pack flag (V2)** | **In 3-pack (position varies by term)** — present in centroid 3-pack for "electrician woodbridge va"; AJ Long dominates Fairfax centroid but Root strong in Woodbridge grid | MI-3 DataForSEO SERP `local_pack` 2026-06-14; Local Falcon geo-grid (partial, EV grid) 2026-06-16 |
| **13** | **Paid/LSA flag (V4)** | **Active (47 ads)** — V4 leader in field. Woodbridge-targeted Search ads, all Google Verified. Last seen 2026-06-13. | MI-3b Google Ads Transparency Center (Chrome) 2026-06-15; scorecard §2b |
| **14** | **Review velocity (M1)** | **112 Google reviews, 4.8★** — velocity estimated ~3–4 reviews/month (based on MI-3 snapshot vs prior BrightLocal baseline). Yelp: 33 reviews. BBB: accredited. Checkbook: 59 ratings (88% superior). No review-generation widget detected on site. | MI-3 DataForSEO `my_business_info` 2026-06-14; Yelp live 2026-06-16; Checkbook live 2026-06-16 |
| **15** | **Social/video flag (V5)** | **Active (channels: IG, YT, TikTok, FB, Twitter)** — IG 133 posts/29 followers, YT 269 videos/87 subscribers, FB linked in schema. High production cadence, near-zero reach. Educational owner-on-camera Reels format. Smash Balloon IG embed on site. | MI-3b scorecard §8 (DG-18 Root social deep-dive) 2026-06-15; homepage live probe 2026-06-16 (schema `sameAs` confirms FB+Twitter) |

## Observations

1. **All 15 columns populated and sourced.** The 5 new cross-arena columns (11–15) each have a cited source and a concrete value — no "unknown" flags needed for this competitor.

2. **Cross-arena story is clear from one row:** Root is the broadest-arena competitor in this field — active in organic (V1), local-pack (V2), AI citations (V3), paid ads (V4, field leader with 47 ads), and social/video (V5, highest production volume). But review velocity (M1) is moderate (112 total, ~3-4/mo) — a clear gap vs AJ Long's 1,147 reviews.

3. **The dual-path method works:** Columns 11 (V3) and 14 (M1) used DataForSEO/Sonar (paid path). Columns 13 (V4) and 15 (V5) used free tools (Transparency Center + direct channel visit). Column 12 (V2) piggybacks on the existing SERP call. No additional paid cost beyond what columns 1–10 already consume.

4. **Incremental time:** ~15 minutes per competitor for the 5 new columns on top of the existing ~10-15 minutes for columns 1–10. The V4 Transparency Center check (Chrome) is the slowest step (~3-5 minutes); the rest are fast lookups.

5. **Homepage WebFetch confirmed:** Root's homepage is WordPress/Thrive (not SPA), so WebFetch works cleanly. Schema `sameAs` confirms FB + Twitter. No Podium/Birdeye/NiceJob review widgets detected — Root relies on organic review accumulation, not a review-generation tool.

## Boundary verification

- **Roll-up NOT produced here.** This is a per-competitor row. The composite scoring (Root = 32, #1 overall) and the perfect-company-profile synthesis live in `market-intelligence-engine` output, not in this skill's Tier-2 table. Boundary clean.
- **Geo-grid NOT expanded.** Column 12 records centroid 3-pack presence only. Full geo-grid (7×7 grid × 6 terms) stays in the MI engine's scope. Boundary clean.
