# CADTALK Deal Desk — Onboarding Setup

Invoked as `/cadtalk-setup`

Welcome to the CADTALK AI Sales Team. This skill walks you through a one-time setup (~10 minutes). Run it once on a new machine before using any other CADTALK skills.

---

## Section A: Identity + CLAUDE.md

**Step A1 — Who are you?**

Ask: "What's your name and role on the CADTALK sales team?"

Present options:
- **Jeff** — CRO / Deal Desk
- **Chris** — BC, F&O, NetSuite, Acumatica
- **Matthew** — IFS, Arena, Infor
- **Lucca** — (role)
- **Other** — enter name manually

Store the name as `$CADTALK_USER` for use in Section D.

---

**Step A2 — GitHub access gate**

Before proceeding, confirm:

> "Do you have collaborator access to the private GitHub repo `jeffbrickler/CADTALK-AI-Sales-Team`?
> (If you just received the install command from Jeff, the answer is yes.)"

If **No**: Stop. Print:
```
Contact Jeff Brickler (jeff.brickler@cadtalk.com) and ask to be added as a
collaborator on: github.com/jeffbrickler/CADTALK-AI-Sales-Team

Once added, re-run: /cadtalk-setup
```

If **Yes**: continue.

---

**Step A3 — Confirm Deal Desk folder access**

The CADTALK Deal Desk CLAUDE.md is the brain of this system — it defines operator identity, connected systems, Pipedrive IDs, pricing logic, and all commands. It lives in your **local Deal Desk Cowork folder**, NOT in the plugin.

The plugin routes commands to skills. The Deal Desk folder is what makes you a CADTALK operator. Both are required.

Ask: "Do you have the CADTALK Deal Desk folder synced to your machine?"

- **Yes** → Ask for the local path (e.g. `C:\Users\[you]\OneDrive - Solutionsx, LLC\ClaudeCoWork\Deal Desk\`). Confirm `CLAUDE.md` exists there. Print: `✓ Deal Desk folder found at [path]`
- **No** → Print:
  ```
  You need the CADTALK Deal Desk folder synced locally before the identity system works.

  Contact Jeff Brickler (jeff.brickler@cadtalk.com) to get access:
    - OneDrive share to your Microsoft account, OR
    - Jeff will walk you through the sync setup on a call

  Once synced, open Claude Code with that folder as your working directory
  (or open a deal subfolder in Cowork). The CLAUDE.md loads automatically.

  Re-run /cadtalk-setup after the folder is synced.
  ```
  Stop here until the folder is set up.

**How it works once synced:**
- Open any deal subfolder (`Deal Desk/deals/[CompanyName]/`) in Cowork
- Claude loads two CLAUDE.md files simultaneously:
  1. **Plugin CLAUDE.md** (this plugin) — routes skill commands
  2. **Deal Desk CLAUDE.md** — full operator identity, systems, pipeline context
- Both are additive. Together they make Claude a fully-loaded CADTALK sales operator.

---

## Section B: Connection Checks

Run each check in order. A PASS means move on. A FAIL means follow the fix instructions before continuing.

---

**B1 — Pipedrive**

Call `pipedrive_me`.

- **PASS** → Shows your name and email. ✓
- **FAIL** → Run:
  ```
  claude mcp add pipedrive
  ```
  When prompted, enter your API key from:
  `Pipedrive > Settings (top-right avatar) > Personal preferences > API > Generate key`

  If you don't have a Pipedrive account: contact Jeff.

---

**B2 — ZoomInfo**

Call `account_research` with company name "CADTALK".

- **PASS** → Returns company data. ✓
- **FAIL** → Contact Jeff Brickler for your ZoomInfo credentials.
  ZoomInfo is a shared team subscription — Jeff provisions access.

---

**B3 — Outlook / Microsoft 365**

Call `ms365 get_me` (the `get_me` tool on the ms365 MCP server).

- **PASS** → Returns your name and email address. ✓
- **FAIL** → Run:
  ```
  claude mcp add ms365
  ```
  Follow the OAuth browser flow. Sign in with your CADTALK Microsoft account.

---

**B4 — CT Document Site**

Call the CT Document site MCP tool to list or search documents (use a structured list or search operation — not a natural language query).

- **PASS** → Returns documents. ✓
- **FAIL** → Contact Jeff for CT Document site access credentials.
  This is a CADTALK internal resource — Jeff configures it per user.

---

**B5 — Python / PDF Reports (optional)**

Run:
```bash
python -c "import reportlab; print('reportlab OK')"
```

- **PASS** → `reportlab OK` ✓
- **FAIL** → Run (optional — only needed for `/sales report-pdf`):
  ```bash
  pip install -r requirements.txt
  ```
  If you don't need PDF reports, skip this. All other skills work without it.

---

**Section B summary:** Print a checklist:
```
Connection Status:
  [✓/✗] Pipedrive
  [✓/✗] ZoomInfo
  [✓/✗] Outlook / ms365
  [✓/✗] CT Document site
  [✓/✗] Python / PDF (optional)
```

If any required connection (B1-B4) failed: stop here and fix before running Section C.

---

## Section C: Smoke Test

Both Pipedrive and Outlook passed. Now confirm live data is flowing.

**Call 1:** `pipedrive_my_upcoming_activities`

**Call 2:** `ms365 get_me`

- **Both pass** → Print:
  ```
  ✓ Live data confirmed. Pipedrive and Outlook are connected and returning data.
  ```

- **Either fails** → Print:
  ```
  ✗ [connection name] returned an error during smoke test.
  Go back to Section B and re-run that check.
  Error: [paste the error]
  ```

---

## Section D: Confirmation

Setup complete. Print:

```
╔══════════════════════════════════════════════════════════╗
║  CADTALK Deal Desk — Setup Complete                      ║
╚══════════════════════════════════════════════════════════╝

You're running as: [Name] on the CADTALK Deal Desk.

Your CLAUDE.md is installed. Claude now knows it's operating
as a CADTALK sales operator with your Pipedrive pipeline,
pricing framework, and qualification process loaded.

Your first command:
  /deal [any deal name you're working right now]

Or jump straight to a discovery call:
  /sales prep [Company Name]

Update this plugin anytime:
  claude plugin update cadtalk-sales-team

Questions? → jeff.brickler@cadtalk.com
```
