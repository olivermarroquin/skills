# Phase 3+ Queue Addition — Task System

This is content to **append** to `second-brain/01_ai-operating-system/roadmap/phase-3-plus-queue.md` under a new entry. Do not replace the existing queue file — add this to it.

---

## Item: Source-linked task system with execution backlog

### What it is

A dedicated task management layer that:

- **Lives separately from source notes** — tasks are first-class artifacts in their own folder (proposed: `second-brain/06_tasks/` or similar)
- **Links bidirectionally to triggering sources** — every task entry references the source note that birthed it; every source note's Action log can reference task entries instead of just inline checkboxes
- **Aggregates across all sources** — produces a unified backlog showing every action item across every source, sortable by priority, status, source, project
- **Auto-creates tasks from execution-recommendation checkboxes** — when a user checks "Act now" on a source note, a task entry is created automatically with the source's context attached
- **Supports prioritization, deferral, killing** — tasks have status (planned, in-progress, done, parked, killed), priority, due date (optional), assigned-to (eventually agents)
- **Queryable via Dataview** — "show me all tier-1 source actions still in 'planned' state from the last 30 days"
- **Integrates with eventual agent system** — agents (when they exist) consume from the backlog rather than parsing individual source notes

### What this enables

- **Cross-source visibility:** the user can see all pending actions from all sources in one place, not buried in 50 individual source notes
- **Honest backlog:** "I'm not actually doing anything I said I'd do from these 12 sources" becomes legible
- **Agent handoff:** when PM agents are real, they can pull tasks from the backlog autonomously rather than the user dispatching one-by-one
- **Decision archaeology:** "where did this task come from?" always traces back to a source

### Why this is deferred

- **Depends on Phase 1 control layer (ECS) being stable.** The task system is, fundamentally, a queue of decisions about what executes next. ECS already owns "what executes next" at the system level. Building a parallel task system without ECS coordination = double work and conflict.
- **Depends on Phase 5 capability engine.** Agents-consuming-from-backlog requires capability tracking ("does the right agent exist for this task?"). No capability engine yet → agents can't safely pull from a backlog.
- **Inline action logs (current solution) handle the immediate need.** With ~5-10 source notes, cross-source aggregation isn't yet a real pain point. Inline logs preserve context where it was created.

### What the inline solution gives up

The user has explicitly named what's missing in the current inline approach:

- No cross-source aggregation
- No way to see "everything I said I'd do" in one query
- Execution-recommendation checkboxes are inert (they don't trigger tracking automatically)
- No backlog for future agents to consume

These are the gaps that the task-system build closes.

### Re-evaluation triggers

Build this when ALL of the following are true:

1. ECS is operational at least at MVP level (control layer can sequence work)
2. At least 1 PM agent (any kind) is functional
3. The user has 50+ source notes in the system AND has explicitly named "I can't see what's pending across sources" as a felt pain
4. The inline Action log pattern has been used long enough to have legitimate complaints (3+ months of real use)

### Sub-items and design notes

When this item is built:

- **The Action log section in source notes becomes a sync target**, not the source of truth. Source notes display a live Dataview query of related tasks. The task system holds the canonical state.
- **Execution-recommendation checkboxes auto-create tasks** with the source's context inherited. If user checks "Act now," a task is created with the source's tier, the source's relevance to current goals, the specific action being recommended.
- **The backlog has its own tier system** that may or may not match source-note tier. (Source-note tier is "how to handle this source"; task tier is "how to handle this specific action.")
- **Status transitions are tracked**: a task moves from `planned` → `in-progress` → `done`/`parked`/`killed` and the date of each transition is logged. Reports show throughput, deferral rates, kill rates.
- **The user can manually create tasks** that link to a source even without using the auto-creation flow. Tasks aren't only-from-extractions.

### Dependencies on other queue items

- Depends on: ECS MVP, capability engine MVP, at least one PM agent
- Blocks: future agent-driven task assignment, advanced delegation
- Adjacent to: continuous testing/QA system (which has its own backlog of test failures → fixes)

### Source / triggering insight

Identified during Phase 2 first extraction (2026-05-05). User explicitly named the gap: "when actions are taken on knowledge gathered from videos, I think there should be a way to track what things are actually implemented and make a list of to-do's that we have to do, I will eventually need agents or a control and coordination system to manage all of the tasks."
