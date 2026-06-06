---
type: reference
status: canonical
created: 2026-05-27
updated: 2026-05-27
related: [perplexity-refinement]
tags: [reference, perplexity, query-templates, refinement]
---

# Perplexity refinement — query templates

The six query shapes the perplexity-refinement skill uses in Phase 2. Each template has a description of when it fires, a parameterized template, a worked example, and notes on what makes the query land well in Perplexity Pro Search.

These templates are sized for **Pro Search** specifically (the heavier-compute mode that justifies the $21.20/mo subscription). Pro Search reads like a small research agent — it expands the query, runs sub-searches, and synthesizes across them. Phrasing that invites it to cite primary sources tends to land better than terse phrasings.

---

## Template 1 — Validate a claim

**Fires when:** the artifact makes a specific factual assertion that can be cross-checked against an authoritative source. Examples: "Federal Pacific panels are documented fire risks," "Astro publishes directly from Claude Code without a CMS login," "Watchdog tracks weekly competitor changes."

**Template:**

```
Is it true that <restate the claim in one sentence>? Cite primary sources
where possible. If the claim is partially true, explain which parts are
correct and which need qualification. If the claim is contested, surface
the strongest counter-position with citations.
```

**Worked example (from the panel-upgrade brief):**

```
Is it true that Federal Pacific Stab-Lok breakers fail to trip in
measurable percentages of cases and pose a documented fire risk? Cite
primary sources where possible. If the claim is partially true, explain
which parts are correct and which need qualification.
```

**What this query is fishing for:**

- Primary sources (testing labs, court filings, industry reports) that back the claim
- Independent corroboration (multiple bodies confirming the same risk)
- Qualifications (e.g., "only in certain panel sub-models," "only at certain amperages")
- Counter-positions (manufacturer rebuttals, alternative explanations)

**How to score the result:**

- Validates → multiple primary sources back the claim cleanly
- Partially validates → main thrust correct but the wording in the artifact overstates / understates
- Contradicts → primary sources push back; the artifact may be wrong or stale
- Inconclusive → Perplexity surfaces speculation only; not enough hard sourcing

---

## Template 2 — Validate a tool's current state

**Fires when:** the artifact names a tool, product, or service and treats its current pricing, feature set, or reputation as load-bearing. Tools go stale fast — pricing changes, features ship, products get acquired or shut down.

**Template:**

```
What is the current pricing, feature set, and reputation of <tool name>
as of 2026? Cite the vendor's pricing page and any independent reviews
or comparison articles. Note any major changes in the last 12 months
(price increases, new tiers, deprecated features, acquisitions).
```

**Worked example (from the SEO tooling inventory):**

```
What is the current pricing, feature set, and reputation of Otterly.ai
as of 2026? Cite the vendor's pricing page and any independent reviews
or comparison articles. Note any major changes in the last 12 months
(price increases, new tiers, deprecated features, acquisitions).
```

**What this query is fishing for:**

- The vendor's current pricing page (the canonical source)
- Recent third-party reviews (Capterra, G2, vendor-comparison blogs)
- Recent feature changelog or product updates
- Any acquisition / shutdown / pivot news

**How to score the result:**

- Validates → pricing and features match what the artifact claims
- Updates → pricing or features have shifted; the artifact should be amended
- Contradicts → the tool no longer exists, or its positioning has fundamentally changed
- Inconclusive → only marketing copy returned; no independent reviews surfaced

---

## Template 3 — Validate a statistic

**Fires when:** the artifact quotes a specific number — a percentage, a dollar range, a count, a benchmark. Stats are especially worth refining because they often trace to a single study that may or may not hold up.

**Template:**

```
What is the original source of the statistic "<exact stat from artifact>"?
Is the statistic currently accurate as of 2026? Cite the primary study or
data source where the number originated, plus any independent corroboration
or contradiction. If the stat traces to a single study, name the study, the
publication date, the sample size, and the methodology.
```

**Worked example (from the Nico Four Systems source note):**

```
What is the original source of the statistic "only about 60% of published
blog content stays indexed in Google over time"? Is the statistic
currently accurate as of 2026? Cite the primary study or data source
where the number originated, plus any independent corroboration or
contradiction.
```

**What this query is fishing for:**

- The original study or data source (often a single industry report)
- The study's methodology and sample size (so the operator can judge weight)
- Any independent corroboration from a second methodology
- Any update or revision since the original publication

**How to score the result:**

- Validates → original study found, methodology defensible, no contradicting evidence
- Partially validates → original study found but methodology limits generalization
- Contradicts → original study debunked, or independent data contradicts the number
- Inconclusive → no primary source surfaced; stat appears to be folklore

---

## Template 4 — Deepen a concept

**Fires when:** the artifact references a named concept (pattern, technique, principle) and the operator could benefit from more expert voices on it. Examples: Capsule Content technique, Attribute Match, structural-vs-editorial backlinks, fan-out cluster dashboard.

**Template:**

```
What are the latest 2026 perspectives on <concept name>? Surface 3-5
expert viewpoints with citations. Include both the canonical articulation
(if there's a recognized originator) and any alternative framings or
extensions from other practitioners. Briefly note where the perspectives
agree and where they diverge.
```

**Worked example (from the SEO tactic notes):**

```
What are the latest 2026 perspectives on the "Capsule Content" technique
for AI search citation? Surface 3-5 expert viewpoints with citations.
Include both the canonical articulation (if there's a recognized
originator) and any alternative framings or extensions from other
practitioners. Briefly note where the perspectives agree and where they
diverge.
```

**What this query is fishing for:**

- The canonical source for the concept (who coined it, when, in what context)
- Adjacent or competing frameworks (multiple ways the same problem is solved)
- Recent expert commentary (blog posts, podcasts, conference talks)
- Points of disagreement among practitioners

**How to score the result:**

- New perspectives → 3+ voices surface that weren't in the artifact
- Reinforces → only the same voices the artifact already cites surface
- Contradicts → the concept turns out to be contested or recently debunked
- Inconclusive → concept is too niche; Perplexity finds little

---

## Template 5 — Find counter-evidence

**Fires when:** the artifact takes a strong position and the operator wants to pressure-test it before relying on it. Counter-evidence queries are especially valuable on decision docs, strategy notes, and synthesis docs that recommend a path.

**Template:**

```
What are the strongest arguments against <claim, position, or
recommendation>? Surface 3-5 counter-positions with citations. Include
both empirical counter-evidence (data that contradicts) and reasoned
critiques (arguments that the framing itself is flawed). Don't soften —
I want the strongest version of the counter-case.
```

**Worked example (from the panel-upgrade brief):**

```
What are the strongest arguments against the position that residential
electrical contractors should NOT publish pricing on their service pages?
Surface 3-5 counter-positions with citations. Include both empirical
counter-evidence (e.g., conversion-rate data) and reasoned critiques
(e.g., consumer-trust arguments). Don't soften the counter-case.
```

**What this query is fishing for:**

- Empirical pushback (data, studies, A/B tests that contradict)
- Reasoned critique (arguments the framing itself is wrong)
- Cases where the opposite worked (counter-examples)
- The most charitable version of the opposing view

**How to score the result:**

- Substantial counter-evidence → flag for operator review; the artifact's position may need to soften
- Weak counter-evidence → operator can note the counter-position briefly and proceed
- No counter-evidence → operator has confidence; position holds
- Inconclusive → Perplexity surfaces only meta-commentary; not enough hard sourcing

---

## Template 6 — Find updated info

**Fires when:** the artifact was written some time ago and the operator wants to know what's changed since. Especially useful for briefs (which have a refresh trigger of 6 months), tactic notes, and SEO / AI-search content (which moves fast).

**Template:**

```
What's changed about <topic> since <date in artifact>? Surface 3-5
material developments with citations. Include product launches, pricing
changes, algorithm updates, new entrants, or shifts in expert consensus.
Skip developments that don't change operational decisions; focus on what
would change how someone acts on the topic.
```

**Worked example (from the panel-upgrade brief, refresh trigger 6 months out):**

```
What's changed about residential electrical panel-upgrade pricing,
permitting, and code requirements since May 2026? Surface 3-5 material
developments with citations. Focus on what would change how a
homeowner researches the service or how a contractor positions it.
```

**What this query is fishing for:**

- New developments since the artifact's `created` or `updated` date
- Changes that affect operational decisions (vs. cosmetic news)
- The pace of change (lots of motion vs. quiet period)
- Any reversals of earlier conclusions

**How to score the result:**

- Significant updates → refresh the artifact; multiple things have shifted
- Minor updates → annotate the artifact with the new info; full refresh not yet needed
- No updates → the artifact is current; note "checked YYYY-MM-DD, no changes"
- Inconclusive → Perplexity finds little; topic may be slower-moving than assumed

---

## Picking the right template

Match category to template:

| Category from Phase 1b | Default template |
|---|---|
| Factual claim | Template 1 — Validate a claim |
| Tool / product named | Template 2 — Validate a tool's current state |
| Statistic quoted | Template 3 — Validate a statistic |
| Concept that could be deepened | Template 4 — Deepen a concept |
| Entity (person, business, place) | Template 1 (claim-style) or Template 4 (perspective-style) depending on what the artifact asserts |
| Decision or recommendation | Template 5 — Find counter-evidence |
| Anything in an artifact older than 6 months | Template 6 — Find updated info |

When an item could fit multiple templates, pick the one that best matches the operator's stated focus area. If no focus area, default to the template whose verdicts (validates / updates / contradicts) most directly answer the question the artifact poses.

---

## What good Perplexity Pro queries look like

A few principles for landing useful answers:

1. **Be specific about what counts as evidence.** "Cite primary sources" and "include the publication date" beat "find sources." Pro Search will work harder when the bar is named.

2. **Name the date when relevance is time-bound.** "As of 2026" or "since May 2026" anchors the search to the period the artifact cares about. Pro Search often returns 5-year-old content if no date is named.

3. **Ask for counter-positions explicitly.** Perplexity is biased toward confirming the framing of the question. Adding "include counter-positions" or "don't soften the counter-case" surfaces the opposing view it would otherwise underweight.

4. **Cap the response size.** "Surface 3-5 expert viewpoints" beats "find expert viewpoints." Without a cap, Pro Search can sprawl across 10+ low-quality sources and dilute the answer.

5. **Don't over-prompt.** The templates above are calibrated; adding more instructions tends to make Pro Search defensive. Keep to one paragraph per query.

---

## What bad Perplexity Pro queries look like

Three failure modes the templates above are designed to avoid:

- **Yes/no questions with no source ask.** "Is FPE dangerous?" returns "Yes" with vague sourcing. Template 1's "cite primary sources" anchor fixes this.
- **Open-ended deep-dive prompts.** "Tell me everything about Capsule Content" returns a sprawl that's hard to cite back to specific URLs. Template 4's "surface 3-5 expert viewpoints" caps the spread.
- **Stat questions without provenance ask.** "Is 95% accurate?" returns "It's a commonly cited figure" with no trace to the original study. Template 3's "name the study, the publication date, the sample size, and the methodology" gets to provenance.

---

## See also

- `[[../SKILL]]` — the perplexity-refinement skill that uses these templates
- `[[plain-language-conventions]]` — voice rules (queries themselves stay plain)
- `[[conventions]]` — KOS naming and frontmatter
