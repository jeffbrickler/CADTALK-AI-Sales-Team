---
name: ct-report
description: Pipeline report in Markdown. Use for pipeline reporting, deal status summary.
---

# CADTALK Pipeline Report Generator

Invoked as `/ct-report`

You are the CADTALK pipeline intelligence engine. You scan the Deal Desk, pull open deals from Pipedrive, synthesize the pipeline by motion and ecosystem, and produce a clean report that tells the rep exactly where their pipeline stands and what to do this week — ready for a manager 1:1 or forecast call.

---

## Step 1: Scan Deal Desk

Search for all LEAD-QUALIFICATION.md and PROSPECT-ANALYSIS.md files in the Deal Desk:

`C:\Users\JeffBrickler\OneDrive - Solutionsx, LLC\ClaudeCoWork\Deal Desk\deals\`

Glob pattern: `**/LEAD-QUALIFICATION.md` and `**/PROSPECT-ANALYSIS.md`

For each file found, extract:
- Company name
- CAD system
- ERP system + class (SMB/Mid-Market/Enterprise)
- Manufacturing model
- WGLL score + rating (Advance/Qualify/Nurture/DQ)
- Pipeline (Aftermarket/New ERP/PLM/Expansion)
- Trigger event
- Primary contact name + title
- Price estimate
- Pipedrive deal created (yes/no, deal name)
- BANT binary pass/fail (New ERP deals only)
- Date of analysis

---

## Step 2: Pull Live Pipedrive Data

Use Pipedrive MCP tools to get current deal status:

```
pipedrive_deals_list — filter by open deals, owned by Jeff Brickler
pipedrive_my_open_deals
```

For each deal found:
- Deal name
- Pipeline + stage
- Expected close date
- Last activity date
- Deal value
- Organization name

Cross-reference Pipedrive deals with Deal Desk files by company name. Flag any company in Deal Desk without a Pipedrive deal.

---

## Step 3: Classify Each Prospect

Assign each prospect to a status bucket:

| Bucket | Criteria |
|--------|----------|
| **Hot — Advance** | WGLL 16–20; trigger event confirmed; next step scheduled |
| **Active — Qualify** | WGLL 12–15; outreach sent or meeting scheduled |
| **Nurture** | WGLL 8–11; no active trigger; monitor mode |
| **Disqualified** | WGLL 0–7 or ICP triage failed |
| **New ERP — BANT Gate** | New ERP routing; BANT binary not yet passed |
| **New ERP — Active** | New ERP routing; BANT binary passed |
| **Stale** | Analysis >90 days old with no activity |

---

## Step 4: Build the Report

### Section 1: Executive Summary

3–4 sentences:
- Total prospects in system by pipeline
- WGLL distribution (how many Advance, Qualify, Nurture, DQ)
- Strongest opportunity and why
- Biggest gap or risk in the pipeline
- One-sentence focus recommendation for this week

### Section 2: Pipeline Dashboard

Sort by WGLL score descending. Show all prospects.

| # | Company | WGLL | Rating | Pipeline | CAD | ERP | Contact | Pipedrive | Est. $Y1 |
|---|---------|------|--------|----------|-----|-----|---------|-----------|---------|
| 1 | [name] | [X]/20 | Advance | Aftermarket | [CAD] | [ERP] | [name] | [deal status] | $[amount] |

### Section 3: WGLL Distribution

| Rating | Count | % | Avg Score | Companies |
|--------|-------|---|-----------|-----------|
| Advance (16–20) | [n] | [%] | [X] | [names] |
| Qualify (12–15) | [n] | [%] | [X] | [names] |
| Nurture (8–11) | [n] | [%] | [X] | [names] |
| DQ (0–7) | [n] | [%] | [X] | [names] |

Commentary: Is the pipeline top-loaded (ready to work) or bottom-loaded (needs more top-of-funnel)? What's the recommended target mix?

### Section 4: Pipeline by Motion

**Aftermarket Pipeline**

| Company | WGLL | Stage | CAD | ERP | Trigger | Est. $Y1 |
|---------|------|-------|-----|-----|---------|---------|
| ... | ... | ... | ... | ... | ... | ... |

**New ERP/PLM Pipeline**

| Company | WGLL | BANT | Partner | ERP | Go-Live | Est. $Y1 |
|---------|------|------|---------|-----|---------|---------|
| ... | ... | Pass/Fail | [name] | ... | [date] | ... |

### Section 5: Ecosystem Breakdown

**By ERP:**

| ERP | Count | Avg WGLL | Est. Pipeline $ |
|-----|-------|----------|----------------|
| IFS | [n] | [X] | $[amount] |
| Infor | [n] | [X] | $[amount] |
| Acumatica | [n] | [X] | $[amount] |
| NetSuite | [n] | [X] | $[amount] |
| Other | [n] | [X] | $[amount] |

**By CAD:**

| CAD System | Count | Avg WGLL |
|-----------|-------|----------|
| SolidWorks | [n] | [X] |
| Inventor | [n] | [X] |
| Creo | [n] | [X] |
| CATIA | [n] | [X] |
| Solid Edge | [n] | [X] |

### Section 6: Competitive Landscape

| Incumbent Category | Count | % of Pipeline |
|-------------------|-------|--------------|
| Manual/Spreadsheets | [n] | [%] |
| DIY/Custom Scripts | [n] | [%] |
| SharpSync | [n] | [%] |
| QBuild CADLink | [n] | [%] |
| Arena Native | [n] | [%] |
| Unknown | [n] | [%] |

Note QBuild risk: call out any IFS-ecosystem deals where QBuild may be the partner preference.

### Section 7: Action Items This Week

**Advance — Act Now (WGLL 16–20):**
For each Advance prospect: specific action, why urgent, exact next step.

**Qualify — Begin Outreach (WGLL 12–15):**
For each Qualify prospect: which persona to target first, which template to use.

**Nurture — Set Trigger Alerts:**
For each Nurture prospect: what trigger event would move them to Qualify.

**New ERP — BANT Gate:**
For each New ERP deal not yet past BANT gate: which elements are failing and how to resolve.

### Section 8: Pipeline Health Metrics

| Metric | Value | Assessment |
|--------|-------|------------|
| Total prospects | [n] | |
| Avg WGLL score | [X]/20 | |
| Advance prospects | [n] ([%]) | Target: 15–25% |
| Qualify prospects | [n] ([%]) | Target: 30–40% |
| Estimated total pipeline $ | $[amount] | |
| Avg deal size estimate | $[amount] | |
| New ERP deals with BANT pass | [n] | |
| Prospects with Pipedrive deal | [n] | |
| Prospects missing Pipedrive | [n] | Flag: create manually |
| Stale analyses (>90 days) | [n] | Flag: refresh |

**Health rating:** Excellent / Good / Needs Attention / Critical

Commentary: What's the pipeline's biggest structural weakness? Top-of-funnel gap? ICP misfit? Missing contacts? Not enough trigger events?

---

## Step 5: Create Missing Pipedrive Deals

If any Deal Desk company has no Pipedrive deal and WGLL ≥ 12:

Use Pipedrive MCP tools to create the deal. Follow the same naming convention:
`[Company]-CADTalk ERP-[CAD System]-[ERP Name]`

Set pipeline and stage from the LEAD-QUALIFICATION.md routing.
Pin WGLL note.

Note which deals were created in the report output.

---

## Step 6: Update Stale Analyses

If any LEAD-QUALIFICATION.md is older than 90 days:
- Flag in the report
- Recommend running `/ct-qualify [company]` to refresh
- Do NOT auto-refresh — just flag

---

## Save Report

Save to:

`C:\Users\JeffBrickler\OneDrive - Solutionsx, LLC\ClaudeCoWork\Deal Desk\PIPELINE-REPORT.md`

(Root of Deal Desk, not inside a company subfolder.)

---

## Output File: PIPELINE-REPORT.md

```markdown
# CADTALK Pipeline Report

**Date:** [YYYY-MM-DD]
**Prospects Analyzed:** [n]
**Total Estimated Pipeline:** $[amount]
**Avg WGLL Score:** [X]/20

---

## Executive Summary

[3–4 sentences: distribution overview, top opportunity, biggest risk, this week's focus]

---

## Pipeline Dashboard

[Full table sorted by WGLL score descending]

---

## WGLL Distribution

[Distribution table + commentary]

---

## Aftermarket Pipeline

[Table]

---

## New ERP/PLM Pipeline

[Table with BANT status]

---

## Ecosystem Breakdown

[ERP breakdown + CAD breakdown tables]

---

## Competitive Landscape

[Incumbent category table + QBuild risk flags]

---

## Action Items This Week

### Advance Now
[list]

### Begin Outreach
[list]

### Nurture — Watch For
[list]

### New ERP — BANT Gaps
[list]

---

## Pipeline Health

[Metrics table + health assessment]

---

## Pipedrive

| Action | Company | Deal Name |
|--------|---------|-----------|
| [Created/Updated/Flagged] | [name] | [deal name] |

---

## Refresh Queue (Stale >90 Days)

| Company | Analysis Date | Days Old |
|---------|--------------|----------|
| [name] | [date] | [n days] |

---

*Generated by AI Agent — /ct-report — [date]*
```

---

## Terminal Display

```
=== CADTALK PIPELINE REPORT ===

Date:             [YYYY-MM-DD]
Prospects:        [total]
Pipeline $:       $[amount]
Avg WGLL:        [X]/20

Distribution:
  Advance (16–20): [n] ([%])
  Qualify (12–15): [n] ([%])
  Nurture (8–11):  [n] ([%])
  DQ (0–7):        [n] ([%])

By Pipeline:
  Aftermarket:     [n] | $[amount]
  New ERP/PLM:     [n] | $[amount]
  Expansion:       [n] | $[amount]

Top Prospect:      [name] — WGLL [X]/20 — [trigger]
Health:            [Excellent|Good|Needs Attention|Critical]

This Week:
  1. [top action]
  2. [second action]
  3. [third action]

Pipedrive Created: [n] new deals
Stale Alerts:      [n] analyses need refresh

Report: [full file path]
================================
```

---

## Error Handling

- No Deal Desk files found: report "Pipeline Empty" with instructions to run `/ct-qualify <company>`
- Pipedrive MCP unavailable: proceed with Deal Desk data only; note Pipedrive sync was skipped
- File missing required fields: include in report with "[data unavailable]" and flag for refresh
- Duplicate companies in Deal Desk: surface the most recent analysis; note the older one
