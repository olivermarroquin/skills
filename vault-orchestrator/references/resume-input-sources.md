# RESUME — input sources + read order

Mode 5 reads project state from six sources, in a deliberate order, and reconciles contradictions between them. This reference names each source, what Mode 5 extracts from it, and how to handle missing or stale inputs.

## What Mode 5 needs to know before it can read

To resolve any of the per-project inputs below, Mode 5 needs:

- **The project slug.** Operator-provided when triggering RESUME ("resume s-and-h-contracting" / "where are we on ev-electric"). If ambiguous (multiple matches in `04_projects/`), Mode 5 asks one clarifying question.
- **The project's vault path.** Resolved by walking `04_projects/clients/_active/`, `04_projects/clients/_private/`, and `04_projects/personal/` for the matching slug. If the slug exists in multiple areas (e.g., a personal-and-client overlap), Mode 5 surfaces the ambiguity rather than guessing.

If the project slug doesn't resolve, Mode 5 stops with an honest finding ("no project named X in the vault — did you mean Y?") rather than producing an empty report.

## Read order

Mode 5 reads inputs in this order. The order is deliberate — the most authoritative + freshest signal comes first, so later reads can be reconciled against it:

1. **Master tracker** — `~/workspace/second-brain/_meta/handoffs/_active-chats-tracker.md`
2. **Event log delta** — `~/workspace/second-brain/_meta/_event-log.md`, filtered to events since the state file's `updated_at` (or last 24 hours if no state file)
3. **State file** — `04_projects/.../{slug}/_state/onboarding.json` (or equivalent for non-onboarding projects)
4. **Execution logs, newest-first** — `04_projects/.../{slug}/execution-logs/execution-log-*.md`
5. **Per-project chat tracker + digest** — `04_projects/.../{slug}/_chat-tracker.md` and `_chat-status.md`
6. **Handoffs naming this project** — `~/workspace/second-brain/_meta/handoffs/handoff-*.md` whose frontmatter `client:` field matches the project slug, OR whose body names the project in its `purpose:` or `tags:`

Why this order: the master tracker is the inter-chat coordination layer's source of truth (any parallel chat updates it at Opening / Closing); the event log captures everything since the state file last wrote; the state file is canonical "where the project thinks it is" but can lag if a sibling chat shipped without updating it. Execution logs add the recent-action context that may not yet be summarized in `wave_log`. Per-project trackers can be 1-2 days stale by design (they're project-scoped mirrors, not the authoritative source). Handoffs are the spawn-graph inputs — Mode 5 reads them last because their relevance depends on what state files + trackers already covered.

## Per-source extraction rules

### 1. Master tracker

Extract rows naming the project in question across:

- "Active / in-flight chats" — any row whose Notes column references the project slug, or whose handoff filename contains the slug
- "Ready to spawn next" — same matching rule
- "Queued — Tier 2" and "Queued — Tier 3" — same matching rule
- "Recently closed chats" within past 14 days — same matching rule (used for "what shipped recently for this project" framing)
- "Recently completed (past 7 days)" — same matching rule

The aggregator's generated rollup section between `<!-- AGGREGATOR:BEGIN -->` and `<!-- AGGREGATOR:END -->` MAY contain a per-project digest block for this project. If present, capture it as a parallel summary — Mode 5 will reconcile it against the state file in Step 7.

If the master tracker is malformed or the project has zero matches in any section, surface as "tracker has no rows for `<slug>` — either the project was never registered or the slug doesn't match any handoff naming convention" and continue with the other sources.

### 2. Event log delta

Read the event log and filter rows to:

- Timestamp >= the state file's `updated_at` value (if state file exists), OR
- Timestamp >= 24 hours ago (if no state file)

For each row in the delta, capture:

- Surface (which file/area changed)
- Pass number (correlates with tracker passes)
- Chat ID (which sibling chat made the edit)
- One-line summary

Mode 5 uses the delta for two things downstream: (a) reconciling stale `blocked_on` entries (Section "Stale-state reconciliation rules" below), and (b) the "Cross-project unblockers" output section.

If the event log has zero rows in the delta window, that's normal for projects with no inter-chat activity since last touch — surface as a note ("no events since state file last wrote") rather than a finding.

### 3. State file

For projects with a `client-seo-onboarding`-shaped state file (the canonical shape today, defined in `~/workspace/skills/client-seo-onboarding/state-schema.md` v1.1):

Extract the full JSON object. Key fields Mode 5 cares about:

- `schema_version` — surface as a finding if older than the current skill's version (see "Schema-version handling" below)
- `current_wave` — the wave the project is currently working in (or `null` if no wave in flight)
- `waves[]` — the planned + completed wave list with statuses
- `wave_log[]` — append-only per-wave summaries (closing notes from each closed wave)
- `planned_remaining_waves[]` — forward-planning shape (Mode 5's source for "what's queued")
- `blocked_on[]` — free-text blockers (Mode 5 reconciles these against the event log)
- `failures[]` — catastrophic errors that need operator decisions (surface every entry with `operator_action: pending`)
- `quality_log` — per-artifact verdicts (Mode 5 doesn't need to surface every entry, but flags any `light-escalate` decisions that may still be pending)

For projects with a different state file shape (e.g., non-onboarding work), Mode 5 reads what's present and surfaces the schema-mismatch as a finding rather than aborting. The minimum it needs to be useful: some notion of "current state" + some notion of "what's planned next."

If no state file exists at the expected path, Mode 5 surfaces this clearly ("no state file at `_state/onboarding.json` — this project may not be using a stateful skill, or state may live elsewhere") and continues with the master tracker + execution log signals only.

### 4. Execution logs, newest-first

List `04_projects/.../{slug}/execution-logs/execution-log-*.md` sorted by filename descending (newest-first per the `execution-log-YYYY-MM-DD-<topic>.md` naming convention).

For the newest 1-3 logs, extract:

- Frontmatter `chat:` (the chat ID that produced the log)
- Frontmatter `skill:` and `skill-version:` (so Mode 5 can correlate against the current skill version)
- Section headers (timestamp-prefixed activity markers)
- Any "Decisions made" or "Lessons learned" subsections

The newest execution log is the most-recent narrative of what happened. State file `wave_log` summaries are the structured version; execution logs are the prose version with context that didn't make it into the summary. Mode 5 reads both because each captures different things.

If a project has no execution logs, surface as a finding ("no execution logs found at `execution-logs/` — either the project hasn't run yet or logs live elsewhere") and continue.

### 5. Per-project chat tracker + digest

Both files coexist by design (per `multi-chat-coordination/references/project-chat-tracker-shape.md`):

- `_chat-tracker.md` — human-readable mirror of master tracker rows scoped to this project. Read for project-scoped context the master tracker doesn't include (project-local "Open decisions" lists, project-local "Recently closed" detail).
- `_chat-status.md` — machine-readable digest with frontmatter that the aggregator parses. Read the frontmatter directly: `current-focus`, `in-flight-count`, `ready-to-spawn-count`, `queued-count`, `blockers[]`, `spawn-recommendations[]`, `last-closed`, `last-closed-summary`, `metrics`.

If the digest is >14 days stale (per `multi-chat-coordination`'s drift-detect heuristics), Mode 5 surfaces this and treats the digest as advisory rather than authoritative.

If neither file exists, surface as a finding ("project has no per-project chat tracker — Phase 1 of the vault-orchestrator project shipped this convention; this project predates it or skipped it") and continue with the other sources.

### 6. Handoffs naming this project

Grep `_meta/handoffs/handoff-*.md` for frontmatter `client:` field matching the project slug, OR body text mentioning the slug or project name. For each matching handoff, capture:

- Frontmatter `status:` (queued / active / consumed / superseded / phase-1-*-consumed for multi-phase handoffs)
- Frontmatter `depends-on:` array (Mode 5 walks this to determine readiness)
- Frontmatter `purpose:` (one-line summary)
- The handoff filename (used in the output)

For nested handoffs (e.g., `_meta/handoffs/<project>/<phase>.md`), include them in the grep — those are the project-anchored phase handoffs that decompose a multi-phase initiative.

If the project has zero matching handoffs, that's normal for projects that registered all their work directly in the master tracker without separate handoff files. Surface as advisory ("no separate handoff files found for this project — work is registered directly in tracker rows") and continue.

## Stale-state reconciliation rules

Mode 5's distinctive responsibility: reconciling contradictions between sources. The S&H wave A1 closure on 2026-06-02 is the canonical example — the state file `blocked_on` array shows both blockers un-cleared, but the event log shows both blocker handoffs were consumed 2026-06-02 by sibling chats. State file is stale; event log is fresh.

Mode 5 detects these reconciliations and surfaces them in the output (see [[resume-output-shape]] § "Stale-state reconciliations"). Detection rules:

1. **Blocker apparently un-cleared but handoff consumed.** If `state_file.blocked_on[i]` text contains a handoff filename, and the event log shows that handoff was consumed (status flip to `consumed` or `phase-1-*-consumed`), flag as: "state-file says blocker still active; event log says blocker handoff consumed YYYY-MM-DD by chat X."

2. **Wave in-progress but tracker shows the chat closed.** If `state_file.current_wave` is set and `waves[<current_wave>].status: in-progress`, but the master tracker shows that wave's chat ID in "Recently closed" within the same date the state file last wrote, flag as: "state-file says wave in-progress; tracker says chat closed — state file may not have written the wave-close."

3. **Schema-version drift.** If `state_file.schema_version` is older than the skill version Mode 5 is running against (e.g., state file is `"1.0"` while client-seo-onboarding is `v1.1`), flag as: "state file is schema v1.0; client-seo-onboarding shipped v1.1 on 2026-06-02 adding waves + wave_log + planned_remaining_waves + blocked_on + quality_log fields. The migration is additive and operator-driven; Mode 5 reads what's present."

4. **Execution log newer than state file.** If the newest execution log has a section timestamp later than `state_file.updated_at`, flag as: "execution log mentions activity after the state file last wrote — the wave may have progressed without the state file being updated."

5. **Per-project tracker newer than state file (or vice-versa).** If `_chat-tracker.md` `updated:` frontmatter is newer than `state_file.updated_at` (or vice-versa) by more than 24 hours, flag as: "project surfaces are out of sync — see <which is newer> for the latest activity."

For each reconciliation, Mode 5 names what it inferred + asks the operator to confirm before downstream work treats the reconciled state as truth. The operator may say "yes that's right, run with it" OR "no, the state file is correct" — Mode 5 honors the operator's choice. Mode 5 never silently mutates state files.

## Schema-version handling

If a state file's `schema_version` is older than the current skill version, Mode 5:

- Reads what's present in the file (additive migrations preserve old fields).
- Surfaces the version mismatch as a finding in the output.
- Does NOT auto-migrate the file. Migration is operator-driven OR happens at the next normal write by the owning skill (e.g., the next `client-seo-onboarding` run).
- Notes which v1.1 features are unavailable for projects on v1.0 state (e.g., `wave_log`, `planned_remaining_waves` won't have entries until the file migrates).

This matches `client-seo-onboarding`'s own resume contract — don't quietly mutate operator-edited state.

## Handling missing sources

Mode 5 is honest-gap-surfacing per the standing principle. If any of the six sources is missing, it surfaces the gap rather than skipping it silently. The operator should always be able to see what Mode 5 did and didn't read.

| Source missing | Mode 5 behavior |
|---|---|
| Master tracker zero matches | Surface: "tracker has no rows for `<slug>`" + continue |
| Event log delta empty | Surface (advisory): "no events since state file last wrote" + continue |
| State file absent | Surface: "no state file at `_state/onboarding.json`" + continue with other sources |
| Execution logs absent | Surface: "no execution logs at `execution-logs/`" + continue |
| Per-project tracker absent | Surface (advisory): "project has no per-project tracker yet — Phase 1 convention" + continue |
| Handoff matches zero | Surface (advisory): "no separate handoff files for this project" + continue |

If ALL sources are missing, Mode 5 surfaces this as a hard finding ("project `<slug>` resolves to a folder but has no readable state across all six sources — either it's not yet started, or it lives outside the standard layout") and stops.

## What Mode 5 does NOT read

To keep RESUME scoped and cheap:

- The full body of every handoff file (Mode 5 reads frontmatter + the first paragraph; deeper reads happen during PROVISION when drafting the next wave)
- Domain knowledge under `03_domains/` (that's SURVEY's surface, not RESUME's)
- Other projects' state files (cross-project unblockers comes from the master tracker + event log + handoff frontmatter, not from peeking into sibling state files)
- Memory files (`~/.../memory/MEMORY.md`) — those inform Mode 5's behavior already; not project-specific input
- Git history or repo state — outside the vault contract; future tooling may add this

## Related

- [[SKILL]] § "Mode 5 — RESUME"
- [[resume-output-shape]] — what Mode 5 produces from these inputs
- [[resume-decomposition-diagram-text]] — how Mode 5 renders the wave dependency graph
- [[../../client-seo-onboarding/state-schema|client-seo-onboarding state schema v1.1]] — the canonical state file shape Mode 5 reads
- [[../../multi-chat-coordination/references/project-chat-tracker-shape|project-chat-tracker shape]] — the per-project tracker shape
- [[../../multi-chat-coordination/references/project-status-digest-shape|project-status-digest shape]] — the `_chat-status.md` digest shape
- [[../../../second-brain/_meta/_event-log|event log]] — Mode 5's stale-state reconciliation primary signal
- [[../../../second-brain/_meta/handoffs/_active-chats-tracker|master tracker]] — Mode 5's first read
