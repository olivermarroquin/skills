# Perplexity browser setup — shared reference

> **DEPRECATED 2026-06-01.** This file documents the browser-driven Path A (Claude in Chrome → Perplexity Pro) that was removed 2026-06-01. The only working Perplexity path today is the Sonar API via `~/workspace/second-brain-tier3/automation/scripts/perplexity_sonar.py`. Do not follow the checklist below — it points at infrastructure that no longer applies. The file is kept in place as an audit trail of the prior path's design. For the current working path, see `perplexity-cost-rules.md` and `perplexity-refinement/SKILL.md` Phase 2a.

---

## Historical content (do not act on)

This is the shared checklist that every Perplexity-suite skill pointed at before running queries through the browser. It lived in `skills/perplexity-shared/references/` so the setup steps lived in one place. When the Perplexity UI changed, this file was updated once and every suite skill picked up the change.

## When to use this file

Use this when a Perplexity skill is about to send live Pro Search queries through the browser. The skills that point here are:

- `perplexity-refinement` (Phase 2a) — vault-artifact refinement passes
- Future suite skills as they ship (blueprint-research, topic-gaps, niche-validation, client-discovery, competitor-move-detection, ai-overview-hardening)

Skills that route through the Perplexity Sonar API (citation-monitoring on a schedule, acquisition-signal scans) don't need this file — they hit the API directly.

## Claude in Chrome verification (do this first)

Before the four-step browser check, the calling skill (per the two-path priority decision tree in `perplexity-cost-rules.md`) decides whether Path A is available. This subsection documents what counts as "available."

**Path A is available when ALL of the following hold:**

1. `mcp__Claude_in_Chrome__list_connected_browsers` returns at least one connected browser.
2. The browser tools (`mcp__Claude_in_Chrome__navigate`, `mcp__Claude_in_Chrome__get_page_text`, etc.) are loaded in the current Cowork session. If they appear as deferred tools in the tool registry but haven't been loaded via ToolSearch yet, load them now; if they don't appear at all, the extension isn't active and Path A is unavailable.
3. The operator has the Claude in Chrome extension running in the same tab group as the Perplexity Pro session. (Typical operator setup: a pinned Perplexity Pro tab plus the extension; the extension can drive that tab.)

**Path A is NOT available when:**

- `list_connected_browsers` returns an empty list, OR
- The browser tools aren't in the current Cowork tool registry, OR
- The browser is connected but not signed in to Pro (caught in Step 3 below), OR
- The browser is signed in to a different Perplexity account (free / different operator).

When Path A is unavailable, the calling skill falls through to Path B (Sonar API per `perplexity-cost-rules.md`) — NOT to Cowork's built-in `WebSearch`. Path A failure does not authorize WebSearch substitution under any condition; that's the load-bearing rule the two-path priority enforces.

If both Path A and Path B fail, the skill emits the refusal message in `perplexity-cost-rules.md` and stops.

**Why this subsection exists.** Wave 0 (2026-05-27) shipped the four-step browser check below but didn't document what counts as "Claude in Chrome being available" — and the calling skill (`perplexity-refinement`) silently fell back to WebSearch when the check would have failed. The subsection above plus the calling-skill's three-step decision tree closes that gap. Treat any future regression of "skill ran but didn't use Path A or Path B" as a bug in this file or its callers, not as expected behavior.

## The four-step browser check

After verifying Claude in Chrome is available (above), run these in order. Don't skip steps. A missed step means the run might use standard search (not Pro Search) and waste the user's subscription.

### Step 1 — Confirm a browser is connected

Call `mcp__Claude_in_Chrome__list_connected_browsers`. If the list is empty, stop and ask Oliver to launch the Claude in Chrome extension. Don't try to navigate without a connected browser; the call will fail in a confusing way.

### Step 2 — Navigate to Perplexity

Call `mcp__Claude_in_Chrome__navigate` with the URL `https://www.perplexity.ai/`. Wait for the page to load. If the URL redirects (rare, but possible after Perplexity reorganizes routes), follow the redirect.

### Step 3 — Confirm the session is signed in as Pro

Read the rendered page. Look for the account indicator in the top-right corner. If it says "Pro" or shows a Pro badge, the session is good. If it shows a sign-in button or "Sign up," the session isn't authenticated — stop and ask Oliver to sign in. Don't bypass the sign-in check; running queries against the free tier defeats the purpose of the subscription.

If the indicator is ambiguous (page redesign, A/B test, indicator moved), surface a screenshot to Oliver and ask before continuing.

### Step 4 — Confirm Pro Search is toggled on

Before sending the first query, find the Pro Search toggle near the prompt box. It's the switch that tells Perplexity to use heavier-compute reasoning (the thing the subscription pays for) instead of standard search. If the toggle is off, turn it on.

Re-check the toggle at the start of every new query. Perplexity sometimes resets the toggle between sessions or after navigating away from the chat view.

## What to do when sign-in fails

Three patterns are common.

**Pattern A — the session timed out.** The page loads but shows a sign-in button. Ask Oliver to sign in via the extension; resume when he confirms.

**Pattern B — Perplexity prompts for a captcha or 2FA mid-session.** Pause the run. Surface to Oliver immediately. Don't try to solve the captcha through the browser tool — that's a security boundary the tool isn't supposed to cross.

**Pattern C — the account indicator disappeared.** Perplexity may have redesigned the UI. Surface a screenshot to Oliver, ask whether the session is signed in, and either continue or update this file's Step 3 to match the new UI.

## What to do when the page text doesn't match expectations

If `mcp__Claude_in_Chrome__get_page_text` returns content that doesn't look like a Perplexity answer (truncated, blank, error page, captcha), don't assume the query ran. Surface the actual returned text to Oliver and stop. The failure mode this file is designed to prevent is silently writing a refinement output sourced from broken page text.

## Between-query politeness

Wait a few seconds between queries. Pro Search runs heavier compute and can soft-rate-limit after 5-10 fast back-to-back queries. The rate-limit looks like a slowdown banner, a slow response, or a "you've hit a usage limit" message. If you hit one, pause longer and resume; if it hardens, stop and surface to Oliver.

## UI-change protocol

Perplexity's UI changes over time. When the page text returned from `get_page_text` doesn't match the structure assumed in this file, or when the Pro-Search toggle moves, or when the account indicator's wording changes:

1. Surface the mismatch to Oliver immediately. Don't fake a Pro confirmation.
2. Ask for a fresh screenshot of the current UI.
3. Update this file's Step 3 and Step 4 to match.
4. Bump this file's `updated:` line and re-save.

Every suite skill that points here picks up the fix automatically.

## See also

- [[perplexity-cost-rules]] — per-invocation caps and weekly budget reality
- [[perplexity-query-templates-index]] — index pointing at each skill's query templates
- [[perplexity-refinement]] — the Wave 0 skill that originated these steps
- [[perplexity-research-suite]] — the router skill that lists the whole suite
