# Perplexity query templates — index

The canonical query templates live inside each individual Perplexity skill's `references/` folder. This file is the meta-index — a one-stop map of which template lives where and what shape of question it answers. Use it when you're not sure which skill's template applies, or when you're building a new skill and want to see what's already been written so you don't duplicate.

## How the templates are organized

Each suite skill owns its own template file. Templates are query shapes, not literal strings; the skill that owns the template knows how to fill in the slots from the artifact or research goal at hand.

Templates share a vocabulary across skills. A "validate a claim" template in `perplexity-refinement` and a "validate a counter-claim" template in (a future) `perplexity-niche-validation` have the same backbone but different framing for the surrounding context.

## Index by skill

### perplexity-refinement (Wave 0 — shipped)

Six template shapes. Live at `~/workspace/skills/perplexity-refinement/references/query-templates.md`.

- **Validate a claim** — "Is it true that [claim]? Cite primary sources." Used on factual statements in vault artifacts.
- **Validate a tool's current state** — "What is the current pricing, feature set, and reputation of [tool] in 2026?" Used when an artifact recommends or describes a named tool.
- **Validate a statistic** — "What is the original source of the statistic '[stat]' and is it still accurate?" Used on quoted numbers, percentages, dollar ranges.
- **Deepen a concept** — "What are the latest 2026 perspectives on [concept]? Surface 3-5 expert viewpoints with citations." Used on concepts that could be broadened.
- **Find counter-evidence** — "What are the arguments against [claim or concept]? Surface counter-positions with citations." Used when the artifact's conclusion benefits from pressure-testing.
- **Find updated info** — "What's changed about [topic] since [date in artifact]?" Used when the artifact is more than a few months old or names a moving target.

### perplexity-research-suite (Wave 1B — this skill, the router)

No query templates of its own. The router dispatches; it doesn't query.

### perplexity-citation-monitoring (Wave 1C — pending)

Will own query templates focused on "is this site/page cited by Perplexity for query [X]." Templates land when the skill ships.

### perplexity-blueprint-research (Wave 2 — pending, flagship)

Will own a larger set of query templates covering validation, gap-finding, dependency-checking, and readiness-scoring. Estimated 10-15 templates. Land when the skill ships.

### perplexity-topic-gaps (Wave 3A — pending)

Will own templates for content-gap discovery: "what topics in [niche] have the lowest AI-search saturation?" "What questions are being asked that the existing top results don't answer?" Land when the skill ships.

### perplexity-client-discovery (Wave 3B — pending)

Will own templates for prospect research: business profile validation, decision-maker mapping, current vendor identification. Land when the skill ships.

### perplexity-niche-validation (Wave 4A — pending)

Will own templates for niche-entry validation: market size, competitor density, demand signals. Land when the skill ships.

### perplexity-competitor-move-detection (Wave 4B — pending)

Will own templates for competitor-move detection: new product launches, hiring signals, content velocity changes. Land when the skill ships.

### perplexity-ai-overview-hardening (Wave 4C — pending)

Will own templates for AI-Overview hardening: "what triggers Perplexity to cite [URL] for query [X]," "what content structure correlates with citation." Land when the skill ships.

### perplexity-acquisition-signal (Wave 5 — pending)

Will own templates for acquisition-signal scans: market-event detection, executive-move tracking, fundraising signals. Land when the skill ships.

## How to read this index

Two ways.

**As an operator.** When you're trying to remember which skill answers which kind of question, scan this list. Each entry names what the templates do; the linked skill knows the actual query strings.

**As a skill author.** When you're building a new Perplexity-suite skill, scan this list to see what shapes are already covered. If your skill needs a "validate a tool's current state" template, the refinement skill's version is a good starting point — copy it and adjust the framing for your skill's context.

## Cross-skill template borrowing

When two skills need the same query shape, both can copy the template. There's no rule against duplication across skills — the templates are short, and each skill needs the freedom to adjust framing. The duplication rule applies to longer shared infrastructure (browser-setup, cost-rules), which is what `skills/perplexity-shared/references/` is for.

If a template shape becomes truly common (5+ skills using essentially the same shape), promote it into a `perplexity-shared/references/common-query-shapes.md` file at that point. Don't promote prematurely.

## Maintenance

When a new skill ships:

1. Add a section under "Index by skill" with the skill's name, status, and a brief description of its templates.
2. List the template names (not the full strings — those live in the skill's own references).
3. Bump this file's `updated:` line.

When a skill retires:

1. Mark the section "retired YYYY-MM-DD" but leave it in place. The history is useful.

## See also

- [[perplexity-browser-setup]] — pre-query browser checks
- [[perplexity-cost-rules]] — per-invocation caps and weekly budget
- [[perplexity-refinement]] — Wave 0 skill, the first set of templates
- [[perplexity-research-suite]] — router that dispatches to the right skill
