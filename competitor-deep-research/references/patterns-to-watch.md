# Patterns to watch

Heuristics and fingerprints for the audit phase. Use this as a quick reference when something in the fetched content is ambiguous.

---

## Tech stack fingerprints

### WordPress

- URL contains `/wp-content/`, `/wp-includes/`, `/wp-admin/`, or `/?p=ID`
- HTTP header `x-powered-by: PHP`
- Frequent `?ver=X.Y.Z` query parameters on CSS/JS assets
- Common plugins fingerprintable from source:
  - **Elementor** — `class="elementor-..."`, `elementor-frontend` JS
  - **Divi** — `et_pb_...` class names
  - **Beaver Builder** — `fl-builder-...`
  - **Yoast SEO** — `<!-- This site is optimized with the Yoast SEO plugin -->` in HTML head
  - **All in One SEO (AIOSEO)** — `<!-- All in One SEO ... -->` comment
  - **Rank Math** — `<!-- Powered by Rank Math SEO -->` comment
  - **WP Rocket** — `<!-- Cached by WP Rocket -->` comment
  - **LiteSpeed Cache** — `x-litespeed-cache: hit` header
  - **NitroPack** — `<meta name="generator" content="NitroPack">`

### Static site generators (JAMstack)

- URLs end in `.html` in the sitemap
- HTTP header `server: Netlify` or `server: Vercel` or `server: cloudflare`
- `x-nf-request-id:` header confirms Netlify
- `x-vercel-id:` header confirms Vercel
- `cache-status: "Netlify Edge"` or similar CDN-edge cache markers
- No `/wp-content/` or `/wp-includes/` in any URL
- Often very fast LCP scores
- Common generators: Hugo, Eleventy, Astro, Next.js (export mode), Gatsby, Jekyll. Not always fingerprintable to a specific generator without deeper inspection — that's OK; "static site generator on Netlify" is enough for the brief.

### Enterprise CMS (Mr. Electric pattern)

- Single corporate domain with path-routing per franchise/location (`/fairfax`, `/houston`)
- Asset paths under structured locale folders (`/us/en-us/_assets/...`)
- Centralized booking forms with sophisticated lead routing
- Often .NET, Java, or Sitecore-class CMS

### Shopify, Squarespace, Wix

- Shopify: `myshopify.com` references or `cdn.shopify.com` asset paths
- Squarespace: `static1.squarespace.com` asset paths
- Wix: `parastorage.com` asset paths, `wix-bolt` references

### Hostinger (the client's host)

- HTTP header `platform: hostinger`
- HTTP header `panel: hpanel`
- Nameservers like `horizon.dns-parking.com` + `orbit.dns-parking.com`
- Often paired with LiteSpeed web server

---

## Content depth heuristics

When auditing a service or location page, look for:

| Signal | Strong | Weak |
|---|---|---|
| Word count | 2,000+ for primary pages | <800 generic-template |
| Neighborhood mentions | Named, specific, locally accurate | Just city name swapped in |
| Permit references | Specific office names, code citations (NEC, AFCI, GFCI) | Generic "permits required" boilerplate |
| Case studies | 3+ named scenarios with city + outcome | None or one generic blurb |
| FAQs | 5–8 inline, neighborhood-aware questions | None inline; only on /faq page |
| Pricing transparency | Specific dollar ranges published | "Call for quote" only |
| Internal links | 20+ contextual links woven into prose | Only nav/footer links |
| Service × city sub-pages | `/services/X/<city>` matrix built out | Single service page, no city variants |
| Original imagery | Real job-site photos or branded illustrations | Stock photos or theme defaults |
| FAQs in schema | FAQPage JSON-LD present | Q&A in HTML but no schema |

---

## Common winning patterns (across home-services niches)

Things that correlate with ranking outcomes in home-services audits:

1. **Many indexed pages with genuine local specificity.** Not 200 thin pages, but 50–300 pages where each one names neighborhoods, permits, code references, and recent project examples.
2. **Real Google review base in the hundreds.** Below 100 reviews, the local-pack winners don't include you. 500+ is industry-leading.
3. **Founder or family narrative on the home page.** "Father and son since 1996" or "third-generation electrician" outperforms faceless corporate copy.
4. **5-year (or longer) workmanship warranty.** Most competitors offer 1-year; the longer warranty is differentiated and concrete.
5. **Transparent pricing published on-page.** Specific ranges ("$2,400–$3,500 for a panel upgrade") signal Helpful Content + capture comparison-shopping searches.
6. **Embedded FAQs with FAQPage schema.** Captures AI Overviews and ChatGPT/Perplexity citations.
7. **Three-jurisdiction licensing displayed in footer.** Multi-state licenses build trust and let one site serve a regional market.
8. **JAMstack or modern WordPress with disciplined plugin stack + premium host.** Speed matters; bloated WordPress is a structural disadvantage.

---

## Common losing patterns (across home-services niches)

Things that correlate with poor ranking outcomes:

1. **Generic template content with city name swapped in.** Google's Helpful Content Update penalizes this; users bounce.
2. **Stale promotions still displayed.** Expired coupon codes signal the site isn't actively managed.
3. **Lorton/Sterling/peripheral physical address marketed as "of [Central City]."** Geographic triangulation can't be faked; Google figures out where you actually are.
4. **Heavy commercial split when targeting residential customers.** Mixed messaging dilutes relevance.
5. **No founder face, no real customer photos, only stock imagery.** Trust signal damage.
6. **No FAQ section on service pages.** Missing AI Overview opportunity.
7. **No transparent pricing.** Lost to competitors who publish.
8. **Old-school meta-keywords tags + no JSON-LD schema.** Indicates the SEO setup hasn't been updated since ~2015.
9. **Franchise-network link-juice misinterpreted as local authority.** High domain-authority score from corporate footers doesn't translate to local-pack rankings.
10. **24/7 emergency leading the marketing for a non-emergency business.** Misaligned with target customer; attracts the wrong calls.

---

## Where to escalate

Some signals are confirmable only with browser-rendered tooling, not WebFetch:

- **JavaScript-injected JSON-LD schema** — confirm with Google Rich Results Test or browser DOM inspection
- **Client-rendered SPAs returning empty content from WebFetch** — escalate to Claude in Chrome (`navigate` + `get_page_text`)
- **Mobile-specific rendering issues** — needs mobile viewport in browser tools
- **Visual design quality, image polish, layout coherence** — needs a screenshot (Claude in Chrome can capture)

When escalation tools aren't available in the current session, flag the gap in the synthesis's "blocked questions" section and move on.

---

## Where to find prior data

Look for these in the client's vault folder before starting the live audit:

- `admin-extracts/google-business-profile/audit-brightlocal-baseline-*.pdf` — competitor rankings + review/link counts
- `admin-extracts/google-business-profile/audit-gbp-baseline-*.md` — client's GBP baseline
- `admin-extracts/search-console/*` — client's keyword performance
- `admin-extracts/wordpress/audit-wp-plugins-baseline-*.md` — client's tech stack
- `README.md` — client's confirmed identity, service area, services, and strategic context

The client's own README is often the most important input — it contains the operator-confirmed service area, avoid list, priority services, and pricing structure. Read it first.
