# Evaluation Rubric

Use absolute scores for triage only. Use layered test gates plus paired comparisons for promotion.

## Quality dimensions

| Dimension | Weight | Question |
|---|---:|---|
| Evidence grounding | 20 | Are executable claims traceable through the graph to evidence or explicit policy? |
| Cognitive/operating fidelity | 15 | Does the Skill preserve real mechanisms instead of generic advice? |
| Generativity | 15 | Can the model transfer to new cases? |
| Decisions and corrections | 10 | Are real choices, failures, and updates represented? |
| Contradiction retention | 10 | Are temporal/contextual/value tensions preserved? |
| Boundaries and honesty | 10 | Does the Skill label uncertainty and scope? |
| Usability and workflow | 10 | Can another model execute it reliably? |
| Source transparency | 5 | Is provenance compact and inspectable? |
| Anti-drift safeguards | 5 | Are identity limits, gates, and rollback explicit? |

## Hard gates

A release candidate fails regardless of score if any condition holds:

- major unsupported executable claim,
- provenance graph fails audit,
- missing boundary behavior,
- contradiction evidence deleted without justification,
- any required test suite missing,
- deceptive identity claim,
- full copyrighted corpus embedded in the Skill,
- autonomous promotion without comparison record,
- constitution guard failure for meta evolution.

## Three test suites

### Regression

Stable tests for capabilities already earned. Keep these cases relatively fixed. Candidate result must be at least as good as incumbent.

### Challenge

Real failures, difficult edge cases, and newly discovered weaknesses. When an evolution is intended to fix a challenge, candidate result must improve over incumbent on the relevant challenge set.

Append real failure cases; do not rewrite old challenge cases merely to favor a candidate.

### Shadow

Withheld transfer/adversarial cases. The candidate author must not see their contents during mutation design. Candidate result must be at least as good as incumbent.

Shadow cases should be refreshed by a human or independent evaluator when they become exposed.

## Required case families

Across the three suites cover:

1. known evidence,
2. transfer/generativity,
3. boundary honesty,
4. contradiction/tension,
5. adversarial ambiguity.

## Promotion gate

Use `scripts/suite_gate.py` with a comparison summary. Promotion requires:

- hard gates pass,
- regression candidate >= incumbent,
- challenge candidate > incumbent for weakness-fixing evolution,
- shadow candidate >= incumbent.

A suite gate is necessary but not sufficient; paired judge majority is also required.
