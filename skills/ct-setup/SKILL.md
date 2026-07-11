---
name: ct-setup
description: First-time setup and onboarding for the CADTALK sales plugin. Use for initial configuration, connecting systems, 'set me up'.
---

# CADTALK Deal Desk — Onboarding Setup

Invoked as `/ct-setup`

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

Once added, re-run: /ct-setup
```

If **Yes**: continue.

---

**Step A3 — Create the Deal Desk folder**

The Deal Desk folder is your local context hub. It holds the CADTALK identity file (CLAUDE.md), your deal subfolders, and all deal memory. This folder ships with the plugin — setup creates it for you now.

**Step A3a — Choose a location**

Ask: "Where do you want the CADTALK Deal Desk folder?"

Suggest default: `C:\Users\[username]\Documents\CADTALK-Deal-Desk\`

Store as `$DEAL_DESK_PATH`.

**Step A3b — Find the plugin template**

Run this PowerShell to locate the deal-desk template in the plugin install:

```powershell
# Search for the deal-desk template shipped with the plugin
$template = Get-ChildItem -Path "$env:APPDATA\Claude" -Recurse -Filter "CLAUDE.md" -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -like "*templates*deal-desk*" } |
    Select-Object -First 1 -ExpandProperty DirectoryName

if ($template) {
    Write-Host "Plugin template found: $template"
} else {
    Write-Host "ERROR: Could not find plugin template. Is the plugin installed?"
    Write-Host "Run: claude plugin add github:jeffbrickler/CADTALK-AI-Sales-Team"
}
```

If not found: stop and re-run `claude plugin add github:jeffbrickler/CADTALK-AI-Sales-Team` first.

**Step A3c — Create the folder**

Run:

```powershell
$templatePath = "<path from A3b>"
$destPath = "<$DEAL_DESK_PATH>"

# Copy full template structure
Copy-Item -Path $templatePath -Destination $destPath -Recurse -Force
Write-Host "Deal Desk created at: $destPath"
Write-Host "Contents:"
Get-ChildItem $destPath -Recurse | Select-Object FullName
```

**Expected result:**
```
CADTALK-Deal-Desk/
├── CLAUDE.md                  ← Deal Desk identity (the brain)
├── MEMORY.md                  ← Hub memory (starts empty)
└── deals/
    ├── _deal-template/        ← Copy this when starting a new deal
    │   ├── CLAUDE.md
    │   └── MEMORY.md
    └── _archive/
        ├── won/
        └── lost/
```

**How to use it:**
- Open `CADTALK-Deal-Desk/` (or any deal subfolder) in Claude Code / Cowork
- The `CLAUDE.md` there loads automatically — Claude is now a CADTALK operator
- The plugin CLAUDE.md (routing) + the Deal Desk CLAUDE.md (identity) load together
- Start a new deal: copy `_deal-template/` → rename to `[CompanyName_ERP]/` → fill in the deal CLAUDE.md

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
- **FAIL** → Run (optional — only needed for `/ct-report-pdf`):
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
  /ct-prep [Company Name]

**Next step:** Run `/ct-train` to complete your training (~20 min).

Update this plugin anytime:
  claude plugin update cadtalk-sales-team

Questions? → jeff.brickler@cadtalk.com
```
