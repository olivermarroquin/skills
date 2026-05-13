# Appendix A entry template

Use this template when adding new vocabulary entries to Appendix A of the master primer (`primer-synthesis-vocabulary-and-concepts.md`).

## Entry shape

```
**<Term>** — <1–3 sentence definition assuming Part 1 context>. <Cross-reference.>
```

## Rules

1. **Bold the term.** Use `**Term**` markdown bold.
2. **Em-dash separator** between term and definition: `**Term** — definition.`
3. **1–3 sentences max.** Longer entries signal the term deserves Part 1 treatment, not Appendix A treatment.
4. **Assume Part 1 context.** The reader has access to Part 1; don't re-explain concepts. Cross-reference instead.
5. **Cross-reference using existing format:**
   - `Section X.` — single Part 1 section reference
   - `Sections X and Y.` — multiple sections
   - `Precedent #N.` — one of the 10 operator-discipline precedents
   - `Synthesis Section N.` — section of the Phase B synthesis Part 2 walkthrough
   - `No Part 1 reference needed.` — for narrow technical terms that don't compose with broader concepts
6. **Alphabetical placement.** Splice into Appendix A alphabetically. Don't append to the end.

## Examples (existing entries — match this shape exactly)

```
**Agent** — a program where the LLM runs a decide-act-observe loop until the goal is met. Section B.

**At threshold** — pattern at 3/3 cross-creator. Ready for batch promotion. Section E.

**Cross-substrate-independent-arrival** — three independent creators arriving at the same architectural commitment using three different substrates. Reaches 3/3. Precedent #6. Section G.

**MCP** — Model Context Protocol. Standardized way to expose tools to an LLM. Section C.

**ToS** — Terms of Service (Anthropic's). Section I.
```

## Anti-patterns to avoid

**Too long:**
> ❌ **Substrate** — the foundational layer of software that an agent runs on top of, providing the loop that calls the LLM, the wiring for tools the LLM can use, memory storage, deployment surfaces, and the basic plumbing of "given a goal, run an agent loop until done." Examples include Hermes, OpenClaw, Claude Agent SDK. The word comes from chemistry and biology — a substrate is the material underneath that everything else grows on or reacts with.

This is Part 1 territory, not Appendix A. The actual Appendix A entry should be:
> ✅ **Substrate** — foundational layer your agent runs on. Section B.

**Re-explaining instead of cross-referencing:**
> ❌ **Promoted** — when a pattern has been seen from three different independent creators in their own frameworks, and the operator has run the batch-promotion ritual to move it from at-threshold status to operationally canonical status, the pattern is considered promoted.

The cross-reference does this work:
> ✅ **Promoted** — pattern has run the promotion ritual; moved from at-threshold to operationally canonical. Section E.

**Missing cross-reference:**
> ❌ **Vault** — Obsidian-based collection of markdown notes.

Add the cross-reference:
> ✅ **Vault** — Obsidian-based collection of markdown notes; dual-purpose human/AI data layer. Section D.

**Definitions that drift from Part 1:**
If the Appendix A entry says X and Part 1 says Y, that's a drift bug. Always check that the entry is consistent with what Part 1 teaches.
