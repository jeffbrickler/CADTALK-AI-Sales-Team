---
name: ct-help
description: Help with plugin commands. Use for command reference, 'how do I use [skill]'.
---

# /ct-help — CADTALK AI Sales Team Reference

Quick reference for all CADTALK AI Sales Team skills.

- `/ct-help` — full skill map
- `/ct-help [skill]` — detail block for that skill (e.g., `/ct-help prep`)

---

## Instructions for Claude

If the user runs `/ct-help` with no argument, show the Full Skill Map below.

If the user runs `/ct-help [skill]`, find the matching detail block and show it. Match on the skill name or any reasonable abbreviation (e.g., "prep" → ct-prep, "report pdf" → ct-report-pdf, "icp" → ct-icp).

If the skill name is not recognized, say: "Unknown skill. Here's the full skill map:" then show the Full Skill Map.

---

## Full Skill Map

```
CADTALK AI Sales Team — Skill Map
====================================

WORKFLOW (run in this order for a new deal)
-------------------------------------------
/ct-research [Company]          Research a company before first contact
/ct-qualify [Company]           BANT + MEDDIC qualification — or Coach Mode: review/coach a live deal
/ct-score [Deal]                WGLL discovery scorecard (0–20) + Pipedrive pin
/ct-commit [Deal]               Commit gate — real-commit test + weighted forecast
/ct-prep [Company + context]    Pre-call brief, agenda, and talk track
/ct-outreach [Company + info]   Cold email + LinkedIn sequence
/ct-followup [Company]          Post-meeting follow-up sequence

DEAL TOOLS
----------
/ct-contacts [Company]          Find decision makers and contact info
/ct-se [Company]                Technical demo prep — CAD×ERP fit, demo script (Brain-grounded)
/ct-crm [what to do]            Update Pipedrive — fields, calls, notes, stage moves, queries
/ct-voice [text or request]     Write / review / coach any copy in the CADTALK voice
/ct-proposal [Company]          Generate a proposal
/ct-objections [Objection]      Handle a specific sales objection

INTELLIGENCE
------------
/ct-icp                         Review ideal customer profile criteria
/ct-competitors [Competitor]    Competitive intelligence on a named competitor
/ct-prospect [Company]          Full prospect audit (research + qualify + contacts)

PIPELINE
--------
/ct-report                      Pipeline summary (Markdown)
/ct-report-pdf                  Pipeline summary (PDF)
/ct-fulfill                     Order emails for closed-won deals (one per order → fulfillment)

ONBOARDING & ENABLEMENT
-----------------------
/ct-train                       Training walkthrough (~20 min) — or Enablement Mode: playbooks, ramp plans, battlecards, audits
/ct-setup                       First-time plugin setup

Type /ct-help [skill] for full detail on any command above.
```

---

## Detail Blocks

### ct-research

```
/ct-research [Company Name]
---------------------------
WHAT IT DOES:    Pulls firmographics, tech stack signals, recent news, and
                 Pipedrive status for a target company.

WHEN TO RUN IT:  Before any first outreach or discovery call. Run it first —
                 it feeds every other skill.

HOW TO USE IT:   /ct-research Acme Fabrication
                 /ct-research "Lakeside Systems LLC"

WHAT YOU'LL GET: Employee count, HQ location, estimated revenue, current tech
                 stack, recent news signals, and whether they're already in
                 Pipedrive.

COMMON MISTAKES:
• Skipping this and going straight to outreach — you'll miss signals that
  change your talk track entirely.
• Not saving key findings to the deal folder before moving on.
```

---

### ct-qualify

```
/ct-qualify [Company Name]
---------------------------
WHAT IT DOES:    Two modes. QUALIFY MODE (default): runs BANT + MEDDIC + WGLL
                 on a new/early prospect, routes the pipeline, creates Pipedrive
                 records. COACH MODE: reviews a live deal the AE already owns —
                 BANTED health check, 9 cycle killers, buying-committee mapping,
                 Success Plan, stuck-deal protocols, and a Deal Health Card.

WHEN TO RUN IT:  Qualify Mode after research, before booking discovery. Coach
                 Mode when a deal is stuck, dark, single-threaded, or you're not
                 sure it's real — "review this deal", "coach my AE", "why is it
                 stuck", "build a success plan".

HOW TO USE IT:   /ct-qualify Acme Fabrication
                 /ct-qualify "review the Contoso deal — stuck 40 days, champion went quiet"

WHAT YOU'LL GET: Qualify Mode — BANT scores, MEDDIC breakdown, WGLL, verdict.
                 Coach Mode — Deal Health Card, risk rating, next 48h / 7d
                 actions, and the coaching question to ask the AE.

COMMON MISTAKES:
• Treating YELLOW as GREEN — budget and timeline unknown means you still have
  work to do, not that they're qualified.
• Running the new-prospect flow on a coaching request — if the deal already
  exists, that's Coach Mode.
```

---

### ct-prep

```
/ct-prep [Company + context]
-----------------------------
WHAT IT DOES:    Builds a pre-call brief with agenda, discovery questions,
                 talk track, competitive notes, and landmines to avoid.

WHEN TO RUN IT:  30–60 minutes before any call — discovery, demo, or check-in.
                 The more context you give, the better the prep.

HOW TO USE IT:   /ct-prep Acme Fabrication discovery call
                 /ct-prep "Lakeside Systems — second call, they're comparing us to IFS"

WHAT YOU'LL GET: Suggested agenda with timing, 5–8 discovery questions, pain
                 hook talk track, competitive notes, and things to avoid saying.

COMMON MISTAKES:
• Running it the day before and not reviewing it right before the call.
• Not customizing the agenda — it's a starting point, not a script.
```

---

### ct-outreach

```
/ct-outreach [Company + context]
---------------------------------
WHAT IT DOES:    Generates a 3-touch cold email sequence plus a LinkedIn
                 message, personalized to the company and contact.

WHEN TO RUN IT:  When you need to cold-reach a prospect who hasn't engaged.
                 Also useful to restart a stalled deal.

HOW TO USE IT:   /ct-outreach "Acme Fabrication, CFO Sarah Chen, QuickBooks user"
                 /ct-outreach "Medford Industrial — stalled 30 days, re-engage"

WHAT YOU'LL GET: 3 emails spaced over 9 days + 1 LinkedIn message, with
                 subject lines, body copy, and customization notes.

COMMON MISTAKES:
• Sending without customizing — especially location references and pain points.
• More than 4 touches on cold outreach. If no response after Touch 3 + LinkedIn,
  move on or schedule a follow-up in 90 days.
```

---

### ct-followup

```
/ct-followup [Company + context]
---------------------------------
WHAT IT DOES:    Generates a post-meeting follow-up sequence: thank you email,
                 recap of what was discussed, and agreed next steps.

WHEN TO RUN IT:  Within 1 hour of ending a call while it's fresh.

HOW TO USE IT:   /ct-followup "Acme Fabrication — discovery call, CFO Sarah Chen,
                 discussed QuickBooks pain, agreed to send ROI calculator"

WHAT YOU'LL GET: A thank-you email with meeting recap, next steps, and a
                 follow-up nudge if they go quiet.

COMMON MISTAKES:
• Waiting more than 24 hours — follow-ups sent same day convert significantly
  better.
• Sending without adding the agreed next steps — that's what gets a response.
```

---

### ct-contacts

```
/ct-contacts [Company Name]
----------------------------
WHAT IT DOES:    Finds decision makers at a company with titles, LinkedIn
                 profiles, and contact info via ZoomInfo.

WHEN TO RUN IT:  After research, when you need to find the right person to
                 contact or map the buying committee.

HOW TO USE IT:   /ct-contacts Acme Fabrication
                 /ct-contacts "Acme Fabrication — looking for CFO and IT director"

WHAT YOU'LL GET: List of contacts with name, title, LinkedIn URL, email
                 (if available), and phone (if available).

COMMON MISTAKES:
• Contacting the first name you find instead of the economic buyer.
• Not cross-referencing with Pipedrive — the contact may already be in your CRM.
```

---

### ct-se

```
/ct-se [Company Name]
---------------------
WHAT IT DOES:    Builds a technical demo-prep brief — maps the prospect's CAD
                 and ERP stack to CADTALK capabilities, writes a demo script for
                 that stack, and pre-answers technical objections. Every
                 capability claim is grounded in the CADTALK Brain (or the CT
                 Outline docs when the Brain is offline) and flagged "verify with
                 a senior SE / engineering / solution architect" when neither has
                 evidence.

WHEN TO RUN IT:  Before a technical demo, once you know (or can find) their CAD
                 and ERP. Pairs with /ct-prep — /ct-prep is the AE meeting plan,
                 /ct-se is the SE demo plan.

HOW TO USE IT:   /ct-se Acme Fabrication
                 /ct-se "Lakeside Systems — Inventor + Epicor, demo Thursday"

WHAT YOU'LL GET: TECH-DEMO-PREP.md in the deal folder: stack snapshot, a
                 capability map with per-claim evidence status, a step-by-step
                 demo script with talk track, and technical objection prep.

COMMON MISTAKES:
• Treating it like /ct-prep — it's the technical layer, not business discovery.
  Run both for a technical demo.
• Demoing a capability tagged "verify with human" — confirm it with a senior SE,
  engineering, or a solution architect first.
• Running it with both the Brain and Outline offline and trusting the claims —
  the brief banners itself UNVERIFIED for a reason.
```

---

### ct-crm

```
/ct-crm [what to do]
--------------------
WHAT IT DOES:    Direct Pipedrive updates — set fields (MEDDPICC, Forecast, Tier,
                 Health), log calls, add notes, move stages, create records, or
                 query the pipeline. The single CRM write path every skill uses,
                 so a manual update and an automatic one land identically.

WHEN TO RUN IT:  Any time you need the CRM changed and aren't already inside a
                 skill that updates it for you.

HOW TO USE IT:   /ct-crm set MEDDPICC champion to Jane Smith on the Acme deal
                 /ct-crm log a discovery call, done, on Contoso; set Health Green
                 /ct-crm show me stale deals and overdue activities

WHAT YOU'LL GET: A one-line confirmation per write (record, field, new value), or
                 a clean pipeline read.

COMMON MISTAKES:
• Guessing a field key — never do it; the skill resolves keys from the reference.
• Writing Pipedrive from another skill directly instead of through this contract.
```

---

### ct-voice

```
/ct-voice [text or request]
---------------------------
WHAT IT DOES:    The one CADTALK voice system. Three modes — WRITE (produce copy),
                 REVIEW (critique with before/after fixes), COACH (build the habit).
                 Applies personal voice, anti-AI-slop, Strunk & White clarity, and
                 CADTALK brand in one pass.

WHEN TO RUN IT:  Any email, follow-up, recap, script, proposal, or post you'll
                 send — or any "does this sound on-brand?" check.

HOW TO USE IT:   /ct-voice review this cold email: [paste]
                 /ct-voice write a 3-line follow-up after a discovery no-show
                 /ct-voice coach me on my recap style

WHAT YOU'LL GET: Polished, brand-compliant, AI-free copy (WRITE), a marked-up
                 critique with fixes (REVIEW), or a coaching drill (COACH).

COMMON MISTAKES:
• Sending copy without a voice pass — the content skills apply it automatically;
  use /ct-voice for anything you wrote by hand.
```

---

### ct-proposal

```
/ct-proposal [Company + context]
---------------------------------
WHAT IT DOES:    Generates a proposal document with scope, pricing summary,
                 timeline, and ROI framing.

WHEN TO RUN IT:  After a qualified discovery call, when the prospect has asked
                 for a proposal or you're ready to advance to that stage.

HOW TO USE IT:   /ct-proposal "Acme Fabrication — 175 users, NetSuite, 6-month
                 implementation, $X ACV"

WHAT YOU'LL GET: Proposal draft with executive summary, scope, investment
                 summary, implementation timeline, and next steps.

COMMON MISTAKES:
• Sending a proposal before confirming budget exists — proposals without budget
  conversations go nowhere.
• Not customizing the ROI section — generic proposals don't close deals.
```

---

### ct-objections

```
/ct-objections [Objection]
---------------------------
WHAT IT DOES:    Returns a structured response to a specific sales objection
                 with acknowledge/reframe/close technique.

WHEN TO RUN IT:  Before a call when you expect a specific objection, or right
                 after a call when you got blindsided and need to prepare for
                 the follow-up.

HOW TO USE IT:   /ct-objections "the price is too high"
                 /ct-objections "we're happy with QuickBooks for now"
                 /ct-objections "we're also talking to IFS"

WHAT YOU'LL GET: Acknowledge, reframe, and close script for that objection,
                 plus 2–3 probing questions to dig deeper.

COMMON MISTAKES:
• Jumping to the reframe without acknowledging — prospects feel steamrolled.
• Using the script word-for-word — it's a framework, not a line to memorize.
```

---

### ct-icp

```
/ct-icp
--------
WHAT IT DOES:    Displays the CADTALK Ideal Customer Profile — the criteria
                 that define a well-qualified prospect worth pursuing.

WHEN TO RUN IT:  When you're unsure if a company fits, or when explaining
                 qualification criteria to a new contact or colleague.

HOW TO USE IT:   /ct-icp

WHAT YOU'LL GET: ICP criteria including company size range, industry verticals,
                 tech stack signals, budget indicators, and disqualifying factors.

COMMON MISTAKES:
• Treating ICP as a checklist — it's a pattern, not a binary pass/fail.
• Ignoring disqualifying factors because you like the company.
```

---

### ct-competitors

```
/ct-competitors [Competitor Name]
----------------------------------
WHAT IT DOES:    Returns competitive intelligence on a named competitor:
                 strengths, weaknesses, common objections they raise against
                 us, and how to counter them.

WHEN TO RUN IT:  When a prospect mentions a competitor, or before a call where
                 you know they're evaluating alternatives.

HOW TO USE IT:   /ct-competitors IFS
                 /ct-competitors SAP
                 /ct-competitors "Microsoft Dynamics"

WHAT YOU'LL GET: Competitor overview, where they win, where they lose, common
                 FUD they use against NetSuite, and your counter-positioning.

COMMON MISTAKES:
• Badmouthing the competitor directly — focus on your fit, not their flaws.
• Not knowing their strengths — if you can't articulate why IFS is good,
  Sarah Chen will trust you less.
```

---

### ct-report

```
/ct-report
-----------
WHAT IT DOES:    Pulls your pipeline from Pipedrive and returns a formatted
                 Markdown summary by stage with deal values, ages, and
                 action items.

WHEN TO RUN IT:  Weekly, before your manager 1:1, or before any forecast call.

HOW TO USE IT:   /ct-report

WHAT YOU'LL GET: Pipeline by stage, deal count and value, average age,
                 stalled deal flags (30+ days in stage), and priority actions.

COMMON MISTAKES:
• Running it and not acting on the stalled deals it surfaces.
• Waiting until the 1:1 to run it — run it the day before so you have time
  to update Pipedrive first.
```

---

### ct-report-pdf

```
/ct-report-pdf
---------------
WHAT IT DOES:    Same as ct-report but generates a formatted PDF suitable for
                 sharing with your manager or in a meeting.

WHEN TO RUN IT:  When you need to share pipeline with someone who doesn't have
                 access to Pipedrive or Claude.

HOW TO USE IT:   /ct-report-pdf

WHAT YOU'LL GET: A PDF file saved to your deal-desk folder with the same
                 pipeline data as ct-report in a formatted layout.

COMMON MISTAKES:
• Using this for your own review — ct-report is faster for daily use.
  Save the PDF version for sharing externals.
```

---

### ct-prospect

```
/ct-prospect [Company Name]
----------------------------
WHAT IT DOES:    Full prospect audit in one command: research + qualification
                 + contact mapping + outreach recommendation.

WHEN TO RUN IT:  When you want a comprehensive view of a new prospect without
                 running each skill individually.

HOW TO USE IT:   /ct-prospect Acme Fabrication
                 /ct-prospect "Lakeside Systems"

WHAT YOU'LL GET: Research summary, BANT/MEDDIC assessment, key contacts,
                 pursue/hold/disqualify verdict, and recommended next step.

COMMON MISTAKES:
• Using this instead of ct-research for a quick lookup — ct-prospect goes deep
  and takes longer. Use ct-research for speed, ct-prospect for thoroughness.
```

---

### ct-fulfill

```
/ct-fulfill
------------
WHAT IT DOES:    Turns closed-won deals into per-deal order-submission emails to
                 fulfillment@cadtalk.com, built to the New Order Processing SOP.
                 One order = one email (a single batch email gets bounced back).
                 Applies partner rules (Arena/IFS/Infor/direct), PO handling,
                 pod, and HOLD conditions, in the CADTALK internal voice.

WHEN TO RUN IT:  When deals close and you need to hand them to order processing —
                 "send these orders to fulfillment", "process this order".

HOW TO USE IT:   /ct-fulfill
                 /ct-fulfill "the three deals that closed this week"

WHAT YOU'LL GET: Fulfillment-Order-Emails_v1.md — copy-paste-ready emails, one per
                 order, each with the Pipedrive link, order summary, partner flags,
                 pod, and a single clear ask (process or hold + why).

COMMON MISTAKES:
• Sending one batch email — order processing works one order at a time.
• Inventing quote-only fields — write "see signed quote"; never guess a PO,
  license count, or term.
• Processing a HOLD order — missing contact, PO "to be provided" (non-Arena), or
  Phase 2 work holds, it doesn't process.

NOTE: ct-fulfill only reads Pipedrive (through the sales-crm contract) and never
      writes it or sends the email — it produces the copy for you to send.
```

---

### ct-train

```
/ct-train
----------
WHAT IT DOES:    Two modes. TRAINING (default): interactive 7-stage mock-deal
                 walkthrough of the full workflow (~20 min, no MCP needed).
                 ENABLEMENT: builds team tools — sales playbook, 30/60/90 ramp
                 plan, weekly sales-meeting agenda, competitive battlecard, or an
                 enablement audit — via references/sales-enablement.md.

WHEN TO RUN IT:  Training on a new rep's first week. Enablement when a manager
                 needs a playbook, ramp plan, meeting format, battlecard, or audit.

HOW TO USE IT:   /ct-train
                 /ct-train "build a 30/60/90 ramp plan for a new AE"
                 /ct-train "run an enablement audit"

WHAT YOU'LL GET: Training — a guided walkthrough with check-ins per stage.
                 Enablement — the requested deliverable, pulling CADTALK specifics
                 from /ct-icp, /ct-qualify, /ct-objections, /ct-competitors and
                 voiced via the voice reference.

COMMON MISTAKES:
• Reinventing CADTALK facts in an enablement build — pull them from the content
  skills; the reference is structure, not content.
```
