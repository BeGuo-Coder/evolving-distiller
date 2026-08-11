# Evolution Constitution

## Purpose

Keep the autonomous optimizer from optimizing away the rules that make its own evidence and evaluation trustworthy.

The machine-readable authority is `references/constitution.json`. This document explains the intent.

## Immutable invariants during autonomous evolution

1. Provenance cannot be removed as a release requirement.
2. Rollback/keep-revert capability cannot be removed.
3. Candidate authorship cannot become the only judge.
4. Hard gates cannot be weakened or bypassed.
5. Stable versions cannot be silently replaced.
6. Test standards cannot be changed merely to make a candidate pass.
7. Weak inference cannot be promoted to fact without stronger evidence.
8. Reverted/failed experiment history cannot be deleted to improve apparent success rate.
9. Shadow tests must remain hidden from the candidate author during optimization.
10. Meta-skill promotion requires explicit human approval.

## Protected files

`references/constitution.json` defines the protected path set. During meta evolution, snapshot these files from the stable incumbent before editing the candidate, and check the candidate against that external manifest afterward.

Run the guard from the stable incumbent, not from the candidate.

## Constitutional amendment

Changing the constitution is not an evolution candidate. It is a separate human-directed governance action:

1. user explicitly requests a constitutional change,
2. explain the invariant being changed and the new failure modes introduced,
3. edit the stable constitution outside the autonomous loop,
4. create a new baseline manifest,
5. only then resume autonomous evolution.

Never let an autonomous candidate amend the constitution that judges that same candidate.
