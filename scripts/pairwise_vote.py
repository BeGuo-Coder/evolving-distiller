#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

VALID = {"better", "worse", "tie"}


def main():
    p = argparse.ArgumentParser(description="Aggregate paired judge votes from a JSON array or JSONL file.")
    p.add_argument("votes")
    args = p.parse_args()
    text = Path(args.votes).read_text(encoding="utf-8").strip()
    if not text:
        raise SystemExit("empty vote file")
    if text.startswith("["):
        rows = json.loads(text)
    else:
        rows = [json.loads(line) for line in text.splitlines() if line.strip()]
    if not isinstance(rows, list) or not rows:
        raise SystemExit("vote file must contain at least one vote")

    counts = {k: 0 for k in VALID}
    judges = set()
    for i, row in enumerate(rows, 1):
        verdict = row.get("verdict")
        if verdict not in VALID:
            raise SystemExit(f"vote {i}: invalid verdict {verdict!r}")
        judge = row.get("judge")
        if not judge:
            raise SystemExit(f"vote {i}: missing judge")
        if judge in judges:
            raise SystemExit(f"vote {i}: duplicate judge {judge!r}")
        judges.add(judge)
        counts[verdict] += 1

    warnings = []
    if len(rows) % 2 == 0:
        warnings.append("even judge count; use an odd number for decisive comparisons")
    decision = "keep_candidate" if counts["better"] > counts["worse"] else "keep_incumbent"
    print(json.dumps({"counts": counts, "judges": len(rows), "decision": decision, "warnings": warnings}, indent=2))


if __name__ == "__main__":
    main()
