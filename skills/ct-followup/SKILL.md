# CADTALK Follow-Up Sequence Generator

Invoked as `/ct-followup <company> [scenario]`

You generate stage-specific follow-up sequences for CADTALK prospects after initial engagement. These are NOT cold outreach — they're follow-ups after a meeting, demo, or proposal. Every email adds new value, references what was discussed, and moves toward a concrete next step.

---

## Input

- `<company>`: Company name (required)
- `[scenario]`: Optional — "discovery", "demo", "proposal", "ghost", or "nurture". If omitted, ask the user which scenario fits.

---

## Step 1: Pull Context

Check the Deal Desk for an existing analysis:

`C:\Users\JeffBrickler\OneDrive - Solutionsx, LLC\ClaudeCoWork\Deal Desk\deals\[CompanyName]\`

Read any files present:
- `LEAD-QUALIFICATION.md` — pipeline, CAD/ERP, pain hypothesis, contacts
- `PROSPECT-ANALYSIS.md` — full subagent outputs
- `MEETING-PREP.md` — what was discussed in the last meeting

If no files exist, ask the user:
1. What CAD system and ERP do they use?
2. Who did you meet with (name, title)?
3. What were the 2–3 key takeaways from the conversation?
4. What next step did you agree to?
5. What's the prospect's temperature (hot/warm/cool/cold)?

---

## Step 2: Select Scenario

| Scenario | Use When |
|----------|----------|
| `discovery` | After a first discovery call |
| `demo` | After a CAD→ERP demo walkthrough |
| `proposal` | After sending a CADTALK quote or proposal |
| `ghost` | Prospect stopped responding |
| `nurture` | Good ICP fit, not ready to buy yet |

---

## Jeff's Voice Rules

Apply to every email:
- Short sentences. Under 200 words. `— Jeff` sign-off.
- No em dashes for emphasis. No AI vocabulary (leverage, underscore, pivotal, etc.)
- No "just checking in." No "bumping this to the top of your inbox."
- Every email must add something new — a stat, a case reference, a question, or a resource.

---

## Scenario 1: Post-Discovery Follow-Up

**3 emails. Send timeline: Same day, +3 days, +7 days.**

### Email 1 — Same Day (Within 2 Hours)

**Subject:** [Topic from the call — not "Great meeting today"]

Open with one specific thing they said — shows you were listening.

Body structure:
- What they shared about their current process (1 sentence — paraphrase back)
- 3 key points from the conversation (numbered list is fine here)
- Agreed next step with a specific date/time
- Confirmation question: "Does this capture what we discussed?"

Under 100 words. `— Jeff`

### Email 2 — Day 3

**Subject:** [Reference a pain point they mentioned]

Open with a relevant reference tied to what they described.

Body:
- Share the labor cost estimate: "[X] engineers × [Y] hrs/week × $60/hr × 50 weeks = $[amount]/year in manual BOM entry"
- Connect it to what they described in the call — "That tracks with what you said about [specific thing they mentioned]"
- Offer: "I can put together a more precise estimate once we know [specific thing to confirm in next call]"
- Soft next step

Under 80 words. `— Jeff`

### Email 3 — Day 7

**Subject:** Forward-looking — their goal, not the sale

Open with a question about where they are.

Body:
- Reference their timeline or initiative (ERP migration date, fiscal year, headcount growth)
- Share one CADTALK stat relevant to their situation:
  - For ETO shops: "Most ETO shops we work with see their BOM errors drop to near-zero within 60 days of go-live."
  - For migration-triggered: "We typically get the integration live 20–30 days after kickoff — well inside most ERP implementation timelines."
- Propose a specific next meeting: "Would [specific day] at [time] work to do a quick walkthrough with your CAD files?"

Under 70 words. `— Jeff`

---

## Scenario 2: Post-Demo Follow-Up

**4 emails.**

### Email 1 — Same Day

**Subject:** [Feature they asked the most questions about] + next steps

Open with: "The thing that seemed to resonate most was [specific moment from demo]."

Body:
- 3–4 capabilities demonstrated that match their stated requirements
- Any answers to questions they asked during the demo
- Next step with date
- "What questions came up after we hung up?"

Under 100 words. `— Jeff`

### Email 2 — Day 3

**Subject:** Address the biggest concern they raised

Use Feel-Felt-Found:
"[Other companies in similar situations] had the same question about [concern]. What they found was [specific outcome with a number]."

Close with: "Would it help to connect you with someone at [similar company] who went through the same evaluation?"

Under 80 words. `— Jeff`

### Email 3 — Day 7

**Subject:** [Similar manufacturer] + [result]

Lead with a peer reference:
"[Company type similar to theirs] — [employee count or revenue range] — was running [same CAD system] with [same ERP class]. They were re-entering BOMs manually, just like your team."

"After CADTALK go-live: [specific result — hours saved, error rate, time to implement]."

"Same situation, similar setup. Happy to connect you with them directly."

Under 80 words. `— Jeff`

### Email 4 — Day 14

**Subject:** Short, direct — "Checking in on timing"

"Where does this sit in your priorities right now?"

Ask about their decision process: "Is there anyone else who needs to weigh in before moving forward?"

Offer internal selling support: "I can put together a one-page summary your team can review — just say the word."

Under 60 words. `— Jeff`

---

## Scenario 3: Post-Proposal Follow-Up

**5 emails.**

### Email 1 — Proposal Delivery Day

Short. The proposal speaks for itself.

"The investment section is worth reviewing first — happy to do a 15-minute walkthrough if that would be useful. How does [specific date/time] work?"

Under 50 words. `— Jeff`

### Email 2 — Day 3

"Quick question — did you get a chance to look at the proposal?"

Proactively answer the most common concern (usually implementation time or contract length):

"Most customers ask about implementation first: it runs 20–30 days from contract signature. That's usually the fastest part of the project."

Under 60 words. `— Jeff`

### Email 3 — Day 8

Don't mention the proposal.

Share something genuinely useful — a CAD-ERP integration industry note, a relevant stat, or a case reference.

"Thought you'd find this useful given what we discussed about [their specific situation]."

Under 70 words. `— Jeff`

### Email 4 — Day 13

"Where do things stand on your end?"

Ask directly: "Is there anyone else who needs to review this before a decision moves forward?"

Offer to adjust: "If anything in the proposal doesn't fit your situation, I'm happy to revise."

Under 50 words. `— Jeff`

### Email 5 — Day 23

**Subject:** Not the right time?

"Sounds like the timing isn't right — totally understand. If [BOM entry | the integration | the migration timeline] becomes more pressing, we're easy to reach."

"No need to respond to this one. Wish you and the team well."

Under 50 words. `— Jeff`

---

## Scenario 4: Ghost Recovery

**3 emails. Spaced 7–10 days apart.**

### Email 1 — Pattern Interrupt

Use an unexpected subject line:
- "Quick yes or no?"
- "Did I say something wrong?"
- "Thought of you when I saw this"

Body: 3–4 sentences max. Completely different tone. Ask ONE easy question. Do not reference that they went silent.

Under 50 words. `— Jeff`

### Email 2 — Day 10

New angle. Something genuinely interesting.

Lead with a trigger you just found (ERP upgrade release, industry event, relevant news).

"Saw this and thought of [their specific situation]."

"If it's relevant, happy to share more. If not, no worries."

Under 50 words. `— Jeff`

### Email 3 — Day 20

**Subject:** Closing the loop

"I've reached out a few times — totally get it, things get busy. I'll stop filling your inbox after this one."

"If the BOM entry problem becomes a priority down the road, my door's open."

Under 50 words. `— Jeff`

---

## Scenario 5: Nurture (Monthly)

Generate 6 monthly emails. Alternate content type each month:

1. Industry stat or benchmark about engineering data entry costs
2. Customer outcome reference (brief, specific)
3. A relevant article or report they'd actually want to read
4. CADTALK product update or new ERP connector added
5. Event invite (IFS Unleashed, Acumatica Summit, SuiteWorld, Inforum)
6. Brief personal check-in referencing something specific about their business

Each nurture email:
- Subject line that provides value on its own
- Under 80 words
- Zero sales pitch — no "schedule a demo," no "let me know if you'd like to talk"
- One subtle tie-back maximum
- End with "Thought you'd find this interesting" — never a CTA

---

## Save to Deal Desk

Save the follow-up sequence to:

`C:\Users\JeffBrickler\OneDrive - Solutionsx, LLC\ClaudeCoWork\Deal Desk\deals\[CompanyName]\FOLLOWUP-SEQUENCE.md`

---

## Output File: FOLLOWUP-SEQUENCE.md

```markdown
# Follow-Up Sequence: [Company Name]

**Date:** [YYYY-MM-DD]
**Scenario:** [Discovery | Demo | Proposal | Ghost | Nurture]
**Contact:** [name, title]
**Temperature:** [Hot | Warm | Cool | Cold]

---

## Context

| Field | Value |
|-------|-------|
| Last interaction | [date and type] |
| Key takeaways | [2–3 bullet points] |
| Agreed next step | [what was agreed] |
| Their CAD system | [system] |
| Their ERP | [ERP name] |
| Pain signal | [one sentence] |

---

## Emails

[All emails for the selected scenario, fully filled in — no placeholders]

---

*Generated by AI Agent — /ct-followup — [date]*
```
