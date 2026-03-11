---
name: materiality
description: Calculate planning materiality, performance materiality, and trivial threshold for audits
---

# Materiality Assessment

## Materiality Benchmarks

| Entity Type | Benchmark | Typical % |
|-------------|-----------|-----------|
| Trading/Manufacturing | Revenue | 0.5% - 1% |
| Service | Revenue or Total Assets | 1% - 2% |
| Investment Holding | Total Assets or Net Assets | 1% - 2% |
| Loss-making | Total Assets or Revenue | 1% - 2% |
| Non-profit | Total Expenses | 1% - 2% |

## Calculation Framework

### Planning Materiality (PM)
- Select appropriate benchmark based on entity type
- Apply percentage within the typical range
- Consider: entity size, industry norms, user reliance, prior year

### Performance Materiality (PerfM)
- **Range**: 50% - 75% of Planning Materiality
- Use **50-60%** for: first-year audit, higher risk, history of adjustments
- Use **65-75%** for: recurring audit, lower risk, few prior adjustments

### Trivial Threshold (TT)
- **Range**: 3% - 5% of Planning Materiality
- Misstatements below this are clearly trivial and need not be accumulated

## Calculation Template

```
MATERIALITY CALCULATION

Client: [Name]
Year End: [Date]

Selected Benchmark: [Revenue / Total Assets / etc.]
Benchmark Amount: RM [Amount]

Planning Materiality:
  [Benchmark] x [%] = RM [Amount]

Performance Materiality:
  PM x [%] = RM [Amount]

Trivial Threshold:
  PM x [%] = RM [Amount]

Justification:
[Why this benchmark and percentage were selected]
```

## Revision Triggers

Reassess materiality if during the audit:
- Significant new information becomes available
- Actual results differ materially from estimates used at planning
- Significant misstatements are identified
- Changes in circumstances (e.g., going concern issues)

---

## Performance Materiality Justification Framework (ISA 320)

### PM% Selection Guide

| PM% Range | When to Use | Risk Profile |
|-----------|-------------|-------------|
| **50-60%** of PM | First-year engagement; history of many audit adjustments; weak internal controls; complex entity; significant estimation uncertainty; prior fraud indicators | **Higher risk** |
| **60-70%** of PM | Recurring engagement with some adjustments PY; moderate controls; some complexity | **Moderate risk** |
| **70-75%** of PM | Recurring engagement; few/no PY adjustments; reasonable controls; straightforward entity | **Lower risk** |

### Factors to Document

When selecting the PM percentage, document assessment of ALL these factors:

| Factor | Assessment | Impact on PM% |
|--------|-----------|---------------|
| Nature of entity (complexity, size) | [Simple/Moderate/Complex] | [Lower/Higher PM%] |
| First year vs recurring engagement | [First/Recurring] | [Lower for first year] |
| Prior year audit adjustments | [None/Few/Many] | [Lower if many] |
| Control environment assessment | [Weak/Moderate/Strong] | [Lower if weak] |
| Risk of material misstatement | [Low/Moderate/High] | [Lower if high] |
| Understanding of the entity | [Limited/Good/Excellent] | [Lower if limited] |
| Volume and nature of transactions | [Low/Moderate/High] | [Lower if high volume] |

### Documentation Template

```
Performance Materiality: PM x [%] = RM [Amount]

Selected percentage: [X]%

Justification:
- [Factor 1]: [Assessment] — supports [higher/lower] PM%
- [Factor 2]: [Assessment] — supports [higher/lower] PM%
- [Factor 3]: [Assessment] — supports [higher/lower] PM%

Overall assessment: [X]% is appropriate because [summary rationale]
```

---

## Qualitative Materiality Considerations

### Lower Materiality Thresholds

Certain items may be material at amounts BELOW the calculated planning materiality:

| Item | Why Lower Threshold | Typical Approach |
|------|-------------------|-----------------|
| Related party transactions | User sensitivity; regulatory focus; potential non-arm's length | Apply 50% of PM or lower |
| Director remuneration | Disclosure requirement; user interest | Test 100% regardless of amount |
| Regulatory breaches (fines, penalties) | May be material regardless of amount | Qualitative assessment |
| Going concern items | Small amounts can trigger GC doubt | Qualitative assessment |
| Fraud-related items | Any fraud may be material | Qualitative assessment |
| Illegal acts | May be material regardless of amount | Qualitative assessment |
| Tax non-compliance | Penalties; statutory obligation | Apply lower threshold |
| Prior period errors | Indicates control weakness | Test if identified |

### Qualitative Factors in Benchmark Selection

Consider qualitative factors when selecting the materiality benchmark:

| Factor | Impact on Selection |
|--------|-------------------|
| Entity is loss-making | Avoid using profit as benchmark; use revenue or total assets |
| Volatile earnings | Use a more stable benchmark (total assets, revenue) |
| Entity is approaching breakeven | Small misstatements could change profit/loss; consider lower PM |
| Regulatory capital requirements | Consider regulatory thresholds |
| Debt covenants | Consider covenant compliance thresholds |
| User reliance on specific metrics | Align benchmark with what users focus on |

---

## Materiality Revision Tracking (ISA 320.12-13)

### When to Revise Materiality

Materiality MUST be revised if during the audit:
- Significant new information becomes available that would have affected the original calculation
- Actual financial results differ materially from estimates used at planning stage
- Significant misstatements are identified (may indicate more exist)
- Changes in circumstances (e.g., going concern issues emerge)

### Revision Template

| | Original | Revised | Change |
|---|----------|---------|--------|
| **Date** | [Planning date] | [Revision date] | |
| **Benchmark** | [Original benchmark] | [Revised benchmark] | [Same/Changed] |
| **Benchmark amount** | RM [X] | RM [X] | RM [X] |
| **PM %** | [X]% | [X]% | [Same/Changed] |
| **Planning Materiality** | RM [X] | RM [X] | RM [X] |
| **Performance Materiality** | RM [X] | RM [X] | RM [X] |
| **Trivial Threshold** | RM [X] | RM [X] | RM [X] |

### Reason for Revision
[Document why materiality was revised]

### Impact on Audit Procedures
| Impact Area | Action Required |
|------------|----------------|
| Sample sizes | [Increase/Decrease/No change] |
| Scope of testing | [Expand/Contract/No change] |
| Previously completed procedures | [Sufficient/Need additional work] |
| Audit differences evaluation | [Re-evaluate against revised materiality] |
