---
name: meta-document-primer
description: Help the user (or another agent) read documents in the Knowledge OS vault with full comprehension by routing to the right primer(s) — system, domain, or project. Maintains primer files at multiple scopes (the master/system primer at `_meta/primers/` for synthesis-class meta-documents, per-domain primers at `03_domains/<domain>/` for knowledge domains like marketing or web-development, per-project primers at `04_projects/<area>/<project>/` for specific projects) and generates per-document reading guides on demand. Triggers on phrases like "help me read this," "explain this synthesis to me," "I want to understand this document," "give me a primer for this," "what does this meta-doc mean," "walk me through this," "make this readable," "create a reading guide for this," "compound the marketing primer," "extend the domain primer from recent notes," "primer-currency check on this domain," or any time the user (or an agent) needs comprehension support for a vault document — synthesis, decisions, roadmap, alignment, domain insight notes, project artifacts, or any other doc whose vocabulary spans the working knowledge. Also triggers when the operator wants to grow a primer from recent activity, when a phase closes and primer-currency needs checking, or when an agent needs vocabulary scaffolding before working on a document. This is the primary path for Knowledge OS comprehension support and primer maintenance.
---

# Meta-document Primer Skill (v2.0 — multi-primer)

The Knowledge OS comprehension skill. Maintains primers at three scopes (system, domain, project), generates per-document reading guides, and grows primers from recent vault activity. v2.0 generalizes the v1.0 single-primer design into multi-primer routing.

**Critical behavior (read this before anything else):**
- **Read-only by default.** Default mode is `read-for-me` — comprehension scaffold delivered inline; no files written. Only switch to `extend-and-write` when the user explicitly says so.
- **Primers are the source of truth.** Before extending, read the applicable primer(s). Before generating a reading guide, consult them. Don't duplicate content already in a primer; reference it instead.
- **Conservative on extension.** When new vocabulary surfaces, flag the gap and propose extension. Don't write to a primer without operator confirmation, even in `extend-and-write` mode.
- **Don't replace the target document.** The skill produces comprehension support; it never modifies the document being read.
- **Don't drift into producing the document's analysis.** Reading guides scaffold comprehension; they don't decide, advocate, or propose work the document itself is supposed to do.
- **Primers serve two audiences at once.** Every entry has to land for both the operator (layman-accessible teaching) and agents (precise enough for deterministic term resolution). Don't drift the voice toward only one audience. See "Audiences" below.

## Primer scopes — the three layers

Three layers of primer can exist:

1. **System primer** — synthesis-class meta-document vocabulary. The original primer. Path:
   `second-brain/_meta/primers/primer-synthesis-vocabulary-and-concepts.md`.

2. **Domain primer** — vocabulary for a knowledge domain. One per domain that has dense or specialized vocabulary. Path pattern:
   `second-brain/03_domains/<domain>/primer-<domain>-vocabulary-and-concepts.md`.
   Example: `second-brain/03_domains/marketing/primer-marketing-vocabulary-and-concepts.md`.

3. **Project primer** — vocabulary specific to one project. One per project where project-specific terminology exists (client names, internal product terms, business-specific systems). Lives in the project's `.kos/` folder; visible in the vault via symlink. Path pattern:
   `repos/<project>/.kos/primer-<project>-vocabulary-and-concepts.md`
   (visible in vault at `second-brain/04_projects/<area>/<project>/primer-<project>-vocabulary-and-concepts.md`).

When more than one primer applies to a document, the skill loads all applicable. Most-specific primer wins on conflicting term definitions; the others act as cross-references.

### Synthesis-class docs that touch multiple scopes

When a synthesis-class meta-document spans clusters (e.g., a cross-domain or cross-project synthesis), the system primer is the base AND any applicable domain/project primers stack on top. Example: a synthesis covering Phase B + marketing source notes for a specific client would load the system primer, the marketing domain primer, and the client's project primer.

## Audiences

Every primer is written for two audiences simultaneously:

- **The operator (Oliver).** Layman-accessible teaching that builds genuine mental models. Etymology used where it makes terms stick. Concrete examples from the vault rather than generic textbook ones. Cross-references active.
- **Agents.** Definitions precise enough that an agent can deterministically resolve a term and use it in downstream work without re-deriving meaning from context.

The two audiences are compatible: precise definitions are what teach, and good teaching is what makes agents useful. The system primer (`primer-synthesis-vocabulary-and-concepts.md`) is the canonical voice example — match it.

Don't write primers as if they're for only one audience. If a section reads like a textbook chapter but doesn't define terms crisply, it fails the agent audience. If a section reads like a spec but doesn't teach concepts in plain language, it fails the operator audience.

## Modes

Four modes:

- `read-for-me` (default) — comprehension scaffold delivered inline; no files written; primers not modified.
- `extend-and-write` — write a per-document reading guide as a file; optionally extend the affected primer(s).
- `currency-check` — gap scan + proposed extensions only; no reading guide generated.
- `compound-primer` — point at a domain or project (not a specific doc); scan recent notes in that scope for vocabulary missing from the primer; propose extensions in batch.

If the user doesn't specify a mode, default to `read-for-me`. Explicit signals only.

Override triggers:
- "extend the primer," "write the reading guide to a file," "save this as a primer reading," "make it permanent," "extend and write" → `extend-and-write`
- "is the primer current?" "does the primer need updating?" → `currency-check`
- "compound the primer," "extend the marketing primer from recent notes," "primer-currency check on <domain>," "primer-extension pass on <scope>" → `compound-primer`

## Core workflow (per-document modes)

For `read-for-me`, `extend-and-write`, and `currency-check`. The `compound-primer` workflow is described separately below.

### Step 1 — Identify the target document

The user gave you one of:
- A path to a vault document
- A document title or descriptor
- A direct paste of document content

If the input is ambiguous, list candidate paths in likely locations and ask. Don't guess.

If the user pasted content directly without specifying a path, treat that as the document; note that no file will be referenced by path, but the comprehension scaffold can still be produced (file-output modes won't be available for inline-only documents).

### Step 2 — Resolve and load the applicable primer(s)

Resolution algorithm:

1. **Did the user name a primer explicitly?** ("Use the marketing primer to read this.") If yes, that primer is the primary. Continue to check whether other primers also apply.

2. **Walk up from the target's folder.** Collect every primer whose scope is in-path:
   - If target is inside `04_projects/<area>/<project>/`, look for the project primer at the project root.
   - If target is inside `03_domains/<domain>/`, look for the domain primer at the domain root.
   - If target's frontmatter has `domain:`, `client:`, `venture:`, or `relevant-projects:` fields, look for matching domain/project primers too. Marketing tactic notes with `relevant-projects: [s-and-h-contracting, ev-electric-services]` would load the marketing domain primer plus both project primers (if they exist).

3. **Is the target synthesis-class?** If it lives in `_meta/synthesis/`, `_meta/decisions/`, `_meta/roadmap/`, or `_meta/alignment/`, always load the system primer. Domain/project primers stack on top if applicable per step 2.

4. **Does the target reference system-vocab terms even though it isn't synthesis-class?** Quick scan of the doc for system-primer vocabulary signals (e.g., "1/3 cross-creator math," "canonical creator," "operator-discipline precedent," "Karpathy weight," "stat-gated," "premature-abstraction"). If any appear, also load the system primer as a **secondary**. This catches domain/project docs that lean on the system primer's framework without being formally synthesis-class.

5. **No primer found at the relevant scope?** If the target is a domain doc and no domain primer exists, ask the user: "No marketing domain primer found. Do you want me to bootstrap one, or proceed with just the system primer?" Don't auto-bootstrap.

The most-specific primer that applies becomes the **primary**. The others are **secondary**.

Read each loaded primer's Part 1 sections and Appendix A into working context. Hold them all in memory simultaneously — gap scanning needs to check the term against every loaded primer's vocabulary.

### Step 3 — Capture optional scope hint

If the user provided a one-liner explaining what aspect of the document they're trying to understand, capture it. It tunes the reading guide's emphasis.

If they didn't, leave the field empty.

### Step 4 — Read the target and scan for vocabulary gaps

Read the target document fully.

Pass through the document with every loaded primer's Appendix A in working context. For each technical term, acronym, named convention, named precedent, or framing-specific phrase, ask:

1. Is the term defined in any loaded primer's Appendix A?
2. Is the concept the term references explained in a Part 1 section of any loaded primer?
3. If not, is it explained inline in the target document itself?
4. If not, this is a vocabulary gap. Capture it.

Produce a gap list with three categories:
- **Missing from Appendix A** (term used but not in any loaded primer's vocabulary). Note where the term appears and which primer it most naturally belongs in (based on the term's most-central scope).
- **Missing from Part 1** (concept used but not taught in any loaded primer's foundational sections). Note where it appears and which primer it belongs in.
- **Borderline** (term is in a loaded primer's Appendix A but the current entry may be inadequate for the way it's used). Note the friction point.

When tagging gaps to a primer scope, use these heuristics:
- Term is specific to a single project → project primer
- Term is specific to a single domain → domain primer
- Term is cross-cutting (used in synthesis-class docs across scopes) → system primer
- Term spans 2+ domains but isn't synthesis-vocab → flag as candidate for future cross-domain primer (don't create one; just note it; see "Cross-domain vocabulary handling" below)

### Step 5 — Decide whether to extend the primer(s)

Apply this decision rule per affected primer:

- **No gaps found for this primer** → primer is current. Skip extension for it.
- **1–3 gaps, all Appendix A only** → minor extension. In `read-for-me` mode, flag to user and continue. In `extend-and-write` mode, proceed to Step 6 for this primer.
- **Substantial gaps (4+ entries, or any missing-from-Part-1 gap)** → significant extension. Flag explicitly. In either mode, propose the extension to the user before drafting.
- **Borderline-only gaps** → no extension needed for this run; flag for retrospective.

If multiple primers need extension, present the gap list grouped by primer scope so the user can decide whether to extend all, some, or none.

### Step 6 — Extend the affected primer(s) (extend-and-write mode only)

For each primer to extend, follow the same two-path logic as v1.0 (Appendix A entries vs. Part 1 subsection/section). Load the entry template and extension prompt:

```bash
cat /Users/olivermarroquin/workspace/skills/meta-document-primer/templates/appendix-a-entry-template.md
cat /Users/olivermarroquin/workspace/skills/meta-document-primer/prompts/primer-extension-prompt.md
```

Write paths by scope:
- System primer: `second-brain/_meta/primers/primer-synthesis-vocabulary-and-concepts.md`
- Domain primer: `second-brain/03_domains/<domain>/primer-<domain>-vocabulary-and-concepts.md`
- Project primer: `repos/<project>/.kos/primer-<project>-vocabulary-and-concepts.md` (vault-visible at `second-brain/04_projects/<area>/<project>/...`)

Update the relevant primer's `updated:` frontmatter to today's date.

**Always confirm before writing.** Even in `extend-and-write` mode, surface the proposed extension to the user as a diff or summary before writing to disk. Primers are foundational; conservative discipline applies.

### Step 7 — Generate the reading guide

Reading guide structure is the same regardless of primer scope; only the write path changes.

Two delivery shapes depending on mode:

**Inline delivery (read-for-me mode, default).** Deliver in the conversation. Structured response with:
- Brief opener naming the document and its frontmatter type
- Section-by-section walkthrough
- For each section: what to watch for; gaps flagged in Step 4 that affect comprehension; cross-references to specific primer sections or Appendix A entries (cite which primer each cross-reference is in)
- Short closer noting cross-cutting items

**File delivery (extend-and-write mode).** Load the reading-guide template and prompt:

```bash
cat /Users/olivermarroquin/workspace/skills/meta-document-primer/templates/primer-reading-template.md
cat /Users/olivermarroquin/workspace/skills/meta-document-primer/prompts/reading-guide-prompt.md
```

Write path by **primary primer scope** (the most-specific primer that applied):
- System primary: `second-brain/_meta/primers/readings/primer-reading-<doc-base-name>.md`
- Domain primary: `second-brain/03_domains/<domain>/primer-readings/primer-reading-<doc-base-name>.md`
- Project primary: `repos/<project>/.kos/primer-readings/primer-reading-<doc-base-name>.md`

Where `<doc-base-name>` is the target document's filename minus its extension.

The reading guide's frontmatter `related:` field lists every primer loaded (primary + secondary), so the guide cross-references all of them.

If the corresponding `primer-readings/` subfolder doesn't exist yet, create it.

If a reading guide already exists for this document (filename collision), surface it. Don't silently overwrite. Ask whether to overwrite, append, or skip.

### Step 8 — Generate the final report

The final report goes in the conversation, not in the vault. Format below.

## Final report format

```
META-DOCUMENT PRIMER COMPLETE

Target document: <path-or-descriptor>
                 → frontmatter type: <type>
                 → <word-count> words; <section-count> top-level sections
- Mode: <read-for-me|extend-and-write|currency-check|compound-primer>
- Scope hint: <captured-or-none>

Primers loaded:
- Primary: <path-to-primary-primer>
- Secondary: <list-of-secondary-primers-if-any>

Primer status (per loaded primer):
- <primer-name>: vocabulary gaps found this run: <count>; extensions written this run: <count or "none">

Reading guide delivery:
- Shape: <inline|file>
- Path (if file): <full-path>
- Length: <approximate-word-count>

Gaps flagged for operator review (if any):
- <list of gaps; for each: term-or-concept, where it appeared, which primer it belongs in, suggested disposition>

Borderline items (if any):
- <list of Appendix-A entries whose current shape may be inadequate>

Files written / modified (if extend-and-write):
M <path-to-each-modified-primer>
A <path-to-reading-guide>

Next steps for you:
1. <document-specific suggestion>
2. <if extensions written: "Inspect the primer diff and commit if it looks right">
3. <if gaps flagged but not addressed: "Consider invoking the skill in extend-and-write mode...">
4. Commit (when ready, run yourself):

   cd /Users/olivermarroquin/workspace/second-brain && git add . && git commit -m "<suggested-message>"
```

## Compound-primer mode — workflow

`compound-primer` is the proactive primer-growth mode. The operator points the skill at a scope (a domain folder, a project folder, or a primer file directly), and the skill scans recent notes in that scope for vocabulary missing from the primer, then proposes extensions in batch.

This is the mode that makes primers self-maintaining. Without it, primers drift out of date as vocabulary accumulates in the vault faster than reading-guide invocations surface it.

### Trigger context

`compound-primer` typically gets invoked after a batch of new vocabulary has just landed in the vault. Examples:
- After a VIS skill ingestion run that produced 5–20 new source notes in a domain
- After a phase of client work that introduced new project-specific terms
- On a periodic primer-currency cadence (monthly per domain, for instance)

The mode is also invocable directly any time the operator suspects the primer is out of date.

### Step C1 — Identify the scope

The user gave you one of:
- A domain name ("marketing") → scope is `second-brain/03_domains/marketing/`; primer at `second-brain/03_domains/marketing/primer-marketing-vocabulary-and-concepts.md`
- A project name ("ev-electric-services") → scope is the project folder; primer at the project root
- A path to a primer file directly

If no primer exists at the resolved scope, ask: "No primer found at <path>. Do you want me to bootstrap one as part of this compound run, or skip?"

### Step C2 — Identify the candidate notes

Default: all notes in the scope folder modified in the last 30 days. Override options the user might specify:
- "From these specific notes" (provide paths) — scan only the listed notes
- "Everything in the domain" — scan every note in the scope folder regardless of date
- "Since <date>" — scan notes modified after a specific date
- "Notes referenced by <source>" — scan notes that frontmatter-link to a specific source

If no override, default to last-30-days. State the chosen window in the proposal.

### Step C3 — Load the primer and scan each note

Read the target primer's Part 1 + Appendix A into working context.

For each candidate note, scan for vocabulary gaps using the same heuristics as per-document Step 4. Aggregate gaps across notes — if the same term appears in 5 notes, that's one gap with high signal, not five separate gaps.

Track per gap: the term, where it appears (which notes), suggested entry shape (Appendix A entry vs. Part 1 subsection), and rough confidence in the term's load-bearing status (a term that appears across many notes is more load-bearing than one that appears in one).

### Step C4 — Propose the batch extension

Present the proposal in a structured shape:

```
Compound primer extension — <primer-name>

Scanned: <count> notes modified <date-range>
Notes contributing to gaps: <count>

Appendix A additions proposed (alphabetical):
- <term> — appeared in <count> notes (e.g., <example-note-1>, <example-note-2>)
  Proposed entry: <draft>
- <term> — ...

Part 1 changes proposed:
- <section/subsection> at <position>: <rationale> — <draft outline>

Borderline items (in primer but possibly inadequate):
- <term> — friction observed in <notes>; <suggested revision>

The primer's `updated:` field will advance to <today's date>.

Confirm batch extension? (yes / revise / partial / skip)
```

If the user says:
- `yes` → write all proposed extensions to the primer
- `revise` → ask which to change
- `partial` → ask which to include and which to skip
- `skip` → don't write; the gaps stay flagged for a future run

### Step C5 — Write and report

If approved, write extensions to the primer (alphabetical splice for Appendix A; conceptual-tier ordering for Part 1). Update `updated:` field. Generate a final report:

```
COMPOUND PRIMER COMPLETE

Scope: <domain or project>
Primer: <path>
Notes scanned: <count>
Date range: <range>

Extensions written:
- Appendix A entries: <count>
- Part 1 additions: <count>

Files modified:
M <path-to-primer>

Next steps for you:
1. Review the primer diff
2. Commit (when ready):
   cd /Users/olivermarroquin/workspace/second-brain && git add . && git commit -m "primer: compound from <scope> activity"
```

## Closing step — Auto-invoke output-quality-loop

After the per-document reading guide or compound-primer extension has been written and the final report has printed, emit the standard auto-invoke block per `~/workspace/skills/output-quality-loop/references/auto-invoke-convention.md` and `~/workspace/second-brain/_meta/conventions.md` § "Output quality". This is the closing step every artifact-producing skill emits before declaring the chat done. Convention shipped Phase 5 of the output-quality-loop project (2026-05-28).

**Artifact list for this skill.** In single-doc primer mode: the reading guide written into the scope-appropriate `primer-readings/` folder (e.g., `~/workspace/second-brain/_meta/primers/readings/primer-reading-<topic>-<YYYY-MM-DD>.md` or domain/project equivalent per the conventions filing rule). In compound-primer mode: the primer file that was extended. Do NOT include the target document being read — this skill never modifies it.

**The block to emit (verbatim):**

````markdown
## Auto-invoke output-quality-loop

This skill produced the following artifact(s):
- `<reading-guide-path>`        ← single-doc primer mode
- `<extended-primer-path>`      ← compound-primer mode

[output-quality-loop:eval] — for each artifact, run output-quality-loop in EVALUATE mode. If PASS, declare the chat done. If NEEDS REVISION or FAIL, ingest the revision prompt as if it were operator input and regenerate the artifact, then re-invoke output-quality-loop. Cap at 3 iterations; on the 3rd FAIL, escalate to the operator with the evaluation report.
````

Required-element discipline per the convention spec: heading text matches verbatim (`## Auto-invoke output-quality-loop`); one bullet per artifact with full path in backticks; directive opens with `[output-quality-loop:eval]` and includes the iteration-cap discipline language.

**Note on reading guides.** If the spec-routing table at `~/workspace/skills/output-quality-loop/references/spec-routing-table.md` doesn't yet have a row for reading guides, Mode 1 will surface the gap explicitly ("no spec routing for type X"). The operator either names spec sources for that invocation, extends the routing table, or skips the evaluation per case. Don't fabricate spec sources.

**Iterate or declare done.** All PASS → declare done. Any NEEDS REVISION (minor / substantive) → Mode 2 auto-fires a revision prompt; ingest as operator input, apply fixes (for reading guides: tighten the section-by-section guidance, add missing vocab gloss, fix a wikilink to the parent primer; for primer extensions: re-tier an entry's conceptual placement, adjust an alphabetical splice, fix a Part 1 anchor), re-emit the block, loop. Any FAIL → revision prompt includes root-cause analysis; address the root cause (often: primer extension drifted beyond compound-only scope, advocate-for-options leak in a decision-doc reading guide, comprehension scaffolding muddled with analysis), regenerate, re-emit, loop.

**Iteration cap (3 max).** Track count via the folder-quality-log's per-artifact section before each regeneration. If three iteration entries exist and the verdict is still not PASS, **escalate** to the operator with the evaluation report and stop. Don't run a fourth iteration — that's the load-bearing cost-control discipline.

**Operator bypass.** Include `--bypass-quality-loop` (or "skip the quality loop") in the original request to skip the block for that invocation. The bypass records to the closest folder's `_quality-log.md` under `### Bypassed (manual override)`.

## What this skill does NOT do

- Does NOT modify the target document. Comprehension support only; never edits the doc being read.
- Does NOT produce analysis, decisions, or recommendations that the document itself was supposed to produce.
- Does NOT advocate for or against options in a decisions-class document.
- Does NOT auto-write extensions without explicit confirmation, even in `extend-and-write` or `compound-primer` mode.
- Does NOT commit to git. User runs the commit command after inspecting.
- Does NOT push to GitHub.
- Does NOT bootstrap a primer from scratch without confirmation. If the target's scope has no primer, ask.
- Does NOT do extraction. That's `vis-extraction`'s job.
- Does NOT chase pattern promotions, cross-creator math, or other extraction-time discipline.

## Edge cases

**No primer found at the relevant scope.** Ask the user whether to bootstrap one as part of this run, or proceed with whichever primers do load (and fall back to system primer for synthesis-class docs).

**Multiple primers apply but their definitions of the same term conflict.** Most-specific primer wins for the reading guide's purposes. Flag the conflict to the operator in the report so they can decide whether to reconcile.

**Target document doesn't exist at the path the user named.** List candidates from likely locations and ask.

**Target is not a meta-document but is in a domain with a domain primer.** This is fine — domain primers serve any note in their scope (insights, tactics, sources, etc.), not just meta-documents. Generate a reading guide if the target's vocabulary density warrants one. If the target is so simple it doesn't need one, say so and offer to skip.

**Reading guide already exists at the target path.** Surface and ask: overwrite, append, or skip.

**Primer is heavily out-of-date.** If gap count exceeds ~10 entries or includes multiple Part 1 gaps, treat as substantial-extension; propose a focused extension session. Suggest `compound-primer` mode if the gap density suggests broader maintenance is needed.

**User pastes document content directly.** Inline-only; file output isn't possible without a stable filename. Note in the final report.

**Compound-primer scope has zero recent notes.** Tell the user the scope had no qualifying activity in the date window and offer to widen the window.

**Compound-primer scope has primer-missing terms but they're all single-occurrence.** Flag them lower-confidence. Single-occurrence terms might be one-off rather than load-bearing. Recommend either skipping them or holding for the next compound run when more signal accumulates.

**Synthesis-class document references a domain that has no primer yet.** Load the system primer; flag the gap; offer to bootstrap the domain primer if the synthesis would meaningfully benefit. Don't auto-bootstrap.

## Cross-domain vocabulary handling

Default rule: each term lives in the most-central primer for its scope. Other primers reference via wikilink:
```
**JSON-LD** — see [[primer-marketing-vocabulary-and-concepts#json-ld]].
```

This avoids duplication while preserving cross-domain discoverability.

**Trigger to revisit:** if you find a term being cross-referenced from 3+ domain primers, that's the signal to consider lifting it into a shared primer. Shape it would take:
- Path: `second-brain/_meta/primers/primer-cross-domain-vocabulary.md`
- Structure: same as a domain primer (Part 1 + Appendix A)
- Scope: terms that genuinely span 3+ domains
- Domain primers cross-reference into it instead of redefining

This isn't built yet. The trigger is documented so you'll know when it's time.

## Index for reading guides

A single index file lives at `second-brain/_meta/primers/readings/INDEX.md`. It's a Dataview-based auto-index:

````markdown
# Reading guides — index

> Auto-generated from `type: primer-reading` frontmatter. Don't edit by hand.

```dataview
TABLE
  file.path AS "Reading guide",
  related[0] AS "Target document",
  updated AS "Updated"
FROM "second-brain" OR "repos"
WHERE type = "primer-reading"
SORT updated DESC
```
````

Because the index is a Dataview query, it never goes stale — every reading guide written anywhere in the vault (any domain, any project, the system path) shows up automatically as long as its frontmatter is correct.

If a reading guide is written by this skill, its frontmatter must include `type: primer-reading` for the index to pick it up. The template enforces this.

## Reference files

The skill's working materials (templates, prompts, references):

- **Primer structure reference:** `/Users/olivermarroquin/workspace/skills/meta-document-primer/references/primer-structure.md` (formerly `master-primer-structure.md`; generalized in v2.0 to apply to all primers)
- **Reading-guide prompt:** `/Users/olivermarroquin/workspace/skills/meta-document-primer/prompts/reading-guide-prompt.md`
- **Primer-extension prompt:** `/Users/olivermarroquin/workspace/skills/meta-document-primer/prompts/primer-extension-prompt.md`
- **Reading-guide template:** `/Users/olivermarroquin/workspace/skills/meta-document-primer/templates/primer-reading-template.md`
- **Appendix-A entry template:** `/Users/olivermarroquin/workspace/skills/meta-document-primer/templates/appendix-a-entry-template.md`

The vault paths the skill operates on (primer files + reading-guide folders) are scope-derived per the rules above; they're not enumerated here because they grow as new primers come online.

The system primer remains at: `/Users/olivermarroquin/workspace/second-brain/_meta/primers/primer-synthesis-vocabulary-and-concepts.md`.

Vault root: `/Users/olivermarroquin/workspace/second-brain/`.
Conventions reference: `/Users/olivermarroquin/workspace/second-brain/_meta/conventions.md`.

Read these as needed. The prompts are the authoritative specs for content generation; this SKILL.md is the orchestration layer.
