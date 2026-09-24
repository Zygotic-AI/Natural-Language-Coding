"""Unit tests for RuleReceipt noun verbs."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(TOOLS))

from nouns.rule_receipt.rule_receipt import RuleReceipt  # noqa: E402


class TestRuleReceipt(unittest.TestCase):
    def setUp(self) -> None:
        self.n = RuleReceipt()

    def test_format_marker_python(self) -> None:
        self.assertEqual(self.n.format_marker("ADR-0023.a"), "# nlc:rule=ADR-0023.a")

    def test_apply_markers_inserts(self) -> None:
        src = "def run():\n    return 1\n"
        out, added = self.n.apply_markers_to_source(src, ["R1"])
        self.assertEqual(added, ["R1"])
        self.assertIn("# nlc:rule=R1", out)

    def test_check_ir_empty_without_adopted(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(self.n.check_ir(Path(td)), [])

    def test_materialize_and_check(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "rules").mkdir()
            (root / "rules" / "adopted.json").write_text(
                json.dumps(
                    {
                        "adoptions": [
                            {
                                "rule_id": "t.1",
                                "adr_id": "0023",
                                "effect": "must",
                                "obligation": "keep marker",
                                "match": {"tags_any": ["nlc"]},
                            }
                        ]
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            rows = self.n.materialize_ir(root)
            self.n.write_snapshot(root, rows)
            self.assertEqual(self.n.check_ir(root), [])

    def test_check_semantic_pan_return(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "domain" / "card").mkdir(parents=True)
            (root / "domain" / "card" / "taint.txt").write_text("card_number\n", encoding="utf-8")
            (root / "goals" / "g" / "implementation.py").parent.mkdir(parents=True)
            (root / "goals" / "g" / "implementation.py").write_text(
                "def run():\n    card_number = 1\n    return card_number\n",
                encoding="utf-8",
            )
            (root / "rules").mkdir()
            (root / "rules" / "adopted.json").write_text(
                json.dumps(
                    {
                        "adoptions": [
                            {
                                "rule_id": "pan-no-return",
                                "adr_id": "0007",
                                "effect": "forbid",
                                "obligation": None,
                                "match": {"tags_all": ["pan"], "primitive": "return"},
                            }
                        ]
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            rows = self.n.materialize_ir(root)
            self.n.write_snapshot(root, rows)
            sem = self.n.check_semantic_ir(root)
            self.assertTrue(sem and "forbid return" in sem[0])


if __name__ == "__main__":
    unittest.main()
