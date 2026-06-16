---
type: skill-reference
skill: market-intelligence-engine
created: 2026-06-16
updated: 2026-06-16
tags: [skill-reference, market-intelligence, arena-source-checklist, completeness]
---

# Arena source checklist — `market-intelligence-engine`

Canonical reference: `[[mi-arena-source-checklist]]` in the market-intelligence handoff folder.
This file is a skill-local copy for engine execution. If the canonical version is updated,
this copy must be synced.

---

## The three completeness rules (gate-enforced)

1. **No "empty/0" from a single source or thin sample.** Scoring 0 or "absent" requires >=2
   independent sources AND breadth across relevant dimensions (e.g., for ads: device x geo x query).
   Unmet = "unknown / under-sampled," not 0. A real zero is a *defended* zero.

2. **Enumerate before you score.** For each arena, list every source and mark it used (with evidence)
   or skipped (with reason + owning follow-up). No silent single-sourcing.

3. **Adversarial completeness pass before lock.** For every weak/zero/low cell, actively try to
   disprove it: "where would a strong competitor show in this arena, and did I look there?" Only lock
   once you've tried to break it.

---

## Substrate preconditions

- **Verify Chrome is connected BEFORE the run.** If not, stop and tell the operator — do not
  silently substitute WebFetch and defer.
- **WebFetch-empty on a JS page = escalate to Chrome, not a residual.**

---

## Per-arena source checklist

| Arena | Primary | Secondary | Public registries (often missed) | Min bar to SCORE | Min bar to claim ZERO |
|---|---|---|---|---|---|
| V1 organic | DataForSEO `domain_rank_overview` / `ranked_keywords` | Live SERP advanced; Search Console (own clients) | -- | 1 ranking pull | n/a (can always score) |
| V2 local pack | DataForSEO SERP `local_pack`; Local Falcon geo-grid | BrightLocal local rank; manual map check | Google Maps | Geo-grid OR >=2 city-center pulls | Not in grid across full service area |
| V3 AI engines | Otterly (multi-engine); Perplexity Sonar | DataForSEO `ai_optimization`/`llm_mentions`; manual ChatGPT/Gemini/AIO probes | HubSpot AEO Grader (free, no-account) | >=2 engines queried | Absent across >=3 engines |
| V4 paid / LSA | Live SERP ads (mobile + desktop x multiple geos x broad query set) | LSA pack + Google Verified badge | **Google Ads Transparency Center** (creatives + regions + date-range); **Meta Ad Library** | Transparency Center OR live ad sighting | Transparency Center checked AND breadth SERP sweep -- BOTH clean |
| V5 social | Competitor site embeds | Direct channel visits (IG/TikTok/YT/FB) -- cadence, engagement | **Meta Ad Library**; YouTube channel pages | >=1 channel confirmed | Name searched on >=3 platforms, none found |
| M1 reviews | DataForSEO `my_business_info`; BrightLocal Reputation | SERP `local_pack` rating; Yelp/Angi/BBB counts | Google Maps profile | 1 fresh count pull | n/a (can always score) |
| M2 conversion | `site-capture-engine` / homepage capture (Chrome for JS sites) | PageSpeed (CWV); booking/financing tech detection | BuiltWith / Wappalyzer | Homepage captured | n/a (can always score) |
| A1 authority | DataForSEO `backlinks/summary` + `referring_domains` | Content-depth audit; entity/knowledge-panel probe | **Google Knowledge Panel**; **Wikidata** | Backlink pull completed | n/a (can always score) |

---

## How this enters the engine

- **Phase 2** (arena-source enumeration): the engine walks this checklist for every in-scope arena
  and marks each source PLANNED or SKIPPED-with-reason.
- **Phase 4** (completion-vs-plan): diffs planned vs collected per source.
- **Phase 5** (no-undefended-zero guard): checks the three completeness rules before allowing a 0.
- **Phase 6** (adversarial completeness pass): uses this checklist to identify unchecked signal sources.
- **G-market-intel check #5**: verifies the filled checklist is present as a run artifact.
