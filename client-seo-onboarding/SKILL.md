---
name: client-seo-onboarding
description: One-Cowork-message entry point for onboarding a brand-new SEO client end-to-end. Orchestrates research (Tier-1/2/3 briefs), authoring (client/city/service data files), bulk page scaffolding, imagery prompt generation, the human-in-the-loop Higgsfield variant pick, image wiring, publish, GSC indexing, internal linking, and dead-link audit. Triggers on phrases like "process this new client," "onboard this client for SEO," "run client-seo-onboarding on <slug>," "kick off the Core 30 build for <client>," "set up <client> end to end," "ingest these meeting notes and start the onboarding," or any time the operator hands over meeting notes + an intake form + a client slug and wants the full Core 30 pipeline run. Also use to resume a partially-completed onboarding when the operator says "pick up <slug>'s onboarding where we left off" — the skill detects the state file at 04_projects/clients/_active/<slug>/_state/onboarding.json and continues from the last completed step.
---

# Client SEO Onboarding (orchestrator skill)

The capstone of the client-SEO-onboarding automation. Reads meeting notes + intake form, runs every Phase-2/3/4 deliverable in order, pauses at the Higgsfield variant-pick gate, resumes per page after imagery is in, and finishes with a corpus-wide internal-link pass + dead-link audit + a live-URL report.

<!-- v1.1 rewrite must preserve the event-log integration below -->

**Read this file in full before touching any other file.** Every step below has a state contract, a failure mode, and a resume rule. The skill is only as smart as how strictly it follows those rules.

**Before starting any work:** read `~/workspace/second-brain/_meta/_event-log.md` and grep for events since this chat's most-recent prior touch (or last 24 hours if new chat). Note any credential landings, handoff status flips, or skill version bumps that affect this onboarding run.

## When to use this skill

- Brand-new client just signed; meeting notes + intake form just landed.
- A partially-onboarded client needs to pick back up after a pause (chat closed mid-run, operator went away for the weekend, Higgsfield was generating overnight).
- Operator wants to spin up the first wave of 5-10 Core 30 pages within a single focused work session.

## When NOT to use this skill

- A single ad-hoc page on an already-onboarded client. Use `scaffold-core-30-page.py` + `publish-core-30-page.py` directly.
- A non-WordPress client (Squarespace, custom-coded site, Wix). This skill assumes WordPress + Elementor + AIOSEO + LiteSpeed. Custom-coded clients need a separate orchestrator that doesn't exist yet — surface this and stop.
- A client refresh / rebuild on an existing slug where the operator wants to overwrite past work. The skill is non-destructive by default; for refreshes use `refresh-cached-image.py` and per-script `--overwrite` flags directly.

## Plan-bullet opening (always emit this before any tool call)

The first message of every onboarding run is a plain-language plan. Format:

```
**Onboarding plan for <client-slug>**

I'm going to:
- Read meeting notes + intake form + confirm services and cities
- Run research briefs (service base + city base + intersection + client-fact) — reusing any that exist
- Author client.json + city.json + service.json data files
- Verify WP REST API credentials work
- Bulk-scaffold every queued page in _build-order.md
- Generate Higgsfield prompts for every scaffolded page
- **Pause** and hand you the prompts. You generate in Higgsfield. Tell me "images are in" when each page's downloads are ready.
- Per page after that: ask which variant won → organize → wire → publish → request indexing
- Run insert-internal-links across the corpus, then audit-published-links to confirm no 404s
- Report every live URL + indexing status

State will live at `04_projects/clients/_active/<slug>/_state/onboarding.json` so I can resume cleanly if this chat closes.

Stopping now to let you confirm services + cities before I start. Confirm and I'll begin.
```

Always emit this. The operator should be able to spot-check the plan before the skill burns context.

## State file contract

Single source of truth for "where are we in the onboarding": `04_projects/clients/_active/<client-slug>/_state/onboarding.json`.

Shape (full schema lives in `state-schema.md` in this folder):

```json
{
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
  "confirmed_services": ["panel-upgrade", "troubleshooting", "ev-charger"],
  "confirmed_cities": ["fairfax-va", "vienna-va", "mclean-va"],
  "page_status": {
    "01-panel-upgrade-fairfax-va": {
      "scaffolded": true,
      "imagery_prompts_generated": true,
      "imagery_keepers_picked": false,
      "wired": false,
      "published": false,
      "indexed": false
    }
  },
  "failures": []
}
```

**When the skill writes state:**

- After every step transition (always before declaring the step done).
- After every per-page operation in step 8 (per-page granularity matters for resume).
- After every failure (mark step in-progress with a `failures` entry; never silently move on).

**When the skill reads state:**

- At the very start of every invocation, before the plan-bullet opening. If state exists and `current_step != "step-11-report"` and `step_status[current_step] != "done"`, the plan-bullet should reflect "resuming from step X" instead of starting fresh.

**Resume detection rule:** If the operator's message names a client slug whose `_state/onboarding.json` exists, the skill loads state, summarizes what's done, asks "Resume from step <current_step>? (yes / start over)" and waits. The operator's reply determines whether to continue from state or wipe and restart. **Never wipe state without explicit "start over" confirmation.**

## Running execution log

Every onboarding run writes to a single running execution log at:

```
04_projects/clients/_active/<client-slug>/execution-logs/execution-log-YYYY-MM-DD-onboarding-orchestration.md
```

Append (don't overwrite) every time the skill makes a non-trivial decision, hits a failure, or completes a step. Capture:

- Timestamp + step name + outcome (done / failed / paused)
- Any sub-script commands run (the literal command line, useful for debugging later)
- Any operator decisions captured (which services confirmed, which variants picked)
- Any failures with their stderr output

The execution log is the source of truth for "what actually happened" — state file is the source of truth for "where are we now." Both update together.

## The 11 steps

### Step 1 — Ingest

**Input:** meeting notes file path (or pasted text) + intake form path + client slug.

**Action:**
- Read meeting notes. Extract: business name, owner name, services mentioned, cities mentioned, existing website URL, anything the operator flagged as ambiguous.
- Read intake form. Extract the same plus pricing tier, review count, brand colors, target audience.
- Cross-reference. Surface anything inconsistent between the two ("notes say 5 services but intake names 7").
- Confirm the kebab-case `client_slug` exists or needs to be created. Slug format: `<business-name-kebab>` (no state suffix unless disambiguation needed).
- Surface the proposed (services, cities) lists to the operator.

**Operator gate:** "Here's what I extracted: <services list> in <cities list>. Confirm or adjust before I run research." Wait for confirmation. Save confirmed lists into state.

**Output:** state file with `confirmed_services` and `confirmed_cities` populated. Step 1 marked done.

**Failure modes:**
- Meeting notes file missing → stop, ask operator for the path.
- Intake form missing → ask if operator wants to proceed without it (some fields will be flagged TBD in the client brief).
- Operator-confirmed services include one with no existing service data file AND no Tier-1 brief AND no Phase 2a research plan → flag this; researching from scratch is a 30-60 min sub-chat that this skill can't run autonomously.

### Step 2 — Research briefs

**Input:** confirmed services + cities lists from step 1.

**Action:** For each kind of brief, check if it exists before producing it.

- **Service base briefs.** For each confirmed service, check `05_shared-intelligence/research-briefs/services/<service-slug>.md`. If present, reuse. If absent, invoke the `service-seo-research` skill for that service. **One service at a time** — these are 20-30 minute deep-research runs each.
- **City base briefs.** For each confirmed city, check `05_shared-intelligence/research-briefs/cities/<city-slug>.md`. Reuse if present, otherwise invoke `city-base-research`. Also one at a time.
- **Intersection briefs.** For each (service, city) pair, check `05_shared-intelligence/research-briefs/intersections/<service-slug>--<city-slug>.md`. Reuse if present, otherwise invoke `intersection-research`. These are the highest-volume — Ahmad's 30 pages was 60 cells. **Surface the total cell count to the operator and confirm before kicking off.** Operator may want to stage research (e.g., research only the first 10 cells now, defer the rest).
- **Client-fact brief.** Check `05_shared-intelligence/research-briefs/clients/<client-slug>/brief.md`. If absent, invoke `client-fact-research` passing the meeting notes path + the client's domain URL.

**Operator gate:** Before kicking off any research, summarize: "I need to run N new briefs (<service count> service, <city count> city, <intersection count> intersection, <client count> client-fact). Reusing M existing briefs. Total estimated time: <minutes>. Proceed?" Wait for confirmation.

**Output:** All briefs present on disk. State updated with brief paths for each.

**Failure modes:**
- A research sub-skill fails → mark step in-progress, log the failure, stop. Don't move on with a missing brief.
- Operator wants to defer some research → respect that; only complete cells whose briefs exist will scaffold downstream.

### Step 3 — Author data files

**Input:** all briefs from step 2.

**Action:** Run the Phase 3 scaffolders in order.

- **`scaffold-client-data.py`** with `--brief <client-fact-brief-path> --client-slug <slug>`. Produces `data/client-<slug>.json` + `<slug>.config.example.json` + a tier-3 credentials checklist. **Do not pass `--tier3-template-out` to a tier-3 path unless the operator explicitly confirms** — the skill cannot read tier-3 paths to check if they're empty (memory: never propose `--overwrite` against tier-3 paths). Default to printing the checklist to the operator chat.
- **`scaffold-service-data.py`** once per confirmed service, with `--brief <service-brief-path> --output-slug <service-slug>`.
- **`scaffold-city-data.py`** once per confirmed city, with `--city-brief <city-brief-path> --intersection-briefs <comma-separated-service-slugs> --output-slug <city-slug> --client-slug <slug>`. The intersection-briefs flag uses the service-slug convention; the script resolves the actual brief paths.

Capture each script's stdout summary (especially the `needs_authoring` and `needs_confirmation` lists) into the execution log.

**Operator gate:** After all three scaffolders run, surface:
- "Data files written. Here's what still needs operator authoring (FILL placeholders):" — list every `FILL:` field across all the scaffolded JSON.
- "Here's the credentials checklist — paste these into the tier-3 vault and confirm when populated."

Wait for operator to either confirm credentials are in tier-3 OR fill in critical FILL fields manually OR explicitly defer (the operator may want to ship scaffolded-with-FILL pages first and tune copy later).

**Output:** `data/client-<slug>.json` + `data/services/*.json` + `data/cities/*.json` all present.

**Failure modes:**
- A scaffolder refuses to overwrite an existing data file → respect the non-destructive default. Surface the `.scaffolded.json` sibling, ask operator to diff manually.
- A brief is malformed and the scaffolder can't extract mandatory fields → stop, surface the missing fields, let operator fix the brief.

### Step 4 — Verify WP REST API access

**Input:** the scaffolded `<slug>.config.example.json` from step 3.

**Action:**
- Confirm `WP_APP_PASSWORD` is set in the operator's shell environment. If not, surface the export command and the tier-3 vault location to find the password.
- Run `scaffold-client-data.py --client-slug <slug> --test-wp-auth --config <slug>.config.example.json` (or the populated `<slug>.config.json` if the operator filled it in).
- Verify the script reports `✓ User has full Core-30 publishing capability.`

**Operator gate:** None if auth succeeds. If auth fails, surface the exact error (401 / 403 / network) and the canonical fixes (check user role, regenerate app password, verify wp_base_url has no trailing slash, check security plugin like Wordfence/AIOS).

**Output:** Step 4 marked done in state.

**Failure modes:**
- Auth fails → stop. The skill refuses to proceed to step 5. Bulk scaffolding 30 pages and then discovering auth doesn't work is a footgun.

### Step 5 — Bulk scaffold

**Input:** the populated data files + a `_build-order.md` for the client.

**Action:**
- Verify `_build-order.md` exists at `04_projects/clients/_active/<slug>/website-archive/new/core-30/_build-order.md`. If absent, surface: "No build-order file exists for this client. Either create one (template at `04_projects/clients/_active/ev-electric-services/website-archive/new/core-30/_build-order.md`) or hand me the position list directly and I'll create one."
- Confirm `GOOGLE_MAPS_EMBED_API_KEY` is exported. If not, surface the export command + tier-3 vault location.
- Run `bulk-scaffold-pages.py --client <slug> --positions <range> --dry-run` first. Show the operator what would scaffold.
- After operator confirmation, run for real with `--skip-existing`.

**Operator gate:** Before the real run, confirm the position range. "I see N pages in the build order. Scaffold positions 1-N now, or pick a subset?"

**Output:** Per-page folders created under `04_projects/clients/_active/<slug>/website-archive/new/core-30/<NN>-<page-slug>/` with `draft-v1.md` + `draft-v1-WP-WRAPPED.html`. State updated with each page in `page_status` with `scaffolded: true`.

**Failure modes:**
- Any individual page fails (missing data file, malformed slug) → bulk-scaffold-pages.py continues past it and reports at the end. Capture failures into state's `failures` array. Don't try to retry them automatically — surface to operator.

### Step 6 — Imagery prompts

**Input:** all scaffolded page folders from step 5.

**Action:** For each scaffolded page, run `generate-imagery-prompts.py --page-folder <path> --client <slug>`. This creates `<page-folder>/imagery-prompts-log.md` per page with three prompts (hero, about, optional scene).

Aggregate all per-page prompt logs into a single operator-facing summary at:

```
04_projects/clients/_active/<slug>/_state/imagery-prompt-summary.md
```

The summary lists, per page:
- Page slug + position
- Hero prompt (full text, ready to paste)
- About prompt (full text)
- Scene prompt (full text, if generated)
- Per-page reference photo URLs the operator needs to upload in Higgsfield

**Operator gate:** Surface the summary's filepath and a one-line briefing: "Open `<filepath>`. Each page has 3 prompts. Generate variants in Higgsfield using the prompts and reference photos listed. Reply 'images are in' when each page's downloads are ready — we'll process them one page at a time."

**Output:** All `imagery-prompts-log.md` files written. Aggregate summary written. Step 6 marked done.

**Failure modes:**
- `generate-imagery-prompts.py` fails for one page → continue with the others, capture the failure. The operator can hand-write that page's prompts.

### Step 7 — Pause point (Higgsfield)

**Action:** The skill writes state with `current_step: "step-7-pause-higgsfield"` and `step-7-pause-higgsfield: "in-progress"`. Then it stops. Literally stops.

The skill's last message before stopping:

```
**Paused at Higgsfield gate.**

Imagery prompts are written. Open:
- Aggregate summary: <filepath>
- Per-page logs: each <page-folder>/imagery-prompts-log.md

Generate variants in Higgsfield for each page. When a page's downloads are ready, tell me:
"images are in for <page-slug>" (or "images are in for all pages")

I'll resume per-page processing from there. You can close this chat — state is saved at `<state-file-path>`.
```

The skill does NOT keep checking the staging folder or polling. It waits for the operator's next message.

### Step 8 — Resume per page

**Trigger:** Operator says "images are in for <page-slug>" or "images are in for all pages" or "process page <N>".

**Action per page:**

1. **Ask which variant won.** "For page <slug>, which hero variant did you keep (1-N)? Which about variant? Which scene variant (if generated)?" Wait for the operator's picks.
2. **Organize.** Run `organize-image-downloads.py --client <slug> --page-folder <path> --image-type hero --selected-variant <N>`. Once per slot type (hero, about, scene).
3. **Wire.** Run `wire-page-images.py --page-folder <path> --config <config-path>`. This optimizes the keeper PNG, uploads to WordPress, rewrites the HTML, and re-publishes the page.
4. **Update state.** Mark `page_status[<slug>].imagery_keepers_picked: true`, `wired: true`, `published: true`. Update execution log.
5. **Indexing.** If `gsc_service_account_path` is configured in the client config, `wire-page-images.py` → `publish-core-30-page.py` already auto-submits to GSC's Indexing API on every publish. Confirm by checking the script's stdout for `→ GSC indexing: submitted`. Mark `indexed: true`.

**Operator gate:** After each page completes, surface the live URL + indexing status. Confirm before moving to the next page (or let operator say "process all the rest" to batch).

**Failure modes:**
- `organize-image-downloads.py` fails (staging folder empty, variant number invalid) → ask the operator to re-check the Higgsfield downloads folder, surface the script's stderr.
- `wire-page-images.py` fails on upload (auth, network, file size) → capture into `failures`, mark `wired: false`, keep going with the next page if the operator confirms.
- `publish-core-30-page.py` fails on the auto-publish step → likewise capture, surface, don't auto-retry.
- GSC indexing fails → never blocks the publish (per `publish-core-30-page.py` design). Capture the error in state, surface to operator at step-11 report time.

### Step 9 — Indexing pass

In the steady state, indexing happens inline during step 8 (auto-submitted by `publish-core-30-page.py`). Step 9 exists as an explicit gate to:

1. **Confirm every published page has an indexing record.** Cross-check `page_status[*].indexed == true` for every page that completed step 8.
2. **For any page where indexing failed or was skipped** (e.g., GSC service account wasn't configured), surface the manual fallback: "GSC → URL Inspection → request indexing." List the URLs.

**Operator gate:** Surface the indexing status list. Wait for the operator to either resolve the manual ones or explicitly defer them.

**Output:** State updated. Step 9 marked done.

### Step 10 — Internal-link pass + dead-link audit

This step uses two Phase-4b scripts that live in `repos/ai-agency-core/scripts/`:

**10a. Propose internal links across the corpus.**

```bash
python3 insert-internal-links.py \
  --corpus-root <client-corpus-root> \
  --reference-architecture <link-map-synthesis-path> \
  --build-order <build-order-path> \
  --mode data-driven
```

This writes per-page `_internal-link-proposals-YYYY-MM-DD.md` + `.json` files to each page folder.

If a competitor link-map synthesis at `05_shared-intelligence/research-briefs/link-maps/_synthesis-<client>.md` does NOT exist for this client, surface that to the operator. Two options: (a) defer the link pass until a link-map synthesis is produced (via the `competitor-deep-research` skill in link-map mode), or (b) run with `--mode data-driven` only — it doesn't require the synthesis for Axis A + Axis B (only Axis D semantic linking does). The data-driven mode still produces useful proposals.

**10b. Operator review.** Surface the per-page proposal markdown files. Operator reviews and (optionally) hand-edits the JSON to drop rejected proposals.

**10c. Apply approved diffs.** Once the operator confirms, run `insert-internal-links.py` again per page with `--apply --diff-file <approved-json-path>`. Each apply writes a `draft-vN+1-WP-WRAPPED.html` alongside the old one — non-destructive.

**10d. Republish updated drafts.** For each page where links were inserted, run `publish-core-30-page.py --page-folder <path> --config <config> --version vN+1` to push the link-updated HTML to WordPress.

**10e. Dead-link audit.** Run:

```bash
python3 audit-published-links.py --corpus-root <client-corpus-root>
```

Read-only. Walks every page's HTML, reports any internal link whose destination doesn't exist as a `NN-<slug>/` folder. Output lands at `<corpus-root>/_dead-link-audit-YYYY-MM-DD.md`.

Surface the audit's "By destination" view to the operator. Top entries are the highest-leverage build-next candidates (most pages reference them and would close the most dead links).

**Operator gate:** After the audit, surface: "Audit complete. <N> dead links across <M> pages, biggest cluster is `<dest-slug>` referenced by <K> pages. Want to flag any for the build-next backlog?"

**Failure modes:**
- `insert-internal-links.py` fails on a page (malformed HTML, missing build-order) → capture, continue with the others.
- `audit-published-links.py` fails → unusual; check `--corpus-root` is correct.

### Step 11 — Final report

**Action:** Compile a single summary message:

- **Pages live.** Bullet list of `<page-slug>: <live-url>`.
- **Indexing status.** Per-page: submitted / pending / failed.
- **Internal links inserted.** Total count across the corpus, broken out by axis (A / B / C / D).
- **Dead links remaining.** Total count + the top 3 build-next candidates from the audit.
- **What still needs operator follow-up.** Bullet list pulled from `failures` in state + any deferred items + any FILL prose the operator hasn't filled yet.
- **Suggested next steps.** Bias toward what the client-fact brief flagged: analytics setup (GA4), Google Business Profile optimization, citation cleanup, social profile alignment.

Write the report to:

```
04_projects/clients/_active/<slug>/onboarding-report-YYYY-MM-DD.md
```

And surface the filepath + a short in-chat summary.

**State:** Mark `current_step: "done"` and `step-11-report: "done"`. The state file stays around — it's the canonical record of what happened.

**Auto-invoke output-quality-loop:** Per the canonical convention at `~/workspace/skills/output-quality-loop/references/auto-invoke-convention.md`, emit the block at the end of step 11, after the report file has been written and before declaring the chat done. See "Auto-invoke output-quality-loop" section near the end of this skill for the exact block format and composition semantics.

## Per-script reference card

The skill calls these scripts. Each lives at `repos/ai-agency-core/scripts/`. Confirm before calling:

| Step | Script | What it does |
|---|---|---|
| 3 | `scaffold-client-data.py` | Authors `data/client-<slug>.json` + config + credentials checklist |
| 3 | `scaffold-service-data.py` | Authors `data/services/<slug>.json` from a Tier-1 service brief |
| 3 | `scaffold-city-data.py` | Authors `data/cities/<slug>.json` from Tier-2 + Tier-3 briefs |
| 4 | `scaffold-client-data.py --test-wp-auth` | Verifies WP REST API credentials |
| 5 | `bulk-scaffold-pages.py` | Bulk scaffolds N pages from the build-order |
| 6 | `generate-imagery-prompts.py` | Generates 3 Higgsfield prompts per page |
| 8 | `organize-image-downloads.py` | Moves picked Higgsfield variants into the page folder |
| 8 | `wire-page-images.py` | Optimizes + uploads + wires + republishes images |
| 8 | `publish-core-30-page.py` | (Called internally by `wire-page-images.py`) |
| 10 | `insert-internal-links.py` | Proposes + applies internal links across the corpus |
| 10 | `audit-published-links.py` | Reports dead internal links across the corpus |

The skill never calls these:

| Script | Why not |
|---|---|
| `refresh-cached-image.py` | Cache-override for refreshes, not for new-client onboarding |
| `generate-maps-iframe.py` | Called transitively by `scaffold-core-30-page.py`; not invoked directly |
| `optimize-image.py`, `upload-image-to-wp.py`, `wire-images-into-html.py` | Helpers; called transitively by `wire-page-images.py` |

The Phase 2 research skills (`service-seo-research`, `city-base-research`, `intersection-research`, `client-fact-research`) are invoked at step 2 via skill chaining, not as scripts.

## Failure-mode reference card

Every step has a "stop and surface, don't silently continue" contract. Concretely:

- **Sub-script exits non-zero.** Capture stderr, write to execution log + state's `failures` array, surface to operator, stop the current step. Don't auto-retry.
- **A research brief is missing and the operator deferred running it.** Skip the cells whose brief doesn't exist; scaffolding will simply not include those (service, city) pairs.
- **A data file has `FILL:` placeholders in mandatory fields.** Don't scaffold pages that use it until the operator fills them.
- **Tier-3 vault path destination.** Never recommend `--overwrite` against `~/workspace/second-brain-tier3/...`. The skill can't read tier-3 to verify it's empty.
- **Operator wants to skip a step.** Allow it. Mark the step `skipped` (not `done`) in state, log the rationale.
- **Mid-step interruption.** State file persists. On resume, the in-progress step picks up from its last sub-task (e.g., step-8 resumes per-page from the last completed page).

## Plain-language enforcement

Every message the skill sends to the operator follows `second-brain/_meta/plain-language-conventions.md`:

- No jargon without inline gloss on first use ("Indexing API" → "Indexing API [Google's priority crawl queue]" the first time).
- Short sentences. Active voice.
- Lists for sequences; prose for explanations.
- No emoji unless the operator's last message had one.
- No filler ("Let me start by...", "I'll now...", "Great question.").

Every file the skill writes (state file content, execution log entries, report) also follows plain language.

## Plain-language gloss for the most common terms

These appear often enough that the skill should expect to use them; gloss inline on first mention in each new chat:

- WP REST API [WordPress's built-in API for creating and updating pages without logging in]
- Tier-3 vault [the air-gapped credentials folder at `~/workspace/second-brain-tier3/` that the skill cannot read]
- Higgsfield [an AI image generator that takes a face-reference photo and produces consistent shots of that person in different scenes]
- GSC [Google Search Console — Google's tool for monitoring how a site appears in search results]
- Core 30 [a Keelworks methodology — building 30 service-by-city pages per client as the foundation of local SEO]
- Tier-1 / Tier-2 / Tier-3 brief [in the three-tier research model: T1 = service across all cities, T2 = city across all services, T3 = one specific (service, city) pair]

## Robustness rules

- **Plan-bullet opening is mandatory.** Every fresh invocation. Every resume.
- **State file write is atomic.** Write to a temp file, then rename. Never half-write.
- **Per-page granularity in step 8.** Don't batch state writes; each page that completes flips its own `page_status` entry immediately.
- **Read state at the start of every operator message in mid-run.** The operator may have edited state by hand to override the skill's state.
- **Never call a sub-skill that has `status: in-progress` from a prior chat without confirming with the operator first.** Research sub-skills sometimes leave half-written briefs; honor those.

## Testing this skill

First real test target is **S&H Contracting** (per the handoff). Reasons:

- It's a cold-start client (no prior pipeline runs to confuse state).
- Both clients are residential electrical, so most service-base briefs from EV Electric are reusable.
- City briefs for the Fairfax/Vienna/McLean cluster overlap with EV Electric, so most Tier-2 briefs reuse.
- Only intersection briefs + the client-fact brief need fresh research.

Ahmad's EV Electric onboarding is mid-flight and will not exercise the cold-start path cleanly — don't use it for first-test.

After the S&H run, capture lessons into:

```
05_shared-intelligence/lessons/lesson-client-seo-onboarding-skill-first-real-run.md
```

Include: what took longer than expected, what the skill misjudged, what the SOP should be updated to reflect, what new failure modes surfaced.

## Output-quality-loop integration

Per the canonical convention at `~/workspace/skills/output-quality-loop/references/auto-invoke-convention.md` (made universal by Phase 5 of the output-quality-loop project, 2026-05-28), every artifact-producing skill emits the auto-invoke block at the end of its closing protocol.

**Composition note for this orchestrator skill.** Sub-skills and sub-scripts the orchestrator invokes (the four Phase-2 research skills, the Phase-3/4 Python scripts) each emit their own auto-invoke block per the convention — the orchestrator does not re-evaluate their artifacts. The orchestrator's own artifact is the final onboarding report at `04_projects/clients/_active/<client-slug>/onboarding-report-YYYY-MM-DD.md`, plus the state file as the audit-trail record.

**The block to emit at end of step 11** (substitute the actual paths):

```markdown
## Auto-invoke output-quality-loop

This skill produced the following artifact(s):
- `~/workspace/second-brain/04_projects/clients/_active/<client-slug>/onboarding-report-YYYY-MM-DD.md`

[output-quality-loop:eval] — for each artifact, run output-quality-loop in EVALUATE mode. If PASS, declare the chat done. If NEEDS REVISION or FAIL, ingest the revision prompt as if it were operator input and regenerate the artifact, then re-invoke output-quality-loop. Cap at 3 iterations; on the 3rd FAIL, escalate to the operator with the evaluation report.
```

**Operator bypass.** Honors `--bypass-quality-loop` (or "skip the quality loop") in the original onboarding request. The skill still produces the report; just skips the auto-invoke emission and writes a bypass entry to the closest `_quality-log.md`.

**Why this composes well.** Each Phase-2 research brief gets evaluated at its source skill (e.g., `service-seo-research` emits its own auto-invoke block when its brief lands). Each scaffolded JSON file is a deterministic transform of a brief and doesn't warrant its own evaluation pass. Each published page is evaluated at publish-time via the existing `publish-core-30-page.py` quality gate. The orchestrator's evaluation pass focuses on the operator-facing report — does it accurately reflect what was done, what's pending, what to do next.

## Related

- [[client-seo-onboarding-automation]] — the parent blueprint; Phase 5 spec
- [[state-schema]] — full JSON schema for the state file (sibling to this SKILL.md)
- [[sop-core-30-page-build]] — the per-page operator SOP this skill ultimately wraps
- [[sop-ai-imagery-for-core-30-pages]] — the imagery SOP wrapped by step 6-8
- [[sop-wordpress-rest-api-deploy]] — the WP publish SOP wrapped by step 8
- [[vis-extraction]] — orchestrator-skill pattern reference; state + pause + resume conventions adapted from there
- [[plain-language-conventions]] — language enforcement across every output

## Decision archaeology

- 2026-06-01 [v1 written] — initial skill written by Cowork against the Phase 5 handoff. All Phase 2/3/4 prerequisites confirmed shipped (insert-internal-links.py + audit-published-links.py landed 2026-05-31 per Phase 4b close). State file design borrows the per-step + per-page granularity pattern from vis-extraction's Phase B work. Failure-mode contract is strict: any sub-script non-zero exits stops the orchestrator; never silently continues.
