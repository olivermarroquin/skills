---
name: vis-extraction
description: Extract structured intelligence from videos, articles, transcripts, and other long-form content into Oliver's Knowledge OS vault. Triggers on phrases like "ingest this video," "extract this URL," "process this transcript," "pull and extract from a URL," "analyze this article," "ingest this source," "run VIS on this," or any time the user provides a YouTube URL, web article URL, or local transcript file and wants a structured source note plus extracted artifacts (tools, tactics, opportunities, content ideas) written into the second-brain vault. Also use when the user mentions adding a video/article/talk to their vault, or when they paste a URL with no other instruction in a Knowledge OS context. This is the primary path for converting external content into vault artifacts.
---

# VIS Extraction Skill (v1.2)

The Video Intelligence System (VIS) extraction skill. Wraps the `transcript-pull.sh` script and the v3.2 extraction prompt into a single workflow. Pull a transcript, run extraction, write structured notes to the vault.

**Critical behavior (read this before anything else):**
- **Cache and dedup are first-class.** Before pulling a transcript, check the cache. Before running an extraction, check whether the source already exists in the vault. Don't silently re-extract or overwrite the user's calibrated work.
- **Sandbox network may be limited.** If the sandbox can't reach a URL, route the pull to the user's host machine — don't fake the work.
- **Stop at the review gate by default.** Training mode is the default. Only skip review when the user explicitly says "auto."
- **Multi-turn collaboration mode is available and recommended for batch ingestion.** This skill supports two modes: single-agent (one agent does everything; faster per source) and multi-turn (executor agent + review agent + operator collaboration; higher quality on batch ingestion). Both modes are first-class. See "Multi-turn collaboration protocol" below for when to use which.

## Multi-turn collaboration protocol

This skill supports **multi-agent collaboration** as a first-class mode alongside single-agent execution. When invoked, the work can split across three roles depending on the configuration.

### Role definitions (agent-agnostic)

- **Executor agent** — the agent that does the actual file operations: pulls transcripts, reads vault state, drafts notes, writes files. Makes calibration and discipline decisions during execution (not blind execution; the executor reads vault state, applies extraction-discipline precedents, and surfaces judgment calls at approval gates). In current configuration this is typically Cowork. Could be any other agent with vault file-system access (local agent, other cloud agent, etc.).
- **Review agent** — the agent the operator collaborates with to draft prompts for the executor, validate executor outputs, surface concerns, and produce approval prompts. Does NOT execute file operations directly. In current configuration this is typically a web-UI Claude chat. Could be any other agent (local agent, other cloud agent).
- **Operator** — the human in the loop. Decides at approval gates, commits to git, makes final calls on contested points, transcribes outputs between agents.

The skill's behavior depends on what configuration is invoking it. If the executor is invoking directly (no review agent in the loop), it follows the "single-agent mode" path. If the executor is being driven by a review agent + operator combination, it follows the "multi-turn mode" path.

### When to use which mode

**Single-agent mode is appropriate when:**
- One-off ingestion of a single source
- Low-stakes sources where rigorous extraction-discipline review isn't required
- Operator-attention budget is constrained
- Operator has high trust in executor's calibration on the current cluster
- Speed matters more than rigorous quality

**Multi-turn mode is appropriate when:**
- Batch ingestion (5+ sources in a session)
- Sources where extraction-discipline matters (substrate-research lane, opening new clusters, sources that may trigger pattern promotions)
- Operator wants pressure-testing of executor's calibration
- The pattern landscape is approaching promotion thresholds where math accuracy matters
- Operator has the attention budget for multi-turn overhead

**Operator-attention budget reality check:** Multi-turn mode consumes meaningfully more operator-attention per source than single-agent mode. The dominant cost is transcription overhead (copying outputs between agents), which accounts for roughly 30-40% of the per-source time. Variance is high — source complexity, batch position, time of day, current cognitive load all affect actual minutes per source. Budget by sessions not minutes: a batch of 10 sources in multi-turn mode is typically a multi-session effort (across hours or across days), not a single continuous session. Single-agent mode for the same batch is one focused session.

### Single-agent mode workflow

When invoked without a review agent in the loop:

1. Executor runs Phases 0-5 autonomously, applying extraction-discipline precedents (see "Extraction-discipline precedents" section below).
2. Executor stops at Phase 6 review gate, presents structured summary, waits for operator approval.
3. Executor runs Phase 7 + 8 after approval.
4. Executor reports completion to operator.
5. Operator handles triage + commit manually.

This is the standard standalone path. Use when there's no review agent in the loop.

### Multi-turn mode workflow

When a review agent is present, the work flows through 5 phases per source. Each phase has explicit operator-transcription steps where the operator copies output from one agent to another. Transcription is the dominant cost driver of multi-turn mode — see budget callout above.

#### Phase A — Source intake and prompt drafting

- Operator provides URL + optional cluster-context flag to review agent (e.g., "this is for substrate research," "this is ideas-capture-shape," "this is the 4th source in a Hermes-cluster batch")
- Review agent drafts a Phase 0-6 prompt for executor agent including: URL, source context (which source number in the current batch, what cluster framing operator flagged, ideas-capture-shape vs continuation-cluster), Phase B precedent reminders (extraction-discipline precedents that apply — see "Extraction-discipline precedents" section), cluster-fit pre-check instructions, new-direction-surfacing reminder if applicable, standard pipeline instructions, stop-at-Phase-6 instruction
- Operator transcribes prompt from review agent to executor agent

#### Phase B — Phase 6 review cycle

- Executor runs Phases 0-6; stops at Phase 6 review gate; surfaces structured output (tier reasoning, cross-source pattern candidates with mechanism-differentiation analysis, Phase B coverage gap status, relevance tagging proposal, manual-flagged novel proper nouns, alternative writeset shapes if applicable)
- Operator transcribes Phase 6 output from executor to review agent
- Review agent pressure-tests executor's Phase 6 output; flags extraction-discipline violations (premature abstraction, one-creator-only spawn temptations, over-fragmentation candidates, cross-creator counting math errors, cluster-fit mismatches); drafts Phase 7 approval prompt (approve as-is / modify / reject)
- Operator transcribes Phase 7 approval prompt from review agent to executor

#### Phase C — Phase 7 execution

- Executor runs Phase 7; writes files (source note in inbox, supporting notes in canonical locations, task notes if approved, enhancement sections on existing notes, queue-tail amendment); reports completion with file-ops summary
- Operator transcribes Phase 7 completion report from executor to review agent

#### Phase D — Triage cycle

- Review agent validates Phase 7 output landed correctly; drafts triage proposal prompt for executor
- Operator transcribes triage proposal prompt from review agent to executor
- Executor proposes frontmatter values (tier, relevance, actionability, monetization) + destination folder + execution recommendation; stops at triage approval gate
- Operator transcribes triage proposal from executor to review agent
- Review agent validates or modifies triage proposal; drafts triage-apply prompt for executor (revised if modifications needed)
- Operator transcribes triage-apply prompt from review agent to executor
- Executor applies triage; updates frontmatter, moves source note from inbox to canonical destination, appends decision-archaeology entry; reports completion
- Operator transcribes completion from executor to review agent

#### Phase E — Commit and continue

- Review agent drafts commit command (verbose-structured Phase-B-style commit preserving decision archaeology — see "Commit message template" below)
- Operator executes commit manually
- Operator signals next URL to review agent — loop continues

### Why this protocol exists

Phase B (May 2026, 35 sources) established that single-agent extraction without review-agent pressure-testing produces compression-loss and discipline-drift on substantial batch ingestion runs. The review-agent role catches extraction-discipline violations the executor misses (premature abstraction, one-creator-only spawn temptations, over-fragmentation, cross-creator counting math errors). The operator-in-loop approval gates preserve operator-discipline on tier-calibration and spawn-shape decisions.

### Mode switching mid-source

The operator may need to switch modes within a single source's processing. Most common case: Phase 0-5 ran in single-agent mode (operator running executor directly) but operator wants Phase 6 review with a review agent in the loop because the Phase 6 output surfaced contested decisions.

To switch into multi-turn mid-source: operator copies executor's current state output to review agent + tells review agent which phase the executor stopped at. Review agent picks up from that point with appropriate context. The skill doesn't enforce strict mode-purity within a source.

To switch out of multi-turn mid-source: operator tells executor "skip the review-agent loop for the remainder of this source; complete Phase 7 and triage with standard discipline; default to conservative spawn-shape choices when in doubt."

### Mode switching mid-batch

The operator may switch from multi-turn to single-agent mid-batch when review-agent attention is exhausted but ingestion needs to continue. The transition: operator tells executor "skip the review-agent loop for the remaining sources; run Phases 0-7 with standard discipline; surface anything genuinely contested at the Phase 6 gate; default to conservative spawn-shape choices when in doubt."

Operator may also switch from single-agent to multi-turn mid-batch if quality concerns surface or pattern landscape approaches promotion thresholds where rigorous review matters. The transition: operator opens a review agent chat with appropriate project knowledge (see "Project knowledge management for review agent" below), seeds it with current batch context, and resumes batch ingestion in multi-turn mode for remaining sources.

### Fresh-context discipline for review agent

Review agent context fills up over substantial batches. Phase B taught us that a single review agent chat can carry roughly 8-15 sources of substantive Phase 6 review work before context-management overhead starts degrading review quality. Specific symptoms of context fatigue:

- Review agent starts repeating itself across sources
- Review agent's responses become less specific to current source context
- Review agent drifts on extraction-discipline precedents established earlier in the batch
- Review agent's prompt drafts become more generic and less calibrated to the specific source

When these symptoms appear, open a fresh review agent chat. Seed the new chat with: current-goals.md, build plan document (if active), the queue-tail amendments from the prior chat capturing batch state, sample source notes from the current cluster, and the relevant tool notes / pattern notes the batch is touching. The fresh review agent picks up batch ingestion with restored review-quality.

This pattern is itself a Phase B precedent: substantial batch ingestion benefits from periodic review-agent context refresh, similar to how this skill itself recommends Phase 0 stateless re-runs rather than session-level memoization.

### Project knowledge management for review agent

The review agent's quality depends on what's in its project knowledge. Phase B established a minimum set of files the review agent needs to do its job well:

**Always include:**
- `_meta/current-goals.md` — operator-level goals + relevance calibration
- `_meta/scoring-rubric.md` — canonical scoring definitions
- Active build plan document if one exists (e.g., `goal-a-expanded-build-plan.md`) — operator-decision-architecture context
- `01_ai-operating-system/roadmap/phase-3-plus-queue.md` — deferred items + queue-tail observations
- `01_ai-operating-system/master-system-map.md` — architectural context

**Include for batch ingestion in a specific cluster:**
- Sample source notes from the cluster (2-3 canonical examples)
- Sample pattern notes from the cluster (2-3 representative tactics)
- Relevant tool notes the batch is touching (e.g., `tool-hermes.md` if batch is substrate-cluster-on-Hermes)

**Include when relevant:**
- Knowledge architecture context (`knowledge-os-architecture-and-expansion-system.md`, `knowledge-os-obsidian-system-builder.md`)
- VIS system spec (`video-intelligence-system.md`)
- Closed tier-1 tasks that bound decisions (e.g., the ToS task closure if substrate work is in scope)

**Don't include:**
- All vault source notes (too much; executor handles per-source detail)
- All pattern notes (too much; executor handles)
- Tool notes unrelated to current batch
- Project files for projects not relevant to current batch

The principle: upstream-context + meta-artifacts + canonical spot-check samples. Not a full vault replica. Aim for ~10-15 files in project knowledge, weighted toward orientation and calibration material rather than per-source detail.

### What the review agent SHOULD do

- Draft well-structured Phase 0-6 prompts for executor with all relevant context
- Pressure-test executor's Phase 6 output honestly (don't rubber-stamp; don't manufacture problems)
- Flag extraction-discipline violations explicitly (premature abstraction, etc.)
- Calibrate scoring honestly per the calibration framework (see "Honest scoring calibration" section below)
- Surface cluster-fit mismatches if executor missed them
- Draft Phase 7 approval prompts that preserve operator-discipline decisions
- Draft triage prompts that match the source's actual yield, not generic templates
- Draft verbose-structured commit messages preserving decision archaeology
- Recognize own context fatigue and surface it to operator before review-quality degrades

### What the review agent SHOULD NOT do

- Execute file operations directly (that's the executor's role)
- Run transcript pulls directly (that's the executor's role)
- Override operator decisions at approval gates
- Generate content the executor will write (the review agent shapes prompts; the executor produces content)
- Pretend to approve outputs the operator hasn't approved
- Continue past stop-conditions in this skill or in the extraction prompt

### What the operator's role looks like

The operator's role in multi-turn mode is primarily decisional + transcriptive:

- Decides at approval gates (Phase 6, Phase 7, triage, commit)
- Transcribes prompts/outputs between agents (review agent ↔ executor agent)
- Resolves contested decisions when review agent surfaces them
- Commits to git after each source's triage completes
- Provides cluster-context flags at the start of each source's ingestion
- Decides when to switch between multi-turn and single-agent modes (mid-source or mid-batch)
- Decides when to refresh review agent's context (open fresh chat)
- Manages review agent's project knowledge per the guidance above

The operator does NOT need to validate every Phase 6 detail — that's the review agent's job. The operator does need to spot-check that the dance is producing sensible outputs and intervene when discipline is drifting.

## Extraction-discipline precedents

Phase B (May 2026, 35 sources) established a set of precedents for handling specific source-shape patterns. These bound how the executor calibrates writeset shape (Option A standard / Option B minimal / Option C minimal-with-promotion / etc.) and how the review agent pressure-tests executor outputs. Apply these precedents whenever the source-shape matches the trigger conditions.

For vault-curation-level precedents — premature-abstraction, one-creator-only-no-spawn, over-fragmentation, cross-creator counting, cross-substrate-independent-arrival, retroactive-precedent-application, new-cluster-opening, etc. — see **Skill 2: Vault knowledge-curation discipline**. This section covers the extraction-workflow-specific precedents that apply during Phases 1-7 of an extraction run. Where these precedents reference vault-curation discipline (e.g., "cross-creator counting rules apply here"), the reference points to Skill 2 as the authoritative source for those rules.

### Path-B variant 1 — Same-creator-diminishing-returns

**When it applies:** A creator already canonical in the vault for a particular pattern publishes a new source that extends or revisits their existing canonical articulation, but doesn't introduce substantively novel architectural commitment.

**How to recognize:** Look for these signals during Phase 1 context-gathering:
- The source's creator already has 1+ canonical pattern attribution in vault
- The new source is the creator's Nth published source on the same architectural area (N ≥ 2)
- The new source extends rather than fundamentally repositions the creator's earlier articulation
- Most content reads as reinforcement-with-incremental-extension rather than novel-commitment

**What to do:** Apply minimal writeset shape. Don't spawn new tactic notes for incremental extensions of patterns already canonical from this creator; instead, append same-creator-extension sections to the creator's existing canonical tactic notes. Sources-array updates on the existing tactic; no math movement on pattern promotion (same-creator-extension doesn't add cross-creator weight per Skill 2's cross-creator counting rules).

**Phase 6 net suggestion:** Tier-2 strict-minimal writeset (~3-5 file ops): source note + sources-array updates on existing tactics + queue-tail amendment. NO new tactic spawns. NO new tool notes unless source introduces a genuinely new tool that meets standard spawn criteria independently.

**Examples from Phase B:**
- Source 11 Cole Medin headless-loop articulation (Cole's 2nd Phase B source; extended his canonical agent-harness-pattern from source 4)
- Source 21 Nick Saraev auto-research tutorial (Nick's 2nd Phase B source; teaching/extending his canonical CLAUDE.md-4-component-framework from source 20)

**Discipline reminder:** Same-creator extension is real signal — the creator's iterating their thinking matters. But same-creator iteration doesn't satisfy cross-creator-independent-arrival precedent; pattern promotion math requires multiple independent canonical creators. See Skill 2 for the full cross-creator counting rules.

### Path-B variant 2 — Same-feature/different-creator-angle

**When it applies:** A creator NOT yet canonical for a particular pattern publishes a source that teaches the same feature or operates in the same domain as patterns already characterized in vault from other creators. The new creator's angle is different (different use case, different substrate, different scope) but the underlying architectural pattern overlaps with existing canonical patterns. Crucially, this creator ARTICULATES THEIR OWN ARCHITECTURAL CHOICE on top — they're not just teaching what another creator built.

**How to recognize:** Look for these signals:
- The source's creator is NEW to vault for this pattern (or has limited vault presence)
- The source teaches a feature/domain already canonically covered (e.g., another Hermes-substrate tutorial when Hermes is already substantially-characterized)
- The new creator brings a different angle: different specific use case, different substrate-implementation, different scope of application
- The new creator makes architectural choices of their own (they BUILT something using the pattern, even if the pattern itself was articulated by someone else)
- The underlying architectural pattern is the same; the contextual application differs

**What to do:** Tier-2 selective writeset. Source note + sources-array updates on existing tactics that the source's content reinforces (cross-creator evidence for pattern-promotion math IS appropriate here, unlike Path-B variant 1, because the new creator made their own architectural choices). Spawn new tactic notes ONLY if the new creator's angle surfaces a substantively novel architectural commitment that doesn't fold into existing tactic definitions.

**Phase 6 net suggestion:** Tier-2 selective writeset (~6-9 file ops). Cross-creator-counting math applies: if this creator's articulation is canonical-quality (their own architectural choice, not synthesizer/cataloger shape and not teaching-creator shape), it counts toward pattern promotion math. See Skill 2 for the cross-creator counting rules including the strict reading on synthesizer vs canonical distinction.

**Examples from Phase B:**
- Source 12 Nate Herk coder-reviewer multi-agent (Nate built his own coder-reviewer setup; advanced supervisor-multi-agent pattern to threshold)
- Source 13 AI Jason structured-output (AI Jason built his own typed-extraction implementation; different angle on already-2/3 structured-output pattern)
- Source 14 Devsplainers + Source 17 David Ondrej + Source 19 Sharbel A. + Source 22 Jay E + Source 33 Greg+Imran (all built their own Hermes-substrate setups; reinforcement-with-canonical-creator-articulation)

**Discipline reminder:** "Different creator teaches the same thing" is not automatic cross-creator-counting weight. The creator must articulate their OWN architectural choice, not just synthesize or compile what other creators are doing, and not just teach a framework canonically articulated by another creator (which is the strict-minimal precedent's domain, see below). Use review-agent pressure-testing to distinguish canonical-creator-articulation from synthesizer-shape and from teaching-creator-shape. The cross-creator counting rules in Skill 2 give the full distinction.

### Substrate-tutorial-archive precedent (Krish-shape)

**Naming note:** This precedent was informally called "Skip-Phase-7 precedent" during early Phase B discussions, but that name is misleading — Phase 7 still runs in this precedent, just with minimal output. Renamed to reflect what actually happens: the source becomes a tutorial-archive reference for the substrate without driving operator-actionable artifact spawns.

**When it applies:** A source is substrate-tutorial-shape (teaching how-to-use-substrate-X) AND the operator is not adopting substrate X. The source content is reference material for the substrate's existence and shape, but doesn't drive operator-actionable outcomes.

**How to recognize:** Look for these signals:
- Source is creator-teaching-substrate (e.g., "here's how I built X on OpenClaw")
- Substrate is one the operator has explicitly NOT chosen (or has chosen against)
- No novel architectural pattern beyond standard substrate-tutorial content
- Operator-actionability is fundamentally low because substrate is not in operator's adoption path

**What to do:** Tier-3 minimal writeset (~3 file ops): source note in inbox + sources-array updates on existing substrate-tool note (capturing this source as one more example of substrate-X-being-taught) + queue-tail amendment. Phase 7 RUNS with minimal output — source note still gets written; substrate-tool note still gets sources-array update. The minimization is on spawn-shape: NO new tactics, NO new tool notes, NO new tasks. The source-note body captures the substrate-tutorial content for future reference; the lack of supporting artifacts reflects operator-non-adoption-stance.

**Phase 6 net suggestion:** Substrate-tutorial-archive minimal writeset. Surface to operator: "this source is substrate-tutorial-shape for a substrate operator isn't adopting; recommend minimal writeset capturing source as substrate-tutorial-archive material only; Phase 7 runs but with no new spawns."

**Examples from Phase B:**
- Source 10 Krish OpenClaw tutorial (operator not adopting OpenClaw at time; substrate-tutorial-archive only)

**Discipline reminder:** This precedent doesn't apply when the operator IS adopting the substrate (then substrate-tutorial sources are operator-experience evidence and warrant tier-2 selective writeset per Path-B variant 2 Hermes-cluster pattern). It also doesn't apply when the source surfaces novel architectural patterns beyond standard substrate-tutorial content — those tactics may warrant spawning regardless of substrate-adoption status.

### Strict-minimal precedent (cross-creator teaching-only)

**When it applies:** A source's creator is teaching a framework that's already canonical in vault from a DIFFERENT creator. The new creator is operating purely as a teacher/explainer of someone else's canonical articulation — they're not building on top of it, not extending it with their own architectural choices, not adapting it to a different domain. Pure pedagogical amplification.

**Critical distinction from Path-B variant 1:** Path-B variant 1 applies when a creator teaches their OWN canonical framework (creator A teaching framework-A). Strict-minimal applies when a creator teaches SOMEONE ELSE'S canonical framework (creator B teaching framework-A where framework-A is canonical from creator A).

**Critical distinction from Path-B variant 2:** Path-B variant 2 applies when a new creator makes their OWN architectural choices using an existing pattern (creator B builds their own version of framework-A). Strict-minimal applies when the creator doesn't make their own choices — they're just teaching.

**How to recognize:** Look for these signals:
- The framework being taught is already canonical in vault from creator A
- The current source's creator B is teaching framework-A rather than building on top of it
- Creator B doesn't articulate their own architectural choices that extend or recombine framework-A
- The source's value is pedagogical-amplification of existing canonical content
- If you had to attribute the architectural choices in this source, they'd attribute to creator A, not creator B

**What to do:** Tier-2 strict-minimal writeset (~3-4 file ops). Source note + sources-array updates on the canonically-attributed tactic notes (capturing creator B as teaching-creator-not-canonical-creator) + queue-tail amendment. NO new tactic spawns even if pattern reaches threshold via this source — teaching-creator doesn't count for cross-creator-arrival math per Skill 2's cross-creator counting rules.

**Phase 6 net suggestion:** Strict-minimal writeset. Surface to operator: "this source is teaching-creator on canonically-covered framework (creator B teaching creator A's framework); recommend strict-minimal writeset with sources-array updates only on the canonically-attributed tactics; teaching-creator doesn't add cross-creator weight per Skill 2 cross-creator counting rules."

**Examples from Phase B:**
- Source 23 David Ondrej auto-research tutorial (David teaching auto-research patterns canonically articulated by Nick Saraev source 20 and Karpathy source 24; David didn't make his own architectural choices on top, so strict-minimal applied)

**Discipline reminder:** Strict-minimal is different from Substrate-tutorial-archive. Substrate-tutorial-archive applies when operator-actionability is fundamentally low due to non-adoption of the substrate being taught. Strict-minimal applies when operator-actionability may be high but the source's content doesn't add to vault's canonical pattern attribution because the creator is teaching someone else's framework. Both produce minimal writesets but for different reasons.

### Cluster-fit pre-check

**When it applies:** Always. At the start of every extraction, before Phase 6, verify the source's content shape matches the cluster the operator flagged at intake.

**How to recognize:** Operator-flag-fidelity check at Pre-Phase-6:
- Operator flagged source as belonging to cluster X (substrate-cluster, content-cluster, ideas-capture-shape, continuation-cluster, etc.)
- Source content as analyzed in Phases 1-5 actually belongs to cluster Y
- Cluster X ≠ cluster Y

**What to do:** Surface the mismatch honestly at Pre-Phase-6 gate. Do NOT force-fit content into operator-flagged cluster. Do NOT silently re-cluster without operator approval. Specifically:

1. State the operator-flag clearly: "Operator flagged this source as <cluster X>"
2. State the content-shape clearly: "Source content as analyzed actually belongs to <cluster Y> because <specific evidence>"
3. Surface the cluster-correction proposal: "Recommend re-clustering this source to cluster Y for filing and pattern-attribution purposes"
4. Wait for operator approval before proceeding to Phase 6 with corrected cluster framing

**Phase 6 net suggestion:** Apply normal tier-calibration to the corrected cluster, NOT the operator-flagged cluster. The cluster-correction itself doesn't affect tier; tier reflects content + operator-relevance per scoring rubric.

**Examples from Phase B:**
- Sources 27, 28, 29 (operator flagged as Obsidian-with-AI cluster; content was substrate/agent-architecture cluster; cluster-correction applied 3 times consecutively)

**Discipline reminder:** Cluster-fit mismatch is operator-discipline honesty, not failure. Operator flags based on initial intake context (URL title, channel name, etc.); content-shape may differ from intake-impression. Honest correction at Pre-Phase-6 prevents miscategorized filing + miscalibrated pattern attribution.

### New-direction-surfacing protocol

**When it applies:** A source's content opens new cluster territory, affects operator goals in unexpected ways, or surfaces a pattern that suggests a new tier-1 task is warranted.

**How to recognize:** Look for these signals during Phase 1-5 analysis:
- Content doesn't fit any existing vault cluster cleanly (opens new cluster)
- Content surfaces operator-decision-points the operator hasn't considered (e.g., new tier-1 task shape, new build-plan revision trigger)
- Content connects multiple existing clusters in a way that suggests new architectural pattern
- Content reveals a gap in operator's current goal framing

**What to do:** Surface prominently at Phase 6 review gate. Don't bury new-direction observations in standard tier-reasoning output. Specifically:

1. Lead the Phase 6 output with the new-direction observation: "New-direction surfacing: <specific observation>"
2. State explicitly what operator-decision the new direction would require: "This would warrant <new tier-1 task / build-plan revision / new cluster opening / etc.>"
3. State explicitly what would NOT change if operator proceeds with standard tier-reasoning: "If operator proceeds with standard tier-2 selective writeset without acting on the new direction, the source still lands; the new-direction observation is preserved in source-note body but not acted on operationally"
4. Wait for operator decision before proceeding to Phase 7

**Phase 6 net suggestion:** Standard tier-calibration applies to the source content itself. The new-direction observation is meta to the writeset — it's a signal to operator about strategic implications, not a writeset-shape modifier.

**Examples from Phase B:**
- Source 25 The Augmented vault-as-data-lake (new-direction: opened agent-substrate-as-MCP-backend pattern; first cross-substrate-independent-arrival promotion)
- Source 30 Nate Herk Paperclip (new-direction: opened orchestration meta-layer dimension; expanded substrate-decision matrix from 4-substrate-runtime to 4-substrate-runtime × 2-orchestration-layer = 8 combinations)
- Source 31 Cole LLM-knowledge-bases (new-direction: opened memory-architecture sub-layer)
- Source 35 Dave Nick YouTube faceless-AI (new-direction: opened content/video-intelligence cluster as first content-cluster source in Phase B)

**Discipline reminder:** New-direction-surfacing is not tier-inflation justification. A source can surface a substantial new direction AND be tier-3 minimal in writeset shape (e.g., source 35 was tier-3 minimal despite opening a new cluster). Honest scoring applies cluster-agnostically per Phase B's new-cluster-opening discipline (see Skill 2 for the new-cluster-opening precedent; see "Honest scoring calibration" section below for the calibration framework that operationalizes honest scoring during extraction).

### When precedents conflict

If multiple precedents seem to apply, resolve by precedence order:

1. **Cluster-fit pre-check first** — always run Pre-Phase-6. If cluster-correction needed, apply before other precedents.
2. **Substrate-tutorial-archive next** — if substrate-tutorial + operator-not-adopting, apply this precedent and skip the rest.
3. **Strict-minimal next** — if teaching-creator on someone else's canonical framework (no own architectural choices), apply this precedent.
4. **Path-B variant 1 next** — if same-creator-extension shape, apply this precedent.
5. **Path-B variant 2 last** — if same-feature/different-creator-angle shape with own architectural choices, apply this precedent.
6. **New-direction-surfacing always** — orthogonal to other precedents; surface in Phase 6 output regardless of writeset shape.

If genuinely ambiguous (source straddles multiple shapes), surface to operator at Pre-Phase-6: "this source has features of <shape A> and <shape B>; recommend approach X for these reasons; operator decision requested."

## Honest scoring calibration

Phase B (May 2026, 35 sources) established that the scoring rubric (`_meta/scoring-rubric.md`) is canonical for tier/relevance/actionability/monetization values, but the rubric alone doesn't prevent calibration drift on edge cases. This section captures the calibration patterns Phase B operationalized — how to apply the rubric honestly when the source shape creates pressure to inflate or deflate scores beyond what the content actually warrants.

This section operationalizes the canonical scoring rubric; it does not override it. When the calibration patterns below conflict with the rubric, the rubric wins. The calibration patterns are heuristics for applying the rubric, not replacements for it.

### What honest scoring protects against

Honest scoring is operator-discipline against three specific failure modes Phase B encountered:

1. **Cluster-opening inflation.** A source opens new cluster territory (new domain, new substrate, new pattern dimension) and the cluster-opening feels significant. Pressure to inflate tier because "this is the first source in cluster X." But cluster-opening status doesn't affect what the source content itself warrants. Source 35 (Dave Nick YouTube faceless-AI) was the first content-cluster source in Phase B and was correctly scored tier-3 minimal because the content itself was tier-3 regardless of the cluster-opening significance.

2. **Reinforcement-as-novelty inflation.** A source teaches the same pattern from a different angle and the different angle feels like novelty. Pressure to inflate tier because "this creator brings something new." But reinforcement-with-different-angle is canonically Path-B variant 2 territory — selective writeset, not novel-commitment writeset. The cross-creator-counting math captures the value; the tier shouldn't.

3. **New-direction-surfacing inflation.** A source surfaces strategic implications operator hasn't considered (new tier-1 task shape, build-plan revision trigger, etc.) and the strategic significance feels worth high tier. Pressure to inflate tier because "this affects operator's whole approach." But new-direction-surfacing is meta to the writeset — it's a signal to operator, not a writeset-shape modifier. Source 30 (Nate Herk Paperclip) surfaced major new-direction (orchestration meta-layer) AND was correctly scored tier-2 selective because the source content itself was tier-2.

The asymmetric inverse — deflation pressure — is rarer but real: when operator-fatigue or batch-position drives scoring DOWN below what content warrants. Honest scoring protects against deflation too.

### Calibration buckets (Phase B patterns)

These buckets operationalize the scoring rubric for common Phase B source-shapes. They're heuristics, not deterministic rules. The rubric is canonical for edge cases.

**Tier-2, relevance-5, actionability-3-or-4 = novel-contribution-to-substrate**

When the source articulates a substantively novel architectural commitment in operator's substrate/cluster — the creator made their own architectural choices, the choices are operator-actionable, and the choices are within operator's active substrate adoption path. Standard Option A writeset (8-12 file ops; source note + new tactic spawns + tool note updates + queue-tail amendment).

Phase B examples: source 25 The Augmented (agent-substrate-as-MCP-backend pattern); source 31 Cole Medin LLM-knowledge-bases (memory-architecture sub-layer).

**Tier-2, relevance-4, actionability-3 = reinforcement-with-canonical-creator-articulation**

When the source reinforces existing canonical patterns from a different creator's angle, the creator made their own architectural choices, but the choices don't articulate substantively novel commitments beyond what's already canonical. Selective Option B writeset (6-9 file ops; source note + sources-array updates on existing tactics + queue-tail amendment).

Phase B examples: source 12 Nate Herk coder-reviewer; source 13 AI Jason structured-output; source 14 Devsplainers + 17 David Ondrej + 19 Sharbel A. + 22 Jay E + 33 Greg+Imran Hermes-substrate-cluster.

**Tier-2, relevance-3-or-4, actionability-2-or-3 = strict-minimal-shape**

When the source is teaching-creator (Strict-minimal precedent) or same-creator-extension (Path-B variant 1). Strict-minimal Option B-or-C writeset (~3-5 file ops; source note + sources-array updates only + queue-tail amendment).

Phase B examples: source 11 Cole headless-loop (same-creator-extension); source 21 Nick auto-research tutorial (same-creator-extension); source 23 David Ondrej auto-research (teaching-creator on canonical framework).

**Tier-3, relevance-2-or-3, actionability-1-or-2 = substrate-tutorial-archive or first-cluster-source**

When the source is substrate-tutorial for non-adopted substrate (Substrate-tutorial-archive precedent) OR first-cluster-source for cluster operator isn't actively building in. Minimal Option C writeset (~3 file ops; source note + minimal sources-array update + queue-tail amendment). NO new tactic spawns.

Phase B examples: source 10 Krish OpenClaw (substrate-tutorial-archive); source 35 Dave Nick YouTube faceless-AI (first content-cluster source, tier-3 honest despite new-cluster-opening).

**Tier-1 — consult the canonical scoring rubric**

Tier-1 was rare in Phase B and the criteria for tier-1 source-scoring (vs tier-1 task-spawning, which is a separate axis) are governed by `_meta/scoring-rubric.md` as the canonical source. This calibration framework does not attempt to capture tier-1 criteria; defer to the rubric. If a source seems to warrant tier-1 consideration, surface it explicitly at Phase 6 with the rubric-criteria reasoning, and let operator decide.

Note on tier-1 tasks: tier-1 tasks (spawned in `06_tasks/tier-1/`) are a separate axis from tier-1 sources. A source can be tier-2 or tier-3 and still surface a tier-1 task via new-direction-surfacing protocol. The Phase B ToS task was a tier-1 task spawned from substrate-research cluster sources; none of the sources that surfaced the ToS question were themselves tier-1.

### New-cluster-opening discipline

**The precedent:** Opening a new cluster (new domain, new substrate dimension, new pattern dimension) doesn't justify tier inflation on the cluster-opening source. The cluster-opening source gets scored based on what its CONTENT warrants, not based on the cluster-opening significance.

**The reasoning:** If the cluster-opening source were tier-inflated, then the first source in every new cluster would be tier-2-or-higher regardless of content quality, which would systematically distort the vault's tier distribution toward over-representing low-quality first-cluster-sources. Phase B established that honest scoring stays cluster-agnostic.

**The Phase B example:** Source 35 Dave Nick YouTube faceless-AI was the first content-cluster source in Phase B (opening 03_domains/content/video-intelligence/). The source content was tier-3 quality (lightweight tutorial, no novel architectural commitment, low operator-actionability beyond cluster-opening). Honest scoring gave it tier-3 minimal, even though it carried significant operator-attention-value as the cluster-opening source.

**The filing question:** First-cluster-sources get filed in `03_domains/<cluster>/insights/` rather than in `00_inbox/sources-pending/` after triage, regardless of tier. The filing reflects cluster-opening significance; the tier reflects content quality. These are orthogonal axes.

**How to apply:**
- Score the source content as if the cluster were already established
- If new-cluster-opening surfaces operator-decision-points, surface those via new-direction-surfacing protocol (orthogonal to tier)
- File the source in `03_domains/<new-cluster>/insights/` at triage, noting "first-source-in-cluster" in decision-archaeology

### Reinforcement with strategic implications

**The precedent:** A source can simultaneously be reinforcement-shape (Path-B variant 2) AND surface major strategic implications (new-direction). These are orthogonal — the reinforcement-shape determines the writeset; the strategic implications get surfaced via new-direction-surfacing protocol. Don't inflate tier because the strategic implications are significant.

**The Phase B example:** Source 30 Nate Herk Paperclip was reinforcement-shape (Nate's not canonical for orchestration patterns; Paperclip is one example of orchestration-on-substrate). Source 30 also surfaced major new-direction (orchestration as a meta-layer dimension, expanding the substrate-decision matrix from 4-runtime to 4-runtime × 2-orchestration = 8 combinations). Both true simultaneously. Honest scoring gave tier-2 selective writeset based on content; new-direction was surfaced via new-direction-surfacing protocol; matrix expansion got captured as separate decision-architecture observation rather than tier inflation.

**How to apply:**
- Score the source content based on what it articulates within existing pattern landscape (reinforcement-shape calibration)
- Surface strategic implications via new-direction-surfacing protocol at Phase 6 (NOT as tier modifier)
- If the strategic implications warrant operator-action, surface them as a candidate for operator-decided task-spawning via new-direction-surfacing protocol (likely tier-1 task, but operator decides); do NOT treat as tier-inflation of the source itself

### Honest scoring vs first-impression intake

**The precedent:** Operator's cluster-flag at intake reflects first-impression based on URL title, channel name, surface signals. Content as analyzed in Phases 1-5 may differ from first-impression. Honest scoring applies to content-as-analyzed, not to first-impression. This precedent operates in tandem with the Cluster-fit pre-check (see Extraction-discipline precedents section above).

**The Phase B example:** Sources 27, 28, 29 were operator-flagged as Obsidian-with-AI cluster (based on URL titles and channel names). Content analysis showed actual cluster was substrate/agent-architecture. Cluster-correction applied 3 times consecutively. Honest scoring used the corrected cluster's calibration buckets, not the operator-flagged cluster's.

**How to apply:**
- If Cluster-fit pre-check surfaces cluster-correction, apply the corrected cluster's calibration buckets
- Don't anchor on operator's first-impression flag when content analysis shows different cluster
- Surface honestly at Phase 6 if scoring shifted based on cluster-correction

### Cross-references to Skill 2

These calibration patterns interact with vault-curation-level precedents that live in Skill 2. The cross-references below name the topic; Skill 2 is the authoritative source for the rule:

- **Cross-creator counting strict reading** — when a creator's articulation counts for pattern-promotion math vs when it doesn't (synthesizer-shape, teaching-creator-shape, same-creator-extension don't count; canonical-creator-articulation with own architectural choices counts). Affects whether Path-B variant 2 sources move pattern math.
- **Asymmetric attribution (mediated vs direct)** — Karpathy-weight precedent: directly-articulated patterns from canonical creators count more than the same patterns mediated through other creators' coverage. Affects pattern-promotion math.
- **Cross-substrate independent arrival** — when the same architectural commitment arrives from independent sources working in different substrates, the cross-substrate arrival itself satisfies cross-creator-independent-arrival promotion criteria. Affects whether sources from different substrate clusters can collectively reach pattern threshold.
- **New-cluster-opening precedent** — the vault-curation-level version of the new-cluster-opening discipline above. Skill 2 captures the filing + tier-distribution implications; this section captures the extraction-time scoring implications.

### When honest scoring conflicts with operator intuition

Operator may intuit a tier different from what honest-scoring-by-content-shape produces. Two patterns:

**Operator intuits higher tier than content warrants:**
- Possible cause: new-direction-surfacing inflation (operator responding to strategic implications, not content)
- Possible cause: cluster-opening inflation (operator responding to "this opens X" significance)
- Possible cause: operator has context the executor doesn't (e.g., this source's framework is one operator's actively adopting, even though that's not yet reflected in vault)
- **What to do:** Surface the calibration logic honestly. Ask operator to specify which calibration pressure is operating. If operator has context executor doesn't, operator's tier wins. If operator is responding to new-direction or cluster-opening, surface via new-direction-surfacing protocol rather than tier inflation.

**Operator intuits lower tier than content warrants:**
- Possible cause: batch-position fatigue (sources later in batch get under-scored)
- Possible cause: cluster-saturation fatigue (Nth source in same cluster gets under-scored despite canonical-quality content)
- Possible cause: operator is signaling adoption-stance has shifted (e.g., operator now decides not to adopt the substrate this source is teaching)
- **What to do:** Surface the calibration logic honestly. If batch-position or cluster-saturation fatigue, ask operator to spot-check. If adoption-stance has shifted, that's substrate-tutorial-archive precedent and tier-3 is correct.

The principle: honest scoring is operator-discipline through the calibration framework, not through deference to either executor heuristic or operator intuition without examination.

## Triage workflow

Phase 7 of the extraction (file-writing per the v3.2 extraction prompt) completes with the source note in `00_inbox/sources-pending/` and judgment frontmatter fields LEFT EMPTY for the operator to fill. Triage is the distinct workflow step that comes AFTER Phase 7: operator fills frontmatter values, source moves from inbox to canonical destination, decision-archaeology entry gets appended. This section captures the operator-facing orchestration of that step. The extraction-prompt.md spec defines Phase 7 file-writing; this section defines the post-Phase-7 triage workflow.

### Why triage is a distinct step

Three reasons triage is structurally separate from Phase 7 rather than folded into it:

1. **Operator-calibration decisions are decoupled from extraction-execution.** Phase 7 file-writing happens deterministically once Phase 6 review approves; triage decisions (tier, relevance-score, actionability-score, monetization-potential, execution-recommendation, destination folder) require operator judgment that should not be entangled with extraction-time decisions.

2. **The source note's body content is calibrated at Phase 7; the frontmatter is calibrated at triage.** Phase 7 captures "what does this source contain"; triage captures "what tier/relevance/actionability does operator assign." Different decision-axes, different gates.

3. **Triage can be batched across sources for calibration consistency.** In multi-turn mode with batch ingestion, an operator may want to do triage decisions across multiple sources together to maintain calibration consistency, rather than triaging each source immediately after its Phase 7 completes. Triage being a distinct step makes this batching possible.

### Single-agent mode triage

When invoked without a review agent in the loop, triage is operator-handled directly:

1. After Phase 7 completes, operator reviews the source note in Obsidian (frontmatter judgment fields are empty per Phase 7 spec)
2. Operator reads the "Suggested judgments" section in the source-note body (executor's recommended tier/relevance/actionability/monetization values with reasoning)
3. Operator fills the actual frontmatter judgment fields with operator-decided values (may match or differ from suggested values)
4. Operator sets the Execution recommendation checkboxes
5. Operator moves the source note from `00_inbox/sources-pending/` to canonical destination folder
6. Operator appends a `[triaged]` decision-archaeology entry to the source-note body
7. Operator commits the changes

This is the standard standalone triage path.

### Multi-turn mode triage (Phase D of the multi-turn collaboration protocol)

When a review agent is present, triage follows Phase D of the multi-turn collaboration protocol (see "Multi-turn collaboration protocol" section above). The 8-step dance:

1. Review agent validates Phase 7 output landed correctly; drafts triage proposal prompt for executor
2. Operator transcribes triage proposal prompt from review agent to executor
3. Executor proposes frontmatter values + destination folder + execution recommendation; stops at triage approval gate
4. Operator transcribes triage proposal from executor to review agent
5. Review agent validates or modifies triage proposal; drafts triage-apply prompt for executor
6. Operator transcribes triage-apply prompt from review agent to executor
7. Executor applies triage; updates frontmatter, moves source note from inbox to canonical destination, appends decision-archaeology entry; reports completion
8. Operator transcribes completion from executor to review agent

The dance preserves operator-discipline on triage decisions while leveraging review agent for calibration pressure-testing and executor for file operations.

### Triage proposal contents

The executor's triage proposal (step 3 above) should include:

**Frontmatter judgment values:**
- `tier:` (1, 2, or 3 per calibration buckets in "Honest scoring calibration" section)
- `relevance-score:` (1-5 per scoring rubric)
- `actionability-score:` (1-5 per scoring rubric)
- `monetization-potential:` (high / medium / low / none per scoring rubric)

**Execution recommendation:** Which checkbox to mark — Act now / Save for later / Research deeper / Ignore — with one-sentence reasoning.

**Destination folder:** Where the source note should be filed after moving out of inbox. Standard Phase B destinations:
- Substrate/agent-architecture cluster sources → `03_domains/automation-systems/insights/`
- Content/video-intelligence cluster sources → `03_domains/content/video-intelligence/insights/`
- Project-specific sources → `04_projects/<area>/<project>/insights/` (rare; usually project relevance is tagged via frontmatter rather than via folder placement)
- Cross-cutting sources → `03_domains/<primary-domain>/insights/` with secondary domains tagged in frontmatter

**Status field update:** `status: extracted` → `status: triaged` (per Phase B precedent; see example entry shape below).

**Calibration reasoning:** One paragraph stating which calibration bucket the source fits (from "Honest scoring calibration" section) and why the proposed values reflect that bucket. Surface any cluster-fit decisions or extraction-discipline precedents applied during Phases 1-7 that bear on triage.

**Execution recommendation reasoning:** Honest reasoning for the recommended Execution recommendation checkbox. This is where sequencing-discipline applies: a high-relevance + high-actionability source can still warrant "Save for later" if upstream tier-1 work is open or if the operator's current Goal-A-level priorities should not be pulled away from (see Phase B source 34 precedent — Chris Parsons Ralph Loops triaged Save-for-later despite tier-2 + relevance-5 + actionability-4 because Goal A took priority).

### What the executor SHOULD do at triage

- Read the source note's body content (especially the "Suggested judgments" and "Decision archaeology" sections) to ground proposals in Phase 6/7 calibration decisions
- Propose frontmatter values that match the calibration bucket the source fits per "Honest scoring calibration" framework
- Propose destination folder per Phase B precedent (substrate-cluster sources to automation-systems; content-cluster sources to content/video-intelligence; etc.)
- Surface any honest-scoring-vs-operator-intuition conflict at the proposal stage rather than silently deferring to one or the other
- Use `mv` for the file move (Phase 7 already wrote the file; triage moves it, doesn't rewrite it)
- Append the `[triaged]` decision-archaeology entry capturing operator-approved values + filing destination + any consistency notes (wikilinks resolve by slug regardless of folder placement per Obsidian convention; folder relocation doesn't break references)

### What the executor SHOULD NOT do at triage

- Rewrite or modify the source note's body content (Phase 7 captured the body; triage doesn't touch it)
- Modify supporting notes that were created at Phase 7 (tactic notes, tool notes, task notes; these are independently created at Phase 7 and not part of triage)
- Apply frontmatter values without explicit operator approval (the proposal stage is non-binding until operator confirms)
- Commit (operator commits manually after triage completes; see "Commit message template" section below)

### Decision-archaeology entry shape

The `[triaged]` entry appended to the source-note body at triage should capture:

- Operator-approved frontmatter values (tier, relevance-score, actionability-score, monetization-potential)
- Execution recommendation checkbox set
- Destination folder source was filed to
- Whether proposed values matched operator's final values or required modification (and which fields if modified)
- Filing consistency note (e.g., "consistent with Phase B precedent — sources 1-30 all filed in `03_domains/automation-systems/insights/`")
- Any status transition (e.g., `extracted` → `triaged`)
- Any commit-note (e.g., "no commit per operator standing instruction" or commit message reference)

Example entry shape (from Phase B source 34 Chris Parsons Ralph Loops):

```
- 2026-05-10 [triaged] — filed to `03_domains/automation-systems/insights/` per operator-approved triage proposal. Tier 2 (substantive-novel-content category retained); relevance-score 5 (substantive novel content; high relevance to operator's autonomous-agent-layer activation lane); actionability-score 4 (4 operator-applicable workflow suggestions documented in tier-2 task body expansion); monetization-potential low (substrate-execution-discipline content; no direct monetization tactics). Filed in substrate/agent-architecture cluster consistent with Phase B precedent (sources 25-33 all in this folder). Status: extracted → triaged.
```

### Diminishing-returns discipline

**The precedent:** When a batch of sources keeps adding sources-array updates to the same existing tactic note (Nth update on same tactic in same batch), each additional update adds less calibration value than the previous one. Honest discipline is to drop marginal sources-array updates when they add no incremental calibration evidence, rather than mechanically applying updates because the source touched the tactic.

**Why this matters at triage layer specifically:** Triage is where the executor calibrates writeset shape against operator-approved scope. If Phase 7 generated sources-array updates that diminishing-returns discipline would drop, triage is the natural point to surface this and adjust the writeset before final filing.

**How to recognize:** Look for these signals during Phase 6/7 review:
- The source is the Nth source in the same cluster touching the same canonical tactic (N ≥ 4, roughly)
- The sources-array update is "this source also exemplifies tactic X" without adding new mechanism, scope, or angle to tactic X's existing canonical evidence
- The existing tactic note already has 3+ sources in its sources-array from the current cluster
- The update is mechanical (driven by tactic-touched detection) rather than substantive (driven by genuine new evidence)

**What to do:** Drop the marginal sources-array update. Capture rationale in decision-archaeology entry:
- "Source [Nth source in cluster] touched tactic X but diminishing-returns discipline applied — sources-array update dropped because update added no incremental calibration evidence beyond what 3+ existing cluster-sources already provide"
- "Tactic X sources-array preserved at current state ([list of canonical creators]); future cluster-source can update if it surfaces substantively new evidence dimension"

**Phase B example:** Source 33 (Greg+Imran Hermes) was the 5th Hermes-cluster source. Operator approved diminishing-returns discipline: dropped 3 marginal sources-array updates that mechanically detected as touched but added no incremental calibration value. The 5 Hermes-cluster sources collectively are evidence enough; the 5th doesn't need to mechanically update every tactic the first 4 already updated.

**Symmetric to new-cluster-opening discipline:** New-cluster-opening discipline (see "Honest scoring calibration" section) protects against tier-inflation when opening new clusters. Diminishing-returns discipline protects against writeset-bloat when continuing established clusters. Both are operator-discipline through honest restraint on mechanical-detection-driven artifact production.

**When NOT to apply diminishing-returns discipline:**
- The source surfaces substantively new evidence dimension (different mechanism, different scope, different operator-actionability) for the tactic — that warrants a sources-array update regardless of cluster position
- The source is canonical-creator-articulation rather than reinforcement — cross-creator counting math weight applies; mechanical-detection is the right detection in that case
- The cluster has fewer than 4 sources touching the tactic — diminishing-returns hasn't kicked in yet

The principle: triage is where honest scope-discipline gets applied to Phase 7's output. Diminishing-returns is one specific scope-discipline pattern; surface honestly rather than mechanically apply every detected update.

## Step 9 — Perplexity refinement hook (added 2026-05-27; auto-rec upgrade 2026-05-27)

After triage lands and the source note is filed in its canonical destination, the executor runs the Perplexity refinement decision logic. Two paths:

**Tier-1 sources → true auto-run.** Per Oliver's standing direction (2026-05-27), tier-1 sources auto-trigger perplexity-refinement at `deep` depth in `append` mode without an operator prompt. Reasoning: tier-1 is rare (Phase B had zero); when it lands, the stakes justify the cost; skipping the prompt removes friction on high-value sources. The executor runs the refinement and reports the result alongside the triage completion. Operator can still review/revert the appended section afterward.

**Tier-2 and tier-3 sources → calibrated recommendation, default-yes prompt.** The executor always runs the Phase-1 parse-and-tier analysis on the source note (cheap; no Perplexity queries yet) and surfaces a calibrated recommendation. The operator's choice is the only gate before queries run.

### When to offer (tier-2 / tier-3)

The recommendation is always surfaced — what changes is the depth recommended and whether the default leans yes or skip.

**Strongly recommend (default `medium`, lean yes):**

- The source note carries dense factual claims (named tools with pricing, statistics, study citations, product-feature claims) that would benefit from external triangulation
- The source note opens new-cluster territory and is the first cluster source — refining the first one deepens the cluster baseline
- The source note's "Research questions" section names 3+ verification gaps Perplexity could close
- The source was triaged tier-2 with relevance-5

**Recommend (default `light`, lean yes):**

- The source carries 2-4 high-tier claims
- The source was triaged tier-2 with relevance-3 or 4
- The source extends an established cluster with a new creator's angle (Path-B variant 2)

**Skip-recommended (default skip; operator can still pick a depth if they want):**

- The source is substrate-tutorial-archive shape (operator isn't adopting; refinement won't drive action)
- The source is strict-minimal shape (teaching-creator on someone else's canonical framework; refinement adds noise)
- The source's claims are mostly vault-internal operator-discipline observations (Perplexity can't validate vault-internal patterns)
- The source's high-tier-claim count from Phase 1 parse is 0-1

### How to offer (tier-2 / tier-3)

After triage completion, the executor runs the Phase-1 parse and then says:

> "Triage complete. Phase-1 parse on the source note found [N] high-tier claims, [M] medium-tier, [K] low-tier. Examples: [claim 1], [claim 2].
>
> **Recommendation: run perplexity-refinement at `<depth>` depth, `append` mode.** [One-sentence rationale citing the count + the calibration bucket the source fits.]
>
> Picks: yes (default) / light / medium / deep / sister-file / skip"

The operator picks one. On confirmation, the executor invokes perplexity-refinement.

If the operator just says "yes" or doesn't reply within the chat flow, the executor proceeds with the recommended depth and mode.

### How to offer (tier-1)

Tier-1 skips the prompt. The executor reports:

> "Triage complete. Source note triaged tier-1; auto-running perplexity-refinement at `deep` depth per the tier-1 standing rule. Phase-1 parse found [N] high-tier claims. Refinement starting now."

Then the executor runs refinement end-to-end and reports the result as part of the triage completion summary.

The operator can override the auto-run by saying "skip refinement on this one" before triage closes. After triage closes, tier-1 refinement is in flight.

### What the perplexity-refinement skill does from here

See `[[perplexity-refinement]]/SKILL.md`. Briefly: Phase 1 (parse + tier claims), Phase 2 (run Sonar API queries via `~/workspace/second-brain-tier3/automation/scripts/perplexity_sonar.py`; Path A via Claude in Chrome was removed 2026-06-01), Phase 3 (synthesize findings into six buckets), Phase 4 (write back per mode), Phase 5 (surface follow-ups).

The refinement output lands inside the source note (append mode) or as a sister file. The source note's frontmatter gets `perplexity-refined: YYYY-MM-DD` so future invocations can see at a glance that refinement has happened.

### What this does NOT change about VIS extraction

- Triage still owns the tier / relevance / actionability / monetization frontmatter. Refinement does NOT modify those fields.
- Pattern-promotion math is unaffected by refinement. Refinement may surface new candidate sources to ingest (Phase 5a), but those have to go through their own VIS extraction before they count for cross-creator math.
- Commit timing is unchanged. Operator commits triage; refinement is a separate commit if it lands.

### Multi-turn mode interaction

In multi-turn mode, the Step-9 offer comes from the executor at the end of Phase E (Commit and continue). The review agent may pressure-test which items to refine before the operator confirms depth. Standard transcription rules apply.

## Commit message template

This section defines the verbose-structured commit message format used in Phase B and subsequently. The format applies to ANY commit that captures substantive vault changes — extraction commits, triage commits, skill-update commits, build-plan-revision commits, task-closure commits. The format is configuration-specific to operator's git-based vault workflow; the underlying principles generalize.

### Why this format exists

Three principles motivate the verbose-structured format:

1. **Decision archaeology preservation.** Substantive vault changes carry decision-reasoning that's lost if commit messages are terse. A six-month-future operator (or review agent) reading git log shouldn't have to reconstruct why a writeset took the shape it did. The reasoning belongs in the commit message where git log preserves it cheaply.

2. **Per-commit revertability with context.** When operator decides to revert a commit, the commit message should provide enough context to understand what's being reverted and what downstream effects to expect. Terse commits force operator to reconstruct context from file diffs — slow and error-prone.

3. **Context-refresh fuel for review agents.** Review agent context fills up over batch ingestion; a fresh review agent reading git log of recent commits gets calibration context cheaper than re-reading every touched vault file. The verbose-structured format makes git log a viable context-refresh source.

These principles motivate verbose-structured commits regardless of specific shell/git/repo configuration. The specific template below is one implementation of these principles for operator's current vault workflow.

### Template structure

The Phase B template has these sections (in order):

**Subject line** — `<type>(<scope>): <short description>` shape. Examples:
- `feat: extract <source-filename>` (single-source extraction commit)
- `feat(skills): VIS extraction skill v1.2 Chunk N — <chunk-topic>` (skill-update commit)
- `chore: close tier-1 task <task-name> via authoritative research` (task-closure commit)
- `fix: cluster-correction sources <list> from <wrong-cluster> to <correct-cluster>` (cluster-correction commit)

**Summary paragraph (1-2 sentences)** — what the commit accomplishes at the operator-altitude. Not what files changed; what operational outcome.

**File-change summary** — quantitative shape of the commit (line counts, file counts, net deltas). Format: "SKILL.md grew from X lines to Y lines (net +N lines)" or "N new task notes created in 06_tasks/tier-1/" or similar.

**Backup chain (when applicable)** — for skill-update commits or any commit where prior state preservation matters. List backups in oldest-to-newest order with what each captures.

**Key additions** — substantive content additions made by the commit. Itemized list with brief reasoning for each. This is where decision-reasoning gets preserved most densely.

**Fixes from self-review (when applicable)** — when self-review during drafting caught issues that were fixed before commit, document the issues + fixes. Pattern from Chunks 2-5: self-review caught real issues; fixes applied; commit message captures both the issue and the fix so future operator/reviewer can see what discipline was applied.

**Preserved verbatim** — for incremental updates (skill chunks, multi-step build-plan revisions, etc.), list what's preserved unchanged from prior state. Reassures future reviewer that the commit is genuinely incremental.

**Forward references** — for incremental updates that contain dangling references to not-yet-existing content (e.g., Chunk 1's forward-references to Chunks 2-5; Chunk 2's forward-references to Skill 2). Document the references + when they'll resolve.

**Phase B precedent notes (when applicable)** — when commit applies or establishes a Phase B operational discipline, name the precedent explicitly. Examples: "diminishing-returns discipline applied per source 33 precedent"; "honest-self-review precedent applied catching N issues before commit"; "upload-dedup mitigation applied per Chunk-3 precedent."

### Heredoc-to-file pattern for shell-escape-resistant commits

The verbose template above produces commit messages with apostrophes, em-dashes, parentheses, and other characters that shell parsers can interpret as syntax. Passing such messages via `git commit -m "<message>"` produces shell-parse errors (encountered during Chunk 2 commit attempt: zsh choked on embedded apostrophes and special characters).

The mitigation is heredoc-to-file: write the message to a temp file first using a heredoc with quoted delimiter (prevents variable expansion and backtick execution), then `git commit -F <file>` reads from file without shell-parsing. This approach is shell-shape-dependent (zsh/bash heredoc syntax; different shells need different approaches) but works reliably for operator's current zsh-on-macOS configuration.

The three-step pattern:

```bash
# Step 1: write message to temp file via heredoc with quoted delimiter
cat > /tmp/commit-msg.txt << 'COMMIT_MSG_EOF'
<commit message contents, with any special characters>
COMMIT_MSG_EOF

# Step 2: commit using -F flag to read from file (bypasses shell parsing)
git add -A && git commit -F /tmp/commit-msg.txt

# Step 3: clean up temp file
rm /tmp/commit-msg.txt
```

The `'COMMIT_MSG_EOF'` (quoted delimiter) is critical — unquoted delimiter would allow shell expansion of `$variables` and backtick-execution inside the heredoc, which can corrupt the message. Always quote the delimiter for commit messages.

### When to use this template vs lighter commits

The verbose template is appropriate when:
- Commit captures substantive vault changes (new sources extracted; triage applied; skill chunks landed; tier-1 tasks closed; build-plan revisions; decision-architecture changes)
- Commit carries decision-reasoning that's worth preserving in git log
- Commit is part of an incremental sequence where future readers benefit from cross-reference to prior commits

Lighter commits (terse `git commit -m "<one-liner>"`) are appropriate for:
- Mechanical fixes (typos, broken links, frontmatter consistency adjustments)
- Pure rename/move operations with no decision content
- Configuration changes that have no operational implications
- Backup snapshots taken for safety without active changes

The principle: commit-message-weight scales with decision-content-weight. Substantive decisions warrant verbose preservation; mechanical changes don't.

### Self-application note

This SKILL.md file's own evolution from v1.1 → v1.2 Chunks 1-5 used the verbose template at every chunk commit. The git log of `~/workspace/skills/vis-extraction/` preserves the chunk-by-chunk decision archaeology: which sections were added in which chunk, what fixes self-review caught at each chunk, which forward-references were dangling and when they resolved. This is the template applied to itself.

## Cross-reference to Skill 2

Skill 2 (vault knowledge-curation discipline) is the canonical home for the operator-discipline precedents that Phase B established at the vault-curation level. Skill 1 (this skill) references Skill 2 throughout — in Chunks 2 (extraction-discipline precedents), 3 (honest scoring calibration), and 4 (triage workflow) — without restating the rules. This section makes the cross-reference structure explicit.

### Which precedents live in Skill 2

The 10 operator-discipline precedents established in Phase B that live in Skill 2 as the authoritative source:

1. **Premature-abstraction discipline** — when refusing pattern promotions despite mechanical-detection threshold being reached (source 26 precedent)
2. **One-creator-only-no-spawn discipline** — when a pattern has only one canonical creator, no tactic note gets spawned regardless of threshold-math (source 26 precedent)
3. **Over-fragmentation discipline** — when tightly-coupled patterns should consolidate into single tactic note rather than fragmenting into multiple notes (source 26 precedent)
4. **Cluster-correction discipline** — when operator-flagged cluster differs from content-shape; honest correction over force-fitting (sources 27/28/29 precedent)
5. **Karpathy-weight (asymmetric mediated-vs-direct attribution)** — directly-articulated patterns from canonical creators count more than the same patterns mediated through other creators' coverage (source 31 precedent)
6. **Cross-substrate independent arrival** — when the same architectural commitment arrives from independent sources working in different substrates, the cross-substrate arrival satisfies cross-creator-independent-arrival promotion criteria (sources 25 + 32 precedent)
7. **Diminishing-returns discipline (vault-curation perspective)** — operator-curated discipline of dropping marginal sources-array updates when continuing established clusters (source 33 precedent; see also Chunk 4 of this skill for the extraction-time application of the same discipline)
8. **Retroactive-precedent-application** — when a precedent established later in a batch retroactively applies to earlier sources; rewrite earlier attributions for consistency (source 34 precedent)
9. **New-cluster-opening discipline (vault-curation perspective)** — opening a new cluster doesn't justify tier-distribution skew; first-source-in-cluster discipline preserves tier integrity (source 35 precedent; see also Chunk 3 of this skill for the extraction-time application)
10. **First-source-in-folder filing** — filing convention for cluster-opening sources distinguishing them from continuation sources (source 35 precedent)

### Where Skill 1 references which precedents

The cross-references throughout Skill 1's chunks:

- **Chunk 2 (Extraction-discipline precedents)** references Skill 2 for cross-creator counting rules (Path-B variant 1 same-creator-extension; Path-B variant 2 cross-creator-counting weight; Strict-minimal teaching-creator weight)
- **Chunk 3 (Honest scoring calibration)** references Skill 2 for cross-creator counting strict reading, asymmetric attribution (Karpathy-weight), cross-substrate independent arrival, and new-cluster-opening (vault-curation-level)
- **Chunk 4 (Triage workflow)** references Skill 2 implicitly through the calibration-bucket framework (which itself depends on cross-creator counting + cross-substrate independent arrival rules)

**Note on cross-creator counting:** "Cross-creator counting rules" is the foundational rule that operationalizes through several of the numbered precedents above (premature-abstraction, one-creator-only-no-spawn, Karpathy-weight asymmetric attribution, cross-substrate independent arrival). It's not itself a numbered precedent — it's the underlying mechanic that several precedents enforce or modify. Skill 1's references to "cross-creator counting rules" should be read as referencing this foundational mechanic; Skill 2 documents how the numbered precedents collectively define and refine it.

### Why precedents are split between Skill 1 and Skill 2

The split reflects layer-separation: Skill 1 covers extraction-workflow (Phase 0-7 + triage + commit during a source's extraction lifecycle). Skill 2 covers vault-curation (the cross-source, cross-cluster discipline that operates ABOVE individual extractions). Some precedents have aspects in both layers — diminishing-returns and new-cluster-opening both have extraction-time application (this skill) AND vault-curation-level application (Skill 2). The cross-references preserve each precedent's full shape while keeping each skill focused on its own layer.

Until Skill 2 is created, the cross-references in Skills 1's chunks are dangling. When Skill 2 lands, the cross-references resolve. This is the same pattern applied throughout Skill 1's own chunks (Chunk 1's forward-references to Chunks 2-5 were dangling until each chunk landed).

## Core workflow

When invoked, follow these steps in order. Stop and ask the user only when explicitly required.

### Step 1 — Identify the input

The user gave you one of:
- A YouTube URL (most common): `https://www.youtube.com/watch?v=...` or `https://youtu.be/...`
- An article URL: any other `https://` URL
- A local file path: `/path/to/transcript.md` or similar — usually a previously-pulled transcript or an uploaded text file

If the input is ambiguous (e.g., user said "ingest the latest one"), ask which URL or file they want.

### Step 2 — Identify the mode

Default mode: `training` (stops at the Phase 6 review gate; user approves before write).

Override: if the user explicitly says "auto," "auto mode," "no review," or "skip the review," use `auto` mode (writes immediately after extraction, no review gate).

If the user doesn't specify, default to `training`.

### Step 3 — Capture optional "why ingested" note

If the user provided a one-liner explaining why they're ingesting this source (e.g., "want to compare this against my migration pipeline"), capture it. It goes in the source note's "Why ingested" field.

If they didn't provide one, leave the field empty — don't ask for it. The user can fill it later, or it can stay empty.

### Step 4 — Read the extraction prompt and scoring rubric

These are mandatory pre-pull reads. The extraction prompt defines Phase 0 (environment preflight, run in Step 5 below) and Phases 1-8 (the extraction itself, run in Step 7). Read both upfront so the rest of the workflow can proceed without re-reading.

```bash
cat /Users/olivermarroquin/workspace/skills/vis-extraction/prompts/extraction-prompt.md
cat /Users/olivermarroquin/workspace/second-brain/_meta/scoring-rubric.md
```

The extraction prompt is v3.2. It defines Phase 0 (environment preflight) and Phases 1-8 (the extraction itself). The scoring rubric is canonical for tier/relevance/actionability/monetization values.

### Step 5 — Phase 0 environment preflight

Before pulling the transcript, run Phase 0 of the extraction prompt to verify the tools required by `transcript-pull.sh` are available in the current execution environment.

The authoritative spec lives in `prompts/extraction-prompt.md` (the `## Phase 0 — Environment preflight` section, just before Phase 1). You already read it in Step 4 — execute it now:

- For YouTube URLs without a cache hit: verify `yt-dlp` on the augmented PATH (`$HOME/.local/bin`). If missing, attempt `pip install --user --break-system-packages yt-dlp`. If install fails or the post-install re-check fails, hard-fail per the spec.
- For article URLs without a cache hit: verify `curl` and `trafilatura`. Same install + hard-fail pattern (no PYTHONPATH augmentation needed — Python's `site` module auto-includes user-site-packages on `sys.path` when `ENABLE_USER_SITE` is True, so user-installed Python modules are importable without explicit prefix; see Phase 0b spec for the full parity-contrast rationale).
- For local files OR cache hits: skip Phase 0 entirely.

**PATH augmentation contract for YouTube URLs.** Phase 0a's pip install places the yt-dlp binary at `$HOME/.local/bin/yt-dlp`, which is not on the sandbox's default PATH. **Every subsequent bash call in this invocation that touches yt-dlp** — including the `transcript-pull.sh` invocation in Step 6 — **must prepend `PATH="$HOME/.local/bin:$PATH"`** to its environment. Each bash call in the sandbox runs independently with no env carryover, so a one-off `export PATH=...` does not persist; every call sets PATH explicitly. Step 6 below honors this contract.

**Phase 0 is stateless.** Every invocation of the skill re-runs Phase 0 from scratch — there is no session-level memoization. If a previous invocation hit a Phase 0 hard-fail and the operator responded "retry" after installing the missing tool on the host, the new invocation will re-run the in-sandbox availability check from zero, and only proceed if the check (or its install fallback) actually passes this time.

If Phase 0 hard-fails, STOP. Do not proceed to Step 6. Wait for explicit operator acknowledgment per the spec ("acknowledged" / "retry" → re-invokes the skill; "abort" → stops the extraction entirely). No other paths are valid; do not silently degrade to a host pull.

### Step 6 — Pull the transcript

The transcript-pull script may run in different contexts with different network capabilities. Handle three scenarios:

**Scenario A — Cache hit (fastest path):**

Before running the pull, check if a transcript for this URL already exists in the cache:

```bash
ls -t /Users/olivermarroquin/workspace/skills/vis-extraction/cache/*.md 2>/dev/null | head -5
```

If a recent transcript file exists matching the source's video ID or article slug, use it directly. Skip to Step 7 with the cached filename. Tell the user: "Found a pre-existing cached transcript for this exact source from [date]. Using it rather than re-pulling."

**Scenario B — Cloudflare Worker transcript fetch (preferred for YouTube URLs):**

For YouTube URLs, use the sandbox-reachable Cloudflare Worker wrapper instead of `yt-dlp`. This works from both Mac Terminal and Cowork sandbox without network restrictions:

```bash
python3 ~/workspace/repos/ai-agency-core/scripts/fetch_youtube_transcript.py --url "<YOUTUBE-URL>" --markdown --quiet > /Users/olivermarroquin/workspace/skills/vis-extraction/cache/transcript-$(date +%Y-%m-%d-%H%M%S)-<slug>.md
```

The wrapper reads the API token from `~/workspace/second-brain-tier3/automation/secrets/youtube-transcript.key` (Mac Terminal) or `/mnt/user/second-brain-tier3/automation/secrets/youtube-transcript.key` (Cowork sandbox). If this succeeds, capture the output filename and proceed to Step 7.

**Scenario B-legacy — transcript-pull.sh via yt-dlp (fallback for YouTube, required for articles):**

If the Worker is down or for article URLs, fall back to the original `transcript-pull.sh` path. **For YouTube URLs**, the bash call must include the PATH augmentation Phase 0a established (so `transcript-pull.sh`'s internal `command -v yt-dlp` finds the user-local binary):

```bash
PATH="$HOME/.local/bin:$PATH" /Users/olivermarroquin/workspace/skills/vis-extraction/scripts/transcript-pull.sh "<URL-or-path>" /Users/olivermarroquin/workspace/skills/vis-extraction/cache
```

For article URLs and local files, the PATH augmentation isn't strictly required (yt-dlp isn't invoked) but it's harmless to include — using the same invocation form across all input types keeps the orchestration simple. If this succeeds, capture the output filename and proceed to Step 7.

**Scenario C — Sandbox network blocked (two-step path):**

If you see errors like:
- `connection not allowed by ruleset`
- `403 Forbidden ... blocked-by-allowlist`
- `x-deny-reason: blocked-by-allowlist`
- `ERROR: [youtube] ...: connection not allowed`

The sandbox cannot fetch the source via `yt-dlp`. **Try the Cloudflare Worker wrapper first (Scenario B above).** If the Worker is also unreachable, surface this to the user and instruct them to run the pull on their host machine. Provide the exact command:

```
The sandbox can't reach <domain>. Please run this in your Mac terminal:

  cd /Users/olivermarroquin/workspace/skills/vis-extraction/scripts
  ./transcript-pull.sh "<URL>" ../cache

Then paste the resulting filename back to me. I'll continue from Step 7.

(The output will be at /Users/olivermarroquin/workspace/skills/vis-extraction/cache/transcript-YYYY-MM-DD-HHMMSS-<slug>.md)
```

Wait for the user to provide the filename, then proceed to Step 7 using that filename.

**For local file inputs (user provided a path, not a URL):**

Local files don't need network. Run the script normally — it produces a copy in cache with proper frontmatter. If for some reason the script fails on a local file, just use the original file path; the extraction can read from anywhere on disk.

### Step 7 — Run the extraction

Phase 0 (environment preflight) was already executed in Step 5. Following the v3.2 extraction prompt, execute Phases 1-8:

1. **Phase 1 — Context gathering.** Read templates, conventions, broad workspace context (CLAUDE.md, current-goals.md per Phase 1 step 3 of the extraction prompt, project READMEs, existing-note index from the vault).
2. **Phase 2 — Chunking decision.** Determine attention mode:
   - <9,000 words → single-pass
   - 9,000-25,000 words → focused-attention
   - ≥25,000 words → chunked
3. **Phase 3 — Source analysis.** Apply global writing rules (acronym expansion on first use; plain-English coverage at top + 4 jargon-section callouts). Produce all structured analysis. **Also produce a "Structured action items" block organized by kind (experiment / decision / comparison / research / adoption / conditional)** — apply the four-rule inclusion gate (decidable outcome, specific enough to act on, generalizes beyond pattern-watching, actionable to the operator). Soft cap at 8-10 items per source; surplus stays in legacy sections.
4. **Phase 4 — Existing-note check.** Dedup-and-enhance pass against vault content.
5. **Phase 5 — Conservative-creation gate.** Apply the "would this note be useful 3 months from now" filter.
6. **Phase 6 — Review gate.** In `training` mode: STOP and present structured summary including the new "Proposed structured action items" approval block. Wait for user approval. In `auto` mode: skip directly to Phase 7.
7. **Phase 7 — Write to disk.** Write source note to `00_inbox/sources-pending/`, supporting notes to their canonical locations. **Materialize approved structured action items as task notes in `06_tasks/`** with `extracted-via: vis-phase6` and `source: [[<source-note>]]`. Set `attention-mode` in frontmatter. Leave the source note's "Action log" Dataview block in place (it auto-populates from the new task notes). Leave Discussions section's Dataview block in place.
8. **Phase 8 — Report.** Generate the structured report (see "Final report format" below).

**Do NOT touch git.** The user commits manually after inspecting on disk.

### Step 8 — Generate the final report

The final report goes in the conversation, not in the vault. Format below.

### Step 9 — Compound-primer offer

Step 9 is a SKILL.md-layer addition that runs after the v3.2 extraction prompt completes. The prompt itself ends at Phase 8; this step extends the workflow but is not part of the prompt's phase count.

After the final report prints, detect which domain(s) this run touched and surface a one-line offer to invoke the `meta-document-primer` skill in `compound-primer` mode against each. Operator-confirmable; never auto-runs. Format and detection rules below in "Compound-primer offer".

## Final report format

After all writes complete, produce a report with this structure:

```
EXTRACTION COMPLETE

Source: <filename>.md
        → <full-path-relative-to-vault>
- Source-type: <video|article|transcript>
- Mode: <training|auto>
- Word count: ~<N> (file total)
- attention-mode: <single-pass|focused|chunked>
- Frontmatter judgment fields: empty (your call)
- Action log: placeholder only

Created (NEW notes):
- <list of new notes with brief 1-line descriptions and links>
- Task notes in 06_tasks/ (if any approved at Phase 6): N total — experiments=N, decisions=N, comparisons=N, research=N, adoptions=N, conditional=N

Enhanced (existing notes that grew):
- <list of enhanced notes with brief description of what was added>

Linked to existing (no changes to those notes):
- <list of linked notes>

Skipped (with reasons):
- <list of skipped extractions with brief reasons>

Conflicts flagged for your review:
- <list of any architectural conflicts surfaced for user decision>

Visual signals to investigate manually:
- <list of timestamps where visual content seemed important, or "none" for articles>

Suggested judgments included in source note:
- Yes (separate body section; frontmatter empty for you to fill)
- TL;DR: tier <N>, actionability <N>, relevance <N>, monetization <high|medium|low|none>
- Execution recommendation: <Act now|Save for later|Research deeper|Ignore|mixed>

Research questions logged in source note: <count>

Pattern candidates surfaced:
- <list of pattern candidates with their N/3 progress>

Files written / modified:
A  <path>
A  <path>
M  <path>
...

Next steps for you:
1. Review the source note in Obsidian — read the Suggested judgments section.
2. Fill the actual frontmatter judgment fields (tier, relevance-score, actionability-score, monetization-potential) with your own values.
3. Set the Execution recommendation checkboxes.
4. Move the source note out of inbox to <recommended-destination> once judgments are filled.
5. Commit (when ready, run yourself):

   cd /Users/olivermarroquin/workspace/second-brain && git add . && git commit -m "feat: extract <source-filename>"

Optional follow-ups (opt-in; never auto-runs):
- Route any newly extracted tactic / tool / pattern note via intel-routing PUSH.
  Type "route <tactic-slug>" or "PUSH-route <tactic-slug>" to invoke. PUSH derives
  the five project-applicability frontmatter fields, surfaces a routing-decision
  proposal, and writes bridge notes to applicable project folders.
  See ~/workspace/skills/intel-routing/SKILL.md.
- After Step 9 compound-primer offer resolves, optionally run synthesis-readiness-scan
  to detect cluster-ready / pattern-ready candidates in the domains touched by this run.
```

## Compound-primer offer

Step 9 surfaces a follow-up offer after the final report prints. The goal: keep domain primers current as VIS ingests new vocabulary, without forcing the operator to remember to run `compound-primer` manually.

### How to detect affected domain(s)

Collect the distinct domains touched by this run. Sources, in order of preference:

1. **Frontmatter `domain:` field** on any note written or modified in Phase 7 (source note, tactic notes, tool notes, task notes). Read each created file's frontmatter and gather the `domain:` values.
2. **Destination folder inference.** Any supporting note written under `second-brain/03_domains/<domain>/...` implies that `<domain>` was touched. Use this as a fallback when frontmatter is missing or as a cross-check.
3. **Triage destination (if known).** The triage step's recommended destination folder for the source note (e.g., `03_domains/marketing/`) implies the operator-intended primary domain.

Deduplicate. Also keep a separate list of **the actual file paths written or modified in Phase 7** — the run-scoped sub-option below needs them.

If only one domain surfaces, offer once. If multiple surface, offer per domain. If zero surface (rare — source landed entirely outside `03_domains/`, e.g., only in `_meta/` or `05_shared-intelligence/`), skip the offer silently.

### Format of the offer

The presentation depends on the agent's environment:

**Interactive option UI (preferred when available, e.g., Cowork's `AskUserQuestion` multi-select tool):** present one multi-select question with one option per domain × scope combination, plus a "skip — I'll run it later" option. Operator picks zero or more in one response. Use this path whenever the executing agent has access to an interactive option-UI tool, because checkbox/radio UI renders properly and is faster for the operator than parsing a numbered list.

**Inline numbered-list (fallback for chat-only environments without interactive option UI):** after the report block, append in the conversation:

```
Compound-primer offer:
- This run added notes to domain(s): <domain-1>, <domain-2>, ...
- Reply with the numbers you want (multi-select; e.g., "1, 4"):

  1. <domain-1> — full domain (default 30-day window)
  2. <domain-1> — scoped to just the notes from this run
  3. <domain-2> — full domain (default 30-day window)
  4. <domain-2> — scoped to just the notes from this run
  ...
  0. skip — I'll run it later
```

Wait for the operator's response. Then:

- If the operator picks a **full domain** option → invoke `meta-document-primer` in `compound-primer` mode, passing only the domain name as the scope. The compound-primer skill will default to its last-30-days window per its Step C2.
- If the operator picks a **scoped to just the notes from this run** option → invoke `meta-document-primer` in `compound-primer` mode, passing the domain name as the scope AND the explicit list of file paths captured during detection (the Phase 7 write list). This uses the compound-primer skill's "From these specific notes" override per its Step C2, so the scan is bounded to this run's output rather than the rolling 30-day window.
- If the operator picks multiple options across domains, invoke once per chosen line.
- If the operator picks `skip` or doesn't respond with a confirmation → do nothing further. The offer is a prompt, not a queue; it doesn't persist.

The compound-primer workflow has its own approval gates (see that skill's Step C4); this skill's role ends at the handoff.

### Never auto-run

Even in `auto` mode, the compound-primer offer is operator-confirmable. `auto` mode for VIS suppresses the Phase 6 review gate; it does NOT suppress the Step 9 offer. The compound-primer skill has its own discipline around extending primers (read-only by default, conservative on extension) — that contract is preserved by requiring explicit operator confirmation here.

## Closing step — Auto-invoke output-quality-loop

After Step 9 resolves (compound-primer offer accepted, declined, or no domains touched), and after the final report has printed, emit the standard auto-invoke block per `~/workspace/skills/output-quality-loop/references/auto-invoke-convention.md` and `~/workspace/second-brain/_meta/conventions.md` § "Output quality". This is the closing step every artifact-producing skill emits before declaring the chat done. Convention shipped Phase 5 of the output-quality-loop project (2026-05-28).

**Artifact list for this skill.** Always include: the source note. Optionally include (when actually written this run): newly created tactic notes, tool notes, opportunity notes, content-idea notes, pattern notes, task notes. Skip notes that were only linked or enhanced trivially (no new content). The block lists each artifact on its own bullet, full vault-relative or `~/`-prefixed path inside backticks.

**The block to emit (verbatim):**

````markdown
## Auto-invoke output-quality-loop

This skill produced the following artifact(s):
- `<source-note-path>`
- `<tactic-note-path>`         ← only if newly created this run
- `<tool-note-path>`           ← only if newly created this run
- `<opportunity-note-path>`    ← only if newly created this run
- `<content-idea-note-path>`   ← only if newly created this run
- `<pattern-note-path>`        ← only if newly created at 3/3 this run

[output-quality-loop:eval] — for each artifact, run output-quality-loop in EVALUATE mode. If PASS, declare the chat done. If NEEDS REVISION or FAIL, ingest the revision prompt as if it were operator input and regenerate the artifact, then re-invoke output-quality-loop. Cap at 3 iterations; on the 3rd FAIL, escalate to the operator with the evaluation report.
````

Required-element discipline per the convention spec: heading text matches verbatim (`## Auto-invoke output-quality-loop`); one bullet per artifact with full path in backticks; directive opens with `[output-quality-loop:eval]` and includes the iteration-cap discipline language.

**Iterate or declare done.** All PASS → declare done. Any NEEDS REVISION (minor / substantive) → Mode 2 auto-fires a revision prompt; ingest as operator input, apply fixes to the affected source / tactic / tool / etc. notes, re-emit the block, loop. Any FAIL → revision prompt includes root-cause analysis; address the root cause (often a missed extraction discipline rule — frontmatter shape, plain-language layer, action-log placeholder, etc.), regenerate, re-emit, loop.

**Iteration cap (3 max).** Track count via the folder-quality-log's per-artifact section before each regeneration. If three iteration entries exist and the verdict is still not PASS, **escalate** to the operator with the evaluation report and stop. Don't run a fourth iteration — that's the load-bearing cost-control discipline.

**Operator bypass.** Include `--bypass-quality-loop` (or "skip the quality loop") in the original VIS request to skip the block for that invocation. The bypass records to the closest folder's `_quality-log.md` under `### Bypassed (manual override)`.

## What this skill does NOT do

- Does NOT commit to git. User runs the commit command after inspecting.
- Does NOT push to GitHub. User pushes when ready.
- Does NOT move source notes out of `00_inbox/sources-pending/`. User does that after filling judgment fields.
- Does NOT auto-update existing source notes (e.g., bumping `updated:` field) just because a related extraction happened.
- Does NOT chase pattern promotions. If a pattern reaches 3/3, surface it as a candidate; don't auto-create the pattern note.
- Does NOT read or modify discussion files. Discussions are a separate workflow (see `_meta/discussions-engagement-guide.md`).

## Edge cases

**Local file with no metadata:** If the user gave a local file (not a URL), the transcript-pull script will produce a transcript with minimal frontmatter. The extraction proceeds normally; the source note's frontmatter will have empty `url`, `creator`, `published` fields — that's fine, the body content carries the value.

**Re-extracting an already-extracted source:** If the user is re-running on a source you've already extracted (filename collision), report this as a problem and ask whether to overwrite, append-as-update, or skip. Don't silently overwrite.

**Empty or near-empty transcript:** If the transcript file is <500 words, the source likely failed to extract usefully. Report this and ask whether to proceed with a minimal source note or abort.

**User says "auto" mode but you have low confidence:** If you're in auto mode but the source has unusual characteristics (very long, very short, low quality, conflicting evidence with vault content), surface a brief flag in the report rather than silently writing low-quality artifacts. Auto mode skips the review gate but doesn't suspend judgment.

**Skill invoked without a URL or path:** If the user invokes the skill without specifying a source, ask which URL or file they want extracted.

## Reference files

The actual content this skill operates on lives outside the skill folder:

- **Transcript pull script:** `/Users/olivermarroquin/workspace/skills/vis-extraction/scripts/transcript-pull.sh`
- **v3.2 extraction prompt:** `/Users/olivermarroquin/workspace/skills/vis-extraction/prompts/extraction-prompt.md`
- **Scoring rubric (canonical):** `/Users/olivermarroquin/workspace/second-brain/_meta/scoring-rubric.md`
- **Source-video template:** `/Users/olivermarroquin/workspace/second-brain/_meta/templates/vis/template-source-video.md`
- **Vault root:** `/Users/olivermarroquin/workspace/second-brain/`

Read these as needed. The extraction prompt is the authoritative spec; this SKILL.md is the orchestration layer.

---

## Peer-reviewer dispatch (GPR-9, gate-peer-reviewer v3.3)

> **Independence precedence (gate-peer-reviewer v3.8).** The Task sub-agent dispatch described here is the *weaker-independence convenience mode* — acceptable for high-volume, low-stakes gates. For any gate that changes vault/live state, registers a skill, or ships a client deliverable, the CANONICAL and MANDATORY mode is a **separate-session, step-by-step running review** (separate Claude Code or Cowork session; operator pastes each producer output; reviewer disk-verifies and hands back a paste-ready producer-reply block). See `~/workspace/skills/gate-peer-reviewer/SKILL.md` § Independence precedence and `~/workspace/second-brain/05_shared-intelligence/patterns/pattern-independent-peer-review-chat.md`. A sub-agent verdict is never full independent review.

**Gate type:** G-extraction (NOT a closing gate — Check 6 skipped).
**Fires after:** Phase 6 review gate (executor surfaces structured summary before writes).
**Dispatch shape:** Orchestrator spawns the peer-reviewer as a Task sub-agent after the structured summary is ready and before the write-to-vault phase.

**Per-gate dispatch block (Claude Code substrate):**

```
## Peer-reviewer dispatch

Gate type: G-extraction
Orchestrator: vis-extraction
Project: <source-slug>
Wave: null

Context paths for the Task sub-agent:
- Gate output: <structured summary — source note + supporting artifacts>
- Gate-type registry: ~/workspace/skills/gate-peer-reviewer/references/gate-type-registry.md
- Check spec: ~/workspace/skills/gate-peer-reviewer/references/check-spec.md
- Lesson files: ~/workspace/second-brain/05_shared-intelligence/lessons/ (most recent for this skill)

Task instruction: Read the gate-type registry entry for G-extraction. Run Check 1 satisfaction targets.
Run Checks 2-5 per check-spec.md skip logic. This is NOT a closing gate — skip Check 6.
Classify each catch severity per return-contract.md § Severity tiers.
Return the structured JSON verdict per references/return-contract.md.
```

**What the orchestrator does with the verdict:**

- `APPROVE` + `verdict_severity: advisory` → proceed to write phase. No operator review needed.
- `APPROVE-WITH-NOTES` + `verdict_severity: advisory` → proceed to write; notes logged for awareness.
- `APPROVE-WITH-NOTES` + `verdict_severity: blocking` → surface to operator. Operator decides.
- `REJECT-AND-REDO` → fix the catch, re-surface structured summary, re-dispatch peer-reviewer. Cap at 2 iterations; on 3rd REJECT, escalate to operator.
- `ESCALATE-AMBIGUOUS` → surface to operator with the peer-reviewer's ambiguity framing.

**Graceful degradation.** If peer-reviewer dispatch fails (skill unavailable on substrate), log:

```
event-type: peer-reviewer-skipped
reason: skill not available on <substrate>
chat-id: <id>
gate-id: G-extraction
orchestrator: vis-extraction
```

Then proceed to write phase with the skip noted.
