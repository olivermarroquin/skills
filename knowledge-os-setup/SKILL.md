---
name: knowledge-os-setup
description: Set up the user's Knowledge OS vault — the multi-boundary, single-Obsidian-vault system that organizes external content (videos, articles), project knowledge, domain knowledge, and shared compounding intelligence. Use this skill when the user asks to install, scaffold, set up, or initialize their Knowledge OS, second-brain vault, KOS, or knowledge-os system. Also use when the user wants to add a new project vault to their existing KOS, when they reference 'KOS Phase 1', or when they want help wiring up Obsidian Templater/Dataview/QuickAdd against the canonical KOS structure. The skill creates folder structure, installs templates, copies seed notes including the home dashboard, and produces a working Obsidian vault. Even if the user's request is partial (e.g. 'just give me the templates' or 'set up the inbox folder'), use this skill — it has the canonical structure and assets.
---

# Knowledge OS Setup

This skill installs the canonical Knowledge OS into the user's workspace. It creates the folder scaffold, installs templates, drops in seed notes (home dashboard, MOCs, conventions, workflows), and prepares the vault for Obsidian.

## Architecture (read this first)

The Knowledge OS is **one Obsidian vault, multiple folder-level boundaries**. The user previously asked about multi-vault separation; the resolution is:

- **One vault** rooted at `<workspace>/second-brain/` for daily reading, linking, and Dataview queries
- **Multiple top-level folders** that mirror the conceptual "vaults" from their architecture doc (core, domains, projects, shared-intelligence)
- **Project knowledge lives in repo `.kos/` folders**, mirrored into the vault via symlink — this gives agents a scoped context boundary while keeping the human's graph view global
- **Tier 3 sensitive data** (regulated, M&A, personal financial) gets a separate air-gapped Obsidian vault — accept the loss of cross-vault links as the security tradeoff

This satisfies every requirement in their `knowledge-os_architecture-and-expansion-system.md` while respecting how Obsidian actually works (links, search, and Dataview do not cross vault boundaries).

## When to use this skill

Trigger on any of:
- "set up my knowledge OS / KOS / second-brain"
- "install the vault structure"
- "scaffold the Obsidian vault"
- "add a project vault for `<project>`"
- "Phase 1 of the knowledge OS plan"
- "wire up Templater and Dataview for my KOS"

If the user just asks for one piece (e.g. "just give me the source note template"), use this skill anyway — the assets are here.

## Workflow

### Step 1 — Confirm the workspace path

Ask the user to confirm their workspace path. Default expectation: `/Users/<name>/workspace/`. Check that `<workspace>/second-brain/` either exists (existing scaffold to extend) or doesn't (fresh install).

If `second-brain/` already has content, ask whether to install non-destructively (recommended) or do a fresh install. The setup script is idempotent — it skips files that already exist — so non-destructive is the default.

### Step 2 — Run the vault installer

Use the bundled script:

```bash
bash <skill-path>/scripts/setup-knowledge-os.sh <workspace-path> <skill-path>/assets
```

This:
- Creates the full directory tree (`00_inbox`, `01_ai-operating-system`, `02_core`, `03_domains/<5 domains>`, `04_projects`, `05_shared-intelligence`, `_meta`, `99_archive`)
- Installs all templates (KOS + VIS + project) into `_meta/templates/`
- Installs seed notes: `_HOME.md`, `conventions.md`, `obsidian-setup.md`, both MOCs, two workflow notes
- Installs three sample notes (source, tactic, opportunity) so the home dashboard shows real content immediately

Show the user the script output. If errors, surface them immediately.

### Step 3 — Verify the install

After the script runs, list the created tree (or a relevant subset):

```bash
find <workspace>/second-brain -maxdepth 3 -type d | sort
```

Confirm all expected folders exist. Then verify a few key files:

```bash
ls <workspace>/second-brain/_HOME.md
ls <workspace>/second-brain/_meta/templates/vis/template-source-video.md
ls <workspace>/second-brain/_meta/conventions.md
```

### Step 4 — Walk through the next steps

Tell the user:

1. **Open Obsidian and "Open folder as vault"** → select `<workspace>/second-brain/`
2. **Install the four required plugins** from Community Plugins:
   - Templater
   - Dataview
   - QuickAdd
   - Omnisearch (recommended)
3. **Configure them** per `_meta/obsidian-setup.md` — that file has the exact settings, hotkeys, and folder template mappings
4. **Open `_HOME.md`** to verify dashboard queries render. The sample source note should appear in "Recent ingestion" and the sample opportunity in "Decisions waiting"
5. **Read** `_meta/conventions.md` and `05_shared-intelligence/workflows/workflow-knowledge-promotion.md` end-to-end — these are the rules of the system

### Step 5 — Optionally initialize a project vault

If the user has an existing repo they want to bring into the system:

```bash
bash <skill-path>/scripts/init-project-vault.sh \
  <repo-path> \
  <personal|clients> \
  <workspace>/second-brain \
  <skill-path>/assets
```

This:
- Creates `.kos/` inside the repo with `specs/`, `scopes/`, `execution-logs/`, `lessons/`
- Drops `README.md` and `.vault-config.md` from templates
- Symlinks `.kos/` into `04_projects/personal/` or `04_projects/clients/_active/`

### Step 6 — Phase 1 exit conditions

Before declaring Phase 1 complete, verify with the user:

- [ ] Vault structure exists and Obsidian opens it cleanly
- [ ] All four plugins installed and configured
- [ ] `_HOME.md` renders all dashboard queries without errors
- [ ] Sample source visible in "Recent ingestion"
- [ ] Sample opportunity visible in "Decisions waiting"
- [ ] At least one project has `.kos/` + symlink (if any existing projects)
- [ ] Conventions doc read
- [ ] Promotion workflow read

When all eight are checked, Phase 1 is complete. Phase 2 (the VIS extraction layer) is a separate skill, not built yet.

## What this skill does NOT do

- It does not configure Obsidian plugins automatically. Obsidian's plugin settings live in `.obsidian/` and are configured through the Obsidian UI. The skill provides exact instructions in `_meta/obsidian-setup.md` and walks the user through them.
- It does not migrate existing user notes into the new structure. If the user has loose notes, ask before moving anything.
- It does not pull video transcripts or run extractions. That's the Phase 2 VIS skill.
- It does not delete anything. If folders exist, they're left alone.

## Bundled assets

```
assets/
├── templates/
│   ├── kos/        ← pattern, lesson, blueprint, tool, workflow, system templates
│   ├── vis/        ← source-video, tactic, opportunity, content-idea, weekly-synthesis templates
│   └── project/    ← project-readme, vault-config templates
└── seed-notes/     ← _HOME, MOCs, conventions, obsidian-setup, workflows, three sample notes

scripts/
├── setup-knowledge-os.sh    ← main installer (idempotent)
└── init-project-vault.sh    ← per-project initializer

references/
└── architecture-rationale.md  ← why one-vault-multi-folder beats multi-vault
```

## When things go wrong

**"Dataview queries on `_HOME.md` show nothing"** — Verify Dataview is installed AND enabled AND that JavaScript queries are turned on (Settings → Dataview → Enable JavaScript Queries). Also check that the sample notes have valid frontmatter (no tabs, proper YAML).

**"Templater isn't running on new notes"** — Check Settings → Templater → Folder Templates. The mappings in `_meta/obsidian-setup.md` need to be entered manually; the skill cannot configure Obsidian plugins.

**"Symlinks aren't resolving in Obsidian"** — Obsidian on macOS handles symlinks fine, but on Windows you may need to use junctions instead. The init-project-vault script uses `ln -s` which is POSIX. For Windows, the equivalent is `mklink /J`.

**"I want a different folder structure"** — The structure is intentional and maps directly to the user's KOS architecture doc. Push back on changes unless the user has a strong reason. If they do, modify the seed notes and templates rather than the folder layout.

## Reference

For the architectural rationale (why one Obsidian vault instead of multiple), read `references/architecture-rationale.md`.
