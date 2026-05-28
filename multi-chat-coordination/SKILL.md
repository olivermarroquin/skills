---
name: multi-chat-coordination
description: Three-mode skill for organizing Cowork projects that span multiple chats. **Mode 1 (DECOMPOSE):** takes a project goal and decomposes it into a sequenced set of handoff files with declared dependencies, proposes a kebab-case folder slug, generates a per-project README plus one handoff per phase (each with the mandatory closing protocol baked in), and registers the rows in the active-chats tracker at the right tier. **Mode 2 (AUDIT):** walks the active-chats tracker, cross-references every row against handoff frontmatter and on-disk execution logs, surfaces stale rows / missing rows / status drift / frontmatter issues, and proposes patches grouped into labeled A/B/C batches for per-batch operator approval. **Mode 3 (NEXT-MOVE):** ranks the spawnable candidates by leverage (blocker status, calendar gates, file-collision risk, cognitive load, downstream pull, operator priority) and recommends the next move plus a sequence over the next N moves with reasoning per row. Trigger phrases include "decompose [project] into handoffs," "split [project] into chats," "plan a multi-chat rollout for [scope]," "audit my active chats," "check the tracker against disk," "what's drifted," "what should I spawn next," "what chat should I run now," "when [chat] finishes what's next," "give me the sequence for the next [N] moves." Non-destructive by default — every write goes through an explicit operator review gate. Built 2026-05-27 to replace ad-hoc operator-and-Claude tracker maintenance with a deterministic skill invocation.
---

# Multi-Chat Coordination

The skill that organizes Cowork projects spanning multiple chats. When a project is too big for one chat, this skill splits it into a sequenced set of handoffs with declared dependencies, drops the handoffs into a project subfolder under `~/workspace/second-brain/_meta/handoffs/`, registers each in the active-chats tracker at the right tier, and gives the operator clarity reports on demand ("what's blocking what, what should I spawn next, is anything stale").

The skill exists because multi-chat coordination was being done in-chat by Oliver and Claude collaborating in the moment. That works when Claude is the right collaborator at the right moment, but it doesn't compose — every coordination session burned time re-establishing context. The skill captures the discipline so any chat can invoke it without that ramp-up.

## When to trigger

### Mode 1 — DECOMPOSE (project planning)

Direct triggers for breaking a goal into a sequenced set of handoffs:

- "Decompose [project goal] into handoffs"
- "Split [project name] into chats"
- "Plan a multi-chat rollout for [scope]"
- "I have a big project — help me break it into chat-sized pieces"
- "Set up a handoff folder for [initiative]"
- "Scope this initiative into phases"

Indirect triggers — when the operator describes a multi-week, multi-deliverable initiative and there is no existing project subfolder:

- "I want to ship a YouTube channel for Keelworks"
- "Let's build out the Phase 2 client-pivot work"
- "I need to migrate the legacy vault content into the new structure"

If the operator describes a single-chat unit of work (one deliverable, no dependencies, fits in 2-4 hours), surface that a standalone handoff is probably the right shape instead — skip DECOMPOSE, propose a single `handoff-YYYY-MM-DD-<slug>.md` file at the root of `_meta/handoffs/`.

### Mode 2 — AUDIT (tracker maintenance)

Direct triggers for walking the tracker and finding drift:

- "Audit my active chats"
- "Check the tracker against disk"
- "What's the current state of my chats?"
- "Is the tracker out of date?"
- "What's drifted?"
- "Run the audit"

Indirect triggers — when the operator opens a chat after a long gap or after a busy period where multiple chats shipped without explicit closeout:

- "I haven't touched the tracker in a few days — anything stale?"
- "Multiple chats wrapped this evening. The tracker is probably behind."

### Mode 3 — NEXT-MOVE (recommendation)

Direct triggers for ranking what to spawn next:

- "What should I spawn next?"
- "What chat should I run now?"
- "When [chat name] finishes, what's next?"
- "Give me the sequence for the next [N] moves"
- "Should I run [chat name] now or wait?"
- "Rank my spawnable candidates"

Indirect triggers — when the operator finishes a chat and asks an open-ended forward-looking question:

- "Just shipped X. What now?"
- "I have an hour. What's the highest-leverage thing to spawn?"

## Core operating principles

These principles apply across all three modes. Read them before invoking any mode.

**Non-destructive by default.** The skill NEVER edits the tracker, a handoff file, or a project folder without operator approval. Every write goes through an explicit confirmation step. The skill produces proposed patches; the operator confirms; only then does the skill write.

**Plain language.** Every report, recommendation, and decomposition output follows `~/workspace/second-brain/_meta/plain-language-conventions.md`. Drift reports read like a colleague walking the operator through what they found. Recommendations read like a colleague advising on what to spawn next. No jargon density, no AI-generated padding, no executive summaries the operator didn't ask for.

**YAML single-quote-wrap rule.** When the skill edits `_active-chats-tracker.md` frontmatter `last-change:`, the value MUST stay wrapped in single quotes. The value is free-form prose that almost always contains colon-space sequences that break YAML parsing if unquoted. This trap has bitten the file at least four times. Two related traps live in the same field:

- **Apostrophes in single-quoted YAML must be doubled.** `it''s` inside the value, not `it's` — an unescaped apostrophe ends the quoted string early.
- **Literal `---` inside the value can fool naive frontmatter extractors.** The skill uses a regex-based extractor that matches the frontmatter as a whole (opening `---\n` through closing `\n---\n`), not a naive `.split('---')[1]`.

After every tracker edit, the skill runs:

```bash
python3 -c "import yaml, re; m = re.match(r'^---\n(.*?)\n---\n', open('_meta/handoffs/_active-chats-tracker.md').read(), re.DOTALL); yaml.safe_load(m.group(1)); print('OK')"
```

Expected output: `OK`. Any other output is a frontmatter error to fix before declaring the edit complete.

**Batch approval for tracker edits touching 3+ rows.** Per the standing memory `feedback_batch_approval_for_vault_moves`, group proposed tracker edits into labeled batches (A, B, C) with one-line rationales. Don't dump all edits at once. Don't ask per-edit either — that burns turns. Batches respect the non-destructive default while keeping approval cost low.

**No silent overwrites.** If a tracker row says one thing and the disk says another, surface the conflict — do NOT silently pick a winner. Show both states, propose a resolution, wait for confirmation.

**Tracker is canonical when there's a conflict.** Per the file's own Update Protocol section. The skill treats the tracker as the authoritative source of "what was believed to be true at last update" and surfaces disk-state as new information that may or may not need to propagate. The operator decides which side wins.

**Check folder structure before writing.** Per the standing memory `feedback_check_folder_structure_before_writing`, run `ls` of the parent directory before writing any new file into established vault areas. The `_meta/handoffs/` folder has an intentional structure (root-level standalone handoffs + per-project subfolders); don't drift from it.

**Every generated handoff includes BOTH Opening Protocol AND Closing Protocol.** Established by the nineteenth-pass tracker reorganization (2026-05-28) after the operator observed manually instructing every chat at start AND end. The Opening Protocol (verbatim from `references/opening-protocol-template.md`) runs FIRST inside the prompt fence — before any work — and moves the chat's row from queued → in-flight in the tracker. The Closing Protocol (verbatim from `references/closing-protocol-template.md`) runs LAST inside the prompt fence — before declaring done — and moves the chat's row from in-flight → recently-closed plus all the other status updates. DECOMPOSE inserts both verbatim into every generated handoff body.

**Move, don't strikethrough.** When a row leaves a tracker section (chat spawns, ships, or promotes between tiers), MOVE it. **Never** leave a strikethrough'd pointer (~~row~~) in the prior section. The destination section is the canonical location. This rule is established in `references/tracker-row-shapes.md` and enforced by both protocols. AUDIT mode treats strikethrough rows as drift.

**Visual conventions on every tracker section.** Each actionable section opens with a one-line Obsidian callout immediately after the `##` header: `[!warning]` (active/yellow), `[!info]` (spawnable/blue), `[!note]` (queued/blue), `[!question]` (decisions/yellow), `[!success]` (closed/green), `[!danger]` (escalated/red — reserved for future). Each callout includes the section's row count for at-a-glance section sizing. Full mapping in `references/tracker-row-shapes.md`.

## Mode 1 — DECOMPOSE

### What DECOMPOSE produces

For an operator-provided goal, DECOMPOSE returns:

1. A proposed kebab-case project slug for the subfolder (e.g., `youtube-channel-launch`, `keelworks-onboarding-revamp`, `vault-cleanup-q3`)
2. A list of N proposed handoffs — one per discrete unit of work, each sized to fit one Cowork chat (target: 2-4 hours of work; smaller is fine; much bigger means decompose further)
3. A dependency graph in plain text — which handoffs block which, which are parallelizable
4. A proposed per-project `_README.md` body using the project-subfolder-template
5. Proposed full bodies for each generated handoff (frontmatter + prompt body + closing protocol)
6. Proposed tracker rows — Tier-1 Ready-to-spawn for handoffs with no prereqs, Tier-3 queued for handoffs blocked on later phases

DECOMPOSE then surfaces all of this as a single review gate. The operator approves the decomposition as a whole, edits individual proposals, or aborts. Only after approval does DECOMPOSE write any file.

### DECOMPOSE step-by-step

**Step 1 — Gather the goal.**

Read the operator's goal description. If they pointed at source documents (a blueprint, a scope doc, an opportunity note, a strategic-chat output), read those too. Establish:

- What ships at the end of this initiative?
- What constraints exist (deadlines, dependencies on external systems, prerequisite chats already in flight)?
- What "done" looks like — the success criteria for the whole initiative, not just individual phases.

If the goal is underspecified, surface 1-2 clarifying questions BEFORE proposing a decomposition. Common gaps:

- The operator named the deliverable but not the audience (who consumes the output)
- The operator named the scope but not the constraints (deadlines, prerequisite chats)
- The operator named the initiative but not the success criteria

**Step 2 — Decompose into units.**

Break the goal into discrete units of work. Each unit is one handoff. Sizing rules:

- **Target: one Cowork chat = 2-4 hours of focused work.** Smaller is fine. Much bigger means decompose further.
- **One deliverable per handoff.** If a unit produces multiple unrelated deliverables, split it.
- **One concern per handoff.** Research + build + ship is three handoffs, not one.
- **Out of scope is explicit.** Each handoff names what it won't touch — prevents scope creep mid-chat.

For each unit, name:

- A short kebab-case phase slug (e.g., `phase-1-strategy`, `phase-2-research`, `phase-3a-build`)
- A one-sentence purpose
- The deliverable (what file/artifact ships)
- Prerequisite phases (which other handoffs must finish first)
- Estimated build time (range, not point)

**Step 3 — Identify the dependency graph.**

For each unit, identify which other units must ship before this one can start. Then:

- **Tier-1 candidates (Ready to spawn now):** units with no unfinished prerequisites
- **Tier-2 candidates (spawn after Tier-1 lands, within ~1 week):** units whose only prerequisites are Tier-1 handoffs in this same initiative
- **Tier-3 candidates (wait for explicit triggers):** units gated on multi-phase chains, external system events, or calendar dates

Identify parallelizable phases — units with no dependency on each other (e.g., Phase 2a, 2b, 2c, 2d all depend on Phase 1 but not on each other). These can spawn as concurrent chats once their shared prerequisite lands.

Render the graph as plain-text indented ASCII for the project README:

```
Phase 1 (keystone — must ship first)
   1  → strategy

Phase 2 (depends on Phase 1; can run as parallel chats)
   2a → research arm A
   2b → research arm B
   2c → research arm C

Phase 3 (depends on all Phase 2 sub-phases)
   3  → integration
```

**Step 4 — Propose the project slug.**

Generate a kebab-case slug for the subfolder. Rules:

- Reflects the initiative's purpose, not its components (`youtube-channel-launch`, not `videos-plus-distribution`)
- Lowercase, hyphens between words, no underscores
- 2-5 words; keep it scannable in a directory listing
- Avoid date stamps in the folder name (dates go in the handoff frontmatter; project folders persist across years)

Surface the slug as a proposal — operator may override.

**Step 5 — Generate the per-project README.**

Use the body shape from `references/project-subfolder-template.md`. Substitute:

- The proposed slug
- Today's date
- The phase count
- The 2-3 sentence framing (write from the operator's goal)
- The 1-2 paragraph "Why this initiative exists" (write from the operator's goal + source documents)
- The plain-text dependency graph (from Step 3)
- The phase tracker table (one row per generated handoff, each at the appropriate tier)
- The reading-order list (3-5 items pointing to relevant primers, blueprints, specs)
- The "See also" links

**Step 6 — Generate each handoff body.**

For each unit identified in Step 2, generate a full handoff file. Body shape:

```markdown
---
type: handoff
status: active
created: <today>
purpose: <one-sentence purpose from Step 2>
tags: [handoff, <project-slug>, <other-applicable-tags>]
---

# Handoff — <human-readable name>

<2-3 sentence framing — what the chat produces, why it matters, prerequisites if any>

## Prompt to paste into a new chat

--- start prompt ---

<inserted verbatim from references/opening-protocol-template.md — Opening Protocol runs FIRST, before any other work>

<full prompt body — context to read, what you're building, success criteria, deliverables, out of scope. Generated from the operator's source documents + the unit's specific scope.>

## Status

- Created <today> as part of the <project-slug> decomposition
- Prereqs: <list, or "none — no blockers">
- Spawn-readiness: <Ready / Tier-2 / Tier-3 with explanation>
- Estimated build time: <range from Step 2>

<inserted verbatim from references/closing-protocol-template.md, with <HANDOFF_FILE_PATH> and <TRACKER_PATH> substituted — Closing Protocol runs LAST, before declaring done>

--- end prompt ---

## See also

- [[<project-slug>/_README]]
- [[<related blueprints, primers, or specs>]]
```

The closing protocol sits **inside** the prompt block (between Status and `--- end prompt ---`) so the chat consuming the handoff sees it as part of its instructions. This is mandatory — every generated handoff includes it. Reason: prior chats forgot to update the tracker, forgot to flip handoff status to `consumed`, used `git add .` instead of staging files by name, or just declared "done" without doing the bookkeeping. The closing protocol closes those gaps automatically.

**Step 7 — Generate the tracker row additions.**

For each generated handoff, propose a tracker row. Tier determines which table the row lands in:

- Tier-1 candidates → "Ready to spawn next (blockers cleared)" with a Why-now cell explaining what cleared the path
- Tier-2 candidates → "Queued — Tier 2" with a Trigger-to-spawn cell naming the sibling phase that will clear the path
- Tier-3 candidates → "Queued — Tier 3" with a Trigger-to-wait-for cell naming the hard gate

Use wikilink targets per the tracker-row-shapes spec: `[[<project-slug>/phase-N-<short>\|<short label>]]`.

**Step 8 — Surface the review gate.**

Present the full decomposition to the operator as a single review:

```
DECOMPOSITION PROPOSAL — <today>

Initiative: <operator's goal in one sentence>
Proposed subfolder: ~/workspace/second-brain/_meta/handoffs/<project-slug>/

Dependency graph:
<plain-text indented graph from Step 3>

N proposed handoffs:

1. phase-1-<short> — <purpose> (Tier 1, ~Nh)
   Prereqs: none
   Deliverable: <what ships>

2. phase-2a-<short> — <purpose> (Tier 2, ~Nh)
   Prereqs: phase-1-<short>
   Deliverable: <what ships>

... (continue for each phase)

Proposed tracker row additions:
- N rows to "Ready to spawn next"
- N rows to "Queued — Tier 2"
- N rows to "Queued — Tier 3"

Files I would create (none written yet):
- <full path to _README.md>
- <full path to each handoff>

Reply with one of:
- "approved" — write everything as proposed
- "approved with edits: <changes>" — write with your modifications
- "abort" — don't write anything
- specific feedback like "merge 2a and 2b" or "rename to <slug>"
```

Wait for explicit operator approval. Do not write any file until the operator says so. On approval:

- Write the project subfolder + `_README.md` + all handoff files
- Apply the proposed tracker row additions
- Update the tracker's `last-change:` frontmatter (single-quoted) with a one-paragraph summary of what was added
- Run the YAML parse check
- Report what landed

If the operator edits the proposal, regenerate the affected files only, re-surface the changed proposals, and re-confirm before writing.

### DECOMPOSE worked example

**Operator:** "Decompose 'launch the Keelworks YouTube channel' into handoffs."

**Skill response:**

```
DECOMPOSITION PROPOSAL — 2026-05-27

Initiative: Launch the Keelworks YouTube channel — strategy through first three published videos plus distribution setup and an analytics loop.
Proposed subfolder: ~/workspace/second-brain/_meta/handoffs/youtube-channel-launch/

Dependency graph:

Phase 1 (keystone)
   1  → channel-strategy                ← START HERE

Phase 2 (depends on Phase 1; can parallelize)
   2a → brand-setup                     (channel art, banner, about-section copy)
   2b → equipment-and-environment       (mic, lighting, recording space)

Phase 3 (depends on Phase 1 + Phase 2)
   3  → video-1-script-and-record       (proof-of-concept video)

Phase 4 (depends on Phase 3)
   4  → first-3-videos-batch            (videos 2 and 3 + publish all three)

Phase 5 (depends on Phase 4)
   5a → distribution-setup              (cross-post to LinkedIn, Twitter, vault)
   5b → analytics-and-iteration         (analytics baseline + iteration log)

6 proposed handoffs:

1. phase-1-channel-strategy — Strategy doc: niche, target operator profile, content pillars, cadence, success metrics (Tier 1, ~3h)
   Prereqs: none
   Deliverable: ~/workspace/second-brain/02_core/strategy/strategy-youtube-channel-2026-05-27.md

2. phase-2a-brand-setup — Channel art, banner, about-section copy, channel handle (Tier 2, ~2h)
   Prereqs: phase-1-channel-strategy
   Deliverable: Channel set up live + brand assets in ~/workspace/repos/keelworks-brand/

3. phase-2b-equipment-and-environment — Mic, lighting, recording environment baseline (Tier 2, ~2h)
   Prereqs: phase-1-channel-strategy
   Deliverable: Equipment checklist + first room test recording

4. phase-3-video-1-script-and-record — Proof-of-concept video — script, record, edit, publish (Tier 3, ~4h)
   Prereqs: phase-1, phase-2a, phase-2b
   Deliverable: Video 1 published; lessons captured

5. phase-4-first-3-videos-batch — Videos 2 and 3 — script, record, edit, publish (Tier 3, ~6h)
   Prereqs: phase-3-video-1-script-and-record
   Deliverable: 3 videos live on the channel

6. phase-5a-distribution-setup — Cross-post workflow + vault source-note pattern (Tier 3, ~2h)
   Prereqs: phase-4-first-3-videos-batch
   Deliverable: Distribution SOP + first 3 videos cross-posted

7. phase-5b-analytics-and-iteration — Analytics baseline + iteration log shape (Tier 3, ~2h)
   Prereqs: phase-4-first-3-videos-batch
   Deliverable: Analytics dashboard + iteration log template

Proposed tracker row additions:
- 1 row to "Ready to spawn next" (phase-1-channel-strategy)
- 2 rows to "Queued — Tier 2" (phase-2a, phase-2b)
- 4 rows to "Queued — Tier 3" (phase-3, phase-4, phase-5a, phase-5b)

Files I would create (none written yet):
- ~/workspace/second-brain/_meta/handoffs/youtube-channel-launch/_README.md
- ~/workspace/second-brain/_meta/handoffs/youtube-channel-launch/phase-1-channel-strategy.md
- ~/workspace/second-brain/_meta/handoffs/youtube-channel-launch/phase-2a-brand-setup.md
- ~/workspace/second-brain/_meta/handoffs/youtube-channel-launch/phase-2b-equipment-and-environment.md
- ~/workspace/second-brain/_meta/handoffs/youtube-channel-launch/phase-3-video-1-script-and-record.md
- ~/workspace/second-brain/_meta/handoffs/youtube-channel-launch/phase-4-first-3-videos-batch.md
- ~/workspace/second-brain/_meta/handoffs/youtube-channel-launch/phase-5a-distribution-setup.md
- ~/workspace/second-brain/_meta/handoffs/youtube-channel-launch/phase-5b-analytics-and-iteration.md

Reply with "approved", "approved with edits: ...", "abort", or specific feedback.
```

The operator can then approve, edit ("merge 5a and 5b — distribution and analytics are one chat"), or abort. The skill writes nothing until the operator says so.

## Mode 2 — AUDIT

### What AUDIT produces

A drift report following the shape in `references/drift-report-template.md`. The report has four finding categories:

- **STALE in-flight rows** — tracker rows marked in-flight where the handoff says consumed
- **MISSING from tracker** — consumed handoffs or recent execution logs with no tracker row
- **STATUS DRIFT** — tracker state contradicts handoff state in non-stale ways
- **FRONTMATTER ISSUES** — frontmatter errors, missing fields, or malformed YAML

For each drift surfaced, AUDIT proposes a patch. Patches group into labeled A/B/C batches per the batch-approval discipline. The operator approves per batch; the skill applies; the skill re-validates YAML; the skill updates the `last-change:` frontmatter.

### AUDIT step-by-step

**Step 1 — Read the tracker in full.**

Read `~/workspace/second-brain/_meta/handoffs/_active-chats-tracker.md`. Parse:

- Frontmatter (especially `last-change:` for audit-scope reasoning)
- Every row in every table — chat name, handoff wikilink, tier, struck-through state
- The "Hot decisions" list (informational; skill never edits this)

Build an internal map: `{chat_name → {table, handoff_path, status_per_tracker, is_strikethrough}}`.

**Step 2 — Validate tracker YAML.**

Run:

```bash
python3 -c "import yaml, re; m = re.match(r'^---\n(.*?)\n---\n', open('_meta/handoffs/_active-chats-tracker.md').read(), re.DOTALL); yaml.safe_load(m.group(1)); print('OK')"
```

If this fails, surface it as the first finding and stop further audit work until the operator approves a fix. A broken tracker frontmatter blocks every downstream operation.

The regex extractor correctly handles `---` literals inside the `last-change` value (a naive `.split('---')[1]` would falsely truncate the frontmatter mid-value — the regression-test run on 2026-05-27 caught exactly that bug in an earlier version of this command).

**Step 3 — For each tracker row, resolve the handoff file.**

Walk each row. For each handoff wikilink, resolve to an absolute path. Two forms:

- Standalone: `[[handoff-YYYY-MM-DD-<slug>]]` → `~/workspace/second-brain/_meta/handoffs/handoff-YYYY-MM-DD-<slug>.md`
- Project-folder: `[[<project-slug>/phase-N-<short>]]` → `~/workspace/second-brain/_meta/handoffs/<project-slug>/phase-N-<short>.md`

If a referenced handoff doesn't exist on disk, log it as a `FRONTMATTER ISSUES` finding (missing handoff file).

**Step 4 — For each handoff, read frontmatter.**

For each resolved handoff:

- Parse the YAML frontmatter
- Extract `status:`, `consumed:` if present, `actual-deliverable:` if present
- Check for an "Actual deliverable" blockquote at the top of the body (if no `actual-deliverable:` frontmatter field)

**Step 5 — Detect STALE in-flight rows.**

For every row in "Active / in-flight chats", check: does the handoff's `status:` say `consumed`?

- If yes → STALE in-flight row. Propose: move row from "Active / in-flight" to "Recently closed" with outcome paragraph drawn from the handoff's actual-deliverable note or the linked exec log.

**Step 6 — Detect MISSING from tracker.**

Two sub-checks:

**6a — Consumed handoffs without tracker rows:**

Walk `_meta/handoffs/` (root + every subfolder). For every handoff file with `status: consumed` AND `consumed:` date within the past 14 days, check: does any tracker row reference this handoff?

- If no → MISSING from tracker. Propose: add a row to "Recently closed chats" + a one-liner to "Recently completed (past 7 days)" using the handoff's actual-deliverable note as the outcome cell.

**6b — Today's execution logs without matching tracker rows:**

Walk execution log directories (typically `~/workspace/second-brain/04_projects/clients/_active/<client>/execution-logs/` and similar). For every execution log modified today, check: does any tracker row's outcome or handoff reference this exec log?

- If no → MISSING from tracker. Propose: cross-check whether a consumed handoff exists for this work. If yes, surface in 6a's list. If no, add a row for the operator-driven chat (handoff cell: "n/a (operator-driven)").

**Step 7 — Detect STATUS DRIFT.**

For every row that isn't already flagged as STALE:

- Queue rows (Ready-to-spawn / Tier-2 / Tier-3) where the handoff is `status: consumed` → suggests the chat shipped but the queue row was never struck-through. Propose: strike through the queue row + add the "✅ Shipped YYYY-MM-DD" pointer cell.
- Strike-through rows that say "✅ Shipped YYYY-MM-DD" but the handoff still says `status: active` → suggests the strike-through was added prematurely or the closing protocol didn't run. Propose: flip the handoff frontmatter to `consumed` with the date from the strike-through pointer, OR remove the strike-through if the chat hasn't actually shipped (operator decides which).
- Recently-closed rows pointing to handoffs still marked `status: active` → suggests the row was created but the handoff frontmatter never flipped. Propose: flip the handoff to `consumed` with the row's date.

**Step 8 — Detect FRONTMATTER ISSUES.**

For every referenced handoff:

- Consumed handoffs missing the `consumed:` date line → propose: add `consumed: <date>` (use the date from the tracker row).
- Consumed handoffs with neither `actual-deliverable:` frontmatter nor an "Actual deliverable" blockquote → propose: add a minimal actual-deliverable line drawn from the tracker row's outcome cell.
- Handoffs whose YAML doesn't parse → propose: a specific edit (usually un-quoted colon-space values, missing closing quotes, or unbalanced brackets in the tags list).
- Handoffs missing required fields (`type:`, `status:`, `created:`, `purpose:`, `tags:`) → propose: add the missing field.
- Handoffs whose `type:` is not `handoff` → flag for operator review (could be intentional if the file is a different note type that the tracker mis-references).

**Step 9 — Produce the drift report.**

Format per `references/drift-report-template.md`. If zero drift, use the empty-state shape — short, celebratory, no patches proposed.

**Step 10 — Propose patches in labeled batches.**

Group proposed patches into A, B, C batches per the batch-approval discipline. Sizing rules:

- Each batch is internally coherent — same target file or same category of edit
- Each batch is small enough that "approve the whole batch" is a reasonable unit
- Three batches is a healthy maximum; if you find yourself proposing more than four, consider merging
- Always include an "Out of scope (NOT proposing)" section even if empty — names what you considered and rejected

Surface the batches with the standard prompt: "Reply with batches to approve (e.g., 'A, B' or 'all' or 'A only, hold B and C')."

**Step 11 — Apply approved batches.**

For each approved batch:

1. Apply each edit in the batch
2. After all tracker edits in the batch land, re-run the YAML parse check
3. If YAML fails, revert the most-recent tracker edit and surface the error
4. Update the `last-change:` frontmatter with a one-paragraph summary of what this audit pass changed (wrapped in single quotes per the convention)
5. Report what landed

If the operator skips a batch, document it in the "Applied patches" section so the audit trail is honest.

### AUDIT worked example

**Operator:** "Audit my active chats."

**Skill response (abbreviated):**

```
# Tracker drift report — 2026-05-27 22:15

Tracker audited: ~/workspace/second-brain/_meta/handoffs/_active-chats-tracker.md
Tracker last-change timestamp: '2026-05-27 (late evening, fourteenth pass) — ...'
Audit scope:
- 0 rows in "Active / in-flight"
- 16 rows in "Recently closed" (past 14 days)
- 7 rows in "Ready to spawn next" (5 struck-through, 2 live)
- 2 rows in "Queued — Tier 2" (1 struck-through, 1 live)
- 11 rows in "Queued — Tier 3" (9 struck-through, 2 live)
- 3 scheduled Cowork tasks
- 16 rows in "Recently completed (past 7 days)"

YAML parse check: ✅ OK

Handoff files referenced: 28 total, 24 unique
Handoff files found on disk: 24
Handoff files missing on disk: 0

## Findings

### STALE in-flight rows

None — Active/in-flight is empty (per the most recent tracker pass).

### MISSING from tracker

None — every consumed handoff in the past 14 days has a matching Recently-closed row.

### STATUS DRIFT

None — every tracker row's state matches its handoff's frontmatter. Every "✅ Shipped 2026-05-27" strike-through row corresponds to a handoff with `status: consumed` and `consumed: 2026-05-27`.

### FRONTMATTER ISSUES

None — every referenced handoff has valid, complete frontmatter with required fields.

## ✅ Zero drift detected.

The tracker is healthy. Next audit recommended after the next significant tracker pass (after one or more chats ship).
```

In the live-test case, this is what the skill should detect — the tracker was just hand-audited fourteen passes earlier this evening, so a clean result is the right answer. A skill that reports drift here is broken; fix the logic before shipping.

## Mode 3 — NEXT-MOVE

### What NEXT-MOVE produces

A ranked list of spawnable candidates with reasoning per row, plus a recommended sequence over the next N moves (default N=4) with calendar-gate annotations.

The skill does not decide what's important — the operator does. The skill surfaces options with reasoning; the operator picks.

### NEXT-MOVE step-by-step

**Step 1 — Read the tracker.**

Read the tracker. Build the candidate set:

- Every live (non-struck-through) row in "Active / in-flight chats" — currently running, not candidates for spawning
- Every live (non-struck-through) row in "Ready to spawn next" — candidate set
- Every live (non-struck-through) row in "Queued — Tier 2" — candidate set if promotable (Tier-1 prerequisite shipped)
- Every live (non-struck-through) row in "Queued — Tier 3" — candidate set only if explicit trigger has fired

Exclude struck-through rows entirely. They're historical.

**Step 2 — For each candidate, evaluate six factors.**

For each candidate in the candidate set, evaluate:

**Blocker status.** Read the candidate's handoff. Read its prereqs. For each prereq, check the tracker — is it in "Recently closed"? If yes, blocker is cleared. If no, blocker is open (and the candidate isn't actually spawnable yet).

**Calendar gates.** Check the "Scheduled Cowork tasks" table — does any armed scheduled task fire before this candidate could spawn? Check the "Trigger to wait for" cell on Tier-3 rows — does any calendar date matter?

**File-collision risk.** Read the candidate's handoff. Identify the expected file paths the chat will touch (deliverable paths, edited files). Cross-reference against handoffs currently in-flight — would two concurrent chats write to overlapping paths?

**Cognitive-load risk.** How many chats are currently in-flight? Spawning this would bring the total to N+1. Above 3 concurrent chats, the operator starts losing track. Surface high-load risk explicitly.

**Downstream pull.** Read the candidate's prereq graph in reverse — which queued handoffs would this unblock? Higher unblock count = higher leverage.

**Operator-stated priority.** Check `MEMORY.md` for priority project memories (`project_priority_*` entries). Check recent chat history for operator signals about what they most want shipped next. Up-weight candidates that match stated priorities.

**Step 3 — Rank candidates.**

Rank by composite leverage. Heuristic weighting:

- Blocker cleared + no calendar gate + no collision = baseline (eligible)
- Above baseline: high downstream pull + operator priority match + low cognitive-load risk
- Below baseline: open blocker (not actually spawnable) or hard calendar gate (wait)

Ranking is a recommendation, not a verdict. The operator may have reasons (energy level, what they want to spend time on) the skill can't see.

**Step 4 — Produce the ranked list.**

Format:

```markdown
# Next-move recommendation — YYYY-MM-DD HH:MM

Tracker last-change: '<quote>'
In-flight count: N
Candidate count: M

## Ranked candidates

1. **<highest-leverage candidate>** — <one-line summary>
   Why: <downstream pull, no blockers, no collisions, operator priority match>
   Effort: <range>
   Unblocks: <list of handoffs this would unblock>
   Risks: <any concurrency / cognitive-load / collision concerns>

2. **<second-best candidate>** — <one-line summary>
   Why: <reasoning>
   Effort: <range>
   Unblocks: <list>
   Risks: <concerns>

3. ...

## Recommended sequence — next 4 moves

1. <candidate 1> — spawn now
2. <candidate 2> — spawn when candidate 1 lands
3. <candidate 3> — spawn after <calendar gate fires YYYY-MM-DD>
4. <candidate 4> — spawn after candidate 3 lands

Calendar gates noted:
- <date>: <task fires>; promotes <candidate> from queue
- <date>: <calendar trigger>; clears blocker on <candidate>
```

**Step 5 — Surface, don't apply.**

NEXT-MOVE is recommend-only in v1. It does NOT promote candidates, edit the tracker, or open new chats. The operator reads the recommendation and decides.

### NEXT-MOVE worked example

**Operator:** "What should I spawn next?"

**Skill response (abbreviated, based on the tracker as of 2026-05-27):**

```
# Next-move recommendation — 2026-05-27 22:30

Tracker last-change: '2026-05-27 (late evening, fourteenth pass)'
In-flight count: 0
Candidate count: 3 live spawnable

## Ranked candidates

1. **intel-routing-rollout Phase 3 — `intel-routing` skill build (Option C)** — Build the skill that automates the manual operations Phase 2 exercised
   Why: Phase 2 just shipped (2026-05-27) with five friction observations that are the design input. Building now while the observations are fresh costs less than rebuilding from memory later. Operator-stated priority: SEO + traffic-building for clients (memory `project_priority_client_seo_traffic`) — the intel-routing skill directly accelerates per-client intel triage, which feeds the SEO sprint cycle.
   Effort: 2-3 sessions (PUSH first, then PULL, then BOOTSTRAP)
   Unblocks: Every future per-project intel triage cycle. Future BOOTSTRAP for new client onboarding.
   Risks: None — no in-flight chats, no file collisions, low cognitive load.

2. **multi-chat-coordination skill** — Build the skill that organizes Cowork projects spanning multiple chats
   Why: Operator-requested 2026-05-27. No blockers. Spawn anytime. Currently in Tier-2 queue (this very chat may be it).
   Effort: 3-4 hours
   Unblocks: Future multi-chat coordination becomes deterministic instead of ad-hoc.
   Risks: None — no file collisions, low cognitive load.

3. **Phase 3d — generate-imagery-prompts.py** — Reads research briefs + owner reference photos; produces Higgsfield prompts per page
   Why: Blocker cleared 2026-05-27 (Phase 2c + house-voice both shipped). Concrete client-deliverable, fits the client SEO priority.
   Effort: ~3h
   Unblocks: Faster imagery iteration on EV Electric pages.
   Risks: None.

## Recommended sequence — next 4 moves

1. intel-routing Phase 3 — spawn now (highest leverage; operator priority match)
2. multi-chat-coordination skill — spawn after Phase 3's PUSH lands (or in parallel if cognitive load allows)
3. Phase 3d (generate-imagery-prompts) — spawn after Phase 3 ships (or in parallel)
4. Phase 4b (internal linking + competitor link map) — gated on DataForSEO unlocking 2026-06-03

Calendar gates noted:
- 2026-06-03 10am ET: `retry-dataforseo-business-signup` fires; clears blocker on Phase 4b
- 2026-06-03 10am ET: `build-watchdog-analysis-workflow` fires; new spawnable when Watchdog report arrives
- 2026-06-08 10am ET: `otterly-trial-conversion-decision` fires; operator decision, not a chat spawn
```

The operator reads, picks. If they pick something other than rank 1, that's a signal — either the operator's mental model has context the skill missed, or the leverage heuristic needs calibration. Surface that mismatch as a follow-up: "You picked rank 2 over rank 1. Anything I should learn from that for future recommendations?"

## Cross-mode behaviors

**Read all the references first.** Before invoking any mode, the skill reads:

- `references/tracker-row-shapes.md` — the data contract for the six tables
- `references/handoff-frontmatter-spec.md` — the frontmatter shape for handoff files
- `references/project-subfolder-template.md` — the `_README.md` shape for new project subfolders (DECOMPOSE)
- `references/drift-report-template.md` — the drift report format (AUDIT)
- `references/closing-protocol-template.md` — the seven-step protocol DECOMPOSE inserts into every generated handoff

Mode 1 uses all five. Mode 2 uses tracker-row-shapes, handoff-frontmatter-spec, drift-report-template. Mode 3 uses tracker-row-shapes plus the operator's `MEMORY.md` for priority signals.

**Plain language across every output.** The skill's reports, recommendations, and decomposition outputs all read as plain English — short sentences, concrete over abstract, conversational rhythm, technical terms kept when they're the right name for the thing. No jargon density, no AI-generated padding.

**Operator overrides win.** If the operator says "skip the closing protocol for this one" or "I want flat handoffs, no subfolder," honor that. The skill's defaults exist to enforce discipline; explicit operator overrides exist to handle the cases discipline didn't anticipate.

**Surface the work, don't bury it.** Every mode ends with a clear summary of what landed (or what would land, in the case of DECOMPOSE's review gate). No buried decisions, no silent edits.

## Out of scope (v1)

- **Auto-spawning chats.** v1 is recommend-and-approve only. The operator still manually opens new Cowork chats. Auto-spawn (skill literally invokes a new chat session) is risky and out of scope.
- **Cross-vault tracking.** The skill operates on `~/workspace/second-brain/_meta/handoffs/_active-chats-tracker.md` only. Tracking chats that touch other vaults (tier-3, future per-client vaults) is out of scope.
- **Editing execution logs.** The skill reads execution logs (to detect drift) but never writes to them.
- **Modifying handoff bodies.** AUDIT can flip a handoff's `status:` frontmatter and add the `consumed:` line + outputs note. It does NOT rewrite the handoff's prompt body — that's the human's job during the original chat.
- **Project-level priority decisions.** NEXT-MOVE recommends based on declared dependencies, calendar gates, and operator-stated priorities in memory. It does not decide what's important — the operator does.
- **Auto-archiving old rows.** The tracker's "rows older than 60 days move to a quarterly archive" rule stays operator-driven. The skill doesn't auto-archive.
- **Cross-initiative dependency synthesis.** The skill respects declared per-handoff prereqs but does not infer cross-initiative dependencies (e.g., "intel-routing Phase 3 will probably need the multi-chat-coordination skill to ship first" — that's an operator-altitude judgment, not a mechanical inference).

## Maintenance notes (for future skill iterations)

These are observations seeded at skill creation. Promote to standalone notes if they generalize.

**1. Watch for tracker section drift.** The tracker has six tables in a specific order. If a future hand-edit reorders sections or adds new sections, AUDIT's section-walk logic needs to update. Detection: if Step 1 (read the tracker) finds a section header the skill doesn't recognize, surface it as a finding.

**2. Watch for wikilink-resolution failures.** The skill resolves slug-only wikilinks to absolute paths. If a handoff is moved (e.g., promoted from standalone to project-folder), the wikilink target needs updating in the tracker. Detection: AUDIT's Step 3 (resolve handoffs) should log every failure as a FRONTMATTER ISSUES finding.

**3. Watch for closing-protocol drift.** The closing protocol is baked into `references/closing-protocol-template.md`. If the protocol evolves (new step added, existing step refined), update the reference file. DECOMPOSE always reads the current version and inserts verbatim — no stale copies floating around.

**4. Watch for plain-language drift in generated outputs.** Periodically spot-check DECOMPOSE-generated handoff bodies and AUDIT-generated drift reports against the voice rules in `_meta/plain-language-conventions.md`. If outputs start reading dense or padded, the skill prompt needs calibration.

**5. Watch for tier-classification drift.** DECOMPOSE assigns Tier 1 / 2 / 3 to each generated handoff based on prereq analysis. If the operator regularly overrides the tier assignment ("this is Tier 1, not Tier 3"), the heuristic needs calibration. Detection: track operator edits to the proposed tier during DECOMPOSE review gates.

**6. Watch for stale operator-priority signals.** NEXT-MOVE reads `MEMORY.md` priority memories. If a memory becomes stale (priority shifted, project closed), recommendations skew wrong. Detection: at the start of every NEXT-MOVE run, surface the priority memories the skill is reading from so the operator can flag staleness.

## Related

- `~/workspace/second-brain/_meta/handoffs/_active-chats-tracker.md` — the canonical tracker the skill operates on
- `~/workspace/second-brain/_meta/handoffs/_README.md` — the handoffs folder README
- `~/workspace/second-brain/_meta/conventions.md` — vault-wide naming and frontmatter rules
- `~/workspace/second-brain/_meta/plain-language-conventions.md` — voice rules every output follows
- `~/workspace/second-brain/_meta/handoffs/roadmap-client-seo-onboarding-automation/_README.md` — exemplar project subfolder (large)
- `~/workspace/second-brain/_meta/handoffs/perplexity-skill-build/_README.md` — exemplar project subfolder (medium)
- `~/workspace/second-brain/_meta/handoffs/intel-routing-rollout/_README.md` — exemplar project subfolder (small)
- `./references/tracker-row-shapes.md` — data contract for the six tables
- `./references/handoff-frontmatter-spec.md` — data contract for handoff files
- `./references/project-subfolder-template.md` — template for new project READMEs
- `./references/drift-report-template.md` — drift report format
- `./references/closing-protocol-template.md` — closing protocol baked into every generated handoff
