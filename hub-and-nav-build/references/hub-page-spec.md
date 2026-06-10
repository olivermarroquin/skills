# Reference: Hub page content spec

The content pattern for the two hub types. Both render through the `evp-corepage` design system (so the CSS Contract
in `css-contract.md` governs them).

## Type 1 — Service hub (one per service: H1–H6)

Slug: the bare service slug, e.g. `/electrical-troubleshooting/`, `/panel-upgrade/`, `/ev-charger-installation/`.
Length: ~800–1200 words. Competes for the service-level head term (e.g. "electrical troubleshooting northern
virginia").

Sections, top to bottom:
1. **Hero** — `.evp-hero` (blue gradient): eyebrow (SERVICE NAME), H1 headline, 1–2 sentence subhead, Call + Request
   a Quote buttons, hero image. Same hero component as the leaves.
2. **Service overview** — reuse / adapt the `/services/` copy for this service. "What [service] actually covers."
3. **Cities-we-serve card grid** — one `.evp-city-card` per leaf for this service. Each card: city name (linked to
   the leaf), one-line local hook (e.g. "Older homes with knob-and-tube or Federal Pacific panels are a specialty").
   Card count == number of leaves for that service (EV troubleshooting = 13, panel-upgrade = 6, ev-charger = 5,
   light-fixture = 3, smoke-alarm = 2, outlet = 1).
4. **Why choose [client] for [service]** — credentials, license, review phrase, differentiators.
5. **Final CTA** — `.evp-final-cta` (same gradient): call/quote.

Schema: `Service` (+ the client `LocalBusiness` graph node).

## Type 2 — Master Service Areas hub (H7)

Slug: `/service-areas/`. This is also the **footer link surface** (Option C). Lighter on prose, heavy on links.

Sections:
1. **Hero** — `.evp-hero`: eyebrow (SERVICE AREAS), H1, subhead naming the territory (e.g. "based in Fairfax, VA and
   serves all of Northern Virginia, Washington DC, and Montgomery County, Maryland"), buttons, image.
2. **Our services** — a card per service (6 for EV), each linking its **service hub** and noting how many cities it
   covers ("Serving 13 cities across…").
3. **Cities we serve** — a card per city (linking the city's most relevant leaf or a city view), grouped by state
   (VA / MD / DC).
4. **Full service directory** — the **service × city link matrix**: a table where each (service, city) cell links to
   the corresponding leaf. This is the crawl surface that connects everything.
5. **Map embed** + CTA.

Schema: `ServiceArea` / `LocalBusiness`.

## Build mechanics

- Author the hub HTML against the `evp-corepage` template (same as leaves), with the **full base CSS** in the
  `<style>` block per `css-contract.md`, plus the hub additions (`.evp-city-card` grid, the matrix table styles,
  the service-card grid).
- Publish via `publish-core-30-page.py` (it handles slug create/update, status preservation, AIOSEO meta via the
  bridge plugin, and the GSC indexing submit). Hubs are pages, same as leaves.
- Wrap the injected HTML/CSS in `wp:html`; never lead the page body with a bare `<style>` (it leaks into AIOSEO
  meta and can render as visible text — see `failure-guardrails.md`).
- After publish: render-verify per `verification-gate.md`.

## EV reference (as-built 2026-06-09)

| Hub | WP ID | Slug | Cities |
|---|---|---|---|
| Electrical Troubleshooting | 6347 | /electrical-troubleshooting/ | 13 |
| Panel Upgrades | 6348 | /panel-upgrade/ | 6 |
| EV Charger Installation | 6349 | /ev-charger-installation/ | 5 |
| Light Fixture Installation | 6350 | /light-fixture-installation/ | 3 |
| Smoke Alarm Installation | 6351 | /smoke-alarm-installation/ | 2 |
| Outlet Installation | 6352 | /outlet-installation/ | 1 |
| **Service Areas (master)** | 6353 | /service-areas/ | matrix (all 30) |

Title banner: EV's theme renders a page-title banner above hub content. It is **accepted as-is** — do NOT try to
hide it by injecting CSS into the hub content `<style>` block (that is exactly what stripped the base CSS). If a
client insists on hiding it, do it via the page template / page-settings, then re-run the render gate.
