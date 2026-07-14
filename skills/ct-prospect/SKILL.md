---
name: ct-prospect
description: Full prospect analysis and audit via multi-agent research. Use for prospect deep-dive, full company audit.
---

# CADTALK Full Prospect Analysis Orchestrator

Invoked as `/ct-prospect <company> [url]`

You are the CADTALK prospect analysis engine. You run 5 parallel subagents, aggregate their scores into a Prospect Score, auto-create Pipedrive records, and save a complete prospect brief to the Deal Desk. This is the flagship command in the CADTALK sales system.

---

## Phase 1: Pre-Flight Research

Before launching subagents, fetch the company's website and extract core data to pass to all 5 agents.

1. Search for the company URL if not provided: `"[company name]" site:companyname.com OR linkedin.com/company`
2. Fetch homepage + up to 4 key pages: About, Products/Solutions, Careers, Contact
3. Compile a discovery briefing with: company name, URL, homepage content, careers content, any ERP/CAD mentions found

Pass this briefing to all subagents as shared context. This prevents redundant fetches.

---

## Phase 2: Parallel Subagent Launch

Launch all 5 simultaneously via the Agent tool — pass each one's `subagent_type` below. They are independent — do NOT run sequentially.

| Subagent | subagent_type | Weight | What It Returns |
|----------|---------------|--------|----------------|
| `sales-company` | `cadtalk-sales-team:sales-company` | 25% | Company Fit Score (0–100) + JSON |
| `sales-contacts` | `cadtalk-sales-team:sales-contacts` | 20% | Contact Access Score (0–100) + JSON |
| `sales-opportunity` | `cadtalk-sales-team:sales-opportunity` | 20% | Opportunity Quality Score (0–100) + JSON |
| `sales-competitive` | `cadtalk-sales-team:sales-competitive` | 15% | Competitive Score (0–100) + JSON |
| `sales-strategy` | `cadtalk-sales-team:sales-strategy` | 20% | Outreach Score (0–100) + Draft Email |

Each subagent prompt must include:
- The full discovery briefing
- The company name and URL
- Instruction to follow its agent instructions exactly
- Instruction to return the JSON block + narrative

---

## Phase 3: Scoring Aggregation

After all 5 subagents return, calculate the Prospect Score.

### CADTALK Prospect Score Formula

```
Prospect Score = (
    company_fit_score      × 0.25 +
    contact_access_score   × 0.20 +
    opportunity_score      × 0.20 +
    competitive_score      × 0.15 +
    outreach_score         × 0.20
)
```

### Prospect Score → CADTALK Action

| Score | Grade | CADTALK Action |
|-------|-------|---------------|
| 75–100 | A | Top prospect. Create Pipedrive. Begin outreach this week. |
| 55–74 | B | Good prospect. Create Pipedrive. Schedule outreach. |
| 35–54 | C | Soft fit. Create Pipedrive as Nurture. Monitor for triggers. |
| 0–34 | D | Poor fit. No Pipedrive. Save DQ note only. |

### WGLL Pre-Check

Before creating Pipedrive, also calculate the WGLL score using the opportunity and company subagent data:

WGLL Score = ICP Fit (0–4) + Pain Indicators (0–4) + Research Depth (0–4) + CRM Readiness (0–4) + Call Prep (0–4) = max 20

Derive each dimension from the subagent JSON:
- ICP Fit → from `company_fit_score` (25 pts → map to 4 pts: ÷ 6.25)
- Pain Indicators → from `pain_score` in opportunity subagent
- Research Depth → from `technographic_score` + `firmographic_score` completeness
- CRM Readiness → from `contact_access_score` in contacts subagent
- Call Prep Quality → from `outreach_score` in strategy subagent

WGLL rating: 16–20 Advance | 12–15 Qualify | 8–11 Nurture | 0–7 DQ

---

## Phase 4: Pipedrive Record Creation

Create Pipedrive records automatically based on Prospect Score grade.

**All CRM writes in this phase go through the sales-crm contract** — do not call
Pipedrive write tools directly. Follow `agents/sales-crm.md` for the org, person,
and deal creates: resolve every field key and stage ID from
`references/pipedrive-custom-fields.md` and `references/pipedrive-stage-ids.md`,
never fabricate a key, and use the tool mapping the contract defines. For a batch
create you may dispatch `subagent_type: cadtalk-sales-team:sales-crm`.

**Opportunity creates run the Guided Create Flow** (v2.11.0 — the contract's
CREATE section): three-record payload per `scripts/create-contract.json`,
validator gate, Draft → rep Confirm before any write. Facts this skill already
researched (org, contacts, CAD/ERP stack, tier) seed the payload so the rep is
asked only for what research couldn't determine.

**Create records if:** Grade A or B (Score ≥ 55), OR WGLL ≥ 12
**Skip if:** Grade C or D with WGLL < 8 — save DQ note to file only

### 4.1 Organization

Search Pipedrive for existing org by company name. If found: use it. If not found: create.

### 4.2 Person

If the contacts subagent returned a named primary contact: create Person linked to org.
If no named contact found: skip. Note in output.

### 4.3 Deal

**Deal name:** `[Company]-CADTalk ERP-[CAD System]-[ERP Name]`

| Field | Value |
|-------|-------|
| Pipeline | New ERP/PLM or Aftermarket (from opportunity subagent) |
| Stage | First stage (Connect) |
| Source System | [CAD system] |
| Target System | [ERP] |
| Org Source | Web Research — AI Agent |
| Source Channel | Outbound |
| Lead Status | New |

### 4.4 WGLL Note (Pinned)

Create a note on the deal. Pin it.

Title: `WGLL SCORE: [Advance|Qualify|Nurture|DQ] – [YYYY-MM-DD] – AI Agent – [X]/20 – [Pipeline]`

Body:
```
WGLL SCORE: [rating] — [date] — AI Agent — [X]/20 — [pipeline]

ICP Fit:         [X]/4
Pain Indicators: [X]/4
Research Depth:  [X]/4
CRM Readiness:   [X]/4
Call Prep:       [X]/4

Pain:    [one sentence — M hypothesis]
Trigger: [one sentence — I identification]
Pricing: $[subscription]/yr | Y1: ~$[total]
```

### 4.5 Activity

Create a task: "Review AI prospect analysis — [Company]"
Due: Tomorrow. Assigned to Jeff Brickler.

---

## Phase 5: Save to Deal Desk

Save the full report to:

`C:\Users\JeffBrickler\OneDrive - Solutionsx, LLC\ClaudeCoWork\Deal Desk\deals\[CompanyName]\PROSPECT-ANALYSIS.md`

Create the folder if it doesn't exist.

---

## Output File: PROSPECT-ANALYSIS.md

```markdown
# Prospect Analysis: [Company Name]

**Date:** [YYYY-MM-DD]
**URL:** [url]
**Prospect Score:** [X]/100 — Grade [A|B|C|D]
**WGLL Score:** [X]/20 — [Advance|Qualify|Nurture|DQ]
**Pipeline:** [Aftermarket | New ERP/PLM | Expansion | DQ]

---

## Snapshot

| Field | Value |
|-------|-------|
| Company | [name] |
| CAD System | [system] |
| ERP System | [ERP + class] |
| Manufacturing Model | [ETO/CTO/MTO/Unknown] |
| Engineers | [estimate] |
| Revenue | [estimate] |
| Incumbent | [Manual/DIY Scripts/SharpSync/QBuild/Arena/Unknown] |
| Primary Contact | [name, title, LinkedIn] |
| Pipeline | [pipeline] |

---

## Score Breakdown

| Dimension | Score | Weight | Weighted | Key Finding |
|-----------|-------|--------|----------|-------------|
| Company Fit | [X]/100 | 25% | [X] | [one-line] |
| Contact Access | [X]/100 | 20% | [X] | [one-line] |
| Opportunity Quality | [X]/100 | 20% | [X] | [one-line] |
| Competitive Position | [X]/100 | 15% | [X] | [one-line] |
| Outreach Readiness | [X]/100 | 20% | [X] | [one-line] |
| **TOTAL** | | **100%** | **[X]/100** | |

---

## WGLL Scorecard

| Dimension | Score | Evidence |
|-----------|-------|----------|
| ICP Fit | [X]/4 | [evidence] |
| Pain Indicators | [X]/4 | [evidence] |
| Research Depth | [X]/4 | [evidence] |
| CRM Readiness | [X]/4 | [evidence] |
| Call Prep Quality | [X]/4 | [evidence] |
| **Total** | **[X]/20** | **[Advance/Qualify/Nurture/DQ]** |

---

## Company Analysis

[Full output from sales-company subagent narrative]

---

## Contact Intelligence

[Full output from sales-contacts subagent — buying committee table + narrative]

---

## Opportunity Assessment

[Full output from sales-opportunity subagent — MEDDPICC hypotheses + pricing + narrative]

---

## Competitive Position

[Full output from sales-competitive subagent — incumbent + displacement angle + narrative]

---

## Outreach Plan

[Full output from sales-strategy subagent — draft email + follow-up cadence + narrative]

---

## Pipedrive

| Record | Status |
|--------|--------|
| Organization | [Created / Found existing] |
| Person | [Created / Skipped] |
| Deal | [Deal name — Pipeline — Stage] |
| WGLL Note | [Pinned] |
| Activity | [Created — due tomorrow] |

---

## Next Steps

1. [AE first action — outreach or partner engagement]
2. [Second priority]
3. [Watch for: specific trigger that would increase urgency]

---

*Generated by AI Agent — /ct-prospect — [date]*
```

---

## Terminal Display

```
=== CADTALK PROSPECT ANALYSIS ===

Company:       [name]
URL:           [url]
Date:          [YYYY-MM-DD]

Prospect Score: [X]/100 — Grade [A|B|C|D]
WGLL Score:    [X]/20 — [ADVANCE|QUALIFY|NURTURE|DQ]

Score Breakdown:
  Company Fit:          [XX]/100
  Contact Access:       [XX]/100
  Opportunity Quality:  [XX]/100
  Competitive Position: [XX]/100
  Outreach Readiness:   [XX]/100

CAD:     [system]
ERP:     [name] ([class])
Model:   [ETO|CTO|MTO]
Pain:    [one-line hypothesis]
Trigger: [one sentence]

Incumbent: [category]
Contact:   [name, title] — [channel]

Pipedrive:
  Org:    [Created|Found]
  Person: [Created|Skipped]
  Deal:   [name] — [pipeline]
  Note:   WGLL pinned

Report:  [full file path]
=================================
```

---

## Error Handling

- URL unreachable: try alternate formats; proceed with search-only data; note limitation
- Subagent fails: assign score of 50 for that category; note in report; lower confidence
- Company not a discrete manufacturer (company subagent flags disqualification): skip Pipedrive; save DQ file; note in terminal
- Pipedrive duplicate: search before creating; update WGLL note on existing deal if found
