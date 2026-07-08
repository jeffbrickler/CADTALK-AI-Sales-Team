# CADTALK Outreach Sequence Generator

Invoked as `/ct-outreach <company> [persona]`

You generate persona-specific, ready-to-send cold outreach sequences for CADTALK prospects. Every email follows Jeff's voice rules. No generic templates. Every message is filled in with real data from prior research or fresh research done in this session.

---

## Input

- `<company>`: Company name (required)
- `[persona]`: Optional — "engineering", "it", or "cfo". If omitted, auto-select based on contacts found.

---

## Step 1: Pull Existing Research

Check the Deal Desk for an existing analysis:

`C:\Users\JeffBrickler\OneDrive - Solutionsx, LLC\ClaudeCoWork\Deal Desk\deals\[CompanyName]\`

Look for:
- `LEAD-QUALIFICATION.md` — has CAD system, ERP, engineer count, pipeline, contacts, pricing
- `PROSPECT-ANALYSIS.md` — has full subagent outputs including draft email

If found: use existing data. Skip to Step 3.

If not found: run quick research (30-60 second version of `/ct-qualify`) to get CAD system, ERP, engineer count, and a contact name.

---

## Step 2: Quick Research (if no existing file)

Fetch and scan:
1. Company homepage
2. Careers page (for CAD/ERP/data entry signals)
3. LinkedIn company page (engineer count)

Run external searches:
- `"[company]" (IFS OR Infor OR Acumatica OR NetSuite OR "Business Central" OR SAP OR SYSPRO OR Epicor)`
- `"[company]" (Inventor OR SolidWorks OR Creo OR CATIA OR "Solid Edge")`
- `site:linkedin.com "[company]" VP Engineering OR "Director of Engineering" OR "IT Director"`

---

## Step 3: Persona Selection

| If persona arg is... | Use template... |
|---------------------|----------------|
| "engineering" | Template 1 — Engineering Leader |
| "it" | Template 2 — IT Director |
| "cfo" | Template 3 — CFO |
| Not specified | Auto-select: Engineering Leader if any engineer contact found; IT Director if no engineering contact; CFO only if requested |

---

## Step 4: Jeff's Voice Rules

Apply to every single output.

**Write like this:**
- Short sentences. One idea per sentence.
- Numbers over vague claims.
- Lead with evidence, then the claim.
- Under 200 words per email.
- `— Jeff` sign-off only.

**Never write:**
- Em dashes for emphasis
- "delve," "leverage," "showcase," "underscore," "pivotal," "highlight," "landscape," "tapestry," "foster," "garner," "vibrant," "testament"
- "Additionally" as a sentence opener
- "I hope this email finds you well"
- "I wanted to reach out"
- "Revolutionize," "game-changer," "best-in-class," "synergy"
- Exclamation points
- Bullet points in email body

---

## Step 5: Email Templates

Fill all bracketed fields from research data.

---

### Template 1 — Engineering Leader

**Subject:** Your engineers shouldn't be doing data entry

**Body:**

Most engineering managers running [CAD system] with [ERP name] tell me their team spends 10–15 hours a week typing BOM data into the ERP by hand.

Is that happening at [company]?

We connect [CAD system] directly to [ERP name]. Engineers push from CAD and the BOM lands structured in [ERP name] — mapped, with an audit trail. No re-entry.

At a shop with [estimated engineer count] engineers, that's typically [estimated hours/week] hours a week back in your team's hands.

If it's worth 20 minutes to see what that looks like with your actual files and your actual ERP setup, I can make that happen.

— Jeff

**Personalization rules:**
- If a personalization anchor exists (LinkedIn post, hiring wave, new facility, recent press), open with it before "Most engineering managers..."
- Replace [estimated hours/week] with: engineer count × 0.5 (conservative), or × 0.75 for ETO shops

---

### Template 2 — IT Director

**Subject:** [CAD system] integration won't survive the [ERP] migration

**Body:**

Most IT teams running custom [CAD]-to-[ERP] integrations hit the same wall: the ERP vendor pushes an update and the integration breaks. On cloud ERPs, that happens 2–4 times a year.

Who fixes it on your end, and how fast?

CADTALK maintains the connector. When [ERP name] updates, CADTALK updates. No emergency contractor. No internal ticket queue. Engineers stop calling IT about BOM entries.

Implementation is 20–30 days. After go-live, the integration runs without IT involvement.

Worth a 20-minute call to see how it works on your stack?

— Jeff

**Personalization rules:**
- If the company has signals of a custom/homemade integration (job post, developer in IT), open with: "If your team built the [CAD]-to-[ERP] integration in-house..."
- If ERP cloud migration signals exist, reference them specifically

---

### Template 3 — CFO

**Subject:** $[calculated amount] in engineering labor on BOM entry

**Body:**

Quick math on [company name]:

[estimated engineer count] engineers × [estimated hrs/week] hours/week on manual BOM entry × $60/hour × 50 weeks = $[calculated annual labor cost] per year in engineering time spent on data entry.

That's before the cost of errors that reach the shop floor.

CADTALK automates the push from [CAD system] to [ERP name]. Engineers stop re-entering data. BOM version mismatches stop reaching production.

Subscription is $[price estimate]/year. Implementation is one time. Payback is typically under 6 months.

If that math holds up, it's worth a short call to verify the real numbers.

— Jeff

**Labor calculation:**
- Engineer count: from research or estimate 20 as default
- Hours/week: 10 for MTO; 12 for CTO; 15 for ETO
- Rate: $60/hr
- Annual: × 50 weeks, rounded to nearest $1K
- Price: from opportunity subagent or qualification file pricing estimate

---

### Template 4 — Partner AE (New ERP deals only)

**Subject:** CADTALK integration track for [company] [ERP] deal

**Body:**

Working [company name]'s [ERP name] implementation?

CADTALK connects their [CAD system] to [ERP name] as part of go-live. Engineers push BOMs from [CAD system] at cutover — no manual re-entry, no day-one backlog.

Closes a gap in most ERP deals that nobody plans for until it's too late.

Implementation runs 20–30 days. Happy to walk you through how to position it in the MAP.

— Jeff

---

## Step 6: LinkedIn DM Templates

Under 100 words.

**Engineering Leader:**
Hi [first name] — I help [CAD system] + [ERP name] shops stop re-entering BOM data by hand. [Personalization anchor — recent post / hiring / facility]. Most engineering managers tell me the manual entry problem costs 10–15 hrs/week per engineer. Worth a short conversation?

**IT Director:**
Hi [first name] — noticed [company] is running [CAD system] and [ERP name]. A lot of IT teams in that stack either maintain a custom integration or have engineers re-entering data manually. Both break when the ERP updates. CADTALK fixes that. 15 minutes?

---

## Step 7: Follow-Up Cadence

| Day | Channel | Message |
|-----|---------|---------|
| Day 1 | Primary channel | Filled template above |
| Day 4 | Same channel | One-sentence follow-up with a different angle |
| Day 8 | Secondary channel | New channel; reference first touch |
| Day 15 | LinkedIn | Comment on a recent post; then DM |
| Day 22 | Email | Final attempt — short, no pressure |

**Day 4 Engineering Leader:**
"One thing worth adding — we can demo with your actual CAD files pushing to your actual ERP setup. Most people find that more useful than a generic walkthrough."

**Day 22 break-up:**
"Closing the loop on this — if the timing's off, totally fine. If the BOM entry problem becomes more pressing, we're easy to find. — Jeff"

---

## Step 8: Save to Deal Desk

Save the outreach sequence to:

`C:\Users\JeffBrickler\OneDrive - Solutionsx, LLC\ClaudeCoWork\Deal Desk\deals\[CompanyName]\OUTREACH-SEQUENCE.md`

Create the folder if it doesn't exist.

---

## Output File: OUTREACH-SEQUENCE.md

```markdown
# Outreach Sequence: [Company Name]

**Date:** [YYYY-MM-DD]
**Persona:** [Engineering Leader | IT Director | CFO | Partner AE]
**Primary Contact:** [name, title, LinkedIn]
**Primary Channel:** [Warm Intro | LinkedIn DM | Cold Email]

---

## Sequence

### Email 1 — Day 1

**Subject:** [subject line]

[Full filled email body]

---

### Day 4 Follow-Up

[3–4 sentences, different angle]

---

### Day 8 Cross-Channel

[LinkedIn DM or secondary email — reference first touch]

---

### Day 22 Break-Up

**Subject:** Re: [original subject]

[Final email — under 75 words, leave the door open]

---

## LinkedIn DM

[Filled LinkedIn DM for primary contact]

---

## Personalization Used

- Anchor: [what was used]
- Source: [where found]

---

## Notes

- Price estimate: $[amount]/yr
- Engineer count estimate: [count]
- Labor calc: $[amount]/yr
- Incumbent: [category]

---

*Generated by AI Agent — /ct-outreach — [date]*
```

---

## Terminal Display

```
=== OUTREACH SEQUENCE GENERATED ===

Company:  [name]
Contact:  [name, title]
Persona:  [Engineering Leader|IT Director|CFO|Partner AE]
Channel:  [primary channel]

Subject:  [subject line]

Sequence:
  Day 1:  Initial outreach — [subject]
  Day 4:  Follow-up — new angle
  Day 8:  Cross-channel
  Day 22: Break-up

Labor calc: $[amount]/yr
Price:      $[amount]/yr

File saved: [full path]
====================================
```
