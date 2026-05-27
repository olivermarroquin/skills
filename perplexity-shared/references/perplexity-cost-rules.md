# Perplexity cost rules — shared reference

Every Perplexity-suite skill follows the same cost-management rules. This file is the single source. When the rules change (Perplexity changes its tier structure, the weekly cap shifts, a new fallback path opens up), update this file once and every suite skill picks up the change.

## The capacity reality — Perplexity Pro is not unlimited

Pro Search on the $20/mo Perplexity Pro plan is **~200 queries per week**, not unlimited. The published marketing language sometimes reads "unlimited Pro Search," but in practice the cap is around 200 per rolling 7-day window. Heavier weeks can hit a soft limit that looks like a slowdown banner or a "you've hit a usage limit" message.

Quick (non-Pro) search is unlimited. Free tier is 5 Pro Searches per day. The skill suite is built around the assumption of one signed-in Pro account.

What this means in practice:

- A `deep` refinement run uses 15 queries = ~7.5% of the weekly budget.
- A `medium` refinement uses 7 queries = ~3.5%.
- A `light` refinement uses 3 queries = ~1.5%.
- A `perplexity-blueprint-research` run (Wave 2) uses 30-50 queries on a deep pass = 15-25%.
- Standing scans (citation-monitoring, acquisition-signal) routed through the Sonar API don't draw on the Pro weekly cap — they're pay-per-query with no shared limit.

A heavy week (5 deep refinements + 1 blueprint run + a few light scans) can burn 100-150 queries through the browser. Plan around it.

## Per-invocation caps

Hard caps that every suite skill enforces. Don't exceed without operator override.

| Depth | Max queries per invocation | Used by |
|---|---|---|
| `light` | 3 | refinement (quick triangulation) |
| `medium` | 7 | refinement (standard pass) |
| `deep` | 15 | refinement (saturation pass on briefs) |
| `blueprint` | 30-50 | blueprint-research (Wave 2 flagship) |
| `scan` | 5-10 | topic-gaps, niche-validation, competitor-move-detection (varies by skill) |
| `monitor` | 1-3 | citation-monitoring, acquisition-signal (per scheduled run; usually via Sonar API) |

If a high-tier list exceeds the cap for the chosen depth, the skill asks the operator which items to drop before running. Don't silently truncate.

## When to warn the operator

The router skill (`perplexity-research-suite`) tracks rough weekly usage from execution logs. Warn before invoking a high-cost skill when usage looks heavy:

- **> 100 queries in the last 7 days** — surface the tally; ask whether to proceed.
- **> 150 queries in the last 7 days** — warn before any `deep` refinement or any blueprint run. Recommend `light` or `medium` instead, or defer to next week.
- **Approaching 200** — recommend deferring all browser-based runs except critical ones. Standing scans should route through Sonar API where possible.

The tally is best-effort, not authoritative. It's read from execution-log entries that name "Queries run: N" lines. The operator is the source of truth on whether to proceed.

## Cache rule — don't repeat work

Every refinement output writes a frontmatter field `perplexity-refined: YYYY-MM-DD` on the original artifact. Re-running refinement on the same artifact within the refresh window (default 90 days) should ask the operator before sending new queries. The cache is the file itself; the question is whether enough has changed since the last pass to justify the cost.

For blueprint-research and other heavier skills, the corresponding cache field is named per-skill but follows the same pattern: a frontmatter date + a refresh window the skill enforces.

## Sonar API fallback path

Skills that should run on a schedule don't draw on the shared Pro browser cap. They route through the Perplexity Sonar API instead.

What goes through Sonar:

- `perplexity-citation-monitoring` (Wave 1C) — daily or weekly scans of "is Oliver's site or his clients' sites cited by Perplexity for target queries"
- `perplexity-acquisition-signal` (Wave 5) — standing monitoring of acquisition signals across tracked queries

What stays in the browser:

- `perplexity-refinement` — interactive vault-artifact refinement
- `perplexity-blueprint-research` — flagship, interactive
- `perplexity-topic-gaps`, `perplexity-niche-validation`, `perplexity-client-discovery`, `perplexity-competitor-move-detection`, `perplexity-ai-overview-hardening` — situational, interactive

The Sonar API is pay-per-query (token-priced; the math lands somewhere around $0.005-$0.02 per query depending on model). At a few queries per day per scan, monthly cost stays single-digit dollars. Cheap enough to ignore relative to the $21.20/mo Pro subscription.

## The cost surface stays honest

Every skill output writes a one-line tally at the end:

> Queries run: N. Validated: X. Updated: Y. Contradicted: Z. New sources surfaced: W.

That line is the cost receipt. Over time the operator can tune depth and frequency by reading these tallies across execution logs. Don't hide queries; don't batch them in a way that obscures the count.

## When the rules change

If Perplexity changes its tier structure, the weekly cap shifts, or the Sonar pricing changes:

1. Update this file once.
2. Bump the `updated:` line in the frontmatter.
3. Surface to Oliver that the cost surface for the suite has changed.
4. Update any in-flight skill design that assumed the old numbers.

Every suite skill points at this file, so the fix propagates.

## See also

- [[perplexity-browser-setup]] — pre-query browser checks
- [[perplexity-query-templates-index]] — index pointing at each skill's query templates
- [[perplexity-refinement]] — Wave 0 skill
- [[perplexity-research-suite]] — router that surfaces capacity status
