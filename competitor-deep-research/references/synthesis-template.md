# Synthesis template

The synthesis is the deliverable that operators refer to when planning the client's Core 30 build or SEO foundation. Per-competitor briefs are inputs; the synthesis turns them into a plan.

Use this template after every brief is written. Don't try to write the synthesis in parallel with the briefs — the cross-competitor patterns only become visible once you've seen all of them.

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

One row per competitor. Make it scannable. Operators screenshot this table and paste it into client decks.

| Operator | Reviews | Rating | Links | Authority | Tech stack | Pages | Rank for top keyword |
|---|---|---|---|---|---|---|---|
| Competitor A | | | | | | | |
| Competitor B | | | | | | | |
| Competitor C | | | | | | | |
| Competitor D | | | | | | | |
| **Client** | | | | | | | |

Source notes: cite the ranking-data source + date.

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
- No competitive ad-spend research
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
