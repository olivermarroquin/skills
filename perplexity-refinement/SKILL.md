---
name: perplexity-refinement
description: Take any Knowledge OS vault artifact (VIS source notes, research briefs, tactic notes, decision docs, audits, primers, syntheses, anything) and run a structured Perplexity Pro research pass to refine it — validate factual claims, find expert opinions, surface counter-evidence, pull in updated info, attach citations. Triggers on phrases like "refine [filename] with Perplexity," "deepen the research on [filename]," "run a Perplexity pass on [filename]," "fact-check [filename] via Perplexity," "find more sources for [filename]," "what else does Perplexity say about [topic in vault]," or any time the operator wants to triangulate a vault artifact against a fresh Perplexity Pro research pass. Also fires as an optional follow-on step after vis-extraction or service-seo-research finishes producing a new artifact, per Oliver's "make Perplexity a refinement step on everything" direction. Vault artifacts only; not for external/PDF/non-vault content.
---

# Perplexity Refinement Skill (v1.0)

The Perplexity-Pro vault-refinement layer. Takes any vault artifact and runs targeted Perplexity queries against its key factual claims, named tools, statistics, and concepts — then writes the findings back to the vault as a structured refinement section, an inline-merged update, or a sister file.

This skill exists because Oliver upgraded to Perplexity Pro on 2026-05-26 ($21.20/mo all-in). The ROI play is to make Perplexity the standing fact-check + citation-deepening pass on everything that lands in the vault. Any source note, brief, tactic, decision, or primer gets denser, more cited, and more triangulated with one refinement pass.

**Critical behavior (read this before anything else):**

- **Non-destructive by default.** Append mode is the default. Inline edits to existing claims require operator confirmation per claim. The original artifact is never silently rewritten.
- **Vault artifacts only.** Don't refine PDFs, external docs, web pages you don't own, or chat transcripts that aren't already vault notes. Refinement is for things the vault already knows about.
- **Every refinement claim cites its Perplexity-surfaced source.** No claim makes it back to the vault without a URL. This is the load-bearing discipline that justifies the cost of the subscription.
- **Browser-driven only.** Perplexity is reached via Claude in Chrome (`mcp__Claude_in_Chrome__navigate` to `perplexity.ai`). There is no Perplexity API for Pro searches in this configuration. Confirm the browser session is signed into Pro before starting.
- **Cost-managed.** Per-invocation query caps (3/7/15 by depth). Low-tier items skipped by default. Refinements cached in the artifact so re-running doesn't duplicate effort.

---

## When to use this skill

Trigger when the operator points at a specific vault artifact and wants Perplexity to refine it. Typical phrasings:

- "Refine `panel-upgrade.md` with Perplexity"
- "Deepen the research on the Nico source note"
- "Run a Perplexity pass on this brief"
- "Fact-check the panel-upgrade brief via Perplexity"
- "Find more sources for the de-indexation recovery observation"
- "What else does Perplexity say about Capsule Content technique?"
- As an opt-in follow-on after a vis-extraction or service-seo-research run completes

Do **not** use this skill for:

- Refining content that isn't already a vault file (paste-only content)
- Refining external PDFs or docs the vault doesn't own
- Running a Perplexity research session that isn't anchored to an existing artifact (use a regular Cowork prompt with Claude in Chrome)
- Bulk auto-refinement of every vault note on a schedule — over-investment until manual demand justifies it

---

## Inputs the skill needs

Confirm with the operator before running. Present as plain text; the `AskUserQuestion` tool is glitching per Oliver's standing memory.

1. **Target artifact path** (required). The vault file to refine. Use the full path or a vault-relative slug; the skill resolves it. If multiple matches, list them and ask.

2. **Refinement depth** (optional, default `medium`).
   - `light` — up to **3** Perplexity queries. Quick triangulation of the 1-3 most important claims.
   - `medium` — up to **7** queries. Standard pass for source notes and tactic notes.
   - `deep` — up to **15** queries. Reserved for briefs and synthesis docs where saturation matters.

3. **Refinement mode** (optional, default `append`).
   - `append` — add a new "Perplexity refinement — YYYY-MM-DD" section to the bottom of the artifact.
   - `inline-merge` — propose per-claim edits inline; operator confirms each before any rewrite touches the body.
   - `sister-file` — write a separate sister file at `<original>-perplexity-refined-YYYY-MM-DD.md` so the original stays untouched.

4. **Specific focus areas** (optional). Operator can narrow scope: "validate the tool pricing claims," "find counter-evidence on the 60% indexation claim," "focus on AI-search citations only." Narrows the Phase 2 query plan.

If any input is missing, ask before running. Under-specified inputs waste Perplexity queries on the wrong claims.

---

## High-level workflow

Five phases. Each phase has a stop condition; don't run past it without operator approval.

1. **Parse the target artifact** — read it, extract claims/tools/stats/concepts/entities, tier each by refinement value.
2. **Run targeted Perplexity queries** — one query per high-tier item, capped per depth, via Claude in Chrome.
3. **Synthesize findings** — validated / updated / contradicted / new perspectives / new sources to ingest / suggested vault edits.
4. **Apply refinement based on mode** — append, inline-merge, or sister-file. Update frontmatter.
5. **Surface follow-ups** — propose new sources to VIS-ingest, primer extensions, tactic-note candidates. Update the execution log.

Mark each phase as a task in the operator's task list so progress is visible.

---

## Phase 1 — Parse the target artifact

Read the file end to end. Then build a structured list of the things worth refining.

### 1a. What to extract

Five categories. For each item, capture the exact wording from the artifact and the surrounding context (1-2 sentences).

| Category | Examples |
|---|---|
| **Factual claims** | "Otterly.ai Lite is $29/mo for 15 prompts"; "Federal Pacific Stab-Lok breakers fail to trip in measurable percentages of cases" |
| **Tools / products named** | DataForSEO, Otterly.ai, Watchdog, Featured.com, Claude Code, Astro, Higgsfield |
| **Statistics quoted** | "95% of AI citations come from content less than 10 months old"; "~60% of published content stays indexed"; "$1,300–$3,000 typical, $800–$4,000 full range" |
| **Concepts that could be deepened** | Capsule Content technique, Attribute Match, de-indexation recovery, fan-out cluster dashboard, structural vs. editorial backlinks |
| **Entities** (people, businesses, places, organizations) | AJ Long Electric, Mr. Electric, Rewiring America, This Old House, Nico SKOOL, Cole Medin |

### 1b. Tiering by refinement value

For each item, assign a tier:

- **High** — externally verifiable, decision-relevant, and currently load-bearing in the artifact's conclusions. Refine.
- **Medium** — externally verifiable but not load-bearing, or load-bearing but already well-cited. Refine only at `deep` depth.
- **Low** — operator-internal observations, vault-internal patterns, things Perplexity can't reasonably validate (e.g., "Nico already counted in 3 promoted-to-3/3 tactics"). Skip by default.

Tiering heuristics:

- **Numeric claims** default to high (Perplexity is good at finding the primary source for a stat).
- **Pricing or product-feature claims** default to high (these go stale fast).
- **Date-bound claims** ("the 2024 BrightEdge study") default to high (worth verifying the date and the existence of the study).
- **Named tools and products** default to high if the artifact makes a recommendation about them; medium if only mentioned.
- **Definitional claims about widely-used concepts** default to medium (Perplexity can cite multiple definitions but may not add value over what's already in the artifact).
- **Vault-internal pattern math and operator-discipline observations** default to low.

### 1c. Output of Phase 1

A numbered list of refinement candidates, grouped by tier, ready for operator review. Format:

```
HIGH TIER (will refine — N items):
1. [category] "exact quote from artifact" — why this is worth refining
2. ...

MEDIUM TIER (skipped unless deep depth — N items):
...

LOW TIER (skipped by default — N items):
...
```

**Stop condition.** Show the list to the operator. Confirm the high-tier list before running queries. Operator may promote / demote items, add focus areas, or change depth.

---

## Phase 2 — Run targeted Perplexity queries

One query per confirmed high-tier item (plus medium if `deep` depth). Cap per depth:

| Depth | Max queries |
|---|---|
| `light` | 3 |
| `medium` | 7 |
| `deep` | 15 |

If the high-tier list exceeds the cap, ask the operator which items to drop before running. Don't silently truncate.

### 2a. Browser setup

Follow the four-step browser checklist in `~/workspace/skills/perplexity-shared/references/perplexity-browser-setup.md`. That file is the single source for connecting the browser, navigating to Perplexity, confirming the Pro session, and confirming the Pro Search toggle. When the Perplexity UI changes, update that shared file; the change propagates here automatically.

Don't skip the four steps. A missed step means the run might use standard search (not Pro Search) and waste the subscription cost.

### 2b. Query templates

Use the templates in `references/query-templates.md`. Six shapes:

- **Validate a claim** — "Is it true that [claim]? Cite primary sources."
- **Validate a tool's current state** — "What is the current pricing, feature set, and reputation of [tool] in 2026?"
- **Validate a statistic** — "What is the original source of the statistic '[stat]' and is it still accurate?"
- **Deepen a concept** — "What are the latest 2026 perspectives on [concept]? Surface 3-5 expert viewpoints with citations."
- **Find counter-evidence** — "What are the arguments against [claim or concept]? Surface counter-positions with citations."
- **Find updated info** — "What's changed about [topic] since [date in artifact]?"

Pick the template that best matches the high-tier item's category (claim → validate-a-claim; statistic → validate-a-statistic; tool → validate-a-tool; etc.).

### 2c. Per-query capture

For each query, capture exactly:

- The query text as run (verbatim)
- The first 200-400 words of Perplexity's answer (or the full answer if shorter)
- The full source list Perplexity cited (URLs, in the order shown)
- A one-line verdict on the original claim: `validates` / `partially-validates` / `contradicts` / `inconclusive`
- Any notable counter-positions or alternative framings the answer surfaced

The `mcp__Claude_in_Chrome__get_page_text` tool returns the rendered answer; copy the answer and the source list from there.

### 2d. Throttling and politeness

- Wait a few seconds between queries — Pro Search runs a heavier compute pattern and can rate-limit in practice if 10+ run back-to-back.
- If a query times out or returns an error page, retry once after a short pause. Don't loop.
- If Perplexity prompts to sign in mid-session, surface to operator immediately. Do not bypass.

**Stop condition.** All confirmed queries run. Surface the per-query captures to the operator before moving to synthesis if `deep` depth, or proceed directly to Phase 3 for `light` / `medium`.

---

## Phase 3 — Synthesize findings

Group the captured query results into six buckets. Each bucket has a structured shape.

### 3a. Validated claims

The original artifact was correct; Perplexity found primary sources backing it.

Format per item:

> **Claim:** [exact quote from artifact]
> **Verdict:** Validated.
> **Sources:** [URL 1], [URL 2], [URL 3]
> **Notes:** [optional — what the new sources add beyond what the artifact already cited]

### 3b. Updated facts

The original claim was correct *at the time* but newer info exists. The artifact should be updated.

Format per item:

> **Claim:** [exact quote from artifact]
> **Original state (per artifact):** [what the artifact said]
> **Current state (per Perplexity):** [what's true now]
> **Sources:** [URLs]
> **Recommended edit:** [concrete change to make to the artifact]

### 3c. Contradicted claims

Perplexity found evidence against the original claim. Flag for operator review — don't auto-rewrite.

Format per item:

> **Claim:** [exact quote from artifact]
> **Counter-evidence:** [what Perplexity surfaced]
> **Sources:** [URLs]
> **Recommended action:** flag for operator review. Do not auto-edit.

### 3d. New expert perspectives

Voices not in the original artifact that broaden the picture (alternative framings, dissenting takes, additional use cases).

Format per item:

> **Concept:** [concept from artifact]
> **New perspective:** [the angle Perplexity surfaced]
> **Source:** [URL]
> **Why this matters:** [1-sentence relevance to the artifact's conclusion]

### 3e. New sources to ingest

URLs Perplexity cited that look worth running through vis-extraction as their own source notes. Don't ingest here — just surface candidates.

Format per item:

> **URL:** [link]
> **What it covers:** [1-sentence description]
> **Why worth ingesting:** [adds to which cluster, addresses which gap]

### 3f. Suggested vault edits

Concrete one-line edits to the artifact, ready for operator review.

Format per item:

> **Section:** [which section of the artifact]
> **Current text:** [exact quote, or "missing"]
> **Proposed change:** [the new text]
> **Reason:** [which Perplexity finding drives this]

**Stop condition.** Present the six buckets to the operator. Confirm what to write back to the vault before moving to Phase 4.

---

## Phase 4 — Apply refinement based on mode

Three modes; the default is `append`.

### 4a. Append mode (default)

Add a new section to the bottom of the artifact, just before the `## Related` section if one exists, or at the end of the body otherwise.

Section heading: `## Perplexity refinement — YYYY-MM-DD`

Section body: the six Phase-3 buckets in order, with only the populated buckets included. End with a one-line tally:

> Queries run: N. Validated: X. Updated: Y. Contradicted: Z. New sources surfaced: W.

### 4b. Inline-merge mode

For each item in Phase-3 bucket 3f (suggested vault edits), present the diff to the operator and ask for explicit confirmation per edit. Apply only confirmed edits. Don't batch-apply.

After inline edits, also append a slimmed Perplexity-refinement section that lists the edits made + the new sources surfaced (without re-listing the validated claims, since those didn't trigger a body change).

### 4c. Sister-file mode

Write a separate file at:

`<original-path-without-extension>-perplexity-refined-YYYY-MM-DD.md`

Frontmatter:

```yaml
---
type: perplexity-refinement
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
refines: <original-filename>
refined-by: perplexity-refinement-skill-v1
depth: <light|medium|deep>
queries-run: N
sources-surfaced: M
tags: [perplexity-refinement, refinement, <original-domain>]
---
```

Body: the six Phase-3 buckets in order. Link back to the original at the top with `[[<original-slug>]]`.

### 4d. Frontmatter update on the original

Regardless of mode, add this field to the original artifact's frontmatter (if not already present):

```yaml
perplexity-refined: YYYY-MM-DD
perplexity-refined-by: perplexity-refinement-skill-v1
perplexity-refinement-depth: <light|medium|deep>
```

This lets a future skill invocation see at a glance whether and when refinement has happened.

**Stop condition.** All writes complete. Surface the file paths touched to the operator.

---

## Phase 5 — Surface follow-ups

After the refinement is written, the skill proposes downstream actions and lets the operator pick which to run.

### 5a. New sources to VIS-ingest

If Phase 3e surfaced sources worth ingesting, present them as a numbered list:

> 1. [URL] — [1-sentence description] — proposed cluster: [seo / marketing / etc.]
> 2. ...

Operator picks which (if any). For each confirmed pick, invoke [[vis-extraction]] in standard mode.

### 5b. Primer extensions

If Phase 3d (new expert perspectives) surfaced concepts not in the applicable primer's Appendix A, propose primer extensions:

> 1. Term "[concept]" — proposed gloss: "[1-sentence definition]" — proposed home: [system primer / domain primer / project primer]
> 2. ...

For each confirmed pick, invoke [[meta-document-primer]] in `extend-and-write` mode on the named primer.

### 5c. Tactic-note candidates

If Phase 3d revealed a tactic-shaped pattern that's not yet in `seo/tactics/` or the relevant domain's `tactics/` folder:

> 1. Pattern "[name]" — mechanism: "[1-sentence summary]" — proposed home: `03_domains/<domain>/tactics/tactic-<slug>.md`
> 2. ...

For each confirmed pick, draft the tactic note per `_meta/conventions.md` (correct prefix, frontmatter, links to source).

### 5d. Pattern-promotion candidates

If the new sources from Phase 3e plus the existing artifact would push a cluster pattern over the 3/3 promotion threshold (independent creators making the same architectural commitment), flag:

> 1. Pattern "[name]" currently at N/3. The new source(s) [URL] from a new canonical creator would push to (N+1)/3 if ingested and counted. Recommend handing off to [[multi-source-synthesis]] after VIS-ingestion completes.

### 5e. Execution-log update

Update or create the running execution log per the standing memory `feedback_running_execution_log_default.md`. For Keelworks-infrastructure work (a skill build, a Perplexity refinement pass on a service brief), the log lives in the most active client's execution-logs folder. For project-specific refinements, the log lives in that project's `.kos/execution-logs/`.

Log entry per refinement run:

- Date + target artifact path
- Depth used + queries actually run
- Sources surfaced + which were ingested
- Vault edits applied (per mode)
- Cost/time actuals
- Gotchas (rate limits, sign-out events, ambiguous answers)

**Stop condition.** Operator confirms which follow-ups to execute. Run them. Terse completion report follows.

---

## Cost-management rules

The canonical rules live in `~/workspace/skills/perplexity-shared/references/perplexity-cost-rules.md`. That file is the single source for the weekly cap (~200 Pro Search queries per rolling 7-day window — not unlimited, as the published marketing language sometimes implies), the per-invocation caps across all suite skills, the Sonar API fallback path for scheduled scans, and the operator-warning thresholds.

What this skill enforces, on top of the shared rules:

- **Per-invocation caps** — 3 (light), 7 (medium), 15 (deep). Hard caps; don't exceed without operator override. These line up with the suite-wide caps table in the shared cost-rules file.
- **Skip low-tier items by default** — only refine high-tier (and medium-tier at `deep` depth). Operator can promote items manually.
- **Cache results in the artifact** — frontmatter records `perplexity-refined: YYYY-MM-DD`. A re-run on the same artifact within a refresh window (default 90 days) should ask the operator before running new queries.
- **Log query count + estimated value** in the refinement output. The "Queries run: N" tally at the bottom of the appended section is the cost receipt. Over time, the operator can tune depth by seeing which depths produced which yields. The `perplexity-research-suite` router reads these lines from execution logs to surface weekly tally — don't drop the discipline.

When Perplexity changes its tier structure or rate-limits Pro Search more aggressively, the fix happens in the shared cost-rules file; this section picks up the change automatically. The skill is honest about its cost surface; don't hide queries.

---

## Plain-language requirement

Per [[plain-language-conventions]] and the standing `feedback_plain_language_default.md` memory: write the refinement output in plain language. Short sentences. Conversational rhythm. Concrete over abstract. Gloss obscure terms on first use; keep technical terms when they're the right name for the thing.

The original artifact's voice doesn't get rewritten by this skill (non-destructive default), so the refinement section sits alongside it. Match the artifact's level of formality where it makes sense; lean plain otherwise.

---

## Integration with other skills

This skill plays well with the rest of the Knowledge OS skill set. Specific hand-offs:

### vis-extraction

vis-extraction may invoke perplexity-refinement as an optional Step 9 after the standard Phase 0-7 ingestion completes. Trigger: after the source note lands and triage finishes, the executor asks: "Run perplexity-refinement on the new source note?" Default depth: `medium`. Default mode: `append`.

The vis-extraction skill's "Critical behavior" section already names non-destructive defaults; this skill respects them. The Phase 9 hook is operator-opt-in, not automatic.

### service-seo-research

service-seo-research may invoke perplexity-refinement as an optional Phase 9 after the brief is written. Trigger: after Phase 8 (knowledge-growth hooks) completes, the executor asks: "Run perplexity-refinement on the new service brief?" Default depth: `medium` for first refinement; `deep` if the brief has explicit Perplexity gaps (Section 4b says "Perplexity not reachable from this invocation" — exactly the case the refinement skill exists for).

The service brief template's §15 (Methodology) already flags AI-search gaps explicitly. Running this skill is the standing way to close those gaps.

### meta-document-primer

When refinement surfaces new vocabulary (Phase 5b), meta-document-primer is invoked in `extend-and-write` mode on the named primer. The skill itself produces only the proposal; meta-document-primer owns the write.

### multi-source-synthesis

When refinement pushes a cluster pattern over threshold (Phase 5d), multi-source-synthesis is invoked. This skill never promotes patterns directly; it surfaces the math and hands off.

### plain-language-translation

If the operator wants the refinement section in a sister `-plain.md` file (rare — the refinement is already meant to be plain), they can invoke plain-language-translation on the refined artifact. Not the skill's job to invoke it automatically.

### synthesis-readiness-scan

After refinement surfaces new sources via Phase 5a and those get ingested, the operator can manually invoke synthesis-readiness-scan to see if any cluster has crossed threshold. Not auto-invoked from this skill.

---

## Output contract

Every refinement pass produces exactly these artifacts:

1. **Refinement output** — either an appended section, inline edits + a slimmed appended section, or a sister file (per mode).
2. **Frontmatter update on the original** — `perplexity-refined`, `perplexity-refined-by`, `perplexity-refinement-depth` fields added.
3. **Execution-log entry** — appended to the active execution log per the standing memory.
4. **Terse completion report in chat** — per `feedback_terse_completion_reports.md`:
   - Number of claims validated / updated / contradicted
   - Top 3 new sources surfaced
   - Recommendations for follow-up actions (which Phase-5 items the operator should pick)

The completion report uses bullets, not paragraphs. It does not restate the refinement content — the operator can read the file.

---

## Source-attribution discipline

This is the single load-bearing rule that makes Perplexity refinement worth the cost. Every claim that lands in the refinement output cites the Perplexity-surfaced URL that backs it. No claim makes it back without a citation.

Citation format inside the refinement section:

```
[source: perplexity.ai query "<query text>" on YYYY-MM-DD, citing <URL>]
```

For multi-source claims:

```
[source: perplexity.ai query "<query text>" on YYYY-MM-DD, citing <URL 1>, <URL 2>, <URL 3>]
```

If Perplexity surfaces a paywalled source, cite it but note the paywall: `[source: perplexity.ai query "..." on 2026-05-27, citing <URL> (paywalled)]`.

If Perplexity's answer is missing citations for a specific claim, do not include the claim in the refinement output. Perplexity sometimes hallucinates in the prose around its citations; the citations are the trust anchor, the prose isn't.

---

## Vault stewardship

Per [[vault-stewardship-principles]]:

1. **Check folder structure before writing.** Refinement sections go inside the original artifact's file. Sister files go in the same folder as the original. Don't create new top-level folders for refinements.

2. **Update `_README.md` only if a new sub-pattern is introduced.** A single sister file in a folder doesn't trigger README updates. If sister-file refinements become a folder pattern (3+ in the same folder), propose updating that folder's `_README.md` to mention the convention.

3. **Slug-only wikilinks.** When the refinement section links back to other vault notes, use `[[slug]]` not `[[path/slug]]`. Per `conventions.md`.

4. **Non-destructive on existing content.** Append mode default. Inline edits per-claim confirmed. Sister files leave the original untouched. Never silent overwrites.

---

## Verification before declaring done

Before reporting completion to the operator:

1. **Frontmatter check** — the original artifact's frontmatter has the three new fields (`perplexity-refined`, `perplexity-refined-by`, `perplexity-refinement-depth`) and valid YAML.

2. **Citation check** — every claim in the refinement output has a `[source: perplexity.ai ...]` citation. Grep for sentences claiming facts without a trailing source tag.

3. **Wikilink check** — wikilinks resolve (slug-only form).

4. **Plain-language check** — the refinement section reads in plain language. Pick the densest paragraph and confirm.

5. **Stop-condition check** — every phase's stop condition was hit (operator confirmed before the next phase ran).

6. **Cap check** — total queries run is at or under the depth's cap. If over, the operator approved the override.

---

## Reporting back to the operator

Terse completion summary (per `feedback_terse_completion_reports.md`):

- Refinement written to `<path>` in `<mode>` mode at `<depth>` depth.
- N queries run. X validated. Y updated. Z contradicted.
- Top 3 new sources surfaced (one bullet each, with URL).
- Top 3 recommended follow-ups (one bullet each, with the Phase-5 sub-step they belong to).
- Any blocked questions or rate-limit events.

No restating of the refinement content. The file is the artifact; the chat is the receipt.

---

## Out of scope (v1.0)

These are explicit non-goals for the v1 build:

- **Auto-refinement on a schedule.** No daily/weekly cron job that runs perplexity-refinement across the vault. Manual invocation is enough.
- **Multi-LLM refinement.** No parallel queries to ChatGPT + Claude + Gemini. Perplexity-only since that's where the new subscription is.
- **Non-vault content.** No refining PDFs, external docs, or chat-pasted text that isn't a vault file.
- **Recursive refinement.** A refinement section doesn't get re-refined. If the artifact needs a second pass later, the operator re-invokes the skill with a higher depth or a fresh focus area.

---

## Reference files

When you need them, read these:

- `~/workspace/skills/perplexity-refinement/references/query-templates.md` — the six query template shapes with worked examples
- `~/workspace/skills/perplexity-shared/references/perplexity-browser-setup.md` — pre-query browser checks (sourced from Phase 2a)
- `~/workspace/skills/perplexity-shared/references/perplexity-cost-rules.md` — suite-wide cost-management rules
- `~/workspace/skills/perplexity-shared/references/perplexity-query-templates-index.md` — index of every suite skill's query templates
- `~/workspace/skills/perplexity-research-suite/SKILL.md` — the router that lists this skill and dispatches into it
- `~/workspace/second-brain/_meta/plain-language-conventions.md` — voice rules
- `~/workspace/second-brain/_meta/conventions.md` — KOS naming and frontmatter
- `~/workspace/skills/vis-extraction/SKILL.md` — sibling skill for sources entering the vault
- `~/workspace/skills/service-seo-research/SKILL.md` — sibling skill for service briefs
- `~/workspace/skills/meta-document-primer/SKILL.md` — companion for primer extensions

---

## Maintenance notes

### M1: Perplexity Pro UI changes (added 2026-05-27, v1.0)

**The issue:** Perplexity's web UI (toggle for Pro Search, account indicator placement, source list rendering) changes over time. The Phase 2a browser-setup instructions assume the late-May-2026 UI.

**How it surfaces:** `mcp__Claude_in_Chrome__get_page_text` returns content that doesn't match the expected structure, or Pro Search can't be confirmed enabled.

**How to fix:** Surface the mismatch to the operator. Ask for a fresh screenshot of the current UI. Update Phase 2a's setup steps to match. Don't fake the Pro-status confirmation.

### M2: Rate-limit surprises (added 2026-05-27, v1.0)

**The issue:** Pro Search is capped at roughly 200 queries per rolling 7-day window on the $20/mo plan — not unlimited, despite the published marketing language sometimes implying so. A `deep` pass (15 queries) is ~7.5% of weekly budget; back-to-back deep runs can hit the cap. Short-burst rate limits also apply (5-10 fast back-to-back queries can trigger a slowdown banner).

**How it surfaces:** Perplexity returns a slowdown banner, a captcha, or "you've hit a usage limit, slow down." Or the weekly tally surfaced by `perplexity-research-suite` is approaching 180+.

**How to fix:** Pause the run. Surface to operator. Default to resuming with longer between-query waits. For weekly-cap hits, defer to the next 7-day window or route through Sonar API if the work is scheduled-scan-shaped. If the rate limit hardens further, lower the per-invocation caps here and in the shared cost-rules file.

### M3: Hallucinated prose around real citations (added 2026-05-27, v1.0)

**The issue:** Perplexity's answer prose can over-summarize, mis-attribute, or hallucinate claims that *look* cited but actually aren't backed by the listed sources.

**How it surfaces:** A claim in the refinement output reads confidently but, on inspection of the cited URL, the source doesn't actually say what Perplexity claims.

**How to fix:** When transcribing claims for the refinement output, prefer the source's wording over Perplexity's paraphrase. For high-stakes claims (Phase-3 bucket 3c contradictions), the operator should spot-check the cited URL before any inline-merge edit lands.

---

## How to add a new maintenance note

When the skill errors or produces a miss in production, add a new entry: **Issue → How it surfaces → How to fix → Why it wasn't designed away.** Date-stamp the entry. Future-Claude learns from past misses without re-hitting the same wall.

---

## See also

- `[[vis-extraction]]` — the source-ingestion skill this refinement skill optionally extends
- `[[service-seo-research]]` — the service-brief skill this refinement skill optionally extends
- `[[meta-document-primer]]` — primer-extension companion
- `[[multi-source-synthesis]]` — synthesis companion
- `[[plain-language-translation]]` — voice retroactive-translation skill
- `[[plain-language-conventions]]` — voice rules
- `[[conventions]]` — KOS naming and frontmatter rules
- `[[primer|seo/primer]]` — SEO operational primer (Section E names this skill as part of the knowledge-growth ecosystem)
- `[[perplexity-research-suite]]` — the router skill that lists this one and dispatches into it
- `[[perplexity-browser-setup]]` — shared pre-query browser checks
- `[[perplexity-cost-rules]]` — shared cost rules across the whole suite
