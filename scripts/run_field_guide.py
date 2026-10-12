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
    RESULTS, TASKS, build_report, load_json, score_ner, score_pii_residuals,
    validate_run, validate_task_fixtures,
)


def validate(include_runs: bool = False) -> int:
    errors = validate_task_fixtures()
    if include_runs:
        for task_id in ("custom-ner", "pii-redaction"):
            fixture = load_json(TASKS / task_id / "fixture.json")
            run_dir = RESULTS / task_id
            if run_dir.exists():
                for prediction_path in sorted(run_dir.glob("*/predictions.json")):
                    errors.extend(
                        f"{prediction_path.relative_to(ROOT)}: {error}"
                        for error in validate_run(task_id, load_json(prediction_path), fixture)
                    )
    if errors:
        print("Validation failed:\n" + "\n".join(f"- {e}" for e in errors))
        return 1
    print("OK: fixtures and requested run files are valid.")
    return 0


def render_site() -> int:
    matrix = load_json(ROOT / "field_guide/decision_matrix.json")
    report = build_report()
    cards = []
    for scenario in matrix["scenarios"]:
        start = ", ".join(scenario["start_with"])
        alternatives = ", ".join(scenario["alternatives"])
        watch = "; ".join(scenario["disqualifiers"] + scenario["unknowns"])
        link = scenario["example"]
        href = "https://github.com/shivamnegi92/awesome-entity-extraction/blob/main/" + link.replace("../", "")
        cards.append(
            "<tr><th scope=\"row\">" + html.escape(scenario["task"]) + "</th>"
            "<td>" + html.escape(start) + "</td>"
            "<td>" + html.escape(scenario["why"]) + "</td>"
            "<td>" + html.escape(alternatives or "—") + "</td>"
            "<td>" + html.escape(watch) + "</td>"
            "<td><a href=\"" + html.escape(href, quote=True) + "\">Run/setup</a></td></tr>"
        )
    task_status = " · ".join(f"{item['id']}: {item.get('status', 'recorded')}"
                             for item in report["tasks"])
    content = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Entity Extraction Field Guide</title>
<style>
:root{{color-scheme:light dark;font:16px/1.55 system-ui,sans-serif}}body{{max-width:1200px;margin:auto;padding:1rem}}h1{{line-height:1.2}}.notice{{border-left:.3rem solid #b45309;padding:.75rem 1rem;background:color-mix(in srgb,#f59e0b 12%,transparent)}}.scroll{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;min-width:850px}}th,td{{border:1px solid #888;padding:.65rem;text-align:left;vertical-align:top}}th{{background:color-mix(in srgb,#777 18%,transparent)}}a{{text-underline-offset:.2em}}:focus-visible{{outline:3px solid #2563eb;outline-offset:3px}}small{{color:CanvasText}}
</style></head><body>
<p><a href="https://github.com/shivamnegi92/awesome-entity-extraction">Back to Awesome Entity Extraction repository</a></p>
<h1>Choose an entity extraction approach</h1>
<p>Use the task and constraints to find a starting point. These are editorial recommendations from catalog capabilities, not benchmark winners.</p>
<p class="notice"><strong>Status: prototype, not a benchmark.</strong> Task-card results: {html.escape(task_status)}. No model outputs are claimed as passed. Confirm privacy, licensing, model availability, and performance for your environment.</p>
<div class="scroll"><table><caption>Task-to-approach shortlist and caveats</caption><thead><tr><th scope="col">Task</th><th scope="col">Start with</th><th scope="col">Why</th><th scope="col">Alternatives</th><th scope="col">Disqualifiers / unknowns</th><th scope="col">Example</th></tr></thead><tbody>{''.join(cards)}</tbody></table></div>
<h2>Task cards</h2>
<ul><li><a href="../tasks/custom-ner/README.md">Custom-label NER</a>: six synthetic cases; exact and overlap span/type scoring.</li><li><a href="../tasks/pii-redaction/README.md">PII redaction</a>: six synthetic cases; exact-string residual checks only, not a privacy guarantee.</li></ul>
<p>Fixtures, annotation rules, prediction schemas, and raw report: <a href="../tasks/">task data</a> · <a href="../results/report.json">machine-readable run status</a>.</p>
<p><small>Guide version {html.escape(report['guide_version'])}. Reproduce offline from the repository root with <code>python3 scripts/run_field_guide.py validate</code> and <code>python3 -m unittest discover -s tests -v</code>.</small></p>
</body></html>
"""
    output = ROOT / "field_guide/site/index.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    (RESULTS / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Built {output.relative_to(ROOT)} and field_guide/results/report.json")
    return 0


def score(task: str, prediction_path: Path) -> int:
    fixture = load_json(TASKS / task / "fixture.json")
    predictions = load_json(prediction_path)
    errors = validate_run(task, predictions, fixture)
    if errors:
        print("Run validation failed:\n" + "\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    result = score_ner(fixture, predictions) if task == "custom-ner" else score_pii_residuals(fixture, predictions)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    validate_parser = sub.add_parser("validate", help="validate fixtures and optionally recorded runs")
    validate_parser.add_argument("--runs", action="store_true")
    sub.add_parser("report", help="refresh machine-readable run status; no inference")
    sub.add_parser("build", help="generate static HTML chooser and JSON run report")
    score_parser = sub.add_parser("score", help="validate and score a recorded output JSON")
    score_parser.add_argument("task", choices=("custom-ner", "pii-redaction"))
    score_parser.add_argument("prediction_json", type=Path)
    args = parser.parse_args()
    if args.command == "validate":
        return validate(args.runs)
    if args.command == "report":
        return render_report()
    if args.command == "build":
        return render_site()
    return score(args.task, args.prediction_json)


def render_report() -> int:
    report = build_report()
    output = RESULTS / "report.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output.relative_to(ROOT)}; absent candidate outputs are not_run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
