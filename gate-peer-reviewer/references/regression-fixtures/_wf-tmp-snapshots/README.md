---
type: reference
created: 2026-06-16
purpose: Snapshots of the .wf-tmp final-good states from the COA-4b site-capture-engine build
---

# COA-4b .wf-tmp snapshots (committed evidence)

These are snapshots of the `.wf-tmp/` final-good states from the COA-4b build,
copied here BEFORE any cleanup could remove them. The `.wf-tmp/` directory is
ephemeral and not committed; these snapshots are the committed evidence that the
clean fixture states are grounded in real capture output, not purely synthetic.

## What's here

- `ev-capture-test/` — EV Electric 43-page teardown context capture (manifest + structural JSONs)
- `ev-restore-test/` — EV Electric restoration context capture (manifest + structural JSONs + wp-export/)
- `aj-long-regression/` — AJ Long 1,014-page regression teardown (manifest + structural JSONs)

## What's NOT here (too large for git)

- `html/`, `meta/`, `singlefile/`, `assets/`, `extracted-sample/` — the actual captured HTML/media
  (hundreds of MB). The manifests + structural JSONs are sufficient to prove the capture ran and
  produced the expected counts/structures. The full captures exist in `.wf-tmp/` on the host.

## Relationship to fixtures

The `coa4b-*` fixtures use synthetic reconstructions for both defect and clean states.
These snapshots provide the ground-truth reference for the clean states — a future
reviewer can diff `coa4b-c12/clean/` against `ev-capture-test/capture-manifest.json`
to verify the fixture's font count matches the real capture.
