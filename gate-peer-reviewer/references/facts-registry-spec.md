---
type: reference
skill: gate-peer-reviewer
skill-version: 3.1
created: 2026-06-07
updated: 2026-06-07
tags: [reference, facts-registry, ground-truth, value-correctness, engine-level, project-agnostic]
---

# Facts registry spec — ground-truth value-correctness layer

The facts registry is the engine-level mechanism the gate-peer-reviewer uses to
cross-check **value-correctness** — not just consistency/cleanliness (which
existing checks already cover), but whether claimed values are TRUE for a given
subject.

## Why this exists

Every defect that reached live in the S&H wave-2 production run was a wrong
value for the context:

- D-10: Fairfax areaServed on a Stafford page
- D-11: Dominion-only on a 3-utility city
- D-12: 45-min dispatch on a 15-mi city
- D-13: Dispatch time carry-forward from wrong template

The existing 6-check engine verifies contract satisfaction, calibration,
domain plausibility, structural coherence, and carry-forward — but never
asks "is this value TRUE for this subject?" The facts registry adds that
question as a named procedure any gate type can reference.

## Architecture

### Facts profile shape (generic)

A **facts profile** is a declarative configuration that tells the
`ground-truth-value-cross-check` procedure:

1. **Where** to find ground-truth facts for a subject
2. **What fields** to extract and cross-check
3. **Where in the artifact** to look for claimed values (extraction surfaces)

```yaml
facts_profile:
  profile_id: <unique-string>
  description: <one-line purpose>

  # How to resolve ground-truth for a given subject
  ground_truth_source:
    type: <json-files | inline-table | external-api>
    # For json-files:
    paths:
      - pattern: "data/cities/{subject_id}.json"
        fields: [dispatch_time_short, dispatch_time_phrase, county, county_full, utilities_electric, areaServed]
      - pattern: "data/client-{client_id}.json"
        fields: [name, owner_name, phone_display, website_url]
    # For inline-table:
    table: { ... }  # direct key-value map, used for small/static registries

  # Which fields to cross-check (the "facts" this profile validates)
  checkable_facts:
    - fact_key: dispatch_time
      ground_truth_field: dispatch_time_short     # field name in the source
      extraction_surfaces: [body_text, meta_description, jsonld_schema]
      extraction_patterns:                         # regexes to find the claimed value
        - '\b(\d+)[–-]?min(ute)?\b'
        - 'response.{0,30}?(\d+)[–-]?\s*min'
      match_mode: exact                            # exact | contains | regex

    - fact_key: area_served
      ground_truth_field: county_full
      extraction_surfaces: [jsonld_schema.areaServed, meta_description, body_text]
      extraction_patterns:
        - 'areaServed.*?"name"\s*:\s*"([^"]+)"'
      match_mode: contains

    # ... additional fact definitions per profile

  # What artifact surfaces to scan
  extraction_surfaces:
    body_text:
      description: "Rendered HTML body text (stripped of tags)"
    meta_description:
      description: "AIOSEO / Yoast meta description field"
    og_tags:
      description: "Open Graph og:title, og:description"
    jsonld_schema:
      description: "JSON-LD structured data block(s)"
    frontmatter:
      description: "YAML frontmatter in markdown source"
```

### Registered profiles

Profiles are registered in a `facts-profiles/` directory under the peer-reviewer
references, one file per profile. The named procedure loads the profile by ID
from the gate-type entry's configuration.

```
skills/gate-peer-reviewer/references/
  facts-registry-spec.md          (this file)
  facts-profiles/
    core-30-page-build.yaml       (Core 30 SEO pages: service x city)
    research-brief.yaml           (research briefs: city/service/client facts)
    ... future profiles
```

**Zero hardcoding in the engine.** The procedure reads the profile; the profile
declares the sources, fields, surfaces, and match rules. The engine never
mentions "Core 30", "SEO", "city", "service", or any project-specific concept.

### Cross-check algorithm

For each `checkable_fact` in the profile:

1. **Resolve ground truth.** Load the source file(s) using the pattern +
   subject ID. Read the `ground_truth_field`. If the field is missing from
   the source, this is a **facts-completeness failure** (see SC-2) — flag it
   as a separate catch, do not default.

2. **Extract claimed values.** For each `extraction_surface` listed for this
   fact, scan the artifact using the `extraction_patterns`. Collect all
   matches with their locations (surface + line/offset).

3. **Compare.** For each claimed value:
   - `exact`: claimed value must equal ground truth (case-insensitive trim)
   - `contains`: ground truth must appear within the claimed value
   - `regex`: claimed value must match the ground truth when used as a pattern

4. **Verdict per fact.**
   - All claimed values match ground truth = PASS
   - No claimed values found in any surface = MISSING (flag as
     "fact not represented in artifact" — may or may not be a defect
     depending on the fact's `required_in_surfaces` config)
   - Any claimed value mismatches ground truth = **MISMATCH** — this is
     the load-bearing catch. Report: fact key, expected value (from
     registry), found value (from artifact), surface, location.

5. **Aggregate verdict.**
   - Zero MISMATCH + zero MISSING-on-required-surfaces = PASS
   - Any MISMATCH = catch (potential REJECT-AND-REDO)
   - MISSING on required surface without MISMATCH = APPROVE-WITH-NOTES

### Integration with the 6-check engine

The `ground-truth-value-cross-check` is a **named verification procedure**
(same class as `full-placeholder-family-sweep` and `source-client-leak-audit`).
It fires at Check 1 time as a satisfaction sub-check. Gate-type entries
reference it in `check_1_satisfaction_targets`.

It does NOT create a new check (Check 7). It extends Check 1's contract
satisfaction discipline: "the gate output must not only satisfy the kickoff
prompt's asks but also match ground-truth facts for the subject."

### Non-SEO applicability proof

The mechanism is generic. Examples of non-SEO facts profiles:

1. **Research-brief profile:** Cross-check a city-base-research brief's
   utility claims against a municipal-utilities facts table. The brief says
   "Manassas is served by Dominion Energy" — the facts registry says
   "Manassas Electric Department (municipal)." Same algorithm, different
   profile, different domain.

2. **Client-fact-research profile:** Cross-check a client-fact brief's NAP
   data against the client JSON. The brief says phone is "(703) 555-1234" —
   the registry says "(571) 555-9876." Same algorithm.

3. **VIS-extraction profile:** Cross-check a source note's metadata (speaker
   name, talk title, publication date) against the YouTube API / article
   meta. The note says "Published 2025-03-15" — the registry says
   "2025-04-01." Same algorithm.

The engine knows none of these domains. It reads the profile, resolves
ground truth, extracts claims, compares. Domain knowledge lives in the
profile YAML, not the procedure.

## Execution evidence requirement

Same as all named procedures (per v2.1 D-02/D-03 calibration):

- The reviewer must produce **actual extraction output** — real values found
  at real locations, real comparison results.
- "Ground-truth cross-check passed" without showing expected-vs-found is not
  execution evidence.
- Every MISMATCH must cite: fact key, expected (source + field), found
  (surface + location), delta.

## Relationship to SC-1 and SC-2

| Component | When it fires | What it catches |
|---|---|---|
| **SC-2 (facts-completeness gate)** | Pre-scaffold | Missing data fields → prevents silent defaults |
| **SC-1 (hardcode-scanner)** | Post-scaffold | Template defaults that leaked through → catches parameterization misses |
| **GPR-10 (this — ground-truth cross-check)** | At gate review | Wrong values in finished artifacts → catches value errors the operator would catch at live gate |

Three layers, one class of defect (wrong value for context), caught at
three points in the pipeline (pre-scaffold, post-scaffold, gate review).

## Boundary: output-matches-source, NOT source-matches-reality

This mechanism verifies that artifact values match the ground-truth source
(data JSONs). It does NOT verify that the source itself is correct. If a
city JSON says `dispatch_time_short: "25-min"` but the real dispatch time
is 40 minutes, this layer will PASS — the artifact matches its source.

**Source-matches-reality is a different layer's job.** The research gates
(G-city-brief, G-service-brief, G-client-brief) and Check 3 domain
plausibility (Sonar probe) are responsible for verifying source data
against the real world. This layer trusts the source and verifies the
pipeline didn't corrupt, default, or carry-forward a wrong value from it.
