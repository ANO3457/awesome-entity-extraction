#!/usr/bin/env python3
"""Offline structural checks for the independently runnable examples.

Does not import optional ML packages, download models, call APIs, or claim to
verify model quality. Run from the repository root: python3 scripts/check-examples.py
"""
from pathlib import Path
import ast
import sys

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
EXPECTED = {
    "01-spacy-ner", "02-gliner-zero-shot", "03-instructor-structured",
    "04-presidio-pii", "05-rebel-relations", "06-invoice-pdf",
    "07-stanza-multilingual", "08-temporal-quantity",
    "09-scispacy-biomedical", "10-wikidata-linking",
}


def main() -> int:
    folders = {p.name for p in EXAMPLES.iterdir() if p.is_dir() and p.name[:2].isdigit()}
    errors = []
    if folders != EXPECTED:
        errors.append(f"expected ten example folders; found {sorted(folders)}")
    for name in sorted(EXPECTED):
        folder = EXAMPLES / name
        for filename in ("README.md", "main.py", "requirements.txt"):
            if not (folder / filename).is_file():
                errors.append(f"{name}: missing {filename}")
        script = folder / "main.py"
        if script.exists():
            try:
                tree = ast.parse(script.read_text(encoding="utf-8"), filename=str(script))
                if not any(isinstance(node, ast.FunctionDef) and node.name == "main"
                           for node in tree.body):
                    errors.append(f"{name}: main.py has no top-level main()")
                for node in ast.walk(tree):
                    imported_modules = []
                    if isinstance(node, ast.ImportFrom) and node.module:
                        imported_modules.append(node.module)
                    elif isinstance(node, ast.Import):
                        imported_modules.extend(alias.name for alias in node.names)
                    if any(module == "examples" or module.startswith("examples.")
                           for module in imported_modules):
                        errors.append(f"{name}: imports another examples module")
            except SyntaxError as exc:
                errors.append(f"{name}: syntax error: {exc}")
    index = EXAMPLES / "README.md"
    if index.exists():
        text = index.read_text(encoding="utf-8")
        for name in sorted(EXPECTED):
            if f"{name}/README.md" not in text:
                errors.append(f"examples index does not link to {name}/README.md")
    if errors:
        print("Example checks failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"OK: {len(EXPECTED)} independent example folders have README, script, and requirements.")
    print("Note: dependencies, model downloads, network calls, and prediction quality are not tested.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
