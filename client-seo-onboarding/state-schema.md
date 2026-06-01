---
type: schema
status: v1
created: 2026-06-01
tags: [skill, client-seo-onboarding, state-schema, resume-contract]
---

# State Schema — `onboarding.json`

Companion to [[SKILL]]. Defines the shape of the state file the orchestrator reads and writes to support mid-run resume.

**Location:** `~/workspace/second-brain/04_projects/clients/_active/<client-slug>/_state/onboarding.json`

One file per client. The `_state/` folder may also hold sibling artifacts (e.g., `imagery-prompt-summary.md`).

## Full schema

```json
{
  "schema_version": "1.0",
  "client_slug": "s-and-h-contracting",
  "started_at": "2026-06-01T14:00:00Z",
  "updated_at": "2026-06-01T16:30:00Z",

  "current_step": "step-7-pause-higgsfield",
  "step_status": {
    "step-1-ingest": "done",
    "step-2-research": "done",
    "step-3-author-data": "done",
    "step-4-verify-wp": "done",
    "step-5-bulk-scaffold": "done",
    "step-6-imagery-prompts": "done",
    "step-7-pause-higgsfield": "in-progress",
    "step-8-resume-per-page": "pending",
    "step-9-indexing": "pending",
    "step-10-internal-linking": "pending",
    "step-11-report": "pending"
  },

  "ingest": {
    "meeting_notes_path": "/Users/.../meeting-notes-2026-06-01.md",
    "intake_form_path": "/Users/.../intake-form-2026-06-01.md",
    "extracted_business_name": "S&H Contracting Unlimited",
    "extracted_owner_name": "Mohammad ...",
    "extracted_existing_url": "https://...",
    "ambiguities_surfaced": [
      "intake mentioned generator installation but notes did not"
    ]
  },

  "confirmed_services": ["panel-upgrade", "troubleshooting", "ev-charger"],
  "confirmed_cities": ["fairfax-va", "vienna-va", "mclean-va"],

  "research_status": {
    "service_briefs": {
      "panel-upgrade": "reused",
      "troubleshooting": "reused",
      "ev-charger": "produced"
    },
    "city_briefs": {
      "fairfax-va": "reused",
      "vienna-va": "reused",
      "mclean-va": "produced"
    },
    "intersection_briefs": {
      "panel-upgrade--fairfax-va": "produced",
      "panel-upgrade--vienna-va": "reused",
      "panel-upgrade--mclean-va": "produced"
    },
    "client_brief": "produced"
  },

  "data_files": {
    "client_json": "data/client-s-and-h-contracting.json",
    "service_jsons": ["data/services/panel-upgrade.json"],
    "city_jsons": ["data/cities/fairfax-va.json"],
    "config_file": "s-and-h-contracting.config.json",
    "tier3_credentials_status": "pending-operator-population"
  },

  "wp_auth": {
    "verified": true,
    "user_role": "administrator",
    "verified_at": "2026-06-01T15:10:00Z"
  },

  "page_status": {
    "01-panel-upgrade-fairfax-va": {
      "scaffolded": true,
      "scaffolded_at": "2026-06-01T15:30:00Z",
      "imagery_prompts_generated": true,
      "imagery_keepers_picked": false,
      "wired": false,
      "published": false,
      "live_url": null,
      "indexed": false,
      "internal_links_proposed": false,
      "internal_links_applied": false
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

  "failures": [
    {
      "step": "step-5-bulk-scaffold",
      "page_slug": "07-generator-installation-fairfax-va",
      "error": "no service data file: data/services/generator-installation.json",
      "timestamp": "2026-06-01T15:40:00Z",
      "operator_action": "deferred"
    }
  ]
}
```

## Field semantics

### Top-level identity

- **`schema_version`** — `"1.0"` for now. Increment when the schema changes in a way that breaks older state files.
- **`client_slug`** — kebab-case slug; matches the `04_projects/clients/_active/<slug>/` folder name and the `data/client-<slug>.json` filename.
- **`started_at` / `updated_at`** — ISO 8601 UTC timestamps. `updated_at` rewrites on every state write.

### Step tracking

- **`current_step`** — string. The step the skill was last working on. On resume, the skill reads this first.
- **`step_status`** — one of `pending` / `in-progress` / `done` / `skipped` per step. The skill walks these in order; a step can only transition `pending → in-progress → done` (or `pending → skipped` if the operator explicitly skipped).

### Per-step substate

Each step's per-step state lives in its own top-level key:

- **`ingest`** — what was extracted from the meeting notes and intake form
- **`confirmed_services` / `confirmed_cities`** — the operator-confirmed lists (the contract for what gets researched + scaffolded)
- **`research_status`** — per-brief status: `reused` (already existed) / `produced` (newly researched) / `deferred` (operator skipped) / `failed` (sub-skill errored)
- **`data_files`** — paths to the scaffolded JSON files + a `tier3_credentials_status` flag
- **`wp_auth`** — verification result
- **`page_status`** — per-page bitmap of what's been done; the most granular slice (resume into the middle of step 8 reads this to know which page to pick up from)
- **`internal_linking`** — counters + the synthesis-file pointer
- **`report`** — pointer to the final report

### Failures array

- **`failures`** — append-only log. Each entry: `step` + identifying context (`page_slug`, `service_slug`, etc.) + the `error` text + a `timestamp` + an `operator_action` field that the skill updates when the operator decides what to do (`deferred` / `retried` / `accepted` / `pending`).

## Write conventions

1. **Atomic writes.** Write to `onboarding.json.tmp`, then `mv` to `onboarding.json`. Never half-write.
2. **Per-page granularity in step 8.** Each page's per-slot completion flips its own bit in `page_status[<page-slug>]` immediately. Don't batch.
3. **Always update `updated_at` on every write.**
4. **Never delete the `failures` array** without explicit operator confirmation; it's the audit trail.

## Read conventions

1. **Read at every fresh invocation.** Before the plan-bullet opening, the skill checks for an existing state file.
2. **Read at every operator message in mid-run.** The operator may have edited state by hand to override the skill (e.g., flipping a `failures` entry's `operator_action: deferred` to `retried`).
3. **Detect schema-version mismatch.** If `schema_version` in the file is older than the current skill version, surface to the operator: "State file is schema v0.X; this skill is v1.0. Migrate or start over?"

## Resume contract

On invocation with a client slug whose state file exists:

1. Load the state file.
2. If `current_step == "done"`, surface: "This client's onboarding is already complete (finished at <updated_at>). Start a fresh onboarding (rare) or load an existing data refresh script?"
3. If `current_step != "done"`, emit a resume plan-bullet:
   ```
   **Resuming onboarding for <client-slug>**

   State shows we were at: <current_step>
   Done so far: <list of done steps>
   In progress: <current_step substate summary>
   Pending: <list of pending steps>

   Resume from <current_step>? (yes / start over)
   ```
4. Wait for operator confirmation before proceeding.

## Manual operator overrides

The operator can edit the state file directly between invocations to:

- Flip a `failures[].operator_action` from `pending` to `deferred` or `retried`
- Add a service or city to `confirmed_services` / `confirmed_cities` mid-run (the skill picks it up on next invocation)
- Mark a step `skipped` to bypass it (the skill respects this and moves on)
- Reset `current_step` to an earlier step to force a re-run

The skill never overrides operator-edited fields without explicit confirmation.

## Related

- [[SKILL]] — the orchestrator skill that reads and writes this state
- [[client-seo-onboarding-automation]] — Phase 5 of the blueprint
