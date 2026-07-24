from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from value_invest_research.adapters.outbound.filesystem_material_intake import (  # noqa: E402
    FileSystemMaterialIntakeRepository,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Keep IMA search hits under source/ima/unmapped until a dated "
            "directory scan or review verifies their archive location."
        )
    )
    parser.add_argument("project_dir")
    parser.add_argument(
        "--reviews",
        default="material_intake/directory_location_reviews.jsonl",
    )
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    documents = _read_jsonl(
        project_dir / "material_intake" / "documents.jsonl"
    )
    reviews = {
        str(row.get("source_id") or ""): row
        for row in _read_jsonl(project_dir / args.reviews)
        if str(row.get("source_id") or "")
    }
    repository = FileSystemMaterialIntakeRepository(project_dir)
    counts = {
        "verified": 0,
        "pending_directory_reconciliation": 0,
        "moved_originals": 0,
        "non_ima_skipped": 0,
    }

    for document in documents:
        if str(document.get("provider") or "") != "ima":
            counts["non_ima_skipped"] += 1
            continue
        source_id = str(document.get("source_id") or "")
        review = reviews.get(source_id)
        if review:
            status = "verified"
            directory_date = str(review.get("directory_date") or "")
            directory_path = str(review.get("directory_path") or "")
        elif document.get("directory_date") and document.get("directory_path"):
            status = "verified"
            directory_date = str(document["directory_date"])
            directory_path = str(document["directory_path"])
        else:
            status = "pending_directory_reconciliation"
            directory_date = ""
            directory_path = ""
        local_path = repository.update_directory_location(
            source_id=source_id,
            directory_date=directory_date,
            directory_path=directory_path,
            directory_mapping_status=status,
        )
        counts[status] += 1
        counts["moved_originals"] += bool(local_path)

    print(json.dumps(counts, ensure_ascii=False, sort_keys=True))
    return 0


def _read_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    return [
        payload
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
        for payload in [json.loads(line)]
        if isinstance(payload, dict)
    ]


if __name__ == "__main__":
    raise SystemExit(main())
