"""Offline tests for the Wave 0 repository infrastructure.

Covers example discovery and metadata, the model-origin policy, the
dependency-free schema validator, the single decision matrix, metric plugins,
task discovery, and the catalog sidecar.
"""
import datetime as dt
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from _schema import validate as validate_schema  # noqa: E402
from field_guide import evaluate  # noqa: E402
from field_guide.metrics import METRICS, get_metric  # noqa: E402
from model_policy import violations  # noqa: E402


def load_script(name: str):
    """Import a hyphenated script file as a module."""
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


check_examples = load_script("check-examples")
check_catalog = load_script("check-catalog")


class SchemaValidatorTests(unittest.TestCase):
    SCHEMA = {"type": "object", "additionalProperties": False, "required": ["n", "flag"],
              "properties": {"n": {"type": "integer"}, "flag": {"type": "boolean"},
                             "tags": {"type": "array", "minItems": 1, "items": {"enum": ["a", "b"]}}}}

    def test_valid(self):
        self.assertEqual(validate_schema({"n": 1, "flag": True, "tags": ["a"]}, self.SCHEMA), [])

    def test_bool_is_not_an_integer(self):
        self.assertTrue(validate_schema({"n": True, "flag": True}, self.SCHEMA))

    def test_missing_extra_and_enum_errors(self):
        errors = validate_schema({"flag": "yes", "extra": 1, "tags": ["z"]}, self.SCHEMA)
        joined = "\n".join(errors)
        for needle in ("missing required 'n'", "unexpected key 'extra'", "expected boolean", "not one of"):
            self.assertIn(needle, joined)


class ModelPolicyTests(unittest.TestCase):
    def test_flags_barred_families_and_known_derivatives(self):
        for text in ("Qwen/Qwen2.5-7B-Instruct", "deepseek-ai/DeepSeek-V3", "THUDM/chatglm3-6b",
                     "internlm/internlm2-7b", "openbmb/MiniCPM-V", "numind/NuExtract-2.0-8B",
                     "https://github.com/PaddlePaddle/PaddleNLP", "https://github.com/hankcs/HanLP"):
            with self.subTest(text=text):
                self.assertTrue(violations(text))

    def test_allows_permitted_models_and_ordinary_words(self):
        for text in ("meta-llama/Llama-3.1-8B", "microsoft/Phi-3.5-mini-instruct", "google/gemma-2-9b",
                     "numind/NuExtract-1.5", "urchade/gliner_multi-v2.1", "Babelscape/rebel-large",
                     "yield the glimpse of a kimono", "Glossary"):
            with self.subTest(text=text):
                self.assertEqual(violations(text), [])

    def test_readme_passes_policy(self):
        self.assertEqual(check_catalog.check_policy(), [])


class ExampleDiscoveryTests(unittest.TestCase):
    """Run the real checker against a temporary copy of examples/."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.examples = self.tmp / "examples"
        shutil.copytree(ROOT / "examples", self.examples,
                        ignore=shutil.ignore_patterns(".venv", "__pycache__"))
        patcher = mock.patch.object(check_examples, "EXAMPLES", self.examples)
        patcher.start()
        self.addCleanup(patcher.stop)

    def add_example(self, folder: str, **overrides) -> Path:
        path = self.examples / folder
        path.mkdir()
        (path / "README.md").write_text("# Demo\n")
        (path / "main.py").write_text("def main():\n    return 0\n")
        (path / "requirements.txt").write_text("")
        meta = {"id": folder, "title": "Demo", "summary": "Demo", "task": "Demo", "stack": "stdlib",
                "input_type": "plain_text", "languages": ["en"], "runs_locally": True,
                "needs_api_key": False, "needs_gpu": False, "downloads_model": False,
                "needs_network": False, "models": []}
        meta.update(overrides)
        (path / "example.json").write_text(json.dumps(meta))
        return path

    def test_current_examples_pass(self):
        metas, errors = check_examples.check_examples()
        self.assertEqual(errors, [])
        self.assertGreaterEqual(len(metas), 10)

    def test_eleventh_example_needs_no_script_edits(self):
        self.add_example("11-demo")
        metas, errors = check_examples.check_examples()
        self.assertEqual(errors, [])
        self.assertIn("11-demo", [m["id"] for m in metas])
        self.assertIn("11-demo/README.md", check_examples.render_index(metas))

    def test_missing_metadata_fails(self):
        (self.add_example("11-demo") / "example.json").unlink()
        _, errors = check_examples.check_examples()
        self.assertIn("11-demo: missing example.json", errors)

    def test_id_must_match_folder(self):
        self.add_example("11-demo", id="11-other")
        _, errors = check_examples.check_examples()
        self.assertTrue(any("must equal folder name" in e for e in errors))

    def test_barred_base_model_fails(self):
        self.add_example("11-demo", models=[{"name": "acme/extractor", "publisher": "Acme",
                                             "license": "MIT", "base_model": "Qwen/Qwen2.5-7B"}])
        _, errors = check_examples.check_examples()
        self.assertTrue(any("model-origin policy" in e for e in errors))

    def test_stale_index_is_reported(self):
        metas, _ = check_examples.check_examples()
        self.assertEqual(check_examples.sync_index(metas, write=False), [])
        self.add_example("11-demo")
        metas, _ = check_examples.check_examples()
        self.assertTrue(check_examples.sync_index(metas, write=False))


class DecisionMatrixTests(unittest.TestCase):
    def test_single_source(self):
        self.assertFalse((ROOT / "field_guide/tasks/index.json").exists())

    def test_matrix_links_resolve_and_ids_unique(self):
        self.assertEqual(check_examples.check_matrix_links(), [])


class MetricPluginTests(unittest.TestCase):
    def test_every_fixture_declares_a_registered_metric(self):
        for task_id in evaluate.task_ids():
            with self.subTest(task=task_id):
                self.assertIn(evaluate.load_fixture(task_id).get("metric"), METRICS)

    def test_unknown_metric_is_a_clear_error(self):
        with self.assertRaisesRegex(KeyError, "unknown metric"):
            get_metric("bleu")

    def test_new_task_card_is_discovered_without_code_changes(self):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        shutil.copytree(evaluate.TASKS, tmp / "tasks")
        new = tmp / "tasks/demo-pii"
        new.mkdir()
        (new / "fixture.json").write_text(json.dumps({
            "version": "0.1.0", "task": "demo", "metric": "pii_residual",
            "examples": [{"id": "d1", "text": "Email a@example.test", "sensitive_values": ["a@example.test"]}]}))
        with mock.patch.object(evaluate, "TASKS", tmp / "tasks"), \
                mock.patch.object(evaluate, "RESULTS", tmp / "results"):
            self.assertIn("demo-pii", evaluate.task_ids())
            self.assertEqual(evaluate.validate_task_fixtures(), [])
            report = evaluate.build_report()
        demo = next(t for t in report["tasks"] if t["id"] == "demo-pii")
        self.assertEqual(demo["status"], "not_run")


class CatalogTests(unittest.TestCase):
    def test_catalog_valid_and_linked_to_readme(self):
        errors, _ = check_catalog.check_catalog(dt.date(2026, 10, 12), 180)
        self.assertEqual(errors, [])

    def test_staleness_is_detected(self):
        _, stale = check_catalog.check_catalog(dt.date(2027, 12, 31), 180)
        self.assertTrue(stale)


if __name__ == "__main__":
    unittest.main()
