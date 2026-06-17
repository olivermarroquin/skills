---
type: skill-reference
skill: opportunity-finder
version: 1.0
created: 2026-06-17
updated: 2026-06-17
tags: [skill-reference, opportunity-finder, dedup, rejection-log, source-yield, taste-calibration, no-silent-drops]
---

# Dedup · rejection log · source-yield · taste calibration

The vetting layer between discovery and the shortlist. Reuses the `reference-finder` pattern's dedup + rejection-log +
source-weighting + taste-learning (documented in `[DI-7]`; the skill was never built — this reuses the shape). **No
candidate is silently dropped** (`feedback_verify_live_not_vault_and_no_silent_skips`).

## 1. Dedup (always runs, before scoring)

Every surfaced candidate is checked against **three** stores:

1. **`_candidates-cache.md` (always-on, this skill owns it).** The append-only ledger of every candidate ever surfaced
   — keyed by **normalized URL** (strip `utm_*`/query, lowercase host, drop trailing slash) with the product name as a
   secondary key. If a candidate's key is already in the cache → it's a duplicate → log to `_rejection-log.md` with
   reason `already-surfaced (<date first seen>)` and **drop**. This dedup **must actually run** every pass.
2. **The build-it-better registry (`[OR-1.3]`-owned, dedup target in `finder-config-profiles.md`).** If a candidate is
   already a tracked/pursued/rejected entry in the registry → drop with reason `already-in-registry (<status>)`.
   - **Honesty rule:** until `[OR-1.3]`'s registry is on disk, this check is **wired but cannot be exercised**. Report
     it as **"registry-dedup wired-but-deferred-proof (registry absent this run)"** — never claim it "ran." Own-cache
     dedup still runs and is reported as run.

3. **The existing `tools/` library (`05_shared-intelligence/tools/`).** The vault already holds ~88 curated,
   VIS-ingested tool-notes. Grep the library for each candidate (by slug/name); if a `tool-<slug>.md` already exists →
   drop with reason `already-in-library`, **link to the existing note**, don't re-brief. (Surfaced live 2026-06-17:
   Wispr Flow, Granola, Higgsfield all already in the library — deduped out of the shortlist.) This is the
   reference-finder "never re-surface what the library already has" rule.

Dedup is what stops the funnel re-surfacing the same tools every week (`feedback_verify_shipped_state_before_claiming`).

## 2. Rejection log (`_rejection-log.md`) — every drop, with a reason

A candidate is rejected (logged, never silently dropped) for any of:

| Reason code | Meaning |
|---|---|
| `already-surfaced` | duplicate of a cache entry |
| `already-in-registry` | already tracked/pursued/rejected downstream |
| `unverified-existence` | Lane B named it but its URL didn't resolve / no second-source confirmation |
| `out-of-category` | not actually in the scanned category |
| `incumbent-too-saturated` | old + crowded + flat — no clone-and-improve headroom (must clear the no-undefended-zeros bar) |
| `operator-killed` | operator rejected it at Gate 3 (carries the operator's one-line reason → feeds taste profile) |
| `lane-limit-unread` | a source couldn't be read (JS shell + no Chrome, blocked fetch) — **not a true reject**; logged so it's retried, surfaced loud in the headline |

Each row: `date · name · url · reason code · one-line note · lane`. The `lane-limit-unread` rows are the audit trail
that proves no silent WebFetch-empty skips happened.

## 3. Source-yield tracking (`_source-yield.md`) — which lane earns its keep

After each run, record per lane: **# surfaced → # shortlisted → # the operator kept.** Over time this shows which
lanes/sources produce keepers vs. noise, so future runs bias toward the productive ones (source-quality weighting,
spec §3 reuse of the reference-finder mechanism). Light in v1 — just the tally + a running keeper-rate per lane. The
first data point is captured at the first real shortlist (a calibration seed, not yet a strong signal).

## 4. Taste calibration (`_taste-profile.md`) — learn Oliver's bar

A small profile of what the operator **keeps vs. kills** and why. Seeded from the strategic context
(build-for-myself-first; client-routable SEO/traffic bias per `project_priority_client_seo_traffic`; ship-don't-overbuild
per CLAUDE.md Core Principle) and grown from each Gate-3 decision. The finder reads it to bias filtering toward Oliver's
aesthetic and away from patterns he's repeatedly killed. Light in v1: capture the seed + append each keep/kill with the
operator's reason. The compounding (auto-bias future scoring) is a v1.1 enhancement, documented not auto-applied yet.

**Discipline:** taste calibration **biases ranking, never hard-filters** a candidate out before the operator sees it —
the operator owns the taste call (the engine proposes, the operator disposes). A taste signal can lower a score; it
cannot silently delete a candidate.

## How these compose in one pass

```
surface candidates (lanes)
  → dedup vs cache (runs) + registry (wired-but-deferred-proof) → drops → _rejection-log.md
  → score survivors (§4) → rank (prioritization, taste-profile biases) → cap-5 shortlist
  → operator triages: keeps → engine ; kills → _rejection-log.md (operator-killed + reason)
  → update _source-yield.md (per-lane keep tally) + _taste-profile.md (keep/kill + reason)
  → append everything surfaced to _candidates-cache.md (so next run dedups against it)
```

## Related
- `[[SKILL]]` · `[[discovery-lanes]]` · `[[fresh-growing-scoring]]` · `[[finder-config-profiles]]`
- the home files: `[[_candidates-cache]]` · `[[_rejection-log]]` · `[[_source-yield]]` · `[[_taste-profile]]` · `[[_triage-inbox]]`
- spec `[[spec-opportunity-teardown-engine]]` §9 (registry/dedup) · `[[handoff-2026-06-13-di7-reference-discovery-vetting-engine]]` (pattern reused)
