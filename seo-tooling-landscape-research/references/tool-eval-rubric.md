---
name: tool-eval-rubric
description: Scoring rubric for evaluating SEO tools — used by discovery mode and operator intake pipeline to produce consistent adopt/skip recommendations
type: reference
status: canonical
created: 2026-06-15
updated: 2026-06-15
skill: seo-tooling-landscape-research
tags: [reference, seo, tool-eval, rubric, scoring]
---

# Tool-Eval Rubric (v1.0)

Standard scoring rubric for evaluating any SEO-adjacent tool that enters the system — whether
discovered by the recurring scan (discovery mode) or dropped by the operator (intake pipeline).
Every `tool-*.md` note produced by either mode includes a filled rubric.

## The five dimensions

| # | Dimension | Question it answers | Scale | Weight |
|---|---|---|---|---|
| 1 | **Value** | What new signal or capability does this tool give us that we can't get today? | 0–3 | 30% |
| 2 | **Time saved** | How much operator/analyst time does it save per use vs. the manual alternative? | 0–3 | 25% |
| 3 | **Cost** | What does it cost relative to the value delivered? (Inverted: lower cost = higher score) | 0–3 | 15% |
| 4 | **Fit** | How well does it fit the current client vertical (residential services), agency size (solo/small), and workflow? | 0–3 | 20% |
| 5 | **Overlap** | How much does it duplicate tools already in the stack? (Inverted: less overlap = higher score) | 0–3 | 10% |

### Scoring guide per dimension

**Value (0–3)**
- 0 = No new signal; duplicates what we already measure
- 1 = Minor incremental signal (slightly better data on something we already track)
- 2 = Meaningful new signal (covers a gap in `_data-gap-register.md` or opens an arena we weren't measuring)
- 3 = Category-defining signal (the only way to get this data, or dramatically better than alternatives)

**Time saved (0–3)**
- 0 = No time savings; same effort as the manual workaround
- 1 = Saves minutes per use (convenience, not transformation)
- 2 = Saves hours per client per month (automates a recurring manual workflow)
- 3 = Saves days or eliminates a bottleneck entirely (e.g., geo-grid that would take 8+ hours manually)

**Cost (0–3, inverted)**
- 3 = Free or included in a tool we already pay for
- 2 = Under $30/mo (fits solo-tier budget without discussion)
- 1 = $30–$100/mo (requires justification; must score high on Value + Time)
- 0 = Over $100/mo or enterprise-gated pricing (must be category-defining to justify)

**Fit (0–3)**
- 0 = Wrong vertical (e.g., enterprise e-commerce tool for a local-services agency)
- 1 = Tangentially relevant (could be useful but not calibrated for our context)
- 2 = Good fit (designed for or works well with local services / small agencies)
- 3 = Purpose-built for our exact use case (local services SEO, small agency, multi-client)

**Overlap (0–3, inverted)**
- 3 = No overlap; fills a gap no current tool covers
- 2 = Minor overlap; does one thing a current tool does but adds significant unique capability
- 1 = Moderate overlap; replaces part of an existing tool but doesn't clearly justify the switch
- 0 = Full overlap; another tool in the stack already does this equally well

## Composite score and thresholds

**Weighted composite** = (Value * 0.30) + (Time * 0.25) + (Cost * 0.15) + (Fit * 0.20) + (Overlap * 0.10)

| Composite | Recommendation | Action |
|---|---|---|
| **2.0–3.0** | **Adopt** | Write `tool-*.md` with `status: adopted`. Add to `keelworks-standard-seo-stack.md` at the appropriate tier. Register TG-row as "adopted" in `_data-gap-register.md`. |
| **1.5–1.9** | **Trial** | Write `tool-*.md` with `status: evaluating`. Register TG-row as "trial." Set a revisit trigger (date or event). |
| **1.0–1.4** | **Watch** | Write `tool-*.md` with `status: evaluating`. No TG-row unless it closes a known data gap. Re-evaluate at next quarterly scan or if pricing/features change. |
| **0.0–0.9** | **Skip** | Write `tool-*.md` with `status: killed`. Brief note on why. No TG-row. |

## Override rules

The composite score is a starting point, not a mandate. These overrides apply:

1. **Data-gap closer override:** If a tool directly closes a DG-row in `_data-gap-register.md` with status "open," bump the recommendation one tier (e.g., Watch → Trial, Trial → Adopt) regardless of composite score. The register is the system's memory of what it needs.

2. **Cost ceiling override:** If the tool costs >$100/mo AND the composite is below 2.5, force to "Watch" regardless. Solo-tier budget discipline.

3. **Enterprise-gated override:** If pricing requires a sales call or "contact us" and the tool scores below 2.0, force to "Skip." We don't chase enterprise pricing at current scale.

4. **Stack consolidation override:** If adopting the tool would let us drop an existing tool (net cost reduction or simplification), add +0.3 to the composite before applying thresholds.

5. **Business viability override:** If the vendor shows signs of imminent failure — declining MRR (monthly recurring revenue), listed for sale, >50% customer churn, founder exit, or no funding with no revenue — downgrade the recommendation one tier (e.g., Watch → Skip, Trial → Watch). Client-facing tooling that may not exist in 6 months is a liability regardless of feature quality. First exercised on LocalRank.so (2026-06-15): composite 1.20 (Watch) downgraded to Skip due to -39% MRR decline, 68% churn, listed for sale.

## How to use this rubric

### In discovery mode
The discovery scan produces a candidate list. For each candidate, fill the five dimensions using
research data (vendor pages, reviews, practitioner commentary). Write the scored rubric into the
`tool-*.md` note. Candidates scoring Adopt or Trial get a TG-row in the register.

### In operator intake
The operator drops a tool (link, name, or video URL). After research/VIS (structured intelligence extraction from video/article sources) extraction, fill the
rubric in the `tool-*.md` note. Present the scored rubric + recommendation to the operator
before registering a TG-row (operator confirms or overrides).

### Rubric block template (paste into tool-*.md)

```markdown
## Eval rubric

| Dimension | Score | Rationale |
|---|---|---|
| Value | /3 | |
| Time saved | /3 | |
| Cost | /3 | |
| Fit | /3 | |
| Overlap | /3 | |

**Composite:** X.X / 3.0
**Recommendation:** Adopt / Trial / Watch / Skip
**Override applied:** None / [describe]
**Data gaps closed:** [DG-X if applicable]
```

## Versioning

- v1.0 (2026-06-15): Initial rubric. Calibrated against Keelworks residential-services context.
  Dimensions and weights derived from the MI-2 tool-gap pass (TG-1 through TG-6) and the
  operator's stated priorities (value of new signal > cost savings > workflow fit).

## See also

- [[_data-gap-register]] — the tool-gap table this rubric feeds
- [[keelworks-standard-seo-stack]] — where adopted tools land
- [[seo-tooling-landscape-research/SKILL.md]] — parent skill
