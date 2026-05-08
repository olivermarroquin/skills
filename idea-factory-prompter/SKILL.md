---
name: idea-factory-prompter
description: Use this skill whenever the operator asks for help drafting a thorough prompt to spawn or ingest a new strategy in the idea-factory repo. Triggers include phrases like "prompt me an idea-factory request for X", "make me a prompt to add X to the idea factory", "draft a new-chat prompt for the idea factory", "help me prompt a strategy spawn", or any request to convert a short rough idea into a comprehensive, focus-rule-aware spawn prompt for the idea-factory system. Do NOT use this skill for unrelated prompt-engineering requests outside the idea-factory context.
---

# idea-factory-prompter

Converts a short, rough idea from the operator into a fully-loaded spawn or ingestion prompt for the idea-factory repo at `workspace/repos/idea-factory/`. The output prompt is meant to be pasted into a new Claude Cowork chat in the same workspace, so the receiving chat has all context, all focus rules, and all required structure baked in.

## When to use

Operator says something like:

- "Prompt me an idea-factory request for [rough idea]"
- "Make me a new-chat prompt to add [idea] to the idea factory"
- "Draft a spawn prompt for [idea]"
- "I want to add [idea] to the stockpile, give me the prompt"
- Any equivalent that pairs a rough idea with a request for a thorough prompt

## What this skill produces

A single block of prompt text the operator can copy-paste into a new Cowork chat. Not a strategy folder. Not research. Just the prompt.

## Process

### Step 1: Read the live system state before writing

Before drafting the prompt, read these files from the idea-factory repo:

1. `workspace/repos/idea-factory/SYSTEM-SPEC.md` — to ground every prompt in current rules.
2. `workspace/repos/idea-factory/AGENT-TEMPLATE.md` — for the eleven-file structure.
3. `workspace/repos/idea-factory/INGESTION-PROTOCOL.md` — if the source is a video/ad/screenshot/idea-message vs. a from-scratch spawn.
4. `workspace/repos/idea-factory/pipeline.md` — to know what's currently Active, Pilot, or Research. **This determines what stage the new strategy is allowed to enter.**
5. `workspace/repos/idea-factory/decisions.md` — to avoid duplicating an already-killed or already-spawned strategy.
6. `workspace/repos/idea-factory/shared/synergies.md` — to detect cluster opportunities or tool overlap.

If any of these files don't exist, ask the operator — don't guess.

### Step 2: Classify the request

- **Spawn** — operator described an offer/business idea directly. Use the spawn flow from `AGENT-TEMPLATE.md`.
- **Ingestion** — operator referenced a video, ad, screenshot, podcast clip, or external source. Use the ingestion flow from `INGESTION-PROTOCOL.md`.
- **Refine existing** — operator referenced an existing strategy folder. Skip this skill; suggest a normal in-place edit instead.

### Step 3: Determine allowable stage based on pipeline state

This is the most important rule. Check `pipeline.md`:

- **Something is in Active stage** → new strategy is **stockpile-only at Research stage**. The generated prompt must explicitly forbid pilot/active verdicts. Acceptable verdicts: `research-ready` / `revise` / `kill`.
- **Something is in Pilot stage (no Active yet)** → same rule: stockpile-only at Research stage. Even Pilot blocks new pilots.
- **Nothing in Pilot or Active** → new strategy may enter Pilot stage if skeptic green-lights. Standard verdicts apply: `pilot` / `revise` / `kill`.

Bake this into the generated prompt as a non-negotiable constraint.

### Step 4: Detect synergy and cross-strategy notes

From `synergies.md` and `pipeline.md`, identify:

- **Cluster candidates** — does this new idea belong in an emerging cluster (e.g., `content-creation`)?
- **Tool overlap** — likely shared tools with an existing strategy.
- **Test-subject reuse** — has the operator already mentioned a test subject (e.g., dad, dad's business) used in another strategy? If so, reference and flag the synergy.

### Step 5: Draft the prompt using the structure below

Output a single contiguous prompt block, ready to paste. Use this structure:

```
I'm continuing work in the **idea-factory** repo. Don't re-explain the system to me — I built it with you in another chat. Read the project instructions, then read these files in order before doing anything else:

1. `workspace/repos/idea-factory/SYSTEM-SPEC.md`
2. `workspace/repos/idea-factory/AGENT-TEMPLATE.md`
3. `workspace/repos/idea-factory/INGESTION-PROTOCOL.md` *(if ingestion)*
4. `workspace/repos/idea-factory/pipeline.md`
5. `workspace/repos/idea-factory/decisions.md`
6. `workspace/repos/idea-factory/shared/synergies.md`
7. `workspace/repos/idea-factory/agents/[any specifically relevant agent files]`
8. `workspace/repos/idea-factory/strategies/[active-or-pilot strategy]/log.md` *(for context on what's in flight)*

**Critical context before you act:**

- [Current pipeline state — what's Active or Pilot, and the resulting stage cap on this new strategy]
- [Any cluster or synergy notes — which existing strategies this connects to]
- [Test-subject reuse if applicable]
- Per the system's hard focus rules, [explicit stage cap for this strategy].

**The strategy to scaffold:**

**Name:** `[proposed-kebab-case-name]` (or propose better — must reflect the offer, not the source)

**Intent:** [2–4 sentence synthesis of the operator's rough idea, sharpened. Specific buyer, specific deliverable, specific channel or platform.]

**[Test subject / source / starting context, if relevant]**

**Run the standard [spawn / ingestion] process** — eleven-file folder, with these specific things needing extra attention:

1. **`tools.md` requires a real bake-off plan** per the system rules if production speed is the deliverable. Candidate list must include at minimum: [seed list of 6–10 likely tools for this domain]. Don't pick from memory.

2. **`compliance.md` is [normal / heavier than usual] for this strategy.** [Specific compliance flags relevant to this domain — e.g., FTC AI disclosure, likeness/voice consent, ad platform rules, state laws, refund/chargeback exposure.]

3. **`offer.md` — [pricing-tier guidance: tiered like websites, single-tier, retainer-only, propose multiple models, etc. Based on what fits this strategy].**

4. **`unit-economics.md`** — be honest about [domain-specific cost dynamics — subscription tools, per-render costs, per-API-call costs, time-adjusted margin, etc.]. Show economics at 1, 5, and 20 clients.

5. **`research.md`** — include real failure cases. [Specific failure modes for this strategy domain.]

6. **`pilot-plan.md`** — [the smallest test that proves this is real, scaled to this strategy. Specific go/no-go.]

7. **`workflows.md`** — define the repeatable production workflow once tools are picked.

8. **`log.md`** — first entry should tag `source: [operator-message-YYYY-MM-DD / video-url / ad-screenshot / etc.]` and include cross-links to related strategies.

**Skeptic must enforce focus rules:** verdict cannot be `pilot` or `active` — only `[research-ready / revise / kill]` *(if there's an Active or Pilot strategy)* / *(or standard pilot/revise/kill if nothing is blocking)*.

**Update tracking files:**
- Add row to `pipeline.md` under **[Idea or Research]** stage.
- Add row to `decisions.md` with date, source, decision.
- Add entry to `shared/synergies.md` if [cluster or tool overlap detected].

**End with the standard one-line summary.** Format: *"Strategy ready at [stage]. Skeptic says X. Recommended next action: Y — but [Active/Pilot strategy] remains priority until graduation or kill."*
```

### Step 6: Add a brief operator-facing note after the prompt block

Outside the prompt block (so it's clearly *for the operator, not for the receiving chat*), include 2–4 sentences covering:

- **Why this prompt is long** (state, focus rules, synergy reminders).
- **Why the skeptic constraint is set the way it is** (current pipeline state).
- **One honest flag** about the strategy itself — research-vs-execute risk, market saturation, common failure mode for this domain. Treat the operator like a colleague, not a customer.
- **Next action** for the operator after pasting.

## Quality bar

- The prompt must reflect *current* pipeline state, not generic state. Re-read `pipeline.md` every time.
- Stage cap must always be enforced. If unsure whether something is in Active/Pilot, ask the operator before drafting.
- Tool candidate seed lists must be domain-appropriate. Don't list website builders for a video strategy.
- Failure-case prompts must be specific to the strategy's domain — don't paste a generic "find failure stories" line.
- Naming convention: lowercase-kebab-case, derived from the offer (not the source).
- Length: long is correct. New chats lack state. Redundancy is intentional protection.

## What this skill does NOT do

- Does not actually spawn the strategy. The receiving chat does that.
- Does not produce research, prices, or tool comparisons. Those belong in the strategy folder, generated by the receiving chat.
- Does not modify pipeline.md, decisions.md, or any other repo file. Read-only here. The receiving chat does the writes.
- Does not handle requests to refine an *existing* strategy folder — for that, the operator should make in-place edits in the existing chat or open a focused chat about that strategy.

## Examples

### Example A — operator gives a short rough idea (spawn)

**Operator says:**
> Prompt me an idea-factory request for: ai avatars for marketing content using my dad's photos and voice.

**Skill output:** A full spawn prompt with:
- File-read list including websites strategy log.md (since dad is shared test subject)
- Stage cap to Research only (websites is in Pilot prep)
- Tool seed list: HeyGen, Synthesia, Captions, Arcads, D-ID, Hedra, Tavus, Argil, ElevenLabs, Resemble, Descript
- Compliance flags: FTC AI disclosure, FTC Endorsement Guides revision, likeness/voice consent, deepfake state laws, Maryland-specific rules
- Synergy flag: emerging `content-creation` cluster
- Skeptic constraint: research-ready / revise / kill only
- Operator note flagging "this is fun-to-research, hard-to-sell" risk

### Example B — operator references a video (ingestion)

**Operator says:**
> Here's a YouTube video of someone explaining their AI cold email service: [url]. Add it to the factory.

**Skill output:** An ingestion prompt that:
- Routes through `INGESTION-PROTOCOL.md`, not the spawn protocol
- Requires `extraction.md`, `reality-check.md`, `decision.md` in `_inbox/` first
- Sets default disposition expectation as `skip` or `park`, not `adapt`
- Flags any verifiability concerns up front
- Stage cap to Research only if anything is currently Active/Pilot
- Ends with operator note about how often ingestion correctly results in `skip`

### Example C — pipeline has nothing Active or Pilot yet

**Operator says:**
> Prompt me an idea-factory request for productized resume rewrites with AI.

**Skill output:** Spawn prompt with **standard** skeptic verdicts (`pilot` / `revise` / `kill`) since no focus-rule conflict exists. Otherwise same structure.

## Notes for future maintenance

- If `SYSTEM-SPEC.md` adds new required files to a strategy folder, update Step 5's list of "specific things needing extra attention."
- If new agents are added that should be invoked during spawn (e.g., a new compliance agent), add them to the file-read list.
- If the focus rules change (e.g., system allows two parallel Pilots someday), update Step 3.
