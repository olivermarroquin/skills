# Execution log: Nick Saraev course Part 2 (first real run of 900-word dense chunking at scale)

Date: 2026-10-13. Source: yulWjh3rq28, Part 2 of 4. Note: `03_domains/marketing/insights/source-2026-09-26-nick-saraev-claude-code-marketing-course-part-2.md`.

## Numbers
- Real scope: full-transcript words 16,000 to 43,584 = 27,583 words (brief estimated 23,370; the staged slice stopped 1,450 words before the real chapter pivot).
- `--density`: DENSE yes (32 figures, 116 names, 35 example cues, no chapter markers). `--split 900` made 31 chunks in 0.02 s.
- Same-chat method, no helper agents. Token counter: about 81k for reading and inventorying all 31 chunks, about 173k for setup (spec files, Part 1 note, logs, dedup, boundary), about 88k for drafting plus squeeze. About 343k in total. Wall clock about 13 minutes.
- Final note about 13,500 words (24 prompt-library entries). Squeeze: 3 passes used (cap), last pass 2 minor asides, `squeeze-delta: 2`.

## What strained
1. The pace-based end boundary was wrong by about 3,250 words. A slice built from a pace estimate needs the pivot searched in the full transcript, not just near the estimate. Searching the full transcript for "next major step" and "done with" style sentences found it in one call.
2. No timestamps in the captions, so prompt-library "timestamps" are estimated from word position (3.75 words per second). Good to within a few minutes at best.
3. Reading 2 chunks per step with one inventory write per step was the right size. Per-chunk inventory text grew to about 8,600 words; fine for the main context.
4. The inventory categories QUESTIONS and PERSONALITY were the ones I under-captured on the first pass (no questions table, thin on test-gen examples), the same shape of miss as the Codie lesson. Machine scans (list every "?" sentence; check each inventory line against the note) caught them.
5. The coverage-diff script flags caption misspellings of names it cannot match. Writing the dispositions into the note (a "Coverage-diff record") also clears those name flags on re-run, so a clean re-run partly reflects the record. The disposition list is the real evidence.

## Mistakes / what was missed (read by Phase 1 item 7 on the next two VIS runs)
1. Trusting the brief's end boundary. Verify the pivot sentence before chunking. Nearly cost a 1,450-word hole.
2. First draft had no QUESTIONS section and light PERSONALITY and example coverage. Run the "every question" machine list and an inventory-to-note overlap check before the first squeeze pass, not after.
3. A wikilink to a note that does not exist (`[[keelworks-platform]]`) and an ambiguous `[[_README]]` link reached a finished draft. Resolve every wikilink against the vault before declaring done.
4. Task notes and supporting notes were not created (training mode, no review gate run). The Structured action items are proposals only.


## Addendum (2026-10-13, later the same day): what changed after the first write

Written so the next two VIS runs inherit it (Phase 1 item 7 reads the Mistakes sections of the two newest logs).

**Spec and tool changes made from this run's lessons:** extraction prompt v3.6 to v3.7, `vis-extraction` v1.7 to v1.8, `second-squeeze` v1.3 to v1.4, `coverage-diff.py` new modes (`--questions`, `--pivots`, `--find`, `--time-at`, `--inventory-check`, `--links`, `--aliases`), and the source template gained an `analysis-items:` field. Backups sit beside each file as `.pre-v18.bak`, `.pre-v37.bak`, `.pre-v14.bak`. Part 3 was extracted with these checks and its log shows they work.

**Part 1 repair:** Part 1 was cleaned from 31 diff flags to 0 using the blind dense extraction, an aliases file, `--questions` and `--links` (33 detail bullets merged, a Q&A table added, 1 dead link fixed). Part 1 now links forward to Parts 2 and 3 and its promise map has a dated status update.

**Mistakes / what was missed (addendum)**
1. A squeeze-delta row quoted two old bad links as live `[[...]]` text, so the finished note still had 2 dead links. The new `--links` check found them. Write fixed links as plain text in any log row.
2. The first "clean" coverage result depended on spelling the misses out in the note's own record section. That is a fake clean. The script now skips that section and reads an aliases file instead.
3. `squeeze-delta: 7` mixed missed source facts with analysis items. Now `squeeze-delta: 0` and `analysis-items: 7`.
4. I told the operator the Cowork copies of the skills still had the old rules. The sync registry says the account copies are thin launchers that read the workspace files, so no sync was needed. Check the registry before saying a mirror is stale.
5. Prompt-library times here are anchored to the chapter-6 start (01:15:23) and run about 4 minutes later than the plain formula Part 3 uses. Both are estimates; the note now says so.
6. Not done by me and still open for the coordinator: the mega plan row for the 6-hour video still says Parts 3 and 4 are not filed, and the Part 3 note's frontmatter (`squeeze-delta: 0`) disagrees with its own log (`squeeze-delta: 31`).
7. The aliases files first lived in `skills/vis-extraction/cache/`, which git ignores, so a "reproducible" clean result would fail on a fresh checkout. Part 1 and Part 2 alias files are now tracked copies in `skills/vis-extraction/references/aliases/`. The transcript slices stay in `cache/` (re-make them from the full transcript with the word ranges in each note's Series section). The Part 3 aliases file is still in `cache/` and needs the same move.
