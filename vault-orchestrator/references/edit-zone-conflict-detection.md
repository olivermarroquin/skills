# Edit-zone conflict detection

How PROVISION scans drafted + in-flight handoffs for shared-file conflicts, scores each conflict, and surfaces a resolution suggestion. The detection runs after DECOMPOSE has produced the proposed handoff bodies and before the spawn-queue write.

Two chats both editing `_meta/conventions.md` is a merge-conflict footgun. Two chats both editing distinct sections of the master tracker is parallel-safe. The detection logic distinguishes the two so PROVISION can give the operator an honest recommendation instead of either silently passing risky edits or noisily flagging every co-touch.

## What counts as a "shared file"

A file is shared if a write to it from two chats running concurrently is likely to produce a merge conflict, a contract drift, or a discoverability regression. PROVISION reads each candidate handoff's `## Files to edit` and `## Files to create` sections and builds a file-set per handoff. The shared-file detector tags any file matching the patterns below.

| Pattern | Examples | Why it's shared |
|---|---|---|
| `_meta/conventions.md` (exact path) | the canonical conventions doc | Single document; every section is load-bearing; any concurrent edit risks losing one chat's changes |
| `_meta/handoffs/_README.md` | folder-level discoverability doc | Hand-edited prose with structural sections (e.g., "Vault orchestrator — state of play + next moves"); section-level race is plausible |
| `_meta/handoffs/_active-chats-tracker.md` | master tracker | Pass-numbered edits; YAML frontmatter; concurrent passes can collide on the same row |
| `_meta/handoffs/_active-chats-tracker-changelog.md` | changelog | Prepend-at-top discipline means concurrent prepends race on the same line range |
| `_meta/handoffs/_spawn-queue.md` | this skill's queue | PROVISION's own write target — any other handoff that writes here is by definition a self-conflict |
| `skills/*/SKILL.md` | any skill main file | Skill spec is single-source-of-truth per skill |
| `04_projects/clients/_active/*/README.md` | per-project READMEs (canonical project-status doc per CLAUDE.md) | Status section is volatile; concurrent edits collide |
| `04_projects/clients/_active/*/_chat-tracker.md` | per-project chat tracker | Same pattern as master tracker |
| `04_projects/clients/_active/*/_chat-status.md` | per-project digest | Machine-readable; concurrent writes corrupt YAML |
| `_meta/plain-language-conventions.md`, `_meta/working-surfaces.md`, `_meta/decision-research-conventions.md` | canonical conventions in `_meta/` | Same risk profile as `_meta/conventions.md` |
| Any `references/*.md` for a skill currently in-flight | composing skill's references | Race against the in-flight chat actively iterating on its own references |

Files **NOT** flagged (parallel-safe by design):

- New files in disjoint folders (each chat creates its own outputs)
- Per-chat execution logs (each chat owns its own log file under its project)
- Per-chat handoff files (each handoff is its own file)
- Per-project subfolder contents when projects differ

## How conflicts are scored

For each pair of (drafted-or-queued handoff, in-flight handoff) that touches at least one shared file, the detector assigns a severity:

| Severity | Trigger condition | Operator action |
|---|---|---|
| **serial-required** | Both chats edit the same shared file end-to-end (no clear section split). Default for `_meta/conventions.md` full rewrites, master tracker frontmatter passes, any SKILL.md spec rewrite. | Spawn second only after first ships. The queue order encodes the serialization. |
| **parallel-OK-with-note** | Both chats edit the same shared file but in clearly disjoint sections (e.g., chat A edits master tracker's "Ready to spawn" rows; chat B edits "Recently closed" rows). Detector inspects the handoff body for explicit section names. | Spawn concurrently; surface the disjoint-section evidence in the conflict-flag table so the operator can verify. |
| **warning-only** | Both chats edit a discoverability surface (e.g., handoffs `_README.md` "See also" sections, project README "What this is" sections) where a late-arriving chat may need to add a row. | Spawn concurrently; second chat reads the file fresh and adds its row idempotently. No serialization needed. |
| **self-conflict** | A drafted handoff's "Files to edit" includes `_meta/handoffs/_spawn-queue.md`. PROVISION owns this file; any other handoff writing here is by definition a contract violation. | Reject the drafted handoff and surface to the operator. |

The detector errs toward **serial-required** when ambiguous. Better a false positive (operator overrides to parallel) than a silent merge-conflict.

## How section-disjoint is determined

For files with established section structure (master tracker, conventions, READMEs), the detector reads the candidate handoff body for explicit section names:

- "edit the 'Ready to spawn' section" / "append to 'Recently closed'" → section-scoped
- "rewrite the tracker" / "update conventions" / "edit `_meta/conventions.md`" with no section qualifier → file-scoped (serial-required)
- Heading names in markdown code blocks inside the handoff body (e.g., "## Hot decisions sitting on Oliver's plate") that match real headings in the target file → section-scoped

If the detector cannot determine section scope confidently, it defaults to **serial-required** with a note: "Section scope not declared in handoff body — recommend serializing or splitting the handoff to name target sections explicitly."

## How operators resolve

Three resolution paths, named in the conflict-flag table:

**1. Serialize via queue order.** The lower-numbered row in the spawn queue ships first; the higher-numbered row spawns only after the first's tracker row moves to "Recently closed." PROVISION can reorder the queue at the operator's request. This is the default when severity is serial-required.

**2. Split via handoff refactor.** The operator (or a follow-up PROVISION pass) splits one handoff into two so each touches a disjoint section. Example: one handoff that "rewrites conventions" becomes two — one editing the "Naming" section, one editing "Vault stewardship" — each parallel-safe with the other.

**3. Accept-risk via explicit override.** The operator adds `conflict-override: accepted` to the handoff frontmatter with a `conflict-override-reason:` line naming why. PROVISION skips the conflict flag on next scan. The override is auditable in git and in the handoff frontmatter; do not accept-risk silently.

The conflict-flag table in `_spawn-queue.md` names each pair, the shared file, the severity, and the recommended resolution. The operator picks per row.

## Detection algorithm (PROVISION calls this)

```
inputs:
  - drafted_handoffs: list of handoff bodies + file-sets from DECOMPOSE
  - queued_handoffs: parsed from current _spawn-queue.md "Queued" section
  - in_flight_handoffs: parsed from _active-chats-tracker.md "Active / in-flight"

steps:
  1. For each handoff (drafted + queued + in-flight):
       parse "## Files to edit" + "## Files to create" sections → file-set
       parse body for explicit section qualifiers on each file
  2. For each pair (drafted, in-flight) + (drafted, queued):
       intersection = file-set(A) ∩ file-set(B)
       for each f in intersection:
         if f matches shared-file pattern:
           severity = score_severity(A, B, f, section-qualifiers)
           emit (A, B, f, severity, suggested-resolution)
  3. If any emitted severity == self-conflict:
       reject the drafted handoff and surface to operator
  4. Otherwise:
       render conflict-flag table in _spawn-queue.md
       annotate each affected row's "Conflicts" cell with → see conflict table
```

The detector is a markdown parser, not a code-aware diff tool. It catches the common cases (full-file edits, named sections) without trying to predict what every chat will actually do. False positives are acceptable; false negatives (silent conflicts) are not.

## What the detector does NOT do

- It does not run live diffs against current file content. Conflicts are predicted from handoff intent, not from speculative diff resolution.
- It does not block any spawn. The operator always sees the flag and decides.
- It does not detect conflicts within a single chat's own writes (a chat that edits the same file twice is its own problem).
- It does not detect semantic conflicts (two chats updating different sections that are nonetheless contradictory). That's a NEXT-MOVES decision-research convention call, not an edit-zone-conflict call.
- It does not track tier-3 vault files (Cowork can't read tier-3, and tier-3 writes are operator-driven by definition).

## Examples

**Example 1 — Serial-required.** Drafted handoff "Phase 2: rewrite plain-language conventions" edits `_meta/plain-language-conventions.md` end-to-end. In-flight handoff "client-onboarding-automation Phase 0" also edits `_meta/plain-language-conventions.md` (adds a section on client-facing voice). Severity: **serial-required**. Suggested resolution: serialize — spawn Phase 2 only after client-onboarding-automation Phase 0 ships.

**Example 2 — Parallel-OK-with-note.** Drafted handoff "EV blog content calendar Phase 1" appends a row to the master tracker's "Ready to spawn next" section. In-flight handoff "S&H orchestrator first-real-run" eventually moves its row to "Recently closed" at chat end. Both touch `_active-chats-tracker.md` but in disjoint sections. Severity: **parallel-OK-with-note**. Suggested resolution: spawn concurrently; both chats follow the standard tracker-edit discipline.

**Example 3 — Warning-only.** Drafted handoff "Phase 4: vault-orchestrator spawn queue" adds a `## Vault orchestrator — state of play + next moves` section to `_meta/handoffs/_README.md`. Another in-flight chat may add a different section to the same `_README.md` later. Severity: **warning-only**. Suggested resolution: spawn concurrently; second chat reads fresh and adds its row.

**Example 4 — Self-conflict.** Drafted handoff "experimental skill X" claims to write to `_meta/handoffs/_spawn-queue.md`. Severity: **self-conflict**. PROVISION rejects the drafted handoff and surfaces: "the spawn queue is owned by PROVISION; the handoff should produce a project goal that PROVISION decomposes, not write to the queue directly."

## See also

- [[../SKILL|vault-orchestrator SKILL.md]] — PROVISION mode calls this detector
- [[spawn-queue-shape|spawn-queue-shape reference]] — where conflict flags get rendered
- [[checkpoint-integration|checkpoint-integration reference]] — orthogonal discipline for long-running chats
- `~/workspace/skills/multi-chat-coordination/SKILL.md` — DECOMPOSE produces the drafted handoffs scanned here
