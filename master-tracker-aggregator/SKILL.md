---
name: master-tracker-aggregator
description: Two-mode skill that walks every per-project `_chat-status.md` digest under `~/workspace/second-brain/04_projects/` and rolls it up into a generated section the master `_active-chats-tracker.md` consumes. **Mode 1 (AGGREGATE):** parses every digest, produces a vault-wide rollup plus one block per project, writes the result between `<!-- AGGREGATOR:BEGIN -->` / `<!-- AGGREGATOR:END -->` markers in the master tracker (default) or to a sister file `_active-chats-tracker-aggregated.md` (`--output sister-file`). Idempotent — same vault state produces byte-identical output. **Mode 2 (DRIFT-DETECT):** read-only freshness audit; flags digests whose `updated:` field is older than the staleness threshold (default 14 days) and proposes "consider re-running the Phase 1 update protocol" without auto-editing. Phase 2 of the vault-orchestrator project (2026-06-01). Read-only on per-project files; only writes to the master tracker's generated section or the sister file. Composes with multi-chat-coordination (consumes the data contracts it shipped in Phase 1) and emits the standard output-quality-loop auto-invoke block at completion. Trigger phrases include "aggregate the master tracker," "run the master-tracker-aggregator," "roll up project status," "rebuild the master rollup," "regenerate the aggregator section," "what's stale in the digests," "drift-detect the per-project status files," "check digest freshness."
---

# Master Tracker Aggregator

The bottom-up rollup layer between per-project `_chat-status.md` digests and the master `_active-chats-tracker.md`. Reads every digest in the vault, produces a vault-wide rollup plus one block per project, writes the result into a clearly-bounded generated section of the master tracker (or to a sister file the master imports).

The skill exists because the master tracker is already 240+ lines and growing per-pass. Without an aggregated rollup section, "what's the state of the vault?" requires the operator to mentally walk every project. With the rollup, that question becomes one scroll.

The aggregator is **read-only on per-project files**. It never edits `_chat-status.md` or `_chat-tracker.md`. The only file it writes to is the master tracker's generated section (or the sister file). Operator edits to the master tracker outside the marker block are preserved verbatim across aggregation runs.

## When to trigger

### Mode 1 — AGGREGATE (rollup write)

Direct triggers for regenerating the rollup section:

- "Aggregate the master tracker"
- "Run the master-tracker-aggregator"
- "Roll up project status"
- "Rebuild the master rollup"
- "Regenerate the aggregator section"
- "Refresh the rollup"

Indirect triggers — when the operator wants vault-wide state at a glance after multiple per-project chats shipped:

- "What's the state across all projects?"
- "Show me the vault-wide rollup"
- "I want one view of every project's status"

### Mode 2 — DRIFT-DETECT (freshness audit)

Direct triggers for the read-only staleness check:

- "What's stale in the digests?"
- "Drift-detect the per-project status files"
- "Check digest freshness"
- "Which `_chat-status.md` files need updating?"
- "Run drift-detect"

Indirect triggers — when the operator opens a chat after a long gap and wants to know which digests fell behind reality:

- "How fresh is the per-project digest data?"
- "Are any project status files stale?"

## Core operating principles

These hold across both modes. Read them before invoking either.

**Read-only on per-project files.** The aggregator never edits `_chat-status.md`, `_chat-tracker.md`, or any file inside a project folder. The only writes are to the master tracker's generated section (between marker comments) OR to the sister file. Anything else is a discipline violation — surface and stop.

**Non-destructive on hand-edited master tracker content.** Everything outside the `<!-- AGGREGATOR:BEGIN -->` / `<!-- AGGREGATOR:END -->` markers is operator-edited prose and stays verbatim across runs. The aggregator replaces only the content between markers (or replaces the sister file in full when `--output sister-file` is used).

**Idempotent.** Same vault state produces byte-identical output. The generated section is deterministic: project order is alphabetical by slug; field formatting is stable; timestamps inside the block come from digest `updated:` fields, not from `now()`. The only `now()` reference is a single "Generated: YYYY-MM-DD HH:MM" line at the top of the block, which the regression test explicitly excludes from byte-comparison (`--no-timestamp` flag for the regression check).

**Plain language in every cell.** Per `~/workspace/second-brain/_meta/plain-language-conventions.md`. Field values surface plain-language summaries from the digest's `current-focus` and `last-closed-summary` fields verbatim — the digest is the source of plain-language calibration. No re-summarizing, no AI-padding.

**Honest gap surfacing over silent skip.** When a project folder has no `_chat-status.md`, surface it as "no status digest found" with a one-line suggested action ("create one via the Phase 1 pattern at [[project-status-digest-shape]]"). Don't omit the project from the rollup. The aggregator's value is partly in showing which projects lack digests.

**Validation is non-blocking.** When a digest's YAML doesn't parse, surface the project as "digest parse error" with the parser's error message — do not abort the whole run. Half a rollup is better than no rollup when one digest is malformed. Same rule applies to missing required fields, mismatched counts, and other in-digest validation warnings per the digest spec's "Validation rules" section.

**YAML single-quote-wrap rule.** The master tracker's `last-change:` field follows the master tracker's existing single-quote-wrap discipline. When AGGREGATE writes a new `last-change:` value summarizing the run, the value is wrapped in single quotes (apostrophes inside doubled per YAML rules). The regex-extractor YAML parse check runs after the write.

**Check folder structure before writing.** Before writing the generated section into the master tracker, verify the markers exist. If they don't, propose adding them at a specific insertion point — don't write the markers without operator approval. If using `--output sister-file`, verify the sister file's location is the expected path next to the master tracker.

## Mode 1 — AGGREGATE

### What AGGREGATE produces

A generated rollup block with two parts:

1. **Vault-wide header.** Total in-flight count, total ready-to-spawn count, total queued count, stale-digest warnings, operator-fatigue signal.
2. **One block per project.** Project name + slug + last-updated date, one-line current focus, in-flight/queued/ready counts, top blocker (if any), top 1-2 ready-to-spawn chats, 7-day metrics.

The block sits between `<!-- AGGREGATOR:BEGIN -->` and `<!-- AGGREGATOR:END -->` marker comments inside the master tracker (default) or replaces the contents of `_active-chats-tracker-aggregated.md` next to the master tracker (`--output sister-file` flag).

### AGGREGATE step-by-step

**Step 1 — Walk the project folders.**

The aggregator walks two roots:

```
~/workspace/second-brain/04_projects/clients/_active/
~/workspace/second-brain/04_projects/personal/
```

For each immediate child directory, decide whether to aggregate it:

- **Skip** directories starting with `_` (e.g., `_archive`, `_private`, `_strategic-decisions`) — these are meta-folders, not projects.
- **Skip** placeholder/template directories containing `<` or `>` in the name (e.g., `<client-slug>`) — these are scaffolding stubs.
- **Skip** directories whose names start with `.` (hidden / dotfiles).
- **Aggregate** every other directory as a project. Use the directory name as the project slug.

For each aggregated project, look for `_chat-status.md` at the project root. Four outcomes:

- **Digest found and parses.** Add to the rollup with full data.
- **Digest found but YAML parse fails.** Add to the rollup as "digest parse error" with the parser message. Don't abort.
- **Digest missing.** Add to the rollup as "no status digest found" with suggested-action pointer.
- **Project README present but no digest.** Same as "digest missing" — surface as a gap.

Detailed walking + parsing rules: see `references/aggregation-algorithm.md`.

**Step 2 — Parse each digest's YAML.**

Use the regex-based frontmatter extractor (the master tracker's `last-change` field pattern), not naive `split('---')`. Reason: literal `---` inside `last-change` values has bitten the master tracker before; the same can happen inside a digest's `current-focus:` field.

```python
import yaml, re
m = re.match(r'^---\n(.*?)\n---\n', open(digest_path).read(), re.DOTALL)
data = yaml.safe_load(m.group(1)) if m else None
```

For each parsed digest, run the validation checks from the digest spec's "Validation rules" section:

- `updated:` older than the stale threshold → record a `stale_digest` warning.
- `in-flight-count > 0` but corresponding per-project tracker section is empty → record a `count_drift` warning.
- `ready-to-spawn-count` doesn't match `spawn-recommendations` list length → record a `count_drift` warning.
- `blockers[].expected-clear` date in the past → record a `expired_blocker` warning.
- Required fields absent (`type`, `project`, `updated`, `current-focus`) → record an `incomplete_digest` warning.

Warnings are non-blocking. Surface them in the rollup but still emit the project block.

**Step 3 — Build the vault-wide rollup header.**

Aggregate counts across every digest that parsed:

- Total in-flight = sum of `in-flight-count` across all parsed digests
- Total ready-to-spawn = sum of `ready-to-spawn-count`
- Total queued = sum of `queued-count`
- Stale digests = count of digests with `updated:` older than the threshold
- Operator-fatigue signal = total estimated queued hours vs. capacity baseline (see `references/aggregation-algorithm.md` § operator-fatigue heuristic)

For projects without a digest, those counts contribute 0 to the totals (because we have no data) — and the project is named separately under "Projects without status digest" so the gap is visible.

**Step 4 — Render the rollup block.**

Render order:

1. `<!-- AGGREGATOR:BEGIN -->` (marker — preserved verbatim)
2. Section header `## 📊 Vault-wide project rollup (generated)` (with `[!summary]` callout naming generation date + projects-scanned count)
3. Vault-wide header (counts table + warnings list + operator-fatigue line)
4. One project block per project, alphabetical by slug
5. Projects-without-digest section (named projects + suggested action)
6. Footer line: "Regenerate: invoke the `master-tracker-aggregator` skill in AGGREGATE mode."
7. `<!-- AGGREGATOR:END -->` (marker — preserved verbatim)

Per-project block shape per `references/aggregation-algorithm.md` § per-project block.

**Step 5 — Write to the master tracker (default) or sister file.**

**Default mode (inline markers):**

1. Read the master tracker fully.
2. Find `<!-- AGGREGATOR:BEGIN -->` and `<!-- AGGREGATOR:END -->`. If both present, replace the content between them with the new block.
3. If markers are absent, surface a proposed insertion (between the `## How to use this file` section and the first `##` data section is the standard placement — see `references/marker-conventions.md` § insertion point). Wait for operator approval before writing the markers.
4. Bump the master tracker's `last-change:` value to a one-liner naming this aggregation pass.
5. Run the YAML parse check.

**Sister-file mode (`--output sister-file`):**

1. Write the generated block (without surrounding markers — the file itself is the boundary) to `~/workspace/second-brain/_meta/handoffs/_active-chats-tracker-aggregated.md`.
2. Include a top-of-file note: "Auto-generated by master-tracker-aggregator. Do not hand-edit — edits will be overwritten on next run."
3. Do not touch the master tracker's frontmatter. The sister file is the canonical aggregator output in this mode.

**Step 6 — Surface the run report.**

Plain-language summary of what landed:

- Projects scanned (count)
- Digests parsed cleanly (count)
- Digests with parse errors (count + names)
- Projects without digests (count + names)
- Warnings raised (per category)
- Marker action taken (replaced inline / wrote sister file / proposed marker insertion)
- Master tracker `last-change` updated to: (the new value, quoted)

If the run was a regression check (`--no-timestamp` flag) and the output differed from the prior run's byte-stripped version, surface that as an idempotency violation — the rollup should be deterministic.

### AGGREGATE flags

- `--output inline` (default) — write between markers in the master tracker.
- `--output sister-file` — write to `_active-chats-tracker-aggregated.md` next to the master tracker; do not touch the master tracker.
- `--stale-threshold-days N` (default 14) — override the stale-digest threshold.
- `--no-timestamp` — for regression testing; omit the "Generated:" timestamp line at the top of the block so the byte-comparison is deterministic.
- `--dry-run` — render the block to stdout (or chat) without writing any file. Useful for previewing.

### AGGREGATE worked example

**Operator:** "Aggregate the master tracker."

**Skill response (abbreviated):**

```
Walking 04_projects/clients/_active/ and 04_projects/personal/ ...

Projects discovered: 11
  Aggregated: 11
  Skipped (meta / template): 4 (<client-slug>, _archive, _private, _strategic-decisions)

Digests parsed cleanly: 1 (ev-electric-services)
Digests with parse errors: 0
Projects without _chat-status.md: 10
  - s-and-h-contracting
  - ai-agency-core
  - app-factory
  - dad-businesses
  - hire-relay
  - idea-factory
  - keelworks
  - legal-toolkit
  - resume-factory
  - resume-saas

Warnings: 0
  (EV's digest updated 2026-05-31, within the 14-day stale threshold.)

Marker action: inline markers present; replaced generated section.
Master tracker last-change: '2026-06-01 (pass sixty-two) — aggregator run: 11 projects scanned, 1 digest parsed, 10 gaps surfaced'

YAML parse check on master tracker: ✅ OK
```

## Mode 2 — DRIFT-DETECT

### What DRIFT-DETECT produces

A read-only freshness report. For each parsed digest:

- Days since the digest's `updated:` field
- Verdict: `fresh` (≤ threshold), `stale` (> threshold but ≤ 2× threshold), `very stale` (> 2× threshold)
- Suggested action (only for stale or very stale): "consider re-running the Phase 1 update protocol on this project's `_chat-status.md`"

Plus a top-of-report summary: total digests audited, count by freshness verdict, recommended next moves.

The report is plain prose. It does not edit any digest. Phase 3+ may add an auto-prompt to refresh stale digests; Phase 2 is read-only.

### DRIFT-DETECT step-by-step

**Step 1 — Walk project folders (same logic as AGGREGATE Step 1).**

Skip meta-folders, template folders, hidden folders. Identify candidate project folders.

**Step 2 — Check for `_chat-status.md` in each.**

For each project:

- If the digest exists and parses: continue to Step 3.
- If the digest is missing: include in the report's "Projects without a digest" section with the same Phase-1-pattern suggested action.
- If the digest exists but YAML parse fails: include as "digest parse error" — count as `very stale` for purposes of recommended action (operator needs to fix the file before next aggregation).

**Step 3 — Compute freshness for each parsed digest.**

```
days_since_update = (today - digest.updated).days
```

Verdict mapping (defaults; configurable via flag):

- `fresh` if `days_since_update ≤ 14`
- `stale` if `14 < days_since_update ≤ 28`
- `very stale` if `days_since_update > 28`

Per-digest report row:

```
- <project-slug> — updated YYYY-MM-DD (N days ago) — VERDICT [— suggested action]
```

**Step 4 — Apply drift heuristics beyond pure age.**

Even fresh-by-date digests can be stale-in-fact if other project signals advanced past them. The aggregator checks four heuristics from `references/drift-detection-heuristics.md`:

1. **Newer execution log present.** If `<project>/execution-logs/` contains a log file dated after the digest's `updated:` field, flag as "execution log newer than digest — may have unrecorded ships."
2. **Project README updated.** If the project README's `updated:` frontmatter is newer than the digest's `updated:`, flag as "README newer than digest — current-focus may have shifted."
3. **Blocker expected-clear in the past.** Already covered by AGGREGATE's validation; DRIFT-DETECT re-surfaces because expected-clear-passed is a strong signal the digest needs review.
4. **In-flight count > 0 but no recent execution log entry.** If the digest claims active work but no execution log activity in the past 7 days, flag as "claimed in-flight work has no recent log activity."

Heuristics are advisory. They don't change the date-based verdict; they add an annotation that surfaces alongside it.

**Step 5 — Produce the report.**

Plain-language summary at the top:

```
DRIFT-DETECT report — YYYY-MM-DD HH:MM

Threshold: digests older than 14 days flagged stale; older than 28 days flagged very stale.

Audited: <N> project folders, <M> digests parsed.

Verdict counts:
- Fresh: <count>
- Stale: <count>
- Very stale: <count>
- Parse error: <count>
- Missing digest: <count>

Suggested next moves:
1. ...
2. ...
```

Then per-project rows grouped by verdict (very-stale first, then stale, then fresh, then parse-errors, then missing).

**Step 6 — Surface, don't apply.**

DRIFT-DETECT is read-only in v1. It does NOT edit any digest, does NOT trigger AGGREGATE, does NOT open new chats. The operator reads the report and decides which (if any) digests to refresh.

### DRIFT-DETECT flags

- `--stale-threshold-days N` (default 14) — adjust the stale threshold.
- `--very-stale-multiplier M` (default 2) — `very stale` = `N × M` days.
- `--include-fresh` (default true) — include fresh-verdict rows in the report. Set false for a "what's broken only" view.
- `--skip-heuristics` — pure date-based verdicts only; skip the four signal-based heuristics from Step 4.

## Composition with multi-chat-coordination

The aggregator consumes the two data contracts shipped by multi-chat-coordination Phase 1:

- `references/project-chat-tracker-shape.md` — the human-readable tracker companion (the aggregator does not parse it; it's there as the operator-facing rendering of the same data the digest carries machine-readably).
- `references/project-status-digest-shape.md` — the machine-readable digest contract the aggregator parses verbatim.

When the digest spec evolves, the aggregator's parser needs updating. Detection: if AGGREGATE encounters a digest with frontmatter fields the parser doesn't recognize, surface them as informational warnings ("digest schema may have evolved — consider updating the aggregator parser") without blocking the run.

## Composition with output-quality-loop

The aggregator's output (the generated section, or the sister file) is an artifact. Per the auto-invoke convention at `~/workspace/skills/output-quality-loop/references/auto-invoke-convention.md`, emit the standard block at completion of an AGGREGATE run.

Per-project `_chat-status.md` files are also artifacts — but they're operator-edited (not skill-produced), so they're outside the auto-invoke scope. The aggregator does not propose quality-loop runs on digests.

**The block to emit (verbatim) at the end of an AGGREGATE run that wrote to disk:**

````markdown
## Auto-invoke output-quality-loop

This skill produced the following artifact(s):
- `<path to master tracker OR sister file>`

[output-quality-loop:eval] — for each artifact, run output-quality-loop in EVALUATE mode. If PASS, declare the chat done. If NEEDS REVISION or FAIL, ingest the revision prompt as if it were operator input and regenerate the artifact, then re-invoke output-quality-loop. Cap at 3 iterations; on the 3rd FAIL, escalate to the operator with the evaluation report.
````

Skip the block for `--dry-run` runs and for DRIFT-DETECT (which writes nothing).

## Closing step — Emit run summary + (where applicable) auto-invoke block

Every invocation ends with a plain-language summary of what landed plus, in AGGREGATE write mode, the auto-invoke output-quality-loop block. The summary names: projects scanned, digests parsed, gaps surfaced, warnings raised, write action taken, YAML parse result.

DRIFT-DETECT summaries name: digests audited, verdict counts, heuristic annotations, recommended next moves. No quality-loop block because no artifact was written.

## Out of scope (v1)

- **Auto-updating `_chat-status.md` files.** The aggregator is read-only on per-project files. Phase 3+ may add a refresh-prompt orchestration; Phase 2 stays read-only.
- **Cross-vault aggregation.** Single vault only (`~/workspace/second-brain/`). Tier-3 vault is air-gapped and inaccessible to Cowork by design.
- **Metrics from external systems.** No Toggl, Linear, GitHub, or other API reads. The aggregator only reads vault files.
- **Rollup of domain folders.** Domains (`03_domains/`) have no `_chat-status.md` by design — they're accumulating knowledge surfaces, not project surfaces. Phase 3 SURVEY mode (vault-orchestrator) covers domain signal-mining; Phase 2 stays projects-first.
- **Auto-spawning chats from spawn-recommendations.** Phase 4 (vault-orchestrator) introduces PROVISION + `_spawn-queue.md`. Phase 2 surfaces the recommendations in the rollup but does not act on them.
- **Editing the master tracker outside markers.** Operator-edited prose stays verbatim. The aggregator owns only the marker-bounded block (or the sister file).

## Maintenance notes (for future skill iterations)

These observations seed at skill creation. Promote to standalone notes if they generalize.

**1. Watch for digest schema drift.** The digest spec lives at `references/project-status-digest-shape.md` inside multi-chat-coordination. If the spec evolves (new required field, renamed field, dropped field), the aggregator's parser needs updating. Detection: AGGREGATE Step 2's validation checks surface unrecognized fields as informational warnings.

**2. Watch for marker drift.** The marker comments are HTML comments (`<!-- AGGREGATOR:BEGIN -->`). If the master tracker's Markdown renderer changes its comment-stripping behavior, the markers might render visibly. Detection: spot-check the master tracker's Obsidian rendering after each aggregator pass.

**3. Watch for placeholder folder drift.** Step 1's "skip directories containing `<` or `>`" assumes placeholder folders use angle-bracket convention. If the operator changes the convention (e.g., to `_template_<slug>`), update the skip rule.

**4. Watch for staleness-threshold calibration.** Default 14 days reflects today's project tempo. If Oliver's tempo shifts (e.g., faster ships → 7 days more honest; slower → 28 days), adjust the default and document the change.

**5. Watch for parser fragility on `current-focus:` quoting.** The digest spec's YAML safety section calls out single-quote wrapping for `current-focus:`. If digests start showing parse errors, the most-common cause is unquoted colon-space sequences in `current-focus:`. The aggregator surfaces these as parse errors with the YAML library's message; the operator fixes by adding single quotes.

**6. Watch for project-folder drift.** Step 1 walks `clients/_active/` and `personal/`. If new top-level project areas appear (e.g., `04_projects/community/`, `04_projects/research/`), the walking roots need updating.

## Related

- `~/workspace/skills/multi-chat-coordination/SKILL.md` — composes with this; shipped the data contracts in Phase 1
- `~/workspace/skills/multi-chat-coordination/references/project-status-digest-shape.md` — the digest contract this skill parses
- `~/workspace/skills/multi-chat-coordination/references/project-chat-tracker-shape.md` — the human-readable companion (not parsed by this skill)
- `~/workspace/skills/output-quality-loop/SKILL.md` — the auto-invoke target at completion
- `~/workspace/skills/output-quality-loop/references/auto-invoke-convention.md` — the block shape this skill emits
- `~/workspace/second-brain/_meta/handoffs/_active-chats-tracker.md` — the master tracker this skill's generated section lives inside (default mode)
- `~/workspace/second-brain/_meta/handoffs/_active-chats-tracker-aggregated.md` — the sister file written in `--output sister-file` mode
- `~/workspace/second-brain/_meta/handoffs/vault-orchestrator/_README.md` — the project that produced this skill
- `~/workspace/second-brain/_meta/handoffs/vault-orchestrator/phase-2-master-tracker-aggregator.md` — the handoff this skill executes
- `~/workspace/second-brain/_meta/plain-language-conventions.md` — voice rules every output follows
- `./references/aggregation-algorithm.md` — step-by-step walking + parsing logic
- `./references/marker-conventions.md` — where the generated section lives + how to update it idempotently
- `./references/drift-detection-heuristics.md` — staleness thresholds + signal-based heuristics
- `./references/edge-cases.md` — projects with no digest, broken YAML, archived mid-run, conflicting metrics
