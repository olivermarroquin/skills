# Leverage scoring heuristics

How NEXT-MOVES scores leverage on top of the base ranking it gets from `multi-chat-coordination` NEXT-MOVE. The base ranking is good; this layer adds four orchestrator-specific signals so the final ranking reflects vault-wide context the base mode can't see.

## Why an overlay rather than a replacement

`multi-chat-coordination` NEXT-MOVE evaluates six factors (blocker status, calendar gates, file-collision risk, cognitive-load risk, downstream pull, operator-stated priority). Those are project-coordination signals. The orchestrator is a vault-wide layer — it sees the per-project digests, the domain folders, the recently-shipped artifacts, the cross-project effects. The overlay is where those vault-wide signals enter the ranking.

The overlay never overrides the base mode's "this candidate is not actually spawnable" verdict (open blocker, hard calendar gate). It only re-orders eligible candidates.

## The four overlay signals

### 1. Unblocks-downstream-count

For each candidate, count how many queued handoffs name this candidate (or its phase) as a prerequisite. Sources:

- `blocked-by:` field in queued handoff frontmatter
- "Trigger to spawn" cell in the master tracker for queued rows
- "Prereqs:" or "Blocked on" text in queued handoff prompt bodies

**Why this matters.** A candidate that unblocks 5 downstream chats is structurally more valuable than one that unblocks 0, all else equal. Shipping it removes the most parallelism friction.

**Scoring weight.** Candidates with ≥3 downstream unblocks get tagged `high-leverage unblocker` in the report's serial-blocked section. The leverage signal (`high` / `medium` / `low`) up-shifts one tier when unblocks ≥3.

**Edge case.** A candidate that unblocks 5 chats but only ships in 6 hours is structurally similar to one that unblocks 2 chats but ships in 1 hour. The leverage tag is qualitative; the session-budget display surfaces the hours so the operator can compare.

### 2. Time-to-revenue

Does the candidate ship a client-facing artifact? Examples:

- An EV Electric Core 30 page
- An S&H Contracting deliverable
- A keelworks-ai-os-saas milestone (paying customers)
- A client-onboarding-automation phase that ships before the 1-month-to-incoming-client deadline

**Why this matters.** Per the standing `project_priority_client_seo_traffic` memory, current operator priority biases toward client deployment over Keelworks-internal experimentation. Client-revenue-shaped work up-shifts.

**Scoring weight.** Up-shift one tier when the candidate ships client-facing output. Cite the memory in the rationale ("up-weighted per `project_priority_client_seo_traffic`").

**Edge case.** A skill-build that accelerates future client work (like vault-orchestrator Phase 3 itself) is structurally close to client work but not directly client-facing. The overlay gives it half-credit — name it as "infrastructure for client work" rather than "client revenue" so the operator can decide.

### 3. Operator-stated priority

Re-check priority memories and recent strategic-chat outputs before ranking. Sources:

- `project_priority_*` entries in `MEMORY.md`
- The 5-most-recent execution-log entries across all projects (signal: what's been getting attention)
- Recent strategic-chat outputs in `_meta/decisions/` (signal: what was decided lately)
- `feedback_*` entries that name priorities ("X is the priority right now," "don't add Y until Z")

**Why this matters.** Operator-altitude priorities shift faster than the tracker captures. Memories and decisions docs hold the freshest signal.

**Scoring weight.** Up-shift one tier when the candidate matches a stated priority. Cite the memory or decision in the rationale.

**Edge case.** A candidate that conflicts with a stated priority fires the decision-research convention (see `./decision-research-composition.md`). Don't silently down-shift conflicting candidates — surface the conflict and resolve it explicitly.

### 4. Recency-of-related-work

Was the candidate's domain or project just touched (execution log in past 48h, recently-closed sibling chat, recently-edited spec file)?

**Why this matters.** Re-loading context is cheap when it's hot. Two candidates with the same base leverage are easier to ship when one's context is already warm.

**Scoring weight.** Up-shift half a tier when the related work is <48h old. Don't up-shift on >7-day stale context; that's neutral.

**Edge case.** "Hot context" can also mean the operator just spent 5 hours in that project today. If the master tracker shows >2 closed chats in the same project in past 24h, neutralize this signal — the operator's fatigue threshold matters more than context-loading cost.

## How the overlay composes with the base ranking

The base ranking from multi-chat-coordination NEXT-MOVE is a list with per-row reasoning. The overlay:

1. Reads each candidate's base position.
2. Computes each of the four overlay signals.
3. Applies up-shifts / down-shifts qualitatively (no numeric scoring — the qualitative tag is what the operator scans).
4. Re-emits the list in the new order with the overlay rationale appended to each row's reasoning paragraph.

The overlay's rationale paragraph names each signal it weighted ("Up-shifted because: unblocks 4 downstream chats; client-facing; matches priority memory; related context is warm").

## Leverage signal tagging

Each candidate ends with one of three tags. The tag is what the operator scans for at a glance:

- **`high-leverage`** — ships a milestone, unblocks ≥3 downstream chats, matches a stated priority, or directly ships client revenue.
- **`medium-leverage`** — ships a discrete deliverable but no major unblock and no priority match. Most candidates land here.
- **`low-leverage`** — small isolated unit, no downstream unblock, no priority match. Often skippable on a tight session.

The tags are recommendations, not verdicts. A `low-leverage` candidate may be exactly the right thing for a 30-minute session between deeper work.

## When the overlay produces no movement

If all four signals are neutral across the candidate set, the overlay leaves the base ranking intact and notes "no overlay-signal differentiation; base ranking preserved." Don't fabricate movement to justify running the overlay.

## When the overlay produces a tie

Two candidates with identical leverage signals AND comparable session-budget impact fire the decision-research convention (see `./decision-research-composition.md`). The convention's call lands in the report's "Decision-research calls" section.

## See also

- `~/workspace/skills/vault-orchestrator/SKILL.md` § Mode 2 Step 2 — the runtime behavior
- `~/workspace/skills/multi-chat-coordination/SKILL.md` § Mode 3 — the base ranking
- `./session-budget-display.md` — how the leverage signal interacts with hours totals
- `./decision-research-composition.md` — what fires on ties
- `./substrate-recommendation-heuristics.md` — substrate tagging is independent of leverage
