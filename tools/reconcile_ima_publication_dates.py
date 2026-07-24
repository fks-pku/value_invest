from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re
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
            "Reconcile IMA publication dates without treating archive or "
            "provider upload dates as report publication dates."
        )
    )
    parser.add_argument("project_dir")
    parser.add_argument(
        "--reviews",
        default="material_intake/publication_date_reviews.jsonl",
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
        "inferred_from_title": 0,
        "needs_pdf_verification": 0,
        "non_ima_skipped": 0,
    }

    for document in documents:
        if str(document.get("provider") or "") != "ima":
            counts["non_ima_skipped"] += 1
            continue
        source_id = str(document.get("source_id") or "")
        review = reviews.get(source_id)
        if review:
            status = str(review.get("publication_date_status") or "verified")
            repository.update_publication_date(
                source_id=source_id,
                published_at=str(review.get("published_at") or ""),
                publication_date_status=status,
                publication_date_source=str(
                    review.get("publication_date_source")
                    or "manual_verification"
                ),
                publication_date_locator=str(
                    review.get("publication_date_locator") or ""
                ),
            )
            counts[status] += 1
            continue
        title_date = _date_from_title(str(document.get("title") or ""))
        if title_date:
            repository.update_publication_date(
                source_id=source_id,
                published_at=title_date,
                publication_date_status="inferred_from_title",
                publication_date_source="title_suffix",
            )
            counts["inferred_from_title"] += 1
            continue
        repository.update_publication_date(
            source_id=source_id,
            published_at="",
            publication_date_status="needs_pdf_verification",
            publication_date_source="unknown",
        )
        counts["needs_pdf_verification"] += 1

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


def _date_from_title(title: str) -> str:
    for raw in reversed(re.findall(r"(?<!\d)(\d{6})(?!\d)", title)):
        try:
            return date(
                2000 + int(raw[:2]),
                int(raw[2:4]),
                int(raw[4:6]),
            ).isoformat()
        except ValueError:
            continue
    return ""


if __name__ == "__main__":
    raise SystemExit(main())
