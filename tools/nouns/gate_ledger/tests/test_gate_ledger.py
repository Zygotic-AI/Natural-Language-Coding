"""Unit tests for GateLedger noun verbs."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(TOOLS))

from nouns.gate_ledger.gate_ledger import GateLedger  # noqa: E402


class TestGateLedger(unittest.TestCase):
    def setUp(self) -> None:
        self.n = GateLedger()

    def test_add_and_load_scope(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.n.add_scope_path(root, "goals/x/implementation.py")
            self.assertEqual(
                self.n.load_scope_paths(root), ["goals/x/implementation.py"]
            )

    def test_append_record_also_scopes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.n.append_record(
                root,
                artifact="goals/y/implementation.py",
                gate_id="fitness-demo",
                outcome="PASS",
            )
            records = json.loads(
                (root / ".nlc" / "gate-records.json").read_text(encoding="utf-8")
            )
            self.assertEqual(len(records["records"]), 1)
            self.assertIn("goals/y/implementation.py", self.n.load_scope_paths(root))


if __name__ == "__main__":
    unittest.main()
