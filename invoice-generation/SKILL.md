---
name: invoice-generation
description: Use this skill whenever Oliver needs to generate a client invoice for Keelworks LLC. Triggers on phrases like "generate an invoice," "create an invoice for [client]," "send invoice," or any request to produce a billable document. Produces a branded PDF invoice and creates a corresponding vault record. Use this skill before Mercury bank account is set up (uses personal Zelle as payment method); after Mercury arrives, this skill needs to be updated to reflect business banking.
---

# Invoice Generation (Keelworks LLC)

## What this skill does

This skill produces two artifacts when an invoice goes out:

1. A **branded PDF invoice** saved to `~/workspace/repos/keelworks/ops/invoices/`. The PDF is what the client receives by email.
2. A **vault record** saved to `07_business/keelworks-llc/finance/invoices/`. The vault record is the queryable history surface — Dataview blocks in `_index.md` aggregate every invoice ever issued.

Both artifacts share the same invoice number convention (`CCC-NNN`) so they stay tied together.

## When to trigger this skill

Direct triggers — these phrases reliably indicate the skill should run:

- "Generate invoice EVE-002 for Ahmad's monthly retainer"
- "Send Mohammad an invoice for $500 onboarding"
- "Create invoice for new client XYZ"
- "I need an invoice for [client] for [amount]"
- "Bill [client] for [scope]"

Indirect triggers — when Oliver is clearly heading toward an invoice:

- "How much do I bill Ahmad this month?"
- "Time to invoice Mohammad for the matrix work"
- "What was the invoice number for [client]'s last bill?"

When in doubt: trigger the skill. The cost of running it when not strictly needed is low; the cost of generating an invoice by hand without the skill is inconsistent formatting and missing vault records.

## Invoice numbering convention

Format: **`CCC-NNN`** where:

- `CCC` is a three-letter client code (uppercase). EVE for EV Electric Services. SHC for S&H Contracting Unlimited LLC.
- `NNN` is a per-client sequence number (zero-padded to three digits). Each client starts at 001 and increments per invoice.

**New client:** decide a three-letter code first (try to make it memorable — first letters of business name, or a meaningful abbreviation). Then start the sequence at 001.

**Source of truth for codes in use:** `07_business/keelworks-llc/finance/invoices/_index.md` has the canonical client-code reference. Check it before creating a new client code to avoid collisions.

## Action-verb scope language standard

Scope items in Keelworks invoices lead with action verbs. The verbs read as construction, not consulting — important for client perception. Construction language: someone is building things for them. Consulting language: someone is thinking about things. Clients pay for construction.

Standard verb list (use these or close variants):

- **Initiate** — start a discovery or research phase
- **Build** — produce a tangible output (GBP, profile, listing)
- **Architect** — design the structure of something larger (page architecture, matrix)
- **Develop** — execute on architected plans
- **Deploy** — push something live
- **Launch** — start a campaign or outreach
- **Integrate** — connect systems
- **Additional** — wildcard line for unenumerated scope discussed verbally

Standard SEO + marketing onboarding scope (the 6 + 1 template):

1. Initiate site audit and competitive analysis
2. Build out and optimize your Google Business Profile
3. Architect and develop Core 30 service + city pages
4. Deploy technical SEO foundations (schema, performance, fixes)
5. Launch local community signal outreach (Chamber, sponsorships, directories)
6. Integrate call tracking and source attribution
7. Additional services discussed during our call

The 7th item ("Additional services") is the catch-all that gives Oliver room to deliver verbally-agreed extras without re-invoicing. Don't drop it unless the engagement is unusually narrow.

## Payment method (interim — personal Zelle)

Until Mercury business bank account arrives, Keelworks uses Oliver's personal Zelle for payments. Standard payment line on invoices:

```
Zelle / 240-204-3885 / Oliver Marroquin / Reference: [INVOICE-NUMBER]
```

**This section needs to be updated when Mercury arrives.** See "Pending — update when Mercury arrives" at the bottom.

## How to generate an invoice — step-by-step

1. **Check the index** at `07_business/keelworks-llc/finance/invoices/_index.md` to confirm the client code and next sequence number. If it's a new client, decide a three-letter code and update the index.
2. **Run the parameterized script:**
   ```bash
   python3 ~/workspace/skills/invoice-generation/generate_invoice.py \
     --client-name "Ahmad Shaban" \
     --client-business "EV Electric Services" \
     --client-location "Fairfax, Virginia" \
     --client-website "evelectric.pro" \
     --invoice-number "EVE-001" \
     --amount "700.00" \
     --issued-date "May 13, 2026" \
     --due-line "On or before May 20, 2026"
   ```
   See the script's docstring + `--help` for all available flags.
3. **Verify the PDF** rendered correctly. Open in Preview. Check layout, spacing, amount, scope items. The script prints a content-gap diagnostic; review it.
4. **Create the vault record** at `07_business/keelworks-llc/finance/invoices/INV-<INVOICE-NUMBER>-<YYYY-MM-DD>.md`. Use existing records (`INV-EVE-001-2026-05-13.md`, `INV-SHC-001-2026-05-13.md`) as templates. Match the frontmatter shape and section headings.
5. **Update `_index.md`** if a new client code was introduced.
6. **Send the email** with the PDF attached. See the email template section below.
7. **Update the vault record's `status: sent` and `sent-date:`** when the email actually goes out (it may differ from the invoice's `issued-date` field).

## How to update invoice status when payment arrives

When payment lands:

1. Open the invoice record file.
2. Update `status: paid`.
3. Update `paid-date: YYYY-MM-DD`.
4. Update `payment-confirmation:` with whatever proof you have (Zelle confirmation number, screenshot path, or a brief note).
5. Update `updated:` to today's date.

The Dataview block in `_index.md` will automatically move the invoice from the "Open invoices" view to the paid-history view (just the "All invoices" block).

## Email template

Standard email body for sending an invoice. See `templates/email-template.md` for the canonical version (this is a snapshot).

```
Subject: Invoice [NUMBER] — Keelworks [ENGAGEMENT TYPE]

Hi [CLIENT NAME],

[PERSONAL OPENING LINE]

Attached is the invoice for the work we agreed to. [PAYMENT TIMING NOTE — flexible if applicable].

If anything looks off or you have questions, hit reply.

Thanks,
Oliver
```

Personal opening lines are short and grounded in the actual conversation — "Great talking with you yesterday," "Glad we got the kickoff done," "Thanks again for the chat at the meeting." Avoid generic "I hope this email finds you well" filler.

## What lives where (file map)

| Artifact | Path |
| --- | --- |
| Skill files (this folder) | `~/workspace/skills/invoice-generation/` |
| PDF outputs (sent to clients) | `~/workspace/repos/keelworks/ops/invoices/` |
| Vault records (queryable history) | `07_business/keelworks-llc/finance/invoices/` |
| Global cross-reference | `07_business/keelworks-llc/finance/invoices/_index.md` |
| Logo PNGs (for email signatures) | `~/workspace/repos/keelworks/site/` (website source assets) or `~/workspace/repos/keelworks/ops/logos/` (ops use) |

## Pending — update when Mercury arrives

When the Mercury business bank account is set up, the following changes are required:

- Switch the **payment method** on invoices from personal Zelle (240-204-3885) to the Keelworks LLC business account. ACH and wire details replace the Zelle reference.
- Update the **script's default payment line** so new invoices automatically use the business account.
- Update **this skill's "Payment method" section** to remove the "interim" framing.
- **Evaluate Wave** (or similar accounting/invoicing tool) to potentially replace the custom script. Mercury integrates with Wave directly; if the integration covers the use cases this script handles, the script can be retired and the skill simplified to "open Wave, fill the form."
- Update the **vault record template** for invoices to reflect the new payment-method field values.
