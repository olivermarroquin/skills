---
name: prioritization
version: 1.0
status: active
created: 2026-06-06
updated: 2026-06-06
description: Generic engine that turns any candidate set into a ranked, sequenced plan using named scoring criteria, optional registered profiles, and hard dependency constraints. Substrate-, tool-, process-, and output-agnostic. Domain knowledge lives entirely in profiles.
triggers:
  - any workflow needs to rank, sequence, or prioritize a set of items
  - an orchestrator delegates "propose a build order" to this skill
  - operator invokes directly with a candidate set + profile or inline criteria
composes-with:
  - client-seo-onboarding (v1.5+, Step 1 build-order delegation via core-30-service-city-seo profile)
  - any future orchestrator that needs prioritized sequencing
tags: [skill, prioritization, build-order, ranking, sequencing, agnostic, reusable, engine-plus-profile]
---

# `prioritization` skill v1.0

Generic prioritization engine. Takes a candidate set, scores each item against named criteria, enforces hard dependency constraints, and emits a ranked sequence with per-item rationale and the scoring rubric used.

Domain-specific knowledge lives in **profiles** (`references/profiles/`), not in this engine. The engine carries zero references to any specific domain, client, tool, or process.

## Purpose

Many workflows need to turn a flat set of candidates into an ordered plan: which items to do first, which to batch, which to defer. The logic is the same regardless of whether the items are SEO pages, feature tickets, research targets, outreach contacts, or handoff tasks. This skill captures that logic once.

## Concepts

### Candidate set

An array of items to rank. Each item has:
- `id` — unique identifier (slug, name, ticket number, etc.)
- `attributes` — key-value pairs the scoring criteria read (e.g., `service: "panel-upgrade"`, `city: "Vienna"`, `effort: "low"`)
- `group` (optional) — grouping label for batch/wave decomposition

Items can be provided inline (pasted list, table, or structured block) or by reference (path to a file containing the set).

### Scoring criteria

Named dimensions the engine uses to rank items. Each criterion has:

| Field | Type | Description |
|---|---|---|
| `name` | string | Machine-readable key (e.g., `item_priority`) |
| `label` | string | Human-readable display name |
| `description` | string | What this criterion measures |
| `direction` | `higher-is-better` or `lower-is-better` | Sort direction for this criterion |
| `values` | ordered list or numeric range | The legal values, in rank order (for categorical) or min-max (for numeric) |

The engine ships with no built-in criteria. All criteria come from the profile or from inline `criteria_override`.

### Scoring modes

The engine supports two modes. The profile declares which mode to use.

**`lexicographic`** — Sort by criterion 1 (primary key), then criterion 2 (secondary key), and so on. Lower-priority criteria are tie-breakers only — they never override a higher-priority criterion. This is the right mode when the domain has a clear priority hierarchy (e.g., "service type matters more than city, always").

Criteria are listed in priority order in the profile. For each criterion, items are bucketed by their value (using the `values` ordering). Within each bucket of the primary key, items are sub-sorted by the secondary key, and so on.

**`weighted-sum`** — Each criterion has a numeric `weight` (0.0–1.0). Item scores are normalized per criterion, multiplied by weight, and summed. Items are sorted by total score descending. This is the right mode when criteria trade off against each other (e.g., "a very high opportunity score can compensate for moderate effort").

When using `weighted-sum`, each criterion must also have a `weight` field.

### Hard dependency constraints

Dependencies are **not** scoring criteria. They are topological constraints applied **after** scoring:

- Expressed as `must_before` pairs: `[predecessor_id, successor_id]` — predecessor must appear before successor in the final sequence, regardless of score.
- The engine scores all items first, then applies a topological sort pass. If a dependency forces a lower-scored item above a higher-scored one, the rationale for the displaced item notes: "Moved up by dependency: must precede `<successor_id>`."
- Circular dependencies are surfaced as an error: "Circular dependency detected: `<cycle>`. Cannot produce a valid sequence. Resolve before re-running."

Dependencies can be provided:
- Inline in the candidate set (per-item `depends_on: [id, ...]` field)
- As a separate `constraints.must_before` array of `[predecessor, successor]` pairs
- Both (merged)

### Profiles

A profile is a named, reusable bundle of:
- Scoring mode (`lexicographic` or `weighted-sum`)
- Criteria definitions (ordered list for lexicographic; weighted list for weighted-sum)
- Default dependency rules (optional)
- Output format preferences (optional)
- Domain context (what kind of items this profile ranks, for rationale generation)

Profiles live in `references/profiles/`. Each profile is a Markdown file with YAML frontmatter. See the seeded `core-30-service-city-seo` profile for the canonical shape.

Any workflow can use any profile. Profiles are additive — the engine never hard-codes knowledge that should live in a profile.

### How to register a new profile

1. Create a new `.md` file in `references/profiles/` following the profile shape (see existing profiles).
2. Define the scoring mode, criteria, and any default constraints.
3. The engine picks it up by name — no engine edits required.

## Input contract

The engine accepts these inputs (provided by the calling workflow or operator):

| Input | Required | Description |
|---|---|---|
| `candidate_set` | yes | Items to rank — inline or by file reference |
| `profile` | no | Name of a registered profile in `references/profiles/`. If omitted, `criteria_override` is required. |
| `criteria_override` | no | Inline criteria definitions. Overrides profile defaults if both are provided. |
| `constraints` | no | Hard constraints: `must_before` pairs, `exclude` items, `group_by` field |
| `output_path` | no | Where to write output files. Defaults to caller's working directory. |

At least one of `profile` or `criteria_override` must be provided.

## Execution steps

### Step 1 — Resolve criteria

1. If `profile` is named, read it from `references/profiles/<profile>.md`.
2. If `criteria_override` is also provided, merge: overrides win on conflict, additions are appended.
3. If neither `profile` nor `criteria_override` is provided, stop with: "No scoring criteria. Provide a profile name or inline criteria."
4. Validate: each criterion has `name`, `label`, `direction`, `values`. For `weighted-sum` mode, each must also have `weight` (and weights must sum to 1.0 after normalization).

### Step 2 — Score each item

For each item in `candidate_set`:
1. Read the item's `attributes`.
2. For each criterion, compute the item's score on that dimension:
   - **Categorical values:** score = position in the `values` list (0 = best for `higher-is-better`, reversed for `lower-is-better`).
   - **Numeric values:** score = raw value (direction applied at sort time).
   - **Missing attribute:** score = worst possible (item is penalized, not errored). Note in rationale: "Missing value for `<criterion>` — scored at floor."
3. Record per-criterion scores.

### Step 3 — Rank

**If `lexicographic` mode:**
1. Sort items by criterion 1 value (best first per direction).
2. Within ties on criterion 1, sort by criterion 2.
3. Continue through all criteria.
4. Items still tied after all criteria retain their input order (stable sort).

**If `weighted-sum` mode:**
1. Normalize each criterion's scores to 0.0–1.0 range across the candidate set.
2. Multiply each normalized score by the criterion's weight.
3. Sum weighted scores per item.
4. Sort by total score descending.

### Step 4 — Apply dependency constraints

1. Collect all `must_before` pairs (from `constraints` input + per-item `depends_on` fields).
2. If no dependencies, skip to Step 5.
3. Run topological sort on the dependency graph, using the Step 3 ranking as the tie-breaking order.
4. If any item is displaced (moved earlier than its score-rank position), annotate its rationale.
5. If a cycle is detected, stop with error.

### Step 5 — Generate output

Produce two files (per the two-file artifact split pattern):

**Human-readable file (`_build-order.md` or caller-specified name):**

```markdown
---
type: meta
status: draft
created: <date>
profile: <profile-name or "ad-hoc">
scoring_mode: <lexicographic | weighted-sum>
criteria_used: [<criterion names>]
tags: [build-order, prioritization, <profile-name>]
---

# <Title — provided by caller or defaulted to "Prioritized sequence">

## How this list was built

<Scoring rubric: criteria names, weights/priority-order, directions, value definitions.>

## Sequence

| # | ID | <Criterion 1> | <Criterion 2> | ... | Rationale |
|---|---|---|---|---|---|
| 01 | <item_id> | <value> | <value> | ... | <why this rank> |
| ... | ... | ... | ... | ... | ... |

## Dependency constraints applied

<List of must_before pairs that caused rank displacement, or "None.">
```

**Machine-readable file (`_build-order-ranking.json` or caller-specified name):**

```json
{
  "metadata": {
    "profile": "<profile-name or ad-hoc>",
    "scoring_mode": "<lexicographic | weighted-sum>",
    "criteria": [ { "name": "...", "weight": "...", "direction": "..." } ],
    "generated_at": "<ISO-8601>",
    "candidate_count": 0,
    "dependency_displacements": 0
  },
  "ranking": [
    {
      "rank": 1,
      "item_id": "...",
      "scores": { "criterion_name": "value" },
      "total_score": null,
      "rationale": "..."
    }
  ]
}
```

`total_score` is populated only in `weighted-sum` mode; `null` in `lexicographic` mode.

### Step 6 — Surface to caller

Return the two file paths + a summary line:
```
Ranked <N> items using profile "<profile>" (<scoring_mode> mode, <K> criteria).
Dependency constraints displaced <M> items.
Output: <path-to-md>, <path-to-json>.
```

## Auto-invoke output-quality-loop

This skill produced the following artifact(s):
- `<output_path>/_build-order.md`
- `<output_path>/_build-order-ranking.json`

[output-quality-loop:eval] — for each artifact, run output-quality-loop in EVALUATE mode. If PASS, declare the chat done. If NEEDS REVISION or FAIL, ingest the revision prompt as if it were operator input and regenerate the artifact, then re-invoke output-quality-loop. Cap at 3 iterations; on the 3rd FAIL, escalate to the operator with the evaluation report.

## No-regression contract

When an orchestrator delegates build-order generation to this skill (e.g., `client-seo-onboarding` v1.5 Step 1), the acceptance test is: **same ranking from same inputs.** Given the same candidate set and the same profile, the skill must produce the same item ordering as the orchestrator's prior inline logic. Byte-identical output is not required — equivalent ranking is.

## Graceful absence

Callers that delegate to this skill should implement graceful fallback: if the skill directory (`skills/prioritization/`) is absent or the profile is missing, fall back to inline logic and log a warning. This prevents hard coupling.

## What this skill does NOT do

- It does not generate the candidate set (the caller provides items).
- It does not execute the plan (it ranks; the caller acts).
- It does not know about any specific domain (profiles carry domain knowledge).
- It does not modify its own profiles at runtime (profiles are authored, not learned).
- It does not make judgment calls about item quality (it ranks by declared criteria, not by evaluating content).
