---
name: client-seo-onboarding
version: 1.7
description: One-Cowork-message entry point for onboarding a brand-new SEO client end-to-end. v1.1 wraps the v1.0 11-step pipeline (research → author data → verify WP → scaffold → imagery → publish → index → internal links → report) with three load-bearing additions — per-step `output-quality-loop` integration (Mode 1 EVALUATE + Mode 4 AUTO-RESEARCH + Mode 5 AUTO-APPROVE per artifact), multi-chat wave decomposition baked into the plan-bullet opening (scope-estimation gate computes hours + chat count + wave shape before any work fires), and the AI-surface reachability matrix that replaces "Cowork can't reach X" framing with concrete per-surface paths (Perplexity Sonar + OpenAI + Gemini + Anthropic Claude all working today via tier-3 carve-out; AI Overviews via Claude in Chrome). Triggers on phrases like "process this new client," "onboard this client for SEO," "run client-seo-onboarding on <slug>," "kick off the Core 30 build for <client>," "set up <client> end to end," "ingest these meeting notes and start the onboarding," or any time the operator hands over meeting notes + an intake form + a client slug and wants the full Core 30 pipeline run. Also use to resume a partially-completed onboarding when the operator says "pick up <slug>'s onboarding where we left off" — the skill detects the state file at 04_projects/clients/_active/<slug>/_state/onboarding.json and continues from the last completed step (or last in-progress wave for multi-chat runs).
---

# Client SEO Onboarding (orchestrator skill, v1.7)

> **v1.7 changelog (2026-06-12, [WF-2] close-out)** — `seo-site-teardown` (v1.1, registered 2026-06-11) wired into Step 2 as the website-factory path check: when the engagement includes (or will include) a custom-site build, run `seo-site-teardown` on the strongest reference competitor BEFORE or alongside the research briefs — it is the mandatory first step of every website-factory client build and its reproduction blueprint is what the build phases consume. Composes with `competitor-deep-research` (landscape first, teardown the winner). Also fixes the stale title-line version (said v1.5 since the v1.6 bump). No other behavior change.

> **v1.6 changelog (2026-06-06, quality-tool-integration-audit)** — Three D-row fixes from S&H wave-2 calibration. (1) **D-07 fix:** quality-loop-fired checkpoint — orchestrator must verify `quality_log` has a verdict for every artifact before declaring any step done; not optional under time pressure. (2) **D-08 fix:** house-voice-rewrite Mode 2 wired as a mandatory compose step between Produce and Auto-evaluate on Steps 5 and 8 (client-facing copy steps); personality file referenced from client state. (3) **D-09 fix:** meta-vs-body consistency dimension added to `evaluation-heuristics-by-type.md` for Core 30 page drafts — response-time, pricing, and credential claims cross-checked between body HTML and `aioseo_description:` frontmatter.

> **v1.5 changelog (2026-06-06, prioritization-skill-extraction)** — Step 1 build-order generation now delegates to the standalone `prioritization` skill (`skills/prioritization/`) with the `core-30-service-city-seo` profile instead of owning the ranking logic inline. When no `_build-order.md` exists and the prioritization skill is available, Step 1 invokes it with the extracted services + cities as the candidate set and the `core-30-service-city-seo` profile. Output is a two-file pair (`_build-order.md` + `_build-order-ranking.json`) written to the client's `core-30/` directory. When the prioritization skill is absent (directory missing or profile not found), Step 1 falls back to inline build-order proposal (v1.4 behavior) and logs a warning. Same SEO output, no regression. Existing `_build-order.md` cross-check logic (build-order wins on disagreement, per DF-02 + DF-03) is unchanged — it fires before the skill delegation path.

> **v1.4 changelog (2026-06-05, Build wave 4)** — gate-peer-reviewer v2 autonomous dispatch integration. After each artifact-producing step's quality-loop exit (Steps 3/5/6/8/11), the orchestrator spawns the peer-reviewer as a Claude Code Task sub-agent that runs registered Check 1 satisfaction targets (full-placeholder-family-sweep, source-client-leak-audit, live-rendered-cache-busted-verification per gate type) + Checks 2-6. Returns structured JSON verdict inlined alongside gate output for operator — single approve surface, no manual paste-transport. REJECT-AND-REDO auto-fixes before surfacing (capped at 2 iterations). Graceful degradation logs `peer-reviewer-skipped` to event log if Task fails. Steps 1/2/4/7/9/10 excluded (no template-derived artifacts or covered by other orchestrators). See § "Peer-reviewer dispatch (v1.4)" for the full integration block.

> **v1.3 changelog (2026-06-04, [T2-7] + [T2-6])** — Two rounds of substantive Step 6/7/8 edits. **(1) [T2-7] publish-verification hardening (2026-06-04):** Step 8 expanded from 3 substeps to 7 — added substep 4 (live-rendered cache-busted verification: modified_time, eyebrow H1, title visibility, font family, image fill, map fill, zero placeholder text, rendered-structure comparison to known-good sibling), substep 5 (cache-purge + incognito re-check with stale-cache/screenshot-conflict rules), substep 6 (state update with `live_verified: true`), substep 7 (GSC indexing only after substep 4 passes). Both substeps 4 and 5 are convention-class (SOP prose, not deterministic gates). Failure modes updated for template-parity, placeholder hard-block, disk-sync refusal, live-verification failure, stale-cache persistence. Sourced from EV pages 06-12 run Issues #24-#28. **(2) [T2-6] imagery-wave integration (2026-06-04):** Step 6 enhanced — `generate-imagery-prompts.py` now takes `--hero-style {ahmad-centric,service-scene,hands-only}`, emits self-documenting per-prompt headers (Type / Reference photos / Aspect / Produces), carries embroidered-no-patch wardrobe clause (Issue #20), references `marketing-assets/reference-photos/` home per `_meta/conventions.md` § "Client imagery reference assets," surfaces About-portrait reuse from prior-log cache. Step 7 pause message enhanced with self-documenting prompt guidance + reference-photo home path + variant-selection flow preview. Step 8 substep 1 enhanced — variant-selection now routed through `_pending-operator-decisions.md` gate file per `operator-gate-routing`; multi-page same-service batch guidance added. Substep 2 enhanced with `--copy-to` mode for multi-page batches (Issue #19). Publish-depends-on-imagery guard added after Step 8 failure modes (Issue #15: no publish with dangling placeholder image refs unless explicit operator-approved bypass via gate file). Sourced from EV pages 06-12 run Issues #15-#20.

> **v1.2 changelog (2026-06-03, Phase 5B)** — Closed the silent schema-drift hole sweep [4] caught on S&H's `onboarding.json` (file sat at `schema_version: "1.0"` while wave writers added v1.1 fields for 24+ hours). Added to `state-schema.md`: (1) a canonical `SCHEMA_FIELDS` registry (version-keyed top-level field sets), (2) Write convention 9 — schema-version auto-bump + `_schema_version_history` audit on any additive write; refuse non-additive changes (field removal / type change). Reconciled two pre-existing contradictions that previously said additive writes need no bump (the `schema_version` field-semantics line + the migration-notes section). **No schema-shape change** (`schema_version` stays `1.1`); this is a writer-behavior + documentation change. **Enforcement is LLM-convention-class — the same reliability class that drifted at sweep [4]** — it documents the rule and kills the contradiction but is not deterministic. A hard, un-skippable guard (the Python pre-write hook the Phase 5B handoff originally specified) was REJECTED for now because no Python state writer exists — `onboarding.json` is written by this orchestrator following prose conventions, not by a code module. The deterministic guard is parked as Phase 5B Path B, conditional on state writes becoming script-mediated.

The capstone of the client-SEO-onboarding automation. Reads meeting notes + intake form, runs every Phase-2/3/4 deliverable in order through the per-step quality-loop contract, pauses at the Higgsfield variant-pick gate, resumes per page after imagery is in, and finishes with a corpus-wide internal-link pass + dead-link audit + a live-URL report.

<!-- v1.1 PRESERVED: event-log pre-flight integration below; do not strip -->

**Read this file in full before touching any other file.** Every step has a state contract, a quality-loop contract, a failure mode, and a resume rule. The skill is only as smart as how strictly it follows those rules.

**Before starting any work:** read `~/workspace/second-brain/_meta/_event-log.md` and grep for events since this chat's most-recent prior touch (or last 24 hours if new chat). Note any credential landings, handoff status flips, or skill version bumps that affect this onboarding run. Use the helper at `~/workspace/repos/ai-agency-core/scripts/append_event_log.sh` to append rows at significant edits during the run.

## When to use this skill

- Brand-new client just signed; meeting notes + intake form just landed.
- A partially-onboarded client needs to pick back up after a pause (chat closed mid-run, operator went away for the weekend, Higgsfield was generating overnight, prior wave shipped and next wave is queued).
- Operator wants to spin up the first wave of 5-10 Core 30 pages within a single focused work session.

## AI-surface reachability matrix

Before any research sub-skill or sub-script fires, the orchestrator surfaces the current state of each AI surface to the operator. Sourced from [[references/ai-surface-reachability-matrix|ai-surface-reachability-matrix.md]] (which mirrors the `reference_ai_surface_reachability_from_cowork` memory).

**Current matrix (2026-06-02):**

| Surface | Path | Status |
|---|---|---|
| Perplexity Sonar | `perplexity_sonar.py` via tier-3 wrapper | Working today |
| OpenAI gpt-4o | `openai_query.py` via tier-3 wrapper | Working today |
| Gemini gemini-2.5-flash | `gemini_query.py` via tier-3 wrapper | Working today |
| Anthropic claude-sonnet-4-6 | `claude_query.py` via tier-3 wrapper | Working today |
| Google AI Overviews | Claude in Chrome (`mcp__Claude_in_Chrome__navigate` + `mcp__Claude_in_Chrome__get_page_text`) | Working via Chrome; load tools via ToolSearch |

**Plain-language rule (load-bearing):** NEVER frame any of these as "blocked from Cowork." Use concrete path names (e.g., "via Sonar wrapper", "via Claude in Chrome navigate"). The only legitimate per-surface deferral language is "operator declined to provide key" — which doesn't apply post-2026-06-02 since all four keys are wired.

If you find yourself about to write "Cowork can't reach X," stop. Consult the matrix. Verify reachability via direct probe if uncertain (`curl -sSI https://<endpoint>` returning anything other than `000` / timeout = endpoint reachable; auth or path issue is a different problem).

## When NOT to use this skill

- A single ad-hoc page on an already-onboarded client. Use `scaffold-core-30-page.py` + `publish-core-30-page.py` directly.
- A non-WordPress client (Squarespace, custom-coded site, Wix). This skill assumes WordPress + Elementor + AIOSEO + LiteSpeed. Custom-coded clients need a separate orchestrator that doesn't exist yet — surface this and stop.
- A client refresh / rebuild on an existing slug where the operator wants to overwrite past work. The skill is non-destructive by default; for refreshes use `refresh-cached-image.py` and per-script `--overwrite` flags directly.

## Scope-estimation gate (run first)

**Fires BEFORE the plan-bullet opening.** Computes the total run hours + chat count + wave decomposition so the operator sees the real shape upfront instead of discovering it mid-run.

### Steps

1. **Read the build-order.** Glob `04_projects/clients/_active/<slug>/website-archive/new/core-30/_build-order.md`. Extract the services column and the cities column. These are authoritative (see "Pre-flight handoff cross-check" below).
2. **Glob existing artifacts.** For each (service, city, intersection, client-fact) brief and data file, check if it already exists on disk. Record reuse vs new.
3. **Compute total minutes** using [[per-artifact-sizing|per-artifact-sizing.md]]:
   ```
   total_minutes = (
     sum(new_artifacts × per_artifact_minutes) +
     sum(operator_attended_minutes)
   ) × 1.15  # quality-loop overhead
   ```
4. **Compute wave count.** `ceil(total_minutes / 60 / per_chat_budget_hours)` where `per_chat_budget_hours` defaults to 3-4.
5. **Decompose into named waves.** Use the wave-shape recommendations in `per-artifact-sizing.md` (research wave + scaffold wave + N publish waves).
6. **Surface the decomposition to the operator** as part of the plan-bullet opening (next section).

### Pre-flight handoff cross-check

If a handoff prompt claims specific artifacts exist as "reuse," verify each path on disk before trusting. Surface discrepancies as part of the scope-estimation output. The build-order is authoritative when it disagrees with the handoff's claimed services / cities / counts. See lesson `lesson-client-seo-onboarding-skill-first-real-run` § DF-01, DF-02, DF-03 for the precipitating incidents.

## Plan-bullet opening (always emit this before any tool call)

The first message of every onboarding run is a plain-language plan that reflects the scope-estimation gate's output. Format:

```
**Onboarding plan for <client-slug>**

Estimated scope: <total_hours> hours across <wave_count> chats.

AI surfaces for this run:
- Perplexity Sonar — working (tier-3 wrapper)
- OpenAI gpt-4o — working (tier-3 wrapper)
- Gemini gemini-2.5-flash — working (tier-3 wrapper)
- Anthropic claude-sonnet-4-6 — working (tier-3 wrapper)
- Google AI Overviews — via Claude in Chrome

Waves planned:
- wave-A1 (research, ~3h): <scope>
- wave-A2 (research, ~3h): <scope>
- ...
- wave-S1 (scaffold, ~1.5h): <scope>
- wave-P1..P6 (publish, ~2h each, operator-attended): <scope>

This chat will run <wave-id> only — <scope>.

I'm going to (within this chat):
- Read meeting notes + intake form + confirm services and cities (build-order authoritative on disagreement)
- Run the research / scaffold / publish work for this wave
- Run output-quality-loop after every artifact (PASS → proceed; NEEDS REVISION → regenerate via Mode 4 Sonar; FAIL → escalate)
- Update state.waves, state.wave_log, state.planned_remaining_waves on wave close
- Emit per-wave handoff prompt for the next wave

State will live at `04_projects/clients/_active/<slug>/_state/onboarding.json` so we resume cleanly across waves.

Stopping now to let you confirm services + cities + wave shape before I start. Confirm and I'll begin.
```

Always emit this. Operator spot-checks the plan + the wave shape + the surface state before the skill burns context.

## State file contract

Single source of truth for "where are we in the onboarding": `04_projects/clients/_active/<client-slug>/_state/onboarding.json`.

Full schema lives in [[state-schema|state-schema.md]]. v1.1 extends v1.0 with five new top-level structures:

- **`current_wave`** — string. The wave the skill is currently working in.
- **`waves`** — array. Each entry describes one planned or completed wave (`wave_id`, `status`, `started_at`, `closed_at`, `chat_id`, `scope`, `outputs`).
- **`wave_log`** — array. Append-only per-wave summary at wave-close (`wave_id`, `summary`, `key_artifacts`, `spawned_handoffs`, `verdict_summary`).
- **`planned_remaining_waves`** — array. Forward-planning shape (`wave_id`, `scope`, `estimated_hours`, `blocks_on`). Operator-editable between waves.
- **`blocked_on`** — free-text array. One line per blocker. Mirrors the S&H state file shape from 2026-06-01.
- **`quality_log`** — object keyed by step (and nested by artifact for multi-artifact steps). Records per-artifact verdicts + confidence + iteration count from output-quality-loop Modes 1-5.

**When the skill writes state:**

- After every step transition (always before declaring the step done).
- After every per-page operation in step 8 (per-page granularity matters for resume).
- After every quality-loop verdict (per-artifact granularity in `quality_log`).
- After every failure (mark step in-progress with a `failures` entry; never silently move on).
- At wave-close (writes `waves[<wave_id>].status: closed` + `closed_at` + `outputs`; appends `wave_log` entry; clears `current_wave`).

**When the skill reads state:**

- At the very start of every invocation, before the plan-bullet opening. If state exists, the plan-bullet should reflect "resuming from wave <id>" or "resuming from step <X>" instead of starting fresh.
- At every operator message in mid-run. The operator may have edited state by hand (especially `planned_remaining_waves` or `blocked_on`).

**Resume detection rule:** If the operator's message names a client slug whose `_state/onboarding.json` exists, the skill loads state, checks `blocked_on` for un-cleared blockers, summarizes prior-wave context from `wave_log`, asks "Resume from wave <current_wave>? (yes / start over / pause)" and waits. **Never wipe state without explicit "start over" confirmation.**

## Running execution log

Every onboarding run writes to a single running execution log at:

```
04_projects/clients/_active/<client-slug>/execution-logs/execution-log-YYYY-MM-DD-onboarding-orchestration.md
```

Append (don't overwrite) every time the skill makes a non-trivial decision, hits a failure, or completes a step. Capture: timestamp + step name + outcome (done / failed / paused) + any sub-script commands run (literal command line) + any operator decisions captured + any failures with their stderr output + every quality-loop verdict (verdict + confidence + iteration count + decision).

The execution log is the source of truth for "what actually happened" — state file is the source of truth for "where are we now." Both update together.

## Per-step quality loop contract

The orchestrator does not just emit `output-quality-loop` auto-invoke blocks and trust sub-skills to honor them — it actively routes every artifact-producing step through the full four-substep contract before declaring the step done. This is the load-bearing reliability discipline that prevents upstream defects (missing AI-citation backfill in a brief, malformed JSON field in a data file, broken HTML in a scaffolded page) from compounding across the corpus.

See [[../../second-brain/05_shared-intelligence/patterns/pattern-orchestrator-multi-chat-decomposition|the orchestrator multi-chat pattern]] component #2 for the architectural rationale.

### Quality-loop-fired checkpoint (v1.6 — D-07 fix)

Before the orchestrator declares ANY artifact-producing step done (Steps 1, 2, 3, 5, 6, 8, 10, 11), it MUST verify that the four-substep quality loop actually fired for every artifact that step produced. Concretely: check that `quality_log` in the state file has an entry for each artifact path with a verdict value. If any artifact is missing a verdict entry, the quality loop was skipped — do NOT proceed to the next step. Instead, run the quality loop on the unverified artifact(s) now.

**This is not optional under time pressure.** D-07 (S&H wave-2 calibration, 2026-06-06): the orchestrator skipped the quality loop at Step 5 under throughput pressure. The publish gate caught it — but the fix belongs earlier. The state-file check is the enforcement mechanism: no verdict in `quality_log` = step not done, regardless of what the orchestrator thinks it accomplished.

### House-voice composition (v1.6 — D-08 fix)

Every artifact-producing step that generates **client-facing copy** (currently Steps 5 and 8) runs `house-voice-rewrite` Mode 2 as a mandatory compose step between Produce and Auto-evaluate. The house-voice pass rewrites the scaffolded/authored content against the client's personality file before the quality-loop evaluates it — ensuring the quality loop scores the voiced draft, not the generic one.

**Composition shape:**

1. **Produce** — scaffold or author the artifact.
2. **House-voice-rewrite** — invoke Mode 2 with: `draft_path` = the just-produced artifact, `personality_file` = `04_projects/clients/_active/<slug>/_state/personality-<slug>.md` (produced by house-voice-rewrite Mode 1 during client onboarding). If the personality file doesn't exist, surface: "No personality file found for <slug>. Run house-voice-rewrite Mode 1 first, or skip voice-rewrite with `--bypass-house-voice`." The voice-rewritten draft overwrites the original draft file (non-destructive: the original is versioned via `draft-v1` → `draft-v2` naming).
3. **Auto-evaluate** — quality-loop evaluates the voice-rewritten draft.
4. (rest of four-substep contract continues)

**Which steps compose house-voice:** Steps 5 (bulk scaffold) and 8 (resume per page). Steps 1/2/3/6/10/11 do not produce client-facing editorial copy. Step 2 (research briefs) and Step 3 (data files) are internal artifacts.

**Graceful degradation:** If `~/workspace/skills/house-voice-rewrite/SKILL.md` doesn't exist, log `house-voice-skipped` to execution log and proceed without voice-rewriting. The quality-loop's plain-language dimension still fires — the page won't read as well but will still publish.

### The four sub-steps (every artifact-producing step runs these in order)

1. **Produce** — invoke the sub-skill or sub-script that authors the artifact.
1b. **House-voice compose** (Steps 5 and 8 only) — invoke `house-voice-rewrite` Mode 2 per the composition shape above.
2. **Auto-evaluate** — invoke `output-quality-loop` Mode 1 (EVALUATE) on the produced artifact. The orchestrator passes the artifact path; `output-quality-loop` walks its spec-routing table to load the right specs and produces a verdict (PASS / NEEDS REVISION minor / NEEDS REVISION substantive / FAIL) plus a per-checklist-item evaluation report. Verdict and folder-log update happen on every call — no skips.
3. **Auto-elevate** — if verdict ≠ PASS, invoke Mode 4 (AUTO-RESEARCH) via `perplexity-refinement` → Sonar. Mode 4 surfaces top-N gaps, runs cited research, produces elevation suggestions feeding Mode 2's revision prompt. Regenerate the artifact using the revision prompt, loop back to sub-step 2. Cap at 3 iterations per artifact. On 3rd FAIL, stop and escalate.
4. **Auto-decide** — invoke Mode 5 (AUTO-APPROVE-AND-ESCALATE). Mode 5 computes per-type confidence + applies per-type auto-approve threshold from `references/confidence-calibration.md`. Three outcomes: PASS at or above threshold → mark step done + proceed; light escalation → `_escalation-queue.md` row + pause; hard escalation → `_meta/escalations/` file + master tracker row + pause.

### Step-by-step applicability

The 11 steps split into two groups by whether they produce an evaluable artifact:

**Artifact-producing steps (run the four-substep quality loop):**

| Step | Artifact(s) | Mode-1 type routing | Mode-5 threshold |
|---|---|---|---|
| 1 — Ingest | Extracted business context (state `ingest` block) | Meeting-notes extraction completeness | 85 |
| 2 — Research briefs | Service / city / intersection / client-fact briefs (one call per brief) | Research brief spec | 85 |
| 3 — Author data files | `client-<slug>.json`, `services/*.json`, `cities/*.json` | Scaffolded data file (schema validity + cross-brief consistency) | 90 |
| 5 — Bulk scaffold | Per-page `draft-v1.md` + `draft-v1-WP-WRAPPED.html` | Core 30 page draft spec | 95 |
| 6 — Imagery prompts | Per-page `imagery-prompts-log.md` + `_state/imagery-prompt-summary.md` | Imagery-prompt log | 80 |
| 8 — Resume per page | Post-wire `<page-folder>/draft-vN-WP-WRAPPED.html` (highest-N on disk) | Core 30 page draft spec (re-eval post-imagery) | 95 |
| 10 — Internal-link pass + audit | `_internal-link-proposals-*.md`, `_dead-link-audit-*.md` | Internal-link proposals + Dead-link audit | 85 |
| 11 — Final report | `onboarding-report-YYYY-MM-DD.md` | Onboarding final report | 85 |

**Protocol / verification steps (no artifact — SKIP quality loop):**

These steps do real work but produce no evaluable artifact. The orchestrator does NOT route them through `output-quality-loop`. Documented explicitly so maintenance chats don't wonder.

| Step | Why no quality loop |
|---|---|
| 4 — Verify WP REST API | Verification only. Script's PASS / FAIL output IS the gate. |
| 7 — Pause (Higgsfield) | Wait state. Skill emits stop message + waits for next operator message. |
| 9 — Indexing confirmation gate | Cross-checks `page_status[*].indexed == true`. State file IS the artifact; evaluating it would be circular. |

### Per-step quality-loop invocation block

Every artifact-producing step's exit (just before declaring the step done in state) emits an auto-invoke block specific to that step's artifact(s) — see each step's `Quality loop:` subsection below for the exact block format.

Step 11's final-report block aggregates across the run — it does not newly evaluate every prior artifact (those were each evaluated at their own step). Step 11 evaluates the report itself for accuracy + completeness against the run state.

### State-file integration

Per-step quality-loop verdicts persist in state via the `quality_log` field. On resume, the orchestrator reads `quality_log` to know which artifacts already passed and which are mid-iteration. See `state-schema.md` for shape.

### Event-log integration on verdict transitions

On verdict PASS at threshold or any escalation (light or hard), the orchestrator appends a row to `_event-log.md` via `append_event_log.sh`. Mode 4 internal iterations do NOT append (would be log spam); only the final verdict transition appends. This makes per-step quality outcomes visible to parallel chats in other terminals. Concrete row shape:

```bash
~/workspace/repos/ai-agency-core/scripts/append_event_log.sh \
  "04_projects/clients/_active/<slug>" \
  "n/a" \
  "<chat-id>" \
  "Quality-loop <verdict> at confidence <N> on <artifact-path>"
```

### What happens when output-quality-loop itself is unreachable

If `output-quality-loop` returns an error (spec source moved, routing table has no entry for the artifact type), the orchestrator:

1. Captures the error into `failures` array with `step` + `artifact_path` + `error`
2. Surfaces the gap: "output-quality-loop failed on `<artifact>` because `<reason>`. Options: (a) extend the routing table, (b) skip quality-loop for this artifact this run only (`--skip-quality-loop-this-artifact`), (c) abort the step."
3. Waits for operator decision. **Never silently skips the loop** — that would defeat the per-step contract.

## The 11 steps

### Step 1 — Ingest

**Input:** meeting notes file path (or pasted text) + intake form path + client slug.

**Action:**
- Read meeting notes. Extract: business name, owner name, services mentioned, cities mentioned, existing website URL, anything the operator flagged as ambiguous.
- Read intake form. Extract the same plus pricing tier, review count, brand colors, target audience.
- Cross-reference. Surface anything inconsistent between the two.
- **Build-order cross-check.** If `04_projects/clients/_active/<slug>/website-archive/new/core-30/_build-order.md` exists, glob its services + cities columns. Compare against the extracted lists. **Build-order wins on disagreement** (per DF-02 + DF-03 lessons). Surface: "Notes mention 5 services, build-order names 4. Proceeding with build-order's list. Confirm?"
- **Build-order generation (v1.5 — delegated to `prioritization` skill).** If no build-order exists, generate one:
  1. Check if `skills/prioritization/SKILL.md` exists AND `skills/prioritization/references/profiles/core-30-service-city-seo.md` exists.
  2. **If both exist:** invoke the `prioritization` skill with:
     - `candidate_set`: the service × city matrix derived from the extracted lists (each cell = one candidate item with `service` + `city` attributes)
     - `profile`: `core-30-service-city-seo`
     - `output_path`: `04_projects/clients/_active/<slug>/website-archive/new/core-30/`
     - Any operator-stated service priority or city priority from meeting notes / intake form passed as `criteria_override` for the `service_priority` and `city_anchor` value orderings
  3. The skill produces `_build-order.md` + `_build-order-ranking.json` in the output directory.
  4. Surface the generated build-order to the operator for confirmation at the bundled Step-1 gate (same 4-outcome prompt as the cross-check path).
  5. **If skill is absent (graceful fallback):** propose a build-order inline based on the extracted lists (v1.4 behavior). Log: "prioritization skill not found at skills/prioritization/ — falling back to inline build-order proposal."
- Confirm the kebab-case `client_slug` exists or needs to be created.

**Operator gate (bundles 4 outcomes):** The Step-1 operator prompt bundles the extraction-confirmation surface AND the quality-loop verdict so the operator makes both decisions at the same prompt. Four possible outcomes: (a) confirm services+cities + accept verdict, (b) adjust services+cities + accept verdict, (c) confirm services+cities + override verdict, (d) adjust + override. Concrete prompt:

```
Here's what I extracted [services + cities lists, with build-order authority noted].
Quality-loop verdict: <verdict> at confidence <N>.

Confirm extraction + accept verdict? (yes / adjust / accept-but-override-verdict / both)
```

Wait for confirmation. Save confirmed lists + `build_order_path` + `build_order_authoritative: true|false` into state.

**Output:** state file with `confirmed_services`, `confirmed_cities`, and the `ingest` block populated. Step 1 marked done.

**Quality loop:** four-substep contract per "Per-step quality loop contract" § above.
- Mode 1 evaluates extracted summary against source meeting notes for completeness.
- Mode 4 (if NEEDS REVISION) re-reads notes section by section + elevates.
- Mode 5 PASS threshold: 85.
- Verdict surfaced to operator at the bundled Step-1 gate (above).

```markdown
## Auto-invoke output-quality-loop

This step produced:
- `~/workspace/second-brain/04_projects/clients/_active/<slug>/_state/onboarding.json` (`ingest` block)

[output-quality-loop:eval] — see "Per-step quality loop contract" section for the four-substep contract.
```

**Failure modes:**
- Meeting notes file missing → stop, ask operator for the path.
- Intake form missing → ask if operator wants to proceed without it (some fields flagged TBD).
- Build-order parse fails (malformed table) → surface the bad row, ask operator to fix before proposing extraction overrides.
- Operator-confirmed services include one with no existing service data file AND no Tier-1 brief AND no Phase 2a research plan → flag this; researching from scratch is a 25-30 min sub-skill that needs explicit operator OK.

### Step 2 — Research briefs

**Input:** confirmed services + cities from Step 1.

**Action:**

- **AI-surface reachability check (fires first).** Read [[references/ai-surface-reachability-matrix|the matrix]]. Surface the current state of each surface to the operator:

  ```
  AI surfaces for this run:
  - Perplexity Sonar — working (tier-3 wrapper)
  - OpenAI gpt-4o — working (tier-3 wrapper)
  - Gemini gemini-2.5-flash — working (tier-3 wrapper)
  - Anthropic claude-sonnet-4-6 — working (tier-3 wrapper)
  - Google AI Overviews — via Claude in Chrome (load via ToolSearch)

  Per-brief §4 (AI-search question mining) backfills via these surfaces inline. Any FAIL on §4 with a "surface unreachable" framing is a bug, not a legitimate gap.
  ```

- **Website-factory path check (v1.7).** If the engagement includes — or is expected to graduate to — a custom-site build (website-factory program), confirm a `seo-site-teardown` run exists for the client's strongest reference competitor (look for `<client-vault>/admin-extracts/competitor-research/<slug>-teardown/`). If absent, surface to the operator: "This client is on the custom-build path; the website-factory program requires a `seo-site-teardown` of the strongest reference site as the mandatory first step. Run it now (~6–12h, decomposable by pass) or schedule it as a parallel chat?" The teardown's reproduction blueprint is what the build phases consume; the Core 30 pipeline below does not block on it. Compose: `competitor-deep-research` for the landscape → `seo-site-teardown` on the one site to out-build.

- **Build-order cell verification.** Cross-check the cell count from `_build-order.md` against the (service × city) matrix the briefs imply. Surface mismatches.

- **Per-brief invocation (unchanged from v1.0).** For each kind of brief, check if it exists before producing it:
  - Service base briefs (`05_shared-intelligence/research-briefs/services/<service-slug>.md` — reuse if present, else `service-seo-research`)
  - City base briefs (`05_shared-intelligence/research-briefs/cities/<city-slug>.md` — reuse else `city-base-research`)
  - Intersection briefs (`05_shared-intelligence/research-briefs/intersections/<service-slug>--<city-slug>.md` — reuse else `intersection-research`)
  - Client-fact brief (`05_shared-intelligence/research-briefs/clients/<client-slug>/brief.md` — reuse else `client-fact-research`)

  One at a time for service/city/client briefs; intersection briefs can batch but surface total count to operator first.

**Operator gate:** before kicking off any new research, summarize: "I need to run N new briefs (<counts>). Reusing M existing briefs. Total estimated time: <minutes>. Proceed?"

**Output:** all briefs present on disk. `research_status` updated in state.

**Quality loop:** four-substep contract PER BRIEF (not per step). Each brief gets its own Mode 1 → Mode 4 → Mode 5 cycle as it lands.
- Mode 1 routes to "research brief" spec sources.
- Mode 4 backfills §4 (AI-search question mining) inline via Sonar/OpenAI/Gemini/Claude — the canonical path for any §4 gap. **"Cowork can't reach this surface" is never legitimate §4 gap framing.**
- Mode 5 PASS threshold: 85.
- Per-brief auto-invoke block emitted per brief as it lands.
- A brief that stalls at 3 iterations FAIL → hard escalation; orchestrator continues with the next brief (don't block the whole step).

```markdown
## Auto-invoke output-quality-loop

This step produced (per brief; one block emitted per brief landing):
- `~/workspace/second-brain/05_shared-intelligence/research-briefs/services/<service>.md`
- `~/workspace/second-brain/05_shared-intelligence/research-briefs/cities/<city>.md`
- `~/workspace/second-brain/05_shared-intelligence/research-briefs/intersections/<service>--<city>.md`
- `~/workspace/second-brain/05_shared-intelligence/research-briefs/clients/<client>/brief.md`

[output-quality-loop:eval] — see "Per-step quality loop contract" section.
```

**Failure modes:**
- A research sub-skill fails → mark step in-progress, log to `failures`, stop. Don't move on with a missing brief.
- Operator wants to defer some research → respect that; only cells with briefs scaffold downstream.
- Mode 4 returns Sonar refusal → escalate to operator, don't degrade to vault-internal-only research. Per memory `feedback_consult_reference_memories_before_infrastructure_claims`, verify the surface IS unreachable via direct probe before declaring it so.

### Step 3 — Author data files

**Input:** all briefs from Step 2.

**Action:** run the Phase 3 scaffolders in order.
- `scaffold-client-data.py --brief <client-fact-brief-path> --client-slug <slug>`. Do not pass `--tier3-template-out` to a tier-3 path unless operator explicitly confirms (per memory `feedback_never_propose_overwrite_tier3` — can't read tier-3 to verify it's empty).
- `scaffold-service-data.py --brief <service-brief-path> --output-slug <service-slug>` once per confirmed service.
- `scaffold-city-data.py --city-brief <city-brief-path> --intersection-briefs <comma-separated-service-slugs> --output-slug <city-slug> --client-slug <slug>` once per confirmed city.

Capture each script's stdout summary into the execution log.

**Operator gate:** after all three scaffolders run, surface: "Data files written. FILL placeholders: <list>. Credentials checklist: <list>." Wait for operator to confirm credentials in tier-3 OR fill critical FILL fields OR explicitly defer.

**Output:** `data/client-<slug>.json` + `data/services/*.json` + `data/cities/*.json` all present.

**Quality loop:** four-substep contract PER FILE (one Mode 1 call per scaffolded JSON).
- Mode 1 routes to "Scaffolded service/city/client JSON" entry in `output-quality-loop`'s spec-routing table. Spec sources: source brief + canonical reference JSONs (panel-upgrade.json for services; EV city JSON for cities; EV client JSON for clients) + JSON schema validity.
- Mode 4 elevates via cross-brief consistency checks ("service.json's claims field references brand_voice from client.json — present? matching tone?").
- Mode 5 PASS threshold: 90 (data files are schema-validity-sensitive).

```markdown
## Auto-invoke output-quality-loop

This step produced:
- `~/workspace/repos/ai-agency-core/scripts/data/client-<slug>.json`
- `~/workspace/repos/ai-agency-core/scripts/data/services/<service>.json` (one per confirmed service)
- `~/workspace/repos/ai-agency-core/scripts/data/cities/<city>.json` (one per confirmed city)

[output-quality-loop:eval] — see "Per-step quality loop contract" section.
```

**Failure modes:**
- A scaffolder refuses to overwrite an existing data file → respect non-destructive default. Surface `.scaffolded.json` sibling, ask operator to diff manually.
- A brief is malformed → stop, surface missing fields, let operator fix the brief.

### Step 4 — Verify WP REST API access + GSC credential pre-flight

**No quality loop** — verification step. The script's PASS / FAIL output IS the gate. See "Per-step quality loop contract" § "Protocol / verification steps" for the rationale.

**Input:** scaffolded `<slug>.config.example.json` from Step 3.

**Action:**
- Confirm `WP_APP_PASSWORD` is set in the operator's shell environment. If not, surface the export command + tier-3 vault location.
- Run `scaffold-client-data.py --client-slug <slug> --test-wp-auth --config <slug>.config.example.json`.
- Verify the script reports `✓ User has full Core-30 publishing capability.`
- **(ORCH-1) GSC credential pre-flight.** If the client config has `gsc_indexing: true`, run the credential pre-flight NOW — at Step 4, not at Step 8 when each page's indexing silently fails. Two paths:
  - **Standalone check:** `python publish-core-30-page.py --check-credentials`. Returns PASS/FAIL + actionable fix command. No page folder needed.
  - **Inline with first publish:** pass `--preflight-credentials` to the first `publish-core-30-page.py` invocation at Step 8. The script checks credentials before any page work and exits early on failure.
  - If the pre-flight fails, surface: "GSC credentials not configured. Run `gcloud auth application-default login --scopes=https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/indexing` before proceeding to Step 8. Publishing will work without indexing, but you'll need to submit URLs manually."
  - This check is generic — it verifies ADC for the Indexing API, not any client-specific credential.

**Operator gate:** none if both WP auth and GSC pre-flight succeed. If either fails, surface the exact error + canonical fix. GSC failure is a warning, not a hard block — publishing works without indexing.

**Output:** Step 4 marked done in state.

**Failure modes:**
- WP auth fails → stop. Refuses to proceed to Step 5. Bulk scaffolding 30 pages then discovering auth doesn't work is a footgun.
- GSC pre-flight fails → warn but allow proceeding. Mark `gsc_preflight: "failed"` in state so Step 8 knows indexing will fail. The operator can fix credentials between Step 4 and Step 8.

### Step 5 — Bulk scaffold

**Input:** populated data files + `_build-order.md` for the client.

**Action:**
- Verify `_build-order.md` exists at `04_projects/clients/_active/<slug>/website-archive/new/core-30/_build-order.md`. If absent, surface options.
- Confirm `GOOGLE_MAPS_EMBED_API_KEY` is exported. If not, surface export command + tier-3 location.
- Run `bulk-scaffold-pages.py --client <slug> --positions <range> --dry-run` first. Show operator what would scaffold.
- After operator confirmation, run for real with `--skip-existing`.

**Operator gate:** before real run, confirm position range. "I see N pages in build order. Scaffold positions 1-N now, or pick a subset?"

**Output:** per-page folders under `04_projects/clients/_active/<slug>/website-archive/new/core-30/<NN>-<page-slug>/` with `draft-v1.md` + `draft-v1-WP-WRAPPED.html`. State updated with each page's `scaffolded: true`.

**Quality loop:** four-substep contract PER PAGE (one Mode 1 call per scaffolded HTML).
- Mode 1 routes to "Core 30 page draft" spec sources (existing entry; no v1.1 edit needed).
- Mode 4 elevates via `competitor-deep-research` for SERP-level comparison (composes per output-quality-loop's Phase 4 rule).
- Mode 5 PASS threshold: 95 (strictest tier; pages are the production artifact).
- A page that escalates pauses Step 8 publish for that page only — other pages continue.

```markdown
## Auto-invoke output-quality-loop

This step produced (per page; one block emitted per page landing):
- `~/workspace/second-brain/04_projects/clients/_active/<slug>/website-archive/new/core-30/<NN>-<page-slug>/draft-v1-WP-WRAPPED.html`

[output-quality-loop:eval] — see "Per-step quality loop contract" section.
```

**Failure modes:**
- Any individual page fails (missing data file, malformed slug) → `bulk-scaffold-pages.py` continues + reports at end. Capture into `failures`. Surface to operator; don't auto-retry.

### Step 6 — Imagery prompts

**Input:** scaffolded page folders from Step 5.

**Action:** for each scaffolded page, run `generate-imagery-prompts.py --page-folder <path> --client <slug> --hero-style <style>` where `<style>` is one of `ahmad-centric` (default — owner performing the task), `service-scene` (the installed result / work scene, no face), or `hands-only` (faceless worker's hands at the task). The operator chooses the hero style per page or per service at the Step 6 operator gate; the default is `ahmad-centric` for backward compatibility.

Each generated prompt carries a **self-documenting header** (per Issue #17 from `execution-log-2026-06-03-core-30-pages-06-12-dataforseo-run`):
- **Type:** PURE SCENE / HANDS-ONLY / AHMAD-CENTRIC
- **Reference photos to upload:** NONE / logo-only / headshot+logo (keyed to the type)
- **Aspect ratio**
- **Produces:** one-line description

The generated log also includes a types-legend and the save/name/organize flow so the operator never guesses what to upload or where files go.

**Reference photos** are sourced from `04_projects/clients/_active/<client>/marketing-assets/reference-photos/` per `_meta/conventions.md` § "Client imagery reference assets." The prompt headers name which files to pull from that folder. If the folder is missing or empty, Step 6 surfaces the gap before generating prompts.

**About-portrait reuse:** when `generate-imagery-prompts.py` detects a keeper About portrait already exists for the same city (via its prior-log scanning / learning loop), it marks the About prompt with a REUSE NOTE. The operator can skip the Higgsfield run for that slot.

**Embroidered-no-patch wardrobe (Issue #20):** any prompt that may show the uniform (AHMAD-CENTRIC always; HANDS-ONLY when chest/shoulder may render) carries the embroidered-no-patch clause: "embroidered directly onto the fabric — yellow-gold lightbulb + navy 'EV ELECTRIC', no patch, no white background." The generator NEVER instructs uploading the uniform mockup (its white callout boxes cause white name-patches).

Aggregate into `04_projects/clients/_active/<slug>/_state/imagery-prompt-summary.md` listing per-page: slug + position + hero type + hero/about/scene prompts + reference photo requirements.

**Operator gate:** surface summary path + per-page hero-style choices + one-line briefing. The operator can adjust hero styles per page before proceeding to Higgsfield.

**Output:** all `imagery-prompts-log.md` written. Aggregate summary written. Step 6 marked done.

**Quality loop:** four-substep contract PER PAGE on each `imagery-prompts-log.md` + ONE call on the aggregate summary.
- Mode 1 routes to new "Imagery-prompt log" entry in spec-routing table. Spec sources: `sop-ai-imagery-for-core-30-pages.md` + page's data file (verifies reference photo URLs threaded correctly).
- Mode 4 elevates by checking prompts against current Higgsfield prompt-craft best practices.
- Mode 5 PASS threshold: 80.

```markdown
## Auto-invoke output-quality-loop

This step produced:
- `~/workspace/second-brain/04_projects/clients/_active/<slug>/website-archive/new/core-30/<NN>-<page-slug>/imagery-prompts-log.md` (one per page)
- `~/workspace/second-brain/04_projects/clients/_active/<slug>/_state/imagery-prompt-summary.md` (aggregate)

[output-quality-loop:eval] — see "Per-step quality loop contract" section.
```

**Failure modes:**
- `generate-imagery-prompts.py` fails for one page → continue with others, capture failure. Operator can hand-write that page's prompts.

### Step 7 — Pause point (Higgsfield)

**No quality loop** — wait state. See "Per-step quality loop contract" § "Protocol / verification steps".

**Action:** skill writes state with `current_step: "step-7-pause-higgsfield"` + `step-7-pause-higgsfield: "in-progress"`. Then stops.

Last message before stopping:

```
**Paused at Higgsfield gate.**

Imagery prompts written (auto-generated by generate-imagery-prompts.py). Open:
- Aggregate summary: <filepath>
- Per-page logs: each <page-folder>/imagery-prompts-log.md

Each prompt has a self-documenting header telling you:
- TYPE (PURE SCENE / HANDS-ONLY / AHMAD-CENTRIC)
- REFERENCE PHOTOS to upload (NONE / logo-only / headshot+logo)
- ASPECT RATIO to set in Higgsfield
- What it PRODUCES (one-line)

Reference photos to upload are at: <client>/marketing-assets/reference-photos/

Generate 4 variants in Higgsfield for each prompt. When a page's downloads are ready, tell me:
"images are in for <page-slug>" (or "images are in for all pages")

I'll ask you to pick the best variant per slot (the only human-judgment step), then handle organize → wire → publish automatically.

You can close this chat — state is saved at `<state-file-path>`.
```

The skill does NOT keep checking the staging folder or polling. It waits for the operator's next message.

### Step 8 — Resume per page

**Trigger:** operator says "images are in for <page-slug>" or "for all pages" or "process page <N>".

**Action per page:**
1. **Variant-selection gate (operator decision via gate file).** Write a gate row to `_pending-operator-decisions.md` per [[operator-gate-routing]]: "Pick the best variant per slot for <page-slug>: hero (1-N), about (1-N or REUSE from <city-keeper>), scene (1-N or SKIP)." Wait for the operator's variant picks before proceeding. When processing multiple pages in batch ("process all the rest"), write all gate rows at once; the operator can respond with all picks in one message.
   **For same-service multi-page batches** (e.g., ev-charger for pages 03+09): surface that distinct variants should be picked per page for SEO uniqueness. If the operator generated one batch for multiple pages, recommend option (a) generate a fresh batch per page, or (b) organize into the first page then copy an alternate to the second page (per `organize-image-downloads.py` `--copy-to` mode or manual copy — see Issue #19).
2. **Organize.** Run `organize-image-downloads.py --client <slug> --page-folder <path> --image-type hero --selected-variant <N>`. Once per slot type. For multi-page sharing from a single batch, use `--copy-to <second-page-folder>` to copy a chosen alternate without consuming staging files.
3. **Wire.** Run `wire-page-images.py --page-folder <path> --config <config-path>`. Optimizes keeper PNG, uploads to WP, rewrites HTML, re-publishes. (`wire-page-images.py` enforces template-parity before wiring — refuses if the page lacks the current image-integration CSS. If refused, re-scaffold to current template first.)
4. **Live-rendered, cache-busted verification (convention-class — SOP prose, not deterministic code).** After publish, fetch the LIVE published URL with a cache-buster (`?v=<timestamp>`) and verify:
   - `modified_time` advanced past the prior value (confirms WP actually updated the page).
   - H1 matches the expected eyebrow + clean-H1 form (not a combined serif H1 or stale content).
   - Title visibility: the WP page title is hidden (no duplicate theme title above the hero).
   - Font family: the page renders in sans-serif via `.evp-corepage` styling (serif fallback = the style wrapper didn't survive upload — fail).
   - Image fill: hero + about images fill their containers edge-to-edge (no dashed border / blue frame / placeholder chrome).
   - Map fill: Google Maps embed fills its container (not undersized / not a placeholder).
   - Zero placeholder text: no `[…placeholder…]`, `<!-- MISSING -->`, `{tokens}`, `FILL:`, or `TBD` visible on the rendered page.
   - Compare RENDERED structure to a named known-good sibling page (e.g., page 07 for McLean pages, page 04 for Fairfax pages). A grep of `post_content` HTML is NOT acceptance — it cannot detect serif fallback, a duplicate theme title, or old-vs-new content structure.
   **If any check fails, do NOT proceed to indexing. Surface the failure to the operator with the specific finding.**
   **Enforcement note:** this check is convention-class (SOP prose guiding the orchestrator's behavior, not a deterministic script gate). Same honest-limitation framing as the Phase 5B schema-auto-bump fix — it documents the rule but relies on the LLM-orchestrator following it. A deterministic live-verification script is a future hardening candidate.
5. **Cache-purge + incognito re-check (convention-class — SOP prose, not deterministic code).** After verifying the logged-in render, purge the page cache (LiteSpeed Cache → Purge this page, or equivalent CDN purge) and re-fetch the public URL logged-out / cache-busted (`?v=<new-timestamp>`) to confirm anonymous visitors + Googlebot get the new version. A stale cached snapshot at the canonical URL means real visitors see the old page until cache expires.
   - If the cache-busted anonymous fetch returns different content than the logged-in render, the page cache is stale — purge again + wait + re-check.
   - If a `web_fetch` / tool-fetch conflicts with an operator screenshot, treat it as a **cache question first**, not a "the other agent lied" conclusion. Never override direct operator visual evidence with a single anonymous tool fetch.
   **Enforcement note:** convention-class, same as substep 4.
6. **Update state.** `page_status[<slug>].imagery_keepers_picked: true`, `wired: true`, `published: true`, `live_verified: true`. Update execution log.
7. **Indexing.** If `gsc_service_account_path` is configured, `wire-page-images.py → publish-core-30-page.py` auto-submits to GSC Indexing API. Confirm in script's stdout. Mark `indexed: true`. Only fires AFTER substep 4 passes — never submit an unverified page to GSC.

**Operator gate:** after each page completes, surface live URL + indexing status. Confirm before next page (or "process all the rest" to batch).

**Quality loop:** four-substep contract PER PAGE post-publish.
- After `wire-page-images.py → publish-core-30-page.py` completes, Mode 1 fires on the on-disk post-wire HTML (`<page-folder>/draft-vN-WP-WRAPPED.html` — highest-N version on disk; the publish flow already wrote the updated file).
- Routes to "Core 30 page draft" spec sources (same as Step 5; re-evaluates post-imagery).
- Mode 4 elevates via `competitor-deep-research` for SERP comparison post-publish.
- Mode 5 PASS threshold: 95.
- Mode 5 escalation → mark `page_status[<slug>].quality_verdict: <verdict>` in state; DO NOT auto-revert the publish — operator decides whether to unpublish, edit-in-place, or accept.

```markdown
## Auto-invoke output-quality-loop

This step produced (per page):
- `~/workspace/second-brain/04_projects/clients/_active/<slug>/website-archive/new/core-30/<NN>-<page-slug>/draft-vN-WP-WRAPPED.html` (highest N on disk; the publish flow's output)

[output-quality-loop:eval] — see "Per-step quality loop contract" section.
```

**Failure modes:**
- `organize-image-downloads.py` fails → ask operator to re-check Higgsfield downloads folder.
- `wire-page-images.py` refuses with template-parity error → page is on a stale template. Re-scaffold to the current template (carries image-integration CSS + maps embed) before retrying. See Issue #27.
- `wire-page-images.py` fails on upload → capture into `failures`, mark `wired: false`, keep going if operator confirms.
- `publish-core-30-page.py` fails (placeholder hard-block) → fix the draft (remove placeholder text / MISSING comments / unrendered tokens), then re-run. See Issues #15/#24/#26.
- `publish-core-30-page.py` fails (disk sync refusal) → the on-disk draft changed between validation and publish. Re-run from the current disk version.
- Live-rendered verification fails (substep 4) → do NOT proceed to indexing. Surface the specific failure to the operator. Common causes: stale page cache (purge + re-check), old content still live (REST push didn't render — check if page is Elementor-built), template style wrapper not applying (serif font visible).
- Cache-purge re-check shows stale content (substep 5) → purge again, wait, re-check. If persistent, check CDN/LiteSpeed cache settings.
- GSC indexing fails → never blocks publish. Capture, surface at Step 11.

**Publish-depends-on-imagery guard (v1.2, Issue #15).** Step 8 (imagery wiring) must complete for a page BEFORE that page proceeds to publish in any downstream wave. If a page reaches a publish wave with dangling placeholder image references (`*-PLACEHOLDER.png` filenames, `[…placeholder…]` text, or `<!-- MISSING -->` comments in the hero/about slots), the publish script must refuse that page. The only bypass is an explicit operator-approved "publish without images" decision routed through `_pending-operator-decisions.md` — this is never a silent default. When the operator approves publish-without-images, the decision must be matched to the existing imageless-page pattern (consistent with already-live pages that also lack images) — never a one-off that creates inconsistency. This guard closes the gap where EV pages 06-12 almost shipped with 404-returning placeholder image URLs (Issue #15).

### Step 9 — Indexing pass

**No quality loop** — confirmation pass over state. See "Per-step quality loop contract" § "Protocol / verification steps".

In steady state, indexing happens inline during Step 8. Step 9 exists as an explicit gate to:
1. Confirm every published page has an indexing record (`page_status[*].indexed == true`).
2. For any page where indexing failed/skipped, surface manual fallback: "GSC → URL Inspection → request indexing." List URLs.

**Run the post-build discovery checklist — `[[sop-page-indexing-and-discovery]]`.** After a wave is live + verified,
indexing-record confirmation alone is not enough; run the discovery sequence: (a) **sitemap fresh in GSC** —
confirm the new URLs are in the live sitemap AND that GSC's "Last read" is recent; if Last read predates the batch,
**re-submit the sitemap** (Domain property needs the FULL URL) to force a fresh read; remove any bogus
page-as-sitemap entries; (b) **internal-linked** — pages reachable from hubs/nav (the `hub-and-nav-build`
deliverable); (c) **Request-Index priority pages manually** — hubs first, then top-demand city leaves, ~10–12/day
per property (multi-day for big batches → schedule it); (d) kick off **authority signals** (`[[sop-gbp-posting-cadence]]`);
(e) **~2 weeks later** check GSC → Pages for "Crawled – currently not indexed" (= thin/near-dup → differentiate, not
re-submit). **Automation reality (so we don't chase it):** the Indexing-API ping in `publish-core-30-page.py` is
off-label for normal pages (JobPosting/BroadcastEvent only) and unreliable; **GSC "Request Indexing" has NO API and
must stay manual** (don't browser-automate the GSC UI — ToS-gray, brittle, quota-capped). The legit automatable
levers (sitemap + internal linking) are already in the pipeline. Full detail + the options table:
`[[sop-page-indexing-and-discovery]]`.

**Operator gate:** surface indexing status list + the discovery-checklist state. Wait for operator to resolve manual ones or explicitly defer.

**Output:** state updated. Step 9 marked done.

### Step 10 — Internal-link pass + dead-link audit

This step uses two Phase-4b scripts in `repos/ai-agency-core/scripts/`.

**10a. Propose internal links across the corpus.**

```bash
python3 insert-internal-links.py \
  --corpus-root <client-corpus-root> \
  --reference-architecture <link-map-synthesis-path> \
  --build-order <build-order-path> \
  --mode data-driven
```

Writes per-page `_internal-link-proposals-YYYY-MM-DD.md` + `.json` to each page folder.

If link-map synthesis at `05_shared-intelligence/research-briefs/link-maps/_synthesis-<client>.md` doesn't exist, surface to operator. Options: (a) defer link pass until synthesis produced (via `competitor-deep-research` link-map mode), or (b) run `--mode data-driven` only.

**10b. Operator review.** Surface per-page proposal markdown files.

**10c. Apply approved diffs.** Run `insert-internal-links.py` per page with `--apply --diff-file <approved-json-path>`. Each apply writes `draft-vN+1-WP-WRAPPED.html` alongside the old one — non-destructive.

**10d. Republish updated drafts.** For each page where links inserted, `publish-core-30-page.py --page-folder <path> --config <config> --version vN+1`.

**10e. Dead-link audit.**

```bash
python3 audit-published-links.py --corpus-root <client-corpus-root>
```

Read-only. Reports any internal link whose destination doesn't exist as a `NN-<slug>/` folder. Output at `<corpus-root>/_dead-link-audit-YYYY-MM-DD.md`.

Surface audit "By destination" view to operator. Top entries are highest-leverage build-next candidates.

**Operator gate:** after audit, surface: "Audit complete. <N> dead links across <M> pages, biggest cluster is `<dest-slug>` referenced by <K> pages. Want to flag any for the build-next backlog?"

**Quality loop:** four-substep contract on the link-proposal artifacts + dead-link-audit report.
- Mode 1 routes to new "Internal-link proposals" + "Dead-link audit" entries in spec-routing table. Spec sources: `insert-internal-links.py` README + link-map synthesis (if present).
- Mode 4 elevates link proposals via `competitor-deep-research` comparison.
- Mode 5 PASS threshold: 85.

```markdown
## Auto-invoke output-quality-loop

This step produced:
- `<page-folder>/_internal-link-proposals-YYYY-MM-DD.md` (one per page)
- `<corpus-root>/_dead-link-audit-YYYY-MM-DD.md`

[output-quality-loop:eval] — see "Per-step quality loop contract" section.
```

**Failure modes:**
- `insert-internal-links.py` fails on a page → capture, continue with others.
- `audit-published-links.py` fails → check `--corpus-root` is correct.

### Step 11 — Final report

**Action:** compile a single summary message:
- **Pages live.** Bullet list of `<page-slug>: <live-url>`.
- **Indexing status.** Per-page: submitted / pending / failed.
- **Internal links inserted.** Total + per-axis breakdown.
- **Dead links remaining.** Total + top 3 build-next candidates.
- **Quality-loop summary.** Per-step verdict distribution + escalation count.
- **What still needs operator follow-up.** From `failures` + deferred items + unfilled FILL prose.
- **Suggested next steps.** From client-fact brief: analytics setup, GBP optimization, citation cleanup, social profile alignment.

Write report to `04_projects/clients/_active/<slug>/onboarding-report-YYYY-MM-DD.md`. Surface filepath + short in-chat summary.

**State:** mark `current_step: "done"` and `step-11-report: "done"`. State file stays — canonical record.

**Quality loop:** four-substep contract on the report (one Mode 1 call).
- Mode 1 routes to new "Onboarding final report" entry in spec-routing table. Spec sources: this SKILL.md + the run's state file (verifies report accurately reflects state).
- Mode 4 typically returns "validates" on most gaps — final reports are summaries, not novel claims.
- Mode 5 PASS threshold: 85.
- This is the AGGREGATE quality-loop pass for the run — prior steps already evaluated their own artifacts.

```markdown
## Auto-invoke output-quality-loop

This step produced:
- `~/workspace/second-brain/04_projects/clients/_active/<slug>/onboarding-report-YYYY-MM-DD.md`

[output-quality-loop:eval] — see "Per-step quality loop contract" section.
```

## Closing Protocol (multi-chat resume contract)

At wave-close, every chat runs these steps before declaring done:

1. **Update state.** Write `waves[<current_wave>].status: closed` + `closed_at: <UTC>` + `outputs: [<paths>]`. Append a `wave_log` entry with `summary`, `key_artifacts`, `spawned_handoffs`, `verdict_summary`. Update `planned_remaining_waves` (remove the just-closed wave; recompute estimates if needed). Clear `current_wave`.

2. **Append event-log row** via `append_event_log.sh` summarizing the wave close (artifact count + verdict distribution + spawned handoffs).

3. **Spawn the next wave's handoff** if `planned_remaining_waves` is non-empty. Use the substrate-tagged handoff shape per vault-orchestrator's PROVISION mode. The handoff's Opening Protocol will read `wave_log[<prior_wave>]` for context.

4. **Operator gate.** Surface: "Wave <id> closed. Outputs: <list>. Next wave: <id> (<scope>). Spawn now or pause?"

The wave-N → wave-(N+1) flow:
- Wave-N writes `wave_log` at close.
- Wave-(N+1) reads `wave_log` at Opening Protocol; plan-bullet opening reflects "resuming from wave (N+1), prior wave outputs are <list>."
- Operator never has to manually wire up "what's done so far" between waves.

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

The Phase 2 research skills (`service-seo-research`, `city-base-research`, `intersection-research`, `client-fact-research`) are invoked at Step 2 via skill chaining, not as scripts.

## Failure-mode reference card

Every step has a "stop and surface, don't silently continue" contract. Concretely:

- **Sub-script exits non-zero.** Capture stderr, write to execution log + state's `failures` array, surface to operator, stop current step. Don't auto-retry.
- **Research brief is missing and operator deferred running it.** Skip the cells whose brief doesn't exist; scaffolding simply won't include those (service, city) pairs.
- **Data file has `FILL:` placeholders in mandatory fields.** Don't scaffold pages that use it until operator fills them.
- **Tier-3 vault path destination.** Never recommend `--overwrite` against `~/workspace/second-brain-tier3/...`. Skill can't read tier-3 to verify it's empty.
- **Operator wants to skip a step.** Allow it. Mark the step `skipped` (not `done`) in state, log rationale.
- **Mid-step interruption.** State file persists. On resume, in-progress step picks up from last sub-task (e.g., Step 8 resumes per-page from last completed page).
- **Quality-loop FAIL at 3-iteration stall.** Hard escalation per Mode 5; the failure is ALSO written to `failures` array (per state-schema § "failures vs quality_log semantic distinction"). The orchestrator pauses until operator decision.
- **Quality-loop NEEDS REVISION at iteration 1 or 2.** Normal revision cycle. NOT written to `failures`. The artifact regenerates via Mode 2's revision prompt.

## Plain-language enforcement

Every message the skill sends to the operator follows `second-brain/_meta/plain-language-conventions.md`:
- No jargon without inline gloss on first use.
- Short sentences. Active voice.
- Lists for sequences; prose for explanations.
- No emoji unless operator's last message had one.
- No filler ("Let me start by...", "I'll now...", "Great question.").

Every file the skill writes (state file content, execution log entries, report) also follows plain language.

## Plain-language gloss for the most common terms

Gloss inline on first mention in each new chat:

- WP REST API [WordPress's built-in API for creating and updating pages without logging in]
- Tier-3 vault [the air-gapped credentials folder at `~/workspace/second-brain-tier3/` that the skill cannot read]
- Higgsfield [an AI image generator that takes a face-reference photo and produces consistent shots of that person in different scenes]
- GSC [Google Search Console — Google's tool for monitoring how a site appears in search results]
- Core 30 [a Keelworks methodology — building 30 service-by-city pages per client as the foundation of local SEO]
- Tier-1 / Tier-2 / Tier-3 brief [in the three-tier research model: T1 = service across all cities, T2 = city across all services, T3 = one specific (service, city) pair]
- output-quality-loop [the per-artifact quality-evaluation skill the orchestrator routes every artifact through; Modes 1-5 evaluate + revise + research + decide]

## Robustness rules

- **Scope-estimation gate is mandatory.** Every fresh invocation. The plan-bullet opening reflects its output.
- **Plan-bullet opening is mandatory.** Every fresh invocation. Every resume.
- **State file write is atomic.** Write to temp file, then rename. Never half-write.
- **Per-page granularity in Step 8.** Don't batch state writes; each completed page flips its own `page_status` entry immediately.
- **Per-artifact granularity in `quality_log`.** Each artifact's Mode 1-5 cycle writes its own entry.
- **Read state at the start of every operator message in mid-run.** The operator may have edited state by hand to override the skill's state (especially `planned_remaining_waves`, `blocked_on`, or a `quality_log` decision).
- **Never call a sub-skill that has `status: in-progress` from a prior chat without confirming with the operator first.** Research sub-skills sometimes leave half-written briefs; honor those.
- **Never silently skip the quality loop.** If output-quality-loop is unreachable, surface the gap; wait for operator decision.

## Testing this skill

First real test target is **S&H Contracting wave A2** (per the v1.1 ship + the queued S&H wave A2 handoff). Reasons:

- S&H state file already exists from wave A1 (2026-06-01); tests resume + multi-chat decomposition.
- Both API keys + event log Phase 1 + v1.1 land together — tests the per-step quality loop with all four AI surfaces working.
- Wave A2 scope is bounded (2 service briefs) — fits in a single Cowork chat.

After the S&H wave A2 run, capture lessons into `lesson-client-seo-onboarding-v1.1-wave-a2.md` (separate from this rewrite's lesson file).

## Output-quality-loop integration (rewritten for v1.1)

Per the canonical convention at `~/workspace/skills/output-quality-loop/references/auto-invoke-convention.md` (made universal by Phase 5 of the output-quality-loop project, 2026-05-28), every artifact-producing skill emits the auto-invoke block at the end of its closing protocol.

**v1.1 contract for this orchestrator (rewritten from v1.0):** The orchestrator does NOT delegate quality-loop responsibility to sub-skills. v1.0 said "sub-skills emit their own auto-invoke blocks; the orchestrator does not re-evaluate their artifacts." That was the bug — sub-skill auto-invoke blocks are conceptual until something actually runs them.

v1.1 says the orchestrator routes EVERY artifact through `output-quality-loop` per-step, per the "Per-step quality loop contract" section above. The four-substep contract (Produce → Auto-evaluate → Auto-elevate → Auto-decide) fires after each artifact lands; the orchestrator does the invocation; sub-skill auto-invoke blocks are now belt-and-suspenders rather than the primary mechanism.

**The per-step block format** is documented in each step's `Quality loop:` subsection. Step 11's final-report block aggregates the run rather than newly evaluating prior artifacts.

**Operator bypass.** Honors `--bypass-quality-loop` (or "skip the quality loop") in the original onboarding request. The skill still produces all artifacts; just skips the Mode 1-5 invocations and writes a bypass entry to each relevant `_quality-log.md`. Per-artifact bypass also supported via `--skip-quality-loop-this-artifact <path>`.

## Peer-reviewer dispatch (v1.4) — autonomous gate review

> **v1.4 changelog (2026-06-05, Build wave 4)** — gate-peer-reviewer v2 integration. After each artifact-producing step's quality-loop exit, the orchestrator spawns the peer-reviewer as a Task sub-agent. The peer-reviewer runs the registered Check 1 satisfaction targets for that gate type (named procedures: full-placeholder-family-sweep, source-client-leak-audit, live-rendered-cache-busted-verification) + Checks 2-5 (when applicable) + Check 6 (closing gates only). Returns a structured JSON verdict the orchestrator inlines alongside the gate output for operator review. Operator sees one combined surface (gate output + peer-review verdict) and approves with one action. No more manual paste-transport between chats.

**Dispatch shape.** ONE additive block per artifact-producing step, inserted AFTER the quality-loop exit and BEFORE the operator gate. Concrete integration points:

| Step | Gate type | Dispatch fires after | Operator sees |
|---|---|---|---|
| 3 — Author data files | G-data | Quality-loop four-substep exit on all JSONs | Data files + peer-review verdict |
| 5 — Bulk scaffold | G-scaffold | Quality-loop four-substep exit on all pages | Scaffolded pages + peer-review verdict |
| 6 — Imagery prompts | G-imagery | Quality-loop four-substep exit on all logs | Imagery prompts + peer-review verdict |
| 8 — Resume per page | G-publish | Substep 3 (wire) completes, before substep 4 | Published page + peer-review verdict |
| 11 / Closing Protocol | G-wave-close | Wave close state writes complete | Wave-close summary + KCA peer-review |

**Per-gate dispatch block (Claude Code substrate):**

```
## Peer-reviewer dispatch

Gate type: <G-data | G-scaffold | G-imagery | G-publish | G-wave-close>
Orchestrator: client-seo-onboarding
Project: <client-slug>
Wave: <current_wave>

Context paths for the Task sub-agent:
- Gate output: <the artifact(s) just produced — file paths or inline text>
- Gate-type registry: ~/workspace/skills/gate-peer-reviewer/references/gate-type-registry.md
- Check spec: ~/workspace/skills/gate-peer-reviewer/references/check-spec.md
- State file: ~/workspace/second-brain/04_projects/clients/_active/<slug>/_state/onboarding.json
- Build-order: ~/workspace/second-brain/04_projects/clients/_active/<slug>/website-archive/new/core-30/_build-order.md
- Client JSON: ~/workspace/repos/ai-agency-core/scripts/data/client-<slug>.json
- Service JSONs: ~/workspace/repos/ai-agency-core/scripts/data/services/<slug>/ (client-override dir) + shared
- Lesson files: ~/workspace/second-brain/05_shared-intelligence/lessons/ (most recent for this client)

Task instruction: Read the gate-type registry entry for <gate_id>. Run Check 1 satisfaction targets
(including all named procedures listed). Run Checks 2-5 per check-spec.md skip logic. If closing gate,
run Check 6. Return the structured JSON verdict per references/return-contract.md.
```

**What the orchestrator does with the verdict:**

- `APPROVE` → proceed to operator gate (operator sees gate output + "Peer review: APPROVED").
- `APPROVE-WITH-NOTES` → proceed to operator gate with notes inlined (operator decides on notes).
- `REJECT-AND-REDO` → DO NOT surface to operator. Fix the catch, re-run the step, re-dispatch peer-reviewer. Cap at 2 peer-review iterations per gate; on 3rd REJECT, escalate to operator with full catch history.
- `ESCALATE-AMBIGUOUS` → surface to operator with the peer-reviewer's ambiguity framing; operator decides.

**Graceful degradation.** If the Task sub-agent fails (peer-reviewer skill unavailable, context too large, timeout), the orchestrator logs a `peer-reviewer-skipped` row to `_meta/_event-log.md` per the graceful-degradation format in gate-peer-reviewer SKILL.md and proceeds to the operator gate WITHOUT peer review. The operator sees the gate output alone + a note that peer review was skipped with the reason. Skipping is acceptable as long as it's tracked; silently dropping the review step is not.

**Steps that do NOT dispatch the peer-reviewer:**

| Step | Why |
|---|---|
| 1 — Ingest | Extraction, not a template-derived artifact; low leak/placeholder risk |
| 2 — Research briefs | Research-brief gates are vault-orchestrator territory (Mode 6); this orchestrator delegates research to sub-skills |
| 4 — Verify WP REST API | Verification step; no artifact to review |
| 7 — Pause (Higgsfield) | Wait state; no artifact |
| 9 — Indexing confirmation | State-based cross-check; no artifact |
| 10 — Internal-link pass | Link proposals are low-risk for source-client leaks + have their own quality loop |

## Related

- [[client-seo-onboarding-automation]] — the parent blueprint; Phase 5 spec
- [[state-schema]] — full JSON schema for the state file (sibling to this SKILL.md)
- [[per-artifact-sizing]] — canonical per-artifact minute table (sibling; new in v1.1)
- [[references/ai-surface-reachability-matrix]] — AI-surface reachability mirror (sibling; new in v1.1)
- [[sop-core-30-page-build]] — the per-page operator SOP this skill ultimately wraps
- [[sop-ai-imagery-for-core-30-pages]] — the imagery SOP wrapped by Step 6-8
- [[sop-wordpress-rest-api-deploy]] — the WP publish SOP wrapped by Step 8
- [[vis-extraction]] — orchestrator-skill pattern reference; state + pause + resume conventions adapted from there
- [[plain-language-conventions]] — language enforcement across every output
- [[../output-quality-loop/SKILL|output-quality-loop SKILL.md]] — the per-step quality contract's underlying skill
- [[../../second-brain/05_shared-intelligence/patterns/pattern-orchestrator-multi-chat-decomposition|orchestrator multi-chat pattern]] — the architectural rationale
- [[../../second-brain/05_shared-intelligence/lessons/lesson-client-seo-onboarding-skill-first-real-run|first-real-run lesson file]] — the input to this v1.1 rewrite
- [[../../second-brain/05_shared-intelligence/lessons/lesson-client-seo-onboarding-v1.1-rewrite-2026-06-02|v1.1 rewrite lesson file]] — captured during this rewrite

## Decision archaeology

- 2026-06-01 [v1.0 written] — initial skill written by Cowork against the Phase 5 handoff. All Phase 2/3/4 prerequisites confirmed shipped (insert-internal-links.py + audit-published-links.py landed 2026-05-31 per Phase 4b close). State file design borrows the per-step + per-page granularity pattern from vis-extraction's Phase B work. Failure-mode contract is strict: any sub-script non-zero exits stops the orchestrator; never silently continues.

- 2026-06-03 [v1.2 — Phase 5B schema auto-bump] — added schema-version auto-bump-on-additive-write to `state-schema.md` (canonical `SCHEMA_FIELDS` registry + Write convention 9 + reconciliation of two contradictions that previously said additive writes need no bump). Closes the S&H silent-drift hole sweep [4] caught (D-04). **Key decision:** the Phase 5B handoff specified a Python pre-write hook (`write_state_with_schema_check` + `SchemaDriftError`) routed through "the skill's state-file writers" — but disk-verify found NO Python state writer exists; `onboarding.json` is LLM-written per this file's prose conventions. The handoff-as-written was REJECTED (would have built a Python pipeline nothing calls). Chose Path A (prose-convention fix matching the actual architecture); parked Path B (deterministic Python guard) as conditional on state writes becoming script-mediated. Honest tradeoff: Path A's enforcement is convention-class — same reliability class that drifted at sweep [4] — so it documents the rule + removes the contradiction but does not deterministically prevent a future drift. Lesson D-row + disk-verify-integration-target pattern PROMOTED at 2nd instance (cross-ref gate-peer-reviewer build D-11, the prior instance of the same handoff-vs-disk-architecture drift). **Post-close reconciliation (D-06):** an operator "are you sure?" verification caught that the `SCHEMA_FIELDS` registry — built from the documented schema — omitted `operator_decisions_pending`, a real field live on the S&H file; convention 9 would have refused S&H's next write. Added the field to both version sets + documented it + flagged "build the registry from disk, not the doc." The registry-build had itself fallen to the pattern it documents.

- 2026-06-02 [v1.1 rewrite] — three load-bearing architectural changes shipped against the S&H first-real-run lesson file. (1) Per-step output-quality-loop integration — the four-substep contract (Produce → Auto-evaluate → Auto-elevate → Auto-decide) fires after every artifact, not just at Step 11. (2) Multi-chat wave decomposition baked into plan-bullet opening — scope-estimation gate fires first, plan-bullet shows hours + chat count + waves. (3) AI-surface reachability matrix replaces "Cowork can't reach X" framing — Sonar + OpenAI + Gemini + Claude all working today via tier-3; AI Overviews via Chrome. Five smaller spec edits also landed: pre-flight handoff cross-check + build-order authoritative + multi-chat resume contract + AI-citation §4.5 updates + per-step auto-invoke blocks. Plus four new sibling files / additive edits: per-artifact-sizing.md, references/ai-surface-reachability-matrix.md, output-quality-loop's spec-routing-table.md (4 new entries), output-quality-loop's confidence-calibration.md (4 new threshold rows). State-schema extends v1.0 additively with `waves`, `wave_log`, `planned_remaining_waves`, `blocked_on`, `quality_log`, `current_wave` — v1.0 state files load cleanly. Event-log integration on verdict transitions makes per-step quality outcomes visible to parallel chats. Lesson file captured edge cases + non-obvious decisions during the rewrite.
