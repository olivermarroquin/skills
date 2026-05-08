---
type: workflow
status: draft
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
domains: []
tools-required: []
inputs: []
outputs: []
estimated-time: ""
times-run: 0
tags: [workflow]
---

# Workflow: <% tp.file.title.replace(/^workflow-/, "").replace(/-/g, " ") %>

## Goal
What this workflow produces. The deliverable.

## When to run it
Trigger conditions.

## Inputs required
- Input 1:
- Input 2:

## Tools required
- [[ ]]
- [[ ]]

## Steps

### 1.
### 2.
### 3.

## Outputs
- [[ ]]

## Validation
How to know the workflow worked.

## Failure modes
Where this typically breaks.

## Variants
- For X case:
- For Y case:

## Run log
- <% tp.date.now("YYYY-MM-DD") %> — first defined
