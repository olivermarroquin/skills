# Reference: S&H Contracting — first validation run

S&H is the skill's first validation target. It exercises the parts EV's path did **not**: an Option-A
(REST-writable) footer and the admin-caps precondition. S&H and EV are both residential electricians and direct
competitors — no reciprocal-partnership angle; treat as independent.

## S&H starting state (from EV plan recon)

- **29 Core 30 leaves live, 0 in nav.** 4 services × up to 15 cities.
- Header: Plumbit theme renders WP `main-menu` — currently only the 5 original service pages.
- Footer: Plumbit `widget_nav_menu` widgets — **REST-writable** (Option A viable) once the user has admin caps.
- **Blocker: the S&H app-password user lacks `edit_theme_options`** → menu endpoints return 401.
- Needs **5 hubs**: 4 service hubs + 1 master Service Areas matrix.

## Preflight (must clear before any write)

1. **Grant admin** to the S&H app-password user (operator, one-time) — OR issue a new app password under an existing
   admin account. Confirm `GET /wp/v2/menu-items` → 200.
2. **WPvivid backup** of the live site.
3. Identify: the canonical known-good S&H leaf (for the CSS source), `/services/` page id, the header menu id, the
   footer widget/menu, and confirm the S&H design system's CSS block size + brace count (re-derive the contract
   numbers — EV's 20.8K/167 are EV's design system, not S&H's).
4. Confirm 29/29 leaves render styled (render gate on 2–3 samples) before building hubs on top.

## Run sequence (per SKILL.md §2)

- **P1** — scaffold + publish 5 hubs (4 service + Service Areas matrix), each carrying the **full S&H leaf base CSS**
  in its `<style>` block + hub additions. Render-gate each hub type after publish.
- **P2** — header rewire on the Plumbit `main-menu`: Services → 4 hubs + a Service Areas item.
- **P3** — **Option A footer** (S&H's footer IS REST-writable): create a "Footer Services" menu, add leaf + hub
  items grouped by service, assign to the footer widget area.
- **P4** — `/services/` internal links to the 4 hubs (parse-edit).
- **P5** — leaf backlinks (`Home > Hub > This page`) on each of the 29 leaves (parse-edit `_elementor_data`/content
  for whatever Plumbit uses; S&H is not Elementor in header/footer, but confirm the leaf body tech).
- **P6** — render gate (cache-busted `getComputedStyle`) on the simplest + most complex hub, header + footer link
  presence, `audit-published-links.py` clean, LiteSpeed purge, sitemap freshness.

## What this run validates about the skill

- The **CSS Contract** generalizes to a different design system (re-derive the numbers; the *shape* should hold —
  base CSS dominates, additions are a thin tail).
- The **Option-A footer** path (untested on EV, which used Option C).
- The **admin-caps precondition** actually gates the nav steps (don't proceed on 401).
- The **render gate** works against a non-Elementor (Plumbit) theme.

## Notes / guardrails specific to S&H

- S&H homepage was previously broken by a `string-replace` into serialized data and restored — **do not** repeat
  that; parse-edit only, back up first.
- S&H deployment ledger: `04_projects/clients/_active/s-and-h-contracting/_deployment-status.md` — update as built.
- Keep CC paste-backs separate from commit blocks; stage files by name.
