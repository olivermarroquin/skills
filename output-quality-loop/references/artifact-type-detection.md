# Artifact type detection table

The Mode 1 Phase 1 detector walks this table top-to-bottom and picks the most-specific match. Detection signals are: (a) the artifact's filesystem path, (b) its YAML frontmatter, (c) its content shape (key headings or markers in the body).

Each row carries three columns: **artifact type** (the canonical name the routing table uses), **detection signals** (what to look for), and **disambiguation notes** (how to resolve ties when more than one row matches).

## Detection table

### Core 30 page draft

- **Path pattern:** `**/website-archive/new/core-30/**/draft-*.{html,md}`, or `**/04_projects/clients/_active/<client>/website-archive/new/core-30/**/draft-*`
- **Frontmatter:** typically none for raw HTML; `.md` drafts carry `type: page-draft` or `type: core-30-page` if present
- **Content shape:** opens with hero markup or `<!DOCTYPE html>`; embedded JSON-LD `@graph`; service-keyed sections; FAQ block
- **Disambiguation:** If the file is `.md` with frontmatter `type: research-brief`, it's a brief, not a page draft. Page drafts almost always live under `website-archive/`.

### Perplexity-refinement output (sister-file mode)

- **Path pattern:** `**/*-perplexity-refined-YYYY-MM-DD.md`
- **Frontmatter:** `type: perplexity-refinement`, `refines: <original-filename>`, `refined-by: perplexity-refinement-skill-v1`
- **Content shape:** six Phase-3 buckets (Validated / Updated / Contradicted / New perspectives / New sources / Suggested edits)
- **Disambiguation:** sister-file mode is the easy case. Append-mode is detected via the original artifact (next row).

### Perplexity-refinement output (append-mode, embedded in source note)

- **Path pattern:** `**/insights/source-*.md` OR any artifact with `perplexity-refined:` in frontmatter
- **Frontmatter:** `perplexity-refined: YYYY-MM-DD` field present (any value indicates a refinement has been appended)
- **Content shape:** a `## Perplexity refinement — YYYY-MM-DD` section near the bottom (above `## Related` if present)
- **Disambiguation:** the artifact is **both** a source note (or whatever it originally was) AND carries a refinement. When evaluating, the operator usually means the refinement; if ambiguous, ask which axis to evaluate.

### Cluster synthesis

- **Path pattern:** `**/cluster-synthesis-*.md`, typically `03_domains/<cluster>/cluster-synthesis-<cluster>-<date>.md`
- **Frontmatter:** `type: synthesis`, `synthesis-shape: cluster`
- **Content shape:** "Pattern math state" or "Pattern landscape" section; "Tactical convergences" / "Tactical divergences"; "Operator-actionable takeaways"
- **Disambiguation:** if the filename is `pattern-synthesis-*`, it's a pattern synthesis (next row).

### Pattern synthesis

- **Path pattern:** `**/05_shared-intelligence/patterns/pattern-synthesis-*.md`
- **Frontmatter:** `type: synthesis`, `synthesis-shape: pattern`
- **Content shape:** "Pattern definition," "Cross-creator evidence summary," "Mechanism analysis," "Variants and sub-patterns"
- **Disambiguation:** distinct from `pattern-*.md` (which is the tactic-note-shaped pattern). Synthesis carries the longer-form archaeology.

### Cross-cluster synthesis

- **Path pattern:** `_meta/synthesis/cross-cluster-synthesis-*.md`
- **Frontmatter:** `type: synthesis`, `synthesis-shape: cross-cluster`
- **Content shape:** operator-strategic anchor question at top; "Cluster contributions" section; "Tensions and contradictions"; "Operator-decision space"
- **Disambiguation:** the `_meta/synthesis/` location is the strongest signal. Phase artifacts using the grandfathered `phase-<id>-synthesis-` prefix also match here.

### Client-driven synthesis

- **Path pattern:** `04_projects/clients/_active/<client-slug>/client-synthesis-*.md`
- **Frontmatter:** `type: synthesis`, `synthesis-shape: client-driven`, `client: <client-slug>`
- **Content shape:** "Client context summary," "Evidence base used," "Tactical recommendations," "Sequencing"

### SKILL.md (any skill in `~/workspace/skills/`)

- **Path pattern:** `~/workspace/skills/*/SKILL.md` (exactly one segment between `skills/` and `SKILL.md`)
- **Frontmatter:** opens with `name:` and `description:` fields (no `type:` field — skills use a different frontmatter shape)
- **Content shape:** `## Critical behavior`, `## When to use this skill`, workflow sections, `## Reference files`, `## See also`
- **Disambiguation:** distinct from reference files inside a skill's `references/` subfolder, which are evaluated against the same shape but with lighter weight.

### Research brief — service tier

- **Path pattern:** `**/research-briefs/services/*.md` (excluding `_template-service-brief.md` which is the template, not a brief)
- **Frontmatter:** `type: research-brief`, `brief-tier: service`, `service-slug: <slug>`
- **Content shape:** 15 numbered sections from "Service identity and naming" through "Methodology"; "How the scaffolder consumes this brief" table at the end

### Research brief — city tier

- **Path pattern:** `**/research-briefs/cities/*.md`
- **Frontmatter:** `type: research-brief`, `brief-tier: city`, `city-slug: <slug>`, `state: <abbr>`
- **Content shape:** 12 numbered sections; permitting + utility + neighborhoods data; service-specific data deferred to intersection briefs

### Research brief — intersection tier

- **Path pattern:** `**/research-briefs/intersections/<service>--<city>.md` (double-hyphen separator is the locked convention)
- **Frontmatter:** `type: research-brief`, `brief-tier: intersection`, `service-slug: <slug>`, `city-slug: <slug>`
- **Content shape:** 8 numbered sections; "Top 3 city-specific competitors" with per-competitor tables; consumption-contract table at the end

### Research brief — client tier

- **Path pattern:** `**/research-briefs/clients/<client-slug>/brief.md` (per-client subfolder convention)
- **Frontmatter:** `type: research-brief`, `brief-tier: client`, `client-slug: <slug>`
- **Content shape:** 14 numbered sections; business profile, ICP, offer architecture, sequencing rules, open questions

### Tactic note

- **Path pattern:** `**/03_domains/**/tactics/tactic-*.md` or `**/05_shared-intelligence/patterns/tactic-*.md` (legacy location)
- **Frontmatter:** `type: tactic`, `status: <draft|extracted|promoted|validated>`, `sources: [...]`
- **Content shape:** "Mechanism" or "How it works" section; "Sources" or "Cross-creator evidence" section; "Promotion math"

### Tool note

- **Path pattern:** `**/05_shared-intelligence/tools/tool-*.md`
- **Frontmatter:** `type: tool`, `tool-name: <name>`, `category: <category>`
- **Content shape:** "What it does," "Pricing," "Where I learned of it," "Used by" or "Mentioned in"

### Pattern note (cross-source pattern, not the synthesis)

- **Path pattern:** `**/05_shared-intelligence/patterns/pattern-*.md` (excluding `pattern-synthesis-*` which matched earlier)
- **Frontmatter:** `type: pattern`, `times-observed: N`, `confidence: <high|medium|low>`
- **Content shape:** "Problem this solves," "Steps" or "Mechanism," "Key decisions embedded," "Dependencies & prerequisites"

### Lesson note

- **Path pattern:** `**/05_shared-intelligence/lessons/lesson-*.md`
- **Frontmatter:** `type: lesson`, `category: <retro|standalone|other>` (retros are a subset of lessons)
- **Content shape:** for retros, the "What went well / What was harder / Patterns discovered / What to carry forward" shape; for standalone lessons, the rule + why + how-to-apply shape

### Source note (VIS ingestion output)

- **Path pattern:** `**/insights/source-*.md` (typically `03_domains/<domain>/insights/source-*`)
- **Frontmatter:** `type: source`, `source-type: <video|article|tutorial>`, `url:`, `creator:`, `published:`
- **Content shape:** "Take-away," "In plain English," "Tools mentioned," "Workflow breakdown," "Strategy extraction," "Tactic candidates," "Pattern candidates"
- **Disambiguation:** if the source note also carries `perplexity-refined:` in frontmatter, both the source-note row AND the perplexity-refinement-append row apply. Ask the operator which axis to evaluate; default to source-note if ambiguous.

### Blueprint

- **Path pattern:** `**/05_shared-intelligence/blueprints/blueprint-*.md`
- **Frontmatter:** `type: blueprint`, `status: <draft|promoted|validated>`
- **Content shape:** architecture spec; "Components," "Data flow," "Decision points," "Open questions"

## Multi-match resolution

When more than one row matches:

- **Most-specific path pattern wins.** A row whose pattern names a folder (e.g., `**/research-briefs/services/*.md`) wins over a row whose pattern is generic (e.g., `**/*.md`).
- **Frontmatter `type:` field is the tiebreaker.** Path patterns can collide; the frontmatter `type:` is canonical.
- **Content shape is the last resort.** If two rows would match on path and frontmatter, the body markers decide.

When the artifact carries multiple identities (e.g., a source note with an appended refinement), evaluate the most-specific routed identity by default and **note the secondary identity in the evaluation report**. The secondary identity's spec sources may contribute checklist items even if they don't drive the verdict.

## No match

If no row matches:

1. Surface to the operator: "Unable to detect artifact type. Path: `<path>`. Frontmatter `type:` field: `<value or missing>`. Content shape: `<observed markers>`. Tell me the type or extend this table with a row covering this shape."
2. Don't guess. Don't pick the nearest-neighbor row.
3. If the operator names a type, run Mode 1 with that type. Optionally propose a routing-table extension for future runs.

## Update path

When new artifact types appear in the vault, add a row here:

1. Name the type (kebab-case, descriptive).
2. Document detection signals (path / frontmatter / content shape).
3. Add disambiguation notes if the new type could collide with an existing row.
4. Add a matching row to `spec-routing-table.md` naming the spec sources to load.
5. Add a matching block to `evaluation-heuristics-by-type.md` describing the hard requirements, quality dimensions, and discipline rules for the new type.

All three updates land together; partial updates break the skill.
