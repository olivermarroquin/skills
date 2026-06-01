# Aggregation algorithm — Step-by-step walking + parsing

The deterministic core of AGGREGATE mode. Same vault state in → byte-identical block out (modulo the single "Generated:" timestamp line, which the regression test strips before comparison).

This reference documents the exact walking order, parsing rules, and rendering shape AGGREGATE uses. When the parser or renderer evolves, this file is the source of truth.

## Walking roots

The aggregator walks exactly two roots:

```
~/workspace/second-brain/04_projects/clients/_active/
~/workspace/second-brain/04_projects/personal/
```

`clients/_archive/` and `clients/_private/` are intentionally skipped:

- `_archive/` holds closed-out client work. Status digests would be wrong by definition.
- `_private/` holds NDA / pre-signature client material — even reading frontmatter risks leaking project existence into a rollup that ships into the master tracker.

If a future root appears (`04_projects/community/`, `04_projects/research/`), add it to this list, document the rationale here, and update `references/marker-conventions.md` if the rendering order needs adjustment.

## Per-directory decision

For each immediate child directory under a walking root:

```python
def should_aggregate(dir_name: str) -> bool:
    if dir_name.startswith('_'):
        return False  # meta-folder: _archive, _private, _strategic-decisions, etc.
    if '<' in dir_name or '>' in dir_name:
        return False  # placeholder/template: <client-slug>, <project-name>
    if dir_name.startswith('.'):
        return False  # hidden / dotfile
    return True
```

Resulting candidate projects → use the directory name verbatim as the project slug. The slug is the join key between the digest's `project:` field, the project folder name, and the rollup block heading.

**Slug-mismatch check.** When a digest's `project:` frontmatter doesn't match its parent folder name, surface as a non-blocking warning ("digest slug `X` doesn't match folder name `Y`"). Use the folder name as authoritative for the rollup so the master tracker stays consistent with on-disk reality.

## Digest discovery

For each candidate project, look for:

```
<project-dir>/_chat-status.md
```

Filename is literal `_chat-status.md`. Per the Phase 1 actual-deliverable note in `phase-1-per-project-chat-tracker-shape.md`, this filename was chosen specifically to non-destructively coexist with EV's legacy `_status.md` project-wide status doc. The aggregator does **not** look for `_status.md` — those are legacy project status prose docs, not the machine-readable digest.

Four outcomes per project:

1. `_chat-status.md` exists and parses cleanly → full project block.
2. `_chat-status.md` exists but YAML parse fails → "digest parse error" project block with the parser's error message.
3. `_chat-status.md` is missing entirely → "no status digest found" project block with the Phase 1 pattern pointer.
4. The project folder is empty or doesn't contain a README either → still surface as "no status digest found"; do NOT silently skip. Empty folders should be visible.

## YAML parsing

Use the regex-based frontmatter extractor — never naive `split('---')`. Reason: literal `---` sequences inside string values (most commonly `current-focus:`, but also possible in `last-closed-summary`) will fool naive splitters and silently corrupt parsed data.

```python
import yaml, re

def parse_digest(path: str) -> dict | None:
    text = open(path).read()
    m = re.match(r'^---\n(.*?)\n---\n', text, re.DOTALL)
    if not m:
        return None  # no frontmatter — treat as parse error
    try:
        return yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        raise ValueError(f"YAML parse failed: {e}")
```

The aggregator records both success and failure modes per the digest spec's "Validation rules" section. Failures populate the project block but mark it with the warning.

## Required and optional digest fields

Required (from `project-status-digest-shape.md`):

- `type:` — must equal `project-status`
- `project:` — kebab-case slug
- `updated:` — ISO date
- `current-focus:` — single-line plain-language string
- `in-flight-count:` — integer
- `ready-to-spawn-count:` — integer
- `queued-count:` — integer
- `last-closed:` — ISO date
- `last-closed-summary:` — single-line plain-language string

Optional:

- `open-decisions:` — list of one-liners (default `[]`)
- `blockers:` — list of objects, each with `blocker`, `waiting-on`, `expected-clear` (default `[]`)
- `metrics:` — object with four integer fields (defaults 0 per field; entire block defaults to absent)
- `spawn-recommendations:` — list of objects, each with `chat-name`, `handoff-pointer`, `leverage-score`, `reasoning` (default `[]`)

Missing required fields generate an `incomplete_digest` warning but do not block the project block. Render absent required fields as `<unknown>` so the gap is visible.

## In-digest validation

Per the digest spec's "Validation rules (for the Phase 2 aggregator)" section, the aggregator runs these checks per parsed digest and records warnings:

| Check | Warning category | Action |
|---|---|---|
| `updated:` older than `--stale-threshold-days` (default 14) | `stale_digest` | annotate the project block with stale indicator + days-since-update |
| `in-flight-count > 0` but parser cannot find an active section in companion `_chat-tracker.md` | `count_drift` | annotate "in-flight count may not match tracker" |
| `ready-to-spawn-count != len(spawn-recommendations)` | `count_drift` | annotate "ready-to-spawn count vs recommendations mismatch" |
| any `blockers[].expected-clear` date in the past relative to today | `expired_blocker` | annotate "blocker expected to clear YYYY-MM-DD — verify" |
| any required field absent | `incomplete_digest` | render `<unknown>` cell + add warning row |

Warnings are non-blocking. Surfacing > silent-skip is the operating principle.

The `count_drift` `in-flight-count` check requires inspecting the companion `_chat-tracker.md` (counting rows in the `## 🟡 Active / in-flight chats` table excluding the empty-state row). This is the only point at which the aggregator reads `_chat-tracker.md`; it's read-only and only for the drift signal.

## Vault-wide rollup header

After parsing all digests, compute:

```
total_in_flight = sum(d.in_flight_count for d in parsed_digests)
total_ready_to_spawn = sum(d.ready_to_spawn_count for d in parsed_digests)
total_queued = sum(d.queued_count for d in parsed_digests)
stale_count = count of digests where (today - d.updated).days > stale_threshold_days
projects_without_digest = list of candidate projects with no _chat-status.md
parse_error_count = count of digests that failed YAML parse
```

Rendered as:

```markdown
### Vault-wide rollup

| Metric | Count |
|---|---|
| Total in-flight chats | <N> |
| Total ready-to-spawn | <N> |
| Total queued | <N> |
| Projects with current digest | <N> |
| Projects without digest | <N> |
| Digests with parse errors | <N> |
| Stale digests (>N days) | <N> |
```

Followed by warnings list (one bullet per warning, grouped by category) and the operator-fatigue line.

## Operator-fatigue heuristic

Sums estimated hours queued across all projects and compares against a baseline week of operator capacity. Defaults:

- Baseline: 40 hours/week of focused build time (conservative; Oliver typically does fewer).
- Source per project: from `_chat-status.md` `metrics:` block — sum `time-spent-past-7d-hours` across all projects to compute current burn rate. (Not a queued-hours field; the digest doesn't carry queued-hour estimates today. Phase 3+ may add that.)

Today's heuristic, given the digest spec's actual fields:

```
total_queued_chats = sum of queued-count across all projects
estimated_hours = total_queued_chats * 3   # 3 hours per chat is the multi-chat-coordination DECOMPOSE sizing baseline
weeks_to_clear = estimated_hours / 40
```

Rendered as one prose line:

```
**Operator fatigue signal:** ~<N> chats queued across the vault (~<H>h estimated at 3h/chat baseline → ~<W> weeks to clear at 40h/week capacity). <Comment: if weeks_to_clear > 4, surface "queue is deep — consider pruning or batch-closing">.
```

Honest approximation, not precision. Phase 3+ may refine using per-chat duration estimates if the digest spec adds them.

## Per-project block

For each parsed digest, render:

```markdown
#### <project-slug>

| Field | Value |
|---|---|
| Last updated | YYYY-MM-DD (<N> days ago)<stale annotation if applicable> |
| Current focus | <current-focus verbatim from digest> |
| In-flight / Ready / Queued | <N> / <N> / <N> |
| Last closed | YYYY-MM-DD — <last-closed-summary verbatim> |
| 7-day metrics | <chats-closed-past-7d> chats closed · <artifacts-produced-past-7d> artifacts · ~<time-spent-past-7d-hours>h |

**Top blocker:** <first blocker from blockers list — "<blocker text>" · waiting on <waiting-on> · expected clear <expected-clear>>
(omit this line entirely if `blockers: []`)

**Top ready-to-spawn:** <first 1-2 spawn-recommendations as bullets>
- <chat-name> — [[<handoff-pointer-as-wikilink>]] — leverage: <leverage-score>
(omit this section entirely if `spawn-recommendations: []`)

**Warnings:** <list non-blocking warnings inline, if any>
```

Cell rules:

- Missing required fields render as `<unknown>` (literal text including angle brackets so the gap is grep-able).
- Optional fields omit their row entirely when absent (don't render empty rows).
- `current-focus`, `last-closed-summary`, blocker text, and spawn-recommendation reasoning come through verbatim — no re-summarizing. The digest is the source of plain-language calibration.
- Wikilink rendering for `handoff-pointer`: convert a vault-relative path like `_meta/handoffs/vault-orchestrator/phase-3-orchestrator-v1-survey-and-next-moves.md` to `[[vault-orchestrator/phase-3-orchestrator-v1-survey-and-next-moves|phase-3 handoff]]` (drop the `_meta/handoffs/` prefix; project-folder-prefix the slug).

## Projects-without-digest block

For each candidate project with no `_chat-status.md`:

```markdown
- **<project-slug>** — no `_chat-status.md` digest found. Suggested action: create one following [[../../skills/multi-chat-coordination/references/project-status-digest-shape|the digest spec]]; mirror EV's pattern at [[../../04_projects/clients/_active/ev-electric-services/_chat-status|EV's digest]].
```

Group these under a clearly-marked subsection so the rollup distinguishes "no data" from "zero counts".

## Render order

The full generated section renders in this order (deterministic — same vault state → identical bytes):

1. `<!-- AGGREGATOR:BEGIN -->`
2. `## 📊 Vault-wide project rollup (generated)`
3. `> [!summary] Generated by master-tracker-aggregator skill — <N> projects scanned, <M> digests parsed`
4. `Generated: YYYY-MM-DD HH:MM` (stripped under `--no-timestamp`)
5. `### Vault-wide rollup` (counts table)
6. Warnings list (if any)
7. Operator-fatigue line
8. `### Per-project digests`
9. One per-project block per parsed digest, alphabetical by slug
10. `### Projects without status digests`
11. Bulleted list of slugs + suggested actions, alphabetical
12. Footer: `Regenerate: invoke the master-tracker-aggregator skill in AGGREGATE mode.`
13. `<!-- AGGREGATOR:END -->`

Alphabetical ordering is the idempotency anchor. Insertion order from a `find` walk is not deterministic across filesystems; sort explicitly.

## Idempotency contract

Given the same set of `_chat-status.md` files with the same contents, the same project folders, and the same flag values, AGGREGATE must produce the same bytes between markers (modulo the `Generated:` timestamp line under default flags).

Sources of nondeterminism to guard against:

- Filesystem walk order → resolved by sorting candidates alphabetically by slug.
- Python `dict` iteration order → use sorted key access when iterating digest fields.
- `set()` operations → use `sorted(list(set(...)))` if set membership is computed.
- `now()` calls → only one, for the `Generated:` line at the top. `--no-timestamp` omits it.

The regression test in `references/edge-cases.md` § idempotency check runs AGGREGATE twice with `--no-timestamp` and compares the two outputs byte-for-byte. Any difference is a deterministic-rendering bug to fix.

## See also

- `./marker-conventions.md` — where the generated section lives in the master tracker
- `./drift-detection-heuristics.md` — Mode 2's age-and-signal logic
- `./edge-cases.md` — handling broken digests, archived mid-run, slug mismatches
- `~/workspace/skills/multi-chat-coordination/references/project-status-digest-shape.md` — the data contract parsed here
- `~/workspace/second-brain/_meta/handoffs/_active-chats-tracker.md` — where the generated section is written
