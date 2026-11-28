---
type: registry
status: active
created: 2026-11-03
purpose: "Which skills live in labs, where each was born (the master), and every sync done. Rules are in skills-sync/SKILL.md. The general registry for main-vault skills is _sync-registry.md."
tags: [registry, skills, labs, sync]
---

# Lab skill registry

How to read: **Master** is the copy that wins. **Copies** get updated from it. Run `python3 /Users/olivermarroquin/workspace/skills/skills-sync/scripts/skill-sync.py status` to see if copies still match.

## Skills that live in labs

| Skill | Master | Copies | Relation to the main-vault skill | Notes |
|---|---|---|---|---|
| vis-extraction-lite | ai-online-business-lab | ai-marketing-lab, _starter-vault | Lite sibling of `vis-extraction`. Not a file copy: improvements to the real VIS are carried over by hand. | Version 2.0-lab. Identical in all three places since 2026-11-27 (the example line now says `<lab-name>` everywhere). |
| gate-peer-reviewer-lite | ai-online-business-lab | ai-marketing-lab, _starter-vault | Lite sibling of `gate-peer-reviewer` | Version 2.0-lab. Identical in all three places. |
| output-quality-loop-lite | ai-online-business-lab | ai-marketing-lab, _starter-vault | Lite sibling of `output-quality-loop` | Version 2.0-lab. Identical in all three places. |

## Sync log
- 2026-11-03: system created. skills-sync skill and script built and tested (blocks key files, written-out keys, vault paths and private names; dry run by default; keeps the old copy in _sync-backups outside the lab). First status run: 3 lab skills, 1 expected difference.
- 2026-11-27: Lab skills 2.0 (parity) landed. Built in /Users/olivermarroquin/workspace/shared-brains/_skills-staging/ai-online-business-lab/, copied staging to ai-online-business-lab (master), then from the master to ai-marketing-lab and _starter-vault. Status run after the copies: all three fingerprints match for all three skills. Merged: https://github.com/keelworks-hq/ai-online-business-lab/pull/13 , https://github.com/keelworks-hq/ai-marketing-lab/pull/10 , https://github.com/keelworks-hq/lab-starter/pull/4 . Old copies are in /Users/olivermarroquin/workspace/skills/_sync-backups/ (9 folders dated 20261127), safe to delete once checked.

## Still to do
- Stage 2 lite skills (second-squeeze, multi-source-synthesis, plain-language-translation, step-by-step-walkthrough, Perplexity step): when built, add rows here.
- Cowork packaging for Samira (plugin) is separate and not part of this registry yet.
