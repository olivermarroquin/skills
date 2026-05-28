# Project Subfolder Template

When DECOMPOSE creates a new project subfolder at `~/workspace/second-brain/_meta/handoffs/<project-slug>/`, it generates:

1. A `_README.md` using the template below
2. One `.md` handoff file per phase (using the body shape from `handoff-frontmatter-spec.md` + `closing-protocol-template.md`)

The `_README.md` is the per-project tracker. It mirrors the global `_active-chats-tracker.md` for cross-initiative visibility but provides per-initiative depth — the dependency graph, phase-by-phase status, suggested order, and how-to-use instructions for any operator new to the thread.

## Template (substitute the `<PLACEHOLDERS>`)

```markdown
---
type: folder-readme
status: canonical
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
initiative: <project-slug>
phases: <N>
current-phase: <e.g., 0-not-yet-started, 1-shipped, 2-in-flight>
tags: [folder-readme, handoffs, <project-slug>, multi-chat-initiative]
---

# handoffs/<project-slug>/

<2-3 sentence framing — what this initiative produces, why it exists, what success looks like at the end.>

**Each `.md` file in this folder is one self-contained chat prompt.** Open the file, copy everything between the `--- start prompt ---` and `--- end prompt ---` markers, paste into a fresh Cowork chat. The new chat picks up the work without needing context from previous chats.

**This README doubles as the per-initiative tracker** — the source of truth for which phase shipped, which is ready to spawn, and which is queued. Update the table below as each phase moves through its lifecycle.

## Why this initiative exists

<1-2 paragraphs — the gap this initiative closes, the system or pipeline it builds, the downstream value it produces. Cite the originating decision or operator request if it exists.>

## Suggested order

<plain-text dependency graph showing the build order. Use indented ASCII to indicate parallelizable vs. sequential phases. Example:>

```
Phase 1 (foundational — must ship first)
   1  → <short name>                              ← START HERE (keystone)

Phase 2 (build after Phase 1 lands — can run as parallel chats)
   2a → <short name>
   2b → <short name>
   2c → <short name>

Phase 3 (depends on all Phase 2 sub-phases)
   3  → <short name>
```

**Why Phase 1 is the keystone:** <explain the load-bearing reason the first phase blocks everything>.

**Why Phase 2 can parallelize:** <explain which dependencies are absent>.

**Why Phase 3 must wait:** <explain the multi-prerequisite chain>.

## Phase tracker

| Phase | Chat title | Handoff file | Status | Outcome / Blocker |
|---|---|---|---|---|
| 1 | <chat title> | [[phase-1-<short>]] | <status> | <outcome paragraph after shipping, or blocker paragraph while queued> |
| 2a | <chat title> | [[phase-2a-<short>]] | <status> | <outcome / blocker> |
| 2b | <chat title> | [[phase-2b-<short>]] | <status> | <outcome / blocker> |
| ... | ... | ... | ... | ... |

**Status values:**
- ⏳ **Queued — Tier 3** (waiting for explicit trigger; do NOT spawn)
- ⏳ **Queued — Tier 2** (spawn after a sibling phase lands, within ~1 week)
- 🟢 **Ready to spawn** (blockers cleared; spawn whenever bandwidth allows)
- 🔵 **In-flight YYYY-MM-DD** (currently being worked)
- ✅ **Shipped YYYY-MM-DD** (work landed; see Outcome cell)
- ❌ **Cancelled YYYY-MM-DD** (no longer relevant; see Outcome cell for reason)

## How to use a handoff

1. Open the file for the next phase in the suggested order.
2. Copy everything between the `--- start prompt ---` and `--- end prompt ---` markers.
3. Paste into a new Cowork chat. The chat should start in the `second-brain/` project so project instructions auto-load.
4. As the work lands, the chat consuming the handoff runs the closing protocol baked into its prompt — flips the handoff's `status:` to `consumed`, updates this README's tracker, updates the global `_active-chats-tracker.md`, and surfaces a per-repo git command block for the operator to commit.

## Reading order if you're new to this thread

<numbered list pointing to the most relevant primers, blueprints, specs, and execution logs to read before spawning the next phase. Should be 3-5 items.>

1. <link>
2. <link>
3. <link>

## Update protocol

When a phase ships, update this README's tracker table in three ways:

1. Move the status to ✅ **Shipped YYYY-MM-DD**
2. Replace the "Outcome / Blocker" cell with a one-paragraph outcome summary + link to the relevant execution log section
3. Update the next phase's status to 🟢 **Ready to spawn** (or keep ⏳ **Queued** if blockers remain)

Also update the global [[../_active-chats-tracker]] in the same edit. The two trackers must stay in sync — the global one is canonical for cross-initiative visibility; this one is canonical for per-initiative depth.

When a handoff is consumed by a new chat:
1. The closing protocol baked into the handoff flips the handoff file's `status:` from `active` to `consumed`
2. Both this README's tracker and the global tracker get updated in the same closing pass

## What lives here vs. what doesn't

- Phase handoff prompts (this folder) — the bottom-up build sequence for the initiative
- Execution logs of completed phases → `04_projects/clients/_active/<client>/execution-logs/` or repo-level `.kos/execution-logs/`
- Patterns / lessons captured during phase work → `05_shared-intelligence/patterns/` and `lessons/`
- The originating blueprint or spec → `05_shared-intelligence/blueprints/` or `_meta/specs/`

## See also

- [[../_README|handoffs folder README]] — general handoff conventions
- [[../_active-chats-tracker]] — global tracker across all in-flight initiatives
- <link to originating blueprint, spec, or strategic decision>
- <link to relevant execution log if one exists>
```

## Substitution guide for DECOMPOSE

When generating a new project README from this template, DECOMPOSE substitutes:

| Placeholder | What to substitute |
|---|---|
| `<project-slug>` | The kebab-case project slug DECOMPOSE proposed (e.g., `youtube-channel-launch`) |
| `<YYYY-MM-DD>` | Today's ISO date |
| `<N>` | The number of phases in the decomposition |
| `<2-3 sentence framing>` | DECOMPOSE writes from the operator's goal description |
| `<1-2 paragraphs — the gap...>` | DECOMPOSE writes from the operator's goal + any source documents pointed at |
| `<plain-text dependency graph>` | DECOMPOSE generates from its identified dependency graph |
| `<short name>` | Per-phase short name DECOMPOSE proposed |
| Phase tracker rows | One row per generated handoff, all starting at `⏳ Queued — Tier 3` or `🟢 Ready to spawn` per the dependency analysis |
| `<numbered list pointing to primers...>` | DECOMPOSE proposes 3-5 reading-order items based on the source documents the operator pointed at |
| `<link to originating blueprint...>` | DECOMPOSE includes wikilinks to any source docs the operator named |

DECOMPOSE surfaces the substituted README as part of the review gate — operator approves the README + handoff bodies before any file is written.

## Sizing guidance for DECOMPOSE

A good project subfolder has between 3 and 12 handoffs. Outside that range, reconsider:

- **Fewer than 3:** the project might not need a subfolder. A single standalone handoff at `handoff-YYYY-MM-DD-<topic>.md` is enough.
- **More than 12:** the project might need to split into sub-initiatives, each with its own subfolder. Or the unit of work per handoff might be too small — combine related phases.

The three existing exemplar projects size as follows:

- `roadmap-client-seo-onboarding-automation/` — 13 handoffs (large, multi-phase build)
- `perplexity-skill-build/` — 10 handoffs (medium, suite build)
- `intel-routing-rollout/` — 3 handoffs (small, three-chat rollout)

When in doubt, mirror the exemplar most similar in shape to the proposed initiative.

## Related

- `~/workspace/second-brain/_meta/handoffs/roadmap-client-seo-onboarding-automation/_README.md` — exemplar (large, multi-phase build)
- `~/workspace/second-brain/_meta/handoffs/perplexity-skill-build/_README.md` — exemplar (medium, suite build)
- `~/workspace/second-brain/_meta/handoffs/intel-routing-rollout/_README.md` — exemplar (small, three-chat rollout)
- `./tracker-row-shapes.md` — the global tracker shapes the per-project README mirrors
- `./handoff-frontmatter-spec.md` — the per-phase handoff shape
- `./closing-protocol-template.md` — the protocol every generated phase handoff includes
