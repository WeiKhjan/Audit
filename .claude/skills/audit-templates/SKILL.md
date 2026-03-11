---
name: templates
description: Generate standard audit letters and document templates pre-filled with engagement data for Malaysian statutory audits
---

# Audit Letter & Document Templates

## Trigger

`/templates [type]` where `type` is one of:

| Type | Generates |
|------|-----------|
| `all` | All 16 templates (T1-T16) |
| `engagement` | Group A: T1, T2, T3 |
| `confirmations` | Group B: T4, T5, T6, T7, T8, T9, T10, T15, T16 |
| `completion` | Group C: T11, T12 |
| `differences` | Group D: T13, T14 |
| `T1` through `T16` | Individual template by code |

## Output Directory

All templates are generated under the engagement folder:

```
Clients/AWP_[ClientName]_FYE[Year]/T_Templates/
├── T1_Engagement_Letter.md
├── T2_PBC_Request_Letter.md
├── T3_Management_Letter.md
├── T4_Bank_Confirmation.md
├── T5_Bank_Authorization.md
├── T6_Debtor_Confirmation.md
├── T7_Creditor_Confirmation.md
├── T8_Director_Confirmation.md
├── T9_Legal_Confirmation.md
├── T10_Stock_Confirmation.md
├── T11_Management_Representation.md
├── T12_Director_Support_Letter.md
├── T13_Summary_Audit_Adjustments.md
├── T14_Summary_Uncorrected_Differences.md
├── T15_Director_Remuneration_Confirmation.md
└── T16_Director_Shareholding_Confirmation.md
```

## Templates Index

### Group A — Auditor-to-Client Letters

| Ref | Template | ISA | Pages |
|-----|----------|-----|-------|
| T1 | Engagement Letter | ISA 210 | ~2 |
| T2 | PBC Request Letter | Best Practice | ~2-3 |
| T3 | Management Letter | ISA 265 | ~2-4 |

### Group B — External Confirmation Letters

| Ref | Template | ISA | Pages |
|-----|----------|-----|-------|
| T4 | Bank Confirmation | ISA 505 | ~1 per bank |
| T5 | Bank Authorization Letter | ISA 505 | ~1 |
| T6 | Debtor/AR Confirmation | ISA 505 | ~1 per debtor |
| T7 | Creditor/AP Confirmation | ISA 505 | ~1 per creditor |
| T8 | Related Party/Director Confirmation | ISA 550 | ~2-3 per director |
| T9 | Legal Confirmation | ISA 501 | ~1 |
| T10 | Stock/Inventory Confirmation | ISA 505 | ~1 per warehouse |
| T15 | Directors' Remuneration Confirmation | CA 2016 s.230 / MPERS S33 | ~2-3 per director |
| T16 | Directors' Shareholding Confirmation | CA 2016 s.59 / s.230 | ~2-3 per director |

### Group C — Client-to-Auditor Letters

| Ref | Template | ISA | Pages |
|-----|----------|-----|-------|
| T11 | Management Representation Letter | ISA 580 | ~3-4 |
| T12 | Director Support Letter | ISA 570 | ~1 |

### Group D — Audit Differences (Client Sign-off)

| Ref | Template | ISA | Pages |
|-----|----------|-----|-------|
| T13 | Summary of Audit Adjustments | ISA 450 | ~1-2 |
| T14 | Summary of Uncorrected Audit Differences | ISA 450 | ~1-2 |

---

## Variable System

All templates use `{{variable}}` placeholders. Variables are sourced from `master_data.json` in the engagement folder. If `master_data.json` is not found or a variable is missing, the `{{variable}}` placeholder is left intact for manual completion.

### Required master_data.json Variables

```json
{
  "client_name": "Full registered company name",
  "client_registration_no": "SSM registration number",
  "client_address": "Registered address",
  "client_business_nature": "Principal activities",
  "financial_year_end": "YYYY-MM-DD",
  "prior_year_end": "YYYY-MM-DD",
  "reporting_framework": "MPERS or MFRS",
  "currency": "RM",
  "audit_firm_name": "Audit firm name",
  "audit_firm_address": "Audit firm address",
  "audit_firm_tel": "Audit firm telephone",
  "audit_firm_email": "Audit firm email",
  "audit_firm_af_no": "Audit firm AF number (MIA)",
  "engagement_partner": "Engagement partner name",
  "engagement_partner_approval_no": "MIA approval number",
  "engagement_manager": "Engagement manager name",
  "audit_fee": "Audit fee amount",
  "bank_name": "Primary bank name",
  "bank_branch": "Bank branch",
  "bank_branch_address": "Bank branch full address",
  "bank_account_numbers": ["Account 1", "Account 2"],
  "lawyer_name": "Lawyer name",
  "lawyer_firm": "Law firm name",
  "lawyer_address": "Law firm address",
  "pbc_deadline_date": "YYYY-MM-DD",
  "audit_report_date": "YYYY-MM-DD",
  "audit_fieldwork_start": "YYYY-MM-DD",
  "audit_fieldwork_end": "YYYY-MM-DD",
  "director_names": ["Director 1", "Director 2"],
  "director_ic_numbers": ["IC 1", "IC 2"],
  "company_secretary": "Company secretary name",
  "materiality_amount": "Planning materiality figure",
  "performance_materiality": "Performance materiality figure"
}
```

---

## Generation Instructions

### When `/templates all` is invoked:

1. Read `master_data.json` from the engagement folder (if it exists)
2. Create the `T_Templates/` directory if it does not exist
3. Generate all 14 templates (T1-T14) in `T_Templates/`
4. Substitute `{{variable}}` placeholders with values from `master_data.json` where available
5. Leave `{{variable}}` placeholders intact where no value is provided
6. Update `00_Index.md` in the engagement folder to add Section T listing
7. Confirm generation with a summary table showing all 14 files

### When a specific template is requested (e.g., `/templates T4`):

1. Read `master_data.json` from the engagement folder (if it exists)
2. Create the `T_Templates/` directory if it does not exist
3. Generate only the requested template
4. Apply the same variable substitution approach
5. Update `00_Index.md` if Section T is not already listed

### When a group is requested (e.g., `/templates confirmations`):

1. Same steps as above but generate all templates in the specified group
2. Groups: `engagement` (T1-T3), `confirmations` (T4-T10), `completion` (T11-T12), `differences` (T13-T14)

---

## Common Letterhead Block

Every template begins with this letterhead block:

```markdown
---
**{{audit_firm_name}}**
{{audit_firm_address}}
Tel: {{audit_firm_tel}} | Email: {{audit_firm_email}}
AF No: {{audit_firm_af_no}}

**PRIVATE & CONFIDENTIAL**

Date: {{letter_date}}
---
```

For client-to-auditor letters (T11, T12, T13, T14), the letterhead uses the client's details instead:

```markdown
---
**{{client_name}}**
({{client_registration_no}})
{{client_address}}

Date: {{letter_date}}
---
```

---

## Detailed Template Specifications

---

### T1: Engagement Letter (ISA 210)

**File:** `T1_Engagement_Letter.md`
**ISA Reference:** ISA 210 — Agreeing the Terms of Audit Engagements
**Malaysian-Specific:** Companies Act 2016 s.266 (appointment of auditors), MIA By-Laws on Professional Ethics, Conduct and Practice

#### Structure

```
1. LETTERHEAD BLOCK (audit firm)
2. ADDRESSEE
   - To: The Board of Directors
   - {{client_name}}
   - {{client_address}}
3. SUBJECT LINE
   - "Re: Audit of Financial Statements for the Financial Year Ended {{financial_year_end}}"
4. BODY SECTIONS
   4.1 Introduction & Scope
       - Purpose of the letter
       - Financial statements to be audited (SOFP, SOCI, SOCIE, SCF, Notes)
       - Reporting framework: {{reporting_framework}}
       - Financial year: {{prior_year_end}} to {{financial_year_end}}
   4.2 Auditor's Responsibilities
       - Conduct audit in accordance with ISA as adopted in Malaysia
       - Obtain reasonable assurance that FS are free from material misstatement
       - Assess internal controls relevant to the audit
       - Right to modify audit opinion (qualified, adverse, disclaimer)
       - Communicate key audit matters to TCWG
       - ISA 240: Responsibility to consider fraud
       - ISA 250: Responsibility regarding laws and regulations
   4.3 Directors' Responsibilities
       - Preparation of FS in accordance with {{reporting_framework}}
       - Internal controls to prevent and detect fraud and error
       - Provide access to all records, documents, and information
       - Provide written representations (Management Representation Letter)
       - Inform auditor of all known actual or possible non-compliance with laws
       - Companies Act 2016 s.248: Directors responsible for FS giving true and fair view
   4.4 Inherent Limitations
       - Audit is not designed to detect all misstatements
       - Inherent limitations of internal controls
       - Sampling and testing basis
       - Fraud may involve collusion, forgery, deliberate omission
   4.5 Audit Fee and Billing
       - Agreed audit fee: {{audit_fee}}
       - Fee basis (fixed/hourly), disbursements, billing schedule
       - SST on professional fees (if applicable)
   4.6 Planned Timing
       - Fieldwork: {{audit_fieldwork_start}} to {{audit_fieldwork_end}}
       - Target audit report date: {{audit_report_date}}
       - PBC deadline: {{pbc_deadline_date}}
   4.7 Communication with TCWG
       - Significant findings communicated to directors
       - Management letter on internal control weaknesses (ISA 265)
   4.8 Data Protection
       - PDPA 2010 compliance statement
       - Confidentiality of client information
   4.9 Acceptance and Confirmation
       - Request for counter-signature
       - Statement that terms remain in effect for subsequent audits unless revised
5. SIGNATURE BLOCKS
   5.1 Audit Firm Signature
       - {{engagement_partner}}
       - {{engagement_partner_approval_no}}
       - {{audit_firm_name}}
       - Date
   5.2 Client Acknowledgment
       - "Acknowledged and agreed on behalf of the Board of Directors of {{client_name}}"
       - Director Name: _______________
       - Designation: _______________
       - Date: _______________
       - Director Name: _______________
       - Designation: _______________
       - Date: _______________
```

#### Variables Used

`{{audit_firm_name}}`, `{{audit_firm_address}}`, `{{audit_firm_tel}}`, `{{audit_firm_email}}`, `{{audit_firm_af_no}}`, `{{client_name}}`, `{{client_address}}`, `{{client_registration_no}}`, `{{financial_year_end}}`, `{{prior_year_end}}`, `{{reporting_framework}}`, `{{engagement_partner}}`, `{{engagement_partner_approval_no}}`, `{{audit_fee}}`, `{{audit_fieldwork_start}}`, `{{audit_fieldwork_end}}`, `{{audit_report_date}}`, `{{pbc_deadline_date}}`

#### Key Malaysian Requirements

- Reference to Companies Act 2016 s.248 (directors' responsibility for FS) and s.266 (auditor appointment)
- MIA By-Laws on Professional Ethics, Conduct and Practice
- PDPA 2010 data protection clause
- SST on audit fees (6% service tax where applicable)
- Reporting framework must specify MPERS or MFRS explicitly

#### Signature Requirements

- Signed by engagement partner with MIA approval number
- Counter-signed by at least two directors of the client company

---

### T2: PBC Request Letter (Best Practice)

**File:** `T2_PBC_Request_Letter.md`
**ISA Reference:** Best practice (supports ISA 230 documentation, ISA 500 audit evidence)
**Malaysian-Specific:** Companies Act 2016 record-keeping requirements, SSM filings

#### Structure

```
1. LETTERHEAD BLOCK (audit firm)
2. ADDRESSEE
   - To: The Directors / Person-in-charge of Accounts
   - {{client_name}}
   - {{client_address}}
3. SUBJECT LINE
   - "Re: Prepared-by-Client (PBC) Documents for Audit — FYE {{financial_year_end}}"
4. BODY SECTIONS
   4.1 Introduction
       - Purpose: request for documents and information
       - Deadline: {{pbc_deadline_date}}
       - Contact person for queries: {{engagement_manager}}
   4.2 PBC Document List
       Auto-populated from H1 PBC Checklist. Standard categories:

       A. STATUTORY & CORPORATE
          - Certificate of Incorporation / SSM Form 9
          - Constitution (Memorandum & Articles of Association)
          - Register of Members, Directors, Secretaries
          - Board/AGM/EGM minutes for the financial year
          - SSM Annual Return (latest)
          - Business licenses and permits

       B. ACCOUNTING RECORDS
          - Trial balance as at {{financial_year_end}}
          - General ledger for the financial year
          - Bank statements (all accounts) — 12 months + 1 month post year-end
          - Bank reconciliations as at {{financial_year_end}}
          - Fixed asset register
          - Receivable aging / loan listing
          - Payable aging
          - Inventory listing (if applicable)
          - Payroll summary and EPF/SOCSO submissions

       C. TAX & COMPLIANCE
          - Latest tax return (Form C/Form C1)
          - Tax assessment / deemed assessment notices
          - SST returns (if applicable)
          - Transfer pricing documentation (if applicable)
          - Tax computation for current and prior year
          - Withholding tax records (s.109, s.109B)

       D. CONTRACTS & AGREEMENTS
          - Loan agreements, facility letters
          - Hire purchase agreements
          - Tenancy / lease agreements
          - Related party agreements
          - Major contracts entered during the year

       E. OTHER DOCUMENTS
          - Insurance policies schedule
          - Confirmation reply letters (bank, debtor, creditor, legal)
          - Prior year audited financial statements
          - Prior year management letter and status of issues raised
   4.3 Delivery Instructions
       - Format: softcopy (PDF/Excel preferred) and/or hardcopy
       - Naming convention for softcopy files
       - Delivery deadline: {{pbc_deadline_date}}
   4.4 Important Notes
       - Outstanding items may delay audit completion
       - Additional items may be requested during fieldwork
5. SIGNATURE BLOCK
   - {{engagement_manager}} / {{engagement_partner}}
   - {{audit_firm_name}}
```

#### Variables Used

`{{audit_firm_name}}`, `{{audit_firm_address}}`, `{{audit_firm_tel}}`, `{{audit_firm_email}}`, `{{client_name}}`, `{{client_address}}`, `{{financial_year_end}}`, `{{pbc_deadline_date}}`, `{{engagement_manager}}`, `{{engagement_partner}}`, `{{audit_firm_af_no}}`

#### Key Malaysian Requirements

- SSM filings (Form 9, Annual Return) specific to Malaysian companies
- EPF (Employees Provident Fund) and SOCSO contribution records
- SST (Sales and Service Tax) returns
- Transfer pricing documentation per Malaysian TP Guidelines
- Withholding tax under Income Tax Act 1967 s.109/s.109B

#### Cross-Reference

- Links to H1 PBC Checklist — auto-populate the document list from H1 items
- Each PBC item should have a status column (Received / Outstanding / N/A)

#### Signature Requirements

- Signed by engagement manager or engagement partner

---

### T3: Management Letter (ISA 265)

**File:** `T3_Management_Letter.md`
**ISA Reference:** ISA 265 — Communicating Deficiencies in Internal Control to Those Charged with Governance and Management
**Malaysian-Specific:** Companies Act 2016 s.248(4) directors' duties, MIA Practice Note

#### Structure

```
1. LETTERHEAD BLOCK (audit firm)
2. ADDRESSEE
   - To: The Board of Directors
   - {{client_name}}
   - {{client_address}}
3. SUBJECT LINE
   - "Re: Management Letter — Audit for FYE {{financial_year_end}}"
4. BODY SECTIONS
   4.1 Introduction
       - Conducted audit of FS for FYE {{financial_year_end}}
       - Purpose: communicate control deficiencies and recommendations
       - Note: not a comprehensive review of internal controls
   4.2 Status of Prior Year Issues
       - Table: Ref | Prior Year Issue | Management Response | Current Status (Resolved/Recurring)
       - Placeholder rows for prior year items
   4.3 Current Year Observations
       - For each observation:
         - Reference number (ML-YYYY-001 format)
         - Area / audit section
         - Observation: description of deficiency
         - Risk / implication: potential impact
         - Recommendation: suggested improvement
         - Management response: (to be completed by client)
         - Priority: High / Medium / Low
       - Minimum 5 placeholder rows
   4.4 Classification of Deficiencies
       - Significant deficiency: must be communicated to TCWG (ISA 265.9)
       - Other deficiency: communicated to management (ISA 265.10)
       - Material weakness: considered for impact on audit opinion
   4.5 Disclaimer
       - Not an exhaustive list of all deficiencies
       - Audit was not designed to identify all internal control matters
       - No opinion on effectiveness of internal controls
   4.6 Acknowledgment Request
       - Request management to sign and return acknowledgment
5. SIGNATURE BLOCKS
   5.1 Audit Firm
       - {{engagement_partner}}
       - {{engagement_partner_approval_no}}
       - {{audit_firm_name}}
   5.2 Client Acknowledgment
       - Director Name: _______________
       - Designation: _______________
       - Date: _______________
```

#### Variables Used

`{{audit_firm_name}}`, `{{audit_firm_address}}`, `{{audit_firm_tel}}`, `{{audit_firm_email}}`, `{{audit_firm_af_no}}`, `{{client_name}}`, `{{client_address}}`, `{{financial_year_end}}`, `{{engagement_partner}}`, `{{engagement_partner_approval_no}}`

#### Key Malaysian Requirements

- Companies Act 2016 s.248(4): Directors must ensure adequate internal controls
- Reference MIA practice guidance on communicating deficiencies
- Distinguish significant deficiencies requiring TCWG communication (ISA 265.9)

#### Signature Requirements

- Signed by engagement partner
- Client acknowledgment by at least one director

---

### T4: Bank Confirmation (ISA 505)

**File:** `T4_Bank_Confirmation.md`
**ISA Reference:** ISA 505 — External Confirmations
**Malaysian-Specific:** Standard bank confirmation format recognized by Association of Banks in Malaysia (ABM)

#### Structure

```
1. LETTERHEAD BLOCK (audit firm)
2. ADDRESSEE
   - To: The Manager
   - {{bank_name}}, {{bank_branch}}
   - {{bank_branch_address}}
3. SUBJECT LINE
   - "Re: Audit Confirmation Request — {{client_name}} ({{client_registration_no}})"
4. BODY SECTIONS
   4.1 Introduction
       - We are the statutory auditors of {{client_name}}
       - Request confirmation of the following as at {{financial_year_end}}
   4.2 Information Requested
       A. DEPOSIT ACCOUNTS
          - Account number(s): {{bank_account_numbers}}
          - Type (current/savings/fixed deposit)
          - Balance as at {{financial_year_end}}
          - Interest rate
          - Maturity date (for FDs)
          - Any lien or encumbrance

       B. LOAN AND FINANCING FACILITIES
          - Type of facility (term loan, overdraft, trade financing, LC, BG, etc.)
          - Facility limit
          - Outstanding balance as at {{financial_year_end}}
          - Interest/profit rate
          - Repayment terms
          - Maturity date
          - Security/collateral pledged

       C. CONTINGENT LIABILITIES
          - Bank guarantees issued
          - Letters of credit outstanding
          - Bills discounted
          - Any other contingent items

       D. SECURITIES AND COLLATERAL
          - Details of securities held by the bank
          - Fixed deposits pledged
          - Property charges
          - Personal/corporate guarantees given

       E. AUTHORIZED SIGNATORIES
          - Names of authorized signatories on the account(s)
          - Signing mandate (single/joint)

       F. OTHER INFORMATION
          - Safe deposit boxes
          - Any set-off arrangements
          - Any default or breach of covenant
          - Accounts closed during the financial year
   4.3 Reply Instructions
       - Please reply directly to the auditors at:
       - {{audit_firm_name}}
       - {{audit_firm_address}}
       - Attention: {{engagement_manager}}
       - Reference: CONF/BANK/{{client_name}}/{{financial_year_end}}
   4.4 Authorization
       - This confirmation is requested with the authorization of {{client_name}}
       - A copy of the bank authorization letter is enclosed (ref: T5)
5. SIGNATURE BLOCKS
   5.1 Audit Firm
       - {{engagement_partner}}
       - {{engagement_partner_approval_no}}
       - {{audit_firm_name}}
   5.2 Bank Reply Section
       - "We confirm the above information is correct / We note the following exceptions:"
       - Authorized Signatory: _______________
       - Name & Designation: _______________
       - Bank Stamp: _______________
       - Date: _______________
```

#### Variables Used

`{{audit_firm_name}}`, `{{audit_firm_address}}`, `{{audit_firm_tel}}`, `{{audit_firm_email}}`, `{{audit_firm_af_no}}`, `{{client_name}}`, `{{client_registration_no}}`, `{{financial_year_end}}`, `{{bank_name}}`, `{{bank_branch}}`, `{{bank_branch_address}}`, `{{bank_account_numbers}}`, `{{engagement_partner}}`, `{{engagement_partner_approval_no}}`, `{{engagement_manager}}`

#### Key Malaysian Requirements

- ABM (Association of Banks in Malaysia) standard confirmation format
- Islamic banking facilities use "profit rate" terminology instead of "interest rate"
- Include both conventional and Islamic financing sections where relevant
- Bank Negara Malaysia compliance references where applicable

#### Signature Requirements

- Signed by engagement partner
- Bank reply section with authorized signatory and bank stamp
- Must generate one confirmation per bank (if multiple banks, generate multiple T4 files: T4a, T4b, etc.)

---

### T5: Bank Authorization Letter (ISA 505)

**File:** `T5_Bank_Authorization.md`
**ISA Reference:** ISA 505 — External Confirmations (client authorization)
**Malaysian-Specific:** Standard format accepted by Malaysian banks

#### Structure

```
1. LETTERHEAD BLOCK (client letterhead)
   - {{client_name}}
   - ({{client_registration_no}})
   - {{client_address}}
2. ADDRESSEE
   - To: The Manager
   - {{bank_name}}, {{bank_branch}}
   - {{bank_branch_address}}
3. SUBJECT LINE
   - "Re: Authorization to Release Information to Auditors"
4. BODY SECTIONS
   4.1 Authorization Statement
       - We, the undersigned directors of {{client_name}}, hereby authorize and request you to provide
         the following information directly to our statutory auditors:
       - Auditors: {{audit_firm_name}}
       - Address: {{audit_firm_address}}
   4.2 Scope of Authorization
       - All account balances (current, savings, fixed deposits)
       - All loan and financing facility details
       - All contingent liabilities and commitments
       - Securities and collateral information
       - Authorized signatory details
       - Any other information the auditors may request in connection with their audit
   4.3 Account References
       - Account number(s): {{bank_account_numbers}}
       - Period: Financial year ended {{financial_year_end}}
   4.4 Validity
       - This authorization is valid for the purpose of the statutory audit for FYE {{financial_year_end}}
5. SIGNATURE BLOCKS
   - Two director signatures required:
   - Director 1:
     - Name: {{director_names[0]}}
     - IC No: {{director_ic_numbers[0]}}
     - Signature: _______________
     - Date: _______________
   - Director 2:
     - Name: {{director_names[1]}}
     - IC No: {{director_ic_numbers[1]}}
     - Signature: _______________
     - Date: _______________
   - Company Stamp
```

#### Variables Used

`{{client_name}}`, `{{client_registration_no}}`, `{{client_address}}`, `{{bank_name}}`, `{{bank_branch}}`, `{{bank_branch_address}}`, `{{bank_account_numbers}}`, `{{audit_firm_name}}`, `{{audit_firm_address}}`, `{{financial_year_end}}`, `{{director_names}}`, `{{director_ic_numbers}}`

#### Key Malaysian Requirements

- IC (Identity Card / MyKad) numbers required for Malaysian directors
- Passport numbers for foreign directors
- Company stamp (common seal if applicable) is customary
- Two director signatures typically required by Malaysian banks

#### Signature Requirements

- Minimum two directors must sign
- IC / passport number required alongside each signature
- Company stamp / common seal

---

### T6: Debtor/AR Confirmation (ISA 505)

**File:** `T6_Debtor_Confirmation.md`
**ISA Reference:** ISA 505 — External Confirmations (positive confirmation)
**Malaysian-Specific:** For money lenders (Moneylenders Act 1951 / applicable state laws): include loan balance and accrued interest

#### Structure

```
1. LETTERHEAD BLOCK (audit firm)
2. ADDRESSEE
   - To: {{debtor_name}}
   - {{debtor_address}}
3. SUBJECT LINE
   - "Re: Confirmation of Balance — {{client_name}} ({{client_registration_no}})"
4. BODY SECTIONS
   4.1 Introduction
       - We are the statutory auditors of {{client_name}}
       - Request confirmation of balance as at {{financial_year_end}}
   4.2 Balance Details (Standard Trade Receivables)
       - Per our client's records, the amount due from you as at {{financial_year_end}} is:
       - Trade receivable balance: RM {{debtor_balance}}
       - Other amounts (if any): RM {{debtor_other_amounts}}
       - Total: RM {{debtor_total}}
   4.3 Balance Details (Money Lender / Loan Receivable Variant)
       - Loan reference number: {{loan_reference}}
       - Principal outstanding: RM {{loan_principal}}
       - Accrued interest receivable: RM {{loan_accrued_interest}}
       - Total amount due: RM {{loan_total_due}}
       - Interest rate: {{loan_interest_rate}}
       - Maturity date: {{loan_maturity_date}}
       - Security / collateral: {{loan_security}}
   4.4 Confirmation Request (Positive Format)
       - "Please confirm directly to our auditors whether the above balance is correct."
       - "If the balance differs from your records, please provide details of the difference."
   4.5 Reply Instructions
       - Reply directly to: {{audit_firm_name}}, {{audit_firm_address}}
       - Attention: {{engagement_manager}}
       - Reference: CONF/DR/{{client_name}}/{{financial_year_end}}
5. REPLY SECTION
   - [ ] We confirm the above balance is correct as at {{financial_year_end}}
   - [ ] The balance per our records differs. Details:
     - Balance per our records: RM _______________
     - Reason for difference: _______________
   - Authorized Signatory: _______________
   - Name & Designation: _______________
   - Company Stamp: _______________
   - Date: _______________
6. AUDIT FIRM SIGNATURE
   - {{engagement_partner}}
   - {{audit_firm_name}}
```

#### Variables Used

`{{audit_firm_name}}`, `{{audit_firm_address}}`, `{{audit_firm_tel}}`, `{{audit_firm_email}}`, `{{client_name}}`, `{{client_registration_no}}`, `{{financial_year_end}}`, `{{debtor_name}}`, `{{debtor_address}}`, `{{debtor_balance}}`, `{{debtor_other_amounts}}`, `{{debtor_total}}`, `{{loan_reference}}`, `{{loan_principal}}`, `{{loan_accrued_interest}}`, `{{loan_total_due}}`, `{{loan_interest_rate}}`, `{{loan_maturity_date}}`, `{{loan_security}}`, `{{engagement_partner}}`, `{{engagement_manager}}`

#### Key Malaysian Requirements

- Money lender variant includes loan balance, accrued interest, interest rate, security details
- Licensed moneylender must comply with Moneylenders Act 1951 interest rate caps
- For Islamic financing: use "profit" instead of "interest" terminology
- Ringgit Malaysia (RM) currency denomination

#### Signature Requirements

- Audit firm: signed by engagement partner
- Reply section: debtor's authorized signatory with company stamp

---

### T7: Creditor/AP Confirmation (ISA 505)

**File:** `T7_Creditor_Confirmation.md`
**ISA Reference:** ISA 505 — External Confirmations (negative confirmation option for completeness)
**Malaysian-Specific:** Supports completeness assertion for trade payables

#### Structure

```
1. LETTERHEAD BLOCK (audit firm)
2. ADDRESSEE
   - To: {{creditor_name}}
   - {{creditor_address}}
3. SUBJECT LINE
   - "Re: Confirmation of Balance — {{client_name}} ({{client_registration_no}})"
4. BODY SECTIONS
   4.1 Introduction
       - We are the statutory auditors of {{client_name}}
       - Request confirmation of amount owed TO you as at {{financial_year_end}}
   4.2 Balance Details
       - Per our client's records, the amount owed to you as at {{financial_year_end}} is:
       - Trade payable balance: RM {{creditor_balance}}
       - Other amounts (if any): RM {{creditor_other_amounts}}
       - Total: RM {{creditor_total}}
   4.3 Confirmation Request (Negative Confirmation Option)
       - POSITIVE: "Please confirm directly to our auditors whether the above balance is correct."
       - NEGATIVE: "If you do NOT agree with the above balance, please reply directly to our auditors
         with details of the difference. If no reply is received within 14 days, we will assume the
         balance is confirmed."
       - Select format based on engagement risk assessment
   4.4 Reply Instructions
       - Reply directly to: {{audit_firm_name}}, {{audit_firm_address}}
       - Attention: {{engagement_manager}}
       - Reference: CONF/CR/{{client_name}}/{{financial_year_end}}
5. REPLY SECTION
   - [ ] We confirm the above balance is correct as at {{financial_year_end}}
   - [ ] The balance per our records differs. Details:
     - Balance per our records: RM _______________
     - Reason for difference: _______________
   - Authorized Signatory: _______________
   - Name & Designation: _______________
   - Company Stamp: _______________
   - Date: _______________
6. AUDIT FIRM SIGNATURE
   - {{engagement_partner}}
   - {{audit_firm_name}}
```

#### Variables Used

`{{audit_firm_name}}`, `{{audit_firm_address}}`, `{{audit_firm_tel}}`, `{{audit_firm_email}}`, `{{client_name}}`, `{{client_registration_no}}`, `{{financial_year_end}}`, `{{creditor_name}}`, `{{creditor_address}}`, `{{creditor_balance}}`, `{{creditor_other_amounts}}`, `{{creditor_total}}`, `{{engagement_partner}}`, `{{engagement_manager}}`

#### Key Malaysian Requirements

- Completeness assertion is the primary assertion tested for creditors (ISA 505)
- Negative confirmation acceptable when: risk of material misstatement is low, large number of small balances, no reason to believe respondents will disregard
- 14-day response window is standard practice in Malaysia

#### Signature Requirements

- Audit firm: signed by engagement partner
- Reply section: creditor's authorized signatory with company stamp

---

### T8: Related Party/Director Confirmation (ISA 550)

**File:** `T8_Director_Confirmation.md`
**ISA Reference:** ISA 550 — Related Parties; ISA 505 — External Confirmations
**Malaysian-Specific:** MPERS Section 33 Related Party Disclosures, Companies Act 2016 s.221-228 (directors' duties and interests)

#### Structure

```
1. LETTERHEAD BLOCK (audit firm)
2. ADDRESSEE
   - To: {{director_name}}
   - IC No: {{director_ic_number}}
   - [Director address]
3. SUBJECT LINE
   - "Re: Director's Confirmation — {{client_name}} FYE {{financial_year_end}}"
4. BODY SECTIONS
   4.1 Introduction
       - Purpose: confirm related party information for audit purposes
       - Period: financial year ended {{financial_year_end}}

   4.2 SECTION A — Balance Confirmation
       - Amount due from director to the company: RM _______________
       - Amount due from the company to director: RM _______________
       - Director's current account balance: RM _______________
       - Any security provided for the above balances: _______________

   4.3 SECTION B — Transaction Confirmation
       - Details of transactions with the company during the financial year:
         | Date | Description | Amount (RM) | Terms |
         |------|-------------|-------------|-------|
         | | | | |
       - Includes: remuneration, fees, loans, advances, purchases/sales, rental, management fees

   4.4 SECTION C — Related Party Declarations
       - List of entities in which the director has:
         - Direct or indirect shareholding (>= 20%)
         - Directorship or key management position
         - Significant influence or control
       - Table:
         | Entity Name | Reg. No. | Relationship | Nature of Interest |
         |-------------|----------|--------------|-------------------|
         | | | | |

   4.5 SECTION D — Interests in Contracts (Companies Act 2016 s.221)
       - Disclosure of any contracts or proposed contracts with the company in which
         the director has direct or indirect interest
       - Table:
         | Contract Description | Counterparty | Director's Interest | Value (RM) |
         |---------------------|--------------|---------------------|-----------|
         | | | | |

   4.6 SECTION E — Remuneration and Benefits
       - Director's fees: RM _______________
       - Salary and bonus: RM _______________
       - Benefits-in-kind: RM _______________
       - EPF contributions: RM _______________
       - Other emoluments: RM _______________
       - Total: RM _______________

   4.7 SECTION F — RPT Completeness Assertion
       - "I confirm that all related party transactions and balances have been disclosed to the auditors."
       - "I confirm that all my interests in contracts with the company have been disclosed per s.221."
       - "I am not aware of any other related party relationships or transactions not disclosed above."

   4.8 SECTION G — Other Matters
       - Any litigation, claims, or assessments involving the director and the company
       - Any personal guarantees given for company obligations
       - Any subsequent events after year-end involving the director and company
5. SIGNATURE BLOCK
   - Director's Declaration:
     - "I confirm the above information is complete and accurate."
     - Name: {{director_name}}
     - IC No: {{director_ic_number}}
     - Signature: _______________
     - Date: _______________
```

#### Variables Used

`{{audit_firm_name}}`, `{{audit_firm_address}}`, `{{audit_firm_tel}}`, `{{audit_firm_email}}`, `{{client_name}}`, `{{client_registration_no}}`, `{{financial_year_end}}`, `{{director_names}}`, `{{director_ic_numbers}}`, `{{engagement_partner}}`, `{{engagement_partner_approval_no}}`

#### Key Malaysian Requirements

- Companies Act 2016 s.221: Director must disclose interests in contracts
- Companies Act 2016 s.222-228: General duties of directors
- MPERS Section 33: Related Party Disclosures requirements
- MFRS 124: Related Party Disclosures (if MFRS reporting)
- Must generate one confirmation per director
- IC (MyKad) number required for Malaysian directors, passport for foreign directors

#### Signature Requirements

- Each director must individually sign their own confirmation
- IC number alongside signature
- Generate T8a, T8b, etc. if multiple directors

---

### T9: Legal Confirmation (ISA 501)

**File:** `T9_Legal_Confirmation.md`
**ISA Reference:** ISA 501 — Audit Evidence — Specific Considerations for Selected Items (litigation and claims)
**Malaysian-Specific:** Malaysian legal system, High Court proceedings, Malaysian Bar Council practice

#### Structure

```
1. LETTERHEAD BLOCK (audit firm)
2. ADDRESSEE
   - To: {{lawyer_name}}
   - {{lawyer_firm}}
   - {{lawyer_address}}
3. SUBJECT LINE
   - "Re: Legal Confirmation — {{client_name}} ({{client_registration_no}}) — FYE {{financial_year_end}}"
4. BODY SECTIONS
   4.1 Introduction
       - We are the statutory auditors of {{client_name}}
       - Request confirmation of legal matters as at {{financial_year_end}}
       - This request is made with the authorization of the client (authorization letter enclosed)
   4.2 Litigation and Claims
       - "Please provide details of any pending or threatened litigation, claims, or assessments
         involving {{client_name}} as at {{financial_year_end}} and up to the date of your reply:"
       - For each matter:
         | Item | Details |
         |------|---------|
         | Case reference | |
         | Court / tribunal | |
         | Parties involved | |
         | Nature of claim | |
         | Amount claimed / disputed | RM |
         | Current status | |
         | Likelihood of outcome (probable/possible/remote) | |
         | Estimated financial exposure | RM |
         | Expected resolution date | |
   4.3 Unasserted Claims
       - "Are you aware of any unasserted claims or assessments that are probable of assertion
         and may result in an unfavorable outcome?"
   4.4 Legal Fees
       - Outstanding legal fees as at {{financial_year_end}}: RM _______________
       - Unbilled work-in-progress as at {{financial_year_end}}: RM _______________
   4.5 Other Matters
       - Any other matters that may require disclosure in the financial statements
       - Any regulatory or compliance matters
   4.6 Reply Instructions
       - Reply directly to: {{audit_firm_name}}, {{audit_firm_address}}
       - Attention: {{engagement_manager}}
       - Reference: CONF/LEGAL/{{client_name}}/{{financial_year_end}}
       - "This letter serves as the client's authorization for you to communicate directly with us."
5. SIGNATURE BLOCKS
   5.1 Audit Firm
       - {{engagement_partner}}
       - {{audit_firm_name}}
   5.2 Client Authorization
       - "We authorize {{lawyer_firm}} to release the above information to our auditors."
       - Director Name: _______________
       - Date: _______________
   5.3 Lawyer Reply Section
       - Lawyer Signature: _______________
       - Name: _______________
       - Firm: _______________
       - Date: _______________
```

#### Variables Used

`{{audit_firm_name}}`, `{{audit_firm_address}}`, `{{audit_firm_tel}}`, `{{audit_firm_email}}`, `{{client_name}}`, `{{client_registration_no}}`, `{{financial_year_end}}`, `{{lawyer_name}}`, `{{lawyer_firm}}`, `{{lawyer_address}}`, `{{engagement_partner}}`, `{{engagement_partner_approval_no}}`, `{{engagement_manager}}`

#### Key Malaysian Requirements

- Malaysian court system references (High Court, Sessions Court, Magistrate's Court, Industrial Court)
- Malaysian Bar Council practice on legal confirmations
- Employment disputes under Employment Act 1955 and Industrial Relations Act 1967
- Tax appeals to Special Commissioners of Income Tax

#### Signature Requirements

- Audit firm: engagement partner
- Client authorization: at least one director
- Lawyer reply with firm stamp

---

### T10: Stock/Inventory Confirmation (ISA 505)

**File:** `T10_Stock_Confirmation.md`
**ISA Reference:** ISA 505 — External Confirmations; ISA 501 — Inventory held by third parties
**Malaysian-Specific:** Applicable when inventory is held at third-party warehouses, bonded warehouses (Royal Malaysian Customs), or consignment arrangements

#### Structure

```
1. LETTERHEAD BLOCK (audit firm)
2. ADDRESSEE
   - To: The Manager
   - {{warehouse_name}}
   - {{warehouse_address}}
3. SUBJECT LINE
   - "Re: Confirmation of Inventory Held — {{client_name}} ({{client_registration_no}})"
4. BODY SECTIONS
   4.1 Introduction
       - We are the statutory auditors of {{client_name}}
       - Request confirmation of inventory/goods held on behalf of our client as at {{financial_year_end}}
   4.2 Inventory Details
       - "Please confirm the following inventory held on behalf of {{client_name}} as at {{financial_year_end}}:"
       | Item Description | Quantity | Unit | Condition | Location within warehouse |
       |-----------------|----------|------|-----------|--------------------------|
       | | | | | |
   4.3 Additional Information
       - Any lien, pledge, or encumbrance on the inventory: _______________
       - Any damaged, obsolete, or slow-moving items: _______________
       - Any discrepancies noted during recent stock counts: _______________
       - Insurance coverage status: _______________
       - Warehouse receipt/delivery order numbers: _______________
   4.4 Reply Instructions
       - Reply directly to: {{audit_firm_name}}, {{audit_firm_address}}
       - Attention: {{engagement_manager}}
       - Reference: CONF/INV/{{client_name}}/{{financial_year_end}}
5. SIGNATURE BLOCKS
   5.1 Audit Firm
       - {{engagement_partner}}
       - {{audit_firm_name}}
   5.2 Warehouse Reply Section
       - "We confirm the above inventory is held on behalf of {{client_name}} as at {{financial_year_end}}"
       - [ ] Confirmed as stated above
       - [ ] Confirmed with the following exceptions: _______________
       - Authorized Signatory: _______________
       - Name & Designation: _______________
       - Company Stamp: _______________
       - Date: _______________
```

#### Variables Used

`{{audit_firm_name}}`, `{{audit_firm_address}}`, `{{audit_firm_tel}}`, `{{audit_firm_email}}`, `{{client_name}}`, `{{client_registration_no}}`, `{{financial_year_end}}`, `{{warehouse_name}}`, `{{warehouse_address}}`, `{{engagement_partner}}`, `{{engagement_manager}}`

#### Key Malaysian Requirements

- Bonded warehouse under Royal Malaysian Customs Act 1967
- Free zone / licensed manufacturing warehouse inventory
- Consignment stock arrangements common in Malaysian trading companies
- Only generate when applicable (inventory held by third parties)

#### Signature Requirements

- Audit firm: engagement partner
- Warehouse: authorized signatory with company stamp

---

### T11: Management Representation Letter (ISA 580)

**File:** `T11_Management_Representation.md`
**ISA Reference:** ISA 580 — Written Representations
**Malaysian-Specific:** Companies Act 2016 directors' responsibilities, MPERS/MFRS compliance representations

#### Structure

```
1. LETTERHEAD BLOCK (client letterhead)
   - {{client_name}}
   - ({{client_registration_no}})
   - {{client_address}}
2. ADDRESSEE
   - To: {{engagement_partner}}
   - {{audit_firm_name}}
   - {{audit_firm_address}}
3. DATE
   - Same as or close to {{audit_report_date}}
4. SUBJECT LINE
   - "Re: Management Representation Letter — Audit for FYE {{financial_year_end}}"
5. INTRODUCTION
   - "This representation letter is provided in connection with your audit of the financial statements
     of {{client_name}} for the financial year ended {{financial_year_end}}, for the purpose of
     expressing an opinion whether the financial statements give a true and fair view in accordance
     with {{reporting_framework}} and the Companies Act 2016."
6. REPRESENTATION CATEGORIES

   CATEGORY A — FINANCIAL STATEMENTS RESPONSIBILITY
   - We acknowledge our responsibility for the preparation of FS in accordance with {{reporting_framework}}
   - The FS give a true and fair view of the financial position, financial performance, and cash flows
   - We have approved the financial statements
   - Significant assumptions used in making accounting estimates are reasonable

   CATEGORY B — COMPLETENESS OF INFORMATION
   - We have provided you with access to all records, documentation, and information
   - All transactions have been recorded and reflected in the FS
   - We have disclosed all known actual or possible non-compliance with laws and regulations
   - We have disclosed all related party relationships and transactions (MPERS S33 / MFRS 124)
   - We have disclosed all known deficiencies in internal control

   CATEGORY C — FRAUD
   - We acknowledge our responsibility for internal controls to prevent and detect fraud
   - We have disclosed all information relating to fraud or suspected fraud
   - We have disclosed all information relating to allegations of fraud communicated by employees,
     former employees, analysts, regulators, or others
   - There has been no fraud involving management or employees with significant roles in internal control

   CATEGORY D — LAWS AND REGULATIONS
   - We have disclosed all known instances of non-compliance or suspected non-compliance with
     laws and regulations, including Companies Act 2016, Income Tax Act 1967, EPF Act 1991,
     Employees' Social Security Act 1969, Employment Act 1955, and all other applicable legislation
   - All tax liabilities have been properly recorded

   CATEGORY E — ACCOUNTING ESTIMATES
   - The methods, assumptions, and data used in making accounting estimates are appropriate
   - Key estimates include: depreciation, impairment/ECL, provision for tax, provision for liabilities
   - We have disclosed any changes in methods or assumptions from prior year

   CATEGORY F — RELATED PARTIES
   - We have disclosed all related party relationships and transactions per {{reporting_framework}}
   - All related party transactions were conducted on terms disclosed in the FS
   - We have disclosed the identity of related parties and the nature of relationships
   - Companies Act 2016 s.221: All directors' interests in contracts have been disclosed

   CATEGORY G — SUBSEQUENT EVENTS
   - We have disclosed all events subsequent to {{financial_year_end}} that require adjustment
     or disclosure in the FS
   - All events up to the date of this letter have been considered
   - No events have occurred that would cast doubt on the appropriateness of the going concern basis

   CATEGORY H — GOING CONCERN
   - We have assessed the company's ability to continue as a going concern
   - The going concern basis is appropriate for the preparation of the FS
   - We have disclosed all matters that may cast significant doubt on going concern
   - [If applicable: We confirm the financial support commitment as per the Director Support Letter (T12)]

   CATEGORY I — PRIOR PERIOD
   - We have disclosed all matters affecting the prior period FS of which we have become aware
   - Prior period comparative figures are consistent with audited FS
   - Any restatements have been properly disclosed

   CATEGORY J — OTHER MATTERS
   - Title to all assets is vested in the company, free from encumbrance (except as disclosed)
   - All liabilities, actual and contingent, have been recorded or disclosed
   - The company has complied with all contractual covenants
   - There are no plans or intentions that may materially affect the carrying value of assets or
     classification of assets and liabilities
   - We have no knowledge of any matters that would require additional provision or disclosure

7. SIGNATURE BLOCKS
   - ALL directors must sign:
   - Director 1:
     - Name: {{director_names[0]}}
     - IC No: {{director_ic_numbers[0]}}
     - Designation: Director
     - Signature: _______________
     - Date: _______________
   - Director 2:
     - Name: {{director_names[1]}}
     - IC No: {{director_ic_numbers[1]}}
     - Designation: Director
     - Signature: _______________
     - Date: _______________
   - [Additional director signature blocks as needed]
```

#### Variables Used

`{{client_name}}`, `{{client_registration_no}}`, `{{client_address}}`, `{{audit_firm_name}}`, `{{audit_firm_address}}`, `{{financial_year_end}}`, `{{reporting_framework}}`, `{{engagement_partner}}`, `{{audit_report_date}}`, `{{director_names}}`, `{{director_ic_numbers}}`

#### Key Malaysian Requirements

- Reference to Companies Act 2016 (directors' responsibilities, interests in contracts)
- Reference to Income Tax Act 1967 (tax compliance)
- Reference to EPF Act 1991 and Employees' Social Security Act 1969
- Reference to Employment Act 1955
- MPERS Section 33 or MFRS 124 related party disclosure requirements
- Must be dated on or before the audit report date
- ALL directors must sign (not just two)

#### Signature Requirements

- ALL directors of the company must sign
- IC/passport numbers alongside each signature
- Date must be on or before {{audit_report_date}}

---

### T12: Director Support Letter (ISA 570)

**File:** `T12_Director_Support_Letter.md`
**ISA Reference:** ISA 570 — Going Concern
**Malaysian-Specific:** Common in Malaysian private companies with director-funded operations

#### Structure

```
1. LETTERHEAD BLOCK (client letterhead)
   - {{client_name}}
   - ({{client_registration_no}})
   - {{client_address}}
2. ADDRESSEE
   - To: {{engagement_partner}}
   - {{audit_firm_name}}
   - {{audit_firm_address}}
3. DATE
   - Same as or close to {{audit_report_date}}
4. SUBJECT LINE
   - "Re: Director's Undertaking — Financial Support and Going Concern"
5. BODY SECTIONS
   5.1 Context
       - Reference to the audit of FS for FYE {{financial_year_end}}
       - Acknowledge that the company's current liabilities exceed current assets / net liabilities
         position (if applicable)
   5.2 Financial Support Undertaking
       - "We, the undersigned directors of {{client_name}}, hereby jointly and severally undertake to
         provide continuing financial support to the company to enable it to meet its obligations as
         and when they fall due for at least twelve (12) months from the date of approval of the
         financial statements."
   5.3 Non-Demand Undertaking
       - "We further undertake not to demand repayment of any amounts due to us by the company,
         whether in the form of directors' advances, loans, or amounts due to related parties under
         our control, for a period of at least twelve (12) months from the date of approval of the
         financial statements."
       - Amounts covered:
         - Directors' current account: RM _______________
         - Amounts due to directors: RM _______________
         - Amounts due to related parties: RM _______________
         - Total: RM _______________
   5.4 Acknowledgment
       - "We confirm that we have the financial ability to provide the above undertaking."
       - "This undertaking is irrevocable for the stated period."
6. SIGNATURE BLOCKS
   - ALL directors must sign:
   - Director 1:
     - Name: {{director_names[0]}}
     - IC No: {{director_ic_numbers[0]}}
     - Signature: _______________
     - Date: _______________
   - Director 2:
     - Name: {{director_names[1]}}
     - IC No: {{director_ic_numbers[1]}}
     - Signature: _______________
     - Date: _______________
   - [Additional director signature blocks as needed]
```

#### Variables Used

`{{client_name}}`, `{{client_registration_no}}`, `{{client_address}}`, `{{audit_firm_name}}`, `{{audit_firm_address}}`, `{{financial_year_end}}`, `{{engagement_partner}}`, `{{audit_report_date}}`, `{{director_names}}`, `{{director_ic_numbers}}`

#### Key Malaysian Requirements

- Very common in Malaysian private companies where directors fund the company
- "12 months from date of approval" is the standard going concern assessment period
- Joint and several undertaking provides stronger legal basis
- Irrevocability clause is important for auditor reliance
- Directors must demonstrate financial ability (net worth) to support the undertaking

#### Signature Requirements

- ALL directors must sign (joint and several obligation)
- IC/passport numbers required
- Date must be on or before {{audit_report_date}}

---

### T13: Summary of Audit Adjustments (ISA 450)

**File:** `T13_Summary_Audit_Adjustments.md`
**ISA Reference:** ISA 450 — Evaluation of Misstatements Identified During the Audit
**Malaysian-Specific:** Director acknowledgment required under Malaysian practice

#### Structure

```
1. LETTERHEAD BLOCK (client letterhead)
   - {{client_name}}
   - ({{client_registration_no}})
2. TITLE
   - "Summary of Audit Adjustments — FYE {{financial_year_end}}"
3. BODY SECTIONS
   3.1 Introduction
       - "The following audit adjustments have been identified during the audit and have been
         AGREED and PROCESSED in the financial statements for FYE {{financial_year_end}}."
   3.2 Adjustments Table
       | No. | AWP Ref | Description | Account Affected | DR (RM) | CR (RM) | P&L Impact (RM) | BS Impact (RM) |
       |-----|---------|-------------|-----------------|---------|---------|-----------------|----------------|
       | AJ-001 | | | | | | | |
       | AJ-002 | | | | | | | |
       | AJ-003 | | | | | | | |
       | AJ-004 | | | | | | | |
       | AJ-005 | | | | | | | |
       | **TOTAL** | | | | **___** | **___** | **___** | **___** |
   3.3 Impact Summary
       - Total impact on profit before tax: RM _______________
       - Total impact on profit after tax: RM _______________
       - Total impact on net assets: RM _______________
       - Percentage of planning materiality: ___%
   3.4 Reclassification Adjustments
       | No. | AWP Ref | Description | From Account | To Account | Amount (RM) |
       |-----|---------|-------------|-------------|-----------|-------------|
       | RC-001 | | | | | |
       | RC-002 | | | | | |
4. DIRECTOR ACKNOWLEDGMENT
   - "We, the undersigned directors, acknowledge the above audit adjustments and confirm
     that these have been processed in the financial statements of {{client_name}} for
     FYE {{financial_year_end}}."
   - Director 1:
     - Name: {{director_names[0]}}
     - Signature: _______________
     - Date: _______________
   - Director 2:
     - Name: {{director_names[1]}}
     - Signature: _______________
     - Date: _______________
```

#### Variables Used

`{{client_name}}`, `{{client_registration_no}}`, `{{financial_year_end}}`, `{{director_names}}`, `{{materiality_amount}}`

#### Key Malaysian Requirements

- All adjustments must be processed before FS are finalized
- Director acknowledgment is standard Malaysian audit practice
- Cross-reference to AWP section where the adjustment was identified
- Impact analysis against planning materiality

#### Signature Requirements

- At least two directors must acknowledge
- Date should align with FS approval date

---

### T14: Summary of Uncorrected Audit Differences (ISA 450)

**File:** `T14_Summary_Uncorrected_Differences.md`
**ISA Reference:** ISA 450 — Evaluation of Misstatements Identified During the Audit (paragraph 14)
**Malaysian-Specific:** ISA 450.14 requires directors' written acknowledgment of uncorrected misstatements

#### Structure

```
1. LETTERHEAD BLOCK (client letterhead)
   - {{client_name}}
   - ({{client_registration_no}})
2. TITLE
   - "Summary of Uncorrected Audit Differences — FYE {{financial_year_end}}"
3. BODY SECTIONS
   3.1 Introduction
       - "The following misstatements have been identified during the audit but have NOT been
         corrected in the financial statements for FYE {{financial_year_end}}."
       - "In accordance with ISA 450, we request the directors' written acknowledgment."
   3.2 Uncorrected Misstatements Table
       | No. | AWP Ref | Description | Account Affected | DR (RM) | CR (RM) | P&L Impact (RM) | BS Impact (RM) |
       |-----|---------|-------------|-----------------|---------|---------|-----------------|----------------|
       | UM-001 | | | | | | | |
       | UM-002 | | | | | | | |
       | UM-003 | | | | | | | |
       | **TOTAL** | | | | **___** | **___** | **___** | **___** |
   3.3 Aggregate Effect Assessment
       - Total aggregate effect on profit before tax: RM _______________
       - Total aggregate effect on net assets: RM _______________
       - Planning materiality: RM {{materiality_amount}}
       - Performance materiality: RM {{performance_materiality}}
       - Aggregate uncorrected misstatements as % of materiality: ___%
       - Conclusion: [ ] Below materiality — no impact on audit opinion
                      [ ] Approaches materiality — further consideration required
                      [ ] Exceeds materiality — modification of audit opinion required
   3.4 Prior Period Uncorrected Misstatements (Brought Forward)
       | No. | Description | Amount (RM) | Status (Reversed/Persists) |
       |-----|-------------|-------------|---------------------------|
       | PY-001 | | | |
   3.5 Management's Reasons for Not Adjusting
       - For each uncorrected misstatement, management must state reason:
       | No. | Reason for Not Correcting |
       |-----|--------------------------|
       | UM-001 | |
       | UM-002 | |
       | UM-003 | |
4. DIRECTOR ACKNOWLEDGMENT (ISA 450.14)
   - "We, the undersigned directors, acknowledge the above uncorrected misstatements identified
     during the audit of {{client_name}} for FYE {{financial_year_end}}."
   - "We have considered the aggregate effect of these uncorrected misstatements on the financial
     statements and believe they are IMMATERIAL, individually and in aggregate, to the financial
     statements taken as a whole."
   - "We have provided our reasons for not correcting each misstatement above."
   - Director 1:
     - Name: {{director_names[0]}}
     - IC No: {{director_ic_numbers[0]}}
     - Signature: _______________
     - Date: _______________
   - Director 2:
     - Name: {{director_names[1]}}
     - IC No: {{director_ic_numbers[1]}}
     - Signature: _______________
     - Date: _______________
   - [Additional director signature blocks as needed]
5. AUDITOR'S EVALUATION
   - Auditor's conclusion on the aggregate effect of uncorrected misstatements:
   - Impact on audit opinion: [ ] None [ ] Qualified [ ] Adverse
   - Prepared by: _______________ Date: _______________
   - Reviewed by: _______________ Date: _______________
```

#### Variables Used

`{{client_name}}`, `{{client_registration_no}}`, `{{financial_year_end}}`, `{{director_names}}`, `{{director_ic_numbers}}`, `{{materiality_amount}}`, `{{performance_materiality}}`

#### Key Malaysian Requirements

- ISA 450.14: Auditor must request written acknowledgment from directors for uncorrected misstatements
- Directors must confirm they believe misstatements are immaterial individually and in aggregate
- Directors must provide reasons for not adjusting each misstatement
- Aggregate effect must be compared against planning materiality and performance materiality
- Prior period uncorrected misstatements must be considered for reversal or persistence
- If aggregate exceeds materiality, auditor must consider modification of audit opinion

#### Signature Requirements

- At least two directors must acknowledge (ideally all directors)
- IC/passport numbers required
- Auditor preparer and reviewer must also sign

---

## T15 — Directors' Remuneration Confirmation (Companies Act 2016 s.230 / MPERS S33)

### Purpose

Standalone confirmation signed by **each director individually** confirming all remuneration, fees, benefits, and compensation received from the Company during the financial year. Required for:
- Directors' Report disclosure under Companies Act 2016 s.230
- MPERS Section 33 — Key management personnel compensation disclosure
- ISA 550 — Related party transactions verification
- Financial statements note on directors' remuneration

### Structure (per director)

1. **Section A — Directors' Fees & Remuneration**: Directors' fees, salary, bonus, allowances, commission
2. **Section B — Defined Contribution Plans**: EPF, SOCSO, EIS (employer's portion)
3. **Section C — Benefits-in-Kind**: Motor vehicle, fuel, housing, others
4. **Section D — Other Compensation**: Leave passage, insurance premiums, indemnities, others
5. **Section E — Summary**: Grand total of all components
6. **Section F — Confirmation**: Completeness assertion and signature

### Key Variables

- `{{director_N_fees}}`, `{{director_N_salary}}`, `{{director_N_bonus}}`
- `{{director_N_epf_employer}}`, `{{director_N_socso_employer}}`, `{{director_N_eis_employer}}`
- `{{director_N_total_bik}}`, `{{director_N_grand_total_remuneration}}`

### Signature Requirements

- Each director signs their own section individually
- NRIC number required
- One copy per director — do NOT combine into a single document with joint signature

---

## T16 — Directors' Shareholding Confirmation (Companies Act 2016 s.59 / s.230)

### Purpose

Standalone confirmation signed by **each director individually** confirming all direct and indirect interests in shares of the Company and its related corporations. Required for:
- Companies Act 2016 s.59 — Register of members
- Companies Act 2016 s.230 — Directors' Report — directors' interests in shares
- MPERS Section 33 — Related party disclosures (ownership / control)
- ISA 550 — Identification of related party relationships
- D1 Share Capital working paper verification

### Structure (per director)

1. **Section A — Direct Shareholding**: Opening balance, acquisitions, disposals, closing balance, percentage
2. **Section B — Indirect / Deemed Shareholding**: Shares held through spouse, children, nominees
3. **Section C — Shares in Related Corporations**: Subsidiaries, holding company, fellow subsidiaries
4. **Section D — Changes During the Year**: Date, transaction type, number of shares, consideration
5. **Section E — Share Options / Warrants**: Options, warrants, convertible securities
6. **Section F — Confirmation**: Completeness assertion and signature

### Key Variables

- `{{director_N_shares}}`, `{{director_N_shares_bf}}`, `{{director_N_shares_pct}}`
- `{{director_N_shares_acquired}}`, `{{director_N_shares_disposed}}`
- `{{share_capital}}`, `{{fy_start}}`, `{{year_end_date}}`

### Signature Requirements

- Each director signs their own section individually
- NRIC number required
- One copy per director — do NOT combine into a single document with joint signature

---

## Integration Notes

### Cross-References to Other Working Papers

| Template | Cross-Reference |
|----------|----------------|
| T1 Engagement Letter | A1 (Engagement Letter in AWP Section A) |
| T2 PBC Request Letter | H1 (PBC Checklist) — auto-populate document list |
| T3 Management Letter | B3 (Control Deficiencies Summary) — source of observations |
| T4 Bank Confirmation | C9 (Cash & Bank Balances) — verify balances |
| T5 Bank Authorization | C9 (Cash & Bank Balances) — supports T4 |
| T6 Debtor Confirmation | C6 (Trade Receivables), C8 (Related Party Receivables) |
| T7 Creditor Confirmation | D7 (Trade Payables), D8 (Other Payables) |
| T8 Director Confirmation | F3 (Related Party Transactions), D9 (Due to Directors) |
| T9 Legal Confirmation | F4 (Commitments & Contingencies) |
| T10 Stock Confirmation | C5 (Inventories) |
| T11 Management Rep Letter | F7 (Management Representation Letter in AWP) |
| T12 Director Support Letter | F1 (Going Concern) |
| T13 Audit Adjustments | F6 (Summary of Audit Differences) |
| T14 Uncorrected Differences | F6 (Summary of Audit Differences) |
| T15 Director Remuneration Conf | F3 (Related Parties), E4 (Admin Expenses), G1 (Directors' Report) |
| T16 Director Shareholding Conf | D1 (Share Capital), F3 (Related Parties), G1 (Directors' Report) |

### Workflow Integration

1. **During Planning Phase:** Generate T1 (Engagement Letter) and T2 (PBC Request Letter)
2. **During Fieldwork Phase:** Generate T4-T10, T15, T16 (Confirmation Letters) as needed
3. **During Completion Phase:** Generate T3, T11, T12, T13, T14
4. **After generating AWPs via `/awp`:** Run `/templates all` to ensure all required letters exist
5. **T2 auto-population:** When H1 PBC Checklist exists, T2 document list should be populated from H1 items

### Section T in 00_Index.md

When templates are generated, add the following to `00_Index.md`:

```
SECTION T - TEMPLATES & LETTERS
  T1  - Engagement Letter (ISA 210)
  T2  - PBC Request Letter
  T3  - Management Letter (ISA 265)
  T4  - Bank Confirmation (ISA 505)
  T5  - Bank Authorization Letter (ISA 505)
  T6  - Debtor/AR Confirmation (ISA 505)
  T7  - Creditor/AP Confirmation (ISA 505)
  T8  - Related Party/Director Confirmation (ISA 550)
  T9  - Legal Confirmation (ISA 501)
  T10 - Stock/Inventory Confirmation (ISA 505)
  T11 - Management Representation Letter (ISA 580)
  T12 - Director Support Letter (ISA 570)
  T13 - Summary of Audit Adjustments (ISA 450)
  T14 - Summary of Uncorrected Differences (ISA 450)
```

### Quality Control Checklist

Before finalizing any template, verify:

- [ ] All `{{variables}}` are either substituted or left as placeholders (no broken references)
- [ ] Correct ISA reference cited in the template header
- [ ] Malaysian-specific requirements included (Companies Act 2016, relevant legislation)
- [ ] Appropriate signature blocks with IC/passport number fields
- [ ] Reply-to address points to audit firm (not client) for external confirmations
- [ ] Date fields present and consistent
- [ ] Cross-reference to relevant AWP section included
- [ ] Template follows the standard letterhead block format
- [ ] Currency denomination is RM (Ringgit Malaysia)
- [ ] Reporting framework (MPERS/MFRS) correctly referenced where applicable
