# Synthesis template

The synthesis is the deliverable that operators refer to when planning the client's Core 30 build or SEO foundation. Per-competitor briefs and the Tier-2 light-scan rows are inputs; the synthesis turns them into a plan.

Use this template after every Tier-1 brief is written AND the Tier-2 rows are collected. Don't try to write the synthesis in parallel with the briefs — the cross-competitor patterns only become visible once you've seen all of them.

The template uses **12 sections in a fixed order** (Sections 1.5 and 4.5 were added by the 2026-06-03 enhancements; the section numbering preserves the original sequence).

---

```markdown
---
type: competitor-synthesis
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
project: <client-slug>
relevant-projects: [<client-slug>]
tags: [competitor-research, synthesis, <client-slug>, <geography>, <industry>]
---

# Competitor Research Synthesis — <Geography> <Industry>

**Synthesis date:** YYYY-MM-DD
**Competitors profiled:** N (<list>)
**Primary inputs:** Per-competitor briefs in this folder + <ranking-source if any>
**Purpose:** Feed <client>'s page-build / SEO / Core 30 strategy with data-grounded recommendations.

Sibling briefs:
- [[<competitor-slug>]] (primary)
- [[<competitor-slug>]] (primary)
- [[<competitor-slug>]] (secondary)
- [[<competitor-slug>]] (secondary)

---

## 1. Quick-reference comparison table

One row per Tier-1 competitor + the client. Make it scannable. Operators screenshot this table and paste it into client decks.

| Operator | Reviews | Rating | Links | Authority | Tech stack | Pages | Rank for top keyword |
|---|---|---|---|---|---|---|---|
| Competitor A (Tier 1 primary) | | | | | | | |
| Competitor B (Tier 1 primary) | | | | | | | |
| Competitor C (Tier 1 secondary) | | | | | | | |
| Competitor D (Tier 1 secondary) | | | | | | | |
| **Client** | | | | | | | |

Source notes: cite the ranking-data source + date.

---

## 1.5. Tier-2 light-scan table

*(2026-06-03 enhancement — produces the cross-validation layer for the Tier-1 findings.)*

One row per Tier-2 competitor (top 10 in the SERP / ranking-source). The Tier-1 competitors appear here too with full data; Tier-2-only competitors get the same row shape. Sort by **Avg rank for head keyword** ascending.

| # | Domain | Pages | Tech stack | Top 5 keywords | Backlinks | DA / DR | Avg rank | Svc-page words | FAQs | Schema types | AI-cite (V3) | Local-pack (V2) | Paid/LSA (V4) | Review vel. (M1) | Social (V5) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | <Tier-1 A> | | | | | | | | | | | | | | |
| 2 | <Tier-1 B> | | | | | | | | | | | | | | |
| 3 | <Tier-2> | | | | | | | | | | | | | | |
| 4 | <Tier-2> | | | | | | | | | | | | | | |
| 5 | <Tier-1 C> | | | | | | | | | | | | | | |
| 6 | <Tier-2> | | | | | | | | | | | | | | |
| 7 | <Tier-1 D> | | | | | | | | | | | | | | |
| 8 | <Tier-2> | | | | | | | | | | | | | | |
| 9 | <Tier-2> | | | | | | | | | | | | | | |
| 10 | <Tier-2> | | | | | | | | | | | | | | |

**Per-row source annotation** — append a one-line citation row beneath the table naming the method per column group per row. Example: `Cols 1–10: Rows 1, 2, 5, 7 — DataForSEO Labs ranked_keywords + Backlinks Summary 2026-06-03; Rows 3, 4, 6, 8, 9, 10 — free-toolkit. Cols 11–15: V3 — Sonar 6-prompt probe 2026-06-14; V2 — DataForSEO SERP local_pack; V4 — Ads Transparency Center (Chrome) 2026-06-15; M1 — DataForSEO business_data/my_business_info; V5 — direct channel visit.`

**Light-scan observations:**

A few bullets surfacing the patterns visible in the 15-column table that aren't already in the Tier-1 deep dives:

- Page-count distribution (where do most fall? who are the outliers?)
- Tech-stack distribution (WordPress vs static vs enterprise vs hosted-builder)
- Schema saturation (how many emit JSON-LD at all? which types are common?)
- FAQ saturation (proportion of pages with embedded FAQs)
- **Cross-arena heat map** *(v1.4)*: which competitors are active across multiple arenas (organic + local + paid + AI + social) vs single-arena specialists? Surface the 1–2 competitors with the broadest arena coverage — they are the hardest to displace.
- **Review-velocity leaders** *(v1.4)*: who is growing review count fastest? Velocity is the durable lever (spec §3 M1) — a competitor with 200 reviews at 15/month will overtake a competitor with 1,000 reviews at 2/month.
- **Paid-arena density** *(v1.4)*: how many of the 10 competitors run ads? If the arena is contested (6+ running ads), the client needs a paid strategy to compete. If it's empty (0–2 running ads), paid is a wide-open opportunity.
- The 1–2 Tier-2-only competitors that look surprisingly strong (potential Tier-1-promotion candidates for the next refresh cycle)

---

## 2. The headline finding

The single most important pattern in the data. One paragraph + the evidence behind it. Every market has its own headline finding — surface it explicitly.

Examples:
- "Content depth beats domain authority in this niche" (with the evidence: high-authority competitor losing to high-content competitor)
- "Local-pack is owned by the operator with the most reviews + closest physical address"
- "Schema markup is universal — competing on schema isn't a differentiator here"

The headline finding shapes the rest of the synthesis. Get it right.

---

## 3. Common patterns ALL competitors share

What everyone does. These are table stakes — the client can't differentiate by doing them, only lose by skipping them. Usually 6–10 bullets.

Examples of common patterns to look for:
- Service × location URL matrix (any depth)
- 24/7 or same-day positioning
- WordPress or another mainstream CMS
- Outsourced marketing agency
- Licensed/insured displayed in footer
- Coupon/promotion mechanic
- No transparent pricing
- Limited or no FAQ embedding
- No founder personality

---

## 4. Differentiation opportunities (what nobody does well)

What NOBODY does well. These are the gaps the client can exploit. Make each one concretely actionable — each should map cleanly to a specific page or feature on the client's build.

Number them. Each gets a one-paragraph treatment with:
- The gap (what's missing across the competitive set)
- Why it's a gap (what opportunity it leaves on the table)
- How the client can exploit it (specific to the client's actual capabilities and strategy)

Typical count: 7–12 differentiation opportunities.

---

## 4.5. Cross-competitor structural pattern

*(2026-06-03 enhancement — the "what does winning content look like at the page structural level" rollup.)*

Roll up the per-competitor top-5-pages findings (from each Tier-1 brief's Section 7.5) into one cross-competitor view. This is the structural blueprint the Phase 3a scaffolder should reproduce.

**Per-trait cross-competitor table:**

| Structural trait | Competitor A top-5 | Competitor B top-5 | Competitor C top-5 | Competitor D top-5 | Cross-competitor verdict |
|---|---|---|---|---|---|
| Word count band | 5 of 5 @ 3,500–4,000 | 4 of 5 @ 1,800–2,400 | 3 of 5 @ 1,200–1,500 | 5 of 5 @ 2,000–2,800 | Winning pages cluster at 2,000–4,000; sub-2,000 trails |
| Why-choose-us tile structure | 5 of 5 (6 tiles) | 4 of 5 (4 tiles) | 3 of 5 (any) | 5 of 5 (4 tiles) | Universal — 4–6 tiles standard |
| Named-neighborhood density | 5 of 5 (5+) | 1 of 5 (≥1) | 0 of 5 | 2 of 5 (≥3) | Only the strongest competitor does this consistently |
| FAQ count band | 4 of 5 (5 FAQs) | 2 of 5 (3 FAQs) | 0 of 5 | 4 of 5 (6 FAQs) | 4–6 inline FAQs is the winning range |
| Case studies inline | 5 of 5 (1 named) | 0 of 5 | 0 of 5 | 2 of 5 (1 generic) | Strongest competitor's signature; weakest don't do it at all |
| Schema types | 0 of 20 emit FAQPage | — | — | — | Universal gap across all 4 competitors |
| Internal-link density to siblings | 5 of 5 (10+) | 3 of 5 (5–8) | 1 of 5 (2–4) | 4 of 5 (6–10) | High density correlates with ranking |
| Hero treatment | 5 of 5 (real tech photo) | 5 of 5 (stock) | 5 of 5 (illustration) | 5 of 5 (stock) | Only the strongest uses real photos consistently |

**The winning structural blueprint:**

One paragraph naming the structural pattern the data points to. Example: "Winning Fairfax-electrician pages systematically: (a) run 2,000–4,000 words, (b) embed a 4–6 tile differentiator section above the fold, (c) name 3–5+ specific neighborhoods, (d) include 4–6 inline FAQs, (e) embed at least 1 city-specific case study, (f) link densely to sibling city pages in-body. Schema markup is absent across all top-5-trafficked pages on all 4 Tier-1 competitors — a market-wide gap. Hero photography quality differentiates the strongest from the rest. The client's Core 30 build should match every (a)–(f) trait and add FAQPage + AggregateRating schema to take the universal gap."

**Tier-1 vs Tier-2 cross-validation:**

Do the traits in the table above also appear in the Tier-2 light-scan rows? If yes, the structural blueprint is market-wide. If a trait shows up only in Tier-1 (not in the Tier-2-only competitors), it may be specific to the strongest few — call that out. Example: "The 2,000+ word count band holds across both tiers; the 4–6 inline FAQs pattern is concentrated in the Tier-1 set and absent from most Tier-2-only competitors — Tier-1-specific, possibly idiosyncratic."

**Per-trait source annotation:**

Cite which top-5-pages set + which method (DataForSEO Labs / SimilarWeb / sitemap-heuristic) contributed each verdict, so future refreshes can re-derive cleanly.

---

## 5. Keyword targets ranked by competitiveness

Four tiers. For each tier, name specific keywords and explain why they're at that difficulty level.

### Tier 1 — HARD (do not attack head-on)
The keywords the dominant competitor owns. List them with the evidence. Recommend competing on adjacent phrasing instead.

### Tier 2 — MODERATE (winnable with focused page build)
Keywords where the leading competitor has coverage but with thin or replicable pages. Client can compete with depth.

### Tier 3 — EASY (uncontested or weakly contested)
Keywords where no competitor has a dedicated page, or the existing pages are generic. These are the wedge opportunities.

### Tier 4 — DEFENSIVE (already winning, keep claiming)
Keywords the client already ranks for. Don't lose ground; reinforce.

---

## 6. Tech stack pattern: the "winning stack" in this niche

What the data shows about which infrastructure choices correlate with ranking outcomes. Use a small comparison table:

| Element | Winning approach | Acceptable approach | Avoid |
|---|---|---|---|
| Hosting | | | |
| CMS | | | |
| Cache/CDN | | | |
| Images | | | |
| Schema | | | |
| Content depth | | | |
| Internal linking | | | |
| Tracking | | | |

Then: **Client's current stack vs. the winning stack** — one paragraph identifying what to keep, what to upgrade, what to ignore. Be honest about platform-migration cost; don't recommend changes the client can't actually afford.

---

## 7. Top 10 recommendations for the client's page build

Ordered by impact-to-effort ratio. Each recommendation should:

- Map to a specific finding from the briefs (cite the finding)
- Name what to build, not just what to consider
- Be sized for the client's actual resources

Example formats:
- "Implement JSON-LD LocalBusiness + Service + FAQPage schema on every Core 30 page. None of the competitors emit these inline."
- "Build neighborhood-specific content within each city page (named neighborhoods: X, Y, Z). Competitor A names them but has no dedicated pages."
- "Lead the brand with troubleshooting + chandeliers — three service lines that no competitor headlines."

---

## 8. Top 3 risks if the client doesn't act

What happens if they delay. Each risk should be:
- Concrete (not generic "competition gets harder")
- Time-bound where possible ("AJ Long publishes one new city page per week")
- Anchored to a finding from the briefs

---

## 9. Blocked questions / follow-up research

Honest about gaps. Anything that:
- Couldn't be confirmed in this round (SPA-rendered sites that needed browser tools, paid-tool gates, time-budget overruns)
- Surfaced as worth researching but wasn't in scope this cycle
- Would change the recommendations if the data turned out differently

This section signals integrity. Operators trust briefs that admit uncertainty.

---

## 10. Methodology

This section makes the work reproducible and extensible. Append it at the end of the synthesis.

### How competitors were identified
Describe the two-source funnel: prior-data source (BrightLocal, Ahrefs, prior audit) + live Google search. Name the keywords searched, the directories excluded (Yelp, BBB, Angi, etc.), and the criteria for primary vs. secondary classification.

### Tools used per competitor
A table or list of the tools applied at each step:
- `WebFetch` for source-scrape
- `WebSearch` for identifying secondaries + finding canonical URLs
- Bash `curl -sI` for HTTP response headers
- Bash `curl + sitemap.xml` inspection for page counts
- Manual reading of fetched markdown for tech stack fingerprinting
- Cross-reference with prior-data scans

### Decision criteria — what's working vs. what's not working
Restate the three tests for "what's working" bullets:
1. Hard data confirms it
2. It explains a ranking outcome
3. It's a customer-trust mechanism even outside SEO

And the three tests for "what's NOT working" bullets:
1. Exploitable by the client
2. Confirmable in source
3. Aligned with the client's strategic intent

### Gaps and limitations
List specifically what this round of research couldn't reach. Common ones:
- WebFetch doesn't execute JavaScript (SPA-rendered sites returned empty)
- Schema markup audit was source-level only (didn't run Google Rich Results Test)
- Backlink data is from a single source and may be stale
- No automated content-depth measurement (word counts estimated, not tokenized)
- Only one service-page and one location-page audited per competitor
- No mobile-specific audit
- No competitive ad-spend research (note: V4 column captures presence/count from Transparency Center, not spend)
- Cross-arena columns (V3/V2/V4/M1/V5) are point-in-time flags — they don't track change over time without a baseline
- Client's own current state wasn't deeply compared at page level

### What I'd do differently next time
A short list of process improvements observed during the work. Common ones:
- Confirm WebFetch provenance up-front by searching for each target domain first
- Use browser-rendered tools (Claude in Chrome) for SPA-rendered sites
- Run Google Rich Results Test on each homepage for definitive schema verdict
- Capture one screenshot per competitor for visual-design quality
- Tokenize page content for hard word counts via a small script
- Build the synthesis incrementally as cross-cutting notes accumulate
- Run two passes per competitor: data first, narrative second
- Time-box explicitly per competitor

---

## Sources

- [<competitor-slug>.md](<competitor-slug>.md)
- [<competitor-slug>.md](<competitor-slug>.md)
- ...
- [Ranking-data source PDF](path/to/source)
- [Client project README](../../README.md)
```
