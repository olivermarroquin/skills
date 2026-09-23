---
name: second-squeeze
version: 1.1
status: active
created: 2026-09-22
updated: 2026-09-22
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

## Angle menus (pick angles earlier passes did NOT use; invent more)

**Transcripts and meetings:** the MONEY pass (every figure + what drives each price, hedges preserved) · the PROMISES pass, both directions, with dates · the NAMES pass (every person, company, product = intel, relationship, or opportunity) · the ONE-SPEAKER read (one speaker's lines start to finish) · the CORRECTIONS pass (self-corrections and hedges) · the QUESTIONS pass (unanswered ones are open threads) · the TIMING pass (seasons, deadlines) · the DISCOMFORT pass (money tension, pushback, jokes carrying real requests).

**Vault work and deliverables:** open never-listed folders, every layer including _meta corners, archives, inboxes, tier-3 · recency diffs · follow links FROM consuming files INTO the work (a link to nothing is a gap announcing itself) · grep for promised-but-unwritten docs and check whether they got written under other names · machine checks, not eyeballs (YAML parses, path links resolve, tables not orphaned, headline counts match counted rows, no sandbox paths or secret patterns in the diff) · QC your own output with the same lenses.

## Cadence and the stop rule

Minimum two passes on any big task or dense source; three when money decisions ride on it. **Stop when a full pass with genuinely new angles comes back quiet**, not when you feel done: the feeling of done is what pass 1 had. Each pass logs which angles it used so the next pass picks different ones.

## Where it plugs in

VIS ingestion (workflow-video-extraction step 4b, before review closes) · client-meeting transcripts (before the outcome note is final) · big-task closeout (before any batch commit or handoff) · deep harvests (the shared-intelligence-harvest skill's step-3 miss-sweep is this skill applied to a whole domain).

## Output shape

1. Fixes applied in place (dated addendum or correction notes in the real files).
2. A short delta report: what was found, which ANGLE found it, corrections vs additions, retractions of earlier claims.
3. If a miss looks systematic (same blind spot across sources), say so: that is a first-pass process upgrade, not just a finding.
