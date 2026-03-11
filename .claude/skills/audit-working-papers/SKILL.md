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
  B2 - Journal Entry Testing (ISA 240)
  B3 - Walkthrough Tests          B4 - Control Deficiencies Summary

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

EMBEDDED DOCUMENTS (T1-T16)
  Templates are embedded as .docx attachments within their parent working papers.
  Use `/templates` to generate .docx files and add ATTACHMENT comments to WPs.
  Status tracking: unsigned → sent → signed (via viewer attachment cards).
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

## Substantive Analytical Procedures Framework (ISA 520)

### Decision Framework: SAP vs Test of Details (TOD)

When generating working papers, **classify each line item** by the appropriate substantive test method BEFORE designing audit procedures.

**Use SAP (Substantive Analytical Procedure) when:**
- The auditor can independently compute an **expected amount** from known, reliable inputs
- The relationship between data is **predictable and stable** (e.g., fixed monthly amounts, statutory rates)
- The data used to develop the expectation is **reliable** (external source, independently verified, or mathematically derived)
- The resulting precision is **sufficient to detect material misstatement** at the assertion level

**Use TOD (Test of Details / Vouching) when:**
- The amount is **discretionary** (e.g., bonus, entertainment, donations)
- The amount is a **one-off transaction** (e.g., professional fee, penalty, disposal gain/loss)
- The amount **cannot be independently predicted** from available inputs
- The item is a **significant risk** requiring direct evidence (ISA 330.21)

**Use COMBINED (SAP + TOD) when:**
- The account involves **both predictable and unpredictable components** (e.g., revenue = calculated interest on known loan balances, but loan terms need verification)
- **ISA 240 fraud risk** is presumed (revenue recognition) — SAP alone is insufficient; corroborate with TOD
- The overall balance can be estimated via SAP but **individual transactions** require direct testing

### SAP Acceptance Threshold

For each SAP test, the acceptable difference is:

> **Threshold = MAX(Performance Materiality, 5% of line item amount)**

| Example | Line Item Amount | PM | 5% of Amount | Threshold |
|---------|-----------------|-----|-------------|-----------|
| Salaries RM 25,200 | 25,200 | 550 | 1,260 | **1,260** |
| Rental RM 7,600 | 7,600 | 550 | 380 | **550** |
| EPF RM 3,276 | 3,276 | 550 | 164 | **550** |
| Revenue RM 41,303 | 41,303 | 550 | 2,065 | **2,065** |

**If the difference between expected and GL amount exceeds the threshold → investigate and document the cause.**

### SAP Table Format

Every SAP test MUST use this standardized table format:

| # | Expense/Income Item | Auditor's Independent Expectation | Basis of Expectation | GL Amount (RM) | Difference (RM) | Threshold (RM) | Within Threshold? | Conclusion |
|---|--------------------|---------------------------------|---------------------|---------------|-----------------|----------------|-------------------|------------|
| 1 | [Item] | [Calculated amount] | [e.g., RM X/month × 12] | {{variable}} | [Diff] | [max(PM, 5%)] | Yes/No | Satisfactory / Investigate |

### SAP Classification for Common Expense Items (Malaysian SME)

| Line Item | Test Method | Basis of Expectation |
|-----------|-----------|---------------------|
| **Salaries** | SAP | Monthly payroll × 12 months |
| **Office Rental** | SAP | Monthly rent per lease × months occupied |
| **EPF — Employer** | SAP | Statutory rate (12%/13%) × qualifying remuneration |
| **SOCSO — Employer** | SAP | Statutory rate per contribution table × 12 months |
| **EIS — Employer** | SAP | 0.2% × qualifying remuneration |
| **Depreciation** | SAP | Independent recalculation from FAR (cross-ref C1) |
| **Allowance (fixed monthly)** | SAP | Monthly amount × 12 months |
| **Utilities (water, electricity)** | SAP | Monthly average × 12 (verify consistency) |
| **Telephone/Internet** | SAP | Monthly plan rate × 12 months |
| **Bank Charges** | SAP | Verify to bank statements; monthly pattern check |
| **Interest expense (loans)** | SAP | Loan balance × rate × period |
| **Audit Fee** | TOD | Vouch to engagement letter |
| **Bonus** | TOD | Vouch to board resolution / payslip |
| **Professional Fee** | TOD | Vouch to invoice |
| **Tax Agent Fee** | TOD | Vouch to invoice |
| **Penalty** | TOD | Vouch to notice; investigate nature |
| **Entertainment** | TOD | Vouch to receipts |
| **Donations** | TOD | Vouch to receipts; verify approved institution |
| **Commission** | SAP or TOD | SAP if % of revenue; TOD if ad hoc |

### SAP Classification for Revenue (Combined Approach)

Revenue MUST use a **combined SAP + TOD** approach when ISA 240 fraud risk is presumed:

1. **SAP Component:** Independently calculate expected revenue from underlying data
   - Interest income: loan balances × contractual rates × time periods
   - Service revenue: contracts × rates × volume
   - Rental income: tenancy agreements × rates × months

2. **TOD Component:** Vouch a sample of transactions to source documents
   - Select items above PM for 100% testing
   - Sample remaining population per ISA 530
   - Vouch to contracts, invoices, delivery orders, bank receipts

3. **Reconciliation:** SAP total vs GL total vs TOD sample results → combined conclusion

### SAP for Balance Sheet Items

SAP can also be applied to predictable balance sheet items:

| Item | SAP Basis |
|------|----------|
| **Depreciation / Accumulated depreciation** | Recalculate from FAR — rates × cost × time |
| **EPF/SOCSO/EIS accruals** | Last month's statutory contribution accrued |
| **Salary accrual** | Last month's payroll accrued (if paid in arrears) |
| **Interest accrual** | Loan balance × rate × days accrued |
| **Rental accrual/prepayment** | Monthly rent × months accrued/prepaid |
| **Director balance movement** | Opening + advances − repayments = closing (reconcile from GL) |

### GL-Driven Auto-Population for SAP

**If the General Ledger (GL) PDF or data is available** in the engagement's source documents, SAP tables should be **auto-populated** rather than left with placeholder amounts:

1. **Extract GL balances** — read the GL/TB to obtain the actual amount per account code for each line item
2. **Populate the "GL Amount" column** directly from the extracted data
3. **Calculate differences** — compute (Auditor Expected − GL Amount) automatically
4. **Apply threshold test** — compare each difference to MAX(Performance Materiality, 5% of line item) and populate "Within Threshold?" column
5. **Flag exceptions automatically** — any item where difference exceeds threshold gets "Investigate" in the Conclusion column with a note to document the cause
6. **Pre-fill the conclusion** — "Satisfactory" for items within threshold; "Exception — investigate [description]" for items outside threshold
7. **Cross-reference to GL account codes** — include the GL account number in the SAP table for traceability back to the source data

**Same principle applies to all SAP-testable items across working papers:**
- **E4 (Admin Expenses):** Extract each expense line from GL, compare to auditor expectation (rental × 12, EPF rate × remuneration, etc.)
- **E1 (Revenue):** Extract revenue total from GL, compare to SAP calculation from loan data
- **C1 (PPE — Depreciation):** Extract depreciation charge from GL, compare to FAR recalculation
- **D8 (Accruals):** Extract accrual balances from GL, compare to expected statutory accruals
- **Balance sheet items:** Extract closing balances, perform movement analysis (opening + additions − disposals = closing)

**If GL is NOT available**, use `{{variable}}` placeholders from master_data.json and note "GL amount sourced from TB / master_data — to be verified against GL when received."

### Integration with Working Papers

When generating working papers via `/awp`:

1. **Section E (Income Statement):** Classify every line item as SAP, TOD, or COMBINED in the "Test Method Classification" table at the start of the working paper
2. **SAP items:** Build the auditor expectation calculation table as the PRIMARY substantive test
3. **TOD items:** Build the vouching/sampling framework as the PRIMARY substantive test
4. **COMBINED items:** Build both SAP calculation AND TOD sampling, with a reconciliation section
5. **Exceptions from SAP:** Any difference exceeding the threshold must be investigated — document cause, assess whether it represents a misstatement, and record in F6 if applicable
6. **SAP reduces but does not eliminate TOD:** Even when SAP is satisfactory, the auditor should still vouch selected high-value or unusual items for corroboration
7. **GL-driven population:** When GL data is available, auto-populate all SAP tables and B2 journal entry testing with actual figures — do not leave tables empty or pending when the data exists in the source documents

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
│   ├── B2_Journal_Entry_Testing.md
│   ├── B3_Walkthrough_Tests.md
│   └── B4_Control_Deficiencies.md
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
├── 00_Index.md
├── master_data.json
├── generate_templates.py          # Copied from skill asset on /templates run
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

Every working paper MUST include a risk linkage section connecting to the A4 risk assessment:

**Risks Addressed:** [Reference to A4 assertion-level risk assessment — e.g., "A4 Ref: C6-EX HIGH, C6-VAL HIGH, C6-COMP MEDIUM"]
**Inherent Risk Justification (per A4):** [Summarize why inherent risk is at the assessed level — e.g., "HIGH — 93% decline in loan book; borrower creditworthiness uncertain"]
**Control Risk:** HIGH — fully substantive approach; no tests of controls performed (ISA 330.8)
**RMM Level:** [HIGH/MEDIUM/LOW per A4]
**Planned Response per A4:** [Nature, timing, extent + Test Method (SAP/TOD/Combined)]
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

---

## Additional References

For detailed WP templates (A1, B1, B2, F2, F7, F8, F9), ISA procedure guides (ISA 505, 540, 550, 570), and the master_data.json variable schema, see the companion reference file: `AWP_REFERENCE.md` in this skill folder.
