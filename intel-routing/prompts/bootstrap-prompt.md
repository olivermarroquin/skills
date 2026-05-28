# BOOTSTRAP mode operating prompt

This is the executor-facing prompt invoked when intel-routing skill BOOTSTRAP mode fires. Follow the steps in order; do not skip stages.

## Step 0 — Confirm the source artifact

Operator's invocation should name a source artifact (typically an opportunity from `00_inbox/decisions-pending/`, but any artifact type is valid). If missing or ambiguous, ask:

> Which source artifact should I bootstrap from? Provide the full path (e.g., `00_inbox/decisions-pending/opportunity-onboarding-agent-productized-service.md`) or the slug.

If invocation includes an operator-proposed slug (e.g., "bootstrap onboarding-agent from <source>"), record it for the Gate 1 proposal. Otherwise derive the slug at Stage A2.

## Step 1 — Precondition checks

Run in order. Halt on first failure.

1. **Resolve the source artifact path.** If the path doesn't exist, BLOCKED with the unresolved path.
2. **Source has frontmatter.** Minimum `type:`, `status:`, `created:`, `tags:`. If missing or malformed, BLOCKED ("source frontmatter incomplete; fix before re-invoking BOOTSTRAP").
3. **At least one existing project README with `archetypes:`.** Enumerate `04_projects/{clients/_active,clients/_private,personal}/*/README.md`; verify at least one has the `archetypes:` field. If zero, BLOCKED ("BOOTSTRAP needs at least one existing project for apply-to-existing detection; declare archetypes on a project README before re-invoking").
4. **Convention spec readable** at `~/workspace/second-brain/_meta/conventions.md`.
5. **KOS-setup script present** at `~/workspace/skills/knowledge-os-setup/scripts/init-project-vault.sh` AND the assets at `~/workspace/skills/knowledge-os-setup/assets/templates/project/`. If absent, BLOCKED for yes-repo path; knowledge-only path can still proceed if operator opts in at Gate 1.

If any precondition fails, emit:

```
BOOTSTRAP BLOCKED on precondition failure.

Failed precondition: <name>
Required: <what's needed>
Suggested remediation: <what operator should do>

BOOTSTRAP will NOT proceed until precondition is resolved.
```

Exit.

## Step 2 — Gather inputs

In this order:

1. **Source artifact full content** — frontmatter + body. Body is load-bearing for archetype recommendations and apply-to-existing detection. Extract:
   - Existing `applies-to-projects:` (if set)
   - Existing `applies-to-archetypes:` (if set, but may be stale — Phase 2 migration didn't touch most opportunities)
   - Existing `applicability-confidence:` (if set)
   - Existing `routed-at:` (if set)
   - Tier (from `tier:` if present — informs the operator's signal-strength)
   - Body summary in 1-2 sentences

2. **Every existing project README** under `04_projects/`. For each:
   - `archetypes:` (load-bearing for apply-to-existing detection)
   - `archived:` (skip archived projects)
   - Body purpose statement (used for body-alignment check)

3. **Convention spec.** Re-read on every invocation:
   - Project applicability fields section
   - Archetype hierarchy section (specifically: note which archetypes are flagged `(future)`)

4. **Vault reconnaissance for pre-population estimate.** Once you have the recommended archetype set (computed in Stage A2), run an archetype-based query against:
   - `03_domains/`
   - `05_shared-intelligence/`
   - `00_inbox/decisions-pending/`

   Count artifacts whose `applies-to-archetypes:` has any overlap with the recommended set. Surface this count at Gate 1 as the pre-population estimate. (Friction observation #8 maturation — operator should know expected PULL surface size before scaffolding.)

## Step 3 — Compute Stage A scaffold-decision

### Step 3a — Apply-to-existing detection

For each non-archived existing project, compute:

- **Archetype overlap count** — `len(set(source.applies-to-archetypes) ∩ set(project.archetypes))`. If source's `applies-to-archetypes:` is empty or stale, first infer the archetype set from body content (use the same body-driven archetype inference PUSH Stage A Step 1 does — look for hierarchy keywords like "electrical contractor," "saas product," "agency," etc., plus situational keywords).
- **Body alignment** — does source's body describe work that fits within the project's scope per the project's README purpose statement? Heuristic: keyword overlap between source body and project purpose + execution-log signals + name match.

Grade each project:

- **Strong overlap** — ≥3 archetypes match AND body alignment is clear
- **Partial overlap** — 1-2 archetypes match OR body alignment is partial
- **No overlap** — none of the above

Default recommendation:
- If any project has strong overlap → recommend `APPLY-TO-EXISTING` (default per spec open question #6)
- Otherwise → recommend `PROMOTE-TO-PROJECT`

Both paths get presented at Gate 1; operator picks. Apply-to-existing always shows the recommended target slug + a paste-ready PUSH invocation.

### Step 3b — Scaffold parameters proposal (for promote path)

Even if you're recommending apply-to-existing, prepare the promote-path proposal too — operator may choose to override.

**Slug** — derive from source filename. Strip `opportunity-` prefix; keep kebab-case. Example: `opportunity-onboarding-agent-productized-service.md` → `onboarding-agent-productized-service`. If operator provided a slug at invocation, use theirs and verify uniqueness.

**Slug uniqueness check** — search all `04_projects/{personal,clients/_active,clients/_private}/` for an existing folder with this slug. Collision → flag at Gate 1.

**Area** — infer from source body:
- Body explicitly names client / NDA / contract / external engagement → `clients/_active` (or `clients/_private` if NDA-flagged)
- Body describes operator-internal infrastructure, productized service Oliver builds, or operator-personal initiative → `personal/`
- Body is ambiguous → default to `personal/` with note at Gate 1

**Archetypes** — derive from source body content using the canonical Archetype hierarchy in conventions.md. Discipline:
- Compound-tag every applicable hierarchy level (e.g., `[services-business, professional-services]` not just `[professional-services]`)
- Add applicable situational archetypes (`wordpress-site` / `pre-launch-seo` / `post-launch-seo` / `gbp-dependent`) if relevant
- For each recommended archetype, check whether it's listed as live or `(future)` in conventions. Flag `(future)` archetypes at Gate 1.

**Repo-side scaffold** — default per archetypes:
- `saas-product` / `b2b-saas` / `b2c-saas` / `ai-tooling` / `agency` (when promoted from future) / `productized-service` (when promoted from future) → default `yes-repo`
- Any `services-business` / `home-services-trade` / `professional-services` archetype → default `yes-repo` (client engagements use repo `.kos/` for execution-logs + lessons)
- `personal-system` / `infrastructure-tooling` → default `yes-repo` (repo holds execution-logs even if no code)
- Knowledge-only is rare; operator opts in at Gate 1

**Applicability-confidence** — default `medium`. Operator may upgrade to `high` at Gate 1.

**Founding-artifact** — `[[<source-slug>]]`. The source's slug stripped of path and `.md` extension.

**Purpose statement** — draft a 1-2 sentence purpose from source body's hypothesis or thesis. Format: "Project to <verb> <object> for <beneficiary>; bootstrapped from intel surfacing <opportunity shape>." Operator confirms or edits.

**Pre-population estimate** — count from Step 2 input gathering. Format: "PULL on the new project would surface ~<total> artifacts: ~<slug-named> slug-named (already routed to other projects, here as archetype-overlap-only) + ~<archetype-only> archetype-overlap-only matches. Operator should expect Gate 1 with <total> items."

## Step 4 — Surface Gate 1 (scaffold-decision approval, batched)

Emit in this format:

```
BOOTSTRAP SCAFFOLD PROPOSAL — <source-slug>

Source artifact: <full path>
Type: <type from frontmatter>
Tier: <tier if present, else "not set">
Body summary (1-2 sentences): <executor read>

Existing source frontmatter:
  applies-to-projects: <existing or "not set">
  applies-to-archetypes: <existing or "not set">
  applicability-confidence: <existing or "not set">
  routed-at: <existing or "not set">

Apply-to-existing detection:
  Strong overlap with: <project-slug-list, or "none">
    Reason per project: <archetype-overlap-count + body-alignment summary>
  Partial overlap with: <project-slug-list, or "none">
    Reason per project: <one-line>
  No overlap with: <count of projects checked but no signal>

Recommendation: <PROMOTE-TO-PROJECT | APPLY-TO-EXISTING>
Reason: <one-paragraph explanation of the recommendation>

==== PROMOTE-TO-PROJECT proposal ====

Slug:       <slug>
  Uniqueness: <unique | COLLISION with 04_projects/<area>/<slug>/>
Area:       <personal | clients/_active | clients/_private>
  Inference: <one-line reason>
Archetypes: [<list>]
  Conventions check: <all live | promote-needed for <archetype-list>>
Confidence: <medium | high>
Founding-artifact: [[<source-slug>]]
Repo scaffold: <yes-repo | knowledge-only>
  Default reason: <one-line per archetype-driven rule>

Purpose (proposed):
  <one-paragraph purpose statement>

Friction observations:
  - <if any (future) archetypes: name them + propose conventions.md edit>
  - <if yes-repo: note operator will need to run app-factory init separately if repo doesn't yet exist>
  - <any other observation>

Pre-population estimate:
  PULL on the new project would surface ~<total> artifacts at first triage.
  Slug-named to other projects (archetype-overlap-only for the new project): ~<count>
  Speculative routings (low confidence by default per PULL pre-classification): ~<count>
  Operator should expect Gate 1 on PULL with <total> items.

==== APPLY-TO-EXISTING alternative ====

<If at least one project has overlap, surface the strongest match:>
Target project: <project-slug>
Overlap rationale: <reason>
Suggested invocation (paste into a fresh chat or this one):
  "PUSH-route <source-path> to <project-slug>"
  (exit BOOTSTRAP; source artifact stays in 00_inbox/decisions-pending/ and gets routed via PUSH)

<If no overlap, surface:>
No existing project has meaningful overlap with this source. Promote-to-project is the only path.

Confirm promote / confirm apply-to-existing for <project-slug> / modify <field> /
promote conventions edit for <future-archetype> / promote anyway / reject?
```

If the recommendation is apply-to-existing AND operator confirms it, exit BOOTSTRAP at this point — no scaffolding happens. Emit:

```
BOOTSTRAP EXITED — apply-to-existing path chosen.

Source: <source-path>
Target project: <project-slug>

To proceed, invoke PUSH:
  "PUSH-route <source-path> to <project-slug>"

The source artifact stays in 00_inbox/decisions-pending/ and gets routed via PUSH.
PUSH will write bridge notes to <project-slug>/ and update source frontmatter
(applies-to-projects, applies-to-archetypes, applicability-confidence, routed-at).

No BOOTSTRAP writes occurred.
```

Stop. Operator runs PUSH separately.

### Gate 1 response handling (continued — for promote path)

- **Confirm promote** → proceed to Stage B with proposed parameters
- **Modify <field>** → operator names field to change (slug / area / archetypes / repo / confidence / purpose / founding-artifact). Apply edit; re-emit proposal; wait for confirm.
- **Promote anyway** (when recommendation was apply-to-existing) → operator overrides default; proceed with promote path. Record override note for Stage D source-artifact-update friction observation.
- **Promote conventions edit for <future-archetype>** → operator confirms inline promotion of named archetype from `(future)` to live. Record for Stage B5.
- **Reject** → exit; no writes.

## Step 5 — Stage B writes (atomic, after Gate 1 confirm-promote)

### Step 5a (B1) — Optional repo scaffold

If `yes-repo`:

Check `~/workspace/repos/<slug>/` exists via bash:
```bash
if [ -d ~/workspace/repos/<slug> ]; then echo "exists"; else echo "missing"; fi
```

If exists, skip to Step 5b.

If missing, surface the app-factory paste-prompt:

```
The new project needs a repo at ~/workspace/repos/<slug>/.

App-factory init-project is the right way to create it. To set up:

1. Open a fresh terminal:
     mkdir -p ~/workspace/repos/<slug>
     cd ~/workspace/repos/<slug>

2. Open Claude Code in this directory.

3. Paste the following prompt:

---
You are my senior developer helping me bootstrap a new app.

**App name:** <slug>
**Description:** <purpose statement from Gate 1>
**Stack:** <executor's reasonable default per archetypes — see notes below>
**Date started:** <today>
**Stage:** MVP — building the smallest version that delivers real value

## Context

Read all files in the `docs/` folder before doing anything else.
They define the product, scope, and architecture for this app.

- `docs/product-brief.md` — problem, user, core workflow
- `docs/mvp-scope.md` — what is and is not in scope for MVP
- `docs/architecture.md` — stack decisions, folder structure, boundaries
- `docs/roadmap.md` — current phase and what we're building now

## Your first task

Get this app to a working "hello world" state:

1. Scaffold the project using the chosen stack
2. Create all root config files needed to run locally
3. Create the initial folder structure as defined in `docs/architecture.md`
4. Update `CLAUDE.md` with the real folder structure and dev commands once they exist
5. Get the dev command working — the app should render something

Do not build any features yet. Do not connect auth or database yet.

## Constraints

- Stick to the stack defined in `docs/architecture.md` — no new dependencies without asking
- Keep the folder structure flat until complexity requires nesting
- Every file you create should have a clear reason to exist at MVP
---

Stack-recommendation note (operator may edit before pasting): based on the
archetypes [<list>], a reasonable default stack is <stack-suggestion>. Edit to
fit your preference before pasting.

When the repo is created and Claude Code has scaffolded the docs/ + initial
config, type "repo created" to continue BOOTSTRAP. To skip the app-factory step
(e.g., the project is purely knowledge-shaped for now and code comes later),
type "skip repo init".
```

Wait for operator response.

**On "repo created":** proceed to Step 5b (KOS-setup).

**On "skip repo init":** create the empty repo directory at `~/workspace/repos/<slug>/` so the KOS-setup script's `[ ! -d "$REPO" ]` check passes. Add a stub `~/workspace/repos/<slug>/README.md` noting:
```
# <slug>

Repo created by intel-routing BOOTSTRAP from [[<source-slug>]] on <today>.
App-factory init was skipped; run later when project needs code.
```

Proceed to Step 5b.

If `knowledge-only`:

Skip Step 5b entirely. BOOTSTRAP creates the project folder directly under `~/workspace/second-brain/04_projects/<area>/<slug>/` in Step 5c, with subfolders `execution-logs/`, `lessons/`, `scopes/`, `specs/` to match the standard `.kos/` shape.

### Step 5b (B2) — KOS-setup invocation (if yes-repo)

Execute the script:

```bash
bash ~/workspace/skills/knowledge-os-setup/scripts/init-project-vault.sh \
  ~/workspace/repos/<slug> \
  <area-arg> \
  ~/workspace/second-brain \
  ~/workspace/skills/knowledge-os-setup/assets
```

Where `<area-arg>` maps:
- `personal/` → `personal`
- `clients/_active/` → `clients`
- `clients/_private/` → `clients-private`

The script:
- Creates `~/workspace/repos/<slug>/.kos/{specs,scopes,execution-logs,lessons}/`
- Installs `.kos/README.md` and `.kos/.vault-config.md` from templates (Templater placeholders substituted)
- Symlinks `~/workspace/repos/<slug>/.kos/` into `~/workspace/second-brain/04_projects/<area>/<slug>`

Capture stdout/stderr. If error, abort Stage B and roll back any partial work. Surface the error to operator.

### Step 5c (B3) — README customization

For yes-repo path, the README path is `~/workspace/repos/<slug>/.kos/README.md` (which appears in the vault via symlink as `~/workspace/second-brain/04_projects/<area>/<slug>/README.md`).

For knowledge-only path, create the README directly at `~/workspace/second-brain/04_projects/<area>/<slug>/README.md`. Use the same template content as the KOS-setup script's `assets/templates/project/template-project-readme.md`.

Edit the README to replace the template frontmatter with:

```yaml
---
type: project-readme
project-name: <slug>
status: active
created: <today>
updated: <today>
client: <true if area is clients/_active or clients/_private, else false>
sensitivity: <standard | nda | sensitive>
archetypes: [<list from Gate 1>]
applicability-confidence: <medium | high from Gate 1>
founding-artifact: "[[<source-slug>]]"
tags: [project, vault-root, <slug>]
---
```

Then edit the README body Purpose section:

```markdown
## Purpose

<one-paragraph operator-confirmed purpose statement from Gate 1>
```

Add to the Promotion log section:

```markdown
## Promotion log
- <today> — project bootstrapped from [[<source-slug>]] via intel-routing BOOTSTRAP
```

Leave other body sections (Status, Sensitivity tier, Vault contents, Links, Dataview block, Lessons promoted from this project) at template defaults — operator fills in over time.

### Step 5d (B4) — Inbox file instantiation

Read `~/workspace/second-brain/_meta/templates/template-intel-inbox.md`.

Create `<project-folder>/_intel-inbox.md` with substitutions applied:
- `<% tp.date.now("YYYY-MM-DD") %>` → `<today>` (in frontmatter `created:` + `updated:`)
- `<project-slug>` → `<slug>` (in frontmatter `project:` + `tags:`)
- `<Project name>` → `<slug>` (in H1 — operator can edit to display name later)
- `archetypes: []` → `archetypes: [<list from Gate 1>]`

For yes-repo path, the project-folder path resolves via the symlink to `~/workspace/repos/<slug>/.kos/_intel-inbox.md` — but write to the vault path (`~/workspace/second-brain/04_projects/<area>/<slug>/_intel-inbox.md`) since the symlink should handle the write transparently. Verify the write landed in the repo's `.kos/` via the symlink.

### Step 5e (B5) — Conditional conventions.md edit

If operator confirmed `promote conventions edit for <archetype>` at Gate 1:

Edit `~/workspace/second-brain/_meta/conventions.md` to remove the `(future)` marker on each named archetype. Locate the line via Read; use Edit with exact-text match.

Example for promoting `productized-service` from future to live (if it existed):
- Before: `  └── productized-service (future — promote when a productized-service project appears)`
- After: `  └── productized-service`

Apply one Edit per promoted archetype. Track the changes for the Stage D completion report and the suggested commit.

## Step 6 — Verify Stage B writes

Read each touched file to confirm the change landed:
- `<project-folder>/README.md`
- `<project-folder>/_intel-inbox.md`
- Repo `.kos/README.md` (if yes-repo)
- Repo `.kos/.vault-config.md` (if yes-repo)
- `_meta/conventions.md` (if conventions edit landed)
- Vault symlink `<project-folder>` → `<repo>/.kos/` (if yes-repo) via `ls -la`

On any write failure: roll back Stage B (rm the just-created files; if KOS-setup script ran, rm the `.kos/` directory + symlink). Report the failure mode to operator.

## Step 7 — Stage C: chained PULL pre-population

Invoke PULL on the newly-scaffolded project slug. Pass the new project's slug as input; PULL runs its standard workflow (per `prompts/pull-prompt.md`):

1. PULL Step 0-2 (preconditions + inputs)
2. PULL Step 3 (sync validation will pass — README and inbox have matching archetypes by construction; query against vault using new archetype set)
3. PULL Step 4 (Gate 1 — batched triage surface with pre-classification)
4. PULL Step 5-6 (Stage B + Gate 2 — bridge proposals)
5. PULL Step 7 (Stage C writes — bridges + punchlist + per-artifact routed-at + inbox Last triage)
6. PULL Step 8 (completion report)

BOOTSTRAP does NOT intercept PULL's gates. Operator may approve everything, defer everything, or reject. If PULL is rejected entirely at PULL Gate 1, BOOTSTRAP still completes — project folder + README + inbox exist; just no bridges written. Source artifact still gets its `promoted-to-project:` update at Stage D since the scaffolding succeeded.

Capture PULL's completion report output for the BOOTSTRAP completion report.

## Step 8 — Stage D: source artifact update + completion report

### Step 8a — Source frontmatter writes

Edit the source artifact's frontmatter:

- `applies-to-projects:` — set to `[<new-slug>]` if previously empty/absent, otherwise append `<new-slug>` to existing list
- `routed-at: <today>` — set or overwrite
- `promoted-to-project: <today>` — set or add (new field per conventions v1.2)

Do NOT move the source artifact out of `00_inbox/decisions-pending/`. Frontmatter signals the promotion; physical relocation is a separate operation.

Verify the write landed by re-reading the source file.

### Step 8b — Completion report

Emit:

```
BOOTSTRAP COMPLETE — <new-slug>

Source: <source-path>
  Frontmatter updated:
    applies-to-projects: <new value>
    routed-at: <today>
    promoted-to-project: <today>

Project scaffolded: <area>/<slug>
  Path: 04_projects/<area>/<slug>/
  Repo: <~/workspace/repos/<slug>/ or "knowledge-only">
  Symlink: <vault-path → repo-path or "n/a">

README written: <readme-path>
  Archetypes: [<list>]
  Applicability-confidence: <level>
  Founding-artifact: [[<source-slug>]]
  Purpose: <one-line summary>

Inbox instantiated: <inbox-path>

Pre-population (chained PULL outcome):
  Applied: <count>
  Kept: <count>
  Deferred: <count>
  Not-applicable: <count>
  Already-bridged: <count>

Bridges written: <N>
  <bridge-1-path>
  <bridge-2-path>
  ...

Conventions.md edit: <yes — promoted <archetype> from future to live | no>

Suggested commit (stages by name):

cd ~/workspace/second-brain
git add \
  04_projects/<area>/<slug>/README.md \
  04_projects/<area>/<slug>/_intel-inbox.md \
  <bridge-paths from PULL> \
  <punchlist-path from PULL if created> \
  <artifact-paths with routed-at updates from PULL> \
  <source-artifact-path> \
  _meta/conventions.md  # only if convention edit landed
git status  # verify nothing unintended is staged
git commit -m "Bootstrap project <new-slug> from <source-slug> via intel-routing BOOTSTRAP

Scaffolded under 04_projects/<area>/<slug>/. Archetypes: <list>.
Confidence: <level>. Pre-population PULL: <N> applied, <M> kept, <K> deferred.
<Optional: conventions.md edit promoted <archetype> from future to live.>

Refs: _meta/specs/intel-routing-skill-spec.md"

(If yes-repo, also commit in the repo:)

cd ~/workspace/repos/<slug>
git add .kos/README.md .kos/.vault-config.md
git status
git commit -m "Scaffold .kos/ for intel-routing BOOTSTRAP'd project <slug>

Bootstrapped from [[<source-slug>]] via intel-routing BOOTSTRAP.

Refs: ~/workspace/second-brain/_meta/specs/intel-routing-skill-spec.md"
```

Stop. Do not chain into PUSH or another PULL. The source's promotion-to-project IS the routing.

## Edge cases

- **Operator names a source that's not in `00_inbox/decisions-pending/`.** Any artifact path is valid. Proceed normally.
- **Source has multiple projects already in `applies-to-projects:`.** Surface friction note at Gate 1: "source is already routed to <N> projects. Promote-to-project would add a new project to that list. Consider whether the source belongs in any of the existing target projects' scope first."
- **Recommended slug collides with existing project.** Surface at Gate 1; operator picks different slug or invokes a different operation entirely.
- **Repo exists with `.kos/` already.** KOS-setup script is idempotent and skips. But if `.kos/README.md` already has content, surface warning: "repo's `.kos/README.md` already exists with content. BOOTSTRAP will overwrite. Proceed? (yes / use-existing-README / exit)". Default: ask.
- **Operator chose knowledge-only but area is `clients/_active`.** Surface confirmation at Gate 1: "client engagements typically use yes-repo. Confirm knowledge-only? (yes / switch-to-yes-repo)".
- **Multiple `(future)` archetypes in proposal.** Surface all at Gate 1; operator promotes each independently. Single Edit per archetype, all in Stage B5.
- **Source body too thin for purpose statement.** Surface "purpose draft uncertain; suggest manually OR accept placeholder 'TBD — fill in after scaffolding'" at Gate 1.
- **PULL pre-population surfaces zero items.** Common for new project domains with no existing intel. Emit "0 items surfaced; inbox is empty until vault grows" in the BOOTSTRAP completion report. Skip PULL Gate 1/2 entirely.
- **PULL pre-population rejected at PULL Gate 1.** BOOTSTRAP still completes Stage D (source artifact gets `promoted-to-project:` update). Pre-population just produced zero bridges. Report PULL outcome as "operator rejected pre-population; no bridges written" in completion report.
- **Operator confirms apply-to-existing at Gate 1.** Exit BOOTSTRAP cleanly with the paste-ready PUSH invocation. No Stage B/C/D writes. No source-artifact update either — PUSH handles that when operator invokes it separately.
- **App-factory paste-prompt skipped via "skip repo init" but archetypes include `saas-product`.** Surface a one-line caveat in the completion report: "repo created as stub; run app-factory init when ready to add code". No hard block; operator-discretion territory.
- **Source is archived (`archived: true`).** Surface friction note at Gate 1: "source is archived. Bootstrapping a project from an archived source is unusual — consider whether the source's signal is still current." Operator can proceed (override) or exit.
