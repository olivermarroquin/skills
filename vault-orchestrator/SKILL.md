---
name: vault-orchestrator
description: Two-mode orchestrator skill that sits above `multi-chat-coordination` and `master-tracker-aggregator`. Reads the entire vault state — master tracker (including the aggregator's generated rollup section), per-project `_chat-tracker.md` + `_chat-status.md` digests, hot decisions, scheduled tasks, `03_domains/` knowledge surfaces, recently-closed chats, and execution-log activity — and produces operator-facing decision support. **Mode 1 (SURVEY):** plain-language state-of-the-vault report with nine ordered sections (in-flight / ready / queued / open decisions / scheduled / recent wins / domain signals / stale signals / cross-project signals). **Mode 2 (NEXT-MOVES):** composes with multi-chat-coordination's NEXT-MOVE ranking, then layers session-budget totals (neutral, no editorializing), parallel-work detection (disjoint file sets), serial-blocked detection (high-leverage unblockers), per-candidate substrate recommendation (Claude Code / Cowork / either) per the working-surfaces convention, decision-research convention on ranking ties or priority conflicts, and a recommended session plan capped at 8 hours. Both modes auto-invoke `output-quality-loop` on their report artifacts. Read-only on vault content; reports are operator-facing chat output by default, optionally persisted to disk. Phase 3 of the vault-orchestrator project (2026-06-01). Trigger phrases include "run vault-orchestrator," "survey the vault," "state of the vault," "what's the state of play," "give me the vault rollup," "what should I work on next," "what should I spawn next," "rank my next moves," "next-moves recommendation," "session plan for tonight," "give me the spawnable list," "what's the highest-leverage move right now."
---

# Vault Orchestrator (v1)

The hierarchical orchestration layer above `multi-chat-coordination`. Oliver's "vault chief of staff" — the role that today lives in Oliver's head plus the master `_active-chats-tracker.md`. The orchestrator surveys every part of the vault, surfaces what's happening, and ranks what's most valuable to work on next. It does not replace operator judgment. It removes the bottleneck where every "what's the state of play?" or "what should I spawn next?" question requires the operator to mentally walk every project and domain.

The skill exists because the system has grown past one-tracker-can-hold-it-all. 11 projects, 10+ domains, dozens of in-flight + queued chats, scheduled tasks, hot decisions, recently-closed work, unsynthesized sources accumulating in `03_domains/`. Without an aggregating layer, every NEXT-MOVE question routes through Oliver tracking everything manually. This skill is that layer.

The skill is **read-only on vault content**. It never edits per-project files, never edits the master tracker outside the aggregator's marker block (which the aggregator owns, not this skill), never writes a digest. Its outputs are reports — plain-language markdown the operator reads in chat or persists to disk on request. Phase 4 (PROVISION) will add the handoff-drafting + spawn-queue layer; Phase 3 stops short of any spawning.

## When to trigger

### Mode 1 — SURVEY (state-of-the-vault report)

Direct triggers for a full vault-wide state report:

- "Run vault-orchestrator"
- "Survey the vault"
- "State of the vault"
- "Give me the vault rollup"
- "What's the state of play across everything?"
- "Walk me through what's happening"

Indirect triggers — when the operator opens a chat after a long gap, after a busy spell, or before a planning session:

- "I haven't checked in for a few days — what's the picture?"
- "Bring me up to speed on every active project"
- "I'm about to plan tomorrow — what should I know?"

### Mode 2 — NEXT-MOVES (ranked spawnable work + session plan)

Direct triggers for ranking spawnable work plus producing a session plan:

- "What should I spawn next?"
- "What should I work on next?"
- "Rank my next moves"
- "Next-moves recommendation"
- "Session plan for tonight"
- "Give me the spawnable list"
- "What's the highest-leverage move right now?"

Indirect triggers — when the operator finishes a chat or names a time budget:

- "I have 2 hours — what should I run?"
- "Just shipped X. What now?"
- "Pick my next chat for me"

## Core operating principles

These hold across both modes. Read them before invoking either.

**Read-only on vault content.** The orchestrator never edits per-project files, never edits handoff frontmatter, never writes a digest, never edits the master tracker outside the aggregator's marker block (which belongs to the `master-tracker-aggregator` skill, not this one). The orchestrator produces reports. The operator decides what to do with them. Phase 4 adds PROVISION — drafting handoffs + a spawn queue — but that's a separate mode in a separate phase. Don't blur the line here.

**Compose, do not reimplement.** NEXT-MOVES composes with `multi-chat-coordination` NEXT-MOVE mode to get the initial leverage ranking, then layers session-budget display + parallel-work detection + serial-blocked detection + substrate recommendation + decision-research convention on top. SURVEY reads what `master-tracker-aggregator` has already rolled up rather than re-walking every digest. Don't duplicate logic that already lives in dependencies — see `references/composition-with-multi-chat-coordination.md` for the contract.

**Plain language in every output.** Per `~/workspace/second-brain/_meta/plain-language-conventions.md` and the standing `feedback_plain_language_default.md` memory. SURVEY reads aloud as plain prose paragraphs, not bullet walls. NEXT-MOVES per-row reasoning is conversational. Jargon (like "leverage," "operator-fatigue heuristic," "spec-routing coverage") is glossed inline on first use. No executive summaries the operator didn't ask for. See `references/plain-language-discipline.md` for orchestrator-specific examples.

**Operator judgment owns the decisions.** Ranking is a recommendation, not a verdict. Session-budget totals are presented neutrally — never "you should take only the top two" or "this is too much for one day." The operator decides. The skill's job is to surface options with reasoning so the decision is well-informed. If the operator picks something other than rank 1, treat it as a calibration signal, not a mistake.

**Honest gap surfacing over silent skip.** When the aggregator's generated section names projects without digests, SURVEY surfaces them as gaps. When NEXT-MOVES can't find prereqs for a candidate, it names the unknown rather than guessing. When domain folders show 4 unsynthesized sources, SURVEY names them. The orchestrator's value is partly in showing what's missing — if it silently skips gaps, it stops being trustworthy.

**Decision-research convention fires on hard ranking calls.** When NEXT-MOVES has two candidates tied on leverage, or a candidate appears to conflict with stated priorities, or a substrate recommendation is genuinely ambiguous, the orchestrator runs the five-step decision-research convention (see `~/workspace/second-brain/_meta/decision-research-conventions.md`) inline and writes the call into the report. See `references/decision-research-composition.md`.

**Substrate-agnostic by design.** The orchestrator's output is plain markdown that any execution surface can consume — Claude Code, Cowork, the future mission-control-dashboard, a Hermes-based harness, an Agent SDK sub-agent. Every decision lives in the skill markdown. Every state lives in the vault. No proprietary state stores, no API-coupled logic. The orchestrator's NEXT-MOVES report becomes a system prompt + first message for any future spawned-agent system. Don't break that.

**8-hour session-plan cap.** The recommended session plan in NEXT-MOVES never exceeds 8 hours of work. If the top candidates total more than 8 hours, the plan picks the highest-leverage subset that fits and explicitly says so. The cap exists to keep operator-fatigue honest — see `references/session-budget-display.md`.

**YAML safety on any frontmatter writes.** If the operator asks SURVEY or NEXT-MOVES to persist its report to disk, the report gets standard knowledge-os frontmatter (`type: report`, `status: draft`, `created`, `updated`, `tags`) with single-quote-wrapped values for any free-form prose fields. The regex-extractor YAML check runs after the write. This skill does not write to the master tracker, ever.

**Check folder structure before writing.** Per the standing `feedback_check_folder_structure_before_writing.md` memory. If the operator asks for the SURVEY or NEXT-MOVES report to be persisted, write to `~/workspace/second-brain/_meta/handoffs/vault-orchestrator/runs/<YYYY-MM-DD-mode>.md` after `ls`ing the parent and creating `runs/` if absent. The reports are not vault-saved by default.

## Mode 1 — SURVEY

### What SURVEY produces

A plain-language state-of-the-vault report with nine ordered sections. Each section is H2, followed by plain prose paragraphs. The report reads top-to-bottom like a colleague walking the operator through what's happening — not a dashboard, not a wall of bullets.

Section order (mandatory):

1. **What's actively in flight** — every Active/in-flight row across master tracker + per-project trackers, with plain-language descriptions
2. **What's ready to work on next** — every Ready-to-spawn row, with leverage signal and any operator-paused notes
3. **What's queued and why** — Tier 2 + Tier 3 grouped by trigger condition
4. **Open decisions sitting on the operator** — from master tracker's Hot decisions section
5. **What's coming up automatically** — scheduled tasks with fire dates
6. **Recent wins (past 7 days)** — chats closed, artifacts shipped, key outcomes
7. **Domain signals** — `03_domains/` folders with new sources not yet synthesized, lessons not yet promoted, patterns at 3+ observations awaiting promotion
8. **Stale signals** — per-project `_chat-status.md` files >14 days old (from aggregator drift-detect)
9. **Cross-project signals** — handoffs that affect multiple projects, conventions changes pending rollout, etc.

Detailed shape, minimum-content discipline, and section-level examples live in `references/survey-section-shapes.md`.

### SURVEY step-by-step

**Step 1 — Read the master tracker.**

Read `~/workspace/second-brain/_meta/handoffs/_active-chats-tracker.md` end-to-end. Capture:

- Frontmatter `last-change:` (so the report can name when the tracker was last touched)
- The aggregator's generated rollup section between `<!-- AGGREGATOR:BEGIN -->` and `<!-- AGGREGATOR:END -->` (the per-project digests already rolled up)
- Every row in "Active / in-flight chats"
- Every row in "Ready to spawn next"
- Every row in "Queued — Tier 2" and "Queued — Tier 3"
- The "Hot decisions sitting on Oliver's plate" list
- The "Scheduled Cowork tasks" table
- The "Recently closed chats" section (filter to past 7 days for Section 6)
- Section row counts (for the section-level "N chats" framing)

If the aggregator section is missing or malformed, surface it as a gap in Section 9 and read the per-project digests directly as a fallback.

**Step 2 — Walk per-project trackers and digests.**

For each project under `04_projects/clients/_active/` and `04_projects/personal/`:

- Read `_chat-status.md` if present (machine-readable digest) — this is the source of `current-focus`, `last-closed-summary`, `blockers`, `metrics`, `spawn-recommendations` per the digest spec
- Spot-check `_chat-tracker.md` if present (human-readable) — used only to confirm aggregator counts when in doubt; the aggregator already parsed digests, so prefer aggregator output

Projects without a digest get surfaced in Section 8 (stale signals) with the standard suggested action — same logic as the aggregator.

**Step 3 — Walk `03_domains/` for signal-mining.**

For each domain under `03_domains/`:

- Check `insights/` for new `source-YYYY-MM-DD-*.md` files dated within the past 14 days that don't yet appear in any `cluster-synthesis-*.md` (unsynthesized sources)
- Check `lessons/` (if present) for `lesson-*.md` files with `status: draft` or `status: candidate` (unpromoted lessons)
- Check `tactics/` and `tools/` for files with `times-observed: 3+` but `status:` not yet `promoted` (patterns ready for promotion)

Detailed walking logic + heuristics live in `references/domain-signal-mining.md`. Domain signal rows in Section 7 follow the "N unsynthesized sources in `<domain>`" / "M lessons drafted, not promoted" / "K patterns at 3+ observations" plain-language shape.

**Step 4 — Detect stale signals.**

Re-use the aggregator's drift-detect heuristics (see `~/workspace/skills/master-tracker-aggregator/references/drift-detection-heuristics.md`):

- Digests >14 days old → flag as `stale`
- Digests >28 days old → flag as `very stale`
- Per-project execution log newer than digest → "execution log newer than digest — may have unrecorded ships"
- Project README updated after digest → "README newer than digest — current-focus may have shifted"
- Blocker `expected-clear` date in the past → "blocker past expected clear — verify"
- `in-flight-count > 0` but no execution log activity in past 7 days → "claimed in-flight work has no recent log activity"

Surface in Section 8 grouped by verdict (very-stale first, then stale, then heuristic-only annotations on fresh digests).

**Step 5 — Detect cross-project signals.**

Walk the master tracker plus `_meta/conventions.md`, `_meta/handoffs/<project>/_README.md` for each project, and any `_meta/decisions/` files modified in the past 7 days. Look for:

- Handoffs that name multiple projects in their `purpose:` or `tags:` (e.g., a handoff that affects both EV Electric and S&H Contracting)
- Convention changes in `_meta/conventions.md` (frontmatter `updated:` in past 7 days) that imply rollout work across projects
- Pattern promotions in `05_shared-intelligence/patterns/` (status `promoted` in past 7 days) that imply downstream application work
- Recently-closed chats whose outcome names a downstream effect on a different project

Surface in Section 9 with plain-language descriptions of what the cross-project effect is.

Detailed detection logic in `references/cross-project-signal-detection.md`.

**Step 6 — Render the report.**

Render in the nine-section order above. Voice rules:

- H2 headings stay as named in the section list (don't rename for cuteness)
- Each section opens with a one-sentence framing of what's in it
- Plain prose paragraphs, not bullet walls — bullets are fine for lists of rows but the synthesis inside each section is prose
- Plain-language gloss on first use of any term (e.g., "leverage" → "how much downstream work this would unblock")
- Wikilinks preserved exactly per knowledge-os conventions
- Zero invented data — every claim points to a source in the vault

Section-level shape + minimum content rules in `references/survey-section-shapes.md`.

**Step 7 — Emit the report.**

Default: emit the report as chat output. The operator reads it inline.

If the operator says "save the survey" or "persist this", write to `~/workspace/second-brain/_meta/handoffs/vault-orchestrator/runs/<YYYY-MM-DD-survey>.md` after `ls`ing the parent and creating `runs/` if absent. Use minimal frontmatter (`type: report`, `status: draft`, `created: <today>`, `updated: <today>`, `tags: [report, vault-orchestrator, survey]`). Free-form fields stay single-quote-wrapped.

**Step 8 — Auto-invoke output-quality-loop.**

Per the auto-invoke convention at `~/workspace/skills/output-quality-loop/references/auto-invoke-convention.md`, emit the standard block at completion — when the report is persisted to disk. When the report is chat-only, the convention's "ephemeral artifacts" exemption applies; skip the block.

The block to emit (verbatim) when the report was written:

````markdown
## Auto-invoke output-quality-loop

This skill produced the following artifact(s):
- `<path to the persisted survey>`

[output-quality-loop:eval] — for each artifact, run output-quality-loop in EVALUATE mode. If PASS, declare the chat done. If NEEDS REVISION or FAIL, ingest the revision prompt as if it were operator input and regenerate the artifact, then re-invoke output-quality-loop. Cap at 3 iterations; on the 3rd FAIL, escalate to the operator with the evaluation report.
````

### SURVEY flags

- `--persist` — write the report to `_meta/handoffs/vault-orchestrator/runs/<YYYY-MM-DD-survey>.md` in addition to chat output.
- `--sections <list>` — render only the named sections (e.g., `--sections 1,2,7` for in-flight + ready + domain signals). Useful for tight check-ins. Default: all 9.
- `--past-days N` — change the "recent wins" window from 7 days to N (Section 6 only).
- `--skip-domain-walk` — skip Section 7 entirely. Useful when the walk is expensive and the operator only wants project state.
- `--dry-run` — produce the report to stdout/chat without persisting even if `--persist` was requested. Used when the operator wants a preview.

### SURVEY worked example

See `examples/first-survey-2026-06-01.md` for the first real-use run against the live vault.

## Mode 2 — NEXT-MOVES

### What NEXT-MOVES produces

A ranked, reasoned list of spawnable candidates plus a recommended session plan. Output shape:

1. **Header.** Tracker last-change, in-flight count, candidate count, the priority memories being read from (so the operator can flag staleness).
2. **Ranked candidates.** Numbered list, each row with one-line summary + per-candidate reasoning paragraph + effort estimate + unblocks list + substrate recommendation + risks + leverage score / signal (high / medium / low).
3. **Session-budget totals.** Sum of estimated hours across the top N candidates, presented neutrally. E.g., "Top 4 candidates total ~12 hours. Top 2 total ~6 hours." No editorializing.
4. **Parallel-work opportunities.** Pairs of candidates that touch disjoint file sets — flagged as runnable concurrently in two Claude Code sub-agents or two Cowork windows.
5. **Serial-blocked candidates.** Candidates whose completion would unblock the most downstream work — flagged as "high-leverage unblockers."
6. **Decision-research calls.** Any ties on leverage or priority conflicts that the orchestrator resolved using the decision-research convention, with the call and reasoning documented inline.
7. **Recommended session plan.** A specific sequence with substrate tags and time estimates, capped at 8 hours. Format: "Take A first (1 hour, low-context-cost, Claude Code), then B (3 hours, ships a milestone, Cowork for judgment calls), skip C and D until tomorrow."

Plain language throughout per `references/plain-language-discipline.md`.

### NEXT-MOVES step-by-step

**Step 1 — Compose with multi-chat-coordination NEXT-MOVE.**

Invoke `multi-chat-coordination` Mode 3 (NEXT-MOVE) to get the initial leverage ranking. That mode already evaluates the six factors (blocker status, calendar gates, file-collision risk, cognitive-load risk, downstream pull, operator-stated priority) — don't reimplement.

The composition contract: NEXT-MOVE returns a ranked list with per-row reasoning. Vault-orchestrator's NEXT-MOVES consumes that list as its starting point. See `references/composition-with-multi-chat-coordination.md` for the exact handoff shape.

If multi-chat-coordination's NEXT-MOVE returns fewer than 2 candidates, the candidate set is the bottleneck — surface that as a finding ("only 1 spawnable candidate today; consider running SURVEY for domain-signal candidates that could promote into the queue") and stop ranking.

**Step 2 — Apply the orchestrator's leverage-scoring overlay.**

The base ranking from multi-chat-coordination is good. The orchestrator adds four signals on top:

- **Unblocks-downstream-count.** Count how many queued handoffs this candidate would unblock. Higher = higher leverage.
- **Time-to-revenue.** Does the candidate ship a client-facing artifact (EV Electric page, S&H deliverable, client-onboarding-automation milestone)? Up-weight per the standing `project_priority_client_seo_traffic` memory.
- **Operator-stated priority.** Re-check priority memories (`project_priority_*` entries) and recent strategic-chat outputs. Up-weight matches.
- **Recency-of-related-work.** If a candidate's domain or project was just touched (execution log in past 48h, recently-closed sibling), the context is hot — up-weight slightly because re-loading context is cheap.

Detailed scoring heuristics in `references/leverage-scoring-heuristics.md`.

Each candidate gets a leverage signal tagged `high`, `medium`, or `low`. Not a numeric score — the qualitative tag is what the operator scans for.

**Step 3 — Compute session-budget totals.**

For each candidate, pull the estimated hours from its handoff (`Estimated build time:` cell or `## Status` block). Sum across:

- Top 2 candidates
- Top 4 candidates
- All ranked candidates

Display the totals as plain-language sentences:

```
Top 2 candidates total ~6 hours.
Top 4 candidates total ~12 hours.
All N spawnable candidates total ~28 hours.
```

**Neutral presentation.** Do not editorialize ("this is too much for one session" / "you should take only the top two"). The session-plan step decides what fits the 8-hour cap; the budget display is a reference, not a recommendation. See `references/session-budget-display.md`.

**Step 4 — Detect parallel-work opportunities.**

For the top N candidates (default N=4), examine each handoff's expected file paths. A handoff names its deliverables and edited files in its prompt body. Build the file-set for each candidate.

A pair of candidates is "parallel-safe" if:

- Their file-sets are disjoint (no overlapping deliverable paths or edited files)
- Neither blocks the other (no prereq relationship)
- Neither writes to the same convention/spec file (so two chats won't race-edit `_meta/conventions.md` or a shared SKILL.md)

Surface each parallel-safe pair as: "Candidates A + B can run concurrently — disjoint file sets (A touches `<paths>`; B touches `<paths>`)." The operator decides whether to actually run them in parallel via two Claude Code sub-agents or two Cowork windows.

If no pairs are parallel-safe, name that explicitly so the operator doesn't assume it's worth trying.

**Step 5 — Detect serial-blocked candidates.**

For each top-N candidate, count how many queued chats name this candidate (or its phase) in their `blocked-by:` field, their handoff body's "Trigger to spawn" text, or the master tracker's "Trigger to spawn" cell.

Candidates with ≥3 downstream chats waiting are flagged "high-leverage unblocker." These are the chats whose ship event unlocks the most parallel work next.

Surface in a dedicated subsection.

**Step 6 — Tag substrate recommendation per candidate.**

For each ranked candidate, name the best substrate per the working-surfaces convention (`~/workspace/second-brain/_meta/working-surfaces.md`):

- **Claude Code** — multi-file edits, parallel sub-agent work, long-running automation, repos that need git workflows, anything that benefits from the Task tool
- **Cowork** — conversational planning, operator-judgment-heavy work, file-presentation-shaped output, browser-driven research with Claude in Chrome, one-off lookups
- **Either** — the work shape is flexible; pick by operator preference / availability

Cite the convention in the rationale. Don't pick from generic memory.

Decision rules in `references/substrate-recommendation-heuristics.md`.

**Step 7 — Run decision-research convention on hard calls.**

Two cases fire the five-step decision-research convention (`~/workspace/second-brain/_meta/decision-research-conventions.md`):

- **Leverage tie.** Two candidates have indistinguishable leverage signals AND comparable session-budget impact. Decide which to recommend first.
- **Priority conflict.** A candidate appears to conflict with current stated priorities (e.g., a client-internal Keelworks experiment ranked above a client-deliverable from the `project_priority_client_seo_traffic` memory).

The convention's five steps (frame / vault-search / external-research-if-thin / synthesize / decide-and-document) run inline. The call lands in the report's "Decision-research calls" section with a one-paragraph rationale.

Detailed composition logic in `references/decision-research-composition.md`.

**Step 8 — Propose a session plan.**

Walk the ranked list top-down. Add candidates to the proposed session in order. Cap at 8 hours total. Annotate each with:

- Estimated hours
- Substrate recommendation
- One-line reasoning ("low-context-cost first to warm up" / "ships a milestone" / "Cowork for judgment calls")

Stop when adding the next candidate would push the total past 8 hours. Skipped candidates land in a "Skip until tomorrow" list with their leverage signals preserved.

Example output:

```
Take A first (1 hour, Claude Code) — low-context-cost, clears the next blocker.
Then B (3 hours, Cowork) — ships a Phase 4 milestone; judgment calls warrant operator presence.
Skip C and D until tomorrow — C is high-leverage but 4-hour-block doesn't fit; D is medium-leverage and isolatable.
```

Plan rules in `references/session-budget-display.md`.

**Step 9 — Render the report.**

Render in the seven-part order above. Voice rules per `references/plain-language-discipline.md`:

- Section headings stay as named
- Per-candidate reasoning is plain prose, not telegraphic bullets
- Substrate recommendation includes a one-line rationale, not just the tag
- Session plan reads as a colleague's recommendation, not a verdict

**Step 10 — Emit the report.**

Default: emit as chat output. The operator reads inline and picks.

If the operator says "save this" or "persist", write to `~/workspace/second-brain/_meta/handoffs/vault-orchestrator/runs/<YYYY-MM-DD-next-moves>.md`. Same frontmatter shape as the persisted survey.

**Step 11 — Auto-invoke output-quality-loop.**

Same convention as SURVEY Step 8. Emit the standard block only when the report was persisted to disk; skip for chat-only output per the ephemeral-artifacts exemption.

### NEXT-MOVES flags

- `--persist` — write the report to `_meta/handoffs/vault-orchestrator/runs/<YYYY-MM-DD-next-moves>.md`.
- `--top-n N` (default 4) — change how many candidates are examined for parallel-work + serial-blocked detection + session-budget totals.
- `--session-budget H` (default 8) — override the session-plan cap.
- `--substrate cowork|claude-code` — bias the substrate recommendation toward the named surface. Useful when the operator already knows where they're working.
- `--skip-decision-research` — skip the decision-research convention on ties. Falls back to "ranking left as-is; operator decides."
- `--dry-run` — produce the report without persisting even if `--persist` was requested.

### NEXT-MOVES worked example

See `examples/first-next-moves-2026-06-01.md` for the first real-use run against the live vault.

## Composition with master-tracker-aggregator

The aggregator is the bottom-up data layer; the orchestrator is the top-down decision layer. The contract:

- SURVEY reads the aggregator's generated rollup section (between markers) as the authoritative roll-up of per-project state. It does not re-walk every digest from scratch unless the aggregator section is missing/malformed.
- SURVEY's Section 8 (stale signals) reuses the aggregator's drift-detect heuristics rather than reimplementing them. If `master-tracker-aggregator` DRIFT-DETECT has been run recently, the orchestrator may surface its findings; if not, the orchestrator runs the same heuristics in-skill.
- NEXT-MOVES uses the aggregator's per-project rollup blocks to know each project's `current-focus`, `blockers`, and `spawn-recommendations` without parsing digests directly.

When the aggregator has not been run recently (no `Generated: <date>` line in the marker block, or the generated date is >7 days old), SURVEY recommends running it in the report's Section 9 ("cross-project signals") rather than silently using stale data.

## Composition with multi-chat-coordination

The orchestrator composes — does not duplicate — multi-chat-coordination's three modes:

- **NEXT-MOVE composition.** NEXT-MOVES invokes multi-chat-coordination NEXT-MOVE to get the base leverage ranking. The orchestrator's overlays (session-budget totals, parallel-work detection, substrate tagging, decision-research) sit on top.
- **AUDIT composition.** SURVEY's Section 8 (stale signals) can optionally call multi-chat-coordination AUDIT for deeper drift findings. By default it uses the lighter aggregator drift-detect.
- **DECOMPOSE composition.** Out of scope for Phase 3. Phase 4 (PROVISION) composes with DECOMPOSE to draft handoffs.

When invoking a composed mode, the orchestrator reads its output and incorporates it into its own report; it does not re-emit the composed mode's own report verbatim.

See `references/composition-with-multi-chat-coordination.md` for the exact handoff shapes.

## Composition with output-quality-loop

Per the auto-invoke convention. SURVEY and NEXT-MOVES reports are artifacts when persisted. Emit the standard `## Auto-invoke output-quality-loop` block at the end of any invocation that wrote a report to disk. Chat-only output skips the block per the ephemeral-artifacts exemption.

The block contract is documented in detail in this skill's `references/plain-language-discipline.md` Section 5 (the convention applies, but the report's plain-language compliance is what the quality loop most often flags).

## Composition with intel-routing

The orchestrator's SURVEY Section 7 (domain signals) overlaps with `intel-routing` BOOTSTRAP/PUSH/PULL inputs. The contract:

- SURVEY surfaces "X has N keeps unrouted" / "Y has M unsynthesized sources" as signals.
- The operator decides whether to spawn an intel-routing pass.
- NEXT-MOVES may rank an intel-routing pass as a spawnable candidate if the volume crosses a threshold (e.g., >20 keeps unrouted in a single inbox).

Don't auto-route intel from the orchestrator. PUSH/PULL/BOOTSTRAP belong to the intel-routing skill; the orchestrator surfaces the signal.

## Composition with vis-extraction and multi-source-synthesis

SURVEY Section 7 surfaces unsynthesized source counts. NEXT-MOVES may rank a synthesis pass as a candidate if a domain has 3+ unsynthesized sources sharing a theme. Don't auto-extract or auto-synthesize from the orchestrator. Both skills belong in their own invocation.

## Composition with the working-surfaces convention

Substrate recommendation is mandatory on every NEXT-MOVES candidate. Cite the convention at `~/workspace/second-brain/_meta/working-surfaces.md` § "Default routing" in the per-candidate rationale. Generic memory ("Cowork is conversational") is not a substitute for the explicit routing guidance. See `references/substrate-recommendation-heuristics.md`.

## Out of scope (v1)

- **PROVISION mode.** Drafting handoffs and writing a `_spawn-queue.md` lives in Phase 4. Phase 3 reads-and-reports only.
- **Per-project orchestrator decomposition.** Splitting the monolithic orchestrator into project-surveyor + project-analyst + project-decider sub-skills lives in Phase 5.
- **Skill-needs analyzer.** Detecting "this work needs a skill that doesn't exist" patterns lives in Phase 6.
- **Auto-spawn.** Phase 3 produces reports; the operator decides what to spawn. Cowork has no chat-creation API today.
- **Real-time vault watching.** The orchestrator runs on operator invocation, not on file change.
- **Editing the master tracker outside the aggregator's marker block.** That section belongs to `master-tracker-aggregator`, not this skill.
- **Editing per-project digests or trackers.** Read-only on per-project files.
- **Cross-vault federation.** Single vault (`~/workspace/second-brain/`). Tier-3 vault is air-gapped by design.
- **Domain-level per-domain trackers.** Domains stay SURVEY-only — read folder listings + frontmatter freshness signals, don't expect a per-domain tracker.

## Verification before declaring done

Before the chat declares "SURVEY complete" or "NEXT-MOVES complete":

1. Every section listed in the mode's output contract is present (9 sections for SURVEY; 7 parts for NEXT-MOVES).
2. Every per-candidate row in NEXT-MOVES has a substrate recommendation with a one-line rationale.
3. Session-budget totals are computed and displayed neutrally (no editorializing about what the operator should pick).
4. Recommended session plan respects the 8-hour cap (or names the cap explicitly if overridden via `--session-budget`).
5. Any decision-research convention calls are documented inline with their rationale.
6. Plain-language compliance — no jargon-density walls, no executive summary unless requested, glossed terms on first use.
7. If `--persist` was used, the file exists on disk with valid frontmatter and YAML parses.
8. If the report was persisted, the auto-invoke `output-quality-loop` block is emitted.
9. The opening-protocol row move (if running inside a handoff-spawned chat) is honored — the orchestrator does not edit the tracker outside the aggregator marker; if the host chat's row needs updating, the host chat does it.

## Maintenance notes (for future skill iterations)

These observations seed at skill creation. Promote to standalone notes if they generalize.

**1. Watch for aggregator-section drift.** SURVEY reads the aggregator's generated rollup. If the aggregator's marker conventions change (block layout, section names), SURVEY's parsing logic needs updating. Detection: if the rollup section doesn't contain "Vault-wide rollup" or "Per-project digests" headings, surface as a finding.

**2. Watch for substrate-routing-table drift.** Substrate recommendations cite the working-surfaces convention's "Default routing" table. If that table evolves (new surface added, surface deprecated), update the substrate-recommendation reference. Detection: if a candidate's work shape doesn't map to any row in the table, surface as "substrate ambiguous — operator decides."

**3. Watch for priority-memory staleness.** NEXT-MOVES reads `project_priority_*` memories. If a memory becomes stale (priority shifted, project closed), recommendations skew wrong. Detection: at the start of every NEXT-MOVES run, surface the priority memories the orchestrator read so the operator can flag staleness.

**4. Watch for session-budget calibration.** 8-hour cap reflects today's operator tempo. If the operator regularly overrides (`--session-budget 4` for tight sessions, `--session-budget 12` for marathon days), the default may need adjustment. Detection: log override values in a maintenance note over time.

**5. Watch for domain-signal-mining drift.** SURVEY's Section 7 walks `03_domains/` for unsynthesized sources + unpromoted patterns. If the domain folder layout changes (new subfolders, renamed `insights/` → `sources/`), the walking logic needs updating. Detection: if Section 7 returns zero signals across all domains, spot-check the folder structure rather than assuming the vault is quiet.

**6. Watch for plain-language drift in reports.** If reports start reading dense or padded, the skill prompt needs calibration. Detection: output-quality-loop's plain-language compliance check surfaces this on every persisted report.

**7. Watch for cross-project-signal detection gaps.** Section 9 surfaces convention changes, multi-project handoffs, and downstream pattern-promotion effects. If a known cross-project event slips through (e.g., a convention change rolled out without SURVEY catching it), update the detection heuristics in `references/cross-project-signal-detection.md`.

## Related

- `~/workspace/skills/multi-chat-coordination/SKILL.md` — composes with this; provides the base NEXT-MOVE leverage ranking
- `~/workspace/skills/master-tracker-aggregator/SKILL.md` — composes with this; provides the per-project rollup SURVEY reads
- `~/workspace/skills/output-quality-loop/SKILL.md` — auto-invoke target for persisted reports
- `~/workspace/skills/output-quality-loop/references/auto-invoke-convention.md` — the block shape this skill emits when persisting
- `~/workspace/second-brain/_meta/handoffs/_active-chats-tracker.md` — the master tracker SURVEY reads end-to-end
- `~/workspace/second-brain/_meta/handoffs/vault-orchestrator/_README.md` — the project that produced this skill
- `~/workspace/second-brain/_meta/handoffs/vault-orchestrator/phase-3-orchestrator-v1-survey-and-next-moves.md` — the handoff this skill executes
- `~/workspace/second-brain/_meta/working-surfaces.md` — substrate-recommendation source of truth
- `~/workspace/second-brain/_meta/decision-research-conventions.md` — five-step convention NEXT-MOVES invokes on hard calls
- `~/workspace/second-brain/_meta/plain-language-conventions.md` — voice rules every report follows
- `./references/survey-section-shapes.md` — section-by-section shape + minimum-content discipline for SURVEY
- `./references/leverage-scoring-heuristics.md` — how NEXT-MOVES scores leverage
- `./references/session-budget-display.md` — neutral session-budget display rules + 8-hour session-plan cap
- `./references/substrate-recommendation-heuristics.md` — Claude Code / Cowork / either tagging rules
- `./references/domain-signal-mining.md` — how SURVEY walks `03_domains/` for unsynthesized sources + unpromoted patterns
- `./references/cross-project-signal-detection.md` — how SURVEY detects multi-project handoffs + convention rollouts
- `./references/plain-language-discipline.md` — orchestrator-specific plain-language examples
- `./references/composition-with-multi-chat-coordination.md` — when NEXT-MOVES invokes MCC directly vs reimplements
- `./references/decision-research-composition.md` — when SURVEY + NEXT-MOVES invoke the decision-research convention
- `./examples/first-survey-2026-06-01.md` — first real-use SURVEY run
- `./examples/first-next-moves-2026-06-01.md` — first real-use NEXT-MOVES run
