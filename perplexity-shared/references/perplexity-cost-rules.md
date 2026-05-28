# Perplexity cost rules — shared reference

Every Perplexity-suite skill follows the same cost-management rules. This file is the single source. When the rules change (Perplexity changes its plan structure, the credit allocation shifts, a new fallback path opens up), update this file once and every suite skill picks up the change.

**Last revised:** 2026-05-28 — switched from the legacy "~200 Pro Search queries per rolling 7-day window" framing to the current credits-based model. Pro is now metered in credits/month (4,000/mo on the standard plan as of 2026-05-27). The two research paths — Path A (Claude in Chrome browser) and Path B (Sonar API) — bill into separate buckets.

## The capacity reality — Perplexity Pro is metered in credits/month

The current Pro plan ($21.20/mo all-in) is **~4,000 credits per calendar month**, not unlimited and not weekly. The legacy "weekly Pro Search cap" framing was a 2025-era artifact of the older plan; it doesn't reflect how the current plan is billed.

Roughly: one Pro Search query consumes one credit. Heavier-reasoning queries (deep-research-mode toggled on, multi-step reasoning, large output) can consume more. Lightweight queries (single-shot, short answer) can consume fewer. The 4,000/month figure is a planning ceiling, not a precise per-query rate; treat it as "spend within budget" rather than "spend exactly N queries."

Quick (non-Pro) search remains unlimited. Free tier is 5 Pro Searches per day. The suite is built around the assumption of one signed-in Pro account.

What this means in practice across the suite:

- A `deep` refinement run uses 15 queries ≈ ~0.4% of monthly budget.
- A `medium` refinement uses 7 queries ≈ ~0.2%.
- A `light` refinement uses 3 queries ≈ ~0.08%.
- A `perplexity-blueprint-research` run (Wave 2) uses 30-50 queries on a deep pass ≈ ~1%.
- Standing scans (citation-monitoring, acquisition-signal) routed through Path B (Sonar API) don't draw on the Pro credit pool — they're pay-per-query and bill into a separate Sonar invoice.

A heavy month (20+ refinements + a few blueprint runs + several scans) could land at 10-15% of monthly budget. The plan accommodates an aggressive Knowledge-OS cadence without budget pressure most months.

## Two research paths — same skill family, separate cost buckets

Every Perplexity-suite skill that runs interactively (refinement, blueprint, topic-gaps, niche-validation, etc.) follows the same priority decision tree at runtime:

1. **Path A — Claude in Chrome (default).** The skill calls `mcp__Claude_in_Chrome__list_connected_browsers`; if a browser is connected and signed-in to Pro, it drives the logged-in browser session. Queries draw on the operator's monthly Pro credit pool (4,000/mo).
2. **Path B — Sonar API (backup).** When Claude in Chrome is unavailable (no browser, not signed in, headless run, scheduled task), the skill checks for `PERPLEXITY_API_KEY` (env var or configured path) and uses the Sonar HTTP endpoints. Sonar is pay-per-query, billed separately; rough math is $0.005-$0.02 per query depending on model (`sonar`, `sonar-pro`, etc.).
3. **Refusal (no third path).** If neither Path A nor Path B is available, the skill **pauses and surfaces the gap to the operator**. It does NOT fall back to Cowork's built-in `WebSearch` or `web_fetch`. That would silently substitute a different research source (general web search, not Perplexity Pro's curated AI-overview synthesis) and consume zero credits — defeating the contract the subscription pays for.

The refusal step is the structural protection against silent source substitution. Past invocations of `perplexity-refinement` (Wave 0, 2026-05-27) ran without the refusal step and quietly used Cowork WebSearch when the browser wasn't reachable. Phase 2 of the output-quality-loop project (2026-05-28) added the structural refusal; every future suite skill build inherits it.

**Cost-receipt discipline.** Every refinement / research output writes a one-line tally at the end naming the path used:

> Queries run: N via Path A (Claude in Chrome / Pro Search) | Path B (Sonar API). Validated: X. Updated: Y. Contradicted: Z. New sources surfaced: W.

The path-naming half is non-optional. Without it the operator can't audit whether the Pro contract held.

## Per-invocation caps

Hard caps that every suite skill enforces. Don't exceed without operator override. Caps are independent of which path was used — they're about per-invocation discipline, not the underlying meter.

| Depth | Max queries per invocation | Used by |
|---|---|---|
| `light` | 3 | refinement (quick triangulation) |
| `medium` | 7 | refinement (standard pass) |
| `deep` | 15 | refinement (saturation pass on briefs) |
| `blueprint` | 30-50 | blueprint-research (Wave 2 flagship) |
| `scan` | 5-10 | topic-gaps, niche-validation, competitor-move-detection (varies by skill) |
| `monitor` | 1-3 | citation-monitoring, acquisition-signal (per scheduled run; usually via Path B / Sonar API) |

If a high-tier list exceeds the cap for the chosen depth, the skill asks the operator which items to drop before running. Don't silently truncate.

## When to warn the operator

The router skill (`perplexity-research-suite`) tracks rough monthly usage from execution logs (the `Queries run: N via Path A` lines). Warn before invoking a high-cost skill when monthly Path-A usage looks heavy.

- **> 1,500 Path-A queries in the current calendar month (~37% of budget)** — surface the tally; ask whether to proceed.
- **> 2,500 Path-A queries (~62%)** — warn before any `deep` refinement or any blueprint run. Recommend `light` or `medium` instead, or route through Path B (Sonar API) which doesn't draw on the Pro budget.
- **Approaching 3,500 (~87%)** — recommend deferring all Path-A runs except critical ones. Standing scans should already be on Path B; the remaining Path-A budget gets reserved for interactive refinement work.

The tally is best-effort, not authoritative. It's read from execution-log entries that name "Queries run: N via Path A" lines. The operator is the source of truth on whether to proceed. Sonar usage (Path B) doesn't count toward the Pro credit pool, so it doesn't enter these thresholds — but it does generate a separate Sonar bill the operator can track in the Perplexity dashboard.

## Cache rule — don't repeat work

Every refinement output writes a frontmatter field `perplexity-refined: YYYY-MM-DD` on the original artifact. Re-running refinement on the same artifact within the refresh window (default 90 days) should ask the operator before sending new queries. The cache is the file itself; the question is whether enough has changed since the last pass to justify the cost.

For blueprint-research and other heavier skills, the corresponding cache field is named per-skill but follows the same pattern: a frontmatter date + a refresh window the skill enforces.

## Sonar API — Path B specifics

The Sonar API is the canonical Path B endpoint. Pay-per-query (token-priced; the math lands somewhere around $0.005-$0.02 per query depending on model). At a few queries per day per scan, monthly Sonar cost stays single-digit dollars. Cheap enough to ignore relative to the $21.20/mo Pro subscription.

What goes through Sonar by default:

- `perplexity-citation-monitoring` (Wave 1C) — daily or weekly scans of "is the operator's site or his clients' sites cited by Perplexity for target queries"
- `perplexity-acquisition-signal` (Wave 5) — standing monitoring of acquisition signals across tracked queries

What stays in the Path A (browser) by default:

- `perplexity-refinement` — interactive vault-artifact refinement (uses Path B only when Claude in Chrome is unavailable)
- `perplexity-blueprint-research` — flagship, interactive
- `perplexity-topic-gaps`, `perplexity-niche-validation`, `perplexity-client-discovery`, `perplexity-competitor-move-detection`, `perplexity-ai-overview-hardening` — situational, interactive

**API-key setup.** The skill expects either:
- env var `PERPLEXITY_API_KEY` exported in the shell environment, or
- a config-pointed path with the key (e.g., the suite skill reads a path from its own config and loads the key from there).

The key itself lives in the operator's tier-3 vault at `~/workspace/second-brain-tier3/personal/business-keelworks.md` (or wherever the operator's Perplexity entry lives). Cowork does NOT read tier-3 directly; the operator populates the env var or config from the tier-3 vault manually. This honors the standing `feedback_never_propose_overwrite_tier3` discipline — the skill never proposes writes against tier-3 paths.

If the env var is unset and no config path resolves to a key, Path B is unavailable and the skill falls through to refusal (per the two-path priority above).

## The cost surface stays honest

Every skill output writes a one-line tally at the end:

> Queries run: N via Path A (Claude in Chrome / Pro Search) | Path B (Sonar API). Validated: X. Updated: Y. Contradicted: Z. New sources surfaced: W.

That line is the cost receipt. Over time the operator can tune depth and frequency by reading these tallies across execution logs. Don't hide queries; don't batch them in a way that obscures the count; don't omit the path-naming half.

If a refinement output's tally line says `Queries run: N via WebSearch` (or omits the path entirely), the discipline broke. Treat it as a regression and re-run with the correct path.

## When the rules change

If Perplexity changes its plan structure (credit allocation shifts, plan tiers change, Sonar pricing changes, a new tier replaces the current one):

1. Update this file once.
2. Bump the `Last revised:` line at the top.
3. Surface to Oliver that the cost surface for the suite has changed.
4. Update any in-flight skill design that assumed the old numbers.

Every suite skill points at this file, so the fix propagates.

## See also

- [[perplexity-browser-setup]] — Path A pre-query browser checks (including Claude in Chrome verification subsection)
- [[perplexity-query-templates-index]] — index pointing at each skill's query templates
- [[perplexity-refinement]] — Wave 0 skill; carries the canonical two-path decision tree in Phase 2a
- [[perplexity-research-suite]] — router that surfaces capacity status
