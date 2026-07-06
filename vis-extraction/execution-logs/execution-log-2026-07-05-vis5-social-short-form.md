---
type: execution-log
status: draft
created: 2026-07-05
updated: 2026-07-05
venture: vis-extraction
tags: [execution-log, vis-extraction, vis-5, social-reel, short-form]
---

## 2026-07-05 — VIS Phase 5: Social short-form extraction (FB/IG/TikTok reels)

## What Was Built

- `social-pull.sh` — new script that downloads social reels via yt-dlp + transcribes via Whisper, outputting the same markdown transcript shape VIS already consumes
- Phase 0d added to extraction prompt — preflight check for social reel dependencies (yt-dlp + ffmpeg + whisper, host-side)
- Short-form extraction calibration section — depth-calibration for <500 word / <90s reels including mandatory deep-feasibility investigation sub-phase
- Extraction prompt bumped v3.2 → v3.3
- SKILL.md bumped v1.2 → v1.3, social reel routing documented

## Decisions Made

**Created `social-pull.sh` as a separate script** rather than extending `transcript-pull.sh`.

Alternatives considered: Extending transcript-pull.sh with a `social` input type. Rejected because the Whisper dependency (heavy ML model) is qualitatively different from yt-dlp caption scraping, and the Phase 3 sibling handoff explicitly notes coordination risk on transcript-pull.sh.

Why this approach: Clean separation of concerns. The VIS pipeline's Phases 1-7 don't care which pull script produced the transcript — they consume the same markdown shape either way. The split keeps both scripts simple and independently testable.

## End-to-End Test Result

- URL: https://www.facebook.com/reel/1000185322817917
- Creator: Eric Does Ecom (@ericdoesecom)
- Platform: Facebook (public reel, no cookies needed)
- Download: yt-dlp pulled 556KB m4a audio successfully
- Transcription: Whisper base model → 362 words, 21 segments, ~90s
- Deep-feasibility investigation: 4 tools researched via WebSearch, mechanisms reconstructed, evidence URLs cited
- Feasibility ratings: 4 proven (Seedance 2.0, ChatGPT image gen, ElevenLabs STT, Claude scripting), 1 plausible (full chain quality), 1 unsubstantiated (performance claims)
- Operator follow-ups: 6 concrete tasks generated
- Source note written to `second-brain/00_inbox/sources-pending/source-2026-07-05-eric-does-ecom-yapper-ads-seedance.md`

## Dependencies Installed

- ffmpeg (via Homebrew)
- openai-whisper 20250625 (via pip, Python 3.12)
- Both are host-side only; sandbox cannot run this pipeline

## Reusable for Future Apps?

Yes — the social-pull.sh + Whisper pattern is reusable for any short-form video ingestion. The deep-feasibility investigation sub-phase in the extraction prompt is reusable whenever claims need verification beyond the source content.

**Pattern candidate (deferred):** `second-brain/05_shared-intelligence/patterns/pattern-vis-social-reel-whisper-pipeline.md` — to be written at VIS-5 phase-close promotion pass. Tracked in Knowledge Capture Audit item 3 below.

## Knowledge Capture Audit (6-item checklist)

1. **Bugs and failures?** No unexpected failures. yt-dlp pulled the FB reel on first attempt without cookies. Whisper transcription worked cleanly. One Whisper mis-hearing: "Chatchy B.T." for ChatGPT, "claw/clawed" for Claude, "seed dense" for Seedance — expected behavior for brand names in Whisper base model.
2. **Decisions made?** Yes — documented above (separate script vs extending transcript-pull.sh).
3. **Patterns emerging?** Yes — the "download audio → Whisper → standard markdown → existing pipeline" pattern is generalizable beyond social reels (any video source without captions). Deferred to pattern extraction at phase close.
4. **Lessons learned?** Facebook public reels work without cookies (surprising — expected auth to be needed). Whisper base model struggles with brand names but gets the content right. The 4-15s Seedance clip limit is a crucial gap the reel creator doesn't mention — good example of why deep-feasibility investigation matters.
5. **State updates needed?** `02_current-focus.md` — not touched (VIS-5 not in the current focus file). Handoff status flipped to active (done in opening protocol).
6. **Productization-readiness (Productize-tier)?** Not applicable — this is a Capture-only tier run (extending an existing skill, not productizing a new one).
