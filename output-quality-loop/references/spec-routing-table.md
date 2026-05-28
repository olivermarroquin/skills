# Spec routing table

For each artifact type the detector recognizes, this table names the spec sources Mode 1 Phase 2 must load. A spec source is any file (or named section of a file) that defines what "good" looks like for that artifact type.

The routing table is the authoritative map. Don't borrow spec sources from a neighboring type. If a type's row is missing or thin, surface the gap to the operator rather than guessing.

## Path conventions in this file

- `vault://` = `~/workspace/second-brain/` (the vault root)
- `skills://` = `~/workspace/skills/`
- `repos://` = `~/workspace/repos/`

## Routing table

### Core 30 page draft

Page slug parses as `<service-slug>-<city-slug>` (e.g. `panel-upgrade-fairfax-va`, `panel-upgrade-vienna-va`). Page folder is `<NN>-<page-slug>` under the client's `website-archive/new/core-30/`. The detector reads the slug, the folder name, or the draft's frontmatter (`service:` + `city:` + `client:`) to resolve the three keys (service-slug, city-slug, client-slug) before walking this row.

Spec sources to load (eight required + two optional):

1. **Service brief** (required) — `vault://05_shared-intelligence/research-briefs/services/<service-slug>.md`
   - Discovery: the service-slug from the page slug; if a perplexity-refined sibling exists at `services/<service-slug>-perplexity-refined-YYYY-MM-DD.md`, load it as a supplementary source alongside the canonical brief.
   - Drives: page identity, naming, hero copy, what-it-means paragraphs, problem cards, process steps, pricing pattern, FAQs, schema shape, §4.5 AI-citation hardening checklist (item A-G — TL;DR / answer-first / key-takeaways / capsule discipline / attribute density / entity richness / primary-source anchoring / schema markup / anti-tactics).
   - Missing → hard requirement miss (a page can't be evaluated without its brief).

2. **Intersection brief** (optional) — `vault://05_shared-intelligence/research-briefs/intersections/<service-slug>--<city-slug>.md`
   - Discovery: double-hyphen separator is canonical (per `artifact-type-detection.md` intersection-tier row).
   - Drives: city-specific competitive context, top-3 competitor citations, local FAQ wording, neighborhood phrasing.
   - Missing → flag in the evaluation report (`spec source skipped: no intersection brief for <service>--<city>; city-specificity heuristics will rely on city data only`) and proceed. Not a hard requirement — most Core 30 pages get city-specificity from the city data file. The intersection brief is the depth layer when it exists.

3. **City data file** (required) — `repos://ai-agency-core/scripts/data/cities/<city-slug>.json`
   - Drives: permitting info, utility name, neighborhood list, service-keyed symptoms, ZIP codes, the substitution values the scaffolder feeds into `build_context()`.
   - Missing → hard requirement miss (the scaffolder could not have produced the page without it).

4. **Client data file** (required) — `repos://ai-agency-core/scripts/data/client-<client-slug>.json`
   - Discovery: client-slug from the page folder's parent path (e.g. `clients/_active/<client-slug>/website-archive/...`) or from draft frontmatter `client:` field.
   - Drives: business name, contact info, license number, brand colors, owner bio, trust signals, schema LocalBusiness identity, `{client_name}` / `{phone_display}` / `{owner_name}` / `{license_state}` substitutions.
   - Missing → hard requirement miss.

5. **Plain-language conventions** (required) — `vault://_meta/plain-language-conventions.md`
   - Drives: voice rules, gloss conventions, sentence shape, tone calibration.
   - Missing → surface as a vault-state problem and proceed with the standing `feedback_plain_language_default.md` memory as the fallback rule set.

6. **SEO primer §D — AI-citation hardening tactics** (required) — `vault://03_domains/seo/primer.md` § "Section D — AI-citation hardening tactics"
   - Drives: the named tactics list (capsule-content / attribute-match / entity-optimization / content-freshness / schema-markup / anti-AI-slop) and the cross-references each tactic carries to a `tactic-*.md` file.
   - This replaces the legacy "SEO primer Section G" reference Phase 1 documented. The SEO primer has no Section G; the tactics live in §D. The conceptual companion (next item) is in the marketing primer.
   - Missing → degrade to the per-tactic notes (`tactic-capsule-content-technique-for-ai-citation`, etc.) and surface the primer gap.

7. **Marketing primer §G — Content discipline for AI citation** (required) — `vault://03_domains/marketing/primer-marketing-vocabulary-and-concepts.md` § "Section G — Content discipline for AI citation"
   - Drives: the conceptual basis — pluckable units, capsule-content shape (Nico's framing), attribute density vs keyword stuffing, content freshness cadence, anti-slop discipline, primary-source citation.
   - This is the "what shape your content has to take to get cited" doc the service-brief §4.5 checklist operationalizes. Pairs with item 6.

8. **AI-citation hardening checklist** (required) — `vault://05_shared-intelligence/research-briefs/_template-service-brief.md` §4.5 (subsections A through G)
   - Drives: the actual checklist items the evaluation runs. A = structural patterns (TL;DR / answer-first / key-takeaways); B = capsule-content discipline; C = attribute density; D = entity-rich language; E = primary-source anchoring; F = schema markup; G = anti-tactics avoided.
   - The same checklist appears (operationalized into JSON-field assertions) at the bottom of the panel-upgrade service brief. Whichever is the more-recent canonical version wins on conflict; the template is the spec of last resort.

9. **Per-page ingestion / refinement notes** (auto-discovered) — auto-grep for source notes citing the page's service or city
   - Discovery: `grep -li "<service-slug>\|<service-name>\|<city-name>" vault://03_domains/seo/insights/source-*.md` produces the candidate list. For every source note that hits, also load any sibling refinement output (path matches `<source-stem>-perplexity-refined-YYYY-MM-DD.md` in the same folder, or check the source note's frontmatter `perplexity-refined:` field for the append-mode refinement).
   - Drives: spot-check that the page reflects current vault knowledge. If a refinement output validates a claim and the page contradicts it, the page is stale. Anti-staleness layer.
   - Missing (no source notes mention the service/city) → not a defect; the page just hasn't been informed by VIS ingestions yet.

10. **House-voice personality file** (optional, per-client) — `vault://04_projects/clients/_active/<client-slug>/personality-<client-slug>.md`
    - Discovery: per-client personality file from the house-voice-rewrite skill (Phase 1 of 2026-05-27).
    - Drives: client-voice-match dimension (voice consistency across pages for the same client).
    - Missing → skip the voice-match dimension and note in the report; do not flag as a defect because not every client has had personality init run.

Notes:

- Sources #1, #3, #4 are the contract between the brief and the scaffolder. Mismatches between brief and data file (e.g., brief says pricing is "estimate-only" but the data file embeds a published-pricing block) surface as **discipline-rule violations**, not quality dimensions, because they violate the spec-feeds-scaffolder contract.
- Sources #2, #9, #10 are best-effort. Their absence reduces evaluation depth but does not block the verdict. The evaluation report names every source actually loaded so the audit trail is honest about what depth the evaluation reached.
- Sources #6 and #7 are conceptually overlapping — SEO primer §D names the tactics, marketing primer §G explains the underlying content discipline. Both are loaded because the checklist (source #8) cites both as its parent specs.
- For Core 30 pages produced by `scaffold-core-30-page.py`, the routing assumes the page slug parses cleanly. If the slug doesn't end in a known city-slug or the prefix doesn't match a known service-slug template, surface "spec routing failed: page slug doesn't decompose into known service + city" before attempting evaluation.

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
