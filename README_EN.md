[English](README_EN.md) | [中文](README.md)

# Evolving Distiller

An evidence-grounded, self-evolving Skill distillation system designed for long-term use.

Evolving Distiller is not a prompt summarizer, and it is not a loose merge of several Skills. It turns continuously arriving knowledge into Skills that are traceable, testable, reversible, and able to evolve under controlled validation.

Core pipeline:

```text
Raw Knowledge
    ↓
Structured Evidence
    ↓
Claims
    ↓
Mental / Operating Models
    ↓
Executable Skill
    ↓
Regression / Challenge / Shadow Tests
    ↓
Runtime Feedback & New Evidence
    ↓
Controlled Evolution
    ↓
New Stable Version
```

## Project Positioning

Evolving Distiller focuses on a problem that is more important than generating a Skill once:

> When new evidence, real-world feedback, and failure cases keep arriving, how can a Skill improve without drifting, overfitting, expanding beyond its evidence, or optimizing away its own safeguards?

The system therefore runs two closed loops:

```text
Distillation Loop
Sources → Evidence → Claims → Models → Instructions → Tests → Stable Skill

Evolution Loop
Delta / Failure → Mutation → Candidate → Gates → Tests → Paired Judges
                                              ↓
                                      Keep or Revert
                                              ↓
                                      Evolution Memory
```

By default, evolution applies to the child Skills produced by the distillation process. Evolving Distiller itself can only enter Meta Evolution when the user explicitly requests it.

## Core Capabilities

### 1. Evidence-Grounded Distillation

Turn people, teams, companies, domain knowledge, interviews, documents, courses, research materials, or existing Skills into executable Skills.

The goal is not to extract only *what was said*, but to identify:

- how beliefs were formed;
- how real decisions were made;
- which failures changed later judgment;
- which methods recur across different contexts;
- which tensions or contradictions are genuine;
- where the cognitive or operational boundaries are;
- which mechanisms deserve to become executable instructions.

### 2. Claim–Evidence Graph

The system maintains a complete traceability chain:

```text
Evidence E → Claim C → Model M → Instruction I → Test T
```

For example:

```text
E023 → C014 → M03 → I018 → T07
```

If new material changes `E023`, the graph can identify which Claims, Models, Instructions, and Tests are affected instead of redistilling the entire Skill.

This turns knowledge updates from full rewrites into something closer to incremental compilation.

Related files:

- `references/claim-evidence-graph.md`
- `scripts/graph_audit.py`

### 3. Delta Distillation

New material does **not** automatically modify the stable Skill.

The system first classifies each meaningful change as:

- `reinforce`: strengthens an existing conclusion;
- `weaken`: lowers confidence or narrows applicability;
- `contradict`: introduces evidence that cannot be safely reconciled;
- `new_candidate`: may justify a new Claim or Model;
- `no_action`: duplicate, decorative, or insufficient to change behavior.

Core principle:

> No cognitive delta, no Skill delta.

Related files:

- `references/delta-distillation.md`
- `scripts/detect_delta.py`

### 4. Regression / Challenge / Shadow Evaluation

Every long-lived Skill can maintain three test layers.

#### Regression

A fixed suite covering core capabilities.

Purpose: prevent a new version from fixing one issue while silently breaking existing behavior.

#### Challenge

Cases derived from real failures, user corrections, and difficult scenarios.

Purpose: verify that the current evolution actually resolves the problem that triggered it.

#### Shadow

Held-out tests that remain hidden from the candidate-authoring process.

Purpose: detect overfitting to known evaluation cases.

Typical Promotion Gate:

```text
Hard Gates = PASS
Regression(candidate) >= Regression(incumbent)
Challenge(candidate)  > Challenge(incumbent)
Shadow(candidate)     >= Shadow(incumbent)
Paired Judges: better > worse
```

If any required gate fails, the incumbent remains stable and the candidate is not promoted.

Related files:

- `references/evaluation-rubric.md`
- `references/regression-suite.md`
- `scripts/suite_gate.py`
- `scripts/pairwise_vote.py`

### 5. Evolution Memory + Mutation Operators

Evolving Distiller remembers failed experiments as well as successful upgrades.

```text
evolution/
├── history.jsonl
├── failures.jsonl
├── patterns.json
└── state.json
```

The system supports controlled Mutation Operators:

| Operator | Meaning |
|---|---|
| PROMOTE | Promote a well-supported weak rule into a core model |
| DEMOTE | Downgrade an under-supported core model into a heuristic |
| SPLIT | Split an oversized model into context-specific models |
| MERGE | Merge highly redundant models |
| WEAKEN | Convert an absolute rule into a conditional rule |
| BOUND | Add an explicit applicability boundary |
| CONTRADICT | Model unresolved conflict as an explicit tension |
| DELETE | Remove unsupported or low-value rules |
| COMPRESS | Reduce redundancy while preserving capability |
| RESTRUCTURE | Change structure without changing core knowledge |

Historical results can reduce the priority of mutation types with high revert rates, helping the system avoid repeating the same class of failed edits.

Related files:

- `references/mutation-operators.md`
- `references/evolution-protocol.md`
- `scripts/evolution_log.py`
- `scripts/evolution_memory.py`

### 6. Immutable Evolution Constitution

One of the biggest risks in a self-evolving system is allowing the optimizer to eventually optimize away its own constraints.

Evolving Distiller therefore defines a set of constitutional invariants that Meta Evolution cannot autonomously remove, including:

1. Do not remove provenance requirements.
2. Do not remove keep / revert behavior.
3. Do not allow the candidate to become its own sole judge.
4. Do not weaken promotion hard gates.
5. Do not directly overwrite the stable version.
6. Do not silently change test standards to improve scores.
7. Do not promote weak inference into fact without new support.
8. Do not delete failure history.
9. Do not expose Shadow Tests to the candidate-authoring process.
10. Require human confirmation for final Meta Evolution promotion.

Related files:

- `references/evolution-constitution.md`
- `references/constitution.json`
- `scripts/constitution_guard.py`

## What Can Be Distilled?

Evolving Distiller is not limited to “personality” or “thinking style” Skills.

```text
Person
→ Cognitive Skill

Team / Company
→ Operating Skill

Books / Interviews / Course Corpus
→ Framework Skill

Research Field
→ Research Skill

Successful Cases
→ Pattern Skill

Failed Cases
→ Anti-pattern Skill

Existing Skill + Feedback
→ Evolved Skill
```

A useful way to think about the project is:

> Evidence-to-Skill Compiler + Skill Evolution Engine

## Usage

### Scenario A: Build a Skill from Source Material

You can provide:

- PDF, Markdown, TXT, interview transcripts, or course scripts;
- notes or knowledge-base exports;
- a collection of URLs or public sources;
- a person, team, company, or domain topic.

Example:

```text
Distill these interviews and articles into a decision Skill that can be maintained over time.
```

The system processes the material as:

```text
Sources
→ Evidence Extraction
→ Claim-Evidence Graph
→ Model Synthesis
→ Child Skill
→ Three-Layer Evaluation
→ Stable Version
```

### Scenario B: Update an Existing Skill with New Evidence

```text
These three interviews are new. Check whether they should change the existing Skill.
```

The system does not rewrite the Skill by default. It runs:

```text
Old Evidence vs New Evidence
→ Delta
→ Impact Graph
→ Candidate Mutation
→ Regression / Challenge / Shadow
→ Keep / Revert
```

### Scenario C: Evolve from a Real Failure

```text
The previous answer clearly violated this Skill's method. Add it as a failure case and repair the Skill.
```

Real failures can enter the Challenge Set and become part of future evolution.

### Scenario D: Evolve Evolving Distiller Itself

This requires an explicit request such as:

```text
Evolve evolving-distiller itself.
```

Meta Evolution additionally enables the Constitution Guard and requires final human approval.

## Directory Structure

```text
evolving-distiller/
├── README.md
├── README_EN.md
├── NOTICE.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── attribution.md
│   ├── child-skill-template.md
│   ├── claim-evidence-graph.md
│   ├── constitution.json
│   ├── delta-distillation.md
│   ├── distillation-protocol.md
│   ├── evaluation-rubric.md
│   ├── evolution-constitution.md
│   ├── evolution-protocol.md
│   ├── mutation-operators.md
│   ├── regression-suite.md
│   └── schemas.md
└── scripts/
    ├── constitution_guard.py
    ├── detect_delta.py
    ├── evidence_audit.py
    ├── evolution_log.py
    ├── evolution_memory.py
    ├── graph_audit.py
    ├── pairwise_vote.py
    ├── self_test.py
    └── suite_gate.py
```

## Installation

### ChatGPT Skills

Package the complete Skill directory as `skill.zip`, then upload it in an environment that supports Skills.

The project already contains the standard Skill entrypoints:

```text
SKILL.md
agents/openai.yaml
```

### Other Compatible Runtimes

The core workflow is intentionally runtime-neutral. In environments that support Skill or Agent Skill directories, place the complete directory in the runtime's designated Skill location.

If a runtime does not support independent sub-agents, script execution, Git, or another required capability, follow the fallback rules in `SKILL.md`. Do not pretend that unavailable capabilities were executed.

## Local Self-Test

The project includes mechanical smoke tests:

```bash
python scripts/self_test.py
```

Current coverage includes:

- Claim–Evidence Graph;
- Delta Distillation;
- Layered Test Gate;
- Evolution Memory + Mutation;
- Evolution Constitution.

For individual tools, refer to the corresponding files in `references/` and each script's command-line parameters.

## Design Principles

This project follows several long-term constraints:

- Evidence first, not Prompt first.
- Model first, not quote first.
- Delta first, not full rewrite first.
- Test before promotion.
- Pairwise comparison instead of relying on a single absolute score.
- Keep / Revert instead of assuming every change is progress.
- Failed experiments are memory.
- Stable and Candidate versions remain strictly separated.
- The Meta optimizer must not autonomously rewrite its own constitution.

## Design Sources and Attribution

This project is an independently redesigned and integrated implementation inspired by the following public open-source projects:

- [alchaincyf/darwin-skill](https://github.com/alchaincyf/darwin-skill)
- [alchaincyf/nuwa-skill](https://github.com/alchaincyf/nuwa-skill)
- [zjjoe2025/cangjie-skill-](https://github.com/zjjoe2025/cangjie-skill-) / upstream [Yeadon8888/cangjie-skill](https://github.com/Yeadon8888/cangjie-skill)

The main design directions absorbed and reworked include validation-gated optimization, paired keep/revert decisions, multi-source cognitive distillation, mental-model extraction, evidence-grounded research records, and explicit treatment of failures, contradictions, and boundaries.

This project does not directly copy the upstream `SKILL.md` files. Their ideas are reorganized into an Evidence-Grounded Distillation + Validation-Gated Evolution dual-loop architecture.

See `references/attribution.md` for details.

## Copyright Notice

The original integration work, workflow design, maintenance documentation, later revisions, and community-maintained versions in this `evolving-distiller` distribution are reserved by the maintainer unless otherwise stated.

Upstream open-source projects and their code, documentation, and design materials remain governed by their original licenses and copyright terms. This project's copyright notice does not replace or restrict rights already granted by those upstream licenses.

See `NOTICE.md` for the full notice.

## Content Factory Skills Community

The maintainer has built a **Content Factory Skills Community** that continuously collects, tests, and improves practical Skills every week, including:

- self-used Skills under continuous iteration;
- publicly available Skills that have been tested and found useful;
- practical versions for content production, research, knowledge bases, automation, and Agent workflows.

Interested users can contact: `deepgpt911`

Current early-stage membership: **RMB 299 / year**.

Pricing rule: **the annual fee increases by RMB 100 for every additional 50 members.**

Pricing, benefits, and update cadence are subject to future announcements by the maintainer.

## Current Status

Evolving Distiller has implemented and locally smoke-tested the following core modules:

```text
Claim–Evidence Graph
Delta Distillation
Regression / Challenge / Shadow
Evolution Memory + Mutation Operators
Immutable Evolution Constitution
```

The most important next step is not to add more rules, but to connect real long-term usage feedback:

```text
User Correction
Runtime Failure
Human Revision
New Evidence
        ↓
Challenge / Evidence Stream
        ↓
Controlled Evolution
```

The long-term goal is for a Skill to become not merely something that is generated once, but something that can keep improving over time through evidence-backed, test-gated evolution.
