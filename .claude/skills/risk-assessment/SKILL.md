---
name: risk-assessment
description: Perform audit risk assessment and identify red flags for Malaysian statutory audits
---

# Risk Assessment

## Risk Assessment Matrix

| Risk Area | Considerations |
|-----------|----------------|
| **Inherent Risk** | Industry, complexity, related parties, new transactions |
| **Control Risk** | Size of entity, segregation of duties, IT systems |
| **Detection Risk** | Nature of balances, estimation uncertainty |
| **Fraud Risk** | Management override, revenue recognition, journal entries |
| **Going Concern** | Liquidity, profitability, debt covenants |

## Financial Statement Level Red Flags

| Red Flag | Implication | Procedure |
|----------|-------------|-----------|
| Significant related party transactions | Non-arm's length, disclosure risk | Extended RPT procedures |
| High debt-to-equity ratio | Going concern risk | Review loan covenants, cash flows |
| Declining gross margins | Inventory valuation, revenue recognition risk | Detailed margin analysis |
| Unusual journal entries | Fraud risk | Journal entry testing |
| Significant estimates | Valuation risk | Review assumptions, sensitivity |
| Prior period adjustments | Control deficiency | Understand root cause |
| Delays in providing PBC | Potential issues being hidden | Professional skepticism |

## Account Level Common Issues

| Account | Common Issues |
|---------|---------------|
| PPE | Incorrect capitalization, wrong depreciation rates, impairment not assessed |
| Receivables | Inadequate impairment, cutoff errors, fictitious sales |
| Inventory | Obsolescence not provided, NRV below cost, existence |
| Payables | Unrecorded liabilities, cutoff errors |
| Revenue | Premature recognition, channel stuffing, bill-and-hold |
| Expenses | Personal expenses, unsubstantiated claims, WHT non-compliance |

## Malaysia-Specific Issues

| Issue | Consideration |
|-------|---------------|
| Withholding Tax (S109/S109B) | Payments to non-residents - 10% to 15% |
| SST Compliance | Registration threshold RM500k, proper accounting |
| Transfer Pricing | Related party transactions documentation (TP rules) |
| EPF/SOCSO Compliance | Proper contributions, timely remittance |
| Companies Act 2016 | Director duties, S248-251 declaration requirements |
| MACC Act | Anti-corruption provisions, adequate procedures |

## Risk Response

For each identified risk:
1. **Assess** - Inherent risk level (High/Medium/Low)
2. **Evaluate controls** - Does the client have mitigating controls?
3. **Design procedures** - Nature, timing, extent of substantive testing
4. **Document** - Risk, response, and conclusion in working papers

---

## Assertion-Level Risk Assessment (ISA 315)

### Risk-to-Assertion Mapping Template

For EVERY material account, map risks to specific assertions with justifications and AWP links:

| Account | WP Ref | Assertion | Inherent Risk | Inherent Risk Justification | Control Risk | RMM Level | Planned Response (with AWP Link) |
|---------|--------|-----------|---------------|---------------------------|-------------|-----------|--------------------------------|
| Trade Receivables | C6 | Existence | [H/M/L] | [e.g., "HIGH — 93% decline; borrower creditworthiness uncertain; core asset"] | [H/M/L] | [H/M/L] | [e.g., External confirmation + subsequent receipts → See [C6](#awp:C6)] |
| Trade Receivables | C6 | Valuation | [H/M/L] | [e.g., "HIGH — MPERS incurred loss model; significant estimation; aging needed"] | [H/M/L] | [H/M/L] | [e.g., Impairment assessment → See [C6](#awp:C6)] |
| Revenue | E1 | Occurrence | [H/M/L] | [e.g., "MEDIUM — simple model but ISA 240 fraud presumed; declining is consistent"] | [H/M/L] | [H/M/L] | [e.g., SAP + TOD combined → See [E1](#awp:E1)] |

**MANDATORY:** Every row MUST have:
1. A written justification in the "Inherent Risk Justification" column (not blank)
2. A planned response that references the specific AWP section (e.g., "→ See [C6](#awp:C6)")
3. Where SAP is the primary test method, indicate "SAP" or "SAP + TOD" in the planned response

**Cross-reference format:** Planned responses MUST use `[REF](#awp:REF)` format for working paper cross-references (e.g., `→ See [C6](#awp:C6)`) to enable clickable navigation in the audit viewer.

### Risk Assessment Factors

**Inherent Risk** — MUST be justified per assertion with specific engagement factors:

| Inherent Risk Level | Criteria (document at least 2 factors per assessment) |
|--------------------|----------------------------------------------------|
| **HIGH** | Susceptibility to material misstatement is elevated due to: complexity/subjectivity of the balance; significant YoY movements (>30%); related party involvement; estimation uncertainty; fraud risk indicators; regulatory sensitivity; prior period misstatements |
| **MEDIUM** | Moderate susceptibility: some complexity but largely verifiable; moderate movements; standard calculations with limited estimation; single data source |
| **LOW** | Low susceptibility: routine, recurring, predictable amounts; independently verifiable (SAP-suitable); small balances; standard calculations with no estimation; no unusual movements |

Every inherent risk assessment MUST include a **written justification** explaining WHY that level was chosen, referencing specific engagement facts (e.g., "HIGH — 93% decline in receivables; borrower creditworthiness uncertain; core asset of money lending business").

**Control Risk** — document the overall assessment and rationale:

For **small/owner-managed entities** using a fully substantive approach:
> "Control risk is assessed as HIGH for ALL assertions. [Entity name] is a small owner-managed entity with no segregation of duties, no formal internal control system, and no internal audit function. No tests of controls are performed; a fully substantive audit approach is adopted per ISA 330.8."

For entities where controls are tested:
> Document: (1) which controls were tested, (2) results of testing, (3) resulting control risk assessment per assertion.

**RMM (Risk of Material Misstatement)** = function of inherent risk × control risk:

| Inherent Risk | Control Risk HIGH | Control Risk MEDIUM | Control Risk LOW |
|--------------|------------------|--------------------|-----------------|
| HIGH | **HIGH** | HIGH | MEDIUM |
| MEDIUM | MEDIUM | MEDIUM | LOW |
| LOW | LOW | LOW | LOW |

### Significant Risks (ISA 315.28)

A risk is SIGNIFICANT when it requires special audit consideration due to:
- Fraud risk
- Recent significant developments (economic, accounting, regulatory)
- Complexity of transactions
- Significant related party transactions
- High degree of subjectivity/estimation uncertainty
- Unusual transactions outside normal course

**For each significant risk, document:**
1. Why the risk is significant
2. Whether related controls have been identified
3. What substantive procedures specifically address the significant risk (ISA 330.15)
4. These procedures MUST include tests of details (cannot rely solely on substantive analytical procedures)

---

## Fraud Risk Procedures (ISA 240)

### Presumed Fraud Risks

Per ISA 240, the following risks are ALWAYS presumed unless rebutted:

#### 1. Revenue Recognition Fraud (ISA 240.26)
- **Default presumption:** Risk of fraud in revenue recognition
- **Rebuttal:** Only if specific conditions justify (document rationale)
- **Procedures when presumed:**
  - Cutoff testing around year end
  - Search for fictitious revenue entries
  - Analytical review of revenue trends vs. industry
  - Review of unusual revenue transactions (large/unusual customers, round amounts)
  - Contract review for proper recognition criteria
  - Reconcile revenue to cash receipts and receivables

#### 2. Management Override of Controls (ISA 240.32)
- **Cannot be rebutted** — always a fraud risk
- **Mandatory procedures:**
  - **Journal entry testing:** Test journal entries and other adjustments
    - Selection criteria: manual entries, post-closing entries, unusual amounts, round numbers, entries by unexpected users, entries to unusual accounts
    - Testing approach: vouch to supporting documentation, assess business rationale
  - **Review accounting estimates for bias:** Retrospective review of PY estimates; evaluate current year assumptions
  - **Evaluate business rationale** for significant unusual transactions

### Journal Entry Testing Template

| Selection Criteria | Entries Selected | Tested | Finding |
|-------------------|-----------------|--------|---------|
| Manual journal entries | [Count] | [Count] | |
| Post-closing adjustments | [Count] | [Count] | |
| Entries to unusual accounts | [Count] | [Count] | |
| Round-number entries above threshold | [Count] | [Count] | |
| Entries by senior management | [Count] | [Count] | |
| Entries with no/weak description | [Count] | [Count] | |

### Fraud Risk Discussion (ISA 240.15)

Document the engagement team discussion on fraud risks:
- Date of discussion:
- Participants:
- Key points discussed:
  - How and where the FS may be susceptible to material misstatement due to fraud
  - Known fraud risk factors for the entity
  - Revenue recognition risks specific to this entity
  - How management could perpetrate and conceal fraud
  - Management override risks specific to this entity

---

## Risk-Response Traceability (ISA 330)

### Risk Response Design Template

For each risk identified in the risk assessment, document the specific response:

| A4 Risk Ref | Risk Description | RMM Level | Nature of Response | Test Method | Timing | Extent | WP Ref |
|------------|-----------------|-----------|-------------------|------------|--------|--------|--------|
| [e.g., C6-EX] | [e.g., Existence of receivables] | HIGH | [e.g., External confirmation + subsequent receipts] | TOD | [Year-end] | [100% of material balances] | [C6](#awp:C6) |
| [e.g., E4-OCC] | [e.g., Expense occurrence] | LOW | [e.g., SAP for recurring items; vouch one-offs] | SAP + TOD | [Year-end] | [SAP: all recurring; TOD: sample one-offs] | [E4](#awp:E4) |

### Response Design Requirements

**For HIGH risk areas:**
- More persuasive evidence required (external > internal; direct > indirect)
- Larger sample sizes
- More extensive procedures (tests of details rather than analytical procedures alone)
- Consider timing: year-end testing preferred over interim

**For SIGNIFICANT risks (ISA 330.15):**
- Substantive procedures MUST include tests of details
- Cannot rely solely on analytical procedures
- Must specifically address why the risk is significant
- Consider using unpredictable audit procedures

**For ALL risks:**
- Document the linkage between risk assessment and audit response
- Explain how the nature, timing, and extent of procedures address the assessed risk
- If control testing is planned, document the controls tested and results
- If only substantive approach, document why controls are not being tested

### Overall Response to Financial Statement Level Risks

For pervasive risks affecting the FS as a whole:
| Risk | Response |
|------|---------|
| Management integrity concerns | Assign more experienced staff; increase professional skepticism; unpredictable procedures |
| Weak control environment | Fully substantive approach; more procedures at year-end vs interim |
| Going concern | Extended going concern procedures; assess appropriateness of GC basis |
| Fraud risk (general) | Engagement team discussion; journal entry testing; review estimates for bias |
