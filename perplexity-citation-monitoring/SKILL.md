---
name: perplexity-citation-monitoring
description: Run a monthly (or on-demand) scan of which URLs Perplexity is citing for a small set of head queries that matter to a client or a domain. Each run captures the cited source list, diffs it against the prior snapshot, flags newly-emerging sources, drops, and position shifts, and writes the result back to an accumulating citation-history note. Triggers on phrases like "run citation monitoring on [client]," "check AI citations for [domain]," "who's getting cited for [head query] right now," "monthly citation scan for [client/domain]," "has anyone new started showing up in AI citations for [topic]," or any time the operator wants a cheap, repeatable read of "which URLs is the AI-search engine pointing at for the queries that matter." Also fires as a scheduled task once the operator registers a monthly cron via the schedule skill. Vault-writing skill — produces a per-client or per-domain citation-history note that grows over time so trends emerge across months.
---

# Perplexity citation-monitoring skill (v1.0)

The standing-value, cheapest skill in the Perplexity suite. Built to answer one question on a recurring cadence: **which URLs are AI engines citing for the head queries that matter, and is that set shifting?**

This skill exists because Otterly.ai's daily prompt tracking is configured around prompts you already know to watch. It catches movement on the prompts you set up. It can't catch the open-ended "what NEW sources are AI engines citing for the head queries our clients want to win." This skill does that — runs the open-ended Perplexity Pro query "which sources are most authoritatively cited for X right now," diffs against the prior run, and flags newly-emerging sources, drops, and position shifts.

**Critical behaviors — read this first:**

- **Non-destructive append.** Each run appends a new dated section to the citation-history note. Never overwrite prior snapshots. The whole point is that trends emerge across months — that only works if the historical record stays intact.
- **Cheap by default.** 5-8 queries per run, not 15. Citation-monitoring is the cheapest standing skill in the suite. A monthly run for a single client should cost under 5% of the weekly Pro Search budget.
- **Sonar API only.** All runs go through the Perplexity Sonar API via `~/workspace/second-brain-tier3/automation/scripts/perplexity_sonar.py`. (Historical note: v1 of this skill originally specified Claude in Chrome → Perplexity Pro browser session at v1 + Sonar at v2; Path A was removed 2026-06-01 and Sonar became the only path, collapsing v1 + v2 into a single path.)
- **Perplexity only at v1.** ChatGPT, Claude, and Gemini citation tracking land in v2. v1 is the cheapest viable version — one surface, monthly cadence, per-scope citation-history note.
- **Cite every URL Perplexity surfaces.** No URL lands in the citation-history note without the query that surfaced it and the date. The history is the trust anchor; lazy citation poisons it.

---

## When to use this skill

Trigger when the operator wants a recurring read of "what's Perplexity citing for the queries that matter." Typical phrasings:

- "Run citation monitoring on EV Electric Services"
- "Check AI citations for the SEO domain"
- "Who's getting cited for 'panel upgrade Fairfax VA' right now?"
- "Monthly citation scan for S&H Contracting"
- "Has anyone new started showing up in AI citations for residential electrical?"
- As a scheduled task once registered via the `schedule` skill (Phase 3 below explains how to register).

Do **not** use this skill when:

- You want to validate or refine a specific vault artifact (use `perplexity-refinement` instead — that's the artifact-anchored skill).
- You want to do a one-shot competitor scan with no expectation of repeat (you can, but the value of this skill is the trend line; a one-shot scan is a waste of the framing).
- You want multi-surface citation tracking (ChatGPT, Claude, Gemini). That's v2 scope; for now use Otterly.ai for multi-surface configured-prompt monitoring.
- The scope is "everything Keelworks knows about." Citation monitoring is per-client or per-domain by design. Cross-scope aggregation is out of scope at v1.

---

## Inputs the skill needs

Confirm with the operator before running. Present as plain text — the `AskUserQuestion` tool is glitching per Oliver's standing memory.

1. **Scope** (required). One of:
   - A **client** name — `ev-electric-services`, `s-and-h-contracting`, etc. Writes to `04_projects/clients/_active/<client>/citation-history/citation-history-<client>.md`.
   - A **domain** name — `seo`, `marketing`, `residential-electrical`, etc. Writes to `03_domains/<domain>/citation-history.md`.

   If the operator names a scope that doesn't match an existing client folder or domain folder, surface the mismatch and ask. Don't silently create a new scope.

2. **Head queries** (required). The 3-8 head queries to monitor for this scope. Default sourcing:
   - For a client scope: pull from the latest service brief's §3a (head keyword + primary variants), or from a per-client config file if one exists at `04_projects/clients/_active/<client>/citation-history/head-queries.md`.
   - For a domain scope: pull from a domain-level config at `03_domains/<domain>/head-queries.md`, or — if none — surface a proposed list of 5-8 queries based on the domain's primer and ask the operator to confirm.

   Always surface the proposed list to the operator before running queries. Citation monitoring is only as useful as the head queries it's pointed at.

3. **AI surfaces to check** (optional, default `perplexity-only` at v1). At v2 this expands to `perplexity + chatgpt + claude + gemini`. At v1 the only valid value is `perplexity-only`; warn and continue if anything else is named.

4. **Comparison mode** (optional, default `delta-from-last-run`). Other modes:
   - `delta-from-last-run` (default) — compare to the most recent snapshot in the citation-history note.
   - `delta-from-first-run` — compare to the very first snapshot (useful for "how has this drifted over six months").
   - `snapshot-only` — write the new snapshot without diffing. Only useful for the first ever run on a new scope.

5. **Cap override** (optional, default 8 queries). Hard cap is 8 per run. Operator can override down to 3 or up to 12, but anything over 8 should surface a confirmation since the skill's design point is "cheap."

If any required input is missing, ask before running. Under-specified inputs waste Perplexity queries on the wrong scope.

---

## High-level workflow

Three phases. Each has a stop condition; don't run past it without operator approval.

1. **Setup and scope confirmation** — locate or initialize the citation-history note, pull the head queries, confirm the Pro Search browser session.
2. **Run citation queries** — one Perplexity Pro query per head query, capped at 8 by default, capture the cited source list verbatim.
3. **Diff and write back** — compare to the prior snapshot, categorize each source (same / newly-emerging / dropped / position-shifted), append a new dated section to the citation-history note, surface operator-actionable items.

Mark each phase as a task in the operator's task list so progress is visible.

---

## Phase 1 — Setup and scope confirmation

### 1a. Locate or initialize the citation-history note

For a **client scope**, the note lives at:

```
~/workspace/second-brain/04_projects/clients/_active/<client>/citation-history/citation-history-<client>.md
```

For a **domain scope**, the note lives at:

```
~/workspace/second-brain/03_domains/<domain>/citation-history.md
```

If the note exists, read it. If it doesn't, this is the first run for this scope — surface that to the operator and initialize the file with the frontmatter block below, an empty body, and a "## First scan" heading. The first run writes a `snapshot-only` entry (no diff is possible without a prior snapshot).

Initial frontmatter:

```yaml
---
type: citation-history
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
scope: <client-name or domain-name>
scope-type: <client | domain>
surfaces: [perplexity]
head-query-count: N
tags: [citation-history, perplexity, <scope-name>, citation-monitoring]
---
```

### 1b. Pull and confirm the head queries

For a client scope, in order of preference:

1. Per-client config at `04_projects/clients/_active/<client>/citation-history/head-queries.md` — if present, use these.
2. Latest service brief's §3a head queries — for ev-electric, the panel-upgrade brief is the canonical source today.
3. Operator-supplied list in the trigger message.

For a domain scope, in order of preference:

1. Per-domain config at `03_domains/<domain>/head-queries.md` — if present, use these.
2. Surface a proposed list of 5-8 queries based on the domain primer's Section D (named tactics) or Section C (research engines) and ask the operator to confirm.

Always surface the final head-query list to the operator before running. Format:

```
Proposed head queries for <scope> (N queries, cap is 8):
1. "<query>"
2. "<query>"
...
Confirm, edit, or override the cap.
```

### 1c. Confirm the Pro Search browser session

Follow the four-step browser checklist in `~/workspace/skills/perplexity-shared/references/perplexity-browser-setup.md`. This is the shared check every Perplexity-suite skill runs before sending queries. If the checklist fails (no browser connected, not signed into Pro, Pro Search toggle off), stop and surface to the operator.

**Stop condition.** Citation-history note located or initialized. Head queries confirmed. Pro Search session confirmed. Only then move to Phase 2.

---

## Phase 2 — Run citation queries

One Perplexity Pro query per confirmed head query. Cap: 8 by default. Hard cap: 12 (operator-override only).

### 2a. The core query shape

For each head query, send a Perplexity Pro query of this shape (see `references/query-shapes.md` for the full set):

```
For the query "<head query>", which 5-10 sources are most authoritatively
cited as of YYYY-MM-DD? Return the source list in order, with one-line
descriptions of each source. Note any newly-emerging sources or any that
have dropped from earlier citation patterns.
```

The exact template variants live in `references/query-shapes.md`. Pick the shape that best fits the head query (general source list / brand-named source list / cost-anchored query / safety-anchored query).

### 2b. Browser politeness and rate-limit handling

Per the shared browser-setup reference: wait a few seconds between queries. Pro Search runs heavier compute; 8 back-to-back queries can hit a soft rate limit. If you hit a slowdown banner or captcha, pause and surface to the operator.

### 2c. Per-query capture

For each query, capture exactly:

- **Query text as run** (verbatim — including the date stamp)
- **Source list** (URLs, in the order Perplexity showed them, with the one-line descriptions Perplexity gave)
- **Newly-emerging sources Perplexity explicitly flags** (Perplexity sometimes annotates "new" or "emerging" sources directly; capture those flags)
- **Sources Perplexity flags as having dropped** (likewise — capture any explicit drop annotations)

Use `mcp__Claude_in_Chrome__get_page_text` to read the rendered answer. Copy the source list verbatim — do not paraphrase Perplexity's URLs or descriptions.

**Stop condition.** All confirmed queries run and captured. Move to Phase 3.

---

## Phase 3 — Diff, write back, register schedule

### 3a. Diff against the prior snapshot

For each head query, compare the new source list to the most recent snapshot of the same query in the citation-history note. Categorize each URL into one of four buckets:

- **same-as-before** — present in this scan and the prior scan, same position (±1 slot).
- **newly-emerging** — present in this scan, absent from the prior scan.
- **dropped-out** — present in the prior scan, absent from this scan.
- **position-shifted** — present in both scans, moved by 2+ positions.

If this is the first run for the scope (no prior snapshot), every source is "first-seen." Write the snapshot without diff buckets.

### 3b. Surface operator-actionable items

Three categories the operator should always see:

- **New competitors worth investigating.** A newly-emerging source that's a competitor's own site (not a third-party editorial source) is a flag — a new competitor is being cited. Worth a VIS-extraction pass (the skill proposes; operator confirms).
- **Drops worth celebrating.** A previously-cited competitor's URL that dropped out is worth flagging — it may signal their content has gone stale or our pages are catching up.
- **Position shifts on owned URLs.** If the scope is a client and one of the client's own URLs moved up or down by 2+ positions, surface that directly.

### 3c. Append the new dated section

Append a section to the citation-history note. Heading format: `## YYYY-MM-DD — monthly scan` (or `## YYYY-MM-DD — first scan` for the initial run, or `## YYYY-MM-DD — on-demand scan` for ad-hoc runs).

Section body, in this order:

```markdown
## YYYY-MM-DD — monthly scan

**Queries run:** N (cap: 8)
**Pro Search budget used:** N/200 this week (estimated %)
**Comparison:** delta-from-last-run vs. YYYY-MM-DD snapshot

### Newly-emerging sources

- [URL] — [1-line description] — first seen this month, query "<head query>"

### Dropped sources

- [URL] — [1-line description] — present in YYYY-MM-DD scan, absent now, query "<head query>"

### Position shifts

- [URL] moved from #N to #M on query "<head query>" — [direction + one-line interpretation]

### Same-as-before (top-cited URLs that stayed)

- [URL] — query "<head query>" — position #N

### Per-query raw captures

#### Query: "<head query 1>"

- #1 [URL] — [Perplexity's one-line description]
- #2 [URL] — ...
- ...

#### Query: "<head query 2>"

- #1 [URL] — ...
- ...

### Operator-actionable

- [bullet] — [why this matters + suggested next step, with priority]

---
```

The per-query raw captures section is the load-bearing piece — future runs diff against it. Don't truncate URLs, don't paraphrase descriptions.

### 3d. Frontmatter update on the note

Bump the `updated:` date. Increment a `last-scan:` field (add if not present). Add an `last-scan-query-count:` field with the actual number of queries run.

```yaml
updated: YYYY-MM-DD
last-scan: YYYY-MM-DD
last-scan-query-count: N
```

### 3e. Register the monthly scheduled task (offered, not automatic)

After the first successful run for a scope, offer to register a monthly scheduled task that re-runs this skill:

```
This was the first scan for <scope>. Want me to register a monthly
scheduled task that re-runs citation monitoring on the same head
queries? It would fire on the same day of the month each month.

To register: I'd create a scheduled task via mcp__scheduled-tasks__create_scheduled_task
with a cron expression like "0 9 1 * *" (9am on the 1st of every month)
and the prompt "Run citation monitoring on <scope> using the head
queries in the citation-history note."

Confirm, adjust the schedule, or skip.
```

If the operator confirms, register the task via `mcp__scheduled-tasks__create_scheduled_task` with the operator-confirmed cron expression. Surface the task ID back so the operator can find it via `mcp__scheduled-tasks__list_scheduled_tasks` later.

If the operator declines, skip — the skill still works on-demand without a registered schedule. The offer comes once, on the first run for each new scope.

**Stop condition.** Citation-history note updated. Frontmatter bumped. Operator-actionable items surfaced. Schedule offer made (first run only). Move to the completion report.

---

## Output contract

Every citation-monitoring run produces exactly these artifacts:

1. **Citation-history note** — the per-scope file at the canonical path. Either initialized (first run) or appended (subsequent runs).
2. **Execution-log entry** — appended to the active execution log per the standing memory `feedback_running_execution_log_default.md`. For Keelworks-suite work, the log lives in ev-electric-services' execution-logs folder (most active client). For per-client work in a different client, the log lives in that client's `.kos/execution-logs/`.
3. **Terse completion report in chat** — per `feedback_terse_completion_reports.md`:
   - Scope scanned + N queries run
   - Newly-emerging source count + the top 3 by query
   - Dropped source count + the top 3 by query
   - Operator-actionable items count + the top 3 by priority
   - Pro Search budget consumed (estimated %)
   - Whether a schedule was registered (and the task ID if so)

The completion report uses bullets, not paragraphs. It does not restate the citation-history content — the operator can read the file.

---

## Cost-management rules

Canonical rules live in `~/workspace/skills/perplexity-shared/references/perplexity-cost-rules.md`. What this skill enforces on top:

- **Hard cap: 8 queries per run by default.** Override allowed up to 12; below 3 the skill warns "this is too thin to surface trends." The 8-query default keeps a single client's monthly scan at ~4% of the weekly Pro Search budget.
- **Sonar API path (v2).** Scheduled monthly runs should route through Perplexity Sonar (pay-per-query, ~$0.005-$0.02 per query) so they don't draw on the shared Pro browser cap. At v1 the skill is browser-only; v2 picks up Sonar when the integration lands.
- **Don't repeat a scope inside its refresh window.** Default refresh window: 28 days. If the operator triggers the skill against a scope that ran inside the last 28 days, surface the prior run date and ask before proceeding. Citation patterns don't move week-to-week; monthly is the right cadence.
- **Log the query count and the date stamp** in the citation-history note's "Queries run: N" line. The router skill (`perplexity-research-suite`) reads these lines to surface the weekly tally. Don't drop the discipline.

When Perplexity's caps or Sonar pricing changes, the fix happens in the shared cost-rules file; this section picks up the change automatically.

---

## Plain-language requirement

Per [[plain-language-conventions]] and the standing `feedback_plain_language_default.md` memory: write the citation-history note in plain language. Short sentences. Conversational rhythm. Concrete over abstract. The one-line source descriptions should read like a colleague describing a URL, not a search-result snippet.

The operator-actionable section is the most important to keep plain — these are the bullets that turn into next-week's work, and dense prose there means slower follow-through. Lead with the action, not the analysis.

---

## Integration with other skills

This skill plays well with the rest of the Knowledge OS skill set.

### perplexity-refinement

When citation monitoring surfaces a **newly-emerging dominant source** (a URL that appears in the top 3 of 2+ head queries and wasn't in the prior scan), propose running `vis-extraction` on it first, then `perplexity-refinement` on the resulting source note. The new source likely has signal worth absorbing into the vault. The skill proposes; the operator confirms.

### service-seo-research

When citation monitoring surfaces **position shifts on head queries that come from a service brief** (the brief's §3a queries), propose refreshing the service brief. The signal is: the SERP composition the brief assumed has moved. The brief's `updated:` date probably needs to be re-anchored against the current top sources.

### vis-extraction

A newly-emerging source is a candidate for VIS-extraction. The proposal lands in the citation-history note's "Operator-actionable" section as: "Investigate new source [URL] — propose VIS-extraction pass."

### perplexity-research-suite router

This skill registers under the router as Wave 1C. The router lists it in the menu, dispatches to it when the operator describes a citation-tracking goal, and contributes the skill's per-run "Queries run: N" line to the weekly Pro Search budget tally.

### schedule skill / mcp__scheduled-tasks__create_scheduled_task

Phase 3e (above) wires this skill into the scheduling system. The schedule skill is the canonical way to register the monthly cron; this skill calls `mcp__scheduled-tasks__create_scheduled_task` directly on operator confirmation. The fired schedule produces a prompt that re-invokes this skill on the same scope.

### otterly.ai (external tool)

Otterly.ai is the daily-prompt-tracking sibling. Otterly tracks the prompts you already know to watch; this skill tracks the open-ended "what's getting cited for the head queries that matter" question. The two are complementary:

- Otterly answers "is our configured prompt list moving?"
- This skill answers "what NEW sources are appearing on the head queries we want to win?"

Don't replace Otterly with this skill; run both.

---

## Closing step — Auto-invoke output-quality-loop

After the citation-history snapshot is written, the diff against the prior snapshot is produced, and any client-facing recap line is surfaced, emit the standard auto-invoke block per `~/workspace/skills/output-quality-loop/references/auto-invoke-convention.md` and `~/workspace/second-brain/_meta/conventions.md` § "Output quality". This is the closing step every artifact-producing skill emits before declaring the chat done. Convention shipped Phase 5 of the output-quality-loop project (2026-05-28).

**Artifact list for this skill.** In per-client mode: the per-client citation-history snapshot file (e.g., `~/workspace/second-brain/04_projects/clients/_active/<client>/citation-history/<YYYY-MM>.md`). In per-domain mode: the running domain citation-history file at `~/workspace/second-brain/03_domains/<domain>/citation-history.md`. If a per-run digest sister file was produced, list it too.

**The block to emit (verbatim):**

````markdown
## Auto-invoke output-quality-loop

This skill produced the following artifact(s):
- `<citation-history-snapshot-path>`
- `<digest-sister-file-path>`  ← only if produced this run

[output-quality-loop:eval] — for each artifact, run output-quality-loop in EVALUATE mode. If PASS, declare the chat done. If NEEDS REVISION or FAIL, ingest the revision prompt as if it were operator input and regenerate the artifact, then re-invoke output-quality-loop. Cap at 3 iterations; on the 3rd FAIL, escalate to the operator with the evaluation report.
````

Required-element discipline per the convention spec: heading text matches verbatim (`## Auto-invoke output-quality-loop`); one bullet per artifact with full path in backticks; directive opens with `[output-quality-loop:eval]` and includes the iteration-cap discipline language.

**Iterate or declare done.** All PASS → declare done. Any NEEDS REVISION (minor / substantive) → Mode 2 auto-fires a revision prompt; ingest as operator input, apply fixes (tighten the diff section, add missing source classifications, fix a frontmatter field, restore the head-query-list provenance line), re-emit the block, loop. Any FAIL → revision prompt includes root-cause analysis; address the root cause (often: missing per-query response capture, source list shape drift, no Pro Search budget line, snapshot frontmatter shape mismatch), regenerate, re-emit, loop.

**Iteration cap (3 max).** Track count via the folder-quality-log's per-artifact section before each regeneration. If three iteration entries exist and the verdict is still not PASS, **escalate** to the operator with the evaluation report and stop. Don't run a fourth iteration — that's the load-bearing cost-control discipline.

**Operator bypass.** Include `--bypass-quality-loop` (or "skip the quality loop") in the original monitoring request to skip the block for that invocation. The bypass records to the closest folder's `_quality-log.md` under `### Bypassed (manual override)`.

---

## Vault stewardship

Per [[vault-stewardship-principles]]:

1. **Check folder structure before writing.** Per-client citation-history notes live at `04_projects/clients/_active/<client>/citation-history/`. Per-domain notes live at `03_domains/<domain>/citation-history.md`. If the parent client folder has a `_README.md`, scan it for any subfolder conventions before creating `citation-history/`.

2. **Initialize subfolders with a one-line note.** On the first run for a client scope, the `citation-history/` subfolder gets created. If the client folder has a `_README.md` listing children, add a one-line entry: `- citation-history/ — monthly AI-citation snapshots per perplexity-citation-monitoring skill`.

3. **Slug-only wikilinks.** When the citation-history note links to other vault notes (the source service brief, related VIS-extracted sources), use `[[slug]]` not `[[path/slug]]`. Per `conventions.md`.

4. **Non-destructive append.** Every run appends a new dated section. Never overwrite prior snapshots. If a snapshot needs correcting (a URL was captured wrong), add a `**Correction:**` line under the original — don't edit the original line.

5. **Don't propose vault-level changes from this skill.** The skill writes to the per-scope citation-history note and nowhere else. If the operator-actionable section flags a primer extension, tactic candidate, or pattern-promotion candidate, surface it as a proposal in the chat completion report — let the operator pick the next skill to invoke.

---

## Verification before declaring done

Before reporting completion to the operator:

1. **Frontmatter check** — citation-history note's frontmatter has valid YAML, includes `updated:`, `last-scan:`, `last-scan-query-count:`, `surfaces: [perplexity]`, and `scope:` + `scope-type:`.

2. **Citation check** — every URL in the new section has the query that surfaced it noted. Grep for URLs in the new section; each should have a `query "<head query>"` annotation within 5 lines.

3. **Diff sanity check** — the diff buckets (newly-emerging, dropped-out, position-shifted, same-as-before) reconcile with the prior snapshot. The total URL count in this scan + the dropped-out count = the prior-snapshot URL count + the newly-emerging count. Off-by-one is fine; structural mismatches mean the diff was computed against the wrong prior snapshot.

4. **Wikilink check** — wikilinks resolve (slug-only form). If the note references a service brief or source note, confirm the target slug exists.

5. **Cap check** — total queries run is at or under the cap (8 by default, 12 hard ceiling). If over, the operator approved the override.

6. **Schedule check (first run only)** — if a schedule was registered, the task ID is in the completion report and the cron expression is what the operator confirmed.

7. **Plain-language check** — the operator-actionable section reads plain. Pick the densest bullet and confirm.

---

## Reporting back to the operator

Terse completion summary (per `feedback_terse_completion_reports.md`):

- Scope: `<client or domain>`. Queries run: N of 8 cap.
- Newly-emerging: X sources. Dropped: Y. Position-shifted: Z.
- Top operator-actionable: [bullet 1] [bullet 2] [bullet 3].
- Pro Search budget: ~N/200 this week (estimated %).
- Schedule registered: yes (task ID `<id>`, cron `<expr>`) / no.
- Citation-history note: `<path>`.

No restating of the per-query captures. The note is the artifact; the chat is the receipt.

---

## Out of scope (v1.0)

Explicit non-goals for the v1 build:

- **Multi-surface tracking.** Only Perplexity at v1. ChatGPT, Claude, Gemini land in v2 as additional `surfaces:` values.
- **Sonar API integration.** Scheduled monthly runs go through the browser at v1; v2 routes them through Sonar so they don't draw on the shared Pro browser cap.
- **Automatic VIS-ingestion of newly-emerging sources.** The skill surfaces candidates in the operator-actionable section; the operator picks which to ingest and triggers `vis-extraction` separately.
- **Cross-scope trend aggregation.** Each client's citation-history is independent at v1. A future skill could roll up "across all clients in residential-electrical, what sources are appearing in 3+ citation histories" — that's a synthesis-class job, not this skill's.
- **Auto-publication of competitive-intelligence reports.** The citation-history note is internal. No client-facing report is generated from it.
- **Refinement-style triage by tier.** Every head query is treated equally at v1; there's no high/medium/low tiering. The whole skill is shallow by design.

---

## Reference files

When you need them, read these:

- `~/workspace/skills/perplexity-citation-monitoring/references/query-shapes.md` — the 3-4 query shapes the skill uses (general source list, brand-named source list, cost-anchored, safety-anchored)
- `~/workspace/skills/perplexity-shared/references/perplexity-browser-setup.md` — pre-query browser checks (sourced from Phase 1c)
- `~/workspace/skills/perplexity-shared/references/perplexity-cost-rules.md` — suite-wide cost-management rules
- `~/workspace/skills/perplexity-shared/references/perplexity-query-templates-index.md` — index of every suite skill's query templates
- `~/workspace/skills/perplexity-research-suite/SKILL.md` — the router that lists this skill and dispatches into it
- `~/workspace/skills/perplexity-refinement/SKILL.md` — sibling skill for artifact-anchored refinement (newly-emerging sources flow toward refinement after VIS-ingestion)
- `~/workspace/second-brain/_meta/plain-language-conventions.md` — voice rules
- `~/workspace/second-brain/_meta/conventions.md` — KOS naming and frontmatter
- `~/workspace/second-brain/03_domains/seo/tools/aeo-geo-tools-survey.md` — Otterly.ai is the daily-prompt-tracking sibling tool

---

## Maintenance notes

### M1: Perplexity Pro UI changes (added 2026-05-27, v1.0)

**The issue:** Perplexity's web UI for source-list rendering changes over time. Phase 2c assumes the late-May-2026 UI where source lists appear as numbered items with one-line descriptions.

**How it surfaces:** `mcp__Claude_in_Chrome__get_page_text` returns content where the source list structure doesn't match what Phase 2c assumes, or sources are listed in a different order than displayed visually.

**How to fix:** Surface the mismatch to the operator. Ask for a fresh screenshot of the current source-list rendering. Update the shared `perplexity-browser-setup.md` (UI-change protocol). Don't fake the source ordering — the diff math depends on it.

### M2: First-run scope with no prior snapshot (added 2026-05-27, v1.0)

**The issue:** The first run for a new scope can't diff (no prior snapshot exists). The skill needs to recognize this and write a snapshot-only entry without the diff buckets.

**How it surfaces:** Phase 3a's diff logic produces nonsense buckets if it runs against an empty prior state.

**How to fix:** Phase 1a checks whether the citation-history note exists. If it doesn't, the skill initializes the file and sets a flag for Phase 3 that forces snapshot-only mode. The diff buckets are omitted; only the per-query raw captures section is written. Phase 3e (schedule offer) still fires.

### M3: Sonar API integration not yet built (added 2026-05-27, v1.0)

**The issue:** v1 ships browser-only. Scheduled monthly runs draw on the shared Pro Search browser cap even though they should be routed through Sonar to keep budget for interactive work.

**How it surfaces:** A client with 8 head queries scanned monthly burns ~32 queries/month on the browser cap. Five clients on the same cadence = ~160/month. That's ~40 queries/week against a 200/week cap — meaningful.

**How to fix:** Build v2 Sonar integration. Until then, the workaround is to run fewer head queries per scope (3-5 instead of 8) or to space client scans across different weeks of the month. The shared `perplexity-cost-rules.md` flags the Sonar path; this maintenance note tracks the implementation gap.

### M4: Drift in head-query lists (added 2026-05-27, v1.0)

**The issue:** The head queries for a scope change over time — services launch, the client adds a new vertical, a new neighborhood becomes a priority. The citation-history note becomes incoherent if head queries silently change between runs.

**How it surfaces:** A diff bucket shows a "newly-emerging" URL that's actually present in the prior scan but under a different query string.

**How to fix:** Phase 1b surfaces the current head-query list against the prior-run list. If they don't match, ask the operator before running — either update the head-query config and proceed, or revert to the prior list. Don't silently switch query sets.

---

## How to add a new maintenance note

When the skill errors or produces a miss in production, add a new entry: **Issue → How it surfaces → How to fix → Why it wasn't designed away.** Date-stamp the entry. Future-Claude learns from past misses without re-hitting the same wall.

---

## See also

- [[perplexity-refinement]] — Wave 0 sibling; receives newly-emerging sources after VIS-ingestion
- [[perplexity-research-suite]] — Wave 1B router; lists this skill in the menu
- [[perplexity-browser-setup]] — shared pre-query browser checks
- [[perplexity-cost-rules]] — shared cost rules across the whole suite
- [[perplexity-query-templates-index]] — shared templates index
- [[vis-extraction]] — invoked downstream when a newly-emerging source is worth ingesting
- [[service-seo-research]] — proposed for refresh when position shifts on brief-sourced queries
- [[meta-document-primer]] — primer companion (per-scope citation-history doesn't extend primers directly, but operator-actionable items may surface primer-extension candidates)
- [[plain-language-conventions]] — voice rules
- [[conventions]] — KOS naming and frontmatter rules
- [[primer|seo/primer]] — SEO operational primer (Section E names this skill as the 6th in the knowledge-growth ecosystem)
- [[aeo-geo-tools-survey]] — Otterly.ai is the daily-prompt-tracking sibling
- [[_README|perplexity-skill-build roadmap]] — the build sequence this skill is Wave 1C in
