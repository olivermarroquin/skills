---
name: opportunity-finder
version: 1.0
status: active
created: 2026-06-17
updated: 2026-06-17
description: The discovery front-end for the opportunity-teardown engine. Runs multi-lane discovery (AI-surface scan, marketplace/launch-board pulls, expansion-from-a-keeper) over a category, applies a lightweight fresh/growing/saturation score, dedups against the candidate cache + the build-it-better registry, and surfaces a ranked cap-5 shortlist with provenance for operator triage — the keepers flow into opportunity-teardown's quick pass. Use this skill when the operator wants to GO FIND new/fast-growing products worth tearing down, says "what's new/hot in {category}," "scan for opportunities," "find me products to tear down," "run the finder," "what's growing in AI content tools," or wants the top-of-funnel that feeds the teardown engine. Profile-driven (product/AI-content is profile #1; OR-2 startups, OR-4 open-source skills, OR-5 MCPs swap the lane-set via config). Do NOT use this to tear down ONE already-chosen thing (that is opportunity-teardown, Lane A), and do NOT use it for per-client SEO competitor discovery (that is market-intelligence-engine).
triggers:
  - operator wants to GO FIND candidates in a category (not tear down one known thing)
  - phrases like "what's new / hot / growing in {category}," "scan for opportunities," "find products to tear down," "run the finder," "fresh AI tools this week"
  - the scheduled scout fires (v1.1) and needs to populate the triage inbox
  - any opportunity-radar profile run that starts from discovery rather than a handed-down candidate
composes-with:
  - opportunity-teardown (the engine this feeds — keepers become its quick-pass / Lane A inputs; do NOT rebuild the teardown here)
  - prioritization + _meta/scoring-rubric.md (final ranking of the shortlist; build-for-myself-first is a first-class tag)
  - perplexity_sonar.py at the tier-3 carve-out (Lane B AI-surface scan — reachable from the Cowork sandbox)
  - web_fetch + Claude-in-Chrome (Lane C marketplace/launch-board pulls — escalate JS-rendered pages to Chrome, never a silent empty fetch)
  - schedule skill (v1.1 weekly scheduled scout → triage inbox)
  - reference-finder pattern [DI-7] (the discover→vet→register→scout SHAPE this reuses; the skill itself was never built — this reuses the documented pattern)
tags: [skill, opportunity-radar, opportunity-finder, discovery, finder, lanes, fresh-growing, saturation, triage-shortlist, dedup, taste-calibration, source-weighting, scheduled-scout, profile-driven, general-purpose, reusable-engine]
---

# `opportunity-finder` skill v1.0 — the discovery front-end

> **Authority:** built to `second-brain/_meta/handoffs/opportunity-radar/spec-opportunity-teardown-engine.md` §3 (lanes),
> §4 (fresh/growing), §8 (scoring), §9 (registry/dedup target), §13 (scheduled scout). **If this file and the spec
> disagree, the spec wins** until amended there.

This skill is the **top-of-funnel** that feeds the `opportunity-teardown` engine. It **discovers** candidate
opportunities across a category, scores them for **fresh / growing / saturation**, **dedups** them against what's
already been seen or pursued, and surfaces a **ranked cap-5 shortlist** with evidence + provenance for the operator to
triage. The keepers the operator picks flow into `opportunity-teardown`'s quick pass (the engine's Lane A intake).

**It does NOT tear anything down.** Discovery + scoring + a beefy-enough shortlist to decide "dig deeper?" is the whole
job. The teardown, level-up, money layer, and build/buy/use decision all live in `opportunity-teardown` — this skill
hands keepers over and stops.

## What's genuinely new here vs. reused

This skill **reuses the `reference-finder` pattern** from `design-inspiration-system [DI-7]` (the discover → vet →
register → scout shape). That pattern was specced but **never built as a skill on disk** — so this skill reuses the
*documented* shape, it does not import a `reference-finder` skill. Build only the two opportunity-specific pieces that
are genuinely new; reuse the rest:

| Capability | Owned by | This skill's job |
|---|---|---|
| Multi-lane discovery shape, candidate registry, taste-learning, source-weighting, scheduled-scout | `reference-finder` pattern `[DI-7]` (documented) | **Instantiate the shape for opportunities** (`references/discovery-lanes.md`) |
| **Fresh / growing / saturation scoring (NEW)** | **this skill** | `references/fresh-growing-scoring.md` — the §4 noise filter, no equivalent exists |
| AI-surface query (Lane B) | `perplexity_sonar.py` (tier-3) | Call it with the lane's prompt template; consume candidates |
| Marketplace pulls (Lane C) | `web_fetch` + Claude-in-Chrome | Fetch listings; **escalate JS pages to Chrome**; parse candidates |
| Final ranking | `prioritization` + `_meta/scoring-rubric.md` | Hand the shortlist over with the scoring profile |
| The teardown itself | `opportunity-teardown` (the engine) | Hand keepers to its quick pass; do not tear down here |
| Quality gates | `gate-peer-reviewer` + `output-quality-loop` | Dispatch on the SKILL + the first shortlist |

**Do NOT use this skill for** per-client SEO competitor discovery — that is `market-intelligence-engine`. This scans the
*outside world for things worth building*, not a named client's local competitors. And do NOT use it to tear down one
already-chosen thing — that is `opportunity-teardown` Lane A.

---

## Invocation modes

| Mode | When | What it does |
|---|---|---|
| `discover` | operator says "find / scan {category}" | Run the active profile's lanes over the category → dedup → score → ranked cap-5 shortlist → operator triage. The default. |
| `expand` | operator points at a keeper | Run Lane D only from that keeper → adjacent/similar candidates → same dedup + score + shortlist. |
| `scout` (v1.1) | the scheduled task fires | Run Lanes B/C headless on the tracked categories → drop ≤5 into `_triage-inbox.md` for Monday triage. Never auto-ingests. |

All three end at the **operator-triage shortlist**. The engine **proposes; the operator disposes** — nothing is ever
auto-ingested into the teardown engine or the registry.

---

## The pipeline (one pass)

```
pick profile + category
   → run active lanes — BOTH a trending pull AND an indie/under-the-radar pull (each emits candidate + provenance)   [§3]
   → DEDUP against THREE stores: _candidates-cache.md (always) + the build-it-better registry (if present) +
        the existing tools/ library (05_shared-intelligence/tools/)   [§9]
        • already-seen / already-in-registry / already-in-library  → log to _rejection-log.md with reason, link, DROP (never silently)
        • new  → keep
   → SCORE each survivor: recency · velocity · saturation penalty   [§4]   (no undefended zeros)
   → WRITE a per-candidate brief (what · benefit · who-for · worth-pursuing) for every IN-CATEGORY real candidate;
        out-of-category → rejection log only, no brief
   → RANK with prioritization + scoring-rubric (build-for-myself-fit FIRST, fresh/growing composite as tiebreaker)   [§8]
   → present a TRENDING-vs-INDIE comparison + a ranked cap-5 shortlist (saturation = the contrast axis)
   → write briefs + comparison + shortlist to the discovery home; append all surfaced items to _candidates-cache.md
   → SURFACE to operator: cap-5 + the trending-vs-indie comparison + briefs + provenance + pursue/park/skip recs
   → operator picks: keepers → opportunity-teardown (quick pass) ; the rest → evaluation-pending (parked, NOT killed) ;
        out-of-category / dupes → _rejection-log.md
   → update _source-yield.md (which lane produced keepers) + _taste-profile.md (the standing ranking rule + keep/kill)
```

Full contracts: lanes → `references/discovery-lanes.md`; scoring → `references/fresh-growing-scoring.md`; dedup +
rejection + source-yield + taste → `references/dedup-rejection-sourceyield.md`; profile config →
`references/finder-config-profiles.md`.

---

## Lanes (v1) — see `references/discovery-lanes.md` for each lane's method, prompt/fetch template, and provenance shape

- **Lane A — operator manual-add.** Lives in the `opportunity-teardown` engine, not here. The finder simply hands a
  keeper to it. Listed for completeness.
- **Lane B — AI-surface scan.** Ask Perplexity Sonar "what's newly launched / growing fast in {category}" → candidate
  list. Runs from the Cowork sandbox via `~/workspace/second-brain-tier3/automation/scripts/perplexity_sonar.py`
  (confirmed reachable — `reference_ai_surface_reachability_from_cowork`, `reference_perplexity_sonar_only`).
- **Lane C — marketplace / launch-board pull.** Product Hunt, AppSumo, Gumroad, etc. via `web_fetch`. **JS-rendered
  pages (Product Hunt, AppSumo are JS-heavy) escalate to Claude-in-Chrome** — `mcp__Claude_in_Chrome__navigate` +
  `get_page_text`. **Never accept a silent empty WebFetch** (`feedback_verify_substrate_and_escalate_webfetch`).
- **Lane D — expansion.** From a keeper, find adjacent/similar items (its direct competitors, the maker's other work)
  via Sonar + targeted fetches.
- **Deferred to v1.1 (documented, not built):** Meta/TikTok ad libraries (ToS + JS-heavy), app-store charts, Amazon
  Movers & Shakers.

---

## Build-time + run-time discipline (non-negotiable)

1. **No undefended zeros / single-source claims.** Any "0 / nobody's doing this / fully saturated / empty" reading
   requires **≥2 independent sources + an adversarial check** that tries to disprove it. A thin-sample zero is softened
   to "not found in [sources checked]; not confirmed absent" and flagged for the deep dive
   (`feedback_no_undefended_zeros_enumerate_sources`).
2. **Vet before shortlist; log every reject.** Dedup + score happen before anything is shortlisted. Rejected/duplicate
   candidates are logged to `_rejection-log.md` with a reason — **no silent drops**
   (`feedback_verify_live_not_vault_and_no_silent_skips`).
3. **Heavy/browser/slow collection runs host-side or in Chrome, not the 45s Cowork sandbox** — and **fails loud in the
   headline** about every limitation, never in a buried section (`feedback_heavy_collection_hostside_not_cowork`).
4. **Escalate, don't fake.** An empty WebFetch on a JS page is a tool limitation → redo in Claude-in-Chrome. Never
   log-and-defer an empty fetch as a "residual" (`feedback_verify_substrate_and_escalate_webfetch`).
5. **Never auto-ingest.** The finder proposes a ranked shortlist; the operator picks keepers. Auto-flow into the
   teardown engine or the registry is forbidden.
6. **Dedup honesty.** Own-cache dedup must actually run. Registry dedup is wired against the `[OR-1.3]` build-it-better
   registry but, until that registry is on disk, is reported as **wired-but-deferred-proof (registry absent this run)** —
   never claimed to have "run."
7. **Provenance on every candidate.** Lane + source + date, always. A candidate with no provenance is not a candidate.

---

## Standing behaviors — exploration-heavy (operator-directed, 2026-06-17)

The operator wants the finder **exploration-heavy**, not just a teardown funnel. These are now standing behaviors,
recorded here + in the spec (§5 amendment) so they aren't folklore:

1. **Per-candidate brief for every in-category, real candidate.** Each gets a plain-language brief — **what it does ·
   the benefit · who it's for · worth-pursuing read** — saved to the discovery exploration area (the run's
   `_trending-vs-indie-*.md`); pursued/high-value ones get an individual `briefs/brief-<slug>.md` that **graduates** to
   `05_shared-intelligence/tools/` on pursuit. **Out-of-category rejects get NO brief** — just a `_rejection-log.md` row.
2. **Trending + indie, compared.** Keep surfacing trending/popular tools **and** deliberately surface
   lesser-known/indie/few-competitor tools, then present them **side by side** (saturation is the contrast axis). Pull
   the indie side with indie-leaning Lane-B prompts + indie sources (AppSumo, Product Hunt newest, indie directories) —
   see `references/discovery-lanes.md`.
3. **`evaluation-pending` status.** In-category candidates the operator doesn't teardown this round are **parked
   (`evaluation-pending`), not killed** — a held bench for later teardown decisions (in `_triage-inbox.md` +
   `_candidates-cache.md`).
4. **Dedup against the existing `tools/` library** (the 3rd store) — never re-brief a tool already ingested; link it.

## General-purpose: the profile is config (see `references/finder-config-profiles.md`)

The engine logic above is identical across profiles. **Only the lane-set, scoring weights, category, and dedup target
are config.** Product / AI-content is profile #1 (default). `[OR-2]` startup-funding, `[OR-4]` open-source skills, and
`[OR-5]` MCPs swap the lane-set without touching this skill. v1.0 proves a **2nd lane-set (`[OR-2]` startup-funding)
from config alone** — if the finder needs editing to support a new profile, the profile boundary is wrong, which is a
bug in the finder, not the profile (`feedback_tools_reusable_across_project_types`,
`feedback_no_half_finished_build_for_reuse`).

---

## Operator gates (5) — the finder is operator-attended

1. **Plan-bullet** — lane set + scoring + v1/v1.1 split; operator approves before building.
2. **Discovery dry-run** — run the lanes for the slice; surface the raw candidate set + provenance; fail loud on any
   lane limit. Hold for review **before** scoring.
3. **Shortlist spot-check** — ranked cap-5 with scores/evidence/provenance; operator confirms the bar + picks keepers.
4. **Scout + taste-profile confirm (v1.1)** — cadence + the initial taste profile before arming the scheduled scout.
5. **Closing** — review gate (independent reviewer authors the verdict; the producer never self-gates) → tracker close
   → event-log → git staged-by-name.

---

## Files this skill reads / writes

- **Reads:** `references/*` (this skill); `_meta/scoring-rubric.md`; the `opportunity-teardown` quick-pass contract
  (so a keeper hands off cleanly).
- **Writes (the discovery home, `05_shared-intelligence/opportunity-radar/discovery/`):** `_candidates-cache.md`
  (dedup ledger), `_triage-inbox.md` (shortlists + the evaluation-pending bench), `_rejection-log.md` (rejects +
  reasons), `_taste-profile.md` (the standing ranking rule + keep/kill signal), `_source-yield.md` (lane yields),
  `_run-log-YYYY-MM-DD.md` (auditable raw queries/outputs per run), `_trending-vs-indie-YYYY-MM-DD.md` (the comparison +
  the per-candidate briefs for the run), and `briefs/brief-<slug>.md` (individual notes for pursued/high-value
  candidates; graduate to `tools/` on pursuit).
- **Dedups against three stores:** the candidate cache (always), the build-it-better registry (`[OR-1.3]`, if present),
  and the existing `tools/` library (`05_shared-intelligence/tools/`) — never re-surface what the library already holds;
  link to the existing tool-note instead.
- **Coordinates with `[OR-1.3]`:** dedups against its build-it-better registry; does **not** create or own that
  registry. The parent `opportunity-radar/_README.md` is a shared file — edit additively, git-diff-first, coordinated
  multi-writer commit.

## Composes with / boundaries

- **Feeds** `opportunity-teardown` (keepers → quick pass).
- **Reuses** the `reference-finder` pattern `[DI-7]`, `perplexity_sonar.py`, `web_fetch` + Claude-in-Chrome,
  `prioritization` + `scoring-rubric`, `schedule` (v1.1 scout), `gate-peer-reviewer` + `output-quality-loop`.
- **Distinct from** `market-intelligence-engine` (per-client SEO competitor discovery) — clean boundary, shared
  vocabulary only.

## Related
- `[[spec-opportunity-teardown-engine]]` (authority) · `[[opportunity-teardown]]` (the engine this feeds)
- `[[handoff-2026-06-16-or1-1-discovery-finder]]` (this build) · `[[handoff-2026-06-13-di7-reference-discovery-vetting-engine]]` (the pattern reused)
- references: `[[discovery-lanes]]` · `[[fresh-growing-scoring]]` · `[[finder-config-profiles]]` · `[[dedup-rejection-sourceyield]]`
