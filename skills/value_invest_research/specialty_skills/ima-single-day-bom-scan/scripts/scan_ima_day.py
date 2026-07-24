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
            "Scan one IMA archive day for a standalone BOM and archive "
            "downloaded PDFs by their actual publication dates."
        )
    )
    parser.add_argument("project_dir")
    parser.add_argument("--date", required=True, dest="scan_date")
    parser.add_argument(
        "--knowledge-base-name",
        default="环球研报直通车",
    )
    parser.add_argument(
        "--config",
        default="config/material_feeds.json",
    )
    parser.add_argument("--discovered-at", default=None)
    args = parser.parse_args()

    scan_date = date.fromisoformat(args.scan_date).isoformat()
    repo_root = _find_repo_root(Path.cwd())
    project_dir = (repo_root / args.project_dir).resolve()
    if not project_dir.is_dir():
        raise SystemExit(f"BOM project does not exist: {project_dir}")

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
        "scan-ima-materials",
        str(project_dir),
        "--knowledge-base-name",
        args.knowledge_base_name,
        "--config",
        str((repo_root / args.config).resolve()),
        "--start-date",
        scan_date,
        "--end-date",
        scan_date,
        "--discovered-at",
        args.discovered_at or date.today().isoformat(),
    ]
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
