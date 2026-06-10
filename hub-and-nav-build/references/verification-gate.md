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

## Reference snippet

```javascript
(() => {
  const out = { url: location.pathname };
  const p = document.querySelector('.evp-corepage p, .entry-content p, main p');
  out.bodyFont = p ? getComputedStyle(p).fontFamily.split(',')[0] : 'no-p';
  const hero = document.querySelector('.evp-hero');
  out.heroGradient = hero ? getComputedStyle(hero).backgroundImage.slice(0, 70) : 'no-hero';
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

## Sampling rule

A whole batch of hubs restored/published in **one operation** from the **same CSS source** can be verified by
sampling **two representative layouts** — the simplest (e.g. the Service Areas matrix) and the most complex (e.g.
the 13-city service hub). If both pass, the rest of that same-operation batch is high-confidence. If the hubs were
edited individually, verify each.

## Fallback

If Claude in Chrome is unavailable, ask the operator for an **incognito** screenshot of the simplest and most
complex hub. Incognito avoids the operator's own browser cache. The computed-style path is preferred because it's
self-service, exact, and doesn't put the verification back on the operator.

## What to record

In the review-pass marker / execution log, record the **actual computed-style values** returned, the **cache-buster
token used**, and which hubs were sampled. "Greps clean" or "looks styled" is not an acceptable record.
