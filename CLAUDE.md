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
| First-time setup, onboarding, "set me up" | `/cadtalk-setup` |
| Meeting prep, "prep for [company]" | `/sales prep` |
| Prospect analysis, full audit | `/sales prospect` |
| Company research | `/sales research` |
| Lead qualification, BANT, MEDDIC | `/sales qualify` |
| Decision maker mapping, contacts | `/sales contacts` |
| Cold outreach, email sequence | `/sales outreach` |
| Follow-up sequence | `/sales followup` |
| Proposal generation | `/sales proposal` |
| Objection handling | `/sales objections` |
| ICP builder | `/sales icp` |
| Competitive intelligence | `/sales competitors` |
| Pipeline report (Markdown) | `/sales report` |
| Pipeline report (PDF) | `/sales report-pdf` |
| General sales orchestration | `/sales` |
