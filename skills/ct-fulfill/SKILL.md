---
name: ct-fulfill
description: Turn closed-won CADTALK deals into per-deal order-submission emails to fulfillment@cadtalk.com, built to the New Order Processing SOP so order processing can run them without bouncing them back. Use for 'send these orders to fulfillment', 'fulfill these deals', 'order email(s)', 'process this order', 'hand off closed won to fulfillment/order entry', 'kick off billing/onboarding for these deals', or 'email fulfillment about the deals that closed' — one SOP-shaped email per order, not a batch.
---

# CADTALK Fulfillment Order Emails

Turn closed-won deals into per-deal order emails that order processing can execute
against the New Order Processing SOP. One order = one email to **fulfillment@cadtalk.com**.
A single batch email fails: order processing works one order at a time and needs the
SOP inputs and exception flags per order.

Live SOP (source of truth, re-check for changes): https://internal.cadtalk.com/doc/draft-new-order-processing-sop-iALq6fv2dj
The SOP-derived rules are distilled in `references/sop-order-rules.md`. The email format
and voice rules are in `references/fulfillment-email-template.md`. Read both before generating.

## CRM access (read-only, via sales-crm)

This skill only **reads** Pipedrive — it never writes. All reads go through the
sales-crm contract (`agents/sales-crm.md`): deal search/get, person get, organization
get. The `pipedrive_*` names below are legacy — map each to the connected Pipedrive MCP
base name the contract defines (e.g. `pipedrive_deals_list`/`_get` → `getDeals`/`getDeal`
or `searchDeals`; `pipedrive_persons_get` → `getPerson`; `pipedrive_organizations_get`
→ `getOrganization`). Field keys, if needed, come only from
`references/pipedrive-custom-fields.md`. Do not write the CRM from this skill.

## Voice

Every email uses the CADTALK voice — `references/cadtalk-voice-reference.md`, with the
order-email overrides in `references/fulfillment-email-template.md` (Register 4, internal:
opens `Hi, team.`, closes `BR,` + name, zero em-dashes, CADTALK all caps, one ask). Apply
the voice pass before returning the document.

## Workflow

### 1. Get the deals
Default: pull from Pipedrive live so this works for any period.
- List won deals: `pipedrive_deals_list` with `status=won`, sorted by `update_time` desc.
- **Filter to the real close window by `won_time`/`local_won_date`, not `update_time`.**
  Pipedrive has bulk re-sync artifacts: many deals share a near-identical `update_time`
  with old close dates. Confirm each deal's `won_time` falls in the target period.
- If Pipedrive is unavailable, ask the user for the deal IDs (or a pasted list) and proceed.
- Confirm the deal set with the user before generating (list company + deal id + ARR).

### 2. Pull what each email needs
Per deal, gather (see the field checklist in `references/fulfillment-email-template.md`):
- `pipedrive_deals_get` — value, ARR, ACV, MRR, currency, org_id, person_id, partner
  fields, pipeline_id, deal title (source/target are usually in the title), MEDDPICC
  fields for context.
- `pipedrive_persons_get` — primary contact name + email. If the contact belongs to a
  partner org (PTC/Arena/Info Consulting) rather than the customer, treat the customer
  contact as MISSING and set a hold flag.
- `pipedrive_organizations_get` — customer Source System / Target System if on the org.
- Build the Pipedrive deal link: `https://<tenant>.pipedrive.com/deal/<id>`
  (confirm the tenant subdomain with the user; do not hardcode a guess silently).
- Quote-only fields (exact billing term, license count, implementation split, PO number,
  payment terms) live in the signed quote inside the deal. Do NOT invent them — write
  "see signed quote" and let order processing read them, exactly as the SOP expects.

### 3. Apply the SOP rules
Use `references/sop-order-rules.md` to derive, per deal:
- Partner motion: Arena / IFS / Infor / direct — sets discount, PO handling, welcome email.
- Discount: Arena = 30% Reseller Margin Forever; IFS royalty = none; else per quote.
- Billing handling: Arena new orders = process as UNBILLED until the Royalty Report
  (PO arrives with it). Non-Arena missing PO = HOLD per the PO process.
- Pod: ARR over $25,000 USD = Enterprise; otherwise SMB. For non-USD ARR, note "confirm
  USD ARR for pod."
- IFS edge case: no customer welcome email; label "- Initial Setup"; full implementation
  billed to the customer after an SOW.
- ITAR / Arena GovCloud: for defense/aerospace/gov customers, flag US-citizen staffing only.
- Parent account: royalty-report (IFS/Arena) and group-owned customers need a parent.
- HOLD conditions (email says HOLD, not process): missing customer contact; PO "to be
  provided" (non-Arena); Phase 2 / future-dated work; deal conditional on another outcome;
  core scope (source CAD, partner, location) still unconfirmed.

### 4. Generate the emails
Write one email per deal using the template in `references/fulfillment-email-template.md`,
in Jeff's voice (Register 4, internal). Order the output by priority when the user has a
priority view (timed/prove-to-win and committed-kickoff deals first). Combine multiple
linked deals for one customer into a single email with one order block per deal (e.g., a
SW→Arena order plus an Arena→IFS order), noting each order's partner rule separately.

### 5. Deliver
Produce a single markdown document with all emails, clearly delimited and copy-paste ready
(`Fulfillment-Order-Emails_v1.md`), each with its own To/Subject/body. Save to the user's
working folder. Offer to package it into the deal handoff zip if one exists.

### 6. Verify before handing over
- Every email has: a Pipedrive link, PO status, partner rule, pod, and an explicit ask.
- HOLD emails clearly say hold and why; do not tell fulfillment to process an order that
  is missing a contact, PO, or is Phase 2 / conditional.
- Voice check: opens `Hi, team.`, closes `BR,` then name; zero em-dashes; CADTALK in all
  caps; dollar/figure specifics kept; one ask per email.
- Re-read the live SOP link if it may have changed since `references/sop-order-rules.md`
  was written (the SOP is a living draft with open TODOs, e.g., Arena/IFS payment terms).

## Notes
- The salesperson's email supplies Phase 1 inputs and flags only. Order processing runs
  Phases 2-5 (ChargeBee, Freshdesk, LicenseSpring, TMetric, Rocket Lane) from the SOP.
- `pipedrive_files_list` has ignored the per-deal filter in some builds (returns an
  account-wide list). Do not try to attach contracts from it; point to the Pipedrive
  deal link, where signed contracts are attached.
- This skill does not send email or write Pipedrive. It produces copy-paste-ready order
  emails for the rep to send and for order processing to execute.
