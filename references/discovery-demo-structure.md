# Discovery & Demo Structure (CADTALK)

The reusable rep-facing structure for discovery calls, the demo-script scaffold,
and objection handling. Extracted from the retired enablement reference —
consumed by `/ct-se` (demo scaffold), `/ct-prep`, and `/ct-objections`.

## Section 1: The Discovery Call Playbook

Discovery is the most important call in the sales process. Everything else — the demo, the proposal, the close — depends on how well you understood their world. A bad discovery means a bad close rate. **`/ct-prep` builds the per-call brief; `/ct-score` grades the discovery afterward. This is the underlying structure both rest on.**

### Pre-Call Preparation (Required Before Every First Call)
- Research the company: size, industry, recent news, tech stack (`/ct-research`)
- Research the contact: LinkedIn, recent posts, role, tenure (`/ct-contacts`)
- Know the ICP trigger event that brought them in or prompted outreach
- Prepare two or three tailored questions based on their specific situation

### Discovery Call Structure

**Opening (2 min):**
"Before I show you anything, can I ask a few questions to make sure this conversation is actually relevant for your situation?"

This sets the tone as a research call, not a pitch.

**Org mapping (5 min):**
"Can you walk me through how [relevant function] is structured at [Company]?"
Goal: Understand who does what, who has authority, and how decisions are made.

**Current state (5–7 min):**
"How are you handling [the problem space] today?"
"What tools or processes do you have in place for this?"
Goal: Understand their status quo before presenting anything.

**Pain and cost (5–7 min):**
"What's not working about how you're doing it today?"
"What does that cost you?" (time, money, risk, opportunity)
"If this keeps going the way it is, what happens?"
Goal: Quantify the pain. A problem with a number attached closes faster. (For CADTALK: engineer count × BOM-entry hours × loaded rate — see `/ct-qualify` Step 6.)

**Success picture (3–5 min):**
"If you solved this perfectly, what would that look like in 90 days?"
"What would have to change for you to feel like this was worth the investment?"
Goal: Get them to articulate their own success criteria. This becomes the Success Plan.

**Decision process (5 min):**
"If you decided to move forward with something, how would that decision typically get made?"
"Who else would be involved?"
"What does the evaluation process look like?"
Goal: Map the buying committee and understand the approval chain before investing more time.

**Timeline (2 min):**
"Is there a date by which this needs to be solved?"
"What is driving that timeline?"
Goal: Identify forcing functions. No forcing function = long sales cycle.

**Next step (3 min):**
Propose a specific next step based on what you learned.
Do not say "I'll send you some information." Define who does what, by when.
Examples: "Can we schedule a 45-minute demo on Thursday? I'll show you exactly how [specific thing they care about] works." or "Based on what you told me, I'd like to introduce you to our [specific resource] — can we get 30 minutes next week?"

---

## Section 2: Demo Script Scaffold

Every demo follows the same skeleton — the content changes per stack, the structure doesn't:

1. **Opening** — restate their world in their words (from discovery), confirm nothing changed.
2. **Problem framing** — the specific pain this demo addresses and what it costs them today.
3. **Solution proof** — show only what maps to their pain. What NOT to demo: features that confuse or distract from the pain being solved.
4. **Success plan** — what the first 90 days look like if they buy (see the Success Plan format in `references/deal-coach.md`).
5. **Next step** — specific, dated, with an owner, agreed before the call ends.

Common demo mistakes: demoing before the prospect has articulated the cost of the problem; feature tours; ending without a dated next step. **CADTALK technical demo prep (CAD×ERP fit, Brain-grounded script) is `/ct-se`; call prep is `/ct-prep`.**

## Section 3: Objection Handling Guide

Every objection has a root cause. Handling an objection without addressing the root cause just moves it to the next call. **CADTALK's live, product-specific objection responses are `/ct-objections`. This is the framework underneath it.**

### The Four-Step Framework for Every Objection

1. **Acknowledge:** Show you heard them. Do not immediately counter.
2. **Clarify:** Is this the real objection or a surface-level deflection?
3. **Respond:** Address the root cause, not the stated objection.
4. **Confirm:** Did that answer their concern, or is there more?

### Common Objections and Responses

**"We don't have budget."**
- Clarify: "Is there genuinely no budget allocated for this area, or is this not a current priority?"
- If no budget: "When does your budget cycle reset? Can we stay in touch and revisit in [timeframe]?"
- If not a priority: "Help me understand — you mentioned [their pain]. What is the cost of leaving that unsolved for another 12 months?"

**"We need to think about it."**
- Clarify: "What specifically is driving the need to think about it?"
- Usually means: missing information, unresolved concern, or internal approval needed
- Respond: "That's completely fair. To help make that decision easier, what information would be most useful?"
- Follow up: Ask when they'll have had the chance to think about it, and schedule the follow-up call before getting off the current call.

**"We're already using [Competitor]."**
- Acknowledge: "That makes sense — [Competitor] is a solid option for [what they're good at]."
- Clarify: "What do you like most about how it's working for you today? And is there anything you wish worked differently?"
- Goal: If there is no dissatisfaction, disqualify and move on. If there is, focus on the gap.

**"You're too expensive."**
- Clarify: "Compared to what?" (other vendors, internal build, doing nothing, the cost of the problem)
- If compared to competitors: Walk through differentiated value, not features. "The price difference is [X]. If [your product] saves [Y hours/month], how does that math work for your team?"
- If general sticker shock: Return to Success Plan. "You told me solving this was worth [their estimated value]. How does our price compare to that?"
- Never discount without getting something in return (longer contract, expanded scope, faster close).

**"Send me a proposal."**
- Clarify: "Before I put something together, can I make sure I'm proposing the right thing? Can we spend 20 minutes to make sure I have your requirements right?"
- A proposal without discovery is a guess. Make sure you've completed discovery before writing anything. (CADTALK proposals: `/ct-proposal`.)

**"We're not ready right now."**
- Clarify: "What would need to happen for the timing to be right?"
- Document the trigger (budget approval, end of current contract, project phase) and schedule follow-up for 2 weeks before that event.
- Move to "Future" stage in CRM (via the sales-crm contract). Do not abandon.

**"I need to get buy-in from [other stakeholder]."**
- Respond: "That's a great step. Can we set up a 30-minute call to introduce me to [them] and walk through this together?"
- Do not hand off to an internal champion and hope they sell for you. Your champion does not know how to sell your product. (Multi-thread — see `references/deal-coach.md` Section 4.)

---

