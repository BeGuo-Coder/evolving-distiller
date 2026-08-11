# Delta Distillation

## Goal

Update only what new evidence changes. Most new material should not cause a Skill mutation.

## Step 1: Mechanical delta

Compare old and new evidence ledgers with stable IDs:

```text
scripts/detect_delta.py old.jsonl new.jsonl --graph references/provenance/graph.json
```

The script reports `added`, `removed`, `modified`, and `unchanged` evidence IDs plus downstream impacted graph nodes when a graph is supplied.

## Step 2: Semantic impact review

For each added/modified/removed item, classify its effect:

- `reinforce`: same claim/mechanism with materially stronger support.
- `weaken`: confidence, scope, or authority should decrease.
- `contradict`: evidence conflicts with an existing claim/model and must be preserved.
- `new_candidate`: evidence may support a genuinely new claim/model.
- `no_action`: duplicate, decorative, low-value, or non-executable information.

Do not confuse novelty with impact. A new anecdote that does not alter a claim, boundary, contradiction, confidence, or test is `no_action`.

## Step 3: Minimal review set

Use graph impact traversal. Review affected claims first, then propagate only if the claim actually changes.

Example:

```text
new evidence -> existing claim reinforced -> confidence unchanged -> no instruction edit
```

This is a valid evolution result: record the evidence, update provenance, and do not modify the executable Skill.

## Step 4: Trigger test updates

Add or revise a challenge case when the delta reveals a real failure mode, contradiction, boundary, or transfer condition that current tests do not cover.

Do not add a challenge test merely to encode the exact wording of a new source.
