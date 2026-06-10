# Reference: Failure guardrails

Every failure from the 2026-06-09 EV/S&H hub/nav run, its root cause, and the guardrail in this skill that prevents
it. Full narrative catalog: `[[lesson-ev-sh-run-failure-retrospective-2026-06-09]]`.

The through-line of the whole run: **almost every failure was a claim that ran ahead of its evidence** — a proxy
(HTML string, sitemap, vault draft, "submitted") was checked instead of the actual rendered live end-state.

## A. Styling / CSS

| Failure | Root cause | Guardrail |
|---|---|---|
| All 7 hubs rendered unstyled (serif, no hero, plain buttons) — ×3 | Title-hide CSS injected into hub `<style>` blocks; the "revert" stripped ~17K chars of base CSS, leaving ~2K of additions | **CSS Contract** (`css-contract.md`): hub block = full leaf CSS + additions (~20.8K / 167 braces); source base CSS from a known-good leaf |
| Two "all styled" reports were false | HTML-string greps: CSS present in HTML ≠ CSS applying; braces balanced after strip | **Render gate** (`verification-gate.md`): `getComputedStyle` on cache-busted live page is the only accepted evidence |
| Title banner chase broke the design | Treating a template-level concern (theme title banner) as a content-CSS problem | Template-level changes go through page-settings/template, never content `<style>`; accept the cosmetic flaw over a broken render |

## B. Serialized data / Elementor

| Failure | Root cause | Guardrail |
|---|---|---|
| S&H homepage broke (unstyled) | `string-replace` inside serialized `_elementor_data` (CF7 shortcode, char 35931) corrupted the JSON | **Parse → edit node → re-serialize**; never string-replace serialized data (SKILL.md §7) |
| Body CSS/JSON broke on edit | WordPress `wptexturize` converted straight quotes → smart quotes | Wrap raw HTML/CSS in `wp:html`; never lead content with a bare `<style>` |
| Image didn't change after URL replace (favicon, Golden-Services logo) | Elementor renders images by **attachment ID**, not URL; BSR on the URL string is a no-op; attachments were deleted | Re-point the attachment ID via REST; if the file is missing, it needs host file access (gated on Aisha/Hostinger) |

## C. Verification discipline

| Failure | Root cause | Guardrail |
|---|---|---|
| "01–12 clean" while 03/04/05 showed placeholder text live | Asserted from sitemap + vault drafts, not live HTML | Verify the **live rendered** page, not a proxy; operator caught it in incognito |
| Reviewer missed the S&H homepage break | `web_fetch` can't see CSS/layout | Visual changes need the render gate or an incognito screenshot, never a text fetch |
| Indexing "submitted" reported as "indexed/live" | `urlNotifications:publish` = accepted ≠ indexed; `index.inspect` returns last-known state, no live fetch | Report submitted≠indexed; set a recheck date (EV: 2026-06-22); GSC discovered-count is server-side truth |

## D. Navigation / reachability

| Failure | Root cause | Guardrail |
|---|---|---|
| 27/30 leaves orphaned from nav | No hub layer; header pointed at 3 arbitrary leaves; footer had zero links | This skill's whole purpose: hubs + matrix + header rewire + footer surface + leaf backlinks |
| Nav writes 401 on S&H | App-password user lacks `edit_theme_options` | Check `GET /wp/v2/menu-items` == 200 before any nav step; grant admin first |
| Dead internal links shipped | Highest-numbered draft + shared city-data `other_areas_paragraph` carried stale links | `audit-published-links.py` before and after; fix at the data source, not the live page |

## E. Cache / CDN

| Failure | Root cause | Guardrail |
|---|---|---|
| Slot served empty body on bare URL | Stale CDN edge copy | LiteSpeed purge after publish/nav; cache-bust every verification fetch |
| Sitemap served stale | CDN cached the sitemap | LiteSpeed `sitemap` exclusion set on both sites (keep it); pipeline `verify_sitemap_freshness()` |

## The 4 standing rules these reduce to

1. **A status goes green only when its OWN end-state is render-verified** — not a proxy (HTML string, sitemap,
   draft, "submitted").
2. **Never string-replace serialized data; parse and re-serialize.**
3. **Back up first; prefer revision-restore over hand-repair; non-destructive by default.**
4. **Check `edit_theme_options` before nav; check the live render after every visual change.**
