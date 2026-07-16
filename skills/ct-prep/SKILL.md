---
name: ct-prep
description: Generate a CADTALK discovery-call meeting-prep brief for a company. Use for meeting prep, 'prep for [company]'.
---

## Grounding — Brain index

Sales-process, enablement, and asset doc IDs live in `references/brain-index.md`.
Load it when you need to pull a playbook, script, battlecard, or template by ID —
pull by ID directly; search is the fallback. If an ID 404s, search by title and
flag the stale ID.

# CADTALK Discovery Call Prep

Invoked as `/ct-prep <company> [meeting-date]`

You generate a complete meeting preparation brief for a CADTALK discovery call. Every section is specific to this company and this meeting — no generic filler. The brief should make the AE significantly more prepared than walking in blind, using only the cheat sheet if needed.

## CRM update — emit through sales-crm (single writer)

When Pipedrive is connected, leave this stage's standard payload by following the
sales-crm contract (`agents/sales-crm.md`) — never a hand-built field key. This
skill's row in that contract:

- Log a `discovery` activity, pin the prep summary as a note, and schedule the next
  follow-up activity (due date = the meeting date or agreed next touch).
- Note: **SQL Date** is stamped automatically by the sales-crm STAGE MOVE contract
  when the deal enters Discovery — do not set it here.

Keys resolve from `references/pipedrive-custom-fields.md`. If Pipedrive is absent,
produce the brief and note the CRM wasn't updated.

---

## Input

- `<company>`: Company name (required)
- `[meeting-date]`: Optional date/time for the meeting

---

## Step 1: Pull Existing Research

Check the Deal Desk for an existing analysis:

`C:\Users\JeffBrickler\OneDrive - Solutionsx, LLC\ClaudeCoWork\Deal Desk\deals\[CompanyName]\`

If `LEAD-QUALIFICATION.md` or `PROSPECT-ANALYSIS.md` exists: read it. Skip to Step 3.

If nothing exists: run fresh research. Fetch homepage + careers page. Search for CAD system, ERP, engineer count. Build WGLL score at a basic level.

---

## Step 2: Quick Research (if no existing file)

Minimum viable research before the call:
1. Confirm CAD system and ERP from job posts or company website
2. Estimate engineer count from LinkedIn
3. Identify manufacturing model from products page (ETO/CTO/MTO language)
4. Search for any trigger event: `"[company]" ERP implementation OR migration OR acquisition`
5. Find primary contact's LinkedIn profile: recent posts, title, tenure

---

## Step 3: WGLL Pre-Call Check

Before building the prep brief, show the current WGLL score and flag any gaps.

| Dimension | Current Score | Gap |
|-----------|--------------|-----|
| ICP Fit | [X]/4 | [confirm missing data] |
| Pain Indicators | [X]/4 | [confirm in call] |
| Research Depth | [X]/4 | [what's still unknown] |
| CRM Readiness | [X]/4 | [who else needs to be found] |
| Call Prep Quality | [X]/4 | auto-raised by this brief |

**Goal of this call:** Confirm what's inferred. Get to WGLL 12+.

---

## Step 4: Build the Cheat Sheet

This is the most important section. The AE should be able to read it in 90 seconds and walk in confident.

```
CHEAT SHEET — [Company Name] Discovery Call

1. [What they make — one sentence]
2. [CAD system + ERP — what we're connecting]
3. [Primary contact — name, title, what motivates them]
4. [Their likely current state — Manual/DIY Scripts/Unknown]
5. [The ONE thing to confirm in this call]

Opening question: "[First question to ask — specific to their situation]"
Key stat to land: "[Most relevant CADTALK stat for this company type]"
Trap to avoid: "[One thing NOT to say — e.g., don't mention QBuild if IFS partner is present]"
```

---

## Step 5: Company and Contact Snapshot

One paragraph: what they make, who they serve, growth signals, manufacturing model.

Quick-reference table:

| Field | Value |
|-------|-------|
| Company | [name] |
| Products | [what they make] |
| CAD System | [system] |
| ERP System | [ERP name + class] |
| Manufacturing Model | [ETO/CTO/MTO] |
| Engineer Count | [estimate] |
| Revenue | [estimate] |
| Incumbent | [Manual/DIY/SharpSync/QBuild/Unknown] |
| Trigger Event | [if any] |
| Meeting Contact | [name, title] |

---

## Step 6: CADTALK-Specific Discovery Questions

10 questions ordered from rapport to deep qualification. Use these verbatim or adapt to the conversation.

**Q1 — Current Process (Rapport)**
"Walk me through how an engineer gets a BOM from [CAD system] into [ERP name] today — what does that process actually look like, step by step?"

*Why ask it:* Surfaces manual entry, DIY scripts, or existing automation. Tone is curious, not leading. Establishes baseline.

*Listen for:* "They have to open the ERP and type it in" = Manual. "We have a script that does most of it" = DIY. "It's pretty automated" = investigate further.

---

**Q2 — Volume and Time (Pain quantification)**
"How much time would you estimate your engineering team spends on that process in a given week — just the data entry part?"

*Why ask it:* Starts the ROI conversation without pitching.

*Listen for:* Any number above 5 hrs/week is quantifiable pain. "Not sure" = opportunity to estimate together.

---

**Q3 — Engineering Change Propagation**
"When an engineer makes a revision in [CAD system], how does that change get reflected in [ERP name]? How long does that typically take?"

*Why ask it:* Surfaces EC chaos — the most expensive pain point.

*Listen for:* "They have to remember to update it" or "There's a delay" = strong pain signal.

---

**Q4 — Errors and Impact**
"What happens when a BOM error reaches the shop floor? How often does that happen?"

*Why ask it:* Surfaces the cost of errors — this is where ROI becomes real.

*Listen for:* Dollar figures, rework stories, production delays, customer impact.

---

**Q5 — Current Integration**
"Is anyone maintaining a custom script or integration for this, or is it fully manual?"

*Why ask it:* Confirms incumbent category. DIY scripts create migration urgency; manual means pure education.

*Listen for:* "We built something in-house" = DIY risk/opportunity. "It's all manual" = Category 4.

---

**Q6 — Success Definition**
"What would need to be true for you to say an integration project was a success, six months after go-live?"

*Why ask it:* Surfaces decision criteria (D in MEDDPICC) before pitching.

*Listen for:* Time metrics, error rate, engineer satisfaction, IT maintenance burden.

---

**Q7 — Buying Committee**
"Who else is involved in an evaluation like this — would IT need to be part of it? Finance?"

*Why ask it:* Maps the buying committee. Identifies Economic Buyer and Technical Evaluator.

*Listen for:* IT Director involvement (technical evaluator), CFO or Controller (economic buyer for >$20K), procurement process.

---

**Q8 — Timeline**
"Is there anything on the timeline driving urgency — an ERP migration, a new facility, a go-live date, or something else?"

*Why ask it:* Identifies trigger events and pipeline routing (New ERP vs. Aftermarket).

*Listen for:* "We're migrating to [ERP] cloud" = New ERP/PLM route. "No specific date" = Aftermarket, longer cycle.

---

**Q9 — Decision Process**
"What does your current process for evaluating and approving vendor software look like?"

*Why ask it:* Surfaces procurement gates, approval layers, and timeline.

*Listen for:* "I can approve this myself" (small company) vs. "IT and Finance both need to sign off" (longer process).

---

**Q10 — Champion and Path Forward**
"If we decided this was a fit, what would the path to a decision look like on your end — what would need to happen?"

*Why ask it:* Surfaces champion potential and decision process (D in MEDDPICC).

*Listen for:* Whether they describe themselves as the decision-maker or reference someone above them.

---

## Step 7: MEDDPICC Hypotheses to Confirm

Based on prior research, write pre-Discovery hypotheses for the AE to confirm in the call.

**M — Metrics (what success looks like):**
"Hypothesis: [X] engineers × [Y] hrs/week × $60/hr × 50 weeks = $[Z]/year in manual entry savings. Confirm engineer count and actual hours in Q2."

**D — Decision Criteria:**
"Hypothesis: They'll evaluate on (1) supported CAD and ERP, (2) implementation time, (3) maintenance burden after go-live. Confirm in Q6."

**I — Identification of Goal:**
"Hypothesis: [state the trigger or why-now]. Confirm in Q8."

**C — Competition:**
"Hypothesis: [Manual/DIY Scripts]. Watch for: [QBuild risk flag if IFS deal]."

---

## Step 8: Competitive Context for This Call

| If the contact mentions... | Response |
|---------------------------|----------|
| "We looked at QBuild" | "What was your take on the approval-per-push model? CADTALK can run unattended if that matters to your team." |
| "We built something in-house" | "Custom scripts are the most common thing we replace. What happens to it when [ERP] pushes a major update?" |
| "We tried [other tool] and it didn't work" | "What broke? That usually tells us something about what your BOM structure needs." |
| "We're not sure we need this" | "How much time does your team spend on BOM re-entry today? That usually answers the question." |

---

## Step 9: Objections to Expect

**"We're happy with how we're doing it."**
Feel: Totally fair — a lot of teams get used to the process.
Felt: Most engineering managers say the same thing until they quantify the hours.
Found: At a 20-engineer shop, that's usually $60–80K/year in pure labor. Once they run that number, it changes the conversation.

**"We don't have budget for this."**
"The budget question usually follows the ROI question. Once we know how many hours your team is spending on this, we can show whether the math works in year one. Most customers see payback in under 6 months."

**"It's too complex to implement."**
"Implementation runs 20–30 days. That's faster than most ERP customization projects. We do the heavy lifting — your team gives us 2–3 hours total. Worth at least walking through what it would look like?"

**"We'd need IT to evaluate this."**
"Totally makes sense. Can we schedule a follow-up with IT included? I can walk them through the architecture and answer questions about the connector and maintenance model."

**"We already tried an integration and it didn't stick."**
"What went wrong? That's usually a specific issue with mapping or rules — both of which CADTALK handles differently than most DIY approaches. Worth understanding before we go further."

---

## Step 10: Meeting Success Metrics

| Level | What it looks like |
|-------|--------------------|
| **Minimum** | Confirmed CAD system, ERP, and that manual BOM entry is happening. Got a named contact for IT or Finance. |
| **Target** | Quantified pain (hours/week or error cost). Identified timeline driver. Agreed on next step with specific date. |
| **Stretch** | Champion willing to schedule a demo with IT. Economic buyer named and willing to attend demo. Pain quantified and compared to CADTALK pricing. |

---

## Step 11: Agenda Template

### 30-Minute Call
| Time | Activity |
|------|----------|
| 0:00–2:00 | Rapport — open with company-specific observation (cheat sheet opening question) |
| 2:00–15:00 | Discovery — Q1 through Q5 (process, volume, EC, errors, incumbent) |
| 15:00–22:00 | Conditional demo context — "Can I show you what the push from [CAD system] to [ERP name] looks like? Takes 2 minutes." |
| 22:00–27:00 | Q6–Q10 — success criteria, buying committee, timeline, decision process |
| 27:00–30:00 | Next step — propose specific date for demo with IT included |

### 60-Minute Call
| Time | Activity |
|------|----------|
| 0:00–5:00 | Rapport + cheat sheet open |
| 5:00–25:00 | Full discovery — all 10 questions |
| 25:00–45:00 | Live demo with their CAD type + ERP |
| 45:00–55:00 | Objection handling + pricing range introduction |
| 55:00–60:00 | Next step with specific date |

---

## Save to Deal Desk

Save the prep brief to:

`C:\Users\JeffBrickler\OneDrive - Solutionsx, LLC\ClaudeCoWork\Deal Desk\deals\[CompanyName]\MEETING-PREP.md`

---

## Output File: MEETING-PREP.md

```markdown
# Meeting Prep: [Company Name]

**Date:** [YYYY-MM-DD] | **Meeting:** [date/time if provided]
**Contact:** [name, title]
**WGLL Pre-Call:** [X]/20 — gaps to confirm

---

## CHEAT SHEET

[5 things + opening question + key stat + trap to avoid]

---

## Company + Contact Snapshot

[Paragraph + quick-reference table]

---

## WGLL Gap Tracker

[Table: current score per dimension and what to confirm]

---

## CADTALK Discovery Questions

[All 10 questions with Why and Listen For]

---

## MEDDPICC Hypotheses

[Pre-call hypotheses for M, D, I, C]

---

## Competitive Context

[What to do if they mention each competitor/incumbent]

---

## Objections to Expect

[5 objections with Feel-Felt-Found responses]

---

## Success Metrics

[Minimum, target, stretch]

---

## Suggested Agenda

[30-min or 60-min based on meeting type]

---

*Generated by AI Agent — /ct-prep — [date]*
```

---

## CADTALK Voice (apply before output)

Before returning any written copy (email, message, recap, script, proposal), apply the CADTALK voice: follow `references/cadtalk-voice-reference.md`, or run `/ct-voice` in REVIEW mode. Personal voice, no AI slop, Strunk & White clarity, CADTALK brand — one pass. Nothing goes out unvoiced.

## Hygiene sweep (final step)

After this skill's output is delivered, run the CRM hygiene sweep
(`skills/ct-hygiene/SKILL.md`, Sweep mode) with this run's artifacts as the
source — it pushes what this run learned (fields, contacts, participants) into
Pipedrive through the sales-crm contract. Batch review table first; writes only
after the rep confirms. If the deal/org can't be resolved in Pipedrive, skip
silently.
