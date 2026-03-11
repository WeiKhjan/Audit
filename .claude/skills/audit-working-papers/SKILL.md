---
name: awp
description: Generate audit working papers with proper indexing, procedures, and lead schedules for Malaysian statutory audits
---

# Audit Working Papers

## Standard Index System

```
SECTION A - PLANNING & ADMINISTRATION
  A1 - Engagement Letter          A2 - Planning Memorandum
  A3 - Understanding the Entity   A4 - Risk Assessment & Materiality
  A5 - Audit Strategy & Programme A6 - Time Budget
  A7 - Permanent File Updates

SECTION B - INTERNAL CONTROL EVALUATION
  B1 - Internal Control Questionnaire
  B2 - Walkthrough Tests          B3 - Control Deficiencies Summary

SECTION C - ASSETS (SUBSTANTIVE)
  C1 - Property, Plant & Equipment  C2 - Investment Properties
  C3 - Intangible Assets            C4 - Investments
  C5 - Inventories                  C6 - Trade Receivables
  C7 - Other Receivables & Prepayments  C8 - Amount Due from Related Parties
  C9 - Cash & Bank Balances         C10 - Tax Recoverable

SECTION D - EQUITY & LIABILITIES (SUBSTANTIVE)
  D1 - Share Capital       D2 - Reserves
  D3 - Retained Earnings   D4 - Non-controlling Interest
  D5 - Borrowings          D6 - Hire Purchase/Lease Liabilities
  D7 - Trade Payables      D8 - Other Payables & Accruals
  D9 - Amount Due to Directors   D10 - Amount Due to Related Parties
  D11 - Tax Payable        D12 - Deferred Tax

SECTION E - INCOME STATEMENT (SUBSTANTIVE)
  E1 - Revenue             E2 - Cost of Sales
  E3 - Other Income        E4 - Administrative Expenses
  E5 - Selling & Distribution  E6 - Other Expenses
  E7 - Finance Costs       E8 - Tax Expense

SECTION F - COMPLETION
  F1 - Going Concern       F2 - Subsequent Events
  F3 - Related Party Transactions  F4 - Commitments & Contingencies
  F5 - Analytical Review   F6 - Summary of Audit Differences
  F7 - Management Representation Letter
  F8 - Completion Checklist  F9 - Audit Report

SECTION G - FINANCIAL STATEMENTS (DRAFT)
  G1 - Directors' Report   G2 - Statement of Financial Position
  G3 - Statement of Comprehensive Income
  G4 - Statement of Changes in Equity
  G5 - Statement of Cash Flows
  G6 - Notes to Financial Statements  G7 - Supplementary Information

SECTION H - ENGAGEMENT TRACKER
  H1 - PBC Checklist & Tracker    H2 - Audit Query Log
  H3 - Engagement Status Dashboard

SECTION T - TEMPLATES & LETTERS
  T1 - Engagement Letter           T2 - PBC Request Letter
  T3 - Management Letter           T4 - Bank Confirmation
  T5 - Bank Authorization          T6 - Debtor Confirmation
  T7 - Creditor Confirmation       T8 - Director/RP Confirmation
  T9 - Legal Confirmation          T10 - Stock Confirmation
  T11 - Management Representation  T12 - Director Support Letter
  T13 - Audit Adjustments Summary  T14 - Uncorrected Differences
  T15 - Director Remuneration Conf T16 - Director Shareholding Conf
```

After generating working papers, run `/templates all` to generate all required letters and document templates.

## Lead Schedule Format

Every working paper must follow this structure:

```
CLIENT: [Company Name]
YEAR END: [Date]
SUBJECT: [Account Area]
PREPARED BY: [Name]  DATE: [Date]
REVIEWED BY: [Name]  DATE: [Date]
WORKING PAPER REF: [Index]

OBJECTIVE:
- To verify [existence/completeness/accuracy/valuation/rights/obligations/presentation]

AUDIT PROCEDURES:
[ ] Procedure 1
[ ] Procedure 2

SCHEDULE:
                              Current Year    Prior Year    Movement
                                    RM            RM            RM
[Line items]                       XXX           XXX           XXX

CONCLUSION:
Based on procedures performed, [balance] is fairly stated / requires adjustment.

ISSUES NOTED:
1. [Issue] - Impact: [Amount] - Recommendation: [Action]

CROSS-REFERENCES:
- Trial Balance: [Ref]  - Financial Statements: [Ref]
```

## Standard Audit Procedures by Area

### PPE (C1)
| Assertion | Procedure |
|-----------|-----------|
| Existence | Physical verification, title documents |
| Completeness | Review repairs for potential capitalization |
| Accuracy | Verify cost to invoices, recalculate depreciation |
| Valuation | Assess impairment indicators, review useful life |
| Rights | Verify ownership documents, check for charges |
| Presentation | Proper classification, disclosure requirements |

### Cash & Bank (C9)
| Assertion | Procedure |
|-----------|-----------|
| Existence | Bank confirmation, count cash on hand |
| Completeness | Review for unrecorded accounts, cutoff testing |
| Accuracy | Bank reconciliation review, agree to statements |
| Valuation | Review for restricted cash, foreign currency translation |
| Rights | Confirm no liens or restrictions |
| Presentation | Proper classification of cash equivalents |

### Trade Receivables (C6)
| Assertion | Procedure |
|-----------|-----------|
| Existence | Debtor confirmations, subsequent receipts |
| Completeness | Cutoff testing, credit note review |
| Accuracy | Aging analysis, recalculate totals |
| Valuation | Impairment assessment, ECL calculation (MFRS 9) |
| Rights | Review factoring arrangements |
| Presentation | Proper aging disclosure |

### Inventories (C5)
| Assertion | Procedure |
|-----------|-----------|
| Existence | Attend stock count, test counts |
| Completeness | Review for consignment stock, goods in transit |
| Accuracy | Price testing, clerical accuracy |
| Valuation | NRV assessment, obsolescence review |
| Rights | Verify ownership, check for pledges |
| Presentation | Proper classification |

### Trade Payables (D7)
| Assertion | Procedure |
|-----------|-----------|
| Existence | Review for overstated liabilities |
| Completeness | Search for unrecorded liabilities, cutoff testing |
| Accuracy | Creditor confirmations, statement reconciliation |
| Valuation | Review for disputed amounts |
| Obligations | Verify goods/services received |
| Presentation | Proper classification |

### Revenue (E1)
| Assertion | Procedure |
|-----------|-----------|
| Occurrence | Vouch to delivery documents, confirmations |
| Completeness | Cutoff testing, analytical review |
| Accuracy | Recalculate, agree to contracts |
| Cutoff | Test transactions around year end |
| Classification | Review for principal vs agent |
| Presentation | Proper disaggregation |

## Master Data Variable System

When generating working papers, **always create `master_data.json`** alongside the .md files and use `{{variable}}` placeholders for all repeated data.

### master_data.json Generation

Create this file in the client folder root with all engagement variables:

```json
{
  "_meta": { "version": "1.0", "lastModified": "ISO_TIMESTAMP" },
  "variables": {
    "company_name": { "value": "CLIENT NAME", "label": "Company Name", "category": "company", "format": "text" },
    "total_assets": { "value": 500000, "label": "Total Assets", "category": "sofp", "format": "currency" }
  },
  "categories": {
    "company": { "label": "Company Identity", "order": 1 },
    "sofp": { "label": "Statement of Financial Position", "order": 2 },
    "soci": { "label": "Statement of Comprehensive Income", "order": 3 },
    "audit": { "label": "Audit Parameters", "order": 4 },
    "directors": { "label": "Directors & Officers", "order": 5 },
    "prior_year": { "label": "Prior Year Comparatives", "order": 6 }
  }
}
```

### Core Variables (always generate)

| Category | Variables |
|----------|-----------|
| Company | company_name, company_reg_no, year_end_date, fye_year, registered_address, business_address, nature_of_business, principal_activities, date_of_incorporation |
| SOFP - Assets | total_ppe, total_investment_properties, total_intangible_assets, total_inventories, total_trade_receivables, total_other_receivables, total_cash_bank, total_tax_recoverable, total_current_assets, total_non_current_assets, total_assets |
| SOFP - Equity & Liabilities | share_capital, retained_earnings, total_equity, total_borrowings, total_hp_liabilities, total_trade_payables, total_other_payables, amount_due_directors, amount_due_related_parties, total_tax_payable, total_deferred_tax, total_current_liabilities, total_non_current_liabilities, total_equity_liabilities |
| SOCI | revenue, cost_of_sales, gross_profit, other_income, admin_expenses, selling_distribution, other_expenses, finance_costs, profit_before_tax, tax_expense, profit_after_tax |
| Audit | planning_materiality, performance_materiality, trivial_threshold, audit_period_from, audit_period_to, engagement_partner, audit_manager, prepared_by, reviewed_by |
| Directors | director_N_name, director_N_nric, director_N_designation (for each director) |
| Prior Year | py_total_assets, py_total_equity, py_revenue, py_profit_before_tax, py_retained_earnings |

### Dynamic Variables (add per engagement)

Add engagement-specific variables as needed:
- **PPE detail**: ppe_land_buildings, ppe_motor_vehicles, ppe_office_equipment, ppe_furniture_fittings, accumulated_depreciation
- **Receivables detail**: trade_receivables_current, trade_receivables_31_60, trade_receivables_61_90, trade_receivables_over_90, allowance_doubtful_debts
- **Bank detail**: bank_N_name, bank_N_account_no, bank_N_balance (for each bank account)

### Variable Syntax in .md Files

Use `{{variable_name}}` in markdown. The viewer substitutes values at render time.

```markdown
| Company | {{company_name}} |
| Total Assets | {{total_assets}} |
| Adjusted Loss | {{adjusted_loss|bracket}} |
```

Format modifiers: `|rm` (RM prefix), `|bracket` (negative in brackets), `|rm_bracket` (both), `|nil` (zero as NIL), `|raw` (no formatting)

### Calculated Variables (Formula)

For derived/calculated figures, add a `formula` field to show the calculation chain:

```json
"gross_profit": {
  "value": 2908556,
  "label": "Gross Profit",
  "category": "soci",
  "format": "currency",
  "formula": "revenue - cost_of_sales"
},
"total_assets": {
  "value": 500000,
  "label": "Total Assets",
  "category": "sofp",
  "format": "currency",
  "formula": "total_current_assets + total_non_current_assets"
}
```

The viewer renders calculated variables with a **teal underline** (vs purple for input variables), and the popover shows the formula with resolved values.

### Format Types

- `text` — render as-is
- `currency` — `43,600.00`
- `currency_bracket` — negative as `(10,063.75)`
- `currency_nil` — zero as `NIL`

---

## MANDATORY: Variable Usage Rules

**EVERY monetary figure in .md files MUST use `{{variable}}` placeholders — no exceptions.**

When generating or editing working papers, NEVER hardcode financial figures. All numbers must come from `master_data.json` via the variable substitution system.

### CORRECT vs INCORRECT Examples

```markdown
<!-- INCORRECT — hardcoded figures -->
| Total Assets | 500,000 |
| Revenue | 1,200,000 |
| Trade Receivables | 85,000 |

<!-- CORRECT — using variables -->
| Total Assets | {{total_assets}} |
| Revenue | {{revenue}} |
| Trade Receivables | {{total_trade_receivables}} |

<!-- CORRECT — with format modifiers -->
| Share Capital | {{share_capital|rm}} |              <!-- renders as RM 500,000 -->
| Tax Recoverable | {{total_tax_recoverable|nil}} |    <!-- renders as NIL when 0 -->
| Net Loss | {{profit_after_tax|bracket}} |             <!-- renders as (xxx) for negatives -->
```

### Quality Checklist

Before delivering any working paper set, verify:
- [ ] **No hardcoded financial figures in .md files** — search for `\d{1,3}(,\d{3})+` patterns
- [ ] Every figure traces back to a `{{variable}}` in `master_data.json`
- [ ] Format modifiers used appropriately (`|rm`, `|bracket`, `|nil`)
- [ ] All cross-references between working papers are consistent
- [ ] Working paper headers complete (client, year end, subject, preparer, date)
- [ ] Clear conclusion on each audit area

---

## Output Folder Structure

```
Clients/AWP_[Client]_FYE[Year]/
├── A_Planning/
│   ├── A1_Engagement_Letter.md
│   ├── A2_Planning_Memorandum.md
│   ├── A3_Understanding_Entity.md
│   ├── A4_Risk_Assessment_Materiality.md
│   ├── A5_Audit_Strategy_Programme.md
│   ├── A6_Time_Budget.md
│   └── A7_Permanent_File.md
├── B_Internal_Control/
│   ├── B1_ICQ.md
│   ├── B2_Walkthrough_Tests.md
│   └── B3_Control_Deficiencies.md
├── C_Assets/
│   ├── C1_PPE.md
│   ├── C2_Investment_Properties.md
│   ├── C5_Inventories.md
│   ├── C6_Trade_Receivables.md
│   ├── C7_Other_Receivables.md
│   └── C9_Cash_Bank.md
├── D_Liabilities_Equity/
│   ├── D1_Share_Capital.md
│   ├── D3_Retained_Earnings.md
│   ├── D5_Borrowings.md
│   ├── D7_Trade_Payables.md
│   └── D8_Other_Payables.md
├── E_Income_Statement/
│   ├── E1_Revenue.md
│   ├── E2_Cost_of_Sales.md
│   ├── E4_Admin_Expenses.md
│   ├── E7_Finance_Costs.md
│   └── E8_Tax_Expense.md
├── F_Completion/
│   ├── F1_Going_Concern.md
│   ├── F2_Subsequent_Events.md
│   ├── F3_Related_Party.md
│   ├── F5_Analytical_Review.md
│   ├── F6_Audit_Differences.md
│   ├── F7_Management_Representation.md
│   ├── F8_Completion_Checklist.md
│   └── F9_Audit_Report.md
├── G_Outstanding/
│   ├── G1_Directors_Report.md
│   ├── G2_SOFP.md
│   ├── G3_SOCI.md
│   ├── G4_SOCE.md
│   ├── G5_SCF.md
│   ├── G6_Notes.md
│   └── G7_Supplementary_Info.md
├── H_Engagement_Tracker/
│   ├── H1_PBC_Checklist.md
│   ├── H2_Query_Log.md
│   └── H3_Engagement_Dashboard.md
├── T_Templates/
│   ├── T1_Engagement_Letter.md
│   ├── T2_PBC_Request_Letter.md
│   ├── T3_Management_Letter.md
│   ├── T4_Bank_Confirmation.md
│   ├── T5_Bank_Authorization.md
│   ├── T6_Debtor_Confirmation.md
│   ├── T7_Creditor_Confirmation.md
│   ├── T8_Director_Confirmation.md
│   ├── T9_Legal_Confirmation.md
│   ├── T10_Stock_Confirmation.md
│   ├── T11_Management_Representation.md
│   ├── T12_Director_Support_Letter.md
│   ├── T13_Summary_Audit_Adjustments.md
│   ├── T14_Summary_Uncorrected_Differences.md
│   ├── T15_Director_Remuneration_Confirmation.md
│   └── T16_Director_Shareholding_Confirmation.md
├── 00_Index.md
├── master_data.json
├── server.py
└── START_VIEWER.bat
```

## Working Paper .md Template

```markdown
---
ref: [C1]
title: [Property, Plant & Equipment]
section: [C_Assets]
---

# {{company_name}}
## Year End: {{year_end_date}}
## Working Paper: [C1] - Property, Plant & Equipment

| | |
|---|---|
| **Prepared by** | {{prepared_by}} |
| **Date** | [Date] |
| **Reviewed by** | {{reviewed_by}} |
| **Date** | [Date] |

---

### Objective
- To verify existence, completeness, accuracy, valuation, rights, and presentation of PPE

---

### Lead Schedule

| Description | Current Year (RM) | Prior Year (RM) | Movement (RM) |
|---|---|---|---|
| Land & Buildings | {{ppe_land_buildings}} | {{py_ppe_land_buildings}} | {{mv_ppe_land_buildings}} |
| Motor Vehicles | {{ppe_motor_vehicles}} | {{py_ppe_motor_vehicles}} | {{mv_ppe_motor_vehicles}} |
| **Total PPE** | **{{total_ppe}}** | **{{py_total_ppe}}** | **{{mv_total_ppe}}** |

---

### Audit Procedures
- [ ] Procedure 1
- [ ] Procedure 2

---

### Conclusion
Based on procedures performed, [balance] is fairly stated / requires adjustment.

### Issues Noted
1. [Issue] - Impact: [Amount] - Recommendation: [Action]

### Cross-References
- Trial Balance: [Ref]
- Financial Statements: G2, G6 Note [X]
- Sampling Paper: [Ref]-S (if applicable)
```

## ISA Compliance Requirements for All Working Papers

### Assertion-Level Conclusion Table (ISA 315.25)

Every substantive working paper (C/D/E sections) MUST include an assertion-level conclusion table after the audit procedures section:

| Assertion | Tested? | Procedure Ref | Evidence Obtained | Conclusion |
|-----------|---------|---------------|-------------------|------------|
| Existence/Occurrence | [x] | Proc 1, 3 | [Bank confirmation, physical count, etc.] | Satisfied / Exception noted |
| Completeness | [x] | Proc 2, 4 | [Cutoff testing, search for unrecorded items] | Satisfied / Exception noted |
| Accuracy/Valuation | [x] | Proc 5 | [Recalculation, independent estimate] | Satisfied / Exception noted |
| Rights & Obligations | [x] | Proc 6 | [Title documents, agreements] | Satisfied / Exception noted |
| Classification/Presentation | [x] | Proc 7 | [Review against MPERS/MFRS requirements] | Satisfied / Exception noted |

### Evidence Evaluation (ISA 500)

Every working paper MUST document the evidence obtained and its quality:

| Evidence Type | Source | Reliability | Sufficiency | Reference |
|--------------|--------|-------------|-------------|-----------|
| [e.g., External confirmation] | [e.g., Bank] | High (external, direct) | [Adequate/Insufficient] | [Doc ref] |
| [e.g., Management representation] | [e.g., Director] | Low (internal, oral) | [Corroborated by...] | [Doc ref] |

### Risk Linkage (ISA 330)

Every working paper MUST include a risk linkage row connecting to the risk assessment:

**Risks Addressed:** [Reference to A4 risk assessment — e.g., "A4 Ref: C6 HIGH risk — Existence, Valuation"]
**Planned Response per A4:** [Nature, timing, extent as documented in risk assessment]
**Actual Response:** [What was actually performed and any deviations from plan]

## Sampling Cross-Reference (ISA 530)

When an audit area requires sample testing, generate a companion sampling paper using `/sampling [area]`. The companion paper is named `[Ref]-S` (e.g., `C6-S` for Trade Receivables sampling).

### Integration with Working Papers

For areas requiring sampling, include this procedure in the main working paper:

```markdown
- [ ] Perform audit sampling per ISA 530 — see **[REF]-S** for sample selection and evaluation
```

### Areas Commonly Requiring Sampling

| Area | Ref | Companion | Key Assertion |
|------|-----|-----------|---------------|
| Trade Receivables | C6 | C6-S | Existence, Valuation |
| Inventories | C5 | C5-S | Existence, Valuation |
| Trade Payables | D7 | D7-S | Completeness |
| Revenue | E1 | E1-S | Occurrence, Accuracy |
| PPE | C1 | C1-S | Existence, Accuracy |
| Admin Expenses | E4 | E4-S | Occurrence, Classification |

## A1 — Engagement Letter Template (ISA 210)

When generating A1, include the following structure:

### Engagement Letter Content
1. **Addressee** — Directors of the entity
2. **Scope of engagement** — Statutory audit under Companies Act 2016
3. **Management responsibilities** — Preparation of FS per MPERS/MFRS, internal controls, access to records
4. **Auditor responsibilities** — Conduct audit per ISA, express opinion, inherent limitations
5. **Reporting framework** — MPERS or MFRS as applicable
6. **Fee and billing** — Audit fee, additional work, payment terms
7. **Confidentiality** — Data protection, professional obligations
8. **Engagement terms** — Duration, renewal, termination provisions
9. **Signature block** — Both auditor and client acceptance

### Acceptance Checklist
| Item | Completed? | Reference |
|------|-----------|-----------|
| Independence confirmed | [ ] | |
| Client acceptance/continuance procedures performed | [ ] | |
| Predecessor auditor communication (if applicable) | [ ] | |
| Competence and resources assessed | [ ] | |
| Ethical requirements considered | [ ] | |
| Engagement letter signed by both parties | [ ] | |
| Anti-money laundering checks (if applicable) | [ ] | |

## B1 — Internal Control Questionnaire Template (ISA 315.26-27)

When generating B1, cover ALL 5 COSO components:

### 1. Control Environment
| Question | Yes/No/N/A | Comment |
|----------|-----------|---------|
| Is there a governance structure (board/audit committee)? | | |
| Do directors demonstrate commitment to integrity and ethical values? | | |
| Is there an organizational structure with clear lines of authority? | | |
| Are there human resource policies (competence, training)? | | |
| Is there assignment of authority and responsibility? | | |

### 2. Entity's Risk Assessment Process
| Question | Yes/No/N/A | Comment |
|----------|-----------|---------|
| Does management identify business risks? | | |
| Does management assess the likelihood and significance of risks? | | |
| Does management take action to address identified risks? | | |
| Are changes in the business environment monitored? | | |

### 3. Information System and Communication
| Question | Yes/No/N/A | Comment |
|----------|-----------|---------|
| What accounting system/software is used? | | |
| Are transactions recorded timely and accurately? | | |
| Is there a chart of accounts? | | |
| Are financial reports generated regularly? | | |
| Is there adequate IT access control? | | |

### 4. Control Activities
| Question | Yes/No/N/A | Comment |
|----------|-----------|---------|
| Is there segregation of duties (authorisation, recording, custody)? | | |
| Are bank reconciliations prepared and reviewed? | | |
| Are physical controls over assets adequate? | | |
| Is there an approval process for expenditure? | | |
| Are journal entries reviewed and approved? | | |

### 5. Monitoring of Controls
| Question | Yes/No/N/A | Comment |
|----------|-----------|---------|
| Does management review financial results regularly? | | |
| Are control deficiencies identified and corrected? | | |
| Is there internal audit function? | | |
| Are external findings (audit, regulatory) addressed? | | |

### IT General Controls (ITGC)
| Area | Question | Response |
|------|----------|----------|
| Access controls | Are user access rights appropriate? | |
| Change management | Are system changes authorized and tested? | |
| Operations | Are backups performed regularly? | |
| Data integrity | Are there controls over data input/processing? | |

## F2 — Subsequent Events Template (ISA 560)

When generating F2, include this structured procedure checklist:

### Type 1: Adjusting Events (conditions existed at year end)
| Procedure | Done? | Finding | Reference |
|-----------|-------|---------|-----------|
| Review post-YE bank statements for unusual items | [ ] | | |
| Review post-YE receipts from debtors (collectability) | [ ] | | |
| Review post-YE payments to creditors (completeness) | [ ] | | |
| Review post-YE inventory movements/write-downs | [ ] | | |
| Review legal matters resolved post-YE | [ ] | | |
| Review insurance claims settled post-YE | [ ] | | |

### Type 2: Non-Adjusting Events (conditions arose after year end)
| Procedure | Done? | Finding | Reference |
|-----------|-------|---------|-----------|
| Review board/shareholder meeting minutes post-YE | [ ] | | |
| Inquire of management regarding subsequent events | [ ] | | |
| Review for major transactions (acquisitions, disposals) | [ ] | | |
| Review for significant changes in capital structure | [ ] | | |
| Review for natural disasters/major events | [ ] | | |
| Assess COVID-19/pandemic developments | [ ] | | |

### Extended Period Considerations
- If significant time has elapsed between year end and audit date, document:
  - Reason for delay
  - Additional procedures performed to cover extended period
  - Impact on audit evidence reliability
  - Whether subsequent period financial information is available

### Management Inquiry Documentation
| Question Asked | Management Response | Corroborated? | Reference |
|---------------|--------------------|--------------| ----------|
| Any significant events after year end? | | | |
| Any new commitments or contingencies? | | | |
| Any going concern developments? | | | |
| Any legal proceedings commenced/settled? | | | |

## F7 — Management Representation Letter Template (ISA 580)

When generating F7, include ALL of the following representations:

### Standard Representations
1. **Financial Statements** — Directors acknowledge responsibility for preparation of FS in accordance with MPERS/MFRS
2. **Completeness of information** — All transactions recorded; all records and documents made available
3. **Fraud** — Disclosure of knowledge of fraud or suspected fraud involving management, employees, or others
4. **Laws and regulations** — Disclosure of all known instances of non-compliance
5. **Related parties** — Completeness of related party identification and disclosure
6. **Subsequent events** — All events after year end requiring adjustment or disclosure have been addressed
7. **Going concern** — Directors' assessment of going concern basis and plans if applicable
8. **Accounting estimates** — Reasonableness of assumptions and methods used
9. **Litigation and claims** — Disclosure of all known litigation, claims, and assessments
10. **Ownership and rights** — The entity has satisfactory title to all assets
11. **Provisions** — All known liabilities have been recorded or disclosed
12. **Tax** — Tax returns filed; tax liabilities adequately provided

### Malaysia-Specific Representations
13. **Companies Act 2016** — Compliance with applicable provisions
14. **EPF/SOCSO/EIS** — Statutory contributions are up to date
15. **SST** — Compliance with SST requirements (if applicable)
16. **Transfer pricing** — Related party transactions are on arm's length terms
17. **Moneylending/specific licence** — Licence is current and conditions complied with

### Template Format
- Date: Same date as or after the audit report date
- Addressed to: The auditor
- Signed by: Those with overall responsibility for the FS (typically directors)
- Period: Covering the financial year under audit

## F8 — Completion Checklist Template (Best Practice)

When generating F8, include this pre-issuance checklist:

### Pre-Issuance Checklist

#### A. Working Papers
| Item | Done? | Ref | Comment |
|------|-------|-----|---------|
| All working papers prepared | [ ] | | |
| All working papers reviewed by reviewer | [ ] | | |
| Review notes cleared | [ ] | | |
| All cross-references verified | [ ] | | |

#### B. Evidence & Confirmations
| Item | Done? | Ref | Comment |
|------|-------|-----|---------|
| Bank confirmations received | [ ] | C9 | |
| Debtor confirmations received/alternatives performed | [ ] | C6 | |
| Creditor confirmations received (if sent) | [ ] | D7 | |
| Legal confirmation received (if applicable) | [ ] | F4 | |
| Related party confirmations | [ ] | F3 | |

#### C. PBC & Outstanding Items
| Item | Done? | Ref | Comment |
|------|-------|-----|---------|
| All PBC items received | [ ] | PBC | |
| Outstanding queries resolved | [ ] | Query Log | |
| Scope limitations documented (if any) | [ ] | | |

#### D. Completion Procedures
| Item | Done? | Ref | Comment |
|------|-------|-----|---------|
| Going concern assessment finalized | [ ] | F1 | |
| Subsequent events review completed | [ ] | F2 | |
| Related party assessment completed | [ ] | F3 | |
| Analytical review performed | [ ] | F5 | |
| Audit differences evaluated | [ ] | F6 | |
| All differences below materiality OR adjusted | [ ] | F6 | |

#### E. Reporting
| Item | Done? | Ref | Comment |
|------|-------|-----|---------|
| Management representation letter signed | [ ] | F7 | |
| Draft FS reviewed and approved by directors | [ ] | G1-G7 | |
| Audit opinion determined | [ ] | F9 | |
| Audit report drafted | [ ] | F9 | |
| Engagement partner final review | [ ] | | |

## F9 — Audit Report Template (ISA 700/705/706)

When generating F9, provide templates for each opinion type:

### Unmodified Opinion (ISA 700)
- Title: Independent Auditors' Report
- Addressee: Members of [Company]
- Opinion paragraph: "In our opinion, the financial statements give a true and fair view..."
- Basis for Opinion: Conducted audit per ISA; independence per By-Laws; sufficient appropriate evidence
- Key Audit Matters (if applicable — public interest entities)
- Responsibilities of Directors
- Auditors' Responsibilities
- Report on other legal and regulatory requirements (Companies Act 2016, S266(1))
- Signature, date, address

### Modified Opinions (ISA 705)

#### Qualified Opinion
- Use when: misstatements are material but not pervasive, OR unable to obtain sufficient evidence but effects are not pervasive
- Opinion: "Except for the effects of [matter], the financial statements give a true and fair view..."
- Basis for Qualified Opinion: describe the matter

#### Adverse Opinion
- Use when: misstatements are material AND pervasive
- Opinion: "The financial statements do not give a true and fair view..."
- Basis for Adverse Opinion: describe the matter

#### Disclaimer of Opinion
- Use when: unable to obtain sufficient evidence AND possible effects are material and pervasive
- Opinion: "We do not express an opinion..."
- Basis for Disclaimer: describe the matter

### Emphasis of Matter (ISA 706)
- Going concern: "We draw attention to Note [X] in the financial statements, which indicates..."
- Does not modify the opinion
- Placed after the Basis for Opinion paragraph

### Material Uncertainty Related to Going Concern (ISA 570)
- Separate section: "Material Uncertainty Related to Going Concern"
- Reference to the financial statement note
- State the conditions/events giving rise to the uncertainty
- State that the FS are prepared on going concern basis
- State that events may cast significant doubt

### Audit Report Impact Decision Matrix
| Condition | Going Concern Basis Appropriate? | Adequate Disclosure? | Audit Report |
|-----------|--------------------------------|---------------------|-------------|
| No material uncertainty | Yes | N/A | Unmodified |
| Material uncertainty exists | Yes | Yes | Unmodified + Material Uncertainty section |
| Material uncertainty exists | Yes | No | Qualified or Adverse |
| Going concern basis inappropriate | No | N/A | Adverse |
| Multiple uncertainties, cannot form opinion | N/A | N/A | Disclaimer |

## External Confirmation Procedures (ISA 505)

### Mandatory Confirmations

| Confirmation Type | WP Ref | When Required | Alternative Procedures |
|------------------|--------|---------------|----------------------|
| **Bank confirmations** | C9 | ALWAYS — for all bank accounts | No alternative; must confirm |
| **Debtor/borrower confirmations** | C6 | Material receivable balances | Subsequent receipts testing + vouching to supporting docs |
| **Creditor confirmations** | D7 | Material payable balances (completeness) | Subsequent payment testing + statement reconciliation |
| **Related party confirmations** | D9/D10 | Material related party balances | Director/party written confirmation |
| **Legal confirmations** | F4 | When litigation/claims exist or suspected | Management representation + legal review |

### Confirmation Process Template
1. **Design** — Prepare confirmation letter specifying balance/information to confirm
2. **Control** — Auditor maintains control over sending and receiving (ISA 505.7)
3. **Send** — Direct from auditor to confirming party
4. **Follow-up** — Second request if no response within 2-3 weeks
5. **Evaluate responses** — Agree to books; investigate discrepancies
6. **Non-responses** — Perform alternative procedures; document in WP
7. **Management refusal** — Evaluate reasonableness; consider implications for audit (ISA 505.8)

### Evaluation of Confirmation Results
| Response | Action |
|----------|--------|
| Agrees to books | Document; satisfactory evidence obtained |
| Disagrees | Investigate discrepancy; determine who is correct |
| No response (1st request) | Send 2nd request |
| No response (2nd request) | Perform alternative procedures |
| Management refuses to allow | Evaluate reasons; consider scope limitation |

## Accounting Estimates Verification (ISA 540)

### Common Estimates in Malaysian Audits

| Estimate | WP Ref | Key Considerations |
|----------|--------|-------------------|
| Impairment/ECL (receivables) | C6 | Incurred loss model (MPERS) or ECL model (MFRS 9) |
| Inventory NRV | C5 | Selling price less costs to complete and sell |
| Depreciation | C1 | Useful life, residual value, method |
| Tax computation | E8/D11 | Add-backs, capital allowances, tax rate |
| Deferred tax | D12 | Temporary differences, applicable rate, DTA recognition |
| Provisions/accruals | D8 | Best estimate of expenditure required |
| Impairment of PPE | C1 | Indicators, recoverable amount |

### Verification Procedure Template
For each accounting estimate:

1. **Understand management's method**
   - What model/approach was used?
   - What are the key assumptions?
   - What data inputs were used?

2. **Evaluate reasonableness of assumptions**
   - Are assumptions consistent with the entity's plans?
   - Are assumptions supported by market/industry data?
   - Is there management bias?

3. **Test the calculation**
   - Independent recalculation
   - Sensitivity analysis for significant estimates
   - Compare with independent estimate if available

4. **Review subsequent events**
   - Do post-YE events confirm or contradict the estimate?

5. **Conclude**
   - Is the estimate within an acceptable range?
   - Is there a point estimate that differs from management's?
   - Document any audit difference

## Related Party Procedures (ISA 550 / MPERS Section 33)

### Party Identification Procedures
- Review SSM company profile for directors, shareholders, related companies
- Obtain director declarations of related party relationships
- Review prior year working papers and FS for known related parties
- Inquire of management about related party relationships
- Review entity's register of directors' interests
- Search for common addresses, phone numbers, or bank accounts

### Transaction Identification Procedures
- Review GL for transactions with known related parties
- Review journal entries for unusual counterparties
- Review loan agreements and guarantees
- Review significant transactions outside normal business
- Evaluate business rationale for unusual transactions

### Arm's Length Assessment
For each material RPT:
| Factor | Assessment |
|--------|-----------|
| Comparable market terms | [Available/Not available] |
| Business rationale | [Documented/Not documented] |
| Independent valuation (if applicable) | [Obtained/Not obtained] |
| Board approval | [Obtained/Not obtained] |
| Conclusion on arm's length | [Arm's length / Not arm's length — disclose] |

### MPERS Section 33 Disclosure Checklist
| Requirement | Disclosed? | Reference |
|------------|-----------|-----------|
| Nature of related party relationship | [ ] | |
| Types of transactions | [ ] | |
| Amount of transactions | [ ] | |
| Outstanding balances at year end | [ ] | |
| Terms and conditions (secured/unsecured, interest, repayment) | [ ] | |
| Guarantees given or received | [ ] | |
| Provisions for doubtful debts on outstanding balances | [ ] | |
| Expense recognized for bad/doubtful debts | [ ] | |
| Key management personnel compensation | [ ] | |

## Going Concern Assessment Framework (ISA 570)

### Financial Indicators Checklist
| # | Indicator | Threshold/Trigger | Present? | Detail |
|---|-----------|------------------|----------|--------|
| 1 | Net current liability position | CL > CA | | |
| 2 | Capital deficiency / negative equity | Total equity < 0 | | |
| 3 | Accumulated losses exceed share capital | Losses > PUC | | |
| 4 | Consecutive losses | 2+ years of net losses | | |
| 5 | Cash flow difficulties | Operating cash flow negative | | |
| 6 | Inability to pay debts as they fall due | Overdue payables | | |
| 7 | Non-compliance with loan covenants | Covenant breach | | |
| 8 | Significant decline in revenue | >20% YoY decline | | |
| 9 | Loss of major customer/contract | >30% of revenue | | |
| 10 | Adverse key financial ratios | Current ratio < 1, etc. | | |

### Operating Indicators Checklist
| # | Indicator | Present? | Detail |
|---|-----------|----------|--------|
| 1 | Loss of key management without replacement | | |
| 2 | Loss of major market, customer, franchise, licence | | |
| 3 | Labour difficulties / staff shortages | | |
| 4 | Shortage of important supplies | | |
| 5 | Emergence of highly successful competitor | | |
| 6 | Non-compliance with capital or statutory requirements | | |
| 7 | Pending legal proceedings that may result in claims | | |
| 8 | Changes in law/regulation/government policy | | |

### Management's Assessment Evaluation
| Procedure | Done? | Finding |
|-----------|-------|---------|
| Obtain management's own going concern assessment | [ ] | |
| Review management's cash flow forecasts (min 12 months) | [ ] | |
| Challenge key assumptions in forecasts | [ ] | |
| Consider sensitivity of assumptions | [ ] | |
| Assess management's plans to address indicators | [ ] | |
| Evaluate feasibility of management's plans | [ ] | |
| Obtain director support letter (if required) | [ ] | |

### Director Support Letter Requirements
When the entity depends on director/shareholder financial support:
- Written undertaking to continue financial support
- Commitment not to demand repayment of amounts owed
- Specific period covered (at least 12 months from FS date)
- Evidence of director's ability to provide support (personal financial capacity)

### Audit Report Impact Decision Matrix
| Scenario | GC Basis Appropriate? | Adequate Disclosure? | Report Impact |
|----------|----------------------|---------------------|---------------|
| No indicators present | Yes | N/A | Unmodified opinion |
| Indicators present but mitigated | Yes | N/A | Unmodified; consider EOM |
| Material uncertainty exists, disclosed | Yes | Yes | Unmodified + "Material Uncertainty" section |
| Material uncertainty exists, NOT disclosed | Yes | No | Qualified or Adverse opinion |
| GC basis inappropriate | No | N/A | Adverse opinion |
| Unable to conclude (multiple pervasive uncertainties) | Unknown | N/A | Disclaimer of opinion |

### 12-Month Forward-Looking Assessment Template
| Item | Monthly (RM) | 12-Month Total (RM) |
|------|-------------|-------------------|
| **Cash Inflows** | | |
| Revenue/operating receipts | | |
| Debtor collections | | |
| Other inflows | | |
| **Cash Outflows** | | |
| Salaries and wages | | |
| Rental | | |
| Utilities and overheads | | |
| Statutory payments (EPF/SOCSO/tax) | | |
| Loan repayments | | |
| Other outflows | | |
| **Net Monthly Cash Flow** | | |
| **Opening Cash** | | |
| **Projected Closing Cash** | | |
