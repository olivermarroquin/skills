---
name: hub-and-nav-build
version: 1.1
status: active
created: 2026-06-09
updated: 2026-06-09
changelog: "v1.1 (2026-06-09) — added §5 Option D (client-side WPCode JS snippet for non-REST-writable Elementor footers); proven on EV footer-links fix."
description: >
  Builds the hub-page + site-navigation layer on top of an already-live Core 30 leaf corpus for a WordPress
  client, and verifies it renders correctly. This is the layer that makes orphaned city pages reachable: per-service
  hub pages (one per service, each linking its city leaves), one master Service Areas service×city matrix page,
  header-menu rewire (REST), a footer link surface, and leaf backlinks — then a render-accurate verification gate.
  Encodes the hard-won fixes from the 2026-06-09 EV/S&H run: the page <style> CSS contract (the failure that broke
  all 7 hubs three times), the parse-never-string-replace rule for serialized Elementor data, image-by-attachment-ID,
  smart-quote corruption, and the getComputedStyle render gate that finally caught what HTML-string greps and
  web_fetch could not. Composes-with client-seo-onboarding (runs AFTER its leaves are live), gate-peer-reviewer, and
  output-quality-loop.
triggers:
  - "build the hubs and nav for <client>"
  - "the core-30 pages are orphaned, build the hub layer"
  - "add hub pages / service-area hubs for <client>"
  - "wire the header / footer navigation to the core-30 pages"
  - "build the service hubs and the service-areas matrix page"
  - "run hub-and-nav-build on <client>"
  - "do for S&H what we did for EV's hubs"
composes-with:
  - client-seo-onboarding (upstream — builds and publishes the Core 30 leaf pages this skill links together; hubs run after the leaves are live)
  - gate-peer-reviewer (dispatch G-default / G-publish on every hub publish + nav change before it lands)
  - output-quality-loop (artifact-level quality pass on hub page copy)
  - design-emulation-verify (the render-accurate verification gate is shared DNA)
tags: [skill, page-build, hubs, navigation, internal-linking, wordpress, elementor, css-contract, render-verification, seo, substrate-agnostic, client-agnostic]
---

# `hub-and-nav-build` skill v1.0

Builds and verifies the **hub + navigation layer** that sits on top of a live Core 30 leaf corpus. Born from the
2026-06-09 EV Electric run, where the leaves were live but **27 of 30 were orphaned from site navigation**, and the
hub build then broke its own styling three times before a render-accurate check caught it. This skill is the
"never again" version of that build.

**Read this whole file before touching anything.** The load-bearing parts are the **CSS Contract** (§4) and the
**Verification Gate** (§6). Every other step is mechanical; those two are where the run actually bled.

## When to use

- A client's Core 30 leaf pages are published and live, but reachable only via sitemap / sparse in-page cross-links.
- The operator says "build the hubs," "wire the nav," "the pages are orphaned," or "do for S&H what we did for EV."
- NOT for building the leaf pages themselves — that's `client-seo-onboarding` + the `scripts/` toolkit. This skill
  starts where that one ends.

## What it produces

1. **Per-service hub pages** (one per service): service overview + a city-card grid linking every leaf for that
   service + a "why choose" section + CTA. (EV: 6 hubs. S&H: 4.)
2. **One master Service Areas page**: a service×city link matrix + light intro + map. Doubles as the footer link
   surface (Option C, §5).
3. **Header menu rewire**: Services ▾ points at the service hubs (not arbitrary leaves) + a top-level Service Areas
   item. Done over REST.
4. **Footer link surface**: see §5 — Option A (WP nav menu in footer) where the theme allows it, Option C
   (Service Areas hub) where the footer is not REST-writable.
5. **Leaf backlinks**: each leaf gets a `Home > [Service Hub] > This page` breadcrumb back to its parent hub.
6. **A render-verified, cache-busted confirmation** that every new/changed page actually renders styled and linked.

## The non-negotiables (if you remember nothing else)

1. **A hub page's injected `<style>` block must carry the FULL base CSS, not just hub-specific additions.** See §4.
   This single rule is the entire reason the EV hubs broke three times.
2. **Never `string-replace` inside serialized Elementor data (`_elementor_data`).** Parse JSON → edit the node →
   re-serialize. String edits corrupt the structure and silently unstyle the page. See §7.
3. **Verify by RENDER, not by HTML string.** `getComputedStyle` on the live, cache-busted page. `web_fetch` is
   blind to CSS; a grep that finds `gradient` in the HTML does NOT mean the gradient applies. See §6.
4. **Back up first; prefer revision-restore over hand-repair; non-destructive by default.** Never touch the live
   site without a WPvivid backup and without confirming a clean Elementor revision exists to roll back to.

---

## §1. Preconditions & recon (do this before any write)

Confirm and record these for the target client — they differ per theme and per client:

| Fact | EV Electric (reference) | How to find it |
|---|---|---|
| Core 30 leaves live? | 30/30 live | sitemap `page-sitemap.xml` + render-spot-check 2–3 |
| Header menu tech + ID | ElementsKit renders WP Primary Menu **id=55** | `GET /wp/v2/menu-items`; inspect theme |
| Footer tech + REST-writable? | Elementor template **post 4854**, **NOT** REST-writable (no `show_in_rest`) | try `GET /wp/v2/pages/<id>`; check `_elementor_data` exposure |
| `/services/` page ID | **97** | `GET /wp/v2/pages?slug=services` |
| App-password user has `edit_theme_options`? | Yes (`oliver` = Administrator) | `GET /wp/v2/menu-items` returns 200, not 401 |
| Elementor cache clear | `DELETE /elementor/v1/cache` → 200 | — |
| Canonical leaf for CSS source | a known-good leaf, e.g. ev-charger-mclean-va **ID 6330** | pick any leaf confirmed styled-correct |

**S&H deltas (recorded for the test run):** Plumbit theme (no Elementor in header/footer); header = WP `main-menu`,
footer = WP `widget_nav_menu` widgets → **footer IS REST-writable** (Option A viable) **once** the app-password user
has admin caps. The current S&H app-password user **lacks `edit_theme_options`** (menu endpoints 401) → **grant
that user Administrator first** (one-time operator action). 29 leaves → needs **5 hubs** (4 service + 1 master).

If `GET /wp/v2/menu-items` returns 401, stop and surface the admin-caps blocker — do not proceed to nav steps.

## §2. Build sequence

Run in this order. P1 can start immediately; P2–P5 depend on P1; P0 (footer Option A only) is an operator action.

| Phase | What | Mechanism | Depends on |
|---|---|---|---|
| **P0** | (Option A only) operator adds a WP Nav-Menu widget to the footer template | manual, ~5 min | — |
| **P1** | Scaffold + publish the service hubs + the Service Areas matrix | hub template (§3) → `publish-core-30-page.py` | leaves live |
| **P2** | Header rewire: Services ▾ → 6 hubs; add top-level Service Areas | `POST /wp/v2/menu-items` on menu id=55 | P1 |
| **P3** | Footer populate (Option A) OR confirm Service Areas link surface (Option C) | REST menu items / single footer link | P0+P1 or P1 |
| **P4** | `/services/` (ID 97) gets internal links to the 6 hubs | `POST /wp/v2/pages/97` (parse, don't clobber) | P1 |
| **P5** | Leaf backlinks: `Home > Hub > This page` breadcrumb on each leaf | parse-edit `_elementor_data` (§7) | P1 |
| **P6** | **Verification gate** + cache purge + sitemap check | §6 | P2–P5 |

Each publish/nav change goes through gate-peer-reviewer (G-publish or G-default) **before** it lands, per the
Mandatory Pre-Land Review Gate. The §6 render gate is part of P6 and is not skippable.

## §3. Hub page content spec

See `references/hub-page-spec.md` for the full template. In brief:

- **Service hubs (H1–H6):** ~800–1200 words. Service overview (reuse `/services/` copy), **city-card grid** (one
  card per leaf: city name + one-line local hook + link), "Why choose [client] for [service]," CTA. Schema: Service.
- **Master Service Areas (H7):** light intro, **service×city link matrix** (every leaf), map embed, the six service
  cards (each linking its hub). Schema: ServiceArea/LocalBusiness. This page is also the footer link surface (§5).
- Hubs reuse the **same evp-corepage design system** as the leaves — same hero, same fonts, same card styling —
  which is exactly why the **CSS Contract (§4)** governs them.

## §4. THE CSS CONTRACT (load-bearing — read twice)

Hub pages render their body through injected HTML that includes a `<style>` block. That block defines the entire
`evp-corepage` design system: the `Inter` font stack, `.evp-hero` blue gradient, button styles, and the
`.evp-city-card` grid. **The hub-specific rules (city-grid, matrix, check-list) are ADDITIONS on top of the full
base CSS — they are not a replacement for it.**

**The contract:**

- A correct hub `<style>` block ≈ **20,845 chars** = **~18,873 chars of base leaf CSS** + **~1,972 chars of
  hub-specific additions**, with **167 balanced braces**. (EV reference numbers — they scale with the design system,
  not the client; re-measure against your canonical leaf.)
- **Source the base CSS from a known-good leaf** (EV: ev-charger-mclean-va, ID 6330) — extract its full `<style>`
  block, then append the hub additions. Do not hand-author the base CSS.
- **Validate three ways before declaring done:** (a) byte count within ~5% of the leaf's block, (b) balanced
  braces, (c) **render-verify per §6.** Brace-balance alone is NOT sufficient — see the failure below.

**The failure this prevents (EV, 2026-06-09):** an attempt to hide a title banner injected CSS into the hub
`<style>` blocks, then a "revert" **removed** it — and in doing so **stripped ~17K chars of base CSS**, leaving only
the ~2K of hub additions. **Braces stayed balanced, so every string/brace check passed**, but the page rendered in
serif fallback with no hero gradient and plain-text buttons. Two consecutive "all styled" reports were HTML-string
false-passes. Only `getComputedStyle` on the live page caught it. Fix: restore the full leaf CSS + additions; the
correct block is ~20.8K chars / 167 braces.

**Therefore:** never inject or remove a partial CSS edit into a hub's content `<style>` block to achieve a
template-level effect (e.g., hiding a title banner). Template-level changes go through page-settings / the template,
not content CSS. A styled page with an unwanted title banner beats a cosmetically-perfect page that doesn't render.

## §5. Footer options

| Option | When | Trade-off |
|---|---|---|
| **A — WP nav menu in footer widget** | footer is REST-writable (e.g. Plumbit/widget themes) OR operator will do the one-time Elementor widget add | best SEO (site-wide footer links); fully scriptable via `POST /wp/v2/menu-items` thereafter |
| **B — hardcoded HTML grid in footer** | rarely | needs manual update per page; not recommended |
| **C — Service Areas hub as the link surface** | footer NOT REST-writable and no operator edit (e.g. EV's Elementor footer post 4854) | one extra hop vs. direct footer links; scales infinitely; the standard pattern for 30–500 location pages |
| **D — client-side WPCode JS snippet** | footer NOT REST-writable, but you want *real* site-wide footer links (repair wrong hrefs / linkify plain-text items) without an Elementor hand-edit | links appear for users immediately + one-click reversible; injected client-side so crawl-equity is weaker than a server-side menu — pair with C for the crawlable grid |

EV shipped **Option C** for the crawlable grid, then added **Option D** (2026-06-09) to fix/populate the actual
footer Services + Service Areas columns. S&H can do **Option A** once its app-password user has admin caps. Default
to C if the footer is untouchable; add D when the footer's own links are wrong/missing; don't block the whole build
on a footer edit.

### Option D — how (proven on EV, 2026-06-09)

Use when the footer is a non-REST-writable Elementor template and its links need fixing. Deliver as a **WPCode**
snippet: **Code Type = JavaScript Snippet** (raw JS, no `<script>` tags — WPCode auto-wraps), **Location = Site Wide
Footer**, Active. Two hard rules learned the expensive way:

1. **Don't select on a footer wrapper.** Elementor footers frequently have **no** `<footer>` /
   `[data-elementor-type="footer"]` / `.elementor-location-footer` — the footer is just the last
   `.elementor-top-section`, so a wrapper selector matches nothing and the snippet **silently no-ops**. Inspect the
   live DOM and select on the **widget class** that holds the links. On EV the footer columns are Elementor
   **icon-list** widgets → `span.elementor-icon-list-text`.
2. **Scope by widget-class + exact text** (the same service/city strings also appear in body cards
   `h5.dtr-infobox-title`, body buttons `span.dtr-btn-text`, and the header menu `a.ekit-menu-dropdown-toggle`).
   For each matching span: if `closest('a')` exists → set its `href`; else wrap the span in a new `<a>`.

Shape = a `label → URL` map + the text-match loop. Re-inspect the footer widget class per client (may differ by
theme). **Verify live** (Claude in Chrome) before handing the snippet to the operator: confirm every target href and
that the header/body were untouched. Full write-up + reusable snippet:
[[pattern-elementor-clientside-snippet-nav-footer-fix]] · lesson [[lesson-elementor-footer-clientside-link-fix-2026-06-09]] ·
log [[execution-log-2026-06-09-footer-links-fix]]. (Same WPCode channel also fixes header behavior — EV mobile
"Services" dropdown, instance 1 of the pattern.)

## §6. THE VERIFICATION GATE (render-accurate — not skippable)

`web_fetch` and HTML-string greps cannot see whether CSS applies. The only reliable check is computed styles on the
live, cache-busted page. Full protocol + exact assertions in `references/verification-gate.md`. The core:

1. Claude in Chrome → navigate to the live URL **with a cache-buster** (`?v=<token>`).
2. Run `getComputedStyle` assertions on the real elements:
   - body/content paragraph `fontFamily` **starts with the brand font** (`Inter`), not a serif fallback.
   - `.evp-hero` `backgroundImage` **contains `gradient`** and the brand blue (EV: `rgb(2, 40, 64)` → `rgb(8, 113, 188)`).
   - city cards exist and carry their radius (EV: `14px`).
   - styled button count > 0 (anchors with a non-transparent background / radius).
3. **Pass = all assertions true on at least the simplest AND the most complex hub** (EV: `/service-areas/` matrix +
   the 13-city `/electrical-troubleshooting/`). Same restore op ⇒ sampling two representative layouts is sufficient.
4. Log the verdict with the computed-style evidence. A grep for `gradient` in the HTML is **not** evidence.

**The gate always resolves to PASS / FAIL / BLOCKED — and BLOCKED is not a pass.** If the browser/extension is
unavailable, the gate is BLOCKED: raise it loudly, do NOT silently fall back to structural (byte-count / brace /
CSS-present) checks and call it good (a malformed or parse-broken `<style>` passes every structural check while the
rule fails to render). Recovery: run `list_connected_browsers`; if empty, have the operator relaunch Chrome + sign
the extension back in (a pending "Relaunch to update" state is the #1 cause — it suspends the extension); retry. If
still blocked, use the explicit operator-incognito-screenshot fallback and record the verdict as
"PASS-via-operator-screenshot," never a bare PASS. **Two hard corollaries:** (a) the known-good leaf whose CSS the
hubs copy MUST be render-confirmed PASS, never chosen on structural checks (S&H #4895 passed every structural check
and rendered with `backgroundImage: none`); (b) scoping render defects across EXISTING leaves must be done by
render, not a REST CSS-presence diff — a parse-broken leaf still *contains* the right rule, so a presence check
falsely passes it. Full state machine + connectivity protocol: `references/verification-gate.md`.

## §7. Serialized-data safety (Elementor `_elementor_data`)

These rules apply to P4 (`/services/` edit) and P5 (leaf backlinks) and any homepage/footer content touch:

- **Parse → edit the specific node → re-serialize.** Never `string-replace` raw serialized JSON. A bad replace
  corrupts the structure and silently unstyles the page (EV S&H homepage, char 35931, CF7 shortcode).
- **WordPress `wptexturize` turns straight quotes into smart quotes** in body content, which breaks CSS/JSON. Keep
  raw HTML/CSS inside a `wp:html` block; never lead page content with a bare `<style>` (it leaks into AIOSEO meta
  and can render as visible text).
- **Elementor renders images by ATTACHMENT ID, not URL string.** A Better-Search-Replace on the image URL won't
  change a rendered image whose widget references a deleted/renumbered attachment. Re-point the attachment ID via
  REST. (EV favicon-04 fixed this way; Golden-Services-02.png still 404 — gated on host file access.)
- **Back up (WPvivid) before any live edit; prefer Elementor revision-restore over hand-repairing serialized JSON.**

## §8. Failure guardrails (every catalogued failure → its preventive step)

Full catalog with root causes in `references/failure-guardrails.md`, which links the run retrospective
`[[lesson-ev-sh-run-failure-retrospective-2026-06-09]]`. Summary:

| Failure (this run) | Guardrail in this skill |
|---|---|
| Hub CSS stripped → unstyled (×3) | §4 CSS Contract + §6 render gate (byte-count + braces + computed-style) |
| "All styled" HTML-string false-pass (×2) | §6 — render gate is the only accepted evidence |
| Serialized data corrupted by string-replace | §7 parse-not-replace |
| Smart-quote corruption | §7 `wp:html`, no bare leading `<style>` |
| Image didn't change after URL replace | §7 image-by-attachment-ID |
| Indexing "submitted" reported as "indexed/live" | publish reports submitted≠indexed; recheck date set (see onboarding Step 8) |
| Orphaned leaves / dead internal links | this skill's entire purpose + `audit-published-links.py` before/after |
| Stale CDN sitemap / empty bare-URL body | cache purge in P6 + LiteSpeed `sitemap` exclusion (both sites, done) |
| Nav blocked by 401 | §1 — check `edit_theme_options` first; grant admin before nav steps |

## §9. Outputs, logging, commit

- Per significant edit, append a row to `_meta/_event-log.md` (helper: `scripts/append_event_log.sh`).
- Update the client `_deployment-status.md` ledger and `plans/plan-hub-pages-nav-architecture-*.md`.
- Write an execution-log entry under `04_projects/clients/_active/<client>/execution-logs/`.
- Stage commits **by name** (never `git add .`); keep CC paste-backs separate from commit blocks.

## §10. Test / first validation

This skill's first validation target is **S&H Contracting** — 29 leaves live, 0 in nav, needs 5 hubs + nav. The
S&H run exercises the parts EV's path didn't: Option A footer (REST-writable Plumbit widgets) and the admin-caps
precondition. See `references/sh-test-plan.md` for the dispatch.

## See also

- `[[lesson-ev-sh-run-failure-retrospective-2026-06-09]]` — the failure catalog this skill hardens against
- `[[plan-hub-pages-nav-architecture-2026-06-09]]` — the EV architecture this skill generalizes
- `client-seo-onboarding` skill — the upstream leaf pipeline
- `scripts/publish-core-30-page.py`, `scripts/audit-published-links.py`, `scripts/wire-page-images.py`
- patterns: `pattern-core-30-orphan-page-internal-linking`, `pattern-core-30-page-design-system`, `pattern-wordpress-plugin-bridge-rest-shim`
