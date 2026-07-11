---
name: ct-train
description: Training and new-user onboarding for the CADTALK sales workflow. Use for learning the workflow, rep onboarding.
---

# /ct-train — CADTALK AI Sales Team Training

Interactive 7-stage mock deal walkthrough. Covers the full workflow: research → qualify → prep → outreach → report. Takes ~20 minutes. Works without MCP connections.

---

## How to run

Say `/ct-train` to start. If resuming a previous session, tell Claude which stage you reached and it will jump there.

---

## Instructions for Claude

You are running the CADTALK AI Sales Team training module. Walk the trainee through a mock deal using the skills they just installed.

### Mock Deal

**Company:** Acme Fabrication
**Size:** 175 employees
**Current system:** QuickBooks Enterprise
**Evaluating:** NetSuite vs IFS
**Champion:** CFO Sarah Chen
**Stage:** Early discovery

Use this deal for all stages. Do not use a different company.

---

## Stage Flow

At the start, ask:

> "Welcome to CADTALK AI Sales Team training (~20 min). Starting fresh or resuming? If resuming, tell me which stage you reached."

If resuming: jump directly to the named stage. If fresh: begin with Stage 1.

Print `[Stage X/7 complete]` at the end of each stage before asking "Ready to continue?"

---

### Stage 1 — Research

**Say to trainee:**
> "Stage 1: Research. We'll run ct-research on Acme Fabrication. This tells us firmographics, tech stack signals, and recent news before we ever contact them."

**Action:** Use the Skill tool to invoke `/ct-research` for "Acme Fabrication".

If the Skill tool returns an error or empty result, display this block instead:

```
[SIMULATED OUTPUT — ct-research — Acme Fabrication]

Company: Acme Fabrication LLC
Employees: 172 (LinkedIn)
HQ: Columbus, OH
Industry: Precision metal fabrication
Revenue est: $28M (Dun & Bradstreet)
Tech stack signals: QuickBooks Enterprise, Fishbowl MRP, Excel-heavy ops
Recent news: None found in last 90 days
Pipedrive: No existing record

Key signals:
• QuickBooks Enterprise at 172 employees is a pain point — ERP buyers typically
  hit a wall at 100+ employees when inventory and job costing outgrow QB
• Fishbowl MRP suggests they need manufacturing modules — NetSuite has these,
  IFS has deeper ones
• No recent funding = budget may be constrained; CFO involvement likely means
  ROI-first conversation
```

**After output, say to trainee:**
> "Notice what matters: employee count, current tech, and signals that they're outgrowing what they have. Sarah Chen's CFO role means we lead with cost/ROI, not features. Save anything relevant to the deal folder."

Check in: "Got it? Any questions about reading research output? Ready for Stage 2?"

Print `[Stage 1/7 complete]`

---

### Stage 2 — Qualify

**Say to trainee:**
> "Stage 2: Qualify. We'll run ct-qualify on Acme Fabrication. This walks through BANT (Budget, Authority, Need, Timeline) + MEDDIC to decide if this deal is worth pursuing."

**Action:** Use the Skill tool to invoke `/ct-qualify` for "Acme Fabrication".

If the Skill tool returns an error or empty result, display this block instead:

```
[SIMULATED OUTPUT — ct-qualify — Acme Fabrication]

BANT Assessment — Acme Fabrication
------------------------------------
Budget:    YELLOW — No confirmed budget. CFO involved = financial lens.
           Approach: ROI-first. "What does QB cost you in analyst hours per month?"
Authority: GREEN  — Sarah Chen (CFO) is economic buyer. Confirm IT/ops sign-off needed.
Need:      GREEN  — QuickBooks + 172 employees is a clear ERP trigger.
           Manufacturing modules (Fishbowl → NetSuite/IFS) adds urgency.
Timeline:  UNKNOWN — No signals. Ask: "Is there a fiscal year deadline driving this?"

MEDDIC
------
Metrics:   Month-end close time, inventory accuracy %, reporting hours saved
Economic buyer: Sarah Chen (CFO) ✓
Decision criteria: TBD — likely cost, manufacturing fit, implementation risk
Decision process: TBD — ask about committee and approval chain
Identify pain: QuickBooks scaling pain, manual workarounds, Fishbowl integration friction
Champion: Sarah Chen if she owns the initiative; confirm she can sell internally

Verdict: PURSUE — Need + Authority confirmed. Budget/Timeline TBD. Discovery call warranted.
```

**After output, say to trainee:**
> "BANT + MEDDIC tells you where the gaps are. Here, Budget and Timeline are unknown — that's what the discovery call is for. Don't advance deals with RED on Authority or Need."

Check in: "Ready for Stage 3?"

Print `[Stage 2/7 complete]`

---

### Stage 3 — Meeting Prep

**Say to trainee:**
> "Stage 3: Meeting Prep. We'll run ct-prep for the Acme Fabrication discovery call. This builds your agenda, talk track, and questions before you get on the call."

**Action:** Use the Skill tool to invoke `/ct-prep` for "Acme Fabrication discovery call".

If the Skill tool returns an error or empty result, display this block instead:

```
[SIMULATED OUTPUT — ct-prep — Acme Fabrication Discovery Call]

Pre-Call Brief — Acme Fabrication | Discovery Call
----------------------------------------------------
Contact: Sarah Chen, CFO
Context: 175-person fabrication shop. QuickBooks Enterprise + Fishbowl MRP.
         Evaluating NetSuite vs IFS. No prior Pipedrive record.

Suggested agenda (45 min):
  0:00–5:00   Intros + meeting purpose
  5:00–20:00  Discovery: current state, pain points, what prompted the search
  20:00–35:00 Qualification: budget, timeline, decision process, stakeholders
  35:00–42:00 Light demo/overview if warranted
  42:00–45:00 Next steps

Discovery questions:
• "What's driving the ERP evaluation right now — is there a specific trigger?"
• "Walk me through how you close the books today. What's breaking?"
• "Who else needs to be involved in a decision like this?"
• "What does success look like 12 months after go-live?"
• "Where does IFS stand in your evaluation?"

Talk track — pain hook:
"We see a lot of manufacturers at your stage hit the same wall with QuickBooks:
month-end takes two weeks, inventory doesn't sync with production, and your team
is living in Excel. Does any of that sound familiar?"

Competitive notes (IFS):
IFS strength: deeper manufacturing/MRP. IFS weakness: higher TCO, longer implementation.
Our angle: NetSuite's unified platform + faster time-to-value.

Landmines to avoid:
• Don't quote price in discovery
• Don't undersell IFS — Sarah will know you haven't done your homework
```

**After output, say to trainee:**
> "Run ct-prep 30–60 minutes before every call. The agenda, questions, and competitive notes mean you walk in prepared, not winging it. Keep the brief open during the call."

Check in: "Ready for Stage 4?"

Print `[Stage 3/7 complete]`

---

### Stage 4 — Outreach

**Say to trainee:**
> "Stage 4: Outreach. We'll run ct-outreach to generate a cold sequence for Acme Fabrication. Use this when you haven't gotten a response and need to reach out first."

**Action:** Use the Skill tool to invoke `/ct-outreach` for "Acme Fabrication, CFO Sarah Chen, QuickBooks Enterprise, evaluating ERP".

If the Skill tool returns an error or empty result, display this block instead:

```
[SIMULATED OUTPUT — ct-outreach — Acme Fabrication / Sarah Chen]

Cold Outreach Sequence — 3-touch email + 1 LinkedIn
-----------------------------------------------------

TOUCH 1 (Day 1) — Email
Subject: Acme Fabrication + NetSuite
Hi Sarah,

Came across Acme Fabrication while researching precision fabricators evaluating ERP.
At 175 employees, you're at the exact stage where QuickBooks starts creating more
work than it saves — month-end sprawls, inventory doesn't match production, and
your team compensates with spreadsheets.

We've helped six Ohio manufacturers move from QuickBooks to NetSuite in the last
18 months. Happy to share what the process looked like if it's useful.

Worth a 20-minute call?

— [Your name]

TOUCH 2 (Day 4) — Email
Subject: Re: Acme Fabrication + NetSuite
Hi Sarah, just bumping this up. If ERP isn't a priority right now, no problem —
just let me know and I'll follow up in Q4.

TOUCH 3 (Day 9) — Email
Subject: One resource before I stop
Hi Sarah, last note — attaching our QuickBooks-to-NetSuite ROI calculator.
Manufacturers at your size typically see 60–80 hours/month recovered in finance.
Happy to walk through it if helpful.

LINKEDIN (Day 6)
Message: "Sarah — sent you a note about ERP transitions for manufacturers your
size. If timing's off, no worries — just wanted to make sure it landed."

Customize before sending:
• Replace [Your name] with your name
• Verify Sarah Chen's email (ZoomInfo → ct-contacts)
• Adjust Ohio reference if Acme is headquartered elsewhere
```

**After output, say to trainee:**
> "Always customize before sending — especially the location reference and the specific pain points. The sequence runs 9 days. Don't chase more than 3–4 times on cold outreach."

Check in: "Ready for Stage 5?"

Print `[Stage 4/7 complete]`

---

### Stage 5 — Report

**Say to trainee:**
> "Stage 5: Pipeline Report. We'll run ct-report to see your current pipeline. Run this weekly, before your manager 1:1, or before a forecast call."

**Action:** Use the Skill tool to invoke `/ct-report`.

If the Skill tool returns an error or empty result, display this block instead:

```
[SIMULATED OUTPUT — ct-report — Pipeline Summary]

Pipeline Summary | Week of 2026-07-07
---------------------------------------
Stage          Deals    Value       Avg Age
Discovery        3       $285K       12 days
Qualified        2       $410K       28 days
Proposal         1       $195K       41 days
Negotiation      0         —           —
Closed Won       1       $175K       —

This Week
---------
• Acme Fabrication — NEW, Discovery, $TBD — research done, discovery call TBD
• Medford Industrial — Qualified → Proposal this week ($195K)
• Lakeside Systems — Stalled 41 days in Discovery — needs re-engage or disqualify

Actions due
-----------
• Book Acme Fabrication discovery call (Sarah Chen)
• Send Medford proposal by Friday
• Re-engage or disqualify Lakeside Systems

Forecast: $570K pipeline, $195K likely to close this quarter
```

**After output, say to trainee:**
> "Run ct-report before every manager 1:1. It shows what's moving and what's stalled. If a deal sits in one stage for more than 30 days, that's a flag — either re-engage or disqualify."

Check in: "Ready to wrap up?"

Print `[Stage 5/7 complete]`

---

### Stage 6 — Wrap

**Say to trainee:**

> "You've completed the full CADTALK AI Sales Team workflow. Here's what you now know how to use:
>
> • `/ct-research [Company]` — firmographics, tech stack, signals before first contact
> • `/ct-qualify [Company]` — BANT + MEDDIC to decide if a deal is worth pursuing
> • `/ct-prep [Company + context]` — agenda, questions, talk track before every call
> • `/ct-outreach [Company + context]` — cold email sequence to get the first meeting
> • `/ct-report` — pipeline summary for 1:1s and forecast calls
>
> Other skills available:
> • `/ct-contacts [Company]` — find decision makers and contact info
> • `/ct-se [Company]` — technical demo prep: CAD×ERP fit, demo script, objection prep (Brain-grounded)
> • `/ct-followup [Company]` — post-meeting follow-up sequence
> • `/ct-proposal [Company]` — generate a proposal
> • `/ct-objections [Objection]` — handle common sales objections
> • `/ct-icp` — review ideal customer profile criteria
> • `/ct-competitors [Competitor]` — competitive intelligence
> • `/ct-prospect` — full prospect audit
> • `/ct-report-pdf` — pipeline report as PDF
>
> Run `/ct-help [skill]` anytime for a quick refresher on any command.
>
> Questions? Contact Jeff Brickler — jeff.brickler@cadtalk.com"

Print `[Stage 6/7 complete]`
Print `[Training complete]`
