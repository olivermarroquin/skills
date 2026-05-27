# Citation-monitoring query shapes

The four query shapes this skill uses. Each one is a Perplexity Pro query you paste verbatim into the browser; the bracketed slots get filled from the head-query list and the run date.

The point of having shaped templates instead of one generic query: Perplexity gives a different shape of answer depending on how you frame the question. A pricing-anchored query surfaces editorial cost guides and contractor pages. A safety-anchored query surfaces government and product-recall sources. A brand-named query surfaces the brand's own pages plus third-party reviewers. The shapes let the skill match the framing to what the head query is really asking.

When in doubt, default to Shape 1 (general source list) — it's the most neutral.

---

## Shape 1 — General source list (default)

**Use when:** The head query is a generic commercial-intent phrase like `panel upgrade Fairfax VA` or `roof replacement cost`. No brand, no safety angle, no pricing emphasis.

**Template:**

```
For the search query "<head query>", which 5-10 sources are most
authoritatively cited as of <YYYY-MM-DD>? Return the source list in
order of authority, with one-line descriptions of each source. Note any
newly-emerging sources or any that appear to have dropped from earlier
citation patterns. Include the source URL exactly as it appears.
```

**Why this shape:** Perplexity reads "authoritatively cited" as a signal to surface its highest-confidence citations rather than a broad reading list. The "order of authority" phrasing keeps the ranking stable across re-runs.

**Worked example for ev-electric-services:**

```
For the search query "panel upgrade Fairfax VA", which 5-10 sources are
most authoritatively cited as of 2026-05-27? Return the source list in
order of authority, with one-line descriptions of each source. Note any
newly-emerging sources or any that appear to have dropped from earlier
citation patterns. Include the source URL exactly as it appears.
```

---

## Shape 2 — Cost-anchored query

**Use when:** The head query asks about price, cost, or budget. Examples: `electrical panel upgrade cost`, `how much does a roof replacement cost`, `kitchen remodel cost Vienna VA`.

**Template:**

```
For the question "<head query>", which 5-10 sources are most
authoritatively cited as of <YYYY-MM-DD> when someone is looking for
real cost information? Return the source list in order, with each
source's typical price range or cost-data approach in the one-line
description. Note newly-emerging cost-anchored sources or any that have
dropped from earlier citation patterns. Include the source URL exactly
as it appears.
```

**Why this shape:** Pricing queries pull a different citation set than generic commercial queries. Editorial cost guides (This Old House, HomeAdvisor, Angi cost guides), contractor pages with transparent pricing, and AI Overview-eligible "$X to $Y" pages dominate. Asking explicitly about "real cost information" filters out content-marketing pages that mention price without giving real numbers.

**Worked example for ev-electric-services:**

```
For the question "electrical panel upgrade cost", which 5-10 sources are
most authoritatively cited as of 2026-05-27 when someone is looking for
real cost information? Return the source list in order, with each
source's typical price range or cost-data approach in the one-line
description. Note newly-emerging cost-anchored sources or any that have
dropped from earlier citation patterns. Include the source URL exactly
as it appears.
```

---

## Shape 3 — Brand-named / safety-anchored query

**Use when:** The head query names a specific brand, product, or safety topic. Examples: `Federal Pacific panel replacement`, `Zinsco panel danger`, `Stab-Lok recall`, `aluminum wiring remediation`.

**Template:**

```
For the query "<head query>" — which involves a named brand, product,
or safety concern — which 5-10 sources are most authoritatively cited
as of <YYYY-MM-DD>? Prioritize sources that include real safety data,
recall information, or industry analysis over generic contractor pages.
Return the source list in order, with each source's expertise angle in
the one-line description. Note any newly-emerging safety-anchored
sources or any that have dropped from earlier citation patterns.
Include the source URL exactly as it appears.
```

**Why this shape:** Safety and brand-named queries pull from a different citation pool than generic commercial queries. Government recall databases (CPSC), industry analysts, insurance underwriters, and product-historical references show up here that wouldn't show up for "panel upgrade [city]." Filtering for "real safety data" or "industry analysis" keeps Perplexity from defaulting to contractor-blog summaries.

**Worked example for ev-electric-services:**

```
For the query "Federal Pacific panel replacement" — which involves a
named brand, product, or safety concern — which 5-10 sources are most
authoritatively cited as of 2026-05-27? Prioritize sources that include
real safety data, recall information, or industry analysis over generic
contractor pages. Return the source list in order, with each source's
expertise angle in the one-line description. Note any newly-emerging
safety-anchored sources or any that have dropped from earlier citation
patterns. Include the source URL exactly as it appears.
```

---

## Shape 4 — Local-intent / city-anchored query

**Use when:** The head query has a clear local-intent component (city, neighborhood, "near me," service area). Examples: `electrician Vienna VA`, `panel upgrade McLean`, `emergency electrician Falls Church`.

**Template:**

```
For the local-intent query "<head query>", which 5-10 sources are most
authoritatively cited as of <YYYY-MM-DD>? Distinguish between national
editorial sources (cost guides, how-to pages) and local-business pages
(specific contractors serving this area). Return the source list in
order, with each source's geographic relevance in the one-line
description. Note any newly-emerging local contractors or any that have
dropped from earlier citation patterns. Include the source URL exactly
as it appears.
```

**Why this shape:** Local-intent queries blend national editorial sources (which dominate generic queries) with local-business sources (which only show up when the city is named). Asking Perplexity to distinguish the two surfaces the competitive set directly — the local contractors getting cited are the local competitors worth tracking.

**Worked example for ev-electric-services:**

```
For the local-intent query "electrician Vienna VA", which 5-10 sources
are most authoritatively cited as of 2026-05-27? Distinguish between
national editorial sources (cost guides, how-to pages) and local-business
pages (specific contractors serving this area). Return the source list
in order, with each source's geographic relevance in the one-line
description. Note any newly-emerging local contractors or any that have
dropped from earlier citation patterns. Include the source URL exactly
as it appears.
```

---

## Picking the right shape

A simple decision tree:

1. **Does the query name a brand, product, recall, or safety topic?** → Shape 3 (brand-named / safety-anchored).
2. **Does the query include "cost," "price," "how much," "budget"?** → Shape 2 (cost-anchored).
3. **Does the query include a city name, neighborhood, or "near me"?** → Shape 4 (local-intent / city-anchored).
4. **Otherwise** → Shape 1 (general source list, default).

If a head query fits more than one shape (e.g., "panel upgrade cost Vienna VA" is both cost-anchored AND local-intent), default to Shape 2 (cost-anchored) — pricing is the stronger framing signal and pulls the more decision-relevant citations.

---

## Cross-shape rules

These apply to every shape:

- **Always include the date stamp** (`as of YYYY-MM-DD`). Perplexity Pro's reasoning treats date context as a hint to surface recent sources over older ones. Without the date, the citation set can drift toward older editorial pages.
- **Always ask for "5-10 sources"** — not "the top sources" or "a list of sources." The numeric range gives Perplexity room to surface a real ordered list rather than 2-3 dominant URLs.
- **Always ask for the URL "exactly as it appears."** Perplexity sometimes shortens URLs for readability; the diff math depends on URL equality across runs, so the exact form matters.
- **Always ask Perplexity to flag newly-emerging and dropped sources.** Perplexity sometimes annotates these directly in the answer; capturing those flags adds signal even before the skill's own diff math runs.

---

## What good answers look like

A good Perplexity answer to one of these queries includes:

- A numbered list of 5-10 sources, each with a URL and a one-line description.
- The URLs are full and clickable (not truncated `example.com/...` forms).
- The one-line descriptions distinguish sources from each other (not all "an article about panel upgrades").
- Any newly-emerging or dropped annotations are inline.

A bad answer looks like:

- A prose paragraph summarizing "the most cited sources are typically X and Y" without a numbered list.
- URLs truncated to root domains (`thisoldhouse.com` instead of the actual article URL).
- Generic descriptions ("a contractor website") that don't differentiate.

If the answer is bad, re-run the query once with a slight rephrasing (add "Return the source list as a numbered list" if it's missing) before logging it as captured. Don't paste a degraded answer into the citation-history note — it pollutes future diffs.

---

## When to add a new shape

Add a new shape when:

- A head query pattern recurs across 3+ scopes and doesn't fit shapes 1-4 well.
- An existing shape consistently returns a degraded answer for a query class (the prose-summary failure mode above).
- A new Perplexity feature ships that changes how source lists render (a new dimension worth asking about).

When adding a new shape, follow the same structure: name, "Use when," template, "Why this shape," worked example. Add it to the decision tree at the top. Bump the file's `updated:` date if frontmatter is present (this file currently has none — the parent SKILL.md owns the canonical metadata).

---

## See also

- [[SKILL]] — the citation-monitoring skill that consumes these shapes
- [[perplexity-browser-setup]] — pre-query browser checks
- [[perplexity-cost-rules]] — per-invocation caps
- [[perplexity-query-templates-index]] — index of every suite skill's query templates (citation-monitoring's section gets updated when this file lands)
- [[query-templates]] — the perplexity-refinement skill's six template shapes (different purpose; useful contrast)
