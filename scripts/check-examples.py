#!/usr/bin/env python3
"""Offline structural checks for the independently runnable examples.

Examples are *discovered*: any ``examples/NN-slug/`` folder is an example. Each
must contain README.md, main.py, requirements.txt, and a valid example.json.
The table in examples/README.md is generated from the example.json files.

Usage (from the repository root):
    python3 scripts/check-examples.py          # check only (CI)
    python3 scripts/check-examples.py --write  # regenerate examples/README.md index

Does not import optional ML packages, download models, call APIs, or verify
model quality.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _schema import validate as validate_schema  # noqa: E402
from model_policy import violations  # noqa: E402

EXAMPLES = ROOT / "examples"
FIELD_GUIDE = ROOT / "field_guide"
SCHEMA = json.loads((EXAMPLES / "example.schema.json").read_text(encoding="utf-8"))
REQUIRED_FILES = ("README.md", "main.py", "requirements.txt", "example.json")
TASK_FILES = ("README.md", "fixture.json", "annotation.md", "prediction.schema.json")
FOLDER_RE = re.compile(r"^\d{2}-[a-z0-9-]+$")
INDEX_START = "<!-- BEGIN GENERATED EXAMPLES INDEX: edit example.json files, then run scripts/check-examples.py --write -->"
INDEX_END = "<!-- END GENERATED EXAMPLES INDEX -->"


def discover() -> list[Path]:
    return sorted(p for p in EXAMPLES.iterdir() if p.is_dir() and FOLDER_RE.match(p.name))


def check_script(name: str, script: Path) -> list[str]:
    try:
        tree = ast.parse(script.read_text(encoding="utf-8"), filename=str(script))
    except SyntaxError as exc:
        return [f"{name}: syntax error: {exc}"]
    errors = []
    if not any(isinstance(n, ast.FunctionDef) and n.name == "main" for n in tree.body):
        errors.append(f"{name}: main.py has no top-level main()")
    for node in ast.walk(tree):
        modules = ([node.module] if isinstance(node, ast.ImportFrom) and node.module
                   else [a.name for a in node.names] if isinstance(node, ast.Import) else [])
        if any(m == "examples" or m.startswith("examples.") for m in modules):
            errors.append(f"{name}: imports another examples module")
    return errors


def load_metadata(folder: Path) -> tuple[dict | None, list[str]]:
    name = folder.name
    try:
        meta = json.loads((folder / "example.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, [f"{name}: invalid example.json: {exc}"]
    errors = [f"{name}: example.json {e}" for e in validate_schema(meta, SCHEMA)]
    if meta.get("id") != name:
        errors.append(f"{name}: example.json id {meta.get('id')!r} must equal folder name")
    for model in meta.get("models", []):
        text = " ".join(str(model.get(k, "")) for k in ("name", "publisher", "base_model"))
        errors.extend(f"{name}: model {model.get('name')!r} violates model-origin policy ({v})"
                      for v in violations(text))
    return meta, errors


def check_examples() -> tuple[list[dict], list[str]]:
    folders = discover()
    errors = [] if folders else ["no example folders found under examples/"]
    stray = [p.name for p in EXAMPLES.iterdir()
             if p.is_dir() and p.name[:2].isdigit() and not FOLDER_RE.match(p.name)]
    errors.extend(f"{s}: folder name must look like NN-lowercase-slug" for s in stray)
    metas = []
    for folder in folders:
        missing = [f for f in REQUIRED_FILES if not (folder / f).is_file()]
        errors.extend(f"{folder.name}: missing {f}" for f in missing)
        if (folder / "main.py").is_file():
            errors.extend(check_script(folder.name, folder / "main.py"))
        if "example.json" not in missing:
            meta, meta_errors = load_metadata(folder)
            errors.extend(meta_errors)
            if meta and not meta_errors:
                metas.append(meta)
    return metas, errors


def _flags(meta: dict) -> str:
    flags = []
    if meta["needs_api_key"]:
        flags.append("API key")
    if meta["needs_network"]:
        flags.append("network")
    if meta["downloads_model"]:
        flags.append("model download")
    if meta["needs_gpu"]:
        flags.append("GPU")
    return ", ".join(flags) or "none"


def render_index(metas: list[dict]) -> str:
    rows = ["| # | Example | Stack | What it demonstrates | Needs |",
            "|---|---------|-------|----------------------|-------|"]
    for meta in metas:
        number = int(meta["id"][:2])
        rows.append(f"| {number} | [{meta['title']}]({meta['id']}/README.md) | {meta['stack']} "
                    f"| {meta['summary']} | {_flags(meta)} |")
    return "\n".join([INDEX_START, "", *rows, "", INDEX_END])


def sync_index(metas: list[dict], write: bool) -> list[str]:
    path = EXAMPLES / "README.md"
    text = path.read_text(encoding="utf-8")
    if INDEX_START not in text or INDEX_END not in text:
        return ["examples/README.md is missing the generated-index markers"]
    before, rest = text.split(INDEX_START, 1)
    after = rest.split(INDEX_END, 1)[1]
    updated = before + render_index(metas) + after
    if updated == text:
        return []
    if write:
        path.write_text(updated, encoding="utf-8")
        print("Regenerated examples/README.md index.")
        return []
    return ["examples/README.md index is stale; run: python3 scripts/check-examples.py --write"]


def check_field_guide() -> list[str]:
    errors = []
    for rel in ("README.md", "decision_matrix.json", "results/report.json"):
        if not (FIELD_GUIDE / rel).is_file():
            errors.append(f"field guide is missing {rel}")
    if (FIELD_GUIDE / "tasks/index.json").exists():
        errors.append("field_guide/tasks/index.json duplicates decision_matrix.json; delete it")
    tasks = sorted(p.parent for p in (FIELD_GUIDE / "tasks").glob("*/fixture.json"))
    if not tasks:
        errors.append("field guide has no task cards")
    for task in tasks:
        errors.extend(f"field guide task {task.name} is missing {f}"
                      for f in TASK_FILES if not (task / f).is_file())
    for json_path in FIELD_GUIDE.rglob("*.json"):
        try:
            json.loads(json_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid JSON {json_path.relative_to(ROOT)}: {exc}")
    errors.extend(check_matrix_links())
    return errors


def check_matrix_links() -> list[str]:
    """Every path in the decision matrix must exist, so the chooser never 404s."""
    matrix = json.loads((FIELD_GUIDE / "decision_matrix.json").read_text(encoding="utf-8"))
    errors, seen = [], set()
    for scenario in matrix.get("scenarios", []):
        sid = scenario.get("id")
        if sid in seen:
            errors.append(f"decision matrix: duplicate scenario id {sid!r}")
        seen.add(sid)
        for key in ("example", "task_card"):
            target = scenario.get(key)
            if target and not (ROOT / target.split("#", 1)[0]).is_file():
                errors.append(f"decision matrix {sid}: {key} path does not exist: {target}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--write", action="store_true", help="regenerate examples/README.md index")
    args = parser.parse_args()

    metas, errors = check_examples()
    if not errors:
        errors.extend(sync_index(metas, args.write))
    errors.extend(check_field_guide())
    readme = ROOT / "README.md"
    if "field_guide/README.md" not in readme.read_text(encoding="utf-8"):
        errors.append("main README does not link to the Extraction Field Guide")

    if errors:
        print("Example checks failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"OK: {len(metas)} independent example folders have README, script, requirements, and valid metadata.")
    print("Note: dependencies, model downloads, network calls, and prediction quality are not tested.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
