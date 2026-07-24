#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from value_invest_research.adapters.outbound.filesystem_standalone_bom_timeline import (  # noqa: E402
    FileSystemStandaloneBomTimelineRepository,
)
from value_invest_research.adapters.outbound.standalone_bom_markdown_renderer import (  # noqa: E402
    StandaloneBomMarkdownRenderer,
)
from value_invest_research.application.use_cases.refresh_standalone_bom_timeline import (  # noqa: E402
    refresh_standalone_bom_report,
)
from value_invest_research.domain.standalone_bom_timeline import (  # noqa: E402
    STANDALONE_LENSES,
    normalize_timeline_claim,
)


MATERIAL_CLASS_BY_LABEL = {
    "官方财报": "official_filing",
    "官方公司": "official_company",
    "研报": "sell_side_research",
    "第三方权威": "authoritative_third_party",
    "市场消息": "market_news",
    "专家观点": "expert_opinion",
    "其他": "other",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_project")
    parser.add_argument("target_project")
    parser.add_argument("--as-of-date", default=date.today().isoformat())
    args = parser.parse_args()

    source_dir = _resolve(args.source_project)
    target_dir = _resolve(args.target_project)
    source_project = json.loads(
        (source_dir / "project.json").read_text(encoding="utf-8")
    )
    source_markdown = (source_dir / "professional_report.md").read_text(
        encoding="utf-8"
    )
    source_rows = _read_jsonl(source_dir / "sources.jsonl")
    sources_by_url = {
        str(row.get("url") or "").strip(): row
        for row in source_rows
        if str(row.get("url") or "").strip()
    }
    profile, claims, conclusions = _parse_baseline(
        source_markdown,
        source_project=source_project,
        sources_by_url=sources_by_url,
        ingested_at=args.as_of_date,
    )

    target_dir.mkdir(parents=True, exist_ok=True)
    project = {
        **source_project,
        "project_id": target_dir.name,
        "title": str(source_project.get("title") or "独立 BOM 研究").replace(
            "投资研究",
            "实时跟踪",
        ),
        "run_mode": "live_prediction",
        "as_of_date": args.as_of_date,
        "generated_at": args.as_of_date,
        "status": "active",
        "material_feed_queries": [
            "GPU ASIC AI accelerator AI芯片 数据中心加速器",
            "NVIDIA AMD Broadcom TPU custom silicon CUDA",
        ],
        "refresh_cadence": "daily",
    }
    _write_json(target_dir / "project.json", project)
    _write_json(target_dir / "timeline_profile.json", profile)
    _write_jsonl(target_dir / "ledger" / "claims.jsonl", claims)
    _write_jsonl(target_dir / "ledger" / "conclusions.jsonl", conclusions)
    if (source_dir / "sources.jsonl").is_file():
        shutil.copy2(source_dir / "sources.jsonl", target_dir / "sources.jsonl")
    result = refresh_standalone_bom_report(
        repository=FileSystemStandaloneBomTimelineRepository(target_dir),
        renderer=StandaloneBomMarkdownRenderer(),
        as_of_date=args.as_of_date,
    )
    print(
        json.dumps(
            {
                "target_project": str(target_dir),
                "claims": len(claims),
                "conclusions": len(conclusions),
                **result,
            },
            ensure_ascii=False,
        )
    )
    return 0


def _parse_baseline(
    markdown: str,
    *,
    source_project: dict,
    sources_by_url: dict[str, dict],
    ingested_at: str,
) -> tuple[dict, list[dict], list[dict]]:
    source_as_of_date = str(source_project.get("as_of_date") or ingested_at)
    sections = {
        match.group("title").strip(): match.group("body")
        for match in re.finditer(
            r"^##\s+\d+\.\s+(?P<title>.+?)\s*$"
            r"(?P<body>.*?)(?=^##\s+\d+\.|\Z)",
            markdown,
            flags=re.MULTILINE | re.DOTALL,
        )
    }
    profile_lenses = []
    claims = []
    conclusions = []
    for lens_id, label in STANDALONE_LENSES:
        body = sections.get(label, "")
        logic = _between(
            body,
            "### 简单逻辑链",
            "### 信息时间线",
        )
        conclusion = _between(
            body,
            "### 最新结论与趋势",
            None,
        )
        profile_lenses.append(
            {
                "lens_id": lens_id,
                "label": label,
                "logic_chain": _collapse_paragraphs(logic),
                "baseline_conclusion": _collapse_paragraphs(conclusion),
            }
        )
        conclusions.append(
            {
                "lens_id": lens_id,
                "as_of_date": source_as_of_date,
                "conclusion": _collapse_paragraphs(conclusion),
                "trend": "历史截面迁移为实时跟踪基线。",
                "source_ids": [],
                "review_status": "migrated_verified_baseline",
            }
        )
        table = _between(body, "### 信息时间线", "### 最新结论与趋势")
        for cells in _markdown_rows(table):
            published_at, material_label, source_cell, statement = cells
            title, url, location = _parse_source_cell(source_cell)
            source = sources_by_url.get(url) or {}
            source_id = str(source.get("source_id") or "").strip() or _source_id(url, title)
            claims.append(
                normalize_timeline_claim(
                    {
                        "lens_id": lens_id,
                        "source_id": source_id,
                        "published_at": published_at,
                        "material_class": MATERIAL_CLASS_BY_LABEL.get(
                            material_label,
                            str(source.get("material_class") or "other"),
                        ),
                        "ingestion_channel": str(
                            source.get("ingestion_channel") or "manual_import"
                        ),
                        "source_title": title,
                        "source_url": url,
                        "source_location": location,
                        "statement": statement,
                        "claim_type": "opinion",
                        "stance": "neutral",
                        "review_status": "migrated_verified_baseline",
                    },
                    bom_node_id=str(source_project.get("bom_node_id") or ""),
                    ingested_at=ingested_at,
                )
            )
    return (
        {
            "schema_version": "1.0",
            "bom_node_id": source_project.get("bom_node_id"),
            "lenses": profile_lenses,
        },
        claims,
        conclusions,
    )


def _markdown_rows(table: str) -> list[list[str]]:
    rows = []
    for line in table.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 4 or cells[0] in {"时间", "---"}:
            continue
        if re.fullmatch(r"-+", cells[0]):
            continue
        rows.append(cells)
    return rows


def _parse_source_cell(cell: str) -> tuple[str, str, str]:
    match = re.search(r"\[([^\]]+)\]\((https?://[^)]+)\)", cell)
    if not match:
        return cell.strip(), "", ""
    title = match.group(1).strip()
    url = match.group(2).strip()
    location = (cell[: match.start()] + cell[match.end() :]).strip(" ，,")
    return title, url, location


def _between(text: str, start: str, end: str | None) -> str:
    if start not in text:
        return ""
    value = text.split(start, 1)[1]
    if end and end in value:
        value = value.split(end, 1)[0]
    return value.strip()


def _collapse_paragraphs(value: str) -> str:
    paragraphs = [
        " ".join(part.split())
        for part in re.split(r"\n\s*\n", value)
        if part.strip()
    ]
    return "\n\n".join(paragraphs)


def _source_id(url: str, title: str) -> str:
    digest = hashlib.sha256(f"{url}|{title}".encode("utf-8")).hexdigest()[:16]
    return f"SRC-MIGRATED-{digest.upper()}"


def _resolve(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def _read_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


if __name__ == "__main__":
    raise SystemExit(main())
