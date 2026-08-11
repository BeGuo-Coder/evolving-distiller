#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

REQ = {"id", "claim", "evidence_class", "support", "source_id", "confidence"}
CLASSES = {"belief_formation", "decision", "failure_correction", "contradiction", "boundary", "reasoning_habit", "generic_opinion"}
SUPPORT = {"direct", "supported_inference", "weak_inference"}
CONF = {"high", "medium", "low"}


def main():
    p = argparse.ArgumentParser(description="Audit an evidence JSONL ledger.")
    p.add_argument("ledger")
    args = p.parse_args()
    path = Path(args.ledger)
    errors = []
    seen = set()
    count = 0
    direct = 0
    with_locator = 0
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        count += 1
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as e:
            errors.append(f"line {n}: invalid JSON: {e}")
            continue
        missing = REQ - set(row)
        if missing:
            errors.append(f"line {n}: missing {sorted(missing)}")
        rid = row.get("id")
        if rid in seen:
            errors.append(f"line {n}: duplicate id {rid}")
        seen.add(rid)
        if row.get("evidence_class") not in CLASSES:
            errors.append(f"line {n}: invalid evidence_class")
        if row.get("support") not in SUPPORT:
            errors.append(f"line {n}: invalid support")
        if row.get("confidence") not in CONF:
            errors.append(f"line {n}: invalid confidence")
        if row.get("support") == "direct":
            direct += 1
        if row.get("locator"):
            with_locator += 1
    report = {
        "records": count,
        "direct_ratio": round(direct / count, 3) if count else 0,
        "locator_ratio": round(with_locator / count, 3) if count else 0,
        "errors": errors,
        "status": "pass" if count and not errors else "fail",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["status"] == "pass" else 1)


if __name__ == "__main__":
    main()
