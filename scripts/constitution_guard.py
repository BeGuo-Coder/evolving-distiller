#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_rel(value):
    p = Path(value)
    if p.is_absolute() or ".." in p.parts:
        raise ValueError(f"unsafe protected path {value!r}")
    return p


def snapshot(root, manifest_path):
    root = Path(root)
    constitution_path = root / "references" / "constitution.json"
    data = json.loads(constitution_path.read_text(encoding="utf-8"))
    protected = data.get("protected_paths", [])
    if not isinstance(protected, list) or not protected:
        raise ValueError("constitution protected_paths must be a non-empty list")
    files = {}
    for rel_value in protected:
        rel = safe_rel(rel_value)
        path = root / rel
        if not path.is_file():
            raise ValueError(f"protected file missing: {rel}")
        files[str(rel)] = sha256(path)
    manifest = {
        "constitution_version": data.get("version"),
        "protected_files": files,
    }
    Path(manifest_path).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return {"status": "pass", "action": "snapshot", "protected": len(files), "manifest": str(manifest_path)}


def check(root, manifest_path):
    root = Path(root)
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    files = manifest.get("protected_files", {})
    if not isinstance(files, dict) or not files:
        raise ValueError("manifest has no protected_files")
    changed = []
    missing = []
    for rel_value, expected in files.items():
        rel = safe_rel(rel_value)
        path = root / rel
        if not path.is_file():
            missing.append(str(rel))
            continue
        actual = sha256(path)
        if actual != expected:
            changed.append(str(rel))
    status = "pass" if not changed and not missing else "fail"
    return {"status": status, "action": "check", "changed": changed, "missing": missing, "protected": len(files)}


def main():
    p = argparse.ArgumentParser(description="Snapshot or verify protected Evolution Constitution files.")
    sub = p.add_subparsers(dest="cmd", required=True)
    ps = sub.add_parser("snapshot")
    ps.add_argument("skill_root")
    ps.add_argument("manifest")
    pc = sub.add_parser("check")
    pc.add_argument("skill_root")
    pc.add_argument("manifest")
    args = p.parse_args()

    try:
        if args.cmd == "snapshot":
            report = snapshot(args.skill_root, args.manifest)
        else:
            report = check(args.skill_root, args.manifest)
    except Exception as e:
        report = {"status": "fail", "error": str(e)}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report.get("status") == "pass" else 1)


if __name__ == "__main__":
    main()
