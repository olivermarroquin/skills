# Per-project status digest shape — Machine-readable contract

The data contract for `_chat-status.md` files. One lives beside every `_chat-tracker.md` at the root of every active project folder. The digest is **machine-readable** — the Phase 2 master-tracker-aggregator skill parses it directly without fighting markdown parsing on the human-readable `_chat-tracker.md`.

Phase 1 of the vault-orchestrator project (2026-05-30) shipped this shape together with the companion [[project-chat-tracker-shape]] spec.

## Why a separate digest

Two artifacts per project, by design:

- `_chat-tracker.md` (human-readable) — same shape as the master tracker; what the operator scans.
- `_chat-status.md` (machine-readable) — structured YAML the aggregator parses; what Phase 2+ consumes.

Separating them means humans get rich context and machines get clean structured data. The aggregator doesn't have to parse markdown tables, count emoji-prefixed callout sizes, or reason about strikethrough rows. It reads YAML once per project and rolls up.

**Filename note.** The digest is `_chat-status.md`, not `_status.md`. Some projects (e.g., EV Electric) already use `_status.md` for project-wide status prose; the `_chat-` prefix on both files (`_chat-tracker.md` + `_chat-status.md`) signals their purpose — chat-coordination state, not project-wide status — and avoids overwriting legacy files.

## File location

```
~/workspace/second-brain/04_projects/<area>/<active>/<project-slug>/_chat-status.md
```

Beside the `_chat-tracker.md` companion. Both files together represent the project's chat-coordination state.

## File format

YAML-fronted markdown. The frontmatter is the machine-readable contract; the markdown body is operator-facing notes (optional — the aggregator ignores it).

```markdown
---
type: project-status
project: <project-slug>
updated: YYYY-MM-DD
current-focus: <one-line plain-language description of what's actively being worked on>
in-flight-count: <int>
ready-to-spawn-count: <int>
queued-count: <int>
open-decisions: [<one-liner>, <one-liner>]
blockers:
  - blocker: <description>
    waiting-on: <person | external-event | dated-event>
    expected-clear: <YYYY-MM-DD | unknown>
last-closed: <YYYY-MM-DD>
last-closed-summary: <one-line plain-language>
metrics:
  chats-closed-past-7d: <int>
  chats-closed-past-30d: <int>
  artifacts-produced-past-7d: <int>
  time-spent-past-7d-hours: <approx int>
spawn-recommendations:
  - chat-name: <from ready-to-spawn>
    handoff-pointer: <vault-relative path>
    leverage-score: <high | medium | low>
    reasoning: <one-line plain-language>
---

# Status digest — <project-slug>

Machine-readable digest of this project's chat-coordination state. The Phase 2 master-tracker-aggregator parses the frontmatter above and rolls it up into a generated section of `~/workspace/second-brain/_meta/handoffs/_active-chats-tracker.md`.

Update this file alongside `_chat-tracker.md` during Opening / Closing Protocol runs. Until Phase 2 ships, this file is a placeholder — the master tracker remains the editing surface.

## Optional operator notes

Free-form prose the aggregator ignores. Useful for context the structured fields don't carry — open questions, links to recent execution logs, pointers to relevant blueprints.
```

## Field-by-field contract

### Required structured fields

**`type:`** — always `project-status`. Distinguishes from the existing `type: status` used by legacy project-wide status docs.

**`project:`** — kebab-case slug matching the parent folder name.

**`updated:`** — ISO date of last digest refresh. The aggregator uses this to flag stale digests (>14 days untouched warrants a manual recheck).

**`current-focus:`** — one-line plain-language sentence describing what the project is actively pushing on right now. Example: "Building S&H Core 30 page foundation while waiting on GBP verification clear." Should read like a colleague's answer to "what's happening on EV right now?"

**`in-flight-count:`** — integer count of rows in the per-project tracker's "Active / in-flight chats" section. The aggregator rolls this up into a vault-wide concurrency view.

**`ready-to-spawn-count:`** — integer count of rows in the per-project tracker's "Ready to spawn next" section.

**`queued-count:`** — integer count of rows in the per-project tracker's "Queued (project-scoped)" section.

**`last-closed:`** — ISO date of the most recently shipped chat in this project (from "Recently closed chats" table top row).

**`last-closed-summary:`** — one-line plain-language summary of what that most-recent chat shipped. Source: the first sentence of the "Recently closed chats" outcome cell, plain-language-rewritten.

### Optional structured fields

**`open-decisions:`** — list of one-liners, one per open decision in the per-project tracker's "Open decisions / blockers" section. Empty list `[]` is valid if no open decisions.

**`blockers:`** — list of blocker objects, each with three sub-fields. Empty list `[]` is valid.

```yaml
blockers:
  - blocker: <description of what's blocked>
    waiting-on: <named person | external system | dated event>
    expected-clear: <YYYY-MM-DD if known, "unknown" otherwise>
```

Used by the aggregator + Phase 3 SURVEY mode to surface "Project X is waiting on Y; expected to clear Z" in the state-of-vault report.

**`metrics:`** — rollup metrics block. All fields integers; absent fields default to 0 at parse time. Helps the Phase 3 NEXT-MOVES mode + Phase 4 PROVISION mode rank projects by activity.

```yaml
metrics:
  chats-closed-past-7d: <int>
  chats-closed-past-30d: <int>
  artifacts-produced-past-7d: <int>  # rough count of files produced by chats in past 7d
  time-spent-past-7d-hours: <int>     # approx, sourced from chat durations in tracker rows
```

Honest approximations beat fabricated precision. If `time-spent-past-7d-hours` is genuinely unknown, omit the field — don't guess.

**`spawn-recommendations:`** — list of spawn-recommendation objects, one per row in the per-project tracker's "Ready to spawn next" section. Empty list `[]` is valid.

```yaml
spawn-recommendations:
  - chat-name: <from ready-to-spawn row's Chat name>
    handoff-pointer: <vault-relative path to the handoff file>
    leverage-score: high | medium | low
    reasoning: <one-line plain-language reason for the score>
```

Leverage-score categories (intentionally coarse — Phase 3 NEXT-MOVES does the precise ranking):

- **high** — clears multiple downstream chats OR matches a current operator-stated priority OR is a foundation that the project depends on
- **medium** — useful, no special urgency, no immediate downstream pull
- **low** — would be nice to ship eventually; no leverage either direction today

If unsure, default to medium. The Phase 3 ranking re-evaluates with vault-wide context.

## YAML safety

Same single-quote-wrap rule applies to any value containing a colon-space sequence. The `current-focus:` line is the most common offender — plain-language summaries often contain "X: Y" patterns. Wrap it in single quotes when in doubt:

```yaml
current-focus: 'Building S&H Core 30 pages: waiting on GBP verification'
```

Apostrophes inside single-quoted YAML must be doubled (`it''s`, not `it's`).

After every digest edit, verify parses with:

```bash
python3 -c "import yaml, re; m = re.match(r'^---\n(.*?)\n---\n', open('04_projects/<area>/<active>/<project>/_chat-status.md').read(), re.DOTALL); yaml.safe_load(m.group(1)); print('OK')"
```

Expected output: `OK`.

## Honest gap surfacing

When a field cannot be honestly populated, omit it (or use `null` / empty list `[]`) — do NOT fabricate. The Phase 2 aggregator treats absent fields as missing data, not as zero. Examples:

- `metrics.time-spent-past-7d-hours` — if tracker rows don't carry duration estimates, omit the field. Don't guess.
- `spawn-recommendations[].reasoning` — if the operator hasn't articulated why a chat is high-leverage, the digest entry honestly says "leverage TBD — operator hasn't ranked yet" rather than fabricating a reason.
- `blockers[].expected-clear` — if the clear date is genuinely unknown, write `unknown`. Don't guess a date.

This honest-gap-surfacing discipline is the same pattern documented in `pattern-honest-gap-surfacing-over-silent-skip` (intel-routing Phase 2 retro 2026-05-28).

## How the aggregator consumes this

**Phase 2 master-tracker-aggregator skill (planned 2026-05-30):**

1. Walk every `_chat-status.md` in `04_projects/**` (recursive glob).
2. Parse the YAML frontmatter from each.
3. Roll up into a generated section of the master tracker (`## Aggregated project status` or similar — exact section name TBD at Phase 2 build time).
4. Flag stale digests (`updated:` >14 days ago) with a warning row.
5. Cross-reference `spawn-recommendations` lists across projects to flag conflicts (two projects both recommending edits to a shared file).

The digest is the structured input. The master tracker remains the human-editable surface. The aggregator is read-write on the master tracker's generated section only; the rest of the master tracker stays operator-edited.

## Update cadence

**Pre-Phase-2 (today):** Manual updates by the operator (or by a closing-protocol run that knows the per-project tracker exists). Update at every chat ship, every open-decision change, every blocker update. Roughly once or twice per active session per project.

**Post-Phase-2:** The Phase 2 aggregator may write back update timestamps; the Phase 4 PROVISION mode may write `spawn-recommendations` updates. Closing-protocol runs continue to update `in-flight-count` / `ready-to-spawn-count` / `queued-count` / `last-closed` / `last-closed-summary` directly.

**Phase 3+ orchestrator:** SURVEY mode reads digests, doesn't write them. NEXT-MOVES mode produces recommendations the operator approves before they land in digests.

## Validation rules (for the Phase 2 aggregator)

When Phase 2's aggregator parses a digest, it should treat these as validation warnings — not errors that block aggregation:

- `updated:` older than 14 days → "stale digest" warning row in master rollup.
- `in-flight-count > 0` but the per-project tracker's "Active / in-flight" section has zero live rows → drift warning.
- `ready-to-spawn-count` mismatches the digest list length → drift warning.
- `blockers[].expected-clear` date in the past → "blocker may have cleared — verify" warning row in master rollup.
- Any required field absent → "incomplete digest" warning; the project still appears in rollup but with `<unknown>` cells.

Validation is non-blocking by design — half a rollup is better than no rollup when one project's digest is malformed.

## See also

- [[project-chat-tracker-shape]] — companion `_chat-tracker.md` shape spec
- [[tracker-row-shapes]] — master-tracker row contract (the human-readable view this digest mirrors structurally)
- [[chat-resilience-checkpoints]] — checkpoint convention referenced from the tracker's Notes cell
- `~/workspace/second-brain/_meta/handoffs/vault-orchestrator/phase-2-master-tracker-aggregator.md` — the handoff that consumes this contract
- `~/workspace/second-brain/_meta/conventions.md` — vault-wide naming and frontmatter rules
