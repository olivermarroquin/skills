# Revision prompt template

The shape Mode 2 produces when a verdict is NEEDS REVISION (minor), NEEDS REVISION (substantive), or FAIL. The prompt is paste-ready: the operator drops it into the chat that produced the artifact (or a fresh chat), and that chat ingests it as if it were operator input.

## Template (verbatim shape)

```markdown
# Revision needed — <artifact-path>

**Verdict:** <NEEDS REVISION (minor) | NEEDS REVISION (substantive) | FAIL>
**Evaluated:** YYYY-MM-DD HH:MM
**Iteration:** N of 3 (capping at 3 — after this iteration, evaluation will escalate to the operator if not PASS)

Your previous output was evaluated and needs revision. Apply the following fixes and re-output the artifact.

## Hard requirements missed

<For each hard-requirement miss:>

### <Item name>
- **Gap:** <one sentence — what's missing or wrong>
- **Spec source:** <file path + section/line, e.g. `_template-service-brief.md` §4.5 F>
- **What good looks like:** <one paragraph describing the bar the artifact needs to clear>
- **Specific fix:** <concrete edit — exact text to add, exact field to populate, exact section to insert>

## Quality dimensions at fail or partial

<For each quality-dimension fail or partial — grouped by severity, fails first then partials:>

### <Dimension name>
- **Score:** <fail | partial>
- **Gap:** <one sentence>
- **Spec source:** <file path + section/line>
- **What good looks like:** <one paragraph>
- **Specific fix:** <concrete edit>

## Discipline rules violated

<For each discipline-rule violation:>

### <Rule name>
- **Violation:** <one sentence>
- **Spec source:** <file path + section/line>
- **Why this rule exists:** <one sentence — the operator-discipline precedent the rule encodes>
- **Specific fix:** <concrete edit>

## Root cause (only when FAIL or substantive revision)

<One paragraph summarizing the underlying issue — not a restatement of the gaps. Why did the producing chat miss the bar? Is it a misread of the spec, a missing input, a calibration issue with the producing skill itself?>

## Iteration budget

This is iteration N of 3. The output-quality-loop skill caps at 3 iterations per artifact:

- If the next regeneration reaches PASS, the loop closes and the artifact ships.
- If the next regeneration still doesn't reach PASS, the loop runs one more time.
- If the third iteration still doesn't reach PASS, the loop emits a "loop-stalled" escalation report and stops. The operator decides what to do next.

After applying these fixes, the artifact will be re-evaluated by output-quality-loop. The cycle continues until PASS or a maximum of 3 iterations have run.
```

## Guidelines for filling in the template

### Hard requirements

List **every** hard-requirement miss. Hard requirements are the floor; missing any of them means FAIL. Grouping is by hard-requirement category (frontmatter / required sections / schema / named fields).

For each item, the "Specific fix" should be the smallest concrete change that satisfies the bar. Don't ask for a full rewrite; ask for the targeted edit that closes the gap.

### Quality dimensions

List **every fail** and **every partial**. Don't list passes — the producing chat doesn't need to know what's already working.

Group by severity: fails first (these are at threshold), partials second (these are above the floor but below the bar).

The "Specific fix" should be the smallest edit that elevates the dimension from partial → pass, or from fail → partial-or-pass. Calibrate ambition: a quality dimension at fail might need a whole new section; a quality dimension at partial usually needs a few sentences rewritten.

### Discipline rules

Discipline-rule violations are usually one-shot fixes (delete a line, change a frontmatter field, replace a non-canonical citation format). Name the rule, name the precedent that established it, name the fix.

Discipline rules escalate verdicts: 3+ violations at any severity flips an otherwise-PASS verdict to NEEDS REVISION (substantive). Make the count clear.

### Root cause

Only emitted when the verdict is FAIL or NEEDS REVISION (substantive). Skipped for NEEDS REVISION (minor).

The root cause is the diagnostic the producing chat needs to regenerate well. If the producing chat misread the spec, name it. If the spec itself was ambiguous, surface it. If the producing chat skipped a phase of its own workflow, name the phase.

Avoid restating the gaps — the gaps are already listed above. The root cause is the *why* behind them.

### Iteration budget

The iteration count is the producing chat's signal for when to escalate vs. regenerate. The template makes the cap explicit so the producing chat doesn't accidentally regenerate past iteration 3.

## Calibration: ambition of the revision prompt

A revision prompt is calibrated to the verdict:

- **NEEDS REVISION (minor)** — small set of targeted edits. The prompt should read like a punch list. The producing chat applies the edits and re-outputs the artifact; no full regeneration.
- **NEEDS REVISION (substantive)** — moderate-to-large gap list. The producing chat probably needs to redraft sections, not just patch them.
- **FAIL** — the artifact is broken. The prompt names the root cause and the path back to the bar. The producing chat almost always regenerates from scratch (or close to it).

The prompt's tone stays neutral and instructional regardless of severity. No "you got this wrong" framing; the producing chat is doing its best, and the loop's job is to elevate, not scold.

## Citation discipline

Every fix references its spec source by file + section/line. The producing chat can't act on "the spec says X" — it needs to know which spec, which section. Without the citation, the audit trail breaks and future-Claude can't tell what calibration was applied.

If a fix doesn't have a clear spec citation (e.g., the gap is in the artifact's writing quality rather than a named rule), cite the closest relevant convention (`plain-language-conventions.md`, `conventions.md`). Don't fabricate a citation; honest about gaps in the spec sources too.

## Where the prompt gets written

Mode 2 emits the prompt to stdout (so the operator can copy it directly).

If the operator named a path or the artifact already has a `.revision-prompt.md` sibling convention in play, Mode 2 also writes the prompt to `<artifact-path>.revision-prompt.md`. The sibling file is convenient for chats that operate via path references rather than copy-paste.

In auto-invoke mode (Mode 3), the prompt is emitted to the producing chat directly, no sibling file required.

## See also

- `~/workspace/skills/output-quality-loop/SKILL.md` § Mode 2 — the runtime behavior
- `~/workspace/skills/output-quality-loop/references/verdict-rollup-thresholds.md` — the verdict tiers the prompt is calibrated against
- `~/workspace/skills/output-quality-loop/references/evaluation-heuristics-by-type.md` — the per-type checklists that produce the gap list
