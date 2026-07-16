---
name: ct-se
description: Generate a Brain-grounded technical demo-prep brief for a CADTALK prospect — map their CAD×ERP stack to CADTALK capabilities, write a demo script, pre-answer technical objections. Use for demo prep, sales engineering, technical fit.
---

# CADTALK Technical Demo Prep (Sales Engineer)

Invoked as `/ct-se <company>`

You produce a technical demo-prep brief for one named prospect: their CAD/ERP stack mapped to CADTALK capabilities, a demo script against that stack, and pre-answered technical objections. Output goes to the deal folder as `TECH-DEMO-PREP.md`.

This is **SE work, not AE work.** `/ct-prep` handles business discovery (who's in the room, what their pain costs). `/ct-se` handles technical fit (will our addins work with their stack, what do we show). When `/ct-prep` or `/ct-prospect` output already exists for this company, consume it — do not re-research the business side.

## CRM update — emit through sales-crm (single writer)

When Pipedrive is connected, leave this stage's standard payload by following the
sales-crm contract (`agents/sales-crm.md`) — never a hand-built field key. This
skill's row in that contract:

- Log a `demo` activity, write **Feedback on Demonstration**, set **MEDDPICC-Decision
  Criteria** and **MEDDPICC-Competition** from what the demo surfaced, pin a
  technical-fit note.

Keys resolve from `references/pipedrive-custom-fields.md`. Pipedrive reads here are
optional (the brief degrades gracefully); writes only happen when it's connected.

For the demo-script scaffold (opening → problem framing → solution proof → success plan → next step) and the discovery structure feeding it, use `references/discovery-demo-structure.md`. That reference is the reusable structure; this skill supplies the Brain-grounded, stack-specific content.

---

## The Anti-Hallucination Spine (read before anything else)

Every "CADTALK's addin does X" statement in the brief must be grounded in a CADTALK source, never asserted from memory, the website, or the examples in `agents/sales-engineer.md`. This is the whole reason `/ct-se` exists — commercial AI SE tools hallucinate capability claims from marketing collateral; CADTALK grounds in source.

**Grounding chain — try in this order for every capability claim:**

1. **The Brain (`ask_the_brain`)** — primary. Answers from actual addin source code and abstains when evidence is missing. Tag confirmed claims **VERIFIED (Brain)**.
2. **CT Outline document site** — backup, used when the Brain MCP is not connected. Search/fetch CADTALK's technical documentation (the connected Outline workspace) for the capability. Outline is the Brain's backup, not its equal — it's curated docs, not live source. Tag confirmed claims **VERIFIED (Docs)** and cite the doc title.
3. **Escalate to a human** — if neither the Brain nor Outline has evidence for a claim, the line says **"VERIFY WITH A SENIOR SE, ENGINEERING, OR A SENIOR SOLUTION ARCHITECT."** Never guess to fill the gap.

**Rules:**

- **Abstention propagates.** No evidence in Brain AND no evidence in Outline → the human-verify tag above. Never invent a capability.
- **Only if BOTH the Brain and Outline are unavailable** (neither MCP connected) → mark every claim **UNVERIFIED** and banner the brief (see Phase 2).
- **Budget: ≤5 grounding calls** (Brain or Outline). Scope to the detected CAD×ERP pair; batch related claims per question — do not query one call per claim.

---

## Input

- `<company>`: Company name (required). A bare name with no Pipedrive deal yet is valid — degrade to research-only intake (see Phase 1).

---

## Phase 1: Deal Context + Stack Intake

Gather the prospect's CAD and ERP stack in this priority order. Stop as soon as you have both CAD and ERP identified with reasonable confidence; keep going if either is unknown.

1. **Pipedrive** — search the deal and organization for CAD/ERP fields, notes, and activity history.
   - If the Pipedrive MCP is **unavailable**, skip silently to step 2. No banner (unlike the Brain — Pipedrive absence degrades gracefully and is expected off-network).
2. **Deal folder notes** — read existing analysis for this company:
   `C:\Users\JeffBrickler\OneDrive - Solutionsx, LLC\ClaudeCoWork\Deal Desk\deals\[CompanyName]\`
   Consume `PROSPECT-ANALYSIS.md`, `MEETING-PREP.md`, `COMPANY-RESEARCH.md`, `LEAD-QUALIFICATION.md` if present. These usually carry the CAD system, ERP, and manufacturing model already.
3. **Ask the user** — if CAD or ERP is still unknown, ask directly. One focused question beats a wrong guess.
4. **Web research fallback** — only if still unknown: fetch the careers/jobs page and search for CAD (`Inventor OR SolidWorks OR "Solid Edge" OR NX OR Creo OR CATIA`) and ERP mentions.

**Output of Phase 1:** the detected CAD × ERP pair, PDM/PLM if known, manufacturing model (ETO/CTO/MTO) if known, and where each fact came from (Pipedrive / deal folder / user / web). If you had to guess, say so.

---

## Phase 2: Capability Mapping (source-grounded)

Map the prospect's stack to CADTALK capabilities using the grounding chain (Brain → Outline → human). **Scope every query to the detected CAD×ERP pair and batch related claims** — target ≤5 grounding calls total.

Capability areas to cover (batch these into a few scoped questions, not one call each):

- BOM push for `[CAD]` → `[ERP]` — does a connector exist; attended or unattended?
- Engineering-change propagation for the pair — automatic on revision?
- Part-number / property mapping — CAD properties → ERP fields.
- Multi-level / phantom BOM handling.
- Audit trail depth (ISO/AS9100 relevance).
- Batch / parallel processing throughput.

For each capability, record an evidence status:

| Status | Meaning |
|--------|---------|
| **VERIFIED (Brain)** | `ask_the_brain` returned supporting evidence. Note the gist. |
| **VERIFIED (Docs)** | Brain not connected; a CT Outline doc confirms it. Cite the doc title. |
| **VERIFY WITH HUMAN** | Neither Brain nor Outline has evidence — verify with a senior SE, engineering, or a senior solution architect. |
| **UNVERIFIED** | Neither the Brain nor Outline was available (both MCPs offline). |

**Source availability handling:**
- Brain connected → use it first.
- Brain not connected, Outline connected → ground in CT Outline docs (the expected state on machines without the Brain MCP). No banner — this is a supported fallback, just a slightly weaker source.
- **Neither connected** → mark every capability UNVERIFIED and put this banner at the top of the brief:

> ⚠️ **No grounding source available — all claims need human verification.** Neither the CADTALK Brain nor the Outline document site was reachable. Confirm every capability with a senior SE, engineering, or a senior solution architect before the demo.

Zero "yes it works" claims may appear without one of the four tags above.

---

## Phase 3: Demo Script + Talk Track

Write a demo script against the prospect's actual stack, not a generic one. Anchor on the VERIFIED capabilities.

- **The one thing to show:** the BOM push from `[their CAD]` to `[their ERP]`. Lead with it.
- **Sequence:** open a real assembly in `[CAD]` → push → show the part + BOM records land in `[ERP]` → revise a part → show the change propagate → show the audit trail.
- **Talk track:** for each step, one sentence on what the engineer/IT evaluator is watching for and why it matters to THEM (tie to their manufacturing model and pain).
- **Do-not-show list:** any capability tagged VERIFY WITH HUMAN or UNVERIFIED — do not demo it live. Note it as "confirm with a senior SE / engineering / senior solution architect, then show in a follow-up."

---

## Phase 4: Technical Objection Prep

Pre-answer the objections a technical evaluator (engineer or IT) will raise about THIS stack. Ground each answer in a VERIFIED capability (Brain or Docs) where possible; if the answer depends on an unverified capability, say "confirm with a senior SE, engineering, or a senior solution architect."

Cover at minimum:

- "Does it actually work with our `[CAD]` / `[PDM]` version?"
- "What happens to the integration when we upgrade `[ERP]`?"
- "How much maintenance does IT own after go-live?"
- "What about our custom part-numbering / property scheme?"
- "How does it handle our multi-level assemblies?"

Each objection gets: the likely concern, the grounded answer (with evidence status), and — if unverified — the exact question to send a senior SE, engineering, or a senior solution architect before the demo.

---

## Boundary with /ct-prep

`/ct-prep` is AE business-discovery prep. `/ct-se` is SE technical demo prep. When `/ct-prep` output exists, `/ct-se` consumes its company/contact snapshot rather than re-researching, and focuses entirely on the technical layer. Run `/ct-prep` for the meeting plan; run `/ct-se` for the technical demo plan. They are complementary, not overlapping.

---

## Save to Deal Desk

Save the brief to:

`C:\Users\JeffBrickler\OneDrive - Solutionsx, LLC\ClaudeCoWork\Deal Desk\deals\[CompanyName]\TECH-DEMO-PREP.md`

If no deal folder exists yet (pre-pipeline standalone run), create it, or tell the user where you saved it if the Deal Desk path is unavailable.

---

## Output File: TECH-DEMO-PREP.md

Use `templates/demo-prep.md` as the structure. The brief has:

```markdown
# Technical Demo Prep: [Company Name]

**Date:** [YYYY-MM-DD] | **CAD × ERP:** [CAD] × [ERP]
**Stack source:** [Pipedrive / deal folder / user / web]
**Grounding source:** [Brain / Outline docs / none — human verification required]
[⚠️ no-grounding-source banner here if both Brain and Outline were offline]

---

## Stack Snapshot
[CAD, PDM/PLM, ERP + class, manufacturing model — with source of each fact]

## Capability Map
[Table: capability | evidence status (Brain/Docs/human/unverified) | what the source said / the gap]

## Demo Script
[Step-by-step against their stack, with talk track and do-not-show list]

## Technical Objection Prep
[Per objection: concern, grounded answer + evidence status, escalation question (senior SE / engineering / senior solution architect) if unverified]

---

*Generated by AI Agent — /ct-se — [date]. Capability claims grounded in the CADTALK Brain (or Outline docs when the Brain is offline); unverified claims flagged for human verification.*
```

---

## CADTALK Voice (apply before output)

Before returning any written copy (email, message, recap, script, proposal), apply the CADTALK voice: follow `references/cadtalk-voice-reference.md`, or run `/ct-voice` in REVIEW mode. Personal voice, no AI slop, Strunk & White clarity, CADTALK brand — one pass. Nothing goes out unvoiced.

## Hygiene sweep (final step)

After this skill's output is delivered, run the CRM hygiene sweep
(`skills/ct-hygiene/SKILL.md`, Sweep mode) with this run's artifacts as the
source — it pushes what this run learned (fields, contacts, participants) into
Pipedrive through the sales-crm contract. Batch review table first; writes only
after the rep confirms. If the deal/org can't be resolved in Pipedrive, skip
silently.
