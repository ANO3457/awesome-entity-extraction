#!/usr/bin/env python3
"""Validate fixtures, score recorded outputs, and build static field-guide files."""
from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from field_guide.evaluate import (  # noqa: E402
    RESULTS, build_report, load_fixture, load_json, recorded_runs, score_task,
    task_ids, validate_run, validate_task_fixtures,
)

REPO_URL = "https://github.com/shivamnegi92/awesome-entity-extraction"
MATRIX = ROOT / "field_guide/decision_matrix.json"


def repo_link(path: str) -> str:
    """Absolute GitHub URL for a repo-root-relative path.

    The Pages site only deploys ``field_guide/site``, so relative links to
    other repo files would 404. Always link through GitHub instead.
    """
    return f"{REPO_URL}/blob/main/{path.lstrip('/')}"


def validate(include_runs: bool = False) -> int:
    errors = validate_task_fixtures()
    if include_runs:
        for task_id in task_ids():
            fixture = load_fixture(task_id)
            for prediction_path in recorded_runs(task_id):
                errors.extend(
                    f"{prediction_path.relative_to(ROOT)}: {error}"
                    for error in validate_run(task_id, load_json(prediction_path), fixture)
                )
    if errors:
        print("Validation failed:\n" + "\n".join(f"- {e}" for e in errors))
        return 1
    print("OK: fixtures and requested run files are valid.")
    return 0


def _row(scenario: dict) -> str:
    cells = [
        html.escape(", ".join(scenario["start_with"])),
        html.escape(scenario["why"]),
        html.escape(", ".join(scenario["alternatives"]) or "—"),
        html.escape("; ".join(scenario["disqualifiers"] + scenario["unknowns"])),
    ]
    links = [f'<a href="{html.escape(repo_link(scenario["example"]), quote=True)}">Run/setup</a>']
    if scenario.get("task_card"):
        links.append(f'<a href="{html.escape(repo_link(scenario["task_card"]), quote=True)}">Task card</a>')
    return (f'<tr><th scope="row">{html.escape(scenario["task"])}</th>'
            + "".join(f"<td>{c}</td>" for c in cells)
            + f"<td>{' · '.join(links)}</td></tr>")


def _run_links(task: dict) -> str:
    """Link each recorded run's NOTES.md (or its predictions) so status is never bare."""
    links = []
    for run in task["runs"]:
        manifest = run.get("manifest", {})
        label = f"{manifest.get('tool', run.get('tool'))} {manifest.get('model') or ''}".strip()
        folder = run.get("path")
        if folder:
            target = f"{folder}/NOTES.md" if (ROOT / folder / "NOTES.md").is_file() else f"{folder}/predictions.json"
            label = f'<a href="{html.escape(repo_link(target), quote=True)}">{html.escape(label)}</a>'
        else:
            label = html.escape(label)
        links.append(f"{label} ({html.escape(run['status'])})")
    return "; recorded runs: " + ", ".join(links) if links else ""


def _task_list(report: dict) -> str:
    items = []
    for task in report["tasks"]:
        fixture = load_fixture(task["id"])
        status = task.get("status", "recorded")
        items.append(
            f'<li><a href="{html.escape(repo_link(f"field_guide/tasks/{task["id"]}/README.md"), quote=True)}">'
            f'{html.escape(task["id"])}</a>: {len(fixture["examples"])} synthetic cases; '
            f'metric <code>{html.escape(task["metric"])}</code>; status <strong>{html.escape(status)}</strong>'
            f'{_run_links(task)}.</li>'
        )
    return "".join(items)


def render_site() -> int:
    matrix = load_json(MATRIX)
    report = build_report()
    rows = "".join(_row(s) for s in matrix["scenarios"])
    task_status = " · ".join(f"{t['id']}: {t.get('status', 'recorded')}" for t in report["tasks"])
    content = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Entity Extraction Field Guide</title>
<style>
:root{{color-scheme:light dark;font:16px/1.55 system-ui,sans-serif}}body{{max-width:1200px;margin:auto;padding:1rem}}h1{{line-height:1.2}}.notice{{border-left:.3rem solid #b45309;padding:.75rem 1rem;background:color-mix(in srgb,#f59e0b 12%,transparent)}}.scroll{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;min-width:850px}}th,td{{border:1px solid #888;padding:.65rem;text-align:left;vertical-align:top}}th{{background:color-mix(in srgb,#777 18%,transparent)}}a{{text-underline-offset:.2em}}:focus-visible{{outline:3px solid #2563eb;outline-offset:3px}}small{{color:CanvasText}}
</style></head><body>
<p><a href="{REPO_URL}">Back to Awesome Entity Extraction repository</a></p>
<h1>Choose an entity extraction approach</h1>
<p>Use the task and constraints to find a starting point. These are editorial recommendations from catalog capabilities, not benchmark winners.</p>
<p class="notice"><strong>Status: prototype, not a benchmark.</strong> Task-card results: {html.escape(task_status)}. Recorded runs use six-case synthetic fixtures and haven't been independently reproduced; each run's write-up lists its misses. Confirm privacy, licensing, model availability, and performance for your environment.</p>
<div class="scroll"><table><caption>Task-to-approach shortlist and caveats</caption><thead><tr><th scope="col">Task</th><th scope="col">Start with</th><th scope="col">Why</th><th scope="col">Alternatives</th><th scope="col">Disqualifiers / unknowns</th><th scope="col">Links</th></tr></thead><tbody>{rows}</tbody></table></div>
<h2>Task cards</h2>
<ul>{_task_list(report)}</ul>
<p>Fixtures, annotation rules, and prediction schemas: <a href="{REPO_URL}/tree/main/field_guide/tasks">task data</a> · <a href="{repo_link('field_guide/results/report.json')}">machine-readable run status</a> · <a href="{repo_link('field_guide/decision_matrix.json')}">decision matrix (JSON)</a>.</p>
<p><small>Guide version {html.escape(report['guide_version'])}; matrix version {html.escape(matrix['version'])}. Reproduce offline from the repository root with <code>python3 scripts/run_field_guide.py validate</code> and <code>python3 -m unittest discover -s tests -v</code>.</small></p>
</body></html>
"""
    output = ROOT / "field_guide/site/index.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    _write_report(report)
    print(f"Built {output.relative_to(ROOT)} and field_guide/results/report.json")
    return 0


def _write_report(report: dict) -> Path:
    output = RESULTS / "report.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return output


def render_report() -> int:
    output = _write_report(build_report())
    print(f"Wrote {output.relative_to(ROOT)}; absent candidate outputs are not_run.")
    return 0


def score(task: str, prediction_path: Path) -> int:
    fixture = load_fixture(task)
    try:
        predictions = load_json(prediction_path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Cannot read {prediction_path}: {exc}", file=sys.stderr)
        return 1
    errors = validate_run(task, predictions, fixture)
    if errors:
        print("Run validation failed:\n" + "\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print(json.dumps(score_task(task, fixture, predictions), ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    validate_parser = sub.add_parser("validate", help="validate fixtures and optionally recorded runs")
    validate_parser.add_argument("--runs", action="store_true")
    sub.add_parser("report", help="refresh machine-readable run status; no inference")
    sub.add_parser("build", help="generate static HTML chooser and JSON run report")
    score_parser = sub.add_parser("score", help="validate and score a recorded output JSON")
    score_parser.add_argument("task", choices=task_ids())
    score_parser.add_argument("prediction_json", type=Path)
    args = parser.parse_args()
    if args.command == "validate":
        return validate(args.runs)
    if args.command == "report":
        return render_report()
    if args.command == "build":
        return render_site()
    return score(args.task, args.prediction_json)


if __name__ == "__main__":
    raise SystemExit(main())
