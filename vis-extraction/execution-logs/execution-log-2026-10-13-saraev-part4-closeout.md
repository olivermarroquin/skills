# Execution log: Nick Saraev course Part 4 (last part, 21 chunks, closes the 11-promise map)

Date: 2026-10-13. Source: yulWjh3rq28, Part 4 of 4. Note: `03_domains/marketing/insights/source-2026-09-26-nick-saraev-claude-code-marketing-course-part-4.md`. Aliases (tracked): `skills/vis-extraction/references/aliases/aliases-saraev-part4.txt`.

## Numbers
- Verified scope: full-transcript words 62,708 to the end. Spoken-text total is 81,635 words, so the slice is **18,927 words**. The brief said 81,684 and 18,976; 81,684 is `wc -w` of the whole file, which includes a 46-word header and the "## Transcript" marker. Same counting method as Parts 2 and 3.
- Boundary re-check with `--pivots` on the full file: the pivot sentence is still at word 62,725 (inside the sentence that starts at 62,708). Internal markers unchanged (66,984; 75,744; 78,597; the 70,183 line is at 70,180). The video ends on a real sign-off.
- `--density` on the slice: DENSE yes (45 figures, 105 names, 19 example cues, no chapter markers). `--split 900`: 21 chunks. The splitter drops 14 words of bracketed caption tags, so the chunks add up to 18,913 words.
- Same-chat method, no helper agents. Pass-0 inventory about 8,200 words over 177 lines (10 categories). Final note about 17,300 words, 22 prompts (P1 to P22).
- Machine checks before the squeeze, in the mandated order: `--inventory-check` (8 of 177 flagged, all quotes; fixed), `--questions` (80 questions; table plus numbered list of the tags), `--aliases` against the slice (12 flags: 10 real facts added to the note, 1 caption spelling, 1 noise line verified against the raw sentence), `--links` (9 checked, 0 problems).
- Squeeze: pass 1 found 14 small source facts, pass 2 found 2, pass 3 (the cap) found 0. Final `squeeze-delta: 0`, `analysis-items: 19`. No operator-requested pass.
- Part 1 edit: one new "Status update (Part 4 filed)" paragraph in the promise map section, nothing else (checked with a before/after diff).

## What strained
1. The brief's word counts were off by 49 (header words). Always recount the spoken body with the same method as the script before trusting a coordinator's number.
2. The device shell had Python, the script and the vault all in one place this time, so no staging to the container was needed (unlike Part 3). Everything ran where the files live.
3. The squeeze passes were machine-assisted: instead of re-reading the whole 19,000 words three times, I scanned the raw slice for sentences whose rare words were missing from the note, then for whole low-coverage windows, numbers, names and hedges, and read only the hits. That cost a small fraction of three full re-reads and found the same kind of leftovers (small framing facts). It cannot find a missing idea phrased in common words, so the first pass still used the promises and quotes angles by eye.
4. `--aliases` accepts an alias line without checking it is true. I kept the `!` (ignore) lines to one ("Wait," from "Wa, this is way more efficient") and checked it against the raw sentence. Putting real facts into the note beats ignoring them: 10 of 12 flags were small facts worth keeping.
5. Auto-caption names again: "Netlefi/Netlifi" (Netlify), "Kuo" (Quo), "OOTH" (OAuth), "nickleclick.ai / Nickleftclick.ai" (probably his agency domain), "PGs" (probably PNGs), "MR" (probably MRR), "Cance," "Gemini Omni," "Marcus Ben." All copied as captioned and marked unverified where they matter.
6. The Part 3 worry about "Maker Zero": the raw Part 3 text says "Maker School and Maker Zero, which is my free community," so it is a real second community and not caption noise. Part 4 only mentions Maker School.

## Mistakes / what was missed (for future VIS work)
1. First draft of the cost section said the dashboard cost "roughly what a month of an agency-reporting product would." He never says that. Caught on a re-read of my own sentences against the inventory. Check every comparison I write against a quoted line.
2. I turned his spoken "854, 841, 827, 812, 756" into clock times (8:54...). The unit is not said. Copy numbers as spoken and say the unit is unknown.
3. I wrote that Nick "told" the private equity firm "Brother, you're going to be automating a single hour." He says he only thought it. Re-read who the speaker says a line to.
4. I wrote a delta-table sentence about a "Pro-style credit" mistake that never happened in the draft. Delta rows must describe real corrections only; I rewrote it.
5. Two novelty claims were too strong: the "only self-healing hits are git-gate notes" claim came from a grep cut off at 6 files, and the "monthly report SOP is a gap" claim came from a superseded checklist. A "not in the vault" claim needs the full grep, and a gap claim needs the current file, not an old checklist.
6. Not done: no task or supporting notes were created and the Phase 6 review gate was not run (training mode, same as Parts 1 to 3). The action items are proposals only.

## For the coordinator
- Mega plan: the VIS-6H row (line 210 of `03_domains/marketing/mega-plan/mega-marketing-plan.md`) and the frontmatter `sources-waiting` line (line 15) still say Part 4 is pending. I did not edit them. Part 4 is filed.
- Part 1 line 43 still says Part 4 "was not filed when this was updated." Left as written (the brief limited the Part 1 edit to the promise map).
- Whole series: 8 of 11 welcome promises delivered, 3 partly delivered (7, 8, 11), 0 missing. Never built in any part: appointment booking, voice, UTMs, the dashboard's AI assistant, a live dashboard data connection or refresh, an enterprise worked example, and any real send or result data.
- Vault-fit items worth a decision: the stored-log-in "debug flow" conflicts with the open tier-1 audit of plain-text conversation logs (task-2026-05-10-audit-claude-code-conversation-logs-for-secret-leakage, status planned); the monthly client report SOP is still a queued handoff (2026-06-22) and the dashboard method is one possible answer; EV's Stripe runbook already plans dunning, so an invoice-chase build would overlap.

## Files kept for this run
- Note: `second-brain/03_domains/marketing/insights/source-2026-09-26-nick-saraev-claude-code-marketing-course-part-4.md`
- Aliases (tracked): `skills/vis-extraction/references/aliases/aliases-saraev-part4.txt`
- Pass-0 inventory (10 categories, 21 chunks): `skills/vis-extraction/cache/inventory-saraev-part4.md`
- Part 4 slice (words 62,708 to the end): `skills/vis-extraction/cache/slice-saraev-part4-words-62708-81684.md`
- Chunk files, the slice cutter and the gap-scan script: `_scratch/saraev-part4/` (scratch, safe to delete; `part1-before.md` is a copy of Part 1 before the edit)

## Operator-requested extra pass (2026-10-13)
Reason: operator asked for "another squeeze" to get everything usable across projects. Logged as row 5 in the note's delta table, marked operator-requested. Result: 4 tiny missed source facts (squeeze-delta now 4, after a fourth fact (a TV wall display story) turned up on the re-run of --aliases), analysis items 19 to 22, plus two added sections (Project fit map, Reusable skeletons). Re-ran --aliases (clean), --links (9, 0 problems) and --inventory-check. Mistake caught: new analysis items were first inserted out of order (20 to 22 before 19); renumbered by position.
