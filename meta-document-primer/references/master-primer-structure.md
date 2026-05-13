# Master primer structure reference

A reference doc describing the structure of the master primer at `/Users/olivermarroquin/workspace/second-brain/_meta/primers/primer-synthesis-vocabulary-and-concepts.md`. Used by the `meta-document-primer` skill to know what it's extending or referencing when generating reading guides.

This document is read-only reference; it doesn't drive the skill directly. Update it when the master primer's structure changes substantially.

## Structural layout

The master primer has four top-level parts:

1. **Introduction** ("How to use this primer") — short orientation. Not extended by the skill.
2. **Part 1 — Foundational concepts** (Sections A–K) — the reusable conceptual scaffolding. Extended when concept-level gaps appear.
3. **Part 2 — Reading guide for a specific synthesis** — currently scoped to the Phase B synthesis. NOT extended by the skill; per-document reading guides for new meta-documents become *new files* in `_meta/primers/readings/`, not additions to the master primer.
4. **Appendices** (A: Vocabulary; B: Extension path) — Appendix A is extended frequently; Appendix B is reference-only.

## Part 1 section letter assignments (current state)

- **A — The big picture.** What's being built and why these meta-docs exist.
- **B — The agent stack.** Agent, substrate, harness, orchestration layer.
- **C — MCP and tools-the-LLM-can-call.** MCP protocol; MCP servers; agent-substrate-as-MCP-backend.
- **D — The vault.** What it is; note types; prefixes; folder organization.
- **E — Patterns, thresholds, and cross-creator counting.** The 1/3 → 2/3 → 3/3 mechanic; canonical creator vs synthesizer vs inspirational source vs originator lineage; promotion ritual.
- **F — Tiers, clusters, sub-layers, and topology.** Source tier vs task tier; cluster; sub-layer; cluster-correction.
- **G — The operator-discipline precedents (the 10).** What a precedent is; the 10 precedents in plain language.
- **H — Decision lifecycle and build sequence.** 5-step plan; COMMITTED / OPEN / DEFERRED; input context.
- **I — ToS and the auth paths.** Path A / B / C; disposition matrix; why ToS matters.
- **J — Closure mechanisms.** Targeted-research closure vs experiment-closure vs wait-and-see-closure.
- **K — Common confusions.** Disambiguations between similar concepts.

## Conceptual-tier ordering rules

Sections are ordered from most-foundational to most-derivative. A section that depends on another section's concepts should come after that section. Rough tiers:

- **Foundational tier (A–B):** Big picture; agent stack. Everything else builds on these.
- **Vocabulary tier (C–F):** MCP, vault, threshold mechanic, topology. These are the working vocabulary.
- **Operational tier (G–J):** Discipline precedents, decision lifecycle, ToS, closure. How the system actually operates.
- **Reader-support tier (K):** Disambiguations. Always last in Part 1.

When adding a new section, place it in conceptual-tier order. Section letter assignment may need to shift to accommodate; do so only when the new section is genuinely foundational enough to warrant re-lettering.

## Appendix A structure

Alphabetical vocabulary list. Each entry:
- Bold term
- Em-dash separator
- 1–3 sentence definition
- Cross-reference to Part 1 section(s), precedent number(s), or "no Part 1 reference needed"

Maintain alphabetical order strictly. New entries splice in alphabetically, not append at the end.

Current entry count: ~80 entries (as of master primer creation, 2026-05-11).

## Appendix B structure

"How to extend this primer over time." Currently single-section: when to extend, how to extend, skill-ification path, cross-references to add as primer grows.

This appendix is reference-only and should not be extended by the skill. If Appendix B needs updates (e.g., the skill-ification path changes because this skill exists now), update it manually with awareness.

## Part 2 — special case

The current master primer has Part 2 scoped to the Phase B synthesis specifically. This is a transitional state — when this skill produces reading guides for other meta-documents, those reading guides go into *new files* at `_meta/primers/readings/`, not into the master primer's Part 2.

Long-term plan (per Appendix B of the master primer): once multiple reading guides exist, Part 2 of the master primer should be retired or replaced with a pointer to the readings folder. The skill should not modify Part 2; if you're tempted to add a new meta-document's reading guide to the master primer's Part 2, stop — generate it as a new file in `readings/` instead.

## Frontmatter conventions

The master primer's frontmatter:

```yaml
---
type: primer
status: active
created: 2026-05-11
updated: <today>
related: [phase-b-synthesis-2026-05-10, master-system-map, knowledge-os_obsidian-system-builder, knowledge-os_architecture-and-expansion-system, current-goals]
tags: [primer, meta, reading-aid, vocabulary, concepts, synthesis-class-documents]
---
```

When extending the primer, update the `updated:` field to today's date. Leave `created:` unchanged. The `related:` list should grow as new meta-documents accumulate that this primer scaffolds. Tags rarely change.

## Stylistic conventions

The master primer follows these conventions:

- **Tone:** Layman-accessible; second-person occasionally; explanation-first not reference-first.
- **Etymology:** Used when it makes a term sticky (substrate, harness). Not used otherwise.
- **Examples:** From the vault when possible. Generic examples are last resort.
- **Cross-references:** Active and frequent. "See Section X" is correct; restating Section X's content is wrong.
- **Headings:** `##` for top-level sections (with letter-prefix: "Section A — ..."). `###` for subsections. Anything deeper rarely needed.
- **Wikilinks:** `[[bracket-style]]` for vault references; bare references for skill-internal paths.

Extensions should match these conventions. The reference for "what does extension content look like" is the existing Part 1 sections — if a proposed extension reads differently from the existing sections, revise to match.

## Files the master primer references

The master primer's `related:` field points to:

- `phase-b-synthesis-2026-05-10` — the synthesis Part 2 scaffolds
- `master-system-map` — architecture context
- `knowledge-os_obsidian-system-builder` — vault context
- `knowledge-os_architecture-and-expansion-system` — knowledge architecture context
- `current-goals` — operator-level goals

When extending, consider whether new `related:` entries are warranted. They should be if the extension materially depends on a meta-document not already in the list.
