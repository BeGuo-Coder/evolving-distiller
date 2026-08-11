# Schemas

## Evidence ledger: `references/research/02-evidence.jsonl`

One JSON object per line:

```json
{
  "id": "E001",
  "claim": "Concise extracted evidence statement",
  "evidence_class": "belief_formation",
  "support": "direct",
  "source_id": "S01",
  "locator": "chapter 3 / 00:42:10 / URL section",
  "context": "When this evidence applies",
  "counterevidence": ["E014"],
  "confidence": "high",
  "notes": "Short synthesis note"
}
```

Allowed `evidence_class`: `belief_formation`, `decision`, `failure_correction`, `contradiction`, `boundary`, `reasoning_habit`, `generic_opinion`.

Allowed `support`: `direct`, `supported_inference`, `weak_inference`.

Allowed `confidence`: `high`, `medium`, `low`.

## Provenance graph: `references/provenance/graph.json`

```json
{
  "nodes": [
    {"id": "E001", "type": "evidence", "label": "..."},
    {"id": "C001", "type": "claim", "label": "..."},
    {"id": "M01", "type": "model", "label": "...", "core": true},
    {"id": "I01", "type": "instruction", "label": "..."},
    {"id": "T01", "type": "test", "label": "..."}
  ],
  "edges": [
    {"from": "E001", "to": "C001", "relation": "supports"},
    {"from": "C001", "to": "M01", "relation": "supports"},
    {"from": "M01", "to": "I01", "relation": "implements"},
    {"from": "I01", "to": "T01", "relation": "covered_by"}
  ]
}
```

Node types: `evidence`, `claim`, `model`, `instruction`, `test`, `policy`.

## Delta review

```json
{
  "evidence_id": "E091",
  "change": "added",
  "impact": "contradict",
  "target_ids": ["C014", "M03"],
  "reason": "New first-party evidence conflicts with the prior universal claim"
}
```

`impact`: `reinforce`, `weaken`, `contradict`, `new_candidate`, `no_action`.

## Test case

Use the same case schema in `tests/regression.json`, `tests/challenge.json`, and `tests/shadow.json`:

```json
[
  {
    "id": "T01",
    "family": "known_evidence",
    "prompt": "...",
    "expected": "Grounded behavior to preserve",
    "must_not": "Known failure or overclaim",
    "evidence_ids": ["E001", "E004"]
  }
]
```

## Three-suite comparison summary

```json
{
  "hard_gates": "pass",
  "regression": {"incumbent": 8, "candidate": 8},
  "challenge": {"incumbent": 4, "candidate": 5},
  "shadow": {"incumbent": 6, "candidate": 6},
  "require_challenge_improvement": true
}
```

Scores can be pass counts or another consistent monotonic metric. Use the same metric for incumbent and candidate within each suite.

## Paired judge vote

```json
{
  "judge": "J1",
  "verdict": "better",
  "margin": "slight",
  "reason": "Candidate fixes the boundary failure without regression"
}
```

`verdict`: `better`, `worse`, `tie`.

## Evolution history: `evolution/history.jsonl`

```json
{
  "candidate_id": "v1.2-c1",
  "parent": "v1.1",
  "trigger": "challenge_failure",
  "trigger_ids": ["T14"],
  "hypothesis": "...",
  "mutation": "BOUND",
  "changes": ["SKILL.md"],
  "votes": {"better": 2, "worse": 1, "tie": 0},
  "hard_gates": "pass",
  "suite_gate": "pass",
  "decision": "keep",
  "timestamp": "2026-08-11T12:00:00Z"
}
```

## Evolution memory aggregates

`patterns.json` is derived from history and groups experiments by mutation and trigger with attempts, keeps, reverts, and keep rate.

`failures.jsonl` is derived from history and contains reverted experiments.

`state.json` records the latest kept candidate, experiment counters, and rebuild timestamp.
