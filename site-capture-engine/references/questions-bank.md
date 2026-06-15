# Teardown questions bank — "why did they do that?"

A living set of questions to ask of every site, every page, and every *change* — to reverse the
**psychology and strategy** behind the build, not just catalog it. Run the relevant block during each pass
and on every before/after diff. Add new good questions as they come up (operator + analyst). The goal is
always: **what decision did they make, why, and what outcome were they betting on — and should we copy it?**

## Ask of the whole site (each teardown)
- What is this site *for*, commercially? Which page types are the money pages vs. top-of-funnel?
- What did they invest the most effort in (page count, schema, voice agent, GBPs, financing)? Effort
  reveals priorities. Why those?
- What's the single biggest bet, and how recent is it? (sitemap `lastmod`, rebuild date) How far into it
  are they — is the payoff in or pending? (DataForSEO history)
- What's the gap between what they *built* and what actually *ranks/converts*? (pages vs top-3 positions)
- If they're winning, is it the pages, the local pack/GBPs, the reviews, the links, or the conversion
  layer? Which lever is doing the work?

## Ask of each PAGE captured
- What search intent + funnel stage is this page for? What's the ONE action it wants?
- What data points are fused in (and where did they research them)? Could we get the same data at scale?
- What trust signals are present, and where (above the fold)? What objection does each pre-empt?
- What's the CTA hierarchy? How many capture paths, sized to what readiness?
- What's templated vs. hand-crafted here? Why did they spend craft here and not elsewhere?
- What would make THIS page convert better than theirs? (our edge)

## Ask of the DATA (rankings/traffic/history)
- Which pages/URLs actually earn the traffic? Are they the new pages or the old (redirected) ones?
- Is keyword *breadth* rising while *position* stalls? What does that say about authority vs content?
- What proven-winner content types should we prioritize first in our build?
- What's the trend direction + inflection points? What changed in the month the trend moved?

## Ask on every CHANGE (before/after diff — HeyTony-triggered)
- WHAT changed: pages added/removed, schema, tech, CTAs, pricing, nav, design?
- WHY now? What signal (season, competitor, algorithm update, business goal) likely triggered it?
- What outcome are they betting this change produces? (more breadth? better CTR? faster booking?)
- Is this a test or a commitment? (partial rollout vs. site-wide)
- Does the change reveal a weakness they found in their own funnel — and is it one we share?
- Should we match, beat, or ignore it? What's the cost/benefit for our clients?

## Strategy/psychology probes (the "why" behind scaling)
- Why scale to ~1,000 pages *now*? What does the page count buy that they didn't have?
- Why those specific cities/services/neighborhoods? What does the matrix shape reveal about their market read?
- Why mass-publish all at once vs. drip? (indexing strategy — see SKILL "indexing/publishing" lesson)
- Why build a voice agent / financing / multi-GBP? Each maps to a booking lever — which bottleneck were
  they solving?
- What are they NOT doing that they easily could? (the gap = our opportunity)
- If we were their competitor with a fresh Next.js build, where would we attack? (the window)

## Examples generated during the AJ Long run (seed entries)
- "They published 630 pages in one day (2026-05-09) but they're not ranking yet — so why publish all at
  once instead of dripping? → sitemap publishing has no limit; the ~200/day cap is on *manual/API indexing
  requests*; they dumped via sitemap + let Google crawl. Lesson: mass-publish, then accelerate the money
  pages via the Indexing API/IndexNow."
- "Breadth climbing (246→395 kw) but top-3 flat at 2 → pages get found but don't win position; revenue
  needs the authority+conversion layer, not more pages."
- "They closed every schema gap + added llms.txt + allow-listed AI crawlers → they're betting on the
  answer-engine era (ChatGPT/Perplexity/AI Overviews), not just blue links. Should we lead there?"
- "Their blog is genuinely excellent (code-cited, priced, local) but ranks page-2 → great content ≠
  position without authority. What would get our equally-good content to top-3?"
