---
type: source
source-type: video
status: ingested
created: <% tp.date.now("YYYY-MM-DD") %>
ingested: <% tp.date.now("YYYY-MM-DD") %>
published: ""
title: ""
creator: ""
url: ""
duration: ""
category: ""
tier: 
relevance-score: 
actionability-score: 
monetization-potential: 
chunked: false
segment-count: 1
attention-mode: single-pass
domains: []
relevant-projects: []
relevant-domains: []
tags: [source, video]
---

# <% tp.file.title.replace(/^source-/, "").replace(/-/g, " ") %>

> **Source URL:** 
> **Why ingested:** 

---

## Take-away
*(1-3 paragraphs, dense and specific. The reader should understand the source's core value from this alone.)*



### In plain English
*(1-3 sentences. Translate the jargon. Imagine explaining the gist to a thoughtful operator who isn't a specialist in this subdomain. State the thing — no "this section discusses..." meta-language.)*



---

## In plain English
*(3-5 sentences. The fastest possible comprehension surface — a reader should understand the source's gist in 30 seconds. No bullets, flowing prose. No jargon, or expand it inline. This is what you'd want to read 3 months from now to remember why this source mattered.)*



---

## Main claim or claims
*(One sentence if one central argument. List of bullets if multiple distinct claims.)*

- 

## Problem being solved

### The pain in detail
*(Concrete: who experiences this pain, when, what triggers it, what does it cost them, why does the existing approach fail. Make the reader feel the pain.)*



### How this pain manifests in your work
*(Where does this pain show up in your projects, clients, capabilities? Tie to specific projects in `04_projects/` or `current-goals.md`. If no clear fit, note as research question.)*



## Audience / use case
Who would benefit from acting on this?

## Novelty assessment
- [ ] New idea
- [ ] New combination of known ideas
- [ ] Repackaging of known idea
- [ ] Hype with little substance

---

## Tools mentioned

### Explicit
- [[tool-X]] —

### Inferred (from screen / workflow / context)
- [[tool-Y]] — *inferred*, confidence: medium

### Uncertain
- 

### In plain English
*(1-3 sentences explaining what these tools actually do for someone who hasn't used them. Skip tools that are universally known like "Git" or "Chrome" — focus on the unfamiliar ones.)*



---

## Workflow breakdown

### Demonstrated workflow
*(Steps the source actually showed or described.)*

1. 
2. 
3. 

### Notable implementation details
- 

### Likely architecture
What's probably happening under the hood, based on what was demonstrated.

### Workflow (constructed by Claude — not shown in source)
*(Optional. Used when the source describes a goal/outcome but doesn't show steps. This is Claude's reconstruction, not the source's content.)*

### In plain English
*(1-3 sentences explaining the workflow's overall shape — what comes in, what goes out, where the human is needed vs. where automation runs.)*



---

## Strategy extraction

### Business strategy
*(If source addressed: capture directly. If not: see "Inferred strategy" below.)*

### Growth strategy

### Automation strategy

### Content strategy

### Sales / offer strategy

### Inferred strategy (Claude's analysis — source did not state)
*(Optional. Categories above where the source didn't explicitly address but content has implications. Clearly labeled as analysis, not source claim.)*

### In plain English
*(1-3 sentences on the strategic shape — who's buying what from whom, what's the angle, why does this approach work or not work.)*



---

## Replication potential

### Directly copyable
- 

### Needs adaptation
- 

### Likely fluff or non-reusable
- 

---

## Visual signal markers
*(Moments where the transcript hinted at visual content that mattered. Manually inspect if relevant. Future: auto-screenshot will land images here.)*

- 

---

## Opportunities surfaced

### Product / SaaS ideas
- 

### Client-service ideas
- 

### Internal tool / automation ideas
- 

### Content ideas
- 

---

## Speculative extensions (Claude's analysis — not from source)
*(Optional. "What could this become" thinking. Clearly separated from source content. Empty is fine if there's nothing meaningful to add.)*

- 

---

## Suggested judgments (Claude's analysis — verify before adopting)

> **Scoring quick-reference** (full rubric: [[scoring-rubric]])
> - **Tier:** 1 act now / 2 save soon / 3 save general / 4 ignore
> - **Relevance:** 1 unrelated → 5 dead-on
> - **Actionability:** 1 inspirational only → 5 act today
> - **Monetization:** high / medium / low / none

*(Advisory only. Read each suggestion, verify against your goals, then fill the frontmatter fields above with your actual judgment. Don't anchor on these.)*

- **Suggested tier:** — *reasoning:*
- **Suggested actionability score:** — *reasoning:*
- **Suggested relevance score:** — *reasoning:*
- **Suggested monetization potential:** — *reasoning:*
- **Suggested execution recommendation:** — *reasoning:*

---

## Execution recommendation
- [ ] Act now
- [ ] Save for later
- [ ] Research deeper
- [ ] Ignore

**Reasoning:**

---

## Action log
*(What you actually did with this source over time. Update by hand as you act. When task management exists, this will sync to/from a separate task system — see [[phase-3-plus-queue]]. For now, inline.)*

*(Format: `- [status] action description (date) — outcome/notes`)*
*(Statuses: `[ ]` planned, `[x]` done, `[~]` in progress, `[parked]` paused, `[killed]` decided not to do)*

- 

---

## Discussions
*(Conversations and open questions about this source. Discussions auto-list below as they're created. To start a new one: hit `Cmd+Shift+D` or ask Cowork. See [[MOC-discussions]] for the cross-vault view.)*

```dataview
TABLE WITHOUT ID
  file.link AS "Discussion",
  status,
  updated AS "Updated"
FROM "00_inbox/discussions-pending" OR "03_domains"
WHERE type = "discussion" AND contains(sources, this.file.name)
SORT updated DESC
```

---

## Confidence assessment
- High confidence claims: 
- Medium confidence claims: 
- Low confidence / inferred: 
- Missing details / unanswered questions: 

---

## Extracted artifacts

### Newly created
- [[ ]]

### Existing notes enhanced
- [[ ]] — what was added

### Existing notes linked (no changes)
- [[ ]]

---

## Research questions
*(Things the source hinted at but didn't fully reveal. Worth investigating further. Questions you might want to discuss can be promoted to a discussion via QuickAdd.)*

- 

---

## Related sources
- 

## Pattern candidates
*(Sources that show the same thing — if 3+ accumulate, promote to a pattern note.)*

- [[ ]]
