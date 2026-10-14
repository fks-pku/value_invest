"""Question-first answer rules and review consistency; no renderer or provider."""

ANSWER_PROTOCOL = "direct-answer-v1"
ANSWER_RULES = """先把当前问题当成用户单独提出的问题来回答。
开头给实质答案：是什么就解释对象，谁就列清人群，如何就说明过程，多少就给口径和数值，
比较就给同维度差异，是否/为什么就给判断及原因。按问题选择展开方式，不套统一投资段落。
覆盖题目中每一个实质提问；提供理解答案所需的定义、具体事实、例子、日期和适用条件。
依据紧跟事实，区分已实现、计划、预测和未知；关键限制随对应答案出现。
查不到时明确哪一部分无法回答、已知什么及原因，不能用方法论或“需进一步验证”替代已知答案。
先完成本题，再简短说明对父问题的意义；父题背景只能消歧，不能把本题偷换成投资价值或采购判断。
自然段、小标题、清单、对比表按信息需要使用，不固定段数、字数或材料数。
正文是给读者的回答，不叙述搜索步骤、验收过程或“本题到此停止”；研究状态留在内部记录。
公共正文只呈现当前最准确的答案：关键事实或数字、必要的计算或因果、会改变判断的限制。
这适用于整棵问题树的父节点、叶节点和每个小标题。每段应直接回答当前问题的一部分；
父节点综合回答父问题，不逐条复述子题限制。证据适用范围的细节留在对应数据行或审计，
只有改变判断的缺口、反证和决定性假设在对应答案旁简短出现一次。
按信息价值压缩段落；同一事实和限制只在最相关的位置解释一次，不为了显示研究过程而重复。
默认先提供读者要的信息。回答“为什么”时，围绕实际任务、机制和因果展开；
不要用一串“不能据此”“不等于”代替正面解释。只有某个限制会实质改变本题答案，
才在对应事实旁简短说明；其它限制留在证据审计或更相关的数量、替代与风险问题中。
修订前写过什么、这次补了什么、原稿漏了什么留在版本和复核记录，不写进标题、核心观点或论证。
不要用“本报告此前”“本轮检索”“本题的准确答案”“对父问题的意义”等编辑或工作流措辞；
必要的来源归属直接写来源及其主张，推算值直接标明输入、公式和情景性质。
充分性按原题完整范围判断；不能自行缩窄为容易确认的小结论后宣布通过。"""


def answer_contract() -> dict:
    return {"protocol": ANSWER_PROTOCOL, "standalone_answer_first": True,
            "preserve_full_question_scope": True, "review_required": True,
            "rule": ANSWER_RULES}


def validate_answer_review(node: dict) -> None:
    """Require review tied to visible prose; GPT still judges semantic coverage."""
    review = node.get("answer_review")
    comparison = review.get("draft_comparison") if isinstance(review, dict) else None
    comparison_valid = isinstance(comparison, str) and bool(comparison.strip())
    if isinstance(comparison, dict):
        groups = [comparison.get(key, []) for key in ("retained", "corrected", "omitted")]
        comparison_valid = (any(groups) and all(isinstance(group, list) for group in groups)
                            and all(isinstance(item, str) and item.strip() for group in groups for item in group))
    if (not isinstance(review, dict) or review.get("question") != node["question"]
            or not isinstance(review.get("coverage"), list) or not review["coverage"]
            or not comparison_valid):
        raise ValueError(f"{node['id']} 缺少针对完整原题的回答复核。")
    lead = review.get("direct_answer_excerpt")
    if not isinstance(lead, str) or not lead.strip() or lead not in node["conclusion"]:
        raise ValueError(f"{node['id']} 的直接答案复核必须引用当前核心观点。")
    main = [node["conclusion"]]
    for section in node["analysis"]:
        if not section.get("supplementary"):
            main.extend(section["paragraphs"])
            main.extend(str(cell) for table in section.get("tables", []) for row in table["rows"] for cell in row)
    main.extend(str(cell) for table in node.get("tables", []) for row in table["rows"] for cell in row)
    for item in review["coverage"]:
        if not isinstance(item, dict) or not str(item.get("requirement", "")).strip():
            raise ValueError(f"{node['id']} 的回答复核缺少具体提问要求。")
        excerpt = item.get("answer_excerpt")
        if item.get("status") == "answered":
            if not isinstance(excerpt, str) or not excerpt.strip() or not any(excerpt in text for text in main):
                raise ValueError(f"{node['id']} 的已回答要点没有出现在正文。")
        elif item.get("status") == "unresolved":
            gap = item.get("gap")
            if node["passed"] or not gap or gap not in node["gaps"]:
                raise ValueError(f"{node['id']} 尚有未回答要点，不能宣称充分。")
        else:
            raise ValueError(f"{node['id']} 的回答覆盖状态无效。")
