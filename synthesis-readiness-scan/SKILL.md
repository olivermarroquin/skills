---
name: synthesis-readiness-scan
description: Scan the vault for synthesis-ready clusters and patterns, surface them as a numbered offer, and hand off operator-confirmed picks to the multi-source-synthesis skill. Triggers on phrases like "scan for synthesis-ready," "what's synthesis-ready," "any clusters ready to synthesize," "check synthesis readiness," or invocation as a follow-on step after VIS extraction completes. Detects two of the four synthesis shapes automatically (cluster, pattern); cross-cluster and client-driven remain operator-invoked. Never auto-runs synthesis; the offer is a prompt, not a queue.
---

# Synthesis-Readiness Scan Skill (v1.0)

Detects which clusters and patterns in the vault are at synthesis-readiness thresholds, surfaces them as a numbered offer, and hands operator-confirmed picks off to the multi-source-synthesis skill. Composes with the VIS extraction skill's Step 9 pattern: detect state → surface offer → operator confirms → handoff → prompt-not-queue.

**Critical behavior (read first):**
- **Read-only on the vault.** This skill never writes, moves, or modifies files. All writes happen downstream in multi-source-synthesis.
- **Never auto-runs synthesis.** Every pick passes through two operator confirmations: the scan offer here, then the shape-and-destination gate inside multi-source-synthesis.
- **Offer is a prompt, not a queue.** If operator picks `skip` or doesn't respond, nothing is remembered. Re-invoke the scan to see candidates again.
- **Pattern-readiness detection depends on operator-set frontmatter.** Specifically `times-observed:` and `confidence:` fields on pattern/tactic notes. Detection is heuristic; the scan reports the detected counts alongside each pattern offer so the operator can verify the detection is reasonable before confirming.

## Two invocation paths

### Path A — Standalone (operator-invoked)

Operator triggers with one of: "scan for synthesis-ready," "what's synthesis-ready," "any clusters ready to synthesize," "check synthesis readiness," or similar. The skill scans the entire vault and surfaces all current candidates.

This is the primary path. Use when operator wants to know what's ripe across the whole vault.

### Path B — As VIS Step 10 (post-extraction)

VIS extraction skill invokes this skill after its Step 9 (compound-primer offer) completes. Scope is restricted to the domain(s) the VIS run just touched (collected from frontmatter `domain:` fields or destination-folder inference, same as Step 9's detection).

In Path B, the scan checks only the touched domain(s) and only surfaces candidates that crossed threshold on this run. If nothing crossed threshold this run, the offer is silently skipped — same discipline as Step 9.

Path B keeps the scan close to the moment new sources land, so the operator catches readiness when it happens rather than learning about it weeks later via Path A.

**Architectural note:** Path B creates two sequential offers after a VIS run (Step 9's compound-primer offer + Step 10's synthesis-readiness offer). This is deliberate — they serve different concerns. If this proves noisy in practice, consolidation can be considered as a future VIS edit; for now they stay separate.

## Detection logic

The scan detects two of the four synthesis shapes. Two shapes stay operator-invoked.

### Cluster-readiness detection

For each cluster folder in `03_domains/`:

1. Enumerate notes under `03_domains/<cluster>/insights/` (and any sub-folders) with `type: source` in frontmatter.
2. Count by tier:
   - Total source count
   - Load-bearing count: sources with `tier:` value of `1` or `2`
3. Gate: load-bearing count ≥ 5 (the threshold defined in multi-source-synthesis Stage 2 preconditions).
4. Check for existing cluster synthesis at `03_domains/<cluster>/cluster-synthesis-*.md`:
   - **No existing synthesis** → surface as "synthesis-ready"
   - **Existing synthesis** → compute load-bearing growth since that synthesis's `created:` date. If growth ≥ 5, surface as "synthesis-refresh ready." If growth < 5, do not surface.

Report both counts in the offer line for operator validation: `<cluster> — <total> sources / <load-bearing> load-bearing`.

### Pattern-readiness detection

Scan pattern-shaped notes in two locations:
- `05_shared-intelligence/patterns/*.md`
- `03_domains/*/insights/tactic-*.md`

For each:

1. Read frontmatter.
2. Marker for synthesis-ready (3/3): `times-observed: 3` (or higher) AND `confidence: high`. This is the current loose convention — the scan reports the detected `times-observed` and `confidence` values alongside the offer so the operator can verify before confirming.
3. Marker for watch list (close to ready): `times-observed: 2` AND `confidence:` is `medium` or `high`. Patterns with `times-observed: 2` and `confidence: low` are NOT watch-list candidates — watch list means genuinely close to ready, not just at-2.
4. Check for existing pattern synthesis at `05_shared-intelligence/patterns/pattern-synthesis-<pattern-name>-*.md`. If present, do not surface.

**Detection is heuristic.** The frontmatter convention isn't well-exercised yet (only one pattern note currently in `05_shared-intelligence/patterns/`, at 1/3). Mis-fires are possible until the convention settles. Reporting the detected counts in the offer is the safety net.

### Shapes that are NOT auto-detected

- **Cross-cluster:** requires an operator-strategic anchor question. Cannot be inferred from vault state.
- **Client-driven:** requires a current client-deliverable need. Even if a client README exists, the synthesis fires when the operator has a specific outcome to drive toward, not on file presence.

Both stay operator-invoked via direct calls to multi-source-synthesis. The scan never proposes them.

## Offer format

Numbered per shape per cluster, grouped by shape, never collapsed. Watch list items use `W` prefix.

**Standard offer (Path A, vault-wide scan):**

```
SYNTHESIS-READINESS SCAN

Synthesis-ready (cluster shape):
  1. automation-systems — 40 sources / 28 load-bearing
  2. marketing — 21 sources / 14 load-bearing
  3. app-building — 6 sources / 5 load-bearing

Synthesis-ready (pattern shape):
  (none — no patterns at 3/3 yet)

Watch list (close to ready, override to synthesize early):
  W1. pattern-three-tier-prompt-architecture — at 2/3 (times-observed: 2, confidence: medium)
  W2. pattern-llm-knowledge-bases — at 2/3 (times-observed: 2, confidence: high)

Reply with picks (multi-select; e.g., "1, 2" or "1, W1"):
  0. skip — I'll run them later
```

**Refresh-ready variant:**

```
Synthesis-refresh-ready (cluster shape, existing synthesis present):
  1. automation-systems — 45 sources / 33 load-bearing (last synthesis: 2026-03-10, +6 load-bearing since)
```

**Empty-scan handling:**

If both synthesis-ready and watch list blocks are empty, the scan reports:

```
SYNTHESIS-READINESS SCAN

No synthesis-ready candidates and no watch list items.
```

No empty prompt is issued. The skill exits.

**Path B (post-VIS) offer:**

Same format, but the introductory line names the scope: `Scanning domains touched by this VIS run: automation-systems`. Only candidates within those domains appear in the offer.

## Handoff to multi-source-synthesis

Each pick maps to a multi-source-synthesis invocation with shape + scope pre-selected:

- Pick `1` (cluster automation-systems) → invoke multi-source-synthesis with `shape: cluster`, `scope: automation-systems`, default whole-cluster scope.
- Pick `W1` (watch-list pattern) → invoke multi-source-synthesis with `shape: pattern`, `scope: pattern-three-tier-prompt-architecture`, AND pass an operator-override flag indicating "synthesized at 2/3 per operator override." The downstream skill records this in the synthesis frontmatter `notes:` field (or equivalent) AND in the synthesis body's decision-archaeology section so the audit trail is clear.

**Refresh handoff** (existing synthesis present): pass the previous synthesis's path so multi-source-synthesis reads it as context before drafting. Multi-source-synthesis frontmatter on the refresh synthesis includes `supersedes: <previous-synthesis-filename>` for lineage. The previous synthesis file stays in place; the refresh is filed alongside with a new date stamp.

**Multi-pick handoff:** if operator picks "1, 2," the skill invokes multi-source-synthesis once per pick, sequentially. Each invocation runs its own shape-and-destination confirmation gate per the multi-source-synthesis contract. This skill does not override or filter those gates.

## Discipline

### Read-only on the vault

This skill performs no writes. It scans frontmatter and counts files. All file modification happens downstream in multi-source-synthesis after operator confirms picks.

### Never auto-run synthesis

Even when invoked from VIS Step 10, the offer is operator-confirmable. The multi-source-synthesis skill has its own gates that fire after operator confirms here; both layers are preserved.

### Offer is a prompt, not a queue

If operator picks `skip` or doesn't respond, the scan exits. The list is not persisted, no follow-up reminder is scheduled. Re-invoking the scan produces a fresh detection pass against current vault state.

### Loose detection is acknowledged

Pattern-readiness depends on operator-set frontmatter that isn't strictly enforced yet. The scan reports detected `times-observed` and `confidence` values alongside each pattern offer so mis-fires are caught at the operator-confirm step. Cluster-readiness is deterministic (counts files), but tier filtering depends on operator-set `tier:` frontmatter; same caveat applies in a softer form.

## Edge cases

- **Cluster folder with no `insights/` subfolder:** treat as zero sources; do not surface.
- **Tier frontmatter missing on some sources:** count as non-load-bearing for the gate; report the gap in the offer so operator can fix attribution if needed (`marketing — 21 sources / 14 load-bearing / 3 untriaged`).
- **Pattern frontmatter missing `times-observed` or `confidence`:** treat as non-ready; do not surface in watch list or synthesis-ready.
- **Pattern with `times-observed: 2` and `confidence: low`:** not surfaced. Below the watch-list bar by design.
- **Existing synthesis with no `created:` date:** treat as recent enough to suppress (fail-safe toward not duplicating).
- **Multiple cluster syntheses already filed for one cluster:** use the most recent by `created:` date for the refresh-gate comparison.

## Cross-references

- **multi-source-synthesis skill** — the downstream skill this hands off to. All actual synthesis drafting happens there, including the shape-and-destination confirmation gate.
- **vis-extraction skill (Step 9)** — the architectural reference for the detect → offer → confirm → handoff pattern. Path B (VIS Step 10) sits directly after Step 9 in the VIS workflow.
- **meta-document-primer skill (Step C2)** — the architectural reference for specific-notes-scope override. multi-source-synthesis adopts the same override pattern (separate edit, alongside this skill).
- **conventions.md** — file-naming and folder-placement rules for synthesis outputs.

## What this skill does NOT do

- Does NOT draft synthesis content (that's multi-source-synthesis)
- Does NOT promote patterns from 1/3 to 2/3 or 2/3 to 3/3 (that's vault-curation discipline)
- Does NOT modify frontmatter (read-only)
- Does NOT commit to git
- Does NOT detect cross-cluster or client-driven readiness (those stay operator-invoked)
