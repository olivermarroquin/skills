---
type: execution-log
status: complete
created: 2026-09-26
updated: 2026-09-26
venture: vis-extraction
tags: [execution-log, vis-extraction, second-squeeze, higgsfield, marketing, prompt-library, spec-gap]
---

## 2026-09-26 — VIS extraction + 4x second-squeeze: Nate Herk "Turn Claude Into a One Person Marketing Team"

**Source:** https://www.youtube.com/watch?v=yCACmFTiCto (Nate Herk | AI Automation, 2026-08-21, 38:28)
**Mode:** training (review gate closed 2026-09-26 under extraction-prompt v3.6; Phase 7 write completed same session)
**Chat:** Cowork, Oliver.

---

## What Was Done

### Phase 0-6 (initial extraction pass)

- Cache miss; ran `transcript-pull.sh` on the user's device. yt-dlp was missing entirely — installed via `pip install --user yt-dlp` (not in the skill's documented Phase 0a path since this ran on the desktop-bridge VM, not the cloud sandbox).
- `transcript-pull.sh`'s hardcoded `PYTHON_BIN="/opt/homebrew/bin/python3.12"` doesn't exist on this device (Linux VM, not macOS) — patched in place to `/usr/bin/python3` (backup kept: `transcript-pull.sh.pre-pythonfix.bak`). Needed because the device_bash bridge runs a Linux sandbox even though the connected folder is the user's Mac's `~/workspace`.
- First two pull attempts returned "no captions available" — yt-dlp's own `--write-auto-subs --sub-langs "en.*,en-orig"` combination was hitting **HTTP 429 (rate-limited)** on YouTube's caption endpoint, most likely from the request pattern (two-language wildcard) rather than genuine unavailability (manual `yt-dlp --list-subs` confirmed English auto-captions existed). Patched `sub-langs` from `"en.*,en-orig"` to `"en-orig,en"` — succeeded on next run. This is a standing script edit, not a one-off workaround; worth revisiting if a future pull hits 429 again with the narrower list.
- Full Phase 1 context-gathering completed: templates, conventions.md, current-goals.md (noted stale — last updated 2026-05-12, horizon 2026-05-31), scoring-rubric.md, active-project directory listings, AGENTS.md.
- Phase 3-5 analysis produced a draft covering: full workflow breakdown, tools mentioned, strategy extraction, replication potential, dedup-and-enhance decisions against `tool-higgsfield.md` and the Wealth Wisdom source, a pattern-promotion candidate flag for `tactic-grill-before-plan` (now 3/3 via Nate's "Grill Me" skill — cross-domain evidence, not just cross-creator).
- Presented Phase 6 review-gate summary. Held for approval per training-mode default (no writes to disk yet).

### Second squeeze — pass 1 (Hunt 1, fresh angles: money / names / corrections-hedges / timing-version)

- Number-check catch: auto-caption transcript literally reads "17.55 cents" for the sizzle-reel cost, but Nate's own follow-up comparison ("more than just 20 bucks") only makes sense if the real figure is **$17.55**. Filed with a confidence note rather than as verbatim.
- Names pass: Scroll World's author is credited on-screen as "Oso" — new attribution for the planned `tool-scroll-world.md`. Also flagged the Calendly logo demo as a throwaway UI example, not a real case study.
- Version-timing catch: source uses "Seedance 2.5" by name; `tool-higgsfield.md` documents "Seedance 2" throughout — a model-version bump the vault hadn't caught yet.
- Actionability-framing catch: Nate states outright he applied no ad-copy subject-matter expertise — meaning the demoed outputs are a floor, not a ceiling, which is a stronger case for Keelworks specifically (existing ad expertise the demo didn't use).
- Risk catch: a logo rendered slightly wrong on the sizzle reel — first mention of *static-asset* brand-fidelity drift (distinct from the UGC-video QA-pass pattern already known).
- Promotion-threshold flag: GPT Image 2 now has 2 independent creator-mentions (1 canonical — Nate Herk), crossing the vault's prior "one-creator-only-no-spawn" bar for a dedicated tool note.

### Second squeeze — pass 2 (Hunt 2, already-covered check against 06_tasks + client plans)

- **Major finding:** `tool-higgsfield.md`'s "Integration notes" section (still says access is "through Higgsfield's UI rather than direct API," `applies-to-projects: []`) is stale relative to the vault's own operational reality. EV Electric Services has an actively-used `higgsfield` CLI pipeline (`generate-and-distribute-heroes.py`, `wire-page-images.py`) governed by a full v2.1 SOP (`sop-ai-imagery-for-core-30-pages.md`) with defined prompt types, reference-photo conventions, and a written-consent-on-file requirement for using a client's face/likeness.
- Reframed the new opportunity note accordingly: this isn't "should Keelworks adopt Higgsfield" (already in production) — it's "extend an already-adopted tool to three new deliverable types (ad creatives, carousels, sizzle reels, UGC) via a different interface (MCP-conversational vs. CLI-batch)."
- Risk flag: Nate's UGC workflow uses synthetic AI-avatar characters, not real client likeness — raised as an open research question whether that carries a separate FTC-disclosure consideration distinct from the existing face-likeness consent SOP (not resolved here, flagged for the source note's Research questions).
- Found an existing stale/overdue task, `task-2026-05-08-try-grill-me-on-resume-saas-feature.md` (status: planned, due 2026-05-15) — recommended cross-linking the new marketing-domain grill-me application to it rather than spawning a disconnected duplicate.

### Second squeeze — pass 3 (Hunt 2 continued, per-client folder checks — user-requested "money decision" third pass)

- **S&H Contracting also runs the Higgsfield CLI pipeline** (not just EV) — confirms it's a standard cross-client Keelworks practice, not a one-off.
- **Real, dated precedent for the exact risk this opportunity would scale up:** execution log `execution-log-2026-09-04-higgsfield-image-libraries.md` (3 weeks old) documented that 67 of 72 files in S&H's Higgsfield image library were byte-identical to EV Electric's — direct competitors in the same market. Filed as a named risk on the opportunity note, not hypothetical.
- **The Excel creative-tracker tactic is a proven fix, not a nice-to-have:** the same log records that ungenerated-and-unlabeled images sat as opaque UUIDs for three months, causing one hero image to land on four unrelated pages in Build Wave 1. The operator's own prevention rule from that incident (T-143: name/file at generation time) is exactly what the video's tracker-spreadsheet tactic solves, just extended to new asset types.
- **A watermark near-miss**, also from the same log: three EV files nearly shipped to a live page with a visible "HIGGSFIELD AI" watermark, caught only on manual review — direct evidence for a QA-gate requirement on any faster-cadence ad-creative pipeline.
- **Scope correction against a standing decision:** `decision-2026-05-14-visual-social-proof-capture-as-service-delivery-model` establishes Keelworks' actual model as real client photos first, AI as gap-filler — stock/synthetic imagery was explicitly rejected for hero/trust content. The new opportunity is scoped accordingly (ad-variant volume, sizzle reels, carousels — not a replacement for real photos).
- Stop-rule called after this pass — quiet after 3, next candidates (keelworks' own brand-scaffold status, WordPress publish-pipeline bugs seen in passing) judged non-load-bearing, deferred.

### Completeness check against the raw video (user-requested, separate from vault cross-checks)

- Walked the full step sequence again end to end. Two additions, not expansions:
  1. Minor tactic: "verify by asking Claude directly, don't infer from a UI glitch" (from the product-shots-folder troubleshooting moment).
  2. Elevated the weekly performance-feedback-loop idea (generate → real ad-performance data → weekly review → next round informed by winners) to its own explicit automation-strategy line, and cross-referenced it to Goal A's still-unstaffed marketing-PM agent (research-worker + content-worker) in `current-goals.md` — a concretely-shaped first workload for that agent slot.
- Conclusion: video content was thoroughly captured in pass 1; the three squeezes added vault-context findings, not missed transcript content — expected when the first pass is done properly.

### Second squeeze — pass 4 (Hunt 1 continued, content-only re-check per operator request — no vault cross-referencing this pass)

- **Prompt-library extraction:** re-read the transcript purely for Nate's actual spoken prompts to Claude, near-verbatim, rather than summarizing the workflow conceptually. Nine distinct reusable prompts identified: (1) initial project-setup/context-dump prompt, (2) Grill Me install + run prompts, (3) the "can you actually see the files" verification prompt, (4) the Scroll-World website-build prompt, (5) BOGO ad-creative-set prompt, (6) Marketing-Studio sizzle-reel prompt, (7) Instagram-carousel prompt, (8) UGC-video-ads prompt, (9) the creative-tracker-spreadsheet prompt. None of these had been captured as a discrete, copy-adaptable prompt set before this pass — prior passes described the workflow, not the actual language that drives it. Recommended home: an appended "Prompt library" section on `tactic-claude-code-project-scaffold-for-brand-context.md` rather than a new note (directly tied to that one tactic; fails the conservative-creation-gate distinctness test on its own).
- **Dependency-order catch:** the steps have a real prerequisite chain that hadn't been made explicit — brand assets/guidelines must exist (or be generated fresh via Higgsfield) before the context-dump prompt is useful; the MCP connector must be live before Claude can drive any generation at all; assets must be physically dropped into the project's `assets/` folder before the website-build prompt (Claude explicitly pulled the color system from the PDF rather than inventing one, which only works because the PDF was already in `assets/`); the four parallel generation prompts and the tracker prompt all presuppose the scaffold + connector are already done. Worth an ordered checklist in the tactic note so a first-time reader doesn't fire prompts out of sequence and get worse results.
- **Small correction:** Nate offers "a simple Google Sheet or a simple Excel Sheet" as equally valid for the tracker — prior drafts had been calling it "the Excel creative-tracker" specifically. Corrected to avoid overstating a tool commitment Nate didn't make.
- **A closing caveat worth quoting directly rather than paraphrasing:** "you can't just expect to throw one prompt out there and then go viral and go make a million dollars" — Nate's own explicit expectation-setting, distinct from (and a good closing companion to) the earlier-noted "I didn't add any subject matter expertise" floor-not-ceiling point.
- **Stop-rule check:** this pass found real, addable material (the prompt library is the single most directly actionable artifact from the whole extraction) — not quiet. A fifth pass on content alone would very likely be diminishing returns; the remaining angle menu (PROMISES, QUESTIONS, TIMING) has now been substantially covered across passes 1-4.

---

## Root-cause diagnosis (post-run, per operator request)

The operator asked why four second-squeeze passes kept finding material the first pass missed, whether
model choice (Sonnet) was a factor, and how many squeeze passes the VIS system should institutionalize
going forward. Full write-up: [[lesson-second-squeeze-not-wired-into-vis-extraction-2026-09-26]].
Summary of the three verified causes and the answer on model choice:

1. **Second-squeeze is documented as mandatory ("do not skip," Step 4b) in `workflow-video-extraction.md`,
   but never wired into `SKILL.md`'s own Steps 1-7 or into `extraction-prompt.md` at all** — grepped, zero
   "squeeze" mentions in the spec actually followed on a run. The mandate only ran here because the
   operator asked for it by name, four separate times.
2. **`extraction-prompt.md`'s Phase 4 existing-note check never scopes to
   `04_projects/clients/_active/*/`** — only `05_shared-intelligence/`, `03_domains/*/insights/`, and
   `00_inbox/decisions-pending/`. Nearly every high-value squeeze finding this run (stale tool note vs.
   the real production pipeline, competitor-asset-leak precedent, watermark near-miss, real-photos-first
   scope decision) lived in exactly the client-project folders Phase 4 never reads.
3. **Phase 3 has no instruction to extract a source's demonstrated prompts verbatim as a reusable
   library** — this is why the 9-item prompt library (pass 4's single most actionable finding) wasn't
   caught until it was specifically hunted for.
4. **Was it Sonnet?** No evidence points there. All three gaps are gaps in what the spec instructs any
   model to do, not in how well instructions were executed — a model following `extraction-prompt.md`
   literally has no way to know to check client folders or extract a prompt library, because the spec
   never says to, regardless of which model is running it. The fix is closing the spec gaps, not
   upgrading the model.

Recommended fix (detail in the lesson): wire second-squeeze into `SKILL.md`'s actual steps as a
mandatory, loop-until-quiet gate between Phase 3 and Phase 5, with Phase 6 refusing auto-approval on a
non-zero final squeeze-delta; expand Phase 4's scope to include client-project folders; add a
prompt-library extraction instruction to Phase 3. Not yet applied to `extraction-prompt.md`/`SKILL.md`
themselves — this run only documents the diagnosis, per operator instruction; applying the fixes is a
separate, not-yet-requested step. Phase 7 write of the Nate Herk source remains on hold pending explicit
operator go-ahead, unrelated to this diagnosis.

---

## Phase 6-7 — spec-fixed re-run and write (2026-09-26, same session)

After the root-cause diagnosis above, the operator had the VIS-system chat apply the three spec fixes directly (SKILL.md v1.5 -> v1.6, extraction-prompt v3.5 -> v3.6). This session then re-read both files, confirmed the fixes were live (second-squeeze wired as a mandatory Phase 4b step with quiet-pass loop; Phase 6 squeeze enforcement; client-project folders added to the Phase 4 dedup scope; verbatim prompt-library extraction mandated in Phase 3), and finished this run under v3.6 per the operator's explicit instruction:

- Folded all four manual squeeze passes into the source note's `## Second-squeeze delta` table honestly, including the pass that was NOT quiet (final pass found 3 significant items) — surfaced per v3.6's enforcement rule rather than zeroed out.
- Added the mandated `## Prompt library (from source)` section to the source note: 10 near-verbatim prompts (the second-squeeze finding described "9 distinct reusable prompts" bundled the Grill-Me install+run as one item; split into two here for copy-adaptable precision — noted inline in the source note).
- Set `squeeze-delta: 3` in the source note's frontmatter, matching the final pass's item count — not silently set to 0.
- Ran Phase 6 (review gate, single-agent training mode — this session acted as both executor and reviewer, no separate G-extraction peer-reviewer dispatch available in this environment): the non-zero squeeze-delta surfaced as an explicit to-fix finding per spec (documented in the source note's delta-table closing note), operator had already reviewed and instructed proceeding rather than a 6th pass.
- Ran Phase 7 (write): all files below written to disk under `~/workspace/second-brain/`.

### Files written at Phase 7

- **New:** `03_domains/marketing/insights/source-2026-08-21-nate-herk-claude-marketing-team-higgsfield.md` (the source note)
- **New:** `05_shared-intelligence/tools/tool-scroll-world.md`
- **New:** `00_inbox/decisions-pending/opportunity-ai-creative-package-productized-service.md`
- **New:** `03_domains/app-building/coding-workflow/tactics/tactic-claude-code-project-scaffold-for-brand-context.md`
- **Enhanced:** `05_shared-intelligence/tools/tool-higgsfield.md` (Integration-notes correction, `applies-to-projects` populated, Seedance 2.5 version-name update, per-generation cost benchmarks, competitor-asset-leak + watermark-near-miss risk precedents, real-photos-first scope note)
- **Enhanced:** `03_domains/app-building/coding-workflow/tactics/tactic-grill-before-plan.md` (3rd independent, cross-domain source added — now at the 3-source pattern-promotion threshold; promotion itself left to operator)
- **Enhanced:** `06_tasks/tier-1/task-2026-05-08-try-grill-me-on-resume-saas-feature.md` (light cross-link to the 3rd-source finding; scope/due date unchanged)
- **New (added after initial Phase 7 pass, closing a template-compliance gap — Structured action items are supposed to become task notes, not just source-note prose):** `06_tasks/tier-2/task-2026-09-26-decision-pilot-higgsfield-mcp-ad-creative-extension.md`, `06_tasks/tier-2/task-2026-09-26-research-ugc-synthetic-avatar-ftc-disclosure.md`

**Not created this run** (flagged, deferred to operator, consistent with conservative-creation discipline): `tool-gpt-image-2.md` — GPT Image 2 has now crossed the vault's 2-independent-creator-mention bar per the source note's Tools-mentioned section, but spawning the note is left as an explicit operator decision rather than auto-created.

---

## Mistakes, dead ends and false alarms

| # | What happened | Cost | Prevention |
|---|---|---|---|
| 1 | Assumed `transcript-pull.sh`'s hardcoded macOS Homebrew Python path would resolve on the device-bridge VM. | 1 failed run. | The desktop bridge is a Linux sandbox even when the connected folder is a Mac's home directory — never assume host OS from the folder path. |
| 2 | First auto-subs pull used the script's default `"en.*,en-orig"` sub-lang pattern and hit a 429 from YouTube, misreported by the script as "no captions available." | 2 failed runs, one misleading "no captions" message before diagnosing via manual `yt-dlp --list-subs`. | `"en.*,en-orig"` may fan out into more caption-track requests than YouTube's rate limit tolerates; `"en-orig,en"` succeeded immediately after. Script patched; worth re-checking if it recurs on a future pull. |
| 3 | Device-bridge connection dropped mid-squeeze-pass-1, blocking the planned vault cross-check. | Delayed the already-covered check by one user turn ("try again please"). | No prevention available on this end — transient connection drop; correctly reported rather than guessed around. |
| 4 | **Declared Phase 7 "done" without creating the `06_tasks/` task notes the template itself requires** ("Each item below becomes a task note in `06_tasks/` at Phase 7 if approved at the Phase 6 review gate" — `template-source-video.md`). The Decision and Research structured-action-items were only left as prose in the source note. Caught only because the operator asked "are we done?" and that question was treated as a real completeness check rather than a rhetorical one. | Two task notes (`task-2026-09-26-decision-pilot-higgsfield-mcp-ad-creative-extension.md`, `task-2026-09-26-research-ugc-synthetic-avatar-ftc-disclosure.md`) had to be created and cross-linked in a follow-up pass after the initial "done" claim — not a large fix, but the initial "done" was wrong when stated. | This is the same failure shape as the lesson this run itself produced ([[lesson-second-squeeze-not-wired-into-vis-extraction-2026-09-26]]): a spec requirement that exists in writing doesn't execute itself just because it's read — it has to be checked against, item by item, at the moment of claiming completion. Add an explicit Phase-7 self-check step ("did every Decision/Research/Conditional/Experiment/Comparison/Adoption item in Structured action items get a task note, not just source-note prose?") before ever stating a run is complete. |

## Retractions

- None of the pass-1 draft's substantive claims were wrong — the "17.55 cents" transcription artifact was caught and corrected to $17.55 (with a confidence note) before it was ever filed as fact, so this is a catch, not a retraction of something already on record.

## Knowledge Capture Audit (6-item checklist)

1. **Bugs and failures?** Yes — documented above (Python path, 429 rate-limit, connection drop).
2. **Decisions made?** Yes — patched `transcript-pull.sh` in place rather than working around it per-run (two script edits: Python interpreter path, sub-lang pattern). Reframed the pending opportunity note from "tool-adoption decision" to "extend an already-adopted tool" based on Hunt 2 findings.
3. **Patterns emerging?** Yes — three-pass second-squeeze cadence on a money-shaped decision paid off in escalating value (pass 3 outweighed passes 1+2 combined). Worth noting as reinforcement of the skill's own documented cadence rule rather than a new pattern.
4. **Lessons learned?** The "already-covered" check against the vault's own operational client folders (not just prior source notes) surfaced the highest-value findings of the whole run — a general argument for always including live client-project folders in Hunt 2, not just `05_shared-intelligence/` and `00_inbox/`.
5. **State updates needed?** Applied at Phase 7 (see section above): `tool-higgsfield.md` updated (Integration notes, `applies-to-projects`, Seedance 2.5 version bump, cost benchmarks, risk precedents); `tactic-grill-before-plan.md` updated (3rd source, promotion-threshold flag); stale task cross-linked.
6. **Productization-readiness?** Not applicable — Capture-only tier (VIS ingestion of one source), not a productize-tier run.

## Related

- `[[source-2026-08-21-nate-herk-claude-marketing-team-higgsfield]]` — the written source note (Phase 7)
- `[[tool-scroll-world]]`, `[[opportunity-ai-creative-package-productized-service]]`, `[[tactic-claude-code-project-scaffold-for-brand-context]]` — newly created supporting artifacts
- `[[tool-higgsfield]]`, `[[tactic-grill-before-plan]]`, `[[decision-2026-05-14-visual-social-proof-capture-as-service-delivery-model]]`, `[[execution-log-2026-09-04-higgsfield-image-libraries]]` — enhanced/cross-linked existing notes
- `[[lesson-second-squeeze-not-wired-into-vis-extraction-2026-09-26]]` — root-cause diagnosis for this run's repeated squeeze misses
