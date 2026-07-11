# CADTALK Pipedrive Custom Field Reference

Last updated: 2026-07-11 (from data_fields exports)

**Scope: sales rep loop only.** Customer-success, billing, renewal, support, and internal-marketing fields (CSS, NPS, CSP, renewal/quarterly check-ins, FreshDesk/Chargebee/Invoice, license, lifecycle Status, Marketing Status/Assets, web-visitor plumbing) are intentionally excluded — the sales-crm writer does not touch them. They still exist in Pipedrive; they're just out of scope for this reference.

## How to use
- **Single option field** → pass option ID as integer: `field_key: 14`
- **Multiple option field** → pass option IDs as array: `field_key: [43, 44]`
- **Text / Large text / Relate field** → pass value directly: `field_key: "some text"` or `field_key: 12345` (record ID)
- **Date field** → pass as YYYY-MM-DD string: `field_key: "2026-09-30"`
- **Number / Monetary field** → pass as integer or float: `field_key: 50000`
- **Relate field (Person or Organization type)** → pass the numeric Pipedrive record ID (search first to find the ID)
- **API key** = the value in the "API key" column (hash string or short field name)

---

## DEAL Fields

### Dropdown Fields (use option IDs)

#### Forecast Category
- API key: `1a706bae5b0046828ae5a1b573c722bd96068058`
- Type: Single option
- Options:
  - `13` → Definitely
  - `14` → Probably
  - `15` → Maybe
  - `284` → Probably Not
  - `285` → No

#### Tier
- API key: `d38199423f99049250425b8d2f00b1e2832c661a`
- Type: Single option
- Options:
  - `363` → Tier A
  - `364` → Tier B
  - `373` → Tier C - Quiet
  - `394` → Tier C - Costly
  - `395` → Tier C - Problem

#### Health Score
- API key: `9e43542d72f1017c3c7d5a1619ff6b30c65cd9d3`
- Type: Single option
- Options:
  - `374` → Red
  - `375` → Yellow
  - `376` → Green
  - `460` → Unscored

#### Source channel
- API key: `channel`
- Type: Single option
- Options:
  - `264` → Inbound Website
  - `265` → Partner-PLM Publisher
  - `311` → Partner-ERP Publisher
  - `346` → Partner-CAD/PLM VAR/GSI
  - `347` → Partner-ERP VAR/GSI
  - `348` → Referral
  - `362` → Partner.io
  - `390` → Trade Show/User Conference
  - `391` → Webinar/Virtual Event
  - `392` → Email Campaign
  - `393` → Web Visitor - Outbound

#### Lost reason
- API key: `lost_reason`
- Type: Single option (Lost reason)
- Note: When marking a deal lost, also set `status: "lost"` in the update call
- Options:
  - `80` → Competitor-Value Not Proven
  - `81` → Competitor: Cost of Ownership too high
  - `82` → Product Fit: Did not meet requirements
  - `83` → Competitor-Critical functionality missing
  - `88` → Product Fit: Reliability or technical support
  - `89` → Product Fit: Missing Integration
  - `215` → Competitor-Price was Too High
  - `239` → Competitor-Feature Gap
  - `240` → DQ: No Budget
  - `241` → DQ: No Need
  - `242` → DQ: Timing not right
  - `243` → Product Fit: Negative Experience
  - `244` → Product Fit: Trial failure
  - `245` → No Decision: Stayed with current solution
  - `246` → No Decision: Champion could not get buy in
  - `247` → No Decision: No Authority
  - `248` → Data security concerns
  - `249` → Scalability concerns
  - `250` → Implementation: Too complex/too long
  - `251` → Legal: Contract T&C
  - `263` → DQ: BAD Data
  - `275` → Partner lost: Competitor
  - `276` → Partner Lost: NO Decision

#### Compelling Event *(a.k.a. Trigger Type)*
- API key: `fc04c8c4f1ec476b52805eeb68e8ee634a7f5854`
- Type: Single option
- Note: paired with the **Compelling Event Date** date field (`467d2b…`). Set both together.
- Options:
  - `336` → ERP change (new selection / major upgrade / cloud move)
  - `337` → PLM change (new rollout / upgrade / PDM→PLM)
  - `338` → CAD change (platform change / multi-CAD consolidation)
  - `339` → Manufacturing expansion (new plant/line / multi-site standardization)
  - `340` → NPI / Program launch (NPI/NPD/ETO/MTO)
  - `341` → Quality / Compliance mandate (audit findings/traceability/PPAP)
  - `342` → Supply-chain performance initiative (cost reduction, lead-time/OTD)
  - `343` → Integration modernization (iPaaS/ESB initiative or replace brittle custom)
  - `344` → M&A / Executive change (post-merger integration or new sponsor)
  - `345` → Other
---

### Deal Custom Text / Date / Number / Relate Fields

Pass values directly — no option ID lookup needed.

#### MEDDPICC Fields (Large text — pass as plain string)
| Field | API Key |
|---|---|
| MEDDPICC-Metrics | `bc8758d7a38ca8717dc6fa1953cbc5d9fb2386aa` |
| MEDDPICC-Economic Buyer | `7840e1da07759897a1ab77b326df0aac162c9742` |
| MEDDPICC-Decision Criteria | `2a9a94b8d55ce9ae1c3258667128b18b5651a95f` |
| MEDDPICC-Decision Process | `c15a5b78f3c77054896a7bff8f18a11631000fe3` |
| MEDDPICC-Paperwork Process | `4c319bdc3c30891c0a2aa9b46727307d306fbc45` |
| MEDDPICC-ID the Pain | `bc8545bb1ccc96fc858f3ba1c24370c7432ec086` |
| MEDDPICC-Champion | `15c0da01397abe35f21777a2bde7980eb86fe713` |
| MEDDPICC-Competition | `a8eaee25ee5d8a845fcd43cd4c09d8af16ecaa08` |
| MEDDPICC-Coach | `9630a483f8cfed06738edfb6983b7e8f91792b26` |

#### Feedback Fields (Large text — pass as plain string)
| Field | API Key |
|---|---|
| Feedback on Proposal | `11ccf0523794e2106def77d237e67a5af558846f` |
| Feedback on Demonstration | `fac33f3eebff2842168fae3f3a0a116c24d13fc4` |

#### Date Fields (pass as YYYY-MM-DD)
| Field | API Key |
|---|---|
| SQO Date | `6e75c1b17be487e2b52f2282ac4e06e39c90e3b5` |
| SQL Date | `80d471aaf715fb3bfd6320d1874949a864e0e909` |
| Compelling Event Date *(a.k.a. Trigger Date)* | `467d2b2404255773f9cb432405321334be7af2ef` |
| EB Last Direct Touch | `41662152f27ebaff54b95a09a1db24947e8e213f` |
| Latest web visit | `a729373c45a1852300cc3e18b136ebb1982e58ed` |

#### Relate Fields (pass the Pipedrive record ID as integer — search first)
| Field | Type | API Key |
|---|---|---|
| Partner Contact | Person ID | `3822d7bfd3ef5868838c59a50a082466301bab4a` |
| Partner Rep | Person ID | `a23c4576d5ef92465a18573e92fc434d1ac02b89` |
| Partner | Organization ID | `b64d21bb099713db82fad0f52bdfc2536e75252c` |
| Partner Organization | Organization ID | `e68fdddb4ec05f227c2b607947da2a36a524b350` |

---

### Deal Standard Fields

These use standard Pipedrive API field names — pass values directly, no hash key needed.

| Field | API Name | Value format |
|---|---|---|
| Title | `title` | Text string |
| Value | `value` | Number (deal amount) |
| Currency | `currency` | 3-letter code, e.g. `"USD"` |
| Expected close date | `expected_close_date` | YYYY-MM-DD |
| Probability | `probability` | Number 0–100 |
| Stage | `stage_id` | Stage ID (use `pipedrive_stages_list` to find) |
| Pipeline | `pipeline_id` | Pipeline ID |
| Status | `status` | `"open"`, `"won"`, or `"lost"` |
| Owner | `user_id` | User ID |
| Organization | `org_id` | Organization record ID |
| Contact person | `person_id` | Person record ID |
| ACV | `acv` | Monetary |
| ARR | `arr` | Monetary |
| MRR | `mrr` | Monetary |
| Visible to | `visible_to` | `1`=owner only, `3`=everyone |
| Score | `score` | Numerical |

---

## ORGANIZATION Fields

### Dropdown Fields (use option IDs)

#### Organization Type
- API key: `6ae364c9b85558dc16195fa5d7f1a103c3c12aa2`
- Type: Single option
- Options:
  - `19` → End user
  - `20` → CAD reseller
  - `21` → ERP reseller
  - `22` → CAD software publisher
  - `23` → ERP software publisher
  - `24` → PLM software publisher
  - `25` → Independent Consultant
  - `26` → Friend of CADTALK
  - `221` → News/Publication

#### Label
- API key: `label`
- Type: Single option
- Options:
  - `5` → Customer
  - `6` → Hot lead
  - `7` → Warm lead
  - `8` → Cold lead
  - `29` → Reseller
  - `116` → Cool Lead
  - `121` → Actively closing deal
  - `123` → Lost Deal
  - `127` → Microsoft Dynamics
  - `260` → Dream 100 Partner
  - `261` → Customer Story Prospect

#### Target System
- API key: `aa5aa1fc7b186d3c374ed613edeee5d7bf1b19d2`
- Type: Multiple options
- Options:
  - `38` → Infor CSI
  - `39` → Infor Visual
  - `40` → MS Dynamics BC
  - `41` → MS Dynamics F&O
  - `42` → QAD
  - `43` → IFS
  - `44` → SYSPRO
  - `45` → Acumatica
  - `46` → MYOB
  - `47` → Lexbiz (German Acumatica)
  - `48` → Sage X3
  - `49` → SAP 4/Hana
  - `50` → Oracle Netsuite
  - `52` → Infor LN
  - `67` → Infor M3
  - `68` → Epicor
  - `70` → SAP Business One
  - `87` → Arena PLM
  - `212` → Oracle JD Edwards
  - `295` → Priority ERP
  - `326` → GP
  - `327` → M1
  - `328` → Mietrack Pro
  - `329` → NAV
  - `330` → Priority

#### Source System
- API key: `e414c6d4c2487ea53dc006d5bc8835fb0af6b9fd`
- Type: Multiple options
- Options:
  - `53` → Solidworks
  - `54` → Solidworks PDM
  - `55` → Autodesk Inventor
  - `56` → Autodesk Vault
  - `57` → Autodesk Revit
  - `58` → Autodesk AutoCAD
  - `59` → Autodesk Fusion 360
  - `60` → PTC Creo
  - `61` → PTC Windchill
  - `62` → Siemens Solidedge
  - `63` → Siemens Teamcenter
  - `64` → PTC Arena PLM
  - `65` → Spreadsheet
  - `71` → Other
  - `72` → Tekla
  - `73` → Ennovia
  - `74` → General Database
  - `96` → Aveva
  - `132` → 3DX
  - `133` → Catia
  - `281` → Siemens NX
  - `282` → TBD
  - `294` → ShipConstructor

### Organization Custom Non-Dropdown Fields

#### Numerical Fields (pass as integer or float)

| Field | API Key |
|-------|---------|
| ERP Fit Score | `5e4b234610e26fe59b791d26d0934390fbd44c89` |
| PLM Fit Score | `be163b353da3d3fdde6364d13b3edeab27a0e615` |
| Interaction Fit Score | `884f5c3173580a23307141f80a45022e97d0a844` |

#### Date Fields (pass as YYYY-MM-DD)

| Field | API Key |
|-------|---------|
| CADTALK Renewal | `5796cd487f0fcab360287b82cfada4bc76db92fa` |
| Last Scored Date | `498f836fcbce170e202eebbd689a9e07acedc571` |
| Latest web visit | `55bfe5f3339809828615c72331d2029ad634b5c9` |

#### Text Fields (pass as plain string)

| Field | API Key |
|-------|---------|
| Revenue Range | `3509c95ed7feffc9c5483e2206f0c489852af533` |
| Company Email | `5cf6f02740b052550fa471aeee3a60503e6d6723` |
| Company Descriptions | `64c76bfcdb9bd4f8eeca28238c8b186eafe10679` |
| SIC Codes | `97623abea6e10c03b19e0358fd55328cf470e05e` |
| Website (custom) | `bf684efd9c61b4bb8c94144d2cdf9c39127754b4` |

#### Large Text Fields (pass as plain string)

| Field | API Key |
|-------|---------|
| NAICS Codes | `49919d664525620ca2601ff2e4505ed97d545453` |
| Collateral | `a8afdcc63f0b357925977c7d06deedbd042c0506` |

#### Phone Fields (pass as plain string)

| Field | API Key |
|-------|---------|
| Company Phone | `83fd951bf7c484f4a88cbbe830e84f8326163b1a` |
| Phone Number | `bc1dd986bcca7b4d7204891c2430502255040823` |

#### Relate Fields (pass Pipedrive record ID as integer — search first)

| Field | Links To | API Key |
|-------|----------|---------|
| Reference Contact | Person | `2d02dedc102c03c0939d80e5d4284a3ec15a0c08` |
| Source System VAR/GSI | Organization | `33b5e9ba5d2272462c261c43d7bb244947bc8caa` |
| Target System VAR/GSI | Organization | `e429940d53fcab7ee7f98f6adc62a98809d8d01e` |

### Organization Standard Fields

Standard fields use short names directly — no hash key.

| Field | API Name | Notes |
|-------|----------|-------|
| Name | `name` | Organization display name |
| Owner | `owner_id` | Numeric user ID |
| Website | `website` | Standard website field |
| LinkedIn | `linkedin` | LinkedIn URL |
| Employee Count | `employee_count` | Integer |
| Industry | `industry` | Text |
| Annual Revenue | `annual_revenue` | Monetary |
| Visibility | `visible_to` | 1=owner, 3=everyone |
| Label | `label` | Pipeline label |

---

## PERSON Fields

### Dropdown Fields (use option IDs)

#### Last Cold Call Result
- API key: `c0f7f94af27cebdfc7e5b9d7d70f22a9fcdaa78c`
- Type: Single option
- Options:
  - `185` → Contacted - Left Voicemail
  - `186` → Contacted - Left Message w/ Admin
  - `187` → Contacted - Verbal Contact - Referred On
  - `188` → Contacted - Verbal Contact - Not Interested
  - `189` → Contacted - Verbal Contact - Call Back
  - `190` → Contacted - Verbal Contact - Meeting Booked
  - `191` → No Contact - Wrong Number
  - `192` → Meeting Booked
  - `193` → Attempted Contact

#### Role
- API key: `f5d67b4aa3e4eed83649da00e9c3d5a48f892c01`
- Type: Multiple options
- Options:
  - `201` → Decision Maker
  - `202` → Economic Buyer
  - `203` → Technical Buyer
  - `204` → Champion
  - `205` → End User
  - `206` → Blocker
  - `207` → Influencer
  - `208` → Executive Sponsor

### Person Custom Non-Dropdown Fields

#### Date Fields (pass as YYYY-MM-DD)

| Field | API Key |
|-------|---------|
| Last Cold Call Date | `1bc3b82f930f4852ee7d3046c7cc3572c7bc2f2a` |

#### Numerical Fields (pass as integer or float)

| Field | API Key |
|-------|---------|
| Lead Score | `03302f440981024b67500e6433f64fa1139a379f` |

#### Text Fields (pass as plain string)

| Field | API Key |
|-------|---------|
| LinkedIn Profile | `225288986c53af10b1d4b5c70f6a30e238bf8e46` |

#### Phone Fields (pass as plain string)

| Field | API Key |
|-------|---------|
| Direct Phone Number | `d43370ff03c208a683ac739dab8da8bc4f010731` |
| Mobile Phone Number | `6d6a886f6acc014da73785800fdc732c2487e618` |

### Person Standard Fields

Standard fields use short names directly — no hash key.

| Field | API Name | Notes |
|-------|----------|-------|
| Full Name | `name` | Full display name |
| First Name | `first_name` | |
| Last Name | `last_name` | |
| Email | `email` | Array or string |
| Phone | `phone` | Array or string |
| Job Title | `job_title` | |
| Organization | `org_id` | Numeric org ID |
| Owner | `owner_id` | Numeric user ID |
| Birthday | `birthday` | YYYY-MM-DD |
| Visibility | `visible_to` | 1=owner, 3=everyone |
| Label | `label` | |

---

## LEAD Fields

*(No custom fields referenced — leads use title, owner_id, person_id, org_id, value, expected_close_date)*

---

## ACTIVITY Fields

*(No custom fields referenced — activities use subject, type, due_date, due_time, duration, user_id, deal_id, person_id, org_id, note, done)*

---

## PRODUCT Fields

### Category
- API key: `category`
- Type: Single option
- Options:
  - `9` → Implementation Services
  - `10` → Software
  - `11` → Commission
  - `12` → Reseller margin
