---
type: skill-reference
skill: market-intelligence-engine
created: 2026-06-16
updated: 2026-06-16
tags: [skill-reference, market-intelligence, ad-intelligence, paid-arena, V4, transparency-center]
---

# Ad-intelligence module — V4 paid arena deep pass

Distilled from the [MI-3c] ad-creative scrape (2026-06-16). This module is the paid-arena (V4)
deep-pass sub-procedure of `market-intelligence-engine`. It produces a themed ad-creative swipe file
from the Google Ads Transparency Center (+ optional Meta Ad Library), then synthesizes winning
patterns and per-client ad-angle recommendations.

**Mandatory substrate:** Claude-in-Chrome. The Transparency Center is JS-rendered AND ad previews
are server-rendered images (copy is not in the DOM text layer). WebFetch returns empty. **Step 0:
confirm Chrome is connected, else STOP.** Do not silently skip.

---

## Workflow (per advertiser)

Given a list of competitor domains from the run config:

1. **Navigate** to `https://adstransparency.google.com/?region=US&domain=<domain>`.
2. **Read live count** from header via JS:
   ```javascript
   [...document.querySelectorAll('*')].map(e => e.childElementCount === 0 ? e.textContent : '').find(x => /\d+ ads/.test(x))
   ```
3. **Expand grid:** click "See all ads" -> verify via `document.querySelectorAll('a[href*="/creative/"]').length`.
4. **De-virtualize for counting:** set `document.body.style.zoom='0.4'`, wait, re-count.
   Header label often differs from grid count (Root: "47" header vs 80 grid items — 80 was a
   single non-reproduced reading; true verified count = 40 per-creative URLs).
5. **Capture screenshots:** zoom 0.55-0.6, scroll in ~750px steps, `screenshot{save_to_disk:true}`.
6. **Transcribe distinct creatives** from screenshots into swipe file, grouped by theme.
7. **Sample detail pages** for `Last shown` + `Format` + variation count: navigate to
   `/advertiser/<AID>/creative/<CRID>?region=US`.
8. **Write manifest JSON** per advertiser:
   ```json
   {
     "competitor": "",
     "domain": "",
     "advertiser_account": "",
     "advertiser_id": "",
     "header_count": 0,
     "grid_creative_count": 0,
     "verified": false,
     "captured_date": "YYYY-MM-DD",
     "formats_seen": [],
     "distinct_transcribed_count": 0,
     "notes": ""
   }
   ```

---

## Output A — Themed swipe file

One section per advertiser, creatives grouped by theme (examples from electrician field):
- EV-charger / panel-breaker / offer / trust-heritage / emergency-same-day / geo-targeted /
  service-specific / LSA.

Each section includes:
- Per-creative: headline, description, sitelinks, callouts, format, last-shown date (if sampled).
- One-paragraph "advertiser read" (what their ad strategy signals).
- Cross-competitor synthesis (recurring patterns across all advertisers).
- Completion ledger: "X distinct of Y grid creatives" per advertiser.

## Output B — Synthesis + per-client recommendations

- Winning patterns: hooks/offers/formats/geo that recur across advertisers.
- Per-client ad-angle recommendations: which angles to run first, sequenced, routed to ads execution.

---

## Known limitations (design around these)

1. **Screenshots save to host, not sandbox** — manifest + transcription are the durable artifact.
   PNGs are not vault-reachable from Cowork.
2. **Ad copy is image-rendered** — must be read from screenshots (vision), not scraped from DOM.
3. **Grid virtualization** — counts fluctuate; confirm via zoom-out + live DOM count.
4. **Header count != grid creative count** — record both; true count = verified per-creative URLs.
5. **Counts drift daily** — timestamp every capture.
6. **Meta Ad Library** — check for all advertisers; Meta paid = 0 is common in local services
   (confirmed for electrician field: Root/PRO/Kolb run 0 paid Meta ads).

---

## Gate rules (G-market-intel enforced)

- **Completion-vs-plan:** state "X distinct of Y grid creatives" per advertiser; never imply
  exhaustive when sampled.
- **No undefended zeros:** re-confirm every 0-ad target live in Transparency Center; enumerate sources.
- **No self-gate:** independent reviewer runs before close.
- **Loud limitations:** screenshots-on-host, image-rendered copy, count drift, virtualization,
  reference-tier sampling — in headline ledger, not buried.
