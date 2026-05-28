# PULL mode operating prompt

This is the executor-facing prompt invoked when intel-routing skill PULL mode fires. Follow the steps in order; do not skip stages.

## Step 0 — Confirm the project slug

Operator's invocation should include a project slug (or recognizable project name). If missing or ambiguous, ask:

> Which project should I triage? Provide the slug (e.g., `ev-electric-services`, `s-and-h-contracting`, `keelworks`, `dad-businesses`, etc.).

If invocation includes `--lookback <days>`, record the value; otherwise default to 14.

## Step 1 — Precondition checks

Run these in order. Halt on first failure.

1. **Resolve the project folder.** Search `04_projects/{clients/_active,clients/_private,personal}/<slug>/`. If no match, BLOCKED with the unresolved slug.

2. **Read the project README** at `<project-folder>/README.md`. Verify `archetypes:` is declared in frontmatter. If missing, BLOCKED ("project README missing required `archetypes:` field; declare archetypes before re-invoking PULL").

3. **Check `archived:` flag.** If `archived: true` on the README, BLOCKED ("project is archived; PULL does not operate on archived projects").

4. **Check for `_intel-inbox.md`.** If exists, proceed. If missing, surface a one-question gate:

   > Project has no `_intel-inbox.md` at `<expected-path>`. Scaffold from `_meta/templates/template-intel-inbox.md` and proceed? (yes / no)

   On yes: read the template, fill `project:` and `archetypes:` from the README, write the inbox file to `<project-folder>/_intel-inbox.md`. On no: BLOCKED.

5. **Read convention spec** at `~/workspace/second-brain/_meta/conventions.md` Project applicability fields section. Skill is read-only on the convention.

If any precondition fails, emit:

```
PULL BLOCKED on precondition failure.

Failed precondition: <name>
Required: <what's needed>
Suggested remediation: <what operator should do>

PULL will NOT proceed until precondition is resolved.
```

Exit.

## Step 2 — Gather inputs

In this order:

1. **Project README full content.** Extract:
   - `archetypes:` (load-bearing for query)
   - `applicability-confidence:` (project-level signal)
   - `archived:` (already checked)
   - Body skim for current-state signals — keywords like "active engagement," "in flight," "Phase 1," "blocked," "paused," "pre-build," "pre-launch," "waiting on <X>." Used in Stage A3 pre-classification.

2. **Project `_intel-inbox.md` full content.** Extract:
   - `archetypes:` (for sync validation against README)
   - Most recent "Last triage" date and counts
   - Existing applied/kept/deferred lists (continuity context)

3. **Convention spec.** Re-read on every invocation; spec changes get picked up.

4. **Enumerate existing bridge notes** in `<project-folder>/`. Use bash:
   ```
   find <project-folder> -maxdepth 1 -name "bridge-*.md" -type f
   ```
   Hold the list for Stage A2 already-bridged tagging.

5. **Run the surface query.** PULL implements the equivalent of the inbox Dataview query:
   - Folders: `03_domains/`, `05_shared-intelligence/`, `00_inbox/decisions-pending/`
   - Match: artifact's `applies-to-projects:` contains `<project-slug>` OR any of artifact's `applies-to-archetypes:` overlaps any of project README's `archetypes:`
   - Suppression: artifact's `routed-at:` is unset OR `routed-at:` < (today - lookback)
   - Exclude: artifacts with `archived: true`
   - Sort: by `applicability-confidence` DESC (high > medium > low > unset), then by `file.mtime` DESC

   In execution environments without Dataview (Cowork shell), implement via bash + Python: enumerate matching files via `find`, parse frontmatter with PyYAML, filter and sort in Python, output the result set.

## Step 3 — Compute Stage A surface

### Step 3a — Project↔inbox archetype sync validation

Compare README `archetypes:` against inbox `archetypes:`.

- **Matched** — proceed; no surface entry needed at Gate 1 beyond a single "Match: matched" line.
- **Inbox subset of README** (README has extras) → surface as warning at Gate 1:
  > README archetypes: [<list>]; inbox declares only [<list>]. Sync inbox to README? (yes / proceed-anyway / exit)
- **Inbox superset of README** (inbox has extras) → same warning, opposite direction.

If operator approves sync:
1. Edit the inbox file frontmatter `archetypes:` to match README.
2. Re-run Step 2.5 surface query with the synced archetypes.
3. Re-emit Stage A.

If operator picks "proceed anyway," use the inbox archetypes for the query (matching the Dataview behavior); record the choice for the Last-triage friction note.

### Step 3b — Tag each surfaced artifact

For each artifact in the result set, compute:

- **Match type** — `slug-named` if `<project-slug>` appears in the artifact's `applies-to-projects:`; otherwise `archetype-overlap`.
- **Signal 2 status** — same logic as PUSH Step 3a: infer artifact's situational state from body (post-launch-shaped / pre-launch-shaped / agnostic). Compare to project's situational archetypes from README. Conflict = artifact post-launch + project pre-launch-only, or vice versa.
- **Existing confidence** — from artifact's `applicability-confidence:`; record `not-set` if missing.
- **Bridge already exists** — boolean from the existing-bridge list. Filename pattern: `bridge-<artifact-slug>-to-<project-slug>.md`. Match against each surfaced artifact's slug.
- **Routed-at** — from artifact's `routed-at:`; record `not-set` if missing.
- **One-line body summary** — executor's read of what the artifact is about. One sentence.

### Step 3c — Pre-classify into bins

Apply rules in order; first matching rule wins:

1. **Bridge already exists** → `already-bridged`
2. **Signal 2 conflict AND archetype-overlap-only** → `not-applicable` (reason: "situational conflict (archetype-overlap-only): artifact <state>, project <state>; archetype-sharpen to suppress")
3. **Signal 2 conflict AND slug-named** → `defer` (reason: "situational conflict: artifact <state>, project <state>; activate on project transition"). Do NOT default to not-applicable for slug-named conflicts — the slug is present because someone decided the artifact applies eventually; preserve the routing.
4. **Slug-named AND body content directly actionable in current project state** → `apply`. "Directly actionable" = work can ship under current state (active deployment OR a known blocker-recovery path applies to this artifact specifically). Examples: Core 30 tactic on EV (active); GSC self-takeover pattern on S&H (actionable via Haris-outreach despite pre-launch state).
5. **Slug-named AND project active AND body not immediately actionable (already in context)** → `keep` (reason: "slug-named + already in engagement context; revisit on next triage"). Most slug-named items on active client projects.
6. **Slug-named AND project blocked/pre-deployment AND body not actionable now** → `keep` (reason: "applicable but project currently <blocker>; activate when <unblocker>"). Foundational artifacts that will apply once state changes.
7. **Slug-named AND project blocked AND artifact names a future-gated lane** → `defer` (reason: "slug-named but gated on <future event>"). Examples: Featured.com / Qwoted / image-link-building lanes on EV gated by Phase-1 audit.
8. **Archetype-overlap only AND project active** → `defer` (reason: "archetype match, no explicit body naming; defer pending review")
9. **Archetype-overlap only AND project blocked/pre-deployment** → `defer`
10. **Existing confidence is `low`** → bias toward `defer` regardless

For each item, record bin + reason for Gate 1 surface.

**Asymmetry with PUSH on signal 2.** PUSH excludes situational-conflict projects from routing (operates at routing-time, no future obligation). PULL defers slug-named situational conflicts (operates on cadence; re-evaluates as project state changes). `not-applicable` is reserved for archetype-spurious matches the operator should sharpen out.

### Step 3d — Compute counts

- Total surfaced
- Slug-named vs archetype-overlap split
- Suppressed (routed within lookback) — count the artifacts that matched the query body but were filtered out by the routed-at suppression. This is informational; surface at Gate 1.
- Per-bin counts (apply / keep / defer / not-applicable / already-bridged)

## Step 4 — Surface Gate 1 (batched triage approval)

Emit in this format:

```
PULL TRIAGE — <project-slug>

Project name: <project-name>
Project README: <full path>
Inbox file: <full path>
Lookback window: <days> (suppressing items with routed-at after <date>)
Last operator triage: <date from inbox Last triage section, or "first triage">

Sync status:
  README archetypes: [<list alphabetized>]
  Inbox archetypes: [<list alphabetized>]
  Match: <matched | inbox-subset-of-readme | inbox-superset-of-readme>
  (If mismatched, ask the sync question here BEFORE listing bins.)

Items surfaced: <total>
  slug-named: <count>
  archetype-overlap-only: <count>
Items suppressed (routed within lookback): <count>
Items already bridged (informational): <count>

==== APPLY (proposed: M) ====
  - [[<artifact-slug>]] (<type>, confidence: <c>)
    <one-line body summary>
    Reason: <pre-classification reason>
  ...

==== KEEP (proposed: M) ====
  - [[<artifact-slug>]] (<type>, confidence: <c>)
    <one-line body summary>
    Reason: <pre-classification reason>
  ...

==== DEFER (proposed: M) ====
  - [[<artifact-slug>]] (<type>, confidence: <c>)
    <one-line body summary>
    Reason: <pre-classification reason>
  ...

==== NOT APPLICABLE (proposed: M, situational conflict) ====
  - [[<artifact-slug>]] (<type>)
    Conflicting situational: <archetype>
    Reason: <situational conflict description>
  ...

==== ALREADY BRIDGED (informational: M) ====
  - [[<artifact-slug>]] → <existing-bridge-filename>
  ...

Confirm bins as proposed / move <item> to <bin> / move all <bin> to <bin> /
sharpen archetypes on <item> / lower confidence on <item> to <level> /
refresh bridge on <item> / reject?
```

If the inbox has a long-gap signal (last triage >60 days ago, or never), prepend a one-line note above the bins:

> Long gap since last triage (<N> days). Surface size <count> reflects accumulation. Consider triaging in batches; you can re-invoke with `--lookback 30` for a tighter window.

Wait for operator response.

### Gate 1 response handling

- **Confirm bins as proposed** → proceed to Step 5
- **Move <item-slug> to <bin>** → re-bin; re-emit updated bins; wait for confirm
- **Move all <bin-X> items to <bin-Y>** → bulk re-bin; re-emit; wait for confirm
- **Sharpen archetypes on <item-slug>: drop <archetype>** (only valid for `not-applicable` items) → record archetype-sharpening for Stage C; surface updated proposal at Gate 2 with the operation noted
- **Lower confidence on <item-slug> to <level>** (only valid for `defer` items) → record confidence write for Stage C
- **Refresh bridge on <item-slug>** (only valid for `already-bridged` items) → move item to `apply` with refresh flag (Stage C will overwrite the existing bridge file)
- **Reject** → exit without any writes; no inbox update

## Step 5 — Compute Stage B bridge-note proposal

For each operator-approved `apply` item, draft a bridge note proposal using the same template as PUSH:

```yaml
---
type: bridge-note
status: draft
created: <today>
updated: <today>
project: <project-slug>
source-artifact: "[[<artifact-slug>]]"
applies-to-projects: [<project-slug>]
tags: [bridge-note, <project-slug>]
---

# Bridge: <artifact-title> → <project-name>

**Source:** [[<artifact-slug>]]
**Filed:** <today>

## Why this applies to <project-name>

<1-2 paragraph operational framing. Reference: what signal in artifact body makes it actionable for this project now; how it intersects with current project state per README.>

## Concrete action items

1. <action item>
2. <action item>
3. <action item>
(1-3 items typical)

## Punchlist entry (proposed)

> <one-line punchlist entry; goes into project's _punchlist.md>

## See also

- [[<artifact-slug>]] (source)
- [[<project-slug>/README]] (project context)
```

Bridge filename: `bridge-<artifact-slug>-to-<project-slug>.md`. Truncate artifact-slug if filename exceeds 80 chars per conventions.

Default: one bridge per applied artifact. If an apply item is a synthesis covering 5+ tactics, prepare a per-tactic-bridge opt-in offer for Gate 2 (do NOT auto-include).

## Step 6 — Surface Gate 2 (bridge-note approval gate)

Emit:

```
BRIDGE-NOTE PROPOSALS — <project-slug>

<N> bridges proposed (one per applied artifact):

  1. <project-folder>/bridge-<artifact-1-slug>-to-<project-slug>.md
     Action items: <count>
     Punchlist: <one-line proposed entry>

  ...

Per-bridge content (expanded):

  --- Bridge 1: <project-folder>/<bridge-filename> ---
  <full proposed bridge body>

  --- Bridge 2: ... ---
  ...
```

If any apply item is a synthesis covering 5+ tactics, append:

```
Per-tactic bridges (opt-in — default off):
  <Synthesis-artifact-slug> covers <N> promoted tactics. Default discipline
  (single-bridge-per-cluster): one cluster-level bridge per applied artifact. Opt in for
  per-tactic bridges by saying "also add per-tactic bridges on <artifact-slug>" — produces
  <N> additional bridges for that artifact.
```

Always close with:

```
Confirm all / modify per bridge / skip per bridge / reject all?
```

Wait for operator response.

### Gate 2 response handling

- **Confirm all** → proceed to Step 7
- **Modify bridge <N>** → operator edits content; accept edits; re-emit Gate 2
- **Skip bridge <N>** → exclude from writes; the corresponding artifact's `routed-at:` still updates at Stage C (apply was confirmed at Gate 1); the punchlist entry for that artifact is also skipped
- **Add per-tactic bridges on <artifact-slug>** → expand proposal; re-emit Gate 2
- **Reject all** → exit; no writes including no per-item frontmatter changes; no inbox update; clean no-op

## Step 7 — Stage C writes

Perform in this order. All-or-nothing semantics — any failure rolls back all touched files to pre-Step-7 state.

1. **For each `apply` item with approved bridge:**
   - Write bridge file to `<project-folder>/bridge-<artifact-slug>-to-<project-slug>.md` using Write tool. If a file already exists at the path (refresh case), use Write to overwrite.
   - Append punchlist entry to `<project-folder>/_punchlist.md`. If the file doesn't exist, create with minimal frontmatter:
     ```yaml
     ---
     type: punchlist
     project: <project-slug>
     status: active
     created: <today>
     tags: [punchlist, <project-slug>]
     ---

     # Punchlist — <project-name>

     ## Open

     - <new entry from this PULL>
     ```
     If it exists, append under the current `## Open` section (or top-level list).
   - Update artifact's `routed-at:` to today via Edit tool. If field doesn't exist, add it after the last frontmatter field (just before closing `---`).

2. **For each `apply` item where operator skipped the bridge at Gate 2:**
   - Update artifact's `routed-at:` to today (apply still applied; no bridge / punchlist).

3. **For each `defer` item where operator explicitly lowered confidence at Gate 1:**
   - Update artifact's `applicability-confidence:` to the new level.

4. **For each `not-applicable` item:**
   - Default (operator did not opt for archetype-sharpening): remove `<project-slug>` from artifact's `applies-to-projects:` list using Edit tool. Resulting empty list becomes `[]`; do not remove the field itself.
   - If operator opted for archetype-sharpening: remove the named archetype(s) from `applies-to-archetypes:`. Do NOT touch `applies-to-projects:`.

5. **Update `_intel-inbox.md` Last triage section.** Use Edit tool to replace the existing "Last triage" block with:
   ```
   **Date:** <today>
   **Items surfaced:** <total>
   **Items applied:** <count> → bridge notes filed in this folder; punchlist entries appended
     - [[<artifact-1-slug>]]
     - [[<artifact-2-slug>]]
     - ...
   **Items kept:** <count>
   **Items deferred:** <count>
   **Items marked not-applicable:** <count>
   ```
   If operator surfaced a friction observation at Gate 1 or Gate 2, append a one-paragraph friction block below the counts. Otherwise omit.

6. **Verify writes** by reading each touched file. On any failure, revert all touched files to pre-Step-7 state. Report failure mode.

## Step 8 — Completion report

Emit:

```
PULL COMPLETE — <project-slug>

Triage outcome:
  Applied: <count> (bridges + punchlist + routed-at updates)
  Kept: <count> (no writes)
  Deferred: <count> (<N> with confidence lowered)
  Not-applicable: <count> (<N> via slug-removal, <N> via archetype-sharpening)
  Already-bridged (skipped): <count>

Files written:
  Bridges: <N>
    <bridge-1-path>
    ...
  Punchlist appends: <N>
    <punchlist-path>
  Artifact frontmatter updates: <N>
    <artifact-path>: <fields changed>
    ...
  Inbox Last-triage updated: <inbox-path>

Suggested commit (stages by name):

cd ~/workspace/second-brain
git add \
  <bridge-1-path> \
  <bridge-2-path> \
  <punchlist-path> \
  <artifact-1-path> \
  <artifact-2-path> \
  ...
  <inbox-path>
git status  # verify nothing unintended is staged
git commit -m "Triage <project-slug> intel inbox via intel-routing PULL

<N> applied, <N> kept, <N> deferred, <N> not-applicable.
<Optional one-line friction observation if surfaced.>

Refs: _meta/specs/intel-routing-skill-spec.md"
```

Stop. Do not chain into PUSH or BOOTSTRAP. Operator commits manually after reviewing diffs.

## Edge cases

- **Zero items surfaced.** Emit completion report with all counts at zero. Still update inbox Last-triage section with today's date and "0 items surfaced" so cadence is recorded. No bridges written. Don't BLOCK.
- **Every apply has bridge-already-exists after Gate 1.** Stage B emits no bridges. Stage C only updates inbox Last-triage. Report PULL completed with "no new bridges written; all applied items had existing bridges (operator did not refresh)."
- **Surfaced item has `applies-to-projects: []` and matched only by archetype.** Operator picks not-applicable → only archetype-sharpening is available (no slug to remove). Surface this constraint at Gate 1.
- **Inbox sync was approved.** Sync writes the inbox `archetypes:` before re-running the query. Subsequent Stage C inbox update at Step 7.5 overwrites only the Last triage section; the sync write stays.
- **Long-gap-since-last-triage signal.** Inbox last-triage date >60 days old (or never) → surface a one-line note above bins recommending tighter lookback or batch processing.
- **Operator runs PULL twice in same day.** Second invocation surfaces only items routed BEFORE today's first-PULL routed-at updates. Effectively idempotent on the apply side; defer/keep can shift if operator changes mind. Inbox Last-triage section gets overwritten with the second triage's counts.
- **`current-blocker:` field on project README (v1.2 forward reference).** Pre-launch projects produce heavy defer ratio (friction #11). v1.1 surfaces the friction observation but does not auto-defer; operator handles via "Move all <bin> to <bin>" at Gate 1. v1.2 may introduce a `current-blocker:` field that auto-defers archetype-overlap items not relevant to the blocker.
