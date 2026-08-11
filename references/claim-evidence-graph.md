# Claim-Evidence Graph

## Purpose

Use a typed provenance graph so a change in evidence can be traced to the exact claims, models, runtime instructions, and tests that may need review.

The canonical chain is:

```text
E evidence -> C claim -> M model -> I instruction -> T test
```

Safety/runtime rules that are not source-derived may use a `policy` node type and must be explicitly marked as such.

## Node types

- `evidence`: one ledger record such as `E023`.
- `claim`: a concise proposition supported by evidence such as `C014`.
- `model`: a reusable mechanism synthesized from one or more claims such as `M03`.
- `instruction`: an executable child-Skill rule such as `I018`.
- `test`: an evaluation case such as `T07`.
- `policy`: a runtime, safety, or constitutional rule not derived from subject evidence.

## Allowed edge direction

- evidence -> claim: `supports`, `weakens`, `contradicts`
- claim -> model: `supports`, `limits`, `contradicts`
- model -> instruction: `implements`, `limits`
- instruction -> test: `covered_by`
- policy -> instruction: `constrains`
- policy -> test: `covered_by`

Keep the graph acyclic across the primary E->C->M->I->T flow. Contradiction edges may point to claims/models but must not create an executable dependency cycle.

## Grounding rule

Every `instruction` node must have at least one upstream path to an `evidence` node or a `policy` node. Every core `model` must have an upstream evidence path.

A graph that contains an instruction with no evidence/policy ancestry fails release.

## Stable IDs

Never reuse a deleted ID. Preserve IDs across wording edits so delta detection can distinguish modification from replacement.

## Impact analysis

When an evidence or claim node changes, traverse downstream dependencies and review only affected nodes. Example:

```text
E091 changed
-> C014
-> M03
-> I018
-> T07, T11
```

Use:

```text
scripts/graph_audit.py references/provenance/graph.json --impact E091
```

The result is a review set, not an automatic instruction to mutate every downstream node.
