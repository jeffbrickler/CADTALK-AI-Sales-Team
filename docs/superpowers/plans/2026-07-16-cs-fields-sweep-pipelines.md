# CS Fields Out + Sweep Pipeline Scoping Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove Tier and Health Score from the CREATE contract (so sweeps stop flagging them and /ct-crm new stops asking reps for them), and add pipeline-scope control to /ct-sweep (arg override → interactive ask → profile default).

**Architecture:** Two independent changes. Change 1 is data (JSON) + test fixups; Change 2 is skill-doc only. No new scripts. Both fit cleanly inside the existing single-writer + contract-as-source-of-truth patterns.

**Tech Stack:** Python (pytest), JSON, Markdown skill docs

---

## File Map

| File | Action | What changes |
|---|---|---|
| `scripts/create-contract.json` | Modify | Remove Tier + Health Score from `records.deal.required`; add to `excluded_at_create` |
| `scripts/validate_create_payload.py` | Modify | Docstring example: swap `"_unknown": ["Tier"]` → `"_unknown": ["Source channel"]` |
| `scripts/test_validate_create_payload.py` | Modify | `full_payload()` fixture + 4 tests that reference Tier/Health Score |
| `skills/ct-sweep/SKILL.md` | Modify | Step 1 pipeline resolution + queue header note in Step 5 |

---

## Task 1: Update create-contract.json — remove Tier and Health Score from required

**Files:**
- Modify: `scripts/create-contract.json`

- [ ] **Step 1: Edit the contract**

In `scripts/create-contract.json`, find `records.deal.required` (line 12–18):

```json
"required": [
  "Title", "Pipeline", "Stage", "Value", "Currency",
  "Expected close date", "Owner", "Organization", "Person", "ACV",
  "Forecast Category", "Tier", "Health Score", "Source channel",
  "Compelling Event"
],
```

Replace with:

```json
"required": [
  "Title", "Pipeline", "Stage", "Value", "Currency",
  "Expected close date", "Owner", "Organization", "Person", "ACV",
  "Forecast Category", "Source channel",
  "Compelling Event"
],
```

Then find the `excluded_at_create` array (lines 31–38) and add Tier + Health Score with a CS-owned comment:

```json
"excluded_at_create": [
  "MEDDPICC-Metrics", "MEDDPICC-Economic Buyer", "MEDDPICC-Decision Criteria",
  "MEDDPICC-Decision Process", "MEDDPICC-Paperwork Process", "MEDDPICC-ID the Pain",
  "MEDDPICC-Champion", "MEDDPICC-Competition", "MEDDPICC-Coach",
  "Feedback on Proposal", "Feedback on Demonstration", "SQO Date",
  "EB Last Direct Touch", "Latest web visit", "Lost reason",
  "Probability", "ARR", "MRR", "Status", "Visible to", "Score",
  "Tier", "Health Score"
],
```

Also update the top-level `_comment` string to add a sentence about CS fields (find the opening `"_comment"` key):

```json
"_comment": "Single source of truth for the opportunity CREATE contract (design doc 2026-07-14, eng review 3A). Logical field NAMES only — hash API keys and option IDs live exclusively in the vendored references (references/pipedrive-custom-fields.md, pipedrive-stage-ids.md; upstream repo jeffbrickler/pipedrive-update). agents/sales-crm.md and skills/ct-crm point here instead of restating the list. Changing this file requires updating the Pipedrive-side native required-fields configuration to match (eng review T1-A sync rule). Tier and Health Score are CS-owned (confirmed 2026-07-15/16): excluded_at_create, never gated, never written by any rep-loop skill.",
```

- [ ] **Step 2: Verify JSON is valid**

```bash
python -c "import json; json.load(open('scripts/create-contract.json'))" && echo "valid"
```

Expected: `valid`

- [ ] **Step 3: Commit**

```bash
git add scripts/create-contract.json
git commit -m "chore: Tier + Health Score → excluded_at_create (CS-owned, 2026-07-16)"
```

---

## Task 2: Update validate_create_payload.py docstring example

**Files:**
- Modify: `scripts/validate_create_payload.py` (lines 16–19 only)

- [ ] **Step 1: Edit docstring example**

Find in the module docstring (around line 16):

```python
      "deal":         {"Title": "...", "Pipeline": "Partners", ...,
                       "_unknown": ["Tier"]},
```

Replace with:

```python
      "deal":         {"Title": "...", "Pipeline": "Partners", ...,
                       "_unknown": ["Source channel"]},
```

- [ ] **Step 2: Commit**

```bash
git add scripts/validate_create_payload.py
git commit -m "docs: swap Tier example in validator docstring (now excluded_at_create)"
```

---

## Task 3: Fix test_validate_create_payload.py — fixture and 4 broken tests

**Files:**
- Modify: `scripts/test_validate_create_payload.py`

**Context:** After Task 1, Tier and Health Score are no longer required. Four tests need updating:
1. `full_payload()` fixture carries `"Tier"` and `"Health Score"` → remove them
2. `test_all_missing_fields_reported_not_just_first()` pops `"Tier"` to trigger a missing-required error → swap for `"Source channel"`
3. `test_unknown_flagged_field_passes()` pops `"Tier"` then flags it as unknown → swap for `"Source channel"`
4. `test_silent_blank_still_fails()` blanks `"Tier"` → swap for `"Source channel"`

- [ ] **Step 1: Confirm tests currently pass before changes**

```bash
cd scripts && python -m pytest test_validate_create_payload.py -v 2>&1 | tail -20
```

Expected: all tests pass (Tier still in contract right now only if this runs before Task 1; if Task 1 is done, 3–4 tests will FAIL — that is expected and confirms the tests are real).

- [ ] **Step 2: Update full_payload() fixture — remove Tier and Health Score**

Find `full_payload()` (around line 28). The `deal` dict contains:

```python
        "Forecast Category": "Pipeline",
        "Tier": "Tier 1",
        "Health Score": "Green",
        "Source channel": "Partner referral",
```

Replace with:

```python
        "Forecast Category": "Pipeline",
        "Source channel": "Partner referral",
```

- [ ] **Step 3: Update test_all_missing_fields_reported_not_just_first (line 163)**

Find:

```python
def test_all_missing_fields_reported_not_just_first():
    payload = full_payload()
    payload["deal"].pop("Tier", None)
    payload["organization"].pop("Source System", None)
    payload["person"].pop("Role", None)
    res = run(payload)
    assert res.returncode == 1
    assert "deal.Tier" in res.stderr
    assert "organization.Source System" in res.stderr
    assert "person.Role" in res.stderr
```

Replace with:

```python
def test_all_missing_fields_reported_not_just_first():
    payload = full_payload()
    payload["deal"].pop("Source channel", None)
    payload["organization"].pop("Source System", None)
    payload["person"].pop("Role", None)
    res = run(payload)
    assert res.returncode == 1
    assert "deal.Source channel" in res.stderr
    assert "organization.Source System" in res.stderr
    assert "person.Role" in res.stderr
```

- [ ] **Step 4: Update test_unknown_flagged_field_passes (line 231)**

Find:

```python
def test_unknown_flagged_field_passes():
    payload = full_payload()
    payload["deal"].pop("Tier", None)
    payload["deal"]["_unknown"] = ["Tier"]
    res = run(payload)
    assert res.returncode == 0
```

Replace with:

```python
def test_unknown_flagged_field_passes():
    payload = full_payload()
    payload["deal"].pop("Source channel", None)
    payload["deal"]["_unknown"] = ["Source channel"]
    res = run(payload)
    assert res.returncode == 0
```

- [ ] **Step 5: Update test_silent_blank_still_fails (line 239)**

Find:

```python
def test_silent_blank_still_fails():
    payload = full_payload()
    payload["deal"]["Tier"] = "   "  # whitespace ≠ filled
    res = run(payload)
    assert res.returncode == 1
    assert "deal.Tier" in res.stderr
```

Replace with:

```python
def test_silent_blank_still_fails():
    payload = full_payload()
    payload["deal"]["Source channel"] = "   "  # whitespace ≠ filled
    res = run(payload)
    assert res.returncode == 1
    assert "deal.Source channel" in res.stderr
```

- [ ] **Step 6: Run the full test suite**

```bash
cd scripts && python -m pytest test_validate_create_payload.py -v
```

Expected: all tests pass (0 failures). If any fail, the test still references Tier or Health Score — grep and fix:

```bash
grep -n "Tier\|Health Score" test_validate_create_payload.py
```

- [ ] **Step 7: Commit**

```bash
git add scripts/test_validate_create_payload.py
git commit -m "test: re-anchor Tier/Health Score tests on Source channel (now excluded_at_create)"
```

---

## Task 4: Update ct-sweep SKILL.md — pipeline resolution + queue header

**Files:**
- Modify: `skills/ct-sweep/SKILL.md`

**Context:** Step 1 currently reads the pipeline IDs from `crm-profile.md` and passes them straight to the script. We need to insert a pipeline resolution sub-step before that. Step 5 writes the queue MD — add a note that the header line must show which pipelines were swept.

- [ ] **Step 1: Update Step 1 in the skill**

Find the current Step 1 block in `skills/ct-sweep/SKILL.md`:

```markdown
## Step 1: Locate context

1. Deal Desk root: the current working folder if it contains `crm-profile.md`,
   else ask (interactive) or abort with a clear log line (headless).
2. Read `crm-profile.md` → rep's pipeline IDs + Pipedrive Owner ID.
3. Ensure `inbox/` and `inbox/processed/` folders exist at the Deal Desk root.
```

Replace with:

```markdown
## Step 1: Locate context + resolve pipelines

1. Deal Desk root: the current working folder if it contains `crm-profile.md`,
   else ask (interactive) or abort with a clear log line (headless).
2. Read `crm-profile.md` → rep's pipeline IDs (full profile set) + Pipedrive Owner ID.
3. **Pipeline resolution — determine which pipelines to sweep this run:**
   - **Argument given** (`/ct-sweep New ERP` or `/ct-sweep 1,2` or a mix of
     names and IDs): resolve names to IDs via `crm-profile.md` first, then
     `references/pipedrive-stage-ids.md`. Use only the resolved IDs.
     - Interactive: if any name/ID cannot be resolved, list the valid pipelines
       from `crm-profile.md` and ask the rep to pick — do not abort.
     - Headless: if any name/ID cannot be resolved, fall back to the full
       `crm-profile.md` set and record the fallback in the queue MD header
       (e.g. "⚠ pipeline arg unresolvable — swept full profile set").
   - **No argument, interactive**: list the rep's pipelines from `crm-profile.md`
     (names + IDs) and ask which to sweep. The full profile set is the default
     answer (rep hits Enter to accept).
   - **No argument, headless/nightly**: use the full `crm-profile.md` set. No
     behavior change from the prior spec.
4. Ensure `inbox/` and `inbox/processed/` folders exist at the Deal Desk root.
```

- [ ] **Step 2: Update Step 2 snapshot command to reflect resolved pipelines**

In Step 2 the snapshot command is:

```
python ${CLAUDE_PLUGIN_ROOT}/scripts/pipedrive_read.py snapshot --owner-id <id> --pipelines <ids> --out <deal-desk>/inbox/.snapshot-{YYYY-MM-DD}.json
```

No change to the command itself — `<ids>` already means the resolved IDs from Step 1. Add a parenthetical note directly after the command:

```
(use the resolved pipeline IDs from Step 1 — never the raw crm-profile set if an argument was given)
```

- [ ] **Step 3: Update Step 5 queue MD header**

In Step 5, find the queue MD description:

```markdown
4. Write `inbox/REVIEW-QUEUE-{YYYY-MM-DD}.md` — the human brief, Jeff-voice
   Register 4 (direct, numbered, short), sectioned:
   ① Hygiene gaps ② Commit integrity ③ Stuck & dark ④ Today (due activities)
   ⑤ Reconcile (CREATE-contract gaps — `reconcile-fill` items from Step 3b,
   pre-filled where context knew the value, ask-the-rep otherwise; approving
   writes the field through the sales-crm contract).
   Each item shows: deal, finding, proposed action, evidence, item id.
   Header line: item counts per section + "open /ct-inbox to review".
```

Replace the last sentence:

```markdown
   Header line: item counts per section + "open /ct-inbox to review" +
   pipelines swept (names + IDs, e.g. "Pipelines: Aftermarket (1), New ERP/PLM Prospects (2)").
   If a fallback occurred (unresolvable arg, headless), note it here too.
```

- [ ] **Step 4: Validate plugin**

```bash
python scripts/validate-plugin.py
```

Expected: `OK — 0 failures, 0 warning(s). Plugin valid.`

- [ ] **Step 5: Commit**

```bash
git add skills/ct-sweep/SKILL.md
git commit -m "feat: /ct-sweep pipeline scoping — arg override, interactive ask, profile default"
```

---

## Task 5: Smoke-test and final validation

- [ ] **Step 1: Run full validate_create_payload test suite one more time**

```bash
cd scripts && python -m pytest test_validate_create_payload.py -v
```

Expected: all 14+ tests pass, 0 failures.

- [ ] **Step 2: Confirm Tier + Health Score no longer appear as required in contract**

```bash
python -c "
import json
c = json.load(open('scripts/create-contract.json'))
req = c['records']['deal']['required']
excl = c['records']['deal']['excluded_at_create']
assert 'Tier' not in req, 'Tier still in required'
assert 'Health Score' not in req, 'Health Score still in required'
assert 'Tier' in excl, 'Tier missing from excluded_at_create'
assert 'Health Score' in excl, 'Health Score missing from excluded_at_create'
print('OK: Tier and Health Score correctly excluded')
"
```

Expected: `OK: Tier and Health Score correctly excluded`

- [ ] **Step 3: Run plugin validator**

```bash
python scripts/validate-plugin.py
```

Expected: `OK — 0 failures, 0 warning(s). Plugin valid.`

- [ ] **Step 4: Final commit if anything was missed**

If any straggling file is unstaged, add and commit now. Otherwise done.

---

## Post-ship note (Jeff's action item)

The contract carries a sync rule with Pipedrive's native required-fields config (eng review T1-A). After this ships, verify in the Pipedrive web UI that Tier and Health Score are NOT set as native required fields at deal creation. This is outside the plugin — no code change needed.

Also run `/ct-setup pipelines` once in your Deal Desk to trim `crm-profile.md` to sales pipelines only — that fixes nightly sweep scope immediately.
