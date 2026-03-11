# AWP Reference: Templates, Variables & ISA Procedures

This file contains detailed templates and reference material for the /awp skill.

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

## B2 — Journal Entry Testing Template (ISA 240.32)

**MANDATORY for ALL engagements** — management override is a presumed fraud risk that cannot be rebutted.

### GL-Driven Auto-Population

**If the General Ledger (GL) PDF or data is available** in the engagement's source documents, the B2 working paper should be **auto-populated** rather than left pending:

1. **Parse the GL** — extract all journal entries (date, reference, description, account code, debit, credit, posted by)
2. **Apply selection criteria** — filter entries matching the 10 fraud risk indicators below (criteria 2-5 are mandatory; apply judgment for 1, 6-10)
3. **Populate the testing results table** (Part 4) with all selected entries pre-filled
4. **Cross-reference known transactions** — match GL entries to known material movements from other WPs (e.g., director account entries to D9, receivable entries to C6, revenue entries to E1)
5. **Flag anomalies automatically**:
   - Round-number entries ≥ Performance Materiality
   - Entries with blank or generic descriptions (e.g., "adjustment", "JV", "correction")
   - Entries to revenue accounts near period end (cutoff risk)
   - Entries to related party accounts
   - Post-closing entries (entries dated after year-end but posted to the FY)
   - Debit/credit combinations that are unusual for the account type
6. **Pre-assess business rationale** where determinable from GL context (e.g., monthly salary entries = routine; one-off large transfers = flag for investigation)
7. **Set testing status** — mark entries as "Verified" where GL data alone provides sufficient evidence (e.g., recurring entries matching SAP expectations), or "Requires Vouching" where supporting documents are needed

**If GL is NOT available**, leave Part 4 as pending with PBC requirements documented in Part 9.

When generating B2, include ALL of the following sections:

### Part 1: Understanding the Journal Entry Process
| Aspect | Description |
|--------|-------------|
| Accounting software | [Software used] |
| Who posts journal entries | [Directors / accountant / external] |
| Approval process | [Formal / informal / none] |
| Types of entries | Standard (recurring), Non-standard (manual), Post-closing (year-end) |
| Segregation of duties | [Yes / No — if no, state why management override risk is elevated] |

### Part 2: Population & Selection Criteria

**Population:** All journal entries posted during the financial year.

**Mandatory Selection Criteria (ISA 240 fraud risk indicators):**

| # | Criterion | Rationale |
|---|-----------|-----------|
| 1 | Manual journal entries | Higher manipulation risk than system-generated |
| 2 | Post-closing / year-end adjustments | May manipulate year-end results |
| 3 | Entries to related party accounts | Management override risk; RPT manipulation |
| 4 | Entries to revenue accounts | ISA 240 presumed fraud risk on revenue |
| 5 | Entries to material asset/liability accounts | Existence and valuation risk |
| 6 | Round-number entries ≥ Performance Materiality | Common fraud indicator |
| 7 | Entries with no or weak description | May indicate unauthorized entries |
| 8 | Entries posted by unusual persons | Detection of unauthorized access |
| 9 | Unusual account combinations | Debit/credit pairs not aligned with normal transactions |
| 10 | Entries above Performance Materiality | Material entries warrant individual examination |

**Selection method:** Select ALL entries meeting criteria 2-5 (mandatory fraud risk accounts). Apply professional judgment for remaining criteria. Ensure coverage across all periods.

### Part 3: Testing Procedures
For each selected entry:
1. Verify correct period recording
2. Agree to supporting documentation
3. Assess valid business rationale
4. Verify authorization (who posted, who approved)
5. Evaluate appropriateness of debit/credit accounts
6. For RPT entries — trace to bank statements or agreements
7. For revenue entries — verify occurrence against source documents
8. For post-closing entries — assess business purpose

### Part 4: Testing Results Table
| # | Date | JE Ref | Description | Account DR | Account CR | Amount | Criterion Met | Support Verified? | Business Rationale? | Result |
|---|------|--------|-------------|-----------|-----------|--------|---------------|-------------------|-------------------|--------|

Include a "Key Focus Areas" section listing known material transactions from other WPs that must be verified through JE testing (cross-reference to relevant AWP refs using `[REF](#awp:REF)` format).

### Part 5: Review of Accounting Estimates (ISA 240.32(b))
For every accounting estimate in the FS:
| Estimate | Method | Auditor Assessment | Bias Indicator? | WP Ref |
|----------|--------|-------------------|----------------|--------|

Assess direction of bias based on entity's financial position and management motivation.

### Part 6: Evaluation of Unusual Transactions (ISA 240.32(c))
| # | Transaction | Nature | Amount | Business Rationale | Assessment |
|---|-------------|--------|--------|-------------------|------------|

Assess whether significant unusual transactions have a valid business purpose or indicate fraud/error.

### Part 7: Assertion-Level Conclusions
Conclude on: Occurrence, Completeness, Accuracy, Classification, Cutoff.

### Part 8: Evidence Quality
Document type, source, reliability, and sufficiency of evidence obtained.

### Part 9: PBC Requirements
List all documents needed from client for journal entry testing with status and priority.

**Cross-references:** Link to [A4](#awp:A4) (risk assessment — ISA240-MO), [B1](#awp:B1) (ICQ), and all material balance WPs tested.

---

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

---

## Engagement Team Fraud Discussion (ISA 240.15)

**Mandatory for every engagement.** Document in A2 (Planning Memorandum) or as a standalone section in A5.

### Template

| | |
|---|---|
| **Date of Discussion** | [Date] |
| **Participants** | [Names and roles — must include engagement partner] |
| **Location/Format** | [In-person / video / phone] |

### Required Discussion Points

| # | Discussion Topic | Key Points Raised | Impact on Audit Plan |
|---|-----------------|-------------------|---------------------|
| 1 | **How and where the FS may be susceptible to material misstatement due to fraud** | [e.g., Revenue recognition, expense manipulation, journal entries] | [e.g., Extended cutoff testing, SAP + TOD on revenue] |
| 2 | **Known fraud risk factors for this entity** | [e.g., Owner-managed, no segregation of duties, cash-intensive, related party dominance] | [e.g., Journal entry testing per B2, RPT verification per F3] |
| 3 | **Revenue recognition risks specific to this entity** | [e.g., Interest income calculation, timing of recognition, fictitious loans] | [e.g., Independent recalculation, confirmation of loan balances] |
| 4 | **How management could perpetrate and conceal fraud** | [e.g., Override journal entries, manipulate estimates, fictitious transactions with related parties] | [e.g., B2 journal entry testing, ISA 540 estimate review] |
| 5 | **Management override risks specific to this entity** | [e.g., Director controls all banking, single signatory, no board oversight of transactions] | [e.g., Test 100% of director account transactions, verify to bank] |
| 6 | **Professional skepticism emphasis** | [e.g., Do not assume management is dishonest or honest; challenge evidence that appears too convenient] | [e.g., Corroborate all management representations with external evidence where possible] |

**Note:** The discussion must occur BEFORE designing substantive procedures. Conclusions from this discussion inform the risk assessment (A4) and fraud procedures (B2).

---

## Directors' Report Consistency Review (ISA 720)

**Mandatory for every engagement.** Document in G1 (Directors' Report) working paper.

### Procedure

When the directors' report (G1) is drafted or received, the auditor must:

1. **Read the directors' report** and identify all financial and non-financial information
2. **Compare financial information** to the audited financial statements for consistency:

| Directors' Report Item | FS Cross-Reference | Consistent? | Exception Detail |
|----------------------|-------------------|-------------|-----------------|
| Revenue / turnover figures | G3 (SOCI), Note [X] | [ ] | |
| Profit / loss figures | G3 (SOCI) | [ ] | |
| Dividend declared / proposed | D2 (Reserves), Note [X] | [ ] | |
| Directors' remuneration | Note [X], T15 | [ ] | |
| Directors' shareholding | Note [X], T16 | [ ] | |
| Principal activities description | A3 (Understanding Entity) | [ ] | |
| Significant events after year end | F2, Note [X] | [ ] | |

3. **Assess for material inconsistency** — if the directors' report contains information that is materially inconsistent with the audited FS:
   - Determine whether the FS or the directors' report needs revision
   - Discuss with management
   - If not corrected: describe the material inconsistency in the auditor's report (ISA 720.22)

4. **Assess for material misstatement of fact** — if information in the directors' report (not derived from FS) appears materially misstated:
   - Discuss with management
   - If not corrected: take appropriate action (communicate to TCWG, obtain legal advice)

---

## Audit Report Modification Decision Tree (ISA 705)

Use this decision tree when determining the appropriate audit opinion:

### Step 1: Are there misstatements?

```
Has the auditor identified misstatements?
├── YES → Go to Step 2
└── NO → Has the auditor been unable to obtain sufficient appropriate evidence?
    ├── YES → Go to Step 3
    └── NO → UNMODIFIED OPINION (ISA 700)
```

### Step 2: Misstatements identified

```
Are the misstatements material?
├── NO → UNMODIFIED OPINION (communicate uncorrected misstatements to TCWG per ISA 450)
└── YES → Are the misstatements pervasive? (affects multiple elements, substantial portion, or fundamental to users)
    ├── NO → QUALIFIED OPINION ("Except for...")
    └── YES → ADVERSE OPINION ("Do not give a true and fair view...")
```

### Step 3: Inability to obtain sufficient evidence

```
Is the possible effect material?
├── NO → UNMODIFIED OPINION (document limitation and why impact is immaterial)
└── YES → Is the possible effect pervasive?
    ├── NO → QUALIFIED OPINION — scope limitation ("Except for the possible effects...")
    └── YES → DISCLAIMER OF OPINION ("We do not express an opinion...")
```

### Step 4: Going concern considerations (ISA 570)

```
Does material uncertainty exist related to going concern?
├── NO → No GC modification needed
└── YES → Is the GC basis of accounting appropriate?
    ├── NO → ADVERSE OPINION (GC basis inappropriate)
    └── YES → Is there adequate disclosure of the material uncertainty?
        ├── YES → UNMODIFIED + "Material Uncertainty Related to Going Concern" section
        └── NO → QUALIFIED or ADVERSE (depending on severity)
```

### Step 5: Emphasis of Matter (ISA 706)

```
Is there a matter already disclosed in the FS that is fundamental to users' understanding?
├── YES → Add EOM paragraph (does NOT modify opinion)
└── NO → No EOM needed
```

### Quick Reference Matrix

| Situation | Material? | Pervasive? | Opinion |
|-----------|-----------|------------|---------|
| Misstatement — corrected | N/A | N/A | Unmodified |
| Misstatement — uncorrected, immaterial | No | N/A | Unmodified |
| Misstatement — uncorrected | Yes | No | Qualified |
| Misstatement — uncorrected | Yes | Yes | Adverse |
| Scope limitation — immaterial | No | N/A | Unmodified |
| Scope limitation | Yes | No | Qualified |
| Scope limitation | Yes | Yes | Disclaimer |
| GC uncertainty — adequate disclosure | Yes | N/A | Unmodified + Material Uncertainty section |
| GC uncertainty — inadequate disclosure | Yes | No | Qualified |
| GC uncertainty — inadequate disclosure | Yes | Yes | Adverse |
| GC basis inappropriate | Yes | Yes | Adverse |
