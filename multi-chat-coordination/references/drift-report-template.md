# Drift Report Template

The structured report Mode 2 (AUDIT) produces. Read this before generating an audit so the output shape stays consistent across runs.

## Header

```markdown
# Tracker drift report — YYYY-MM-DD HH:MM

Tracker audited: `~/workspace/second-brain/_meta/handoffs/_active-chats-tracker.md`
Tracker `last-change` timestamp: <copy the most recent timestamp from frontmatter>
Audit scope:
- N rows in "Active / in-flight"
- N rows in "Recently closed" (past 14 days)
- N rows in "Ready to spawn next"
- N rows in "Queued — Tier 2"
- N rows in "Queued — Tier 3"
- N scheduled Cowork tasks
- N rows in "Recently completed (past 7 days)"
- N rows total across all tables

YAML parse check: ✅ OK / ❌ FAILED — <error if failed>

Handoff files referenced: N total, M unique
Handoff files found on disk: N
Handoff files missing on disk: N
```

The header gives the operator a single-glance summary of audit scope. If YAML parse fails, that's a blocking issue — surface it first and stop further audit work until the operator approves a fix.

## Drift findings

Group findings into four categories:

```markdown
## Findings

### STALE in-flight rows

Rows in "Active / in-flight" whose handoff file already has `status: consumed`.

<for each, list:>
- **Row:** <chat name>
  - Handoff path: <path>
  - Tracker says: ⏳ In-flight (started YYYY-MM-DD)
  - Disk says: status: consumed (consumed YYYY-MM-DD per frontmatter)
  - Evidence: <quote relevant frontmatter line>
  - Proposed fix: move row from "Active / in-flight" to "Recently closed" with outcome paragraph drawn from <source — exec log path, or handoff's actual-deliverable note>

If none: "None — all in-flight rows correspond to handoffs still marked `status: active`."

### MISSING from tracker

Handoff files that appear consumed (status: consumed in frontmatter) within the past 14 days but have no corresponding row in any tracker table.

<for each, list:>
- **Handoff:** <path>
  - Consumed: YYYY-MM-DD per frontmatter
  - Tracker has no row referencing this handoff
  - Evidence: <quote actual-deliverable line if present>
  - Proposed fix: add a row to "Recently closed chats" + a one-liner to "Recently completed (past 7 days)" using the handoff's actual-deliverable as the outcome cell

ALSO: Execution logs from today not matched to any tracker row (chat shipped but tracker doesn't know).

<for each, list:>
- **Execution log:** <path>
  - Last modified: YYYY-MM-DD
  - No tracker row references this exec log
  - Proposed fix: cross-check whether a consumed handoff exists for this work; if yes, surface it in the previous list; if no, add a row for the operator-driven chat (handoff cell: "n/a (operator-driven)")

If none: "None — every consumed handoff and today's execution logs have matching tracker rows."

### STATUS DRIFT

Rows whose tracker state contradicts the handoff state in non-stale ways. Includes:

- Queue rows (Ready-to-spawn / Tier-2 / Tier-3) where the handoff is `status: consumed` (suggests the chat already shipped but the queue row was never struck-through)
- Strike-through rows that say "✅ Shipped YYYY-MM-DD" but the handoff still says `status: active` (suggests the strike-through was added prematurely or the closing protocol didn't run)
- Recently-closed rows that point to a handoff still marked `status: active` (suggests the row was created but the handoff frontmatter never flipped)

<for each, list:>
- **Row:** <chat name>
  - Location: <which table>
  - Tracker says: <state>
  - Disk says: <state>
  - Proposed fix: <flip handoff status / move tracker row / both>

If none: "None — every tracker row's state matches its handoff's frontmatter."

### FRONTMATTER ISSUES

Handoff frontmatter issues that don't fit the above categories. Includes:

- Consumed handoffs missing the `consumed:` date line
- Consumed handoffs with neither `actual-deliverable:` frontmatter nor an "Actual deliverable" blockquote in the body
- Handoffs whose YAML doesn't parse (typos in field names, unquoted colon-space values, etc.)
- Handoffs missing required fields (`type:`, `status:`, `created:`, `purpose:`, `tags:`)
- Handoffs whose `type:` is not `handoff`

<for each, list:>
- **Handoff:** <path>
  - Issue: <specific problem>
  - Evidence: <quote the problematic line>
  - Proposed fix: <concrete edit>

If none: "None — every referenced handoff has valid, complete frontmatter."
```

## Patch proposals (batched A/B/C)

After the findings, propose patches grouped into labeled batches per the batch-approval discipline (memory `feedback_batch_approval_for_vault_moves`).

```markdown
## Proposed patches

### Batch A — <category> (N edits)

<one-paragraph rationale — what these patches share, why batch them together>

| Target | Edit | Why |
|---|---|---|
| <file:section> | <concrete edit description> | <one-line rationale> |
| ... | ... | ... |

### Batch B — <category> (N edits)

<rationale>

| Target | Edit | Why |
|---|---|---|
| ... | ... | ... |

### Batch C — <category> (N edits)

<rationale>

<table>

### Out of scope (NOT proposing to apply)

Things considered and rejected. Naming them prevents the operator wondering whether you missed something.

- **<edit considered>** — <reason for not proposing it>
- ...

---

Reply with batches to approve (e.g., "A, B" or "all" or "A only, hold B and C").
```

**Batch sizing rules:**

- Each batch is internally coherent — same target file or same category of edit (stale-row cleanup, frontmatter fix, missing-row addition).
- Each batch is small enough that "approve the whole batch" is a reasonable unit.
- Three batches is a healthy maximum. If you find yourself proposing more than four batches, consider whether some are too granular and should merge.
- Always include the "Out of scope" section — even if empty (then say "None — every drift surfaced has a proposed patch above").

## Post-approval section (only fill in after operator replies)

```markdown
## Applied patches

Operator approved: <batches approved>
Operator skipped: <batches not approved>

### Edits applied

<for each applied batch, list the actual edits made>

- <file:section>: <change> ✅
- ...

### YAML re-parse check

After applying tracker edits, re-ran:

\`\`\`
python3 -c "import yaml, re; m = re.match(r'^---\n(.*?)\n---\n', open('_meta/handoffs/_active-chats-tracker.md').read(), re.DOTALL); yaml.safe_load(m.group(1)); print('OK')"
\`\`\`

Result: ✅ OK / ❌ FAILED — <error and fix>

### Updated tracker `last-change`

The `last-change:` value was updated to:

'<new prose summarizing this audit pass — wrapped in single quotes per the convention>'
```

## Empty-state report (no drift)

When the audit comes back clean, the report is short. Use this shape:

```markdown
# Tracker drift report — YYYY-MM-DD HH:MM

Tracker audited: `~/workspace/second-brain/_meta/handoffs/_active-chats-tracker.md`
Tracker `last-change` timestamp: <quote>
YAML parse check: ✅ OK
Handoff files referenced: N total, M unique
Handoff files found on disk: N (all)
Handoff files missing on disk: 0

## Findings

✅ **Zero drift detected.**

- All N in-flight rows correspond to handoffs marked `status: active`.
- All N recently-closed rows correspond to handoffs marked `status: consumed` with valid `consumed:` dates and actual-deliverable notes.
- All N queue rows correspond to handoffs marked `status: active`.
- All N struck-through rows correctly mirror promoted rows elsewhere in the tracker.
- Frontmatter on all N referenced handoffs parses cleanly and contains required fields.
- Today's execution logs all have matching tracker rows.

No patches needed.

## Note

The tracker is healthy. Next audit recommended after the next significant tracker pass (after one or more chats ship).
```

## Format and voice

- **Plain language** per `~/workspace/second-brain/_meta/plain-language-conventions.md`. Drift reports should read like a colleague walking the operator through what they found, not a compliance scanner output.
- **Concrete over abstract.** "The row says ⏳ In-flight but the handoff says consumed" beats "Status discrepancy detected."
- **Quote the evidence.** When citing a frontmatter line, paste the actual text. The operator should be able to verify the finding without opening the file.
- **Propose, don't apply.** The report is a proposal; the operator approves; only then does the skill write. Never apply patches without explicit per-batch approval.

## Related

- `./tracker-row-shapes.md` — the row shapes AUDIT validates against
- `./handoff-frontmatter-spec.md` — the frontmatter shape AUDIT validates against
- Memory `feedback_batch_approval_for_vault_moves.md` — the batch-approval discipline this report follows
