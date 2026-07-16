# Deal Desk — Workspace Facts

<!--
Written by /ct-setup. Your personal Deal Desk configuration.
The plugin never overwrites this file on upgrade. Edit it directly, or re-run
/ct-setup to regenerate. Skills read individual sections by heading — keep the
## headings intact.
-->

## Autonomy Phase

**Current phase: 1 (Draft Only).** Do not escalate without explicit permission.

- **Phase 1 — Draft Only:** CRM updates, emails, activities, notes, stage changes
  are all proposed for approval, never executed automatically.
- **Phase 2 — Semi-Automated:** unlocked per action type. Say "go semi-auto on
  [action type]" to unlock. Record each unlock below.
- **Phase 3 — Autonomous:** exception-only review. Not active.

**Unlocked actions (Phase 2):** _(none yet)_

## Pipelines & Stages

All revenue pipelines share the same four stages:

| Stage | Name | Probability |
|-------|------|-------------|
| 1 | Discovery | 30% |
| 2 | Prove | 50% |
| 3 | Propose | 75% |
| 4 | Contracts | 95% |

**Revenue pipeline IDs:**
- Aftermarket (id=1) — direct/CADTALK-controlled
- New ERP/PLM Prospects (id=2) — partner-led, BANT+H mandatory
- Expansions (id=4) — existing-customer upsell

**Reference-only pipelines:** Aftermarket Nurture (12), SDR Leads (6),
PDR leads (8), Partners (3), Customer Success (7), Collections (5),
IFS Lead Enrichment (11).

> Pipeline scope + your Pipedrive Owner ID live in `crm-profile.md` (written by
> `/ct-setup pipelines`). This section is the shared stage/ID reference.

## Metrics Baseline

<!-- Dated snapshot. /ct-report flags a baseline older than one quarter. -->

- **As of:** [DATE]
- ARR: [$] | MRR: [$]
- Active customers: [n] | ACV: [$]
- Annual target: [$] net-new (~[$] gross to offset churn)
- Win rates: close [%] | New ERP [%] | IFS [%]
- Deal floor: [$] (universal)
- Cycle: [n] days direct, [n] months partner-led

## Team

| Role | Name |
|------|------|
| CRO | [name] |
| Partner Dev Manager | [name] |
| Assoc Channel Manager | [name] |
| Territory Dev Rep / SDR | [name] |
| Marketing Manager | [name] |
| EA | [name] |
| CSM | [name] |
| Implementation PM | [name] |

## Pricing & Quoting Doc IDs

Pull quoting rules and pricing from the CT Document site by ID — never quote from
memory.

| Document | CT Document ID |
|----------|----------------|
| Deal Desk Rules & Quoting Decision Trees | `41b8a592-7afd-4e80-aa1f-fc149d6ba141` |
| IFS — Partner Pricing Guide 2026 | `b52815b3-ae4d-49f4-8a7e-d5770961fe15` |
| IFS — End User Pricing Guide 2026 | `414d48bc-0a40-4a70-9ee5-ae8ebc45a21a` |
| How We Make Money (internal) | `417c544f-6ed3-4a6c-abfa-3fa2f4edbfc4` |
| Ecosystem Pricing Guides (2026 — all ERPs) | `b7058202-b11c-46c0-a720-a9c8d91932cb` |
| Currency Conversion Policy | `6175abf9-6cac-47c5-87ed-94a692b945f7` |

## Brand Kit

- **Canva Brand Kit ID:** `kAE2Ycu3mWI`
- Always pass `brand_kit_id` when generating Canva designs; search brand templates
  before creating from scratch.
