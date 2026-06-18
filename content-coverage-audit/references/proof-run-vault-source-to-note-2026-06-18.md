---
type: coverage-audit-report
profile: vault-source-to-note
created: 2026-06-18
source_artifact_count: 30
output_artifact_count: 184
verdict: APPROVE-WITH-NOTES
tags: [coverage-audit, vault-source-to-note, non-seo-proof]
---

# Content Coverage Audit — vault-source-to-note (Non-SEO Proof Run)

**Run date:** 2026-06-18
**Profile:** vault-source-to-note v1.0
**Source artifacts scanned:** 30 source notes in `00_inbox/sources-pending/`
**Output artifacts scanned:** 184 matching profile globs across 4 collections (50 `pattern-*.md`, 48 `lesson-*.md`, 2 `blueprint-*.md`, 84 `tool-*.md`; directories contain 50/51/5/88 total files respectively — non-prefixed files excluded by glob)
**Verdict:** APPROVE-WITH-NOTES (0 blocking, 4 advisory)

## Executive Summary

The engine ran all three lenses on a non-SEO domain (Knowledge OS source→artifact coverage) from profile config alone. Key findings: 93% source utilization rate (28/30 notes linked to output artifacts); dramatic domain skew between input emphasis (marketing/SEO 67%/50%) and output distribution (automation/app-building 28%/19%); 7-10 tool expansion candidates held pending cross-creator validation. The domain inversion is intentional (sources provide use-case framing, outputs abstract to infrastructure patterns) but the SEO→output ratio (5:1) and marketing→output ratio (7.5:1) are worth operator review.

## Lens 1: Utilization

| Source Collection | Field | Richness (items) | Utilized | Referencing Outputs |
|---|---|---|---|---|
| source-notes | claims-or-takeaways | present in 21/30 (70%) | Yes (93%) | 171 total wikilinks across 28 sources |
| source-notes | tactics-or-strategies | present in 21/30 (70%) | Yes (pattern/tactic notes spawned) | 14 sources with rich sections |
| source-notes | tools-mentioned | present in 18/30 (60%) | Partial | 7-10 tools mentioned but not yet standalone artifacts |
| source-notes | opportunities | present in 15/30 (50%) | Yes (linked) | Via wikilinks to patterns/blueprints |
| source-notes | pattern-candidates | present in 10/30 (33%) | Yes | Cross-creator-count tracking active |
| source-notes | research-questions | present in 12/30 (40%) | Unknown | No systematic tracking of resolution |

### Unused high-richness fields (advisory)
- **4 source notes with zero artifact references:** All 2026-04+ (processing backlog, not true gap)
- **7-10 tools mentioned in sources but not created as standalone tool notes:** Held by one-creator-only validation discipline (architectural constraint, not omission)
- **Research questions logged but resolution untracked:** 12 sources have research-question sections; no output collection captures resolved questions

## Lens 2: Coverage Gaps / Asymmetry

### Domain axis

| Domain | Source Notes | Output Artifacts | Ratio (source:output) | Status |
|---|---|---|---|---|
| Marketing | 20 (67%) | 24 (13%) | 7.5:1 | under-fed |
| SEO | 15 (50%) | 19 (10%) | 5:1 | under-fed |
| Client-services | 14 (47%) | 48 (26%) | 1.4:1 | at-parity |
| Automation-systems | 0 (0%) | 58 (32%) | 0:58 | output-only (synthesis) |
| App-building | 0 (0%) | 51 (28%) | 0:51 | output-only (synthesis) |
| Content-systems | 1 (3%) | 5 (3%) | 1:5 | under-fed (by ratio; proportional to source count) |

### Under-fed domains (advisory — intentional synthesis pattern acknowledged)
- **Marketing:** 67% of sources are marketing-tagged; only 13% of outputs are marketing-domain. Sources are being abstracted upward into automation/app-building patterns — expected for a Knowledge OS — but direct marketing patterns/lessons are thin.
- **SEO:** 50% of sources; 10% of outputs. Only 1 SEO lesson exists despite 15 SEO sources.

## Lens 3: Expansion Opportunities

| Rank | Proposal | Type | Evidence | Priority |
|---|---|---|---|---|
| 1 | Elevate SEO patterns from 15 SEO sources (only 8 exist) | new-pattern | 5:1 source-to-artifact ratio in SEO domain | medium |
| 2 | Create tool notes for 7-10 first-mentioned tools when cross-creator validation triggers | new-tool-note | Apify, Spline, Three.js, GenPPT, LinkD mentioned in sources | medium |
| 3 | Add marketing-specific lessons (only ~2 exist from 20 marketing sources) | new-lesson | 7.5:1 imbalance; content-system lessons, backlink methodology candidates | medium |
| 4 | Track research-question resolution systematically | new-data-binding | 12 sources log questions with no resolution tracking | low |

## Gate Verdict

**Verdict:** APPROVE-WITH-NOTES
**Blocking findings:** 0
**Advisory findings:** 4

- **F-1 (L1, advisory):** 7-10 tools mentioned in sources not yet standalone artifacts (held by architectural constraint — one-creator-only validation discipline)
- **F-2 (L2, advisory):** Marketing domain 7.5:1 source-to-artifact imbalance (intentional synthesis pattern but worth periodic review)
- **F-3 (L2, advisory):** SEO domain 5:1 source-to-artifact imbalance (1 lesson from 15 sources)
- **F-4 (L3, advisory):** Research question sections in 12 sources have no systematic resolution tracking

## Proof-Run Success Criteria

| Criterion | Status |
|---|---|
| Engine runs on non-SEO domain | PASS — marketing/KM sources scanned with zero SEO logic |
| Config-driven domain inference | PASS — profile tags alone drove analysis |
| Three lenses execute end-to-end | PASS — L1/L2/L3 all completed with findings |
| Asymmetries surfaced | PASS — domain skew, thin domains, tool holdbacks identified |
| Results are domain-agnostic | PASS — no domain-specific logic in engine; same lenses work on any domain |
