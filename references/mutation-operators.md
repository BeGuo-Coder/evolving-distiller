# Mutation Operators

Use a bounded mutation vocabulary so evolution experiments are comparable and evolution memory can learn which changes work.

| Operator | Use when | Typical risk |
|---|---|---|
| PROMOTE | Repeated evidence makes a tentative heuristic core | Overstating confidence |
| DEMOTE | A core rule has weak, narrow, or conflicting evidence | Losing useful default behavior |
| SPLIT | One model behaves differently across contexts | Complexity growth |
| MERGE | Two models are redundant and behave the same | Erasing meaningful distinctions |
| WEAKEN | Absolute wording exceeds evidence strength | Becoming too vague |
| BOUND | A rule needs an explicit applicability condition | Over-constraining transfer |
| CONTRADICT | New evidence reveals a real unresolved tension | False balance if evidence is asymmetric |
| DELETE | A rule adds no tested value or is unsupported | Removing hidden dependencies |
| COMPRESS | Runtime instructions contain redundant detail | Losing execution-critical nuance |
| RESTRUCTURE | Workflow order/shape blocks reliable execution | Cosmetic rewrite disguised as improvement |

## Selection rule

1. Identify the failure/delta.
2. List one to three plausible operators.
3. Check `evolution/patterns.json` for prior results.
4. Prefer historically useful operators for similar triggers, but require current evidence and tests.
5. Generate separate candidates rather than combining unrelated operators.

## Tournament rule

For high-impact changes, create up to three candidates with different operators. First eliminate candidates that fail constitution or hard gates, then use layered tests and paired judges against the incumbent. Promote only the winning candidate that satisfies all promotion rules.

## Negative knowledge

A reverted mutation remains valuable. Keep it in `history.jsonl` and `failures.jsonl`. Repeated reverts should reduce future priority, not create a permanent ban unless the failure is constitutional.
