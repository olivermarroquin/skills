# Drift-detection heuristics — Staleness thresholds + signal-based augments

The deterministic core of DRIFT-DETECT mode. Reads per-project `_chat-status.md` digests and per-project context signals, produces a freshness verdict per digest, and surfaces suggested next moves.

DRIFT-DETECT is **read-only**. It never edits any digest. The output is a report the operator reads; the operator decides which (if any) digests to refresh.

## Verdict categories

Three categories based purely on date arithmetic, plus two terminal states:

| Verdict | Date condition | Meaning |
|---|---|---|
| `fresh` | `(today - digest.updated).days ≤ N` | digest is current; no action needed |
| `stale` | `N < (today - digest.updated).days ≤ N × M` | digest is getting old; consider refreshing |
| `very stale` | `(today - digest.updated).days > N × M` | digest is unreliable; refresh recommended |
| `parse error` | YAML parse fails | digest is broken; fix YAML before anything else |
| `missing digest` | no `_chat-status.md` in the project folder | digest never created; follow Phase 1 pattern |

Defaults: `N = 14` days (`--stale-threshold-days`), `M = 2` (`--very-stale-multiplier`). So very-stale fires at 28 days.

Calibration logic: 14 days reflects a typical "I've been working in this project recently enough that the digest mostly reflects reality" window. 28 days reflects "long enough that significant ships might have happened without digest updates." Adjust if Oliver's tempo shifts.

## Signal-based augments

Pure date arithmetic misses cases where a digest is technically fresh (updated within 14 days) but stale-in-fact because something else moved. DRIFT-DETECT applies four signal-based heuristics that annotate the date-based verdict without overriding it.

### Heuristic 1 — Execution log newer than digest

Walk `<project-folder>/execution-logs/`. Find the most recent file by modification time. If its `mtime` is newer than the digest's `updated:` field:

- **Annotation:** "execution log activity since last digest update — may have unrecorded ships"
- **Strength:** Strong signal. Execution logs land at chat-end-time; if a chat shipped after the digest update, the digest hasn't captured it.
- **Suggested action surfaced:** "Refresh the digest to reflect work shipped on YYYY-MM-DD per the latest execution log."

If `execution-logs/` doesn't exist in the project folder, this heuristic is a no-op (don't penalize projects that organize execution logs differently — some live inside the corresponding repo's `.kos/` folder).

### Heuristic 2 — Project README updated more recently

Read `<project-folder>/README.md` (or `_README.md` if the project uses the underscore convention). Parse its frontmatter `updated:` field. If it's newer than the digest's `updated:`:

- **Annotation:** "README updated since digest — current-focus may have shifted"
- **Strength:** Medium signal. README updates often capture strategic shifts the digest's `current-focus` should mirror.
- **Suggested action surfaced:** "Compare digest `current-focus` against README; refresh if stale."

If no README exists or has no `updated:` frontmatter field, this heuristic is a no-op.

### Heuristic 3 — Blocker expected-clear date in the past

For each entry in the digest's `blockers:` list, parse `expected-clear`. If it's a date in the past (relative to today):

- **Annotation:** "blocker '<text>' expected to clear YYYY-MM-DD — verify it cleared and refresh blockers list"
- **Strength:** Strong signal. The digest is asserting a blocker that, per the digest's own metadata, should have cleared.
- **Suggested action surfaced:** "Verify whether the blocker cleared on YYYY-MM-DD; if yes, refresh digest. If no, update `expected-clear` to a new date or `unknown`."

Skip entries where `expected-clear` is `unknown` (honest-gap entries don't trigger this heuristic).

### Heuristic 4 — Claimed in-flight work, no recent log activity

If the digest's `in-flight-count > 0` AND no execution log in `<project-folder>/execution-logs/` has `mtime` within the past 7 days:

- **Annotation:** "claims `<N>` in-flight chats but no execution log activity in the past 7 days — chats may be stalled or completed without logging"
- **Strength:** Medium signal. Could be a long-running chat that hasn't checkpointed; could be a chat that died silently; could be log convention drift.
- **Suggested action surfaced:** "Check whether the in-flight chats are still active; update count if not."

The 7-day window aligns with the `metrics.chats-closed-past-7d` field — same horizon as the digest's own activity metric.

## Heuristic compositing rules

Heuristics annotate; they don't change the date-based verdict. A digest can be:

- `fresh` + 3 annotations → "fresh, but signals suggest review"
- `stale` + 0 annotations → "stale; standard refresh recommended"
- `fresh` + 0 annotations → "fresh, no signals; no action"

The annotation count is reported alongside the verdict so the operator can rank attention. A fresh-with-3-annotations digest probably needs more urgent review than a stale-with-0-annotations digest that just hasn't been touched in 15 days during a slow week.

## Suggested-action ordering

When DRIFT-DETECT reports a project with multiple heuristic annotations, order suggested actions by strength:

1. Strong signals (Heuristics 1, 3) → surface first; these are concrete asks.
2. Medium signals (Heuristics 2, 4) → surface second; these are review-and-decide asks.
3. Date-based suggestion (refresh per stale-ness) → surface last; this is the default if no other signal speaks louder.

If two strong signals fire (e.g., newer execution log AND expired blocker), surface both — the operator may need to refresh both `current-focus` and `blockers`.

## Per-digest report row format

Plain-language, one row per audited project. Format:

```
- **<project-slug>** — updated YYYY-MM-DD (<N> days ago) — VERDICT
  <comma-separated annotation labels, if any>
  Suggested: <plain-language ask, or "no action" if fresh + no annotations>
```

Example fresh + no annotations:

```
- **ev-electric-services** — updated 2026-05-31 (1 day ago) — fresh
  Suggested: no action
```

Example stale + annotations:

```
- **resume-saas** — updated 2026-05-10 (22 days ago) — stale
  execution log newer than digest, README updated since digest
  Suggested: refresh digest to reflect work shipped through 2026-05-28 per the most recent execution log; review `current-focus` against the README's recent update.
```

Example very stale + parse-error:

```
- **app-factory** — last successful parse 2026-04-12 (50 days ago) — parse error
  YAML parse failed: "could not find expected ':' at line 7, column 18"
  Suggested: fix YAML in `_chat-status.md` (likely an unquoted colon-space in `current-focus:`); re-run DRIFT-DETECT after fix.
```

## Report-level summary

Top of the report:

```
DRIFT-DETECT report — YYYY-MM-DD HH:MM

Threshold: digests older than 14 days flagged stale; older than 28 days flagged very stale.
Signal heuristics: enabled (4 heuristics applied). [or "disabled" if --skip-heuristics]

Audited: <N> project folders, <M> digests parsed.

Verdict counts:
- Fresh: <count>
- Stale: <count>
- Very stale: <count>
- Parse error: <count>
- Missing digest: <count>

Annotation counts (strong signals):
- Execution log newer than digest: <count>
- Expired blocker: <count>

Annotation counts (medium signals):
- README newer than digest: <count>
- Claimed in-flight, no log activity: <count>

Recommended next moves:
1. <first concrete action — usually "refresh <slug>'s digest because X">
2. <second action>
3. ...
```

The recommended next moves list is the actionable headline. Surface 3-5 items. If everything's fresh, the list reads "no action needed; all digests current."

## Sample regression scenarios

These run during skill development and after any heuristic change:

1. **All fresh + no signals.** Report verdict counts: all fresh. Suggested actions list: "no action needed." Validates no-false-positives.
2. **One digest back-dated 20 days.** Verdict: stale. Validates the 14-day threshold and a digest that triggers a single annotation if applicable.
3. **One digest with `expected-clear` in the past.** Annotation: expired blocker. Validates Heuristic 3.
4. **One digest with `in-flight-count = 2` but no recent execution log.** Annotation: claimed in-flight, no log activity. Validates Heuristic 4.
5. **One project with no `_chat-status.md`.** Verdict: missing digest. Validates the missing-digest branch.
6. **One digest with broken YAML.** Verdict: parse error. Annotation: parser error message. Validates parse-error handling.

The regression-test 2 in Phase 2's handoff (`back-date EV's _chat-status.md by 20 days, re-run DRIFT-DETECT, expected: warning surfaced`) maps directly to scenario 2 above.

## Calibration log

When defaults change, document here:

- **2026-06-01 (Phase 2 install)** — defaults locked at 14-day stale / 28-day very-stale / 4 signal heuristics enabled. Reflects today's project tempo. Revisit at Phase 5 (orchestrator decomposition) when real-use signal accumulates.

## See also

- `./aggregation-algorithm.md` — AGGREGATE mode's complementary in-digest validation checks (some overlap with these heuristics, but AGGREGATE's are non-blocking annotations on a write; DRIFT-DETECT's are the primary output of a read-only audit)
- `./edge-cases.md` — handling parse errors, archived projects, and slug mismatches in both modes
- `~/workspace/skills/multi-chat-coordination/references/project-status-digest-shape.md` — the digest contract; "Honest gap surfacing" section governs how `unknown` and absent fields interact with these heuristics
