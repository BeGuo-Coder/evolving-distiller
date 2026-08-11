#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def read_score(data, suite):
    row = data.get(suite)
    if not isinstance(row, dict):
        raise ValueError(f"missing suite {suite}")
    inc = row.get("incumbent")
    cand = row.get("candidate")
    if not isinstance(inc, (int, float)) or not isinstance(cand, (int, float)):
        raise ValueError(f"{suite}: incumbent/candidate must be numeric")
    return inc, cand


def main():
    p = argparse.ArgumentParser(description="Enforce regression/challenge/shadow promotion gates.")
    p.add_argument("comparison")
    args = p.parse_args()

    try:
        data = json.loads(Path(args.comparison).read_text(encoding="utf-8"))
        reg_i, reg_c = read_score(data, "regression")
        cha_i, cha_c = read_score(data, "challenge")
        sha_i, sha_c = read_score(data, "shadow")
    except Exception as e:
        print(json.dumps({"status": "fail", "reasons": [str(e)]}, indent=2))
        raise SystemExit(1)

    reasons = []
    if data.get("hard_gates") != "pass":
        reasons.append("hard_gates_not_pass")
    if reg_c < reg_i:
        reasons.append("regression_worse")
    require_challenge = data.get("require_challenge_improvement", True)
    if require_challenge and cha_c <= cha_i:
        reasons.append("challenge_not_improved")
    if not require_challenge and cha_c < cha_i:
        reasons.append("challenge_worse")
    if sha_c < sha_i:
        reasons.append("shadow_worse")

    report = {
        "status": "pass" if not reasons else "fail",
        "promotion_gate": "pass" if not reasons else "block",
        "reasons": reasons,
        "deltas": {
            "regression": reg_c - reg_i,
            "challenge": cha_c - cha_i,
            "shadow": sha_c - sha_i,
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not reasons else 1)


if __name__ == "__main__":
    main()
