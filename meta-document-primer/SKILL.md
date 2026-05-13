---
name: meta-document-primer
description: Help the user (or another agent) read meta-documents in the Knowledge OS vault — synthesis documents, decisions documents, roadmap documents, alignment documents, and other cross-cutting inventory or analysis files — with full comprehension. Maintains the master primer at `/Users/olivermarroquin/workspace/second-brain/_meta/primers/primer-synthesis-vocabulary-and-concepts.md` and generates per-document reading guides on demand. Triggers on phrases like "help me read this synthesis," "explain this synthesis to me," "I want to understand this decisions document," "give me a primer for this," "what does this meta-doc mean," "walk me through this synthesis," "make this readable," "I'm stuck on this synthesis vocabulary," "create a reading guide for this," or any time the user (or an agent) needs comprehension support for a vault meta-document (frontmatter `type: synthesis`, `type: decisions`, `type: roadmap`, `type: alignment`, `type: primer`, or other cross-cutting inventory/analysis files). Also triggers when the user mentions they're about to read a synthesis-class document and wants help, when a phase closes and the operator wants a primer-currency check, or when a Cowork/Claude review chat needs comprehension scaffolding before doing review work on a meta-document. This is the primary path for meta-document comprehension support in the Knowledge OS.
---

# Meta-document Primer Skill (v1.0)

The meta-document comprehension skill. Maintains the master primer (`primer-synthesis-vocabulary-and-concepts.md`) and produces per-document reading guides for synthesis-class meta-documents in the Knowledge OS vault.

**Critical behavior (read this before anything else):**
- **Read-only by default.** Default mode is `read-for-me` — comprehension scaffold delivered inline; no files written. Only switch to `extend-and-write` when the user explicitly says so.
- **The master primer is the source of truth.** Before extending it, read it. Before generating a reading guide, consult it. Don't duplicate content already in the master primer; reference it instead.
- **Conservative on extension.** When new vocabulary surfaces in a meta-document, flag the gap and propose extension. Don't write to the master primer without operator confirmation, even in `extend-and-write` mode for the master primer itself.
- **Don't replace the meta-document.** The skill produces comprehension support; it never modifies the meta-document being read.
- **Don't drift into producing the meta-document's analysis.** Reading guides scaffold comprehension; they don't decide, advocate, or propose work the meta-document itself is supposed to do.

## Core workflow

When invoked, follow these steps in order. Stop and ask the user only when explicitly required.

### Step 1 — Identify the target meta-document

The user gave you one of:
- A path to a vault meta-document (e.g., `_meta/synthesis/phase-b-synthesis-2026-05-10.md`)
- A document title or descriptor ("the Phase B synthesis," "the decisions document," "the latest synthesis")
- A direct paste of meta-document content into the conversation

If the input is ambiguous (e.g., user said "help me read the latest synthesis" and multiple syntheses exist), list candidate paths from `_meta/synthesis/`, `_meta/decisions/`, `_meta/roadmap/`, `_meta/alignment/` and ask which one. Don't guess.

If the user pasted content directly without specifying a path, treat that as the meta-document; note that no file will be referenced by path, but the comprehension scaffold can still be produced.

### Step 2 — Identify the mode

Default mode: `read-for-me` (read-only; comprehension scaffold delivered inline; no files written; master primer not modified).

Override: if the user explicitly says "extend the primer," "write the reading guide to a file," "save this as a primer reading," "make it permanent," "extend and write," or any clear indication that file output is wanted, use `extend-and-write` mode.

If the user doesn't specify, default to `read-for-me`. Explicit signals only.

A third implicit mode exists — `currency-check`. If the user asks "is the primer current?" or "does the primer need updating?" without referencing a specific meta-document, run only Steps 4 and 5 (gap scan + extension proposal); skip reading-guide generation.

### Step 3 — Capture optional scope hint

If the user provided a one-liner explaining what aspect of the document they're trying to understand (e.g., "I'm trying to understand the decisions section specifically," or "I need to spot-check this before commit"), capture it. It tunes the reading guide's emphasis.

If they didn't provide one, leave the field empty — don't ask. The default reading guide covers the whole document evenly.

### Step 4 — Read the master primer

This is a mandatory pre-extension and pre-reading-guide read:

```bash
cat /Users/olivermarroquin/workspace/second-brain/_meta/primers/primer-synthesis-vocabulary-and-concepts.md
```

Hold the master primer's Part 1 sections (A–K), Appendix A (vocabulary), and Appendix B (extension conventions) in working context. The master primer is what the reading guide will reference, and what extensions will modify.

If the master primer doesn't exist, surface this as a problem and ask the user how to proceed — the skill is designed to compose with a pre-existing master primer, not to bootstrap one from scratch. Bootstrapping is out of scope for v1.

### Step 5 — Read the target meta-document and scan for vocabulary gaps

Read the target meta-document fully (paste content from conversation, or read from the provided path):

```bash
cat <path-to-meta-document>
```

Pass through the document with the master primer's Appendix A in working context. For each technical term, acronym, named convention, named precedent, or framing-specific phrase in the meta-document, ask:

1. Is this term defined in Appendix A?
2. Is the concept this term references explained in a Part 1 section?
3. If not, is it explained inline in the meta-document itself?
4. If not, this is a vocabulary gap. Capture it.

Produce a gap list with three categories:
- **Missing from Appendix A** (term used but not in vocabulary reference). Note where the term appears.
- **Missing from Part 1** (concept used but not taught in foundational sections). Note where the concept appears.
- **Borderline** (term is in Appendix A but its current entry may be inadequate for the way it's used in this document). Note the friction point.

### Step 6 — Decide whether to extend the master primer

Apply this decision rule:

- **No gaps found** → primer is current. Skip Step 7. Proceed to Step 8 (reading-guide generation).
- **1–3 gaps found, all missing-from-Appendix-A only** → minor extension. In `read-for-me` mode, flag the gaps to user and continue. In `extend-and-write` mode (for the primer), proceed to Step 7.
- **Substantial gaps (4+ entries, or any missing-from-Part-1 gap)** → significant extension. Flag explicitly. In either mode, propose the extension to the user before drafting — don't draft significant extensions autonomously.
- **Borderline-only gaps** → no extension needed for this run, but flag for retrospective consideration.

When flagging gaps in `read-for-me` mode, present the gap list compactly. Don't lecture; let the user decide whether extension is worth a separate `extend-and-write` invocation later.

### Step 7 — Extend the master primer (extend-and-write mode only)

Two extension paths:

**Path A — Appendix A entries only.** For each new vocabulary entry:

1. Load the entry template:

   ```bash
   cat /Users/olivermarroquin/workspace/skills/meta-document-primer/templates/appendix-a-entry-template.md
   ```

2. Fill the template per the vocabulary item observed in the meta-document. Be concise — Appendix A entries are 1–3 sentences, with a cross-reference to the Part 1 section that would explain the term in full context (or "no Part 1 reference" if the concept doesn't warrant a section).

3. Splice the new entries into Appendix A alphabetically. Maintain alphabetical order.

4. Update the master primer's `updated:` frontmatter field to today's date.

**Path B — New Part 1 subsection or section.** For concepts substantial enough to warrant Part 1 treatment:

1. Load the extension prompt:

   ```bash
   cat /Users/olivermarroquin/workspace/skills/meta-document-primer/prompts/primer-extension-prompt.md
   ```

2. Follow the extension prompt to draft the new content. It will include guidance on layman-tone, etymology when helpful, common-confusions disambiguation, and cross-references.

3. Insert the new content into Part 1 at the appropriate position (concept-tier ordering — earlier sections are more foundational; later sections build on earlier ones).

4. Update Appendix A with corresponding entries cross-referencing the new section.

5. Update the master primer's `updated:` frontmatter field.

**Always confirm before writing.** Even in `extend-and-write` mode, surface the proposed extension to the user as a diff or summary before writing to disk. The master primer is foundational; conservative discipline applies.

### Step 8 — Generate the reading guide

The reading guide is the Part 2 deliverable — a section-by-section walkthrough of the target meta-document, with notes on what to watch for given Part 1 concepts.

Two delivery shapes depending on mode and document type:

**Inline delivery (read-for-me mode, default for non-synthesis documents):**

Deliver the reading guide directly in the conversation. Structured response with:
- A brief opener naming the document and its frontmatter type
- A section-by-section walkthrough (matching the meta-document's own section structure)
- For each section, what to watch for given Part 1 concepts; any gaps flagged in Step 5 that affect comprehension of that section; cross-references to specific Part 1 sections or Appendix A entries
- A short closer noting any audit-pass-shaped items or unresolved questions the reader should keep in mind

Keep the inline reading guide proportional to the meta-document's density. A short decisions document might warrant a 200–400 word guide; a synthesis document warrants 800–2000+ words. Don't pad.

**File delivery (extend-and-write mode, default for synthesis-class documents):**

Load the reading-guide template:

```bash
cat /Users/olivermarroquin/workspace/skills/meta-document-primer/templates/primer-reading-template.md
```

Load the reading-guide prompt:

```bash
cat /Users/olivermarroquin/workspace/skills/meta-document-primer/prompts/reading-guide-prompt.md
```

Generate the full reading guide following the template structure and the prompt's guidance. Write the file to:

```
/Users/olivermarroquin/workspace/second-brain/_meta/primers/readings/primer-reading-{document-base-name}.md
```

Where `{document-base-name}` is the meta-document's filename minus its extension and minus any `phase-*` prefix where redundant. Examples:
- Target: `phase-b-synthesis-2026-05-10.md` → Reading guide: `primer-reading-phase-b-synthesis-2026-05-10.md`
- Target: `phase-b-decisions-2026-05-11.md` → Reading guide: `primer-reading-phase-b-decisions-2026-05-11.md`

If the `readings/` subfolder doesn't exist yet, create it.

If a reading guide already exists for this meta-document (filename collision), surface it. Don't silently overwrite. Ask whether to overwrite, append, or skip.

### Step 9 — Generate the final report

The final report goes in the conversation, not in the vault. Format below.

## Final report format

After the reading guide and any primer extension are complete, produce a report with this structure:

```
META-DOCUMENT PRIMER COMPLETE

Target document: <path-or-descriptor>
                 → frontmatter type: <synthesis|decisions|roadmap|alignment|other>
                 → <word-count> words; <section-count> top-level sections
- Mode: <read-for-me|extend-and-write|currency-check>
- Scope hint: <captured-or-none>

Master primer status:
- Path: /Users/olivermarroquin/workspace/second-brain/_meta/primers/primer-synthesis-vocabulary-and-concepts.md
- Last updated: <date>
- Vocabulary gaps found this run: <count>
- Extensions written this run: <count or "none">

Reading guide delivery:
- Shape: <inline|file>
- Path (if file): <full-path>
- Length: <approximate-word-count>

Gaps flagged for operator review (if any):
- <list of gaps; for each: term-or-concept, where it appeared, why it's a gap, suggested disposition>

Borderline items (if any):
- <list of Appendix-A entries whose current shape may be inadequate; for each: term, friction point observed in this document>

Files written / modified (if extend-and-write):
M <path-to-master-primer>     (if extended)
A <path-to-reading-guide>      (if written as file)

Next steps for you:
1. <document-specific suggestion — e.g., "Review the reading guide alongside the synthesis to spot-check sections 4 and 7">
2. <if extensions written: "Inspect the primer diff and commit if it looks right">
3. <if gaps flagged but not addressed: "Consider invoking the skill in extend-and-write mode to address the flagged gaps, or defer to retrospective">
4. Commit (when ready, run yourself):

   cd /Users/olivermarroquin/workspace/second-brain && git add . && git commit -m "<suggested-message>"
```

## What this skill does NOT do

- Does NOT modify the target meta-document. The meta-document is the subject of comprehension support; it's not edited by this skill.
- Does NOT produce analysis, decisions, or recommendations that the meta-document itself was supposed to produce. Reading guides scaffold comprehension; they don't substitute for the work the meta-document represents.
- Does NOT advocate for or against options in a decisions-class document. The skill explains what's being decided and where the evidence is; the user/agent decides.
- Does NOT auto-write extensions to the master primer without explicit confirmation, even in `extend-and-write` mode.
- Does NOT commit to git. User runs the commit command after inspecting.
- Does NOT push to GitHub. User pushes when ready.
- Does NOT bootstrap a master primer from scratch. If the master primer doesn't exist, surface that and stop.
- Does NOT do extraction. That's `vis-extraction`'s job. The two skills operate at different altitudes (extraction = source → vault; primer = meta-document → comprehension).
- Does NOT chase pattern promotions, cross-creator math, or any other extraction-time discipline. Those are extraction-time concerns. The primer skill is comprehension-time.

## Edge cases

**No master primer at the canonical path.** Surface as a problem. Do not bootstrap. Tell user: "The master primer is expected at `/Users/olivermarroquin/workspace/second-brain/_meta/primers/primer-synthesis-vocabulary-and-concepts.md` but doesn't exist. This skill composes with a pre-existing primer. If you want me to help draft a master primer from scratch, that's a separate, larger task — let me know."

**Target meta-document doesn't exist at the path the user named.** List candidates from likely locations (`_meta/synthesis/`, `_meta/decisions/`, `_meta/roadmap/`, `_meta/alignment/`, plus `_meta/` itself) and ask which the user meant.

**Target document is not a meta-document.** If the user points the skill at a source note, tactic note, tool note, task note, or other non-meta document, gently surface this — those have their own conventions and may not benefit from a primer-style reading guide. Ask whether the user actually wants this skill or a different kind of help.

**Reading guide already exists at the target path.** Don't silently overwrite. Surface the existing file's `updated:` field and ask: overwrite (regenerate fresh), append (add new sections leaving existing), or skip (use existing).

**Master primer is heavily out-of-date.** If gap count exceeds ~10 entries or includes multiple Part 1 gaps, treat this as a substantial-extension situation. Don't draft autonomously; propose a focused extension session to the user. Suggest invoking `extend-and-write` mode specifically for currency-check work before resuming reading-guide generation.

**User pastes meta-document content directly.** Proceed with reading-guide generation in inline shape; file shape isn't possible without a stable filename. Note in the final report that the reading guide was inline-only.

**User asks for a reading guide in `read-for-me` mode but the meta-document is a synthesis-class document.** Honor the mode; deliver inline. Mention at the end of the inline guide that the user can re-invoke in `extend-and-write` mode to persist the reading guide as a file. Don't write the file just because the document type would default to file.

**Skill invoked without a target document.** Ask what document the user wants help reading. List recently-modified meta-documents from `_meta/synthesis/`, `_meta/decisions/`, `_meta/roadmap/`, `_meta/alignment/` as candidates.

**Cowork or another agent invokes the skill on behalf of an upstream task.** The skill's behavior doesn't change based on caller; it produces comprehension support either way. If the caller is an agent doing review work, the reading guide may be more valuable as an inline scaffold for the agent's review than as a file for the operator. Default inline delivery is correct for that case.

## Reference files

The actual content this skill operates on lives outside the skill folder:

- **Master primer:** `/Users/olivermarroquin/workspace/second-brain/_meta/primers/primer-synthesis-vocabulary-and-concepts.md`
- **Reading guides folder:** `/Users/olivermarroquin/workspace/second-brain/_meta/primers/readings/`
- **Vault meta-documents:**
  - Synthesis: `/Users/olivermarroquin/workspace/second-brain/_meta/synthesis/`
  - Decisions: `/Users/olivermarroquin/workspace/second-brain/_meta/decisions/` (if exists)
  - Roadmap: `/Users/olivermarroquin/workspace/second-brain/_meta/roadmap/` (if exists)
  - Alignment: `/Users/olivermarroquin/workspace/second-brain/_meta/alignment/` (if exists)
- **Vault root:** `/Users/olivermarroquin/workspace/second-brain/`
- **Conventions reference:** `/Users/olivermarroquin/workspace/second-brain/_meta/conventions.md`

The skill's own working materials:

- **Reading-guide prompt:** `/Users/olivermarroquin/workspace/skills/meta-document-primer/prompts/reading-guide-prompt.md`
- **Primer-extension prompt:** `/Users/olivermarroquin/workspace/skills/meta-document-primer/prompts/primer-extension-prompt.md`
- **Reading-guide template:** `/Users/olivermarroquin/workspace/skills/meta-document-primer/templates/primer-reading-template.md`
- **Appendix-A entry template:** `/Users/olivermarroquin/workspace/skills/meta-document-primer/templates/appendix-a-entry-template.md`
- **Master primer structure reference:** `/Users/olivermarroquin/workspace/skills/meta-document-primer/references/master-primer-structure.md`

Read these as needed. The prompts are the authoritative specs for content generation; this SKILL.md is the orchestration layer.
