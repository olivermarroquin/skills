---
type: source
source-type: video
status: extracted
created: 2026-04-28
ingested: 2026-04-28
published: 2026-04-15
title: "How to build a $10k/mo onboarding agent in 4 hours"
creator: "Example Creator"
url: "https://www.youtube.com/watch?v=EXAMPLE"
duration: "32:14"
category: monetization-workflow
tier: 1
relevance-score: 5
actionability-score: 5
monetization-potential: high
domains: [automation-systems, app-building, client-services]
tags: [source, video]
---

# Source: example creator — onboarding agent in 4 hours

> **Source URL:** https://www.youtube.com/watch?v=EXAMPLE
> **Why ingested:** Tier 1 — directly maps to the AI Factory's first revenue-producing offer

---

## One-paragraph takeaway
The creator builds a client-onboarding agent for SMB service businesses in one session using Claude Code, an Airtable backend, and a webhook layer. The pricing wedge is $2k setup + $500/mo, sold to coaches/consultants. The reusable pieces are the schema, the agent system prompt, and the deployment pattern — the niche is interchangeable.

## Main claim
You can productize a single agent into a $5k–$10k/mo recurring offer in a weekend if you sell a specific outcome to a specific niche.

## Problem being solved
SMB service providers lose 30%+ of inbound leads at the booking stage because intake is manual, slow, and inconsistent.

## Audience / use case
Coaches, consultants, agencies, service providers with 20–200 leads/month and no ops person.

## Key insights
- The agent isn't the product — the *configured workflow + schema + integration* is the product
- Niche specificity beats generality at this price point
- Deployment is mostly Airtable + a Claude API wrapper + 2 webhooks
- The buyer doesn't care about the agent, they care about the conversion lift

## Novelty assessment
- [ ] New idea
- [x] New combination of known ideas
- [ ] Repackaging of known idea
- [ ] Hype with little substance

---

## Tools mentioned

### Explicit
- [[tool-claude-code]]
- [[tool-airtable]]
- Make.com (webhook orchestration)

### Inferred
- Some kind of frontend for the form — probably Tally or Typeform, *inferred* from screen
- Stripe for billing — *inferred*, never shown

### Uncertain
- The "memory" claim — unclear if it's actual persistent memory or just session context

---

## Workflow breakdown

1. Define the niche and the outcome (15 min)
2. Build Airtable schema: leads, conversations, qualification fields (30 min)
3. Write the agent system prompt against the niche's known objections (45 min)
4. Wire form → Make.com → Claude API → Airtable (60 min)
5. Test end-to-end with 5 fake leads (45 min)
6. Package as a $2k setup with a 30-day handoff (productization step)

### Notable implementation details
- The system prompt embeds objection handling, not just info gathering
- Qualification scoring lives in Airtable, not in the prompt — keeps the prompt stable
- Make.com is used because the buyer can edit it; n8n was rejected for that reason

### Likely architecture
Form → webhook → Make.com scenario → Claude API call → Airtable write → conditional Slack notification → optional reply email.

---

## Strategy extraction

### Business strategy
- Niche-first packaging
- Productized service ($2k setup + $500/mo) instead of consulting
- Outcome-priced (conversion lift) not effort-priced

### Growth strategy
- Cold outreach to specific niche after first 2 case studies
- Demo video that shows the *result*, not the agent

### Automation strategy
- Stack chosen for buyer-editability, not power
- Schema-first design keeps the prompt thin

### Content strategy
- Build-in-public — same workflow as content topic

### Sales / offer strategy
- Sells a metric (lift) not a tool (agent)
- 30-day handoff = upsell to MRR

---

## Replication potential

### Directly copyable
- Schema structure
- The "objection-aware" system prompt pattern
- Make.com scenario layout

### Needs adaptation
- Niche-specific qualifying questions
- Pricing tier (varies by niche LTV)

### Likely fluff or non-reusable
- The "$10k/mo in 4 hours" framing — first one took weeks, not 4 hours

---

## Opportunities surfaced

### Product / SaaS ideas
- [[opportunity-vertical-onboarding-agent-for-coaches]]

### Client-service ideas
- [[opportunity-onboarding-agent-productized-service]]

### Internal tool / automation ideas
- Use the same schema for the AI Factory's own client intake

### Content ideas
- [[content-why-niche-onboarding-agents-beat-generic-ones]]

---

## Execution recommendation
- [x] Act now

**Reasoning:** This maps directly to a current revenue lane. The schema + prompt + Make.com scenario can be adapted to one of the existing client conversations within a week. Worst case: a reusable blueprint for the AI Factory.

---

## Confidence assessment
- High confidence: niche-first works, schema-first works, Make.com choice rationale
- Medium confidence: the specific $2k/$500 price point — depends on niche
- Low confidence / inferred: the "$10k/mo in 4 hours" claim
- Missing details: actual close rate from outreach, churn after month 1

---

## Extracted artifacts (created from this source)
- [[tactic-objection-aware-system-prompt]]
- [[tactic-schema-first-agent-design]]
- [[tactic-buyer-editability-as-stack-criterion]]
- [[opportunity-onboarding-agent-productized-service]]
- [[content-why-niche-onboarding-agents-beat-generic-ones]]
- [[tool-make-com]]

## Related sources
- 

## Pattern candidates
- "Niche productized agent" — if 2+ more sources show this, promote to pattern
- "Schema-first prompt design" — already seen elsewhere, candidate for pattern note
