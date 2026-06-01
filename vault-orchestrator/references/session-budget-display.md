# Session-budget display + session-plan cap

How NEXT-MOVES presents time totals neutrally and respects the 8-hour session-plan cap. The hard rule: the display shows numbers; the plan honors the cap; neither editorializes about what the operator should pick.

## Why neutral display is load-bearing

The orchestrator is downstream of operator judgment. The session-budget display exists to surface facts (hours per candidate, hours across top N) so the operator can choose well. The moment the display starts editorializing — "this is too much for one day," "you should take only the top two," "consider saving D for tomorrow" — the surface becomes a tutor, not a tool. Operators stop trusting tutors that override their own judgment without being asked.

The session plan is the place where the orchestrator gets to recommend a sequence. The budget display is the place where it stays neutral.

## The budget display shape

For the top N candidates (default N=4) from the ranking, sum the estimated hours from each handoff's "Estimated build time:" cell or "## Status" block.

Display three totals:

```
Top 2 candidates total ~6 hours.
Top 4 candidates total ~12 hours.
All N spawnable candidates total ~28 hours.
```

Three sentences, each on its own line. No interpretation, no recommendation, no comparison to operator capacity.

**When a handoff's estimated hours is a range** (e.g., "2-3 hours"), use the upper bound for the totals. This bias-toward-caution matches honest planning — actual hours tend toward the upper end of estimates.

**When a handoff's estimated hours is missing**, surface that as "estimate unknown" for that candidate and exclude from the totals. Don't fabricate a number. The display then reads "Top 2 candidates total ~6 hours (1 candidate has no estimate)."

## The 8-hour session-plan cap

The recommended session plan never exceeds 8 hours of work. The plan walks the ranked list top-down, adding candidates in order. Stops when adding the next candidate would push the total past 8 hours.

**Why 8 hours.** Reflects today's operator tempo — a long focused day, not a marathon. Lower cap reflects the standing operator-fatigue heuristic: surface this as a discipline rather than a soft suggestion, and let `--session-budget H` override when the operator has a different shape of day.

**What happens when the top candidate alone is >8 hours.** The plan recommends taking that candidate and explicitly names the overage: "Take A (10 hours, exceeds cap — recommend splitting into two sessions per its phases)." Don't silently demote a high-leverage candidate just because of cap math.

**What happens when the cap is overridden.** The plan honors `--session-budget H` and names the override in the rationale: "Session plan respects the operator-set cap of N hours (default 8)."

## How the budget display and session plan compose

The display is reference. The plan is recommendation. The two compose like:

```
## Session-budget totals

Top 2 candidates total ~6 hours.
Top 4 candidates total ~12 hours.
All 7 spawnable candidates total ~28 hours.

## Recommended session plan (capped at 8 hours)

Take A first (1 hour, Claude Code) — low-context-cost, clears the next blocker.
Then B (3 hours, Cowork) — ships a Phase 4 milestone; judgment calls warrant operator presence.
Then C (3 hours, Claude Code) — high-leverage unblocker; total now at 7 hours.

Skip until tomorrow:
- D (4 hours, Claude Code) — high-leverage but 4-hour block doesn't fit today.
- E (2 hours, either) — medium-leverage and isolatable.
- F (3 hours, Cowork) — medium-leverage; gated on D shipping first.
- G (6 hours, Claude Code) — high-leverage but too large for any remaining slot today.
```

The display surfaces what's true (28 hours of work is queued). The plan recommends a sequence (A → B → C fits in 7 hours). Operator picks.

## Voice rules for the budget display

- "Top N candidates total ~M hours" — present tense, ~M is rounded to the nearest hour
- No words like "manageable," "tight," "comfortable," "ambitious" — those editorialize
- No comparison to operator-typical days unless the operator asked for that comparison
- No "leaving room for X" framing — the plan can frame budget; the display stays bare

## Voice rules for the session plan

- "Take A first" / "Then B" / "Skip D until tomorrow" — recommendation voice is allowed here
- Each candidate gets a one-line rationale (context cost, milestone shape, substrate-fit, leverage signal)
- Skipped candidates land in a labeled "Skip until tomorrow" list with their leverage signals preserved — the operator may override
- The plan reads as a colleague's recommendation, not a verdict. "Take" not "you must take"

## Per-candidate rationale shape

Each plan row names:

1. The candidate slug or short name
2. The estimated hours
3. The recommended substrate
4. The one-line reasoning

Format: `Take A first (1 hour, Claude Code) — low-context-cost, clears the next blocker.`

The substrate tag composes with the substrate-recommendation heuristics — see `./substrate-recommendation-heuristics.md` for the full decision rules.

## When the plan recommends fewer candidates than fit

If the top candidate is high-leverage but the next-best is low-leverage AND the remaining hours don't fit any other candidate cleanly, the plan can recommend a smaller sequence and explicitly say so: "Recommend stopping after A. The next candidate that would fit (E) is low-leverage; better to save the remaining 5 hours for something higher-leverage that's not in today's queue."

This is rare. Most days, the plan fills toward the 8-hour cap.

## When the plan recommends parallel work

If the parallel-work detection found pairs that can run concurrently in two Claude Code sub-agents or two Cowork windows, the plan can recommend parallelism:

```
Take A and B in parallel (1 hour each, 2 Claude Code sub-agents) — disjoint file sets, no blocker conflict.
Then C (3 hours, Cowork) — ships a milestone after the parallel pair lands.

Session total: ~4 hours wall-clock (5 hours of work in parallel).
```

Parallel work compresses wall-clock time but doesn't reduce work-hours toward the cap. The cap still respects work-hours, not wall-clock. If A + B in parallel + C in series totals 5 work-hours and the cap is 8, the plan has room for more.

## See also

- `~/workspace/skills/vault-orchestrator/SKILL.md` § Mode 2 Steps 3 and 8 — runtime behavior
- `./leverage-scoring-heuristics.md` — leverage tagging that the plan uses
- `./substrate-recommendation-heuristics.md` — substrate tags the plan inherits
- `./plain-language-discipline.md` — voice rules for both display and plan
