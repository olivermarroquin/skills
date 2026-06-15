# SEO Site Teardown — tells catalog

Expanded reference of concrete things to look for on every teardown. Each tell is a binary
(present/absent) — **absence is a finding too.** Organized by pass.

## Pass 1 — Forensic structure

| Tell | What to look for | Where | Why it matters |
|---|---|---|---|
| Next.js RSC | `self.__next_f.push` in page source | HTML source | Full content recoverable without a browser; RSC = App Router (Next 13+) |
| Next.js Pages Router | `<script id="__NEXT_DATA__">` | HTML source | Older Next.js; page props contain all content as JSON |
| WordPress | `wp-content/`, `wp-includes/`, `wp-json/` in source | HTML source / headers | Most common CMS; content in HTML body, not JSON payloads |
| Sitemap index | Multiple nested sitemaps vs single sitemap.xml | `/sitemap.xml` | Split sitemaps = deliberate organization by page type; count each |
| Framework artifact sitemaps | `tcb_symbol-sitemap` (Thrive), `elementor_library-sitemap`, `wp_template-sitemap` | Sitemap index | Exclude from true page count — these are template fragments |
| Service×city matrix | URL pattern `/services/<svc>/<city>` or similar | Sitemap URLs | The page-count engine; compute the gap grid. Absent = flat structure |
| Per-entity data layer | Permit authority, utility, code dates, neighborhoods, housing era, pricing, ZIPs, population fused into templates | Decoded page content | Expensive to research; cheap to template. THIS is the moat |
| Craft ladder | Premium money pages (~2,000+ words, hand-crafted) vs light long-tail (~500-800, slot-filled) | Word count comparison across tiers | Voice/depth difference reveals where they invest effort |
| Internal-linking architecture | Hub→leaf, breadcrumbs, cross-sell sidebar, blog→service funneling | Decoded page links | Template-driven = automatic scaling; hand-curated = labor cost |

## Pass 2 — Gap-fill

| Tell | What to look for | Where | Why it matters |
|---|---|---|---|
| AI-crawler allow-list | GPTBot, OAI-SearchBot, PerplexityBot, ClaudeBot, Google-Extended, Applebot-Extended, CCBot, Bytespider explicitly allowed | `robots.txt` | Deliberate answer-engine play; cheapest highest-leverage thing to copy |
| `llms.txt` | Site index for LLMs | `/llms.txt` | Answer-engine optimization; may be hand-written or plugin-generated (Rank Math) |
| Modern image pipeline | `/_next/image`, `.webp`/`.avif` serving, `srcset` responsive | Page source / response headers | Modern-format gap open or closed |
| Matrix gap grid | Which service×city cells built vs not | Computed from sitemap URLs | Saturation tells their frontier; unclaimed cells = our opportunity |
| Demographic-aware variation | "Common issues" line shifting by city wealth/age | Cross-city page comparison | Signal of genuine per-entity research, not just city-name substitution |

## Pass 3 — Tech/tools fingerprint

| Tell | What to look for | Where | Why it matters |
|---|---|---|---|
| Hosting/CDN | `server:` header, `x-nf-request-id` (Netlify), `via`/`x-vercel` (Vercel) | Response headers (`curl -I`) | Stack reproducibility |
| ISR/caching | `x-nextjs-stale-time`, `cache-control` | Response headers | Build/render strategy |
| Turbopack | `turbopack-*` chunk names | Page source | Next.js 15+ signal |
| Tailwind | Utility classes (`flex`, `px-4`, `text-lg`) | HTML class attributes | CSS framework identification |
| Self-hosted fonts | `next/font` woff2, `font-display: swap` | CSS / link tags | Performance + brand control |
| Booking/CRM | HousecallPro (`online-booking.housecallpro.com`), ServiceTitan, Jobber, Calendly | Script tags / iframes | Revenue infrastructure |
| Analytics | GTM container ID, GA4 measurement ID | Script tags | Tracking sophistication |
| Voice/chat AI | ElevenLabs, Vapi, Retell, OpenAI/GPT widget | Script tags / `Permissions-Policy: microphone=self` | 24/7 booking capability |
| Review widgets | Birdeye, Podium, NiceJob — or custom/none | Script tags / embeds | Trust layer strategy |
| SEO plugin | Rank Math, Yoast, AIOSEO, custom | HTML meta / schema patterns | Schema generation approach |
| Comprehensive JSON-LD | `FAQPage`, `Offer`/`PriceSpecification`, `AggregateRating`, `BreadcrumbList`, `HowTo`, `SpeakableSpecification` | JSON-LD blocks | Schema completeness; `SpeakableSpecification` = voice/AI-answer bet |

## Pass 4 — Conversion/UX

| Tell | What to look for | Where | Why it matters |
|---|---|---|---|
| Persistent header CTAs | Click-to-call + "Book Online" in sticky header | Page header | Multi-path capture |
| Conversion sidebar | Need-Help-Now, Request-Quote, response-time reassurance, Service-Area-Info card, Other-Services cross-sell | Page sidebar | Per-page conversion system |
| Symptom checklists | "Signs You Need…" sections | Page body | Qualify the visitor; trigger urgency |
| 24/7 voice booking | AI voice agent that books real jobs after hours | Script tags / widget | After-hours revenue capture |
| Redirect preservation | Old URLs 301/308-redirect to new | `curl -I` on old URLs | Migration equity preservation |

## Pass 5 — Design, intent & money mechanics

| Tell | What to look for | Where | Why it matters |
|---|---|---|---|
| Single-day mass-generation | Hundreds of pages with same `<lastmod>` date | Sitemap | Programmatic scaling event; reveals the machine |
| Design tokens | Hex palette, CSS custom properties, font families | CSS chunks | Re-themeable per client |
| Financing | Synchrony, Wisetack, Hearth, GreenSky, Sunbit, Affirm | Page body / script tags | Close-rate lever |
| Sticky mobile CTA | Fixed-bottom call/book bar on mobile | Page source (mobile viewport) | Mobile conversion |
| Click-to-call density | `tel:` link count per page | Page source | Conversion path count |
| Form friction | Number of `<form>` elements × field count | Page source | Minimal = good (route to booking, not forms) |
| Call tracking | CallRail, CallTrackingMetrics | Script tags | Lead attribution |

## Pass 6 — Blog

| Tell | What to look for | Where | Why it matters |
|---|---|---|---|
| Code citations | NEC §, local code references | Blog post body | Depth + authority signal |
| Real price ranges | Year-stamped pricing with ranges | Blog post body | Trust + conversion signal |
| Authority links | CPSC, NFPA, ESFI, manufacturer sites | Blog post links | E-E-A-T signal |
| Local specificity | County names, permit authorities, utility companies | Blog post body | Hyper-local content signal |
| Blog→service funneling | Internal links from blog posts to service/city pages | Blog post links | Informational→commercial funnel |
| Topic taxonomy | Geo-tagged, seasonal, county-data, decision-stage categories | Blog post topics | Content strategy signal |
