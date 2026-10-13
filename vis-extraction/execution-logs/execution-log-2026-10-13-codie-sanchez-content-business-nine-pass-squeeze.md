---
type: execution-log
status: complete
created: 2026-10-13
skill: vis-extraction
skill-version: "1.6.1 (extraction-prompt v3.6)"
source: "[[source-2026-07-21-codie-sanchez-dont-become-a-content-creator-build-a-content-business]]"
tags: [execution-log, vis-extraction, second-squeeze, codie-sanchez, marketing]
---

# Execution log: Codie Sanchez "Don't Become A Content Creator" VIS ingestion (nine-pass squeeze)

## Summary

Ran VIS on https://www.youtube.com/watch?v=ZvAwqGH_79Q (Codie Sanchez, "Don't Become A Content Creator,
Build A Content Business.") per operator request. Operator explicitly asked, before starting, to confirm
the live spec (v1.6.1 / extraction-prompt v3.6, not a stale synced copy) and to execute Phase 1 item 7
(recent-mistakes ledger) against the Nate Herk run's lesson and Mistakes table. Both done. Pulled
transcript via yt-dlp (installed fresh this run — not present on the device's PATH beforehand, per Phase
0a's documented first-run procedure).

Extraction produced a source note plus two new tactic notes and one enhancement to an existing tactic.
Nine second-squeeze passes were run before operator sign-off to write — see this file's parent source
note for the full pass-by-pass delta table. This execution log exists to carry forward what the squeeze
process itself revealed about the extraction pipeline, per Phase 1 item 7's own requirement that future
runs read this file's Mistakes section.

## Files written

- `03_domains/marketing/insights/source-2026-07-21-codie-sanchez-dont-become-a-content-creator-build-a-content-business.md` (new source note)
- `03_domains/content-systems/tactics/tactic-swipe-file-content-ideation-system.md` (new tactic)
- `03_domains/marketing/product-sales/tactics/tactic-product-ladder-monetization-framework.md` (new tactic)
- `03_domains/seo/tactics/tactic-founder-influencer-marketing-as-llm-defensibility.md` (enhanced — cross-creator-count 1→2, new creator-convergence section appended, `.bak-pre-codie-enhancement` backup left alongside for this run only)
- `06_tasks/tier-3/task-2026-10-13-comparison-platform-sequencing-pick-one-vs-two-keelworks-channel.md`
- `06_tasks/tier-3/task-2026-10-13-adoption-swipe-file-content-ideation-system.md`
- `06_tasks/tier-3/task-2026-10-13-adoption-three-notes-per-post-review-ritual.md`
- `06_tasks/tier-3/task-2026-10-13-conditional-platform-calibration-metrics-first-channel.md`
- `06_tasks/tier-3/task-2026-10-13-experiment-review-codies-free-swipe-file-log-and-newsletter.md`
- `05_shared-intelligence/lessons/agent-ops/lesson-dense-narrative-source-first-pass-undercaptures-qualitative-content-2026-10-13.md`
- This file.

## Judgments (left empty in frontmatter per template convention; suggested values live in the source note's body)

Suggested tier 2, relevance 5, actionability 4, monetization medium — reasoning for each is in the source
note's "Suggested judgments" section, including the explicit retraction of an earlier, lower relevance
score caught mid-run (see Mistakes below).

## Second-squeeze summary (nine passes)

Full pass-by-pass table lives in the source note itself. Headline shape: passes 1-3 were the ordinary
money/numbers/dedup checks (pass 3 came back quiet). Passes 4-9 were all operator-requested continuations
and each found real material — see Mistakes section below for what that implies about the pipeline, not
just this source.

## Mistakes / what was missed (read by Phase 1 item 7 on the next two VIS runs)

1. **Treated two connected client businesses as unconnected on the first three passes.** Marr Auto
   Sales and Latin United Multiservices are a documented, pre-existing vault fact (the "Marr cross-feed"
   in `plan-customer-acquisition-2026-08-07.md`) — a Marr buyer needs Marr's state inspection to complete
   the registration LUM performs, so their marketing is one content engine, not two. Passes 1-3 missed
   this entirely and concluded the swipe-file tactic was content-systems-only / not client-applicable.
   The operator caught this with a direct correction, not a fresh read. **Fix for next run:** when two
   active client projects share an operator, explicitly check for a documented cross-business
   relationship before concluding they're independent — don't assume business-entity separation implies
   marketing-strategy separation.
2. **The single largest content gap (qualitative platform-personality framing + every worked good/bad
   example) wasn't found until pass 6 of 9, and only because the operator asked a pointed question.**
   Passes 1-5 had fully and accurately captured every numeric claim in the source (sponsorship $, RPM,
   reach ratios, ticket attribution) but had not inventoried a single one of the source's six
   platform-personality descriptions or its six paired worked examples — material the source spends most
   of its runtime on. See the new lesson
   [[lesson-dense-narrative-source-first-pass-undercaptures-qualitative-content-2026-10-13]] for the full
   diagnosis and proposed spec fix (an explicit narrative-completeness checklist item for Phase 3, and a
   recommendation to sequence the second-squeeze angle menu so a qualitative-completeness angle runs
   early on dense, multi-example sources rather than only after the numeric angles are exhausted).
3. **Judgment frontmatter fields were initially pre-filled against the template's own stated
   convention.** `template-source-video.md` leaves `tier` / `relevance-score` / `actionability-score` /
   `monetization-potential` blank in frontmatter by design, with numeric suggestions living only in the
   body's "Suggested judgments" section. An earlier draft of this note filled them in directly. Caught and
   corrected before write — left blank in the shipped file.

## Research questions logged (not resolved this run)

- What Codie Sanchez means by her own coined term "fastvertising" (used once, undefined, while narrating
  a YouTube retention-graph example) — no definition in the available auto-caption transcript, no prior
  reference anywhere in the vault.
- Whether Codie's ~2M-follower, live-event business model's product-ladder top rungs (fund investment,
  "sell us your business") generalize below her scale.
- Whether "pick one platform first" (this source) actually outperforms "pick two concurrently" (the
  existing founder-influencer tactic) specifically for a B2B/agency audience — logged as an open
  Comparison task, not yet resolved.

## Note on git

Per the skill's standing convention, this run never ran `git add`/`git commit`/`git push` — those remain
the operator's own step whenever Oliver is ready to commit this batch of writes.
