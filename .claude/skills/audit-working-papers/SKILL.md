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
│   └── F8_Completion_Checklist.md
├── G_Outstanding/
│   ├── G1_Directors_Report.md
│   ├── G2_SOFP.md
│   ├── G3_SOCI.md
│   ├── G4_SOCE.md
│   ├── G5_SCF.md
│   ├── G6_Notes.md
│   └── G7_Supplementary_Info.md
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
```
