---
name: output-quality-loop
description: Evaluate a finished Knowledge OS artifact against the specs that define what "good" looks like for its type, produce a structured verdict (PASS / NEEDS REVISION minor or substantive / FAIL), and — when revision is needed — generate a revision prompt the producing chat can ingest to regenerate. Triggers on phrases like "quality-check <artifact-path>," "evaluate <artifact-path>," "run output-quality-loop on <artifact-path>," "is this draft ready to ship," "does this brief meet the spec," "did the refinement pass actually elevate the source note," "audit this synthesis against its sources," or any time the operator wants a structured fitness evaluation of an artifact already on disk. Also fires via the auto-invoke convention block other skills emit at completion (see references/auto-invoke-convention.md). The keystone of the output-quality-loop system; Phases 2-6 of the roadmap build on top of this skill.
---

# Output Quality Loop Skill (v1.0)

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

## Three invocation modes

### Mode 1 — EVALUATE (the core mode)

Reads an artifact, builds the checklist, scores it, writes the verdict to the folder log + the artifact's frontmatter, and produces the evaluation report.

**Trigger phrases:**

- "Quality-check `<artifact-path>`"
- "Evaluate `<artifact-path>`"
- "Run output-quality-loop on `<artifact-path>`"
- The auto-invoke `[output-quality-loop:eval]` directive from another skill (see `references/auto-invoke-convention.md`)

**Operator overrides (bypass the routing table):**

- "Quality-check `<artifact>` against `<spec1>` `<spec2>`" — the named specs are used instead of the auto-routed ones
- "Quality-check `<artifact>` with depth=deep" — runs the auto-research path (Phase 4 mode; for v1 this surfaces as a deferred capability)

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

Mode 1 (EVALUATE) is cheap — it reads files and runs heuristics. The only cost surface is when Mode 1 needs to fetch a spec source from outside the vault (e.g., a citation URL the artifact references). For v1, external fetches are **not** part of Mode 1; the skill evaluates against vault-resident specs only. Phase 4 introduces auto-research mode (which composes with `perplexity-refinement` for external benchmarking) — at that point the cost-management rules in `~/workspace/skills/perplexity-shared/references/perplexity-cost-rules.md` apply.

Mode 2 (REVISE-PROMPT) is free.

Mode 3 (AUTO-INVOKE-CONVENTION) runs Mode 1 N times — same cost surface, multiplied by N.

The cap discipline (3 iterations per artifact) is the load-bearing cost control. Don't let a loop run forever.

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

### Phase 4 auto-research mode

Adds a new "what's the strongest version of this in the world?" pass. Composes with `perplexity-refinement` (browser-driven Perplexity Pro, per the architecture decision) for external benchmarking. Routes through the Perplexity Pro contract — no silent fallback to Cowork WebSearch.

### Phase 5 convention rollout

Every artifact-producing skill in the vault emits the auto-invoke block at completion. The convention becomes the default; this skill is the universal evaluator.

### Phase 6 auto-approve thresholds

Adds a confidence score per evaluation. High-confidence PASS verdicts ship without operator review; everything else queues for human judgment. The frontmatter field set grows to include `quality-confidence:` (high / medium / low).

---

## Output contract

Every Mode 1 invocation produces exactly these artifacts:

1. **Evaluation report** — emitted to the operator (and to the producing chat in auto-invoke mode).
2. **Folder log update** — new iteration entry appended to the per-artifact section in `<folder>/_quality-log.md`; folder log created if absent.
3. **Artifact frontmatter update** — `quality-log:`, `last-evaluated:`, `last-verdict:` fields added or updated on the artifact being evaluated.
4. **Revision prompt (when verdict ≠ PASS)** — emitted to stdout; written to `<artifact-path>.revision-prompt.md` if the operator named a path or auto-invoke mode is active.
5. **Terse completion summary in chat** — per the standing `feedback_terse_completion_reports.md` memory:
   - Verdict + iteration count
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
6. **Non-destructive check** — the artifact body is unchanged. Only the three frontmatter fields were touched.

---

## Out of scope (v1.0)

- **Auto-research / external benchmarking.** Phase 4 work. v1 evaluates against vault-resident specs only.
- **Body editing.** v1 never touches the artifact body. Future phases may add a "body fix proposal" mode, but it would still be operator-gated.
- **Multi-LLM verdict consensus.** Single evaluator. No parallel scoring across models.
- **Cross-folder log consolidation.** The Dataview dashboard at `_meta/dashboards/quality-loop-dashboard.md` (skeleton shipped Phase 1) aggregates state; the skill itself doesn't reach across folders.
- **Confidence-score auto-approval.** Phase 6 work. v1 emits verdicts; the operator decides what to do with NEEDS REVISION outputs.

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

### M4: Iteration cap stalls (added 2026-05-27, v1.0)

**The issue:** An artifact runs three iterations and never reaches PASS. The producing chat keeps regenerating; the same gaps reappear.

**How it surfaces:** The folder log shows three iteration entries for the same artifact with similar revision prompts.

**How to fix:** The escalation report goes to the operator. The operator either (a) edits the artifact directly, (b) extends the spec source so the producing chat has clearer guidance, or (c) deems the artifact "good enough" and overrides the verdict manually. The skill doesn't run a fourth iteration.

---

## How to add a new maintenance note

When the skill errors or produces a miss in production, add a new entry: **Issue → How it surfaces → How to fix → Why it wasn't designed away.** Date-stamp the entry. Future-Claude learns from past misses without re-hitting the same wall.

---

## See also

- `[[perplexity-refinement]]` — the refinement skill whose output type 1 of this skill's regression tests evaluates
- `[[multi-source-synthesis]]` — the sibling synthesis skill; first Phase 2 retrofit
- `[[service-seo-research]]` — produces research briefs that this skill evaluates
- `[[meta-document-primer]]` — neighbor skill with a similar routing-by-type pattern
- `[[plain-language-conventions]]` — voice rules every evaluation report follows
- `[[conventions]]` — KOS naming and frontmatter rules
- `[[output-quality-loop-folder-readme|_meta/handoffs/output-quality-loop/_README]]` — the project this skill is Phase 1 of
- `[[_template-service-brief]]` — example of a spec the skill routes to when evaluating page outputs
