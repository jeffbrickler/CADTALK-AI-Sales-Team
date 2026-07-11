# Order email template + voice rules

Voice defers to `references/cadtalk-voice-reference.md`; the rules below are the
order-email-specific overrides (Register 4, internal).

## Voice (Jeff, internal / Register 4)
- Open `Hi, team.` (comma after Hi, period after the name). Close `BR,` then the sender's name.
- No em-dashes anywhere. Use a period, comma, colon, or a spaced hyphen.
- CADTALK always all caps. Never use ALL CAPS for emphasis; use bold.
- Keep numbers specific: dollar/NZD signs, exact figures, no rounding when the quote has it.
- One clear ask at the end (process / hold, with owner and date when the user has one).
- Lead with the point. State the order, then the summary, then the flags, then the ask.

## Subject line
- Process now:  `New order to process - [Company] (Deal [id])`
- Hold:         `New order (hold - [reason]) - [Company] (Deal [id])`
- Two linked orders: `New orders to process - [Company] (Deals [id] and [id])`

## Body template (one order)

```
To: fulfillment@cadtalk.com
Subject: New order to process - [Company] (Deal [id])

Hi, team.

New order to set up. Signed quote and products are in Pipedrive.
Pipedrive: [deal link]

Order summary
- Customer: [Company]
- Primary contact (invoice/portal): [Name], [title] - [email]
- Products: [source] to [target] integration [bundle/tier if known]
- Integration source / target: [source] / [target]
- Licenses: [# or "see signed quote"]
- ARR (subscription only): [$X USD / NZD]
- Implementation: [$X or "see signed quote"]
- Billing term: [term or "see signed quote"]
- PO number: [# / "see signed quote, hold if to be provided" / "Arena royalty report exception - process as unbilled"]
- Payment terms: [terms or "see signed quote"]
- Reseller / partner: [Arena / IFS / Infor partner / direct]
- Pod: [Enterprise (ARR over $25K) / SMB]
[- Parent account: [name]  ← only if royalty-report or group-owned]

Flags
- [partner rule: Arena = process unbilled until Royalty Report, apply 30% Reseller Margin Forever]
- [IFS = no discount, no customer welcome email, label "- Initial Setup", full impl billed after SOW]
- [ITAR / GovCloud: US-citizen staffing only, if defense/aerospace/gov]
- [expansion: add to existing subscription; ERP-only: skip CAD add-ons; etc.]
- [priority/timeline note if the deal is timed, prove-to-win, or committed to a kickoff date]

Ask: [process this order by <date> / hold for <reason> and what you will supply].

BR,
[Sender]
```

## Hold variants (use when the order is not ready to run)
- **Missing customer contact** (only a partner rep on record): "Hold Freshdesk,
  LicenseSpring, and Rocket Lane portal steps until I send the customer contact."
- **PO to be provided (non-Arena)**: "Hold per the PO process until the PO arrives."
- **Phase 2 / future**: "Do not begin setup yet. Phase [n], ~[timeframe]. I will release it."
- **Conditional deal**: "Confirm [dependency] is final before setup."
- **Unconfirmed scope**: "Confirm [partner / source CAD / location] on the quote first."

## Multi-order customers
One email, one order block per deal, each with its own Pipedrive link and partner rule
(e.g., an Arena order and an IFS order under one customer are staged differently).
