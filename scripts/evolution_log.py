#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

MUTATIONS = {"PROMOTE", "DEMOTE", "SPLIT", "MERGE", "WEAKEN", "BOUND", "CONTRADICT", "DELETE", "COMPRESS", "RESTRUCTURE"}


def split_csv(value):
    if not value:
        return []
    return [x.strip() for x in value.split(",") if x.strip()]


def main():
    p = argparse.ArgumentParser(description="Append one auditable evolution experiment to history JSONL.")
    p.add_argument("history")
    p.add_argument("--candidate-id", required=True)
    p.add_argument("--parent", required=True)
    p.add_argument("--trigger", required=True)
    p.add_argument("--trigger-ids", default="")
    p.add_argument("--hypothesis", required=True)
    p.add_argument("--mutation", required=True)
    p.add_argument("--changes", default="")
    p.add_argument("--decision", choices=["keep", "revert"], required=True)
    p.add_argument("--better", type=int, default=0)
    p.add_argument("--worse", type=int, default=0)
    p.add_argument("--tie", type=int, default=0)
    p.add_argument("--hard-gates", choices=["pass", "fail"], required=True)
    p.add_argument("--suite-gate", choices=["pass", "fail"], required=True)
    args = p.parse_args()

    mutation = args.mutation.upper()
    if mutation not in MUTATIONS:
        raise SystemExit(f"invalid mutation {args.mutation!r}; expected one of {sorted(MUTATIONS)}")

    path = Path(args.history)
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "candidate_id": args.candidate_id,
        "parent": args.parent,
        "trigger": args.trigger,
        "trigger_ids": split_csv(args.trigger_ids),
        "hypothesis": args.hypothesis,
        "mutation": mutation,
        "changes": split_csv(args.changes),
        "votes": {"better": args.better, "worse": args.worse, "tie": args.tie},
        "hard_gates": args.hard_gates,
        "suite_gate": args.suite_gate,
        "decision": args.decision,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps(row, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
