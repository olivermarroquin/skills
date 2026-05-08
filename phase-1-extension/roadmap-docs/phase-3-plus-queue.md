---
type: roadmap
status: living-document
created: 2026-05-04
updated: 2026-05-04
phase: 3-plus
tags: [roadmap, phase-3-plus, queued]
---

# Phase 3+ Queue

> **Purpose:** A living record of capabilities deliberately deferred after Phase 1, to be re-evaluated after Phase 2 ships its MVP. This is committed work that's been sequenced, not forgotten.
>
> **How to use this doc:**
> 1. Don't activate any item until Phase 2 has shipped and run for at least 4 weeks of real use
> 2. Before activating, re-read the "Pushback / what I might be wrong about" section for that item
> 3. Items can be re-prioritized, scoped down, or killed at any review
> 4. New items get added to "Captured but not yet structured" first; promote to a full entry when seriously considering

---

## Re-evaluation discipline

Every item in this doc had a reason for being deferred. Some of those reasons:
- Phase 2 needs to ship and prove value first
- Capability requires AI agents to do something they can't reliably do yet
- The item assumes muscle memory or workflow patterns that don't exist yet
- The cost of building blind is high relative to the value of building informed

When re-evaluating an item, ask:
1. Has Phase 2 shipped and been used for at least 4 weeks?
2. Has the underlying constraint (capability, capacity, dependency) actually changed?
3. Have I learned anything from using the system that changes the design?
4. Is this still the highest-value next thing, or has something else surfaced?

If yes to all four, scope it as Phase N. If no to any, defer further.

---

# Active queue

Items below are in rough priority order, but priority is not commitment.

---

## 1. Intelligent ingestion organizer (auto-routing of extracted notes)

### Hypothesis
After Phase 2 extracts source notes, an intelligent layer automatically organizes them into existing domain clusters, creates new domain folders when a critical mass of related sources accumulates, and updates relevant MOCs without manual intervention.

### Why this matters
At 10+ sources/week, manual organization is the friction point that kills compounding intelligence. Sources sit in `00_inbox/sources-pending/` because organizing them feels heavy.

### Why not now
- Phase 2's MVP needs to ship first to produce the source notes that need organizing
- The "right" clustering taxonomy emerges from 50+ real source notes, not from a priori design — we'd be building organization rules blind
- Manual organization for the first 4 weeks of Phase 2 reveals what natural categories actually emerge

### What would have to be true to start
- Phase 2 has shipped and been used for at least 4 weeks
- At least 30 source notes have been processed and manually filed
- Clear categories have emerged organically (e.g., "agent-architecture sources," "monetization-strategy sources," "tool-discovery sources")
- The cost of manual organization is documented as a real friction point in retros

### Dependencies
- Phase 2 (paste URL → auto-extract pipeline)
- A meaningful corpus of organized sources to learn from

### Pushback / what I might be wrong about
The instinct that "AI should organize this for me" is often a way to avoid the *judgment* of organization rather than its *execution*. The actual decision of "this source is about X domain" requires understanding what the source argues, which is the same judgment you'd apply manually anyway. An organizer that auto-routes might just shuffle sources into wrong buckets at scale.

If this becomes the next priority: scope it as a *suggestion engine* (proposes a destination, you confirm with one click), not an *auto-router* (moves files without confirmation).

### Re-evaluation trigger
After 4 weeks of Phase 2 use, if the inbox backlog has grown past 10 unprocessed sources for the wrong reason (organization friction, not judgment).

---

## 2. Cross-domain idea synthesis & cluster growth

### Hypothesis
The system identifies when ideas across different domains (e.g., AI knowledge × wholesaling real estate × content systems) connect into novel offerings. Clusters of related sources grow over time, and the system proactively surfaces "you have enough material on X domain to do something with it" insights.

### Why this matters
The compounding value of a knowledge OS isn't in the individual notes — it's in the connections between them. The user explicitly named real estate × AI as an example: the idea is that ingested knowledge in two unrelated domains can be combined into a service or product offering.

### Why not now
- Cross-domain synthesis requires a substantial corpus across multiple domains; we don't have that yet
- The "real estate × AI" example was hypothetical, not an active interest; the actual cross-domain pairs that matter will surface from real ingestion patterns
- This is downstream of #1 (organization) — synthesis without clean clusters is noise

### What would have to be true to start
- Phase 2 has shipped and produced at least 50 source notes across 3+ domains
- At least 5 patterns have been promoted to `05_shared-intelligence/patterns/`
- The user has noticed at least one valuable cross-domain connection manually (validates the underlying hypothesis)

### Dependencies
- Phase 2
- Item #1 (intelligent organization) likely needs to ship first
- A working `MOC-shared-intelligence` view (already exists)

### Pushback / what I might be wrong about
"AI surfaces cross-domain connections" sounds magical but in practice often produces low-signal pairings. The connections that matter usually require human judgment about what's actually pursuing-worthy. An auto-synthesizer might generate 20 "interesting connections" per week, of which 1-2 are real, and the noise will drown the signal.

If this becomes priority: build it as a *weekly digest* of candidate connections you can browse and dismiss, not as a real-time alerting system.

### Re-evaluation trigger
After 8+ weeks of Phase 2, when the user spontaneously says "I noticed this video about X relates to that older one about Y" without prompting.

---

## 3. YouTube channel monitoring with auto-alerts

### Hypothesis
The system watches a curated list of YouTube channels, automatically processes new videos when they drop, places them in the right domain folder, and alerts the user with: where it landed, how it relates to existing knowledge, and what business possibilities the new content surfaces.

### Why this matters
At the user's intake volume goal (10+/week), manual checking of channels is a real chore. Channel monitoring reduces capture friction to zero for known-good sources.

### Why not now
- Need a curated channel list, which only emerges after a few weeks of "which creators consistently produce signal vs. noise"
- "Alert me when processed" requires the processing pipeline (Phase 2) to be reliable enough that automatic processing doesn't generate noise
- YouTube API and/or yt-dlp polling is solvable but not trivial; not worth building until the consumer (Phase 2 pipeline) is stable

### What would have to be true to start
- Phase 2 has shipped and is reliable for manually-pasted URLs
- User has identified 5-10 channels worth monitoring (signal-rate ≥ 50%)
- A retention policy exists for channels that drift to noise

### Dependencies
- Phase 2 reliable
- A workflow for "I want to add this channel to monitoring" / "this channel is producing noise, drop it"

### Pushback / what I might be wrong about
Channel monitoring at 10+ channels easily generates 5-10 videos/day. Even if 80% are tier-3-or-noise, the ones that surface as alerts will create FOMO pressure to engage. The user could end up *more* time-fragmented, not less, because every alert pulls attention.

If this becomes priority: scope it as a daily/weekly digest, never real-time alerts. And include a noise-rate retention policy: any channel with <30% tier-1-or-2 over 4 weeks gets auto-dropped.

### Re-evaluation trigger
After Phase 2 stable, when manual URL pasting becomes the bottleneck and the user has 5+ channels they consistently want to track.

---

## 4. Pivot detector for active projects

### Hypothesis
When a newly-ingested source describes a faster/better/more efficient way to do something the user is actively building, the system flags this with: pros, cons, and a structured pivot conversation prompt.

### Why this matters
Without this, valuable improvements get buried in the source corpus and never make it back to active work. The user explicitly cited examples (Figma + AI design, Claude managed agents, etc.) where they wanted to know.

### Why not now
- Requires a reliable model of "what the user is actively building" — only achievable once project vaults (`.kos/`) are populated for at least 2 active projects
- The "pivot or not" decision requires nuanced judgment about sunk cost, transition risk, and timing — AI's track record at this kind of advice is mixed at best
- High false-positive rate would destroy ability to ship — every other day generating a "you should pivot" suggestion is worse than no suggestion

### What would have to be true to start
- At least 2 projects have `.kos/` initialized with current spec/scope/state
- Phase 2 is producing reliable extracted insights
- The user has had at least one valuable pivot moment they'd want the system to have caught (validates the need)

### Dependencies
- Phase 2
- Project vault initialization for active projects (deferred from Phase 1)
- Some form of "active project state awareness" mechanism

### Pushback / what I might be wrong about
This is the highest-risk item in the queue. AI-suggested pivots, applied at the rate ingestion would generate, can destroy the consistency required to actually finish projects. Most "you could do this faster" suggestions are not worth the context-switch cost. The user's instinct to want this is real, but the feature as imagined could easily produce a worse outcome than ignoring it.

If this becomes priority: scope it as a *weekly retrospective companion* — once a week, surface up to 2 candidate pivots from the past week's ingestion, with both pros and cons, and require a 24-hour cool-off before acting. Never real-time.

### Re-evaluation trigger
After Phase 2 stable AND at least one project shipped using the system. Don't activate before the system has helped ship something.

---

## 5. Specialized agent teams with daily standups

### Hypothesis
The user can call on a team of specialized AI agents (frontend designer, backend coder, API automation tester, UI automation tester, etc.) for an active project. The agents meet on a recurring schedule (e.g., 8am daily scrum), discuss progress, identify blockers, plan recruitment of new agents for emerging needs.

### Why this matters
The user wants the leverage of a real team without the overhead of hiring. The vision extends to expert agents (investment/trading strategist, etc.) who synthesize ingested knowledge into actionable expertise.

### Why not now
- Multi-agent collaboration is *the* hardest unsolved problem in current AI tooling. Agents productively disagreeing, building on each other, self-correcting, and recovering from errors is mostly fantasy at present capability levels
- The "8am daily scrum" pattern assumes agents have memory continuity, durable opinions, and goal-stability across sessions — they don't, reliably
- Even if it worked technically, the management overhead of N agents could exceed the leverage gain. A 20-minute "daily scrum" that catches nothing is a 20-minute tax
- Anthropic's own products (Claude Code, sub-agent patterns) are evolving fast in this space — building custom multi-agent tooling now will likely be obsoleted by platform features within 6 months

### What would have to be true to start
- Multi-agent frameworks (LangGraph, AutoGen, OpenAI Agents SDK, or platform features) demonstrate reliable productive disagreement and self-correction
- The user has a project with workload genuinely too large for solo + Claude execution
- A specific pain (not general aspiration) drives the need

### Dependencies
- Phase 2
- Phase 1 of capability engine (mentioned in master-system-map but not built)
- Likely external dependencies on platform capability evolution

### Pushback / what I might be wrong about
This is the user's most enthusiastic item and also the one with the largest "imagined value vs. real-world complexity" gap. The image of a coordinated AI team is compelling. The reality of running one productively, today, is mostly a frustration generator.

A scoped-down version that *would* work today: a single project agent (PM-style) that maintains context and asks the user clarifying questions, with sub-agents called sequentially (not concurrently) for specialized tasks. That's much closer to what's currently buildable. Reframe before activating.

### Re-evaluation trigger
When an active project genuinely exceeds solo + single-agent capacity, AND multi-agent tooling has matured demonstrably (concrete examples of teams working productively, not vendor demos).

---

## 6. Web automation (Playwright) for tool documentation & SOPs

### Hypothesis
The system browses the web, figures out tool workflows by interacting with them, documents the workflows, creates SOPs to teach the user, captures "business secrets" (the non-obvious details that matter), and stores those secrets in a special place.

### Why this matters
Tool literacy is a real competitive advantage. Most YouTube tool tutorials skip the 20% of details that actually matter for production use. A system that probes a tool and documents it from first principles is genuinely valuable.

### Why not now
- Playwright + AI for autonomous web exploration is technically feasible but reliability is poor; sites change, auth breaks, rate limits hit
- "Capture business secrets" is the hardest part — figuring out what's actually non-obvious requires expertise the system doesn't have
- This is a substantial separate build (likely 4+ weeks of focused work), worth doing only after Phase 2's value is proven

### What would have to be true to start
- A specific tool the user wants to document (not abstract — a real one)
- Phase 2 stable so the documentation has a place to land
- Anthropic's "Claude in Chrome" beta or similar tooling has matured (this is mentioned in product info as a beta product)

### Dependencies
- Phase 2
- Browser automation tooling that's reliable (potentially Claude in Chrome rather than custom Playwright)

### Pushback / what I might be wrong about
The "system documents tools by exploring them" pattern is appealing but requires the system to have *taste* about what matters in a tool. Without that, you get exhaustive procedural documentation that doesn't capture the non-obvious value. The good documentation of tools comes from people who've used them in production and learned the failure modes — which a system can't do without actually trying to ship something with the tool.

If this becomes priority: scope it as a *companion* to manual tool exploration. The system observes you using a tool, takes structured notes, asks clarifying questions about why you made certain choices, and produces a draft SOP you refine.

### Re-evaluation trigger
When Anthropic's Claude in Chrome ships (currently beta) or when a comparable tool reaches production reliability.

---

## 7. Personal learning & retention system

### Hypothesis
A separate repo (or vault domain) where the user can ask questions about ingested knowledge, get explanations, generate flashcards/quizzes from the corpus, and run hands-on practice projects. Connected to the ingestion pipeline so new knowledge automatically generates learning materials. Tracks knowledge growth and learning trajectory by subject.

### Why this matters
Ingestion without retention is just hoarding. The user explicitly wants to actually *learn* the tools, strategies, and concepts being captured, not just file them.

### Why not now
- This is a substantial separate system, likely 2-4 weeks to build
- Without Phase 2 producing structured source notes, there's no source corpus to generate learning materials from
- The retention method (flashcards vs. projects vs. spaced repetition) needs to match how the user actually learns — which is best determined empirically with a few test sources

### What would have to be true to start
- Phase 2 has produced a corpus of source notes
- The user has identified 1-2 specific knowledge areas where retention is lacking
- A retention method has been tested manually (Anki, hands-on project, teaching it back) and validated

### Dependencies
- Phase 2
- A separate repo or vault domain (architectural decision: where does this live?)

### Pushback / what I might be wrong about
Many "learning systems" become procrastination structures — the user spends time managing the learning system instead of actually applying knowledge to ship things. The fastest retention loop is: ingest → try to apply to a real project → retain through use. Adding a separate flashcard layer might be redundant.

If this becomes priority: start with the simplest version — a weekly "explain it back" session against the past week's syntheses. Build complexity only if simple is insufficient.

### Re-evaluation trigger
When the user notices specific knowledge gaps despite consistent ingestion, OR when ingested knowledge consistently fails to translate into shipped work.

---

## 8. Investment / trading expert agent

### Hypothesis
A specialized agent (or agent system) that synthesizes ingested investment/trading knowledge, helps the user learn, strategize, build, and eventually automate a trading or investment system that produces profit. Open-ended on what to trade.

### Why this matters
The user articulated this as a long-term vision: an expert system that knows the best strategies, hidden gems, and lessons from online content, and helps execute on them.

### Why not now
- This is the highest-risk item in financial terms — automated trading without deep domain expertise is well-documented as a path to losses
- "Synthesize the best strategies from online content" is exactly the kind of pattern that, applied to financial markets, produces overfit strategies that fail in live conditions
- Belongs to "Phase 5+" if at all; not adjacent to anything else in the queue
- The user said "not sure trade what yet" — which is a strong signal this is aspiration, not active need

### What would have to be true to start
- A concrete trading strategy the user has manually validated for 3+ months
- Demonstrated profitability before automation
- A risk management framework the user has internalized
- The user has explicitly chosen what to trade

### Dependencies
- Substantial domain expertise that the user would need to build first
- Capital they're willing to risk during the validation phase
- Not a system-build dependency — primarily a personal-readiness dependency

### Pushback / what I might be wrong about
The pattern "AI synthesizes the best strategies from content" is exactly how retail traders lose money. Strategies that "work" in articles and YouTube videos rarely work in production because: (1) they're already priced in by the time content is produced, (2) selection bias — you only hear about strategies that worked once, (3) sizing and risk management are 80% of returns and rarely covered in content.

If this ever becomes priority: scope it down dramatically. Start with paper trading. Use the system for *journal/analysis* before *execution*. Never let the system place trades without human approval until it has demonstrated 6+ months of paper-traded profitability against the user's chosen benchmark.

### Re-evaluation trigger
When the user has manually validated a specific strategy, paper-traded it for 3+ months, and is ready to systematize execution. Not before.

---

## 9. Idea-factory repo integration

### Hypothesis
The vault feeds into a separate `idea-factory` repo (mentioned by user as "almost done" or "somewhat complete") which monetizes ingested knowledge.

### Why this matters
Ingestion → ideation → monetization is the user's stated goal. The idea-factory is the bridge from knowledge to revenue.

### Why not now
- The idea-factory repo exists but is "somewhat complete" — its current state and shape are unknown to me
- Integration design depends on what the idea-factory actually does, which I'd need to see before specifying the integration
- This is more of a *connection* task than a *build* task; the work is in defining the contract

### What would have to be true to start
- I have access to the idea-factory repo or a clear description of what it consumes
- Phase 2 is producing structured outputs the factory can consume (opportunities, content ideas, tool notes)
- The user has identified a specific bottleneck where vault-to-factory friction is real

### Dependencies
- Phase 2
- Visibility into the idea-factory repo

### Pushback / what I might be wrong about
"Integration with another system" projects often fail because the two systems' shapes don't actually fit, and forcing them together creates more friction than separation. Better to know how the idea-factory works first and design the integration once, than build a generic export layer that has to be re-done.

### Re-evaluation trigger
When the user can articulate the specific handoff: "the vault produces X, the factory needs Y, the gap is Z."

---

## 10. Self-aware brain growth tracking

### Hypothesis
The system reports on its own state: how the brain is growing, what's been ingested when, what kinds of content would enhance it next, and produces a self-directed plan to make itself smarter over time.

### Why this matters
Self-awareness about knowledge gaps is genuinely useful. The user articulated wanting the system to "think smartly about where things are going" and "self-make a plan."

### Why not now
- Some of this is already in `_HOME.md`'s existing Dataview queries (recent ingestion, promotion velocity, orphans, domain activity)
- Building a "what should I ingest next" recommender requires understanding what the user's actual goals are at any given moment, which changes
- Premature optimization — easier to start with simple metrics in `_HOME.md` and let the user notice what's missing

### What would have to be true to start
- Phase 2 has produced a substantial corpus
- User has used the existing dashboard for at least 4 weeks
- Specific gaps in self-awareness have been identified ("I wish I knew which domains are stagnating")

### Dependencies
- Phase 2
- 4+ weeks of dashboard use

### Pushback / what I might be wrong about
"AI suggests what to learn next" can produce confident-sounding recommendations that aren't grounded in actual user goals. The user knows their goals; the system knows what's been ingested. The gap that matters is *unknown unknowns*, which AI is bad at surfacing.

If this becomes priority: scope as a monthly retrospective question prompt, not an automated recommender. "Looking at the past month's ingestion: what domain is underrepresented relative to your stated goals? What kind of source would you reach for next?"

### Re-evaluation trigger
When the existing dashboard's metrics no longer feel sufficient AND the user can articulate specifically what's missing.

---

# Captured but not yet structured

(Items that come up later, not yet worth full roadmap entries. Move up to a numbered entry when seriously considering.)

- 

---

# Closed / killed items

(Items that were considered and decided against, with reasoning. Important to keep so we don't accidentally re-consider them.)

- 

---

# Operating principle

When in doubt: defer.

Phase 1 worked because we shipped a small thing well. Phase 2 will work for the same reason. The roadmap above is not a commitment to build any of it — it's a record of considered options, with honest pushbacks, so future-you (or future-Claude) can re-evaluate against real conditions instead of inheriting current enthusiasm.

The most valuable thing about this doc isn't the item list. It's the **pushback sections**. Re-read them before activating anything.
