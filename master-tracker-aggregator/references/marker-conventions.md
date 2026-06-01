# Marker conventions — Where the generated section lives + how to update it idempotently

The aggregator owns one and only one section of the master tracker. Everything else stays operator-edited. The marker comments are the contract — they define the boundary the aggregator is allowed to write inside.

## The markers

```html
<!-- AGGREGATOR:BEGIN -->
<!-- AGGREGATOR:END -->
```

Two HTML comments. Markdown renderers (Obsidian, GitHub, VS Code preview) hide HTML comments by default, so the markers don't appear in the rendered view. The aggregator parses them as plain-text anchors.

**Markers must be standalone lines.** The aggregator matches markers using a line-anchored regex (`^<!-- AGGREGATOR:BEGIN -->\s*$` with multiline mode), not raw substring search. Rationale: the marker strings frequently appear inside outcome paragraphs of Recently-closed rows when an aggregator-related chat is documented (e.g., the Phase 2 closing row mentions the markers by name). Line-anchored matching ignores those mentions and only treats markers on their own line as canonical. If a future edit needs to reference a marker inline, it can be wrapped in backticks or quoted — neither will register as a marker.

**Why HTML comments specifically.** Two alternatives were considered and rejected:

- Front-of-section headings (e.g., `## Aggregator-generated section (start)`) — visible to readers, easy to accidentally edit, no rendering distinction between marker and content.
- Frontmatter pointers (e.g., `aggregator-section-start-line: 42`) — line-numbers shift every time the operator edits above the section; pointer drifts.

HTML comments are invisible-by-default, unique-by-design (no chance of collision with handwritten content), and resilient to content shifts above or below.

## Default placement

The expected location inside `~/workspace/second-brain/_meta/handoffs/_active-chats-tracker.md`:

- After the `## How to use this file` section (including its subsections: Opening Protocol, Closing Protocol, Visual conventions, etc.).
- Before the first data section (`## 🟡 Active / in-flight chats`).

Visual layout:

```markdown
## How to use this file

[opening protocol, closing protocol, conventions, cleanup discipline]

<!-- AGGREGATOR:BEGIN -->
## 📊 Vault-wide project rollup (generated)

[generated content — replaced on every aggregator run]
<!-- AGGREGATOR:END -->

## 🟡 Active / in-flight chats

[hand-edited rows]
```

The rationale: the rollup is a high-altitude summary the operator wants right after the operating instructions and right before the per-row drill-down. Putting it at the very top (before "How to use") buries the operating instructions; putting it at the very bottom buries the rollup beneath 200+ lines of detail.

## Initial-installation protocol

When the aggregator runs for the first time against a master tracker that does not yet have markers:

1. Parse the master tracker to find the boundary between `## How to use this file` and the first data section.
2. Surface a proposed insertion to the operator showing the exact lines to add (`<!-- AGGREGATOR:BEGIN -->`, then the rollup content, then `<!-- AGGREGATOR:END -->`) and where they would land.
3. Wait for operator approval. Do NOT write the markers without explicit approval.
4. On approval, write the markers + initial generated section in one atomic edit.
5. Bump `last-change:` with a single-line note: `'YYYY-MM-DD (pass N) — aggregator markers installed + initial rollup generated'`.
6. Run the YAML parse check.

This installation gate is the only marker-related action that requires operator approval. Subsequent runs replace the content between existing markers without re-asking — the markers are the standing approval.

## Replace-between-markers protocol

Once markers exist, an AGGREGATE run does:

1. Read the master tracker fully.
2. Find `<!-- AGGREGATOR:BEGIN -->` (first occurrence).
3. Find `<!-- AGGREGATOR:END -->` (first occurrence after BEGIN).
4. Replace the content between (exclusive of the markers themselves) with the newly rendered block.
5. Re-write the file.
6. Bump `last-change:` with a one-liner naming the run.
7. Run the YAML parse check.

The markers themselves stay verbatim. If a future run needs to add or rename markers, that's a discipline change documented here, not a casual edit.

## Replace-content rules

The rendered block goes between the markers with one blank line of padding above and below:

```markdown
<!-- AGGREGATOR:BEGIN -->

## 📊 Vault-wide project rollup (generated)
[...]

<!-- AGGREGATOR:END -->
```

The blank lines exist so the markers don't visually fuse to the adjacent content in any renderer that does not strip comments.

The aggregator strictly replaces the content. It does NOT preserve operator edits made between the markers since the last run. If the operator typed something into the marker block, it gets overwritten. (This is the contract: the marker block is generated; the rest of the master tracker is operator-edited.)

## Sister-file mode

When invoked with `--output sister-file`, the aggregator does NOT touch the master tracker. Instead:

- Writes to `~/workspace/second-brain/_meta/handoffs/_active-chats-tracker-aggregated.md`.
- File is overwritten in full on every run (no marker discipline needed — the file IS the boundary).
- Top of the file carries a banner: `> [!warning] Auto-generated by master-tracker-aggregator. Do not hand-edit — edits will be overwritten on next run.`
- File frontmatter:

```yaml
---
type: aggregated-rollup
status: generated
generated: YYYY-MM-DD HH:MM
generator: master-tracker-aggregator
project-count: <N>
parsed-digest-count: <N>
missing-digest-count: <N>
tags: [meta, aggregator-output, rollup, generated]
---
```

The frontmatter's `generated:` timestamp is the single source of nondeterminism in sister-file mode (the analog to the `Generated:` line in inline mode). The regression test stripper handles both.

The sister file can be referenced from the master tracker via a one-line pointer in the "How to use this file" section: "**See also:** [[_active-chats-tracker-aggregated|vault-wide rollup view]] (auto-generated, do not hand-edit)." The aggregator does not add that pointer itself; the operator adds it once at installation if they prefer the sister-file view.

## Idempotent edit pattern

The aggregator does atomic edits (read full file → render new block → string-replace between markers → write full file). The atomic pattern matters because:

- A partial write between markers leaves the file in a corrupt state that the next run might not recover from.
- A non-atomic edit (multiple successive write calls) risks Obsidian or another reader catching a half-edited file and crashing or showing stale content.

Implementation pattern (pseudocode):

```python
content = read_file(master_tracker_path)
begin_idx = content.index('<!-- AGGREGATOR:BEGIN -->')
end_idx = content.index('<!-- AGGREGATOR:END -->', begin_idx)
before = content[:begin_idx + len('<!-- AGGREGATOR:BEGIN -->')]
after = content[end_idx:]  # starts with <!-- AGGREGATOR:END -->
new_block = '\n\n' + render_aggregator_block() + '\n\n'
write_file(master_tracker_path, before + new_block + after)
```

One read, one write. Anything more is a discipline violation that risks corrupting the master tracker.

## Marker-not-found behavior

If the aggregator runs and finds:

- BEGIN marker but no END marker (or vice versa) → STOP and surface as a hard error. Don't write. The master tracker is in a confused state; let the operator fix the marker before the next run.
- Multiple BEGIN markers (or multiple END markers) → STOP and surface. The first occurrence might not be the intended boundary; let the operator decide.
- Neither marker → fall into the initial-installation protocol above (propose insertion, wait for approval).

These three error modes are loud. The aggregator never silently guesses the operator's intent on marker placement.

## YAML safety after writes

After every master-tracker write, run the regex-based YAML parse check:

```bash
python3 -c "import yaml, re; m = re.match(r'^---\n(.*?)\n---\n', open('_meta/handoffs/_active-chats-tracker.md').read(), re.DOTALL); yaml.safe_load(m.group(1)); print('OK')"
```

Expected output: `OK`. Any other output → revert the most-recent edit and surface the error.

The aggregator only touches frontmatter when bumping `last-change:`. The risk: an unescaped apostrophe or unwrapped colon-space sequence in the new value breaks the YAML. The aggregator's `last-change:` writer wraps in single quotes and doubles internal apostrophes per the master-tracker convention.

## When the master tracker section adjacent to markers changes

If the operator restructures the master tracker (e.g., adds a new top-level `## Notes` section between "How to use" and the markers), the aggregator continues to work — the markers anchor on themselves, not on adjacent section headings.

If the operator moves the markers to a different location entirely (e.g., to the bottom of the file), the aggregator continues to work — the markers are the boundary; placement is operator preference.

If the operator deletes the markers, the next run falls into the initial-installation protocol and re-proposes them.

## Regression test for marker behavior

Beyond the idempotency regression in `edge-cases.md`, marker-specific regressions to spot-check after any aggregator code change:

1. **Markers preserved.** After a run, the markers themselves are still present and not modified.
2. **Content above markers unchanged.** Diff the file's prefix (everything before BEGIN) against the prior version — no aggregator-driven changes there.
3. **Content below markers unchanged.** Same check on the suffix (everything after END).
4. **One BEGIN, one END.** Counts of each marker remain at exactly 1.

If any of these regress, fix before shipping the change.

## See also

- `./aggregation-algorithm.md` — what content lives inside the markers
- `./edge-cases.md` — non-happy-path marker scenarios
- `~/workspace/second-brain/_meta/handoffs/_active-chats-tracker.md` — the master tracker the markers live inside
- `~/workspace/skills/multi-chat-coordination/SKILL.md` — the operator-facing skill whose tracker convention this composes with
