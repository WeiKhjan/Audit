---
name: sampling
description: Generate ISA 530 compliant audit sampling working papers with MUS calculation, selection methods, and evaluation framework
---

# Audit Sampling (ISA 530)

## Overview

This skill generates formal audit sampling documentation compliant with ISA 530 *Audit Sampling*. It produces companion working papers (suffixed `-S`) that sit alongside the main substantive testing paper for each audit area.

## Naming Convention

- Companion papers: `[Ref]-S` (e.g., `C6-S` for Trade Receivables sampling)
- Variables: `samp_[area]_[field]` (e.g., `samp_c6_population_value`, `samp_c6_sample_size`)
- Sampling table markers: `<!-- SAMPLING_TABLE -->` / `<!-- /SAMPLING_TABLE -->` for viewer detection

---

## MUS (Monetary Unit Sampling) Formula

```
n = CF × (PV / TM)
```

Where:
- **n** = Sample size (number of sampling units)
- **CF** = Confidence Factor (based on Risk of Incorrect Acceptance)
- **PV** = Population Value (total book value of the population)
- **TM** = Tolerable Misstatement (usually = Performance Materiality)

### Confidence Factor Table (Poisson-based)

| Risk of Incorrect Acceptance (RIA) | Risk Level | Confidence Factor (CF) | ISA 530 Guidance |
|-------------------------------------|------------|------------------------|------------------|
| 37% | Low | 1.00 | Low assessed RMM; strong controls |
| 20% | Moderate-Low | 1.61 | Some reliance on controls |
| 14% | Moderate | 2.00 | Moderate RMM; limited control reliance |
| 10% | High | 2.31 | High assessed RMM; little control reliance |
| 5% | Very High | 3.00 | Very high RMM; no control reliance |

### RIA Determination

RIA is derived from the Audit Risk Model (ISA 530.A10):

```
Audit Risk (AR) = IR × CR × DR
Detection Risk (DR) = AR / (IR × CR)
RIA ≈ DR for substantive tests of details
```

| Inherent Risk | Control Risk | RIA | CF |
|---------------|-------------|-----|-----|
| Low | Low | 37% | 1.00 |
| Moderate | Low | 20% | 1.61 |
| Moderate | Moderate | 14% | 2.00 |
| High | Moderate | 10% | 2.31 |
| High | High | 5% | 3.00 |

---

## Selection Methods

| Method | ISA Reference | When to Use | Procedure |
|--------|--------------|-------------|-----------|
| **Random** | ISA 530.A13 | Large populations, computerised records | Use random number generator; every unit has equal chance |
| **Systematic** | ISA 530.A14 | Sequentially numbered populations | Calculate interval = PV ÷ n; random start, then every k-th unit |
| **MUS / PPS** | ISA 530.A15 | Testing for overstatement; monetary populations | Probability proportional to size; larger items more likely selected |
| **Haphazard** | ISA 530.A16 | Small populations; no structured numbering | Select without conscious bias; NOT truly random |

### Systematic Selection Detail

```
Sampling Interval (k) = Population Value / Sample Size
Random Start = Random number between 1 and k
Selected units: Random Start, Random Start + k, Random Start + 2k, ...
```

---

## Evaluation Framework

### Step 1: Project Misstatements

For each misstatement found in the sample:

```
Projected Misstatement = (Misstatement in sample item / Book value of sample item) × Stratum population value
```

For MUS: each sampling unit represents one interval of TM/CF, so:

```
Projected Misstatement = Sum of (Tainting % × Sampling Interval) for each error
Tainting % = (Book Value - Audit Value) / Book Value × 100
```

### Step 2: Calculate Upper Limit on Misstatement (ULM)

```
ULM = Projected Misstatement + Allowance for Sampling Risk (ASR)
```

### Step 3: Compare to Tolerable Misstatement

| Result | Conclusion |
|--------|-----------|
| ULM < TM | Sample supports that the population is not materially misstated |
| ULM ≥ TM | Sample does NOT support; consider extending procedures, requesting adjustment, or qualifying |

---

## Working Paper Template

When the user invokes `/sampling [area]`, generate the following companion working paper. Replace `[AREA]`, `[REF]`, `[DESCRIPTION]` with the audit area details.

### Output File

Save as: `[Section]/[Ref]-S_Sampling_[Area].md` (e.g., `C_Assets/C6-S_Sampling_Trade_Receivables.md`)

### Template

````markdown
---
ref: [REF]-S
title: Audit Sampling - [DESCRIPTION]
section: [SECTION_FOLDER]
---

# {{company_name}}
## Year End: {{year_end_date}}
## Working Paper: [REF]-S - Audit Sampling: [DESCRIPTION]

| | |
|---|---|
| **Prepared by** | {{prepared_by}} |
| **Date** | [Date] |
| **Reviewed by** | {{reviewed_by}} |
| **Date** | [Date] |

---

### 1. Objective

To determine an appropriate sample size, select sample items, and evaluate results for the testing of **[DESCRIPTION]** in accordance with ISA 530 *Audit Sampling*.

**Related Working Paper:** [REF] - [DESCRIPTION]

---

### 2. Population Definition

| Parameter | Detail |
|-----------|--------|
| **Population description** | [e.g., All trade receivable balances as at year end] |
| **Population source** | [e.g., Aged debtors listing from accounting system] |
| **Population value (PV)** | {{samp_[ref]_population_value}} |
| **Number of items in population** | {{samp_[ref]_population_count}} |
| **Items above materiality (100% test)** | {{samp_[ref]_items_above_pm}} |
| **Remaining population for sampling** | {{samp_[ref]_remaining_population}} |
| **Completeness verified** | [Yes/No — reconciled to TB/GL] |
| **Period covered** | {{audit_period_from}} to {{audit_period_to}} |

---

### 3. Sample Size Calculation

| Parameter | Value | Basis |
|-----------|-------|-------|
| **Tolerable Misstatement (TM)** | {{performance_materiality}} | = Performance Materiality |
| **Assessed Risk of Material Misstatement** | [Low/Moderate/High] | Per A4 Risk Assessment |
| **Inherent Risk** | [Low/Moderate/High] | |
| **Control Risk** | [Low/Moderate/High] | Per B1 ICQ |
| **Risk of Incorrect Acceptance (RIA)** | [X%] | IR × CR matrix |
| **Confidence Factor (CF)** | {{samp_[ref]_confidence_factor}} | Per Poisson table |
| **Expected Misstatement** | {{samp_[ref]_expected_misstatement}} | Based on prior year / nature |

**MUS Calculation:**

```
n = CF × (PV / TM)
n = {{samp_[ref]_confidence_factor}} × ({{samp_[ref]_remaining_population}} / {{performance_materiality}})
n = {{samp_[ref]_sample_size}}
```

**Final sample size: {{samp_[ref]_sample_size}}** items

---

### 4. Selection Method

| Parameter | Detail |
|-----------|--------|
| **Method chosen** | [Random / Systematic / MUS-PPS / Haphazard] |
| **ISA 530 reference** | [A13 / A14 / A15 / A16] |
| **Justification** | [Why this method is appropriate for this population] |
| **Sampling interval (if systematic)** | {{samp_[ref]_sampling_interval}} |
| **Random start (if systematic)** | {{samp_[ref]_random_start}} |

---

### 5. Sample Listing

<!-- SAMPLING_TABLE -->
| # | Item Ref | Description | Amount (RM) | Vouched | Remark | Discrepancy (RM) |
|---|----------|-------------|-------------|---------|--------|------------------|
| 1 | | | | [ ] | | |
| 2 | | | | [ ] | | |
| 3 | | | | [ ] | | |
| 4 | | | | [ ] | | |
| 5 | | | | [ ] | | |
<!-- /SAMPLING_TABLE -->

---

### 6. Evaluation of Results

| Metric | Value |
|--------|-------|
| **Total items tested** | {{samp_[ref]_sample_size}} |
| **Items with no exception** | {{samp_[ref]_no_exception}} |
| **Items with discrepancy** | {{samp_[ref]_with_discrepancy}} |
| **Total misstatement found in sample** | {{samp_[ref]_total_misstatement}} |
| **Projected misstatement** | {{samp_[ref]_projected_misstatement}} |
| **Allowance for sampling risk** | {{samp_[ref]_sampling_risk_allowance}} |
| **Upper Limit on Misstatement (ULM)** | {{samp_[ref]_ulm}} |
| **Tolerable Misstatement (TM)** | {{performance_materiality}} |

**Projection Calculation:**

```
Projected Misstatement = (Total Misstatement / Sample Value) × Population Value
= ({{samp_[ref]_total_misstatement}} / {{samp_[ref]_sample_value}}) × {{samp_[ref]_population_value}}
= {{samp_[ref]_projected_misstatement}}
```

**Result:** ULM [</>] TM → [Sample supports / does not support] that the population is not materially misstated.

---

### 7. Conclusion

Based on the sampling procedures performed in accordance with ISA 530:

- [ ] Sample results support that **[DESCRIPTION]** is not materially misstated
- [ ] Exceptions noted have been followed up and resolved — see remarks above
- [ ] Projected misstatement is below Tolerable Misstatement
- [ ] No systematic or pattern-based errors identified
- [ ] Results communicated to engagement partner

**Overall conclusion:** [State conclusion]

---

### Cross-References

- Main Working Paper: [REF] - [DESCRIPTION]
- Risk Assessment: A4
- Internal Controls: B1
- Materiality: A4 (Planning & Performance Materiality)
- Audit Differences: F6 (if adjustments required)
````

---

## master_data.json Variables

When generating a sampling paper, add these variables to `master_data.json` under the `sampling` category:

```json
{
  "categories": {
    "sampling": { "label": "Audit Sampling", "order": 7 }
  },
  "variables": {
    "samp_[ref]_population_value": { "value": 0, "label": "[Area] - Population Value", "category": "sampling", "format": "currency" },
    "samp_[ref]_population_count": { "value": 0, "label": "[Area] - Population Count", "category": "sampling", "format": "text" },
    "samp_[ref]_items_above_pm": { "value": 0, "label": "[Area] - Items Above PM", "category": "sampling", "format": "text" },
    "samp_[ref]_remaining_population": { "value": 0, "label": "[Area] - Remaining Population", "category": "sampling", "format": "currency" },
    "samp_[ref]_confidence_factor": { "value": 0, "label": "[Area] - Confidence Factor", "category": "sampling", "format": "text" },
    "samp_[ref]_expected_misstatement": { "value": 0, "label": "[Area] - Expected Misstatement", "category": "sampling", "format": "currency" },
    "samp_[ref]_sample_size": { "value": 0, "label": "[Area] - Sample Size", "category": "sampling", "format": "text" },
    "samp_[ref]_sampling_interval": { "value": 0, "label": "[Area] - Sampling Interval", "category": "sampling", "format": "currency" },
    "samp_[ref]_random_start": { "value": 0, "label": "[Area] - Random Start", "category": "sampling", "format": "text" },
    "samp_[ref]_no_exception": { "value": 0, "label": "[Area] - No Exception Count", "category": "sampling", "format": "text" },
    "samp_[ref]_with_discrepancy": { "value": 0, "label": "[Area] - Discrepancy Count", "category": "sampling", "format": "text" },
    "samp_[ref]_total_misstatement": { "value": 0, "label": "[Area] - Total Misstatement", "category": "sampling", "format": "currency" },
    "samp_[ref]_sample_value": { "value": 0, "label": "[Area] - Sample Value Tested", "category": "sampling", "format": "currency" },
    "samp_[ref]_projected_misstatement": { "value": 0, "label": "[Area] - Projected Misstatement", "category": "sampling", "format": "currency" },
    "samp_[ref]_sampling_risk_allowance": { "value": 0, "label": "[Area] - Sampling Risk Allowance", "category": "sampling", "format": "currency" },
    "samp_[ref]_ulm": { "value": 0, "label": "[Area] - Upper Limit on Misstatement", "category": "sampling", "format": "currency" }
  }
}
```

Replace `[ref]` with the lowercase area reference (e.g., `c6`, `d7`, `e1`) and `[Area]` with the area name.

---

## Procedure Checklist Integration

When a sampling paper is generated, the **main working paper** (e.g., C6) should include a procedure linking to the sampling companion:

```markdown
- [ ] Perform audit sampling per ISA 530 — see **[REF]-S** for sample selection and evaluation
```

---

## Guidance for Specific Audit Areas

| Area | Typical Population | Typical Selection Method | Key Assertion |
|------|-------------------|------------------------|---------------|
| C6 Trade Receivables | Aged debtors listing | MUS/PPS or Random | Existence, Valuation |
| C5 Inventories | Stock listing | Systematic or Random | Existence, Valuation |
| D7 Trade Payables | Creditors listing | Random or Haphazard | Completeness |
| E1 Revenue | Sales invoices for the year | Systematic | Occurrence, Accuracy |
| C1 PPE | Fixed asset register | Random | Existence, Accuracy |
| E4 Admin Expenses | Expense vouchers | Systematic or Random | Occurrence, Classification |
