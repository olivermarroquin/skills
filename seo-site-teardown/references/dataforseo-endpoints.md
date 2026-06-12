# DataForSEO endpoints used in SEO Site Teardown

Quick reference for the exact API calls, parameters, and costs. All calls go through the
tier-3 wrapper at `~/workspace/second-brain-tier3/automation/scripts/dataforseo_query.py`.

## Pre-flight

Before Pass 3, confirm:
1. Wrapper probes clean: `python3 dataforseo_query.py --probe`
2. Which subscriptions are active — **Labs** is required for ranked_keywords + historical.
   **Backlinks** is separate and often not subscribed. Note non-active subs explicitly.
3. Sufficient balance (~$0.05–0.50 for a full teardown depending on domain size).

## Pass 3 — What ACTUALLY ranks

### 1. Ranked Keywords (the most important call)

**Endpoint:** `dataforseo_labs/google/ranked_keywords/live`

**Purpose:** What keywords the domain ranks for, estimated traffic/value, and critically
**which URLs** rank (new programmatic pages or old legacy pages?).

```json
{
  "target": "<domain>",
  "location_code": 2840,
  "language_code": "en",
  "order_by": ["keyword_data.keyword_info.search_volume,desc"],
  "limit": 100
}
```

**Cost:** ~$0.01–0.02 per call (varies by result count).

**What to extract:**
- Total ranked keywords count
- Estimated monthly visits + traffic value
- Top 20 keywords by volume → which URLs rank for them
- **Critical question:** Are the NEW programmatic URLs ranking, or OLD URLs that redirect?
  (Canonical run: only old URLs ranked; new 1,018 pages were mid-indexation-transition)

### 2. Historical Rank Overview (the trend)

**Endpoint:** `dataforseo_labs/google/historical_rank_overview/live`

**Purpose:** 6–12 months of keyword count + estimated traffic + position band distribution.
Shows whether the site is growing, stalling, or declining.

```json
{
  "target": "<domain>",
  "location_code": 2840,
  "language_code": "en"
}
```

**Cost:** ~$0.01 per call.

**What to extract:**
- Monthly keyword count trend (is breadth rising?)
- Monthly estimated traffic value trend
- Position band distribution (top-3, 4-10, 11-20, 21-100)
- **Critical question:** Is breadth (keyword count) rising while top-3 count is flat?
  That means pages rank but on page 2 — revenue needs position, not just pages.
  (Canonical run: kw 246→395 but top-3 flat at 2 = breadth≠position≠money)

## Pass 3 — PageSpeed (optional, if CWV needed)

### 3. PageSpeed (Lighthouse)

**Endpoint:** `on_page/page_screenshot` or direct Lighthouse API

**Purpose:** Core Web Vitals (LCP, CLS, INP) for the target site vs client.

**Cost:** ~$0.01 per URL. Usually run on 3-5 representative URLs.

**When to use:** If CWV comparison is part of the teardown scope (often deferred to Phase 0).

## Pass 6 — Blog ranking check

### 4. Ranked Keywords filtered to blog URLs

Same endpoint as #1 but filtered:

```json
{
  "target": "<domain>",
  "filters": ["ranked_serp_element.serp_item.relative_url", "like", "%/blog/%"],
  "limit": 50
}
```

**Purpose:** Which blog posts actually rank, for what keywords, at what position.
(Canonical run: blog content was excellent but ranked page-2 — model-worthy content,
position-cautionary lesson.)

## Cost summary

| Call | Typical cost | When |
|---|---|---|
| Ranked keywords | $0.01–0.02 | Pass 3 (always) |
| Historical rank overview | $0.01 | Pass 3 (always) |
| PageSpeed / CWV | $0.03–0.05 | Pass 3 (optional) |
| Blog-filtered keywords | $0.01–0.02 | Pass 6 (if blog exists) |
| **Total typical teardown** | **$0.03–0.10** | — |

## Fallbacks when DataForSEO unavailable

If Labs subscription is not active or balance is insufficient:
- **BrightLocal scan** — if operator has a recent one, use the keyword/ranking data from it
- **Ahrefs export** — if operator has access, export top organic keywords
- **Manual SERP check** — web-search the top 5-10 target keywords and note positions
- **Note the gap** — always document "DataForSEO not available; ranking data is [source] or absent"

Never fake ranking data. State the source and its limitations.
