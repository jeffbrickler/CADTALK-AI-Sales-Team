---
name: ct-assets
description: Generate deal collateral — pitch/proposal decks, one-pagers and battlecards, and ROI calculators. Use for 'build a deck', 'make a one-pager', 'generate an ROI calculator', 'create a battlecard'.
---

## Grounding — Brain index

Sales-process, enablement, and asset doc IDs live in `references/brain-index.md`.
Load it when you need to pull a playbook, script, battlecard, or template by ID —
pull by ID directly; search is the fallback. If an ID 404s, search by title and
flag the stale ID.

# CADTALK Sales Asset Generator

Invoked as `/ct-assets <type> [args]`. Types: `deck`, `collateral`, `roi`.
Every asset is deal-specific — pull deal context first (through the sales-crm read
path) and write the output to the deal folder's `artifacts/` subfolder, never the
current working directory.

SOWs and pricing sheets are **not** here — those stay in `/ct-proposal`.

## Brand + grounding

- Canva designs use the brand kit whose ID is in `deal-desk.local.md` → Brand Kit.
  Always pass it; search brand templates before building from scratch.
- Structure references (executive one-pager, business case template, battlecards)
  come from `references/brain-index.md` — pull by ID.
- Apply the CADTALK voice (`/ct-voice`) to any headline or body copy before finalizing.

## Graceful degradation

If a connector is absent, fall back and say which fallback you used:
- Gamma missing → build the deck with the `pptx` skill.
- Canva missing → build collateral with the `docx` skill (no brand kit; note it).
- Always available: `xlsx` for ROI.

---

## Type: deck — `/ct-assets deck <company> [pitch|proposal|demo-overview|partner-overview]`

Default `pitch`. Generate with Gamma (default) or Canva (branded). Contents by type:
- `pitch`: company overview, problem/solution, proof points, integration highlights,
  pricing overview.
- `proposal`: executive summary, technical fit, business case, pricing, timeline,
  next steps.
- `demo-overview`: what we'll show, expected outcomes, attendee prep, agenda.
- `partner-overview`: CADTALK value prop for partner AEs, co-sell benefits, how the
  integration fits the ERP deal.

## Type: collateral — `/ct-assets collateral <company> [one-pager|battlecard|business-case]`

Canva with the brand kit from `deal-desk.local.md`. Contents by type:
- `one-pager`: product overview for the prospect's ecosystem/ERP class (structure:
  executive one-pager doc from brain-index).
- `battlecard`: positioning vs. the named competitor (structure: battlecards doc).
- `business-case`: ROI summary for the deal (structure: business case template doc).

## Type: roi — `/ct-assets roi <company>`

Build an `.xlsx` ROI calculator with the `xlsx` skill. Include: hours saved per week,
BOM-error reduction, audit-compliance value, payback period. Use deal-specific inputs
from the deal folder / Pipedrive where available; reasonable defaults otherwise, and
label which are defaults. Format for sharing with the economic buyer.

---

## Common mistakes

- Writing the asset to the cwd instead of `deals/<Company>/artifacts/`.
- Skipping the brand kit on Canva output — pull it from `deal-desk.local.md`.
- Generic ROI numbers — anchor to the deal's actual engineering headcount and pain.
