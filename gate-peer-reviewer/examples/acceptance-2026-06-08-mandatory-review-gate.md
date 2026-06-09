---
type: acceptance-test
skill: gate-peer-reviewer
gate: mandatory-review-gate
created: 2026-06-08
updated: 2026-06-09
tags: [acceptance-test, review-gate, hooks]
---

# Acceptance tests: Mandatory pre-land review gate (2026-06-08, rev 2)

Real script invocation output for each acceptance criterion. All tests invoke the
actual `mandatory-review-gate.py` / `dirty-ledger-track.py` / `log-review-pass.py`
scripts, not a simulated harness. Rev 2 replaces the original evidence file which
documented bug D-11 (invalid hookSpecificOutput on approve path) as a passing test.

## Test A: Approve path — schema-valid clean stop (no dirty entries)

Invoke `mandatory-review-gate.py` with an empty session (no dirty ledger).

```
exit_code: 0
stdout: {"continue": true}
```

**Validation:** Valid JSON. No `hookSpecificOutput` key (not valid for Stop events).
`continue: true` only. Exit 0.

**VERDICT: PASS**

## Test B: Approve path — all dirty files reviewed

Write a file → log review pass → invoke `mandatory-review-gate.py`.

```
exit_code: 0
stdout: {"continue": true}
```

**Validation:** Same schema as Test A. No `hookSpecificOutput`. Exit 0.

**VERDICT: PASS**

## Test C: Block path — unreviewed file blocks stop

Write a file → attempt stop without review.

```
exit_code: 2
stderr: MANDATORY PRE-LAND REVIEW GATE — BLOCKED

1 unreviewed artifact(s) detected. Review tier: full.

Unreviewed:
  - /private/tmp/rt-c-test.md  (tool: Write, tier: full)

REQUIRED ACTION before you can stop:
...
```

**Validation:** Exit 2. Stderr contains block message with file path and review instructions.

**VERDICT: PASS**

## Test D: Read-only exempt — cd && git status leaves zero dirty entries

Track `cd ~/workspace/second-brain && git status` as a Bash tool call.

```
Dirty ledger exists: False
Stop exit_code: 0
```

**Validation:** No dirty ledger file created at all. Stop passes immediately (no entries to check).

**VERDICT: PASS**

## Test E: Boilerplate evidence rejected (anti-gaming)

```
"all checks passed." → exit=1
  stderr: [review-gate] REJECTED: Evidence too short (18 chars, need >=50).

"gate-peer-reviewer: [summary of checks run and findings]; output-quality-loop: [verdict]"
  → exit=1
  stderr: [review-gate] REJECTED: Evidence matches boilerplate pattern.
```

**Validation:** Both boilerplate strings rejected (exit 1). Template text from the block
message itself is caught. Real evidence with named check keywords (50+ chars) accepted
(verified in Test F).

**VERDICT: PASS**

## Test F: BASH entry clears end-to-end (deadlock fix)

Track a Bash command with quotes in it: `CORE30="/workspace" && python3 publish.py --client ev`

```
BASH key: BASH:80c286dc0ccd
Key is argv-safe: True (no quotes in key)

Stop before review: exit=2 (blocked)
[review pass logged with exact BASH:80c286dc0ccd key]
Stop after review: exit=0

Approve JSON: {"continue": true}
Has hookSpecificOutput: False
```

**Validation:** Hash-only key round-trips through argv without quote escaping issues.
Blocks before review, clears after. Approve JSON is schema-valid.

**VERDICT: PASS**

## Test G: Meta-description regression replay

Edit an HTML file changing meta description from Fairfax to Vienna (simulating the
cross-surface meta-description regression that shipped unreviewed in a client session).

```
Stop blocks unreviewed edit: exit=2
Block message mentions the file: True

[BLOCKING review logged with findings:
  "Meta description city mismatch: body=Fairfax but meta description changed to Vienna.
   og:description still says Fairfax. Cross-surface inconsistency."]

Stop after BLOCKING review: exit=0 (findings surfaced, gate clears)
```

**Validation:** The edit is tracked. Stop blocks until review runs. The reviewer catches
the city mismatch (value-cross-check) and logs BLOCKING with specific findings. BLOCKING
clears the gate because the point is catching-before-land, not blocking forever — the
findings are surfaced to the operator.

**VERDICT: PASS**

---

## Summary

| Test | What it proves | Result |
|---|---|---|
| A | Approve path emits valid Stop JSON (`{"continue": true}`, no hookSpecificOutput) | PASS |
| B | Approve path works after dirty→reviewed cycle | PASS |
| C | Block path exits 2 with review instructions | PASS |
| D | Read-only Bash (cd && git status) creates zero dirty entries | PASS |
| E | Boilerplate evidence rejected by anti-gaming filter | PASS |
| F | BASH hash-only key round-trips through argv, clears end-to-end | PASS |
| G | Meta-description regression caught by the gate before landing | PASS |

All 7 tests PASS against the real scripts. Rev 2 supersedes the original evidence file
which documented bug D-11 (hookSpecificOutput on Stop approve path) as a passing test.
