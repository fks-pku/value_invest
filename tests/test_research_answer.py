from copy import deepcopy

import pytest

from value_invest_research.domain.research_answer import validate_answer_review


def answer():
    return {"id": "Q1", "question": "产品是什么，谁能使用？", "passed": True, "gaps": [],
            "conclusion": "它是邮件助理，面向美国成年用户。",
            "analysis": [{"paragraphs": ["网页已开放，手机版仍待发布。"]}],
            "answer_review": {"question": "产品是什么，谁能使用？",
                              "direct_answer_excerpt": "它是邮件助理，面向美国成年用户。",
                              "coverage": [{"requirement": "产品用途", "status": "answered", "answer_excerpt": "邮件助理"},
                                           {"requirement": "使用者与入口", "status": "answered", "answer_excerpt": "网页已开放，手机版仍待发布。"}],
                              "draft_comparison": "保留用途与年龄、地区、入口限制；删除无关上层投资推断。"}}


def test_review_can_match_a_complete_answer():
    validate_answer_review(answer())


def test_draft_comparison_accepts_meaningful_structured_review():
    node = answer()
    node["answer_review"]["draft_comparison"] = {
        "retained": ["保留用途、人群与入口。"], "corrected": [], "omitted": []}
    validate_answer_review(node)
    for invalid in ({}, {"retained": []}, {"corrected": [""]}, {"retained": "未按项目列出"}):
        node["answer_review"]["draft_comparison"] = invalid
        with pytest.raises(ValueError, match="回答复核"):
            validate_answer_review(node)


def test_unresolved_part_prevents_false_pass_but_allows_honest_partial_answer():
    node = answer()
    node["answer_review"]["coverage"][1] = {"requirement": "开放对象", "status": "unresolved", "gap": "未查明开放地区"}
    with pytest.raises(ValueError, match="尚有未回答要点"):
        validate_answer_review(node)
    node.update(passed=False, gaps=["未查明开放地区"])
    validate_answer_review(node)


@pytest.mark.parametrize("fault", ["missing", "other_question", "stale_excerpt", "supplement_only", "evidence_only"])
def test_review_must_address_current_question_in_main_answer(fault):
    node = deepcopy(answer())
    if fault == "missing":
        node.pop("answer_review")
    elif fault == "other_question":
        node["answer_review"]["question"] = "产品是否会拉动投资？"
    elif fault == "stale_excerpt":
        node["answer_review"]["direct_answer_excerpt"] = "过期答案"
    elif fault == "supplement_only":
        node["analysis"][0]["supplementary"] = True
    else:
        node["evidence"] = [{"fact": node["analysis"][0]["paragraphs"][0]}]
        node["analysis"] = []
    with pytest.raises(ValueError):
        validate_answer_review(node)
