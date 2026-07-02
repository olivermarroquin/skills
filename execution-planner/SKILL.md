---
name: execution-planner
description: >
  Recurring vault state-of-play + execution-planning + tracker-hygiene skill. Reproduces the audit→clean→plan
  pass run by hand on 2026-06-16. In one run it (1) reads the whole handoff/tracker system, (2) DISK-VERIFIES the
  true status of every open handoff (truly-done vs partial vs not-started — never trusts tracker labels), (3) triages
  every open item for VALUE (flagging low-value / stale / superseded / deletable / convert-to-scheduled candidates),
  (4) cleans and organizes the active-chats tracker (remove shipped rows + write their closure records, flip stale
  frontmatter, move consumed files to complete/, promote unblocked downstream chats, reconcile counts) NON-DESTRUCTIVELY,
  collision-safely, and in FULL compliance with the Closing Protocol, (5) asks clarifying questions when scope or
  priority is ambiguous (plain text — never the AskUserQuestion tool), and (6) writes a dated execution plan to
  second-brain/_meta/handoffs/execution-plans/ with fixed sections, each retained item carrying a plain-language
  "what it does + impact." Composes vault-orchestrator (SURVEY + NEXT-MOVES), the gate-peer-reviewer disk-verify
  discipline, and the producer↔peer-review pairing convention. Runs every 3 days on a schedule, or on demand. Trigger
  phrases: "run the execution planner", "build today's execution plan", "what's next + clean the tracker", "do the
  3-day vault planning pass", "audit and plan the vault", "state of play + execution plan".
---

# Execution Planner (v1.1)

> **v1.1 (2026-06-16)** — Hardened after an independent adversarial review of v1.0. Added: a Value-triage step + a
> "Retire / low-value / convert-to-scheduled" plan section (operator-requested output that v1.0 dropped); plain-language
> "what it does + impact" required across EVERY item section, not just spawnable-now; full Closing-Protocol compliance
> in the cleanup step (write closure records to `_recently-closed.md`, NOT the changelog; promote unblocked downstream
> chats; run the anti-orphan invariant check; leverage `_drift-check.md`; use `update-tracker-last-change.py`); concrete
> last-run anchor + first-run handling; explicit AskUserQuestion prohibition; sub-agent cap + concise-return rule;
> required plan frontmatter; commit + multi-writer-diff guidance.
> **v1.0 (2026-06-16)** — Initial build codifying the manual 2026-06-16 audit→clean→plan pass.

## Purpose

The operator's recurring "where are we, what's real, what's worth doing, and what do I spawn next" pass. Without it,
the active-chats tracker drifts (rows say "ready" for work that already shipped; "consumed" for work that never landed;
frontmatter goes stale under heavy concurrent passes) and deciding what to spawn requires re-walking the whole vault by
hand. This skill turns that into a repeatable run that ends in one clean dated artifact plus a tidied, protocol-correct
tracker.

It is the **cadence layer** above `vault-orchestrator`: vault-orchestrator answers "state of the vault" / "what's next"
on demand and read-only; this skill adds the disk-verified truth audit, the value triage, the tracker *cleanup* (done
to Closing-Protocol spec), the clarifying-question loop, and the **persisted dated execution-plan artifact** — on a
schedule.

## When to run

- **Scheduled:** every 3 days (task `execution-planner-every-3-days`, cron `0 9 */3 * *` ≈ every 3rd day at 9am).
- **On demand:** anytime the operator asks (trigger phrases above).

## Substrate

- **Cowork** is the default — most of the work is reading the vault + writing the plan + light tracker edits.
- **Claude Code** if this run will also *commit* the cleanup (only Claude Code runs git). If run in Cowork, hand the
  operator a paste-ready commit block instead.
- State the substrate in any spawn prompt for this skill (substrate-in-every-spawn-prompt convention).

## Inputs to read (Step 1)

1. `~/workspace/CLAUDE.md` — session-start protocol, commit mechanics, stewardship rules, Closing Protocol.
2. `second-brain/_meta/handoffs/_drift-check.md` — the ~10-second Dataview drift surface (orphan handoffs, dangling
   tracker rows, consumed-handoffs-still-at-root). Read it FIRST as a fast pre-scan of where the drift is.
3. `second-brain/_meta/_event-log.md` — events since the last run (see last-run anchor below); also tells you whether
   any chat is currently live-writing the tracker (collision check).
4. `second-brain/_meta/handoffs/_active-chats-tracker.md` — Active / Ready / Tier-2 / Tier-3 / Scheduled / Hot decisions.
5. `second-brain/_meta/handoffs/_recently-closed.md` — what already closed (don't re-audit it).
6. The newest file in `second-brain/_meta/handoffs/execution-plans/` — **this is the last-run marker.** Diff against it.
7. Relevant `MEMORY.md` / project + feedback memories — operator preferences and hard-won rules.

**Last-run anchor + first run:** the newest `execution-plan-*.md` in `execution-plans/` is "last run"; compute the delta
from its date using `_event-log.md` rows since then. If no prior plan exists (first run), do a full from-scratch audit
and say so in the plan header.

## Procedure

### Step 1 — Orientation
Read the inputs above. Anchor on the newest prior plan so this run is a diff, not a rebuild. Note what the last plan
called "spawnable now" / "in flight" and check what changed.

### Step 2 — Disk-verified status audit (never trust tracker labels)
For every open handoff (Ready + Tier-2 + Tier-3) and every "in flight" row, verify the TRUE state ON DISK:
- Does the named deliverable exist (skill dir, script, vault file, repo)? Is it non-stub?
- "Consumed/done" claims: confirm the artifact is actually there and complete (counts counted from source, values
  cross-checked) — catch "marked done but not on disk" and "shipped but row never cleaned."
- "Ready/blocked" claims: confirm the blocker really is/ isn't cleared.
- Classify each: **truly done / partial (state "X of Y") / not started.** Treat partial honestly — no silent "done."

**Fan out, but bounded.** When there are many open handoffs, dispatch parallel sub-agents by cluster — **cap ≤5–6 per
run** (batch clusters if more). Each sub-agent returns a COMPACT structured block (status enum + evidence path + 1-line
plain-language status + impact + disposition), NOT raw file dumps, to protect main context.

### Step 2b — Value triage (operator-requested output)
For every open item, flag whether it is **low-value / stale / superseded / deletable / convert-to-scheduled**, with a
recommended disposition: keep · delete/archive · convert-to-scheduled-task · just-do-and-close (trivial) · defer. This
feeds plan Section 4b. (On 2026-06-16 this surfaced: stale review-gate duplicates → close; G5 → scheduled task; DA6 →
just-do; OR cluster → operator-judgment.) Capture the *why* for each.

### Step 3 — Collision safety (mandatory before ANY tracker edit)
The master tracker + `_recently-closed.md` are shared files. Before editing them, check the event log + Active section
for chats currently writing them. **If another chat is live-writing, do the read-only audit + produce the plan, but
HOLD the cleanup** and surface it as a proposed batch. Never edit the tracker concurrently with a producer chat.

### Step 4 — Tracker hygiene (NON-DESTRUCTIVE, Closing-Protocol-compliant, confirmation-gated for moves)
When safe (no concurrent writers) and approved, for each item verified shipped:
1. **Write its closure record to `_recently-closed.md`** — the full prose outcome paragraph AND the scannable
   "past-7-days" one-liner. (Closing Protocol step 3. This is the closure HISTORY — do NOT put it in the changelog.)
2. **Remove the row** from the tracker's Ready/Tier section (move, don't strikethrough). Move root handoff files to
   `complete/`; topic folders move only when 100% consumed.
3. **Flip frontmatter to the truth** (`active`→`consumed` for shipped; `active`→`queued` for not-actually-running).
4. **Promote unblocked downstream chats** — if a closure cleared a blocker, move that chat to Ready-to-spawn
   (Closing Protocol step 4).
5. **Reconcile section counts** + the `last-change:` one-liner (use `_meta/scripts/update-tracker-last-change.py` where
   applicable); **prepend a separate per-pass entry to `_active-chats-tracker-changelog.md`** (changelog = edit history,
   distinct from the closure records in step 1).
6. **Anti-orphan invariant check** — confirm afterward: every `active` handoff has an Active tracker row; every
   `queued` handoff has a Ready/Tier/Scheduled row; no `consumed` handoff is left at the handoffs root. Fix violations.
7. **Append an `_event-log.md` row.**
- **Batch discipline:** group >3 proposed moves into labeled batches (A/B/C) with target paths + one-line rationales;
  get operator approval. **Scheduled runs do NOT auto-execute moves or row removals** — they PROPOSE the batch in the
  plan's "proposed cleanup" note + Section 7 for the operator to approve on the next interactive turn. Safe frontmatter
  truth-flips on clearly-shipped items may be applied; file moves, row removals, and `_recently-closed` writes wait for
  approval on scheduled runs.

### Step 5 — Clarifying questions
If scope, priority, or an ambiguous status genuinely blocks a good plan:
- **Interactive run:** ask the operator in **plain text in the message body** (one or two high-value questions).
  **Never use the AskUserQuestion tool** — it glitches in Cowork (operator standing instruction).
- **Scheduled run (no live operator):** do NOT block. Make the most reasonable assumption, proceed, and surface the
  question in the plan's Section 7 (Open operator decisions).

### Step 6 — Write the dated execution plan
Write `second-brain/_meta/handoffs/execution-plans/execution-plan-<YYYY-MM-DD>.md` using the template below. Every
RETAINED item carries a one-line plain-language "what it does + impact (vault/client)". Plain language throughout; gloss
jargon. Slug-only wikilinks. New file per run (never edit an older dated plan). Get today's real date from the shell.

### Step 7 — Quality gate (practice the pairing convention)
Disk-verify the plan's own claims before declaring done. For a substantive run, run an independent QC (a sub-agent
reviewer, or recommend a paired peer-review chat per `_meta/templates/template-peer-review-chat.md`) — **no self-gate.**
Fix what it catches; re-verify.

### Step 8 — Commit (if applicable) + report
- **Commit (Claude Code only):** before committing the shared files (`_active-chats-tracker.md`, `_recently-closed.md`,
  the changelog, the new plan, moved files), run `git diff HEAD -- <file>` on each shared file to detect another chat's
  uncommitted edits (multi-writer check). Stage **by name** (never `git add .`), one block per repo, **operator pushes.**
  On Cowork, hand the operator a paste-ready commit block instead.
- **Report** in plain language: what's spawnable in parallel now, what's sequenced next + on what trigger, any new
  handoffs to author first, retire/low-value recommendations, what you cleaned (or proposed), and open decisions —
  with a link to the new plan file.

## Execution-plan section template (every plan uses these)

```
---
type: execution-plan
status: active
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
spawned-from: <chat-id or "execution-planner scheduled run">
tags: [execution-plan, handoffs, tracker-companion, waves, parallel-spawn]
---

# Execution Plan — <YYYY-MM-DD>     (note "FIRST RUN — full audit" if no prior plan)

## 0. In flight right now            (chats actively running: who / what / where)
## 1. Spawnable IN PARALLEL right now (no blockers + disjoint files; table: item | what it does + impact (plain) | substrate | zone)
## 2. Sequenced next                 (table: item | what it does + impact (plain) | waits on | then it does)
## 3. New handoffs to AUTHOR first   (foundation ready but no handoff yet; each: what it does + impact + why author now)
## 4. On hold / gated                (don't spawn; name the gate; one-line what it does)
## 4b. Retire / low-value / convert  (table: item | why low-value/stale/superseded | recommendation: delete | archive | convert-to-scheduled | just-do-and-close | defer)
## 5. Done / closed this pass        (cleanup + completions record; or "PROPOSED cleanup batch (awaiting approval)" on scheduled runs)
## 6. Pass structure                 (Pass 1 / Pass 2 / Pass 3 — how it'll actually execute)
## 7. Open operator decisions        (questions needing the operator; mark RESOLVED when answered)
## 8. Dependency map                 (what unblocks what)
## Related                           (tracker, recently-closed, key handoffs — slug-only wikilinks)
```

## Conventions this skill obeys

- **Disk-verify, never trust labels**; treat silent skips as defects (fail loud + track).
- **Closing-Protocol-correct:** closures → `_recently-closed.md`; per-pass edits → changelog; promote unblocked
  downstream; anti-orphan invariant holds after every cleanup.
- **Non-destructive**; never move/rename/delete in `second-brain/` without confirmation.
- **Collision-safe:** never edit the tracker/`_recently-closed` while another chat is writing them; `git diff HEAD`
  before committing shared files.
- **Batch approval** for >3 moves; **scheduled runs propose, don't auto-move.**
- **Plain language** everywhere (gloss jargon). **Never the AskUserQuestion tool** — plain-text questions.
- **Slug-only `[[wikilinks]]`**; new subfolder ⇒ write its `_README` + update the parent's; new file cross-links a
  parent + a peer.
- **Event-log row** on every significant edit. **No self-gate** — independent QC on substantive runs.

## Composition (don't rebuild these)

- `vault-orchestrator` SURVEY (state read) + NEXT-MOVES (leverage ranking) — sections 0–2.
- `gate-peer-reviewer` + `references/independent-reviewer-mandate.md` — disk-verify + QC discipline (Step 7).
- `multi-chat-coordination` — parallel-vs-serial detection feeding Section 1 vs 2.
- `_meta/templates/template-handoff.md` + `template-peer-review-chat.md` — when Section 3 says "author a handoff."
- `_meta/handoffs/_drift-check.md` + `_meta/scripts/update-tracker-last-change.py` — existing drift surface + helper.

## Scheduling

Registered via the `scheduled-tasks` MCP (`create_scheduled_task`) / the `schedule` skill as
`execution-planner-every-3-days`, cron `0 9 */3 * *` (≈ every 3rd day at 9am; cron has no exact 72h interval — this is
the standard day-interval approximation). Scheduled runs are Cowork and therefore PROPOSE cleanup (no auto-moves).

## Related

- `second-brain/_meta/handoffs/_active-chats-tracker.md` · `.../execution-plans/_README.md` · `.../_recently-closed.md` ·
  `second-brain/_meta/handoffs/_README.md` (pairing convention + Closing Protocol) · `.../_drift-check.md` ·
  `skills/vault-orchestrator/SKILL.md` · `skills/gate-peer-reviewer/SKILL.md`
