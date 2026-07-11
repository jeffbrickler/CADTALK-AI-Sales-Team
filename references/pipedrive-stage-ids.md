# CADTALK Pipedrive Stage & Resource IDs

Last updated: 2026-06-15

## How to use this reference

- **Stage moves**: `pipedrive_deals_move_stage` with `deal_id` + `stage_id`
- **Deal creates**: include `pipeline_id` + `stage_id` in `pipedrive_deals_create`
- **Activities**: use `type` (key_string column) in `pipedrive_activities_create`
- **Deal products**: use `product_id` in `pipedrive_deal_products_add`

---

## Pipelines

| ID | Name |
|---|---|
| 1 | Aftermarket |
| 2 | New ERP/PLM Prospects |
| 3 | Partners |
| 4 | Expansions |
| 5 | Collections |
| 6 | SDR Leads |
| 7 | Customer Success |
| 8 | PDR Leads |
| 11 | IFS Lead Enrichment |
| 12 | Aftermarket Nurture |
| 13 | BC/F&O Leads |
| 14 | IFS/Infor Leads |
| 15 | Acumatica/SYSPRO/Other Leads |
| 16 | New Pipeline |

---

## Stages by Pipeline

### Pipeline 1 -- Aftermarket

| Stage ID | Stage Name |
|---|---|
| 4 | Discovery |
| 5 | Prove |
| 43 | Propose |
| 6 | Contracts |

### Pipeline 2 -- New ERP/PLM Prospects

| Stage ID | Stage Name |
|---|---|
| 9 | Discovery |
| 10 | Prove |
| 11 | Propose |
| 12 | Contracts |

### Pipeline 3 -- Partners

| Stage ID | Stage Name |
|---|---|
| 15 | Discovery |
| 16 | Prove |
| 17 | Propose |
| 18 | Contracts |

### Pipeline 4 -- Expansions

| Stage ID | Stage Name |
|---|---|
| 27 | Discover (T-120 to T-90) |
| 28 | Prove (T-90 to T-60) |
| 29 | Propose (T-60 to T-30) |
| 55 | Selected (T-30) |
| 30 | Contract |

### Pipeline 5 -- Collections

| Stage ID | Stage Name |
|---|---|
| 34 | Owing - Under 20 days |
| 31 | Initial contact - Over 20 days |
| 63 | 1st Follow-up |
| 64 | 2nd Follow-up |
| 65 | Email & Phone Follow-up |
| 92 | Blocked |
| 32 | Payment agreed |
| 36 | Closed - Weekly |

### Pipeline 6 -- SDR Leads

| Stage ID | Stage Name |
|---|---|
| 45 | Data Maintenance |
| 44 | Nurture |
| 37 | Open |
| 38 | Working |
| 39 | Connected/Prospect |
| 40 | SDR Qualification |
| 42 | AE Qualification |

### Pipeline 7 -- Customer Success

| Stage ID | Stage Name |
|---|---|
| 60 | Clients |
| 98 | Q2 Tier A/B Renewals |
| 99 | Q2 Tier C Renewals |
| 100 | Q2 A/B Renewals Completed |
| 101 | Q2 C Renewals Completed |
| 50 | CADTALK - Implementing |
| 58 | Agni Link - Implementing |
| 51 | CADTALK - Active |
| 59 | Agni Link - Active |
| 104 | Migrated |
| 105 | Possible Churn |
| 73 | Churned |

### Pipeline 8 -- PDR Leads

| Stage ID | Stage Name |
|---|---|
| 66 | Nurture |
| 67 | Open |
| 68 | Working |
| 69 | Connected/Prospect |
| 70 | PDR Qualification |
| 71 | PM Qualification |

### Pipeline 11 -- IFS Lead Enrichment

| Stage ID | Stage Name |
|---|---|
| 85 | Open |
| 90 | Contact Attempted |
| 86 | Contact Made - ERP Confirmed |
| 87 | Mapping Underway |
| 88 | Partially Mapped |
| 89 | Mapped Lead |

### Pipeline 12 -- Aftermarket Nurture

| Stage ID | Stage Name |
|---|---|
| 93 | Qualified |
| 94 | Contact Made |
| 95 | Demo Scheduled |
| 96 | Proposal Made |
| 97 | Negotiations Started |

### Pipeline 13 -- BC/F&O Leads

| Stage ID | Stage Name |
|---|---|
| 123 | Nurture |
| 106 | Open |
| 107 | Contact Initiated |
| 108 | Contact Made |
| 109 | Discovery Booked |

### Pipeline 14 -- IFS/Infor Leads

| Stage ID | Stage Name |
|---|---|
| 124 | Nurture |
| 110 | Open |
| 111 | Contact Initiated |
| 112 | Contact Made |
| 113 | Discovery Booked |

### Pipeline 15 -- Acumatica/SYSPRO/Other Leads

| Stage ID | Stage Name |
|---|---|
| 125 | Nurture |
| 114 | Open |
| 115 | Contact Initiated |
| 116 | Contact Made |
| 117 | Discovery Booked |

### Pipeline 16 -- New Pipeline

| Stage ID | Stage Name |
|---|---|
| 118 | Qualified |
| 119 | Contact Made |
| 120 | Demo Scheduled |
| 121 | Proposal Made |
| 122 | Negotiations Started |

---

## Activity Types

Use the `type` key_string when calling `pipedrive_activities_create`.
Set `done: 1` for past activities, `done: 0` for scheduled future activities.

| ID | Name | key_string (use for `type` field) |
|---|---|---|
| 1 | Call-Active deal | `call` |
| 2 | Meeting-Proposal | `meeting` |
| 3 | Task | `task` |
| 5 | Email | `email` |
| 7 | Meeting-Demo | `demo` |
| 8 | Account Management | `account_management` |
| 9 | Partner Management | `partner_management` |
| 10 | Cold Call-No Answer | `cold_call` |
| 11 | Cold Email | `cold_email` |
| 12 | Meeting-Discovery | `discovery` |
| 13 | Cold Call - Answered | `cold_call___conversation` |
| 14 | Call - Meeting Booked | `call___meeting_booked` |
| 15 | Meeting-Negotiations | `meeting_negotiations` |
| 16 | Inbound Call | `inbound_call` |

---

## Products

Use `product_id` when calling `pipedrive_deal_products_add`.

| ID | Name |
|---|---|
| 4 | Margin |
| 5 | Software |
| 6 | Setup Fee |
| 104 | Customer Success |
| 105 | Fixed Implementation |
| 106 | Software: One-time discount |
| 108 | Services: One-Time Discount |
