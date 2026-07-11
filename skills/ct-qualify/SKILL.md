---
name: ct-qualify
description: Lead qualification (BANT/MEDDIC) AND enterprise deal coaching. Use for qualifying a lead or deal and scoring fit; and — in Coach Mode — for 'review this deal', 'coach my AE on this opportunity', 'why is this deal stuck', 'is this deal real', 'how do I multi-thread this account', 'the deal went dark — what now', 'build a success plan', or 'my AE says it's close but I'm not sure'.
---

# CADTALK Lead Qualification Engine

Invoked as `/ct-qualify <company> [url]`

You are the CADTALK lead qualification engine. When this skill runs, you research the prospect, score them against the CADTALK ICP, route them to the right pipeline, create Pipedrive records automatically, and save the full qualification report to the Deal Desk.

No confirmation prompts. Research, score, create, save.

---

## Two modes — pick before Step 1

- **Qualify Mode (default)** — a new or early prospect. Run Steps 1–9 below:
  research → ICP triage → pipeline routing → WGLL score → BANT gate → pain
  hypotheses → pricing → Pipedrive records → save. This is the flow when the
  request is a company name or "qualify [company]".
- **Coach Mode** — an *existing* deal the AE already owns, and the ask is to
  review it, diagnose why it's stuck, coach the AE, multi-thread it, restart a
  dark deal, or build a Success Plan. Triggers: "review this deal", "coach my AE
  on this", "why is [company] stuck", "is this deal real", "the deal went dark",
  "help me multi-thread", "build a success plan", "my AE says it's close but I'm
  not sure". **Run the framework in `references/deal-coach.md`** (BANTED review →
  9 cycle killers → buying-committee mapping → Success Plan → coach-without-taking-
  over → stuck-deal protocols → Deal Health Card output). Do not run the
  new-prospect Steps 1–9 for a coaching request.

Coach Mode complements the forecast/stage gates: `/ct-commit` decides forecast
integrity, `/ct-score` grades a discovery call, and Coach Mode coaches the live
deal in between. Any CRM read/write in either mode goes through the sales-crm
contract (`agents/sales-crm.md`) — never write Pipedrive with a hand-built key.

---

## Inputs

- `<company>`: Company name (required)
- `[url]`: Company website (optional — search for it if not provided)

---

## Step 1: Research

Fetch and scan these sources. Run in parallel where possible.

| Source | What to Extract |
|--------|----------------|
| Company homepage | Products made, industries served, manufacturing signals |
| Products/Solutions page | Custom vs. standard, ETO/CTO/MTO language |
| Careers page | Engineering roles (CAD requirements), IT roles (ERP + integration), any "data entry" language |
| LinkedIn company page | Employee count, engineering department size, recent activity |
| External search: `"[company]" (IFS OR Infor OR Acumatica OR "Business Central" OR NetSuite OR SAP OR SYSPRO OR Epicor OR QAD OR "Dynamics F&O")` | ERP detection |
| External search: `"[company]" (Inventor OR SolidWorks OR Creo OR CATIA OR "Solid Edge")` | CAD detection |
| External search: `"[company]" ERP implementation OR "go live" OR migration` | Trigger detection |

---

## Step 2: ICP Triage (4-Question Gate)

Run these 4 questions against everything you found. If any mandatory question fails, disqualify immediately. Do not create Pipedrive records for disqualified prospects.

| # | Question | Pass | Fail |
|---|----------|------|------|
| 1 | Designs in supported 3D CAD? | Inventor, SolidWorks, Creo, CATIA, or Solid Edge confirmed or strongly implied | 2D CAD only, no 3D, or unsupported system |
| 2 | Discrete manufacturer? | Machinery, assemblies, equipment, electronics, defense, fabricated metal parts | Chemicals, pharma, food/beverage, oil & gas, textiles |
| 3 | Supported ERP? | IFS, Infor, Acumatica, BC, NetSuite, SAP, F&O, SYSPRO, Epicor, QAD, Arena PLM | ERP not supported AND no migration underway |
| 4 | Champion signal or pain indicator? | Engineering role with data entry language; ETO/CTO environment; integration developer job; trigger event | No signals, fewer than 3 engineers visible, revenue clearly under $5M |

**If Q1, Q2, or Q3 fails:** Write a short DQ note. Do not create Pipedrive records. Output a brief DQ summary to the terminal and save LEAD-QUALIFICATION.md with DQ status.

**If Q4 fails:** Score as low priority (WGLL 0–7). Still create Pipedrive record as a Nurture lead.

---

## Step 3: Pipeline Routing

Based on research, route to one of three pipelines before scoring.

| Signal | Pipeline |
|--------|----------|
| ERP is being implemented or actively evaluated | New ERP/PLM |
| ERP go-live announced or implementation partner named | New ERP/PLM |
| ERP is live and running (>30 days) | Aftermarket |
| No ERP context found | Aftermarket (default) |
| Arena PLM present with need to push to ERP | Aftermarket (Arena→ERP product line) |
| Existing CADTALK customer adding users or sites | Expansion |

For **New ERP/PLM** routing: complete the BANT binary gate in Step 5 before advancing.

---

## Step 4: WGLL Scoring

Score the prospect across 5 dimensions. Max 20 points. Record the score per dimension.

### Dimension 1: ICP Fit (0–4)

| Score | Criteria |
|-------|----------|
| 4 | Discrete mfg confirmed, 3D CAD + supported ERP confirmed, 5–50 engineers, $10M–$250M revenue, ETO or CTO model |
| 3 | Meets 4 of 5 criteria above; one gap (size slightly off, or mfg model inferred not confirmed) |
| 2 | Meets 3 of 5 criteria; CAD + ERP confirmed but size or model unclear |
| 1 | Meets 1–2 criteria; likely fit but significant unknowns |
| 0 | Fails ICP triage or disqualifying signal present |

### Dimension 2: Pain Indicators (0–4)

| Score | Criteria |
|-------|----------|
| 4 | Explicit pain confirmed — job post mentions "data entry" or "BOM entry" in engineering role; or press/review mentions BOM errors; or direct statement |
| 3 | Strong implicit pain — ETO/CTO shop with 10+ engineers, no visible integration tool anywhere |
| 2 | Moderate — CAD + ERP present, moderate engineer count, standard manufacturing model |
| 1 | Weak signals — small team (<5 engineers) or simple product structure |
| 0 | No pain signals, or existing working automation detected |

### Dimension 3: Research Depth (0–4)

| Score | Criteria |
|-------|----------|
| 4 | CAD confirmed, ERP confirmed, engineer count estimated, manufacturing model identified (ETO/CTO/MTO), and at least one trigger event found |
| 3 | CAD confirmed, ERP confirmed, engineer count estimated; manufacturing model inferred but not confirmed |
| 2 | CAD + ERP confirmed; size and model not determinable from available data |
| 1 | One of CAD or ERP confirmed; the other is unknown |
| 0 | Minimal public data available; can't confirm CAD or ERP |

### Dimension 4: CRM Readiness (0–4)

| Score | Criteria |
|-------|----------|
| 4 | Named decision maker found (VP/Dir Engineering or IT Director) with LinkedIn URL and at least one personalization anchor |
| 3 | Title-level contact found on LinkedIn; no direct personalization anchor but reachable |
| 2 | Company found on LinkedIn; engineer or IT roles visible but no named individual |
| 1 | Company only; no individual contact data at all |
| 0 | No usable contact data |

### Dimension 5: Call Prep Quality (0–4)

| Score | Criteria |
|-------|----------|
| 4 | Trigger event identified, pain quantified or estimated, MEDDPICC hypotheses built (M + I), competitive landscape assessed, stat hook ready |
| 3 | Most prep complete; trigger identified; pain estimated; minor gaps in MEDDPICC |
| 2 | Basic pain hypothesis + pricing estimate only; no trigger, no competitive intel |
| 1 | Minimal prep; only company name and product type confirmed |
| 0 | Not ready for a call |

### WGLL Rating

| Score | Rating | Action |
|-------|--------|--------|
| 16–20 | **Advance** | Schedule discovery immediately. High-confidence ICP fit. |
| 12–15 | **Qualify** | Good prospect. Begin outreach sequence. |
| 8–11 | **Nurture** | Soft ICP fit or insufficient data. Monitor for triggers. |
| 0–7 | **Disqualify** | No fit or data gap too large. |

---

## Step 5: BANT Binary Gate (New ERP/PLM routing only)

If pipeline = New ERP/PLM, run this gate. All 4 must pass to advance the deal.

| Element | Pass | Fail |
|---------|------|------|
| **Budget** | Integration is part of the ERP project budget; ERP project has active funding | "Phase 2" or no mention of integration budget |
| **Authority** | Named customer decision-maker who controls integration decisions can be identified | Can't name anyone; partner-only contact |
| **Need** | Customer has confirmed requirement or strong preference for CAD-ERP integration at go-live | "Nice to have" or "maybe later" |
| **Timeline** | ERP selection within 12 months or active evaluation in progress | >12 months out; no ERP timeline visible |

**BANT result:**
- All 4 pass: `bant_binary_pass: true` — route to New ERP/PLM, advance
- Any fail: `bant_binary_pass: false` — flag which elements failed; default to Aftermarket or hold

---

## Step 6: Pain Hypotheses (MEDDPICC — M and I)

Build pre-Discovery hypotheses from what you found. These are starting points for the AE, not confirmed facts.

**M — Metrics (How will they measure success?)**
Write one sentence: "[Estimated engineer count] engineers × [estimated BOM entry hours/week] hrs/week × $60/hr = $[amount]/year in labor savings from eliminating manual entry."

If engineer count unknown: use "20 engineers" as the default for a company in CADTALK's ICP range.

**I — Identification of Goal (Why now?)**
State the trigger: "They're implementing [ERP] and need integration at go-live." / "Their CAD-to-ERP scripts will break during the cloud migration." / "Engineer count doubled; manual entry is no longer sustainable." / "No visible trigger — pain is likely chronic but not acute."

---

## Step 7: Pricing Estimate

### Product Line

| Situation | Product Line |
|-----------|-------------|
| 3D CAD connecting to ERP | Standard CAD/PDM/PLM → ERP |
| MCAD connecting to Arena PLM | MCAD → Arena PLM |
| Arena PLM connecting to ERP | Arena PLM → ERP |

### Tier

| Tier | Use When |
|------|----------|
| Tier 1 | Single CAD source, standard items/BOM only, no routings, no rules, no DFM |
| Tier 2 | Needs rules engine, routings, costing, DFM access, or ECO support |
| Tier 3 | Multi-site, batch/unattended automation, WBS/Projects |

**Default to Tier 2** when manufacturing model is ETO or CTO and company has 10+ engineers. Default to Tier 1 for MTO or small shops (<10 engineers).

### Price Matrix (subscription/year)

| | Tier 1 | Tier 2 | Tier 3 |
|--|--------|--------|--------|
| SMB (Acumatica, BC, NetSuite, MYOB) | $10,995 | $16,995 | $24,995 |
| Mid-Market (Infor, Epicor, SYSPRO) | $14,995 | $21,995 | $32,995 |
| Enterprise (IFS, SAP, F&O, JDE, QAD) | $19,995 | $29,995 | $44,995 |

Implementation: $6,995–$14,995 (one-time). Startup grant (revenue <$5M): 50% off implementation only.

**Year 1 total** = subscription + implementation midpoint.

---

## Step 8: Pipedrive Record Creation

Create all three records automatically. No confirmation prompt.

### 8.1 Search for Existing Org

Search Pipedrive for the company name. If found, use the existing org ID. If not found, create:

**Organization:**
- Name: [company name]
- Set Organization Type field if visible (Manufacturer)

### 8.2 Create Person (if contact found)

Only if a named contact was found in research:
- Name: [contact name]
- Title: [title]
- LinkedIn: [URL if found]
- Link to org

If no named contact found: skip Person creation. Note it in the qualification file.

### 8.3 Create Deal

**Deal name format:** `[Company]-CADTalk ERP-[CAD System]-[ERP Name]`

Examples:
- `Acme Industries-CADTalk ERP-SolidWorks-IFS`
- `Midland Fabricators-CADTalk ERP-Inventor-Acumatica`
- `Precision Dynamics-CADTalk ERP-Creo-NetSuite`

**Deal fields to set:**
| Field | Value |
|-------|-------|
| Pipeline | New ERP/PLM or Aftermarket (per Step 3 routing) |
| Stage | First stage of selected pipeline |
| Expected close | Leave blank (AE sets after discovery) |
| Source System | [CAD system name] |
| Target System | [ERP name] |
| Org Source | Web Research — AI Agent |
| Source Channel | Outbound |
| Lead Status | New |

### 8.4 Pin WGLL Score Note

Create a note on the deal. Mark it as pinned.

**Note title:** `WGLL SCORE: [Rating] – [Date] – AI Agent – [X]/20 – [Pipeline]`

**Note body:**
```
WGLL SCORE: [Advance|Qualify|Nurture|DQ] — [YYYY-MM-DD] — AI Agent — [X]/20 — [Pipeline]

ICP Fit:         [X]/4
Pain Indicators: [X]/4
Research Depth:  [X]/4
CRM Readiness:   [X]/4
Call Prep:       [X]/4

Pain Hypothesis: [one sentence from Step 6 — M]
Trigger:         [one sentence from Step 6 — I]
Pipeline:        [Aftermarket|New ERP/PLM]
Price Estimate:  $[subscription]/yr + $[implementation] impl | Y1 Total: ~$[y1_total]
```

### 8.5 Create Activity

Create a Pipedrive activity linked to the deal:
- Type: Task
- Subject: "Review AI qualification — [Company Name]"
- Note: "WGLL [X]/20 — [Rating]. AI agent completed full qualification. Review before outreach."
- Due: Tomorrow
- Assigned to: Jeff Brickler

---

## Step 9: Save to Deal Desk

Save the full qualification report to:

`C:\Users\JeffBrickler\OneDrive - Solutionsx, LLC\ClaudeCoWork\Deal Desk\deals\[CompanyName]\LEAD-QUALIFICATION.md`

Create the folder if it doesn't exist.

---

## Output File: LEAD-QUALIFICATION.md

```markdown
# Lead Qualification: [Company Name]

**Date:** [YYYY-MM-DD]
**URL:** [company URL]
**Pipeline:** [Aftermarket | New ERP/PLM | Expansion | Disqualified]
**WGLL Score:** [X]/20 — [Advance | Qualify | Nurture | DQ]

---

## Qualification Snapshot

| Field | Value |
|-------|-------|
| Company | [name] |
| CAD System | [system] |
| ERP System | [ERP] |
| ERP Class | [SMB / Mid-Market / Enterprise] |
| Manufacturing Model | [ETO / CTO / MTO / Unknown] |
| Employee Count | [estimate] |
| Engineer Count | [estimate] |
| Revenue Estimate | [range] |
| Pipeline | [pipeline] |
| WGLL Score | [X]/20 — [Rating] |
| ICP Triage | [Pass / Fail — reason if fail] |

---

## WGLL Scorecard

| Dimension | Score | Evidence |
|-----------|-------|----------|
| ICP Fit | [X]/4 | [key evidence] |
| Pain Indicators | [X]/4 | [key evidence] |
| Research Depth | [X]/4 | [key evidence] |
| CRM Readiness | [X]/4 | [key evidence] |
| Call Prep Quality | [X]/4 | [key evidence] |
| **Total** | **[X]/20** | **[Advance / Qualify / Nurture / DQ]** |

---

## Pipeline Routing

**Routed to:** [Pipeline name]
**Reason:** [One sentence explaining the routing decision]

[If New ERP/PLM:]
### BANT Binary Gate
| Element | Result | Evidence |
|---------|--------|----------|
| Budget | Pass / Fail / Unknown | [evidence] |
| Authority | Pass / Fail / Unknown | [evidence] |
| Need | Pass / Fail / Unknown | [evidence] |
| Timeline | Pass / Fail / Unknown | [evidence] |
**Gate result:** [Pass / Fail — note which elements failed]

---

## Pain Hypotheses

**M — Metrics:**
[Labor calc: X engineers × Y hrs/week × $60/hr × 50 weeks = $Z/year]

**I — Identification of Goal:**
[Trigger statement — why now]

---

## Competitive Position

**Incumbent:** [Manual | DIY Scripts | SharpSync | QBuild | Arena | Unknown]
**Displacement angle:** [one sentence]
**Risk flags:** [QBuild/partner risk if applicable]

---

## Pricing Estimate

| | Value |
|--|-------|
| Product Line | [Standard CAD→ERP / MCAD→Arena / Arena→ERP] |
| Tier | [Tier 1 / 2 / 3] |
| Subscription/Year | $[amount] |
| Implementation | $[range] |
| Year 1 Total | ~$[amount] |
| Startup Grant Eligible | [Yes / No] |

---

## Contacts Found

| Name | Title | Role | LinkedIn | Anchor |
|------|-------|------|----------|--------|
| [name or "Not found"] | [title] | [persona] | [URL] | [anchor] |

---

## Pipedrive

| Record | Status |
|--------|--------|
| Organization | [Created / Found existing — ID: X] |
| Person | [Created / Skipped — no contact found] |
| Deal | [Created — Name: X, Pipeline: Y, Stage: Z] |
| WGLL Note | [Pinned to deal] |
| Activity | [Created — due: tomorrow] |

---

## Next Steps

1. [AE action — outreach to primary contact or partner AE]
2. [Discovery prep — key questions based on pain hypothesis]
3. [If New ERP: confirm partner AE and get on MAP]
4. [Watch for: specific trigger or signal that increases urgency]

---

*Generated by AI Agent — /ct-qualify — [date]*
```

---

## Terminal Display

After completing all steps, display in the terminal:

```
=== CADTALK LEAD QUALIFICATION ===

Company:    [name]
URL:        [url]
Date:       [YYYY-MM-DD]

ICP Triage: [PASS | FAIL — reason]

CAD System: [system]
ERP System: [ERP] ([SMB|Mid-Market|Enterprise])
Mfg Model:  [ETO|CTO|MTO|Unknown]
Engineers:  [estimate]

WGLL Score: [X]/20 — [ADVANCE | QUALIFY | NURTURE | DQ]
  ICP Fit:         [X]/4
  Pain Indicators: [X]/4
  Research Depth:  [X]/4
  CRM Readiness:   [X]/4
  Call Prep:       [X]/4

Pipeline:   [Aftermarket | New ERP/PLM | Expansion]
[If New ERP:] BANT Gate: [PASS | FAIL — elements that failed]

Pain:       [one-line M hypothesis]
Trigger:    [one-line I hypothesis]

Pricing:    $[subscription]/yr | Y1: ~$[total]
Incumbent:  [category]

Pipedrive:
  Org:      [Created | Found]
  Person:   [Created | Skipped]
  Deal:     [Deal name]
  Pipeline: [pipeline name]
  Note:     WGLL pinned

Report:     [full file path]
===================================
```

---

## Error Handling

- URL unreachable: try alternate URL formats (www, no-www, /about, /company); note failure and proceed with search-only data
- Pipedrive org already exists: use existing; do not duplicate
- Pipedrive deal already exists for this company: flag in output; do not duplicate; update WGLL note instead
- Company has no LinkedIn presence: note the gap; score Research Depth at 1 maximum
- No contacts found: skip Person creation; set CRM Readiness to 2 or below; note in output
- Deal Desk folder doesn't exist: create it before saving the file
