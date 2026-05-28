# Auto-invoke convention

The standard block other skills emit at the end of their work to hand off to output-quality-loop. Phases 2-5 of the output-quality-loop roadmap retrofit existing skills to include this block; Phase 5 makes it the convention every artifact-producing skill follows.

## The block (verbatim)

Other skills emit this block at the end of their closing protocol, after the artifact(s) have been written and before the chat declares done:

```markdown
## Auto-invoke output-quality-loop

This skill produced the following artifact(s):
- `<artifact-path-1>`
- `<artifact-path-2>`

[output-quality-loop:eval] — for each artifact, run output-quality-loop in EVALUATE mode. If PASS, declare the chat done. If NEEDS REVISION or FAIL, ingest the revision prompt as if it were operator input and regenerate the artifact, then re-invoke output-quality-loop. Cap at 3 iterations; on the 3rd FAIL, escalate to the operator with the evaluation report.
```

The block is plain markdown so any chat (Cowork or web-UI Claude) can parse it. The bracketed `[output-quality-loop:eval]` directive is the trigger string Mode 3 listens for.

## Required elements

- **Heading:** `## Auto-invoke output-quality-loop` (exact text, including capitalization)
- **Artifact list:** one bullet per artifact, full path inside backticks
- **Directive line:** opens with `[output-quality-loop:eval]` and includes the iteration-cap discipline

## Optional elements

- **Spec override:** if the producing skill wants the operator to evaluate against specific spec sources, append `against <spec1> <spec2>` to the directive line. Mode 3 reads this and passes the override into Mode 1.
- **Depth flag:** for future Phase 4 auto-research mode, append `depth=deep` to the directive line.

Example with override:

```markdown
## Auto-invoke output-quality-loop

This skill produced the following artifact(s):
- `~/workspace/second-brain/03_domains/seo/insights/source-2026-04-26-jono-catliff-claude-code-seo-50000-clicks-per-month-masterclass.md`

[output-quality-loop:eval against `~/workspace/skills/perplexity-refinement/SKILL.md` `~/workspace/second-brain/_meta/plain-language-conventions.md`] — for each artifact, run output-quality-loop in EVALUATE mode. If PASS, declare the chat done. If NEEDS REVISION or FAIL, ingest the revision prompt as if it were operator input and regenerate the artifact, then re-invoke output-quality-loop. Cap at 3 iterations; on the 3rd FAIL, escalate to the operator with the evaluation report.
```

## How Mode 3 handles the block

1. **Parse the artifact list.** One path per bullet. Paths can be absolute or use the `~/` shortcut.
2. **Parse the directive line.** Pull out the `eval` mode, any `against` overrides, and any flags.
3. **Run Mode 1 (EVALUATE) on each artifact.** Each evaluation is independent.
4. **Aggregate verdicts:**
   - All PASS → emit "All N artifacts passed. Producing chat may declare done."
   - Any NEEDS REVISION / FAIL → list the failing artifacts with their verdicts + a pointer to the revision prompt for each. The producing chat is responsible for ingesting the prompts and regenerating.
5. **Update the folder log** per Phase 6 of Mode 1 for every artifact evaluated.

## The iteration cap (load-bearing)

The cap is **3 iterations per artifact, total**. The producing chat tracks the iteration count by checking the folder log's per-artifact section before regenerating. If three iteration entries already exist and the verdict is still not PASS, the loop escalates instead of regenerating.

The cap exists because:

- Letting the loop run forever burns operator attention with no improvement
- Three iterations is enough to catch most fixable gaps without consuming the artifact's value to over-polish
- The escalation report names the unresolved gaps so the operator can decide: fix manually, extend the spec, or accept the artifact as-is

## Producing-chat responsibilities

The producing chat owns:

- Deciding when to invoke the auto-invoke block (typically at the end of the closing protocol)
- Ingesting the revision prompt as if it were operator input
- Regenerating the artifact per the revision prompt
- Re-invoking the auto-invoke block after regeneration
- Tracking the iteration count
- Declaring done when verdict is PASS or escalation fires

The producing chat does **not** own:

- The verdict itself (this skill emits it)
- The folder log writes (this skill writes them)
- The artifact's frontmatter quality-tracking fields (this skill writes them)

## When NOT to emit the block

Some skills produce ephemeral artifacts (a one-off summary in chat, a quick calculation) that don't warrant quality-loop evaluation. The convention covers artifact-producing skills that write to disk. Skills that don't write to disk, or whose outputs are explicitly transient, don't emit the block.

If a skill writes to disk but its output type isn't in the routing table, emit the block anyway — Mode 1 will surface the gap, and the operator can either name a type, extend the routing table, or skip the evaluation.

## Retrofit checklist (for Phase 2-5)

When retrofitting an existing skill to emit the auto-invoke block:

1. **Identify the artifact path(s).** The skill's completion report already names them; surface them as a bulleted list.
2. **Append the block** to the end of the skill's closing protocol or final report section.
3. **Test once manually.** Run the skill end-to-end, confirm the block emits with the right paths, confirm Mode 3 reads it correctly.
4. **Update the skill's SKILL.md** with a note in the "Integration with other skills" section pointing at this convention file.
5. **Update the skill's maintenance notes** if the retrofit revealed a new failure mode.

## Future evolution

When Phase 5 makes auto-invoke the default everywhere, `_meta/conventions.md` will reference this file as the canonical convention spec. Until then, the convention lives only in the skills that have been explicitly retrofitted.

## See also

- `~/workspace/skills/output-quality-loop/SKILL.md` § Mode 3 — the runtime behavior
- `~/workspace/second-brain/_meta/handoffs/output-quality-loop/_README.md` — the project roadmap
- `~/workspace/skills/output-quality-loop/references/revision-prompt-template.md` — what Mode 2 produces when verdict ≠ PASS
