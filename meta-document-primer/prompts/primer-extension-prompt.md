# Primer-extension prompt (v1.0)

The authoritative spec for extending the master primer (`primer-synthesis-vocabulary-and-concepts.md`) — adding new entries to Appendix A and, when warranted, drafting new Part 1 subsections or sections.

This prompt is loaded by `meta-document-primer/SKILL.md` Step 7.

## When extensions are appropriate

Two kinds of extension exist; choose based on the gap shape Step 5 produced.

**Appendix A extension (vocabulary-only).** Use when:
- A term, acronym, or named convention appears in a meta-document but isn't in Appendix A
- The concept the term references is already covered by an existing Part 1 section (or doesn't need full Part 1 coverage because it's narrow)
- The entry can be 1–3 sentences with a cross-reference

**Part 1 extension (concept-level).** Use when:
- A *concept* appears that isn't taught in any Part 1 section, and the concept is broad enough that an Appendix A entry alone would leave the reader without scaffolding
- Multiple terms cluster around a single concept that needs sustained explanation (the agent stack, the threshold mechanic, the operator-discipline precedents — these are all Part 1-shaped)
- The concept is foundational enough that future syntheses will likely build on it

When in doubt, prefer Appendix A. Part 1 extensions are heavier and should be reserved for genuinely new conceptual territory.

## Appendix A entry shape

Each Appendix A entry follows this shape:

```
**<Term>** — <1–3 sentence definition assuming Part 1 context>. <Cross-reference: "Section X." or "Sections X and Y." or "No Part 1 reference needed.">
```

Examples (existing entries the new ones should match in shape):

```
**Agent** — a program where the LLM runs a decide-act-observe loop until the goal is met. Section B.

**Cross-substrate-independent-arrival** — three independent creators arriving at the same architectural commitment using three different substrates. Reaches 3/3. Precedent #6. Section G.

**MCP** — Model Context Protocol. Standardized way to expose tools to an LLM. Section C.
```

Rules:

- Entries assume Part 1 context. Don't re-explain Part 1 concepts in the entry; cross-reference them.
- Entries are 1–3 sentences. Anything longer signals the term deserves a Part 1 subsection rather than an Appendix A entry.
- Cross-references use the existing format: "Section X." for single-section references; "Sections X and Y." for multiple; "Precedent #N." when referencing one of the 10 operator-discipline precedents; "Synthesis Section N." when referencing the Phase B synthesis Part 2 walkthrough.
- "No Part 1 reference needed" is acceptable for narrow technical terms that don't compose with broader concepts.
- Splice entries alphabetically into Appendix A. Maintain the existing alphabetical order strictly.

## Part 1 subsection shape

When a new Part 1 subsection is warranted (extending an existing section with a sub-concept), follow this shape:

```
### <Sub-concept heading>

<Opening sentence framing the sub-concept in plain language>

<Body: 2–6 paragraphs teaching the concept. Use etymology when helpful (the "why is it called that" pattern). Use concrete examples from the vault when possible. Define dependencies on other Part 1 concepts by cross-referencing rather than re-explaining.>

<Closing observation or "putting this together" pointer that connects the sub-concept to the broader section.>
```

Rules:

- Match the layman-tone of existing Part 1 sections. The reference for tone is the existing `primer-synthesis-vocabulary-and-concepts.md`.
- Use concrete examples from the operator's vault. Generic textbook examples are worse than specific vault examples.
- Cross-reference other Part 1 sections actively when the new sub-concept depends on them.
- End the subsection with explicit guidance for how to read the synthesis when the sub-concept appears ("when you see X in a synthesis, it means Y").

## Part 1 section shape

When an entirely new Part 1 section is warranted (a new conceptual layer not yet covered), follow this shape:

```
## Section <Letter> — <Concept name>

<Opening paragraph: why this section exists; what it covers; where it sits in the conceptual stack.>

### <Sub-concept 1 heading>
<Body following the subsection shape above.>

### <Sub-concept 2 heading>
<Body following the subsection shape above.>

### <Putting this together / cross-reference closer>
<Closing subsection summarizing the new section and pointing forward/backward to related sections.>
```

Rules:

- Assign a section letter that places the new section in conceptual-tier order. Earlier letters are more foundational. The new section should be placed where its dependencies are satisfied by preceding sections.
- This may require re-lettering subsequent sections. If the re-lettering is extensive (touching more than 2 sections), surface the choice to the user before writing.
- Match the existing section structure: opening framing paragraph, 2–5 subsections, optional putting-it-together closer.
- Update Appendix A with corresponding entries cross-referencing the new section.

## What to do when the same gap appears multiple times across recent meta-documents

If Step 5 surfaces a vocabulary item that appears across multiple recent meta-documents (not just the current one), this is stronger signal for extension. Mention this in the extension proposal — repeated appearance suggests the concept is becoming load-bearing in the operator's work.

## Tone calibration

The master primer's Part 1 sections are written for someone who:
- Is technically literate but not a specialist in AI agent infrastructure
- Wants to understand *why* terms exist, not just what they mean
- Will re-read sections months later and needs them to still teach, not just remind
- Reads other meta-documents in the vault and needs scaffolding to make those documents readable

Extensions should match this voice. Specifically:
- **Use the second person occasionally** when the explanation is grounded in the operator's own work ("when you read X in the synthesis, it means Y"). Don't overdo it.
- **Use etymology when it makes a term sticky** ("substrate" gets several sentences on the soil-for-plants metaphor because that's what makes the term land). Skip etymology when it doesn't.
- **Use named examples from the vault** ("Hermes is the substrate baseline" rather than "an example substrate would be..."). Generic examples are worse than specific ones.
- **Acknowledge the line between standard discourse and vault-specific terms** explicitly. The reader should know when a term is industry-standard (MCP, agent, harness) vs vault-specific (premature-abstraction precedent, the 1/3-2/3-3/3 mechanic).

## Honesty checks before delivering an extension

Before writing the extension to disk:

1. **Is this extension actually needed, or am I lowering the bar for "extension-worthy" because the gap is here?** If the concept could be adequately explained in 1–2 sentences inline in a reading guide instead of being added to the primer, prefer the inline explanation. The primer should accumulate concepts that are genuinely foundational, not every term that ever appears.

2. **Does this extension duplicate content already in Part 1 or Appendix A?** If yes, the duplicate should not be added. Cross-reference instead.

3. **Does this extension use vault examples?** If the proposed extension reads like a generic textbook entry, it's not earning its place in the operator's primer. Ground it.

4. **Does the cross-reference work?** Test by reading the new entry/section as if you don't know the underlying concept yet. Does following the cross-reference get you there?

5. **For Part 1 extensions: does the section letter assignment respect conceptual-tier ordering?** Earlier sections should be more foundational. A new section that depends on Section G shouldn't be placed at Section D.

If any answer reveals a problem, revise before writing.

## Confirmation discipline

Even in `extend-and-write` mode, the skill surfaces the proposed extension to the user before writing. The shape of the confirmation:

```
Proposed primer extension:

Appendix A additions (alphabetical):
- <new entry 1>
- <new entry 2>

Part 1 changes (if any):
- <section/subsection> at <position>: <brief description>

The master primer's `updated:` field will be advanced to <today's date>.

Confirm extension? (yes / revise / skip)
```

If the user says "yes," write. If "revise," ask what to change. If "skip," don't write; the gap stays flagged for retrospective.
