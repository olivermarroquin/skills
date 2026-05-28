---
name: intel-routing
description: Route vault artifacts (tactics, patterns, tools, syntheses, opportunities, content ideas, source notes) to applicable projects, or pull applicable intel from the vault into a project, or bootstrap a new project from accumulated intel. Triggers on phrases like "route this," "route this synthesis," "route this tactic," "push this to applicable projects," "what's new for project X," "what intel applies to <client>," "pull intel for <project>," "triage the inbox for <project>," "promote this opportunity to a project," "create a new project from this," "bootstrap <slug> from <opportunity>," or invocation as a follow-on step after VIS extraction or after multi-source-synthesis. Reads and writes the five project-applicability frontmatter fields (`applies-to-projects`, `applies-to-archetypes`, `applicability-confidence`, `routed-at`, `based-on-clients`) defined in `_meta/conventions.md`. Composes with VIS Step 10 (synthesis-readiness-scan), `multi-source-synthesis` Stage 6, `knowledge-os-setup` add-project-vault mode, and app-factory `init-project`.
---

# Intel-routing skill (v1.1 — PUSH + PULL modes)

The skill that closes the loop between vault artifacts and projects. Operates on the convention layer landed in Phase 1 of the intel-routing rollout and matured against friction observed in Phase 2. Phase 3 ships the skill itself across three sessions: PUSH first (v1.0, shipped 2026-05-28), then PULL (v1.1, this version), then BOOTSTRAP.

**Critical behavior (read this before anything else):**

- **Approval gates are mandatory.** Every mode runs two gates: routing-or-triage decision (Gate 1), then bridge-note approval (Gate 2). PUSH and PULL never write without explicit operator approve/modify/reject passes on both.
- **PUSH and PULL are inverses on the same convention.** PUSH operates on one artifact and proposes N projects; PULL operates on one project and proposes N artifacts. Both write the same five frontmatter fields and the same bridge-note shape. They share defaults (single-bridge-per-cluster, situational gating, low-default-confidence on bulk-migrated, no half-states).
- **Neither mode promotes, synthesizes, or substitutes for vault curation.** They compute applicability and write bridges. Synthesis lives in `multi-source-synthesis`. Pattern promotion is vault-curation discipline. BOOTSTRAP (Session 3) handles new-project creation; PULL operates only on existing projects.
- **PUSH re-derives frontmatter; PULL trusts the surfaced values.** PUSH's job is to fix bulk-migration drift on a single artifact at routing-time. PULL's job is to triage 50-100 already-routed artifacts against one project; re-deriving each would burn the operator's attention budget. If an operator suspects a surfaced item's frontmatter is inflated, the right move is to invoke PUSH on that item separately. PULL flags the suspicion and exits the surfaced item to a defer/keep bin.
- **Default discipline: single-bridge-per-cluster, not per-artifact-match.** Phase 2 friction observation #4 (bridge note proliferation) confirmed in practice. In PUSH a "cluster" is the project; in PULL a "cluster" is the artifact. Per-tactic-bridge writing for synthesis artifacts is operator-explicit opt-in at Gate 2 in both modes.
- **Situational archetypes are gates, not additive tags — but PUSH and PULL gate asymmetrically.** Phase 2 friction observation #11. PUSH excludes situationally-conflicted projects from routing entirely (with operator override) — it operates at routing-time and has no temporal commitment. PULL defers situationally-conflicted slug-named artifacts (rule 3 in Step A3) — it operates on cadence and the same conflict re-evaluates next triage as project state evolves. `not-applicable` in PULL is reserved for archetype-spurious matches (rule 2) or operator-explicit promotion from defer. Operator can override either default at Gate 1.
- **PULL is the operator-facing mode.** Where PUSH typically fires opt-in after VIS or synthesis runs, PULL is what the operator invokes when they start a project review session ("what's new for EV"). Designed for the recurring monthly-client-cadence triage Phase 2 exercised manually.
- **BOOTSTRAP still forward-referenced.** Ships in Session 3. See `_meta/specs/intel-routing-skill-spec.md`.

## Three modes (overview)

The skill has three modes, each invoked independently. Modes do not share state; each runs its own approval cycle.

### PUSH mode — artifact → applicable projects

Trigger: operator says "route this," or invoked automatically (opt-in) by `multi-source-synthesis` after writing a synthesis, or invoked automatically (opt-in) by VIS Step 10 after a newly extracted tactic or tool note is calibrated.

Input: a single artifact path (tactic, pattern, tool, synthesis, opportunity, source note, content idea).

Output: five frontmatter fields written on the artifact + N bridge notes written to applicable project folders + N punchlist entries appended.

PUSH is the focus of this v1.0. Full specification below.

### PULL mode — project → applicable artifacts (Session 2, shipped 2026-05-28)

Trigger: operator says "what's new for project X," "pull intel for <project>," "triage the inbox for <project>," or invoked at the start of a project review session.

Input: a project slug.

Output: updated `_intel-inbox.md` (Last triage section) + N bridge notes + N artifact frontmatter updates (`routed-at` on applied items; optional `applicability-confidence` lowering on deferred items; optional `applies-to-projects` slug removal on not-applicable items).

PULL is the focus of this v1.1. Full specification below the PUSH section.

### BOOTSTRAP mode — new project ← accumulated intel (Session 3, not yet shipped)

Trigger: operator says "create a new project from opportunity X."

Input: an opportunity artifact path (or any artifact + a proposed project slug and archetype list).

Output: new project folder + project README + new `_intel-inbox.md` + initial inbox population (via PULL on the new project) + source artifact frontmatter updates.

Status: forward reference. The `_meta/intel-opportunities-inbox.md` global queue currently documents an 8-step manual flow; BOOTSTRAP collapses it to one skill invocation. See spec.

## Multi-turn collaboration protocol

This skill supports two collaboration modes alongside single-agent execution. The role definitions are agent-agnostic; current configuration is typically Cowork (executor) + Claude.ai web chat (review agent) + Oliver (operator). Same pattern as `multi-source-synthesis`'s protocol — re-read that skill if the role definitions are unfamiliar.

### Role definitions (agent-agnostic)

- **Executor agent** — does the file operations: reads artifact + project READMEs + convention spec, computes the routing decision, drafts bridge notes, writes files on approval. Makes calibration decisions during execution; surfaces judgment calls at the routing-decision gate. In current configuration this is typically Cowork.
- **Review agent** — collaborates with the operator to draft the skill invocation prompt, validates the executor's routing proposal, pressure-tests calibration on contested cases (situational archetype gating, confidence calls, bridge-note granularity), recommends revisions. Does NOT execute file operations. In current configuration this is typically a web-UI Claude chat.
- **Operator** — decides at the two approval gates (routing decision; bridge proposal), decides whether to override situational-archetype gating, transcribes between agents when multi-turn is active, commits manually.

### When to use which mode

**Single-agent mode is appropriate when:**
- Routing target is one artifact with clear archetype signal (e.g., a tactic with a single hierarchy archetype)
- Operator already has a clear answer on which projects apply (PUSH validates rather than discovers)
- Operator-attention budget is constrained
- Speed matters more than calibration pressure-testing

**Multi-turn mode is appropriate when:**
- Routing target is a synthesis or pattern (multi-project routing is the norm, calibration decisions are heavier)
- Situational archetype gating is contested (artifact straddles pre/post-launch boundaries)
- Confidence calls are non-obvious (mixed signal across projects)
- Bridge-note granularity is contested (operator unsure whether one cluster-level bridge or N tactic-level bridges is right)
- The artifact being routed will be referenced extensively by downstream work, making routing precision matter

PUSH's typical case is single-agent. The synthesis test case in this version's examples is multi-turn-flavored because the cluster synthesis touches four projects with mixed pre/post-launch profiles.

**For PULL the typical case is also single-agent.** A monthly EV inbox triage with ~90 surfaced items reaches no contested calibration in most months — the operator skims bins, approves, done. Multi-turn becomes valuable when the project hits a state-change moment (S&H exiting the GBP-blocker; EV's Phase 2 Next.js pivot starting) and a large fraction of surfaced items shift bins simultaneously — having a review agent pressure-test the new bin assignments catches drift before bridge proliferation happens.

### Single-agent workflow

When invoked without a review agent in the loop:

1. Executor receives operator's PUSH request
2. Executor reads artifact frontmatter + body + enumerates project READMEs + reads convention spec
3. Executor computes Stage A routing-decision proposal
4. Executor surfaces proposal at routing-decision gate (Gate 1)
5. Operator confirms / modifies / rejects
6. On confirm: executor drafts bridge notes per Stage B
7. Executor surfaces bridge-note proposal at bridge gate (Gate 2)
8. Operator confirms / modifies / rejects per project
9. On confirm: executor writes frontmatter + bridges + punchlist entries (Stage C)
10. Executor reports completion with all files touched + diff summary

### Multi-turn workflow

When a review agent is in the loop, the work flows in phases. Transcription overhead is the dominant cost driver.

#### Phase A — Request analysis and prompt drafting

- Operator provides PUSH request to review agent ("route the SEO cluster synthesis," "route this tactic")
- Review agent reads the artifact (provided as project knowledge or fetched), reads the convention spec, drafts PUSH invocation prompt for executor including: artifact path, observed archetype signals from body, suspected applicable projects, suspected confidence, any contested calibration to watch
- Operator transcribes prompt from review agent to executor

#### Phase B — Routing-decision proposal

- Executor reads artifact + project READMEs + convention spec
- Executor produces Stage A routing-decision proposal at Gate 1
- Operator transcribes proposal from executor to review agent
- Review agent pressure-tests: project list correct? archetype union correct? confidence calibrated? situational gating respected? bridge-note granularity recommendation reasonable?
- Operator transcribes review agent's assessment back to executor (approve / modify per item / reject)

#### Phase C — Bridge-note proposal and write

- On routing-decision approve, executor drafts bridge notes per Stage B
- Executor surfaces bridge proposals at Gate 2 to operator
- Operator may transcribe to review agent for pressure-test on bridge content (especially action items + punchlist entries)
- On bridge approve, executor performs Stage C writes
- Executor reports completion; operator commits manually

### Mode switching mid-PUSH

If Stage A reveals contested calibration that operator wants review-agent pressure on, switch to multi-turn mid-PUSH per the same pattern documented in `multi-source-synthesis`'s mode-switching section. Operator copies executor's current proposal to review agent + names the contested point; review agent picks up from there.

## PUSH mode — full specification

### Trigger phrases

- "route this"
- "route this synthesis"
- "route this tactic" / "route this pattern" / "route this tool"
- "push this to applicable projects"
- "PUSH-route <artifact-path>"
- Automatic invocation (opt-in) by `multi-source-synthesis` Stage 6 after writing a synthesis
- Automatic invocation (opt-in) by VIS Step 10 after a newly extracted tactic / tool note is calibrated

### Preconditions

Before producing a routing proposal, executor verifies:

1. **Artifact exists and is readable.** If path doesn't resolve, executor reports a blocked-on-precondition response with the unresolved path. No silent skip.
2. **Artifact has frontmatter.** If frontmatter is missing or malformed, executor reports the gap and exits. (`type:`, `status:`, `created:`, `updated:`, `tags:` are minimum per conventions.) Do not silently invent frontmatter — that's a different operation.
3. **At least one project README exists with `archetypes:` declared.** If no project has archetypes set, PUSH cannot route. Surface as blocked-on-precondition.
4. **Convention spec is readable** at `second-brain/_meta/conventions.md` Project applicability fields section. The skill is read-only on the spec; it does not modify the convention.

If any precondition fails, executor surfaces:

```
PUSH BLOCKED on precondition failure.

Failed precondition: <specific precondition>
Required: <what's needed>
Suggested remediation: <what operator should do before re-invoking>

PUSH will NOT proceed until precondition is resolved.
```

### Inputs gathered before Stage A

Executor reads, in this order:

1. **The artifact's full content** — frontmatter + body. Body is the load-bearing input for routing because it carries the project-applicability signal that the LLM heuristic computes against.
2. **Every project README** under `04_projects/clients/_active/`, `04_projects/clients/_private/`, and `04_projects/personal/` — extract `archetypes:`, `applicability-confidence:`, and `archived:` (if present). Archived projects are excluded from routing. Use the bash `find` pattern from the skill's reference reads.
3. **The convention spec** at `_meta/conventions.md`, specifically the Project applicability fields section and the Archetype hierarchy subsection. Re-read on every invocation so spec changes are picked up.
4. **Artifact's existing frontmatter values** for the five fields (`applies-to-projects`, `applies-to-archetypes`, `applicability-confidence`, `routed-at`, `based-on-clients`) — held for the existing-vs-rederived diff at Gate 1.

### Stage A — Routing-decision computation

PUSH's routing-decision algorithm is project-first, not archetype-first. The discipline: decide which projects apply, then derive archetypes as the union of selected projects' archetypes, then set confidence based on signal strength.

This matches how the Phase 2 SEO cluster synthesis was operator-routed: Oliver decided projects (EV + S&H + Keelworks + dad-businesses) at the synthesis shape-and-destination gate, and the synthesis's `applies-to-archetypes` field is the union of those four projects' archetypes. See `03_domains/seo/cluster-synthesis-ai-era-seo-cluster-2026-05-27.md` audit-pass item #6 for the precedent.

Project-first means the LLM heuristic does the load-bearing work in step 1 below (which projects apply based on body content), and steps 2-4 derive mechanically from that decision.

#### Step 1 — Propose applicable projects

For each non-archived project, the executor asks: does this artifact's body apply to this project, given the project's README archetypes + active engagement state (if known from the README) + situational compatibility?

The heuristic combines three signals:

**Signal 1 — Hierarchy archetype overlap.** Does any hierarchy archetype the artifact embeds match any hierarchy archetype the project declares? Hierarchy archetypes are `services-business`, `home-services-trade`, `electrical-contractor`, `professional-services`, `product-business`, `saas-product`, `b2b-saas`, `b2c-saas`, `infrastructure-tooling`, `ai-tooling`, `personal-system`. Overlap is necessary for routing; bare overlap is not sufficient (signals 2 and 3 must clear).

**Signal 2 — Situational archetype compatibility.** Situational archetypes are `wordpress-site`, `pre-launch-seo`, `post-launch-seo`, `gbp-dependent`. If the artifact embeds a situational archetype AND the project carries a CONFLICTING situational archetype (e.g., artifact is post-launch-shaped + project is pre-launch-only), the project is excluded UNLESS the operator overrides at Gate 1. If the artifact embeds no situational archetype, or only matches situational tags, the project clears signal 2.

This rule is the maturation of friction observation #11 from Phase 2. A bulk-migrated artifact tagged `[pre-launch-seo, post-launch-seo]` covers both gates and routes broadly. An operator-routed artifact tagged with one or the other gates the routing. The discipline: PUSH-derived artifacts should tag the specific situational state they embed, not both.

**Signal 3 — Body-content applicability.** Does the artifact's body actually inform action on this project? Examples that pass: a Core 30 SEO tactic on EV (live engagement deploying Core 30); a Claude Code SEO masterclass on Keelworks (operator's own SEO surface); a multi-project synthesis on all named projects (synthesis explicitly references each). Examples that fail: a Claude Code SEO masterclass routed to ai-agency-core (infrastructure-tooling, no SEO surface); a Figma-to-React tactic routed to S&H (no custom-build path yet).

Signal 3 is the most LLM-judgment-heavy. Reasoning per project must be surfaced at Gate 1 so operator can audit.

For each project that clears all three signals, executor includes it in the proposed list with a one-line reason. For each project that clears signals 1 + 3 but fails signal 2 (situational gating), executor lists it under "Excluded by situational gating" with the conflicting archetype named — operator can override.

#### Step 2 — Derive `applies-to-archetypes` as union of selected projects' archetypes

Once the proposed project list is known, the artifact's `applies-to-archetypes` is the union of every selected project's `archetypes:` field. No body-derived archetypes are added or removed; the field is mechanically derived.

This produces a clean mental model: archetypes on the artifact describe "the union of archetypes the artifact applies to." Archetypes on the project describe "what this project IS." Match logic is set-overlap.

For situational tags specifically, the union may include both `pre-launch-seo` and `post-launch-seo` if the artifact applies to projects on both sides. This is correct and expected — a synthesis covering both states should carry both tags so it surfaces in both kinds of project inbox. Single-state artifacts (a post-launch-only tactic) will only carry one situational tag because they only route to one kind of project.

#### Step 3 — Propose `applicability-confidence`

Confidence calibration follows three rules:

- **High** — Artifact's body explicitly names the selected projects (by slug or name), OR artifact embeds archetypes that strictly match the selected projects, OR artifact is operator-produced output (synthesis, client-driven artifact) whose project list is explicit. Multi-project routings where every project has strong signal are high.
- **Medium** — Artifact body covers the selected project's archetype but does not explicitly name the project. Single-project routing on archetype-match alone is medium. Multi-project routings where one or more projects have weaker signal are medium.
- **Low** — Speculative routing. Artifact's body covers an archetype but the project-fit is uncertain (e.g., tactic for "electrical contractors generally" routed to a pre-build project where deployment is still hypothetical). Single-project routing on weak archetype-match is low.

Friction observation #2 calibration: do NOT default to high on bulk-routed artifacts. If the artifact has been migrated rather than operator-routed, default confidence is medium unless body content explicitly elevates.

#### Step 4 — Set `routed-at` and `based-on-clients`

- `routed-at: <today>` — set to the routing date in ISO format. Only updated by routing operations; manual reads don't update.
- `based-on-clients: [...]` — provenance, not applicability. Carry forward whatever exists on the artifact; PUSH does not modify this field. (Patterns and tactics derived from client work have `based-on-clients:` filled at extraction-time; PUSH does not touch it.)

### Gate 1 — Routing-decision approval gate

Executor surfaces the proposal in this format:

```
ROUTING-DECISION PROPOSAL — <artifact-slug>

Artifact: <full path>
Type: <type from frontmatter>
Body summary (1-2 sentences): <executor's read of what the artifact is about>

Existing frontmatter:
  applies-to-projects: <existing value or "not set">
  applies-to-archetypes: <existing value or "not set">
  applicability-confidence: <existing value or "not set">
  routed-at: <existing value or "not set">
  based-on-clients: <existing value or "not set">

Re-derived values:
  applies-to-projects: [<slug-1>, <slug-2>, ...]
  applies-to-archetypes: [<union archetypes>]
  applicability-confidence: <high | medium | low>
  routed-at: <today>
  based-on-clients: <unchanged>

Diff vs existing: <one of: no diff (existing matches re-derived) | minor (1-2 fields differ) | substantive (3+ fields differ or projects list differs)>

Per-project reasoning:
  <project-1-slug>: <one-line reason — what signal drives the routing>
  <project-2-slug>: <one-line reason>
  ...

Excluded by situational gating (operator can override):
  <project-slug>: <conflicting archetype + reason>
  (omit section if no situational exclusions)

Excluded by signal 3 (operator can override):
  <project-slug>: <body-content gap reason>
  (omit section if none)

Confirm / modify per project / reject?
```

Operator response options:

- **Confirm** — proceed to Stage B with re-derived values
- **Modify per project** — operator names projects to add/drop. Executor recomputes archetype union + confidence; surfaces updated proposal.
- **Override situational gating for <project>** — operator names a project the situational gate excluded; executor adds it; recomputes union (situational tags will now include both gates); confidence may drop to medium.
- **Keep existing frontmatter** — do not overwrite; skip Stage B entirely; report no-op completion.
- **Reject** — exit without writing.

### Stage B — Bridge-note proposal

For each project in the approved routing list, executor drafts a bridge note proposal. Default discipline (Phase 2 friction #4 maturation): **one bridge per cluster, not per artifact-match**.

A "cluster" for bridge-note purposes is:
- For a tactic / tool / pattern / opportunity / content idea / source note → the cluster = the project. One bridge per project.
- For a synthesis → the cluster = the project. One bridge per project, summarizing the synthesis's applicability to that project. Individual tactic-level bridges (one bridge per tactic the synthesis covers) are NOT the default — they're operator-explicit opt-in.

Per-project bridge note template:

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

<1-2 paragraph operational framing: what signal in the artifact's body makes it actionable on this project; reference project README context if relevant>

## Concrete action items

1. <action item — concrete enough to land on punchlist>
2. <action item>
3. <action item>
(1-3 items typical; if more, operator should consider whether per-tactic bridges are warranted)

## Punchlist entry (proposed)

> <one-line punchlist entry; goes into project's _punchlist.md>

## See also

- [[<artifact-slug>]] (source)
- [[<project-slug>/README]] (project context)
```

### Gate 2 — Bridge-note approval gate

Executor surfaces all proposed bridges together:

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

Per-tactic bridges (opt-in — default off):
  <If the source artifact is a synthesis covering multiple tactics, executor may surface this as an optional follow-on: "synthesis covers 6 promoted tactics; default is one cluster-level bridge per project; opt in for per-tactic bridges by saying 'also add per-tactic bridges'.">

Confirm all / modify per bridge / reject all?
```

Operator response options:

- **Confirm all** — proceed to Stage C; write everything as proposed
- **Modify bridge <N>** — operator edits a specific bridge; executor accepts edits; re-presents updated proposal
- **Skip bridge <N>** — exclude that bridge from writes; routing-decision still applied (frontmatter still updated; just no bridge for that project)
- **Add per-tactic bridges** — operator opts in to per-tactic granularity; executor expands proposal with one bridge per tactic per project
- **Reject all** — exit; routing-decision frontmatter is NOT written either (no half-states)

### Stage C — Writes (on Gate 2 approval)

Executor performs writes in this order:

1. Update artifact frontmatter — five fields per re-derived values. Use Edit tool with exact existing-line targeting. If a field doesn't exist on the artifact, add it after the existing frontmatter fields.
2. For each approved bridge: write the bridge file to `<project-folder>/bridge-<artifact-slug>-to-<project-slug>.md`. Use Write tool.
3. For each approved bridge: append the punchlist entry to `<project-folder>/_punchlist.md`. Append, do not overwrite. If `_punchlist.md` doesn't exist, create it with a minimal scaffold (heading + frontmatter).
4. Verify all writes by reading each touched file and confirming the change landed.

Report at completion:

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
  <bridge-2-path>
  ...

Punchlists updated: <N>
  <punchlist-1-path>
  <punchlist-2-path>
  ...

Suggested commit (stages by name):

cd ~/workspace/second-brain
git add \
  <artifact-path> \
  <bridge-1-path> \
  <bridge-2-path> \
  ...
  <punchlist-1-path> \
  <punchlist-2-path> \
  ...
git status  # verify nothing unintended is staged
git commit -m "Route <artifact-slug> via intel-routing PUSH

<N> bridge notes filed across <project-slug-list>.
Confidence: <high | medium | low>.
Situational gating: <applied | overridden for <project-slug-list> | not relevant>.

Refs: _meta/specs/intel-routing-skill-spec.md"
```

## PULL mode — full specification

### Trigger phrases

- "what's new for project <slug>" / "what intel applies to <client>"
- "pull intel for <slug>" / "PULL-route <slug>"
- "triage the inbox for <slug>" / "run the <slug> inbox triage"
- "what's in <client>'s inbox" / "review <client>'s intel inbox"
- Invocation at the start of a project review session (operator-cadence, typically monthly for clients)
- Optional invocation parameter: `--lookback <days>` to override the default 14-day suppression window

### Preconditions

Before producing a surface, executor verifies:

1. **Project folder resolves.** If `04_projects/<area>/<slug>/` doesn't exist for any `<area>` in {`clients/_active`, `clients/_private`, `personal`}, surface BLOCKED with the unresolved slug.
2. **Project README exists with `archetypes:` declared.** PULL is archetype-driven; without README archetypes, the surface query cannot run. Surface BLOCKED naming the missing field.
3. **Project is not archived.** If `archived: true` on the README, surface BLOCKED — PULL does not operate on archived projects (consistent with PUSH excluding archived projects from candidate sets).
4. **`_intel-inbox.md` exists OR operator opts into scaffolding.** If the file is missing, surface a one-question gate at the top of Stage A: "no inbox file at `<path>`. Scaffold from `_meta/templates/template-intel-inbox.md` and proceed? (yes / no)." Default behavior on operator yes: scaffold (filling `project:` + `archetypes:` from the README), then continue. On no: BLOCKED.
5. **Convention spec readable** at `_meta/conventions.md` Project applicability fields section.

If any blocking precondition fails, emit:

```
PULL BLOCKED on precondition failure.

Failed precondition: <name>
Required: <what's needed>
Suggested remediation: <what operator should do>

PULL will NOT proceed until precondition is resolved.
```

### Inputs gathered before Stage A

Executor reads, in this order:

1. **Project README** — extract `archetypes:`, `applicability-confidence:` (project-level signal of how confident the project is in its own archetype declaration), `archived:` (already checked at precondition), and a body skim for current-state signals (active engagement / blocked / paused / pre-build) used in Stage A pre-classification.
2. **Project `_intel-inbox.md`** — extract `archetypes:` (for sync validation against README), the most recent "Last triage" date (informs whether the operator is on cadence or catching up), the existing list of "Items applied" / "Items kept" / "Items deferred" / "Items marked not-applicable" (informs continuity).
3. **The convention spec** — re-read on every invocation.
4. **Query execution** against the vault. PULL runs the equivalent of the Dataview query embedded in `_intel-inbox.md`:
   - Folders: `03_domains/`, `05_shared-intelligence/`, `00_inbox/decisions-pending/`
   - Match: `applies-to-projects` contains `<this-project-slug>` OR any `applies-to-archetypes` overlaps any project README `archetypes:`
   - Filter: artifact's `routed-at:` is missing OR `routed-at:` < `today - lookback`
   - Exclude: artifacts with `archived: true`
   - Sort: by `applicability-confidence` DESC, then `file.mtime` DESC

   Default lookback is 14 days. Operator can override with `--lookback <days>` at invocation. Executor must use bash `find` + frontmatter parsing if Dataview isn't available in the execution environment; the result set must match what Obsidian's Dataview would surface from the inbox.

5. **Existing bridge notes in the project folder** — read filenames matching `bridge-*.md`. Used to detect "already-bridged" artifacts at Stage B (avoids duplicate bridge writes; analogous to PUSH's existing-bridge detection).

### Stage A — Surface computation

PULL produces a single batched surface, not a per-item proposal. Three sub-steps.

#### Step A1 — Project↔inbox archetype sync validation

Compare README `archetypes:` against inbox `archetypes:`. Three outcomes:

- **Matched** — proceed silently.
- **Inbox is subset of README** (README has more archetypes than inbox) — surface as warning at Gate 1, offer to sync inbox to README before proceeding ("project README declares X; inbox declares Y; sync inbox? — yes / proceed-anyway / exit").
- **Inbox has archetypes README doesn't** — same warning, opposite direction. Almost always means the README was updated without updating the inbox.

If operator approves sync, executor writes the inbox `archetypes:` field to match the README and re-runs the query (the sync may change which artifacts surface). Sync is a single Edit call to the inbox file's frontmatter; no inbox-body changes.

This is friction observation #5 baked into v1.1. Cheap check; surfaces drift before it propagates.

#### Step A2 — Run the query and tag each surfaced artifact

For each artifact in the result set, compute:

- **Match type** — `slug-named` (artifact's `applies-to-projects` includes this project slug) or `archetype-overlap` (matched via archetype intersection only)
- **Signal 2 status** — does the artifact embed a situational archetype that conflicts with the project's situational archetype? (Same Signal 2 logic as PUSH. Post-launch artifact + pre-launch-only project = conflict.)
- **Existing confidence** — from the artifact's `applicability-confidence:` field; `not-set` if missing
- **Bridge already exists** — boolean from the existing-bridge file list
- **Routed-at** — from the artifact's `routed-at:` field; `not-set` if missing
- **One-line body summary** — executor's read of what the artifact is about (used for the surface listing; ~one sentence per artifact)

Items where bridge already exists are surfaced under a separate **ALREADY BRIDGED** bin — informational only, not a triage decision; operator can opt to refresh the bridge or skip.

#### Step A3 — Pre-classify each surfaced artifact into a bin

PULL pre-classifies bins as a *recommendation*; operator confirms or moves items at Gate 1. Pre-classification rules in order — first matching rule wins:

1. **Bridge already exists** → `already-bridged` (no triage action).
2. **Signal 2 conflict AND artifact is archetype-overlap-only** → `not-applicable` (default; operator can override). The slug isn't on the artifact to keep, so the only remediation is archetype-sharpening. Reason: "situational conflict (archetype-overlap-only): artifact <state>, project <state>; archetype-sharpen to suppress future surface."
3. **Signal 2 conflict AND artifact is slug-named** → `defer` (default; operator can override). The slug is present because someone — operator or bulk-migration — decided this artifact would apply to this project. The situational conflict is typically temporal (project will exit the blocker eventually). Reason: "situational conflict: artifact <state>, project <state>; activate on project transition."
4. **Slug-named AND body content directly actionable in current project state** → `apply`. "Directly actionable" means the artifact's body describes work that can ship under the project's current state (active deployment OR a known blocker-recovery path). Examples: a Core 30 tactic on EV (active deployment); a GSC self-takeover pattern on S&H (actionable via Haris-outreach despite pre-launch state). Reason: "slug-named + directly actionable in current state."
5. **Slug-named AND project active AND body not immediately actionable (already in context)** → `keep`. Most slug-named artifacts on active client projects land here — the engagement context already contains them; bridge-noting each would be noise (friction #4). Reason: "slug-named + already in engagement context; revisit on next triage."
6. **Slug-named AND project blocked/pre-deployment AND body not actionable now** → `keep`. Foundational tactics, syntheses, patterns that will apply when state changes but aren't doing work today. Reason: "applicable but project currently <blocker>; activate when <unblocker condition>." Examples: the SEO cluster synthesis on S&H — high confidence, slug-named, but lands in keep because S&H isn't deploying yet.
7. **Slug-named AND project blocked AND artifact is a future-gated lane** → `defer`. The artifact names a future-pilot or future-lane that's gated on a known event. Operator typically deferred these in Phase 2 (Featured.com / Qwoted / image-link-building lanes on EV gated by Phase-1 audit). Reason: "slug-named but gated on <future event>."
8. **Archetype-overlap only AND project active** → `defer` (default; operator can promote to `apply` if signal-3 actually applies). Reason: "archetype match, no body-content explicit naming; defer pending review."
9. **Archetype-overlap only AND project blocked/pre-deployment** → `defer`. Combines weakening factors.
10. **Existing confidence is `low`** → biases toward `defer` regardless of earlier rules (low-confidence is the operator's earlier "speculative routing" signal).

Pre-classification is heuristic — operator reclassifies any item at Gate 1.

**Note on rule 3 (slug-named situational conflict → defer).** This differs from PUSH's discipline (situational conflict → exclude from routing). The asymmetry is intentional: PUSH operates at routing-time and has no temporal commitment to update; PULL operates on a recurring cadence and the same conflict will re-evaluate every triage as the project state evolves. Defer-with-reason preserves the routing AND the temporal awareness. `not-applicable` for slug-named items is reserved for cases where the operator decides the slug shouldn't be there in the first place (which they can promote any defer-bin item to at Gate 1).

### Gate 1 — Triage-decision approval gate (batched)

Executor surfaces the bins together. Operator approves bins as proposed, or names individual items to move. No per-item gates — Phase 2's first triage at 98 candidates per project demonstrated that per-item gates burn operator attention; batched bins with movability is the right shape.

```
PULL TRIAGE — <project-slug>

Project name: <project-name>
Project README: <full path>
Inbox file: <full path>
Lookback window: <days> (suppressing items with routed-at after <date>)
Last operator triage: <date from Last triage section, or "first triage">

Sync status:
  README archetypes: [...]
  Inbox archetypes: [...]
  Match: <matched | inbox-subset-of-readme | inbox-superset-of-readme>
  (If mismatched, ask: sync inbox to README? yes / proceed-anyway / exit)

Items surfaced: <total N>
  slug-named: <count>
  archetype-overlap-only: <count>
Items suppressed (routed within lookback): <count>
Items already bridged (informational): <count>

==== APPLY (proposed: M) ====
  - [[<artifact-slug>]] (<type>, confidence: <c>)
    <one-line body summary + one-line reason for apply>
  ...

==== KEEP (proposed: M) ====
  - [[<artifact-slug>]] (<type>, confidence: <c>)
    <one-line body summary + reason for keep>
  ...

==== DEFER (proposed: M) ====
  - [[<artifact-slug>]] (<type>, confidence: <c>)
    <one-line body summary + reason for defer>
  ...

==== NOT APPLICABLE (proposed: M, situational conflict) ====
  - [[<artifact-slug>]] (<type>)
    <conflicting situational tag + reason>
  ...

==== ALREADY BRIDGED (informational: M) ====
  - [[<artifact-slug>]] → <existing-bridge-filename>
  ...

Confirm bins as proposed / move <item> to <bin> / sharpen archetypes on <item> / reject?
```

### Gate 1 response handling

Operator response options:

- **Confirm bins as proposed** → proceed to Stage B
- **Move <item-slug> to <bin>** (e.g., "move tactic-foo to apply") → executor moves; re-emits updated bins; waits for confirm
- **Move all <bin-X> items to <bin-Y>** → bulk move (useful when operator wants e.g., "defer everything currently in keep because I won't get to it this month")
- **Sharpen archetypes on <item-slug>: drop <archetype>** → only valid for items in `not-applicable` bin; executor records the archetype-sharpening for Stage C writes; surfaces updated proposal
- **Lower confidence on <item-slug> to <level>** → only valid for items in `defer` bin; executor records the confidence write for Stage C
- **Refresh bridge on <item-slug>** → only valid for items in `already-bridged` bin; moves the item back to `apply` with a "refresh existing" flag
- **Reject** → exit without any writes

### Stage B — Bridge-note proposal for "apply" items

For each item operator placed in the `apply` bin, executor drafts a bridge note proposal. Same template as PUSH:

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

<1-2 paragraph operational framing — what signal in artifact body makes it actionable for this project right now; reference current project state from README.>

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

Bridge filename: `bridge-<artifact-slug>-to-<project-slug>.md`. Truncate artifact-slug if filename exceeds 80 chars.

**Default discipline: one bridge per applied artifact** (single-bridge-per-cluster — friction observation #4). If an apply item is a synthesis covering 5+ tactics, executor surfaces the per-tactic-bridge opt-in at Gate 2 (identical to PUSH's offer).

### Gate 2 — Bridge-note approval gate

Executor surfaces all proposed bridges:

```
BRIDGE-NOTE PROPOSALS — <project-slug>

<N> bridges proposed (one per applied artifact):

  1. <project-folder>/bridge-<artifact-1-slug>-to-<project-slug>.md
     Action items: <count>
     Punchlist: <one-line proposed entry>

  2. <project-folder>/bridge-<artifact-2-slug>-to-<project-slug>.md
     Action items: <count>
     Punchlist: <one-line proposed entry>

  ...

Per-bridge content (expanded):
  --- Bridge 1: ... ---
  <full proposed bridge body>

  --- Bridge 2: ... ---
  <full proposed bridge body>

  ...

Per-tactic bridges (opt-in — default off):
  <If any apply item is a synthesis covering 5+ tactics, surface the same per-tactic
  opt-in as PUSH Gate 2. Default off.>

Confirm all / modify per bridge / skip per bridge / reject all?
```

### Gate 2 response handling

- **Confirm all** → proceed to Stage C; write everything as proposed
- **Modify bridge <N>** → operator edits bridge content; accept edits; re-emit Gate 2
- **Skip bridge <N>** → exclude that bridge from writes; the corresponding artifact's `routed-at:` still gets updated (apply was operator-confirmed at Gate 1; only the bridge write is skipped). Punchlist entry is also skipped.
- **Add per-tactic bridges** → expand proposal; re-emit Gate 2
- **Reject all** → no writes happen at all; not just bridges but also the per-item frontmatter changes from Gate 1 (no half-states). Inbox Last-triage section is also not updated. Exit.

### Stage C — Writes (on Gate 2 approval)

Executor performs writes in this order. All-or-nothing semantics: any write failure rolls back all touched files.

1. **For each `apply` item with approved bridge:**
   - Write bridge file to `<project-folder>/bridge-<artifact-slug>-to-<project-slug>.md`
   - Append punchlist entry to `<project-folder>/_punchlist.md` (create with minimal scaffold if missing — same shape as PUSH)
   - Update the artifact's `routed-at:` to today via Edit tool. If field doesn't exist, add it.

2. **For each `apply` item where operator skipped the bridge at Gate 2:**
   - Update artifact's `routed-at:` to today (apply decision still applied; just no bridge)

3. **For each `defer` item where operator explicitly lowered confidence at Gate 1:**
   - Update artifact's `applicability-confidence:` to the new level via Edit tool

4. **For each `not-applicable` item:**
   - Default: remove `<this-project-slug>` from the artifact's `applies-to-projects:` list. If the resulting list is empty, set the field to `[]` (do not remove the field).
   - If operator chose archetype-sharpening instead: remove the named archetype(s) from the artifact's `applies-to-archetypes:` list. Do NOT touch `applies-to-projects:` in this case.

5. **Update `_intel-inbox.md` "Last triage" section.** Use Edit tool with exact-match against the existing section. New section content:
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
   If operator surfaced a friction observation at Gate 1 or Gate 2 (e.g., "kept count is unsustainable"), include a one-paragraph friction observation block below the counts. Otherwise omit.

6. **Verify all writes** by reading each touched file. On failure, revert.

### Step 9 — Completion report

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
    <list of artifact paths with field changed in parens>
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

### PULL edge cases

- **Zero items surfaced.** Emit a tight completion report with all counts at zero, still update the inbox Last-triage section with today's date and "0 items surfaced" so future triages know this date was on cadence. Don't BLOCK; an empty surface is a valid outcome.
- **Operator approves bins but every apply has bridge-already-exists.** Already-bridged items can be operator-promoted back to apply with a "refresh existing" flag at Gate 1. If no apply items remain after de-duplication, Stage B emits nothing and Stage C only updates the inbox Last-triage section. Report PULL as completed with "no new bridges written."
- **Surfaced item has `applies-to-projects: []` and is matched only by archetype-overlap.** Operator marks not-applicable → only archetype-sharpening is available (no slug to remove). Surface this constraint at Gate 1 when operator picks not-applicable.
- **Inbox sync was approved at Gate 1.** Executor writes the sync to the inbox file BEFORE re-running the query, so the second run reflects the synced archetypes. The Stage C inbox-update at Step 5 still runs and overwrites only the Last triage section.
- **Cadence detector — operator catches up after long gap.** If the inbox's last triage date is >60 days old (or never triaged), the surface count will be high. PULL surfaces a note above the bins: "long gap since last triage (<N> days). Surface size <count> reflects accumulation. Consider triaging in batches rather than all at once." Operator may exit and re-run with `--lookback 30` to filter to most-recent items only.
- **`current-blocker:` field on project README (v1.1 forward reference).** Pre-launch projects produce heavy defer ratio (friction #11). The full v2.0 solution might surface a `current-blocker:` field on the project README that auto-defers archetype-overlap items not relevant to the blocker. v1.1 does not implement this — surfaces the friction observation in the Stage A pre-classification reason for operator awareness; the operator handles bulk-defer via "Move all <bin> to <bin>" at Gate 1. Capture as v1.2 candidate.
- **Project has `_intel-inbox.md` but no archetypes set in inbox frontmatter** (likely manually-created or partially-instantiated). Sync validation surfaces as "inbox-superset-of-readme" if README has any archetypes; offer to sync. If both inbox and README are empty on archetypes, BLOCKED.

## BOOTSTRAP mode — forward reference (Session 3)

Not yet shipped. Spec lives at `_meta/specs/intel-routing-skill-spec.md` section "BOOTSTRAP mode." Operator runs the 8-step manual flow in `_meta/intel-opportunities-inbox.md` until BOOTSTRAP ships.

Per spec composition points: BOOTSTRAP delegates project-folder scaffolding to the `knowledge-os-setup` add-project-vault mode and optionally invokes the app-factory `init-project` flow for the repo side. Once BOOTSTRAP ships, the manual 8-step flow in the opportunities inbox compresses to one skill invocation.

## Metadata contract

### Reads (does not write) — from artifact frontmatter

- `applies-to-projects: [project-slug, ...]` — existing value (for diff display)
- `applies-to-archetypes: [archetype-tag, ...]` — existing value (for diff display)
- `applicability-confidence: high | medium | low` — existing value (for diff display)
- `routed-at: YYYY-MM-DD` — existing value (for diff display)
- `based-on-clients: [project-slug, ...]` — provenance, carried forward unchanged
- `new-business-direction: true` (on tool notes) — flag for BOOTSTRAP mode candidate (forward reference)
- `could-become-project: true` (on content-idea notes) — same as above
- `archived: true` (any artifact) — excludes from PUSH

### Reads (does not write) — from project README frontmatter

- `archetypes: [archetype-tag, ...]` — load-bearing for routing
- `applicability-confidence: high | medium | low` — informs the operator's calibration sanity but does not directly drive routing
- `archived: true` (if present) — excludes the project from routing

### Writes — only on Gate 2 approval

- `applies-to-projects: [...]` — overwritten with re-derived value
- `applies-to-archetypes: [...]` — overwritten with archetype union
- `applicability-confidence: high | medium | low` — overwritten with re-derived value
- `routed-at: YYYY-MM-DD` — set to today
- `based-on-clients: [...]` — not touched (provenance is not PUSH's concern)
- New file: `<project-folder>/bridge-<artifact-slug>-to-<project-slug>.md` per approved project
- Appends to: `<project-folder>/_punchlist.md` per approved project

PUSH never touches any other frontmatter field. Status, tags, type, created, updated, and all other fields are left alone.

## Composition with existing skills

### VIS Step 10 (`synthesis-readiness-scan`)

`synthesis-readiness-scan` runs as VIS Step 10 after extraction. If the scan surfaces a synthesis-ready cluster or pattern AND the operator confirms a pick AND the resulting synthesis is written (via `multi-source-synthesis`), the synthesis path can be optionally chained into PUSH.

**Default: opt-out.** Per spec open question #1, automatic PUSH after every VIS-completed extraction is noise. Per-extraction PUSH on tactics or tools is also opt-out — operator opts in per run with "and route the new tactic/tool" or similar.

Composition point lives in `multi-source-synthesis` Stage 6 (the new synthesis path is available there) and in `vis-extraction` Step 10 (the new tactic/tool paths are available there). Both skills are edited to surface the opt-in prompt; PUSH never auto-runs.

### `multi-source-synthesis` Stage 6

After Stage 6 of `multi-source-synthesis` writes the synthesis and invokes companion skills (meta-document-primer, optional plain-language-translation), the chat surfaces:

```
Optional next step: route this synthesis via intel-routing PUSH.
Type "route this" or "PUSH-route this synthesis" to invoke.
(Skip to commit only; PUSH does not auto-run.)
```

PUSH then takes the synthesis path as input and runs its standard two-gate flow.

### `knowledge-os-setup` add-project-vault mode

BOOTSTRAP mode (Session 3) delegates project-folder scaffolding to `knowledge-os-setup`'s init-project-vault.sh script. Not relevant to v1.0 PUSH.

### app-factory `init-project`

BOOTSTRAP mode (Session 3) optionally invokes `repos/app-factory/prompts/init-project.md` for repo-side scaffolding when the new project needs code. Not relevant to v1.0 PUSH.

## Friction-point-driven defaults (Phase 2 observations)

The skill's defaults respond to friction observed during Phase 2 deployment. Each default below cites the friction observation it addresses.

### Bridge-note proliferation (#4) — default single-bridge-per-cluster

Naive "one bridge per artifact-match" produced ~98 candidates per project in Phase 2's first triage on EV and S&H. Right discipline (used in Phase 2): one bridge per genuinely-actionable apply. PUSH v1.0 default: one bridge per project per artifact. Per-tactic-bridges for syntheses are operator opt-in at Gate 2.

### Confidence calibration drift (#2) — default lower on bulk-routed

Bulk-set high-confidence on migrated artifacts is inflation. PUSH default: high only when body explicitly names projects or when operator-produced artifact has explicit project list; medium for archetype-overlap-only routings; low for speculative single-project routings.

### Phase 1 reconnaissance was 7-10x off (#8) — pre-flight reconnaissance

For PUSH, the artifact is one file; reconnaissance is cheap (read the file). For BOOTSTRAP (Session 3), pre-flight will produce an accurate "files to be touched" estimate before approval so operator can right-size batches.

### Pre-launch projects produce heavy defer ratio (#11) — situational archetype gating

Maturation: situational archetypes are gates, not additive tags. PUSH excludes pre-launch projects from routing on post-launch-shaped artifacts (and vice versa), surfacing the exclusion at Gate 1 so operator can override.

### Dual-field artifacts required fix-up pass (#10) — diff display at Gate 1

PUSH compares existing frontmatter to re-derived values and surfaces the diff. If existing frontmatter has the deprecated `relevant-projects:` or `projects-using:` fields, the diff makes this visible and the rewrite cleans up.

### Over-tagged archetypes (#1) — operator can narrow at Gate 1

Operator can drop projects at Gate 1; archetype union recomputes. If the operator says "drop dad-businesses; not actually applicable," dad-businesses' archetypes drop from the union, narrowing the artifact's tag set.

### Project-archetype divergence (#5) — sync validation at every PULL invocation

PULL (v1.1) validates that project README `archetypes:` matches the project's `_intel-inbox.md` `archetypes:` at every invocation. Mismatch surfaces at Gate 1 with operator options: sync inbox to README (default — single-Edit write before re-running the query), proceed anyway, or exit. Not applicable to PUSH (PUSH doesn't read inbox files).

### Sources-as-applicability question (#12) — open

Sources got migrated to `applies-to-projects` during Phase 2 even though the convention spec lists the field as for "tactics, patterns, tools, syntheses, opportunities, and content ideas" — not sources. PUSH treats source notes as valid inputs (operator may want to PUSH-route a high-value source). The convention question (whether sources should carry applies-to-projects or just provenance) is operator-discipline territory; PUSH does not legislate.

## Closing step — Auto-invoke output-quality-loop

After both gates resolve and writes have landed (PUSH: artifact frontmatter five fields + per-project bridge notes; PULL: project punchlist additions + per-artifact `routed-at:` bumps + inbox `last-triaged:` update; BOOTSTRAP: project folder scaffolded + initial PULL run), emit the standard auto-invoke block per `~/workspace/skills/output-quality-loop/references/auto-invoke-convention.md` and `~/workspace/second-brain/_meta/conventions.md` § "Output quality". This is the closing step every artifact-producing skill emits before declaring the chat done. Convention shipped Phase 5 of the output-quality-loop project (2026-05-28).

**Artifact list for this skill.**

- **PUSH mode:** the bridge notes written into each selected project's folder (one per project per cluster by default). The artifact whose frontmatter got updated is NOT included — frontmatter-only edits don't trigger spec-routing re-evaluation; the artifact's own quality state is independent. If a per-tactic bridge was operator-opt-in at Gate 2, list each bridge.
- **PULL mode:** any newly written bridge notes inside the target project's folder + the project's `punchlist.md` if it gained entries this run. The `_intel-inbox.md` last-triaged metadata is a state update, not an artifact in the evaluation sense.
- **BOOTSTRAP mode:** the new project `_README.md` + `_intel-inbox.md` template + any bridge notes the inline PULL run created.

**The block to emit (verbatim):**

````markdown
## Auto-invoke output-quality-loop

This skill produced the following artifact(s):
- `<bridge-note-1-path>`
- `<bridge-note-2-path>`
- `<project-README-path>`     ← BOOTSTRAP mode only
- `<project-punchlist-path>`  ← PULL mode if punchlist gained entries

[output-quality-loop:eval] — for each artifact, run output-quality-loop in EVALUATE mode. If PASS, declare the chat done. If NEEDS REVISION or FAIL, ingest the revision prompt as if it were operator input and regenerate the artifact, then re-invoke output-quality-loop. Cap at 3 iterations; on the 3rd FAIL, escalate to the operator with the evaluation report.
````

Required-element discipline per the convention spec: heading text matches verbatim (`## Auto-invoke output-quality-loop`); one bullet per artifact with full path in backticks; directive opens with `[output-quality-loop:eval]` and includes the iteration-cap discipline language.

**Note on bridge notes.** Bridge notes are a young artifact type. If the spec-routing table at `~/workspace/skills/output-quality-loop/references/spec-routing-table.md` doesn't yet have a row for bridge notes, Mode 1 will surface the gap explicitly ("no spec routing for type bridge-note"). The operator either names spec sources for that invocation (likely the canonical bridge-note shape from `_meta/templates/template-bridge-note.md` or equivalent + the project's `_README.md` archetypes), extends the routing table, or skips the evaluation per case.

**Iterate or declare done.** All PASS → declare done. Any NEEDS REVISION (minor / substantive) → Mode 2 auto-fires a revision prompt; ingest as operator input, apply fixes (for bridge notes: tighten the apply-action, restore the source-artifact backlink, fix the project-README cross-link; for project READMEs: realign archetypes after operator-confirmed Gate 1 changes), re-emit the block, loop. Any FAIL → revision prompt includes root-cause analysis; address the root cause (often: bridge note missing source backlink, archetype union not actually computed as mechanical union, situational gating violated, half-state write where Gate 2 should have killed Gate 1 writes), regenerate, re-emit, loop.

**Iteration cap (3 max).** Track count via the folder-quality-log's per-artifact section before each regeneration. If three iteration entries exist and the verdict is still not PASS, **escalate** to the operator with the evaluation report and stop. Don't run a fourth iteration — that's the load-bearing cost-control discipline.

**Operator bypass.** Include `--bypass-quality-loop` (or "skip the quality loop") in the original routing request to skip the block for that invocation. The bypass records to the closest folder's `_quality-log.md` under `### Bypassed (manual override)`. Useful for low-stakes batch routing where the operator already trusts the bridge-note shape.

## What this skill does NOT do

- Does NOT promote patterns from 1/3 to 2/3 or 2/3 to 3/3 (vault-curation discipline; no skill yet)
- Does NOT write or modify synthesis documents (that's `multi-source-synthesis`)
- Does NOT triage already-routed artifacts inside project inboxes (that's PULL, Session 2)
- Does NOT scaffold new project folders (that's BOOTSTRAP, Session 3; delegates to `knowledge-os-setup`)
- Does NOT auto-run after VIS or `multi-source-synthesis` (composition is opt-in only)
- Does NOT commit to git (operator commits manually after reviewing diffs)
- Does NOT touch frontmatter fields outside the five named ones (type, status, tags, etc. are left alone)
- Does NOT touch archived projects or archived artifacts

## Reference files

Vault content this skill operates on:

- **Convention spec:** `~/workspace/second-brain/_meta/conventions.md` (Project applicability fields section)
- **Skill spec:** `~/workspace/second-brain/_meta/specs/intel-routing-skill-spec.md`
- **Running execution log:** `~/workspace/second-brain/_meta/execution-logs/exec-log-2026-05-27-intel-routing-rollout.md`
- **Per-project inbox template:** `~/workspace/second-brain/_meta/templates/template-intel-inbox.md`
- **Global opportunities inbox:** `~/workspace/second-brain/_meta/intel-opportunities-inbox.md`
- **Project READMEs:** `~/workspace/second-brain/04_projects/clients/_active/<slug>/README.md` and `~/workspace/second-brain/04_projects/personal/<slug>/README.md` (symlinked from `~/workspace/repos/<slug>/.kos/README.md`)
- **Per-project punchlist:** `~/workspace/second-brain/04_projects/<area>/<slug>/_punchlist.md`

Composition skills:

- **VIS extraction:** `~/workspace/skills/vis-extraction/SKILL.md`
- **Synthesis readiness scan:** `~/workspace/skills/synthesis-readiness-scan/SKILL.md`
- **Multi-source synthesis:** `~/workspace/skills/multi-source-synthesis/SKILL.md`
- **Knowledge OS setup:** `~/workspace/skills/knowledge-os-setup/SKILL.md`
- **App-factory init-project:** `~/workspace/repos/app-factory/prompts/init-project.md`

Worked examples for PUSH:

- **PUSH complex case (multi-project synthesis):** `examples/push-on-seo-cluster-synthesis.md` — PUSH against `03_domains/seo/cluster-synthesis-ai-era-seo-cluster-2026-05-27.md`. Routes to EV + S&H + Keelworks + dad-businesses. Validates the project-first algorithm + archetype union derivation + multi-project bridge discipline.
- **PUSH simple case (narrow source-note routing):** `examples/push-on-jono-claude-code-seo-masterclass.md` — PUSH against the Jono Catliff source. Validates situational archetype gating (excludes S&H + dad-businesses despite hierarchy overlap, because Jono is post-launch-shaped methodology).
- **PULL post-launch case (active engagement):** `examples/pull-on-ev-electric.md` — PULL against EV's inbox. Regression test reproducing Phase 2 manual triage outcome (99 candidates → 6 applies + 88 keeps + 5 defers + 0 not-applicable) exactly. Includes Window B idempotence walkthrough validating routed-at suppression prevents re-bridge churn the day after a triage runs. Validates batched Gate 1 + 10-rule pre-classification + single-bridge-per-cluster discipline at full inbox scale.
- **PULL pre-launch case (GBP-blocked):** `examples/pull-on-s-and-h.md` — PULL against S&H's inbox. Reproduces Phase 2 manual triage outcome (99 candidates → 1 apply + 11 keeps + 87 defers + 0 not-applicable) exactly. Critical validation of rule 3 (slug-named situational conflicts default to defer, not not-applicable) against 87-item bulk situational-conflict scenario; rule 4 validated by GSC-self-takeover apply despite GBP blocker. Exercises the friction-observation-#11 "heavy defer ratio" shape and asymmetry-with-PUSH on situational gating.

Read the worked examples to see Gate 1 + Gate 2 outputs in full for both PUSH and PULL.

## Self-application note

PUSH v1.0 was built in Session 1 of Phase 3 of the intel-routing rollout. Sessions 2 (PULL) and 3 (BOOTSTRAP) follow. Each session lands one mode end-to-end, including composition with existing skills.

The design responds to friction Phase 2 surfaced — bridge-note proliferation, confidence inflation, situational archetype gating, dual-field artifacts — by encoding the right discipline as defaults rather than retrofitting them after PUSH ships. The project-first routing-decision algorithm (vs spec's archetype-first) was a refinement surfaced during the Session 1 design pass; the original spec assumed PUSH would trust existing frontmatter, but the Phase 2 migration-induced over-tagging proved the assumption wrong. PUSH re-derives from body and surfaces the diff against existing.

The two-gate structure (routing decision + bridge proposal) is the load-bearing discipline. Operator decisions on routing are upstream of and orthogonal to operator decisions on bridge content; conflating them at one gate would force the operator to think about both at once and produce worse decisions on both.

After Session 1 ships, the `_meta/specs/intel-routing-skill-spec.md` "Build outcomes" section gets a PUSH-shipped entry noting what was built differently from the original spec and why (the project-first algorithm + the two-gate structure + the situational-archetype-as-gate semantics are the load-bearing differences).
