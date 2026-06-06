---
name: core-30-service-city-seo
version: 1.0
created: 2026-06-06
updated: 2026-06-06
description: Prioritization profile for Core 30 service-by-city SEO page builds. Lexicographic mode — service priority is the primary key, city/geographic anchor is the secondary key, competitive opportunity and content reuse are tie-breakers. Extracted from the EV Electric Services and S&H Contracting build-order files (2026-05-23 / 2026-05-28).
domain: service-by-city SEO page builds
tags: [profile, prioritization, core-30, seo, page-build, service-city]
---

# Profile: `core-30-service-city-seo`

Ranks service-by-city SEO page candidates for a Core 30 build. Designed to reproduce the ordering logic used in the EV Electric Services and S&H Contracting build-order files.

## Scoring mode

`lexicographic`

Criteria are listed in strict priority order. Criterion 1 is the primary sort key; criterion 2 breaks ties within criterion 1 buckets; and so on. A lower-priority criterion never overrides a higher one.

## Criteria (in priority order)

### 1. `service_priority`

- **Label:** Service priority
- **Description:** How important is this service line to the business, per operator/stakeholder input. Top-revenue or brand-lead services rank highest.
- **Direction:** `higher-is-better`
- **Values:** Ordered list, defined per client at intake. Example (EV): `[troubleshooting, panel-upgrade, ev-charger, light-fixtures, smoke-alarm, outlets-switches]`. Example (S&H): `[panel-upgrade, emergency-electrician, ev-charger, light-fixture]`.
- **How to populate:** Read the client's intake notes, kickoff meeting, or operator-stated service priority. The operator's ranking is authoritative.

### 2. `city_anchor`

- **Label:** City / geographic anchor priority
- **Description:** How close or strategically important is this city relative to the business's geographic anchor point (HQ, primary service area). Anchor cities rank highest; expansion cities rank lowest.
- **Direction:** `higher-is-better`
- **Values:** Ordered list, defined per client based on geographic strategy. Example (EV): `[vienna, fairfax, mclean, oakton, tysons, falls-church, burke, annandale, bethesda, rockville, chevy-chase, potomac, dc]`. Example (S&H): `[woodbridge, lake-ridge, manassas, dale-city, lorton, springfield, alexandria, burke, stafford]`.
- **How to populate:** Read the client's service area, HQ location, and geographic expansion strategy. Anchor cities (HQ + immediate neighbors) rank first; boundary/overlap zones rank middle; max-reach cities rank last.

### 3. `competitive_opportunity`

- **Label:** Competitive opportunity
- **Description:** How easy or valuable is it to rank for this service-city combination? Uncontested queries, high search volume with low competition, or existing topical authority boost a candidate.
- **Direction:** `higher-is-better`
- **Values:** `[uncontested, low-competition, moderate-competition, high-competition]`
- **How to populate:** Read competitor synthesis, keyword difficulty data, or the client's existing SERP positions. If no competitive data is available, default to `moderate-competition` (neutral).

### 4. `content_reuse`

- **Label:** Content reuse / effort reduction
- **Description:** How much of this page's content can be reused from an already-built sibling page (same service in a different city, or same city for a different service)? Higher reuse = faster build = rank boost.
- **Direction:** `higher-is-better`
- **Values:** `[high-reuse, moderate-reuse, low-reuse, no-reuse]`
- **How to populate:** Check if a sibling page (same service, different city) already exists or is sequenced earlier. If yes, estimate content reuse percentage: high (60%+), moderate (30-60%), low (<30%), none.

### 5. `strategic_differentiation`

- **Label:** Strategic differentiation
- **Description:** In multi-client or competitive contexts, how clearly can this candidate be positioned relative to competitors or sibling clients in the same market? Geographic exclusives rank highest; overlap zones requiring positioning work rank lower.
- **Direction:** `higher-is-better`
- **Values:** `[geographic-exclusive, differentiated-positioning, overlap-undifferentiated]`
- **How to populate:** Check if the city is in a geographic exclusive zone (no sibling client competes), a boundary zone (sibling client also targets, but positioning is differentiated), or an undifferentiated overlap (same service, same city, no clear angle). Default to `geographic-exclusive` for single-client engagements.

## Default dependency rules

Dependencies are hard topological constraints, not scoring criteria. Common patterns for Core 30 builds:

- **Anchor-city-first:** The first page for each service should be in the anchor city (establishes the template pattern before city variations).
- **License/jurisdiction gating:** Pages in jurisdictions requiring license verification are gated on that verification completing. Express as `must_before: [license-verification-<jurisdiction>, <gated-page-id>]`.
- **Phase gating:** Phase 2 items (category hub pages, geographic expansion) depend on Phase 1 reaching a threshold (e.g., 12+ pages live).

These are expressed per-client in the candidate set's `constraints` block, not hard-coded here.

## Output preferences

- **Human-readable title:** "Core 30 build order — `<client_name>`"
- **Table columns:** `#`, `Slug`, `Service`, `City`, `Priority tier`, `Rationale`
- **Priority tier labels:** Map rank ranges to `High` / `Medium` / `Low` for operator readability. Suggested: top third = High, middle third = Medium, bottom third = Low.

## Extraction source

This profile was extracted from:
- `second-brain/04_projects/clients/_active/ev-electric-services/website-archive/new/core-30/_build-order.md` (2026-05-23)
- `second-brain/04_projects/clients/_active/s-and-h-contracting/website-archive/new/core-30/_build-order.md` (2026-05-28)

The de-facto scoring model in both files uses the same 4-criterion lexicographic hierarchy (service priority → city anchor → competitive opportunity → content reuse), with S&H adding a 5th (strategic differentiation vs sibling client). This profile generalizes both into a single reusable configuration.

## No-regression test

Given the EV or S&H candidate sets with their respective `service_priority` and `city_anchor` orderings, this profile must produce the same page sequencing as the manually-authored `_build-order.md` files. "Same" means equivalent ranking — not byte-identical output.
