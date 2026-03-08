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

## Python Scripts

Located in `scripts/` within this skill folder:
- `word_utils.py` - Create Word documents for FS, management letters, representation letters
- `fs_generator.py` - MPERSFinancialStatements class for complete FS packages

### Usage
```python
from fs_generator import generate_mpers_fs, MPERSFinancialStatements

# Quick generation
generate_mpers_fs(
    filepath='output.docx',
    company_name='ABC Sdn. Bhd.',
    company_no='123456-X',
    year_end='31 December 2024'
)

# With data
fs = MPERSFinancialStatements(
    company_name='ABC Sdn. Bhd.',
    company_no='123456-X',
    year_end='31 December 2024',
    directors=['Director A', 'Director B']
)
fs.set_sofp_data({...})
fs.set_soci_data({...})
fs.generate_full_fs('output.docx')
```
