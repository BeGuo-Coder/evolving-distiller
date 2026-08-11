#!/usr/bin/env python3
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def run(script, *args, expect=0):
    proc = subprocess.run([sys.executable, str(HERE / script), *map(str, args)], capture_output=True, text=True)
    if proc.returncode != expect:
        raise RuntimeError(f"{script} returned {proc.returncode}, expected {expect}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
    return proc.stdout


def write_json(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        old = td / "old.jsonl"
        new = td / "new.jsonl"
        old.write_text(json.dumps({"id":"E001","claim":"A","evidence_class":"decision","support":"direct","source_id":"S1","confidence":"high","locator":"p1"}) + "\n", encoding="utf-8")
        new.write_text(
            json.dumps({"id":"E001","claim":"A revised","evidence_class":"decision","support":"direct","source_id":"S1","confidence":"high","locator":"p1"}) + "\n" +
            json.dumps({"id":"E002","claim":"B","evidence_class":"boundary","support":"direct","source_id":"S2","confidence":"medium","locator":"p2"}) + "\n",
            encoding="utf-8",
        )
        run("evidence_audit.py", new)

        graph = td / "graph.json"
        write_json(graph, {
            "nodes": [
                {"id":"E001","type":"evidence"},
                {"id":"E002","type":"evidence"},
                {"id":"C001","type":"claim"},
                {"id":"M01","type":"model","core":True},
                {"id":"I01","type":"instruction"},
                {"id":"T01","type":"test"}
            ],
            "edges": [
                {"from":"E001","to":"C001","relation":"supports"},
                {"from":"E002","to":"C001","relation":"limits"},
                {"from":"C001","to":"M01","relation":"supports"},
                {"from":"M01","to":"I01","relation":"implements"},
                {"from":"I01","to":"T01","relation":"covered_by"}
            ]
        })
        graph_out = json.loads(run("graph_audit.py", graph, "--impact", "E001"))
        assert "I01" in graph_out["impact"]["E001"]["all"]

        delta_out = json.loads(run("detect_delta.py", old, new, "--graph", graph))
        assert delta_out["added"] == ["E002"]
        assert delta_out["modified"] == ["E001"]

        comparison = td / "comparison.json"
        write_json(comparison, {
            "hard_gates":"pass",
            "regression":{"incumbent":8,"candidate":8},
            "challenge":{"incumbent":4,"candidate":5},
            "shadow":{"incumbent":6,"candidate":6},
            "require_challenge_improvement":True
        })
        run("suite_gate.py", comparison)

        votes = td / "votes.json"
        write_json(votes, [
            {"judge":"J1","verdict":"better"},
            {"judge":"J2","verdict":"better"},
            {"judge":"J3","verdict":"worse"}
        ])
        vote_out = json.loads(run("pairwise_vote.py", votes))
        assert vote_out["decision"] == "keep_candidate"

        history = td / "evolution" / "history.jsonl"
        run("evolution_log.py", history,
            "--candidate-id", "v1-c1", "--parent", "v1", "--trigger", "challenge_failure",
            "--trigger-ids", "T14", "--hypothesis", "Add a boundary", "--mutation", "BOUND",
            "--changes", "SKILL.md", "--decision", "keep", "--better", "2", "--worse", "1",
            "--hard-gates", "pass", "--suite-gate", "pass")
        run("evolution_log.py", history,
            "--candidate-id", "v1-c2", "--parent", "v1-c1", "--trigger", "challenge_failure",
            "--trigger-ids", "T15", "--hypothesis", "Compress rules", "--mutation", "COMPRESS",
            "--changes", "SKILL.md", "--decision", "revert", "--better", "1", "--worse", "2",
            "--hard-gates", "pass", "--suite-gate", "pass")
        memory_out = td / "evolution"
        run("evolution_memory.py", history, memory_out)
        patterns = json.loads((memory_out / "patterns.json").read_text(encoding="utf-8"))
        assert patterns["by_mutation"]["BOUND"]["keeps"] == 1
        assert patterns["by_mutation"]["COMPRESS"]["reverts"] == 1

        stable = td / "stable"
        candidate = td / "candidate"
        shutil.copytree(ROOT, stable)
        shutil.copytree(ROOT, candidate)
        manifest = td / "constitution-manifest.json"
        run("constitution_guard.py", "snapshot", stable, manifest)
        run("constitution_guard.py", "check", candidate, manifest)
        protected = candidate / "references" / "constitution.json"
        protected.write_text(protected.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        run("constitution_guard.py", "check", candidate, manifest, expect=1)

    print(json.dumps({"status":"pass","modules":[
        "claim_evidence_graph",
        "delta_distillation",
        "layered_test_gate",
        "evolution_memory_mutations",
        "evolution_constitution"
    ]}, indent=2))


if __name__ == "__main__":
    main()
