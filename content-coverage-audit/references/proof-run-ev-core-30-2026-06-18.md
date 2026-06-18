---
type: coverage-audit-report
profile: core-30-service-city-seo
created: 2026-06-18
source_artifact_count: 102
output_artifact_count: 31
verdict: APPROVE-WITH-NOTES
blocking_count: 2
advisory_count: 4
tags: [coverage-audit, core-30-service-city-seo, ev-electric-services, acceptance-test]
---

# Content Coverage Audit — core-30-service-city-seo (EV Electric Services)

**Run date:** 2026-06-18
**Profile:** core-30-service-city-seo v1.0
**Client:** ev-electric-services
**Source artifacts scanned:** 102 glob-matched (9 service brief `*.md` [7 briefs + 2 meta], 15 city brief `*.md` [13 briefs + 2 meta], 32 intersection `*.md` [30 briefs + 2 meta], 8 service `*.json`, 22 city `*.json`, 16 competitor `*.txt`)
**Output artifacts scanned:** 31 files matching `**/draft-v*.md` across 30 Core 30 page folders
**Verdict:** APPROVE-WITH-NOTES (2 blocking, 4 advisory)

## Executive Summary

The audit reproduces the manual 2026-06-07 analysis. Three findings confirmed: (a) AJ Long teardown inventories (urls-problems/neighborhoods/guides) are extracted but operationally unused — zero references in 31 draft-v*.md pages; (b) per-service depth asymmetry — troubleshooting has full city-level data scaffolding (4/4 cities) while panel-upgrade and EV-charger have 0/4; (c) ranked expansion backlog of 6 tiers from housing-era sections to 200+ neighborhood pages.

## Lens 1: Utilization

### Competitor teardown inventories

| Source File | Line Count | Utilized in Draft Pages | Status |
|---|---|---|---|
| urls-problems.txt | 14 (13 URLs) | 0 references | **UNUSED** |
| urls-neighborhoods.txt | 219 (218 URLs) | 0 references | **UNUSED** |
| urls-guides.txt | 14 (13 URLs) | 0 references | **UNUSED** |
| problem-slugs.txt | 14 (13 slugs) | 0 references | **UNUSED** |
| neighborhood-slugs.txt | 219 (218 slugs) | 0 references | **UNUSED** |
| guide-slugs.txt | 14 (13 slugs) | 0 references | **UNUSED** |

**Finding:** The AJ Long teardown captured 13 problem URLs, 218 neighborhood URLs, and 13 guide URLs. These exist in `admin-extracts/competitor-research/aj-long-teardown/data/` but are not referenced in any Core 30 page content. The only usage is strategic planning (in `_build-order.md` meta doc), not content implementation.

### Research brief utilization

| Source Collection | Count | Utilized | Notes |
|---|---|---|---|
| Service briefs (Tier 1) | 6 | Yes — feeds service JSON templates | All 6 services have corresponding JSON data files |
| City briefs (Tier 2) | 13 | Partial — 4 of 13 cities have JSON data files | Bethesda-MD and Rockville-MD briefs not yet on disk |
| Intersection briefs (Tier 3) | 30 | Partial — feeds per-intersection positioning | Distribution is asymmetric (see L2) |

## Lens 2: Coverage Gaps / Asymmetry

### Per-service city-data coverage (parity fields)

| Service | quick_ref_localized | most_common_problem | neighborhood_problems | Cities with data | Status |
|---|---|---|---|---|---|
| troubleshooting | 4/4 cities | 4/4 cities | 4/4 cities | Vienna, Fairfax, McLean, Oakton | **at-parity** |
| light-fixture | 2/4 cities | 2/4 cities | 2/4 cities | McLean, Vienna | **under-fed** |
| smoke-alarm | 1/4 cities | 1/4 cities | 1/4 cities | Vienna only | **under-fed** |
| outlet-installation | 1/4 cities | 1/4 cities | 1/4 cities | Vienna only | **under-fed** |
| panel-upgrade | **0/4 cities** | **0/4 cities** | **0/4 cities** | none | **missing** |
| ev-charger | **0/4 cities** | **0/4 cities** | **0/4 cities** | none | **missing** |

### Per-service intersection brief coverage

| Service | Brief Count | Status |
|---|---|---|
| panel-upgrade | 10 | at-parity |
| emergency-electrician (troubleshooting) | 9 | at-parity |
| ev-charger-installation | 7 | at-parity |
| light-fixture-installation | 4 | under-fed |
| smoke-alarm-installation | 0 | **missing** |
| outlet-installation | 0 | **missing** |

### Asymmetry verdict

**Panel-upgrade and EV-charger pages are thinner than troubleshooting** because city-level data scaffolding (quick_ref_localized_items, most_common_problem_paragraph, specific_problems_neighborhood_phrase) is concentrated in troubleshooting. Panel and EV pages have zero cities' worth of structured localized problem data to draw from — they silent-degrade to generic content where troubleshooting pages have localized depth.

This is the DA2 class defect the handoff describes.

## Lens 3: Expansion Opportunities

| Rank | Proposal | Type | Evidence | Priority |
|---|---|---|---|---|
| 1 | Phase 2 service category hubs (6 pages) | new-artifact-type | All 6 services have >=3 city pages live; architectural trigger reached per build-order | high |
| 2 | "Issues by home era" subsections | new-section | All 4 anchor cities have >=3 documented housing eras with electrical implications | high |
| 3 | "Neighborhood-specific electrical problems" blocks | new-section | All 4 anchor cities have >=6 neighborhoods documented; competitor has 218 neighborhood pages | medium |
| 4 | Dedicated problem/symptom pages (new page type) | new-artifact-type | Competitor (AJ Long) has 13 problem URLs; EV has 0 dedicated problem pages | high |
| 5 | Dedicated guide/educational pages (new page type) | new-artifact-type | Competitor has 13 guide URLs; EV has 0 guide pages | medium |
| 6 | Dedicated neighborhood pages (scale play) | new-artifact-type | Competitor has 218 neighborhood URLs; EV has 0; massive long-tail opportunity | medium |

## Gate Verdict

**Verdict:** APPROVE-WITH-NOTES (blocking findings surfaced to operator)

**Blocking findings (2):**
- **F-1 (L2):** Panel-upgrade city data coverage: 0/4 cities — missing all parity fields (quick_ref, problem_paragraph, neighborhood_phrase). Pages will silent-degrade.
- **F-2 (L2):** EV-charger city data coverage: 0/4 cities — same missing-parity-field class as panel-upgrade.

**Advisory findings (4):**
- **F-3 (L1):** 6 competitor inventory files (244+ unique URLs) extracted but operationally unused in draft pages.
- **F-4 (L2):** Smoke-alarm and outlet-installation have 0 intersection briefs and only 1/4 cities with data.
- **F-5 (L3):** 3 new page types supportable from existing competitor architecture (problem, guide, neighborhood).
- **F-6 (L3):** Housing-era subsections supportable for all 4 anchor cities (all have >=3 eras).

## Acceptance Criterion Match

| Manual 2026-06-07 Finding | Engine Finding | Match |
|---|---|---|
| (a) AJ Long teardown urls-problems/neighborhoods/guides inventories extracted and never mined | L1: 6 inventory files (244+ URLs) with ZERO references in 31 draft-v*.md pages | CONFIRMED |
| (b) Troubleshooting pages have localized depth; panel/EV pages don't (DA2 asymmetry) | L2: Troubleshooting 4/4 cities; panel 0/4; EV 0/4 — missing parity fields | CONFIRMED |
| (c) Ranked expansion backlog of supportable new sections and page types | L3: 6-tier ranked backlog from housing-era sections to 200+ neighborhood pages | CONFIRMED |
