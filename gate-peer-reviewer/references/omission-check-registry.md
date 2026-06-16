---
type: reference
skill: gate-peer-reviewer
skill-version: 3.6
created: 2026-06-15
updated: 2026-06-15
gate-type: G-chat-close
registry-discipline: append-only — every operator-caught gap becomes a new OC row, incident cited
supersedes-drafts:
  - second-brain/_meta/handoffs/review-gate-hardening/spec-omission-check-profiles.md (draft, retained)
  - second-brain/_meta/handoffs/review-gate-hardening/spec-g-chat-close-gate-type.md (draft, retained)
tags: [reference, gate-type-registry, omission-checks, profiles, g-chat-close, chat-completeness, substrate-agnostic]
---

# Omission-check registry + per-chat-type profiles (G-chat-close)

The **G-chat-close** gate's verification surface. Every check is disk-verifiable (`ls`/`grep`),
`$0`/no-LLM, and traces to a real caught incident. The registry is append-only: every
operator-caught gap after a gated close becomes a new OC row (the compounding rule).

> **Shipped by [RGH-6]** (`rgh6-g-chat-close-omission-audit-202606151200`). Draft specs
> retained at `second-brain/_meta/handoffs/review-gate-hardening/spec-g-chat-close-gate-type.md`
> + `spec-omission-check-profiles.md` for lineage.

---

## A. The omission-check registry (OC rows — append-only)

### OC-1: Execution log exists

**Check:** Multi-step chat (3+ steps, external systems touched, or multi-session) has a
non-placeholder execution log.

**Procedure:**
1. Determine expected path: `repos/<venture>/.kos/execution-logs/execution-log-YYYY-MM-DD-<topic>.md`
   OR `second-brain/_meta/execution-logs/exec-log-YYYY-MM-DD-<topic>.md` (for non-venture chats).
   Also check `second-brain/_meta/handoffs/<project>/execution-log-*.md`.
2. `ls` the expected path(s). If no file matches → BLOCKING.
3. `grep` for substantive sections (## What happened, ## Decisions, ## D-rows). If only
   frontmatter or a stub body → BLOCKING.

**Seed incident:** [WF-1] 06-12 gap #1; S&H wave A2 06-03; per `feedback_running_execution_log_default`.

---

### OC-2: Knowledge Capture Audit ran

**Check:** A D-row exists for every surprise/failure/reversal the chat's records show; lesson
file exists if any D-row generalizes.

**Procedure:**
1. Read the execution log. Scan for D-rows / KCA section.
2. Grep the event-log for this chat's ID — extract surprises, failures, reversals named there.
3. For each surprise/failure without a corresponding D-row → BLOCKING.
4. For any D-row flagged as generalizing beyond this project, check
   `second-brain/05_shared-intelligence/lessons/` for a corresponding lesson file.

**Seed incident:** [WF-1] gap #2; S&H wave A2 (3 D-rows missing until asked).

---

### OC-3: Owner-dependent decisions are tracked

**Check:** Every decision/question requiring operator or client action is on a tracked surface.

**Procedure:**
1. Grep produced artifacts for owner-action markers:
   `"operator owns"`, `"ask <name>"`, `"TBD (operator)"`, `"pending <name>"`,
   `"owner decision"`, `"client decision"`, `"Ahmad"`, `"Mohammad"`, `"Oliver"`.
2. For each hit, verify it has a tracking row on one of:
   - Client `_punchlist.md`
   - Tracker Hot-decisions section
   - A scheduled task
   - The execution log's open-items section
3. Any untracked owner-dependent decision → BLOCKING.

**Seed incident:** [WF-1] gap #3 (Ahmad booking/financing/multi-GBP questions lived only in handoff bodies).

---

### OC-4: Memory staleness pass (Cowork-only)

**Check:** Project memories whose gating claims had their events fire this chat are updated.

**Procedure:**
1. `grep MEMORY.md` for memories naming this chat's project.
2. For each memory with gating language ("gated behind X", "pending Y", "blocked on Z"),
   check whether the gate/event has been met.
3. Any stale gating claim → WARN (fix is one edit).

**Substrate:** Cowork-only. Claude Code reports `skipped (substrate: claude-code — cannot read Cowork memories)`.

**Seed incident:** [WF-1] gap #4 (`project_website_factory_program` still said "gated behind Core 30").

---

### OC-5: Stat provenance + retraction scan

**Check:** Every numeric claim traces to a source artifact, and the source carries no retraction.

**Procedure:**
1. Grep produced artifacts for numeric claims (percentages, counts, dollar amounts, dates
   with metrics attached).
2. For each, identify the cited source artifact.
3. Open each source; scan for retraction markers: `"do not present"`, `"retracted"`,
   `"correction:"`, `"OBSOLETE"`, `"superseded by"`.
4. Any retracted/unverifiable stat presented → BLOCKING.

**Seed incident:** [WF-1] D-01 (retracted 84%-GSC stat from an event-log row); `feedback_verify_stats_against_source_retractions`.

---

### OC-6: Recommended recurring actions are armed

**Check:** Any "monthly / weekly / re-check on DATE" recommendation has a scheduled task or
explicit operator deferral.

**Procedure:**
1. Grep produced artifacts for cadence/recheck language:
   `"monthly"`, `"weekly"`, `"quarterly"`, `"re-check"`, `"revisit"`, `"recheck on"`,
   `"monitor"`, `"recurring"`.
2. For each hit, check the scheduled-tasks list + tracker Scheduled section.
3. Any unarmed recommendation without an explicit deferral → WARN.

**Seed incident:** [WF-1] (AJ Long + Root Electric monthly ranking monitor recommended, never armed).

---

### OC-7: Event-log completeness

**Check:** Every significant state change has an event-log row with this chat's ID.

**Procedure:**
1. Enumerate significant edits: tracker pass bumps, handoff status flips, skill version bumps,
   credential landings, promotions, registrations.
2. `grep <chat-id> second-brain/_meta/_event-log.md` — list all rows.
3. Diff: any significant edit without an event-log row → BLOCKING.

**Seed incident:** CLAUDE.md event-log contract; anti-orphan incidents ([G6] orphaned at creation, pass 147).

---

### OC-8: Closing Protocol full compliance

**Check:** Tracker counts updated, rows MOVED not struck through, closure rows in
`_recently-closed` (both prose + one-liner), downstream-unblock promotion check ran, YAML parses.

**Procedure:**
1. Verify Active count in callout matches actual table rows.
2. Verify no strikethrough pointers left in prior sections.
3. `grep` `_recently-closed.md` for this chat's closure row (both full paragraph + one-liner).
4. If this chat cleared a downstream blocker, verify the downstream chat was promoted.
5. Run YAML parse check on tracker + `_recently-closed`.
6. Cosmetic count drift (off by one) → WARN. Missing closure row → BLOCKING.

**Seed incident:** Tracker protocol; stale-row incidents (pass 145 prune; [WF-1] stale spawn-queue rows).

---

### OC-9: Handoff-deliverables diff

**Check:** Every deliverable named in the originating handoff exists on disk, non-placeholder.

**Procedure:**
1. Read the originating handoff's deliverables/DoD section.
2. Include any operator-approved edits to the plan (noted in the execution log or chat records).
3. `ls` + `grep` each deliverable for existence + non-placeholder content.
4. Missing deliverable → BLOCKING.

**Seed incident:** Closing Protocol step 1, mechanized; [WF-1] operator edits 1-4 verification.

---

### OC-10: Version paperwork

**Check:** Any SKILL.md or registered-tool edit carries a version bump, changelog entry, and
event-log row.

**Procedure:**
1. Identify all SKILL.md files touched (from dirty ledger or execution log).
2. For each, verify:
   - `version:` in frontmatter bumped vs prior value
   - Changelog entry in version history section
   - Event-log row with the version bump
3. Missing any of the three → BLOCKING.

**Seed incident:** competitor-deep-research v1.1 close (missing version paperwork, caught by operator 06-03).

---

### OC-11: Silent-skip / orphaned-promise sweep

**Check:** Everything marked "deferred / later / I'll also" is done, tracked, or explicitly
surfaced as open.

**Procedure:**
1. Grep execution log + produced artifacts for deferral language:
   `"deferred"`, `"later"`, `"I'll also"`, `"TODO"`, `"will also"`, `"follow-up"`,
   `"next session"`, `"deliberately open"`.
2. The execution log MUST carry a "deliberately open items" or "open questions" section.
3. For each deferred item, verify it names its tracking surface (tracker row, punchlist,
   scheduled task, or the open-items section itself).
4. Any orphaned promise → BLOCKING.

**Seed incident:** `feedback_verify_live_not_vault_and_no_silent_skips`; [WF-1] exec-log open-items pattern.

---

### OC-12: Per-deliverable existence + non-stub (Layer A — deterministic)

**Check:** Every deliverable in the handoff's DoD manifest exists on disk, non-empty, no
placeholder/FILL body, real values present.

**Procedure (built by [RGH-7] — cite, don't rebuild):**
1. Walk the DoD manifest (the handoff's `## Definition of Done (machine-checkable)` section,
   per [[spec-definition-of-done-manifest|RGH-7 spec]]).
2. For each row: `ls` the path/glob → verify exists.
3. Check `size > 0`.
4. Grep for placeholder markers: `FILL:`, `<!-- MISSING`, `TBD`, `TODO`, `{placeholder}`.
5. "X captured" count is NOT evidence for "deliverable Y exists" — each deliverable verified
   independently.

**Note:** Until [RGH-7] ships the DoD manifest contract, fall back to OC-9 (handoff-deliverables
diff) for the deliverable enumeration. OC-12 adds the non-stub + real-values assertion on top.

**Seed incident:** COA-4b C-11 (fabricated SingleFile), C-14 (empty form fields), C-18/C-19 (unshipped criteria).

---

### OC-13: Count-reconciliation against the SOURCE (Layer A — deterministic)

**Check:** Every count assertion reconciles against a named source fetched fresh; total never
exceeds the source; manifest claims equal on-disk reality.

**Procedure (built by [RGH-7] — cite, don't rebuild):**
1. For each count claim in produced artifacts, identify the named source
   (live sitemap, spec list, canonical reference path).
2. Fetch/read the source fresh (not from the producer's work-list).
3. Assert `count == source` or `count <= source_count`.
4. `captured > source_count` → BLOCKING (C-17 class: 84 of 43).
5. **OC-13b (manifest/disk consistency):** for any claim in a manifest ("skipped", "exported",
   "N items"), verify the claim matches on-disk reality.

**Applies to:** build / research / production-fire profiles.

**Seed incident:** COA-4b C-12/C-13/C-16 (incomplete vs source), C-17 (84 of 43), C-15 (manifest
says skipped, export exists), C-20 (value vs canonical).

---

### OC-14: Rename-propagation completeness (Layer A — deterministic)

**Check:** After any identifier rename, zero stale references remain in LIVE paths.

**Procedure (built by [RGH-7] — cite, don't rebuild):**
1. Identify the old name and new name from the chat's records.
2. Grep old-name across ALL paths in the workspace.
3. Apply a historical allowlist (exclude from flagging):
   - `second-brain/_meta/_event-log.md`
   - `_active-chats-tracker-changelog.md`
   - `_recently-closed.md`
   - `execution-logs/` (historical records)
   - Consumed handoffs (status: consumed)
   - Lineage notes
4. Any live hit outside the allowlist → BLOCKING.

**Fires on:** any chat that renames an identifier (skill rename, file move, slug change).

**Seed incident:** COA-4b C-03 (dead path in program handoff), C-04 (stale registry),
C-05/C-08/C-09/C-10/C-25 (stale live forward-refs).

---

### OC-15: Frontmatter freshness (Layer A — deterministic)

**Check:** Every file the chat touched that carries an `updated:` field has it bumped to today.

**Procedure (built by [RGH-7] — cite, don't rebuild):**
1. Enumerate all files touched by this chat (from dirty ledger or execution log).
2. For each file with an `updated:` YAML frontmatter field:
   - Read the current value.
   - Assert `updated == <today's date>`.
3. Full sweep, not spot-check — the COA-4b close checked 2 files, missed 3 of the same class.
4. Any stale `updated:` → WARN (fix is one edit; BLOCKING if ≥3 stale).

**Seed incident:** COA-4b C-24 (changelog/coverage-matrix/toolkit-reuse-map stale after edit).

---

### OC-16: Commit-staging audit (Layer A — deterministic)

**Check:** The commit stages exactly the chat's touched files — no foreign chat's deliverables,
no omitted artifacts, rename deletions staged, no build artifacts.

**Procedure (built by [RGH-7] — cite, don't rebuild):**
1. Run `git status` in each repo touched.
2. Diff against the dirty ledger (or execution log artifact list):
   - **Staged-not-touched (foreign):** file staged that this chat didn't produce → flag.
   - **Touched-not-staged (omitted):** file this chat produced that isn't staged → flag.
   - **Rename deletions:** if a rename occurred, the old-path deletion must be staged.
   - **Build artifacts:** `__pycache__/`, `*.pyc`, `node_modules/`, `.DS_Store` → flag.
3. Any foreign-staged or omitted-artifact → BLOCKING.

**Trigger timing:** OC-16 cannot run at Closing Protocol step 0 (which fires before commits
exist). In the current manual-dispatch path, OC-16 is always DEFERRED at gate time. Its real
trigger is **commit-time**: a `pre-push` hook (RGH-2, Tier B) or RGH-5 post-commit independent
dispatch. Until one of those ships, OC-16 is a documented silent gap in the manual path —
the operator's commit-block review is the backstop.

**Seed incident:** COA-4b C-21 (staged MI-1's deliverables), C-22 (omitted review log),
C-23 (rename deletions unstaged), C-07 (pycache committed).

---

## B. Per-chat-type profiles (classification → check set)

### Classification logic

1. Read the originating handoff's `type:` and `tags:` frontmatter fields.
2. Match against the profile signals below.
3. **Ambiguous/hybrid chats take the UNION** of matching profiles (err toward more checks).
4. **OC-14 (rename-propagation) fires on any chat that renames an identifier** — not tied
   to a profile; triggered by the rename action itself.

### Universal checks (run on ALL profiles including micro)

OC-7 (event-log completeness), OC-8 (Closing Protocol compliance), OC-9 (handoff-deliverables
diff), OC-11 (silent-skip sweep), OC-12 (per-deliverable existence), OC-15 (frontmatter
freshness), OC-16 (commit-staging audit — **deferred at step-0 time**; runs at commit-time
via pre-push hook or RGH-5 post-commit dispatch; see OC-16 trigger-timing note).

### Profile table

| Profile | Identifying signals | Adds (on top of universal) | Expected artifacts (disk-verified) |
|---|---|---|---|
| **planning / decision** | handoff tagged planning/strategy; PROVISION run; decision slate | OC-1, OC-2, OC-3, OC-4, OC-5, OC-6 | decision record · exec log · PROVISION'd handoffs + queue rows + tracker rows · punchlist/Hot-decisions rows for owner-dependent items |
| **build** (pages/sites/tools/skills) | code/artifact production; publishes; repo edits | OC-1, OC-2, OC-5, OC-6, OC-10, OC-13 | exec log · per-task build-log entries · pattern candidates noted · live-verify evidence · zero-hardcoded proof where DoD names it |
| **research / extraction** (VIS, teardowns, deep-research) | source ingestion; dossiers; briefs | OC-1, OC-2, OC-5, OC-13 | source notes/dossier with retained raw evidence · intel-routing fields · quality-loop verdicts · synthesis cross-links |
| **production-fire / deployment** | live-state changes (publish, GSC, DNS, cache, payments) | OC-1, OC-2, OC-3, OC-5, OC-6 + full 6-item KCA | exec log with live-verification evidence · `_deployment-status.md` ledger sync · D-rows for every surprise |
| **skill-build** | creates/bumps a skill | OC-1, OC-2, OC-10 | SKILL.md + references on disk · version paperwork · second-config/second-target proof where DoD names it · toolkit-reuse-map sync · lesson file |
| **micro** (single small artifact, <30 min, no state flips) | trivial edits | universal checks only (fast-path) | the artifact itself |

---

## C. Severity + verdict mapping

### BLOCKING (gate does not pass)
- Missing expected artifact with no surfaced deferral (OC-1, OC-2, OC-9, OC-12)
- Untracked owner-dependent decision (OC-3)
- Retracted/unverifiable stat presented (OC-5)
- Missing version paperwork on a shipped skill (OC-10)
- Orphaned promise with no tracking surface (OC-11)
- Missing event-log row for significant state change (OC-7)
- Foreign-staged or omitted artifact in commit (OC-16)
- Stale live reference after rename (OC-14)
- Count exceeds source (OC-13)

### WARN (pass with findings — fix before declaring done)
- Stale memory (OC-4 — fix is one edit)
- Unarmed recurring recommendation with a named excuse (OC-6)
- Cosmetic protocol drift — count off by one (OC-8)
- 1-2 stale `updated:` frontmatter fields (OC-15)

### Verdict mapping to return contract
- Zero catches → `PASS`
- Any BLOCKING catch → `BLOCKING` (chat fixes omissions, re-runs)
- WARN-only catches → `PASS` with findings listed in `catches[]`

---

## D. How to run G-chat-close (the procedure)

### Step 1: Classify the chat

Read the originating handoff's frontmatter (`type:`, `tags:`). Match against the profile
table (§B). Ambiguous → UNION. Record the matched profile(s).

### Step 2: Assemble the check set

Start with the 7 universal checks (OC-7/8/9/11/12/15/16). Add the profile-specific checks.
If the chat renamed an identifier, add OC-14. Record the full check set.

### Step 3: Gather inputs

- **Originating handoff** (for OC-9, OC-12 deliverable enumeration)
- **Execution log** (for OC-1 existence, OC-2 D-rows, OC-11 open items)
- **Event-log rows** for this chat's ID (for OC-7)
- **Dirty ledger** (Claude Code) or execution-log artifact list (Cowork) for OC-15/OC-16
- **Produced artifacts** (for OC-3/5/6 content scanning)
- **Tracker state** (for OC-8 protocol compliance)

### Step 4: Run each check

Execute each check's procedure in order. For each:
- Record the check ID, what was verified, and the result (PASS / BLOCKING / WARN / SKIPPED).
- For SKIPPED: state the reason (e.g., "OC-4: skipped — substrate: claude-code").
- For BLOCKING/WARN: describe the finding with specifics (file path, missing item, stale value).

### Step 5: Produce the verdict

Aggregate per §C severity mapping. Emit the standard gate-peer-reviewer return contract:

```json
{
  "verdict": "PASS|BLOCKING",
  "checks_run": [
    {"name": "OC-1-exec-log", "result": "PASS|BLOCKING|WARN|SKIPPED", "detail": "..."},
    {"name": "OC-2-kca", "result": "...", "detail": "..."}
  ],
  "catches": [
    {"check": "OC-N", "severity": "BLOCKING|WARN", "finding": "..."}
  ],
  "cost_usd": 0.0
}
```

Write verdict file to `.review-gate/state/verdict-G-chat-close-<timestamp>.json`.

---

## E. Honest limits

1. **Catches known gap classes only.** Novel omissions still need the human question once —
   then they become an OC row (the compounding rule, §A preamble). A checklist auditor is
   convergent but not complete on day one.

2. **OC-4 is Cowork-only.** Claude Code cannot read Cowork memories. Report
   `skipped (substrate)`, never drop silently.

3. **Producer dispatches its own audit until [RGH-5] ships.** Weaker than independent
   dispatch — the same structural limit as the Phase-1 self-claim marker, narrowed to
   omission checks. The verdict file + operator spot-checks are the integrity backstop.
   [RGH-5]'s mandate auto-dispatches G-chat-close under independent review.

4. **OC-12..16 procedures are built by [RGH-7].** Until [RGH-7] ships, OC-12 falls back to
   OC-9's deliverable enumeration (handoff body, not a DoD manifest); OC-13/14/15/16 run
   their grep/ls procedures directly (the check logic is defined above; [RGH-7] wraps them
   in scripts). The checks fire regardless — [RGH-7] makes them cheaper and scriptable.

5. **No API cost.** All checks are vault reads + greps. Target <5 min wall-clock per close.
   This gate must be affordable enough to run on literally every close ([RGH-5] cost constraint).

---

## F. Compounding rule

Every gap the operator catches by hand after a gated close becomes a new OC row in this
registry, with the incident cited. The registry is append-only. The system's job: make sure
no gap class is ever caught by hand twice.

---

## Related

- [[gate-type-registry]] — G-chat-close registered there
- [[../../second-brain/_meta/handoffs/review-gate-hardening/spec-g-chat-close-gate-type|spec-g-chat-close-gate-type]] (draft, retained for lineage)
- [[../../second-brain/_meta/handoffs/review-gate-hardening/spec-omission-check-profiles|spec-omission-check-profiles]] (draft, retained for lineage)
- [[../../second-brain/_meta/handoffs/review-gate-hardening/handoff-2026-06-12-phase-6-g-chat-close-omission-audit|RGH-6 build handoff]]
- [[../../second-brain/_meta/handoffs/review-gate-hardening/handoff-2026-06-11-phase-5-independent-reviewer-dispatch|RGH-5]] (mandate amended to require G-chat-close)
- [[../../second-brain/_meta/handoffs/review-gate-hardening/spec-definition-of-done-manifest|RGH-7 DoD manifest spec]] (OC-12..16 procedures)
- [[../../second-brain/_meta/handoffs/website-factory/execution-log-2026-06-11-wf1-program-planning|WF-1 exec log]] (seed corpus #1)
- [[../../second-brain/_meta/handoffs/review-gate-hardening/evidence-2026-06-15-coa4b-25-catch-replay-corpus|COA-4b evidence]] (replay corpus #2)
