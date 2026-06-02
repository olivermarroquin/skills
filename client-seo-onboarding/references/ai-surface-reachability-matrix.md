---
type: reference
status: v1.1
created: 2026-06-02
updated: 2026-06-02
skill: client-seo-onboarding
source-of-truth: ~/Library/Application Support/Claude/local-agent-mode-sessions/.../memory/reference_ai_surface_reachability_from_cowork.md
tags: [skill-reference, ai-surface-reachability, perplexity-sonar, openai, gemini, anthropic-claude, ai-overviews]
---

# AI-surface reachability matrix

Skill-local mirror of the canonical reachability state. Step 2 of the orchestrator reads this file at runtime to surface the current AI-surface state to the operator before any research sub-skill fires.

## Source of truth

**The canonical source is the memory file:** `reference_ai_surface_reachability_from_cowork.md`.

This file is a **skill-local mirror** for runtime discoverability. When adding new AI surfaces or changing the status of existing ones:

1. **Update the memory FIRST** (it's the authoritative version that other skills + future chats consult)
2. **Then re-sync this mirror** (so this skill's Step 2 surfaces the same state)

Drift between this file and the memory is a known risk. If the two disagree, the memory wins. The orchestrator's Step 2 also reads the memory directly when it's running; this file is the human-readable in-skill version.

## Current matrix (2026-06-02)

| Surface | Endpoint reachable from Cowork sandbox? | Key wired? | Wrapper script | Current status |
|---|---|---|---|---|
| Perplexity Sonar API | YES (`api.perplexity.ai`) | Yes — `automation/secrets/perplexity-sonar.key` | `automation/scripts/perplexity_sonar.py` | **Working today.** Default model `sonar-pro`. Cost ~$0.005-$0.02/query. |
| OpenAI API (gpt-4o) | YES (`api.openai.com`) | Yes — `automation/secrets/openai.key` | `automation/scripts/openai_query.py` | **Working today.** Default model `gpt-4o`. Wired 2026-06-02. |
| Gemini API | YES (`generativelanguage.googleapis.com`) | Yes — `automation/secrets/gemini.key` | `automation/scripts/gemini_query.py` | **Working today.** Default model `gemini-2.5-flash` (free-tier-friendly; `gemini-2.0-flash-exp` retired). Wired 2026-06-02. |
| Anthropic Claude API | YES (`api.anthropic.com`) | Yes — `automation/secrets/anthropic-claude.key` | `automation/scripts/claude_query.py` | **Working today.** Default model `claude-sonnet-4-6`. Wired 2026-06-02. |
| Google AI Overviews | NO direct API; browser-only | N/A | Claude in Chrome (`mcp__Claude_in_Chrome__navigate` + `mcp__Claude_in_Chrome__get_page_text`) | **Working via Chrome.** Tools listed as deferred; load via ToolSearch before use. |
| ChatGPT web UI | Same — browser-only | Login required | Claude in Chrome | Use only if API doesn't cover the use case. |
| Perplexity web UI | Same — browser-only | N/A | n/a | **Don't use.** Sonar API supersedes for all use cases. |

## Path resolution (Mac Terminal vs Cowork sandbox)

The wrapper scripts auto-detect context:

- **Mac Terminal:** `~/workspace/second-brain-tier3/automation/scripts/<service>.py`
- **Cowork sandbox:** `~/mnt/workspace/second-brain-tier3/automation/scripts/<service>.py`

The scripts handle both paths transparently. No operator action needed beyond invoking the right script name.

## Step 2 surface message

When Step 2 fires the reachability check, it surfaces a message in this shape to the operator:

```
AI surfaces for this run:
- Perplexity Sonar — working (tier-3 wrapper)
- OpenAI gpt-4o — working (tier-3 wrapper)
- Gemini gemini-2.5-flash — working (tier-3 wrapper)
- Anthropic claude-sonnet-4-6 — working (tier-3 wrapper)
- Google AI Overviews — via Claude in Chrome (load via ToolSearch)

Per-brief §4 (AI-search question mining) backfills via these surfaces inline. Any FAIL on §4 with a "surface unreachable" framing is a bug, not a legitimate gap. Only legitimate deferral language: "operator declined to provide key" — which doesn't apply post-2026-06-02 since all keys are wired.
```

## Plain-language rule (load-bearing)

**NEVER use "blocked from Cowork" framing.** Replace with concrete path naming:

- ❌ "Perplexity is blocked from Cowork"
- ✅ "Perplexity reached via Sonar API at tier-3 carve-out (`perplexity_sonar.py`)"

- ❌ "OpenAI can't be reached from sandbox"
- ✅ "OpenAI gpt-4o reached via tier-3 wrapper (`openai_query.py`)"

- ❌ "Gemini unavailable"
- ✅ "Gemini gemini-2.5-flash reached via tier-3 wrapper (`gemini_query.py`)"

If a surface is genuinely down (rare — endpoint outage), name the outage explicitly + estimated restoration: "OpenAI endpoint returning 503 since HH:MM; retry after HH:MM."

## Verification protocol (re-run quarterly or when reachability is questioned)

```bash
# Quick endpoint reachability test (no key needed; just confirms TCP + TLS + HTTP works)
curl -sSI https://api.perplexity.ai/ -o /dev/null -w "%{http_code}\n"
curl -sSI https://api.openai.com/v1/models -o /dev/null -w "%{http_code}\n"
curl -sSI https://generativelanguage.googleapis.com/v1beta/models -o /dev/null -w "%{http_code}\n"
curl -sSI https://api.anthropic.com/v1/messages -o /dev/null -w "%{http_code}\n"

# Working-end-to-end test (uses the wrappers; counts against quota; ~$0.001 total)
python3 ~/mnt/workspace/second-brain-tier3/automation/scripts/perplexity_sonar.py "what is 2+2"
python3 ~/mnt/workspace/second-brain-tier3/automation/scripts/openai_query.py "what is 2+2"
python3 ~/mnt/workspace/second-brain-tier3/automation/scripts/gemini_query.py "what is 2+2"
python3 ~/mnt/workspace/second-brain-tier3/automation/scripts/claude_query.py "what is 2+2"
```

Any `404` / `401` / `403` on the endpoint test = endpoint reachable (the auth or path is wrong; the network works). Any timeout or `000` = real reachability problem.

## Update history

| Date | Change | Trigger |
|---|---|---|
| 2026-06-02 | Initial mirror created from `reference_ai_surface_reachability_from_cowork.md`; all 4 API surfaces marked working | v1.1 ship + API keys handoff closure (same day) |

## Related

- `reference_ai_surface_reachability_from_cowork.md` — **source of truth** (memory file)
- [[SKILL]] — Step 2 reads this matrix at runtime
- [[../../../second-brain/_meta/handoffs/handoff-2026-06-01-openai-gemini-claude-api-keys-tier3-wiring|API keys handoff (consumed 2026-06-02)]]
