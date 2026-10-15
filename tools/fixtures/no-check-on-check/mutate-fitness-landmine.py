"""Known-bad Candidate for C4: mutates a fitness tool and asserts the gate turns red."""

from pathlib import Path

target = Path("tools/fitness-hub-own-property-exit.py")
target.write_text("# mutated fitness tool — check-on-check landmine\n", encoding="utf-8")
print("mutated", target, "expect gate red")
