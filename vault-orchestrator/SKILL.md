---
name: vault-orchestrator
description: Five-mode orchestrator skill that sits above `multi-chat-coordination` and `master-tracker-aggregator`. Reads the entire vault state — master tracker (including the aggregator's generated rollup section), per-project `_chat-tracker.md` + `_chat-status.md` digests, hot decisions, scheduled tasks, `03_domains/` knowledge surfaces, recently-closed chats, execution-log activity, project state files, and the inter-chat event log — and produces operator-facing decision support plus (in Mode 3) drafted handoffs + a substrate-agnostic spawn queue plus (in Mode 6) dispatched sub-agents that produce per-artifact outputs under orchestrator coordination. **Mode 1 (SURVEY):** plain-language state-of-the-vault report with nine ordered sections (in-flight / ready / queued / open decisions / scheduled / recent wins / domain signals / stale signals / cross-project signals). **Mode 2 (NEXT-MOVES):** composes with multi-chat-coordination's NEXT-MOVE ranking, then layers session-budget totals (neutral, no editorializing), parallel-work detection (disjoint file sets), serial-blocked detection (high-leverage unblockers), per-candidate substrate recommendation (Claude Code / Cowork / either) per the working-surfaces convention, decision-research convention on ranking ties or priority conflicts, and a recommended session plan capped at 8 hours. **Mode 3 (PROVISION):** composes with multi-chat-coordination's DECOMPOSE to split a project goal into N drafted handoffs, runs decision-research at every meaningful decomposition decision, tags each drafted handoff with a `preferred-substrate:` field, scans drafted + in-flight + queued handoffs for shared-file conflicts (edit-zone detection), appends substrate-agnostic copy-paste-ready rows to `_meta/handoffs/_spawn-queue.md`, registers the new project at the appropriate tracker tier, integrates the chat-resilience checkpoint reminder into long-running handoffs, ties the operator-fatigue heuristic to queue totals (warns at >10h queued), and produces a plain-language operator summary. **Mode 5 (RESUME):** project-scoped mid-project visibility — reads a named project's state file, execution logs newest-first, per-project chat tracker + digest, the event log delta since the state file's `updated_at`, the master tracker rows naming this project, and the handoff files whose `client:` field matches; produces a six-section plain-language report (project state summary + available next-wave handoffs + cross-project unblockers + decomposition diagram text + stale-state reconciliations + what-I-read audit trail), surfaces every stale-state reconciliation Mode 5 applied (state-file-says-X-but-event-log-says-Y) with operator confirmation prompts, and chains into Mode 3 PROVISION when the operator wants the ready-waves drafted into handoffs. **Mode 6 (EXECUTE):** multi-agent control plane — takes a specific next-wave handoff (Mode-3-PROVISION-drafted or operator-drafted) + dispatches narrowly-scoped per-artifact sub-agents under orchestrator coordination, with substrate-adaptive dispatch (true parallel on Claude Code Task tool; sequential one-shot on Cowork Agent tool; push-driven on future Hermes-harness), inter-agent coordination via the project state file's per-key write isolation, operator-gate routing via a per-project `_pending-operator-decisions.md` file, and parallel-safe coordination via reuse of Phase 4's edit-zone conflict detection over the sub-agent set. Closes the EXECUTION side of v1.1 known-gap-1; with Mode 5 + Mode 6 shipped the v1.2 trio (RESUME → PROVISION → EXECUTE) closes known-gap-1 end-to-end. All five modes auto-invoke `output-quality-loop` on their artifacts EXCEPT Mode 6 (per lesson D-05, the per-sub-agent four-substep loops cover quality at the artifact level; an aggregated wave-close roll-up substitutes). Modes 1, 2, and 5 are read-only on vault content; Mode 3 writes drafted handoffs + queue rows + tracker rows + new project subfolders only after operator approval at a single review gate; Mode 6 writes the project state file (via sub-agents' per-key writes), the gate file, and the dispatch log only after operator approval of the dispatch plan at a single review gate. Phase 3 + Phase 4 + v1.2 Phase 1 + v1.2 Phase 2 of the vault-orchestrator project (2026-06-01 + 2026-06-02 + 2026-06-03). Trigger phrases include "run vault-orchestrator," "survey the vault," "state of the vault," "what's the state of play," "give me the vault rollup," "what should I work on next," "what should I spawn next," "rank my next moves," "next-moves recommendation," "session plan for tonight," "give me the spawnable list," "what's the highest-leverage move right now," "provision <goal>," "draft handoffs for <goal>," "decompose this project into chats," "set up a spawn queue for <goal>," "scaffold this initiative," "resume <project>," "where are we on <project>," "what's next for <project>," "show wave status for <project>," "decompose what's left for <project>," "execute wave-<id> for <project>," "dispatch sub-agents for <wave>," "run wave-<id> through the orchestrator," "fire the next wave for <project>."
---

# Vault Orchestrator (v1.5)

> **v1.5 changelog (2026-06-04)** — Imagery pipeline integrated as a first-class orchestrated wave. Mode 3 PROVISION: added mandatory DECOMPOSE composition rule — any page-build decomposition must include an imagery wave sequenced AFTER content/draft and BEFORE publish, with 5 sub-steps (auto-generate prompts → operator Higgsfield pause → operator variant-selection gate via `_pending-operator-decisions.md` → organize → wire). Publish wave hard-depends on imagery wave OR an explicit operator-approved "publish without images" decision routed through the gate file. Imagery wave inputs (reference photos at `marketing-assets/reference-photos/`, prompts, scripts) flow through the existing Step 3 disk-verify. Mode 6 EXECUTE: added imagery-wave dispatch flow (Phase A prompt-gen parallel → Phase B Higgsfield pause → Phase C variant-selection gate → Phase D organize+wire parallel → Phase E wave-close). Operator-legibility requirement: dispatch plan must surface prompt-gen location, variant-selection gate, image save/wire flow, and per-prompt-type reference-photo requirements without operator asking. **Why:** EV pages 06-12 run Issue #16 — imagery pipeline existed as SOP+scripts but was orchestration-invisible; deferred at PROVISION with no re-entry; prompts hand-authored; no variant-selection gate fired; save/wire flow undiscoverable; almost published with 404 placeholder images (Issue #15). See `execution-log-2026-06-03-core-30-pages-06-12-dataforseo-run.md` Issues #15-#20.

> **v1.4 changelog (2026-06-04)** — Added mandatory disk-verify step to Mode 3 PROVISION (new Step 3, between DECOMPOSE composition and decision-research; all subsequent PROVISION steps renumbered +1, now 12 steps total). PROVISION now `ls`/greps every input artifact each wave consumes before emitting a gap analysis — the "exists vs not found" set is built from disk only, never from the model's assumption. Full consumption chain traced (briefs + data files + scripts + templates), not one layer. Missing inputs default to inserting an upstream authoring wave; hard-reject only when the input genuinely can't be produced in-pipeline. Disk-verified asset-inventory table emitted per wave in the Step 9 review-gate proposal. Producer-side enforcement of `pattern-disk-verify-integration-target-before-drafting`. **Why:** EV pages 06-12 PROVISION (first production run) claimed a non-existent troubleshooting brief existed AND missed McLean/Oakton city data files — both would have broken Wave 2; caught only by manual peer-review. See `execution-log-2026-06-03-core-30-pages-06-12-dataforseo-run.md` Issue #7. Cross-references updated: PROVISION flags, peer-reviewer gate-type registry, calibration watches. Event-log row appended for the version bump.

> **v1.3.1 changelog (2026-06-03)** — Hardened the Mode 6 peer-reviewer graceful-degradation behavior: a skipped peer-reviewer (skill unavailable on substrate) now MUST surface a LOUD operator-visible warning block at the dispatch-plan gate, not just a buried event-log line. **Why:** the prior behavior (skip + log warning to event log only) meant an operator approving a plan mid-run could mistake an un-reviewed plan for a reviewed one — the operator isn't grepping the event log at the gate. The run still does not hard-block (degradation preserved); it just fails loudly instead of quietly. Surfaced during pre-first-run review of the EV/S&H page-build wiring; quiet failure is a bad property for any future unattended run too. Event-log row appended for the version bump.

> **v1.3 changelog (2026-06-03)** — Added peer-reviewer dispatch slot at Mode 6 EXECUTE Step 6/7 single review gate per `gate-peer-reviewer` skill v1.0 ship. Single additive block (~30 lines), no Mode 6 rewrites. Cross-mode integration (Mode 5 RESUME Step 11 + Mode 3 PROVISION Step 9 + Mode 6 Step 10 wave-close + Step 9 conditional sub-agent gates) deferred to v1.1 of gate-peer-reviewer as production calibration data drives expansion. Deliberate evolution per `feedback_check_folder_structure_before_writing` discipline — vault-orchestrator v1.2 had 1 explicit Mode 6 operator-attended gate, not 5; v1.3 honestly reflects this in the integration block + the gate-peer-reviewer registry. Self-applying-spec demonstration documented in gate-peer-reviewer build lesson D-row.

The hierarchical orchestration layer above `multi-chat-coordination`. Oliver's "vault chief of staff" — the role that today lives in Oliver's head plus the master `_active-chats-tracker.md`. The orchestrator surveys every part of the vault, surfaces what's happening, and ranks what's most valuable to work on next. It does not replace operator judgment. It removes the bottleneck where every "what's the state of play?" or "what should I spawn next?" question requires the operator to mentally walk every project and domain.

The skill exists because the system has grown past one-tracker-can-hold-it-all. 11 projects, 10+ domains, dozens of in-flight + queued chats, scheduled tasks, hot decisions, recently-closed work, unsynthesized sources accumulating in `03_domains/`. Without an aggregating layer, every NEXT-MOVE question routes through Oliver tracking everything manually. This skill is that layer.

**Modes 1, 2, and 5 are read-only on vault content.** SURVEY, NEXT-MOVES, and RESUME never edit per-project files, never edit the master tracker outside the aggregator's marker block (which the aggregator owns, not this skill), never write a digest, never mutate state files. Their outputs are reports — plain-language markdown the operator reads in chat or persists to disk on request.

**Mode 3 (PROVISION) writes — but only after operator approval at a single review gate.** PROVISION composes with `multi-chat-coordination` DECOMPOSE to draft handoffs for a proposed initiative, scans them for cross-project edit-zone conflicts, tags each with a preferred substrate, and stages them in a substrate-agnostic `_spawn-queue.md`. No file is written until the operator approves the full decomposition + queue at the review gate. Once approved, PROVISION writes the new project subfolder + `_README.md` + per-phase handoffs + queue rows + master tracker rows atomically. The operator drives every spawn — Mode 3 does not auto-execute any drafted chat.

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

### Mode 3 — PROVISION (draft handoffs + populate spawn queue)

Direct triggers for decomposing a project goal into drafted handoffs and staging them in the spawn queue:

- "Provision <goal>"
- "Draft handoffs for <goal>"
- "Decompose this project into chats"
- "Scaffold this initiative"
- "Set up a spawn queue for <goal>"
- "Plan the chats for <project name>"

Indirect triggers — when the operator names a multi-phase initiative without specifying decomposition:

- "I want to launch <X>. Walk me through what chats this needs."
- "Build me the project structure for <X>."
- "Take this strategic-chat output and turn it into spawnable chats."
- A NEXT-MOVES output chained into PROVISION (operator says "now provision the top candidate" or "draft handoffs for what you just ranked")

### Mode 5 — RESUME (project-scoped mid-project visibility)

Direct triggers for reading a specific project's state + surfacing where it is + which next-wave handoffs are ready:

- "Resume <project>"
- "Where are we on <project>?"
- "What's next for <project>?"
- "Show wave status for <project>"
- "Decompose what's left for <project>"
- "Run RESUME on <project>"

Indirect triggers — when the operator returns to a project after a gap, or asks a project-scoped state question:

- "Pick up <project> from where we left off"
- "What's the state of <project> right now?"
- "Are wave A2 / phase 3 / step N for <project> ready to spawn?"
- A SURVEY output where the operator narrows to one project ("zoom into S&H")

### Mode 6 — EXECUTE (multi-agent dispatch over a named wave)

Direct triggers for dispatching sub-agents to produce a wave's artifacts under orchestrator coordination:

- "Execute wave-<id> for <project>"
- "Dispatch sub-agents for <wave>"
- "Run wave-<id> through the orchestrator"
- "Fire the next wave for <project>"
- "Run EXECUTE on <project> wave-<id>"

Indirect triggers — when a Mode 5 RESUME output names a state-file-ready wave with a handoff present, or when the operator wants the orchestrator to coordinate the dispatch instead of pasting the handoff into a fresh Cowork window:

- "Now execute the ready waves" (chained off a Mode 5 output)
- "Spawn the dispatch plan" (chained off a Mode 5 output)
- "Don't just draft — run wave-<id>"
- A PROVISION output where the operator says "fire the queued handoff via Mode 6 instead of pasting"

## Core operating principles

These hold across both modes. Read them before invoking either.

**Modes 1, 2, and 5 are read-only on vault content.** SURVEY, NEXT-MOVES, and RESUME never edit per-project files, never edit handoff frontmatter, never mutate state files, never write a digest, never edit the master tracker outside the aggregator's marker block (which belongs to the `master-tracker-aggregator` skill, not this one). They produce reports; the operator decides what to do with them.

**Mode 3 writes only after operator approval.** PROVISION drafts handoffs, queue rows, and tracker rows but stages them at a single review gate before any file is written. No drafted handoff is written, no queue row appended, no tracker row added until the operator says "approved" (with or without edits). On approval, PROVISION writes all proposed files atomically — handoff bodies + project `_README.md` + spawn-queue rows + master-tracker rows in one pass — then runs YAML parse checks on every touched file and emits the auto-invoke quality-loop block. The operator-driven spawn step (paste or fire) is always separate from the draft step.

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

### Pre-flight (all modes)

**Before running any mode:** read `~/workspace/second-brain/_meta/_event-log.md` and grep for events since the orchestrator's most-recent prior touch (or last 24 hours if first run of the session). Incorporate any credential landings, handoff status flips, skill version bumps, or pattern promotions into the survey/ranking/provision context. This supplements — does not replace — the master tracker read.

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
- **Cowork** — conversational planning, operator-judgment-heavy work, file-presentation-shaped output, one-off lookups, judgment-gated research where the operator wants to weigh in mid-flight
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

## Mode 3 — PROVISION

### What PROVISION produces

For an operator-provided project goal (or a NEXT-MOVES output chained directly into PROVISION), Mode 3 returns:

1. **A decomposition proposal** — N proposed phase handoffs with dependencies, estimated times, deliverables, and tier classification (Tier 1 ready-to-spawn / Tier 2 same-week queue / Tier 3 explicit-trigger queue)
2. **A disk-verified asset-inventory table** — per-wave enumeration of every input artifact each wave consumes, `ls`/grep-verified on disk, with "exists on disk" or "not found on disk" status and cited paths; every gap maps to an upstream authoring wave
3. **A per-handoff substrate tag** — `preferred-substrate: claude-code | cowork | either` baked into each drafted handoff's frontmatter, plus a one-line rationale in the proposal
4. **A conflict scan** — every drafted handoff's file-set checked against in-flight + queued handoffs' file-sets, with severity scored per [[edit-zone-conflict-detection]]
5. **Decision-research calls** — every meaningful decomposition decision (phase ordering, scope cuts, dependency choices, substrate ambiguity) run through the five-step decision-research convention with the call documented inline in the proposal
6. **Checkpoint reminders** — chat-resilience checkpoint reminder section inserted into each drafted handoff whose estimate crosses 2 hours, per [[checkpoint-integration]]
7. **Spawn-queue rows** — one row per drafted handoff, substrate-agnostic copy-paste-ready prompt, ready to append to `_meta/handoffs/_spawn-queue.md` per [[spawn-queue-shape]]
8. **Master-tracker rows** — proposed rows at the appropriate tier (default Tier 2 for new projects; Tier 1 only when the operator names a phase as ready-to-spawn immediately)
9. **Operator-fatigue check** — sum of all drafted-handoff hours; if the spawn queue would exceed 10 hours total, a warning banner is surfaced and the operator can re-rank, defer, or split before approval
10. **A plain-language operator summary** — "I drafted N handoffs for project X. K conflicts flagged. M ready for Claude Code Task tool, P ready for Cowork paste, Q decisions surfaced for your call before any spawn."

PROVISION surfaces all of this as a **single review gate**. The operator approves the full proposal, edits individual rows, or aborts. No file is written until approval lands.

### When PROVISION fires

The operator triggers PROVISION explicitly (the direct triggers in "When to trigger" above) OR PROVISION is chained from a NEXT-MOVES output when the operator says "now provision the top candidate" / "draft handoffs for what you just ranked." Both entry paths produce the same shape; the chain just supplies the goal automatically.

PROVISION does NOT auto-fire from SURVEY findings. SURVEY surfaces signals; the operator decides whether to provision an initiative around them.

### PROVISION step-by-step

**Step 1 — Receive or gather the project goal.**

Two entry shapes:

- **Operator-provided.** The operator names a goal in plain language: "Build a content calendar generator for EV Electric's blog" / "Launch the Keelworks YouTube channel" / "Stand up the per-client onboarding automation." PROVISION reads the goal, asks 1-2 clarifying questions if underspecified (audience, success criteria, deadlines, prerequisite chats), and proceeds.

- **NEXT-MOVES-chained.** The operator's most recent NEXT-MOVES output named a high-leverage candidate; the operator says "provision that" or "draft handoffs for the top candidate." PROVISION reads the candidate row + its linked handoff (if it exists) + any strategic-context document for the project, then proceeds.

If the goal is genuinely ambiguous (multiple plausible decompositions, no clarifying signal from existing vault docs), PROVISION runs the decision-research convention to lock the goal frame before decomposing. Document the call in the proposal.

**Step 2 — Compose with multi-chat-coordination DECOMPOSE.**

Invoke `multi-chat-coordination` Mode 1 (DECOMPOSE) with the goal. DECOMPOSE returns:

- A proposed kebab-case project slug for the subfolder
- A list of N phase handoffs with one-sentence purpose + deliverable + prereqs + estimated time
- A dependency graph in plain text (indented ASCII)
- A proposed `_README.md` body using the project-subfolder-template
- Proposed full bodies for each generated handoff (frontmatter + prompt body + closing protocol)
- Proposed tracker rows at the appropriate tier

PROVISION consumes DECOMPOSE's output as the starting point. The orchestrator does NOT reimplement DECOMPOSE's logic — sizing rules, dependency analysis, tier classification all belong to multi-chat-coordination. See [[composition-with-multi-chat-coordination]] for the handoff shape (composition contract). Phase 4 extends that document to cover DECOMPOSE composition.

If DECOMPOSE returns a single-unit decomposition (one handoff, no dependencies), PROVISION surfaces the result as "this looks like a single-chat unit — propose `handoff-YYYY-MM-DD-<slug>.md` at the root of `_meta/handoffs/` instead of a project subfolder?" The operator confirms or asks PROVISION to push for a multi-phase decomposition.

**Mandatory DECOMPOSE composition rule — imagery wave (v1.5).** When DECOMPOSE returns a page-build decomposition (any decomposition containing a page-scaffold/draft wave AND a publish wave), PROVISION must verify the decomposition includes an **imagery wave** sequenced AFTER the content/draft wave and BEFORE the publish wave. If DECOMPOSE omits it, PROVISION inserts it. The imagery wave has this fixed shape:

1. **Auto-generate prompts** — `generate-imagery-prompts.py --page-folder <path> --client <slug> --hero-style <style>` per page. Prompts are machine-generated, never hand-authored. Each prompt carries a self-documenting header (Type, Reference photos, Aspect, Produces). The generated `imagery-prompts-log.md` per page is the artifact.
2. **Operator Higgsfield session** — out-of-band; the wave pauses here. The orchestrator writes state with `imagery_wave_status: "paused-higgsfield"` and stops. Resumes on operator's "images are in" message.
3. **Operator variant-selection gate** — an explicit "pick the best variant per slot" operator decision, routed through `_pending-operator-decisions.md` per [[operator-gate-routing]]. The gate row names each page + slot + variant count. The operator responds with variant picks per page per slot.
4. **Organize** — `organize-image-downloads.py` per page per slot, using the operator's variant picks from the gate response.
5. **Wire** — `wire-page-images.py --page-folder <path> --config <config>` per page. Optimizes, uploads to WP Media Library, rewires HTML, optionally republishes.

The imagery wave's **disk-verified inputs** (checked at Step 3) include: reference photos at `04_projects/clients/_active/<client>/marketing-assets/reference-photos/` (per `_meta/conventions.md` § "Client imagery reference assets"), `generate-imagery-prompts.py` script, client config JSON, and the page folders from the draft wave. Step 3's asset-inventory table surfaces these — PROVISION does not need a separate imagery-specific disk check.

The **publish wave must hard-depend on the imagery wave** OR on an explicit operator-approved "publish without images" decision. The "publish without images" decision must be routed through `_pending-operator-decisions.md` — it is never a silent default. The dispatch plan must state the dependency explicitly. No publish proceeds with dangling placeholder image references (per Issue #15 guard from `execution-log-2026-06-03-core-30-pages-06-12-dataforseo-run`).

**Operator-legibility requirement:** the imagery wave's dispatch plan must state, without the operator asking: (a) prompts are auto-generated and where they are written (`<page-folder>/imagery-prompts-log.md`), (b) variant-selection is an operator gate routed through the gate file, (c) where generated images are saved (`<page-folder>/images/`) and how they get wired into the HTML (`wire-page-images.py`), (d) reference photos to upload per prompt type (NONE for PURE SCENE, logo-only for HANDS-ONLY, headshot+logo for AHMAD-CENTRIC — per the types-legend in each generated log).

**Step 3 — Disk-verify the input-consumption chain for every wave.**

DECOMPOSE (Step 2) returns a decomposition with waves, deliverables, and dependencies. Before any decision-research or proposal emission, PROVISION grounds the gap analysis in disk reality — never in the model's assumption about what "obviously exists."

For every wave in the decomposition:

1. **Enumerate every input artifact the wave consumes.** Trace the full consumption chain, not one layer. A page-scaffold wave consumes service data JSON + city data JSON + research briefs + the scaffolder script. A publish wave consumes drafted HTML + imagery assets + the publish script + credentials config. List every artifact at every layer the wave's tools/scripts will read at execution time.

2. **`ls` or grep each enumerated artifact on disk.** Build the "exists on disk vs not found on disk" set from these results only. A file is "exists on disk" if the path resolves; this step does NOT verify the file's content correctness, template version, or schema completeness — those are downstream quality concerns, not input-existence concerns.

3. **Build the disk-verified asset-inventory table.** Every wave gets a table in the proposal with this shape:

   ```
   Wave N — <wave name>
   | Input artifact | Expected path | Disk status | Source |
   |---|---|---|---|
   | vienna-va.json | repos/ai-agency-core/scripts/data/cities/vienna-va.json | ✅ exists | ls |
   | mclean-va.json | repos/ai-agency-core/scripts/data/cities/mclean-va.json | ❌ not found | ls |
   | troubleshooting brief | second-brain/05_shared-intelligence/research-briefs/services/brief-troubleshooting.md | ❌ not found | ls |
   | scaffold-core-30-page.py | repos/ai-agency-core/scripts/scaffold-core-30-page.py | ✅ exists | ls |
   ```

   Every "exists" claim cites the verified path. No claimed-existing input ships unverified.

4. **For every "not found" input, insert an upstream authoring wave that produces it.** This is the constructive default — a missing input triggers a new wave (or extends an existing earlier wave) so the consuming wave's dependencies are satisfied at execution time. Examples: if `mclean-va.json` is not found, an earlier wave must run `scaffold-city-data.py` to produce it; if a service brief is missing, an earlier wave must author it.

5. **Hard-reject the decomposition only when a missing input genuinely cannot be produced in-pipeline** — e.g., the input requires an external system the pipeline has no access to, or producing it would violate a scope constraint the operator set. In that case, surface the gap to the operator at the review gate (Step 9) with the constraint that blocks in-pipeline production, and wait for operator judgment.

6. **Verify wave ordering satisfies the production chain.** Every authoring wave that produces a missing input must be sequenced upstream of (earlier than) the wave that consumes it. If the decomposition's dependency graph doesn't already enforce this ordering, adjust it before proceeding to Step 4 (decision-research).

7. **Emit the asset-inventory summary for the Step 9 review-gate proposal.** Aggregate per-wave tables into a top-level summary block:

   ```
   Disk-verified asset inventory:
   - <N> inputs verified across <M> waves
   - <K> gaps detected → <K> authoring waves inserted (see per-wave tables below)
   - 0 unresolved gaps | <P> unresolvable gaps requiring operator decision
   ```

   The per-wave tables and this summary become part of the Step 9 proposal so the operator sees exactly what PROVISION verified on disk.

This step is the producer-side enforcement of `pattern-disk-verify-integration-target-before-drafting`. The asset-inventory table surfaces disk reality at the review gate — not the model's belief about disk reality.

**Step 4 — Run decision-research at every meaningful decomposition decision.**

DECOMPOSE makes several non-obvious decisions during decomposition. PROVISION's added discipline is to surface those decisions and run the five-step decision-research convention (see [[decision-research-composition]] and `~/workspace/second-brain/_meta/decision-research-conventions.md`) on each one. Typical fire points:

- **Phase ordering.** Two equally-valid orderings (e.g., research-then-build vs build-then-research-during-iteration). Fire the convention; document the call.
- **Scope cuts.** A proposed phase is too large; should it split into 2 phases or merge two adjacent narrow phases? Fire the convention.
- **Dependency choices.** A handoff could depend on either of two upstream handoffs; the choice affects parallelizability. Fire the convention.
- **Substrate ambiguity at draft time.** A drafted handoff's work shape could fit either Claude Code or Cowork; the substrate tag (Step 6) is ambiguous. Fire the convention.
- **Tier classification.** A handoff is borderline Tier 2 vs Tier 3; the trigger condition isn't clearly named. Fire the convention.

Document each call inline in the PROVISION proposal under a "Decision-research calls" subsection. Each call gets: the question, the option set considered, the recommendation, the rationale.

The convention does NOT fire on every choice — only meaningful ones. PROVISION's job is to err toward firing rather than burying decisions; over-firing produces noise but under-firing produces silent drift.

**Step 5 — Scan for cross-project edit-zone conflicts.**

For each drafted handoff, parse its `## Files to edit` and `## Files to create` sections. Build a file-set per drafted handoff. Then run the detection algorithm in [[edit-zone-conflict-detection]]:

- Pairs of (drafted, in-flight) handoffs touching the same shared file → flag with severity (serial-required / parallel-OK-with-note / warning-only / self-conflict)
- Pairs of (drafted, queued) handoffs same → flag
- Pairs of (drafted, drafted) within this PROVISION run → flag (intra-batch conflicts)

For each flagged pair, name the suggested resolution (serialize via queue order, split via handoff refactor, accept-risk via override). The conflict-flag table goes into both the PROVISION proposal AND the spawn-queue's "Conflict flags" section after approval.

Self-conflicts (a drafted handoff that writes to `_spawn-queue.md` or claims to edit the orchestrator's own owned files) are rejected at draft time, not deferred to approval. PROVISION re-drafts or surfaces the contract violation.

**Step 6 — Tag preferred substrate per drafted handoff.**

For each drafted handoff, set `preferred-substrate: claude-code | cowork | either` in its frontmatter. Rules:

- **`claude-code`** — multi-file edits, parallel sub-agent work, long-running autonomous execution, repo-level git workflows, anything that benefits from the Task tool. Default for handoffs estimated >3h with >3 file deliverables and minimal operator gates.
- **`cowork`** — judgment-heavy conversational work, file-presentation-shaped output, operator-attended research, one-off lookups where the operator wants to weigh in mid-flight. Default for handoffs with explicit operator gates or "discussion chat" framing.
- **`either`** — the work shape is flexible; either substrate handles it well. Document why (which factors balance out) in the per-handoff rationale.

Cite the working-surfaces convention's "Default routing" table in the rationale (see [[substrate-recommendation-heuristics]]). Generic memory is not a substitute for the explicit routing table.

The substrate tag is the source of truth for the spawn-queue row's "Substrate rec" cell (see [[spawn-queue-shape]] invariant 4).

**Step 7 — Inject the chat-resilience checkpoint reminder where triggers fire.**

For each drafted handoff, check the checkpoint triggers from [[checkpoint-integration]]:

- Estimated time > 2h, OR
- Deliverable count > 5 files, OR
- Multi-session shape (operator gates, calendar holds, "across sessions"), OR
- Research-heavy shape ("deep research" / "many sources" / "synthesis")

Where any trigger fires, insert the "Chat-resilience checkpoint reminder" section between the work description and the closing protocol per the shape in [[checkpoint-integration]]. Where no triggers fire, skip the reminder (avoid convention-noise).

Record the inclusion/skip decision in the proposal: "Included checkpoint reminder in Phases 2, 3, 4 (each >2h); skipped Phase 1 (45min, single-file)."

**Step 8 — Compute the operator-fatigue check.**

Sum the estimated build times across all drafted handoffs. Add to the current spawn-queue total (the queue may already hold rows from prior PROVISION runs). If the resulting queue total exceeds **10 hours**, surface a warning banner at the top of the proposal:

```
⚠️ Operator-fatigue warning: queued spawn-queue total would reach <Nh> after this PROVISION. The 10-hour ceiling matches the NEXT-MOVES 8-hour session cap plus a context-switch buffer. Re-rank, defer, or split before approval.
```

The warning is advisory — the operator can approve anyway. Do not block approval on this; the operator's judgment owns the decision. The warning also lands at the top of `_spawn-queue.md` "Queued" section after approval if the threshold is crossed.

**Step 9 — Surface the single review gate.**

Present the full proposal to the operator in plain language with this shape:

```
PROVISION PROPOSAL — <today>

Goal: <operator's goal in one sentence>
Proposed subfolder: ~/workspace/second-brain/_meta/handoffs/<project-slug>/
Tier registration: <default Tier 2 unless one Phase is named as ready-to-spawn now>

Dependency graph:
<plain-text indented graph from DECOMPOSE Step 3>

N proposed handoffs:

1. phase-1-<short> — <purpose> (Tier 1, ~Nh, claude-code)
   Prereqs: none
   Deliverable: <what ships>
   Checkpoint reminder: included | skipped
   Conflicts: none | flagged → see conflict table
   Asset inventory: N inputs verified, K gaps → authoring waves inserted | see table

2. phase-2a-<short> — <purpose> (Tier 2, ~Nh, cowork)
   Prereqs: phase-1-<short>
   Deliverable: <what ships>
   Checkpoint reminder: included
   Conflicts: serial-required with "<in-flight chat name>" on `_meta/conventions.md` → see conflict table
   Asset inventory: N inputs verified, K gaps → authoring waves inserted | see table

... (continue for each phase)

Substrate distribution:
- M handoffs prefer claude-code (Task tool path)
- P handoffs prefer cowork (paste path)
- Q handoffs are either

Decision-research calls run:
1. <call 1 question + recommendation + rationale>
2. <call 2 ...>

Conflict-flag table:
| Conflicts with | Shared file | Severity | Suggested resolution |
|---|---|---|---|
| ... | ... | ... | ... |

Disk-verified asset inventory (Step 3):
- <N> inputs verified across <M> waves
- <K> gaps detected → <K> authoring waves inserted (see per-wave tables below)
- 0 unresolved gaps | <P> unresolvable gaps requiring operator decision

<per-wave asset-inventory tables here>

Operator-fatigue check:
Drafted handoff total: <Nh>
Current queue total: <Nh>
Combined: <Nh>
Status: under-ceiling | ⚠️ over-ceiling

Proposed tracker row additions:
- M rows to "Ready to spawn next" (Tier 1)
- P rows to "Queued — Tier 2"
- Q rows to "Queued — Tier 3"

Proposed spawn-queue row additions:
- N rows to "Queued" section of `_meta/handoffs/_spawn-queue.md`

Files I would write (none written yet):
- <full path to <project-slug>/_README.md>
- <full path to each drafted handoff>
- <full path to _spawn-queue.md row additions>
- <full path to _active-chats-tracker.md row additions>

Reply with one of:
- "approved" — write everything as proposed
- "approved with edits: <changes>" — write with your modifications
- "abort" — don't write anything
- specific feedback like "merge 2a and 2b" or "rename slug to <X>" or "downgrade Phase 3 to Tier 3"
```

Wait for explicit operator approval. Do not write any file until the operator says so.

**Step 10 — On approval, write everything atomically.**

After approval:

1. Create the project subfolder under `_meta/handoffs/<project-slug>/`
2. Write the `_README.md` from DECOMPOSE's proposed body
3. Write each drafted handoff file with frontmatter (including `preferred-substrate:`) + body + checkpoint reminder (where triggered) + closing protocol
4. Append spawn-queue rows to `_meta/handoffs/_spawn-queue.md` "Queued" section (append-only, monotonic numbering)
5. Regenerate the spawn-queue "Conflict flags" table from current Queued + in-flight file-sets
6. Add master-tracker rows in the appropriate tier sections
7. If the operator-fatigue warning fires, render the banner at the top of `_spawn-queue.md` "Queued" section
8. Bump frontmatter `last-change:` on the master tracker (one line) and prepend the full pass notes to `_active-chats-tracker-changelog.md`
9. Bump `_spawn-queue.md` frontmatter `last-change:` + `updated:`
10. Run the YAML parse check on every touched file. If any fails, surface the failure and offer to roll back.

The writes are atomic per run — handoff written but tracker row missing is a contract violation. If any step fails, surface to operator with a roll-back proposal.

**Step 11 — Tell the operator what to do next.**

Render the plain-language operator summary:

```
✅ PROVISION complete for <project name>.

What I drafted:
- N handoffs in `_meta/handoffs/<project-slug>/`
- N rows in `_spawn-queue.md` (queued, ready to spawn)
- N rows in the master tracker at <tier>

What's ready to spawn now (Tier 1, K rows):
- Row 1: <chat name> — substrate rec: <claude-code | cowork | either>
- ...

What's queued (Tier 2 / Tier 3, P rows):
- ...

Substrate routing for the queued rows:
- M rows are best fired via Claude Code Task tool — operator says "fire row N via Task tool" in this orchestrator chat
- P rows are best pasted into fresh Cowork windows — operator opens a new Cowork chat and pastes verbatim
- Q rows are either — operator picks by current context

Decision-research calls surfaced for your awareness:
- <call 1 one-line>
- <call 2 one-line>

Conflicts flagged: K total. <one-line summary of severity + suggested resolution>

Operator-fatigue check: <under-ceiling | ⚠️ over-ceiling at Nh — consider deferring before spawning>

What's next: review the spawn queue, resolve any conflicts, then spawn rows in your preferred order. Master tracker is updated; spawn queue is the audit trail.
```

**Step 12 — Auto-invoke output-quality-loop.**

PROVISION's writes are artifacts (drafted handoffs + queue rows + tracker rows + new project README). Per the auto-invoke convention, emit the standard block at completion:

````markdown
## Auto-invoke output-quality-loop

This skill produced the following artifact(s):
- `<full path to <project-slug>/_README.md>`
- `<full path to each drafted handoff>`
- `<full path to _spawn-queue.md>` (modify-only; the existing file was edited)
- `<full path to _active-chats-tracker.md>` (modify-only; the existing file was edited)

[output-quality-loop:eval] — for each artifact, run output-quality-loop in EVALUATE mode. If PASS, declare the chat done. If NEEDS REVISION or FAIL, ingest the revision prompt as if it were operator input and regenerate the artifact, then re-invoke output-quality-loop. Cap at 3 iterations; on the 3rd FAIL, escalate to the operator with the evaluation report.
````

Per the multi-chat-coordination DECOMPOSE convention, tracker edits are NOT in the evaluation list — they're the index, not the artifact. Only the drafted handoffs + `_README.md` + the spawn-queue rows are evaluated.

### PROVISION flags

- `--dry-run` — produce the proposal without ever writing on approval. Useful for previewing decomposition without committing.
- `--tier <1|2|3>` — override the default tier-2 registration for the new project's tracker rows.
- `--skip-conflict-scan` — skip Step 5 conflict detection. Use only when the operator explicitly accepts the risk; PROVISION still records the flag in the proposal so it's auditable.
- `--skip-decision-research` — skip Step 4's convention firing. Falls back to "decomposition left as DECOMPOSE proposed." Discouraged.
- `--skip-checkpoint-reminders` — skip Step 7 checkpoint-reminder injection for all drafted handoffs. Discouraged for handoffs >2h.
- `--fatigue-ceiling H` (default 10) — override the operator-fatigue warning threshold.
- `--chain-from-next-moves` — read the most recent NEXT-MOVES output for goal context (used when chaining; usually inferred from operator phrasing).

### PROVISION worked example

See `examples/first-provision-2026-06-01-ev-blog-content-calendar.md` for the first real-use run.

## Mode 5 — RESUME

### What RESUME produces

A project-scoped plain-language report with six sections (the four-part output contract from the v1.2 handoff plus a stale-state-reconciliation surface added at v1.2 Gate 1 operator refinement, plus a brief audit trail):

1. **Project state summary** — current wave, last closed wave, scope of next planned wave, blockers the project flagged, plus the state-file freshness signal.
2. **Available next-wave handoffs** — `planned_remaining_waves[]` entries whose dependencies are cleared, matched against handoff files Mode 5 found via `client:` frontmatter grep, with a tracker-Ready vs state-file-ready distinction.
3. **Cross-project unblockers** — a FILTERED SUBSET of vault-wide cross-project signals: only those whose source handoff has `client:` matching this project, OR explicitly names this project's slug, OR appears in a wave's `blocks_on:` array.
4. **Decomposition diagram** — text rendering of the project's wave dependency graph with status markers (`[✓]` closed · `[~]` in-progress · `[•]` ready · `[✗]` blocked · `[!]` superseded). Cycle detection runs every render; circular dependencies surface with a warning banner.
5. **Stale-state reconciliations** — every reconciliation Mode 5 applied (state-file-says-X-but-event-log-says-Y) with operator confirmation prompts. Transparency over magic.
6. **What I read to produce this** — brief audit trail of the six input sources, in read order, with freshness signals.

Detailed shape + minimum content + voice rules in [[resume-output-shape]].

RESUME is read-only on vault content (same as SURVEY and NEXT-MOVES). It does not mutate state files, never edits the master tracker, never writes a digest. Its output is a markdown report — emit to chat by default, persist to `_meta/handoffs/vault-orchestrator/runs/<YYYY-MM-DD-resume-<slug>>.md` on `--persist`.

### When RESUME fires

The operator triggers RESUME explicitly (the direct triggers in "When to trigger" above) OR a SURVEY output gets narrowed to one project ("zoom into S&H").

RESUME does NOT auto-fire from NEXT-MOVES outputs. NEXT-MOVES already ranks spawnable work across projects; RESUME's value is project-scoped visibility. The operator chains them deliberately if they want NEXT-MOVES first then RESUME on a specific candidate's project.

### RESUME step-by-step

**Step 1 — Receive the project slug.**

Operator-provided when triggering. If ambiguous (multiple project folders match), Mode 5 asks one clarifying question:

```
You said "resume S&H." I see two matching project folders:
1. s-and-h-contracting (under clients/_active)
2. s-and-h-personal-notes (under personal)

Which one?
```

If the slug doesn't resolve, Mode 5 stops with an honest finding rather than producing an empty report.

**Step 2 — Read the master tracker.**

Read `~/workspace/second-brain/_meta/handoffs/_active-chats-tracker.md`. Extract rows naming the project across in-flight / Ready / Tier-2 queued / Tier-3 queued / Recently closed (past 14 days) / Recently completed (past 7 days). The matching rule: row's Notes column references the project slug, OR row's handoff filename contains the slug.

The aggregator's generated rollup section MAY contain a per-project digest block for this project; if present, capture as a parallel summary for reconciliation in Step 7.

**Step 3 — Read the event log delta.**

Read `~/workspace/second-brain/_meta/_event-log.md` and filter rows to:

- Timestamp >= state file's `updated_at` value (if state file exists), OR
- Timestamp >= 24 hours ago (if no state file)

For each row in the delta, capture surface + pass + chat-id + summary. Mode 5 uses the delta for the stale-state reconciliation step and the cross-project-unblockers output section.

**Step 4 — Read the state file.**

Read `04_projects/.../{slug}/_state/onboarding.json` (or equivalent). Key fields: `schema_version`, `current_wave`, `waves[]`, `wave_log[]`, `planned_remaining_waves[]`, `blocked_on[]`, `failures[]` (entries with `operator_action: pending`), `quality_log` (any `light-escalate` decisions still pending).

If `schema_version` is older than the current skill version, surface as a finding — do NOT auto-migrate. Migration belongs to the owning skill.

If no state file exists, surface clearly and continue with master tracker + execution log signals only.

**Step 5 — Read the execution logs, newest-first.**

List `04_projects/.../{slug}/execution-logs/execution-log-*.md` sorted by filename descending. For the newest 1-3 logs, extract frontmatter + section headers + any "Decisions made" / "Lessons learned" subsections.

The newest execution log is the most-recent narrative; state file `wave_log` is the structured summary. Mode 5 reads both because each captures different things.

**Step 6 — Read the per-project chat tracker + digest.**

Read `_chat-tracker.md` (human-readable mirror) + `_chat-status.md` (machine-readable digest). The digest frontmatter is the primary read for `current-focus`, `blockers[]`, `spawn-recommendations[]`. If the digest is >14 days stale, surface that signal and treat the digest as advisory.

If neither file exists, surface as advisory (project predates the Phase 1 convention) and continue.

**Step 7 — Compute wave readiness + apply stale-state reconciliations.**

Build the wave graph from `state_file.waves[]` + `planned_remaining_waves[]`. For each pending wave, compute readiness by checking whether all `blocks_on[]` deps are closed-or-cleared.

Apply the five stale-state reconciliation detection rules from [[resume-input-sources]] § "Stale-state reconciliation rules":

1. Blocker apparently un-cleared but handoff consumed in event log
2. Wave in-progress but tracker shows the chat closed
3. Schema-version drift
4. Execution log newer than state file
5. Per-project tracker out-of-sync

For each reconciliation, name the source contradiction + Mode 5's inferred resolution + an operator confirmation prompt. Mode 5 NEVER writes a fix to the state file; it just produces an accurate read.

**Step 8 — Detect cross-project unblockers (filtered subset).**

Walk `_meta/handoffs/handoff-*.md` for frontmatter `client:` matching the named project, plus any handoff explicitly mentioning the project's slug in `purpose:` or body text, plus handoffs whose filename appears in any wave's `blocks_on:` array. For each qualifying handoff, capture filename + status + what it ships + which of this project's waves it would unblock.

The filter is mandatory — Section 3 of the output is project-scoped, not vault-wide. See [[resume-output-shape]] § "Section 3 — Cross-project unblockers" filter rule.

**Step 9 — Render the report.**

Render in the six-section order per [[resume-output-shape]]. Voice rules: plain prose paragraphs as synthesis, bullets fine for naming rows, jargon glossed inline on first use, wikilinks preserved per knowledge-os conventions, zero invented data.

Render the decomposition diagram per [[resume-decomposition-diagram-text]] — ASCII for ≤10 waves, table fallback for >10 waves, cycle detection on every render.

**Step 10 — Emit the report.**

Default: emit as chat output. The operator reads inline + responds to any confirmation prompts.

If the operator says "save the resume report" or "persist this," write to `~/workspace/second-brain/_meta/handoffs/vault-orchestrator/runs/<YYYY-MM-DD-resume-<slug>>.md` after `ls`ing the parent and creating `runs/` if absent. Frontmatter:

```yaml
---
type: report
status: draft
created: <today>
updated: <today>
project: <slug>
mode: resume
tags: [report, vault-orchestrator, resume, <slug>]
---
```

Free-form fields single-quote-wrapped. YAML parses-check runs after the write.

**Step 11 — Handle operator confirmation flow.**

When Section 5 (stale-state reconciliations) fires, the report includes per-reconciliation `Operator confirm: ...` prompts. The operator responds inline:

- On "yes" → Mode 5 treats the reconciled state as truth for downstream sections (e.g., wave A2 is unblocked if both reconciliations confirm)
- On "no" → Mode 5 reverts to state-file truth + re-renders the relevant sections
- On "edit" → Mode 5 asks one clarifying question + re-renders

Mode 5 NEVER writes a fix to the state file as part of confirmation. State file edits remain the owning skill's responsibility. Mode 5 just produces an accurate read.

**Step 12 — Auto-invoke output-quality-loop.**

Per the auto-invoke convention. Emit the standard block at completion — when the report is persisted to disk. When the report is chat-only, the "ephemeral artifacts" exemption applies; skip the block.

The block (verbatim) when the report was written:

````markdown
## Auto-invoke output-quality-loop

This skill produced the following artifact(s):
- `<path to the persisted resume report>`

[output-quality-loop:eval] — for each artifact, run output-quality-loop in EVALUATE mode. If PASS, declare the chat done. If NEEDS REVISION or FAIL, ingest the revision prompt as if it were operator input and regenerate the artifact, then re-invoke output-quality-loop. Cap at 3 iterations; on the 3rd FAIL, escalate to the operator with the evaluation report.
````

Spec routing for the RESUME report lives in `output-quality-loop/references/spec-routing-table.md` § "Vault-orchestrator RESUME report" (v1.2 additive routing entry — mirrors the v1.1 additive pattern).

### RESUME flags

- `--persist` — write the report to `_meta/handoffs/vault-orchestrator/runs/<YYYY-MM-DD-resume-<slug>>.md` in addition to chat output.
- `--persist-path <path>` — override the default persist path.
- `--dry-run` — produce the report without persisting even if `--persist` was requested.
- `--include-decomposition-diagram` (default true) — emit Section 4. Use `--include-decomposition-diagram=false` for terse outputs.
- `--skip-event-log-cross-reference` — skip Step 3's event log delta read. Used when the operator explicitly wants only state-file truth; loses the stale-state reconciliation surface.
- `--past-days N` (default 14) — change the "recent closed for this project" lookback window.

### RESUME → PROVISION chain

Mode 5 RESUME identifies which `planned_remaining_waves[]` are ready but lack handoff files. The operator's natural next move on those waves: "provision wave-X for <project>" — which invokes Mode 3 PROVISION to draft the handoff.

Mode 5 names this chain explicitly in its Section 2 output:

```
Chain note: wave A3 is state-file-ready but no handoff exists. To draft one,
say "provision wave-A3 for s-and-h-contracting" and Mode 3 will decompose +
draft + queue the handoff.
```

The chain closes known-gap-1 from v1.1 (mid-project resume for existing projects): Mode 5 surfaces remaining work; Mode 3 PROVISION drafts it; Mode 6 EXECUTE (separate chat tomorrow) handles the spawn side.

The composition contract: Mode 5 produces project-scoped state, Mode 3 PROVISION consumes that state as decomposition input for the named wave. The operator drives the chain — Mode 5 does NOT auto-invoke PROVISION.

### RESUME worked examples

See `examples/first-resume-2026-06-02-s-and-h.md` and `examples/first-resume-2026-06-02-ev-electric.md` for the first real-use runs against the live S&H and EV project state.

## Mode 6 — EXECUTE

The multi-agent control plane. Takes a specific next-wave handoff (either drafted by Mode 3 PROVISION or already on disk from operator drafting) + dispatches sub-agents to produce the wave's artifacts under orchestrator coordination. Closes the EXECUTION side of v1.1 known-gap-1; Mode 5 ships the read side, Mode 6 ships the dispatch side, the trio (RESUME → PROVISION → EXECUTE) closes the gap end-to-end.

### What EXECUTE produces

A dispatch plan (rendered up front for operator confirmation) plus orchestrated sub-agent execution that writes per-artifact verdicts to the project state file. The dispatch plan has six sections:

1. **Wave header** — wave ID, project slug, source handoff path, total artifact count, substrate detected, execution-shape label (parallel | sequential | push-driven).
2. **Sub-agent fan-out** — one row per planned sub-agent: artifact path, artifact type, spec source, estimated minutes, edit-zone declaration.
3. **Conflict-flag table** — output of [[parallel-safe-coordination|the edit-zone detector]] over the sub-agent set; severity per pair; resolution-path per row.
4. **Polling cadence + operator-gate routing** — `_pending-operator-decisions.md` path (per [[operator-gate-routing]]); polling cadence (parallel substrate) OR sequential-call ordering (Cowork substrate).
5. **Wave-close conditions** — what verdicts close the wave; what failures escalate; what triggers `wave_log` appending + `current_wave` clearing.
6. **Substrate-adapted wall-clock estimate** — total estimated time under the detected substrate, with a parallel-substrate alternative when relevant.

After operator confirmation, the orchestrator dispatches per the plan, polls (or sequentially calls), surfaces gates as they fire, and runs wave-close on completion. The persisted artifact is the dispatch log at `~/workspace/second-brain/_meta/handoffs/vault-orchestrator/runs/<YYYY-MM-DD-execute-<slug>-<wave-id>>.md` capturing the plan + every sub-agent verdict + every gate firing + the wave-close outcome.

EXECUTE writes (the project state file via sub-agents' per-key writes + the gate file at gates + the dispatch log on `--persist`) but only on operator confirmation of the dispatch plan. The dispatch plan IS the review-gate surface (same single-review-gate discipline Mode 3 PROVISION uses).

### When EXECUTE fires

The operator triggers EXECUTE explicitly OR a Mode 5 RESUME output chained ("now execute wave A2") OR a Mode 3 PROVISION output chained ("fire the queued handoff via Mode 6 instead of pasting").

EXECUTE does NOT auto-fire from Mode 5 or Mode 3 output. The orchestrator surfaces the option ("Mode 6 can dispatch this wave for you — say 'execute wave-X for <project>'") but the operator drives the chain.

EXECUTE requires:

- A named project slug + named wave ID.
- A handoff file on disk for that wave (either Mode-3-PROVISION-drafted or operator-drafted).
- The wave's state-file `planned_remaining_waves[]` entry exists with `blocks_on:` resolved (Mode 5's reconciliation surface clarifies this).
- The runtime substrate detected (Cowork Agent tool, Claude Code Task tool, or operator-stated Hermes-harness).

If any precondition fails, EXECUTE stops with an honest finding ("wave A2 handoff missing — run Mode 3 PROVISION first" / "state file says wave A2 is blocked on X — clear blocker or override before dispatching"). Mode 5 RESUME is the canonical first move when preconditions are uncertain.

### EXECUTE step-by-step

**Step 1 — Receive the project slug + wave ID.**

Operator-provided when triggering. The slug + wave ID together are the dispatch target. If the operator names only the project ("execute the next wave for S&H"), the orchestrator runs an internal Mode 5 RESUME first to identify the ready wave, then routes back to EXECUTE.

**Step 2 — Read the wave's handoff + state file.**

Read the wave's handoff (frontmatter + body) for the artifact list + spec sources + scope. Read the project state file for `planned_remaining_waves[<wave-id>]` + `blocked_on[]` (to confirm preconditions) + `quality_log` (to know which artifacts the wave already produced, if this is a resume of a partial wave).

Build the planned sub-agent set: one sub-agent per artifact the handoff names. The sub-agent's slug derives from the artifact path (per [[sub-agent-dispatch-contract]] § "Sub-agent failure modes" — slugs must be artifact-path-derived to prevent collision).

**Step 3 — Detect the runtime substrate.**

Per [[sub-agent-dispatch-contract]] § "Substrate detection":

1. Check for operator-stated substrate. If named, use it.
2. Probe tool availability. `mcp__cowork__*` markers + workspace path under `/sessions/.../mnt/` indicates Cowork Agent tool. Task tool availability + Mac filesystem path indicates Claude Code. Ambiguous → ask one clarifying question.
3. Default to Cowork Agent tool when fully ambiguous.

Record the detected substrate in the dispatch plan header.

**Step 4 — Compute edit-zones + run the conflict detector.**

For each planned sub-agent, compute the edit-zone per [[sub-agent-dispatch-contract]] § "Sub-agent edit-zone declaration":

- `writes`: the artifact path the sub-agent produces
- `state_keys`: `quality_log[<step>][<artifact-name>]`
- `append_only`: `waves[<wave-id>].outputs`, `failures[]`

Run the Phase 4 edit-zone conflict detector over the sub-agent set per [[parallel-safe-coordination|the reuse contract]]. Emit the conflict-flag table.

If any pair scores `serial-required` at sub-agent granularity, that's a contract violation (the dispatch plan is malformed). Stop + surface to operator.

If any pair scores `self-conflict` (a sub-agent's edit-zone names an orchestrator-owned key), stop + surface as a malformed sub-agent contract.

Normal output: `parallel-OK-with-note` on the shared `waves[<wave-id>].outputs` append-only array; rare `warning-only` on shared reference touches.

**Step 5 — Adapt the dispatch model to the substrate + compute the cost surface.**

Per [[sub-agent-dispatch-contract]] § "Substrate matrix" + lesson D-07:

- Cowork Agent tool: sequential one-shot. Total wall-clock ≈ sum of per-sub-agent minutes.
- Claude Code Task tool: true parallel. Total wall-clock ≈ slowest sub-agent + small coordination overhead.
- Hermes-harness (future): long-lived sub-agents + push-driven coordination.

Render the substrate-adapted wall-clock estimate. When the substrate is Cowork but the conflict-flag table shows `parallel-OK-with-note` rows, name the parallel alternative ("on Claude Code Task tool, ~1.5-2h instead").

Compute the cost surface per [[sub-agent-dispatch-contract]] § "Cost estimation aggregated from per-artifact-sizing":

- **Always-fires per artifact (pre-fire validation):** ~$0.001-0.003 per artifact for OpenAI + Gemini + Claude direct citation comparison + Mode 1 EVALUATE local spec walk. Aggregate: `validation_subtotal = per_artifact_validation × N`.
- **Conditional per artifact (Mode 4 Sonar escalation):** ~$0.06-$0.15 per Mode 4 iteration; worst case 3 iterations = ~$0.30-$0.45 per artifact. Aggregate: `sonar_ceiling = per_artifact_sonar_worstcase × N`.
- **Operator-visible cost line:** name BOTH the always-fires subtotal AND the conditional ceiling explicitly. Operator sees the floor + ceiling, NOT an opaque "approximately $X" estimate.
- **When project quality_log history exists:** use it to name an expected-cost range (e.g., "first brief landed at NEEDS REVISION minor with 1 iteration → expect ~$0.06-$0.12 per artifact"). When no signal exists, render the wide range + name the assumption.

**Step 6 — Render the dispatch plan + emit for operator confirmation.**

Render in the six-section order at the top of this Mode 6 spec. Voice rules: plain prose paragraphs for synthesis, tables for sub-agent rows + conflict flags, plain-language substrate explanation up front, zero invented data.

Emit the dispatch plan to chat. Honor the standing operator-fatigue heuristic — if total wall-clock crosses the 10-hour ceiling, render the advisory warning + name the option to split the wave across multiple Mode 6 invocations.

**Step 7 — Wait for operator confirmation.**

The operator confirms with `approve` / `edit <field> <new-value>` / `abort`. On `approve`, proceed to Step 8. On `edit`, apply the edit + re-render the plan + re-confirm. On `abort`, stop without writing.

This IS the single review gate for Mode 6. No sub-agents fire until the operator approves.

#### Peer-reviewer dispatch (v1.3)

After the dispatch plan emits (end of Step 6), BEFORE the operator sees it for confirmation in Step 7:

1. Detect substrate (3-probe sequence per [[../gate-peer-reviewer/SKILL.md]] § Substrate detection).
2. Dispatch the `gate-peer-reviewer` skill with:
   - `gate_reviewed.orchestrator: "vault-orchestrator"`
   - `gate_reviewed.mode: "Mode 6 EXECUTE"`
   - `gate_reviewed.gate_id: "Gate 3 dispatch plan + Gate 4 dispatch prompts (combined at Mode 6 v1.2 single review gate)"`
   - `gate_reviewed.wave_id: <current wave>`
   - `gate_reviewed.chat_id: <this chat's ID>`
   - `gate_reviewed.project_slug: <current project slug>`
   - Dispatch plan text + wave kickoff + (for Gate 4 structural compliance sub-check) prior wave's revised-final dispatch prompts
3. Hold operator return until peer-reviewer returns JSON.
4. Emit BOTH to operator: dispatch plan + peer-reviewer JSON (rendered as markdown with verdict + verdict_rationale + catches table + operator_reply_text in a copy-paste block).
5. Operator approves with one action.

**Skip if:** peer-reviewer skill not available on this substrate (graceful degradation — the run does NOT hard-block). When skipped, the orchestrator MUST do BOTH:

1. **Surface the skip LOUDLY to the operator at the gate** — render a visible warning block immediately above the approval prompt, never only in a log the operator won't be reading mid-run:

   ```
   ⚠️ PEER-REVIEWER DID NOT RUN — gate-peer-reviewer skill unavailable on this substrate.
   You are about to approve this dispatch plan WITHOUT independent review.
   Proceed only if you have reviewed the plan yourself.
   ```

   An un-reviewed plan must never be presented in a way that lets the operator mistake it for a reviewed one. This is the load-bearing half of the degradation: silent skip + buried log line is the failure mode this guards against.

2. **Log the skip to the event log** per the 5-field format in `gate-peer-reviewer/SKILL.md` § Graceful degradation, so the skip is also grep-discoverable after the fact.

**Cost:** $0.05-$0.12 Opus per gate + $0.025-$0.08 Sonar per wave (Check 3 fires ~1-2 of 5 conceptual gates). Total per-wave incremental: $0.28-$0.68.

**Cross-mode integration (v1.3 scope clarification).** The peer-reviewer's `gate-type-registry.md` names 5 conceptual gates (1 RESUME / 2 PROVISION / 3 dispatch plan / 4 dispatch prompts / 5 wave-close). In Mode 6 v1.2's actual architecture, these map across modes:
- Gate 1 RESUME = Mode 5 RESUME Step 11 confirmation (separate mode; future v1.1 integration point)
- Gate 2 PROVISION = Mode 3 PROVISION Step 9 single review gate (separate mode; future v1.1 integration point)
- **Gates 3 + 4 (combined) = Mode 6 EXECUTE Step 6/7 single review gate (THIS integration point; v1.3 ships)**
- Gate 5 wave-close = Mode 6 EXECUTE Step 10 wave-close (auto-closes in v1.2; future v1.1 integration point when operator-attended wave-close lands)
- Conditional sub-agent gates surfaced in Step 9 = handled by `operator-gate-routing` separately

v1.3 ships with the Mode 6 Step 6/7 hook because that's the single existing operator-attended gate where the catches from waves A2-A6 (Manassas MED utility, PWC carry-forward contradiction, A4/A5 dispatch prompt drift) all fired. Future hooks at Mode 5 + Mode 3 + Mode 6 Step 10 ship as production calibration data drives the expansion.

**Step 8 — Initialize the wave state.**

Atomic writes to the project state file:

- `current_wave: <wave-id>`
- `waves[<wave-id>].status: "in-progress"`
- `waves[<wave-id>].started_at: <ISO UTC>`
- `waves[<wave-id>].chat_id: <this chat's ID>`
- `waves[<wave-id>].dispatch_plan_path: <persisted plan path if --persist>`

Initialize the gate file at `04_projects/.../{slug}/_pending-operator-decisions.md` if absent (per [[operator-gate-routing]] § "File shape").

Append an event-log row via `append_event_log.sh`:

```
~/workspace/repos/ai-agency-core/scripts/append_event_log.sh \
  "04_projects/clients/_active/<slug>" \
  "n/a" \
  "<this chat's ID>" \
  "Mode 6 EXECUTE dispatch initialized for wave <wave-id> via <substrate>"
```

**Step 9 — Dispatch + poll (or sequential-call, per substrate).**

On Claude Code Task tool: fire all `parallel-OK-with-note` sub-agents in one message via concurrent Task calls. Fire `serial-required` sub-agents in dependency order (one Task call per message). Enter the polling loop per [[inter-agent-coordination-via-state-file]] § "Polling cadence." Default cadence 10s.

On Cowork Agent tool: fire sub-agent A via a single Agent call. Block until return. Read sub-agent A's structured response. Write the corresponding `quality_log` key + append `waves[<wave-id>].outputs` if PASS at threshold. Fire sub-agent B via the next Agent call. Repeat through the sub-agent list.

In both cases:

- On a sub-agent verdict `PASS at threshold` → mark sub-agent done in dispatch log.
- On `ESCALATED` (gate-file row written) → mark sub-agent paused; surface the gate row to the operator via [[operator-gate-routing]]; wait for operator response.
- On `FAIL after 3 iterations` → escalate per [[operator-gate-routing]] § "Gate types" → quality-loop-3-iter-stall.
- On `external-write-confirm` gate (per lesson D-06) → surface for operator confirmation before any external action fires.

The orchestrator NEVER auto-resolves a gate. Operator response drives every resume.

**Imagery-wave dispatch (v1.5).** When the wave being executed is an imagery wave (identified by its handoff containing `generate-imagery-prompts.py` invocations or `imagery_wave: true` in its frontmatter), Step 9 follows this adapted flow instead of the standard parallel/sequential sub-agent dispatch:

1. **Phase A — prompt generation (autonomous).** Fire one sub-agent per page to run `generate-imagery-prompts.py`. These are parallel-safe (each writes to its own page folder). Collect verdicts. On all PASS, proceed.
2. **Phase B — Higgsfield pause (operator out-of-band).** Write `imagery_wave_status: "paused-higgsfield"` to the project state file. Surface the pause message (same shape as client-seo-onboarding Step 7): aggregate summary path, per-page log paths, instruction to say "images are in for <slug>" when ready. The orchestrator stops and waits.
3. **Phase C — variant-selection gate (operator decision).** On resume, write a gate row to `_pending-operator-decisions.md` per page: "Pick the best variant per slot for <page-slug>: hero (1-N), about (1-N or REUSE), scene (1-N or SKIP)." Wait for operator response per [[operator-gate-routing]].
4. **Phase D — organize + wire (autonomous).** On gate resolution, fire one sub-agent per page to run `organize-image-downloads.py` (per slot, with the operator's variant picks) then `wire-page-images.py`. These are parallel-safe per page. Collect verdicts.
5. **Phase E — wave-close.** Standard Step 10 wave-close. The publish wave's `blocks_on` is now satisfied.

The imagery-wave dispatch plan (Step 6) must surface the Phase B pause and Phase C gate explicitly — the operator must see at plan-approval time that the wave will pause for Higgsfield and that variant selection is an operator gate, not a silent default.

**Step 10 — Wave-close.**

When all sub-agents in the wave have status `done` OR all gates resolve to non-pending outcomes:

- Write `waves[<wave-id>].status: "closed"` + `closed_at: <ISO UTC>` + `waves[<wave-id>].outputs` (already appended by sub-agents).
- Append a `wave_log[]` entry with summary + key_artifacts + spawned_handoffs (if any) + verdict_summary.
- Remove the just-closed wave from `planned_remaining_waves[]`.
- Clear `current_wave` (set to `null`).
- Truncate the gate file's "Closed gates (this wave)" section per the default cleanup rule (or preserve on `--preserve-gate-history`).
- Append a closing event-log row.

If `--persist` was used, finalize the dispatch log at `~/workspace/second-brain/_meta/handoffs/vault-orchestrator/runs/<YYYY-MM-DD-execute-<slug>-<wave-id>>.md` with the full audit trail. Frontmatter:

```yaml
---
type: report
status: shipped
created: <today>
updated: <today>
project: <slug>
wave: <wave-id>
mode: execute
skill: vault-orchestrator
skill-version: v1.5
tags: [report, vault-orchestrator, execute, <slug>, <wave-id>]
---
```

Free-form fields single-quote-wrapped. YAML parses-check runs after the write.

If a wave doesn't close cleanly (sub-agent stalled at `--defer`, operator hasn't responded to a gate within `--max-poll-iterations`), the orchestrator stops + surfaces the wave-open state for operator decision. The wave does NOT close silently with a missing artifact.

## Auto-invoke output-quality-loop

Per lesson D-05: Mode 6 does NOT auto-invoke `output-quality-loop` on its own dispatch plan or dispatch log. Each sub-agent's per-artifact output IS routed through `output-quality-loop` as part of the sub-agent's four-substep contract (Mode 1 EVALUATE + Mode 4 AUTO-RESEARCH + Mode 5 AUTO-APPROVE-AND-ESCALATE). Evaluating the dispatch plan would double-count the per-artifact loops + give a misleading "did the wave pass quality?" verdict (the wave's quality is the sum of its sub-agents' verdicts, recorded in `quality_log`).

The dispatch log's spec-routing entry at `output-quality-loop/references/spec-routing-table.md` § "Vault-orchestrator EXECUTE dispatch plan" is marked `quality-loop-skip: true` with the per-sub-agent-loop rationale.

If the operator wants a post-wave quality summary, the orchestrator emits an aggregated `quality_log` roll-up at wave-close (verdict + confidence + iteration count per artifact) — NOT a fresh output-quality-loop evaluation.

### EXECUTE flags

- `--persist` — write the dispatch log to `_meta/handoffs/vault-orchestrator/runs/<YYYY-MM-DD-execute-<slug>-<wave-id>>.md` in addition to chat output.
- `--dry-run` — produce the dispatch plan for operator review without firing any sub-agent or writing to the state file. Useful for capturing the plan in a worked example or for operator pre-confirmation.
- `--max-parallel N` (default 4) — cap concurrent sub-agents on parallel substrate. Useful for cost control or when the operator wants conservative dispatch.
- `--polling-cadence Ns` (default `10s`) — polling interval on parallel substrate; ignored on sequential substrate.
- `--silence-threshold Ns` (default `300s`) — flag a sub-agent as stalled if no `quality_log` entry lands in this window.
- `--max-poll-iterations N` (default `360`) — stop polling and escalate the open sub-agents if no completion happens in this window.
- `--gate-file-path <path>` — override the default `04_projects/.../{slug}/_pending-operator-decisions.md` location.
- `--skip-conflict-detection` — skip Step 4 (use only when the operator has manually verified the sub-agent set is parallel-safe). Audit-trail flag — the dispatch plan names the skip + reason.
- `--substrate <name>` — override substrate detection (`cowork-agent-tool` / `claude-code-task-tool` / `hermes-harness`).
- `--preserve-gate-history` — at wave-close, keep the gate file's "Closed gates" section as a per-wave archive instead of clearing it.

### EXECUTE worked example

See `examples/first-execute-2026-06-03-s-and-h-wave-a2.md` for the first documented dispatch plan (S&H wave A2: ev-charger-installation + light-fixture-installation sub-agents). Per the v1.2 handoff's explicit DO NOT directive, the example documents the dispatch plan without firing sub-agents; live dispatch is reserved for the actual S&H wave A2 run (which the operator may spawn manually OR via Mode 6 EXECUTE composition once this chat closes).

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
- **DECOMPOSE composition.** PROVISION (Mode 3) composes with DECOMPOSE to draft phase handoffs. PROVISION consumes DECOMPOSE's slug, dependency graph, handoff bodies, README body, and proposed tracker rows; it layers conflict detection + substrate tagging + checkpoint reminders + decision-research convention firing + operator-fatigue check + spawn-queue writes on top. The orchestrator does not reimplement DECOMPOSE's sizing rules, dependency analysis, or tier classification.
- **RESUME → PROVISION chain (v1.2).** Mode 5 RESUME identifies which `planned_remaining_waves[]` are ready but lack handoff files. The operator can chain into Mode 3 PROVISION on a specific ready wave by saying "provision wave-X for <project>." PROVISION consumes the RESUME report's wave scope as decomposition input rather than starting from a fresh strategic-chat goal. This chain closes v1.1's known-gap-1 on the drafting side. The operator drives the chain — RESUME does NOT auto-invoke PROVISION.
- **RESUME → PROVISION → EXECUTE chain (v1.2 full closer).** With Mode 6 EXECUTE shipped 2026-06-03, the v1.1 known-gap-1 closes end-to-end. RESUME identifies ready waves (the read side); PROVISION drafts handoffs for waves that lack them (the draft side); EXECUTE dispatches sub-agents per the handoff under orchestrator coordination (the dispatch side). The full chain runs as: "resume <project>" → operator picks a ready wave → "provision wave-X for <project>" (if no handoff exists yet) OR proceed directly → "execute wave-X for <project>." Each link is operator-driven; the orchestrator does not auto-chain. EXECUTE's substrate-adaptive dispatch model (parallel on Claude Code Task tool; sequential on Cowork Agent tool; push-driven on future Hermes-harness) is documented in [[sub-agent-dispatch-contract]] § "Substrate matrix."

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

## Out of scope (v1.2)

- **True autonomous spawning of WHOLE chats.** PROVISION drafts handoffs + queues prompts; Mode 6 EXECUTE dispatches narrowly-scoped per-artifact sub-agents under orchestrator coordination. Neither auto-spawns a fresh full-orchestrator chat. Auto-pasting whole handoff prompts from the queue is deferred until platform support exists (Anthropic Agent SDK long-lived chats, a host-machine harness, or Claude in Chrome driving the Cowork app).
- **Fully autonomous external actions (v1.2 Mode 6 specifically).** Per lesson D-06, Mode 6 stops at every external write (WP REST API, GSC Indexing API, git push, Higgsfield variant generation, any tier-3 API call that mutates external state). The sub-agent queues the external action via the operator-gate file; the operator confirms before any external fire. Read-only API calls (Sonar query, GBP read, etc.) proceed without gating.
- **Cross-project resource allocation.** If two projects' Mode 6 invocations want the same sub-agent slot (e.g., both projects need a Sonar-backed brief in the same window), v1.2 is first-come-first-serve; resource-aware scheduling is v1.3 work.
- **Sub-agent quality-loop integration beyond the four-substep contract.** Sub-agents implement the canonical four-substep quality loop (Mode 1 + Mode 4 + Mode 5) per [[sub-agent-dispatch-contract]]. v1.2 doesn't add new per-sub-agent quality gates beyond that. Cost-budget enforcement at the orchestrator level (total quality-loop cost cap per wave, total Sonar spend per dispatch) is v1.3.
- **Per-project orchestrator decomposition.** Splitting the monolithic orchestrator into project-surveyor + project-analyst + project-decider sub-skills lives in Phase 5 of this project, gated on 1 week of v1.1 real-use calibration.
- **Skill-needs analyzer.** Detecting "this work needs a skill that doesn't exist" patterns lives in Phase 6.
- **Real-time vault watching.** The orchestrator runs on operator invocation, not on file change.
- **Editing the master tracker outside the aggregator's marker block (Modes 1-2).** That section belongs to `master-tracker-aggregator`, not this skill. PROVISION (Mode 3) edits the hand-edited "Ready to spawn" / "Queued — Tier 2" / "Queued — Tier 3" sections via row additions — never edits the aggregator's marker block.
- **Editing per-project digests or trackers.** Read-only on per-project digests; PROVISION may write a new per-project subfolder + `_README.md` only when the operator approves a new project at the review gate.
- **Editing in-flight or already-queued handoffs.** PROVISION drafts new handoffs; it does not modify handoffs that already exist. Edits to existing handoffs are operator-driven or a separate maintenance chat.
- **Decomposing + dispatching remaining work for EXISTING projects — fully closed in v1.2 as of 2026-06-03.** v1.1's PROVISION created a new project subfolder for a new initiative; it had no path for existing-project resumes. v1.2 Mode 5 RESUME closes the identification side (2026-06-02): read the project's state file + execution logs + event log + master tracker rows naming this project, surface which `planned_remaining_waves[]` are ready, chain into Mode 3 PROVISION when the operator wants ready-waves drafted into handoff files. v1.2 Mode 6 EXECUTE closes the dispatch side (2026-06-03): take a wave's handoff + dispatch narrowly-scoped per-artifact sub-agents under orchestrator coordination, with the substrate-adaptive dispatch model (parallel on Claude Code Task tool; sequential on Cowork Agent tool; future push-driven on Hermes-harness). Together the trio (RESUME → PROVISION → EXECUTE) closes known-gap-1 end-to-end. Workaround for projects not yet using state files: Mode 5 reads what's present (master tracker rows + execution logs + handoffs naming the project) and produces a partial report; operator drafts the next-wave handoff by hand from that report; Mode 6 then dispatches against the hand-drafted handoff.
- **Cross-vault federation.** Single vault (`~/workspace/second-brain/`). Tier-3 vault is air-gapped by design.
- **Domain-level per-domain trackers.** Domains stay SURVEY-only — read folder listings + frontmatter freshness signals, don't expect a per-domain tracker.
- **Semantic-conflict detection.** Edit-zone conflict detection catches shared-file races; it does not predict semantic contradictions between two chats updating disjoint sections. That's a NEXT-MOVES decision-research call when surfaced.

## Verification before declaring done

Before the chat declares "SURVEY complete," "NEXT-MOVES complete," or "PROVISION complete":

**Modes 1 and 2 (SURVEY / NEXT-MOVES):**

1. Every section listed in the mode's output contract is present (9 sections for SURVEY; 7 parts for NEXT-MOVES).
2. Every per-candidate row in NEXT-MOVES has a substrate recommendation with a one-line rationale.
3. Session-budget totals are computed and displayed neutrally (no editorializing about what the operator should pick).
4. Recommended session plan respects the 8-hour cap (or names the cap explicitly if overridden via `--session-budget`).
5. Any decision-research convention calls are documented inline with their rationale.
6. Plain-language compliance — no jargon-density walls, no executive summary unless requested, glossed terms on first use.
7. If `--persist` was used, the file exists on disk with valid frontmatter and YAML parses.
8. If the report was persisted, the auto-invoke `output-quality-loop` block is emitted.
9. The opening-protocol row move (if running inside a handoff-spawned chat) is honored — Modes 1-2 do not edit the tracker outside the aggregator marker; if the host chat's row needs updating, the host chat does it.

**Mode 3 (PROVISION):**

1. The review gate fired — no file was written before operator approval landed.
2. Every drafted handoff has `preferred-substrate:` frontmatter (claude-code, cowork, or either) with a one-line rationale in the proposal.
3. Conflict scan ran and the conflict-flag table is rendered both in the proposal and (after approval) in `_spawn-queue.md`.
4. Every drafted handoff >2h estimated has a checkpoint-reminder section, or the proposal explicitly named the skip with reasoning.
5. Decision-research convention fired on every meaningful decomposition decision (phase ordering, scope cuts, dependency choices, substrate ambiguity, tier classification) with the call documented inline.
6. Operator-fatigue check ran; if queue total would exceed 10h, the warning banner is rendered in both the proposal and `_spawn-queue.md`.
7. Spawn-queue invariants hold per [[spawn-queue-shape]] (append-only at bottom of Queued, substrate-rec matches handoff frontmatter, prompts are verbatim, YAML parses).
8. Master-tracker rows landed in the appropriate tier sections; tracker frontmatter `last-change:` bumped (one line) and full pass prose prepended to `_active-chats-tracker-changelog.md`.
9. YAML parses on every touched file (drafted handoffs + project `_README.md` + `_spawn-queue.md` + master tracker).
10. Auto-invoke quality-loop block emitted naming every artifact (drafted handoffs + project `_README.md` + spawn-queue write); tracker edits excluded per the multi-chat-coordination convention.
11. Plain-language operator summary rendered with substrate routing breakdown, conflict count, fatigue-check status, and "what's next" guidance.

**Mode 5 (RESUME):**

1. The six input sources were read in the order specified in [[resume-input-sources]] § "Read order" — master tracker, event log delta, state file, execution logs newest-first, per-project chat tracker + digest, handoff `client:` grep. Missing sources are surfaced honestly per the honest-gap-surfacing rule.
2. The six output sections are present per [[resume-output-shape]] — project state summary, available next-wave handoffs, cross-project unblockers (filtered subset), decomposition diagram, stale-state reconciliations, what-I-read audit trail.
3. Every stale-state reconciliation detected (per the five rules in [[resume-input-sources]] § "Stale-state reconciliation rules") is surfaced in Section 5 with the source contradiction + Mode 5's inferred resolution + an operator confirmation prompt. If zero reconciliations fire, Section 5 explicitly says so.
4. Section 3's cross-project unblockers list passes the filter rule (only signals with `client:` matching this project, or explicitly naming the project slug, or appearing in a wave's `blocks_on:` array). Vault-wide signals that don't pass the filter are not surfaced here.
5. The decomposition diagram renders per [[resume-decomposition-diagram-text]] — ASCII for ≤10 waves, table fallback for >10 waves, cycle detection on every render with `⚠️ CIRCULAR DEPENDENCY` banner if any cycle detected.
6. Mode 5 did NOT write to the state file. No fixes, no migrations, no mutations. Reconciliations are surfaced for operator confirmation only.
7. If `--persist` was used, the file exists on disk with valid frontmatter and YAML parses; the auto-invoke `output-quality-loop` block is emitted naming the persisted report (spec routing via `spec-routing-table.md` § "Vault-orchestrator RESUME report").
8. Plain-language compliance — no jargon-density walls, no executive summary unless requested, glossed terms on first use.
9. The opening-protocol row move (if running inside a handoff-spawned chat) is honored — Mode 5 doesn't edit the tracker outside the aggregator marker; if the host chat's row needs updating, the host chat does it.
10. If the operator chains into PROVISION ("provision wave-X for <project>"), the chain handoff names the Mode 5 report as input — PROVISION reads the wave scope from the RESUME output rather than re-deriving from scratch.

**Mode 6 (EXECUTE):**

1. The substrate was detected (or operator-stated) BEFORE dispatch — operator-stated > tool probe > Cowork default. Dispatch plan names which detection path resolved + names the substrate explicitly per [[sub-agent-dispatch-contract]] § "Substrate detection."
2. Each sub-agent in the dispatch plan declares an edit-zone (artifact path + state-file `quality_log` key + append-only arrays it'll touch) per [[sub-agent-dispatch-contract]] § "Sub-agent edit-zone declaration."
3. The Phase 4 edit-zone conflict detector ran over the sub-agent set per [[parallel-safe-coordination]]; the conflict-flag table is rendered in the dispatch plan; no `serial-required` or `self-conflict` row escaped to fire (both are contract violations — the orchestrator stops + surfaces).
4. The substrate-adapted wall-clock estimate is rendered in the dispatch plan + names the parallel alternative when the substrate is Cowork but conflict-flags allow parallelism.
5. The operator confirmed the dispatch plan before any sub-agent fired (single review gate — same discipline as Mode 3 PROVISION).
6. The wave's state was initialized atomically — `current_wave`, `waves[<wave-id>].status: "in-progress"`, `waves[<wave-id>].started_at`, `waves[<wave-id>].chat_id`.
7. The operator-gate file at `04_projects/.../{slug}/_pending-operator-decisions.md` was initialized if absent + every gate fire wrote a row per [[operator-gate-routing]] § "Gate row schema." No gate auto-resolved silently — every gate's "Operator response" cell got either a non-pending value (proceed) or `--defer` (pause) or `--abort` (stop wave).
8. The wave-close ran cleanly — all sub-agents have status `done` OR all gates resolved; `waves[<wave-id>].status: "closed"` + `closed_at` written; `wave_log[]` appended; `planned_remaining_waves` updated to remove the just-closed wave; `current_wave` cleared.
9. The auto-invoke `output-quality-loop` block is NOT emitted on the dispatch plan itself (per lesson D-05) — per-sub-agent quality loops covered the per-artifact verdicts; the aggregated `quality_log` roll-up at wave-close substitutes.
10. If `--persist` was used, the dispatch log exists on disk at the named path with valid frontmatter + YAML parses; the dispatch log captures the plan + every sub-agent verdict + every gate firing + the wave-close outcome. Event-log rows appended at dispatch init + wave-close.

## Maintenance notes (for future skill iterations)

These observations seed at skill creation. Promote to standalone notes if they generalize.

**1. Watch for aggregator-section drift.** SURVEY reads the aggregator's generated rollup. If the aggregator's marker conventions change (block layout, section names), SURVEY's parsing logic needs updating. Detection: if the rollup section doesn't contain "Vault-wide rollup" or "Per-project digests" headings, surface as a finding.

**2. Watch for substrate-routing-table drift.** Substrate recommendations cite the working-surfaces convention's "Default routing" table. If that table evolves (new surface added, surface deprecated), update the substrate-recommendation reference. Detection: if a candidate's work shape doesn't map to any row in the table, surface as "substrate ambiguous — operator decides."

**3. Watch for priority-memory staleness.** NEXT-MOVES reads `project_priority_*` memories. If a memory becomes stale (priority shifted, project closed), recommendations skew wrong. Detection: at the start of every NEXT-MOVES run, surface the priority memories the orchestrator read so the operator can flag staleness.

**4. Watch for session-budget calibration.** 8-hour cap reflects today's operator tempo. If the operator regularly overrides (`--session-budget 4` for tight sessions, `--session-budget 12` for marathon days), the default may need adjustment. Detection: log override values in a maintenance note over time.

**5. Watch for domain-signal-mining drift.** SURVEY's Section 7 walks `03_domains/` for unsynthesized sources + unpromoted patterns. If the domain folder layout changes (new subfolders, renamed `insights/` → `sources/`), the walking logic needs updating. Detection: if Section 7 returns zero signals across all domains, spot-check the folder structure rather than assuming the vault is quiet.

**6. Watch for plain-language drift in reports.** If reports start reading dense or padded, the skill prompt needs calibration. Detection: output-quality-loop's plain-language compliance check surfaces this on every persisted report.

**7. Watch for cross-project-signal detection gaps.** Section 9 surfaces convention changes, multi-project handoffs, and downstream pattern-promotion effects. If a known cross-project event slips through (e.g., a convention change rolled out without SURVEY catching it), update the detection heuristics in `references/cross-project-signal-detection.md`.

**8. Watch for shared-file-pattern drift (PROVISION).** The edit-zone-conflict-detection reference enumerates shared-file patterns. If the vault gains a new canonical shared file (e.g., a new `_meta/<convention>.md`), the detector's pattern table needs the addition. Detection: if a real conflict ships through to merge time without being flagged, retro the missing pattern.

**9. Watch for operator-fatigue ceiling calibration (PROVISION).** The 10-hour ceiling matches today's 8-hour session cap + buffer. If the operator regularly overrides (`--fatigue-ceiling 6` for tight weeks, `--fatigue-ceiling 14` for marathon weeks), the default may need adjustment. Detection: track override values over time.

**10. Watch for substrate-tag accuracy (PROVISION).** Each drafted handoff gets a `preferred-substrate:` tag. If the operator regularly overrides at review-gate ("downgrade Phase 3 to cowork"), the substrate-tagging heuristics need refinement. Detection: log operator edits during PROVISION review gates.

**11. Watch for checkpoint-reminder over-inclusion or under-inclusion (PROVISION).** Step 7 triggers should fire on long-running handoffs and skip short ones. If short handoffs regularly arrive with checkpoint reminders (noise) or long ones arrive without (missed discipline), refine the trigger thresholds. Detection: spot-check drafted handoffs from each PROVISION run.

**12. Watch for stale-state reconciliation false-positives (RESUME).** Step 7 fires reconciliations when the event log + state file appear to disagree. False-positives (reconciliation fires but operator says "no, state file is correct") indicate the detection rules are too aggressive. Detection: log operator confirmation responses; if >20% of reconciliations get a "no" response, refine the detection rules in [[resume-input-sources]] § "Stale-state reconciliation rules."

**13. Watch for cross-project unblocker filter calibration (RESUME).** Section 3's filter (signal references project slug OR handoff `client:` matches) may turn out too narrow (missing relevant signals) or too broad (vault-wide noise leaking through). Detection: spot-check whether the operator regularly says "you missed signal X" or "signal Y wasn't relevant"; tune the filter rule in [[resume-output-shape]].

**14. Watch for state-file schema-version drift (RESUME).** State files for new project types may not match the `client-seo-onboarding` v1.1 schema. If Mode 5 encounters non-onboarding state files (e.g., a future hermes-harness state file, a future ads-and-marketing state file), the input extraction rules in [[resume-input-sources]] § "State file" may need additions per new schema. Detection: log "non-onboarding state file encountered" events; build out the extraction rules in [[resume-input-sources]] when a second schema shows up.

**15. Watch for substrate-detection accuracy drift (EXECUTE).** Step 3 detects the runtime substrate via operator-stated > tool probe > Cowork default. If the operator regularly overrides the detected substrate (`--substrate <name>` flag fires often), the probe heuristics may be missing a substrate signal — e.g., a new Claude Code substrate variant, or a Cowork-with-extended-tools mode that the probe misclassifies. Detection: log `--substrate` overrides; if >20% of dispatches override, refine the probe rules in [[sub-agent-dispatch-contract]] § "Substrate detection."

**16. Watch for operator-gate-file growth (EXECUTE).** `_pending-operator-decisions.md` files should stay small — open gates resolve in minutes; closed gates clear at wave-close by default. If a project's gate file grows past 500 lines or accumulates rows older than 7 days, that's a sign the operator isn't responding to gates (project may be paused) or the gate-types are mis-calibrated (sub-agents are escalating too aggressively). Detection: a sweep at wave-close that warns if any gate has been open > 24 hours.

**17. Watch for concurrent-write false-positive rate (EXECUTE).** Per [[inter-agent-coordination-via-state-file]] § "Concurrent-write risks + mitigations," the state file's per-key isolation rules SHOULD prevent collisions. If the orchestrator catches malformed-JSON reads regularly (parse failure → retry on next poll), that's a sign the isolation rules are leaking somewhere — likely a sub-agent writing a key it doesn't own. Detection: log JSON parse failures during polling; if >5% of polls catch one, audit the sub-agent contracts for the leaking key.

**18. Watch for sub-agent return-malformedness (EXECUTE).** Per [[sub-agent-dispatch-contract]] § "Sub-agent failure modes," sub-agents should return structured JSON responses. If sub-agents regularly return prose ("here's what I did...") instead of the structured contract, the dispatch prompt may not be emphasizing the contract clearly enough OR the sub-agent substrate may be silently editing the prompt. Detection: log return-malformedness rate; if > 10%, audit the dispatch prompt template + the substrate-specific call site.

## Related

- `~/workspace/skills/multi-chat-coordination/SKILL.md` — composes with this; provides the base NEXT-MOVE leverage ranking
- `~/workspace/skills/master-tracker-aggregator/SKILL.md` — composes with this; provides the per-project rollup SURVEY reads
- `~/workspace/skills/output-quality-loop/SKILL.md` — auto-invoke target for persisted reports
- `~/workspace/skills/output-quality-loop/references/auto-invoke-convention.md` — the block shape this skill emits when persisting
- `~/workspace/second-brain/_meta/handoffs/_active-chats-tracker.md` — the master tracker SURVEY reads end-to-end
- `~/workspace/second-brain/_meta/handoffs/vault-orchestrator/_README.md` — the project that produced this skill
- `~/workspace/second-brain/_meta/handoffs/vault-orchestrator/phase-3-orchestrator-v1-survey-and-next-moves.md` — the handoff that shipped Modes 1-2
- `~/workspace/second-brain/_meta/handoffs/vault-orchestrator/phase-4-provision-and-autospawn-queue.md` — the handoff that shipped Mode 3
- `~/workspace/second-brain/_meta/handoffs/_spawn-queue.md` — the substrate-agnostic queue PROVISION writes to
- `~/workspace/second-brain/_meta/working-surfaces.md` — substrate-recommendation source of truth
- `~/workspace/second-brain/_meta/handoffs/handoff-2026-06-01-vault-orchestrator-mid-project-resume-capability.md` — the v1.2 handoff that shipped Modes 5 + 6 (Mode 5 RESUME 2026-06-02; Mode 6 EXECUTE 2026-06-03)
- [[references/sub-agent-dispatch-contract]] — Mode 6 per-sub-agent contract + substrate-adaptive dispatch model
- [[references/inter-agent-coordination-via-state-file]] — Mode 6 polling + per-key write isolation
- [[references/operator-gate-routing]] — Mode 6 `_pending-operator-decisions.md` contract
- [[references/parallel-safe-coordination]] — Mode 6 reuse of Phase 4 edit-zone detector
- `~/workspace/skills/client-seo-onboarding/SKILL.md` § "Per-step quality loop contract" — the four-substep contract Mode 6 sub-agents implement
- `~/workspace/skills/client-seo-onboarding/state-schema.md` — the state file Mode 6 sub-agents write per-key
- `~/workspace/second-brain/_meta/decision-research-conventions.md` — five-step convention NEXT-MOVES + PROVISION invoke on hard calls
- `~/workspace/second-brain/_meta/plain-language-conventions.md` — voice rules every report follows
- `./references/survey-section-shapes.md` — section-by-section shape + minimum-content discipline for SURVEY
- `./references/leverage-scoring-heuristics.md` — how NEXT-MOVES scores leverage
- `./references/session-budget-display.md` — neutral session-budget display rules + 8-hour session-plan cap
- `./references/substrate-recommendation-heuristics.md` — Claude Code / Cowork / either tagging rules
- `./references/domain-signal-mining.md` — how SURVEY walks `03_domains/` for unsynthesized sources + unpromoted patterns
- `./references/cross-project-signal-detection.md` — how SURVEY detects multi-project handoffs + convention rollouts
- `./references/plain-language-discipline.md` — orchestrator-specific plain-language examples
- `./references/composition-with-multi-chat-coordination.md` — when NEXT-MOVES + PROVISION invoke MCC directly vs reimplement
- `./references/decision-research-composition.md` — when SURVEY + NEXT-MOVES + PROVISION invoke the decision-research convention
- `./references/edit-zone-conflict-detection.md` — how PROVISION scans for shared-file conflicts + scores severity + suggests resolutions
- `./references/spawn-queue-shape.md` — substrate-agnostic shape of `_spawn-queue.md` + invariants
- `./references/checkpoint-integration.md` — when PROVISION bakes chat-resilience checkpoint reminders into drafted handoffs
- `./references/resume-input-sources.md` — six input sources Mode 5 reads, read order, and the five stale-state reconciliation detection rules (v1.2)
- `./references/resume-output-shape.md` — six-section RESUME report shape + stale-state reconciliation surface + filter rule for Section 3 cross-project unblockers (v1.2)
- `./references/resume-decomposition-diagram-text.md` — ASCII wave-graph rendering rules + cycle detection + table fallback (v1.2)
- `~/workspace/skills/output-quality-loop/references/spec-routing-table.md` § "Vault-orchestrator RESUME report" — spec sources for evaluating persisted RESUME reports (v1.2 additive)
- `./examples/first-survey-2026-06-01.md` — first real-use SURVEY run
- `./examples/first-next-moves-2026-06-01.md` — first real-use NEXT-MOVES run
- `./examples/first-provision-2026-06-01-ev-blog-content-calendar.md` — first real-use PROVISION run (EV Electric blog content calendar generator)
- `./examples/first-resume-2026-06-02-s-and-h.md` — first real-use RESUME run (S&H Contracting; wave A1 closed + wave A2 unblocked via stale-state reconciliation)
- `./examples/first-resume-2026-06-02-ev-electric.md` — first real-use RESUME run (EV Electric; pages 06-12 closed-as-superseded + Mode-6-gated re-attempt + pages 13-30 queued behind)
