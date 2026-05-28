---
name: intel-routing
description: Route vault artifacts (tactics, patterns, tools, syntheses, opportunities, content ideas, source notes) to applicable projects, or pull applicable intel from the vault into a project, or bootstrap a new project from accumulated intel. Triggers on phrases like "route this," "route this synthesis," "route this tactic," "push this to applicable projects," "what's new for project X," "what intel applies to <client>," "pull intel for <project>," "triage the inbox for <project>," "promote this opportunity to a project," "create a new project from this," "bootstrap <slug> from <opportunity>," or invocation as a follow-on step after VIS extraction or after multi-source-synthesis. Reads and writes the five project-applicability frontmatter fields (`applies-to-projects`, `applies-to-archetypes`, `applicability-confidence`, `routed-at`, `based-on-clients`) defined in `_meta/conventions.md`. Composes with VIS Step 10 (synthesis-readiness-scan), `multi-source-synthesis` Stage 6, `knowledge-os-setup` add-project-vault mode, and app-factory `init-project`.
---

# Intel-routing skill (v1.0 — PUSH mode)

The skill that closes the loop between vault artifacts and projects. Operates on the convention layer landed in Phase 1 of the intel-routing rollout and matured against friction observed in Phase 2. Phase 3 ships the skill itself across three sessions: PUSH first (this version), then PULL, then BOOTSTRAP.

**Critical behavior (read this before anything else):**

- **Approval gate is mandatory.** PUSH never writes without an explicit operator approve/modify/reject pass on the proposed routing AND on the proposed bridge notes. Two gates, not one — routing decision is upstream of bridge decision.
- **PUSH does not promote, does not synthesize, does not triage.** It computes the five project-applicability fields and writes bridge notes per the operator's bridge-note discipline. Synthesis lives in `multi-source-synthesis`. Pattern promotion is vault-curation discipline (no skill yet). Triage of artifacts already routed is PULL mode.
- **PUSH writes to the artifact's frontmatter and to project folders. Both writes happen on the same approval pass.** Operator approving "routing + bridges" is one decision, not two commits.
- **Read existing frontmatter; do not blindly trust it.** PUSH re-derives the five fields from the artifact body + project READMEs + the convention spec. If existing frontmatter differs from re-derived values, PUSH surfaces the diff at the approval gate so the operator can choose: accept re-derivation (overwrite), keep existing (skip writes), or merge case-by-case.
- **Default discipline: single-bridge-per-cluster, not per-artifact-match.** Phase 2 friction observation #4 (bridge note proliferation) confirmed in practice. PUSH on a synthesis that applies to 4 projects writes 4 bridges (one per project), not 4 × N tactic-match bridges. Per-tactic-bridge writing is operator-explicit opt-in at the approval gate.
- **Situational archetypes are gates, not additive tags.** Phase 2 friction observation #11. If an artifact is post-launch-shaped (its body assumes a live site with measurement baselines), it does not route to pre-launch-only projects even when other archetypes overlap. Same in reverse. Operator can override at the gate.
- **PUSH is the smallest of the three modes; PULL and BOOTSTRAP forward-referenced.** PULL ships in Session 2; BOOTSTRAP ships in Session 3. See `_meta/specs/intel-routing-skill-spec.md` for the full multi-mode plan.

## Three modes (overview)

The skill has three modes, each invoked independently. Modes do not share state; each runs its own approval cycle.

### PUSH mode — artifact → applicable projects

Trigger: operator says "route this," or invoked automatically (opt-in) by `multi-source-synthesis` after writing a synthesis, or invoked automatically (opt-in) by VIS Step 10 after a newly extracted tactic or tool note is calibrated.

Input: a single artifact path (tactic, pattern, tool, synthesis, opportunity, source note, content idea).

Output: five frontmatter fields written on the artifact + N bridge notes written to applicable project folders + N punchlist entries appended.

PUSH is the focus of this v1.0. Full specification below.

### PULL mode — project → applicable artifacts (Session 2, not yet shipped)

Trigger: operator says "what's new for project X," or invoked at the start of a project review session.

Input: a project slug.

Output: updated `_intel-inbox.md` + N bridge notes + N artifact frontmatter updates.

Status: forward reference. The per-project `_intel-inbox.md` Dataview query currently handles PULL manually. When PULL ships, the skill compresses the manual triage loop Phase 2 exercised on EV and S&H. See spec for full operation.

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

## PULL mode — forward reference (Session 2)

Not yet shipped. Spec lives at `_meta/specs/intel-routing-skill-spec.md` section "PULL mode." Operator runs the per-project `_intel-inbox.md` Dataview query manually until PULL ships. The query handles the surface; the manual triage handles the apply/keep/defer/not-applicable decision per item.

Per Phase 2 friction observations: PULL must default to single-bridge-per-cluster, validate project-README/inbox archetype sync at every invocation, default-lower confidence calibration on suspect-high inflated artifacts, and respect situational archetype gating in its query (operator can override per item).

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

PULL (Session 2) will validate that project README `archetypes:` matches the project's `_intel-inbox.md` `archetypes:` at every invocation; warn on mismatch. Not applicable to PUSH.

### Sources-as-applicability question (#12) — open

Sources got migrated to `applies-to-projects` during Phase 2 even though the convention spec lists the field as for "tactics, patterns, tools, syntheses, opportunities, and content ideas" — not sources. PUSH treats source notes as valid inputs (operator may want to PUSH-route a high-value source). The convention question (whether sources should carry applies-to-projects or just provenance) is operator-discipline territory; PUSH does not legislate.

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

- **Complex case (multi-project synthesis):** `examples/push-on-seo-cluster-synthesis.md` — PUSH against `03_domains/seo/cluster-synthesis-ai-era-seo-cluster-2026-05-27.md`. Routes to EV + S&H + Keelworks + dad-businesses. Validates the project-first algorithm + archetype union derivation + multi-project bridge discipline.
- **Simple case (narrow source-note routing):** `examples/push-on-jono-claude-code-seo-masterclass.md` — PUSH against the Jono Catliff source. Validates situational archetype gating (excludes S&H + dad-businesses despite hierarchy overlap, because Jono is post-launch-shaped methodology).

Read the worked examples to see Gate 1 + Gate 2 outputs in full for both cases.

## Self-application note

PUSH v1.0 was built in Session 1 of Phase 3 of the intel-routing rollout. Sessions 2 (PULL) and 3 (BOOTSTRAP) follow. Each session lands one mode end-to-end, including composition with existing skills.

The design responds to friction Phase 2 surfaced — bridge-note proliferation, confidence inflation, situational archetype gating, dual-field artifacts — by encoding the right discipline as defaults rather than retrofitting them after PUSH ships. The project-first routing-decision algorithm (vs spec's archetype-first) was a refinement surfaced during the Session 1 design pass; the original spec assumed PUSH would trust existing frontmatter, but the Phase 2 migration-induced over-tagging proved the assumption wrong. PUSH re-derives from body and surfaces the diff against existing.

The two-gate structure (routing decision + bridge proposal) is the load-bearing discipline. Operator decisions on routing are upstream of and orthogonal to operator decisions on bridge content; conflating them at one gate would force the operator to think about both at once and produce worse decisions on both.

After Session 1 ships, the `_meta/specs/intel-routing-skill-spec.md` "Build outcomes" section gets a PUSH-shipped entry noting what was built differently from the original spec and why (the project-first algorithm + the two-gate structure + the situational-archetype-as-gate semantics are the load-bearing differences).
