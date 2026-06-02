# Composition with multi-chat-coordination

When NEXT-MOVES invokes `multi-chat-coordination` NEXT-MOVE directly versus reimplementing the logic in the orchestrator. The short answer: compose, don't duplicate.

## The base contract

`multi-chat-coordination` NEXT-MOVE (Mode 3 of that skill) takes the master tracker as input and produces a ranked list of spawnable candidates with per-row reasoning. The six factors it evaluates (blocker status, calendar gates, file-collision risk, cognitive-load risk, downstream pull, operator-stated priority) cover project-coordination concerns.

That mode is well-trodden. The orchestrator does not reimplement it.

## What NEXT-MOVES invokes directly

The orchestrator's Mode 2 NEXT-MOVES invokes `multi-chat-coordination` NEXT-MOVE for:

- The initial leverage ranking based on the six factors
- The candidate set (which rows from the master tracker are spawnable)
- The per-row reasoning paragraph (which the orchestrator augments rather than replaces)
- The cognitive-load risk signal (concurrent-chat count)

The orchestrator does NOT re-walk the master tracker, re-evaluate the six factors, or re-rank from scratch. That's wasted effort and a source of drift.

## What NEXT-MOVES layers on top

After receiving the base ranking, the orchestrator adds:

1. **Four overlay leverage signals** — unblocks-downstream-count, time-to-revenue, operator-stated-priority cross-check, recency-of-related-work (see `./leverage-scoring-heuristics.md`)
2. **Session-budget totals** — sum of estimated hours across top N, neutrally displayed (see `./session-budget-display.md`)
3. **Parallel-work detection** — disjoint file-set pairs across top N
4. **Serial-blocked detection** — high-leverage unblockers
5. **Substrate recommendation per candidate** — Claude Code / Cowork / either per the working-surfaces convention (see `./substrate-recommendation-heuristics.md`)
6. **Decision-research convention** on ties + priority conflicts (see `./decision-research-composition.md`)
7. **Session plan** — recommended sequence capped at 8 hours

The output combines the base ranking's per-row reasoning with the overlay's overlay-rationale paragraph. The final report shows both — the operator can see what the base ranking said and what the orchestrator added.

## The handoff shape

When NEXT-MOVES invokes `multi-chat-coordination` NEXT-MOVE:

**Input to MCC NEXT-MOVE:**
- Master tracker path (`~/workspace/second-brain/_meta/handoffs/_active-chats-tracker.md`)
- Operator's question (e.g., "what should I spawn next?")
- Memory file path for priority-memory cross-reference

**Output from MCC NEXT-MOVE (what the orchestrator consumes):**
- Ranked list of candidates (slug + handoff path + tier)
- Per-row reasoning paragraph (the "Why" + "Effort" + "Unblocks" + "Risks" blocks)
- Recommended sequence over the next N moves (the orchestrator may discard this — NEXT-MOVES builds its own session plan from the overlay-augmented ranking)
- Calendar-gate annotations

The orchestrator takes the ranked list + reasoning + calendar gates. It discards MCC's "Recommended sequence over the next N moves" because the orchestrator's session plan adds substrate tagging and the 8-hour cap that MCC doesn't.

## When the orchestrator DOESN'T compose with MCC

Two cases:

### 1. SURVEY does not invoke MCC NEXT-MOVE

SURVEY is a state-of-the-vault report, not a recommendation. It reads the tracker, walks domains, surfaces signals. NEXT-MOVE-style ranking only fires when the operator explicitly asks for NEXT-MOVES.

The exception: SURVEY's Section 2 ("what's ready to work on next") lists Ready-to-spawn candidates with leverage signals. Those signals can come from a cached recent NEXT-MOVES run; if no recent run exists, SURVEY shows the candidates without leverage tags rather than triggering MCC NEXT-MOVE inline.

### 2. NEXT-MOVES skips MCC when the candidate set is empty

If the master tracker has zero Ready-to-spawn candidates and zero promotable Tier-2 candidates, the orchestrator does not invoke MCC NEXT-MOVE. The bottleneck is the candidate set, not the ranking — surface that as the finding and stop.

## Composing with MCC AUDIT

The orchestrator's SURVEY Section 8 (stale signals) can optionally call `multi-chat-coordination` AUDIT for deeper drift findings.

By default, SURVEY uses the lighter `master-tracker-aggregator` DRIFT-DETECT mode (which the aggregator already documents). DRIFT-DETECT covers digest staleness and four signal-based heuristics — fast and read-only.

When the operator wants the deeper drift report (tracker rows vs handoff frontmatter, missing rows, status drift), SURVEY can invoke MCC AUDIT and surface its findings in Section 8 instead of the lighter drift-detect output. Flag this via `--full-audit` on SURVEY (not currently in the skill's flag set; reserved for v2).

## Composing with MCC DECOMPOSE

Out of scope for Phase 3. Phase 4 (PROVISION) composes with DECOMPOSE to draft handoffs from spawn-candidate proposals.

## Mode 5 RESUME → Mode 3 PROVISION chain (v1.2)

Mode 5 RESUME identifies which `planned_remaining_waves[]` for a named project are ready but lack handoff files. The operator's natural next move on those waves: "provision wave-X for <project>." That invokes Mode 3 PROVISION on the named wave, but with a key difference from a fresh PROVISION run:

- **Fresh PROVISION (v1.1 default):** operator names a strategic-chat-style goal; DECOMPOSE generates the full N-phase plan from scratch.
- **Chained PROVISION (v1.2 RESUME → PROVISION):** the wave scope comes from the RESUME report's Section 2 entry for the named wave. PROVISION consumes the existing scope + estimated hours + `blocks_on` array rather than re-deriving them.

The chain composition contract:

- Mode 5 RESUME's Section 2 names each ready wave with: `wave_id`, scope summary, estimated hours (from `planned_remaining_waves[].estimated_hours`), `blocks_on` array, and a chain note inviting PROVISION on that wave.
- When the operator says "provision wave-X for <project>" after a RESUME run, Mode 3 PROVISION reads the RESUME output (chat-only if recent, or `--persist`ed file if archived) as the goal source. The wave's scope becomes PROVISION Step 2's input to DECOMPOSE; the `blocks_on` array becomes prerequisite context for the dependency graph.
- PROVISION still runs its full discipline (Steps 3-11) — decision-research convention firing, edit-zone conflict scan, substrate tagging, checkpoint reminders, operator-fatigue check, single review gate. The chain just supplies the goal source automatically.
- The drafted handoff file gets registered against the EXISTING project subfolder (e.g., `_meta/handoffs/<project-slug>/wave-X-<topic>.md`) rather than a new project subfolder. This is the key v1.1 known-gap-1 closer: PROVISION can now draft INTO an existing project, not just create a new one.

The chain closes known-gap-1 from v1.1 on the drafting side. With Mode 6 EXECUTE shipped 2026-06-03, the full trio (RESUME → PROVISION → EXECUTE) closes the gap end-to-end — see the next section.

The operator drives the chain — Mode 5 RESUME does NOT auto-invoke PROVISION. The composition shape preserves the operator-driven separation between identification and drafting (same shape as NEXT-MOVES → PROVISION).

## Mode 6 EXECUTE — sub-agent dispatch over the RESUME → PROVISION chain (v1.2)

Mode 6 EXECUTE is the third link in the chain. RESUME identifies ready waves; PROVISION drafts handoffs for waves that lack them; EXECUTE dispatches narrowly-scoped per-artifact sub-agents under orchestrator coordination to actually produce the wave's artifacts.

The chain composition contract:

- **Fresh dispatch (operator triggers EXECUTE directly):** operator names a project slug + wave ID with a handoff file already on disk; Mode 6 reads the handoff + dispatches per its artifact list.
- **RESUME-chained dispatch:** Mode 5 RESUME output names a wave as "state-file-ready + tracker-Ready + handoff exists"; operator chains with "execute wave-X for <project>"; Mode 6 reads the wave's handoff (named in the RESUME output) + dispatches.
- **PROVISION-chained dispatch:** Mode 5 RESUME → operator chains into PROVISION on a wave that lacks a handoff → PROVISION drafts the handoff → operator chains into EXECUTE on the freshly-drafted handoff → Mode 6 dispatches against it. Three operator-driven hops; each one operator-confirmed at its own review gate.

EXECUTE composes with `client-seo-onboarding`'s per-step quality loop contract (NOT with `multi-chat-coordination`'s NEXT-MOVE / DECOMPOSE / AUDIT). The sub-agent contract that EXECUTE dispatches IS the four-substep loop from `client-seo-onboarding` v1.1 SKILL.md § "Per-step quality loop contract." See [[sub-agent-dispatch-contract]] for the prompt template + return contract + substrate-adaptive dispatch matrix.

The composition shape vs PROVISION:

| Aspect | PROVISION | EXECUTE |
|---|---|---|
| What it operates on | A project goal | A wave handoff |
| What it produces | N drafted phase handoffs + queue rows + tracker rows | A dispatch plan + sub-agent verdicts in `quality_log` + a wave-close `wave_log` entry |
| Single review gate | Yes — operator approves the proposal before any write | Yes — operator approves the dispatch plan before any sub-agent fires |
| Composes with | DECOMPOSE | `client-seo-onboarding`'s per-step quality loop |
| Edit-zone detector input | Drafted + queued + in-flight handoffs | Sub-agent set within the wave |

Both modes use Phase 4's edit-zone conflict detector, but at different granularities (handoff-level vs sub-agent-level). See [[parallel-safe-coordination]] for the EXECUTE-side reuse.

The operator drives every chain hop — Mode 5 does not auto-invoke PROVISION; Mode 3 does not auto-invoke EXECUTE; Mode 6 does not auto-invoke other modes. The chain preserves the operator-driven separation between identification, drafting, and dispatch.

## Avoiding the double-bookkeeping trap

The most common composition failure: invoking MCC NEXT-MOVE, then re-evaluating the six factors in the orchestrator, then ranking again. That's double-bookkeeping — the two rankings drift, the operator sees two different recommendations, trust erodes.

The discipline: MCC owns the six-factor evaluation and base ranking. The orchestrator owns the overlay signals and session plan. Each layer is responsible for what it does; neither reimplements what the other does.

## Future evolution

When the orchestrator decomposes in Phase 5 (per-project orchestrator decomposition into project-surveyor + project-analyst + project-decider sub-skills), the composition contract here splits:

- project-surveyor composes with MCC NEXT-MOVE at the project scope
- project-analyst composes with MCC AUDIT for project-scoped drift
- project-decider composes with MCC DECOMPOSE for project-scoped phase planning

Phase 3 stays monolithic. The composition contract above is the v1 shape.

## See also

- `~/workspace/skills/vault-orchestrator/SKILL.md` § Mode 2 Step 1 — runtime behavior
- `~/workspace/skills/multi-chat-coordination/SKILL.md` § Mode 3 — the base mode this composes with
- `./leverage-scoring-heuristics.md` — what the orchestrator adds on top
- `./decision-research-composition.md` — when ties fire the convention
