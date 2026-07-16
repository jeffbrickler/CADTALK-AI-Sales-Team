---
name: ct-contract
description: Contract preparation — NDA triage, redline review, legal risk assessment, and package assembly for a CADTALK deal. Use for 'review this NDA', 'redline this contract', 'assess contract risk', 'assemble the contract package'.
---

## Grounding — Brain index

Sales-process, enablement, and asset doc IDs live in `references/brain-index.md`.
Load it when you need to pull a playbook, script, battlecard, or template by ID —
pull by ID directly; search is the fallback. If an ID 404s, search by title and
flag the stale ID.

# CADTALK Contract Prep

Invoked as `/ct-contract <mode> [args]`. Modes: `triage`, `review`, `risk`, `package`.
Everything this skill produces is a **draft for the rep's legal review** — it never
sends, signs, or executes a contract regardless of autonomy phase.

## Grounding docs

Pull by ID from `references/brain-index.md`: contract redline policy
(`d0fa5886-…`), CADTALK agreement (`6cf13bd3-…`), currency conversion policy
(`6175abf9-…`).

## Wraps the legal skills

Where the `legal` plugin is installed, delegate the heavy lifting:
- `triage` → `legal:triage-nda` (GREEN / YELLOW / RED classification).
- `review` → `legal:review-contract` against the CADTALK redline policy.
- `risk` → `legal:legal-risk-assessment` (severity × likelihood).
If the legal skills are absent, do the classification/review inline against the
redline policy doc and flag that a legal skill would normally run.

---

## Mode: triage — `/ct-contract triage`

Screen an incoming NDA before any other work. Run `legal:triage-nda`; return
GREEN / YELLOW / RED with the flagged clauses. RED = stop and escalate to legal.

## Mode: review — `/ct-contract review`

Review the contract against the redline policy: flag deviations, suggest redlines,
cite the policy clause each redline maps to.

## Mode: risk — `/ct-contract risk`

Severity × likelihood assessment on the deal-specific clauses; rank the risks and
name which need senior/outside counsel.

## Mode: package — `/ct-contract package <company>`

Assemble the contract package for the deal: subscription agreement (from the CADTALK
agreement template), the SOW (from `/ct-proposal`), and the order form. Pre-fill deal
details from Pipedrive (sales-crm read). Write the package to the deal folder's
`artifacts/`. Present for the rep's legal review — do not send.

---

## Common mistakes

- Doing any contract work before triaging an incoming NDA — triage first.
- Treating output as final — it is always a draft for legal review.
- Fabricating a clause — cite the redline policy or the agreement template; flag gaps.
