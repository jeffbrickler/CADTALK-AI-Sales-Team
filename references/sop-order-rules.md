# New Order Processing SOP — rules that shape the order email

Distilled from the New Order Processing SOP (living draft):
https://internal.cadtalk.com/doc/draft-new-order-processing-sop-iALq6fv2dj
Re-read the live doc if it may have changed. Open TODOs in the SOP as of this writing:
Arena/IFS payment terms rows were unfinished — default those to "see signed quote"
unless the user gives a standing term.

## What order processing extracts in Phase 1 (so the email must surface it)
1. The Pipedrive quote link (signed quote: products/bundles + billing term).
2. PO number — from the quote's Customer Information section.
3. Payment terms — order-field terms override the terms-and-conditions page.

## Partner motions and the rules they trigger
- **Arena (reseller)**: PO arrives with the Royalty Report. Process as **UNBILLED charges
  until the Royalty Report is received**. Apply **30% Reseller Margin Forever** discount.
  Customers DO get a welcome email. Parent account required (royalty report).
- **IFS**: **No discount** (margin taken at the royalty report). **No customer welcome
  email.** Integration Setup only — label **"- Initial Setup"** in TMetric and Rocket
  Lane; the full implementation is billed to the customer after an **SOW**. Parent account
  required (royalty report).
- **Infor / other partner (e.g. Info Consulting, EMDA)**: discount and invoicing per the
  signed quote. Confirm whether the customer or the reseller is invoiced.
- **Direct**: customer invoiced directly; discount per quote.

## PO handling
- PO present → include it.
- PO "To be provided" and **not** an Arena order → **HOLD**; follow the PO process
  (email customer contacts, copy salesperson, attach signed quote, state you cannot
  process without it).
- Arena new order → exception: proceed as unbilled; PO comes with the Royalty Report.

## Pod (Rocket Lane)
- **Enterprise** pod if ARR **over $25,000 USD**; otherwise **SMB / Mid-Market**.
- Non-USD ARR (e.g., NZD): note "confirm USD ARR for pod threshold."

## Other edge cases to flag in the email when they apply
- **ERP-only (no CAD)**: skip CAD add-ons and CAD license features.
- **ITAR / Arena GovCloud** (defense, aerospace, government customers): US-citizen
  staffing only. Do not assign the Canadian consultant without a compliance check.
- **Existing-customer expansion**: add licenses to the existing ChargeBee subscription
  rather than creating a net-new customer; confirm the sites in scope.
- **Parent account / group ownership**: name the parent account to set up.

## Systems order processing will populate (context; the email need not repeat these)
ChargeBee (customer, parent, product subscription in CADTALK ERP family, integration
add-ons, discount, billing term with fixed cycles for multi-year, implementation
subscription = ERP Fixed Implementation 90 days, unbilled charges, invoice) →
Freshdesk (company + contact, activation email) → LicenseSpring (CADTALKUSER, time-limited
end 3000-01-01, max simultaneous = licenses purchased, product features per integration) →
TMetric (client + project, budget 60% of impl fee) → Pipedrive Customer Success pipeline
deal ("[Company] - Implementing", value = ARR only) → Rocket Lane (account + project,
pod, source/target, licenses, ARR, subscription id; upload signed contract).

## Fields the email should carry so those systems can be populated
Customer; primary customer contact name + email (invoice/Freshdesk/LicenseSpring/portal);
products / bundle; integration source; integration target; # licenses; ARR (subscription
only) + currency; implementation fee; billing term; PO number/status; payment terms;
reseller/partner; discount rule; pod; parent account; any ITAR/ERP-only/expansion flags.
Anything not known from CRM = "see signed quote."
