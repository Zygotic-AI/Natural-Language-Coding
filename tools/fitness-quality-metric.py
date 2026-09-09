#!/usr/bin/env python3
"""BBP fitness check: quality metric validation (Q1-Q5, CS9-CS10).

Validates quality metric requirements from integrity/QUALITY_METRIC.md:
  Q1/CS9: Produce package must include gate receipts with outcome + timestamp
  Q2: Adversarial artifact must have ssot_leaf_ids + quality_snapshot.opportunities > 0
  Q3/CS10: Quality snapshot must have {opportunities, ops, defects, quality}, ops+defects=opportunities
  Q4: Defect classification is binary (op or defect only, no partial/weighted)
  Q5: Quality formula is ops/opportunities (within tolerance 1e-9)

Input: no argv. Scans tools/fixtures/quality-metric/ for validation fixtures.
  Each fixture file tests one or more requirements.
  Valid fixtures must pass; invalid fixtures must fail as expected.

Output: lines among
  CHECK <requirement> <fixture>:MET|NOT_MET [reason]
  FIXTURE_GATE <fixture>:PASS|FAIL [expected_result]
  RESULT:MET|NOT_MET

Failure mode: process exit 0 = RESULT:MET (PASS); exit 1 = RESULT:NOT_MET (FAIL).
  Does not swallow exceptions silently — unexpected errors propagate and abort.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURES_DIR = ROOT / "tools" / "fixtures" / "quality-metric"
QUALITY_METRIC_MD = ROOT / "integrity" / "QUALITY_METRIC.md"

VALID_OUTCOMES = {"PASS", "FAIL", "MET", "REFUSE", "NOT_MET"}
VALID_CLASSIFICATIONS = {"op", "defect"}
FORMULA_TOLERANCE = 1e-9


def load_fixture(path: Path) -> dict[str, Any]:
    """Load and parse a JSON fixture file."""
    return json.loads(path.read_text())


def validate_q1_cs9_produce_package(data: dict[str, Any]) -> tuple[bool, str]:
    """Q1/CS9: Check produce package has gate receipts with outcome + timestamp.
    
    Returns (passed, reason).
    """
    quality_evidence = data.get("quality_evidence")
    
    if not quality_evidence:
        return False, "quality_evidence missing from produce package"
    
    if not isinstance(quality_evidence, list) or len(quality_evidence) == 0:
        return False, "quality_evidence must be non-empty array"
    
    for i, receipt in enumerate(quality_evidence):
        gate_id = receipt.get("gate_id")
        outcome = receipt.get("outcome")
        timestamp = receipt.get("timestamp")
        
        if not gate_id:
            return False, f"gate_receipt[{i}] missing gate_id"
        
        if not outcome:
            return False, f"gate_receipt[{i}] missing outcome"
        
        if outcome not in VALID_OUTCOMES:
            return False, f"gate_receipt[{i}] invalid outcome: {outcome}"
        
        if not timestamp:
            return False, f"gate_receipt[{i}] missing timestamp"
    
    return True, f"{len(quality_evidence)} valid gate receipt(s)"


def validate_q2_adversarial(data: dict[str, Any]) -> tuple[bool, str]:
    """Q2: Check adversarial artifact has ssot_leaf_ids + quality_snapshot.opportunities > 0.
    
    Returns (passed, reason).
    """
    ssot_leaf_ids = data.get("ssot_leaf_ids")
    quality_snapshot = data.get("quality_snapshot")
    
    if not ssot_leaf_ids:
        return False, "ssot_leaf_ids missing"
    
    if not isinstance(ssot_leaf_ids, list) or len(ssot_leaf_ids) == 0:
        return False, "ssot_leaf_ids must be non-empty array"
    
    if not quality_snapshot:
        return False, "quality_snapshot missing"
    
    opportunities = quality_snapshot.get("opportunities")
    if opportunities is None:
        return False, "quality_snapshot.opportunities missing"
    
    if not isinstance(opportunities, (int, float)) or opportunities <= 0:
        return False, f"quality_snapshot.opportunities must be > 0, got {opportunities}"
    
    return True, f"ssot_leaf_ids present, opportunities={opportunities}"


def validate_q3_cs10_quality_snapshot(data: dict[str, Any]) -> tuple[bool, str]:
    """Q3/CS10: Check quality_snapshot has all 4 fields and ops+defects=opportunities.
    
    Returns (passed, reason).
    """
    quality_snapshot = data.get("quality_snapshot")
    
    if not quality_snapshot:
        return False, "quality_snapshot missing"
    
    required_fields = ["opportunities", "ops", "defects", "quality"]
    missing = [f for f in required_fields if f not in quality_snapshot]
    
    if missing:
        return False, f"quality_snapshot missing fields: {', '.join(missing)}"
    
    opportunities = quality_snapshot["opportunities"]
    ops = quality_snapshot["ops"]
    defects = quality_snapshot["defects"]
    quality = quality_snapshot["quality"]
    
    if not all(isinstance(v, (int, float)) for v in [opportunities, ops, defects]):
        return False, "opportunities/ops/defects must be numeric"
    
    if not isinstance(quality, (int, float)):
        return False, "quality must be numeric"
    
    if ops + defects != opportunities:
        return False, f"ops({ops}) + defects({defects}) != opportunities({opportunities})"
    
    return True, f"snapshot valid: {ops}+{defects}={opportunities}"


def validate_q4_binary_classification(data: dict[str, Any]) -> tuple[bool, str]:
    """Q4: Check all outcomes are binary (op or defect only, no partial/weighted).
    
    Returns (passed, reason).
    """
    outcomes = data.get("outcomes")
    
    if not outcomes:
        return True, "no outcomes to validate"
    
    if not isinstance(outcomes, list):
        return False, "outcomes must be an array"
    
    for i, outcome in enumerate(outcomes):
        classification = outcome.get("classification")
        
        if not classification:
            return False, f"outcome[{i}] missing classification"
        
        if classification not in VALID_CLASSIFICATIONS:
            return False, f"outcome[{i}] non-binary classification: {classification}"
        
        if "weight" in outcome:
            return False, f"outcome[{i}] has weight (weighted not allowed)"
        
        if outcome.get("partial") or outcome.get("provisional"):
            return False, f"outcome[{i}] has partial/provisional flag"
    
    return True, f"{len(outcomes)} outcomes all binary"


def validate_q5_formula(data: dict[str, Any]) -> tuple[bool, str]:
    """Q5: Check quality = ops/opportunities (within tolerance).
    
    Returns (passed, reason).
    """
    quality_snapshot = data.get("quality_snapshot")
    
    if not quality_snapshot:
        return False, "quality_snapshot missing for formula check"
    
    opportunities = quality_snapshot.get("opportunities")
    ops = quality_snapshot.get("ops")
    quality = quality_snapshot.get("quality")
    
    if opportunities is None or ops is None or quality is None:
        return False, "missing fields for formula verification"
    
    if opportunities == 0:
        expected = 0.0
    else:
        expected = ops / opportunities
    
    if abs(quality - expected) > FORMULA_TOLERANCE:
        return False, f"quality({quality}) != ops/opportunities({expected})"
    
    return True, f"quality={quality} matches ops/opportunities"


def validate_ssot_formula_section() -> tuple[bool, str]:
    """Q5 structural: Check QUALITY_METRIC.md has locked formula definition."""
    if not QUALITY_METRIC_MD.is_file():
        return False, "integrity/QUALITY_METRIC.md not found"
    
    content = QUALITY_METRIC_MD.read_text().lower()
    
    has_formula = "quality = ops / opportunities" in content
    has_no_weighted = "no weighted" in content or "no weighting" in content
    
    if has_formula and has_no_weighted:
        return True, "formula locked in SSOT"
    
    if not has_formula:
        return False, "formula definition missing from SSOT"
    
    return True, "formula present in SSOT"


def run_fixture_tests() -> list[tuple[str, str, bool, str]]:
    """Run validation on all fixtures, return results.
    
    Returns list of (requirement_id, fixture_name, passed, reason).
    """
    results = []
    
    if not FIXTURES_DIR.is_dir():
        return results
    
    for fixture_path in sorted(FIXTURES_DIR.glob("*.json")):
        fixture_name = fixture_path.stem
        is_valid_fixture = fixture_name.startswith("valid-")
        is_invalid_fixture = fixture_name.startswith("invalid-")
        
        if not (is_valid_fixture or is_invalid_fixture):
            continue
        
        data = load_fixture(fixture_path)
        
        if "produce-package" in fixture_name:
            passed, reason = validate_q1_cs9_produce_package(data)
            if is_valid_fixture:
                results.append(("Q1", fixture_name, passed, reason))
                results.append(("CS9", fixture_name, passed, reason))
            else:
                expected_fail = not passed
                results.append(("Q1", fixture_name, expected_fail, 
                               f"expected fail: {reason}" if expected_fail else f"should have failed: {reason}"))
                results.append(("CS9", fixture_name, expected_fail,
                               f"expected fail: {reason}" if expected_fail else f"should have failed: {reason}"))
        
        if "adversarial" in fixture_name:
            passed, reason = validate_q2_adversarial(data)
            if is_valid_fixture:
                results.append(("Q2", fixture_name, passed, reason))
            else:
                expected_fail = not passed
                results.append(("Q2", fixture_name, expected_fail,
                               f"expected fail: {reason}" if expected_fail else f"should have failed: {reason}"))
        
        if "snapshot" in fixture_name or "quality-snapshot" in fixture_name:
            passed, reason = validate_q3_cs10_quality_snapshot(data)
            if is_valid_fixture:
                results.append(("Q3", fixture_name, passed, reason))
                results.append(("CS10", fixture_name, passed, reason))
            else:
                expected_fail = not passed
                results.append(("Q3", fixture_name, expected_fail,
                               f"expected fail: {reason}" if expected_fail else f"should have failed: {reason}"))
                results.append(("CS10", fixture_name, expected_fail,
                               f"expected fail: {reason}" if expected_fail else f"should have failed: {reason}"))
        
        if "binary-outcome" in fixture_name or ("outcome" in fixture_name and "produce-package" not in fixture_name):
            passed, reason = validate_q4_binary_classification(data)
            if is_valid_fixture:
                results.append(("Q4", fixture_name, passed, reason))
            else:
                expected_fail = not passed
                results.append(("Q4", fixture_name, expected_fail,
                               f"expected fail: {reason}" if expected_fail else f"should have failed: {reason}"))
        
        if "formula" in fixture_name:
            passed, reason = validate_q5_formula(data)
            if is_valid_fixture:
                results.append(("Q5", fixture_name, passed, reason))
            else:
                expected_fail = not passed
                results.append(("Q5", fixture_name, expected_fail,
                               f"expected fail: {reason}" if expected_fail else f"should have failed: {reason}"))
        
        if "valid-quality-snapshot" in fixture_name:
            passed, reason = validate_q5_formula(data)
            results.append(("Q5", fixture_name, passed, reason))
    
    return results


def main() -> int:
    results: list[tuple[str, str, bool, str]] = []
    
    results.extend(run_fixture_tests())
    
    passed, reason = validate_ssot_formula_section()
    results.append(("Q5", "SSOT-formula-lock", passed, reason))
    
    all_passed = True
    for req_id, fixture, passed, reason in results:
        status = "MET" if passed else "NOT_MET"
        print(f"CHECK {req_id} {fixture}:{status} {reason}")
        if not passed:
            all_passed = False
    
    seen_reqs = {r[0] for r in results}
    expected_reqs = {"Q1", "Q2", "Q3", "Q4", "Q5", "CS9", "CS10"}
    missing_reqs = expected_reqs - seen_reqs
    
    if missing_reqs:
        for req in sorted(missing_reqs):
            print(f"CHECK {req} fixtures:NOT_MET no fixtures found")
            all_passed = False
    
    if all_passed:
        print("RESULT:MET")
        return 0
    else:
        print("RESULT:NOT_MET")
        return 1


if __name__ == "__main__":
    sys.exit(main())
