---
name: evolving-distiller
description: Evidence-grounded Skill distillation and validation-gated evolution for turning people, teams, domains, document sets, interviews, notes, URLs, or existing Skills into reusable cognitive or operating Skills. Use when the user asks to distill reasoning or methods, merge source material into a Skill, update a distilled Skill from new evidence or feedback, detect knowledge deltas, trace claims to evidence, run regression/challenge/shadow evaluations, choose evolution mutations, or evolve a Skill through controlled keep/revert experiments with audit history and constitutional safeguards.
---

# Evolving Distiller

Compile raw knowledge into an evidence-grounded child Skill, then improve that Skill through controlled experiments without losing provenance, prior capability, or safety invariants.

Treat the system as two loops:

1. Distillation: sources -> evidence -> claims -> models -> instructions -> tests -> stable Skill.
2. Evolution: delta/failure -> mutation candidates -> gated evaluation -> keep/revert -> evolution memory.

Default to evolving the generated child Skill. Evolve this meta-skill only when the user explicitly asks to improve the distiller itself.

## Non-negotiable principles

- Distill mechanisms, not memorable wording.
- Trace executable instructions through claims and models back to evidence.
- Preserve contradictions instead of inventing reconciliation.
- Keep extraction, synthesis, candidate authorship, and certification separated when possible.
- Use absolute scores only for diagnosis. Use paired comparison and test gates for promotion.
- Prefer first-party evidence. Label inference strength explicitly.
- Do not claim to impersonate a real person or infer private beliefs as facts.
- Keep raw copyrighted corpora outside the final Skill package.
- Do not change a stable Skill merely because wording could be prettier.
- Never bypass the Evolution Constitution during autonomous evolution.

## Phase 0: Route the request

Choose one primary mode.

| Mode | Trigger | Action |
|---|---|---|
| Local distillation | Files, transcripts, notes, exports, books, interviews | Use supplied material as anchor evidence |
| Research distillation | Subject/domain but no material | Build a source plan, research, then distill |
| Hybrid distillation | Subject plus partial material | Use local evidence first and research only gaps |
| Child evolution | Existing Skill plus feedback, failures, or new evidence | Load stable state and enter Phase 5 |
| Meta evolution | Explicit request to improve this distiller | Clone incumbent, protect constitution, run meta regression, require human promotion |

Use safe defaults when details are missing. Default focus is comprehensive. Default deliverable is a complete child Skill with provenance graph, layered tests, evaluation report, and evolution state.

If neither usable evidence nor a research path exists, produce a provisional scaffold and evidence acquisition plan. Do not fabricate a finished evidence-grounded Skill.

## Phase 1: Build structured evidence

Read `references/distillation-protocol.md` and `references/schemas.md`.

Create or update this child structure:

```text
<child-skill>/
├── SKILL.md
├── references/
│   ├── research/
│   │   ├── 01-sources.md
│   │   ├── 02-evidence.jsonl
│   │   ├── 03-contradictions.md
│   │   └── 04-synthesis-notes.md
│   └── provenance/
│       └── graph.json
├── tests/
│   ├── regression.json
│   ├── challenge.json
│   └── shadow.json
├── EVAL.md
└── evolution/
    ├── history.jsonl
    ├── failures.jsonl
    ├── patterns.json
    └── state.json
```

Prioritize evidence about belief formation, real decisions, admitted failures, reversals, contradictions, boundaries, repeated reasoning habits, and mechanisms that recur across contexts.

Run `scripts/evidence_audit.py` on the evidence ledger when local execution is available.

## Phase 2: Build the Claim-Evidence Graph

Read `references/claim-evidence-graph.md`.

Represent provenance as typed nodes and edges:

```text
Evidence E -> Claim C -> Model M -> Instruction I -> Test T
```

Every executable instruction must have a downstream path to at least one evidence node unless it is an explicit runtime/safety rule. Every core model must trace to claims, and claims must trace to evidence.

Use stable IDs. Do not recycle IDs after deletion.

Run `scripts/graph_audit.py <graph.json>` before release. Use `--impact <ID>` to find downstream nodes affected by changed evidence or claims.

## Phase 3: Synthesize the child Skill

Use six independent lenses when possible:

1. source curator,
2. belief/decision extractor,
3. failure/contradiction extractor,
4. mental-model extractor,
5. boundary skeptic,
6. synthesizer.

If independent agents are unavailable, use separated sequential passes and record `non_independent` in `EVAL.md`.

Promote a candidate model only when it is sufficiently recurrent, generative on new problems, and distinctive rather than generic. Keep 3-7 core models by default.

Read `references/child-skill-template.md` and assemble a compact control plane. Put detailed evidence in references.

## Phase 4: Establish layered evaluation

Read `references/evaluation-rubric.md`.

Maintain three suites:

- `regression.json`: stable cases that must never get worse.
- `challenge.json`: real failures and difficult cases that should improve over time.
- `shadow.json`: withheld cases not shown to the candidate author during optimization.

Create at least one case each for known evidence, transfer, boundary honesty, contradiction handling, and adversarial ambiguity across the suites.

Hard release gates:

- no major executable claim without evidence or explicit inference label,
- provenance graph passes audit,
- boundary behavior exists,
- supported contradictions remain represented,
- all three test files exist,
- no deceptive identity claim,
- no raw full-text corpus bundled,
- autonomous promotion has a comparison record.

## Phase 5: Delta Distillation

Read `references/delta-distillation.md` before changing a stable Skill from new material.

Compare the previous and current evidence states. Run:

```text
scripts/detect_delta.py OLD_EVIDENCE NEW_EVIDENCE [--graph GRAPH]
```

Classify meaningful changes as:

- reinforce: strengthens an existing claim/model,
- weaken: reduces confidence or scope,
- contradict: introduces unresolved counterevidence,
- new_candidate: may justify a new claim/model,
- no_action: duplicate, decorative, or non-executable information.

Default to `no_action` unless the delta changes a claim, confidence, boundary, contradiction, or evaluation case.

Use graph impact traversal to identify exactly which claims, models, instructions, and tests need review. Do not re-distill unaffected parts.

## Phase 6: Choose mutation candidates

Read `references/mutation-operators.md` and current `evolution/patterns.json` if present.

Select mutations from a bounded operator set such as PROMOTE, DEMOTE, SPLIT, MERGE, WEAKEN, BOUND, CONTRADICT, DELETE, COMPRESS, or RESTRUCTURE.

Prefer mutations with a good historical success rate for the same failure type. Penalize mutations that repeatedly reverted. Do not ban a mutation solely from small samples.

For important changes, generate up to three coherent candidates using different mutation operators. Avoid bundles of unrelated edits.

## Phase 7: Validation-gated evolution

Read `references/evolution-protocol.md`.

For each candidate:

```text
trigger -> hypothesis -> mutation -> candidate -> constitution/hard gates -> layered tests -> paired judges -> keep/revert -> log -> rebuild memory
```

Use 3 independent paired judges by default, 5 for close or high-impact changes. Each judge compares incumbent and candidate in the same call with randomized A/B order and returns `better`, `worse`, or `tie` with a reason.

Promotion requires all conditions:

1. hard gates pass,
2. constitution guard passes,
3. regression candidate result >= incumbent,
4. challenge candidate result > incumbent for an evolution intended to fix a known weakness,
5. shadow candidate result >= incumbent,
6. paired `better` votes exceed `worse` votes,
7. evidence coverage does not decrease without explicit justification.

Use `scripts/suite_gate.py` for the three-suite mechanical gate and `scripts/pairwise_vote.py` for paired vote aggregation.

A tie is not an improvement. Keep the incumbent.

Log every candidate, including reverted candidates, using `scripts/evolution_log.py`. Then rebuild evolution memory with `scripts/evolution_memory.py`.

Stop when two consecutive candidates fail, gains are cosmetic, evidence is insufficient, scope begins expanding, or the user requests a checkpoint.

## Phase 8: Evolution Memory

Evolution history is training data for future mutations, not just an audit trail.

Maintain:

```text
evolution/history.jsonl   all experiments
evolution/failures.jsonl  reverted experiments
evolution/patterns.json   mutation statistics and failure associations
evolution/state.json      current stable version and counters
```

Do not delete failed experiments. Use them to avoid repeating unproductive mutation patterns.

Rebuild deterministic memory from history rather than manually editing aggregate files.

## Phase 9: Evolution Constitution

Read `references/evolution-constitution.md` and `references/constitution.json`.

For meta evolution, snapshot protected files from the stable incumbent before creating a candidate:

```text
scripts/constitution_guard.py snapshot STABLE_SKILL MANIFEST
```

After candidate editing, run the stable incumbent copy of the guard:

```text
scripts/constitution_guard.py check CANDIDATE_SKILL MANIFEST
```

Autonomous evolution must not change protected constitutional files or invariants. A constitutional amendment is a separate human-directed operation, never part of the autonomous optimization loop.

## Phase 10: Human checkpoint and delivery

Before declaring a materially evolved Skill final, report:

- trigger and delta,
- impacted graph nodes,
- chosen mutation and hypothesis,
- test-suite results,
- paired vote result,
- hard-gate and constitution status,
- what changed and what remains uncertain.

For meta evolution, require explicit human approval before replacing the stable version.

Deliver the complete Skill package, not just a rewritten `SKILL.md`.

## Failure handling

| Failure | First response | Fallback |
|---|---|---|
| Source unavailable | Mark the gap | Lower confidence; never invent |
| Conflicting sources | Preserve both | Add contradiction node and tests |
| Sparse first-party evidence | Narrow claims | Produce provisional low-confidence model |
| Graph has dangling nodes | Block release | Repair or delete ungrounded downstream nodes |
| Delta is mostly duplicate | Choose no_action | Do not mutate stable Skill |
| Candidate overfits challenge set | Reject | Check shadow suite and revert |
| Regression worsens | Reject | Form a narrower mutation |
| Shadow worsens | Reject | Treat as overfitting or hidden drift |
| Candidate fails paired vote | Revert | Log negative result |
| Mutation repeatedly fails | Lower priority | Try another operator or gather evidence |
| Constitution changes autonomously | Block promotion | Restore incumbent and require explicit amendment flow |
| Legacy Skill lacks evidence/graph | Import as provisional | Reconstruct evidence and tests before autonomous evolution |

## Anti-patterns

Do not:

- merge source workflows verbatim into one giant prompt,
- let synthesis invent evidence,
- allow instructions with no provenance path,
- rewrite all models because one source changed,
- treat every new source as a reason to update,
- optimize against challenge tests while exposing shadow tests to the candidate author,
- use a single absolute score to justify promotion,
- let the candidate author be the only evaluator,
- erase contradictions for persona consistency,
- delete reverted experiments,
- let autonomous meta evolution modify its constitution or promotion gates,
- promote a meta candidate without explicit human approval.

## Bundled resources

- `references/distillation-protocol.md`: evidence extraction and synthesis.
- `references/claim-evidence-graph.md`: typed provenance graph and impact analysis.
- `references/delta-distillation.md`: incremental evidence change protocol.
- `references/evaluation-rubric.md`: quality rubric, hard gates, and three-suite evaluation.
- `references/evolution-protocol.md`: candidate tournament, keep/revert loop, and memory update.
- `references/mutation-operators.md`: bounded mutation library.
- `references/evolution-constitution.md`: immutable autonomous-evolution rules.
- `references/constitution.json`: machine-readable constitutional invariants and protected paths.
- `references/schemas.md`: machine-readable record formats.
- `references/child-skill-template.md`: child Skill scaffold.
- `references/regression-suite.md`: meta-skill regression scenarios.
- `references/attribution.md`: design provenance and licenses.
- `scripts/evidence_audit.py`: validate evidence ledgers.
- `scripts/graph_audit.py`: validate provenance graph and trace impact.
- `scripts/detect_delta.py`: compute evidence deltas and impacted nodes.
- `scripts/suite_gate.py`: enforce regression/challenge/shadow promotion gates.
- `scripts/pairwise_vote.py`: aggregate paired judge votes.
- `scripts/evolution_log.py`: append auditable experiments.
- `scripts/evolution_memory.py`: rebuild negative and positive evolution memory.
- `scripts/constitution_guard.py`: snapshot/check protected constitutional files.
- `scripts/self_test.py`: deterministic smoke tests for bundled scripts.

## Copyright and community notice

Preserve `NOTICE.md` and `references/attribution.md` when redistributing this Skill. Do not remove upstream attribution or imply that downstream copyright terms override upstream open-source licenses.

For maintainer, community, contact, and membership information, read `NOTICE.md`.
