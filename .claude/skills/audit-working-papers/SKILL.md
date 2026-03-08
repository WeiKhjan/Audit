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
```

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

## Python Scripts

Located in `scripts/` within this skill folder:
- `excel_utils.py` - Create Excel lead schedules, PPE schedules, bank reconciliations, PBC checklists, query lists
- `audit_runner.py` - AuditEngagement class for orchestrating full audit workflow

### Usage
```python
from excel_utils import create_lead_schedule, create_ppe_schedule, create_bank_reconciliation
from audit_runner import AuditEngagement

engagement = AuditEngagement(
    client_name="Company Sdn. Bhd.",
    company_no="123456-X",
    year_end="31 December 2024",
    output_dir="./Clients/AWP_Company_FYE2024"
)
```

## Output Folder Structure

```
Clients/AWP_[Client]_FYE[Year]/
├── A_Planning/
├── B_Internal_Control/
├── C_Assets/
├── D_Liabilities_Equity/
├── E_Income_Statement/
├── F_Completion/
├── G_Outstanding/
├── 00_Index.md
├── audit_viewer.html
└── START_VIEWER.bat
```
