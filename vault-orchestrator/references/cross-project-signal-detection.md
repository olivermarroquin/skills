# Cross-project signal detection

How SURVEY Section 9 detects signals that span multiple projects. The category is small but high-value — these are the signals that fall through the cracks of per-project tracking.

## What counts as a cross-project signal

Four signal types:

1. **Multi-project handoffs.** A handoff whose `purpose:` or `tags:` name two or more projects, or whose deliverable explicitly affects multiple project areas.
2. **Convention changes pending rollout.** Edits to `_meta/conventions.md`, `_meta/plain-language-conventions.md`, `_meta/working-surfaces.md`, or similar canonical convention docs that imply downstream application work.
3. **Recently-promoted patterns.** Patterns in `05_shared-intelligence/patterns/` flipped to `status: promoted` recently — these often imply application work across the projects they touch.
4. **Multi-project decisions.** Decision-record files in `_meta/decisions/` modified recently that affect 2+ projects.

The fifth implicit signal (changes to canonical conventions that haven't propagated to dependent files) is the highest-friction one — and the easiest to miss without explicit detection.

## Signal 1 — Multi-project handoffs

### Detection

Walk every handoff file under `_meta/handoffs/`:

1. Parse frontmatter.
2. Check `purpose:` for explicit naming of 2+ projects (slugs or names).
3. Check `tags:` for 2+ project tags (e.g., `[handoff, ev-electric-services, s-and-h-contracting, intel-routing-rollout]`).
4. Spot-check the prompt body for "affects both X and Y" phrasing.

Count a handoff as multi-project when 2+ project slugs are named.

### What to surface

Per multi-project handoff: name the handoff (wikilink), the projects affected, and the implied downstream work.

Example surface:

> The `intel-routing-rollout/phase-3-skill-build` handoff affects all 11 inboxes vault-wide (10 projects + the master inbox at `_meta/`). When Phase 3 ships, every project that has an inbox needs to be updated to use the new convention.

### Threshold

Always surface multi-project handoffs that are still `status: active`. Closed handoffs are historical and surface only if their downstream work didn't roll out yet (rare).

## Signal 2 — Convention changes pending rollout

### Detection

Watch a small set of canonical convention files:

- `~/workspace/second-brain/_meta/conventions.md`
- `~/workspace/second-brain/_meta/plain-language-conventions.md`
- `~/workspace/second-brain/_meta/working-surfaces.md`
- `~/workspace/second-brain/_meta/decision-research-conventions.md`
- `~/workspace/second-brain/_meta/vault-stewardship-principles.md`

For each, check frontmatter `updated:` against today. If `updated:` is within the past 14 days, the convention is recently-edited and may have downstream rollout work.

To detect "pending rollout," check if the changed convention is referenced in any open issues, recent handoffs, or recent execution logs as "needs rollout."

### What to surface

Per recently-changed convention: name the file, the date of the change, and what the change implies in plain language.

Example surface:

> `_meta/plain-language-conventions.md` was canonicalized 2026-05-16. Affects every operator-facing output across every project. Rollout is ongoing as new chats spawn and existing artifacts get touched; no dedicated rollout chat is needed because the convention applies on next-edit. Surface here so the operator can spot-check that recent outputs are honoring it.

### Threshold

Surface every recent convention change. Even when no rollout is needed, the operator wants to know what changed.

## Signal 3 — Recently-promoted patterns

### Detection

Walk `05_shared-intelligence/patterns/pattern-*.md`:

1. Parse frontmatter.
2. Check `status: promoted` AND `updated:` (or `promoted:` if present) within past 14 days.

For each recently-promoted pattern, check the `applies-to:` or `domains:` field to identify which projects could apply it.

### What to surface

Per recently-promoted pattern: name the pattern, when it was promoted, and which projects could apply it.

Example surface:

> `pattern-two-file-artifact-split` was promoted 2026-06-01 (second observation: vault-orchestrator Phase 1's human + machine companion files; first: output-quality-loop's folder log + per-artifact frontmatter). Applies to any future skill that produces both operator-scannable and machine-parsed artifacts. No immediate downstream application chat; the pattern is now available for future skill-builds to reference.

### Threshold

Surface every promotion in the past 14 days. Even without immediate downstream work, recently-promoted patterns are signal worth surfacing.

## Signal 4 — Multi-project decisions

### Detection

Walk `_meta/decisions/`:

1. List recently-modified decision files (`updated:` within past 14 days).
2. For each, check the decision's scope. Multi-project decisions name 2+ project slugs or describe a system-wide effect.

### What to surface

Per multi-project decision: name the decision, the date, and the projects affected.

Example surface:

> The 2026-05-30 decision to lock hermes-harness at Option A Path 2 affects the hermes-harness project (architecture) and the vault-orchestrator project (composition map — hermes-harness becomes the autonomy layer that follows vault-orchestrator). No immediate cross-project chat needed; surfaces here so the orchestrator's recommendations stay aligned with the decision.

### Threshold

Surface every multi-project decision in the past 14 days.

## Implicit signal — Stale convention propagation

The hardest signal to detect mechanically: a canonical convention was edited weeks ago and dependent files haven't been updated to match. The orchestrator can't fully detect this without walking every file that should follow the convention.

The heuristic that catches most cases: when a convention was edited >14 days ago AND `_meta/handoffs/` has no chat in the past 14 days addressing rollout to dependent files, surface as "convention edited <N> days ago — verify dependent files still align."

This is a soft signal — high false-positive rate. Use sparingly. Surface only when the convention's edits are substantive (not typo fixes).

## Voice rules

- One signal per row
- Plain language; gloss any convention names on first use
- Always cite the affected files / projects
- Don't editorialize ("major change") — describe what changed

## Empty-state shape

"No active cross-project signals. Every recent change is project-scoped. No convention edits in the past 7 days. No pattern promotions in the past 7 days requiring downstream application. No multi-project decisions in the past 7 days."

## See also

- `~/workspace/skills/vault-orchestrator/SKILL.md` § Mode 1 Step 5 — runtime behavior
- `./survey-section-shapes.md` § Section 9 — output shape
- `~/workspace/second-brain/05_shared-intelligence/workflows/workflow-knowledge-promotion.md` — promotion workflow that produces Signal 3
- `~/workspace/second-brain/_meta/decisions/` — Signal 4 source
