---
name: output-quality-loop
description: Evaluate a finished Knowledge OS artifact against the specs that define what "good" looks like for its type, produce a structured verdict (PASS / NEEDS REVISION minor or substantive / FAIL), generate a revision prompt the producing chat can ingest to regenerate, and (Mode 4) compose with `perplexity-refinement` to research the strongest published version of each gap and feed those elevation suggestions back into the revision prompt. Triggers on phrases like "quality-check <artifact-path>," "evaluate <artifact-path>," "run output-quality-loop on <artifact-path>," "is this draft ready to ship," "does this brief meet the spec," "did the refinement pass actually elevate the source note," "audit this synthesis against its sources," "elevate this draft against the strongest published version," "what's the best version of this artifact in the world," or any time the operator wants a structured fitness evaluation of an artifact already on disk. Also fires via the auto-invoke convention block other skills emit at completion (see references/auto-invoke-convention.md). The keystone of the output-quality-loop system; Phases 2-6 of the roadmap build on top of this skill.
---

# Output Quality Loop Skill (v1.3)

The quality-evaluation layer of the Knowledge OS. Runs after an artifact lands. Reads the artifact, walks the spec-routing table to gather every spec source that applies to that artifact type, builds an evaluation checklist from the specs, scores the artifact against the checklist, lands a verdict, writes the verdict to the folder-level quality log, and — when the verdict is NEEDS REVISION or FAIL — produces a revision prompt the producing chat can ingest to regenerate.

**Critical behavior (read this before doing anything else):**

- **Non-destructive on the artifact body.** The skill never edits the substance of the artifact being evaluated. It only writes (1) to the folder-level `_quality-log.md` (creating it if absent), and (2) three quality-tracking fields in the artifact's frontmatter (`quality-log:`, `last-evaluated:`, `last-verdict:`). The producing chat owns the body; this skill judges and records.
- **Perplexity Pro is the only external research source.** When external benchmarking is required (Phase 4 auto-research mode and any spec-source loading that needs fresh data), route through `perplexity-refinement` — which, after Phase 2's fix, drives a logged-in Perplexity Pro browser session by default and falls back to the Sonar API only when Pro is unreachable. Silent fallback to Cowork `WebSearch` is forbidden. If Perplexity Pro is unavailable, this skill pauses and surfaces the gap; it does not degrade to a different source.
- **Honest verdicts.** If the artifact is genuinely good, return PASS. Don't fabricate revision suggestions to justify the skill running. If the artifact is broken, return FAIL with diagnosis. Picking an intermediate verdict when one extreme is true erodes the loop's usefulness over time.
- **Cap at 3 iterations per artifact.** If the loop runs three times against the same artifact and still hasn't reached PASS, emit a "loop-stalled" escalation report naming the unresolved gaps and stop. The artifact then needs human judgment, not another machine pass.
- **No invented spec sources.** If the spec-routing table has no entry for the detected artifact type, surface that gap explicitly ("no spec routing for type X — operator needed to name spec sources or extend the routing table"). Don't borrow specs from a neighboring type and hope they fit.
- **Cite spec sources by line in evaluation reports.** When evaluating against a spec, name the specific section or line that defines the bar (e.g., "spec source: `_template-service-brief.md` §4.5 — AI-citation hardening checklist item C, attribute density"). Auditability matters; vague citations erode trust.
- **Plain language in every report.** Per [[plain-language-conventions]] and the standing `feedback_plain_language_default.md` memory. Short sentences, conversational rhythm, gloss obscure terms inline on first use, keep technical terms when they're the right name for the thing.
- **Check folder structure before writing the quality log.** Per the standing `feedback_check_folder_structure_before_writing.md` memory. `_quality-log.md` lives at the root of the artifact's immediate folder; if that folder has a `_README.md`, read it before creating the log file so the new file lines up with the folder's intent.

---

## When to use this skill

Trigger when the operator (or another skill via the auto-invoke convention) wants a structured fitness evaluation of an artifact already on disk. Typical phrasings:

- "Quality-check `panel-upgrade--vienna-va.md`"
- "Evaluate `source-2026-04-26-jono-catliff-claude-code-seo-50000-clicks-per-month-masterclass.md`"
- "Run output-quality-loop on `cluster-synthesis-ai-era-seo-cluster-2026-05-27.md`"
- "Is this draft ready to ship?"
- "Did the refinement pass actually elevate the source note, or is it filler?"
- "Audit this synthesis against its sources"
- The standard auto-invoke block emitted by other skills at completion (documented in `references/auto-invoke-convention.md`)

Do **not** use this skill for:

- Drafting artifacts (that's the producing skill's job — VIS, perplexity-refinement, multi-source-synthesis, service-seo-research, etc.)
- Pure formatting fixes (use targeted edits or the plain-language-translation skill)
- Web pages, PDFs, or external content the vault doesn't own
- Running the evaluation in a loop without operator visibility (the cap is 3 iterations, no exceptions)

---

## Five invocation modes

### Mode 1 — EVALUATE (the core mode)

Reads an artifact, builds the checklist, scores it, writes the verdict to the folder log + the artifact's frontmatter, and produces the evaluation report.

**Trigger phrases:**

- "Quality-check `<artifact-path>`"
- "Evaluate `<artifact-path>`"
- "Run output-quality-loop on `<artifact-path>`"
- The auto-invoke `[output-quality-loop:eval]` directive from another skill (see `references/auto-invoke-convention.md`)

**Operator overrides (bypass the routing table):**

- "Quality-check `<artifact>` against `<spec1>` `<spec2>`" — the named specs are used instead of the auto-routed ones
- "Quality-check `<artifact>` with depth=deep" — runs Mode 4 (AUTO-RESEARCH) after the EVALUATE pass, regardless of verdict (including PASS — Mode 4 normally only fires on NEEDS REVISION / FAIL but the operator can force it on PASS to elevate further)
- "Quality-check `<artifact>` with auto-research max=N" — overrides the per-type cap from `references/research-budget-per-type.md` for this single run

**Workflow:** 6 phases. Each phase has a stop condition; honor it.

#### Phase 1 — Detect the artifact type

Walk the detection table in `references/artifact-type-detection.md`. Match the artifact's path pattern, frontmatter `type:` field, and content shape against the table's rows. Pick the most-specific match.

If no row matches, surface the gap: "I can't detect the artifact type from path / frontmatter / content shape. Tell me the type or extend `references/artifact-type-detection.md` with a row that covers this shape."

If multiple rows match (e.g., a research brief that's also a synthesis-class meta-document), pick the most-specific match and note the secondary match in the evaluation report — the secondary spec source might still add a checklist item.

#### Phase 2 — Walk the spec-routing table

Open `references/spec-routing-table.md`. Find the row for the detected type. Load every spec source the row names. For each spec source:

- Read the file end to end (or the named section, if the routing table points at a section)
- Capture every hard requirement (must-have for ship), every quality dimension (must-have at threshold), and every discipline rule the spec encodes

If a spec source is unreachable (file moved, link broken, external URL unreachable), surface the gap. Don't silently skip — the evaluation's audit trail depends on naming every spec source loaded.

#### Phase 3 — Build the evaluation checklist

Combine the loaded spec sources into a single checklist. Items split into three categories:

1. **Hard requirements** — frontmatter shape, required sections, schema validity, named fields present. A miss on any hard requirement is sufficient cause for FAIL.
2. **Quality dimensions** — citation density, plain-language compliance, attribute density per AI-citation discipline, voice-match for client work, completeness against named criteria. Each scored pass / partial / fail.
3. **Discipline rules** — non-destructive editing (where the artifact extends an existing one), git-add-by-name (for repo-touching artifacts), premature-abstraction avoidance, plain-language conventions, etc.

Per-artifact-type specifics live in `references/evaluation-heuristics-by-type.md`. Pull from there once the artifact type is detected.

Each checklist item carries a one-line citation back to the spec source that defines it (e.g., "spec source: `_template-service-brief.md` §4.5 A — TL;DR rule"). The citation is mandatory; without it the evaluation isn't auditable.

#### Phase 4 — Evaluate the artifact against the checklist

Walk each checklist item. For each:

- **Hard requirements:** pass / fail with a one-line justification quoting the spec or the artifact
- **Quality dimensions:** pass / partial / fail with a one-line justification
- **Discipline rules:** pass / fail with a one-line justification

If a checklist item is genuinely not applicable to the artifact (e.g., a discipline rule that only fires when the artifact extends an existing one, and this artifact doesn't extend anything), mark it `not-applicable` with a one-line explanation. Do not mark items not-applicable to inflate the pass rate.

#### Phase 5 — Roll up the verdict

Apply `references/verdict-rollup-thresholds.md`:

- **PASS** — all hard requirements met + at least 85% of applicable quality dimensions at threshold + zero discipline-rule violations
- **NEEDS REVISION (minor)** — all hard requirements met + 70–84% of quality dimensions at threshold + at most 2 minor discipline-rule violations. Fixable with targeted edits, not a full regeneration.
- **NEEDS REVISION (substantive)** — hard requirements met + 50–69% of quality dimensions at threshold OR 3+ discipline-rule violations. Needs regeneration with explicit gap closure, not surface edits.
- **FAIL** — any hard requirement missed OR fewer than 50% of quality dimensions at threshold. Root-cause analysis required before regeneration.

Edge case: if hard requirements all pass but a single high-stakes quality dimension (e.g., "every claim has a citation" for refinement outputs) is at fail and the rest are clean, the verdict still elevates to NEEDS REVISION at the appropriate severity. Discipline rules can also escalate a verdict — e.g., a non-destructive violation flips an otherwise-PASS artifact to NEEDS REVISION (substantive) because the discipline rule is load-bearing.

#### Phase 6 — Write the verdict to the folder log + artifact frontmatter

Per `references/folder-quality-log-shape.md`:

1. **Locate the folder log.** It's at the root of the artifact's immediate folder, filename `_quality-log.md`. If it doesn't exist, create it using the shape in `references/folder-quality-log-shape.md` (frontmatter + empty per-artifact section list).
2. **Find or create the per-artifact section.** Each artifact in the folder gets its own `## <artifact-slug>` section. If the section doesn't exist yet, append it.
3. **Append the new iteration entry.** Full evaluation report inline (the same shape as the on-screen report — see "Evaluation report format" below), date-stamped.
4. **Update the section's "Latest:" line at the top.** Single line at the top of the section that names the most recent verdict + date. Downstream gates read this line.
5. **Update the folder log's frontmatter counters.** Increment `shipped`, `iterating`, or `escalated` per the verdict; bump `last-updated`.
6. **Update the artifact's own frontmatter** with three fields:

```yaml
quality-log: "[[_quality-log#<artifact-slug>]]"
last-evaluated: YYYY-MM-DD
last-verdict: PASS | NEEDS REVISION (minor) | NEEDS REVISION (substantive) | FAIL
```

These three fields are what downstream gates (Phase 3 publish gate, Phase 6 auto-approve) read. The folder log holds the full archaeology; the artifact's frontmatter holds the latest verdict pointer.

7. **Emit the evaluation report to the operator** (same shape as what was just written to the folder log).

If the verdict is NEEDS REVISION (minor), NEEDS REVISION (substantive), or FAIL, automatically continue to Mode 2 (REVISE-PROMPT) and produce the revision prompt. The producing chat needs both the evaluation and the revision prompt to close the loop.

If this is the third iteration on the same artifact and the verdict is still not PASS, **escalate**: emit a "loop-stalled" report naming the unresolved gaps, write the escalation to the folder log, and stop. The artifact moves to human-judgment territory.

---

### Mode 2 — REVISE-PROMPT (the loop-completing mode)

Produces a paste-ready prompt the operator can drop into the chat that produced the artifact (or a fresh chat if the original is closed). The producing chat ingests the prompt as if it were operator input, regenerates the artifact, and triggers a re-evaluation.

**Trigger phrases:**

- Auto-fires as the second step of Mode 1 when the verdict is NEEDS REVISION (minor), NEEDS REVISION (substantive), or FAIL
- Manual: "Generate revision prompt for `<artifact-path>` based on `<evaluation-path>`"

**Workflow:**

1. Read the evaluation report (in-memory if just produced, from the folder log if invoked manually).
2. Build the revision prompt per `references/revision-prompt-template.md`. The prompt must:
   - Open with: "Your previous output was evaluated and needs revision. Apply the following fixes and re-output the artifact."
   - List failing items, grouped by severity (hard requirements first, then quality dimensions, then discipline rules)
   - For each failing item: name the specific gap, reference the spec source that defined the bar, describe what good would look like
   - Close with: "After applying these fixes, the artifact will be re-evaluated by output-quality-loop. The cycle continues until PASS or a maximum of 3 iterations have run."
3. Emit the prompt to stdout. If the operator named a path or the artifact has a `.revision-prompt.md` sibling convention in play, also write the prompt to `<artifact-path>.revision-prompt.md`.
4. Log the prompt generation in the folder log's per-artifact section (one line: "Revision prompt generated YYYY-MM-DD HH:MM").

---

### Mode 3 — AUTO-INVOKE-CONVENTION (the convention spec)

Other skills emit a standard convention block at the end of their work; this skill reads the block, runs Mode 1 on each named artifact, and reports back. The producing chat declares done if all results are PASS, or ingests the revision prompts and regenerates if any are NEEDS REVISION / FAIL.

The convention block other skills emit (specified in full in `references/auto-invoke-convention.md`):

```markdown
## Auto-invoke output-quality-loop

This skill produced the following artifact(s):
- `<artifact-path-1>`
- `<artifact-path-2>`

[output-quality-loop:eval] — for each artifact, run output-quality-loop in EVALUATE mode. If PASS, declare the chat done. If NEEDS REVISION or FAIL, ingest the revision prompt as if it were operator input and regenerate the artifact, then re-invoke output-quality-loop. Cap at 3 iterations; on the 3rd FAIL, escalate to the operator with the evaluation report.
```

**Workflow when this skill sees the convention block:**

1. Parse the artifact path list out of the block (one path per bullet).
2. For each artifact, run Mode 1 (EVALUATE). Each evaluation is independent — one artifact's verdict doesn't affect another's.
3. Aggregate results into a single summary back to the producing chat:
   - All PASS → "All N artifacts passed. Producing chat may declare done."
   - Any NEEDS REVISION / FAIL → list the failing artifacts with their verdicts and a pointer to the revision prompt for each. The producing chat is responsible for ingesting the prompts.
4. Update the folder log per Phase 6 of Mode 1 for every artifact evaluated.

The producing chat retains responsibility for the iteration cap (3) — this skill emits verdicts and revision prompts; the producing chat decides when to escalate.

---

### Mode 4 — AUTO-RESEARCH (the elevation mode)

The deepening capability. Modes 1-3 evaluate fit against the spec — they enforce the floor. Mode 4 asks "what's the strongest version of this argument or claim or section that exists in current published work?" and compares the artifact against that external benchmark. The gap becomes new revision suggestions that feed back into Mode 2's prompt.

Mode 4 turns the loop from policing-only into quality-elevation. Without it the loop only enforces the spec the artifact was written against — which may itself be incomplete or out of date. With it the loop pushes outputs toward the frontier.

**Trigger phrases:**

- Auto-fires after Mode 1's verdict on NEEDS REVISION (minor), NEEDS REVISION (substantive), or FAIL by default
- Operator-opt-in on PASS via "Quality-check `<artifact>` with depth=deep" (skipped by default for PASS to keep the loop fast)
- Manual: "Run auto-research on `<artifact-path>` using the existing evaluation"
- "Elevate `<artifact-path>` against the strongest published version"
- "What's the best version of `<artifact-path>` in the world?"

**Critical behavior for Mode 4:**

- **Perplexity Sonar is the only external research source.** Mode 4 invokes `perplexity-refinement` as a subroutine, which routes through the Sonar API (via `~/workspace/second-brain-tier3/automation/scripts/perplexity_sonar.py`) → refusal. **Silent fallback to Cowork's `WebSearch` is forbidden at every layer.** If `perplexity-refinement` returns the refusal message, Mode 4 surfaces the gap to the operator and stops; it does not degrade to vault-internal research and pretend it filled the external benchmark. (Historical note: an earlier framing of this skill carried a two-path priority — Path A Claude in Chrome → Path B Sonar API. Path A was removed 2026-06-01.)
- **Capped per artifact type.** See `references/research-budget-per-type.md`. Hard ceiling is 8 queries per artifact regardless of type; soft ceiling is top-5 gaps researched. Don't pad runs to hit the cap.
- **Non-destructive.** Mode 4 writes only to the folder log (a new `### External research (Mode 4)` sub-section under the artifact's per-artifact section) and to Mode 2's revision prompt. It never edits the artifact body.
- **Honest about inconclusive results.** If Perplexity returns "inconclusive" three queries in a row, stop and surface in the folder log. The artifact's gaps may not be researchable externally (vault-internal patterns, operator-discipline observations, proprietary knowledge). Don't fabricate elevation suggestions to justify the cost.
- **Cache reuse within iteration only.** Two gaps that trigger the same query share one query. Cross-artifact cache reuse is not allowed in v1 — gap shapes differ enough that reusing a query would silently drop attribution discipline.

**Workflow:** 7 steps. Each step has a stop condition; honor it.

#### Step 1 — Identify the top-N gaps

Read the EVALUATE pass's checklist results (in-memory if just produced, from the folder log if invoked manually). Rank gaps by severity using this order:

1. Hard-requirement misses (every miss is in scope, no top-N cutoff)
2. High-stakes quality dimensions at fail (per `references/verdict-rollup-thresholds.md` and the per-type heuristics — these are the verdict-elevating items)
3. Quality dimensions at fail
4. Discipline-rule violations that elevate verdicts (3+ violations bumping severity)
5. Quality dimensions at partial
6. Discipline-rule violations not elevating verdicts

Take the top-N for the artifact type (per `references/research-budget-per-type.md`). For most types N=5; for source notes and small notes N=3.

**Stop condition.** If fewer gaps were surfaced than N, take them all. Don't pad. If zero gaps were surfaced (the verdict was PASS and the operator forced Mode 4), pick the top-N quality dimensions even though they passed — Mode 4 on PASS targets quality dimensions where partial-score is already implicit "could be strengthened."

#### Step 2 — Formulate a research question per gap

For each gap, write one research question of the form: **"What's the strongest version of [claim / pattern / argument / section] in current published work?"** Be specific:

- For a hard-requirement miss (missing schema field): "What's the canonical shape of the [missing field] in current Schema.org documentation for [entity type]?"
- For a quality-dimension fail (low attribute density): "What's the highest-attribute-density published version of [section topic] currently ranking on [target SERP / cited by Perplexity]?"
- For a discipline-rule violation: "What's the best practice for [discipline rule topic] in current published work on [artifact type]?"

Use the per-artifact-type strategy in `references/evaluation-heuristics-by-type.md` § "Auto-research strategy" — each type has its own characteristic gap shapes and the strategy section names the right query templates.

**Cache check.** If two gaps share the same question shape, merge them. Run the query once and attribute the answer to both gaps in Step 4.

**Stop condition.** N questions written (or fewer if N gaps were merged through cache check).

#### Step 3 — Invoke `perplexity-refinement` as a subroutine

For each unique research question, invoke `perplexity-refinement` with:

- **Target artifact path:** the artifact being evaluated (the same one EVALUATE just ran on)
- **Refinement depth:** `light` (3-query cap) by default for recursive composition. Operator can override to `medium` on a per-gap basis if a gap warrants deeper triangulation.
- **Refinement mode:** `append` (Mode 4 doesn't want body edits — it wants research findings it can interpret)
- **Specific focus area:** the research question text from Step 2

The recursive `perplexity-refinement` call inherits the Perplexity Sonar contract: Sonar API → refusal. If it refuses, Mode 4 surfaces the refusal to the operator and stops.

Compose with **type-specific sibling skills** where they exist (per `references/evaluation-heuristics-by-type.md`):

- **Core 30 page:** also compose with `competitor-deep-research` for SERP-level comparison (its own Perplexity queries count against the per-artifact cap)
- **Cluster synthesis:** also compose with `multi-source-synthesis` review-agent mode for additional pattern-math triangulation
- **SKILL.md:** Perplexity Pro queries about skill-design literature and agent-skill conventions (no specific sibling skill yet)
- **Brief:** target sections marked "operator follow-up pending" or "AI surfaces not reachable from Cowork" — those gaps now ARE reachable through Perplexity Pro
- **Refinement output:** recursive composition with `perplexity-refinement` itself (deeper triangulation on the gaps the first pass left)

**Stop condition.** All N queries run, OR three consecutive `inconclusive` verdicts surface, OR `perplexity-refinement` refuses, OR the operator overrides mid-run. Per the termination rules in `references/research-budget-per-type.md`.

#### Step 4 — Compare findings against the artifact

For each query result, do a side-by-side:

- What does the artifact currently say or do for this gap?
- What does the strongest published version say or do?
- What's the gap between them?

Land the comparison in one sentence per gap of the form: **"Claim X in [section] could be strengthened by citing [source] which [adds / changes / contradicts] [specific finding]. Section Z misses the framing the strongest published work uses ([describe framing])."**

If the verdict was `validates` and the artifact already cites the strongest source, the gap is closed — no elevation suggestion needed for this gap. Record "Validated by external source" in the folder log and move on.

If the verdict was `inconclusive` (Perplexity couldn't find authoritative published work on this gap), surface that explicitly. Don't fabricate an elevation suggestion. Record "External research inconclusive — gap may not be externally researchable" in the folder log.

**Stop condition.** All query results processed; per-gap elevation sentences written for the gaps with research findings.

#### Step 5 — Surface elevation suggestions

Group the per-gap elevation sentences into a structured block to feed Mode 2. The block carries:

- The gap (one line, copied from Step 1)
- The strongest source surfaced (URL + one-line characterization)
- The elevation suggestion (the comparison sentence from Step 4, plus a concrete "add this, change that, cite this source" edit)

This block becomes the new "Elevation suggestions from auto-research" section in the revision prompt template (see `references/revision-prompt-template.md`).

#### Step 6 — Integrate into Mode 2's revision prompt

If Mode 2 has already produced its prompt (auto-fired after Mode 1's verdict), reopen it and add the new section. If Mode 2 hasn't fired yet (Mode 4 ran on PASS at operator opt-in), generate the prompt now with the elevation suggestions in place — the prompt is the artifact even when the verdict was PASS, because it tells the producing chat how to elevate further.

The revision prompt's tone stays neutral and instructional. The elevation suggestions read as "the strongest published version uses framing X; consider adopting it" — not "your version is worse than X."

#### Step 7 — Record the external research in the folder log

Per `references/folder-quality-log-shape.md` and `references/research-budget-per-type.md` § "Tracking and audit":

1. **Locate the artifact's per-artifact section** in `<folder>/_quality-log.md` (already exists from Mode 1).
2. **Append a new `### External research (Mode 4)` sub-section** beneath the iteration entry that triggered Mode 4. Shape per `references/research-budget-per-type.md`:

```markdown
### External research (Mode 4) — YYYY-MM-DD

**Path used:** Sonar API (`sonar-pro` or `sonar`)
**Queries run:** N of cap N (top M of top-N gaps researched; K gaps skipped per termination rule)
**Cost incurred:** ~$X.XX

**Per-gap queries:**

1. **Gap:** <one-line gap from EVALUATE>
   - **Query:** "<query as run>"
   - **Verdict:** validates / partially-validates / contradicts / inconclusive
   - **Strongest source surfaced:** [URL]
   - **Elevation suggestion:** <comparison sentence + concrete edit>
2. ...

**Cache hits:** N (queries reused from earlier in this iteration)
**Termination reason:** "Top-N gaps covered" | "3 inconclusive results" | "Perplexity Sonar unavailable" | "Operator override"
```

3. **Update the artifact's frontmatter** to add (or update) `auto-research-last-run: YYYY-MM-DD` and `auto-research-path: sonar-pro | sonar`. These are read by Phase 6 (auto-approve thresholds) when calibrating confidence. (Historical note: pre-2026-06-01 versions used `auto-research-path: A | B`; Path A was removed.)

4. **The artifact's main frontmatter `last-verdict:` field is not touched by Mode 4** — it carries the EVALUATE verdict from Mode 1. Mode 4's findings shape the next iteration's regeneration; the next EVALUATE pass produces the next `last-verdict:`.

**Stop condition.** Folder log written, frontmatter updated, revision prompt updated. Mode 4 done.

---

### Mode 5 — AUTO-APPROVE-AND-ESCALATE (the operator-bottleneck mode)

The judgment mode. Modes 1–4 evaluate fit and elevate quality; Mode 5 decides what happens with the verdict. High-confidence PASS verdicts ship without operator review. Low-confidence PASS, NEEDS REVISION, FAIL, and 3-iteration stalls escalate to the operator on two paths (light vs hard) with full diagnostic.

Mode 5 turns the loop from "operator reviews every verdict" into "operator reviews only the verdicts that need judgment." The cost of being wrong is bounded — operator can override any auto-approve, any escalation, any threshold.

**Trigger phrases:**

- Auto-fires as the third step of Mode 1, after the verdict + folder-log write (and after Mode 4 if Mode 4 ran)
- Manual: "Run Mode 5 on `<artifact-path>`" — re-evaluates the auto-approve decision against the current calibration table without re-running Mode 1

**Critical behavior for Mode 5:**

- **Confidence is per-type, not global.** A PASS at 95 on a refinement output is a different decision than a PASS at 95 on a Core 30 page. Read `references/confidence-calibration.md` for the per-type thresholds; don't apply a uniform cutoff.
- **The auto-approve gate reads the artifact's own frontmatter, not the folder log.** Same pointer pattern as Phase 3's publish gate. Mode 5 writes `last-confidence-score:` into frontmatter; downstream gates read it from there. The folder log holds the archaeology, not the gate signal.
- **Operator overrides are first-class events, not edge cases.** `--bypass-confidence`, `--force-escalate`, `--escalate "<reason>"` all leave audit records in the folder log under `### Operator override`. The Phase 5 `--bypass-quality-loop` pre-existing flag continues to skip the whole loop with its own audit record. See `references/operator-controls.md` for the full flag set.
- **Light vs hard escalation are different surfaces.** Light escalation surfaces in the producing folder's `_escalation-queue.md` — borderline PASS verdicts and NEEDS REVISION verdicts that came in below the auto-revise threshold land there for operator review. Hard escalation surfaces in `_meta/escalations/escalation-YYYY-MM-DD-<artifact-slug>.md` PLUS as a tracker row in `_active-chats-tracker.md` § "Hot decisions sitting on Oliver's plate" — FAIL verdicts and 3-iteration stalls land there.
- **Conservative-by-default during the calibration window.** The starter thresholds in `references/confidence-calibration.md` are intentionally tight (Core 30 95 / cluster 90 / SKILL.md 90 / tactic 85 / brief 85 / refinement 80). Quarterly refresh tunes them based on real operator-agreement rates. Skewing toward more escalations during the early-data window is the right trade-off.

**Workflow:** 5 steps. Each step has a stop condition; honor it.

#### Step 1 — Compute the confidence score

Inputs (per `references/confidence-calibration.md` § "How the score is computed"):

1. **Hard-requirement margin** — how comfortably the artifact cleared (or missed) hard requirements
2. **Quality-dimension margin** — how far above (or below) the verdict's quality-dimension threshold
3. **Discipline-rule cleanliness** — zero violations vs minor vs severe
4. **Iteration position** — first-iteration verdict vs third-iteration verdict
5. **Spec-routing coverage** — all routed spec sources loaded cleanly vs missing or stale sources

Weighted average per the per-type weights in the calibration table. Rounded to nearest integer. Result is a number 0–100.

Apply the elevation rules from `references/confidence-calibration.md` § "How the score elevates or de-elevates":

- Spec-routing coverage gap → score capped at 70 (regardless of weighted average)
- Third-iteration PASS verdicts capped at PASS-confidence anchor minus 5
- Mode 4 "validates" on every gap → +5
- Mode 4 "inconclusive" on 3+ gaps → −10

**Stop condition.** Final confidence score computed.

#### Step 2 — Write the score to frontmatter + folder log

1. **Artifact frontmatter** gains a fourth quality-tracking field:

   ```yaml
   last-confidence-score: 95
   ```

   This sits alongside the three Mode 1 fields (`quality-log:`, `last-evaluated:`, `last-verdict:`).

2. **Folder log per-artifact section's Latest line** extends with confidence:

   ```markdown
   **Latest:** PASS (2026-05-28) — iteration 1 of 3 — confidence 95
   ```

3. **Folder log iteration entry metadata block** gains a Confidence line:

   ```markdown
   **Confidence:** 95 (PASS anchor 80; +10 hard-requirement margin; +5 spec-routing coverage clean; +0 iteration position; +0 Mode 4 not run)
   ```

   The breakdown is one line per non-zero input contribution. If a contribution was zero, omit it from the breakdown (don't pad).

**Stop condition.** Frontmatter updated, Latest line updated, iteration metadata block updated.

#### Step 3 — Apply the auto-approve gate

Read the per-type auto-approve threshold from `references/confidence-calibration.md` § "Per-artifact-type calibration."

For the artifact:

- **Verdict is PASS AND confidence ≥ threshold** → auto-ship. Skip to Step 5.
- **Verdict is PASS AND confidence < threshold** → light escalation. Continue to Step 4 with the light path.
- **Verdict is NEEDS REVISION (minor) AND iteration < 3** → not Mode 5's problem (Mode 2 loops it; Mode 5 fires next iteration).
- **Verdict is NEEDS REVISION (substantive) AND iteration < 3** → not Mode 5's problem (Mode 2 loops it).
- **Verdict is NEEDS REVISION (any tier) AND iteration = 3** → hard escalation (3-iter stall). Continue to Step 4 with the hard path.
- **Verdict is FAIL** → hard escalation regardless of iteration. Continue to Step 4 with the hard path.
- **Operator flagged `--force-escalate`** → light escalation regardless of confidence.
- **Operator flagged `--bypass-confidence`** → auto-ship regardless of confidence; record the override.
- **Operator flagged `--escalate "<reason>"`** → hard escalation regardless of verdict; record the reason.

**Stop condition.** Auto-approve decision made; the artifact is routed to ship / light / hard.

#### Step 4 — File the escalation (light or hard)

##### Light escalation path

1. **Locate or create `<folder>/_escalation-queue.md`.** Same folder as the artifact. Same convention as `_quality-log.md` — underscore prefix.
2. **Append a row to the "Awaiting review" section** per the shape in `references/operator-controls.md` § 5:

   ```markdown
   ### <artifact-slug>
   - **Verdict:** PASS | NEEDS REVISION (minor) | NEEDS REVISION (substantive)
   - **Confidence:** 78 (threshold 85 for type `tactic-note` — below by 7)
   - **Path:** `<absolute-path>`
   - **Folder log:** [[_quality-log#<artifact-slug>]]
   - **Revision prompt:** `<artifact-path>.revision-prompt.md` (when verdict ≠ PASS)
   - **Recommended action:** ship | revise | regenerate
   - **Why escalated:** confidence below auto-approve threshold | high-stakes dimension partial | operator forced
   ```

3. **Emit a stdout notification** to the operator naming the artifact + revision prompt path + recommended action.

##### Hard escalation path

1. **Create `_meta/escalations/escalation-YYYY-MM-DD-<artifact-slug>.md`** per the file shape in `_meta/escalations/_README.md`. Includes full verdict summary quoted verbatim from the folder log + iteration history when 3-iter stall + recommended next steps.
2. **Add a row to `_meta/handoffs/_active-chats-tracker.md` § "Hot decisions sitting on Oliver's plate"** with a one-line summary referencing the escalation file. Bump tracker `last-change:` per the standard tracker-edit pattern.
3. **Emit a stdout notification** naming both files.

**Stop condition.** Escalation files written, tracker updated (hard path only), operator notified.

#### Step 5 — Record the auto-approve audit (when auto-shipped)

When the artifact auto-ships (Step 3 decision was "auto-ship"), append a `### Auto-ship audit — YYYY-MM-DD` H3 section to the artifact's per-artifact section in the folder log. Shape:

```markdown
### Auto-ship audit — YYYY-MM-DD HH:MM

**Verdict:** PASS
**Confidence:** 95
**Threshold:** 95 (type: Core 30 page draft)
**Decision:** auto-ship — confidence at or above threshold
**Override flag:** none | `--bypass-confidence` | `--force-escalate` (but suppressed because... — only fires when an override is in play)
**Downstream gate:** publish-core-30-page.py reads `last-verdict: PASS` + `last-confidence-score: 95` from frontmatter
```

This is the auto-ship paper trail. The Phase 5 dashboard's "auto-shipped vs escalated" distribution Dataview-queries this section across folders.

**Stop condition.** Audit section appended. Mode 5 done.

---

## Evaluation report format

Every Mode 1 run produces a report in this exact shape (mirrors what gets written to the folder log):

```markdown
# Quality-loop evaluation — <artifact-path>

**Evaluated:** YYYY-MM-DD HH:MM
**Artifact type:** <detected-type>
**Spec sources loaded:** [<source1>, <source2>, ...]
**Verdict:** PASS | NEEDS REVISION (minor) | NEEDS REVISION (substantive) | FAIL
**Iteration:** N of 3

## Hard requirements
- [✓] Frontmatter present and well-formed — `type: source` + required fields
- [✓] Required sections all present — TLDR, Take-away, Tools mentioned, ...
- [✗] Schema validation — missing `aggregateRating` block (spec source: `_template-service-brief.md` §4.5 F)
- ...

## Quality dimensions
- [✓] Citation density: 12 inline citations vs target of 10+ (PASS) (spec source: `_template-service-brief.md` §14)
- [Partial] Plain language compliance: 3 jargon-heavy sentences flagged (NEEDS POLISH) (spec source: `plain-language-conventions.md`)
- [✗] Attribute density: 1 named brand in problem cards vs target of 3+ (FAIL) (spec source: `_template-service-brief.md` §4.5 C)
- ...

## Discipline rules
- [✓] Non-destructive editing: original content preserved
- [✓] Plain-language conventions honored
- ...

## Root cause (only when FAIL or substantive revision)
<one-paragraph explanation of why the bar was missed — be specific>

## Suggested fixes
1. <specific edit>
2. <specific edit>
3. ...
```

The "Suggested fixes" section feeds Mode 2's revision prompt directly.

---

## Spec routing — high-level

The full routing table lives in `references/spec-routing-table.md`. The initial type set this skill supports:

| Artifact type | Detection signal | Spec sources loaded |
|---|---|---|
| Core 30 page draft | path matches `**/website-archive/new/core-30/**/draft-*.{html,md}` | service brief + intersection brief + city data + client data + plain-language conventions + SEO primer §G + AI-citation §4.5 + per-page refinement notes |
| Perplexity-refinement output | source note with "Perplexity refinement" section appended | perplexity-refinement SKILL.md + query-templates.md + original source note + plain-language conventions |
| Cluster synthesis | path matches `**/cluster-synthesis-*.md`, frontmatter `type: synthesis` | multi-source-synthesis SKILL.md + every source in `related:` + intel-routing spec + conventions.md synthesis-shape rules |
| Cross-cluster synthesis | path matches `_meta/synthesis/cross-cluster-synthesis-*.md` | multi-source-synthesis SKILL.md + cluster summaries cited + conventions.md cross-cluster rules |
| SKILL.md | path matches `~/workspace/skills/*/SKILL.md` | conventions.md skills section + 2–3 reference skills (perplexity-refinement, multi-source-synthesis, house-voice-rewrite) |
| Research brief (service / city / intersection / client) | path matches `**/research-briefs/**/*.md`, frontmatter `type: research-brief` | brief's template file + the brief's consumption-contract table |
| Tactic note | path matches `**/03_domains/**/tactics/tactic-*.md`, frontmatter `type: tactic` | conventions.md artifact rules + promotion-threshold rules + every source cited |
| Tool note | path matches `**/03_domains/**/tools/tool-*.md`, frontmatter `type: tool` | conventions.md artifact rules + every source cited |
| Pattern note | path matches `**/05_shared-intelligence/patterns/pattern-*.md`, frontmatter `type: pattern` | conventions.md artifact rules + promotion-threshold rules + every source cited |
| Lesson note | path matches `**/05_shared-intelligence/lessons/lesson-*.md`, frontmatter `type: lesson` | conventions.md artifact rules + every source cited |
| Source note (VIS ingestion) | path matches `**/insights/source-*.md`, frontmatter `type: source` | vis-extraction SKILL.md + source-note conventions + plain-language conventions |
| Blueprint | path matches `**/blueprints/blueprint-*.md`, frontmatter `type: blueprint` | multi-source-synthesis SKILL.md + every cited artifact + conventions.md blueprint-shape rules |

When operator overrides with explicit spec sources, the routing table is bypassed.

---

## Cost-management rules

Mode 1 (EVALUATE) is cheap — it reads files and runs heuristics. The only cost surface is when Mode 1 needs to fetch a spec source from outside the vault (e.g., a citation URL the artifact references). For v1, external fetches are **not** part of Mode 1; the skill evaluates against vault-resident specs only.

Mode 2 (REVISE-PROMPT) is free.

Mode 3 (AUTO-INVOKE-CONVENTION) runs Mode 1 N times — same cost surface, multiplied by N.

Mode 4 (AUTO-RESEARCH) is the meaningful cost surface. Every Mode 4 run composes with `perplexity-refinement`, which routes through Path A (Claude in Chrome / Pro Search) → Path B (Sonar API) → refusal. Each query consumes either a Pro credit (Path A) or a per-query Sonar charge (Path B). Per-artifact-type caps live in `references/research-budget-per-type.md`; hard ceiling is 8 queries per artifact regardless of type. Suite-wide cost rules apply per `~/workspace/skills/perplexity-shared/references/perplexity-cost-rules.md`. See Mode 4 § "Critical behavior" for the refusal-vs-fallback contract.

The cap discipline (3 iterations per artifact, plus 8-query hard ceiling per Mode 4 run) is the load-bearing cost control. Don't let a loop run forever; don't let auto-research spend its way past the per-type budget.

---

## Plain-language requirement

Per [[plain-language-conventions]] and the standing `feedback_plain_language_default.md` memory: write the evaluation report and the revision prompt in plain language. Short sentences. Conversational rhythm. Gloss obscure terms inline the first time they appear. Keep technical terms when they're the actual subject (e.g., "FAQPage schema" stays "FAQPage schema").

The artifact being evaluated may itself be dense (a synthesis, a brief, a primer). The evaluation report sits outside the artifact and follows plain-language by default. If the operator wants a dense version of the report, they can ask explicitly.

---

## Integration with other skills

This skill is the keystone of the output-quality-loop system. Phases 2-6 of the roadmap describe how it composes with the rest of the Knowledge OS skill set.

### Phase 2 retrofits (perplexity-refinement, multi-source-synthesis)

After Phase 2 ships, both of these skills emit the auto-invoke convention block at completion. The producing chat reads the block, calls this skill via Mode 3, and loops on revision prompts until PASS or escalation.

### Phase 3 publish gate (Core 30 pages)

`scaffold-core-30-page.py` + `bulk-scaffold-pages.py` + `publish-core-30-page.py` route every page through Mode 1 before publish. The publish gate reads the artifact's `last-verdict:` frontmatter field (with a 7-day staleness window) and refuses to publish anything not at PASS.

### Phase 4 auto-research mode (shipped as Mode 4 in v1.1, 2026-05-28)

Adds the "what's the strongest version of this in the world?" pass as Mode 4 above. Composes with `perplexity-refinement` (Sonar API on `sonar-pro` per the post-2026-06-01 path; the architecture decision originally specified browser-driven Perplexity Pro but Path A was removed 2026-06-01) for external benchmarking. Routes through the Perplexity Sonar contract — no silent fallback to Cowork WebSearch at any layer. Per-artifact-type caps in `references/research-budget-per-type.md`; per-type research strategies in `references/evaluation-heuristics-by-type.md` § "Auto-research strategy" subsections.

### Phase 5 convention rollout

Every artifact-producing skill in the vault emits the auto-invoke block at completion. The convention becomes the default; this skill is the universal evaluator.

### Phase 6 auto-approve thresholds (shipped as Mode 5 in v1.2, 2026-05-28)

Adds a numeric confidence score per evaluation. High-confidence PASS verdicts ship without operator review; everything else queues for human judgment on one of two surfaces (light escalation in the producing folder's `_escalation-queue.md`; hard escalation in `_meta/escalations/escalation-*.md` plus a row in the master tracker's "Hot decisions" section). Frontmatter gains `last-confidence-score: <0-100>` alongside the Mode 1 three-field set. Per-type thresholds + score math + calibration history live in `references/confidence-calibration.md`; operator override flags and clearing workflows live in `references/operator-controls.md`. Conservative starter thresholds (Core 30 95 / cluster 90 / SKILL.md 90 / tactic 85 / brief 85 / refinement 80) anchor against the sparse Phase 1–5 calibration data; quarterly refresh tunes them against accumulated operator-agreement signal.

---

## Output contract

Every Mode 1 invocation produces exactly these artifacts:

1. **Evaluation report** — emitted to the operator (and to the producing chat in auto-invoke mode).
2. **Folder log update** — new iteration entry appended to the per-artifact section in `<folder>/_quality-log.md`; folder log created if absent.
3. **Artifact frontmatter update** — `quality-log:`, `last-evaluated:`, `last-verdict:` fields added or updated on the artifact being evaluated.
4. **Revision prompt (when verdict ≠ PASS)** — emitted to stdout; written to `<artifact-path>.revision-prompt.md` if the operator named a path or auto-invoke mode is active.
5. **External-research findings (when Mode 4 fires)** — appended as a `### External research (Mode 4)` sub-section to the artifact's per-artifact section in the folder log; elevation suggestions integrated into the revision prompt's "Elevation suggestions from auto-research" section; `auto-research-last-run:` + `auto-research-path:` added to artifact frontmatter.
6. **Confidence score (when Mode 5 fires)** — `last-confidence-score: <0-100>` added to artifact frontmatter; folder log Latest line and iteration metadata block both name the score; auto-approve decision routed to ship / light-escalate / hard-escalate.
7. **Auto-ship audit (when Mode 5 decides auto-ship)** — `### Auto-ship audit — YYYY-MM-DD` sub-section appended to the artifact's per-artifact section in the folder log naming the threshold + decision + downstream gate.
8. **Light escalation queue (when Mode 5 light-escalates)** — row added to `<folder>/_escalation-queue.md` § "Awaiting review" naming the artifact + confidence + recommended action + revision prompt path. File created if absent.
9. **Hard escalation file (when Mode 5 hard-escalates)** — `_meta/escalations/escalation-YYYY-MM-DD-<artifact-slug>.md` created with full diagnostic; row added to `_active-chats-tracker.md` § "Hot decisions sitting on Oliver's plate"; tracker `last-change:` bumped.
10. **Terse completion summary in chat** — per the standing `feedback_terse_completion_reports.md` memory:
   - Verdict + iteration count + confidence score (Mode 5)
   - Auto-ship / light-escalate / hard-escalate decision (Mode 5)
   - 2-3 top fixes if revision needed
   - File paths touched

The summary doesn't restate the full evaluation — the report itself is the artifact.

---

## Verification before declaring done

Before reporting completion to the operator:

1. **Frontmatter check** — the artifact's frontmatter has `quality-log:`, `last-evaluated:`, `last-verdict:` and valid YAML.
2. **Folder log check** — `<folder>/_quality-log.md` exists; per-artifact section has the new iteration entry; "Latest:" line updated; frontmatter counters incremented.
3. **Citation check** — every checklist item in the evaluation report cites its spec source by file + section.
4. **Plain-language check** — pick the densest paragraph of the evaluation report and confirm it reads conversationally.
5. **Cap check** — if this is iteration 3 and verdict ≠ PASS, the escalation report is emitted, not a new revision prompt.
6. **Mode-4 budget check** — if Mode 4 ran, the per-artifact query count is at or under the cap in `references/research-budget-per-type.md`; the `Path used:` line is named (Sonar API + model); the `Termination reason:` line is named; the elevation suggestions cite their Perplexity-surfaced URLs.
7. **Mode-4 refusal check** — if `perplexity-refinement` returned the refusal message during Mode 4, the folder log records the refusal and the revision prompt does NOT include fabricated elevation suggestions sourced from vault-internal content.
8. **Non-destructive check** — the artifact body is unchanged. Only the frontmatter fields (the three Mode-1 fields plus the two Mode-4 fields when applicable plus the `last-confidence-score:` field when Mode 5 ran) were touched.
9. **Mode-5 confidence check** — if Mode 5 ran, the artifact's frontmatter has `last-confidence-score: <0-100>`; the folder log's Latest line names the confidence; the iteration metadata block has a Confidence breakdown line. The score is consistent across the three places.
10. **Mode-5 escalation check** — if Mode 5 escalated (light or hard), the relevant escalation surface exists (`<folder>/_escalation-queue.md` for light; `_meta/escalations/escalation-*.md` PLUS a tracker row for hard); the operator notification was emitted to stdout. If Mode 5 auto-shipped, the `### Auto-ship audit` section was appended to the artifact's folder-log section.

---

## Out of scope (v1.0)

- **Auto-research on PASS verdicts by default.** Mode 4 fires on NEEDS REVISION / FAIL by default. The operator can opt in for PASS via "with depth=deep" but the default skips it to keep the loop fast.
- **Re-running auto-research within the same loop iteration.** One Mode 4 run per iteration. If iteration 2 surfaces fresh gaps, Mode 4 fires again on iteration 2 — but never twice within iteration 1.
- **Cross-artifact cache reuse.** Mode 4's cache is per-iteration-on-one-artifact. Reusing a query result across separate artifacts would silently drop attribution discipline.
- **Body editing.** v1 never touches the artifact body. Future phases may add a "body fix proposal" mode, but it would still be operator-gated.
- **Multi-LLM verdict consensus.** Single evaluator. No parallel scoring across models.
- **Cross-folder log consolidation.** The Dataview dashboard at `_meta/dashboards/quality-loop-dashboard.md` (skeleton shipped Phase 1) aggregates state; the skill itself doesn't reach across folders.
- **Auto-tuning thresholds based on operator overrides.** Phase 6 v1.2 calibrates manually via the quarterly refresh in `references/confidence-calibration.md`. Auto-tuning (learning new thresholds from override patterns) is future work.
- **Operator-side escalation UI.** Escalations surface as markdown files (`_escalation-queue.md` per folder; `_meta/escalations/escalation-*.md` for hard escalations) and tracker rows. A dedicated UI for managing the queue is future work.
- **Cross-artifact-type confidence generalizations.** Each artifact type carries its own calibration row; no shared confidence-anchor logic. Generalizing across types is future work.

---

## Reference files

When you need them, read these:

- `references/artifact-type-detection.md` — the detection table (path patterns + frontmatter signals → artifact type)
- `references/spec-routing-table.md` — the artifact-type → spec-sources table
- `references/evaluation-heuristics-by-type.md` — per-artifact-type quality dimensions + discipline rules + hard requirements
- `references/auto-invoke-convention.md` — the convention spec for other skills to include the auto-invoke block at completion
- `references/revision-prompt-template.md` — the template Mode 2 uses to produce revision prompts
- `references/verdict-rollup-thresholds.md` — the per-verdict threshold rules (PASS / REVISION-minor / REVISION-substantive / FAIL)
- `references/folder-quality-log-shape.md` — the folder-level `_quality-log.md` file structure, frontmatter, per-artifact section shape, and the artifact's own frontmatter pointer convention
- `references/research-budget-per-type.md` — Mode 4 cost discipline: per-artifact-type query caps, top-N gap selection, cache reuse rules, termination conditions, audit-trail shape
- `references/confidence-calibration.md` — Mode 5 score math + per-artifact-type auto-approve thresholds + score-elevation rules + calibration history (updated quarterly)
- `references/operator-controls.md` — Mode 5 operator override flags + manual escalation + threshold-adjustment workflow + escalation-clearing workflow

---

## Maintenance notes

### M1: Spec routing gaps (added 2026-05-27, v1.0)

**The issue:** A new artifact type appears in the vault (Phase 1 introduces type X), and the spec-routing table doesn't have a row for it.

**How it surfaces:** Mode 1 Phase 1 (detection) returns no match, or matches a too-generic row.

**How to fix:** Surface the gap to the operator: "I can't detect the artifact type, or the routing table has no spec sources for it. Tell me the type + spec sources, or extend the routing table." Don't guess.

### M2: Stale spec sources (added 2026-05-27, v1.0)

**The issue:** A spec source the routing table points at gets renamed, moved, or deleted.

**How it surfaces:** Phase 2 (spec-source loading) returns "file not found" on a routed spec source.

**How to fix:** Surface the gap to the operator. Don't fall back to a neighbor spec. Update the routing table when the operator confirms the new path.

### M3: Verdict drift (added 2026-05-27, v1.0)

**The issue:** Over time, the skill's verdicts drift — too many PASS, too many FAIL, too many borderline-revision verdicts that should have been one or the other.

**How it surfaces:** The folder log's frontmatter counters skew unusually. The Dataview dashboard at `_meta/dashboards/quality-loop-dashboard.md` shows lopsided distributions.

**How to fix:** Re-calibrate the heuristics. Pull the last 10 evaluations across types, compare verdicts against the operator's manual judgment, adjust `references/evaluation-heuristics-by-type.md` and `references/verdict-rollup-thresholds.md` accordingly. Don't quietly drift the bar.

### M5: Mode 4 budget creep (added 2026-05-28, v1.1)

**The issue:** Mode 4 consistently spends the full per-type cap on artifacts that surface only 2-3 real gaps. Queries are being padded to fill the budget; elevation suggestions read as filler.

**How it surfaces:** Folder log entries show "Queries run: 8 of cap 8" on most Mode 4 runs; elevation suggestions for the bottom 2-3 gaps add nothing concrete the producing chat can act on.

**How to fix:** Reread `research-budget-per-type.md` § "Termination rules (when to stop auto-research within a single run)." Rule #1 is "Top-5 gaps already covered — if EVALUATE surfaced only 3 gaps, run only 3 queries." Mode 4 isn't honoring the rule. Calibrate by hand on the next 3 runs (force-stop after the real gaps); update the rule's wording if the rule itself is ambiguous.

### M6: Cowork WebSearch substitution at the Mode 4 layer (added 2026-05-28, v1.1)

**The issue:** Mode 4 silently fell back to Cowork `WebSearch` when `perplexity-refinement` refused. The folder log shows queries run but the source ranking doesn't match Perplexity Pro's curated AI-overview synthesis.

**How it surfaces:** The `Path used:` line in the folder log says "Sonar API" but the cited sources are generic web results, not Perplexity-Sonar-curated sources. Or the line is missing entirely.

**How to fix:** The refusal step in `perplexity-refinement` is structural — it's supposed to make this impossible. If Mode 4 is bypassing the refusal, it's calling some other research tool directly. Find the call site, route it through `perplexity-refinement`, and verify the refusal cascades. This is the same failure mode that caused Wave 0 of `perplexity-refinement` to silently substitute Cowork `WebSearch` — the Phase 2 fix to `perplexity-refinement` doesn't help if Mode 4 dodges around it. (Historical note: pre-2026-06-01 versions of this entry referenced `Path A` instead of `Sonar API` — that path was removed.)

### M7: Calibration drift on confidence scores (added 2026-05-28, v1.2)

**The issue:** Mode 5's confidence scores drift away from operator-agreement rates over time. The auto-approve gate ships artifacts the operator would have escalated, or escalates artifacts the operator would have shipped.

**How it surfaces:** Per-type override rate (operator manually flipping the Mode 5 decision via `--bypass-confidence` or `--force-escalate`) exceeds 10% over a trailing 30-day window. The dashboard at `_meta/dashboards/quality-loop-dashboard.md` surfaces the threshold-tune candidate. Or: an auto-shipped artifact gets reverted within 48 hours of publish.

**How to fix:** Trigger a non-quarterly calibration refresh per `references/confidence-calibration.md` § "When to recalibrate." Either retune the auto-approve threshold (column 1 of the calibration table) or retune the per-type anchors (columns 2-4) depending on whether the issue is gate-level or score-level. Add the refresh to the calibration history table at the bottom of the file.

### M8: Auto-shipped artifact reverted post-ship (added 2026-05-28, v1.2)

**The issue:** Mode 5 auto-shipped an artifact at high confidence; downstream consumer (publish gate, scaffolder, deployment) revealed a problem the loop didn't catch.

**How it surfaces:** The artifact's `last-confidence-score:` is at or above the per-type threshold, but the operator reverted the publish or rolled back the deploy within 48 hours. The folder log's `### Auto-ship audit` section is now misleading.

**How to fix:** (1) Append a `### Post-ship correction` H3 section under the artifact's per-artifact section in the folder log naming what the loop missed and how the issue was discovered. (2) Trigger M7 — calibration drift — and lower the per-type auto-approve threshold by 5 points (Core 30 95 → 100, etc.) until the next quarterly refresh. The dataset is now telling us the prior threshold was too low. (3) If the gap the loop missed is a spec-source gap (the artifact passed every loaded spec, but a relevant spec wasn't in the routing table), trigger M1 — spec-routing gaps — and extend the routing table.

### M4: Iteration cap stalls (added 2026-05-27, v1.0)

**The issue:** An artifact runs three iterations and never reaches PASS. The producing chat keeps regenerating; the same gaps reappear.

**How it surfaces:** The folder log shows three iteration entries for the same artifact with similar revision prompts.

**How to fix:** The escalation report goes to the operator. The operator either (a) edits the artifact directly, (b) extends the spec source so the producing chat has clearer guidance, or (c) deems the artifact "good enough" and overrides the verdict manually. The skill doesn't run a fourth iteration.

---

## How to add a new maintenance note

When the skill errors or produces a miss in production, add a new entry: **Issue → How it surfaces → How to fix → Why it wasn't designed away.** Date-stamp the entry. Future-Claude learns from past misses without re-hitting the same wall.

---

### M-catchall: Catch-all routing for unrouted types (added 2026-06-08, v1.3)

**The change:** `spec-routing-table.md` now has a catch-all entry that fires when no artifact type matches. Previously, unrouted types caused the quality loop to surface a gap and stop. Now, unrouted types get a baseline evaluation against 3 project-agnostic spec sources (plain-language-conventions, conventions, CLAUDE.md) + conservative confidence threshold (90 auto-approve, 65 PASS anchor). The catch-all evaluation report flags the missing routing row so it can be added if the type recurs. Companion `confidence-calibration.md` row added. Driven by the mandatory pre-land review gate build (every task must pass quality evaluation, including ad-hoc tasks producing unrouted artifact types).

## See also

- `[[perplexity-refinement]]` — the refinement skill whose output type 1 of this skill's regression tests evaluates
- `[[multi-source-synthesis]]` — the sibling synthesis skill; first Phase 2 retrofit
- `[[service-seo-research]]` — produces research briefs that this skill evaluates
- `[[meta-document-primer]]` — neighbor skill with a similar routing-by-type pattern
- `[[plain-language-conventions]]` — voice rules every evaluation report follows
- `[[conventions]]` — KOS naming and frontmatter rules
- `[[output-quality-loop-folder-readme|_meta/handoffs/output-quality-loop/_README]]` — the project this skill is Phase 1 of
- `[[_template-service-brief]]` — example of a spec the skill routes to when evaluating page outputs
