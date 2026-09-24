"""Landmine ADR 0014/0015: hermetic store upgrade 0.1.0 → 0.1.1 via nlc-update."""

from __future__ import annotations

BOUNDARY = "bba-emit"

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    sys.path.insert(0, str(ROOT / "tools"))
    from nlc_distribution import (
        copy_tree_into_version,
        install_hub_from_path,
        read_hub_version,
        read_project_lock,
    )

    with tempfile.TemporaryDirectory(prefix="nlc-up-") as tmp:
        work = Path(tmp)
        store = work / "store"
        app = work / "app"
        store.mkdir()
        hub_from = work / "hub-from"
        shutil.copytree(
            ROOT,
            hub_from,
            ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv", "node_modules"),
        )
        ver_from = "0.1.0"
        (hub_from / "integrity" / "nlc-version.json").write_text(
            json.dumps({"version": ver_from}, indent=2) + "\n",
            encoding="utf-8",
        )
        install_hub_from_path(store, hub_from)

        hub_next = work / "hub-next"
        shutil.copytree(
            hub_from,
            hub_next,
            ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv", "node_modules"),
        )
        (hub_next / "integrity" / "nlc-version.json").write_text(
            json.dumps({"version": "0.1.1"}, indent=2) + "\n",
            encoding="utf-8",
        )
        copy_tree_into_version(hub_next, store, "0.1.1")

        env = os.environ.copy()
        env["NLC_HUB"] = str(store / "hub")
        init = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "nlc-init.py"), str(app), "--name", "UpTest"],
            cwd=str(ROOT),
            env=env,
            capture_output=True,
            text=True,
        )
        if init.returncode != 0:
            print("ASSERT:FAIL nlc-init", init.stderr)
            return 1

        lock = read_project_lock(app)
        lock["store"] = "path"
        lock["store_path"] = str(store)
        lock_path = app / ".nlc" / "lock.json"
        lock_path.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")

        upd = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "nlc-update.py"),
                "--project",
                str(app),
                "--to",
                "0.1.1",
                "--install-root",
                str(store),
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        out = (upd.stdout or "") + (upd.stderr or "")
        if upd.returncode != 0:
            print("ASSERT:FAIL nlc-update hermetic")
            print(out[-1200:])
            return 1
        if "UPGRADE:MET" not in out and "UPGRADE:STEP" not in out:
            print("ASSERT:FAIL missing UPGRADE log lines")
            print(out[-800:])
            return 1
        after = read_project_lock(app)
        if str(after.get("hub")) != "0.1.1":
            print(f"ASSERT:FAIL lock hub not 0.1.1: {after}")
            return 1

    print("ASSERT:PASS hermetic nlc-update 0.1.0→0.1.1")
    return 0


