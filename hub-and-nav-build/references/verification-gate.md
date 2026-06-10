# Reference: The render-accurate verification gate

> The check that finally caught what HTML-string greps and `web_fetch` missed all run. Use it on every
> new/changed hub, leaf-backlink, and nav change before declaring done.

## Why HTML-string checks are not enough

- `web_fetch` retrieves raw HTML without applying CSS. It can confirm text exists; it **cannot** tell you whether a
  page renders styled. Treat its "looks fine" as "the text is present," nothing more.
- A grep that finds `gradient`, `Inter`, or a button class **in the HTML** proves the CSS is *present*, not that it
  *applies*. The EV failure had all those strings present while the page rendered in serif fallback (the rules were
  in a stripped/non-applying block, or the class existed only as an element attribute).
- Brace-balance and byte-count are structural, not visual. Necessary, not sufficient.

**The only accepted evidence of a visual result is computed style on the live, cache-busted page.**

## Protocol (Claude in Chrome)

1. `list_connected_browsers` → `select_browser` → `tabs_context_mcp(createIfEmpty:true)` to get a tab.
2. `navigate` to the live URL **with a cache-buster** so you never read a stale CDN/page cache copy:
   `https://<domain>/<hub-slug>/?v=<unique-token>`.
3. Run a `javascript_tool` snippet that returns computed styles of the real elements (below).
4. Assert. Pass only when every assertion holds on **at least the simplest AND the most complex hub** in the batch.
5. Log the returned values as the evidence in the review-pass marker. Not a grep — the actual `getComputedStyle`
   output.

## The assertions (EV reference values — re-derive per client design system)

| Element | Property | Pass condition (EV) |
|---|---|---|
| body/content `<p>` | `fontFamily` | starts with `Inter` (brand sans), **not** a serif fallback |
| `.evp-hero` | `backgroundImage` | contains `gradient` AND brand blue `rgb(2, 40, 64)` → `rgb(8, 113, 188)` |
| `.evp-final-cta` | `backgroundImage` | contains the same gradient |
| `.evp-city-card` (or `[class*="city-card"]`) | count + `borderRadius` | count == leaf count for that hub; radius `14px` |
| styled `<a>` buttons | count | > 0 (non-transparent background or radius / padding) |
| `.evp-hero-image` | **image fill** | contains a real `<img>` whose `naturalWidth > 0`, OR a non-empty `backgroundImage`. **NOT just placeholder caption text.** A styled-but-empty hero-image box is an INCOMPLETE page, not a pass. |

**Hero-image fill is part of the gate, learned the hard way (S&H hubs, 2026-06-09):** all 5 S&H hubs passed
font/gradient/cards/buttons but shipped with an EMPTY hero-image slot — the generator emitted a placeholder caption
("<Service> — N Cities Served") in a translucent box and no `<img>` was ever wired. The render gate missed it
(it didn't assert image fill); the operator caught the ghosted box by eye. Always assert the hero image is actually
filled, not just that the surrounding CSS applies.

## Reference snippet

```javascript
(() => {
  const out = { url: location.pathname };
  const p = document.querySelector('.evp-corepage p, .entry-content p, main p');
  out.bodyFont = p ? getComputedStyle(p).fontFamily.split(',')[0] : 'no-p';
  const hero = document.querySelector('.evp-hero');
  out.heroGradient = hero ? getComputedStyle(hero).backgroundImage.slice(0, 70) : 'no-hero';
  const himg = document.querySelector('.evp-hero-image');
  const im = himg ? himg.querySelector('img') : null;
  out.heroImageFilled = !!(im && im.naturalWidth > 0) || (himg && getComputedStyle(himg).backgroundImage !== 'none');
  const cards = document.querySelectorAll('.evp-city-card, [class*="city-card"]');
  out.cardCount = cards.length;
  out.cardRadius = cards[0] ? getComputedStyle(cards[0]).borderRadius : 'n/a';
  out.styledButtons = [...document.querySelectorAll('a')].filter(a => {
    const cs = getComputedStyle(a);
    return cs.backgroundColor !== 'rgba(0, 0, 0, 0)' || cs.borderRadius !== '0px';
  }).length;
  out.evpPresent = !!document.querySelector('.evp-corepage');
  return out;
})()
```

Expected on a healthy EV hub:
`bodyFont: "Inter"`, `heroGradient` contains `linear-gradient(135deg, rgb(2, 40, 64) 0%, rgb(8, 113, 188)…`,
`cardCount` == that hub's city count, `cardRadius: "14px"`, `styledButtons > 0`, `evpPresent: true`.

## Detector caution — don't over-exclude `<nav>` (breadcrumbs)

When verifying body content like breadcrumbs, do NOT blanket-exclude `<nav>` / `[class*="menu"]` ancestors to
"skip the nav menu" — a breadcrumb is a **semantic `<nav class="evp-breadcrumb">`** living in page content, so a
nav-exclusion filter false-negatives it. Match the breadcrumb element directly (`nav.evp-breadcrumb` /
`[class*="breadcrumb"]`). Also note the leaf breadcrumb's **last segment is the page TITLE, not the literal "This
page."** (S&H 2026-06-10: the reviewer's first breadcrumb check false-negatived on both counts; the breadcrumbs
were actually fine. Looking at the real DOM, not trusting the failing automated check, is what resolved it.)

## Sampling rule

A whole batch of hubs restored/published in **one operation** from the **same CSS source** can be verified by
sampling **two representative layouts** — the simplest (e.g. the Service Areas matrix) and the most complex (e.g.
the 13-city service hub). If both pass, the rest of that same-operation batch is high-confidence. If the hubs were
edited individually, verify each.

## Gate states — PASS / FAIL / BLOCKED (the gate ALWAYS resolves to one)

The render gate is not optional and it never silently degrades. Every run resolves to exactly one state, and the
state is recorded:

- **PASS** — computed-style assertions all true on the live cache-busted page. Only then may the artifact land.
- **FAIL** — an assertion is false (e.g. hero `backgroundImage: none`). Stop, surface the defect, fix, re-run.
- **BLOCKED** — the gate could **not be run** (browser/extension unavailable, no `getComputedStyle` access). **BLOCKED
  IS NOT A PASS.** It must be raised LOUDLY and it blocks "done." It may NEVER be silently downgraded to a
  structural check (byte-count / brace-balance / CSS-string-present) and called good. Structural checks are a
  pre-filter, not a substitute for the render verdict — a malformed or parse-broken `<style>` block passes every
  structural check while the rule fails to apply (this is exactly how EV's hubs and S&H's broken leaves slipped).

### What to do on BLOCKED (do not proceed on structural checks)

1. **Connectivity preflight first.** Before relying on the gate, call `list_connected_browsers`. Empty array = the
   extension is offline. Do not pretend the gate ran.
2. **Try to recover:** ask the operator to **relaunch Chrome and sign the extension back in** (a pending "Relaunch
   to update" state suspends the extension's service worker and drops the connection — the #1 cause of BLOCKED).
   Then retry `list_connected_browsers` → `select_browser` → `tabs_context_mcp`.
3. **If still BLOCKED, use the explicit operator-screenshot fallback** — ask for an **incognito** screenshot of the
   sampled page(s) (incognito avoids the operator's own cache; note the extension does NOT drive incognito tabs, so
   the reviewer's own `getComputedStyle` must run in a normal-profile tab). Record the verdict as
   "PASS-via-operator-screenshot," not "PASS." This keeps a human render-check in the loop instead of a silent skip.
4. **Never let a CSS-source / known-good leaf be selected on a BLOCKED basis.** The leaf whose CSS the hubs copy
   MUST be render-confirmed PASS. Choosing it on structural checks alone is how a broken leaf becomes the template
   for every hub (S&H #4895: passed byte/brace/marker checks, rendered with `backgroundImage: none`).

## Scope-checking EXISTING leaves: render, not CSS-presence

When auditing how many existing leaves carry a render defect, you CANNOT rely on a REST markup/CSS-presence diff.
A parse-broken `<style>` block still *contains* the correct rule and the correct element class — the rule simply
doesn't apply at render. A CSS-presence check reports such a leaf as healthy (false PASS). The only reliable scope
check is the **computed style on each rendered page** (e.g. `getComputedStyle('.evp-hero').backgroundImage !==
'none'`). Budget for a render sweep of the corpus, not a text diff. (S&H 2026-06-09: #4895 and #4911 had identical
gradient rules present; only #4911 computed the gradient — REST presence-diff would have missed the breakage.)

## What to record

In the review-pass marker / execution log, record the **actual computed-style values** returned, the **cache-buster
token used**, and which hubs were sampled. "Greps clean" or "looks styled" is not an acceptable record.
