# Execution log: Nick Saraev course Part 3 (21 chunks, machine checks before the squeeze, aliases file)

Date: 2026-10-13. Source: yulWjh3rq28, Part 3 of 4. Note: `03_domains/marketing/insights/source-2026-09-26-nick-saraev-claude-code-marketing-course-part-3.md`. Aliases: `skills/vis-extraction/cache/aliases-saraev-part3.txt`.

## Numbers
- Verified scope: full-transcript words 43,583 to 62,708 = 19,125 words. Coordinator estimate for the end was 62,725; the pivot finder put the real cut 17 words earlier, at the start of the sentence "And if you think about it, that now takes us to our next task..." Start overlaps Part 2 by one word ("Let's", Part 2 counted its end as 43,584).
- `--density`: DENSE yes (43 figures, 162 names, 31 example cues, no chapter markers). `--split 900` made 21 chunks.
- Same-chat method, no helper agents. Pass-0 inventory about 8,900 words over 102 lines (10 categories).
- Machine checks run in the mandated order before the squeeze: `--inventory-check` (2 of 102 missing, fixed), `--questions` (88 questions; 10 Q&A rows added, filler listed), `--aliases` (43 flags: 7 real facts added, the rest caption noise in the aliases file), `--links` (16 checked, 0 problems).
- Squeeze: pass 1 combined (31 missed source facts), pass 2 lens-switched scan (0 new), pass 3 requested by Oliver with fresh lenses (2 missed facts, 3 new analysis items, a consolidation section). At the 3-pass cap. Final `squeeze-delta: 2`, `analysis-items: 16` (2 already resolved).
- Final note about 11,500 words, 16 verbatim prompts (P1 to P16) plus 5 copy templates. Cut points for Part 4: word 62,708.

## What strained
1. The new aliases file worked and kept caption noise out of the note. It does not understand a wrong alias: I labeled "Maker Zero" as noise and the diff accepted it, even though it is a real community name. The file hides a flag if you tell it to, so each "!" line needs a quick re-read against the raw text.
2. `--aliases` and `--questions` must be pointed at the part's slice, not the 6-hour file, or every flag is wrong. The scripts have no notion of "part," so I made my own slice file (`part3-slice.md`) and a tiny word-range printer, because importing `coverage-diff.py` runs `main()`.
3. 88 questions is mostly tags ("right?"). The Q&A table needed a judgement call per question. Listing the tag questions as filler in one line was the practical answer.
4. The device shell and the container are separate. The script and the vault live on the Mac, the Read tool and the inventory live in the container. I staged the script and slice into the container to run most checks there, and only ran `--links` on the Mac. Moving the note across needs SendUserFile plus a commit step each time it changes.
5. Auto-caption names are unreliable in both directions: I invented "Boise" for "Bissi" and wrote "Meta" for "XCO." Both slipped past the inventory and were caught by the diff and the squeeze. Placeholder-looking names in a sample email should be copied as captioned and marked unverified.
6. Prompt-library times: Part 2 anchored its estimates about 4 minutes off from the formula. Part 3 uses the script's formula directly and says so.

## Mistakes / what was missed (read by Phase 1 item 7 on the next two VIS runs)
1. Wrote "Meta" and "Boise" into the first draft from guesswork on garbled captions. Copy uncertain names as captioned and mark them unverified.
2. Labeled a real name ("Maker Zero") as caption noise in the aliases file. Re-read each "!" alias against the raw sentence.
3. The first draft left out about 31 small framing facts and quotes (campaign types, war story, "wet rag," Jonno detail, the 75 percent rule behind the 15-of-20 gate). They came out only on the raw read. The inventory had most of them in a short form that did not reach the note. Check the inventory against the note line by line, not just by keyword overlap.
4. The first question table covered about 24 of 88. The extra 10 rows and the filler list only came after the machine list was printed in full. Print and read the whole list before writing the table.
5. Part 1's squeeze item (e) said speed-to-lead was "genuinely absent from the vault." It is covered by the Jono Catliff source, the marketing primer and the conversion benchmarks. Part 1 was not edited; the retraction is in Part 3's analysis items. A claim of "absent from the vault" needs a grep for the term, not a memory check.
6. No task or supporting notes were created and the Phase 6 review gate was not run (training mode, same as Parts 1 and 2). Action items are proposals.

7. In the first draft I told the coordinator that the mega plan row and Part 1 still needed fixing. By the time I filed, the coordinator had already fixed both. The third pass's current-disk check caught it. Re-check "still needs fixing" claims against the live file right before reporting.
8. I called EV and S&H leads "mostly LSA" with no test. The vault only shows S&H runs LSA. Reworded.

## For the coordinator
- Nothing to fix in the mega plan or Part 1 (both already updated).
- Part 3 is at the 3-pass cap and the last pass still found 2 small source facts. Surfacing that instead of looping.
- New vault-fit finding for the EV and S&H trackers: EV has an approved "respond within one business day" promise and a Contact Form 7 form 5816 only rule; S&H copy says "not a next-day callback." A five-minute promise would be a new decision.
