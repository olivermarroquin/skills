# Evaluation heuristics by artifact type

Per-type breakdown of hard requirements (must-have for ship), quality dimensions (must-have at threshold), and discipline rules. Mode 1 Phase 3 combines the loaded spec sources with these heuristics to build the checklist.

Each checklist item is one bullet. Each bullet carries a one-line citation to the spec source that defines it.

Each type also has an **Auto-research strategy** subsection used by Mode 4 (AUTO-RESEARCH). The strategy names the characteristic gap shapes for that type and the research-question templates Mode 4 uses to elevate them. All composition routes through Perplexity Pro (via `perplexity-refinement`, per the architecture-decision contract); the strategy specifies WHICH queries to ask, not which research tool to use. Per-type query caps live in `research-budget-per-type.md`.

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

### Auto-research strategy (Mode 4)

**Cap:** 3 queries; top-3 gaps. The source note is already the operator's distillation of one piece of content — Mode 4 triangulates the 2-3 highest-tier extracted claims, not the whole VIS pass. For deeper refinement the operator invokes `perplexity-refinement` directly with `medium`/`deep` depth, which is its own contract.

**Characteristic gap shapes:**

- Tactic / tool / pattern candidates that the source asserts confidently but cites only the creator — Mode 4 asks "what's the strongest published version of [tactic / pattern / tool claim] in current work?"
- Statistics quoted from the source without a primary-source citation — Mode 4 asks "what's the original source of [statistic] and is it still accurate?"
- Cross-references claimed but missing wikilinks — Mode 4 doesn't research these; it flags them for direct vault grep instead

**Compose-with skills:** None at v1. The recursive `perplexity-refinement` call is the only composed skill. Don't promote this strategy beyond triangulation queries; deep refinement is a different operator decision.

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
- Sister-file mode (when used): file at `<original>-perplexity-refined-YYYY-MM-DD.md` with frontmatter `type: perplexity-refinement` and `refines: <original>-filename>` (spec source: `perplexity-refinement/SKILL.md` Phase 4c)

### Auto-research strategy (Mode 4)

**Cap:** 6 queries; top-5 gaps. Recursive composition with `perplexity-refinement` is the load-bearing move here.

**Characteristic gap shapes:**

- High-tier claims in the original artifact that the first refinement pass covered shallowly (one source cited; counter-evidence not surfaced) — Mode 4 asks "what's the counter-position to [claim] in current published work? Surface 3-5 expert viewpoints with citations."
- Claims marked `inconclusive` in the first refinement pass — Mode 4 reformulates with a sharper question shape (e.g., narrowing date range, naming the entity more specifically) and re-asks
- Claims marked `contradicted` where the counter-evidence summary is thin — Mode 4 asks "what's the strongest version of the counter-argument for [claim]?"

**Compose-with skills:** Recursive call to `perplexity-refinement` is mandatory; depth defaults to `light` (3-query cap) for the recursive call so the combined run (6 + 3 = 9) stays under the type's 6-query Mode 4 cap (recursive `light` calls reuse the parent cap; they don't add to it). For deeper triangulation on a single high-stakes gap, the operator can override the recursive depth to `medium` per-gap; that single gap then consumes more of the parent cap.

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

### Auto-research strategy (Mode 4)

**Cap:** 6 queries; top-5 gaps. The premature-abstraction edge is where Mode 4 earns its keep on syntheses.

**Characteristic gap shapes:**

- Cluster claims with fewer than 3 sources cited (the premature-abstraction discipline edge per `multi-source-synthesis/SKILL.md` summarize-don't-promote) — Mode 4 asks "what current published work covers [claim]? Surface 3-5 sources triangulating the claim from independent creators."
- Operator-actionable takeaways that read as generic ("consider exploring X") — Mode 4 asks "what's the strongest published recommendation for [takeaway topic]? Surface concrete actions other practitioners have published."
- Contradictions between creators flagged but not adjudicated — Mode 4 asks "which position has stronger evidence in current published work — [position A] or [position B]?"
- Cross-cluster connections asserted but unsourced — Mode 4 asks "what published work has explored the connection between [cluster A topic] and [cluster B topic]?"

**Compose-with skills:** `multi-source-synthesis` review-agent mode (when shipped) for additional pattern-math triangulation on the cluster's 1/3 → 2/3 → 3/3 promotion math. Until shipped, Mode 4 stays in the Perplexity-only path and surfaces the missing review-agent composition as a known limitation in the folder log.

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

### Auto-research strategy (Mode 4)

**Cap:** 8 queries; top-5 gaps. Higher cap than cluster synthesis — cross-cluster spans more topics and the anchor question benefits from broader triangulation.

**Characteristic gap shapes:**

- The anchor question itself, asked of current published work — Mode 4 asks "what current published work addresses [anchor question]? Surface 3-5 frameworks or recommendations."
- Operator-decision-space options listed without pros/cons — Mode 4 asks "what are the trade-offs of [option X] vs [option Y] per current published work?"
- "What this does NOT decide" section that hides actual unknowns — Mode 4 asks "what current published work has resolved [topic the synthesis explicitly leaves open]?"

**Compose-with skills:** Same as cluster synthesis — `multi-source-synthesis` review-agent mode when shipped, Perplexity-only until then.

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

### Auto-research strategy (Mode 4)

**Cap:** 5 queries; top-3 gaps. Briefs already came out of a research-heavy producing skill — Mode 4 closes specific named gaps, not the whole spec.

**Characteristic gap shapes:**

- Sections marked "operator follow-up pending" — Mode 4 asks the question the section names, directly
- Sections marked "AI surfaces not reachable from Cowork" — those gaps are now reachable through Perplexity Pro, so Mode 4 asks them ("what is [topic] currently per [AI surface name]?"). This is a high-leverage gap shape; the producing skill deferred them as unreachable but Mode 4 closes them automatically.
- AI-citation hardening checklist items marked as gap rather than pass-with-evidence — Mode 4 asks for the missing evidence ("what's the canonical published example of [checklist item topic] for [city / service / intersection]?")
- Pricing-visibility decisions where the brief flagged the policy but didn't cite the source — Mode 4 asks "what's current best practice for pricing visibility on [client type] residential pages?"

**Compose-with skills:** For service briefs: optional composition with `service-seo-research` if that skill ships a "refresh" mode. For city briefs: optional composition with `city-base-research` refresh mode. For intersection briefs: optional composition with `intersection-research` refresh mode. For client briefs: optional composition with `client-fact-research` refresh mode. At v1 these refresh modes don't exist; Mode 4 stays Perplexity-only.

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

### Auto-research strategy (Mode 4)

**Cap:** 3 queries; top-2 gaps. Small artifacts; don't over-research.

**Characteristic gap shapes:**

- Tactic / pattern claim with only 1-2 cited sources — Mode 4 asks "what other current published work covers [tactic / pattern]? Surface 2-3 sources for promotion math."
- Tool note where pricing or feature claims aren't time-stamped — Mode 4 asks "what's the current pricing and feature set of [tool] in 2026?"
- Lesson where rule + **Why** + **How to apply** is present but the **Why** is thin — Mode 4 asks "what current published work justifies [lesson rule]?"

**Compose-with skills:** None at v1. If more queries are warranted, the operator promotes to a full `perplexity-refinement` run on the note directly.

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

### Auto-research strategy (Mode 4)

**Cap:** 8 queries; top-5 gaps. Blueprints are high-leverage architectural artifacts; the cap matches Core 30 pages.

**Characteristic gap shapes:**

- Components asserted without primary-source backing — Mode 4 asks "what's the canonical published implementation of [component] in [domain]?"
- Data-flow edges where the mechanism isn't cited — Mode 4 asks "what's the standard mechanism for [edge] in current published architectures?"
- Decision points listed without trade-off analysis — Mode 4 asks "what are the published trade-offs of [decision-point options]?"
- Open questions that have actually been answered in current published work — Mode 4 asks the question directly

**Compose-with skills:** When `perplexity-blueprint-research` (Wave 2) ships, that skill becomes the primary composer for blueprint Mode 4 runs (it's purpose-built for blueprint research at 30-50 query depth). Until then Mode 4 stays in the standard Perplexity-only path.

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

### Auto-research strategy (Mode 4)

**Cap:** 4 queries; top-3 gaps. Skill-design literature returns diminishing returns past ~4 queries.

**Characteristic gap shapes:**

- Workflow phases without explicit stop conditions — Mode 4 asks "what's the canonical published pattern for stop conditions in [workflow phase topic]?"
- Critical-behavior items that name a discipline without citing a source for it — Mode 4 asks "what's the published precedent for [discipline]?"
- Trigger phrases that may miss common operator phrasings — Mode 4 asks "what are the natural-language phrasings users actually type when they want [skill purpose]?" (this draws on agent-skill design literature)
- Maintenance notes section with zero entries — Mode 4 asks "what published failure modes are common for skills in this space?" and seeds 1-2 candidate maintenance notes

**Compose-with skills:** None at v1. Perplexity Pro queries about skill-design literature, agent-skill conventions, related work in the agent-orchestration space.

## Core 30 page draft

The Core 30 page is the highest-stakes artifact type the routing supports — pages get published to live client sites where ranking + AI-citation outcomes compound over months. The hard-requirement bar is correspondingly tight: schema validity, placeholder resolution, and section completeness are non-negotiable. Quality dimensions cover the §4.5 AI-citation hardening checklist + the plain-language layer + citation density to vault sources. Discipline rules cover scaffolder-contract integrity (substitution-map honesty, no invented facts).

### Hard requirements

- **Frontmatter present and well-formed on the `.md` companion** — `client:`, `page-slug:`, `target-url:`, `target-keyword:`, `service:`, `city:`, `core-30-position:`, `tags:` all present (spec source: `_template-service-brief.md` §6 + scaffolder's `render_markdown()` output contract)
- **All FILL placeholders resolved** — no `FILL:`, `TODO:`, `XXX:`, or `NEEDS_AUTHORING:` markers anywhere in the HTML body or markdown draft. The scaffolder may have written placeholders for data fields the brief didn't fill; the page can't ship with any of them left behind. (spec source: `scaffold-service-data.py` `needs_authoring` field convention)
- **All `{placeholder}` substitutions resolved** — no orphan `{xyz}`, `{city_name}`, `{client_name}`, etc., anywhere in the rendered HTML or markdown. Run `grep -E '\{[a-z_]+\}' draft-v1-WP-WRAPPED.html` — must return zero matches. (spec source: `scaffold-core-30-page.py` `build_context()` substitution map)
- **JSON-LD validates** — exactly three entities in `@graph`: `LocalBusiness` + `Service` + `FAQPage`, each with `@id` references that resolve. JSON parses cleanly; required schema-org fields present. (spec source: `_template-service-brief.md` §4.5 F + `publish-core-30-page.py` `validate_jsonld()`)
- **AggregateRating in LocalBusiness schema** — `ratingValue`, `reviewCount`, `bestRating`, `worstRating` all populated from `client-<slug>.json` `review_rating` and `review_count` (spec source: `_template-service-brief.md` §4.5 F)
- **LocalBusiness + Service + FAQPage entities linked via `@id`** — Service block references `{client_website_url}#business`; FAQPage references `{page_url}#faq`. No dangling references. (spec source: `_template-service-brief.md` §4.5 F)
- **Required section skeleton present** — TL;DR paragraph at the top (1-2 sentences, stands alone); hero section with city-specific heading; what-it-means paragraphs; problem cards (6-8); process steps (5-7); FAQ block (6-8); about section; key takeaways at the end (3-5 bullets); related-cards grid (spec source: `_template-service-brief.md` §4.5 A + §10 page structure)
- **Word count within ±10% of target** — target = median of top-10 SERP results +20%, rounded to nearest 200. For panel-upgrade/troubleshooting/EV-charger pages on EV Electric's site, target is ~2,500 words per `target-word-count:` frontmatter. (spec source: SEO primer §E.5 "Word-count target — 2,000-2,400, not 3,500-4,000" + per-page frontmatter)

### Quality dimensions

- **Capsule-content discipline** — every FAQ answer's first sentence stands alone if extracted; ~70% of body content follows H2-as-question + answer-in-first-sentence shape (threshold: 100% on FAQ first sentences, pass overall on body sections; spec source: `_template-service-brief.md` §4.5 B + marketing primer §G "Capsule Content Technique"). **High-stakes dimension** — a single fail here flips an otherwise-PASS verdict to NEEDS REVISION (substantive) per `verdict-rollup-thresholds.md`.
- **Attribute density** — 3+ named brands per major section (e.g., Federal Pacific, Zinsco, Siemens, Square D for panel-upgrade pages); time qualifiers ("same-day", "weekday morning") + service-area cities + customer-language phrasings (threshold: pass per major section; spec source: `_template-service-brief.md` §4.5 C + SEO primer §D)
- **Entity richness** — 3+ named entities per major section (brands, neighborhoods, code/article names, permit offices, utility companies); owner name in about section + alt text; county references in service-area copy; license jurisdiction phrase (e.g., "Master Electrician licensed in Virginia") appears 2+ times on the page (threshold: pass per major section + ≥2 license-jurisdiction mentions; spec source: §4.5 D)
- **TL;DR + key-takeaways structure** — TL;DR (1-2 sentences) renders at the top; key-takeaways block (3-5 self-contained bullets) renders at the bottom; both stand alone if extracted (threshold: pass both; spec source: §4.5 A)
- **Schema-checklist compliance** — every checkbox in §4.5 F passes: LocalBusiness AggregateRating, Service areaServed + termsOfService, FAQPage mainEntity wraps each Q&A exactly, all three @type entities linked via @id (threshold: 100% of checklist items; spec source: `_template-service-brief.md` §4.5 F)
- **Anti-tactics avoidance** — no AI-generated meta at scale (each title/description hand-tuned per page), no bolt-on PAA-derived FAQ blocks, no paid-link references in content, no more than ~30 pages in the services × locations matrix per the cluster discipline (threshold: pass; spec source: §4.5 G + SEO primer §D anti-tactics)
- **Citation density to vault** — ≥10 inline citations to source notes + refinement outputs (the per-page ingestion notes loaded by routing item #9). Format: wikilinks to source notes in the SEO insights folder, or footnote-style references to refinement-output sister files. (threshold: 10+ citations from the body to vault sources; spec source: SEO primer §D + intel-routing convention)
- **Plain-language compliance** — body prose reads conversationally per `_meta/plain-language-conventions.md`. Short sentences, "you/your" voice in customer-facing sections, no jargon-density without inline gloss. (threshold: ≥85% of body paragraphs honor the conventions; spec source: `plain-language-conventions.md`)
- **Primary-source citations** — every statistic cites a primary source (.gov, .edu, NFPA, NEC article number, utility company data) — not aggregator articles. The `dateModified` schema field carries a current timestamp; the page visibly shows a recency cue (threshold: 100% of statistics; spec source: §4.5 E + SEO primer §D content-freshness)
- **Meta-vs-body consistency (D-09 fix, 2026-06-06)** — extract response-time claims (e.g., "20-30 minutes", "same-day"), pricing claims (e.g., "starting at $X", "free estimates"), and credential claims (e.g., "Master Electrician", "licensed in Virginia") from BOTH the body HTML AND the `aioseo_description:` / `aioseo_page_title:` frontmatter fields. Flag any divergence between the two. A body edit that changes a claim MUST be reflected in the meta description — the meta is what Google shows in SERPs and AI surfaces cite. A desync means the SERP snippet contradicts the page content. (threshold: 100% consistency on response-time + pricing + credential claims; spec source: D-09 calibration defect from S&H wave-2 build 2026-06-06 — quality-loop fixed "45 minutes" to "20-30 minutes" in body but left "45-min response" in meta description, which went live and required post-publish REST API fix)
- **City-specific specificity** — neighborhoods named (not "your area"), permit office named (not "your local permit office"), utility company named (e.g., "Dominion Energy" not "your power company), county references present (threshold: pass; spec source: §4.5 D + city data file consumption contract)

### Discipline rules

- **Non-destructive editing of the draft body** — the quality-loop never edits the draft HTML or markdown body. It updates `last-verdict:` + `last-evaluated:` + `quality-log:` frontmatter only. Producing chats own body revisions. (spec source: `SKILL.md` § Critical behavior)
- **No invented facts** — every claim about pricing, brands, permits, code references, neighborhoods, utility companies, response times, or owner credentials traces to a named source: the service brief, the city data file, the client data file, the intersection brief (if present), or a vault source note (per routing item #9). If a fact is in the HTML body but not in any spec source, flag it as invented. (spec source: `vis-extraction/SKILL.md` no-fabricated-citation principle + scaffolder spec-feeds-contract)
- **Substitution-map honesty** — every `{client_name}`, `{city_name}`, `{owner_name}`, `{phone_display}`, etc., resolves to the value in `client-<slug>.json` / `city-<slug>.json` exactly. No silently substituted defaults, no client-A name appearing on client-B's page. (spec source: `scaffold-core-30-page.py` `build_context()`)
- **Pricing-visibility matches client policy** — estimate-only for Keelworks residential clients per the 2026-05-26 decision; no published price grids in the body for residential-electrical clients (spec source: `decision-2026-05-26-no-pricing-on-residential-contractor-core-30-pages` + service brief §11)
- **License jurisdiction discipline** — license jurisdiction phrase (e.g., "Master Electrician licensed in Virginia") appears at minimum twice on the page in distinct sections (spec source: `_template-service-brief.md` §4.5 D)
- **Owner identity discipline** — owner name appears in the about-section paragraphs AND the alt text of the owner portrait. Owner face image present (or placeholder marked clearly with `needs_authoring`). (spec source: §4.5 D + §8 image-style observations + client data file `owner_name` field)
- **Per-page meta hand-tuning** — `aioseo_meta_description` and `aioseo_page_title` are not the scaffolder's default template output without per-page calibration. They carry the page's specific value proposition, the target keyword phrasing, and the calibrated character counts. (spec source: §4.5 G anti-AI-meta-at-scale rule)
- **No bolt-on PAA-derived FAQ blocks** — FAQs are authored from the brief's §4d "questions our page must answer" list, not scraped from "people also ask" data and answered generically. (spec source: §4.5 G + SEO primer §D anti-tactics)

### High-stakes dimensions (verdict-elevation flags)

Per `verdict-rollup-thresholds.md` § "high-stakes dimension at fail" rule, the following Core 30 dimensions elevate the verdict regardless of overall percentage:

- **Capsule-content discipline at fail** → at minimum NEEDS REVISION (substantive). Capsule discipline is the page's reason for ranking + getting cited; a fail here means the page won't perform even if everything else is clean.
- **Substitution-map honesty at fail (e.g., a wrong client name on the page)** → FAIL. A page published with another client's name is a load-bearing trust violation, not a polish concern.
- **No invented facts at fail (a fabricated brand / code / permit reference)** → FAIL. Fabrication on a published page is a published-misinformation risk.
- **Schema-checklist compliance at fail** → at minimum NEEDS REVISION (substantive). Schema is what AI engines parse to attribute citations; a fail here means the page is structurally invisible to the AI-search layer it's optimized for.

### Auto-research strategy (Mode 4)

**Cap:** 8 queries; top-5 gaps. The highest-stakes artifact type — per-page rank + AI-citation outcomes compound over months, so the cap matches the stakes. The page-level gap shapes are the most diverse in the routing table.

**Characteristic gap shapes:**

- **Cost ranges where the brief doesn't cite a primary source** — Mode 4 asks "what's the current published price range for [service] in [city / county] as of 2026? Surface 3-5 cited examples."
- **Schema patterns where the JSON-LD validates but the field shapes feel templated** — Mode 4 asks "what's the canonical current Schema.org pattern for [LocalBusiness / Service / FAQPage] entities being cited by AI search? Surface examples from currently-cited pages."
- **FAQ depth and attribute density where the page hits the minimum but feels thin** — Mode 4 asks "what's the highest-attribute-density published version of [service] in [city] currently ranking? Surface 3-5 examples with capsule-content shape analysis."
- **Anti-tactics avoidance where the page might be drifting into AI-generated-meta-at-scale or PAA-derived FAQ blocks** — Mode 4 asks "what's the strongest published approach to [meta-description / FAQ authoring] that AI search rewards in 2026?"
- **Citation density where the page cites fewer than 10 vault sources** — Mode 4 asks "what's the strongest published version of [page topic] in current work? Surface 3-5 primary-source candidates Mode 4 can add to the page."
- **Plain-language compliance where the page is dense but could be more conversational** — Mode 4 doesn't research this; it's a vault-internal discipline. Mode 4 skips plain-language gaps and lets the standard `plain-language-translation` skill handle them.

**Compose-with skills:** `competitor-deep-research` for SERP-level comparison (the skill that runs the per-page audit against top-10 ranking competitors and identifies the patterns the top-rankers use that the artifact misses). After Phase 5's convention rollout reaches `competitor-deep-research`, its own research step uses Perplexity Pro — those queries count against the per-artifact 8-query cap.

**Special-case high-stakes path:** If the EVALUATE pass flagged a high-stakes dimension at fail (capsule-content, substitution-map, invented facts, or schema-checklist), Mode 4 prioritizes that gap first. The first 1-2 queries go to the high-stakes gap; remaining budget covers the top-N of the other gaps. The folder log's `### External research (Mode 4)` block names the high-stakes gap first.

## Code artifact (executable source)

**Evidence-based (v1.4, 2026-06-18):** every check below traces to a real catch in `[[_review-gate-catch-register]]` that a producer's self-review missed and the independent peer-review caught (firing-tracker, 2026-06-18). Apply the **baseline** to ALL code; add the one **shape** block that matches.

### Hard requirements (all code)

- **It builds / compiles / imports clean** — `tsc` / `next build` / `python -c "import ..."` passes; no syntax or type errors. (spec source: repo tests + RGH-7 routing)
- **Tests exist and pass ON DISK** — run them and paste the count. "I ran it" / "tested" without the output is a D-05 self-claim (CR-016/017). No tests on a state-writing or gate artifact = hard miss.
- **No dead code left by a refactor** — every function is reachable; a removed path leaves no orphan (CR-016: dead `fetchRemoteEtags`).
- **No placeholders / secrets / hardcoded client values** — no TODO/FIXME/FILL, no committed keys, no single client's data baked into a reusable tool (reuse rule).

### Quality dimensions (all code)

- **Run-it-and-diff, don't read-it** — execute the thing and compare the actual result to what the comment / log claims. "Described-as-demonstrated" is a structural blind spot same-context review cannot see (CR-016/017).
- **Error handling** — failure paths return / throw correctly; no silent swallow.
- **Plain-language comments, logs, and error messages.**

### Shape — state-writing service (route handler / connector / ingestion / migration)

- **Idempotency** — running it twice changes nothing the second time; no full re-write every run (CR-017: all 436 files re-upserted each run).
- **Write-correctness** — update / delete WHERE-clauses target the right rows; a soft-delete actually filters deleted rows on read (CR-018: un-delete bug — WHERE checked etag, not the deleted flag).
- **Migration integrity** — the migration journal / snapshot exists and the pipeline applies cleanly end-to-end (CR-016: missing Drizzle journal = broken pipeline).

### Shape — verification / gate engine

- **Adversarial escape-hatch probe** — try to BYPASS it: poison the inputs, pass the bypass flags, hit the boundaries (CR-011/012: history-file poisoning + flag-heuristic bypass — two gate bypasses the producer's reviewer missed).
- **Test on data DIFFERENT from what the author used** — same-test-data bias hides input-specific defects (CR-019: 36% of cities broke; the author tested only the one city that had all fields).
- **Real-runner test, not simulated** — the test exercises the real entry point, not a mock harness (CR-004: every v1 gate bug reached live sessions because tests ran against a simulated harness).

### Discipline rules

- **Reuse RGH-7's OC-12..16 where they apply (`$0`); do not reimplement** the deterministic checks by LLM.
- **Count claims are globbed from disk, never estimated** (CR-020/023: producers estimate counts; same-context reviewers confirm the estimate).
- **Non-destructive:** no silent behavior change to an existing public interface without surfacing it.

### Auto-research strategy (Mode 4)

**Cap:** 4 queries; top-3 gaps (lower than content types — most code quality is verifiable on disk, not researched). Characteristic gap shapes: an unfamiliar framework's idempotency / migration idiom (e.g. "what is the canonical idempotent-upsert pattern for <ORM> as of 2026?"), or a security boundary on a gate artifact ("known bypass classes for <auth/gate pattern>"). **Compose-with:** the `gate-peer-reviewer` independent-reviewer mandate (Phase C adversarial disciplines) governs HOW the reviewer probes; this skill defines WHAT good looks like. Add the matching row to `research-budget-per-type.md`.

## Update path

When a new artifact type appears, add a block here mirroring the structure above:

- Hard requirements
- Quality dimensions
- Discipline rules
- Auto-research strategy (Mode 4)

Each item cites its spec source. The detection table and routing table update in lockstep. The Auto-research strategy section names the type's characteristic gap shapes + the research-question templates + any compose-with skills; also add a corresponding row to `research-budget-per-type.md`.
