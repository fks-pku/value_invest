import json
from pathlib import Path
import shutil
import tempfile

import pytest

from value_invest_research.adapters.outbound.filesystem_interactive_research import (
    FileSystemInteractiveResearch, hashes, project_files, read, rows, write,
)
from value_invest_research.domain.interactive_research import tree_version
from value_invest_research.domain.passage_comments import propose_passage_comment, validate_passage_result


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "research/events/gpt6_ai_industry_impact_20260910"


def comment_request(tree):
    original = next(n for n in tree["nodes"] if n["id"] == "F1.1.3")["analysis"][0]["paragraphs"][0]
    return {"version": tree_version(tree), "node_id": "F1.1.3", "section": 0,
            "paragraph": 0, "quote": original[:18], "comment": "这一数字的原始依据是什么？"}


def researched_result():
    return {"status": "ready", "replacement": "9月9日发布的原始价格表列出了这一口径；按其数字计算，任务成本仍需结合输出量判断。[1]",
            "change_note": "补充原始价目与计算口径。", "search_queries": ["official model pricing September 2026"],
            "refutation_result": "核对了只看输入单价的反向解释；输出量会改变总成本。",
            "sources": [{"title": "Official pricing", "url": "https://example.com/original-pricing",
                         "publisher": "Example Research", "published_at": "2026-09-09",
                         "material_class": "official_company", "locator": "Pricing table, row 2",
                         "fact": "该价格表列出输入与输出单价。", "boundary": "价目并非实际任务总成本。",
                         "effect": "support", "review": "打开原价目表并逐项核对输入、输出栏及发布日期。"}]}


@pytest.fixture
def project_repository(tmp_path, monkeypatch):
    project = tmp_path / "project"
    for name, path in project_files(PROJECT).items():
        destination = project / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
    original = tempfile.mkdtemp
    monkeypatch.setattr("value_invest_research.adapters.outbound.filesystem_interactive_research.tempfile.mkdtemp",
                        lambda **kwargs: original(dir=tmp_path, **kwargs))
    return FileSystemInteractiveResearch(project)


def test_comment_anchor_is_one_current_leaf_paragraph(project_repository):
    tree = project_repository.tree()
    request = comment_request(tree)
    proposal = propose_passage_comment(tree, request)
    assert proposal["target"]["original"].startswith(request["quote"])
    assert proposal["affected_ids"] == ["F1.1.3"]
    with pytest.raises(ValueError, match="重新选中"):
        propose_passage_comment(tree, {**request, "version": "old"})
    with pytest.raises(ValueError, match="不一致"):
        propose_passage_comment(tree, {**request, "quote": "完全不在原段中的文字"})
    with pytest.raises(ValueError, match="L3"):
        propose_passage_comment(tree, {**request, "node_id": "F1"})


def test_comment_result_requires_dated_cited_evidence(project_repository):
    original = propose_passage_comment(project_repository.tree(), comment_request(project_repository.tree()))["target"]["original"]
    ready = researched_result()
    assert validate_passage_result(ready, original=original, as_of_date="2026-09-10") == ready
    late = json.loads(json.dumps(ready))
    late["sources"][0]["published_at"] = "2026-09-11"
    with pytest.raises(ValueError, match="晚于"):
        validate_passage_result(late, original=original, as_of_date="2026-09-10")
    undated = json.loads(json.dumps(ready))
    undated["sources"][0]["published_at"] = "2026-09"
    with pytest.raises(ValueError, match="完整发布日期"):
        validate_passage_result(undated, original=original, as_of_date="2026-09-10")
    uncited = {**ready, "replacement": "这个说法需要重新核实，暂时只能给条件判断。"}
    with pytest.raises(ValueError, match="逐一引用"):
        validate_passage_result(uncited, original=original, as_of_date="2026-09-10")


def test_comment_publishes_only_selected_paragraph_and_its_evidence(project_repository):
    repository = project_repository
    before_tree = repository.tree()
    proposal = propose_passage_comment(before_tree, comment_request(before_tree))
    job = repository.prepare(proposal)
    baseline = hashes(repository.project)
    write(Path(job["workspace"]) / "comment_result.json", researched_result())
    result = repository.validate_and_publish_comment(job)
    assert result["status"] == "ready"
    after_tree = repository.tree()
    before_nodes = {n["id"]: n for n in before_tree["nodes"]}
    after_nodes = {n["id"]: n for n in after_tree["nodes"]}
    for node_id in before_nodes.keys() - {"F1.1.3"}:
        assert after_nodes[node_id] == before_nodes[node_id]
    before_node, after_node = before_nodes["F1.1.3"], after_nodes["F1.1.3"]
    assert after_node["conclusion"] == before_node["conclusion"]
    assert after_node["passed"] == before_node["passed"]
    assert after_node["analysis"][0]["paragraphs"][1:] == before_node["analysis"][0]["paragraphs"][1:]
    assert "原始价格表" in after_node["analysis"][0]["paragraphs"][0]
    assert len(after_node["evidence"]) == len(before_node["evidence"]) + 1
    assert len(rows(repository.project / "source_extractions.jsonl")) > len(rows(Path(job["audit_dir"]) / "before/source_extractions.jsonl"))
    assert "原始价格表" in (repository.project / "professional_report.html").read_text()
    assert "原始价格表" in (repository.project / "professional_report.md").read_text()
    assert read(Path(job["audit_dir"]) / "publication.json")["committed"]
    assert hashes(repository.project) != baseline


def test_comment_insufficient_or_mutated_stage_keeps_original(project_repository):
    repository = project_repository
    proposal = propose_passage_comment(repository.tree(), comment_request(repository.tree()))
    job = repository.prepare(proposal)
    baseline = hashes(repository.project)
    write(Path(job["workspace"]) / "comment_result.json",
          {"status": "needs_full_research", "reason": "新证据会改变核心结论。"})
    assert repository.validate_and_publish_comment(job)["status"] == "needs_full_research"
    assert hashes(repository.project) == baseline
    write(Path(job["workspace"]) / "project/target_gates.json", {"forged": True})
    with pytest.raises(ValueError, match="修改了项目副本"):
        repository.validate_and_publish_comment(job)
    assert hashes(repository.project) == baseline
