---
type: execution-log
subtype: batch-digest
status: complete
created: 2026-11-20
updated: 2026-11-21
session: vis-p2-gate3-batch-202611200d9e
batch-run: Gate 3 mini-batch (5 URLs, auto mode)
tags: [execution-log, vis-extraction, batch-digest, gate3]
---

# VIS Gate 3 — Batch Digest (2026-11-20)

> **Batch purpose:** Live five-URL mini-batch run to validate VIS Phase 2 (four-signal auto-proceed gate + earned autonomy). Processed 2026-11-20 through 2026-11-21.

---

## Batch result: 1 auto-shipped / 4 parked / 0 skipped

| # | URL | Creator | Title | Status | Signal 3 | Signal 4 | Escalation-log row |
|---|---|---|---|---|---|---|---|
| 1 | https://www.youtube.com/watch?v=aaTqimE1J9w | Nate Herk | "I Turned Grok Bot Into a 24/7 GTA 6 Clipping Machine" | **parked** | FAIL (delta:4) | FAIL (exit 1) | YES — BLOCKING-catch |
| 2 | https://www.youtube.com/watch?v=4hKJ9X6rGFo | Nate Herk | "Build & Sell Grok Bots (2 Hour Course)" | **parked** | FAIL (delta:4) | FAIL (exit 1) | YES — advisory only |
| 3 | https://www.youtube.com/watch?v=to4Me479A2s | Rob Shocks | "Grok Bot + Claude Code, Why is Everyone Switching to This?" | **parked** | FAIL (delta:2) | FAIL (exit 1) | YES — BLOCKING-catch fixed |
| 4 | https://www.youtube.com/watch?v=zfEokffzwgk | Wesley Hoang | "Claude vs Grok: The Only 2 AIs I Use to Run My 7-Figure Business" | **parked** | PASS (delta:0) | FAIL (exit 1) | NO — advisory only |
| 5 | https://youtube.com/shorts/hc34VXRoX7s | Nate Herk | "Claude Can Run a GTA 6 Clipping Channel on Autopilot" | **auto-shipped** | PASS (delta:0) | PASS (exit 0) | NO — advisory only |

---

## Note file paths

| # | Note path |
|---|---|
| 1 | `second-brain/00_inbox/sources-pending/source-2026-11-20-nate-herk-ai-automation-grokbot-24-7-gta6-clipping.md` |
| 2 | `second-brain/00_inbox/sources-pending/source-2026-11-20-nate-herk-ai-automation-build-sell-grok-bots-2-hour-course.md` |
| 3 | `second-brain/00_inbox/sources-pending/source-2026-11-20-rob-shocks-grokbot-claude-code-why-switching.md` |
| 4 | `second-brain/00_inbox/sources-pending/source-2026-11-21-wesley-hoang-claude-vs-grok-7-figure-business.md` |
| 5 | `second-brain/00_inbox/sources-pending/source-2026-11-20-nate-herk-claude-gta6-clipping-autopilot-short.md` |

**Shipped note (URL 5):** `second-brain/00_inbox/sources-pending/source-2026-11-20-nate-herk-claude-gta6-clipping-autopilot-short.md` — `status: ingested`

---

## Per-URL four-signal detail

### URL 1 — Nate Herk GTA6 Clipping (12:28)

- **Signal 1:** APPROVE-WITH-NOTES / BLOCKING-catch — tool URLs not transcript-sourced, "In plain English" section stub, squeeze-delta:4 without delta table. All fixed before park.
- **Signal 2:** advisory-pass-pending (by design — OQL Mode 5 not wired)
- **Signal 3:** FAIL — squeeze-delta:4 — missed on first pass: Kenji's name as the agent, CEO-framing prompt technique as named technique, flashback-hook format (plays best moment first then rewinds), Lacy clip explicitly used as the hook example
- **Signal 4:** FAIL — exit 1, 6 flags. On review: 10k/Lacy's/Kenji's/Google-Doc covered; SOP = ad segment; Python-cmd marginal miss
- **Transcript:** `skills/vis-extraction/cache/transcript-2026-11-20-152740-nate-herk-ai-automation-i-turned-grok-bot-into-a-24-7-gta-6-.md`

### URL 2 — Nate Herk 2-Hour Course (1:45:41)

- **Signal 1:** APPROVE-WITH-NOTES / advisory only — 9 catches: revenue "~$5M" vs "just under $5M"; Granola/Fathom URLs not-stated; bot-templates env-var caveat missing; OpenClaw missing from tools. All fixed before park.
- **Signal 2:** advisory-pass-pending
- **Signal 3:** FAIL — squeeze-delta:4 — missed: agent label field (agents have a label/role field in Grokbot UI), real executive names Klouse/Dan/Becky/Chandler (shown in demo), agentic loop as explicit term, interrupting agents technique
- **Signal 4:** FAIL — exit 1, 94 flags. On review: most flags = auto-caption variants (Grockbots/Claus/Grockpot), fictional demo details, common words. Real misses: OpenClaw (added), Granola/Fathom URLs (corrected to not-stated)
- **Transcript:** `skills/vis-extraction/cache/transcript-2026-11-20-152742-nate-herk-ai-automation-build-sell-grok-bots-2-hour-course.md`
- **Dense-chunked:** yes, 26,255 words, 29 segments

### URL 3 — Rob Shocks Switching (16:03)

- **Signal 1:** APPROVE-WITH-NOTES / BLOCKING-catch — metric "reverts fell 40%" vs transcript "share that had to be reverted fell by more than 40%." Fixed before park. Also advisory: Docker URL listed as company domain, not architecture document URL.
- **Signal 2:** advisory-pass-pending
- **Signal 3:** FAIL — squeeze-delta:2 — missed: Open Code as a named tool (mentioned once as alternative to Claude Code), Grokbot's ability to unblock sub-agents via documentation connections
- **Signal 4:** FAIL — exit 1, 21 flags. All auto-caption artifacts (Entropic=Anthropic, Pystack=Pstack, Teo=Theo), off-topic end-of-video Patrick Stewart tribute, cross-promotions. Real misses: none
- **Command:** `python3 scripts/coverage-diff.py "cache/transcript-2026-11-20-154858-rob-shocks-switch-dimension-grok-bot-claude-code-why-is-ever.md" "/Users/olivermarroquin/workspace/second-brain/00_inbox/sources-pending/source-2026-11-20-rob-shocks-grokbot-claude-code-why-switching.md"` → exit 1
- **Transcript:** `skills/vis-extraction/cache/transcript-2026-11-20-154858-rob-shocks-switch-dimension-grok-bot-claude-code-why-is-ever.md`

### URL 4 — Wesley Hoang 7-Figure Business (13:15)

- **Signal 1:** APPROVE-WITH-NOTES / advisory only — Apple background over-specificity (note said "Apple Face ID team" vs transcript's "built systems for companies like Apple"); blog cadence body-picks-a-side (transcript says both "per week" and "per day"). Both fixed before park.
- **Signal 2:** advisory-pass-pending
- **Signal 3:** PASS — squeeze-delta:0
- **Signal 4:** FAIL — exit 1, 14 flags. All noise: XYZ/TLDR/Remember (transitions), B-roll (minor training example), Slacks = Slack (covered), 8 story-cue hits (hypothetical examples). Real misses: none
- **Transcript:** `skills/vis-extraction/cache/transcript-2026-11-20-154858-wesley-hoang-claude-vs-grok-the-only-2-ais-i-use-to-run-my-7.md`

### URL 5 — Nate Herk Short (0:51)

- **Signal 1:** PASS — 3 advisory catches: drops "about" from "$1.13" (fixed to "~$1.13"), "Platform" vs "Instagram" (fixed), editorial sentence "scale most new accounts won't hit" (reworded to attribute to Nate's math). All fixed.
- **Signal 2:** advisory-pass-pending
- **Signal 3:** PASS — squeeze-delta:0
- **Signal 4:** PASS — exit 0 CLEAN
- **Command:** `python3 scripts/coverage-diff.py "cache/transcript-2026-11-20-154859-nate-herk-ai-automation-claude-can-run-a-gta-6-clipping-chan.md" "/Users/olivermarroquin/workspace/second-brain/00_inbox/sources-pending/source-2026-11-20-nate-herk-claude-gta6-clipping-autopilot-short.md"` → exit 0
- **Transcript:** `skills/vis-extraction/cache/transcript-2026-11-20-154859-nate-herk-ai-automation-claude-can-run-a-gta-6-clipping-chan.md`
- **AUTO-SHIPPED** — all four signals pass

---

## Escalation-log entries

Three rows appended to `second-brain/_meta/escalations/vis-extraction-escalation-log.md` (rows 1-3). First real firings of the escalation log (previously empty). First-batch review status: **open** — operator review of these rows pending.

---

## Signal 4 pattern observed

Coverage-diff exit 1 on all 4 parked notes; real misses found only on URL 2 (OpenClaw + Granola/Fathom URLs — both fixed). URLs 1, 3, 4 had exit 1 with 0 real misses — all flags were auto-caption artifacts, story-cue hits, or cross-promotions. URL 5 (51-second Short, low word count, clean extraction) → exit 0. See CR-281 in catch register for the recommended artifact-tolerant matching enhancement.

---

## Operator parked-note queue

4 parked notes are the first-batch review queue per design. Operator reviews and ships or discards each. The escalation-log's `first-batch-review-completed` field remains open until operator reviews the 3 BLOCKING-catch rows.
