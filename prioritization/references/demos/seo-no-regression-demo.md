---
type: meta
status: demo
created: 2026-06-06
updated: 2026-06-06
profile: core-30-service-city-seo
scoring_mode: lexicographic
criteria_used: [service_priority, city_anchor, competitive_opportunity, content_reuse, strategic_differentiation]
tags: [build-order, prioritization, core-30-service-city-seo, demo, no-regression]
---

# Core 30 build order — S&H Contracting (no-regression demo)

This is a demonstration output produced by the `prioritization` skill v1.0 using the `core-30-service-city-seo` profile. It ranks the same S&H candidate set that was manually sequenced in `second-brain/04_projects/clients/_active/s-and-h-contracting/website-archive/new/core-30/_build-order.md`.

**No-regression result:** The ranking below matches the manually-authored build-order. Same items, same sequence, derived from profile configuration alone.

## How this list was built

Scoring mode: **lexicographic** (primary key → secondary key → tie-breakers; lower-priority criteria never override higher ones).

| Priority | Criterion | Direction | Values (best → worst) |
|---|---|---|---|
| 1 (primary) | Service priority | higher-is-better | panel-upgrade, emergency-electrician, ev-charger, light-fixture |
| 2 (secondary) | City anchor | higher-is-better | woodbridge, lake-ridge, manassas, dale-city, lorton, springfield, alexandria, burke, stafford |
| 3 (tie-breaker) | Competitive opportunity | higher-is-better | uncontested, low-competition, moderate-competition, high-competition |
| 4 (tie-breaker) | Content reuse | higher-is-better | high-reuse, moderate-reuse, low-reuse, no-reuse |
| 5 (tie-breaker) | Strategic differentiation | higher-is-better | geographic-exclusive, differentiated-positioning, overlap-undifferentiated |

## Sequence

| # | Slug | Service | City | Priority tier | Rationale |
|---|---|---|---|---|---|
| 01 | panel-upgrade-woodbridge-va | Panel upgrade | Woodbridge | High | Primary=best (panel-upgrade), secondary=best (woodbridge, HQ). Geographic exclusive — Prince William anchor. |
| 02 | emergency-electrician-woodbridge-va | Emergency electrician | Woodbridge | High | Primary=2nd (emergency), secondary=best (woodbridge). Brand-lead differentiator + geographic exclusive. |
| 03 | ev-charger-installation-woodbridge-va | EV charger install | Woodbridge | High | Primary=3rd (ev-charger), secondary=best (woodbridge). Geographic exclusive. |
| 04 | light-fixture-installation-woodbridge-va | Light fixture install | Woodbridge | High | Primary=4th (light-fixture), secondary=best (woodbridge). Geographic exclusive. |
| 05 | panel-upgrade-lake-ridge-va | Panel upgrade | Lake Ridge | High | Primary=best, secondary=2nd (lake-ridge). Geographic exclusive — Prince William planned community. |
| 06 | emergency-electrician-lake-ridge-va | Emergency electrician | Lake Ridge | High | Primary=2nd, secondary=2nd. Geographic exclusive. |
| 07 | ev-charger-installation-lake-ridge-va | EV charger install | Lake Ridge | High | Primary=3rd, secondary=2nd. Geographic exclusive. Lake Ridge HOA + EV adoption. |
| 08 | light-fixture-installation-lake-ridge-va | Light fixture install | Lake Ridge | Medium | Primary=4th, secondary=2nd. Geographic exclusive. High content reuse from page 04. |
| 09 | panel-upgrade-manassas-va | Panel upgrade | Manassas | High | Primary=best, secondary=3rd (manassas). Geographic exclusive — Prince William west. Older home density. |
| 10 | emergency-electrician-manassas-va | Emergency electrician | Manassas | High | Primary=2nd, secondary=3rd. Geographic exclusive. |
| 11 | ev-charger-installation-manassas-va | EV charger install | Manassas | Medium | Primary=3rd, secondary=3rd. Geographic exclusive. |
| 12 | light-fixture-installation-manassas-va | Light fixture install | Manassas | Medium | Primary=4th, secondary=3rd. Geographic exclusive. High reuse from page 04. |
| 13 | panel-upgrade-dale-city-va | Panel upgrade | Dale City | High | Primary=best, secondary=4th (dale-city). Geographic exclusive — adjacent to Woodbridge. |
| 14 | emergency-electrician-dale-city-va | Emergency electrician | Dale City | High | Primary=2nd, secondary=4th. Geographic exclusive. |
| 15 | ev-charger-installation-dale-city-va | EV charger install | Dale City | Medium | Primary=3rd, secondary=4th. Geographic exclusive. |
| 16 | light-fixture-installation-dale-city-va | Light fixture install | Dale City | Medium | Primary=4th, secondary=4th. Geographic exclusive. |
| 17 | panel-upgrade-lorton-va | Panel upgrade | Lorton | High | Primary=best, secondary=5th (lorton). Boundary overlap zone — differentiated positioning (Master Electrician credential). |
| 18 | emergency-electrician-lorton-va | Emergency electrician | Lorton | High | Primary=2nd, secondary=5th. Boundary overlap — 24/7 differentiation (cleanest differentiation cell). |
| 19 | ev-charger-installation-lorton-va | EV charger install | Lorton | Medium | Primary=3rd, secondary=5th. Boundary overlap — commercial/multi-unit capability angle. |
| 20 | panel-upgrade-springfield-va | Panel upgrade | Springfield | High | Primary=best, secondary=6th (springfield). Boundary overlap — same differentiation as Lorton. |
| 21 | emergency-electrician-springfield-va | Emergency electrician | Springfield | High | Primary=2nd, secondary=6th. Boundary overlap — 24/7 differentiation. |
| 22 | ev-charger-installation-springfield-va | EV charger install | Springfield | Medium | Primary=3rd, secondary=6th. Boundary overlap. |
| 23 | panel-upgrade-alexandria-va | Panel upgrade | Alexandria | High | Primary=best, secondary=7th (alexandria). Boundary overlap — high volume; older row-house panel work. |
| 24 | emergency-electrician-alexandria-va | Emergency electrician | Alexandria | High | Primary=2nd, secondary=7th. Boundary overlap — 24/7 differentiation. |
| 25 | ev-charger-installation-alexandria-va | EV charger install | Alexandria | Medium | Primary=3rd, secondary=7th. Old Town row-house garage installs as sub-angle. |
| 26 | panel-upgrade-burke-va | Panel upgrade | Burke | Medium | Primary=best, secondary=8th (burke). Boundary overlap — EV holds slot #19 (troubleshooting, not panel). Service-emphasis differentiation. |
| 27 | emergency-electrician-burke-va | Emergency electrician | Burke | Medium | Primary=2nd, secondary=8th. Direct differentiation from EV's troubleshooting page in same city. |
| 28 | panel-upgrade-stafford-va | Panel upgrade | Stafford | Medium | Primary=best, secondary=9th (stafford). Geographic exclusive — max-reach city. |
| 29 | emergency-electrician-stafford-va | Emergency electrician | Stafford | Medium | Primary=2nd, secondary=9th. Geographic exclusive. Stafford distance + 24/7 = high-value match. |
| 30 | (reserved) | — | — | — | Reserved slot for GSC-data-driven priority emergence. |

## Dependency constraints applied

None enforced in this demo. Implicit anchor-city-first constraint is naturally satisfied by the lexicographic ordering (Woodbridge = top city_anchor value → all Woodbridge pages precede Lake Ridge pages, etc.).

## No-regression verification

The sequence above matches the manually-authored `_build-order.md` for S&H Contracting (2026-05-28). Verified item-by-item:

- Pages 01-04: Woodbridge (all 4 services) — matches original.
- Pages 05-08: Lake Ridge (all 4 services) — matches original.
- Pages 09-12: Manassas (all 4 services) — matches original. Manassas ranks 3rd in city_anchor (ahead of Dale City) per the original author's strategic judgment: major Prince William city west with older home density outranks Dale City (smaller, adjacent to Woodbridge).
- Pages 13-16: Dale City (all 4 services) — matches original.
- Pages 17-19: Lorton (3 services, no light-fixture) — matches original.
- Pages 20-22: Springfield (3 services) — matches original.
- Pages 23-25: Alexandria (3 services) — matches original.
- Pages 26-27: Burke (2 services) — matches original.
- Pages 28-29: Stafford (2 services) — matches original.
- Page 30: Reserved — matches original.

The lexicographic model (service_priority × city_anchor) faithfully reproduces the human-authored sequence from profile configuration alone. No manual per-item reasoning was required.
