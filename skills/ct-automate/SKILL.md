---
name: ct-automate
description: Set up and manage scheduled CADTALK sales automations — morning brief, stale alerts, pre-meeting prep, weekly council, deal health checks, and the nightly sweep. Use for 'schedule my morning brief', 'automate stale alerts', 'set up the nightly sweep', 'list my automations'.
---

# CADTALK Automation Backbone

Invoked as `/ct-automate <mode> [args]`. This is the one skill that owns every
scheduled CADTALK task — it creates, lists, and removes them through the
scheduled-tasks MCP. Each scheduled job runs a `/ct-*` command headlessly with the
rep's Deal Desk folder as the working directory.

## Autonomy

Scheduled jobs that only **read and draft** (morning brief, stale alert, pre-meeting
prep, deal health check, council, nightly sweep) are safe at Phase 1 — they produce
briefs and review queues, they do not write the CRM. Any write a job proposes flows
through `/ct-sweep` → `/ct-inbox` (the sales-crm contract) with rep approval. Respect
the autonomy phase in `deal-desk.local.md`; never schedule a job that writes Pipedrive
unattended unless the rep has unlocked that action type.

## Prerequisites

The scheduled-tasks MCP must be connected. The nightly sweep also needs the
Participants API env vars from `/ct-setup` Section F (`PIPEDRIVE_API_TOKEN`,
`PIPEDRIVE_DOMAIN`). If a prerequisite is missing, say so and stop — do not create a
job that will fail every night.

---

## Modes

Each mode maps to a scheduled task. Use the scheduled-tasks MCP `create_scheduled_task`
with the working directory set to the rep's Deal Desk root.

| Mode | Schedule | Command it runs |
|------|----------|-----------------|
| `morning-brief` | weekdays 07:00 local | `/ct-report` (daily brief view) |
| `stale-alert` | Mondays 06:00 local | `/ct-report` filtered to stale (>14 days) |
| `pre-meeting-prep [company]` | 24h before the next linked calendar event | `/ct-prep <company>` |
| `weekly-council` | Sundays 20:00 local | `/ct-report council` |
| `deal-healthcheck [company]` | every 7 days | `/ct-report` health view for that deal |
| `nightly-sweep` | weeknights 05:00 local | `/ct-sweep` |

For `pre-meeting-prep`, look up the next Outlook calendar event tied to the company's
contacts and schedule a one-time task 24 hours before it; if no event is found, tell
the rep and skip.

## `list`

Run the scheduled-tasks MCP list operation. Show each job: name, schedule, last run,
next run, status. Flag any that failed or haven't run when they should have.

## `remove <name>`

Delete the named scheduled task. Confirm the deletion in one line.

---

## Common mistakes

- Scheduling a writing job at Phase 1 — automations stage into `/ct-inbox` for
  approval; they never write Pipedrive unattended.
- Creating the nightly sweep before Section F env vars exist — it will exit 2 every
  night. Verify first.
- Setting the working directory to anything but the Deal Desk root — headless runs
  resolve the deal folder from there.
