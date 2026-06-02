# Perplexity cost rules — shared reference

Every Perplexity-suite skill follows the same cost-management rules. This file is the single source. When the rules change (Perplexity changes its plan structure, the credit allocation shifts, a new fallback path opens up), update this file once and every suite skill picks up the change.

**Last revised:** 2026-06-01 — narrowed the "Cowork never reads tier-3" rule to the `automation/` carve-out. Path B key now lives at `~/workspace/second-brain-tier3/automation/secrets/perplexity-sonar.key` (script-readable, value only, perms 600), paired with rolodex entry at `personal/credentials/perplexity-sonar.md` (operator-readable, metadata + value). Env var `PERPLEXITY_API_KEY` is no longer used; scripts read the file directly via a two-candidate-path lookup that works from both Mac Terminal and Cowork sandbox.

**Previous revision:** 2026-05-28 — switched from the legacy "~200 Pro Search queries per rolling 7-day window" framing to the current credits-based model. Pro is now metered in credits/month (4,000/mo on the standard plan as of 2026-05-27). The two research paths — Path A (Claude in Chrome browser) and Path B (Sonar API) — bill into separate buckets.

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

## Path A status — REMOVED as of 2026-06-01 (Cowork pairing bug; Sonar API is the only working Perplexity path)

**Effective 2026-06-01, Path A (Claude in Chrome → Perplexity Pro) is no longer a working path for Perplexity-suite skills.** This section in the doc below still describes Path A for archival reasons, but every suite skill should treat Path B (Sonar API) as the de-facto default until Anthropic ships a fix for the known Cowork pairing bug.

**What happened:** the Cowork desktop ↔ Claude in Chrome native-messaging handshake has been broken since the April 15, 2026 Cowork desktop update. Symptom: `mcp__Claude_in_Chrome__list_connected_browsers` returns `[]` even when the extension is installed, signed in, and the desktop-side connector is toggled on. Anthropic's [Claude in Chrome Troubleshooting article](https://support.claude.com/en/articles/12902405-claude-in-chrome-troubleshooting) acknowledges the bug; tracked at [anthropics/claude-code GitHub issue #48806](https://github.com/anthropics/claude-code/issues/48806). The standard recovery sequence (disable/re-enable extension → restart Chrome → restart Cowork) does NOT fix it.

**What this means for suite skills:**

- The two-path decision tree below collapses to one path: Path B (Sonar API via `~/workspace/second-brain-tier3/automation/scripts/perplexity_sonar.py`).
- The refusal step still applies if Path B is also unavailable (no API key configured in `automation/secrets/perplexity-sonar.key`).
- Cost is now metered exclusively on the Sonar pay-per-query bill (~$0.005-$0.02/query), not the Pro subscription credit pool. The $21.20/mo Pro subscription still exists for the operator's interactive Perplexity use (browser, mobile apps) but isn't reachable from skills until Anthropic fixes the pairing bug.
- The 2026-06-01 dual-substrate research comparison ([`phase-0-research-comparison-2026-06-01.md`](../../../second-brain/_meta/handoffs/local-model-migration/phase-0-research-comparison-2026-06-01.md)) is the worked example: 14 queries on `sonar-pro` for ~$0.36 via the Sonar script, confirming the path works end-to-end.

**Re-check trigger:** any of the following flips Path A back to default:

- Anthropic ships a Cowork update that fixes the pairing bug (watch the release notes)
- `mcp__Claude_in_Chrome__list_connected_browsers` starts returning a non-empty array spontaneously
- The operator manually re-tests the pairing and confirms it works (re-running the disable/enable + restart sequence)

When any of the above happens, restore Path A as the default in this doc + update the auto-memory `reference_perplexity_sonar_only.md`.

**Drift in other vault docs (cleanup queued, not blocking):** several vault docs still describe Path A as the primary/preferred path. Per the auto-memory `reference_perplexity_sonar_only.md`, these are the known stale references:

- `~/workspace/skills/perplexity-refinement/SKILL.md` — extensive Path A documentation with browser checklists
- `~/workspace/second-brain/_meta/decision-research-conventions.md` — references "Perplexity Pro via Claude in Chrome → Sonar API → refusal"
- `~/workspace/second-brain/_meta/handoffs/_active-chats-tracker.md` — Hermes Prework C "Why now" cell references "Path A or Path B"
- `~/workspace/second-brain/_meta/handoffs/hermes-harness/prework-c-perplexity-validation-load-bearing-claims.md` — likely Path A references in body
- Other `~/workspace/second-brain/_meta/handoffs/perplexity-skill-build/` wave handoffs probably mention Path A as primary

A future cleanup pass should reconcile these against the post-2026-06-01 reality. Not a blocker for current Perplexity-suite skills — they read this file first and inherit the current path state.

## Research workflow — WebSearch first pass, Sonar Pro verification (added 2026-06-01)

After the Phase 0 hardware-research comparison (operator-driven A/B test, 2026-06-01), the standing default for any research task is:

1. **First pass: Cowork WebSearch** (free, fast, currency-strong). Captures the headline facts, recent news, and broad coverage of the question.
2. **Verification + refinement pass: Perplexity Sonar Pro via Path B** (~$0.02-0.03 per query). Runs on the same questions as the WebSearch pass to: (a) verify load-bearing claims against curated AI-overview synthesis, (b) extract precise numbers where WebSearch had ranges or approximations, (c) reach beyond the WebSearch results to find data WebSearch missed.
3. **Compare + reconcile.** Produce a comparison file noting where they agree, disagree, and miss each other. WebSearch tends to be more current on recent pricing/news; Sonar tends to be more rigorous, citation-dense, and willing to refuse-when-uncertain.

**When to skip the Sonar verification pass:**
- Research informs a low-stakes decision (<$5K, easily reversible)
- Question is informational only, not feeding a commitment
- WebSearch results were already from authoritative primary sources and the claims are clearly current

**When to skip the WebSearch first pass and go straight to Sonar:**
- Question requires citation-rigorous answer the first time (e.g., decision-research handoffs feeding hardware purchase, client commitments, contract decisions)
- Operator has explicitly requested the Pro verification

The comparison discipline is a one-time validation, not a permanent overhead. Once the operator has done ~3-5 paired A/B runs and has personal confidence in when each source wins, the explicit comparison file can become optional and the standard pattern collapses to "WebSearch first, Sonar selectively on claims that matter." Track the per-source strengths the operator observes over time at `~/workspace/second-brain/03_domains/automation-systems/research-substrate-comparison.md` (or wherever fits the vault structure).

## Research path — Sonar API only (post-2026-06-01)

Every Perplexity-suite skill follows the same decision tree at runtime:

1. **Sonar API (the only working path).** The skill calls `~/workspace/second-brain-tier3/automation/scripts/perplexity_sonar.py`, which reads the Sonar API key from the tier-3 automation carve-out at `~/workspace/second-brain-tier3/automation/secrets/perplexity-sonar.key` (operator-managed plain-text file, perms 600) and hits the Sonar HTTP endpoints. Sonar is pay-per-query, billed monthly; rough math is $0.005-$0.04 per query depending on model (`sonar`, `sonar-pro`) and answer length.
2. **Refusal (no fallback path).** If the script or key is missing, the skill **pauses and surfaces the gap to the operator**. It does NOT fall back to Cowork's built-in `WebSearch` or `web_fetch`. That would silently substitute a different research source (general web search, not Perplexity Sonar's curated AI-overview synthesis) — defeating the contract the subscription pays for.

The refusal step is the structural protection against silent source substitution. Past invocations of `perplexity-refinement` (Wave 0, 2026-05-27) ran without the refusal step and quietly used Cowork WebSearch when the browser wasn't reachable. Phase 2 of the output-quality-loop project (2026-05-28) added the structural refusal; every future suite skill build inherits it.

**Historical note.** Earlier versions of this doc carried a two-path priority — Path A (Claude in Chrome → Perplexity Pro browser) and Path B (Sonar API). Path A was removed 2026-06-01 (see the "Path A status — REMOVED" section above for the precipitating Cowork pairing bug). The Sonar API is the canonical and only working path now.

**Cost-receipt discipline.** Every refinement / research output writes a one-line tally at the end naming the path used + the dollar cost:

> Queries run: N via Sonar API (sonar-pro), ~$<cost>. Validated: X. Updated: Y. Contradicted: Z. New sources surfaced: W.

The path-naming + cost half is non-optional. Without it the operator can't audit Sonar spend across the vault.

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

The router skill (`perplexity-research-suite`) tracks rough monthly Sonar spend from execution logs (the `Queries run: N via Sonar API ~$X` lines). Warn before invoking a high-cost skill when monthly spend looks heavy.

- **> $5/month on Sonar across the suite** — surface the tally; ask whether to proceed.
- **> $15/month** — warn before any `deep` refinement or any blueprint run. Recommend `light` or `medium` instead.
- **Approaching $30/month** — recommend deferring all non-critical runs. The remaining spend gets reserved for interactive refinement work.

These thresholds are operator-set defaults, not Perplexity-imposed caps; Sonar has no hard monthly cap. Adjust upward as cadence grows. The tally is best-effort, not authoritative; it's read from execution-log entries that name `Queries run: N via Sonar API` lines.

## Cache rule — don't repeat work

Every refinement output writes a frontmatter field `perplexity-refined: YYYY-MM-DD` on the original artifact. Re-running refinement on the same artifact within the refresh window (default 90 days) should ask the operator before sending new queries. The cache is the file itself; the question is whether enough has changed since the last pass to justify the cost.

For blueprint-research and other heavier skills, the corresponding cache field is named per-skill but follows the same pattern: a frontmatter date + a refresh window the skill enforces.

## Sonar API — canonical path specifics

The Sonar API is the canonical (and only) path post-2026-06-01. Pay-per-query (token-priced; ~$0.005-$0.04 per query depending on model and answer length). At a few queries per day across the suite, monthly Sonar cost stays low single-digit dollars.

Every suite skill routes through Sonar:

- `perplexity-refinement` — interactive vault-artifact refinement
- `perplexity-blueprint-research` — flagship interactive research
- `perplexity-topic-gaps`, `perplexity-niche-validation`, `perplexity-client-discovery`, `perplexity-competitor-move-detection`, `perplexity-ai-overview-hardening` — situational, interactive
- `perplexity-citation-monitoring` (Wave 1C) — daily or weekly scans
- `perplexity-acquisition-signal` (Wave 5) — standing monitoring across tracked queries

Model selection per skill: `sonar` for lightweight scans, `sonar-pro` for refinement / blueprint / load-bearing research where curation matters.

**API-key setup (revised 2026-06-01).** The Sonar API key lives in two places by design:

1. **Rolodex (human-readable master record)** at `~/workspace/second-brain-tier3/personal/credentials/perplexity-sonar.md`. Has the key value PLUS metadata: console URL, account, generation date, rotation date, billing details, notes. Cowork does NOT read this file. The operator looks here when auditing or rotating credentials.
2. **Vending-machine file (script-readable)** at `~/workspace/second-brain-tier3/automation/secrets/perplexity-sonar.key`. Plain text, value only, no newline, no quotes, perms 600. Scripts (including `perplexity_sonar.py` in the same `automation/` subtree) read from here.

**Convention carve-out.** Cowork DOES read `second-brain-tier3/automation/` (this one carve-out only). Everything else under tier-3 — `personal/credentials/*.md`, `personal/business-keelworks.md`, `personal/financial.md`, `clients/*`, `_HOME.md`, `conventions.md` — remains air-gapped per the original tier-3 protocol. The "feedback_never_propose_overwrite_tier3" discipline still applies to writes anywhere in tier-3; Cowork does not write to tier-3 (including the automation/ carve-out) without per-path operator approval in chat.

**Path resolution from script.** `perplexity_sonar.py` resolves the key path from either execution context:
- Mac Terminal: `~/workspace/second-brain-tier3/automation/secrets/perplexity-sonar.key`
- Cowork sandbox: `~/mnt/workspace/second-brain-tier3/automation/secrets/perplexity-sonar.key` (workspace is mounted under `~/mnt/` in the sandbox)

The script uses whichever path exists. No env var or external config needed.

If the key file is absent from both candidate paths, Path B is unavailable and the skill falls through to refusal (per the two-path priority above).

## The cost surface stays honest

Every skill output writes a one-line tally at the end:

> Queries run: N via Sonar API (sonar-pro), ~$<cost>. Validated: X. Updated: Y. Contradicted: Z. New sources surfaced: W.

That line is the cost receipt. Over time the operator can tune depth and frequency by reading these tallies across execution logs. Don't hide queries; don't batch them in a way that obscures the count; don't omit the path-naming + cost half.

If a refinement output's tally line says `Queries run: N via WebSearch` (or omits the path entirely), the discipline broke. Treat it as a regression and re-run with the correct path.

## When the rules change

If Perplexity changes its plan structure (credit allocation shifts, plan tiers change, Sonar pricing changes, a new tier replaces the current one):

1. Update this file once.
2. Bump the `Last revised:` line at the top.
3. Surface to Oliver that the cost surface for the suite has changed.
4. Update any in-flight skill design that assumed the old numbers.

Every suite skill points at this file, so the fix propagates.

## See also

- [[perplexity-browser-setup]] — historical Path A browser checks (deprecated 2026-06-01; kept as audit trail)
- [[perplexity-query-templates-index]] — index pointing at each skill's query templates
- [[perplexity-refinement]] — Wave 0 skill; carries the canonical Sonar-only decision tree in Phase 2a
- [[perplexity-research-suite]] — router that surfaces capacity status
