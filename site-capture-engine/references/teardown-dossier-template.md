# Teardown dossier template

Copy this structure when starting a new teardown. Section numbers match the canonical worked
example (AJ Long, 29 sections). Not all sections apply to every site — mark inapplicable
sections "N/A — [reason]" rather than omitting them (absence is a finding).

---

```markdown
# [Site Name] — Full Build Teardown & Analysis

**Date:** YYYY-MM-DD
**Target:** [domain]
**Client context:** [who we're building for, their geography + service set]
**Analyst:** [Claude Code / Cowork / operator]
**DataForSEO spend:** $X.XX

---

## 1. The page count, verified

[True page count from sitemap. Per-type breakdown. Framework artifact sitemaps excluded.]

## 2. The page-tier taxonomy (the quality ladder)

[Tiers identified, URL patterns, counts per tier. Note if service×city matrix is absent.]

## 3. The engine: the service × city matrix

[Matrix dimensions, gap grid, saturation. Or: "Matrix absent — flat service + city pages."]

## 4. Per-template anatomy

### 4a. [Tier name] — [template description]
[Section order, FAQ Q&As verbatim, pricing, data points fused, word/heading counts, internal links.]

### 4b. [Next tier]
[...]

(One subsection per tier with decoded representative page.)

## 5. The data-fusion layer — what they researched per entity

[Per-city/entity facts fused: neighborhoods, housing era, permit authority + portal, utility,
code/regulation specifics, brand/condition prevalence, year-stamped pricing, ZIPs, population,
cross-sells. Note demographic-aware variation.]

## 6. Language & voice

[Craft ladder: premium vs templated. Trust devices. Voice characteristics.]

## 7. SEO & schema architecture

[JSON-LD graph summary: types present, FAQPage, BreadcrumbList, SpeakableSpecification, etc.
Plugin-generated (Rank Math/Yoast) vs custom. Gaps.]

## 8. Internal linking — how it connects

[Linking topology: hub→leaf, breadcrumbs, cross-sell, blog→service funneling, footer/nav.
Template-driven vs hand-curated. Max click-depth. Orphan risk.]

## 9. Tech stack

[Framework, hosting/CDN, CSS framework, fonts, image pipeline. Summary table.]

## 10. The reverse-engineered machine (synthesis)

[How all the pieces compound: structure + data + schema + conversion + authority as a system.
What's the competitive advantage? One-page synthesis.]

## 11. Quality tells & exploitable inconsistencies

[What's excellent. What's inconsistent/broken. Where can we beat them.]

## 12. What changed vs prior dossiers

[If a prior competitor brief or teardown exists, what's different. Or "First teardown."]

## 13. Sources & method

[Tools used, DataForSEO endpoints + cost, what was fetched vs inferred, limitations.]

---

## 14. Gap-fill addendum (Pass 2)

[robots.txt + AI-crawler posture. llms.txt. Image pipeline. Full slug inventories.
Service-category IA.]

## 15. Full tech & tools stack (Pass 3)

| Category | Tool | Evidence | Notes |
|---|---|---|---|
| Framework | [e.g., Next.js 15 App Router] | [e.g., self.__next_f, turbopack chunks] | |
| Hosting/CDN | [e.g., Netlify] | [e.g., x-nf-request-id header] | |
| CSS | [e.g., Tailwind v4] | [e.g., utility classes] | |
| Booking/CRM | [e.g., HousecallPro] | [e.g., iframe src] | |
| Analytics | [e.g., GTM + GA4] | [e.g., container ID] | |
| Voice/Chat AI | [e.g., ElevenLabs + GPT] | [e.g., script tag + Permissions-Policy] | |
| Review widget | [e.g., Custom / None] | | |
| SEO plugin | [e.g., Rank Math] | [e.g., meta generator] | |
| Fonts | [e.g., Inter, self-hosted] | [e.g., next/font woff2] | |
| Image pipeline | [e.g., Next.js Image, WebP/AVIF] | [e.g., /_next/image] | |

## 16. Service taxonomy

[Service categories from mega-menu/nav. The IA that organizes their offerings.]

## 17. DataForSEO reality-check — what ACTUALLY ranks

[Ranked keywords: total kw, est. visits/value, which URLs rank (new vs old?).
Historical: 6-12mo trend, breadth vs position. THE most important finding.]

## 17b. Local-pack presence (V2) — Pass 3

[In Google 3-pack for head keyword at client's city centroid? Position, GBP rating +
review count visible in pack, Google Guaranteed badge. Or "Not in 3-pack."
Free path: incognito search screenshot. DataForSEO: parse `local_pack` from existing SERP call.]

## 18. Additional patterns worth stealing

[Anything not captured in the main sections. Noteworthy design/content/UX choices.]

---

## 19. Conversion, UX & the path to money (Pass 4)

[Header CTAs, per-page conversion sidebar, symptom checklists, 24/7 booking, the full funnel
map: organic/local-pack → hyper-local page → qualify → trust stack → multi-path CTAs → booking.]

## 19b. Review velocity + reputation snapshot (M1) — Pass 4

| Metric | Value | Source |
|---|---|---|
| Google reviews | [count] | [DataForSEO / Maps] |
| Google rating | [x.x★] | |
| Est. reviews/month | [N or "pending"] | [BrightLocal / snapshot delta] |
| Yelp reviews | [count, x.x★] | |
| BBB | [accredited? rating?] | |
| Angi | [count, x.x★] | |
| Owner response rate | [x%] | |
| Review-gen tools | [Podium/Birdeye/NiceJob/None] | [footer scripts] |

[Why it matters: authority and review-volume are decoupled (MI-3 finding). Velocity
is the durable lever.]

## 20. Traffic history + the breadth-vs-position reality

[DataForSEO historical trend. State plainly: pages ≠ money without authority + conversion.]

## 21. Migration playbook

[Old URL → new URL redirect map. 301/308 equity preservation. Or "No migration detected."]

## 22. Old-page archaeology

[Wayback Machine recovery of proven-winner old pages. Or "Wayback offline — deferred."]

---

## 23. The visual / design layer (Pass 5)

[Design tokens from CSS: hex palette, custom properties, font stack, motion.
Visual composition from screenshots (if available). Or "Screenshots needed — gap named."]

## 24. Strategic intent — WHY they scaled

[Sitemap lastmod analysis: mass-generation event? When? Each invested attribute → lead-gen lever.
Why scale, why these attributes, how recent.]

## 25. Money mechanics

[Financing, sticky mobile CTA, click-to-call density, form friction, call tracking.
Are we copying BOTH ends (pages + conversion/authority)?]

---

## 26. Blog deep-analysis (Pass 6)

[≥6 posts sampled. Writing style/voice, structure, depth signals, topic taxonomy,
internal linking to service pages. Cross-ref DataForSEO: which posts rank.]

## 27. Indexing & publishing lesson

[If relevant: sitemap publishing vs priority-indexing distinction. Mass-publish + accelerate.]

---

## 28. Deferred items

[Genuinely deferred: CWV behind quota, Wayback offline, Backlinks unsubscribed, etc.
Each with a follow-up action.]

## Related

- [[blueprint-website-factory]] (or client-specific blueprint)
- [[competitor dossier links]]
- [[handoff links]]
```
