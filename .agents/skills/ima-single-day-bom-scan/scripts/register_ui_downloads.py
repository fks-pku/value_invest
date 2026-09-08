#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import date
import os
from pathlib import Path
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Register PDFs downloaded by visible IMA UI clicks in the "
            "workspace-level source/ima mirror."
        )
    )
    parser.add_argument("--date", required=True, dest="archive_date")
    parser.add_argument("--candidate-list", required=True)
    parser.add_argument("--download-dir", default="~/Downloads")
    parser.add_argument("--download-marker", default=None)
    parser.add_argument(
        "--config",
        default="config/ima_daily_archive.json",
    )
    parser.add_argument("--scanned-at", default=None)
    args = parser.parse_args()

    archive_date = date.fromisoformat(args.archive_date).isoformat()
    repo_root = _find_repo_root(Path.cwd())
    env = dict(os.environ)
    src_path = str(repo_root / "src")
    env["PYTHONPATH"] = (
        f"{src_path}{os.pathsep}{env['PYTHONPATH']}"
        if env.get("PYTHONPATH")
        else src_path
    )
    command = [
        sys.executable,
        "-m",
        "value_invest_research",
        "archive-ima-ui-day",
        "--date",
        archive_date,
        "--candidate-list",
        args.candidate_list,
        "--download-dir",
        args.download_dir,
        "--config",
        str((repo_root / args.config).resolve()),
        "--scanned-at",
        args.scanned_at or date.today().isoformat(),
    ]
    if args.download_marker:
        command.extend(["--download-marker", args.download_marker])
    completed = subprocess.run(command, cwd=repo_root, env=env, check=False)
    return int(completed.returncode)


def _find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").is_file() and (
            candidate / "src" / "value_invest_research"
        ).is_dir():
            return candidate
    raise SystemExit("Run this skill from inside the Value Invest Research repo")


if __name__ == "__main__":
    raise SystemExit(main())
