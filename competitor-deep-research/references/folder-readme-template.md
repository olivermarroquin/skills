# Folder _README.md template

When creating the `competitor-research/` subfolder for a new client, write this `_README.md` inside it. Also update the parent folder's `_README.md` to list the new child, per the vault stewardship principle that subfolder creation and README maintenance are one atomic action.

---

```markdown
---
type: folder-readme
status: canonical
created: YYYY-MM-DD
updated: YYYY-MM-DD
client: <client-slug>
tags: [folder-readme, client-ops, <client-slug>, competitor-research]
---

# competitor-research — competitive intelligence briefs

External competitive-intelligence research on direct competitors in <client>'s <geography> <industry> market. Feeds the page-build, Core 30, and SEO foundation strategy.

## What goes here

- One markdown brief per competitor, named `<competitor-slug>.md` (e.g., `aj-long-electric.md`)
- Cross-competitor synthesis files named `synthesis-YYYY-MM-DD.md`
- Optional: raw page captures, screenshots, or saved-source artifacts useful for re-audit comparison

## Standard brief template (sections)

1. Identity & positioning
2. Tech stack
3. Content structure
4. SEO signals
5. Reviews / social proof
6. Backlink hints
7. What's working
8. What's NOT working
9. Sources audited

Full template lives in the `competitor-deep-research` skill at `~/workspace/skills/competitor-deep-research/references/per-competitor-brief-template.md`.

## Current briefs

- [[<competitor-slug-1>]] — primary
- [[<competitor-slug-2>]] — primary
- [[<competitor-slug-3>]] — secondary
- [[<competitor-slug-4>]] — secondary
- [[synthesis-YYYY-MM-DD]] — cross-competitor patterns + Core 30 recommendations

## Refresh cadence

Recommended: re-audit primary competitors quarterly; re-audit secondaries every 6 months. Trigger an off-cycle re-audit when the client launches major site changes (so the post-launch competitive picture is on record before competitors react).

## Parent

- [[../_README|admin-extracts folder]]
- [[../../README|<client> project README]]
```

---

## Parent _README.md update pattern

If the parent folder's `_README.md` has a "Subfolders" section, add a line for the new child. If it doesn't have one, add a "Subfolders" section.

Example (from EV Electric's `admin-extracts/_README.md`):

```markdown
## Subfolders

- `analytics/` — GA4 exports, performance reports
- `competitor-research/` — competitive intelligence briefs (added YYYY-MM-DD)
- `google-business-profile/` — GBP baselines, audits, BrightLocal scans
- ...
```

Bump the parent's `updated:` frontmatter date so future audits can see when the subfolder was added.
