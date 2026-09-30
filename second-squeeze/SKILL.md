---
name: second-squeeze
version: 1.2
status: active
created: 2026-09-22
updated: 2026-09-30
canonical-copy: "workspace/skills/second-squeeze/SKILL.md (this repository file); installed/account copies are distribution mirrors, not authorities."
description: "Independent fresh-angle re-review of a source or finished work; hunt for what the first pass missed and what it got wrong, verify against the whole vault, and fix the record in place. Triggers: second squeeze, gap sweep, run another pass, what did we miss, independent review, squeeze the transcript."
---

# The second squeeze

**The problem this solves, plainly.** A first pass grabs what jumps out, which means it grabs what it was already looking for. One read-through has two built-in failure modes: **missed stuff** (it was sitting right there in the source, but nobody was hunting for it yet) and **wrong stuff** (it made the cut, sounded like a clean win, and got filed as fact without being checked against what the vault already knows). This skill is the deliberate return trip: re-enter the same material as a second, more skeptical reviewer, with different questions, and correct the record where the record actually lives.

**Where it is proven.** The Sept-12 EV client call: pass 1 filed the obvious wins, pass 2 found six more real items, pass 3 found seven MORE including the job-level pricing anatomy, a live referral opportunity with the main competitor, and an unkept operating promise. The vault replication audit: three miss-sweeps, every one found real things. The pattern held every time: the next pass with new angles finds real material.

## Canonical copy and model routing

This on-disk skill is the shared source of truth for every agent. Reconcile changes here first, then sync installed or account copies explicitly; never overwrite it merely because an account copy differs. If a mirror contains unique changes, compare and preserve them for review before syncing. This change does not assert any remote mirror has been updated.

Select producer/reviewer tiers and record runtime identity per `~/workspace/second-brain/_meta/model-routing.md`. Dense or high-stakes second-pass work requires the one-tier-up rule (or its explicit FRONTIER ceiling exception) and a different reviewer; a same-agent fresh-angle pass is a self-check, never independent gate clearance. Keep source access, evidence and existing review gates intact.

## The stance

- You are not the person skimming again. Use the second-reviewer stance to check the first pass. When the first reviewer was you, label the result as self-review; it does not satisfy an independent-review requirement.
- Never re-read the same way twice. Every pass gets angles the previous passes did not use.
- A claim that sounds like a clean win gets MORE scrutiny, not less.
- Findings are fixed in the real files, with dated addendum or correction notes (history stays intact, never silently edited). A gap review that only hands back a list of findings is half done.
- Keep an execution log per `second-brain/_meta/execution-log-convention.md`; retractions of earlier claims go in it. Uncertainty is marked, never guessed.

## The two hunts, run separately

**Hunt 1: missed stuff.** Go back to the RAW source (transcript, logs, folder), not the summary of it, and sweep with fresh angles from the menus below.

**Hunt 2: wrong stuff.** Take what the earlier pass DID file, especially its cleanest wins, and stress-test each:
- **Already-covered check:** before treating anything as "new, nobody has this," search the vault homes the first pass did not check: domain folders (including client-services and client-acquisition), shared-intelligence subsystems, master plans, prior briefs and campaigns, monitoring logs, tier-3 tooling, 06_tasks. The biggest reversal on record (the Federal Pacific "gap" that already had a page, a shelved Ads campaign, AND months of citation monitoring) hid exactly here.
- **Evidence check:** a claim someone made (the client's "most customers come from ChatGPT," our own "number one across the board") is a lead, not a fact, until it matches logged data.
- **Number check:** machine-transcribed figures get sanity-checked against a known baseline ($64.80 once arrived as $6,480).
- **Current-disk check:** anything you are about to call open, missing, or broken gets verified against today's files first.
- **Own-claims check (added 2026-09-29):** reread your own confident lines from the earlier pass ("no competitor has this", "we are the only ones") and ask what test backed them. An untested claim gets retracted or reworded to "few" or "likely" and logged as your own retraction. (Proven on the EV surge page: "no competitor has real install proof" was never tested, and contractor install videos ranked on 3 of 4 searches.)
- **Blind re-fetch check (added 2026-09-29):** anything new added during the squeeze (a fact, a number, a quoted line) goes to a fresh reviewer who re-fetches the original sources itself and returns SUPPORTED / STRETCHED / NOT FOUND per sentence. Where two sources pull opposite ways, drop the claim instead of picking a side. (Proven: it caught "a higher kA rating means more protection", which another maker page contradicted.)

## Angle menus (pick angles earlier passes did NOT use; invent more)

**Transcripts and meetings:** the MONEY pass (every figure + what drives each price, hedges preserved) · the PROMISES pass, both directions, with dates · the NAMES pass (every person, company, product = intel, relationship, or opportunity) · the ONE-SPEAKER read (one speaker's lines start to finish) · the CORRECTIONS pass (self-corrections and hedges) · the QUESTIONS pass (unanswered ones are open threads) · the TIMING pass (seasons, deadlines) · the DISCOMFORT pass (money tension, pushback, jokes carrying real requests).

**Vault work and deliverables:** open never-listed folders, every layer including _meta corners, archives, inboxes, tier-3 · recency diffs · follow links FROM consuming files INTO the work (a link to nothing is a gap announcing itself) · grep for promised-but-unwritten docs and check whether they got written under other names · machine checks, not eyeballs (YAML parses, path links resolve, tables not orphaned, headline counts match counted rows, no sandbox paths or secret patterns in the diff) · QC your own output with the same lenses.

**Finished pages, products or deliverables someone is trying to rank or sell (added 2026-09-29, proven on the EV surge protector page):**
- The SERP-FEATURE pass: list every feature type on the results (video, People Also Ask, related searches, AI overview, image pack, short videos), not just the ten blue links. Each is a content format competitors win with and a possible add.
- The SEASONALITY pass: pull the monthly shape of demand (5-year trend). Timing decides when to publish and when posts and follow-ups go out.
- The RULE-ORIGIN pass: for every "never do X" rule on the work, find whose rule it is (client decision, our source-discipline rule, a safety rule), its date, and whether it is reversible. Answer the owner's "would breaking it help?" honestly: real upside, real risk, and an option that captures the value safely. A rule the owner has since changed is a live opportunity, not a fixed limit.
- The SOURCE-GAP pass: list every claim the first pass avoided for lack of a source (numbers, ratings, lifespans, warning signs, brands). Go find primary sources (maker manuals, standards bodies, the code itself). Log each as fetched, blocked, or lead-only. If a fetch is blocked, do not get around it. If only one weak or overseas source has a number, keep it as a lead and ask the client for their own experience instead.
- The FIRST-HAND-PROOF pass: list what only the client can supply (photo, video, a job story, their own numbers and habits) and turn it into one short plain text the owner can send.
- The COMPETITOR-COPY pass: a table with three columns: already have, copy, skip on purpose (with the reason). Never leave competitor tactics as a loose list.
- The BACKLOG pass: every spin-off page, article, post or video the material suggests, each with intent, what it depends on, and a cannibalization check against the page just built.

## Cadence and the stop rule

Minimum two passes on any big task or dense source; three when money decisions ride on it. **Stop when a full pass with genuinely new angles comes back quiet**, not when you feel done: the feeling of done is what pass 1 had. Each pass logs which angles it used so the next pass picks different ones.

## Where it plugs in

VIS ingestion (workflow-video-extraction step 4b, before review closes) · client-meeting transcripts (before the outcome note is final) · big-task closeout (before any batch commit or handoff) · deep harvests (the shared-intelligence-harvest skill's step-3 miss-sweep is this skill applied to a whole domain).

## Output shape

1. Fixes applied in place (dated addendum or correction notes in the real files).
2. A short delta report: what was found, which ANGLE found it, corrections vs additions, retractions of earlier claims.
3. If a miss looks systematic (same blind spot across sources), say so: that is a first-pass process upgrade, not just a finding.
4. (Added 2026-09-29.) When the work is a page or product with rules on it: a decision menu. Each rule becomes one line: who decides, the honest upside, the risk, and the safe option. Nothing is broken until the owner says so.
5. Deferred ideas go into the client's master tracker as checkboxes with a pointer to the note that explains them (a tracker line, not a vault note nobody reopens). Add a dated log line to the plan file.
6. When something needs the client's input, hand the owner ONE copy-ready text to send, in plain words, with each question answerable in a sentence.
