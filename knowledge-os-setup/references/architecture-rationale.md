# Architecture Rationale

## Why one Obsidian vault, not many

The user's `knowledge-os_architecture-and-expansion-system.md` calls for a "Multi-Vault Architecture" with separate vaults for core, projects, domains, and shared intelligence. This sounds right but conflates two concepts: **knowledge boundaries** (folder roots that scope agent context, repo locality, and human mental models) and **Obsidian vaults** (the technical primitive that defines indexing, linking, search, and graph view).

The user wants both. The trick is recognizing they are different layers of abstraction.

### What Obsidian vaults actually do

A vault is a folder Obsidian points at, with its own `.obsidian/` config. Inside one vault:
- `[[wikilinks]]` resolve
- The graph view shows all connections
- Dataview indexes everything
- Omnisearch indexes everything
- Quick switcher finds anything

Across vault boundaries: none of that works. Links don't resolve. Graph stops. Dataview is per-vault. The user is in a different app instance.

### What the user's architecture doc actually requires

Reading the doc carefully, the requirements are:

- **Core, project, domain, and shared-intelligence separation** — for organization
- **Project knowledge living next to code** — so agents working on a project read scoped context
- **Cross-project intelligence sharing** — the compounding loop (`05_shared-intelligence/`)
- **Promotion from project → shared** — non-negotiable, "no project is complete without promotion"
- **Knowledge reuse across projects** — query shared first, contribute back

Of these, only the cross-project sharing requires the things-can-link assumption. The rest are organizational.

### The resolution

- **Folders** for the conceptual separation (core, domains, projects, shared)
- **One Obsidian vault** at the root so the human's daily reading and the cross-project sharing both work
- **Repo-local `.kos/` directories** for project knowledge that lives with the code
- **Symlinks** from the vault into repos so the human reads project notes inside Obsidian without duplicating files
- **Separate Obsidian vaults** only when sensitivity demands a hard air gap (Tier 3)

### Why this is right for this user specifically

The user is a solo operator processing 10+ external sources/week. At that volume:
- Cross-source pattern recognition is the highest-value output
- Patterns become visible only when Dataview can query across all source notes
- Dataview only queries within one vault
- → Multi-vault would defeat the entire purpose

For a team or an enterprise with strict role separation, multi-vault might be defensible. For a solo operator, it's a self-imposed handicap.

### The Tier 3 exception

When data sensitivity makes the air gap a feature (regulated clients, M&A work, personal financial data), use a separate Obsidian vault. Yes, you lose cross-vault links. That's the security tradeoff and it's worth it for this category. Patterns can still be promoted manually after sanitization — copy the pattern, strip the specifics, paste into the main vault.

### What this means for agents reading this skill

If a future agent (or this user, or another Claude instance) suggests splitting the second-brain vault into multiple Obsidian vaults to "match the architecture doc," push back. The architecture doc's intent is satisfied by the folder structure. Splitting at the Obsidian level breaks compounding intelligence and contradicts the user's actual requirement.

If the user themselves asks for the split: explain this rationale, offer the Tier 3 air-gapped vault for the sensitivity case, and confirm before changing anything structural.
