# Domain signal mining

How SURVEY walks `03_domains/` to surface unsynthesized sources, unpromoted patterns, and lesson candidates. The walking is read-only; the orchestrator never edits domain content or auto-routes signals.

## What's in scope

The orchestrator surfaces three kinds of domain signals:

1. **Unsynthesized sources** — VIS-extracted source notes in `03_domains/<domain>/insights/` (or equivalent) that don't yet appear in any cluster synthesis or pattern document.
2. **Unpromoted lessons** — `lesson-*.md` files with `status: draft` or `status: candidate` in `05_shared-intelligence/lessons/` that map to a domain.
3. **Patterns ready for promotion** — `pattern-*.md` files in `05_shared-intelligence/patterns/` with `times-observed: 3+` but `status:` not yet `promoted`.

The signal is surfaced as a count + plain-language description. The operator decides whether to spawn a synthesis chat, a promotion chat, or an intel-routing pass.

## Domain folder structure (as of 2026-06-01)

`03_domains/` contains 10 domains:

- `ai`
- `app-building`
- `automation-systems`
- `client-services`
- `content-systems`
- `marketing`
- `personal-development`
- `seo`
- `video-intelligence`
- `website-design`

Each domain follows a similar layout (canonical: `seo/`):

```
03_domains/<domain>/
├── _README.md
├── _quality-log.md
├── primer.md
├── primer-readings/
├── insights/            # VIS-extracted source notes + cluster syntheses
│   ├── _README.md
│   ├── _quality-log.md
│   ├── source-YYYY-MM-DD-<creator>-<topic>.md
│   ├── cluster-synthesis-<theme>-YYYY-MM-DD.md
│   └── cluster-synthesis-<theme>-YYYY-MM-DD-plain.md
├── lessons/             # domain-scoped lesson candidates
├── tactics/             # domain-scoped tactics
├── tools/               # tools-as-notes
├── platforms/           # platform notes
└── ...
```

Not every domain has every subfolder. The walking logic checks for presence before scanning.

## Signal 1 — Unsynthesized sources

### Detection

For each domain:

1. List `<domain>/insights/source-*.md` (or equivalent VIS-extracted source notes).
2. List `<domain>/insights/cluster-synthesis-*.md` (the synthesis-class artifacts).
3. For each source note, check if its slug or filename appears in any cluster synthesis (grep the synthesis bodies + the synthesis "Sources" sections).
4. If the source is not referenced in any synthesis AND it's >7 days old AND there's no draft synthesis claiming to cover it, count as `unsynthesized`.

The 7-day threshold prevents noise from very-recent sources that haven't had time to get synthesized yet.

### What to surface

Per domain, surface: `N unsynthesized sources in <domain>` with the source slugs and one-line "could feed" description.

Example surface:

> `seo` has 4 unsynthesized sources from the past 14 days: Jono Catliff (50K-clicks masterclass), Nico (AI ranking explained), Vasco (Claude builds backlinks), Caleb Ulku (Google broke SEO). Could feed a Phase 2-style cluster synthesis or get routed via intel-routing PUSH against the SEO inboxes.

### Threshold for "worth surfacing"

If a domain has 0-1 unsynthesized sources, don't surface — that's normal background noise. Surface when count ≥2.

### Edge cases

- **Source note that's a single capture (no synthesis intent).** Some sources are quick captures meant for reference, not synthesis. Detect via the source's frontmatter (`type: source-note` + `tags: [capture]` or `synthesis-intent: none`). Exclude from the count.
- **Source already routed via intel-routing.** If the source appears in any project's `_inbox-keeps/` (sign of routing without synthesis), exclude from "unsynthesized" — it was triaged. Surface separately as "routed but not synthesized" if the operator wants that level of detail (default: don't).

## Signal 2 — Unpromoted lessons

### Detection

For each domain:

1. List `05_shared-intelligence/lessons/lesson-*.md` filtered by `tags:` containing the domain.
2. Parse each lesson's frontmatter `status:`.
3. Count lessons with `status: draft` or `status: candidate`.

If the domain has its own `lessons/` subfolder (`03_domains/<domain>/lessons/`), check there too.

### What to surface

Per domain, surface: `M draft lessons in <domain>` with the lesson slugs and one-line "what generalizes" description.

Example surface:

> `automation-systems` has 2 draft lessons: `lesson-auto-invoke-retrofit` (the convention-rollout pattern from output-quality-loop Phase 5) and `lesson-two-file-artifact-split` (human + machine companions from vault-orchestrator Phase 1). Both are candidates for promotion to `status: promoted` if they generalize past their first observation.

### Threshold for "worth surfacing"

Always surface when count ≥1. Lessons that sit at `draft` for a long time are signal worth not losing.

### Edge cases

- **Lesson without a domain tag.** Surface in a "domain unassigned" subsection rather than dropping. Operator may add the tag.
- **Lesson with `status: promoted` but no second-observation note.** Not a draft, technically — but if the promotion was over a year ago and never gathered a second observation, surface as "promoted but stale" only if the operator asks for that level of detail (default: don't).

## Signal 3 — Patterns ready for promotion

### Detection

For each pattern in `05_shared-intelligence/patterns/pattern-*.md`:

1. Parse frontmatter `times-observed:` and `status:`.
2. Count patterns with `times-observed: >= 3` AND `status:` not in `[promoted, archived]`.

Patterns at 3+ observations are eligible for promotion per the standard knowledge-promotion workflow.

### What to surface

Per domain (or vault-wide for cross-domain patterns), surface: `K patterns ready for promotion in <domain>` with the pattern slugs.

Example surface:

> `content-systems` has 1 pattern ready for promotion: `pattern-intel-routing-five-field-convention` (4 observations across EV, S&H, vault-orchestrator).

### Threshold for "worth surfacing"

Always surface when count ≥1. The promotion-ready signal is the whole point.

### Edge cases

- **Pattern at `times-observed: 3` but with stale `updated:` (>60 days).** Surface with annotation "pattern at 3 observations but stale — verify before promoting."
- **Pattern at `times-observed: 5+` but still draft.** Surface with annotation "long overdue for promotion." This is a sign the promotion workflow stalled.

## Cross-domain signals

Some signals span domains:

- A source note in `seo/insights/` that also tags `marketing` and `ai`.
- A pattern that applies to `automation-systems` AND `app-building`.

When walking, attribute multi-domain signals to all named domains. If the operator wants to deduplicate, the report can group cross-domain signals in a separate subsection — but the default is to count them per-domain so the per-domain rollups stay honest.

## Reporting voice

Domain signals in SURVEY Section 7 follow the section-shape rules:

- Per-domain row when the domain has any signal
- Plain-language description of what acting on the signal would look like
- Counts always honest ("4 unsynthesized" not "several unsynthesized")
- Wikilinks to specific source or pattern files

The operator should be able to scan Section 7 and see at a glance: "SEO domain is hot, automation-systems has accumulated lesson candidates, content-systems has a pattern ready."

## What domain-signal-mining does NOT do

- **It does not auto-route sources.** Intel-routing is its own skill with PUSH/PULL/BOOTSTRAP modes. The orchestrator surfaces "X sources unrouted" as a signal; the operator decides.
- **It does not auto-promote patterns.** The promotion workflow is operator-driven per `05_shared-intelligence/workflows/workflow-knowledge-promotion.md`.
- **It does not auto-synthesize.** `multi-source-synthesis` is its own skill. The orchestrator surfaces "domain ready for synthesis"; the operator decides.

## See also

- `~/workspace/skills/vault-orchestrator/SKILL.md` § Mode 1 Step 3 — runtime behavior
- `./survey-section-shapes.md` § Section 7 — Domain signals — output shape
- `~/workspace/skills/intel-routing/SKILL.md` — composes with the surfaced signals
- `~/workspace/skills/multi-source-synthesis/SKILL.md` — what runs when synthesis is acted on
- `~/workspace/second-brain/05_shared-intelligence/workflows/workflow-knowledge-promotion.md` — promotion workflow
