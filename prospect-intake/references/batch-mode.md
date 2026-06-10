# Batch mode — triaging multiple prospects

Use when the operator hands over more than one lead at once and wants to know who's worth a call.

## Input shapes accepted

- A pasted list: one prospect per line, `Business Name, https://domain, source`.
- A CSV file path with headers `name,domain,source` (source optional).
- A loose paste of names + URLs — normalize it, then confirm the parsed list back as plain text
  before running.

## How to run

1. **Parse + confirm.** Echo the normalized list back (name → slug → domain → source) and the depth
   setting (default: light competitor pass per prospect). Wait for a go-ahead.
2. **Per prospect, run Phases 1–6** of the main skill. Each prospect is fully self-contained in its
   own `_prospects/<slug>/` folder — no shared state between them.
3. **One pipeline view.** Add every prospect as a row in `_prospect-pipeline.md`. This is the
   operator's at-a-glance funnel.
4. **Recommend a triage order.** After all rows are built, rank them for call priority on three
   axes and give a one-line rationale each:
   - **Fit** — in service area, right vertical, right size.
   - **Pain** — how fixable/severe the site + ranking gaps are (more pain = easier pitch).
   - **Winnability** — budget signals, no incumbent agency, owner reachable.
5. **Qualify out loud.** Explicitly flag any prospect that looks like a poor fit (dead site, out of
   area, no contact path, enterprise too big for the model) so the operator skips it. The value of
   batch mode is saving call time, not inflating the list.

## Performance / cost notes

- Light competitor pass keeps each prospect at ~15–20 min of research. A batch of 5–8 is reasonable
  in one run; larger batches should be chunked and the operator told the rough time.
- Don't silently upgrade any prospect to a full competitor-deep-research run — that's a deliberate,
  per-prospect decision the operator makes after triage.

## Output

A short ranked summary in chat (top-to-bottom call order + one-line rationale + any qualify-outs),
plus the populated pipeline table. Folders are the durable artifact; the chat summary is the
decision aid.
