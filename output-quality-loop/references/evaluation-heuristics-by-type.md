# Evaluation heuristics by artifact type

Per-type breakdown of hard requirements (must-have for ship), quality dimensions (must-have at threshold), and discipline rules. Mode 1 Phase 3 combines the loaded spec sources with these heuristics to build the checklist.

Each checklist item is one bullet. Each bullet carries a one-line citation to the spec source that defines it.

## Source note (VIS ingestion)

### Hard requirements

- Frontmatter present and well-formed; required fields: `type: source`, `source-type:`, `url:`, `creator:`, `published:`, `created:`, `updated:`, `tags: [source, ...]` (spec source: `conventions.md` §3.2)
- Required sections present in order: Take-away → In plain English → Tools mentioned → Workflow breakdown → Strategy extraction → Tactic candidates → Pattern candidates (spec source: `vis-extraction/SKILL.md`)
- Plain-English layer present: top-level `## In plain English` section after Take-away (3-5 sentences) (spec source: `conventions.md` §3.2)
- Plain-English callouts at end of Take-away, Tools mentioned, Workflow breakdown, Strategy extraction (1-3 sentences each) (spec source: `conventions.md` §3.2)
- Acronym expansion on first use for every acronym (spec source: `conventions.md` §3.2)
- Source URL resolvable (or flagged as paywalled / dead) (spec source: `vis-extraction/SKILL.md`)

### Quality dimensions

- Take-away is concrete and operator-actionable, not generic restatement of source title (threshold: pass)
- At least 3 tactic candidates surfaced (threshold: pass for tier-1/tier-2 sources)
- At least 1 pattern candidate surfaced for sources of operator-strategic interest (threshold: pass)
- Voice matches the source-note conventions (technical-dense in the structured sections; plain in the callouts) (threshold: pass)
- Cross-references to related vault artifacts present via wikilinks (threshold: 2+ for tier-1, 1+ for tier-2)
- Project-applicability frontmatter fields (`applies-to-projects`, `applies-to-archetypes`, `applicability-confidence`) present and non-empty (threshold: present + confidence assessed)

### Discipline rules

- Non-destructive on the original transcript / URL (the source note doesn't claim to be the source) (spec source: `vis-extraction/SKILL.md`)
- Plain-language compliance in the callouts (spec source: `plain-language-conventions.md`)
- No fabricated citations (every claim attributed to the creator is actually in the source) (spec source: `vis-extraction/SKILL.md`)
- Slug-only wikilinks (spec source: `conventions.md` § "Cross-task wikilink convention")
- Tags follow the structural-not-topical convention (spec source: `conventions.md` § "Tag rules")

## Perplexity-refinement output

### Hard requirements

- Refinement section present (append mode) OR sister file present (sister-file mode) (spec source: `perplexity-refinement/SKILL.md` Phase 4)
- Six Phase-3 buckets in order (when populated): Validated → Updated → Contradicted → New perspectives → New sources → Suggested edits (spec source: `perplexity-refinement/SKILL.md` Phase 3)
- Frontmatter update on the original artifact: `perplexity-refined:`, `perplexity-refined-by:`, `perplexity-refinement-depth:` (spec source: `perplexity-refinement/SKILL.md` Phase 4d)
- Query tally at the bottom of the section: "Queries run: N. Validated: X. Updated: Y. Contradicted: Z. New sources surfaced: W." (spec source: `perplexity-refinement/SKILL.md` Phase 4a)

### Quality dimensions

- **Every claim cites its Perplexity-surfaced URL** (threshold: 100% — this is the load-bearing rule; spec source: `perplexity-refinement/SKILL.md` Source-attribution discipline)
- Citation format matches `[source: perplexity.ai query "<query>" on YYYY-MM-DD, citing <URL>]` (threshold: 100%)
- High-tier claims in the original artifact were actually refined (not low-tier ones in their place) (threshold: pass)
- New sources surfaced are genuinely useful for VIS ingestion (not aggregator articles or rehashes of existing vault content) (threshold: pass on at least one if any surfaced)
- Contradicted claims include counter-evidence summary + recommended-action line (threshold: pass per item)
- Plain-language compliance in the refinement section (threshold: pass)

### Discipline rules

- Non-destructive on the original artifact body (no silent rewrites in inline-merge mode) (spec source: `perplexity-refinement/SKILL.md` critical-behavior)
- Per-claim confirmation visible in inline-merge mode (no batch-apply) (spec source: `perplexity-refinement/SKILL.md` Phase 4b)
- Cap respected: light=3, medium=7, deep=15 queries (spec source: `perplexity-refinement/SKILL.md` Phase 2 caps)
- No silent fallback to Cowork WebSearch when Perplexity Pro is unavailable (spec source: project-level architecture decision 2026-05-27)
- Sister-file mode (when used): file at `<original>-perplexity-refined-YYYY-MM-DD.md` with frontmatter `type: perplexity-refinement` and `refines: <original-filename>` (spec source: `perplexity-refinement/SKILL.md` Phase 4c)

## Cluster synthesis

### Hard requirements

- Frontmatter: `type: synthesis`, `synthesis-shape: cluster`, `status:`, `created:`, `updated:`, `related: [...]`, `tags: [synthesis, cluster, ...]` (spec source: `multi-source-synthesis/SKILL.md` Stage 5 frontmatter)
- Required sections: Executive summary → Pattern math state → Tactical convergences → Tactical divergences → Operator-actionable takeaways → Open questions → Cross-cluster connections (spec source: `multi-source-synthesis/SKILL.md` cluster-synthesis shape)
- Filed at `03_domains/<cluster>/cluster-synthesis-<cluster>-<date>.md` (cluster-folder root, not `insights/`) (spec source: `multi-source-synthesis/SKILL.md` cluster-synthesis destination)
- Every source named in the synthesis body is also in `related:` frontmatter (spec source: `conventions.md` linking rules)

### Quality dimensions

- Pattern-math state is summarized, not promoted (no quiet 2/3 → 3/3 escalation in the synthesis) (threshold: pass; spec source: `multi-source-synthesis/SKILL.md` summarize-don't-promote)
- Contradictions between creators preserved, not papered over (threshold: pass per surfaced disagreement)
- Operator-actionable takeaways are concrete (not "consider exploring X") (threshold: pass)
- Cross-creator attributions are accurate (no claim that creator X said something they didn't) (threshold: 100%)
- Plain-language compliance in the body (threshold: pass — synthesis carries denser prose but conventions still apply)
- Citation density: every claim attributable to a source carries a wikilink to that source (threshold: 90%+)

### Discipline rules

- Non-destructive on cited source notes (the synthesis doesn't rewrite the sources it cites) (spec source: `multi-source-synthesis/SKILL.md` critical-behavior)
- Premature-abstraction avoidance: synthesis doesn't redefine pattern boundaries to make math read cleanly (spec source: `multi-source-synthesis/SKILL.md` pattern-math-state precedent)
- Project-applicability frontmatter fields present (spec source: `intel-routing-skill-spec.md`)
- Slug-only wikilinks (spec source: `conventions.md`)
- Companion artifact path: reading guide via meta-document-primer + optional plain-language sister file (presence is a quality signal, absence is a minor flag)

## Cross-cluster synthesis

### Hard requirements

- Frontmatter: `type: synthesis`, `synthesis-shape: cross-cluster` (spec source: `multi-source-synthesis/SKILL.md`)
- Filed at `_meta/synthesis/cross-cluster-synthesis-<topic>-<date>.md` (spec source: `multi-source-synthesis/SKILL.md`)
- Operator-strategic anchor question named at the top of the synthesis (spec source: `multi-source-synthesis/SKILL.md` cross-cluster shape)
- Required sections: Executive summary → Cluster contributions → Cross-cluster pattern evidence → Tensions and contradictions → Operator-decision space → What this does NOT decide (spec source: `multi-source-synthesis/SKILL.md` cross-cluster shape)

### Quality dimensions

- Anchor question is load-bearing throughout (every section refers back to it) (threshold: pass)
- Decisions are surfaced, not analyzed (the "gated on downstream document" discipline) (threshold: pass; spec source: `multi-source-synthesis/SKILL.md` decision-archaeology)
- Cluster contributions are balanced (no one cluster dominates without reason) (threshold: pass)
- Operator-decision space lists pros + cons + dependencies per option (threshold: pass per surfaced decision)
- Plain-language compliance (threshold: pass)
- Citation density: every claim from each cluster carries a wikilink to a source in that cluster (threshold: 90%+)

### Discipline rules

- Same as cluster synthesis: non-destructive, premature-abstraction avoidance, slug-only wikilinks, project-applicability frontmatter fields

## Research brief (any tier)

### Hard requirements

- Frontmatter: `type: research-brief`, `brief-tier: <tier>`, `status:`, `created:`, `updated:`, `research-date:`, `researcher:`, `tools-used: [...]`, `sources-cited:`, `tags: [research-brief, ...]` (spec source: the tier's template file)
- Every section the template's consumption-contract table feeds is present (spec source: template's "How the scaffolder consumes this brief" table)
- Inline citations per section: `[source: <tool/url> on YYYY-MM-DD]` (spec source: template's citation discipline)
- Sources-cited roll-up section at the end (`§14 Sources cited` for service briefs; equivalent for other tiers)
- Methodology section at the end naming tools used, what's missing, what the brief assumed, refresh trigger

### Quality dimensions

- Citation density: matches or exceeds the template's expected count (typically 10+ for service briefs, 15+ for city briefs, 12+ for intersection briefs)
- Distinct sources cited (not repeated): typically 5+ for service briefs, 10+ for city briefs, 8+ for intersection briefs
- AI-citation hardening checklist items (§4.5 for service briefs) all present or honestly flagged as gaps (threshold: 80%+ honestly addressed)
- Pricing-visibility recommendation matches client policy (estimate-only vs published-pricing) (threshold: pass; spec source: §11 of service-brief template + decision-2026-05-26-no-pricing-on-residential-contractor-core-30-pages)
- Plain-language compliance (threshold: pass)
- Consumption contract honored: every JSON field the scaffolder reads has a matching brief section (threshold: 100% — hard requirement, repeated here as a quality dimension because partial coverage is possible)

### Discipline rules

- Non-destructive on the template (the brief doesn't rewrite the template's section structure) (spec source: `service-seo-research/SKILL.md`)
- AI-citation hardening checklist surfaced honestly (every checkbox either marked pass with evidence or marked gap) (spec source: `_template-service-brief.md` §4.5)
- Honest about gaps (e.g., "GSC not connected — flagged in §15") rather than fabricating coverage (spec source: `service-seo-research/SKILL.md`)

## Tactic / tool / pattern / lesson note

### Hard requirements

- Frontmatter shape per `conventions.md`: `type:`, `status:`, `created:`, `updated:`, `tags:` plus type-specific fields (sources: for tactics/patterns; tool-name: for tools; category: for lessons)
- Filename starts with the correct prefix (`tactic-`, `tool-`, `pattern-`, `lesson-`) (spec source: `conventions.md` § File naming)
- Filed in the correct folder (per conventions § Folder placement)
- At least one outgoing link (parent context + at least one related artifact) (spec source: `conventions.md` § Linking rules)
- For tactics/patterns: cross-creator math accurately stated (1/3, 2/3, 3/3) (spec source: `conventions.md` + `multi-source-synthesis/SKILL.md`)

### Quality dimensions

- Plain-language compliance (threshold: pass)
- Sources cited are accurate (no fabricated attributions) (threshold: 100%)
- Mechanism / how-it-works section is concrete (threshold: pass — for tactics/patterns)
- For tools: pricing and feature claims are time-stamped (threshold: pass; tools go stale fast)
- For lessons: rule + **Why:** + **How to apply:** structure honored (threshold: pass)

### Discipline rules

- Slug-only wikilinks (spec source: `conventions.md`)
- Promotion math: 1/3 patterns don't claim 3/3 evidence; 2/3 patterns don't quietly promote (spec source: `multi-source-synthesis/SKILL.md`)
- Project-applicability frontmatter fields present (spec source: `intel-routing-skill-spec.md`)

## Blueprint

### Hard requirements

- Frontmatter: `type: blueprint`, `status:`, `created:`, `updated:`, `tags: [blueprint, ...]`
- Filed at `05_shared-intelligence/blueprints/blueprint-*.md`
- Required sections: Components → Data flow → Decision points → Open questions
- Every component named in §1 reappears in §2 (data flow)

### Quality dimensions

- Components are concrete (each has a 2-3 sentence description; not just a name)
- Data flow is traceable end-to-end (no orphan components)
- Open questions are real (not rhetorical)
- Citations to vault artifacts that inform the design (threshold: 5+)
- Plain-language compliance (threshold: pass)

### Discipline rules

- Non-destructive on cited artifacts
- Slug-only wikilinks
- No premature commitment to implementation details (blueprints are spec-level)

## SKILL.md (a new skill being evaluated)

### Hard requirements

- Frontmatter opens with `name:` and `description:` fields (the autoinvoke uses these — they're load-bearing) (spec source: existing skill SKILL.md files)
- `description:` field names trigger phrases the autoinvoke listens for (spec source: pattern across existing skills)
- `## Critical behavior` section near the top (spec source: pattern across existing skills)
- `## When to use this skill` section (spec source: pattern across existing skills)
- Workflow described in phases or stages with explicit stop conditions
- `## Reference files` section listing any references the skill carries
- `## See also` section with wikilinks to related skills + conventions

### Quality dimensions

- Description field is specific enough to drive autoinvoke (not "helps with stuff") (threshold: pass)
- Trigger phrases cover the operator's natural phrasings (threshold: 3+ distinct phrasings)
- Critical-behavior section names the non-obvious discipline rules (not just generic "be careful") (threshold: pass)
- Workflow stop conditions are explicit (every phase says when to stop) (threshold: pass per phase)
- Plain-language compliance (threshold: pass)
- Maintenance notes section seeded (threshold: 1+ entry, indicating known failure modes already documented)

### Discipline rules

- Non-destructive on neighbor skills (the new skill doesn't claim authority over things a neighbor skill owns)
- Plain-language compliance (spec source: `plain-language-conventions.md`)
- Cost-management rules named where applicable (spec source: pattern across existing skills using external APIs)

## Core 30 page draft

### Hard requirements

- Frontmatter (if `.md`) or JSON-LD `@graph` block (if `.html`) with required entities
- LocalBusiness + Service + FAQPage schema entities present, linked via `@id` references (spec source: `_template-service-brief.md` §4.5 F)
- TL;DR paragraph at the top (1-2 sentences, stands alone) (spec source: `_template-service-brief.md` §4.5 A)
- Hero section with city-specific heading
- What-it-means paragraphs, problem cards (6-8), process steps (5-7), FAQ block (6-8), about section, related-cards grid
- Key takeaways at the end (3-5 bullets) (spec source: `_template-service-brief.md` §4.5 A)
- AggregateRating in LocalBusiness schema (spec source: `_template-service-brief.md` §4.5 F)

### Quality dimensions

- Attribute density: 3+ named brands per major section (e.g., Federal Pacific, Zinsco, Siemens, Square D for panel-upgrade pages) (threshold: pass per section; spec source: `_template-service-brief.md` §4.5 C)
- Entity richness: 3+ named entities per major section (brands, neighborhoods, code names, permit offices, utility companies) (threshold: pass per section; spec source: §4.5 D)
- Capsule discipline: every FAQ answer's first sentence stands alone if extracted (threshold: pass per FAQ; spec source: §4.5 B)
- Plain-language compliance (threshold: pass; spec source: `plain-language-conventions.md`)
- City-specific specificity: neighborhoods, permit office, utility company named (not "your local utility") (threshold: pass)
- Word count: median of top 10 SERP results +20%, rounded to nearest 200 (threshold: within ±10% of target)
- Primary-source citations: statistics cite .gov / .edu / NFPA / NEC / utility company data (threshold: 100% of statistics)

### Discipline rules

- Pricing-visibility matches client policy (estimate-only for Keelworks residential clients) (spec source: decision-2026-05-26-no-pricing)
- No AI-generated meta titles/descriptions at scale (each hand-tuned) (spec source: §4.5 G)
- No bolt-on PAA-derived FAQ blocks (spec source: §4.5 G)
- No paid-link references in content (HARO/editorial only) (spec source: §4.5 G)
- License jurisdiction appears 2+ times (spec source: §4.5 D)
- Owner name + owner face on the page (differentiation discipline) (spec source: §4.5 D + §8 image-style observations)

## Update path

When a new artifact type appears, add a block here mirroring the structure above:

- Hard requirements
- Quality dimensions
- Discipline rules

Each item cites its spec source. The detection table and routing table update in lockstep.
