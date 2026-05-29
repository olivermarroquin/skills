# Operator controls (Mode 5)

How the operator steers the auto-approve gate, the escalation queue, and the per-type thresholds. Every Mode 5 behavior is operator-overridable; nothing in the loop is a forcing function the operator can't escape.

This is the operator manual for Mode 5. The behavior spec lives in `../SKILL.md` § Mode 5; the math lives in `confidence-calibration.md`; the audit-trail shape lives in `folder-quality-log-shape.md`.

---

## 1. How to override auto-approve

By default, when a PASS verdict's confidence score is at or above the per-type auto-approve threshold (see `confidence-calibration.md`), Mode 5 ships the artifact without operator review — the publish gate (Phase 3) reads the `last-verdict: PASS` field and proceeds.

### Force escalation on a PASS that would otherwise auto-ship

Paste either flag into the original quality-check invocation, or into a fresh "re-gate this artifact" invocation:

```
quality-check <artifact-path> --force-escalate
quality-check <artifact-path> --no-auto-approve
```

Both flags do the same thing. The verdict is still recorded as PASS; the confidence score is still computed and written; the artifact is added to the light-escalation notification queue (see § 5) rather than auto-shipping. Use this when:

- A PASS landed at 96 confidence on a Core 30 page, but you know the client mentioned a constraint the loop didn't see (a brand-name they don't use anymore, a city they don't service).
- The artifact is being published for the first time and you want eyes on it regardless of confidence.
- The producing chat used a non-canonical voice or a fresh template the loop hasn't seen before.

### Force auto-ship on a below-threshold PASS

```
quality-check <artifact-path> --bypass-confidence
```

The verdict is PASS, the confidence score is computed and written, the artifact ships even if the score is below the per-type threshold. Use this rarely — once an artifact ships at low confidence, the operator owns the outcome. The override is recorded in the folder log under `### Operator override` so the audit trail captures the decision.

The bypass does NOT propagate to downstream artifacts produced from this one. Each artifact carries its own gate.

### Bypass the whole quality loop

Pre-existing flag from Phase 5:

```
quality-check <artifact-path> --bypass-quality-loop
```

This skips Mode 1 entirely. No verdict is computed, no confidence is computed, no folder log entry is written beyond the bypass record. Use this for genuinely-non-evaluable artifacts (binary outputs ridden on a sibling artifact's verdict, throwaway scratch files). The bypass record lands at `<folder>/_quality-log.md` § `### Bypassed (manual override) — YYYY-MM-DD` per the Phase 5 convention.

---

## 2. How to manually escalate

The operator can force any artifact into the hard-escalation queue regardless of its verdict, confidence, or iteration count.

```
quality-check <artifact-path> --escalate "<reason>"
```

A hard-escalation file lands at `_meta/escalations/escalation-YYYY-MM-DD-<artifact-slug>.md` with the operator's reason. A tracker row lands in `_active-chats-tracker.md` § "Hot decisions sitting on Oliver's plate" the same pass.

Use this when the loop says PASS but you want the escalation paper trail anyway — for example, a high-stakes client artifact where the explicit decision-record is more important than the auto-ship efficiency.

---

## 3. How to adjust per-type thresholds

The thresholds live in `confidence-calibration.md` § "Per-artifact-type calibration." The operator edits the file directly.

### Workflow

1. Open `references/confidence-calibration.md`.
2. Edit the Auto-approve threshold column for the type you want to retune.
3. Save.
4. Add a row to the Calibration history table at the bottom of the file with:
   - Today's date
   - Author: `operator-adjusted`
   - Change: one-line summary (`Raised Core 30 threshold 95 → 97 after panel-upgrade-vienna-va auto-shipped a fact error`)
   - Trigger: the event that motivated the change

The next Mode 5 invocation reads the table fresh and applies the new threshold. No restart required.

### When to adjust without waiting for the quarterly refresh

The triggered-refresh rules live in `confidence-calibration.md` § "When to recalibrate." The headline rules are:

- Operator overrides cross 10% on a type (the threshold is wrong; tune it)
- An auto-shipped artifact produces a post-ship correction within 48 hours (lower the threshold on that type)
- A new artifact type appears in the routing table (add a row with conservative starter anchors)

### Anchors vs threshold

The threshold is what gates auto-ship. The anchors (PASS-confidence anchor, REVISION-confidence anchor, FAIL-confidence anchor) shape the score's starting point before the five-input weighting fires. Edit anchors only if a type's verdicts are systematically over- or under-scoring against operator judgment — that's a deeper calibration than threshold tuning.

---

## 4. How escalations clear

Two queues. Different clearing workflows.

### Light escalation (low-confidence PASS, NEEDS REVISION below the auto-revise threshold)

**Where it lands:** the producing chat's folder gains (or extends) `_escalation-queue.md`. Each row is one artifact awaiting operator review. Format per § 5 below.

**How to clear:**

1. Open the `_escalation-queue.md` file in the folder.
2. For each row, decide one of: **ship anyway** / **revise** / **regenerate from scratch** / **deprecate**.
3. Move the row from the "Awaiting review" section to the "Resolved" section, adding a one-line note: `Resolved YYYY-MM-DD — <decision> — <one-line rationale>`.
4. If the decision was "revise," apply edits and re-invoke `quality-check <artifact-path>` to produce a fresh verdict.

The `_escalation-queue.md` file is per-folder and lightweight — no folder gets a queue file until at least one light escalation lands there. Empty queues stay un-created.

### Hard escalation (FAIL verdict, 3-iteration stall)

**Where it lands:**

1. `_meta/escalations/escalation-YYYY-MM-DD-<artifact-slug>.md` — full diagnostic per the shape in `_meta/escalations/_README.md`
2. `_active-chats-tracker.md` § "Hot decisions sitting on Oliver's plate" — visible at-a-glance row referencing the escalation file

**How to clear:**

1. Open the escalation file. Read the diagnostic.
2. Decide one of: **override and ship** / **edit the artifact directly** / **extend the spec source so the producing chat has clearer guidance** / **regenerate from scratch with the spec extension** / **deprecate the artifact entirely**.
3. Apply the decision.
4. Edit the escalation file: change frontmatter `status: open` → `status: resolved`; add a `## Resolution` section with the decision + rationale + date.
5. Remove the row from the master tracker's "Hot decisions" section.
6. If the artifact was edited or regenerated, re-invoke `quality-check <artifact-path>` to produce a fresh verdict.

Resolved escalations stay in `_meta/escalations/` as audit trail. Don't delete; rename in place by flipping the status field.

### Clearing escalations in bulk

For sweeps that touch more than 3 escalations at once, the operator can use the multi-chat-coordination skill's AUDIT mode (`audit escalations`) which surfaces all open escalations in a single A/B/C batch view per the operator's batch-approval preference. Same workflow as above but applied in batches.

---

## 5. Escalation file and queue shapes

### Light escalation row shape

Per row in `<folder>/_escalation-queue.md`:

```markdown
## Awaiting review

### <artifact-slug>
- **Verdict:** PASS | NEEDS REVISION (minor) | NEEDS REVISION (substantive)
- **Confidence:** 78 (threshold 85 for type `tactic-note` — below by 7)
- **Path:** `<absolute-path>`
- **Folder log:** [[_quality-log#<artifact-slug>]]
- **Revision prompt:** `<artifact-path>.revision-prompt.md` (when verdict ≠ PASS)
- **Recommended action:** ship | revise | regenerate
- **Why escalated:** confidence below auto-approve threshold | high-stakes dimension partial | operator forced

(repeat per artifact)

## Resolved

### <artifact-slug>
- Resolved YYYY-MM-DD — shipped — confidence borderline but operator hand-checked the citations
```

### Hard escalation file shape

Per `_meta/escalations/escalation-YYYY-MM-DD-<artifact-slug>.md`:

```markdown
---
type: escalation
status: open
created: YYYY-MM-DD
artifact-path: <absolute-path>
artifact-type: <type>
verdict: FAIL | NEEDS REVISION (3-iter stall)
confidence: <0-100>
iteration-count: 3
tags: [escalation, quality-loop, <artifact-type>]
---

# Escalation — <artifact-slug>

**Reason:** FAIL on first iteration | 3-iteration stall on NEEDS REVISION | operator-forced

## Verdict summary

Quoted from the folder log's iteration entry — copy the Hard requirements, Quality dimensions, Discipline rules, Root cause, Suggested fixes sections verbatim.

## Iteration history (when stall)

For 3-iter stalls, list what changed (or didn't) each iteration. Surface whether the producing chat is regenerating against the same gap or shifting gaps without closing any.

## Recommended next steps

One of:
- **Override and ship** — when the artifact is genuinely good enough and the spec is wrong
- **Edit directly** — when 1-2 targeted edits would close the gap the loop keeps flagging
- **Extend the spec source** — when the producing chat is generating to an outdated or incomplete spec
- **Regenerate from scratch with spec extension** — when the gap is systemic
- **Deprecate** — when the artifact shouldn't exist after all

## Resolution

(filled in when status flips to resolved)
```

---

## 6. Operator-facing telemetry

These signals tell the operator whether Mode 5 is calibrated correctly.

**On the master tracker (`_active-chats-tracker.md`):**

- The "Hot decisions sitting on Oliver's plate" section shows open hard-escalations as rows.
- The frontmatter `last-change:` line documents any auto-ship event when the score sits above 95 (i.e., shipping happens, but high-confidence ships are still logged so the trail exists).

**On the quality-loop dashboard (`_meta/dashboards/quality-loop-dashboard.md`):**

- Distribution of auto-shipped vs light-escalated vs hard-escalated by type (Dataview query against folder-log frontmatter counters).
- Per-type override rate over the trailing 30 days (Dataview query against `_escalation-queue.md` files and `### Operator override` blocks in folder logs).
- Triggered-refresh signal — if any per-type override rate exceeds 10%, the dashboard surfaces the threshold-tune candidate.

**In every Mode 5 stdout summary:**

- Verdict + confidence + auto-approve decision (auto-ship / light-escalate / hard-escalate)
- File paths touched
- Override flags applied (when any)
- Next-step pointer (folder-log link for audits, escalation-queue link for light, escalation-file link for hard)

---

## 7. Decision shortcuts

Common operator decisions with copy-paste-ready forms.

| Situation | What to type |
|---|---|
| Auto-ship a low-confidence PASS this once | `quality-check <path> --bypass-confidence` |
| Want eyes on a high-confidence PASS this once | `quality-check <path> --force-escalate` |
| Skip the loop entirely (binary output, throwaway) | `quality-check <path> --bypass-quality-loop` |
| Force a hard escalation on an artifact regardless of verdict | `quality-check <path> --escalate "<reason>"` |
| Raise the Core 30 threshold permanently | Edit `confidence-calibration.md` § "Per-artifact-type calibration" Core 30 row + add row to history table |
| Clear a light escalation queue | Open `<folder>/_escalation-queue.md`, decide row-by-row, move from Awaiting to Resolved |
| Clear a hard escalation | Open `_meta/escalations/escalation-*.md`, decide, flip `status: open` → `resolved`, add `## Resolution` block, remove tracker row |

---

## See also

- `../SKILL.md` § Mode 5 — AUTO-APPROVE-AND-ESCALATE — the mode spec
- `confidence-calibration.md` — per-type thresholds and the score math
- `verdict-rollup-thresholds.md` — verdict assignment rules (Mode 5 doesn't change these)
- `folder-quality-log-shape.md` — where confidence scores and auto-ship audits land in folder logs
- `auto-invoke-convention.md` — the convention block other skills emit; Mode 5 extends it with `confidence-target:` optionally
- `[[_meta/escalations/_README|_meta/escalations/_README.md]]` — the hard-escalations folder README
