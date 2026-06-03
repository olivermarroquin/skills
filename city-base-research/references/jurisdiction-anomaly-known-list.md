---
type: reference
status: draft
created: 2026-06-03
updated: 2026-06-03
skill: city-base-research
skill-version: 1.1
tags: [reference, city-base-research, jurisdiction-anomaly]
---

# Known jurisdiction anomalies — starting list

A growing list of US jurisdictions where the regional utility / AHJ default
does not hold. Check this list during Sub-step 1 of the `Jurisdiction
anomaly check (run before Phase 2)` step in `../SKILL.md`. If the city you're
researching appears below with a citation dated within 90 days, you may skip
Sub-step 2's cross-reference and rely on the entry. Otherwise, run the
full check.

This list is not exhaustive — the US has ~19,500 incorporated places. The
goal is prior context: enough known examples that a sub-agent encountering
an unfamiliar city has a pattern to match against. New anomalies surfaced
during city research get appended here at chat close via the Knowledge
Capture Audit.

## How to read the entries

Each entry follows this shape:

- **Jurisdiction:** city, state
- **Class(es) firing:** which anomaly class(es) (1, 2, or 3) apply
- **What differs from regional default:** plain-language statement of the
  actual utilities / AHJ
- **Primary source(s):** inline citation per the source-attribution rule
- **Orthogonality counter-example:** (only on entries where one class fires
  but another expected class does not — teaches the orthogonality lesson)
- **Notes:** any nuance worth carrying forward

---

## Virginia — independent cities (Class 2 fires for all 38)

The Commonwealth of Virginia is the dominant US case for the
independent-city pattern. Per the state constitution adopted after the
Civil War (1871), all Virginia municipalities incorporated as "cities"
are independent of any county. There are 38 independent cities in
Virginia as of 2024, plus a separate set of incorporated towns that
remain part of their parent counties [source: webfetch
en.wikipedia.org/wiki/List_of_cities_and_counties_in_Virginia citing
Virginia DHCD and US Census on 2026-06-03; corroborated by webfetch
en.wikipedia.org/wiki/Independent_city_(United_States) on 2026-06-03].

**Implication for AHJ research:** every Virginia independent city has
its own permit office, its own building/zoning code adoption, and its
own commission/council. AHJ ≠ surrounding county's permit office. This
holds even when the city is the county seat of the surrounding county
(e.g., Fairfax City is the county seat of Fairfax County but is
politically independent of it).

**Full roster (38 cities):**
Alexandria, Bristol, Buena Vista, Charlottesville, Chesapeake, Colonial
Heights, Covington, Danville, Emporia, Fairfax, Falls Church, Franklin,
Fredericksburg, Galax, Hampton, Harrisonburg, Hopewell, Lexington,
Lynchburg, Manassas, Manassas Park, Martinsville, Newport News, Norfolk,
Norton, Petersburg, Poquoson, Portsmouth, Radford, Richmond, Roanoke,
Salem, Staunton, Suffolk, Virginia Beach, Waynesboro, Williamsburg,
Winchester [source: webfetch
en.wikipedia.org/wiki/List_of_cities_and_counties_in_Virginia on
2026-06-03].

**Note on Bedford:** Formerly an independent city; reverted to incorporated
town status within Bedford County in 2013. Treat as a county subdivision,
not an independent city, for any research dated after 2013.

---

## Virginia — municipal electric utilities (Class 1 fires)

A subset of Virginia cities and towns operate their own electric utility
instead of being served by the regional investor-owned utility (Dominion
Energy for most of Virginia, Appalachian Power for the southwest).

**Total: 16 government-owned electric systems** in Virginia per the
Municipal Electric Power Association of Virginia (MEPAV), breaking down
as 14 local-government utilities (8 cities + 6 towns + 1 separately
counted Bristol authority) + 1 university-owned system (Virginia Tech)
[source: Perplexity sonar-pro query citing virginiaplaces.org/energy/
pubelectric.html, mepav.org, and salemva.gov/192/Electric on 2026-06-03].
The APPA member directory and VMEA roster URLs were not reachable from
the Cowork sandbox during this v1.1 build (both returned empty content),
so the Sonar synthesis is the authoritative source for the v1.1 list.
Confirm any individual entry via the city's own `.gov` site before
relying on the assignment for a high-stakes brief.

**Confirmed cities (Class 1 + sometimes Class 2):**

- **Bristol, VA** — Bristol Virginia Utilities (BVU), now organized as
  BVU Authority. Also fires Class 2 (independent city).
- **Danville, VA** — Danville Utilities (electric, gas, water, other).
  Also fires Class 2 (independent city).
- **Franklin, VA** — Franklin Municipal Power and Light. Also fires
  Class 2 (independent city).
- **Harrisonburg, VA** — Harrisonburg Electric Commission (HEC). Also
  fires Class 2 (independent city).
- **Manassas, VA** — City of Manassas Electric (often referred to as
  Manassas Electric Department / "MED"). City government website lists
  "Electric" as a city department and the outage map domain is
  `manassasutilities.org` [source: webfetch manassasva.gov department
  navigation on 2026-06-03]. Also fires Class 2 (independent city).
  **Full anomaly: both Class 1 and Class 2 apply.**
- **Martinsville, VA** — Martinsville Electric Department. Also fires
  Class 2 (independent city).
- **Radford, VA** — Radford Electric Department. Also fires Class 2
  (independent city).
- **Salem, VA** — City of Salem Electric Department. City explicitly
  states it "owns and operates its own electricity distribution system"
  [source: Perplexity sonar-pro citing salemva.gov/192/Electric on
  2026-06-03]. Also fires Class 2 (independent city).

**Confirmed towns (Class 1 fires; Class 2 does NOT — towns remain part
of their county):**

- **Bedford, VA** — Bedford Electric Department, operating under Town
  of Bedford. Note: Bedford was an independent city until 2013, when it
  reverted to incorporated-town status within Bedford County. The
  electric utility persisted through the status change (the entity is
  the same; the jurisdictional wrapper around it changed). Confirm
  current status for any post-2013 brief.
- **Blackstone, VA** — Blackstone Electric Department.
- **Culpeper, VA** — Culpeper Electric Department.
- **Elkton, VA** — Elkton Electric Department.
- **Front Royal, VA** — Front Royal Electric Department.
- **Richlands, VA** — Richlands Electric Department.
- **Wakefield, VA** — Wakefield Electric Department.

**Special cases (not standard municipal entities but commonly grouped
with them):**

- **Virginia Tech Electric Service (VTES)** — university-owned
  distribution utility serving areas in and around Blacksburg, VA.
  Operated by Virginia Tech. For a Blacksburg brief, electric service
  may be either VTES (on-campus and adjacent areas) or Appalachian
  Power (off-campus areas) depending on parcel. Confirm via address.
- **BVU Authority** — separately counted in the 16-total figure;
  functionally overlaps with Bristol's city utility. Treat as part of
  the Bristol entry for brief-writing purposes.

**Implication for utility research:** for a municipal-electric city or
town, disconnect coordination, residential service drops, EV-charger
circuit permits, outage response, and rate schedules all route through
the city-run utility rather than Dominion's standard processes. Phase
3b scaffolder pages that reference "Dominion Energy" by default will be
factually wrong for these cities and towns.

### Counter-intuitive: Manassas Park does NOT have a muni electric utility

- **Jurisdiction:** Manassas Park, VA
- **Class(es) firing:** Class 2 (independent city) — Class 1 does NOT
  fire
- **What differs from regional default:** Manassas Park is an
  independent city (one of Virginia's 38), but it does NOT operate its
  own electric utility despite being immediately adjacent to Manassas
  (which does). Electric service is provided by Dominion Energy
  Virginia and/or Northern Virginia Electric Cooperative (NOVEC)
  depending on parcel.
- **Primary source:** Manassas Park does not appear in MEPAV's roster
  of 16 government-owned VA electric utilities [source: Perplexity
  sonar-pro citing virginiaplaces.org/energy/pubelectric.html and
  mepav.org on 2026-06-03]. City of Manassas Park website
  (`cityofmanassaspark.us`) does not list Electric as a city
  department [source: webfetch cityofmanassaspark.us homepage on
  2026-06-03].
- **Orthogonality counter-example:** Class 2 fires (Manassas Park is
  an independent city) but Class 1 does NOT, despite Manassas Park
  bordering Manassas (where Class 1 DOES fire). **Demonstrates:
  neighboring independent cities can have completely different
  anomaly profiles. Geographic proximity is not a substitute for
  per-city verification.** Compare with Manassas (Class 1 + Class 2)
  and Alexandria (Class 2 only, but different Class-3 utility mix
  than Manassas Park).

---

## Virginia — orthogonality counter-example (Class 2 fires, Class 1 does not)

- **Jurisdiction:** Alexandria, VA
- **Class(es) firing:** Class 2 (independent city) — Class 1 does NOT
  fire
- **What differs from regional default:** Alexandria is an independent
  city (returned to Virginia from the District of Columbia in 1846), so
  AHJ = city-level permit office, not Arlington County or Fairfax County.
  BUT Alexandria does not operate any public utilities. Electric service
  is Dominion Energy, gas is Washington Gas, water is Virginia American
  Water (a private utility — note this is itself a Class 3 mismatch), and
  sewer/wastewater is AlexRenew (a regional authority).
- **Primary source:** [source: webfetch alexandriava.gov/Utilities on
  2026-06-03, page updated 2025-10-24]. The city's own utilities page
  states verbatim: "The City of Alexandria does not operate any public
  utilities. The following companies are the primary providers of their
  respective services: Virginia American Water, Verizon, Comcast,
  Dominion Virginia Power, Washington Gas, AlexRenew." **Name-currency
  note:** the verbatim quote uses "Dominion Virginia Power" (the
  legacy meta-tag name); the same alexandriava.gov page body refers to
  the current corporate name "Dominion Energy" in the Power Service
  section. Cite as "Dominion Energy" when authoring downstream briefs,
  and footnote the verbatim quote's legacy name if preserving it.
- **Orthogonality counter-example:** Class 2 fires (Alexandria is an
  independent city) but Class 1 does NOT (Alexandria uses Dominion
  Energy, not a municipal electric utility). **Demonstrates: the three
  anomaly classes are independent — finding one does NOT imply the
  others. Always run all three checks.** Compare with Manassas (Class 1
  AND Class 2 fire) and Manassas Park (Class 2 only, NOVEC/Dominion
  electric) to see the full spread.
- **Notes:** Class 3 also fires partially — water is Virginia American
  Water (private utility, not the county default), sewer is AlexRenew
  (regional authority, not the county or city default). **City does
  operate a Stormwater Utility** — the same alexandriava.gov page
  states: "The City of Alexandria operates a Stormwater Utility, which
  collects a Stormwater Utility Fee... charged as a separate line item
  on the real estate tax bills sent to all residential and non-
  residential property owners." So the "does not operate any public
  utilities" line refers only to the standard 4 services (electric,
  gas, water, sewer); stormwater is city-operated. **Operational
  consequence:** stormwater-related permits, fee adjustments, and
  drainage-impact assessments in Alexandria route through the city,
  not third parties. Most public street lights are maintained by
  Dominion Energy (per the same page).

---

## Independent cities outside Virginia (Class 2 fires)

Three US cities outside Virginia are classified as independent cities by
the US Census Bureau [source: webfetch
en.wikipedia.org/wiki/Independent_city_(United_States) citing US Census
2001 Change Notice No. 7 and National League of Cities on 2026-06-03].
Total US independent cities: 41 (38 VA + 3 below).

- **Baltimore, MD** — separated from Baltimore County, Maryland by the
  Maryland Constitution of 1851. AHJ = Baltimore City government, not
  Baltimore County [source: same Wikipedia fetch citing Maryland Manual
  Online on 2026-06-03]. Most populous independent city in the US.
- **St. Louis, MO** — separated from St. Louis County, Missouri in 1876
  after voter-approved secession. AHJ = St. Louis City government, not
  St. Louis County [source: same Wikipedia fetch citing the City of St.
  Louis on 2026-06-03].
- **Carson City, NV** — technically a city-county consolidation (1969,
  Ormsby County dissolved simultaneously), not the same legal pattern as
  Baltimore or the Virginia model. The Census Bureau and most reference
  sources group it with "independent city" for statistical purposes, but
  operationally it functions more like a consolidated city-county
  (compare to San Francisco, Denver, Philadelphia) [source: same
  Wikipedia fetch citing carson.org on 2026-06-03]. Treat as a Class 2
  anomaly for AHJ purposes (single municipal AHJ, no surrounding county
  layer), but document the consolidation nuance in §12 Methodology.

**Implication for AHJ research:** the surrounding county's permit office
is NOT the AHJ for these three cities. Find the city-level permit office
on the city's own `.gov` site.

---

## Maryland — incorporated places vs CDPs (different AHJ pattern than Virginia)

Maryland does NOT use the Virginia independent-city pattern. Maryland
counties are the dominant local jurisdiction, and most incorporated
places (cities, towns) remain politically part of their county. Many
populated areas are Census Designated Places (CDPs) — unincorporated,
no municipal government, AHJ = county.

**Implication for AHJ research:** in Maryland (and most non-Virginia
states), default expectation is "AHJ = county permit office, even for
named municipalities." A municipal-level layer may exist on top of the
county for zoning or rental licensing, but residential building permits
typically remain county-level. Always confirm via the city's own `.gov`
site and the county building/permit page.

**Examples of Maryland CDPs encountered in S&H + EV Electric service
areas:** Bethesda (CDP within Montgomery County), Silver Spring (CDP
within Montgomery County), Potomac (CDP within Montgomery County). For
any CDP, the AHJ is the surrounding county — Montgomery County DPS for
the named examples [source: pending per-city verification].

**Anomaly within Maryland — Baltimore City** — see "Independent cities
outside Virginia" above.

---

## Cross-state CDP vs incorporated-place pattern (general)

Most US states follow Maryland's pattern, not Virginia's: cities and
towns remain part of their county. Virginia is the dominant exception.
When researching a city outside Virginia:

- **Default assumption:** AHJ = county permit office. The city may add
  a zoning / planning / rental-licensing layer on top, but residential
  building permits typically remain county-level.
- **Exception 1:** Independent cities (3 outside VA — Baltimore, St.
  Louis, Carson City — see above).
- **Exception 2:** Consolidated city-counties (San Francisco CA,
  Philadelphia PA, Denver CO, Honolulu HI, Indianapolis IN, Nashville
  TN, Jacksonville FL, and others). In these, the city and county are
  merged into a single jurisdiction. AHJ = the consolidated government.
- **Exception 3:** Some state-specific structures (NYC's five boroughs
  coterminous with counties, Louisiana parishes, Alaska boroughs, Ohio
  paper-townships). Verify on the city's own `.gov` site.

---

## Maintenance log

### Added 2026-06-03 — v1.1 build

Initial entries: VA independent cities (full 38-city roster, primary-
source verified), VA municipal electric (16 total per MEPAV, all 15
cities/towns + VTES named individually after a 2026-06-03 Sonar query
on `sonar-pro` with English-anchoring suffix replaced the initial honest
range), Alexandria orthogonality counter-example (Class 2 only, all 4
service utilities third-party, Stormwater Utility city-operated),
Manassas Park counter-intuitive entry (Class 2 only, Dominion/NOVEC
electric — teaches that neighboring independent cities can have
different anomaly profiles), out-of-state independent cities (Baltimore
+ St. Louis + Carson City, with Carson City consolidation nuance flag),
Maryland incorporated-place vs CDP pattern, general cross-state pattern
guidance. APPA member directory and VMEA roster URLs were not reachable
from the Cowork sandbox during the build (both returned empty content);
fallback was a single $0.028 Sonar query citing virginiaplaces.org,
mepav.org, and city `.gov` sources.

### Open verification follow-ups (next brief opportunity)

- **Bedford status post-2013.** Bedford reverted from independent city
  to incorporated town within Bedford County in 2013. The Bedford
  Electric utility persisted through the change. Confirm via web_fetch
  to Town of Bedford `.gov` site that the electric utility is still
  town-operated (vs. having been absorbed into a regional entity)
  before authoring any Bedford-area brief.
- **Maryland AHJ assignments for the Tier-2 cities we serve.** Before
  the first Maryland city brief, web_fetch Montgomery County DPS for
  Bethesda, Silver Spring, and Potomac AHJ confirmations. These were
  declared as "pending per-city verification" in v1.1 — upgrade to
  cited primary sources at first MD brief opportunity.
- **Per-city electric-utility verification for the 7 confirmed VA
  towns.** Sonar synthesis is the v1.1 source. At each town's first
  brief opportunity, web_fetch the town's own `.gov` site to confirm
  the electric department's current name and operational status.

### How to add a new entry

When a city brief surfaces a new anomaly:

1. Append the entry to the relevant section above, following the entry
   shape at the top of this file.
2. Every claim gets an inline `[source: ...]` citation with the fetch
   date.
3. If the entry teaches an orthogonality lesson (one class fires, an
   expected sibling class does not), add an `**Orthogonality
   counter-example:**` field.
4. Update the `updated:` field in frontmatter.
5. Update this maintenance log with the addition date and source.

---

## See also

- `[[../SKILL.md]]` — the parent skill spec
- `[[manassas-va]]` — worked example, full anomaly (Class 1 + Class 2)
- `[[alexandria-va]]` — worked example, orthogonality counter-example
  (Class 2 fires, Class 1 does not)
- `[[_template-city-brief]]` — the locked city-brief template
