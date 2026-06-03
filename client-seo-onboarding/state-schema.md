---
type: schema
status: v1.1
created: 2026-06-01
updated: 2026-06-03
tags: [skill, client-seo-onboarding, state-schema, resume-contract, multi-chat-decomposition, schema-auto-bump]
---

# State Schema — `onboarding.json` (v1.1)

Companion to [[SKILL]]. Defines the shape of the state file the orchestrator reads and writes to support mid-run resume + multi-chat wave decomposition.

**Location:** `~/workspace/second-brain/04_projects/clients/_active/<client-slug>/_state/onboarding.json`

One file per client. The `_state/` folder may also hold sibling artifacts (e.g., `imagery-prompt-summary.md`, `_escalation-queue.md`).

## What's new in v1.1 (additive over v1.0)

- **`current_wave`** — string. Wave the skill is currently working in.
- **`waves`** — array. Planned + completed waves.
- **`wave_log`** — array. Per-wave summaries at close (append-only).
- **`planned_remaining_waves`** — array. Forward-planning shape.
- **`blocked_on`** — free-text array. One line per blocker.
- **`quality_log`** — object keyed by step + artifact. Per-artifact verdicts from output-quality-loop Modes 1-5.
- **`schema_version`** — bumped from `"1.0"` to `"1.1"`.

v1.0 state files load cleanly under v1.1 *for reads* — all v1.1 additions are new top-level fields or new optional sub-fields. **But a write that introduces any v1.1 field into a v1.0-stamped file must bump `schema_version` first** (see "Schema field registry" and Write convention 9 below). Reading a v1.0 file under v1.1 is fine; *writing v1.1 fields without bumping* is the silent-drift bug. See "Migration notes" at the bottom.

## Schema field registry (`SCHEMA_FIELDS`)

This is the canonical, version-keyed set of top-level fields for each `schema_version`. The orchestrator consults it before every state write to decide whether a write is additive (introduces fields outside the current version's set) and therefore requires an auto-bump. **This registry is the single source of truth for "which fields belong to which version."** When a future version adds fields, add a new keyed set here and bump the skill version in the same edit.

```
SCHEMA_FIELDS = {
  "1.0": {
    "schema_version", "client_slug", "started_at", "updated_at",
    "current_step", "step_status",
    "ingest", "confirmed_services", "confirmed_cities",
    "research_status", "data_files", "wp_auth", "page_status",
    "internal_linking", "report", "failures",
  },
  "1.1": {  # v1.0 set + six additive fields
    "schema_version", "client_slug", "started_at", "updated_at",
    "current_step", "step_status",
    "ingest", "confirmed_services", "confirmed_cities",
    "research_status", "data_files", "wp_auth", "page_status",
    "internal_linking", "report", "failures",
    "current_wave", "waves", "wave_log", "planned_remaining_waves",
    "blocked_on", "quality_log",
  },
}
```

**`_schema_version_history` is version-agnostic.** It is the audit array the auto-bump rule writes into; it is allowed in any version and writing it NEVER counts as additive drift (otherwise the bump would recurse). Treat it as implicitly present in every `SCHEMA_FIELDS[<version>]` — do not list it, do not let it trigger a bump.

**Schema version ≠ skill version.** The highest-defined `schema_version` is `1.1`; the skill is at v1.2 (the v1.2 bump added this auto-bump *rule*, not a new schema *field*). Auto-bump targets the `schema_version` — it bumps a file TO the highest schema version whose `SCHEMA_FIELDS` set contains the field being written (currently `1.1`). Never stamp `schema_version: "1.2"` — there is no `SCHEMA_FIELDS["1.2"]`. A write is "additive" when it introduces a field in `SCHEMA_FIELDS[<highest schema version>]` that is NOT in `SCHEMA_FIELDS[<file's current schema_version>]`.

## Full schema

```json
{
  "schema_version": "1.1",
  "client_slug": "s-and-h-contracting",
  "started_at": "2026-06-01T14:00:00Z",
  "updated_at": "2026-06-02T18:30:00Z",

  "current_step": "step-2-research",
  "current_wave": "wave-A2-research-service-briefs-2-and-3",
  "step_status": {
    "step-1-ingest": "done",
    "step-2-research": "in-progress",
    "step-3-author-data": "pending",
    "step-4-verify-wp": "pending",
    "step-5-bulk-scaffold": "pending",
    "step-6-imagery-prompts": "pending",
    "step-7-pause-higgsfield": "pending",
    "step-8-resume-per-page": "pending",
    "step-9-indexing": "pending",
    "step-10-internal-linking": "pending",
    "step-11-report": "pending"
  },

  "waves": [
    {
      "wave_id": "wave-A1-research-service-brief-1-spotcheck",
      "status": "closed",
      "started_at": "2026-06-01T14:00:00Z",
      "closed_at": "2026-06-01T18:00:00Z",
      "chat_id": "s-and-h-orchestrator-first-run-202606011400",
      "scope": "Produce emergency-electrician Tier-1 service brief + spot-check + ready-to-close",
      "outputs": [
        "05_shared-intelligence/research-briefs/services/emergency-electrician.md",
        "05_shared-intelligence/research-briefs/services/_quality-log.md (folder log opened)"
      ]
    },
    {
      "wave_id": "wave-A2-research-service-briefs-2-and-3",
      "status": "in-progress",
      "started_at": null,
      "closed_at": null,
      "chat_id": null,
      "scope": "Produce ev-charger + light-fixture-installation Tier-1 service briefs via v1.1 orchestrator (per-step quality loop + Mode 4 AI-surface backfill on §4 across all 4 surfaces)",
      "outputs": []
    }
  ],

  "wave_log": [
    {
      "wave_id": "wave-A1-research-service-brief-1-spotcheck",
      "summary": "1 Tier-1 brief shipped (emergency-electrician); Sonar Mode 4 backfilled §4 + §5; verdict NEEDS REVISION minor at confidence 78 (single FAIL is §4c gated on API-keys handoff — cleared 2026-06-02)",
      "key_artifacts": [
        "emergency-electrician.md (folder-log Latest: NEEDS REVISION minor, confidence 78, iteration 1 of 3)",
        "services/_quality-log.md (folder log opened)"
      ],
      "spawned_handoffs": [
        "handoff-2026-06-01-client-seo-onboarding-v1.1-skill-rewrite",
        "handoff-2026-06-01-openai-gemini-claude-api-keys-tier3-wiring",
        "handoff-2026-06-01-s-and-h-wave-a2-service-briefs",
        "handoff-2026-06-01-vault-orchestrator-mid-project-resume-capability",
        "handoff-2026-06-01-inter-chat-communication-layer-event-log"
      ],
      "verdict_summary": "wave-A1 closed with spawned blockers (5 follow-up handoffs); not a clean pass but architecturally load-bearing"
    }
  ],

  "planned_remaining_waves": [
    {"wave_id": "wave-A2-research-service-briefs-2-and-3", "scope": "ev-charger + light-fixture service briefs", "estimated_hours": 2.5, "blocks_on": []},
    {"wave_id": "wave-A3-research-city-briefs-batch-1", "scope": "Woodbridge + Lake Ridge + Dale City + Manassas Tier-2 city briefs", "estimated_hours": 3.0, "blocks_on": ["wave-A2"]},
    {"wave_id": "wave-A4-research-city-briefs-batch-2", "scope": "Lorton + Springfield + Burke + Alexandria + Stafford Tier-2 city briefs", "estimated_hours": 3.5, "blocks_on": ["wave-A2"]},
    {"wave_id": "wave-A5-research-intersections-batch-1", "scope": "15 intersection briefs (positions 1-15)", "estimated_hours": 4.0, "blocks_on": ["wave-A3", "wave-A4"]},
    {"wave_id": "wave-A6-research-intersections-batch-2", "scope": "15 intersection briefs (positions 16-30)", "estimated_hours": 4.0, "blocks_on": ["wave-A5"]}
  ],

  "blocked_on": [
    "v1.1 SKILL rewrite (handoff-2026-06-01-client-seo-onboarding-v1.1-skill-rewrite) — CLEARED 2026-06-02 by chat client-seo-onboarding-v1.1-rewrite-202606021400",
    "OpenAI + Gemini + Claude API keys (handoff-2026-06-01-openai-gemini-claude-api-keys-tier3-wiring) — CLEARED 2026-06-02"
  ],

  "ingest": {
    "meeting_notes_path": "/Users/.../meeting-notes-2026-06-01.md",
    "intake_form_path": "/Users/.../intake-form-2026-06-01.md",
    "extracted_business_name": "S&H Contracting Unlimited",
    "extracted_owner_name": "Mohammad ...",
    "extracted_existing_url": "https://...",
    "build_order_path": "04_projects/clients/_active/s-and-h-contracting/website-archive/new/core-30/_build-order.md",
    "build_order_authoritative": true,
    "ambiguities_surfaced": [
      "intake mentioned generator installation but notes did not"
    ]
  },

  "confirmed_services": ["panel-upgrade", "troubleshooting", "ev-charger", "emergency-electrician", "light-fixture-installation"],
  "confirmed_cities": ["woodbridge-va", "lake-ridge-va", "dale-city-va", "manassas-va", "lorton-va", "springfield-va", "burke-va", "alexandria-va", "stafford-va"],

  "research_status": {
    "service_briefs": {
      "panel-upgrade": "reused",
      "troubleshooting": "reused",
      "emergency-electrician": "produced"
    },
    "city_briefs": {},
    "intersection_briefs": {},
    "client_brief": "produced"
  },

  "data_files": {
    "client_json": "data/client-s-and-h-contracting.json",
    "service_jsons": [],
    "city_jsons": [],
    "config_file": "s-and-h-contracting.config.json",
    "tier3_credentials_status": "pending-operator-population"
  },

  "wp_auth": {
    "verified": false,
    "user_role": null,
    "verified_at": null
  },

  "page_status": {},

  "quality_log": {
    "step-1-ingest": {
      "artifact": "state.ingest",
      "iterations": [
        {"iteration": 1, "timestamp": "2026-06-01T14:30:00Z", "verdict": "PASS", "confidence": 88, "spec_sources": ["meeting-notes-extraction-completeness"], "mode_4_run": false, "decision": "auto-ship"}
      ],
      "latest_verdict": "PASS",
      "latest_confidence": 88,
      "iteration_count": 1
    },
    "step-2-research": {
      "emergency-electrician": {
        "artifact": "05_shared-intelligence/research-briefs/services/emergency-electrician.md",
        "folder_log": "05_shared-intelligence/research-briefs/services/_quality-log.md",
        "iterations": [
          {"iteration": 1, "timestamp": "2026-06-01T17:30:00Z", "verdict": "NEEDS REVISION (minor)", "confidence": 78, "spec_sources": ["_template-service-brief.md", "plain-language-conventions.md"], "mode_4_run": true, "mode_4_queries": 3, "mode_4_cost_usd": 0.06, "decision": "light-escalate"}
        ],
        "latest_verdict": "NEEDS REVISION (minor)",
        "latest_confidence": 78,
        "iteration_count": 1
      }
    }
  },

  "internal_linking": {
    "synthesis_path": "05_shared-intelligence/research-briefs/link-maps/_synthesis-s-and-h-contracting.md",
    "synthesis_status": "missing",
    "proposed_total": 0,
    "applied_total": 0,
    "dead_links_remaining": 0
  },

  "report": {
    "path": null,
    "completed_at": null
  },

  "failures": []
}
```

## Field semantics

### Top-level identity

- **`schema_version`** — `"1.1"` as of 2026-06-02. Increment when the schema changes — **including additive changes**: the first write that introduces a field outside the file's current version's `SCHEMA_FIELDS` set auto-bumps `schema_version` and appends a `_schema_version_history` entry (see "Schema field registry" + Write convention 9). Breaking (non-additive) changes — field removal or type change — are refused, not bumped. *(Note: this reverses the earlier "additive changes don't require a bump" guidance, which let S&H's file drift at v1.0 while carrying v1.1 fields; the auto-bump rule shipped 2026-06-03 Phase 5B closes that hole.)*
- **`client_slug`** — kebab-case slug; matches the `04_projects/clients/_active/<slug>/` folder name and the `data/client-<slug>.json` filename.
- **`started_at` / `updated_at`** — ISO 8601 UTC timestamps. `updated_at` rewrites on every state write.

### Step tracking

- **`current_step`** — string. The step the skill was last working on. On resume, the skill reads this first.
- **`step_status`** — one of `pending` / `in-progress` / `done` / `skipped` per step. The skill walks these in order; a step can only transition `pending → in-progress → done` (or `pending → skipped` if explicitly skipped).

### Wave tracking (new in v1.1)

- **`current_wave`** — string. The wave the skill is currently working in. Set at wave-start, cleared at wave-close. On resume, the orchestrator reads this first to know which wave's context to load. `null` if no wave is in flight.

- **`waves`** — array. Each element describes one planned or completed wave:
  - `wave_id` — kebab-case slug; canonical wave identifier
  - `status` — one of `pending` / `in-progress` / `closed` / `closed-with-spawned-blockers` / `superseded`
  - `started_at` / `closed_at` — ISO 8601 UTC timestamps (null until set)
  - `chat_id` — the chat that ran the wave (matches event-log chat-id convention `<project-slug>-<topic>-<YYYYMMDDHHMM>`); null until wave starts
  - `scope` — one-paragraph human-readable description of what the wave covers
  - `outputs` — array of file paths the wave produced (populated at wave-close)

- **`wave_log`** — array. Append-only per-wave summary written at wave-close. Each entry:
  - `wave_id` — matches the `waves[]` entry
  - `summary` — one-paragraph plain-language summary of what the wave shipped
  - `key_artifacts` — array of canonical artifact paths + their quality-loop verdicts at wave-close
  - `spawned_handoffs` — array of handoff filenames created during the wave (without `.md` extension)
  - `verdict_summary` — one-line scoring against the wave's intended scope (clean-pass / partial / closed-with-spawned-blockers / superseded)

  This is the canonical "what did wave N produce that wave N+1 can rely on" record. Wave-(N+1) chats read this first at Opening Protocol.

- **`planned_remaining_waves`** — array. Forward-planning shape. Each entry:
  - `wave_id` — proposed kebab-case slug
  - `scope` — one-paragraph description
  - `estimated_hours` — number; computed from `per-artifact-sizing.md` lookup at the wave-decomposition gate
  - `blocks_on` — array of `wave_id`s this wave depends on (empty array if none)

  Operator-editable between waves: operator can collapse, split, or reorder waves; the orchestrator respects the edited array on next invocation.

- **`blocked_on`** — array of free-text strings. One line per blocker. Mirrors the S&H state file shape that shipped 2026-06-01 and worked well in practice. Typical entries name a handoff filename + a current-status note:
  - `"v1.1 SKILL rewrite (handoff-2026-06-01-client-seo-onboarding-v1.1-skill-rewrite) — CLEARED 2026-06-02 by chat <chat-id>"`

  When a blocker clears, the line is updated in place (not deleted) with `— CLEARED YYYY-MM-DD by <chat-id>` appended. This preserves the dependency audit trail.

### Per-step substate

Each step's per-step state lives in its own top-level key:

- **`ingest`** — what was extracted from the meeting notes and intake form. v1.1 adds `build_order_path` + `build_order_authoritative` fields.
- **`confirmed_services` / `confirmed_cities`** — operator-confirmed lists (the contract for what gets researched + scaffolded).
- **`research_status`** — per-brief status: `reused` (already existed) / `produced` (newly researched) / `deferred` (operator skipped) / `failed` (sub-skill errored).
- **`data_files`** — paths to scaffolded JSON files + `tier3_credentials_status` flag.
- **`wp_auth`** — verification result.
- **`page_status`** — per-page bitmap of what's been done; most granular slice (resume into mid-Step-8 reads this to know which page to pick up from).
- **`internal_linking`** — counters + synthesis-file pointer.
- **`report`** — pointer to final report.

### Quality log (new in v1.1)

- **`quality_log`** — object keyed by step (e.g., `step-1-ingest`, `step-2-research`). For artifact-producing steps with a single artifact (Steps 1, 11), the value is a flat object. For steps producing multiple artifacts (Steps 2, 3, 5, 6, 8, 10), the value is nested keyed by artifact slug.

  Each leaf record:
  - `artifact` — path or symbolic reference (e.g., `state.ingest` for Step 1's in-state artifact)
  - `folder_log` — path to the relevant `_quality-log.md` folder log (when present)
  - `iterations` — array of per-iteration records (verdict, confidence, spec_sources, mode_4 metadata, decision)
  - `latest_verdict` / `latest_confidence` / `iteration_count` — denormalized rollups for fast resume reads

  On resume, the orchestrator reads this object to know (a) which artifacts already passed and can be skipped, (b) which are mid-iteration (and need to resume from iteration N+1), and (c) which were light-escalated (need operator decision before continuing).

### Failures array

- **`failures`** — append-only log. Each entry: `step` + identifying context (`page_slug`, `service_slug`, etc.) + `error` text + `timestamp` + `operator_action` field that the skill updates when the operator decides what to do (`deferred` / `retried` / `accepted` / `pending`).

## `failures` vs `quality_log` — semantic distinction

The schema has two parallel state structures that look similar but serve different purposes. Don't conflate them.

- **`failures`** — catastrophic errors that STOP the orchestrator. Sub-script exited non-zero, missing required file, malformed brief that scaffolder couldn't parse, WP auth fail, network outage during publish. Each entry has step + identifying context + error text + timestamp + operator_action. Append-only; the orchestrator WAITS on operator decision before moving on. The failure entries represent "the orchestrator can't proceed without you."

- **`quality_log`** — per-artifact quality verdicts from output-quality-loop's Modes 1-5. Includes PASS (auto-ship), NEEDS REVISION (regenerate via revision prompt), FAIL (escalate). The orchestrator CONTINUES across artifacts even when one light-escalates (escalations queue for operator review without blocking the rest of the step's artifacts). The quality_log entries represent "here's what happened to each artifact" — they're a quality audit, not a failure audit.

### The bridging rule

A quality-loop **FAIL at 3-iteration stall** ALSO writes a `failures` entry. The loop stalled is an exceptional condition the orchestrator records to its own failures audit trail. The state has both a `quality_log` entry (the verdict history) AND a `failures` entry (the orchestrator-can't-proceed signal).

A quality-loop **NEEDS REVISION at iteration 1 or 2** does NOT write to `failures`. It's a normal revision cycle. The state has only a `quality_log` entry (the iteration history); the orchestrator regenerates the artifact via Mode 2's revision prompt and continues.

A quality-loop **FAIL at iteration 1 or 2** does NOT write to `failures` either — Mode 2 still has iterations left. The state has only a `quality_log` entry; regeneration proceeds.

A **light escalation** (PASS below threshold, or NEEDS REVISION at iteration < 3) does NOT write to `failures`. It writes a `_escalation-queue.md` row in the folder for operator review; the orchestrator continues with the next artifact.

A **hard escalation that isn't a 3-iter stall** (e.g., operator-forced `--escalate "<reason>"`) also doesn't write to `failures` — the orchestrator escalates per Mode 5's hard-escalation path without flagging itself as blocked.

This rule keeps the two arrays semantically clean: `failures` = "I can't proceed"; `quality_log` = "here's what happened to each artifact."

## Write conventions

1. **Atomic writes.** Write to `onboarding.json.tmp`, then `mv` to `onboarding.json`. Never half-write.
2. **Per-page granularity in Step 8.** Each page's per-slot completion flips its own bit in `page_status[<page-slug>]` immediately. Don't batch.
3. **Per-artifact granularity in `quality_log`.** Each artifact's Mode 1-5 cycle writes its own entry immediately.
4. **Always update `updated_at` on every write.**
5. **Never delete the `failures` array** without explicit operator confirmation; it's the audit trail.
6. **Update `blocked_on` in place** (append the `— CLEARED ...` suffix); never delete a blocker entry — preserves dependency archaeology.
7. **Append to `wave_log` at wave-close** (don't overwrite); each wave-close adds one entry.
8. **At wave-close**, write `waves[<wave_id>].status: closed` + `closed_at` + `outputs`; append `wave_log` entry; clear `current_wave`; update `planned_remaining_waves` (remove the just-closed wave).
9. **Schema-version auto-bump on additive write.** Before committing ANY write, compare the field set being written against `SCHEMA_FIELDS[<file's current schema_version>]` (see "Schema field registry" above). Run this check on every write — wave-state writes, `quality_log` writes, `blocked_on` updates, all of them.
   - **Additive write (default — auto-bump + audit + write).** If the write introduces one or more fields present in `SCHEMA_FIELDS[<highest schema version>]` but absent from `SCHEMA_FIELDS[<file's version>]`, then in the SAME atomic write: (a) set `schema_version` to the highest schema version whose `SCHEMA_FIELDS` set contains the new field(s) — currently `1.1`, never the skill version — and (b) append one entry to `_schema_version_history` (create the array if missing). The entry is append-only — never overwrite or reorder existing entries. Entry shape:
     ```json
     {
       "version": "1.1",
       "bumped_at": "<ISO-8601 UTC>",
       "bumped_by": "<chat-id, per event-log convention>",
       "reason": "Additive fields written: [\"<sorted field names>\"]"
     }
     ```
   - **Non-additive change (REFUSE, always).** If the write would REMOVE a field that exists in `SCHEMA_FIELDS[<file's version>]`, or change a field's type/shape from what the schema documents, do NOT write. Surface to the operator with the offending field(s) and stop — this holds regardless of any "allow additive" intent, because the auto-bump path only ever covers *adding* fields, never removing or reshaping them.
   - **No-drift write (no bump).** If every field being written is already in `SCHEMA_FIELDS[<file's version>]` (plus the version-agnostic `_schema_version_history`), write normally — no bump, no audit entry.
   - **Unknown field (REFUSE, always).** If the write introduces a field that is in NO version's `SCHEMA_FIELDS` set (neither additive, nor removal, nor no-drift), refuse + surface — it's a typo, or an unregistered field that must be added to the registry and skill-bumped first. Never auto-write a field the registry doesn't know.
   - **Why this exists.** S&H's `onboarding.json` sat at `schema_version: "1.0"` while wave writers added v1.1 fields for 24+ hours before sweep [4] caught it (2026-06-03). This rule makes that drift impossible to write silently: the first v1.1-field write self-bumps and self-audits. **Enforcement is convention-class — the orchestrator (an LLM) must run the check; there is no deterministic guard.** A hard, un-skippable guard would require routing state writes through a script (parked as Phase 5B Path B, conditional on state writes becoming script-mediated).

## Read conventions

1. **Read at every fresh invocation.** Before the plan-bullet opening, the skill checks for an existing state file.
2. **Read at every operator message in mid-run.** The operator may have edited state by hand (especially `planned_remaining_waves`, `blocked_on`, or a `quality_log` decision).
3. **Detect schema-version mismatch.** If `schema_version` is older than the current skill version, surface the migration prompt (see "Migration notes" below).

## Resume contract

On invocation with a client slug whose state file exists:

1. Load the state file.
2. **Read the master tracker + event log first** (per Opening Protocol). Note any events since the last state-file `updated_at` — specifically credential landings, skill version bumps, or handoff status flips that affect this onboarding.
3. **Check `blocked_on` array.** If any blockers are still un-cleared (no "— CLEARED ..." suffix), surface them: "This client is still blocked on: <list>. Proceed anyway, or wait?"
4. If `current_wave` is set and `waves[<current_wave>].status == "in-progress"`, emit a wave-resume plan-bullet:

   ```
   **Resuming onboarding for <client-slug> at <current_wave>**

   Wave context (from wave_log[<prior_wave>]):
   - Prior wave shipped: <key_artifacts>
   - Spawned handoffs from prior wave: <spawned_handoffs>
   - Wave summary: <summary>

   This wave's scope: <waves[<current_wave>].scope>
   Estimated remaining: <waves[<current_wave>].estimated_hours_remaining>

   State shows step: <current_step> (<step_status[current_step]>)
   Quality-log latest: <quality_log[current_step].latest_verdict at confidence latest_confidence>

   Resume from <current_wave>? (yes / start over / pause)
   ```

5. If `current_step == "done"` and all `waves[].status == "closed"`, surface: "This client's onboarding is complete (finished at <updated_at>). No more waves planned. Start a refresh cycle?"
6. Wait for operator confirmation before proceeding.

### Wave-N → Wave-(N+1) flow

- Wave-N's Closing Protocol writes `waves[<wave_id>].status: closed` + `closed_at` + `outputs`; appends a `wave_log` entry; updates `planned_remaining_waves` (removes the just-closed wave); clears `current_wave`.
- Wave-(N+1)'s Opening Protocol reads `wave_log` for prior-wave context, sets `current_wave` to its own ID, sets `waves[<own_id>].status: in-progress` + `started_at` + `chat_id`.

## Manual operator overrides

The operator can edit the state file directly between invocations to:

- Flip a `failures[].operator_action` from `pending` to `deferred` or `retried`
- Add a service or city to `confirmed_services` / `confirmed_cities` mid-run
- Mark a step `skipped` to bypass it
- Reset `current_step` to an earlier step to force a re-run
- **Edit `planned_remaining_waves`** to collapse, split, or reorder upcoming waves. The orchestrator respects the edited shape.
- **Edit `blocked_on`** to remove or clarify blockers when they clear out-of-band (e.g., credentials wired in a separate Claude Code session). Append a CLEARED suffix rather than deleting.
- **Edit a `quality_log` iteration's `decision`** field to override Mode 5's auto-approve (`auto-ship` → `light-escalate`, etc.). The orchestrator re-reads on next invocation and honors the override.

The skill never overrides operator-edited fields without explicit confirmation.

## Migration notes (v1.0 → v1.1)

v1.0 state files load cleanly under v1.1 *for reads* — all v1.1 additions are new top-level fields or new optional sub-fields. The orchestrator's schema-version check fires on load:

- If `schema_version: "1.0"` is detected on load, the orchestrator surfaces: "State file is v1.0; this skill is v1.1. v1.1 adds `waves`, `wave_log`, `planned_remaining_waves`, `blocked_on`, `quality_log`, and `current_wave`. Migrate now (additive — preserves all v1.0 fields), or continue at v1.0 (the file stays v1.0 and must stay within v1.0 fields only — no wave/quality-log features for this client)?"
- **"Continue at v1.0" does not mean "use v1.1 features without bumping."** It means the file stays v1.0 *and the orchestrator must not write any v1.1 field*. The moment a v1.1 field would be written — whether the operator chose explicit migration or not — Write convention 9's auto-bump fires: `schema_version` bumps to `1.1` and a `_schema_version_history` entry is appended in the same write. So "continue at v1.0" is only honored as long as no v1.1 field is actually written; there is no path where a v1.1 field lands in a file still stamped v1.0.
- Explicit migration (operator chose "migrate now") is a deterministic transform: bump `schema_version`, add the new fields as empty arrays/objects, recompute `current_wave` as `null` (since v1.0 didn't track waves; the operator may need to backfill), and append the `_schema_version_history` entry. Auto-bump (a v1.1 field written without an explicit migration choice) produces the same end state via the same audit entry — explicit migration just front-loads the empty scaffolding.
- **`failures` array preserves as-is during migration.** v1.0's failure entries remain valid under v1.1's semantic distinction (catastrophic errors that stopped the orchestrator). Don't try to retroactively classify them as quality-loop entries.

## Related

- [[SKILL]] — the orchestrator skill that reads and writes this state
- [[per-artifact-sizing]] — per-artifact minute table the scope-estimation gate uses; the `planned_remaining_waves` field's `estimated_hours` comes from here
- [[references/ai-surface-reachability-matrix]] — Step 2 reads this; not state-file-related but referenced for context
- [[client-seo-onboarding-automation]] — Phase 5 of the blueprint
- [[../../second-brain/05_shared-intelligence/patterns/pattern-orchestrator-multi-chat-decomposition|orchestrator multi-chat pattern]] — the architectural rationale for v1.1's wave additions
