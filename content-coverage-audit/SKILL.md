---
type: skill
skill: content-coverage-audit
version: 1.0
status: active
created: 2026-06-17
updated: 2026-06-18
substrate: claude-code
reusability: reusable-as-is
domains: [content-quality, research-coverage, gap-analysis]
composes-with: [gate-peer-reviewer, client-seo-onboarding, prioritization, output-quality-loop]
tags: [skill, content-coverage-audit, agnostic, three-lens, utilization, coverage-gaps, expansion, engine-plus-profiles]
---

# content-coverage-audit — skill definition (v1.0)

**Purpose:** Given a body of source material and a set of output artifacts, audit how well the source is converted into the output — surfacing unused research, uneven coverage, and expansion opportunities. Domain-agnostic engine; all source→output mapping lives in **profiles**.

**Origin:** Operator-directed 2026-06-07 during EV Core 30 peer review. The manual analysis ("what research do we have, how much is the output using, what new sections could we generate?") caught two real gaps — this skill automates that analysis for every future build.

## 1. Engine overview

The engine runs **three lenses** against any (source-set, output-set, profile) triple:

| Lens | Question answered | Output |
|------|-------------------|--------|
| **L1 — Utilization** | What source data is consumed vs. sitting unused? | Per source-field: referenced in any output? List of unused fields with richness score |
| **L2 — Coverage gaps / asymmetry** | Where is the output thinner than the source could support? | Per output-variant: source depth comparison. Which variants are under-fed, by which missing source fields |
| **L3 — Expansion opportunities** | What new sections / artifacts could the existing source justify? | Ranked expansion backlog: new sections, new data bindings, new artifact types — each with supporting-evidence citation |

**Zero domain logic in the engine.** The engine knows about source-fields, output-sections, and the mapping between them. It does NOT know about SEO, pages, cities, services, competitors, or any domain concept. Those live entirely in the profile.

## 2. Input contract

### 2.1 Source set

A collection of files the engine reads as "what we researched / gathered." Specified by the profile as glob patterns or explicit paths relative to a base directory.

```yaml
source_set:
  base_dir: "<path>"
  collections:
    - name: "<collection-name>"
      description: "<what this collection represents>"
      glob: "<pattern>"          # e.g. "research-briefs/cities/*.md"
      format: md | json | yaml | txt | html
      field_extraction: frontmatter | json_keys | section_headings | line_inventory
      fields:                    # explicit field list (overrides auto-extraction)
        - name: "<field-name>"
          path: "<jsonpath or heading path>"
          description: "<what this field contains>"
          richness_metric: word_count | item_count | boolean | line_count
```

### 2.2 Output set

A collection of files the engine reads as "what we produced." Same structure:

```yaml
output_set:
  base_dir: "<path>"
  collections:
    - name: "<collection-name>"
      description: "<what this collection represents>"
      glob: "<pattern>"
      format: md | json | yaml | html
      variant_key: "<field that distinguishes variants>"  # e.g. "service-slug" or "city-slug"
      section_extraction: headings | css_selectors | json_keys
      sections:                  # explicit section list
        - name: "<section-name>"
          selector: "<heading text or CSS selector or JSON path>"
          description: "<what this section should contain>"
```

### 2.3 Profile

The profile is a YAML file in `references/profiles/` that binds source fields to output sections. It defines:

1. **source_set** — what to read as source material
2. **output_set** — what to read as produced output
3. **field_to_section_map** — which source fields should feed which output sections (the utilization + coverage map)
4. **variant_axes** — dimensions across which to compare coverage (e.g., per-service, per-city)
5. **expansion_rules** — heuristics for proposing new sections/artifacts from source richness
6. **competitor_architecture** (optional) — competitor artifact inventories to diff against our output set
7. **severity_thresholds** — when findings are blocking vs. advisory

```yaml
profile:
  name: "<profile-name>"
  domain: "<domain description>"
  version: "1.0"

  source_set:
    # ... (per §2.1)

  output_set:
    # ... (per §2.2)

  field_to_section_map:
    - source_collection: "<collection-name>"
      source_field: "<field-name>"
      target_collection: "<output-collection-name>"
      target_section: "<section-name>"
      required: true | false       # if true, absence = blocking finding
      notes: "<why this mapping exists>"

  variant_axes:
    - name: "<axis-name>"           # e.g. "service" or "city"
      source_key: "<frontmatter field or JSON key that identifies the variant>"
      expected_values: []           # optional explicit list; if empty, auto-discovered
      parity_fields:                # fields that should have equal depth across all variants
        - "<field-name>"

  expansion_rules:
    - name: "<rule-name>"
      trigger: "<condition>"        # e.g. "source field X has ≥N items"
      proposal: "<what to add>"     # e.g. "add a '{field}-by-era' subsection"
      evidence_source: "<which source collection/field>"
      priority: high | medium | low

  competitor_architecture:
    inventory_source: "<path to competitor URL/page-type inventories>"
    diff_against: output_set        # compare competitor page types vs our output set
    expansion_signal: true          # propose new artifact types from competitor architecture

  severity_thresholds:
    unused_source_field: advisory           # L1: source field not referenced in any output
    variant_depth_asymmetry: blocking       # L2: one variant significantly thinner than peers
    variant_missing_field: blocking         # L2: a parity field missing for one variant but present for others
    expansion_high_priority: advisory       # L3: high-priority expansion opportunity
    expansion_competitor_gap: advisory      # L3: competitor has page type we don't
```

## 3. Engine procedure

### Step 1: Load profile + discover artifacts

1. Read the profile YAML.
2. Glob for source artifacts. For each, extract fields per `field_extraction` method.
3. Glob for output artifacts. For each, extract sections per `section_extraction` method.
4. If `variant_axes` defined, group both source and output artifacts by variant key.

### Step 2: Lens 1 — Utilization audit

For each source collection → for each field defined in the profile:

1. Search all output artifacts for references to this field's content (substring match on field values, heading match on field names, or explicit `field_to_section_map` lookup).
2. Score: **utilized** (referenced in ≥1 output) or **unused** (referenced in 0 outputs).
3. For unused fields, compute a **richness score** (word count, item count, etc.) — high richness + unused = higher-priority finding.
4. Emit per-field utilization row: `{source_collection, field_name, richness, utilized: bool, referencing_outputs: []}`.

### Step 3: Lens 2 — Coverage gaps / asymmetry

For each variant axis → for each parity field:

1. Measure depth per variant (word count, item count, presence/absence).
2. Compute cross-variant statistics: median depth, min depth, max depth, coefficient of variation.
3. Flag **asymmetric** variants: any variant with depth < 50% of median (or missing entirely).
4. For asymmetric variants, identify which source fields are missing or thin compared to peers.
5. Emit per-variant-axis coverage row: `{axis, variant_value, field, depth, median_depth, ratio_to_median, status: "at-parity" | "under-fed" | "missing"}`.

### Step 4: Lens 3 — Expansion opportunities

1. **Source-driven expansion:** For each expansion rule in the profile, evaluate the trigger condition against source data. If met, emit a proposal with evidence citation.
2. **Competitor-driven expansion:** If `competitor_architecture` is configured, read competitor page-type inventories. Diff against our output set's artifact types. Any competitor page type we don't have = expansion candidate.
3. **Cross-reference:** Merge source-driven and competitor-driven proposals. De-duplicate. Rank by priority (from rule) and supporting evidence strength.
4. Emit ranked expansion backlog: `{rank, proposal_name, type: "new-section" | "new-data-binding" | "new-artifact-type", evidence: [], priority, source_richness_score}`.

### Step 5: Assemble report

Produce the **two-file artifact** (per the two-file artifact split pattern (human-scannable `.md` + machine-readable `.json`)):

1. **Human report** (`coverage-audit-report-YYYY-MM-DD.md`) — scannable markdown with tables per lens, executive summary, and actionable recommendations.
2. **Machine findings** (`coverage-audit-findings-YYYY-MM-DD.json`) — structured JSON consumable by orchestrators, prioritization skill, and gate-peer-reviewer.

### Step 6: Emit gate verdict

Map findings to a gate-peer-reviewer-compatible verdict:

| Condition | Severity | Verdict |
|-----------|----------|---------|
| Any L2 variant with `status: "missing"` for a `required: true` field | blocking | REJECT-AND-REDO |
| Any L2 variant with `status: "under-fed"` (depth < 50% median) | blocking | APPROVE-WITH-NOTES (surface for operator) |
| L1 unused fields with high richness (>500 words unused) | advisory | APPROVE-WITH-NOTES |
| L3 high-priority expansion opportunities | advisory | APPROVE-WITH-NOTES |
| All parity fields at parity, no high-richness unused fields | — | APPROVE |

## 4. Output contract

### 4.1 Human report (`.md`)

```markdown
---
type: coverage-audit-report
profile: <profile-name>
created: YYYY-MM-DD
source_artifact_count: N
output_artifact_count: N
verdict: APPROVE | APPROVE-WITH-NOTES | REJECT-AND-REDO
tags: [coverage-audit, <profile-name>]
---

# Content Coverage Audit — <profile-name>

**Run date:** YYYY-MM-DD
**Profile:** <profile-name> v<version>
**Source artifacts scanned:** N across M collections
**Output artifacts scanned:** N across M collections
**Verdict:** <verdict> (<blocking-count> blocking, <advisory-count> advisory)

## Executive Summary

<2-3 sentence summary of findings across all three lenses>

## Lens 1: Utilization

| Source Collection | Field | Richness | Utilized | Referencing Outputs |
|---|---|---|---|---|
| ... | ... | ... | Yes/No | ... |

### Unused high-richness fields (action required)
- ...

## Lens 2: Coverage Gaps / Asymmetry

### <Axis name> (e.g., "per-service")

| Variant | Field | Depth | Median | Ratio | Status |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | at-parity / under-fed / missing |

### Under-fed variants (action required)
- ...

## Lens 3: Expansion Opportunities

| Rank | Proposal | Type | Evidence | Priority |
|---|---|---|---|---|
| 1 | ... | new-section | ... | high |
| 2 | ... | new-artifact-type | ... | medium |

## Gate Verdict

<verdict block with severity-tagged findings list>
```

### 4.2 Machine findings (`.json`)

```json
{
  "schema_version": "1.0",
  "profile": "<profile-name>",
  "profile_version": "<version>",
  "run_date": "YYYY-MM-DD",
  "run_type": "<optional: proof | production | calibration>",
  "source_artifact_count": 0,
  "output_artifact_count": 0,

  "lens_1_utilization": {
    "total_fields_audited": 0,
    "utilized_count": 0,
    "unused_count": 0,
    "unused_high_richness_count": 0,
    "fields": [
      {
        "source_collection": "",
        "field_name": "",
        "richness_score": 0,
        "richness_metric": "word_count",
        "utilized": false,
        "referencing_outputs": [],
        "notes": "<optional: context for edge cases>"
      }
    ]
  },

  "lens_2_coverage": {
    "axes_audited": 0,
    "variants_at_parity": 0,
    "variants_under_fed": 0,
    "variants_missing": 0,
    "axes": [
      {
        "axis_name": "",
        "parity_fields_checked": 0,
        "variants": [
          {
            "variant_value": "",
            "field": "",
            "depth": 0,
            "median_depth": 0,
            "ratio_to_median": 0.0,
            "status": "at-parity",
            "notes": "<optional: context for edge cases, e.g. why ratio is low but status is at-parity>"
          }
        ]
      }
    ]
  },

  "lens_3_expansion": {
    "total_proposals": 0,
    "high_priority_count": 0,
    "backlog": [
      {
        "rank": 1,
        "proposal_name": "",
        "type": "new-section | new-data-binding | new-artifact-type | new-pattern | new-lesson | new-tool-note",
        "evidence": [],
        "priority": "high",
        "source_richness_score": 0,
        "source_collection": "",
        "competitor_signal": false
      }
    ]
  },

  "gate_verdict": {
    "verdict": "APPROVE",
    "verdict_severity": "advisory",
    "blocking_count": 0,
    "advisory_count": 0,
    "findings": [
      {
        "finding_id": "F-1",
        "lens": "L1",
        "severity": "advisory",
        "summary": "",
        "detail": "",
        "action": ""
      }
    ]
  }
}
```

### 4.3 Gate-peer-reviewer integration

The `gate_verdict` block in the machine findings is designed to compose with `gate-peer-reviewer`'s return contract. When `content-coverage-audit` runs as a gate within an orchestrator (e.g., `client-seo-onboarding` Step 2→3 transition), the orchestrator can:

1. Read `gate_verdict.verdict` to decide proceed/block.
2. Pass `gate_verdict.findings[]` to the reviewer as pre-computed checks.
3. The reviewer treats `blocking` findings as `REJECT-AND-REDO` triggers and `advisory` findings as `APPROVE-WITH-NOTES` notes.

Registered gate type: **G-coverage** (see `gate-peer-reviewer/references/gate-type-registry.md`).

## 5. Profile registration

Profiles live in `skills/content-coverage-audit/references/profiles/`. Each profile is a standalone YAML file.

**Shipped profiles:**
- `core-30-service-city-seo.yaml` — Core 30 service×city SEO pages (the seed profile from the EV build)
- `vault-source-to-note.yaml` — Non-SEO proof: audits research-source→vault-note coverage

**Adding a new profile:** Copy an existing profile, change the `source_set`, `output_set`, `field_to_section_map`, `variant_axes`, and `expansion_rules`. The engine runs identically — no code changes needed.

## 6. Composition

| Skill | Relationship |
|-------|-------------|
| `client-seo-onboarding` | Runs as research-wave gate (after Step 2 research, before Step 3 data-file generation). Graceful fallback if skill absent. |
| `gate-peer-reviewer` | Emits G-coverage verdict; reviewer consumes findings as pre-computed checks |
| `prioritization` | Receives L3 expansion backlog for sequencing |
| `output-quality-loop` | Audit report itself goes through OQL Mode 1 |
| `city-base-research` | Source collection: city briefs (Tier 2) |
| `intersection-research` | Source collection: intersection briefs (Tier 3) |
| `competitor-deep-research` | Source collection: competitor briefs + teardown inventories |
| `site-capture-engine` | Source collection: teardown extracted data |
| `synthesis-readiness-scan` | Complementary: SRS checks source readiness for synthesis; CCA checks source utilization in output |

## 7. Substrate

Claude Code (preferred). The engine reads files from disk and produces two output files. No external API calls. No browser needed. Runs in any Claude Code session with access to the source and output directories.

## 8. Invocation

```
Run content-coverage-audit with profile <profile-name>
  source base: <path>
  output base: <path>
  [output dir: <path>]  # where to write the report; defaults to source base
```

The operator (or orchestrator) specifies the profile name. The engine loads the profile from `references/profiles/<name>.yaml`, resolves source/output paths, and runs the three lenses.

## 9. Non-SEO proof requirement

Acceptance requires demonstrating the engine on a non-page source→output set using a config-only profile (no engine changes). The `vault-source-to-note` profile fulfills this: it audits how well VIS-extracted source notes are converted into vault knowledge artifacts (patterns, lessons, blueprints) — a completely different domain with the same engine.
