---
type: folder-quality-log
status: active
created: 2026-05-28
last-updated: 2026-05-28
artifacts-tracked: 1
shipped: 0
iterating: 0
escalated: 0
tags: [folder-quality-log, quality-loop, regression-test]
---

# Quality log — output-quality-loop/regression-tests/

This file tracks evaluations on the regression-test artifacts used to validate output-quality-loop v1.

The artifacts in this folder are intentionally constructed (one deliberately broken) to verify the skill produces expected verdicts. Not for production use.

---

## broken-brief-for-fail-test

**Latest:** FAIL (2026-05-28) — iteration 1 of 3

### Iteration 1 — 2026-05-28 (regression test)

**Artifact type:** research brief (service tier) — inferred from the artifact's claim to be a brief for "Electrical Panel Upgrades," though the file lacks the type-detection signals to confirm cleanly.

**Spec sources loaded:**
- `~/workspace/second-brain/05_shared-intelligence/research-briefs/_template-service-brief.md`
- The brief template's consumption-contract table (§ "How the scaffolder consumes this brief")
- `~/workspace/second-brain/_meta/plain-language-conventions.md`

**Verdict:** FAIL

#### Hard requirements

- [✗] Frontmatter present and well-formed — **the file has no frontmatter at all**. Missing every required field: `type: research-brief`, `brief-tier: service`, `status:`, `service-slug:`, `domain:`, `research-date:`, `researcher:`, `tools-used:`, `sources-cited:`, `tags:` (spec source: `_template-service-brief.md` frontmatter shape)
- [✗] Required sections all present — file has 4 narrow sections (Service Identity, Some SEO Stuff, FAQ, Conclusion). Missing: §2 Top-10 SERP analysis, §3 Keyword and question targets — Google search, §4 Keyword and question targets — AI search, §4.5 AI-citation hardening checklist, §5 Schema patterns, §6 Content depth norms, §7 FAQ patterns, §8 Image-style observations, §9 Internal-linking observations, §10 Problem and process patterns, §11 Pricing-visibility norms, §12 Trust and authority signal norms, §13 Competitive moat assessment, §14 Sources cited, §15 Methodology (spec source: `_template-service-brief.md` § 1-15)
- [✗] Inline citations in the required `[source: <tool/url> on YYYY-MM-DD]` format — **zero citations in the body**. Statistics are claimed without sources ("95% of users click the first result," "67% of homes need a panel upgrade," "average cost is between $0 and $1000000") (spec source: template § citation discipline)
- [✗] Sources-cited roll-up at §14 — section does not exist
- [✗] Methodology section at §15 — section does not exist
- [✗] Consumption-contract table at the end — does not exist; the brief cannot feed `scaffold-service-data.py` in its current shape

5 of 6 hard requirements missed. A single hard-requirement miss is sufficient cause for FAIL.

#### Quality dimensions

Not scored individually because the artifact failed at the hard-requirement floor. For completeness:

- [✗] Citation density: 0 inline citations vs. template expectation of 10+ (FAIL)
- [✗] Distinct sources cited: 0 vs. expectation of 5+ for service briefs (FAIL)
- [✗] AI-citation hardening checklist (§4.5) — does not exist (FAIL)
- [✗] Plain-language compliance — body is jargon-dense ("synergistic capabilities operationalize end-to-end customer journeys," "user-intent paradigm necessitates a holistic content strategy," "omnichannel touchpoints," "dispositive"); no glossing; sentences are corporate-formal whitepaper voice rather than conversational. Direct contradiction of `plain-language-conventions.md` (FAIL)
- [✗] Consumption contract honored — no contract to honor; the brief shape doesn't match the template (FAIL)

Quality dimension score: 0/5 = 0%. Below the 50% FAIL threshold.

#### Discipline rules

- [✗] Honest about gaps — the brief makes load-bearing factual claims ("95%," "67%," "$0 to $1000000" cost range) without any source. The cost range "between $0 and $1000000" is functionally a refusal to commit to a real range, dressed as a claim. (SEVERE — fabricated-or-meaningless-data violation)
- [✗] Plain-language compliance — see above
- [✗] No AI-generated content at scale — the prose has the hallmarks of unedited AI-generated boilerplate ("synergistic," "holistic," "leverages") per the SEO primer §G anti-tactics
- [✓] Non-destructive on neighbor artifacts — the broken brief doesn't claim to replace anything (the one rule it doesn't violate)

3 discipline-rule violations, including 1 severe (fabricated/meaningless data).

#### Root cause

The artifact is not a research brief in any meaningful sense. It carries the surface shape of "a document that talks about panel upgrades" but none of the structural, evidentiary, or discipline requirements that define a service brief in this Knowledge OS. Specifically:

1. **Frontmatter is missing entirely**, which means the artifact is invisible to every Dataview query the vault depends on (Phase 1 detection only worked because the file is inside a path explicitly named in the regression test, not because the artifact identifies itself).
2. **Section structure is unrelated to the template**, which means the consumption contract with `scaffold-service-data.py` is broken and the brief cannot feed the downstream pipeline.
3. **No citations**, which means every claim is unverifiable and the artifact would be filtered out at the "fabricated citation" discipline rule even if the rest were sound.
4. **AI-slop prose** matches the anti-tactics the SEO primer §G explicitly flags as content that won't earn AI citations.

The producing chat (or operator, if hand-authored) would need to regenerate from scratch, following the `_template-service-brief.md` shape, with actual research behind every claim. Surface edits won't recover this artifact.

#### Suggested fixes

Cannot be repaired by targeted edits. Regeneration required. Recommended path:

1. **Regenerate from the template.** Start with `_template-service-brief.md` and fill each of the 15 sections per the template's "What this feeds" annotations. Frontmatter is the first edit; if frontmatter is missing the rest doesn't matter.
2. **Drive the research via the `service-seo-research` skill.** It produces briefs in the right shape and honors the citation discipline by construction.
3. **Run perplexity-refinement on the regenerated brief.** Closes any AI-search surface gaps the skill produces.
4. **Re-evaluate via output-quality-loop after regeneration.** Verdict should land at NEEDS REVISION (minor or substantive) or PASS depending on how the research pass goes; FAIL again means the regeneration also went wrong.

Iteration budget: this is iteration 1 of 3. The artifact will be re-evaluated after regeneration. If iteration 3 still doesn't reach PASS, the loop escalates.

#### Calibration note

The handoff named this regression test as "should land FAIL with specific diagnosis." The skill's verdict (FAIL) matches. The diagnostic specifically names: missing frontmatter, missing section structure, zero citations, AI-slop prose, fabricated/meaningless data. Heuristics calibration confirmed for the FAIL path.

---
