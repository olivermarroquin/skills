# Edge cases — Non-happy-path scenarios in AGGREGATE + DRIFT-DETECT

Every named scenario here has a defined behavior. When a new edge case surfaces, document it here before adding the handling logic — the documentation is what makes the behavior auditable.

The operating principle across every case: **surface, don't silently skip**. The aggregator's value is partly in showing what's broken. Silent skips hide problems; visible warnings let the operator decide.

## Projects with no `_chat-status.md`

**Cause.** Project folder exists, candidate-project filter passes (no leading underscore, no angle brackets), but `_chat-status.md` is absent. Most common in projects scaffolded before Phase 1 of vault-orchestrator shipped (2026-05-30).

**AGGREGATE behavior.** Render the project under the "Projects without status digests" subsection with a one-line suggested action pointing at the Phase 1 pattern. Do NOT omit the project. Increment the `Projects without digest` count in the vault-wide rollup header.

**DRIFT-DETECT behavior.** List the project under verdict `missing digest`. Suggested action: "Create `_chat-status.md` following the Phase 1 spec at `~/workspace/skills/multi-chat-coordination/references/project-status-digest-shape.md`. Mirror EV's pattern at `~/workspace/second-brain/04_projects/clients/_active/ev-electric-services/_chat-status.md`."

**Why surface, not skip.** A project folder with no digest is invisible to the rollup if skipped. With surface-as-gap, the operator sees the gap in every run until they fill it — which is the right incentive.

## Projects with broken YAML in `_chat-status.md`

**Cause.** Most common: unquoted colon-space in `current-focus:` value, unescaped apostrophe inside single-quoted string, malformed list syntax in `blockers:` or `spawn-recommendations:`.

**AGGREGATE behavior.** Render the project block with a `[!warning] digest parse error` callout containing the YAML library's error message verbatim. Render the project's other fields as `<unknown>`. Do NOT abort the run — the rest of the rollup still ships.

**DRIFT-DETECT behavior.** Verdict: `parse error`. Surface the YAML library's error message as the annotation. Suggested action: "Fix YAML in `<project>/_chat-status.md`. Most common cause: unquoted colon-space in `current-focus:`. Wrap with single quotes per the digest spec's YAML safety section."

**Why non-blocking.** A single bad digest must not block the rollup of every other project. Half a rollup is better than no rollup.

## Projects archived mid-aggregation

**Cause.** Rare but possible: operator moves a project folder from `_active/` to `_archive/` while AGGREGATE is running.

**AGGREGATE behavior.** The walk happens at one point in time (Step 1). Whichever side of the move the walk captured is the side the run reports on. If the project was in `_active/` at walk time, it appears in the rollup; if it was in `_archive/` (or had already moved), it doesn't.

The aggregator does NOT retry or re-walk to handle race conditions. If the operator sees a project in the rollup that they just archived, re-running AGGREGATE produces a clean rollup. This is acceptable behavior; the moved project will be absent from the next run.

**DRIFT-DETECT behavior.** Same — single-walk snapshot. No retry.

## Projects with `_status.md` (legacy) and no `_chat-status.md`

**Cause.** The Phase 1 actual-deliverable note explains: EV had a pre-existing `_status.md` that was project-wide status prose. Phase 1 chose `_chat-status.md` specifically to avoid overwriting. Some projects today have only the legacy `_status.md` and no `_chat-status.md`.

**AGGREGATE behavior.** The aggregator looks for `_chat-status.md` only. It does NOT read or parse `_status.md`. A project with only `_status.md` is reported as "no status digest found" per the missing-digest branch.

**DRIFT-DETECT behavior.** Same — verdict `missing digest` regardless of `_status.md` presence.

The suggested action for these projects points the operator to the Phase 1 pattern. The operator may choose to:

- Create a new `_chat-status.md` alongside the legacy `_status.md` (Phase 1's chosen approach for EV).
- Migrate the legacy `_status.md` to `_chat-status.md` (operator-driven; outside aggregator scope).
- Leave the project digest-less if it's dormant (acceptable; just keeps appearing in "Projects without digest" each run).

## Projects whose `project:` slug doesn't match folder name

**Cause.** Operator renamed the project folder without updating the digest's `project:` field. Or a digest was copied from one project to another and the slug was forgotten.

**AGGREGATE behavior.** Use the folder name as the authoritative slug (per aggregation-algorithm.md § slug-mismatch check). Render the project under the folder-name slug. Surface a non-blocking warning: "digest `project:` field (`<value>`) doesn't match folder name (`<value>`). Folder name used as canonical."

**DRIFT-DETECT behavior.** Surface the same warning as a heuristic annotation. Verdict is still date-based.

## Projects with conflicting metrics

**Cause.** `in-flight-count: 3` in the digest, but the companion `_chat-tracker.md`'s `## 🟡 Active / in-flight chats` section has 0 rows. Or `ready-to-spawn-count: 2` but `spawn-recommendations` list is empty.

**AGGREGATE behavior.** Render the digest's stated counts in the project block (the digest is the canonical machine-readable source per the Phase 1 contract). Surface `count_drift` warnings in the project block's Warnings line.

**DRIFT-DETECT behavior.** Surface the same drift as a heuristic annotation. The digest fields are still used for verdict calculation (verdict is purely date-based; counts don't affect it directly).

**Why use the digest's stated counts.** The digest is the machine-readable contract. If the operator hand-edited the human-readable tracker without updating the digest, the digest is "authoritative as of its `updated:` field." The drift warning surfaces the gap so the operator can refresh.

## Projects with required fields absent

**Cause.** Digest was hand-created from a template and a required field (e.g., `last-closed:`) was left blank.

**AGGREGATE behavior.** Render the project block with the missing field shown as the literal text `<unknown>` (angle brackets included for grep-ability). Surface an `incomplete_digest` warning.

**DRIFT-DETECT behavior.** Date verdict still applies if `updated:` is present. If `updated:` itself is absent, treat as parse-error-equivalent for verdict purposes (verdict: `parse error` with annotation "no `updated:` field").

## Projects with `current-focus:` containing problematic characters

**Cause.** Plain-language summaries naturally contain colons (`Building S&H Core 30 pages: waiting on GBP verification`) and apostrophes (`it's blocked`). Both break YAML if not quoted properly per the digest spec's YAML safety section.

**AGGREGATE behavior.** When parsing succeeds (the operator quoted correctly), use the value verbatim in the project block — including any colons or apostrophes. The rendered Markdown table cell can hold them; no escaping needed.

When parsing fails, fall into the "broken YAML" branch above with the parser's error message.

**DRIFT-DETECT behavior.** Same.

## Markers absent from master tracker

**Cause.** First-ever aggregator run, or operator deleted the markers.

**AGGREGATE behavior.** Fall into the initial-installation protocol from `marker-conventions.md`: surface a proposed insertion to the operator, wait for approval. Do NOT write the markers unilaterally.

**DRIFT-DETECT behavior.** Markers are AGGREGATE-only. DRIFT-DETECT does not touch the master tracker; this case doesn't apply.

## Multiple BEGIN or END markers in master tracker

**Cause.** Operator copy-pasted markers, or a prior aggregator bug left orphaned markers.

**AGGREGATE behavior.** STOP and surface the count + line numbers of each marker. Do NOT guess which pair is canonical. Suggested action: "remove the extra markers, leaving exactly one BEGIN and one END."

## Unbalanced markers (BEGIN without END, or vice versa)

**Cause.** Operator hand-edited the master tracker and accidentally removed one of the pair.

**AGGREGATE behavior.** STOP and surface the imbalance with line numbers. Suggested action: "add the missing marker at the appropriate boundary; the prior generated section can be deleted or kept depending on whether you want it preserved."

## Sister file exists but inline markers also present

**Cause.** Operator switched from inline to sister-file mode but didn't remove the inline markers, or vice versa.

**AGGREGATE behavior in inline mode.** Use the inline markers; ignore the sister file. Don't modify or delete the sister file (it's outside the run's write scope).

**AGGREGATE behavior in sister-file mode.** Overwrite the sister file; ignore the inline markers. Don't touch the master tracker.

If the operator wants to switch modes cleanly, the manual steps are: (1) delete the inline markers (or the sister file), (2) run AGGREGATE in the target mode. The aggregator doesn't auto-migrate between modes.

## Project folder with files but no README

**Cause.** Project was scaffolded but never written up.

**AGGREGATE behavior.** Aggregate as normal — README presence is not required for inclusion. If no `_chat-status.md`, fall into the missing-digest branch.

**DRIFT-DETECT behavior.** Heuristic 2 (README newer than digest) is a no-op for these projects — it requires a README with a parseable `updated:` field. Skip silently if absent.

## Empty project folder

**Cause.** Folder created but never populated.

**AGGREGATE behavior.** Still iterates as a candidate project (passes the filter). Falls into missing-digest branch. Renders as "no status digest found" — same treatment as any other digest-less project.

**Why not skip empty folders.** Empty project folders are often a signal of abandoned planning. Surfacing them in the rollup invites cleanup ("oh, I never finished setting that up — let me archive it").

## Aggregator crashes mid-run

**Cause.** Unhandled exception in parsing or rendering logic.

**Recovery.** The aggregator does atomic writes — read full file, build new content, write full file. If the crash happens before the write, the master tracker is unchanged. If the crash happens during the write (rare; file writes are usually atomic at the OS level), the master tracker may be partially written. The operator can revert via git.

**Mitigation discipline.** Run the YAML parse check immediately after every write. If it fails, the master tracker frontmatter got corrupted; revert via git and surface the underlying parse exception. Add a guard for the specific exception class in the next aggregator iteration.

## Operator-set custom stale threshold

**Cause.** `--stale-threshold-days 7` for a project area where Oliver wants tighter freshness, or `--stale-threshold-days 30` for a calmer area.

**AGGREGATE behavior.** Apply the override only to this run. Don't persist it as a vault-wide default. If different thresholds matter for different project areas, Phase 3+ may add per-area config; today's behavior is single-threshold per run.

**DRIFT-DETECT behavior.** Same.

## Idempotency check

The regression test for byte-identical output across two runs:

```bash
cd ~/workspace/second-brain
# Run 1
python3 -c "<aggregator invocation with --no-timestamp --dry-run>" > /tmp/agg-run-1.txt
# Run 2 (same vault state)
python3 -c "<aggregator invocation with --no-timestamp --dry-run>" > /tmp/agg-run-2.txt
# Compare
diff /tmp/agg-run-1.txt /tmp/agg-run-2.txt
```

Expected: empty diff. Any difference is a non-determinism bug; fix before shipping.

Sources of non-determinism the aggregator must guard against (listed in `aggregation-algorithm.md` § idempotency contract): filesystem walk order, Python dict iteration order, set() operations, now() calls.

## Edge cases out of scope (v1)

Documented here for the avoid-scope-creep audit trail; not handled in Phase 2:

- **Tier-3 air-gapped vault.** The aggregator cannot read the tier-3 vault (per Cowork sandbox isolation). Tier-3 projects are invisible to the rollup. This is by design — see project README § What's out of scope.
- **Concurrent aggregator runs.** Running AGGREGATE twice in parallel against the same master tracker would race on the file write. The aggregator does not lock the file. Mitigation: don't run AGGREGATE concurrently. Phase 4+ may add file-locking if multi-spawn becomes a thing.
- **Network-fetched digests.** All digests must be on local disk. The aggregator does not fetch from URLs or remote vaults.
- **Cross-vault aggregation.** Single vault only. Phase 6+ may add multi-vault if it becomes a need.

## See also

- `./aggregation-algorithm.md` — happy-path walking + parsing
- `./marker-conventions.md` — marker placement + atomic-edit pattern
- `./drift-detection-heuristics.md` — DRIFT-DETECT's specific heuristics referenced here
- `~/workspace/skills/multi-chat-coordination/references/project-status-digest-shape.md` § "Validation rules" — the in-digest validation rules many of these edge cases map to
- `~/workspace/skills/multi-chat-coordination/references/project-status-digest-shape.md` § "Honest gap surfacing" — the pattern these edge cases collectively instantiate
