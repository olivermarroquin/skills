# Primer structure reference

A reference doc describing the structure of primers maintained by the `meta-document-primer` skill. Used by the skill to know what shape any primer should take when it's extended or referenced.

This document is read-only reference; it doesn't drive the skill directly. Update it when the canonical primer structure changes.

## Where primers live (the three scopes)

Three primer scopes are supported:

1. **System primer** — synthesis-class meta-document vocabulary.
   Path: `second-brain/_meta/primers/primer-synthesis-vocabulary-and-concepts.md`.
   Audience: anyone reading vault meta-documents (synthesis, decisions, roadmap, alignment).

2. **Domain primer** — vocabulary for a knowledge domain.
   Path pattern: `second-brain/03_domains/<domain>/primer-<domain>-vocabulary-and-concepts.md`.
   One per domain that has dense or specialized vocabulary (marketing, web-development, automation-systems, etc.).

3. **Project primer** — vocabulary specific to one project.
   Path pattern: `repos/<project>/.kos/primer-<project>-vocabulary-and-concepts.md` (vault-visible via symlink at `second-brain/04_projects/<area>/<project>/`).
   One per project where project-specific terms exist.

All three follow the same structural conventions described below.

## Structural layout

Every primer has four top-level parts:

1. **Introduction** ("How to use this primer") — short orientation. Not extended by the skill.
2. **Part 1 — Foundational concepts** — the reusable conceptual scaffolding. Extended when concept-level gaps appear.
3. **Part 2 — Reading guides (legacy/optional)** — pre-v2.0 primers may have an embedded Part 2 reading guide for a specific document. New primers do NOT include Part 2; per-document reading guides become separate files in the corresponding `primer-readings/` folder. See "Part 2 — special case" below.
4. **Appendices** — Appendix A: Vocabulary (alphabetical glossary, extended frequently). Appendix B: Extension path (reference-only).

## Part 1 structure

Part 1 organizes foundational concepts into sections, each labeled with a letter (A, B, C, …). Letters increase as concepts become more derivative (Section A is most foundational; later sections build on earlier ones).

For the system primer, the current section assignments are:

- **A — The big picture.** What's being built and why these meta-docs exist.
- **B — The agent stack.** Agent, substrate, harness, orchestration layer.
- **C — MCP and tools-the-LLM-can-call.**
- **D — The vault.** Note types, prefixes, folder organization.
- **E — Patterns, thresholds, and cross-creator counting.**
- **F — Tiers, clusters, sub-layers, and topology.**
- **G — The operator-discipline precedents.**
- **H — Decision lifecycle and build sequence.**
- **I — ToS and the auth paths.**
- **J — Closure mechanisms.**
- **K — Common confusions.**

For domain and project primers, section letters are assigned per the primer's own conceptual stack. A marketing primer might have sections like:

- A — Search engines and how ranking works
- B — Local search vs. web search
- C — Schema markup and structured data
- D — AEO / GEO / conversational AI search
- E — Conversion rate optimization
- F — Content marketing and authority signals
- ... etc.

The conceptual-tier rule applies regardless of scope: earlier sections are more foundational; later sections build on them.

### Conceptual-tier ordering rules

Sections are ordered from most-foundational to most-derivative. A section that depends on another section's concepts should come after that section. Rough tier framing:

- **Foundational tier (typically A–B).** Big picture; core concepts everything else builds on.
- **Vocabulary tier (typically C–F).** Working terminology used across the domain.
- **Operational tier (typically G–J).** How the system or domain actually operates in practice.
- **Reader-support tier (typically last).** Disambiguations and common confusions.

When adding a new section, place it in conceptual-tier order. Section letter assignment may need to shift to accommodate; re-letter only when the new section is genuinely foundational enough to warrant it.

## Appendix A structure

Alphabetical vocabulary list. Each entry:

- Bold term
- Em-dash separator
- 1–3 sentence definition
- Cross-reference to Part 1 section(s), to another primer (when the term lives in a different primer's Appendix A), or "no Part 1 reference needed."

Maintain alphabetical order strictly. New entries splice alphabetically, not append.

### Cross-primer references

When a term in one primer's domain references a concept central to another primer, cross-reference instead of duplicating. Example in a marketing primer:

```
**JSON-LD** — JavaScript Object Notation for Linked Data; the format Google reads for structured-data markup on web pages. See Section C. Cross-reference: also relevant in web-development primer.
```

Or, when the term is most-central to another primer entirely:

```
**Markov decision process** — see [[primer-automation-systems-vocabulary-and-concepts#markov-decision-process]].
```

The second form is for terms that genuinely belong in a different primer's home scope; don't redefine them.

## Appendix B structure

"How to extend this primer over time." Single-section reference. Covers when to extend, how to extend, and the skill-ification path.

Reference-only — should not be extended by the skill. Update manually when the extension workflow itself changes.

## Part 2 — special case

The original v1.0 system primer had a Part 2 scoped to a specific Phase B synthesis (an embedded reading guide). This was transitional. In v2.0:

- Per-document reading guides are written as **separate files** in the corresponding `primer-readings/` folder, not appended to Part 2 of any primer.
- New primers (domain or project) should NOT include a Part 2. They have Introduction, Part 1, Appendix A, Appendix B — and that's it.
- The system primer's Part 2 may be retired or replaced with a pointer to `_meta/primers/readings/INDEX.md` once enough reading guides have accumulated. This is operator-driven; the skill won't do it automatically.

If you're tempted to add a new reading guide to any primer's Part 2, stop — generate it as a new file in the appropriate `primer-readings/` folder instead.

## Frontmatter conventions

Every primer's frontmatter:

```yaml
---
type: primer
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
scope: <system | domain | project>
related: [<wikilinks-to-related-meta-docs-or-other-primers>]
tags: [primer, meta, reading-aid, vocabulary, concepts, <scope-specific-tags>]
---
```

When extending, update `updated:` to today's date. Leave `created:` unchanged. The `related:` list grows as new meta-documents accumulate that the primer scaffolds. Tags rarely change.

The `scope:` field is new in v2.0 — it tells the skill at a glance which scope this primer occupies. Values: `system`, `domain`, `project`.

## Audiences

Every primer is written for two audiences at once:

- **The operator** — layman-accessible teaching that builds mental models. Etymology used where it makes terms stick. Concrete examples from the vault rather than generic textbook ones.
- **Agents** — definitions precise enough for deterministic term resolution.

The system primer (`primer-synthesis-vocabulary-and-concepts.md`) is the canonical voice example. Match it.

Don't draft sections that read like textbook chapters with vague definitions (fails the agent audience). Don't draft sections that read like dictionary entries without context (fails the operator audience).

## Stylistic conventions

Every primer follows these conventions:

- **Tone:** Layman-accessible; second-person occasionally; explanation-first not reference-first.
- **Etymology:** Used when it makes a term sticky (substrate, harness, JSON-LD's "Linked Data" origin). Not used otherwise.
- **Examples:** From the vault when possible. Generic examples are last resort.
- **Cross-references:** Active and frequent. "See Section X" or "see [[other-primer#term]]" is correct; restating cross-referenced content is wrong.
- **Headings:** `##` for top-level sections (with letter-prefix: "Section A — ..."). `###` for subsections.
- **Wikilinks:** `[[bracket-style]]` for vault references; bare references for skill-internal paths.

Extensions should match these conventions. If a proposed extension reads differently from existing sections of the same primer, revise.

## Cross-domain vocabulary handling

Default rule: each term lives in its most-central primer; other primers cross-reference.

Trigger for a shared cross-domain primer: if a term ends up cross-referenced from 3+ domain primers, consider lifting it into a shared primer at `second-brain/_meta/primers/primer-cross-domain-vocabulary.md`. Shape: same as a domain primer (Part 1 + Appendix A). Domain primers point into it instead of redefining.

The cross-domain primer is not built yet. Document the trigger; build only when actually needed.
