# PUSH mode operating prompt

This is the executor-facing prompt invoked when intel-routing skill PUSH mode fires. Follow the steps in order; do not skip stages.

## Step 0 — Confirm the artifact path

Operator's invocation should include an artifact path. If missing, ask:

> Which artifact should I route? Paste the full path (e.g., `~/workspace/second-brain/03_domains/seo/cluster-synthesis-ai-era-seo-cluster-2026-05-27.md`).

## Step 1 — Precondition checks

Run these in order. Halt on first failure.

1. Read the artifact. If path doesn't resolve, surface BLOCKED with the unresolved path.
2. Verify the artifact has YAML frontmatter. If missing/malformed, surface BLOCKED naming the gap.
3. List project READMEs. Use this bash one-liner:
   ```
   find ~/workspace/second-brain/04_projects -maxdepth 4 -name "README.md" -type f
   ```
   At least one must have `archetypes:` declared. If none, surface BLOCKED.
4. Read `~/workspace/second-brain/_meta/conventions.md` Project applicability fields section. Skill is read-only on the convention.

If any check fails, emit:

```
PUSH BLOCKED on precondition failure.

Failed precondition: <name>
Required: <what's needed>
Suggested remediation: <what operator should do>

PUSH will NOT proceed until precondition is resolved.
```

Exit.

## Step 2 — Gather inputs

In this order:

1. Read the artifact's full content (frontmatter + body).
2. Read every project README from Step 1's list. Extract for each:
   - Project slug (folder name)
   - `archetypes:` field
   - `archived:` flag (if present — exclude archived from candidate set)
   - Short identity / current-state notes from README body (helps signal-3 reasoning later)
3. Re-read the convention spec's Project applicability fields section.
4. Hold the artifact's existing five fields (`applies-to-projects`, `applies-to-archetypes`, `applicability-confidence`, `routed-at`, `based-on-clients`) for diff display at Gate 1.

## Step 3 — Compute Stage A routing-decision proposal

### Step 3a — Propose applicable projects (project-first)

For each non-archived project, ask:

**Signal 1 (hierarchy archetype overlap).** Does any hierarchy archetype in the artifact's body match any hierarchy archetype in the project's README? Hierarchy archetypes are:
- `services-business`, `home-services-trade`, `electrical-contractor`, `professional-services`
- `product-business`, `saas-product`, `b2b-saas`, `b2c-saas`
- `infrastructure-tooling`, `ai-tooling`, `personal-system`

If no overlap, exclude the project. Do not list it in any section.

**Signal 2 (situational archetype compatibility).** Situational archetypes are `wordpress-site`, `pre-launch-seo`, `post-launch-seo`, `gbp-dependent`.

Determine what situational state the artifact embeds based on body content:
- "post-launch-seo" if body assumes a live site with measurement baselines (GSC, GA4), discusses optimizing existing pages, refers to audit-to-fix loops on live URLs, references live GBP optimization
- "pre-launch-seo" if body discusses site-building from scratch, pre-launch GBP setup, choosing stacks before launching
- Both / neither if body covers methodology agnostic to launch state, or covers both

Determine the project's situational state from its `archetypes:`. If the artifact's embedded state conflicts with the project's declared state (artifact post-launch + project pre-launch only, or vice versa), the project is signal-2-excluded. Surface in the "Excluded by situational gating" section with the conflicting archetype named.

If artifact is agnostic on situational state, no project is signal-2-excluded.

**Signal 3 (body-content applicability).** Does the artifact's body actually inform action on this project? Examples:
- Pass: tactic-html-first-static-site routed to dad-businesses (pre-build site, methodology applies directly)
- Pass: Core 30 tactic routed to EV (live engagement deploying Core 30)
- Fail: Claude Code SEO masterclass routed to ai-agency-core (infrastructure-tooling, no SEO surface — archetype overlap fails too, so doesn't reach signal 3)
- Fail (subtle): a saas-onboarding tactic routed to a saas-product project where the operator has no active onboarding work — archetype overlap passes, body-content applicability fails because the project's current state doesn't need it

Signal 3 is judgment-heavy. Surface reasoning per project at Gate 1.

A project passes all three signals → include in proposed list with a one-line reason.
A project passes signals 1 + 3 but fails signal 2 → list under "Excluded by situational gating" with conflicting archetype named.
A project passes signal 1 only (fails 2 or 3) → list under "Excluded by signal 3" with body-content gap reason.
A project fails signal 1 → not listed at all.

### Step 3b — Derive applies-to-archetypes

Once the proposed project list is set, compute the union of every selected project's `archetypes:` field. This is the artifact's new `applies-to-archetypes` value.

Do NOT add or remove archetypes based on the artifact's body content. The field is mechanically derived from the selected project set.

### Step 3c — Propose applicability-confidence

Apply these rules in order — first matching rule wins:

1. Artifact's body explicitly names every selected project (by slug or business name) → **high**
2. Artifact is operator-produced (synthesis, client-driven artifact, opportunity routed at creation) with explicit project list → **high**
3. Artifact body covers strong archetype signal for every selected project but does not explicitly name them → **medium**
4. Multi-project routing where one or more projects have weaker archetype signal → **medium**
5. Single-project routing on archetype-overlap alone with no body-content explicit naming → **medium**
6. Speculative routing — project-fit is uncertain (pre-build project, hypothetical deployment) → **low**

If the artifact was bulk-migrated (existing `applicability-confidence: high` but body content is generic/single-project), default re-derived confidence to medium. Do not preserve inflated high.

### Step 3d — Set routed-at and based-on-clients

- `routed-at:` = today's date in ISO format (e.g., `2026-05-28`)
- `based-on-clients:` = unchanged from existing value (carry forward; PUSH does not modify provenance)

## Step 4 — Surface Gate 1 (routing-decision approval gate)

Emit the proposal in this format, filling in all sections:

```
ROUTING-DECISION PROPOSAL — <artifact-slug>

Artifact: <full path>
Type: <type from frontmatter>
Body summary (1-2 sentences): <executor's read of what the artifact is about>

Existing frontmatter:
  applies-to-projects: <existing or "not set">
  applies-to-archetypes: <existing or "not set">
  applicability-confidence: <existing or "not set">
  routed-at: <existing or "not set">
  based-on-clients: <existing or "not set">

Re-derived values:
  applies-to-projects: [<slug-1>, <slug-2>, ...]
  applies-to-archetypes: [<union archetypes alphabetized>]
  applicability-confidence: <high | medium | low>
  routed-at: <today>
  based-on-clients: <unchanged>

Diff vs existing: <no diff | minor | substantive>

Per-project reasoning:
  <project-1-slug>: <one-line reason — what signal drives the routing>
  <project-2-slug>: <one-line reason>
  ...

Excluded by situational gating (operator can override):
  <project-slug>: <conflicting archetype + reason>
  (omit section if none)

Excluded by signal 3 (operator can override):
  <project-slug>: <body-content gap reason>
  (omit section if none)

Confirm / modify per project / reject?
```

Wait for operator response.

### Gate 1 response handling

- **Confirm** → proceed to Step 5
- **Modify per project** (e.g., "drop dad-businesses; add legal-toolkit") → recompute archetype union + confidence per Steps 3b + 3c; re-emit Gate 1 with updated values; wait for confirm
- **Override situational gating for <project>** → add the project to the proposed list; archetype union now includes both situational tags; confidence may drop one tier (high → medium, medium → low); re-emit Gate 1
- **Keep existing frontmatter** → skip Stage B entirely; emit no-op completion report; exit
- **Reject** → exit without writing anything

## Step 5 — Compute Stage B bridge-note proposal

For each approved project, draft a bridge note using this template:

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

<1-2 paragraph operational framing. Reference: what signal in artifact body makes it actionable; project README context if relevant; how it interacts with current project state.>

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

The bridge filename: `bridge-<artifact-slug>-to-<project-slug>.md`. Truncate artifact-slug if the resulting filename exceeds 80 chars per conventions.md naming rules.

Default: one bridge per project. For synthesis artifacts, do NOT default to per-tactic bridges (Phase 2 friction #4); offer per-tactic as an opt-in at Gate 2.

## Step 6 — Surface Gate 2 (bridge-note approval gate)

Emit:

```
BRIDGE-NOTE PROPOSALS — <artifact-slug>

<N> bridges proposed (one per applicable project):

  1. <project-1-slug>/<bridge-filename>
     Action items: <count>
     Punchlist: <one-line proposed entry>

  2. <project-2-slug>/<bridge-filename>
     Action items: <count>
     Punchlist: <one-line proposed entry>

  ...

Per-project bridge content (expanded):

  --- Bridge 1: <project-1>/<bridge-filename> ---
  <full proposed bridge body>

  --- Bridge 2: <project-2>/<bridge-filename> ---
  <full proposed bridge body>

  ...
```

If the source artifact is a synthesis covering multiple tactics (5+ tactics referenced), append:

```
Per-tactic bridges (opt-in — default off):
  Synthesis covers <N> promoted tactics. Default discipline (single-bridge-per-cluster):
  one cluster-level bridge per project. Opt in for per-tactic bridges by saying
  "also add per-tactic bridges" — produces <N × M> additional bridges.
```

Always close with:

```
Confirm all / modify per bridge / skip per bridge / reject all?
```

Wait for operator response.

### Gate 2 response handling

- **Confirm all** → proceed to Step 7
- **Modify bridge <N>** → operator edits a specific bridge's content; accept edits; re-emit Gate 2 with updated proposal
- **Skip bridge <N>** → exclude that bridge from writes; routing-decision frontmatter still gets applied; that project just doesn't get a bridge or punchlist entry
- **Add per-tactic bridges** → expand proposal to include per-tactic bridges per project; re-emit Gate 2
- **Reject all** → exit; routing-decision frontmatter is NOT written either (no half-states); report no-op completion

## Step 7 — Stage C writes

Perform writes in this order:

1. **Update artifact frontmatter.** Use Edit tool. For each of the five fields:
   - If field exists with old value → exact-match replace with new value
   - If field doesn't exist → add after the last existing frontmatter field (just before the closing `---`)
   - Field order in the frontmatter: insert near other applies-* fields if any; otherwise group together.

2. **Write each approved bridge file** to `<project-folder>/<bridge-filename>`. Use Write tool. Preserve YAML frontmatter exactly per template.

3. **Append punchlist entry** to `<project-folder>/_punchlist.md` for each approved project. Use Edit (append) or Read+Write if the punchlist needs scaffolding. If `_punchlist.md` doesn't exist:
   - Create it with minimal frontmatter (type: punchlist, project: <slug>, created: today, status: active, tags: [punchlist, <slug>])
   - Add a heading and the new entry
   If it exists:
   - Append the new entry under the current section (typically a `## Open` or top-level list)

4. **Verify writes.** Read each touched file and confirm changes landed. If any write failed (frontmatter wasn't replaced correctly, bridge didn't write, punchlist append misfired), report the failure and roll back any partial state by reverting touched files to pre-write state. Do not leave half-committed writes.

## Step 8 — Completion report

Emit:

```
PUSH COMPLETE — <artifact-slug>

Frontmatter updated:
  <artifact-path>:
    applies-to-projects: <new value>
    applies-to-archetypes: <new value>
    applicability-confidence: <new value>
    routed-at: <today>
    based-on-clients: <unchanged>

Bridges written: <N>
  <bridge-1-path>
  ...

Punchlists updated: <N>
  <punchlist-1-path>
  ...

Suggested commit (stages by name):

cd ~/workspace/second-brain
git add \
  <artifact-path> \
  <bridge-1-path> \
  <bridge-2-path> \
  <punchlist-1-path> \
  <punchlist-2-path>
git status  # verify nothing unintended is staged
git commit -m "Route <artifact-slug> via intel-routing PUSH

<N> bridge notes filed across <project-slug-list>.
Confidence: <high | medium | low>.
Situational gating: <applied | overridden for <project-slug-list> | not relevant>.

Refs: _meta/specs/intel-routing-skill-spec.md"
```

Stop. Do not chain into PULL or BOOTSTRAP. Do not commit. Operator commits manually after reviewing diffs.

## Edge cases

- **Artifact already has routed-at set to today.** Re-route is fine; operator may have explicitly invoked PUSH to re-derive. Surface the existing routed-at in the diff; do not block.
- **Artifact has zero matching projects after signals applied.** Surface Gate 1 with empty proposal + reasoning per excluded project. Operator can override situational gating or signal 3, or reject.
- **Artifact embeds situational tags that conflict with each other** (e.g., body discusses both pre and post-launch state). Set artifact situational state to "both"; no situational exclusions apply.
- **Project has no `archetypes:` field.** Skip that project from the candidate set; surface a warning at Gate 1 ("project <slug>/README missing archetypes; skipped from routing"). Operator can fix the README then re-invoke.
- **Operator approves Gate 1 but then rejects Gate 2.** No frontmatter write happens; no bridges; no punchlists. Single-commit semantics preserved.
- **Bridge file already exists at the target path.** Read it; surface to operator at Gate 2 ("bridge already exists at <path>; current content shown below; proposed content above — overwrite / append / skip?"). Default behavior on no operator response: skip.
- **Punchlist append fails partway through.** Roll back artifact frontmatter and bridge writes. Report the failure.
