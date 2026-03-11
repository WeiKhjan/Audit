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

## Related Skills

- **Fraud risk procedures** (ISA 240) and **risk-response traceability** (ISA 330): see `/fraud-risk`
