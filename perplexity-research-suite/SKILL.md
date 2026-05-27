---
name: perplexity-research-suite
description: The menu and router for Oliver's Perplexity-skill suite. Use when the operator wants to see what Perplexity-powered skills are available, doesn't know which one to use, or names a research goal in natural language (validate something, find counter-evidence, blueprint a process, check a niche, monitor citations, scan for acquisition signals, refine an artifact). Triggers on phrases like "what Perplexity skills do I have," "run perplexity research," "what can Perplexity do for me," "perplexity menu," "I want to use Perplexity but don't know which skill," or whenever Oliver describes a research need without naming a specific Perplexity skill. The router presents the menu, maps the goal to the right skill, surfaces current weekly-budget status, and hands off to the specific skill so its own logic runs end-to-end. Read-only by default — the router itself never writes vault files; the skill it routes to owns its own writes.
---

# Perplexity research suite — router skill (v1.0)

The menu layer over Oliver's Perplexity-Pro skill suite. Lists every Perplexity-powered skill, maps natural-language research goals to the right skill, surfaces how much of the weekly Pro Search budget has been used so far, and routes to the chosen skill so its own logic runs end-to-end.

This skill exists because Oliver is building 10 Perplexity-prefixed skills (1 shipped, 9 pending across Waves 1-5). Each skill answers a different research question. Without a router, Oliver has to remember which trigger phrase fires which skill. The router solves that — it's a single entry point that listens for a goal in plain language and dispatches.

**Critical behavior — read this first:**

- **Read-only by default.** The router never writes vault files. It presents the menu, makes the routing decision, and hands off. The skill it routes to owns all writes.
- **No new functionality.** The router is a dispatcher. It doesn't add capability the sub-skills don't already have. If a sub-skill is missing a feature, the fix lives in that sub-skill, not here.
- **Honest about capacity.** Pro Search caps at ~200 queries per week. The router surfaces rough weekly usage from execution logs and warns before invoking high-cost skills when usage looks heavy.
- **Don't fake the routing decision.** When the operator's goal is ambiguous between two skills, present the top two candidates and ask. Don't pick silently.
- **Pending skills don't get invoked.** The lineup includes skills that aren't shipped yet (Waves 1C through 5). When the routing decision lands on a pending skill, surface that fact and either suggest the closest shipped alternative or queue the work for when the skill ships.

---

## When to use this skill

Trigger when the operator asks a general question about Perplexity research or names a research goal without naming a specific skill. Typical phrasings:

- "What Perplexity skills do I have?"
- "Run perplexity research"
- "What can Perplexity do for me?"
- "Perplexity menu"
- "I want to use Perplexity but I don't know which skill"
- "I want to validate this claim — which skill?"
- "Find counter-evidence on this brief"
- "Help me blueprint this process"
- "Is this niche worth entering?"
- "Are my client's pages being cited by Perplexity?"
- "Is anyone making moves in this space?"

Do **not** use this skill when:

- The operator already named a specific skill ("refine the panel-upgrade brief with Perplexity" → route directly to `perplexity-refinement`, no menu).
- The research goal is unrelated to the Perplexity suite (general web research, single-shot question-answering — those don't need a skill at all).
- The operator wants to use a non-Perplexity research tool (DataForSEO, Featured.com, Otterly.ai — those have their own skills or workflows).

---

## The suite — what's shipped and what's pending

Ten skills total. The router enumerates them when the operator asks "what Perplexity skills do I have." Wave status as of this skill's `updated:` date.

### Wave 0 — shipped

**`perplexity-refinement`** (shipped 2026-05-27)
Take any vault artifact and run a Perplexity Pro pass against its key factual claims, named tools, statistics, and concepts. Validate, update, contradict, deepen, or surface new sources. Write findings back as an appended section, inline-merged edits, or a sister file. Per-invocation caps: 3 / 7 / 15 queries for light / medium / deep.

When to use: any time a vault artifact would benefit from external citation, fact-check, or counter-evidence. Source notes, briefs, tactics, decisions, primers, syntheses.

### Wave 1 — foundational

**`perplexity-research-suite`** (this skill — shipped Wave 1B)
The menu and router. You're reading it.

**`perplexity-citation-monitoring`** (Wave 1C — pending)
Will scan whether Oliver's site (or his clients' sites) are cited by Perplexity for target queries. Runs on a schedule via the Sonar API so it doesn't burn the shared Pro browser cap. Output: a tracker of "queries we want to be cited for, and where we currently stand."

When to use (once shipped): standing measurement of AI-search visibility for the most active clients.

### Wave 2 — flagship

**`perplexity-blueprint-research`** (pending)
Takes accumulated vault knowledge (patterns, tactics, tools, opportunities) and produces validated, agent-executable blueprints with readiness scores. The biggest skill in the suite. Uses 30-50 Pro Search queries per deep run.

When to use (once shipped): when a process, system, or workflow needs to graduate from "we have notes on this" to "an agent can run this end-to-end." Examples: a full client-onboarding blueprint, a Core 30 page-build blueprint, a venture-spin-up blueprint.

### Wave 3 — discovery engines

**`perplexity-topic-gaps`** (Wave 3A — pending)
Discovers content gaps in a niche — topics that have low AI-search saturation, questions the existing top results don't answer well.

When to use (once shipped): when planning content for a new client, a new vertical, or an existing client's expansion.

**`perplexity-client-discovery`** (Wave 3B — pending)
Profiles prospects: business shape, current vendors, likely decision-makers, recent moves. The research engine for Keelworks lead-gen.

When to use (once shipped): when researching a specific prospect before outreach.

### Wave 4 — situational

**`perplexity-niche-validation`** (Wave 4A — pending)
Validates whether a niche is worth entering: market size, competitor density, demand signals.

When to use (once shipped): before committing to a new vertical (residential HVAC, plumbing, roofing, etc.).

**`perplexity-competitor-move-detection`** (Wave 4B — pending)
Detects competitor moves: launches, hiring, content velocity, pricing changes.

When to use (once shipped): when a Watchdog report flags movement and Oliver wants the full context.

**`perplexity-ai-overview-hardening`** (Wave 4C — pending)
Researches what triggers Perplexity to cite a given URL. The reverse-engineering skill for AI-search optimization.

When to use (once shipped): after the first 15-30 client pages ship and we want to study why certain pages get cited and others don't.

### Wave 5 — standing monitoring

**`perplexity-acquisition-signal`** (pending)
Standing scan for acquisition signals — buyout chatter, fundraising signals, executive moves in tracked verticals. Runs on a schedule via the Sonar API.

When to use (once shipped): once Keelworks has enough clients in a tracked vertical to make M&A intelligence valuable.

---

## How the router works

Three patterns, depending on what Oliver said.

### Pattern A — Oliver asked for the menu

If the trigger phrase is a general menu question ("what Perplexity skills do I have," "perplexity menu," "what can Perplexity do for me"), present the menu and stop.

Output shape:

> Here's what's in the suite. Shipped skills are ready to run; pending ones land in upcoming waves.
>
> **Shipped:**
> - `perplexity-refinement` — refine a vault artifact with external citations and counter-evidence
> - `perplexity-research-suite` — this router
>
> **Pending (in build order):**
> - `perplexity-citation-monitoring` (Wave 1C) — standing scan of "are my pages cited"
> - `perplexity-blueprint-research` (Wave 2) — turn vault knowledge into agent-executable blueprints
> - ... (the rest)
>
> Capacity this week: ~X of 200 Pro Search queries used (best-effort tally from execution logs).
>
> What do you want to do?

Then wait. Oliver names a goal or a skill. Route accordingly per Pattern B or Pattern C.

### Pattern B — Oliver named a research goal in natural language

Map the goal to a skill. Use this table:

| Goal phrasing | Routes to | Confidence |
|---|---|---|
| "validate / fact-check / find sources for / deepen / refine [vault file]" | `perplexity-refinement` | high |
| "find counter-evidence on [vault file]" | `perplexity-refinement` (with template 5) | high |
| "what's changed about [topic] since [date]" | `perplexity-refinement` (with template 6) | medium |
| "blueprint / build out / agent-executable / readiness-scored process for [X]" | `perplexity-blueprint-research` | high — but skill is pending |
| "what content gaps exist in [niche]" | `perplexity-topic-gaps` | high — pending |
| "research this prospect / who is [business] / profile [client]" | `perplexity-client-discovery` | high — pending |
| "should I enter [niche] / is [vertical] worth pursuing" | `perplexity-niche-validation` | high — pending |
| "what's [competitor] doing / are competitors moving / detect competitor moves" | `perplexity-competitor-move-detection` | high — pending |
| "why does Perplexity cite [URL] / what makes a page get cited" | `perplexity-ai-overview-hardening` | high — pending |
| "is [my site / client site] cited by Perplexity / track citations" | `perplexity-citation-monitoring` | high — pending |
| "any acquisition signals in [vertical] / who's getting bought" | `perplexity-acquisition-signal` | high — pending |

If the routing is unambiguous (one clear match) and the skill is shipped, invoke it directly using its primary trigger phrase. Tell Oliver which skill you're invoking and why.

If the routing is unambiguous but the skill is **pending**, surface that:

> The right skill for that is `perplexity-blueprint-research`, which is pending (Wave 2). It hasn't shipped yet. The closest shipped alternative is `perplexity-refinement` — if you have a vault artifact that already roughs out the process, refinement can pressure-test the claims and surface gaps. Want to do that, or would you rather defer until blueprint-research ships?

If the routing is ambiguous (the goal fits two skills), surface the top two candidates with one-line tiebreakers:

> Two skills fit:
> 1. `perplexity-refinement` — if you have a vault artifact you want me to refine, this writes findings back to that file.
> 2. `perplexity-topic-gaps` — if you're trying to find what's missing in the broader niche (not a specific file), this scans for gaps.
>
> Which?

Wait for Oliver. Then route.

### Pattern C — Oliver named a specific skill

If Oliver said "run perplexity-refinement on the panel-upgrade brief," that's not really a router task — the right move is to skip the menu and invoke `perplexity-refinement` directly. But if the trigger fired anyway (perhaps because the wording was ambiguous), confirm the skill, surface the capacity tally, then hand off.

---

## Capacity status — how the tally works

The router reads recent execution logs and counts query usage from the past 7 days. The tally is **best-effort, not authoritative** — the source of truth is Perplexity's own account dashboard, not vault logs.

### How to build the tally

1. Look in `~/workspace/second-brain/04_projects/clients/_active/ev-electric-services/execution-logs/` and `~/workspace/repos/<venture>/.kos/execution-logs/` for execution-log files updated in the last 7 days.
2. Grep each file for lines matching `Queries run: N` or `Pro Search queries used: N` patterns.
3. Sum the N values. That's the rough weekly tally.

This will miss queries run outside Cowork (manual sessions in the Perplexity web app, queries run from other Claude surfaces). It will also miss usage that wasn't logged. The number is a floor — actual usage is likely a little higher.

### What to surface

Always surface the tally when the router presents the menu (Pattern A) or routes to a high-cost skill (Pattern B with refinement at `deep`, or any blueprint-research call). Format:

> Capacity this week: ~X of 200 Pro Search queries used (best-effort tally from execution logs).

When usage approaches the cap, warn before invoking high-cost skills:

| Tally | Warning behavior |
|---|---|
| < 100 | No warning. Surface the tally only. |
| 100-150 | Surface the tally. Mention that `deep` refinements and any blueprint runs will use a meaningful chunk of remaining budget. |
| 150-180 | Recommend `light` or `medium` instead of `deep`. Defer blueprint-research unless urgent. |
| > 180 | Recommend deferring browser-based runs except critical ones. Standing scans should route through Sonar API where possible. |

The operator decides. The router warns; it doesn't block.

### When the tally can't be built

If no execution logs were updated in the last 7 days, surface that fact instead of a number:

> Capacity this week: no execution-log signal in the last 7 days (so either no Perplexity work has run, or runs weren't logged). Best-effort treat as unknown.

---

## How to hand off to a sub-skill

When the routing decision lands on a shipped skill, the router invokes that skill by using its primary trigger phrase. The handoff is conversational, not magic — the next message to the operator should read like the sub-skill has taken over.

### For perplexity-refinement

The handoff looks like:

> Routing to `perplexity-refinement`. The skill will take it from here.
>
> Running refinement on `<artifact-path>`.
>
> [Now follow the perplexity-refinement skill's Phase 1 — Parse the target artifact.]

The router doesn't repeat the sub-skill's full workflow. It just kicks off the sub-skill's logic by following the sub-skill's SKILL.md from Phase 1.

### For sub-skills that aren't shipped yet

Don't fake the handoff. Tell Oliver the skill is pending and offer:

- The closest shipped alternative (usually `perplexity-refinement` for anything vault-artifact-shaped).
- A note to queue the work for when the skill ships.
- A pointer to the relevant handoff file in `_meta/handoffs/perplexity-skill-build/` so Oliver can prioritize the build sequence.

---

## Inputs the router needs

The router reads these from the operator's message or from vault state. Confirm only when ambiguous. Present any clarifying questions as plain text (the `AskUserQuestion` tool is glitching per Oliver's standing memory).

1. **The research goal** — what does the operator want to know or do? Required. If the trigger phrase didn't include one, ask.
2. **The target artifact (if applicable)** — for refinement and any future skill that operates on a specific vault file. Required for those routes; not required for discovery-engine routes.
3. **Depth / breadth preference (if applicable)** — for refinement, `light` / `medium` / `deep`. For blueprint-research and others, depth controls vary by skill. Defer to the sub-skill's own defaults if Oliver doesn't specify.

If a required input is missing, ask once. Don't keep asking — if Oliver's answer is "you decide," pick the safe default (lowest cost, narrowest scope) and proceed.

---

## Suite-level vocabulary

Terms the router uses that show up across sub-skills.

- **Pro Search** — Perplexity's heavier-compute reasoning mode (the thing the $20/mo subscription pays for). Standard search is the free tier and is unlimited but lighter. Sub-skills run Pro Search by default.
- **Sonar API** — Perplexity's pay-per-query API. Used by scheduled scans (citation-monitoring, acquisition-signal) so they don't draw on the Pro browser weekly cap.
- **Depth** — refinement uses `light` / `medium` / `deep` with caps at 3 / 7 / 15 queries. Other sub-skills have their own depth vocabularies.
- **Weekly cap** — ~200 Pro Search queries per rolling 7-day window. The number the router tracks against.
- **Suite cache** — the frontmatter field (`perplexity-refined: YYYY-MM-DD` for refinement; per-skill equivalents for others) that prevents the same artifact being re-processed inside the refresh window.

---

## Integration with other skills

The router plays well with the existing skill set.

### vis-extraction

When `vis-extraction` finishes producing a new source note and offers the Phase 9 hook for refinement, the router can be invoked instead of jumping straight to `perplexity-refinement` — useful when the operator isn't sure whether refinement is the right next move at all (vs. primer extension, tactic-note draft, or doing nothing). The router presents the menu and dispatches.

### service-seo-research

Same hook as vis-extraction. Service brief finishes; the operator can call the router instead of going straight to refinement.

### meta-document-primer

The router is **not** the primer comprehension surface — `meta-document-primer` owns that. But the two coexist: a comprehension question ("help me read this synthesis") routes to `meta-document-primer`; a research question ("what does Perplexity say about the claims in this synthesis") routes through this router to `perplexity-refinement`.

### multi-source-synthesis

The router can dispatch to `perplexity-refinement` against a synthesis document. After the refinement lands, `multi-source-synthesis` is the natural next step for promoting any new patterns the refinement surfaced. The router doesn't invoke `multi-source-synthesis` directly — it stops after the refinement dispatches.

---

## Output contract

Every router invocation produces exactly these outputs:

1. **The menu (Pattern A only)** — listed in chat. Not a file. Read-only.
2. **A routing decision (Patterns B and C)** — stated in chat. Names the chosen skill, the reason, and any pending-skill caveat.
3. **A capacity tally** — surfaced for menu invocations and for any handoff to a high-cost skill. Best-effort number from execution logs.
4. **The handoff** — the sub-skill's first-step output, run inline. The router doesn't repeat the sub-skill's full workflow; it kicks it off and lets the sub-skill take over.
5. **No vault files** — the router never writes. The sub-skill it routes to owns all writes.

---

## Plain-language requirement

Per [[plain-language-conventions]] and the standing `feedback_plain_language_default.md` memory: the menu listing, the routing explanations, and the capacity tally all read in plain language. Short sentences. Conversational rhythm. Concrete over abstract. The router is a customer-service desk for the suite — write it like one.

---

## Vault stewardship

Per [[vault-stewardship-principles]]:

1. **Read-only.** The router writes nothing to the vault. If the operator asks for a written record of the routing decision, surface the request and offer to write a short note via the appropriate sub-skill or as an execution-log entry — not as a new vault primitive owned by this skill.
2. **Don't propose new folder structure.** The router operates over existing skill files. It doesn't propose new folders in `second-brain/` or new files under `skills/`. Those are the sub-skills' jobs.
3. **Slug-only wikilinks.** When the router's chat output references vault notes, use `[[slug]]`, not `[[path/slug]]`.

---

## Verification before declaring done

Before reporting completion to the operator:

1. **Routing decision is explicit.** The operator knows exactly which skill was chosen and why. No silent picks.
2. **Pending-skill caveats are surfaced.** If the right answer is a pending skill, the operator knows that and was offered an alternative or a deferral.
3. **Capacity tally was surfaced** when it should have been (menu invocations, high-cost handoffs).
4. **The handoff actually ran** when the chosen skill was shipped — the sub-skill's first step was started, not just promised.
5. **No vault writes happened from this skill** — only the sub-skill's writes, if any.

---

## Reporting back to the operator

The router doesn't produce a separate completion report — its job is to dispatch, and the sub-skill produces the actual completion report. The router's "completion" looks like: "Routing to [sub-skill]" followed by the sub-skill running.

If the router stopped without dispatching (Pattern A menu only, or operator chose to defer), the terse summary is one line:

> Menu surfaced. Capacity: ~X / 200 this week. No skill invoked.

That's the receipt.

---

## Cost-management rules

The router itself doesn't run Perplexity queries, so it has no per-invocation cost. Its cost surface is the weekly cap the sub-skills draw against. See `~/workspace/skills/perplexity-shared/references/perplexity-cost-rules.md` for the rules every sub-skill follows.

The router's job in the cost-management story is **surfacing the tally** and **warning before high-cost dispatches**. Don't block — Oliver decides. Don't hide queries — the tally is visible at every menu invocation.

---

## Out of scope (v1.0)

Explicit non-goals for the v1 build:

- **Live API-based budget tracking.** The router does not call the Perplexity account dashboard to read actual usage. The tally is best-effort from execution logs.
- **New sub-skill functionality.** The router doesn't add capability to sub-skills. If a sub-skill needs a feature, the fix lives there.
- **Cross-skill orchestration.** The router routes to one skill at a time. It doesn't chain refinement → blueprint-research → topic-gaps in a single invocation. Multi-step research workflows can be added later as a separate skill.
- **Auto-routing based on vault state.** The router doesn't watch for "vault artifact X is stale, refine it." That belongs to a future maintenance skill, not here.
- **Sonar-API direct calls.** The router doesn't call Sonar. Sub-skills that use Sonar (citation-monitoring, acquisition-signal) call it themselves.

---

## Reference files

When you need them, read these:

- `~/workspace/skills/perplexity-shared/references/perplexity-browser-setup.md` — pre-query browser checks every sub-skill uses
- `~/workspace/skills/perplexity-shared/references/perplexity-cost-rules.md` — per-invocation caps, weekly budget, Sonar fallback
- `~/workspace/skills/perplexity-shared/references/perplexity-query-templates-index.md` — index of every sub-skill's query templates
- `~/workspace/skills/perplexity-refinement/SKILL.md` — the Wave 0 skill the router lists
- `~/workspace/second-brain/_meta/handoffs/perplexity-skill-build/_README.md` — the build roadmap (wave order, pending skills, suite-level rationale)
- `~/workspace/second-brain/_meta/plain-language-conventions.md` — voice rules
- `~/workspace/second-brain/_meta/conventions.md` — KOS naming and frontmatter

---

## Maintenance notes

### M1: New skill ships in the suite (added 2026-05-27, v1.0)

**The issue:** A new Perplexity-suite skill ships (Wave 1C, 2, 3A, etc.). The router's menu list still shows it as "pending."

**How it surfaces:** Oliver triggers the menu and the new skill isn't listed correctly, or the router routes to the pending fallback when the real skill is now ready.

**How to fix:** Update this SKILL.md in two places — the "Wave X — [name]" section under "The suite," and the routing table under "Pattern B." Bump the `updated:` line. Update the shared query-templates-index too if the new skill ships its own templates.

### M2: Perplexity changes the weekly cap (added 2026-05-27, v1.0)

**The issue:** Perplexity changes its tier structure or the weekly Pro Search cap moves from ~200.

**How it surfaces:** The cost-rules file gets updated (it's the single source of truth). The router's warning thresholds (100 / 150 / 180) become wrong.

**How to fix:** Update the thresholds in the "Capacity status" section of this file to match the new cap (rough scaling — 50% / 75% / 90% of new cap). Confirm the cost-rules file already reflects the new number. Bump `updated:`.

### M3: Execution logs stop showing query counts (added 2026-05-27, v1.0)

**The issue:** Sub-skills stop writing "Queries run: N" lines to their execution-log entries. The tally becomes unbuildable.

**How it surfaces:** The router can't surface a usage number; menus go out without capacity status.

**How to fix:** Track down which sub-skill stopped logging and fix its execution-log step. The discipline is in each sub-skill's "Phase 5 — Surface follow-ups" or equivalent — they all need to write the query count. This is a sub-skill bug, not a router bug; the router just exposes it.

---

## How to add a new maintenance note

When the router errors or produces a miss in production, add a new entry: **Issue → How it surfaces → How to fix → Why it wasn't designed away.** Date-stamp it. Future-Claude learns from past misses without re-hitting the same wall.

---

## See also

- [[perplexity-refinement]] — Wave 0, the first skill the router lists
- [[perplexity-browser-setup]] — shared browser setup
- [[perplexity-cost-rules]] — shared cost rules
- [[perplexity-query-templates-index]] — shared templates index
- [[meta-document-primer]] — the comprehension-routing analog (different domain, similar dispatcher shape)
- [[plain-language-conventions]] — voice rules
- [[conventions]] — KOS naming and frontmatter rules
- [[wave-1b-perplexity-research-suite-router|handoff]] — the originating handoff
- [[_README|perplexity-skill-build roadmap]] — the build sequence the router lists
