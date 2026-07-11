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
| Company research | `/ct-research` |
| Lead qualification, BANT, MEDDIC | `/ct-qualify` |
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

**`/ct-prep` vs `/ct-se`:** `/ct-prep` is AE business-discovery prep (who's meeting, what pain, talk track). `/ct-se` is SE technical demo prep (does our addin work with their CAD×ERP stack, what to demo). Run both for a technical demo — they're complementary, not overlapping.
