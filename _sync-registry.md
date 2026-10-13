---
type: registry
status: active
created: 2026-09-22
purpose: "One place that tracks which skills exist where (Claude account library vs this workspace folder), which copy is canonical, and how each direction gets synced. Cowork chats read the account library; Claude Code sessions read this folder; the two do not sync themselves."
tags: [registry, skills, sync, cowork, claude-code]
---

# Skill sync registry

**The two rooms, plainly.** Cowork chats load skills from the Claude ACCOUNT library (saved via review cards or Settings). Claude Code sessions load skills from THIS folder. A skill in only one place is invisible to the other mode.

## The rules

1. **Every skill names its canonical copy** in frontmatter; the other side is the mirror. When either learns something, update canonical first, mirror same session.
2. **Account → workspace:** write the SKILL.md mirror here (done by hand or by any Cowork chat with the folder connected).
3. **Workspace → account, single-file skills:** propose via skill review cards, up to 3 per batch. Say "propose the next skill batch from the sync registry" in any Cowork chat.
4. **Workspace → account, multi-file skills:** cards would strip their reference files and scripts. The right vehicle is a Cowork PLUGIN (the cowork-plugin skill builds one). Until that plugin exists, Cowork chats can still READ these skills as vault files and follow them manually.
5. A new skill gets its row here in the same session it ships (same rule as the toolkit reuse map).
6. **The launcher pattern (adopted 2026-09-22): a workspace skill over ~15KB, or one that cannot run without the vault anyway, gets a THIN LAUNCHER in the account instead of a full copy.** The launcher carries the triggers, the one-paragraph job description, and "read the canonical workspace file and follow it exactly." Canonical flips to the WORKSPACE side for launcher-backed skills. Why: full copies of 40KB manuals drift, and drift is the disease this registry exists to cure. Full mirroring stays for small self-contained skills (both sides usable standalone).

## Launcher update (2026-10-13): vis-extraction and second-squeeze

Both skills now follow the launcher pattern (rule 6). **Canonical = the WORKSPACE files** (`skills/vis-extraction/SKILL.md`, v1.8 at time of writing, and `skills/second-squeeze/SKILL.md`, v1.4 at time of writing; version numbers move, the rule does not). The account copies are thin launchers: triggers, a one-paragraph job description, and "read the canonical workspace file and follow it exactly." Oliver saved the launcher versions to the account on 2026-10-13 (the workspace session could not open a Cowork chat itself; the mega-plan chat then ran the fresh-chat test and logged both launchers as passing in `_meta/_event-log.md`, row 2026-10-13T21:00:00Z).

Why: the old account `vis-extraction` was a standalone v1.1 with the 9,000/25,000 word thresholds and no squeeze or coverage steps, so a Cowork chat ran the old method while the workspace had the new one. See `second-brain/05_shared-intelligence/lessons/agent-ops/lesson-two-rooms-account-copies-must-stay-thin-2026-10-13.md`.

This supersedes the "canonical = account" line and the vis-extraction DRIFT warning in the State block below.

## State (2026-09-22)

**In BOTH places (canonical = account):** shared-intelligence-harvest · client-site-baseline-and-backup · explain-from-scratch · plain-language-translation. **vis-extraction and second-squeeze moved to launcher pattern 2026-10-13 (canonical = WORKSPACE); see the Launcher update section above. The old DRIFT warning is resolved.**

**Account-only, by design:** morning (personal daily brief, no Code use)

**Workspace-only, single-file, Cowork-viable (card these over, in priority order):**
1. client-engagement-audit — SAVED to account 2026-09-22 ✅
2. step-by-step-walkthrough — SAVED ✅
3. synthesis-readiness-scan — SAVED ✅
4. idea-factory-prompter — SAVED ✅
5. perplexity-research-suite — LAUNCHER card SAVED to account 2026-09-22 ✅ (single-file sync COMPLETE; only the multi-file plugin route remains)
6. client-fact-research · service-seo-research · city-and-intersection-research (combined card) — LAUNCHER cards SAVED to account 2026-09-22 ✅
7. execution-planner — LAUNCHER card SAVED to account 2026-09-22 ✅
8. client-call-ingest — LAUNCHER card SAVED ✅ · gsc-performance-pull + index-status-diagnose — combined LAUNCHER card "gsc-data-pulls" SAVED ✅. All three launchers state the computer-linked requirement, since they run local scripts.

**Plugin build note (2026-09-22):** v0.1.0 of the keelworks-skills plugin failed Cowork validation (23 skills had descriptions over the 1024-character cap or containing angle-bracket tags). Fixed in v0.1.1: descriptions cleaned and shortened at sentence boundaries, same fixes applied to the 23 canonical SKILL.md files here so plugin and workspace match. Build at skills/_plugin-builds/keelworks-skills-0.1.1.plugin — SAVED/INSTALLED to Oliver's account 2026-09-22 ✅ (all 37 skills live in Cowork). v0.1.0 build is dead, can be deleted. Rule for future skills: frontmatter description max 1024 characters, no angle brackets.

**Workspace-only, multi-file, plugin route — keelworks-skills v0.1.0 SHIPPED 2026-09-21 ✅:** built via Cowork + the cowork-plugin skill. Delivered as a .plugin file and committed to `skills/_plugin-builds/keelworks-skills-0.1.0.plugin`. Bundles 37 skills:
- 27 client-delivery: client-schema-sync, client-seo-audit, client-seo-onboarding, competitor-architecture-diff, competitor-deep-research, content-coverage-audit, custom-html-build, design-fingerprint, house-voice-rewrite, hub-and-nav-build, invoice-generation, lsa-management, lsa-setup, market-intelligence-engine, opportunity-finder, opportunity-teardown, output-quality-loop, perplexity-citation-monitoring, perplexity-refinement, prioritization, prospect-intake, reference-finder, reference-library, seo-data-wrapper, seo-tooling-landscape-research, website-design, wordpress-to-custom-html
- 10 vault/ops orchestration: hermes-vault-bridge, intel-routing, knowledge-os-setup, master-tracker-aggregator, meta-document-primer, multi-chat-coordination, multi-source-synthesis, operations-planner, reviewer-orchestrator, vault-orchestrator

Fixed along the way, in BOTH the plugin copy and the canonical workspace files (no drift left behind): 7 skills were missing the `name`/`description` frontmatter Cowork's skill loader requires (client-schema-sync, competitor-architecture-diff, content-coverage-audit, custom-html-build, market-intelligence-engine, wordpress-to-custom-html; hermes-vault-bridge had `name: vault-bridge` instead of `name: hermes-vault-bridge`), plus 2 more whose one-line `description:` had an unescaped colon that broke YAML parsing (client-seo-onboarding, seo-tooling-landscape-research) — converted to block-scalar (`description: >`).

**Deliberately deferred (still plugin-route, not yet built):** the 3 giant harnesses — gate-peer-reviewer (431 files), site-capture-engine (191), design-emulation-verify (176) — left out of v0.1.0 to keep the first build tractable; candidate for a v0.2.0 wave or a separate plugin. vault-orchestrator/SKILL.md references `../gate-peer-reviewer/SKILL.md`, which won't resolve until that skill is added.

**Not real standalone skills (no SKILL.md, shared/support files only):** hermes-hooks, perplexity-shared, phase-1-extension.
