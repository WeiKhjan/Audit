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
