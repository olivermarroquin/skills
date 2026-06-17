---
type: skill-reference
skill: opportunity-finder
version: 1.0
created: 2026-06-17
updated: 2026-06-17
tags: [skill-reference, opportunity-finder, scheduled-scout, schedule, v1.1, sandbox-reachable-only]
---

# Scheduled scout (§13) — the weekly compounding layer

A weekly headless Cowork task (via the `schedule` skill) that runs the **sandbox-reachable** lanes, dedups, scores, and
drops a **≤5 fresh-candidate shortlist** into `_triage-inbox.md` for Monday triage. The manual-add + attended runs prove
the engine; the scout keeps the funnel filling without the operator lifting a finger. **It never auto-ingests** — it
proposes a shortlist; the operator disposes.

## Cadence
**Monday mornings, weekly** (operator-approved 2026-06-17). Cron: `0 8 * * 1` (08:00 Mondays).

## Scope — SANDBOX-REACHABLE LANES ONLY (the load-bearing limitation)

> ⚠️ **The headless scout runs ONLY the lanes that work unattended from the Cowork sandbox.** Anything needing
> Claude-in-Chrome or that returns a JS shell is **attended-run only** and is NOT in the scout. This is stated here so
> the scout's coverage is **never silently partial** (`feedback_heavy_collection_hostside_not_cowork`).

| Lane / source | In the weekly scout? | Why |
|---|---|---|
| Lane B — Perplexity Sonar (trending + indie prompts) | ✅ YES | Sonar reachable from the sandbox (tier-3 wrapper) |
| Lane C — Product Hunt (SSR via `web_fetch`) | ✅ YES | PH serves real SSR content to `web_fetch` (verified 2026-06-17) |
| Lane C — AppSumo | ❌ NO — attended only | JS-rendered; needs Claude-in-Chrome (a human-attended browser pick) |
| Lane C — Gumroad | ❌ NO — attended only | JS shell via `web_fetch`; needs Chrome |
| Lane D — expansion from a keeper | ❌ NO — attended only | runs from an operator-chosen keeper, not headless |
| Deferred lanes (ad libraries, app-store charts, Amazon) | ❌ NO | v1.1+, browser/ToS-heavy |

**The scout headline must state its own coverage** every run: "Scout ran Sonar + Product Hunt (SSR) only; AppSumo /
Gumroad / Lane-D are attended-run — not covered this week." So a thin week reads as scoped, not as a silent miss.

## What the scout does each run
1. Run Lane B (trending **and** indie prompts) + Lane C Product Hunt (SSR) for the tracked profile/category.
2. Dedup against all three stores (candidate cache + build-it-better registry + `tools/` library).
3. Score (§4); rank fit-first / composite-tiebreaker.
4. Drop the **top ≤5 fresh** candidates into `_triage-inbox.md` under a dated "Scout — YYYY-MM-DD" heading + append to
   `_candidates-cache.md`; log rejects.
5. State coverage in the headline (the scoped-lanes note above). Never auto-ingest into the engine.

## Taste profile
The scout reads `_taste-profile.md` (the standing fit-first ranking rule + keep/kill signal) to bias its ≤5 toward
Oliver's bar. v1: read + bias ranking. v1.1: auto-weight lanes from `_source-yield.md` keeper-rates.

## Status
Armed 2026-06-17 (operator-approved). Scheduled task: `opportunity-finder-weekly-scout`. v1.1 enhancements (AppSumo via a
host-side/Chrome-attended companion run, auto source-weighting) documented, not built.

## Related
- `[[SKILL]]` · `[[discovery-lanes]]` (which lanes are sandbox-reachable) · `[[fresh-growing-scoring]]` · `[[_triage-inbox]]`
- spec `[[spec-opportunity-teardown-engine]]` §13 · `reference_ai_surface_reachability_from_cowork` · `reference_perplexity_sonar_only`
