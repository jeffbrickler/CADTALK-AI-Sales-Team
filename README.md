<p align="center">
  <img src="banner.svg" alt="CADTALK AI Sales Team" width="100%">
</p>

<p align="center">
  <a href="#install"><img src="https://img.shields.io/badge/install-one--liner-blue?style=for-the-badge" alt="Install"></a>
  <a href="#commands"><img src="https://img.shields.io/badge/16_skills-ready-8b5cf6?style=for-the-badge" alt="16 Skills"></a>
  <a href="#how-it-works"><img src="https://img.shields.io/badge/MCP-powered-22c55e?style=for-the-badge" alt="MCP Powered"></a>
</p>

> **CADTALK's AI-powered deal desk, running inside Claude Code.**
> Research companies, qualify leads with BANT + MEDDIC, map buying committees, generate personalized outreach, prep for calls, and produce pipeline reports — all from the command line with live Pipedrive, ZoomInfo, and Outlook data.

---

## Install

> **Cowork users:** You need the Claude Code CLI installed once to add the plugin. After that, the skills work in Cowork normally. [Install Claude Code →](https://docs.anthropic.com/en/docs/claude-code)

### Step 1 — Add the plugin (terminal, one time)

Open a terminal and run:

```bash
claude plugin add github:jeffbrickler/CADTALK-AI-Sales-Team
```

### Step 2 — Run setup (Cowork or Claude Code, one time)

```
/ct-setup
```

Walks you through: who you are → connection checks (Pipedrive, ZoomInfo, Outlook) → Deal Desk folder creation → smoke test. Takes ~10 minutes the first time.

### Step 3 — Run training (one time)

```
/ct-train
```

20-minute mock deal walkthrough (Acme Fabrication). Covers the full workflow in order. Works even if your MCP connections aren't fully configured yet. Do this before using the plugin on a real deal.

### Update (terminal)

```bash
claude plugin update cadtalk-sales-team
```

---

## Commands

### Workflow (run in this order for a new deal)

| Command | What it does |
|:--------|:-------------|
| `/ct-research [Company]` | Firmographics, tech stack, signals before first contact |
| `/ct-qualify [Company]` | BANT + MEDDIC — pursue, hold, or disqualify |
| `/ct-prep [Company + context]` | Pre-call brief, agenda, discovery questions, talk track |
| `/ct-outreach [Company + context]` | 3-touch cold email + LinkedIn sequence |
| `/ct-followup [Company + context]` | Post-meeting follow-up sequence |

### Deal Tools

| Command | What it does |
|:--------|:-------------|
| `/ct-contacts [Company]` | Find decision makers and contact info via ZoomInfo |
| `/ct-proposal [Company + context]` | Generate a proposal |
| `/ct-objections [Objection]` | Handle a specific sales objection |

### Intelligence

| Command | What it does |
|:--------|:-------------|
| `/ct-icp` | Review CADTALK ideal customer profile criteria |
| `/ct-competitors [Competitor]` | Competitive intel on a named competitor |
| `/ct-prospect [Company]` | Full audit: research + qualify + contacts in one command |

### Pipeline

| Command | What it does |
|:--------|:-------------|
| `/ct-report` | Pipeline summary from Pipedrive (Markdown) |
| `/ct-report-pdf` | Pipeline summary (PDF) |

### Onboarding & Help

| Command | What it does |
|:--------|:-------------|
| `/ct-setup` | First-time plugin setup (run once) |
| `/ct-train` | Interactive training walkthrough (~20 min) |
| `/ct-help` | Full skill map |
| `/ct-help [skill]` | Detail on a specific skill — e.g. `/ct-help prep` |

---

## How It Works

Skills connect to live data via MCP:

- **Pipedrive** — your pipeline, deals, activities, contacts
- **ZoomInfo** — company research, firmographics, decision maker mapping
- **Outlook / ms365** — calendar, email context

The Deal Desk folder (`/ct-setup` creates it) stores your CLAUDE.md identity file and deal subfolders. Open any deal folder in Claude Code — it loads automatically.

---

## Requirements

| Requirement | Status | Notes |
|:------------|:------:|:------|
| **Claude Code** | Required | [Install Claude Code](https://docs.anthropic.com/en/docs/claude-code) |
| **Pipedrive MCP** | Required | Setup via `/ct-setup` |
| **ZoomInfo MCP** | Required | Credentials from Jeff |
| **Outlook MCP** | Required | Setup via `/ct-setup` |
| **Python 3.8+** | Optional | For PDF report generation only |
| **reportlab** | Optional | `pip install reportlab` — PDF reports |

---

## Questions

Contact Jeff Brickler — jeff.brickler@cadtalk.com

Or run `/ct-help [skill]` — that's what it's there for.
