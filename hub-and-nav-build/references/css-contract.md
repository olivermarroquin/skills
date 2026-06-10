# Reference: The hub `<style>` CSS Contract

> The single most important file in this skill. The 2026-06-09 EV hub build broke **three times** on this exact
> issue. Read it, and treat the render gate (`verification-gate.md`) as the only proof it held.

## Why hub pages have an inline `<style>` block at all

Hub pages reuse the leaf design system (`evp-corepage`): the `Inter` font stack, the `.evp-hero` blue gradient,
button styles, section layout, and the `.evp-city-card` grid. That CSS ships **inside the page's injected HTML** as
a `<style>` block (wrapped in `wp:html` so WordPress doesn't mangle it). Hub pages then add a few rules on top —
the city-card grid spacing, the service×city matrix table, the check-list — but those additions are **a thin layer
over the full base CSS, not a substitute for it.**

## The contract

A correct hub `<style>` block is approximately:

```
~18,873 chars  base leaf CSS (the full evp-corepage system)
+  ~1,972 chars  hub-specific additions (city grid / matrix / check-list)
= ~20,845 chars total, with 167 balanced braces
```

These are the **EV reference numbers**. They track the **design system**, not the client — re-measure against the
target client's canonical leaf before asserting them for a new client. What's invariant is the **shape**: base CSS
dominates (~90% of the bytes); the hub additions are a small tail.

## How to build a hub `<style>` block correctly

1. Pick a **known-good leaf** for the client — a page you have render-confirmed is styled correctly. (EV:
   `ev-charger-mclean-va`, WP ID 6330.)
2. Extract that leaf's **entire** `<style>` block. That is your base CSS. Do not hand-author or trim it.
3. Append the hub-specific additions (grid/matrix/check-list rules).
4. Wrap the whole thing for injection (`wp:html`), set the hub body markup, publish.
5. **Validate three ways** (all required):
   - **byte count** within ~5% of the leaf's `<style>` block,
   - **balanced braces** (`{` count == `}` count),
   - **render-verify** per `verification-gate.md`.

## The failure mode (memorize this)

What happened on EV: a round of edits to hide the theme's title banner **injected** CSS into the hub `<style>`
blocks. A later "revert" **removed** that injected CSS — but the removal logic stripped the **entire base CSS**
along with it, dropping each block from ~19K chars to ~2K (only the hub additions survived).

The trap: **the braces stayed balanced.** Every structural check — byte-balance, JSON parse, brace count — passed.
The HTML still *contained* strings like `gradient`, `Inter`, and the button classes (in the surviving additions and
in element class attributes). So two consecutive automated reports said **"all 7 hubs styled."** They were
HTML-string false-passes.

What the page actually did: rendered in **serif fallback** (no `Inter`), **no hero gradient** (the `.evp-hero` rule
was gone), **plain-text buttons** (button rules gone). The operator caught it by eye in incognito; `getComputedStyle`
confirmed it precisely. The fix was to restore the full leaf CSS + the additions — back to ~20.8K chars / 167 braces.

## Rules that fall out of this

- **Never inject or remove a partial CSS edit into a hub's content `<style>` block** to achieve a template-level
  effect. If you need to hide a title banner, change the page template / page-settings, not the content CSS.
- **A balanced-brace / byte-count check is necessary but NOT sufficient.** It cannot distinguish "full CSS" from
  "only the additions survived." Pair it with the computed-style render gate, always.
- **A styled page with an unwanted cosmetic flaw beats a cosmetically-perfect page that doesn't render.** When a
  cosmetic fix risks the design system, stop and leave the cosmetic issue; surface it to the operator.
- **When restoring, prefer the known-good leaf's CSS as the source of truth** over trying to reconstruct what was
  stripped.

## Quick diagnostic

If a hub looks unstyled, before anything else compare its `<style>` block size to the canonical leaf's:

```python
# pseudo: extract <style> from hub HTML and from leaf HTML, compare lengths + brace balance
hub_css   = extract_style_block(hub_html)
leaf_css  = extract_style_block(leaf_html)
print(len(hub_css), hub_css.count('{'), hub_css.count('}'))
print(len(leaf_css), leaf_css.count('{'), leaf_css.count('}'))
# A hub block dramatically smaller than the leaf block = base CSS was stripped. Restore from leaf.
```

A hub block that is a small fraction of the leaf block = base CSS stripped → restore from the leaf, then re-run the
render gate.
