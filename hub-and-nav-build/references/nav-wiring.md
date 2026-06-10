# Reference: Navigation wiring (header + footer)

How to rewire the header menu and establish a footer link surface over REST, with the per-theme differences seen on
EV (ElementsKit + Elementor) and S&H (Plumbit + WP widgets).

## Precondition: admin caps

Menu endpoints require `edit_theme_options`. Check first:

```
GET /wp-json/wp/v2/menu-items   → 200 = the app-password user can manage menus
                                → 401 = the user lacks caps. STOP. Grant Administrator
                                        role to that user (or issue a new app password
                                        under an admin account) before any nav step.
```

EV's `oliver` user is Administrator (200). S&H's app-password user was **401** → operator must grant admin first.
Do not attempt nav writes until this returns 200.

## Header rewire (REST)

The header menu is a WP nav menu the theme renders. Identify it (`GET /wp/v2/menu-items`, find the menu the theme
assigns to the primary location). EV: **menu id=55**, rendered by ElementsKit.

Goal topology (point the menu at HUBS, not individual leaves, so the header never needs editing again as cities are
added):

```
Home | About | Services ▾ | Service Areas | Contact
                 ├─ Electrical Troubleshooting → /electrical-troubleshooting/
                 ├─ Panel Upgrades             → /panel-upgrade/
                 ├─ EV Charger Installation    → /ev-charger-installation/
                 ├─ Light Fixture Installation → /light-fixture-installation/
                 ├─ Smoke Alarm Installation   → /smoke-alarm-installation/
                 └─ Outlet Installation        → /outlet-installation/
```

Steps:
1. `GET /wp/v2/menu-items?menus=<id>` — record current items (and the "Services" parent item id).
2. Remove the arbitrary leaf sub-items currently under Services (EV had 3 random leaves there).
3. `POST /wp/v2/menu-items` one per service hub, `parent=<Services item id>`, `url=/<hub-slug>/`.
4. `POST /wp/v2/menu-items` a top-level **Service Areas** item → `/service-areas/`.
5. Clear Elementor cache: `DELETE /elementor/v1/cache`.
6. Render-verify the header on a cache-busted page (the menu items appear, links resolve).

**Why hubs-not-leaves:** when a new city or service is added later, only the hub content + the Service Areas matrix
change. The header stays fixed. Zero future header edits.

## Footer link surface

Pick the option the theme allows (see SKILL.md §5):

### Option A — WP nav menu in footer (preferred where possible)
- Viable when the footer is a WP widget area / WP-menu-based (S&H Plumbit `widget_nav_menu`), OR the operator does a
  one-time edit to add a "WordPress Menu" widget to the footer template.
- Create a "Footer Services" menu, then `POST /wp/v2/menu-items` for all leaves + hubs, grouped by service.
- Fully scriptable thereafter — a publish hook can add each new leaf's menu item.

### Option C — Service Areas hub as the link surface (EV's choice)
- Use when the footer is NOT REST-writable and there's no operator edit. EV's footer is an **Elementor template,
  post 4854, not `show_in_rest`** → not REST-writable.
- Keep the footer minimal (or a single "Service Areas" link). Make `/service-areas/` the crawlable grid: every page
  reaches it via the header; it links to every leaf and every hub.
- One extra hop vs. site-wide footer links, but it scales infinitely and is the standard pattern for 30–500
  location-page sites.

**Decision rule:** if the footer is REST-writable or the operator will do the one-time widget add → Option A.
Otherwise → Option C. Never block the whole build waiting on a footer edit.

## `/services/` page (P4)
EV `/services/` = **page ID 97**, Elementor content, originally zero internal links. Add links to the 6 service
hubs by **parsing** the page content / `_elementor_data` and inserting link nodes — never clobber the whole page
body with a string replace (see `failure-guardrails.md` and SKILL.md §7).

## Leaf backlinks (P5)
Each leaf gets a `Home > [Service Hub] > This page` breadcrumb linking up to its parent hub. Edit the leaf's
`_elementor_data` by **parse → insert breadcrumb node → re-serialize**. Confirmed rendering on EV leaves (e.g.
`/electrical-troubleshooting-annandale-va/` shows `Home › Electrical Troubleshooting › This page`).

## Cache after every nav change
`DELETE /elementor/v1/cache` (Elementor) + LiteSpeed purge (manual via wp-admin, or the Keelworks LiteSpeed bridge
plugin). LiteSpeed has a **`sitemap` exclusion** set on both EV and S&H so the sitemap is never served stale —
keep that in place.

## Per-client reference (fill in during recon)

| | EV Electric | S&H Contracting |
|---|---|---|
| Header tech / menu | ElementsKit / WP Primary Menu id=55 | Plumbit / WP `main-menu` |
| Footer tech | Elementor template post 4854 (NOT REST) | Plumbit `widget_nav_menu` (REST-writable) |
| Footer option | C (Service Areas surface) | A (footer menu) once admin caps granted |
| /services/ page id | 97 | (recon) |
| App-user admin caps | yes | **no — grant first** |
| Hubs needed | 6 service + 1 master = 7 | 4 service + 1 master = 5 |
