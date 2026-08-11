#!/usr/bin/env python3
import argparse
import json
from collections import defaultdict, deque
from pathlib import Path

NODE_TYPES = {"evidence", "claim", "model", "instruction", "test", "policy"}
RELATIONS = {"supports", "weakens", "contradicts", "limits", "implements", "covered_by", "constrains"}


def load_graph(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("graph root must be an object")
    return data


def ancestors(node_id, reverse):
    seen = set()
    queue = deque([node_id])
    while queue:
        cur = queue.popleft()
        for prev in reverse.get(cur, []):
            if prev not in seen:
                seen.add(prev)
                queue.append(prev)
    return seen


def descendants(node_id, forward):
    seen = set()
    queue = deque([node_id])
    while queue:
        cur = queue.popleft()
        for nxt in forward.get(cur, []):
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return seen


def main():
    p = argparse.ArgumentParser(description="Audit a Claim-Evidence provenance graph and optionally trace downstream impact.")
    p.add_argument("graph")
    p.add_argument("--impact", action="append", default=[], help="Node ID to trace downstream; may be repeated")
    args = p.parse_args()

    errors = []
    warnings = []
    try:
        data = load_graph(args.graph)
    except Exception as e:
        print(json.dumps({"status": "fail", "errors": [str(e)]}, indent=2))
        raise SystemExit(1)

    raw_nodes = data.get("nodes", [])
    raw_edges = data.get("edges", [])
    if not isinstance(raw_nodes, list):
        errors.append("nodes must be a list")
        raw_nodes = []
    if not isinstance(raw_edges, list):
        errors.append("edges must be a list")
        raw_edges = []

    nodes = {}
    for i, node in enumerate(raw_nodes, 1):
        if not isinstance(node, dict):
            errors.append(f"node {i}: must be an object")
            continue
        nid = node.get("id")
        ntype = node.get("type")
        if not nid:
            errors.append(f"node {i}: missing id")
            continue
        if nid in nodes:
            errors.append(f"node {i}: duplicate id {nid}")
            continue
        if ntype not in NODE_TYPES:
            errors.append(f"node {nid}: invalid type {ntype!r}")
        nodes[nid] = node

    forward = defaultdict(set)
    reverse = defaultdict(set)
    edge_count = 0
    for i, edge in enumerate(raw_edges, 1):
        if not isinstance(edge, dict):
            errors.append(f"edge {i}: must be an object")
            continue
        src = edge.get("from")
        dst = edge.get("to")
        rel = edge.get("relation")
        if src not in nodes:
            errors.append(f"edge {i}: unknown source {src!r}")
        if dst not in nodes:
            errors.append(f"edge {i}: unknown target {dst!r}")
        if rel not in RELATIONS:
            errors.append(f"edge {i}: invalid relation {rel!r}")
        if src in nodes and dst in nodes:
            forward[src].add(dst)
            reverse[dst].add(src)
            edge_count += 1

    ungrounded_instructions = []
    ungrounded_core_models = []
    for nid, node in nodes.items():
        ntype = node.get("type")
        if ntype == "instruction":
            upstream = ancestors(nid, reverse)
            source_types = {nodes[x].get("type") for x in upstream if x in nodes}
            if not ({"evidence", "policy"} & source_types):
                ungrounded_instructions.append(nid)
        if ntype == "model" and node.get("core") is True:
            upstream = ancestors(nid, reverse)
            if not any(nodes[x].get("type") == "evidence" for x in upstream if x in nodes):
                ungrounded_core_models.append(nid)

    if ungrounded_instructions:
        errors.append("ungrounded instructions: " + ", ".join(sorted(ungrounded_instructions)))
    if ungrounded_core_models:
        errors.append("ungrounded core models: " + ", ".join(sorted(ungrounded_core_models)))

    for nid, node in nodes.items():
        if node.get("type") == "test" and not reverse.get(nid):
            warnings.append(f"test {nid} has no incoming coverage edge")

    impact = {}
    for start in args.impact:
        if start not in nodes:
            impact[start] = {"error": "unknown node"}
            continue
        affected = descendants(start, forward)
        grouped = defaultdict(list)
        for nid in sorted(affected):
            grouped[nodes[nid].get("type", "unknown")].append(nid)
        impact[start] = {"all": sorted(affected), "by_type": dict(sorted(grouped.items()))}

    counts = defaultdict(int)
    for node in nodes.values():
        counts[node.get("type", "unknown")] += 1

    report = {
        "status": "pass" if not errors else "fail",
        "nodes": len(nodes),
        "edges": edge_count,
        "counts_by_type": dict(sorted(counts.items())),
        "errors": errors,
        "warnings": warnings,
    }
    if args.impact:
        report["impact"] = impact
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["status"] == "pass" else 1)


if __name__ == "__main__":
    main()
