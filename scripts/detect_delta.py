#!/usr/bin/env python3
import argparse
import json
from collections import defaultdict, deque
from pathlib import Path


def load_jsonl(path):
    rows = {}
    for n, raw in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        row = json.loads(raw)
        rid = row.get("id")
        if not rid:
            raise ValueError(f"{path}: line {n} missing id")
        if rid in rows:
            raise ValueError(f"{path}: duplicate id {rid}")
        rows[rid] = row
    return rows


def canonical(row):
    return json.dumps(row, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def graph_impact(graph_path, changed_ids):
    graph = json.loads(Path(graph_path).read_text(encoding="utf-8"))
    nodes = {n.get("id"): n for n in graph.get("nodes", []) if isinstance(n, dict) and n.get("id")}
    forward = defaultdict(set)
    for edge in graph.get("edges", []):
        if not isinstance(edge, dict):
            continue
        src, dst = edge.get("from"), edge.get("to")
        if src in nodes and dst in nodes:
            forward[src].add(dst)
    all_affected = set()
    for start in changed_ids:
        if start not in nodes:
            continue
        queue = deque([start])
        seen = set()
        while queue:
            cur = queue.popleft()
            for nxt in forward.get(cur, []):
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
        all_affected.update(seen)
    grouped = defaultdict(list)
    for nid in sorted(all_affected):
        grouped[nodes[nid].get("type", "unknown")].append(nid)
    return {"all": sorted(all_affected), "by_type": dict(sorted(grouped.items()))}


def main():
    p = argparse.ArgumentParser(description="Compute a stable-ID delta between two evidence ledgers.")
    p.add_argument("old")
    p.add_argument("new")
    p.add_argument("--graph")
    p.add_argument("--out")
    args = p.parse_args()

    try:
        old = load_jsonl(args.old)
        new = load_jsonl(args.new)
    except Exception as e:
        print(json.dumps({"status": "fail", "errors": [str(e)]}, indent=2))
        raise SystemExit(1)

    old_ids, new_ids = set(old), set(new)
    added = sorted(new_ids - old_ids)
    removed = sorted(old_ids - new_ids)
    shared = old_ids & new_ids
    modified = sorted(rid for rid in shared if canonical(old[rid]) != canonical(new[rid]))
    unchanged = sorted(shared - set(modified))
    changed = sorted(set(added + removed + modified))

    report = {
        "status": "pass",
        "added": added,
        "removed": removed,
        "modified": modified,
        "unchanged": unchanged,
        "changed": changed,
        "semantic_review_required": changed,
        "allowed_semantic_impacts": ["reinforce", "weaken", "contradict", "new_candidate", "no_action"],
    }
    if args.graph:
        report["downstream_impact"] = graph_impact(args.graph, changed)

    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
