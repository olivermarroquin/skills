# Spec routing table

For each artifact type the detector recognizes, this table names the spec sources Mode 1 Phase 2 must load. A spec source is any file (or named section of a file) that defines what "good" looks like for that artifact type.

The routing table is the authoritative map. Don't borrow spec sources from a neighboring type. If a type's row is missing or thin, surface the gap to the operator rather than guessing.

## Path conventions in this file

- `vault://` = `~/workspace/second-brain/` (the vault root)
- `skills://` = `~/workspace/skills/`
- `repos://` = `~/workspace/repos/`

## Routing table

### Core 30 page draft

Spec sources to load:

1. **Service brief** — `vault://05_shared-intelligence/research-briefs/services/<service-slug>.md`
   - Drives: page identity, naming, hero copy, what-it-means paragraphs, problem cards, process steps, pricing pattern, FAQs, schema shape
2. **Intersection brief** — `vault://05_shared-intelligence/research-briefs/intersections/<service-slug>--<city-slug>.md`
   - Drives: city-specific competitive context, top-3 competitor citations, local FAQ wording, neighborhood phrasing
3. **City data file** — `repos://ai-agency-core/scripts/data/cities/<city-slug>.json`
   - Drives: permitting info, utility name, neighborhood list, service-keyed symptoms, ZIP codes
4. **Client data file** — `repos://ai-agency-core/scripts/data/client-<client-slug>.json`
   - Drives: business name, contact info, license number, brand colors, owner bio, trust signals
5. **Plain-language conventions** — `vault://_meta/plain-language-conventions.md`
   - Drives: voice rules, gloss conventions, sentence shape, tone calibration
6. **SEO primer Section G** — `vault://03_domains/seo/primer.md` §G (AI-citation content discipline)
   - Drives: attribute density, entity richness, capsule discipline, primary-source anchoring
7. **AI-citation hardening checklist** — `vault://05_shared-intelligence/research-briefs/_template-service-brief.md` §4.5
   - Drives: TL;DR rule, answer-first rule, key-takeaways rule, capsule discipline items A-G
8. **Per-page ingestion / refinement notes** — auto-grep for source notes citing the page's service or city
   - Drives: spot-check that the page reflects current vault knowledge (anti-staleness)

Notes:

- All eight sources are typically needed; skipping any one weakens the evaluation. If a source is missing (e.g., no intersection brief for the city), surface the gap and proceed with the rest.
- For Core 30 pages produced by `scaffold-core-30-page.py`, the data files (#3, #4) are the contract between the brief and the page. Mismatches between brief and data file surface as discipline-rule violations, not quality dimensions.

### Perplexity-refinement output

Spec sources to load:

1. **perplexity-refinement SKILL.md** — `skills://perplexity-refinement/SKILL.md`
   - Drives: the six Phase-3 bucket shape, citation discipline, non-destructive default, depth caps
2. **Query templates** — `skills://perplexity-refinement/references/query-templates.md`
   - Drives: which template shapes should appear given the source's tiered items (validate-a-claim / validate-a-tool / etc.)
3. **The original source note (pre-refinement)** — auto-locate from frontmatter `refines:` field or by stripping the `-perplexity-refined-YYYY-MM-DD` suffix from the path
   - Drives: what claims were tiered as high-value; whether the refinement actually addressed them
4. **Plain-language conventions** — `vault://_meta/plain-language-conventions.md`
   - Drives: voice rules for the refinement section (same as everywhere)

Notes:

- The load-bearing quality dimension for refinement outputs is **every claim has a citation**. The skill's own discipline section names this as the single rule that justifies the subscription cost.
- The original source note matters because a refinement that produces 12 validations on low-tier claims (while the high-tier claims went un-addressed) is a refinement-quality failure even if every claim cites a URL.

### Cluster synthesis

Spec sources to load:

1. **multi-source-synthesis SKILL.md** — `skills://multi-source-synthesis/SKILL.md`
   - Drives: shape-and-destination discipline, pattern-math-state summarize-don't-promote rule, contradiction-handling, decision-archaeology
2. **Every source note named in the synthesis's `related:` frontmatter** — paths resolved from wikilink slugs
   - Drives: whether the synthesis's claims about each source are accurate and whether the synthesis represents the cluster's actual state
3. **Intel-routing convention spec** — `vault://_meta/specs/intel-routing-skill-spec.md`
   - Drives: applies-to-projects / applies-to-archetypes / applicability-confidence fields on the synthesis frontmatter
4. **Conventions.md synthesis-shape rules** — `vault://_meta/conventions.md` (filename + frontmatter + folder sections)
   - Drives: filename prefix, frontmatter shape, folder placement

Notes:

- Cluster syntheses are operator-strategic-altitude. The evaluation needs to check that the synthesis doesn't drift into source-detail-altitude (re-summarizing each source).
- The cross-creator pattern-math state is load-bearing. Mis-stating 2/3 as 3/3 (or vice versa) is a substantive revision trigger.

### Cross-cluster synthesis

Spec sources to load:

1. **multi-source-synthesis SKILL.md** — `skills://multi-source-synthesis/SKILL.md`
2. **Cluster summaries cited** — 2-3 representative sources per cluster spanned, identified from the synthesis's body
3. **Conventions.md cross-cluster rules** — `vault://_meta/conventions.md`
4. **Plain-language conventions** — `vault://_meta/plain-language-conventions.md`

Notes:

- The operator-strategic anchor question is the load-bearing element. A cross-cluster synthesis without a clear anchor is a substantive revision trigger regardless of how well the cluster evidence is summarized.

### SKILL.md (any new skill)

Spec sources to load:

1. **Conventions.md skills section** — `vault://_meta/conventions.md` (the skill-naming / SKILL.md-shape rules)
2. **2-3 high-quality reference skills as comparison anchors:**
   - `skills://perplexity-refinement/SKILL.md`
   - `skills://multi-source-synthesis/SKILL.md`
   - `skills://house-voice-rewrite/SKILL.md`
3. **Plain-language conventions** — `vault://_meta/plain-language-conventions.md`

Notes:

- The reference skills are anchors, not prescriptions. The evaluation checks the new skill against shape (critical-behavior section, when-to-use, workflow, references, see-also) and voice, not against feature-by-feature parity.
- A new skill's `description:` field is the most-load-bearing detection signal in the system. Evaluate it carefully — vague descriptions cause auto-invocation to misfire.

### Research brief — service / city / intersection / client

Spec sources to load:

1. **The brief's template file:**
   - Service → `vault://05_shared-intelligence/research-briefs/_template-service-brief.md`
   - City → `vault://05_shared-intelligence/research-briefs/_template-city-brief.md`
   - Intersection → `vault://05_shared-intelligence/research-briefs/_template-intersection-brief.md`
   - Client → `vault://05_shared-intelligence/research-briefs/_template-client-brief.md`
2. **The brief's consumption-contract table** — the "How the scaffolder consumes this brief" table at the end of the template
   - Drives: every JSON field that derives from the brief must trace back to a brief section; missing sections are hard-requirement misses
3. **Plain-language conventions** — `vault://_meta/plain-language-conventions.md`

Notes:

- The consumption contract is the load-bearing element for research briefs. If the brief is missing a section that feeds a JSON field, the scaffolder breaks. Hard requirement, not a quality dimension.
- Citation density is a quality dimension — every claim should carry `[source: ...]` per the template's citation discipline.

### Tactic note

Spec sources to load:

1. **Conventions.md artifact rules** — `vault://_meta/conventions.md` (filename prefix `tactic-`, frontmatter, folder placement)
2. **Promotion-threshold rules** — `vault://_meta/conventions.md` (the 1/3, 2/3, 3/3 cross-creator math + premature-abstraction discipline)
3. **Every source cited in the artifact's frontmatter / body** — paths resolved from wikilink slugs
4. **Plain-language conventions** — `vault://_meta/plain-language-conventions.md`

Notes:

- A tactic note at 1/3 or 2/3 has different expectations from a tactic note at 3/3. The promotion-threshold rules say what each tier requires.
- Mis-attributing a creator (claiming Nico endorsed a tactic when he didn't) is a hard-requirement miss, not a quality dimension. Attribution accuracy is non-negotiable.

### Tool note

Spec sources to load:

1. **Conventions.md artifact rules** — `vault://_meta/conventions.md`
2. **Every source cited in the artifact's frontmatter / body** — paths resolved from wikilink slugs
3. **Plain-language conventions** — `vault://_meta/plain-language-conventions.md`

Notes:

- Tool notes go stale fast (pricing changes, features ship). The `last-updated` date is a quality dimension — a tool note that hasn't been touched in 6+ months gets a "staleness" flag.

### Pattern note (cross-source)

Spec sources to load:

1. **Conventions.md artifact rules** — `vault://_meta/conventions.md`
2. **Promotion-threshold rules** — `vault://_meta/conventions.md` (the 1/3, 2/3, 3/3 cross-creator math + premature-abstraction discipline)
3. **Every source cited in the artifact's frontmatter / body**
4. **Plain-language conventions** — `vault://_meta/plain-language-conventions.md`

Notes:

- Same as tactic notes: the promotion math is load-bearing. Pattern notes at 3/3 must have three independent canonical creators; mis-counting is a hard-requirement miss.

### Lesson note

Spec sources to load:

1. **Conventions.md artifact rules** — `vault://_meta/conventions.md`
2. **Every source cited in the artifact's frontmatter / body**
3. **Plain-language conventions** — `vault://_meta/plain-language-conventions.md`

Notes:

- For retros (`category: retro`), the "What went well / What was harder / Patterns discovered" shape is the hard-requirement skeleton.
- For standalone lessons, the rule + why + how-to-apply shape is the hard-requirement skeleton.

### Source note (VIS ingestion)

Spec sources to load:

1. **vis-extraction SKILL.md** — `skills://vis-extraction/SKILL.md`
2. **Source-note conventions** — `vault://_meta/conventions.md` (§ "Source note writing conventions v3.2")
3. **Plain-language conventions** — `vault://_meta/plain-language-conventions.md`
4. **The source URL or transcript file** — for spot-checking claim accuracy (optional; if unreachable, surface the gap and proceed with internal-consistency evaluation only)

Notes:

- The "In plain English" section after Take-away is a hard requirement per conventions §3.2.
- Acronym expansion on first use is a hard requirement, not a quality dimension.

### Blueprint

Spec sources to load:

1. **multi-source-synthesis SKILL.md** — `skills://multi-source-synthesis/SKILL.md`
2. **Every cited artifact in the blueprint's body** — paths resolved from wikilink slugs
3. **Conventions.md blueprint-shape rules** — `vault://_meta/conventions.md`
4. **Plain-language conventions** — `vault://_meta/plain-language-conventions.md`

Notes:

- Blueprints are system-architecture specs. The evaluation checks completeness (every named component has a description) and consistency (the components named in §1 reappear in §3's data-flow section).

## Operator overrides

When the operator runs `quality-check <artifact> against <spec1> <spec2>`, the routing table is bypassed and the operator-named specs are used. Surface the override in the evaluation report so the audit trail names what was actually loaded:

```
**Spec sources loaded:** [<spec1>, <spec2>] (operator override; routing table bypassed)
```

If the override skips a spec the routing table would have loaded, the evaluation still proceeds — the operator gets to decide what counts.

## Update path

When a new artifact type appears, add a row here naming the spec sources to load. The detection table (`artifact-type-detection.md`) and the heuristics file (`evaluation-heuristics-by-type.md`) update in lockstep. Partial updates break the skill.
