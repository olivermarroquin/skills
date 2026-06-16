---
type: skill-reference
skill: market-intelligence-engine
created: 2026-06-16
updated: 2026-06-16
tags: [skill-reference, market-intelligence, composition, boundaries]
---

# Composition map — what this engine orchestrates vs what it owns

This document defines the §2a boundaries: what each composed skill owns and what this engine
uniquely owns. The rule is **compose, don't duplicate** — the engine orchestrates existing skills
and adds the cross-arena layer none of them cover.

---

## What each composed skill owns (engine calls it, does not re-implement)

### `competitor-deep-research` v1.4

**Owns:** organic/content/positioning landscape.
- Tier-2 15-column light scan (including MI-7 cols 11-15: V3/V2/V4/M1/V5 arena-presence flags).
- Tier-1 deep per-competitor briefs (9-step forensic research).
- Cross-competitor synthesis.
- Folder hygiene + output-quality-loop.

**Boundary note (from v1.4):** "These columns capture per-competitor arena presence flags. The
multi-arena roll-up, composite scoring, and perfect-company-profile synthesis stays in
`market-intelligence-engine` (spec §2 boundary). This skill surfaces the raw signal; the engine
interprets it."

**Engine calls it for:** Tier-2 scan results feed Phase 1 (competitor confirmation) + Phase 7
(scoring V1 + arena-presence flags for V2-V5/M1). Tier-1 deep briefs feed Phase 8 (deep-N).

### `site-capture-engine` v2.2

**Owns:** deep-site forensic teardown (6-pass, 3 output contexts).
- Pass 3 step 6: local-pack presence snapshot (V2 point-in-time).
- Pass 4 step 2: review-velocity + reputation snapshot (M1 structured data).

**Boundary note (from v2.2):** "Point-in-time snapshots only; trend analysis + geo-grid coverage
stays in `market-intelligence-engine`."

**Engine calls it for:** Phase 8 (deep-N teardowns of top competitors). Feeds back into scoring
for M2, A1, and point-in-time V2/M1 snapshots.

### `seo-tooling-landscape-research` v2.0

**Owns:** tool-gap + tool-discovery + tool-intake engine.
- Survey mode: comprehensive tool landscape.
- Discovery mode: recurring scan for new/emerging tools.
- Intake mode: single-tool evaluation from operator drops.
- Tool-eval rubric.
- `_data-gap-register.md` append (tool-gap entries).

**Boundary:** tool adoption decisions stay there. Engine reads the register, routes tool-gap
findings to discovery/intake. Arena scoring stays in the engine.

**Engine calls it for:** Phase 9 (gap-discovery → route tool gaps to discovery/intake mode).

### `multi-source-synthesis` v1.0

**Owns:** synthesis document production.
- Four shapes: cluster, pattern, cross-cluster, client-driven.
- Confirmation gate (shape + destination) before drafting.
- `meta-document-primer` companion.

**Engine calls it for:** Phase 10 (Output A, cross-cluster shape) + Phase 11 (Output B,
client-driven shape). Engine feeds structured arena data; synthesis skill produces the document.

### Research skills (`service-seo-research`, `city-base-research`, `intersection-research`, `client-fact-research`)

**Own:** data-gathering layer (service taxonomies, city lists, intersection pages, client facts).

**Engine calls them for:** input data to Phase 3 collection. Does not re-implement.

### `perplexity-research-suite` (Sonar) + DataForSEO (tier-3)

**Own:** paid-data + AI-surface substrate.

**Engine calls them for:** V3 probes (Sonar), V1/V2/M1/A1 data (DataForSEO). Does not wrap.

### Ad-intelligence module (from [MI-3c])

**Owns:** V4 paid-arena deep creative capture.
- Google Ads Transparency Center scrape.
- Themed swipe file production.
- Per-client ad-angle recommendations.

**Engine calls it for:** Phase 3 V4 deep pass when Chrome is connected.

---

## What this engine uniquely owns (nothing else does this)

| Capability | Phase |
|---|---|
| The arena model (V1-V5, M1, M2, A1) applied as a scoring framework | §3 / Phase 7 |
| Composite 0-5 scorecard across top-N competitors x all arenas | Phase 7 |
| Arena-source-enumeration phase (walks every source per arena) | Phase 2 |
| No-undefended-zero guard | Phase 5 |
| Adversarial completeness pass | Phase 6 |
| Completion-vs-plan diff | Phase 4 |
| Substrate routing rule (host-side vs Chrome vs Cowork) | Phase 0 |
| Output A: field-level perfect company profile | Phase 10 |
| Output B: per-client gap-to-action plan | Phase 11 |
| Routing actions to downstream programs (website-factory / local-seo-growth / tool change) | Phase 11 |
| Self-expanding gap-discovery pass | Phase 9 |
| `G-market-intel` gate registration and wiring | §5 |
| Residuals queue (every gap gets a method + owner) | Phase 12 |
| Cross-arena trend analysis over time | Future (v1.1+) |
| Geo-grid coverage analysis | Future (v1.1+) |
