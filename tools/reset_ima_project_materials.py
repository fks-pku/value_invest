#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
from typing import Any, Callable


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Remove IMA originals and IMA-derived intake state from one project."
    )
    parser.add_argument("project_dir")
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Confirm the destructive project-local reset.",
    )
    args = parser.parse_args()
    if not args.yes:
        raise SystemExit("Refusing to reset without --yes")

    project_dir = Path(args.project_dir).resolve()
    if not (project_dir / "project.json").is_file():
        raise SystemExit(f"Not a research project: {project_dir}")

    document_path = project_dir / "material_intake" / "documents.jsonl"
    documents = _read_jsonl(document_path)
    removed_source_ids = {
        str(row.get("source_id") or "")
        for row in documents
        if str(row.get("provider") or "") == "ima"
    }
    removed_source_ids.discard("")

    counts: dict[str, int] = {}
    counts["documents"] = _filter_jsonl(
        document_path,
        lambda row: str(row.get("provider") or "") != "ima",
    )
    for relative in (
        "inbox/materials.jsonl",
        "inbox/parse_tasks.jsonl",
        "ledger/claims.jsonl",
        "sources.jsonl",
    ):
        path = project_dir / relative
        counts[relative] = _filter_jsonl(
            path,
            lambda row: (
                str(row.get("source_id") or "") not in removed_source_ids
                and str(row.get("provider") or "") != "ima"
            ),
        )

    for path in sorted((project_dir / "inbox").glob("reviewed_claims*.jsonl")):
        counts[str(path.relative_to(project_dir))] = _filter_jsonl(
            path,
            lambda row: (
                str(row.get("source_id") or "") not in removed_source_ids
                and str(row.get("provider") or "") != "ima"
            ),
        )

    conclusion_paths = [
        *(project_dir / "inbox").glob("reviewed_conclusions*.jsonl"),
        project_dir / "ledger" / "conclusions.jsonl",
    ]
    for path in conclusion_paths:
        counts[str(path.relative_to(project_dir))] = _filter_jsonl(
            path,
            lambda row: not (
                set(str(item) for item in row.get("source_ids") or [])
                & removed_source_ids
            ),
        )

    for relative in (
        "material_intake/directory_candidates.jsonl",
        "material_intake/directory_scan_events.jsonl",
        "material_intake/scan_events.jsonl",
        "material_intake/publication_date_reviews.jsonl",
        "material_intake/directory_location_reviews.jsonl",
        "material_intake/relevance_reviews.jsonl",
    ):
        path = project_dir / relative
        counts[relative] = _filter_jsonl(
            path,
            lambda row: (
                str(row.get("provider") or "") != "ima"
                and str(row.get("source_id") or "") not in removed_source_ids
            ),
        )

    state_path = project_dir / "material_intake" / "feed_state.json"
    state = _read_json(state_path)
    feeds = state.get("feeds") or {}
    removed_feeds = [
        key
        for key, value in feeds.items()
        if str((value or {}).get("provider") or "") == "ima"
        or str(key).startswith("ima:")
    ]
    for key in removed_feeds:
        feeds.pop(key, None)
    state["feeds"] = feeds
    _write_json(state_path, state)
    counts["feed_state"] = len(removed_feeds)

    source_dir = project_dir / "source" / "ima"
    removed_files = (
        sum(path.is_file() for path in source_dir.rglob("*"))
        if source_dir.exists()
        else 0
    )
    if source_dir.exists():
        shutil.rmtree(source_dir)
    source_dir.mkdir(parents=True, exist_ok=True)
    counts["source_files"] = removed_files

    print(
        json.dumps(
            {
                "project_dir": str(project_dir),
                "removed_source_ids": len(removed_source_ids),
                "counts": counts,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def _filter_jsonl(
    path: Path,
    keep: Callable[[dict[str, Any]], bool],
) -> int:
    if not path.exists():
        return 0
    rows = _read_jsonl(path)
    kept = [row for row in rows if keep(row)]
    removed = len(rows) - len(kept)
    _write_jsonl(path, kept)
    return removed


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = "".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n"
        for row in rows
    )
    path.write_text(payload, encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    raise SystemExit(main())
