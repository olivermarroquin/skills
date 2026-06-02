# SURVEY — section shapes + minimum-content discipline

The nine SURVEY sections, in order, with the shape each takes and the minimum content each must include to count as "rendered." If a section is empty (zero in-flight chats, no domain signals), it still appears — with explicit "Nothing here today" prose — rather than getting silently dropped. The orchestrator's value is partly showing what's empty.

## Cross-section voice rules

Every section uses plain prose paragraphs as its synthesis. Bullets are fine for naming the underlying rows (the chats, the decisions, the digests) but the colleague-explaining-over-coffee tone lives in prose. Avoid:

- Bullet walls of 6+ items with no synthesis paragraph
- "Executive summary" wrappers the operator didn't ask for
- Jargon density (always gloss "leverage" / "operator-fatigue heuristic" / "spec-routing coverage" on first use within the report)
- Telegraphic phrasing ("3 in-flight. 4 ready. 6 queued.")

Headings stay verbatim as named below. Don't paraphrase them for cuteness — operator scans on the section names.

## Section 1 — What's actively in flight

**What lives here.** Every Active/in-flight row across master tracker + per-project trackers, with plain-language descriptions of what each chat is doing right now.

**Minimum content.**

- One sentence per in-flight chat naming what it's building and what's blocking-or-not (waiting on operator, waiting on external system, just-in-flight-and-progressing).
- The chat's wikilink to its handoff.
- Estimated remaining hours if known (from the handoff's "Expected duration" minus elapsed).
- Any checkpoint annotations from the chat-resilience convention (`### Checkpoint <timestamp>` blocks in the Notes cell).

**Empty-state shape.** "Nothing in flight right now. The vault is quiet — every chat that started has shipped."

**Voice example.** "Three chats are in flight. The first is `mission-control-dashboard Phase 0` — research across nine stack layers; ~3 hours in, expected 5 total. The second is `client-onboarding-automation Phase 0` — discussion chat walking the discovery shape with you; no deliverable yet, by design. The third is `ads-and-marketing Phase 0` — same shape as the previous, scoped to the 1-month-to-incoming-client urgency."

## Section 2 — What's ready to work on next

**What lives here.** Every Ready-to-spawn row from the master tracker and any project-scoped Ready rows, with the leverage signal (high / medium / low) and any operator-paused notes ("waiting for DataForSEO to unlock" / "queued behind X").

**Minimum content.**

- One sentence per Ready candidate naming what it would ship.
- Why-now from the master tracker's "Why now" cell, plain-language summarized.
- Leverage signal (high / medium / low) with one-line rationale.
- Any operator-paused notes verbatim.

**Empty-state shape.** "Nothing's currently Ready-to-spawn. Either every spawnable chat is already in flight, or every queue is gated on a trigger — see Section 3."

**Voice example.** "Three chats are ready to spawn. `hermes-harness Prework A` ships the Hermes substrate validation — operator-side execution, ~6-8 hours, high leverage because it de-risks the architecture lock before Phase 1 commits. `Prework B` is the Nous Research transparency research — Sonar API queries via the perplexity_sonar.py script, ~2-3 hours, medium leverage. `Prework C` re-runs the load-bearing claims through the Sonar API after Phase 0's Cowork-WebSearch fallback — ~1-2 hours, high leverage because it tightens evidence on the architecture decision."

## Section 3 — What's queued and why

**What lives here.** Tier 2 + Tier 3 queued rows grouped by trigger condition. The grouping is the value — operators want to see "everything waiting for DataForSEO unlocks 2026-06-03" in one place.

**Minimum content.**

- Grouping headers by trigger type ("Waiting on a sibling phase," "Waiting on a calendar date," "Waiting on an external system," "Waiting on operator decision")
- One sentence per queued chat naming what it ships and which group it's in.
- For calendar gates, the specific date.

**Empty-state shape.** "Nothing currently queued. Every candidate is either in flight or Ready-to-spawn."

**Voice example.** "Six chats are queued behind sibling phases: vault-orchestrator Phases 4-6 (waiting on Phase 3 → 4 → 5) plus mission-control-dashboard Phase 1+ (waiting on stack research). Three are queued on calendar gates: competitor-deep-research enhancements (DataForSEO unlocks 2026-06-03), Phase 5 client-seo-onboarding (depends on Phase 4b live), Phase 2 uniqueness 70/30 (15+ pages + Next.js pivot active)."

## Section 4 — Open decisions sitting on the operator

**What lives here.** The master tracker's "Hot decisions sitting on Oliver's plate" section, plain-language framed. Plus any open decisions surfaced in per-project digests' `open-decisions` field.

**Minimum content.**

- One sentence per decision naming what's being decided and what's blocking it.
- The trigger (calendar date, awaiting external info, awaiting operator bandwidth).
- Any deferred-until annotation from the master tracker.

**Empty-state shape.** "No open decisions sitting on you right now — everything's either committed or queued behind a trigger."

**Voice example.** "Six decisions are sitting on you. The Featured.com signup for Ahmad is deferred until you have client-coordination bandwidth — Ahmad still needs to set up the account under his name. DataForSEO Business Account converts automatically 2026-06-03; you approve the charge on signup. Otterly trial → Lite conversion fires 2026-06-08, day before the trial expires. Watchdog Monthly → Annual is a manual decision 2026-06-23 after the 4-week trial results land. HARO Pro upgrade is gated on 90-day free-tier results. Microsoft Clarity Project ID — grab from WP admin, paste into tier-3 credentials."

## Section 5 — What's coming up automatically

**What lives here.** The master tracker's "Scheduled Cowork tasks" table, with each fire date and what the task does in plain language.

**Minimum content.**

- One sentence per scheduled task naming when it fires and what it does.
- The task ID (so the operator can edit/cancel if needed).
- Any post-fire effects (clears a blocker, surfaces a decision, etc.).

**Empty-state shape.** "Nothing scheduled to fire automatically. Every upcoming move is operator-driven."

**Voice example.** "Three tasks fire automatically. On 2026-06-03 at 10am ET, `retry-dataforseo-business-signup` runs — captures credentials once the keelworks.ai domain age clears the 14-day fraud filter; unblocks Phase 4b. Same morning, `build-watchdog-analysis-workflow` builds the auto-ingest pipeline once the first Watchdog weekly report arrives. On 2026-06-08, `otterly-trial-conversion-decision` surfaces the Lite-$29/mo decision the day before the trial expires."

## Section 6 — Recent wins (past 7 days)

**What lives here.** Chats closed in the past 7 days (from the master tracker's "Recently closed chats" section), artifacts shipped, key outcomes.

**Minimum content.**

- Count of chats closed in the window.
- Per-chat one-liner naming what shipped and any standout outcome (a pattern surfaced, a milestone reached, an unblock).
- Aggregate metrics if the per-project digests provide them (artifacts shipped, hours spent).

**Empty-state shape.** "Quiet week — nothing closed in the past 7 days."

**Voice example.** "Eight chats closed in the past 7 days. Phase 2 of vault-orchestrator shipped the master-tracker-aggregator skill (2026-06-01). Phase 4b shipped EV's internal-linking + competitor link-map work (2026-05-31) — three deliverables in one chat. Hermes-harness Phase 0 locked architecture at Option A Path 2 (2026-05-30) after four iterations. Local-model-migration Phase 0 shipped a 10,000-word research report recommending wait-until-October for M5 Ultra. Vault-orchestrator Phase 1 landed the per-project tracker shape. Output-quality-loop Phase 6 closed the project. Across the past 7 days: ~60 artifacts, ~30 hours."

## Section 7 — Domain signals

**What lives here.** `03_domains/` folders with new sources not yet synthesized, lessons drafted but not promoted, patterns at 3+ observations awaiting promotion.

**Minimum content.**

- Per-domain row when the domain has any signal.
- Counts: `N unsynthesized sources` / `M draft lessons` / `K patterns ready for promotion`.
- One-line plain-language description of what the signal would mean if acted on ("4 new SEO sources from past week — could feed a synthesis or get routed via intel-routing PUSH").

**Empty-state shape.** "No active domain signals — every recent source is routed, every lesson is promoted, every pattern is either at <3 observations or already promoted."

**Voice example.** "Three domains have signal. `seo` has 4 unsynthesized sources from the past 7 days (Jono Catliff, Nico, Vasco, Caleb Ulku) — could feed a Phase 2-style cluster synthesis or route via intel-routing PUSH. `automation-systems` has 2 lessons drafted but not promoted (the auto-invoke retrofit lesson, the two-file artifact split). `content-systems` has 1 pattern at 3 observations awaiting promotion (intel-routing convention)."

## Section 8 — Stale signals

**What lives here.** Per-project `_chat-status.md` files older than the stale threshold (14 days default), plus signal-based heuristic flags from `master-tracker-aggregator` DRIFT-DETECT.

**Minimum content.**

- Per-project row for any stale or very-stale digest (or annotated fresh digest).
- The age in days.
- Verdict tag: `stale` (>14d), `very stale` (>28d), `fresh + annotated` (heuristic-only flag).
- The suggested action ("re-run Phase 1 update protocol" / "spot-check the digest against the execution log").

**Empty-state shape.** "Every digest is fresh — no stale signals."

**Voice example.** "All current digests are fresh (within 14 days). Ten projects don't have a digest at all (ai-agency-core, app-factory, dad-businesses, hire-relay, idea-factory, keelworks, legal-toolkit, resume-factory, resume-saas, s-and-h-contracting) — surfaced in the aggregator's projects-without-digest section. Backfilling these is operator-driven; the Phase 1 pattern at `~/workspace/skills/multi-chat-coordination/references/project-status-digest-shape.md` is the shape to mirror."

## Section 9 — Cross-project signals

**What lives here.** Handoffs that affect multiple projects, conventions changes pending rollout, recently-promoted patterns implying downstream application work, multi-project decisions.

**Minimum content.**

- Per-signal row naming the signal type, the projects involved, and the implied downstream work.
- For convention changes: the file path + `updated:` date.
- For pattern promotions: the pattern name + the projects that could apply it.

**Empty-state shape.** "No active cross-project signals. Every change is project-scoped."

**Voice example.** "Two cross-project signals. The intel-routing convention shipped Phase 2 (2026-05-27) — affects all 11 inboxes vault-wide, Phase 3 skill build is queued as a spawnable. The plain-language-conventions canonical doc updated 2026-05-16 — affects every operator-facing output across every project; rollout is ongoing as new chats spawn. No convention changes in the past 7 days, no pattern promotions in the past 7 days requiring downstream application."

## When a section is "rendered"

A section counts as rendered when:

1. The H2 heading is present
2. At least one sentence of synthesis prose exists (even if just the empty-state shape)
3. Underlying rows (if any) are named with wikilinks preserved
4. Voice rules (plain language, no jargon walls) hold

A section that's just `## What's actively in flight` with nothing else is broken. Surface the gap and stop rather than emit a half-rendered section.

## See also

- `~/workspace/skills/vault-orchestrator/SKILL.md` § Mode 1 — the runtime behavior
- `~/workspace/skills/master-tracker-aggregator/references/drift-detection-heuristics.md` — Section 8's underlying heuristics
- `./domain-signal-mining.md` — Section 7's walking logic
- `./cross-project-signal-detection.md` — Section 9's detection rules
- `./plain-language-discipline.md` — voice rules across all sections
