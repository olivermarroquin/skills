# SEO Site Teardown — per-pass checklist

Copy the relevant items into the run's task list. Tick each; record "absent" explicitly when a tell isn't
present (absence is a finding too). Bash = sandbox curl; decode with `scripts/extract_nextjs.py`.

## Setup
- [ ] Folder skeleton (`raw/{sitemaps,payloads,entities,extra}`, `extracted/`, `data/`) + `_README.md`.
- [ ] Copy `extract_nextjs.py` into the folder as `extract.py`.
- [ ] Probe DataForSEO wrapper; record which subscriptions are live (Labs? Backlinks?).

## Pass 1 — Forensic structure
- [ ] Fetch `sitemap.xml`; if index, fetch every nested sitemap; count `<loc>` per file. Record TRUE page count.
- [ ] Classify URLs into tiers (core, service hubs, service×city, city, neighborhood, problem, guide, blog) + counts.
- [ ] Decode ≥1 page per tier (full HTML → `extract.py`): section order, FAQ Q&As verbatim, pricing, headings.
- [ ] List the per-entity data points fused into matrix pages (permit authority/portal, utility, code dates,
      neighborhoods, housing era, brand/condition prevalence, year-stamped price, ZIPs, population, cross-sells).
- [ ] Note the craft ladder (premium vs templated) + voice + trust devices.
- [ ] Map internal-linking architecture: hub→leaf, breadcrumbs, cross-sell sidebar, blog→service funneling,
      footer/nav surfaces. Template-driven or hand-curated? Max click-depth from homepage? Orphan risk?
- [ ] **GATE 1:** report structure + count + headline; confirm real-vs-artifact if signal-triggered.

## Pass 2 — Gap-fill
- [ ] `robots.txt` — AI-crawler allow-list? (GPTBot/OAI-SearchBot/PerplexityBot/ClaudeBot/Google-Extended/
      Applebot-Extended/CCBot/Bytespider). Save it.
- [ ] `llms.txt` — present? Save it; note sections.
- [ ] Image pipeline — `/_next/image`, `.webp`/`.avif`, `srcset`? (modern-format gap open/closed)
- [ ] Matrix gap grid — which (service × city) cells built vs not; saturation + frontier.
- [ ] Fetch + decode ALL city/location pages → `<entities>-research-seed.md` (entity → data fields).
      Watch for demographic-aware variation.
- [ ] Save full slug inventories (blog, neighborhoods, problems, guides) + the service-category IA.

## Pass 3 — Tech/tools + what ranks
- [ ] Response headers: hosting/CDN, framework (`x-nextjs-*`), ISR (`x-nextjs-stale-time`), security,
      `Permissions-Policy` (microphone=self ⇒ voice agent).
- [ ] Framework/build: `self.__next_f`, `turbopack`, Tailwind classes, `next/font`, `/_next/image`.
- [ ] Third-party tools — grep payloads for external domains + `<script src>`. Name each:
  - [ ] Booking/CRM (HousecallPro / ServiceTitan / Jobber / Calendly)
  - [ ] Analytics (GTM / GA4)
  - [ ] Voice/chat AI (ElevenLabs / Vapi / Retell / OpenAI-GPT)
  - [ ] Review widget (Birdeye / Podium / NiceJob — or custom)
  - [ ] Fonts / CDN / auth / forms
- [ ] Trust/cert mining (`/about/credentials`): license #s + verify path, insurance, manufacturer certs.
- [ ] DataForSEO `ranked_keywords` (order_by etv desc): total kw, est. visits/value, **which URLs rank
      (new vs old?)**.
- [ ] DataForSEO `historical_rank_overview`: 6–12mo kw count + etv + position bands. **Breadth vs top-3.**
- [ ] Note non-active subscriptions; fall back to BrightLocal/Ahrefs baseline.
- [ ] **GATE 2:** report the ranked-keywords reframing before Pass 4.

## Pass 4 — Conversion/UX + history + archaeology
- [ ] Conversion/CTA system: header CTAs (call + Book Online); per-page sidebar (Need-Help-Now /
      Request-Quote / response-time / Service-Area-Info w/ county+population+ZIPs / Other-Services);
      symptom checklists ("Signs You Need…"); 24/7 voice booking. Map the funnel.
- [ ] Migration: do old URLs 301/308-redirect to new? Enumerate the old→new map (the client migration playbook).
- [ ] Old-page archaeology: recover proven-winner old URLs via Wayback CDX + snapshots; if archive.org down, defer.
- [ ] Conversion + authority gap: reconcile breadth-vs-position; state "pages ≠ money without reviews/GBP/
      links/conversion".

## Pass 5 — Design, intent & money mechanics
- [ ] Fetch `/_next/static/chunks/*.css`; extract hex palette + CSS custom props + fonts → `data/design-tokens.md`.
- [ ] Screenshots per tier (operator or Claude-in-Chrome), desktop+mobile, above-fold+full → `raw/screenshots/`;
      write a visual-composition section (hero, hierarchy, CTA design/placement, imagery, mobile sticky CTA, motion).
- [ ] Sitemap `<lastmod>`: single-day mass-generation event vs organic? When? (window size)
- [ ] Map each invested attribute → its lead-gen lever (why scale, why these attributes).
- [ ] Money mechanics: financing (Synchrony/Wisetack/Hearth/GreenSky/Sunbit/Affirm), sticky mobile CTA,
      click-to-call density, form friction (count forms+fields), call-tracking.
- [ ] State plainly: are we copying BOTH ends (pages + conversion/authority), not just pages?

## Pass 6 — Blog deep-analysis (for the reusable blog engine)
- [ ] Sample ≥6 posts across topic types (comparison/decision, symptom/emergency, code-explainer,
      seasonal, buyer-stage, positioning). Decode each.
- [ ] Writing style/voice — authoritative + calm + specific? Non-alarmist? Quote real examples.
- [ ] Structure — intro → why it matters → context → identify → code → options+prices → local angle →
      action steps → soft CTA → authoritative sources → FAQ schema.
- [ ] Depth signals — code citations (NEC §), real price ranges, authority links (CPSC/NFPA/ESFI),
      local specificity, word count.
- [ ] Topic engineering — geo-tagged? Seasonal? County-data? Decision-stage? Map the topic taxonomy.
- [ ] Internal linking — does the post funnel informational traffic to service/city pages?
- [ ] Cross-reference DataForSEO: which posts rank, for what, at what position.
- [ ] Output: blog-analysis section + reusable "what good blog content looks like" spec.

## Closing
- [ ] "Reverse-engineered machine" synthesis section written — how structure + data + schema + conversion +
      authority compound into the site's competitive advantage (canonical: §10, ~1 page).
- [ ] Teardown dossier complete (all sections incl. tech table, DataForSEO reality-check, conversion system).
- [ ] Reproduction blueprint (data model + conversion/authority layer + migration + phased program).
- [ ] Non-destructive updates to any prior dossier/synthesis.
- [ ] Folder `_README.md` + parent updated.
- [ ] Auto-invoke `output-quality-loop` on teardown + blueprint; event-log row; git staged by name (no push).
- [ ] Itemize genuinely-deferred items (CWV behind quota, Wayback offline, Backlinks unsubscribed) into a
      Phase-0 follow-up handoff.
