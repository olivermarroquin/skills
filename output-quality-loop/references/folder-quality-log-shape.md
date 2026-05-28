# Folder quality log shape

The per-folder `_quality-log.md` file is the audit trail for every quality-loop evaluation in that folder. One log file per folder. Each artifact in the folder gets a `## <artifact-slug>` section inside.

This shape was chosen 2026-05-27 over sister-file-per-artifact (which would have produced ~500-1000 files vault-wide vs. the current ~30-50). The artifact's own frontmatter holds a pointer + latest verdict + last-evaluated date; downstream gates (Phase 3 publish, Phase 6 auto-approve) read frontmatter directly. The folder log holds the full archaeology.

## Filename and location

- Filename: `_quality-log.md` (underscore prefix so Obsidian sorts it to the top of the folder, same convention as `_README.md`)
- Location: at the root of every folder that contains at least one artifact that's been evaluated by the quality-loop
- Lifetime: persistent. Older-than-6-month entries archive to `_quality-log-archive.md` per the cleanup convention below.

## Folder log frontmatter

```yaml
---
type: folder-quality-log
status: active
created: YYYY-MM-DD
last-updated: YYYY-MM-DD
artifacts-tracked: N
shipped: N        # count of artifacts whose latest verdict is PASS
iterating: N      # count of artifacts whose latest verdict is NEEDS REVISION (any tier)
escalated: N     # count of artifacts that hit the iteration cap without reaching PASS
tags: [folder-quality-log, quality-loop]
---
```

The counters are read by the Dataview dashboard at `_meta/dashboards/quality-loop-dashboard.md`. Increment as artifacts pass through; don't decrement until an artifact moves to archive.

## Folder log body

After the frontmatter, the body is a series of per-artifact sections, one per artifact in the folder that's been evaluated. New sections append at the bottom; existing sections get new iteration entries appended within them.

```markdown
# Quality log — <folder name>

This file tracks every output-quality-loop evaluation for artifacts in this folder.
One section per artifact; iteration history inside each section.

See [[output-quality-loop|the skill]] for evaluation methodology and the verdict-rollup thresholds.

---

## <artifact-slug>

**Latest:** PASS (2026-05-28) — iteration 1 of 3

### Iteration 1 — 2026-05-28 14:23

[full evaluation report inline; same shape as the on-screen report — see SKILL.md § Evaluation report format]

---

## <other-artifact-slug>

**Latest:** NEEDS REVISION (minor) (2026-05-28) — iteration 2 of 3

### Iteration 1 — 2026-05-27 09:15

[evaluation report]

### Iteration 2 — 2026-05-28 11:42

[evaluation report]

---
```

The `## <artifact-slug>` heading uses the artifact's filename minus extension. For example:

- Artifact at `<folder>/source-2026-04-26-jono-catliff.md` → section heading `## source-2026-04-26-jono-catliff`
- Artifact at `<folder>/panel-upgrade--vienna-va.md` → section heading `## panel-upgrade--vienna-va`

The slug-only form lets the artifact's frontmatter pointer (`quality-log: "[[_quality-log#<artifact-slug>]]"`) resolve correctly in Obsidian.

## Latest line discipline

The "Latest:" line right under the artifact heading is the single line downstream queries read. It carries:

- **Verdict** — PASS | NEEDS REVISION (minor) | NEEDS REVISION (substantive) | FAIL
- **Date** — YYYY-MM-DD of the latest evaluation
- **Iteration** — N of 3 (the iteration count)

Format: `**Latest:** <verdict> (<date>) — iteration <N> of 3`

When a new iteration entry is appended below, update the Latest line to reflect the new state. Don't leave a stale Latest line — that's the field everything downstream reads.

## Iteration entries

Each iteration entry uses an `### Iteration N — YYYY-MM-DD HH:MM` heading.

The body of the iteration entry is the full evaluation report (same shape as Mode 1 Phase 6 emits to the operator):

```markdown
### Iteration N — YYYY-MM-DD HH:MM

**Evaluated:** YYYY-MM-DD HH:MM
**Artifact type:** <detected-type>
**Spec sources loaded:** [<source1>, <source2>, ...]
**Verdict:** PASS | NEEDS REVISION (minor) | NEEDS REVISION (substantive) | FAIL

#### Hard requirements
- [✓] Frontmatter present and well-formed
- [✗] Schema validation — missing aggregateRating block (spec source: `_template-service-brief.md` §4.5 F)

#### Quality dimensions
- [✓] Citation density: 12 inline citations vs target 10+
- [Partial] Plain language compliance: 3 jargon-heavy sentences flagged
- [✗] Attribute density: 1 named brand in problem cards vs target 3+

#### Discipline rules
- [✓] Non-destructive editing
- [✓] Plain-language conventions honored

#### Root cause (when applicable)
<one-paragraph explanation>

#### Suggested fixes
1. <specific edit>
2. <specific edit>
```

Followed (if applicable) by a single-line revision-prompt log:

```markdown
**Revision prompt:** generated 2026-05-28 11:42; saved at `<artifact-path>.revision-prompt.md`
```

## Ship record

When an artifact reaches PASS and ships (e.g., a Core 30 page gets published to WordPress, a brief gets handed to a scaffolder), add a ship-record line below the latest iteration:

```markdown
**Shipped:** 2026-05-29 — <what the ship was> (e.g. "published to evelectric.pro via publish-core-30-page.py")
```

Ship records let the dashboard distinguish artifacts that passed but haven't been used yet from artifacts that passed and are now in service.

## Artifact's own frontmatter pointer

The artifact being evaluated gets three frontmatter fields:

```yaml
quality-log: "[[_quality-log#<artifact-slug>]]"
last-evaluated: YYYY-MM-DD
last-verdict: PASS | NEEDS REVISION (minor) | NEEDS REVISION (substantive) | FAIL
```

The wikilink in `quality-log:` is the slug-only form per `conventions.md` § Cross-task wikilink convention. Obsidian resolves the link to the per-artifact section in the folder log.

These three fields are the load-bearing audit hooks for downstream gates:

- Phase 3 publish gate reads `last-verdict:` and `last-evaluated:` (with a 7-day staleness window)
- Phase 6 auto-approve reads `last-verdict:` + a future `quality-confidence:` field
- The Dataview dashboard aggregates `last-verdict:` across artifacts to surface ship-ready vs iterating state

## 6-month archive convention

To keep the folder log scannable, iteration entries older than 6 months move to `_quality-log-archive.md` in the same folder.

Process (run quarterly or when the folder log exceeds ~1000 lines):

1. Identify iteration entries with timestamps older than 6 months.
2. Cut those entries from `_quality-log.md`; paste into `_quality-log-archive.md` under the same `## <artifact-slug>` section structure.
3. In the live `_quality-log.md`, leave a single line at the top of each affected artifact section: `**Earlier iterations:** see [[_quality-log-archive#<artifact-slug>]]`.
4. The `Latest:` line and ship record stay in the live file.

The archive file has the same frontmatter shape as the live log but with `status: archive` and no counters.

## Cross-folder dashboard

The aggregator query lives at `_meta/dashboards/quality-loop-dashboard.md`. It surfaces:

- Total artifacts tracked across the vault
- Distribution across PASS / NEEDS REVISION / FAIL
- Folders with high iteration counts (signal: spec sources may need clarification)
- Recent ship records
- Escalated artifacts awaiting operator judgment

Phase 1 ships the dashboard skeleton (one Dataview block aggregating folder-quality-log frontmatter); Phase 6 elaborates it.

## What to do if the folder log doesn't exist yet

Mode 1 Phase 6 creates the folder log if absent. Initial state:

```yaml
---
type: folder-quality-log
status: active
created: <today>
last-updated: <today>
artifacts-tracked: 1
shipped: 0  # or 1 if the first verdict is PASS
iterating: 0  # or 1 if the first verdict is NEEDS REVISION
escalated: 0
tags: [folder-quality-log, quality-loop]
---

# Quality log — <folder name>

This file tracks every output-quality-loop evaluation for artifacts in this folder.
One section per artifact; iteration history inside each section.

See [[output-quality-loop|the skill]] for evaluation methodology and the verdict-rollup thresholds.

---

## <first-artifact-slug>

**Latest:** <verdict> (<date>) — iteration 1 of 3

### Iteration 1 — <timestamp>

[full evaluation report]
```

Per the standing `feedback_check_folder_structure_before_writing.md` memory: before creating the folder log, `ls` the folder, read any existing `_README.md` to confirm placement convention. The folder log goes at the folder root, not inside a subfolder.

## Update path

When the folder log shape changes (new counters, new section types), update this file first, then the SKILL.md Phase 6, then the dashboard query.

The folder log shape is meant to be stable — downstream gates depend on it. Substantive changes require an operator-approved migration of existing folder logs across the vault.
