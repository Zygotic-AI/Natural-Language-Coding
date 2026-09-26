"""Landmine: release infer pure planning rules."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from nlc_release_tags import parse_semver  # noqa: E402
from nouns.release_infer import (  # noqa: E402
    plan_next_release_target,
    plan_prepare_action,
    plan_target_version,
)

BOUNDARY = "bba-emit"


def main() -> int:
    target, bump, _ = plan_target_version("0.2.0", "0.2.0", "patch")
    if target != "0.2.1" or bump != "patch":
        print("ASSERT:FAIL plan_target_version patch bump")
        return 1

    target2, bump2, _ = plan_target_version("0.2.0", "0.2.1", "patch")
    if target2 != "0.2.1" or bump2 != "keep":
        print("ASSERT:FAIL plan_target_version keep when file ahead")
        return 1

    next_t, next_b, _ = plan_next_release_target("0.2.0", "0.2.0")
    if next_t == "0.2.0":
        print("ASSERT:FAIL plan_next must not re-offer shipped 0.2.0")
        return 1
    if parse_semver(next_t) <= parse_semver("0.2.0"):
        print("ASSERT:FAIL plan_next must be after shipped")
        return 1

    action, _ = plan_prepare_action("feature/x", "0.2.1", "release/v0.2.1", lambda n: False)
    if action != "create_release_from_head":
        print("ASSERT:FAIL create when no release branch")
        return 1

    action2, _ = plan_prepare_action(
        "feature/x", "0.2.1", "release/v0.2.1", lambda n: n == "release/v0.2.1"
    )
    if action2 != "merge_into_release":
        print("ASSERT:FAIL merge when release branch exists")
        return 1

    action3, _ = plan_prepare_action(
        "release/v0.2.1", "0.2.1", "release/v0.2.1", lambda n: True
    )
    if action3 != "stay":
        print("ASSERT:FAIL stay on release line")
        return 1

    print("ASSERT:PASS release infer planning (zero-parameter)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
