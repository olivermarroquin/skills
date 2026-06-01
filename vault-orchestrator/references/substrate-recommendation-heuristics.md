# Substrate recommendation heuristics

How NEXT-MOVES tags each ranked candidate with `Claude Code`, `Cowork`, or `Either`. The tagging is mandatory on every candidate. The rationale cites the working-surfaces convention — not generic memory.

## Why substrate tagging is load-bearing

Operators pick what to run based on what's available right now (terminal open vs. desktop app open), what shape the work is (multi-file edits vs. conversational planning), and what cost the substrate imposes (Task tool parallelism vs. file-presentation cards). A leverage-ranked candidate without a substrate tag is half-useful — the operator still has to decide where to run it.

The orchestrator's job is to take that second decision off the operator. The cost of the wrong substrate is wasted ramp-up: spawning a multi-file refactor in Cowork burns time when Claude Code's Task tool would have done it in half the steps; spawning a discussion chat in Claude Code burns the conversational pacing that Cowork's interface is built for.

## Source of truth

Substrate recommendations cite `~/workspace/second-brain/_meta/working-surfaces.md` § "Default routing." That convention has a table mapping work shapes to surfaces. Use it. Don't substitute generic intuition.

The table (excerpted for reference; the convention file is canonical):

| Work shape | Surface |
|---|---|
| "I want to think through X with you" | Cowork |
| "Show me what's in the vault about Y" | Cowork |
| "Build / edit / retrofit N files" | Claude Code |
| "Run a research batch and bring back findings" | Claude Code |
| "Spawn 3 parallel chats to work on these handoffs" | Claude Code |
| "Read this file and tell me what's in it" | Cowork |
| "Status of everything I'm working on right now" | Dashboard (future) / Cowork (today) |
| "Drive my Cowork-pasted browser to look at competitor sites" | Cowork (with Claude in Chrome) |
| "I want a chat that runs unattended for 2 hours" | Claude Code |
| "Quick decision: which path do you recommend?" | Cowork |

When a candidate doesn't map cleanly to any row, tag it `Either` with a one-line note on what the work could look like in each substrate.

## The three tags

### `Claude Code`

Use when the work is:

- **Multi-file edits across the vault or repos.** Examples: retrofit pass across 14 skills, mass file ops across `04_projects/`, bulk frontmatter normalization.
- **Parallel sub-agent work.** Examples: run 3 research queries in parallel, fan-out fact-finding across competitors, parallel scaffolding of N pages.
- **Long-running automation.** Examples: research batches with many web fetches, content generation across a hundred pages.
- **Direct git workflow.** Examples: commits, branch work, PR review, multi-repo coordination.
- **Skill execution where "run, then report back" is the right shape.** The skill does its thing autonomously; operator reads the result.

**The rationale should cite:** "multi-file edits + Task tool fits Claude Code per `~/workspace/second-brain/_meta/working-surfaces.md` § Default routing."

### `Cowork`

Use when the work is:

- **Conversational planning.** Examples: discussing scope with the operator, walking through options, thinking through a decision together.
- **Operator-judgment-heavy.** Examples: every step needs operator weigh-in, the deliverable shape is unsettled.
- **File-presentation-shaped output.** Examples: producing a polished file the operator will read inline, generating docx/pptx for client delivery.
- **Browser-driven research with Claude in Chrome.** Examples: walking competitor sites with the operator, Perplexity Pro queries via the operator's logged-in browser session.
- **One-off lookups.** Examples: "what do I have on X?" — quick conversational answers.

**The rationale should cite:** "conversational + operator-judgment-heavy fits Cowork per `~/workspace/second-brain/_meta/working-surfaces.md` § Default routing."

### `Either`

Use when:

- The work could happen in either substrate without meaningful difference.
- The deciding factor is operator preference / availability, not work shape.
- The work has phases that suit each substrate (e.g., scope discussion in Cowork + execution in Claude Code) but the candidate is small enough to fit in one chat.

**The rationale should:**

- Name what the work would look like in each substrate, briefly.
- Explicitly say "operator preference decides."
- Not default to `Either` when the work clearly fits one substrate better — that's a sign of incomplete analysis. Pick one if the shape is clear.

## Edge cases

### Candidate is "operator-side execution"

Some candidates explicitly require the operator's hands on a system the orchestrator can't drive (Hostinger SSH, hardware deployment, physical setup). Tag these `Operator-side` with a one-line note pointing at the candidate's handoff that explains why. This isn't one of the three primary tags — it's a fourth implicit case that surfaces when neither Claude Code nor Cowork can execute the work autonomously.

### Candidate spans phases that suit different substrates

Long candidates with phase structure (research → build → polish) may genuinely span substrates. Tag the primary substrate and name the secondary phases in the rationale: "Primary: Claude Code (multi-file build). The final polish phase may benefit from Cowork for file-presentation review."

### Candidate is a discussion chat with no deliverable

Discussion-only chats (Phase 0 scope discussions in `client-onboarding-automation` and `ads-and-marketing`) always tag `Cowork`. The whole point of a discussion chat is conversational pacing — Claude Code's pacing is wrong for it.

### Candidate is a skill-build initiative

Skill-build (writing a SKILL.md + reference files) usually tags `Either` unless the build phase explicitly needs Task tool (parallel reference-file generation) or explicitly needs operator presence (every section is a judgment call). Use the build-time-estimate as a tie-breaker: skill-builds <2h often fit Cowork's pacing; >3h usually go to Claude Code for sustained file edits.

## Voice rules for substrate rationale

- One-line rationale per candidate
- Always cite the working-surfaces convention
- Don't editorialize ("Claude Code is faster" — say "fits the multi-file work shape per the convention")
- Don't hedge ("probably Claude Code") — pick or use `Either` with reasoning

## When operator overrides via `--substrate`

If the operator runs `NEXT-MOVES --substrate cowork`, every candidate's substrate tag is biased toward Cowork unless the work shape is structurally hostile to it. Bias means: when the convention says `Either` or `Claude Code (lightly)`, swap to `Cowork`. When the convention says `Claude Code (strongly, multi-file)`, surface the bias-conflict explicitly: "Operator biased toward Cowork; this candidate's multi-file shape pulls toward Claude Code — operator decides."

## See also

- `~/workspace/skills/vault-orchestrator/SKILL.md` § Mode 2 Step 6 — runtime behavior
- `~/workspace/second-brain/_meta/working-surfaces.md` — canonical convention
- `./leverage-scoring-heuristics.md` — substrate is independent of leverage
- `./session-budget-display.md` — session plan inherits substrate tags
