# CADTALK AI Sales Team — Plugin

This file is part of the `cadtalk-sales-team` Claude Code plugin.
It routes skill commands and works **additively** with your local Deal Desk folder.

**This is not the Deal Desk identity file.**
The full CADTALK identity (connected systems, pipeline IDs, qualification framework,
all commands) lives in your local Deal Desk Cowork folder:

```
Deal Desk/CLAUDE.md   ← master identity — loads when you open a deal folder in Cowork
```

Both files load together when you're working inside a deal folder. This file routes
plugin skills; the Deal Desk CLAUDE.md provides operator identity and context.

---

## Skill Routing

When the user's request matches a skill below, invoke it via the Skill tool.

| Request | Skill |
|---------|-------|
| First-time setup, onboarding, "set me up" | `/ct-setup` |
| Meeting prep, "prep for [company]" | `/ct-prep` |
| Prospect analysis, full audit | `/ct-prospect` |
| Technical demo prep, sales engineering, "will it work with their stack" | `/ct-se` |
| Update Pipedrive, log a call, set MEDDPICC, move stage, pipeline query | `/ct-crm` |
| Voice/tone review, "does this sound on-brand?", write/edit any copy, coaching | `/ct-voice` |
| Company research | `/ct-research` |
| Lead qualification, BANT, MEDDIC | `/ct-qualify` |
| Coach a deal, "review this deal", "why is it stuck", multi-thread, dark deal, success plan | `/ct-qualify` (Coach Mode) |
| Score a discovery call, WGLL, "grade this call" | `/ct-score` |
| Commit gate, "is this a real commit", forecast integrity, find fake commits | `/ct-commit` |
| Post-demo go/no-go, proposal/decision meeting kit | `/ct-proposal` (decision-gate mode) |
| Decision maker mapping, contacts | `/ct-contacts` |
| Cold outreach, email sequence | `/ct-outreach` |
| Follow-up sequence | `/ct-followup` |
| Proposal generation | `/ct-proposal` |
| Objection handling | `/ct-objections` |
| ICP builder | `/ct-icp` |
| Competitive intelligence | `/ct-competitors` |
| Pipeline report (Markdown) | `/ct-report` |
| Pipeline report (PDF) | `/ct-report-pdf` |
| General sales orchestration | `/ct-sales` |
| Help with commands, how do I use [skill] | `/ct-help` |
| Training, new user onboarding, learn the workflow | `/ct-train` |
| Build a playbook, ramp plan, weekly meeting, battlecard, enablement audit | `/ct-train` (Enablement Mode) |
| Hand won deals to fulfillment, order emails, "process this order", billing/onboarding kickoff | `/ct-fulfill` |
| Revenue leadership — forecasting, sales-model design, pricing, NRR, quota/capacity, board reporting, "CRO", "revenue strategy" | `/ct-cro` |

**`/ct-prep` vs `/ct-se`:** `/ct-prep` is AE business-discovery prep (who's meeting, what pain, talk track). `/ct-se` is SE technical demo prep (does our addin work with their CAD×ERP stack, what to demo). Run both for a technical demo — they're complementary, not overlapping.

## CRM hygiene — single writer rule

CADTALK's Pipedrive has exactly one write path: the **sales-crm** contract
(`agents/sales-crm.md`) plus the field references in `references/`. This is what
makes every rep's CRM updates identical.

- **No ct-* skill writes Pipedrive directly.** When a skill needs to update the
  CRM, it follows `agents/sales-crm.md` inline (or dispatches
  `subagent_type: cadtalk-sales-team:sales-crm`). It never calls a Pipedrive
  write tool with a hand-built field key.
- **Field keys and stage IDs come only from `references/pipedrive-custom-fields.md`
  and `references/pipedrive-stage-ids.md`.** Never fabricate a key.
- Each pipeline stage leaves the standard update payload defined in the sales-crm
  per-stage contract, so a deal looks the same no matter which rep worked it.

## Voice — single standard

Every rep-authored output uses one voice standard: `references/cadtalk-voice-reference.md`
(the `/ct-voice` skill is the standalone WRITE/REVIEW/COACH command). Content skills
(`/ct-outreach`, `/ct-followup`, `/ct-proposal`, `/ct-prep`, `/ct-se`) apply it
before returning copy — personal voice, no AI slop, Strunk & White clarity, CADTALK
brand, in one pass. This is what makes the team sound like one voice.
