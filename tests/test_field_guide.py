"""Offline tests for field-guide fixtures and scoring semantics."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from field_guide.evaluate import (  # noqa: E402
    RESULTS, TASKS, build_report, score_ner, score_pii_residuals,
    validate_run, validate_task_fixtures,
)


class FieldGuideTests(unittest.TestCase):
    def setUp(self):
        self.ner = json.loads((TASKS / "custom-ner/fixture.json").read_text())
        self.pii = json.loads((TASKS / "pii-redaction/fixture.json").read_text())

    def test_task_fixtures_validate(self):
        self.assertEqual(validate_task_fixtures(), [])

    def test_ner_exact_and_overlap_metrics(self):
        rows = [{"id": case["id"], "entities": [dict(e) for e in case["entities"]]}
                for case in self.ner["examples"]]
        rows[0]["entities"][0] = {"text": "Maya", "label": "PERSON", "start": 0, "end": 4}
        metrics = score_ner(self.ner, {"examples": rows})
        self.assertLess(metrics["strict_span_type"]["f1"], 1.0)
        self.assertEqual(metrics["overlap_span_type"]["f1"], 1.0)

    def test_ner_missing_case_is_error(self):
        with self.assertRaisesRegex(ValueError, "missing"):
            score_ner(self.ner, {"examples": []})

    def test_ner_wrong_type_is_false_positive_and_false_negative(self):
        rows = [{"id": case["id"], "entities": [dict(e) for e in case["entities"]]}
                for case in self.ner["examples"]]
        rows[0]["entities"][0]["label"] = "ORG"
        result = score_ner(self.ner, {"examples": rows})
        self.assertEqual(result["strict_span_type"]["fp"], 1)
        self.assertEqual(result["strict_span_type"]["fn"], 1)

    def test_pii_residuals_detect_unredacted_value(self):
        outputs = []
        for case in self.pii["examples"]:
            redacted = case["text"].replace(case["sensitive_values"][0], "<REDACTED>") if case["sensitive_values"] else case["text"]
            outputs.append({"id": case["id"], "redacted_text": redacted, "detected_types": []})
        result = score_pii_residuals(self.pii, {"examples": outputs})
        self.assertGreater(result["sensitive_values_remaining"], 0)
        self.assertGreater(result["residual_rate"], 0.0)

    def test_pii_result_must_cover_every_case(self):
        with self.assertRaisesRegex(ValueError, "exactly one"):
            score_pii_residuals(self.pii, {"examples": []})

    def test_run_validation_requires_complete_cases_and_manifest(self):
        predictions = {"examples": []}
        errors = validate_run("custom-ner", predictions, self.ner)
        self.assertIn("prediction file must contain a run manifest", errors)

    def test_valid_manifest_missing_fixture_cases_is_rejected(self):
        predictions = {"run": {"tool": "demo", "version": "1", "fixture_version": "1.0.0",
                               "run_date_utc": "2026-01-01T00:00:00Z", "environment": "test",
                               "status": "passed", "command": "demo", "git_commit": "abc",
                               "network_or_api": False}, "examples": []}
        errors = validate_run("custom-ner", predictions, self.ner)
        self.assertIn("predictions must include exactly one result for every fixture case", errors)

    def test_generated_chooser_links_to_project_repo_not_account_root(self):
        script = ROOT / "scripts/run_field_guide.py"
        subprocess.run([sys.executable, str(script), "build"], check=True, cwd=ROOT,
                       capture_output=True, text=True)
        page = (ROOT / "field_guide/site/index.html").read_text()
        self.assertNotIn('href="../../README.md"', page)
        self.assertIn("https://github.com/shivamnegi92/awesome-entity-extraction", page)
        self.assertIn("blob/main/examples/01-spacy-ner/README.md", page)

    def test_no_recorded_runs_are_not_run(self):
        report = build_report()
        self.assertTrue(all(task.get("status") == "not_run" for task in report["tasks"]))


if __name__ == "__main__":
    unittest.main()
