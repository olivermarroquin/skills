# Execution log: Phase 6 dense-source fix (build, tests, close-out)

Date: 2026-10-13. Chat: `vis-p6-dense-source-fix`. Reports: `second-brain/_meta/handoffs/vis-system-enhancement/phase-6-test-report.md` and `phase-6-closeout-report.md`.

## Numbers
- Codie Sanchez (5,393 words): old method 9 passes, new method 3 passes, same completeness on the 9-pass answer key.
- Nate Herk (9,354 words): new method, blind run found real misses the 5-pass note lacked (details in `phase-6-drafts/blind-test/nate-blind-extraction.md`). Not merged into the Nate note; Oliver decides.
- Course part 1 (16,249 words, 18 chunks of ~900): inventory in 3 batches plus 1 combined pass = 2 passes. Final coverage-diff 9 possible misses (all name garbles or already-covered cues). The finished note scores 30 on the same check.
- Saraev part 2 (27,583 words) ran in another chat and held up at 31 chunks (see its own log).

## What strained (Mistakes: read before the next dense run)
1. Helper agents cost about 84k tokens each, mostly fixed overhead. Chunks run in the SAME chat; do not hand chunks to helpers.
2. Prompts were paraphrased instead of copied word for word. Fix: PROMPTS is now the 10th inventory category.
3. Vault checks cannot be proven on a source that is already in the vault, because the vault already holds its findings. Test vault checks on a FRESH source.
4. Cowork chats read the Claude ACCOUNT skill, not the workspace. The account `vis-extraction` was an old v1.1 and silently ran the old method. Account copies must be thin launchers ("two rooms" lesson). After any skill upgrade, check `skills/_sync-registry.md` and run a fresh-chat test.
5. Version labels drifted (frontmatter 1.6.1, title v1.5, text 1.7). Change all of frontmatter, title and changelog together.
6. The base length bands (under 9,000 / 9,000 to 25,000 / 25,000+) still exist under the density rule. A 9,000 to 25,000 word video that has chapters and is not flagged dense still gets "focused attention", which skims. Open design question for Oliver.
