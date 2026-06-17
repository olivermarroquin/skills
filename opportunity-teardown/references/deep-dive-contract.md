---
type: skill-reference
skill: opportunity-teardown
version: 1.0
created: 2026-06-16
updated: 2026-06-16
tags: [skill-reference, opportunity-teardown, deep-dive-contract, teardown, money-map, build-vs-buy]
---

# Deep-Dive contract (§6) — full report, vetted keepers only

Produced only for a candidate the operator + the engine agree has real value (post-gate). This is the expensive tier;
it earns its cost with depth a decision can be made from.

**Format = a full report:** plain-language, intellectual-but-understandable explanations, **plus diagrams/visuals where
they help** (keepers only — §6.4). **Two-file output** (`reference_pattern_two_file_artifact_split`):

1. a **human markdown report** (the prose below), and
2. a **machine-readable YAML block** (the structured fields, for the registry + Dataview) — embedded as a fenced
   ```yaml block at the top of the report, or as a sibling `.yaml` if the registry wants it separate.

**Evidence discipline runs throughout (no hype laundering):** every factual or quantitative claim carries an evidence
tag — `verifiable` / `partially-verifiable` / `unverifiable` / `likely-fake` — borrowed from the idea-factory
`INGESTION-PROTOCOL`. Strip guru optimism. Real numbers in the ROI math, not vibes.

---

## §6.1 The teardown — what it is and why it wins

Every field below is required. Write each in plain language; gloss jargon inline.

- **Angle / positioning** — how it's framed and sold.
- **Creative & marketing hooks** — the specific pitch/angles that make it land (not "good marketing" — the actual
  hooks).
- **The problem it solves & who has it** — *and what that pain actually looks like in real life,* in plain language
  with concrete real-world examples, so the value lands the way a customer feels it. This is the field people skip and
  shouldn't.
- **How it's actually used** — a **use walk-through**, step by step, not a feature description.
- **Rare-and-valuable core** — what's genuinely defensible / hard to copy.
- **How they likely build it** — stack, inputs, effort, the production method as best inferred (tag confidence).
- **Replication requirements** — what it would take *us* to ship it end-to-end.
- **Value → money mechanism** — where value converts to revenue; pricing/packaging.
- **The one key money-making insight** — a **single sentence**: *why this prints money.* If you can't write it in one
  sentence, you don't understand the business yet.
- **Why buyers are pulled in** — what it saves them: time / money / energy / risk / status.
- **Moat & gaps** — defenses, and the weaknesses a better version would exploit (these feed the level-up).
- **Build-for-myself-first fit** — does Oliver actually want this for his own use? **The north-star filter.** Be
  honest; "no" is a valid and useful answer.
- **Effort-to-clone** — T-shirt size (**S / M / L**) with the current stack, one line of justification.
- **Evidence / confidence tag per claim** — `verifiable` / `partially-verifiable` / `unverifiable` / `likely-fake`.

---

## §6.2 The hands-on trial + build-vs-buy-vs-use-as-is decision

The most money-relevant output. Produce a clear recommendation:

- **Worth paying for a month to try hands-on?** — so Oliver can feel the value, learn how it's built from the inside,
  and find the gaps. **The engine recommends; Oliver decides and makes the purchase — the engine never spends money on
  its own.** State the cost and what the month would teach.
- **The three-way call, honestly:**
  - **Rebuild it ourselves** — and roughly, does that actually save money or cost more than it's worth? Put a number on
    it (build hours × Oliver's effective rate vs. the tool's annual cost).
  - **Use the tool as-is to make money faster** — sometimes the right move is *don't rebuild, just use it and start
    earning.* **The engine must say this out loud when it's true** — a built-in guard against the
    over-build-the-factory trap (CLAUDE.md Core Principle: *when in doubt, ship*).
  - **Skip** — not worth Oliver's time at all.

State the recommended call **and** the runner-up, with the reasoning. "Use as-is" winning is a success, not a failure.

---

## §6.3 The money / go-to-market layer — turn the teardown into a money plan

For pursued candidates, map how it becomes income. Real numbers, honest math.

- **Sectors & domains it connects to** — which business areas this is useful for; which **pains there are worth real
  money.**
- **Where to plug it in** — concrete ideas for applying it across different business areas.
- **Who to pitch + price + the ROI justification** — which clients, what price, and the honest math: *their* benefit in
  real dollars vs. what they'd pay Oliver, so the price is defensible. **Real numbers, not vibes.**
- **How it becomes a Keelworks service** — the path from "interesting tool" to "thing on the menu."
- **Short-term vs. long-term play** — fast cash now vs. the bigger payoff later.
- **The crawl → walk → run playbook** — start small/fast, make money early, keep building toward the higher-value
  version where the real money and client value live.

---

## §6.4 Visuals (keepers only)

Generate simple diagrams/sketches **only where they aid a decision** (how it works, or what the better version looks
like) — not on every item, and not in the quick pass. **Image/diagram generation that must land in the vault runs
host-side, not from the Cowork sandbox** (`reference_cowork_chrome_screenshots_not_vault_reachable`). In Cowork,
produce inline previews (e.g. a Mermaid block or an ASCII sketch) and **flag** any asset that needs host-side rendering
to be committed to the vault. Never silently let an image deliverable fail to land.

---

## Machine-readable YAML block (the second file)

Emit this structured block so the registry + Dataview can read the teardown without parsing prose. Keep keys stable
across profiles (the registry in `[OR-1.3]` consumes them).

```yaml
candidate: <name>
profile: product-offer            # or startup-funding | oss-skill | mcp-connector
provenance: { lane: A, source: <url-or-note>, date: YYYY-MM-DD }
fresh_growing: { recency: <1-5>, velocity: <1-5>, saturation_penalty: <1-5>, evidence: <short> }
the_one_money_insight: <single sentence>
build_for_myself_fit: yes | partial | no
effort_to_clone: S | M | L
decision: rebuild | use-as-is | skip
decision_runner_up: rebuild | use-as-is | skip | <level-up-concept-slug>   # "the better version is the runner-up" is a legitimate engine outcome; if so, use a slug that also appears in level_up_concepts
trial_recommended: yes | no
trial_cost_usd: <number or null>
money: { short_term: <one line>, long_term: <one line>, keelworks_service: <one line> }
scores: { tier: <1-4>, relevance: <1-5>, actionability: <1-5>, monetization: high|medium|low|none }
level_up_concepts: [<concept-1-slug>, <concept-2-slug>]   # filled by level-up step
links: [ "[[parent-context]]", "[[peer-candidate]]", "[[applicable-tool]]" ]
evidence_tags_present: true        # confirms every claim in the prose carries a tag
```

## Definition of "done" for a deep dive
- Every §6.1 field present and non-empty.
- The one money insight is a single sentence.
- §6.2 names a recommended call **and** a runner-up with reasoning, and "use-as-is" was genuinely considered.
- §6.3 ROI math uses real numbers.
- Every claim carries an evidence tag; a full-artifact grep finds no untagged claims, no placeholders, no broken links.
- Both files produced (human report + YAML block).
- `gate-peer-reviewer` (G-default) + `output-quality-loop` run and passed via an **independent** reviewer.

## Related
- `[[SKILL]]` · `[[quick-pass-contract]]` (the tier before) · `[[level-up-frameworks]]` (the tier after) · `[[profiles]]`
- spec `[[spec-opportunity-teardown-engine]]` §6 / §6.2 / §6.3 / §6.4
