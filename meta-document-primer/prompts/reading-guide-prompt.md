# Reading-guide prompt (v2.0)

The authoritative spec for generating per-document reading guides — section-by-section walkthroughs of vault documents (synthesis, decisions, roadmap, alignment, domain notes, project artifacts) that scaffold comprehension using Part 1 concepts from the loaded primer(s).

This prompt is loaded by `meta-document-primer/SKILL.md` Step 7.

**Generalization in v2.0:** the v1.0 version assumed a single master primer was always the conceptual reference. v2.0 supports loading multiple primers simultaneously (primary + secondaries when scope stacks apply). The reading guide cross-references whichever primers were loaded for the target document; the primary primer is the one most-central to the target's scope, secondaries provide cross-reference coverage.

## What a reading guide is

A reading guide is the companion document to a target document. It walks the reader through the target section by section, with notes on what to watch for given the conceptual scaffolding in the loaded primer(s)' Part 1. It's not a summary; it's an annotated tour.

The reader uses the reading guide alongside the target — primer-reading and target document open in parallel. The reading guide assumes the reader has access to all loaded primers' Part 1 sections and Appendix A.

The "loaded primer(s)" depends on the target document's scope. A synthesis-class meta-document might load only the system primer. A marketing tactic note inside a project folder might load the project primer (primary), the marketing domain primer (secondary), and skip the system primer entirely. The skill's Step 2 (resolution) determines which primers are loaded.

## What a reading guide is NOT

- Not a summary that replaces the meta-document. The meta-document is still the canonical content; the reading guide is comprehension scaffolding.
- Not analysis of the meta-document's conclusions. If the meta-document surfaces decisions, the reading guide explains *what's being decided and where the evidence is*; it doesn't weigh the options.
- Not advocacy. If the meta-document is honest about uncertainty or gaps, the reading guide preserves that honesty. It doesn't fill in answers the meta-document deliberately left open.
- Not a re-write of the meta-document's claims. The reading guide refers to the meta-document; it doesn't restate every claim in different words.
- Not a critique of the meta-document. Review work is a separate function; reading guides exist to make comprehension easier, not to evaluate quality. (Exception: genuine ambiguity or unclear phrasing in the meta-document is worth flagging, since it affects comprehension. But that's flagging, not critique.)

## Tone and depth

- **Layman-accessible without dumbing down.** Use plain language but don't sacrifice technical accuracy. If a concept genuinely requires a particular technical term, use the term and cross-reference the primer entry that explains it.
- **Concise where the target is concise; dense where the target is dense.** Don't pad. A short decisions document might warrant a 300-word reading guide; a long synthesis warrants 1500–2500+ words.
- **Cross-reference the loaded primer(s)' Part 1 sections and Appendix A actively.** When a section uses a Part 1 concept, name the concept, cite the section, and name which primer the cross-reference is in ("see marketing primer Section C" or "see system primer Appendix A — substrate"). This is the load-bearing connective tissue.
- **Honest about your own uncertainty.** If the reading guide encounters a section it can't comfortably explain (e.g., because no loaded primer covers the necessary concept), flag this in-line rather than papering over, and identify which primer would need to grow to cover it.

## Structure

The reading guide follows the meta-document's own structural shape. Standard sections:

### Frontmatter

`type: primer-reading`; `status: active`; `created: <today>`; `related: [<target-document>, <primary-primer-base-name>, <any-secondary-primer-base-names>]`; `tags: [primer, reading-aid, <document-type-tag>, <primary-primer-scope-tag>]`.

The `type: primer-reading` field is what the index Dataview query at `_meta/primers/readings/INDEX.md` filters on. It must be exact.

### Opening: what this reading guide is for

A short paragraph (3–5 sentences) naming the target meta-document, its frontmatter type, its overall purpose, and how to use this reading guide alongside it. Mention the master primer as the conceptual reference. State explicitly: "This reading guide does not summarize the meta-document; it scaffolds comprehension of it."

### Document overview at a glance

One short paragraph summarizing the meta-document's shape — how many top-level sections, what the document's overall arc is, where the load-bearing content lives. The reader uses this to orient.

### Section-by-section walkthrough

The body of the reading guide. For each top-level section of the target meta-document:

- **Section heading** matching (or paraphrasing) the meta-document's section heading
- **What this section does** — one sentence on the section's role in the document
- **What to watch for** — the comprehension hooks. What Part 1 concepts are operative; what vocabulary appears; where the load-bearing claims are; what the reader might miss on a first pass
- **Cross-references to master primer** — explicit pointers ("see Part 1 Section E for the cross-creator counting mechanic," "see Appendix A — substrate")
- **Gaps or ambiguity flags (if any)** — anywhere the meta-document is genuinely unclear or where the master primer would need extension to fully cover the section

Subsections of the target meta-document get covered within the parent section unless they're complex enough to warrant their own walkthrough subsection.

### Closing: what to keep in mind

A short closing paragraph (or short list) of cross-cutting things the reader should hold in working memory across the whole document. Examples: audit-pass items that span sections; open decisions whose evidence is distributed; precedents that constrain interpretation throughout.

### Cross-references

`Upstream:` (the master primer; the target meta-document); `Downstream:` (any documents this reading guide will help the reader navigate next); `Related primers:` (other reading guides for related meta-documents).

## Section-walkthrough heuristics

When generating each section's walkthrough:

- **If the meta-document section is mostly inventory** (a list of patterns, tools, tasks): identify the inventory's shape, name the categories, point out which items in the inventory are load-bearing or unusual.
- **If the meta-document section is making claims** (e.g., "the substrate baseline is committed"): identify which claims are foundational vs derived, name the evidence the claims rest on, point out where to cross-check.
- **If the meta-document section is surfacing decisions** (e.g., "6 OPEN decisions"): explain what each decision is asking, where its evidence is, and that the section is *surfacing* not *analyzing*. Don't weigh in.
- **If the meta-document section is summarizing precedents or disciplines**: cite the master primer's Part 1 Section G coverage of operator-discipline precedents and don't re-explain each precedent from scratch.
- **If the meta-document section is an audit-pass or retrospective**: identify which items are reconciliation work (count discrepancies, drift) vs interpretation work (is this metric meaningful?) vs procedural observations (closure-mechanism characterization).

## What to do when concepts are missing from the loaded primer(s)

The skill's Step 4 already produced a gap list, with each gap tagged to the primer it most naturally belongs in. The reading guide should:

- Note the gap inline at the section where the missing concept appears
- Identify which primer the gap belongs in ("this term would belong in the marketing domain primer's Appendix A")
- Provide a one-sentence ad-hoc explanation so the reader isn't stuck mid-document
- Refer to the gap list at the end of the reading guide (or in the final skill report, depending on delivery mode)
- Not pretend any primer covers a term that none of them do; the gap exists and the reader should know

If the gap is large enough to genuinely block comprehension of multiple sections, surface this prominently — at the top of the reading guide — and recommend that the user invoke the skill in `extend-and-write` mode (per-document) or `compound-primer` mode (batch) to address gaps before relying on the reading guide.

## What to do when the meta-document has visible drift or errors

The reading guide is comprehension-focused, not review-focused. But if you encounter content in the meta-document that contradicts itself (e.g., a count in the executive summary that doesn't match the body), or content that contradicts upstream documents in obvious ways, flag it briefly in the relevant section's walkthrough with a note like: "*Note: this section's count of N differs from Section X's count of M. The meta-document doesn't reconcile this; flagging for the reader.*"

Don't editorialize. Don't propose corrections. Just surface the drift so the reader's comprehension isn't built on shaky claims.

If the drift is significant enough that the reading guide's coverage of multiple sections would be misleading, surface this at the top of the reading guide and recommend the user run a review pass (separate from the primer skill) before relying on the meta-document.

## Length calibration

Rough proportions:

- Meta-document ~500 words → reading guide ~200–300 words
- Meta-document ~2000 words → reading guide ~500–800 words
- Meta-document ~5000 words → reading guide ~1200–1800 words
- Meta-document ~10000+ words → reading guide ~2000–3500 words (do not exceed unless the meta-document is genuinely 20000+ words)

These are guidelines, not hard rules. A short meta-document with high vocabulary density may warrant a longer reading guide; a long meta-document that's mostly enumeration may warrant a shorter one. Use judgment.

## Honesty checks before delivering

Before delivering the reading guide:

1. **Did I summarize instead of scaffold?** If the reading guide reads like a summary, it failed. The reader should still need the meta-document; the reading guide should make the meta-document readable, not replace it.
2. **Did I analyze decisions the meta-document deliberately left open?** If yes, strip the analysis. The reading guide explains *what's being decided* and *where the evidence is*; it does not weigh options.
3. **Did I cross-reference Part 1 actively, or did I re-explain Part 1 content inline?** Re-explaining Part 1 inline is duplication and creates drift between the master primer and reading guides. Cross-reference instead.
4. **Did I flag gaps honestly, or paper over them?** Gaps should be visible; reading the guide should make the reader aware of what the master primer doesn't yet cover.
5. **Did I editorialize on the meta-document's quality?** Don't. Reading guides are not reviews.

If any answer reveals a problem, revise before delivering.
