# Evolution Protocol

## Evolution levels

### Level 1: Child Skill

Default. Improve a generated Skill using new evidence, real failures, or user feedback.

### Level 2: Meta Skill

Only when the user explicitly requests improvement of the distiller itself. Keep the stable incumbent untouched, create a candidate copy, snapshot the constitution, run meta regression plus layered tests, and require human approval before replacement.

## Candidate discipline

Each experiment must state:

- trigger,
- impacted graph nodes,
- one explicit hypothesis,
- one primary mutation operator,
- expected test improvement,
- risks.

Do not combine unrelated mutations in one candidate.

## Candidate tournament

For high-impact problems, create up to three candidates with different mutation operators.

1. constitution/hard-gate elimination,
2. regression/challenge/shadow gate,
3. paired comparison against incumbent,
4. choose the strongest passing candidate.

Do not run a large open-ended search. Small bounded tournaments preserve interpretability.

## Paired evaluation

For each judge:

1. present incumbent and candidate in randomized A/B order,
2. provide identical evidence constraints and test outputs,
3. ask which version better satisfies the rubric,
4. return `better`, `worse`, or `tie`, plus reason and margin.

Use an odd number of judges: 3 by default, 5 for close/high-impact changes.

Decision rule:

- all mechanical gates pass,
- better votes > worse votes,
- then candidate may be kept.

Otherwise keep incumbent. Ties do not count as improvement.

## Evolution memory update

Log all experiments, including reverted ones. Record the mutation operator and trigger family. Then rebuild aggregate memory from history using `scripts/evolution_memory.py`.

Use memory as a prior, not as proof. A historically successful mutation can still fail current evidence/tests.

## Stop conditions

Stop after two consecutive non-winning candidates, when gains are cosmetic, when evidence cannot resolve the weakness, when scope expands beyond purpose, or at a user checkpoint.
