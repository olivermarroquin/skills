# Decision-research composition

When SURVEY and NEXT-MOVES invoke the five-step decision-research convention from `~/workspace/second-brain/_meta/decision-research-conventions.md`. The convention's job is to make decisions on the strongest available evidence; the orchestrator's job is to name when a decision warrants invoking it.

## What fires the convention in NEXT-MOVES

Two cases trigger an inline decision-research call:

### Case 1 — Leverage tie

Two candidates have indistinguishable leverage signals AND comparable session-budget impact. The base ranking from `multi-chat-coordination` NEXT-MOVE can't decide between them; the orchestrator's overlay didn't break the tie either.

When this happens, the orchestrator runs the five-step convention to pick which to recommend first.

### Case 2 — Priority conflict

A candidate appears to conflict with current stated priorities. Examples:

- A Keelworks-internal experimentation candidate ranked above a client-deliverable candidate, when the standing `project_priority_client_seo_traffic` memory says client work is the priority right now.
- A skill-build candidate ranked above a client-revenue candidate when the operator's recent execution-log activity shows the client revenue work is hot.
- A nice-to-have refactor candidate ranked above a milestone-shipping candidate.

When the conflict is real (not just a different framing), the orchestrator runs the convention to make the call and documents it.

## What does NOT fire the convention

Don't fire on every ranking question. The convention is for genuine decision points, not for routine ordering. Specifically, do NOT fire on:

- Routine ordering between clearly-distinguished candidates (one is high-leverage, one is medium — no tie)
- Choosing which of two parallel candidates to start first when both are short and disjoint (just pick one and name the parallelism in the session plan)
- Substrate recommendations (the working-surfaces convention is the source of truth; no further research needed)
- Calendar-gate decisions (the date is the date)

The convention has overhead. Fire it when the overhead is justified by the stakes.

## What fires the convention in SURVEY

SURVEY is a state-of-the-vault report, not a decision-making mode. It does not typically fire the convention. The exception:

- **Cross-project signal interpretation.** When Section 9 surfaces a cross-project signal whose downstream implication is genuinely ambiguous (e.g., "convention changed — should this trigger a rollout chat now or wait for organic propagation?"), SURVEY can invoke the convention to make the call. Rare; most cross-project signals are factual.

## The five-step process (orchestrator-internal voice)

When fired, the convention runs inline. The five steps from the canonical convention:

### Step 1 — Frame the decision

Write one sentence naming the decision and the options. Example for a leverage tie:

> "Should NEXT-MOVES rank `hermes-harness Prework A` (Hermes deployment validation, ~6-8h, operator-side) ahead of `hermes-harness Prework B` (Nous Research transparency research, ~2-3h, Cowork)? Both are high-leverage; both unblock Phase 1 commit."

### Step 2 — Search the vault first

The vault holds prior decisions of similar shape. For ranking-and-priority calls, search:

- `_meta/decisions/` for decision records on similar tradeoffs
- `05_shared-intelligence/lessons/` for lessons about phase-sequencing
- `05_shared-intelligence/patterns/` for established patterns
- `04_projects/<project>/handoffs/` for context on how the operator has historically picked
- Priority memories in `MEMORY.md`

If the vault has 2+ relevant sources, move to Step 4.

### Step 3 — Run external research only if the vault is thin

External research is rarely needed for orchestrator-internal ranking calls. The decision is about the vault's own state, which the vault knows. Skip Step 3 unless the decision actually depends on external data (e.g., "should we wait for an external system to launch before ranking this candidate?").

### Step 4 — Synthesize options

For each option in the tie:

- One-line description
- Strongest argument for
- Strongest argument against
- Estimated impact on the session plan
- Reversibility (cheap to swap order later vs. lock-in)

Plain prose. No bullet walls.

### Step 5 — Decide and document

Pick. Write one paragraph naming the call, the reasoning, and which option got the recommendation. Land the paragraph in NEXT-MOVES' "Decision-research calls" section of the report.

The decision-research call is in the report so the operator can scan it and override if they disagree. The orchestrator's call is a recommendation, not a verdict.

## The output shape in the NEXT-MOVES report

When the convention fires, the report has a section:

```markdown
## Decision-research calls

### Tie between Prework A and Prework B (both high-leverage, both unblock Phase 1)

Frame: should NEXT-MOVES rank Prework A (Hermes deployment validation, ~6-8h, operator-side) ahead of Prework B (Nous Research transparency research, ~2-3h, Cowork)?

Vault sources: hermes-harness Phase 0 decision report (Section 6 — what-would-change-recommendation flag #1 calls out org instability as a higher-stakes blocker than substrate stability); Prework B's handoff names this flag explicitly as its scope.

Call: Rank Prework B first. Reasoning: Prework B specifically addresses the highest what-would-change flag from Phase 0; closing that flag may itself change Prework A's scope. Running Prework A before Prework B risks revisiting the deployment shape if Prework B surfaces evidence the substrate decision should shift. Reversibility: cheap to re-order if Prework B closes cleanly; expensive to undo Prework A's deployment work if Prework B blows it up.
```

The framing + sources + call structure mirrors the canonical convention's worked-example shape.

## When to skip Step 5 and surface the tie to the operator

If both vault search AND external research come back thin AND the decision genuinely depends on operator-altitude information (e.g., "depends on whether the operator is comfortable spending 8 hours on operator-side execution this week"), don't force a call. Surface the tie:

```markdown
## Decision-research calls

### Tie between Prework A and Prework B (couldn't break)

Frame: should NEXT-MOVES rank Prework A or Prework B first?

The leverage signals are indistinguishable and the choice depends on operator-altitude factors the orchestrator can't see (how much operator-side execution time you have this week; whether you prefer to close the highest-stakes flag first or de-risk the substrate first). Surfacing the tie for operator judgment.
```

Honest "couldn't break the tie" surfacing is better than fabricating a confident call.

## Composition with `perplexity-refinement`

If external research is needed (rare), the convention's Step 3 specifies `perplexity-refinement`. The orchestrator does not invoke `perplexity-refinement` directly — it routes through the convention's invocation contract. See `~/workspace/second-brain/_meta/decision-research-conventions.md` Step 3 for the budget rules (3-5 queries default).

## Budget discipline

The convention has overhead. The orchestrator's overall NEXT-MOVES budget should account for at most 1-2 convention-firings per invocation. If 4+ decisions look like they need the convention, the orchestrator's overlay logic is likely under-calibrated — surface as a maintenance signal and fall back to operator surface-the-tie behavior for the rest.

## See also

- `~/workspace/skills/vault-orchestrator/SKILL.md` § Mode 2 Step 7 — runtime behavior
- `~/workspace/second-brain/_meta/decision-research-conventions.md` — canonical convention
- `./leverage-scoring-heuristics.md` — what produces the tie
- `./session-budget-display.md` — how the session plan inherits the call
- `~/workspace/skills/perplexity-refinement/SKILL.md` — external research path (rare)
