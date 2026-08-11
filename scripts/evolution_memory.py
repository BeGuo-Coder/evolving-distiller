#!/usr/bin/env python3
import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def load_history(path):
    rows = []
    for n, raw in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as e:
            raise ValueError(f"line {n}: invalid JSON: {e}")
        if row.get("decision") not in {"keep", "revert"}:
            raise ValueError(f"line {n}: invalid decision")
        rows.append(row)
    return rows


def aggregate(rows, key):
    stats = defaultdict(lambda: {"attempts": 0, "keeps": 0, "reverts": 0})
    for row in rows:
        value = row.get(key) or "unknown"
        item = stats[value]
        item["attempts"] += 1
        if row["decision"] == "keep":
            item["keeps"] += 1
        else:
            item["reverts"] += 1
    out = {}
    for value, item in sorted(stats.items()):
        attempts = item["attempts"]
        item["keep_rate"] = round(item["keeps"] / attempts, 3) if attempts else 0.0
        if attempts >= 3 and item["keep_rate"] >= 0.67:
            item["prior"] = "favored"
        elif attempts >= 3 and item["keep_rate"] <= 0.33:
            item["prior"] = "discouraged"
        else:
            item["prior"] = "insufficient_or_mixed"
        out[value] = item
    return out


def main():
    p = argparse.ArgumentParser(description="Rebuild deterministic evolution memory from history JSONL.")
    p.add_argument("history")
    p.add_argument("output_dir")
    args = p.parse_args()

    rows = load_history(args.history)
    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    failures = [row for row in rows if row.get("decision") == "revert"]
    patterns = {
        "version": 1,
        "experiments": len(rows),
        "by_mutation": aggregate(rows, "mutation"),
        "by_trigger": aggregate(rows, "trigger"),
        "note": "Historical priors guide candidate selection but never override current evidence and tests."
    }
    latest_kept = None
    for row in rows:
        if row.get("decision") == "keep":
            latest_kept = row.get("candidate_id")
    state = {
        "version": 1,
        "experiments": len(rows),
        "kept": len(rows) - len(failures),
        "reverted": len(failures),
        "latest_kept_candidate": latest_kept,
        "rebuilt_at": datetime.now(timezone.utc).isoformat(),
    }

    (outdir / "failures.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in failures),
        encoding="utf-8",
    )
    (outdir / "patterns.json").write_text(json.dumps(patterns, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (outdir / "state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "pass", "patterns": patterns, "state": state}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
