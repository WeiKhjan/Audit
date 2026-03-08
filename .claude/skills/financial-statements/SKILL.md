---
name: fs
description: Draft MPERS/MFRS-compliant financial statements for Malaysian statutory audits
---

# Financial Statements

## MPERS Financial Statements Components

1. **Statement of Financial Position** (SOFP)
2. **Statement of Comprehensive Income** (SOCI) - or separate Income Statement + OCI
3. **Statement of Changes in Equity** (SOCE)
4. **Statement of Cash Flows** (SCF)
5. **Notes to the Financial Statements**

## Standard Notes Structure (MPERS)

```
1.  Corporate Information
2.  Basis of Preparation
3.  Significant Accounting Policies
    3.1  Property, Plant & Equipment
    3.2  Investment Properties
    3.3  Financial Instruments
    3.4  Inventories
    3.5  Revenue Recognition
    3.6  Leases
    3.7  Income Tax
    3.8  Employee Benefits
    3.9  Foreign Currency
    3.10 Provisions
4.  Critical Accounting Estimates & Judgements
5.  Property, Plant & Equipment
6.  Investment Properties
7.  Intangible Assets
8.  Investments
9.  Inventories
10. Trade Receivables
11. Other Receivables, Deposits & Prepayments
12. Amount Due from Related Parties
13. Cash & Bank Balances
14. Share Capital
15. Reserves
16. Retained Earnings
17. Borrowings
18. Hire Purchase Payables
19. Deferred Tax Liabilities
20. Trade Payables
21. Other Payables & Accruals
22. Amount Due to Directors
23. Amount Due to Related Parties
24. Revenue
25. Cost of Sales
26. Other Income
27. Administrative Expenses
28. Finance Costs
29. Tax Expense
30. Directors' Remuneration
31. Employee Benefits Expense
32. Related Party Transactions
33. Contingent Liabilities
34. Capital Commitments
35. Financial Instruments
36. Subsequent Events
```

## MPERS vs MFRS Key Differences

| Area | MPERS | MFRS |
|------|-------|------|
| Financial Instruments | Simplified (basic/complex) | MFRS 9 (amortised cost/FVOCI/FVTPL) |
| Impairment of Receivables | Incurred loss model | Expected Credit Loss (ECL) model |
| Leases | Finance vs Operating distinction | MFRS 16 right-of-use model |
| Revenue | Risk & rewards transfer | MFRS 15 five-step model |
| Goodwill | Amortised (max 10 years) | Impairment-only approach |

## Directors' Report Sections

- Principal Activities
- Results (profit/loss for the year)
- Dividends
- Reserves and Provisions
- Directors (list of directors who served)
- Directors' Interests (Section 59 Companies Act 2016)
- Directors' Benefits
- Indemnity and Insurance
- Other Statutory Information (Sections 248-251)
- Auditors / Auditors' Remuneration

## Output Format

Financial statements are generated as `.md` files in the `G_Outstanding/` folder within the client engagement directory:

```
G_Outstanding/
├── G1_Directors_Report.md
├── G2_SOFP.md
├── G3_SOCI.md
├── G4_SOCE.md
├── G5_SCF.md
├── G6_Notes.md
└── G7_Supplementary_Info.md
```

## Variable Usage in Financial Statements

All monetary figures MUST use `{{variable}}` placeholders from `master_data.json`. Never hardcode figures.

### SOFP Template Structure

```markdown
---
ref: G2
title: Statement of Financial Position
section: G_Outstanding
---

# {{company_name}}
## (Company No. {{company_reg_no}})
## STATEMENT OF FINANCIAL POSITION AS AT {{year_end_date}}

| | Note | {{fye_year}} | {{py_fye_year}} |
|---|---|---|---|
| | | **RM** | **RM** |
| **NON-CURRENT ASSETS** | | | |
| Property, plant and equipment | 5 | {{total_ppe}} | {{py_total_ppe}} |
| Investment properties | 6 | {{total_investment_properties}} | {{py_total_investment_properties}} |
| | | **{{total_non_current_assets}}** | **{{py_total_non_current_assets}}** |
| **CURRENT ASSETS** | | | |
| Inventories | 9 | {{total_inventories}} | {{py_total_inventories}} |
| Trade receivables | 10 | {{total_trade_receivables}} | {{py_total_trade_receivables}} |
| Other receivables, deposits & prepayments | 11 | {{total_other_receivables}} | {{py_total_other_receivables}} |
| Cash and bank balances | 13 | {{total_cash_bank}} | {{py_total_cash_bank}} |
| | | **{{total_current_assets}}** | **{{py_total_current_assets}}** |
| **TOTAL ASSETS** | | **{{total_assets}}** | **{{py_total_assets}}** |
| | | | |
| **EQUITY** | | | |
| Share capital | 14 | {{share_capital}} | {{py_share_capital}} |
| Retained earnings | 16 | {{retained_earnings}} | {{py_retained_earnings}} |
| **TOTAL EQUITY** | | **{{total_equity}}** | **{{py_total_equity}}** |
| | | | |
| **NON-CURRENT LIABILITIES** | | | |
| Borrowings | 17 | {{nc_borrowings}} | {{py_nc_borrowings}} |
| Hire purchase payables | 18 | {{nc_hp_liabilities}} | {{py_nc_hp_liabilities}} |
| Deferred tax liabilities | 19 | {{total_deferred_tax}} | {{py_total_deferred_tax}} |
| | | **{{total_non_current_liabilities}}** | **{{py_total_non_current_liabilities}}** |
| **CURRENT LIABILITIES** | | | |
| Trade payables | 20 | {{total_trade_payables}} | {{py_total_trade_payables}} |
| Other payables & accruals | 21 | {{total_other_payables}} | {{py_total_other_payables}} |
| Amount due to directors | 22 | {{amount_due_directors}} | {{py_amount_due_directors}} |
| Tax payable | | {{total_tax_payable}} | {{py_total_tax_payable}} |
| | | **{{total_current_liabilities}}** | **{{py_total_current_liabilities}}** |
| **TOTAL LIABILITIES** | | **{{total_liabilities}}** | **{{py_total_liabilities}}** |
| **TOTAL EQUITY AND LIABILITIES** | | **{{total_equity_liabilities}}** | **{{py_total_equity_liabilities}}** |
```

### Notes Template Structure (PPE Example)

```markdown
### 5. PROPERTY, PLANT AND EQUIPMENT

| | Land & Buildings | Motor Vehicles | Office Equipment | Furniture & Fittings | Total |
|---|---|---|---|---|---|
| **Cost** | | | | | |
| At beginning of year | {{py_ppe_land_cost}} | {{py_ppe_mv_cost}} | {{py_ppe_oe_cost}} | {{py_ppe_ff_cost}} | {{py_ppe_total_cost}} |
| Additions | {{ppe_land_additions}} | {{ppe_mv_additions}} | {{ppe_oe_additions}} | {{ppe_ff_additions}} | {{ppe_total_additions}} |
| Disposals | {{ppe_land_disposals}} | {{ppe_mv_disposals}} | {{ppe_oe_disposals}} | {{ppe_ff_disposals}} | {{ppe_total_disposals}} |
| At end of year | {{ppe_land_cost}} | {{ppe_mv_cost}} | {{ppe_oe_cost}} | {{ppe_ff_cost}} | {{ppe_total_cost}} |
| **Accumulated Depreciation** | | | | | |
| At beginning of year | {{py_ppe_land_ad}} | {{py_ppe_mv_ad}} | {{py_ppe_oe_ad}} | {{py_ppe_ff_ad}} | {{py_ppe_total_ad}} |
| Charge for the year | {{ppe_land_depn}} | {{ppe_mv_depn}} | {{ppe_oe_depn}} | {{ppe_ff_depn}} | {{ppe_total_depn}} |
| Disposals | {{ppe_land_ad_disp}} | {{ppe_mv_ad_disp}} | {{ppe_oe_ad_disp}} | {{ppe_ff_ad_disp}} | {{ppe_total_ad_disp}} |
| At end of year | {{ppe_land_ad}} | {{ppe_mv_ad}} | {{ppe_oe_ad}} | {{ppe_ff_ad}} | {{ppe_total_ad}} |
| **Net Book Value** | **{{ppe_land_nbv}}** | **{{ppe_mv_nbv}}** | **{{ppe_oe_nbv}}** | **{{ppe_ff_nbv}}** | **{{total_ppe}}** |
```

## Quality Checklist for FS Drafts

Before delivering any financial statement set, verify:
- [ ] **No hardcoded financial figures** — all amounts use `{{variable}}` placeholders
- [ ] Every variable exists in `master_data.json`
- [ ] SOFP balances: Total Assets = Total Equity + Total Liabilities
- [ ] SOCI ties to Retained Earnings movement in SOCE
- [ ] Note references in SOFP/SOCI match actual note numbers in G6
- [ ] Prior year comparatives included for all line items
- [ ] Directors' Report profit figure matches SOCI
- [ ] Proper MPERS/MFRS terminology used throughout
