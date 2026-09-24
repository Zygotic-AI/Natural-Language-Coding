"""Friendly CLI messages when required arguments are missing (ADR 0018)."""

from __future__ import annotations

from nouns.human_gap import emit_gap

BOUNDARY = "bba-emit"


def help_new() -> int:
    return emit_gap(
        "I can't start a new app without knowing where to put it.",
        missing=["folder path for the new app"],
        ask="Which folder should we use?",
        choices=[
            "New empty folder → ./nlc new <folder> --name MyApp",
            "You already have code → ./nlc adopt-existing .",
        ],
        examples=["./nlc new ~/projects/my-app --name MyApp"],
    )


def help_pack() -> int:
    return emit_gap(
        "I need to know whether you're exporting or installing a requirement pack.",
        ask="Export a pack you ratified, or install one someone sent you?",
        choices=["export", "install"],
        examples=[
            "./nlc pack export --name my-pack --version 1.0.0",
            "./nlc pack install dist/pack-my-pack-1.0.0.tar.gz",
        ],
    )


def help_pack_export() -> int:
    return emit_gap(
        "Export needs a pack name and version.",
        missing=["--name", "--version"],
        examples=["./nlc pack export --name company-payments --version 1.0.0"],
    )


def help_pack_install() -> int:
    return emit_gap(
        "Install needs the pack file you received.",
        missing=["path to .tar.gz"],
        examples=["./nlc pack install dist/pack-company-payments-1.0.0.tar.gz"],
    )


def help_regen_plan() -> int:
    return emit_gap(
        "Regen planning needs what changed.",
        missing=["--change kind:id"],
        ask="Agents usually run this — are you maintaining the repo?",
        examples=[
            "./nlc maintainer regen-plan --change rule:my-rule --orchestrate --write-queue",
        ],
        machine="NLC:NOT_MET",
    )
