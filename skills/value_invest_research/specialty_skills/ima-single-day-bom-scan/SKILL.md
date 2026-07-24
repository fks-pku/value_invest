---
name: ima-single-day-bom-scan
description: 扫描 IMA 环球研报直通车中指定单日目录，按当前独立 BOM 的相关性筛选 PDF，下载原文，核验报告实际发布日期，并写入材料账本和解析任务。用户提到“扫描某天 IMA”“把当天研报纳入当前 BOM”“按 PDF 实际发布日期归档”时使用。
---

# IMA 单日 BOM 扫描

## 目标

只扫描一个 IMA 归档日，把与当前独立 BOM 相关的 PDF 下载到项目内。IMA 目录日期仅表示材料被归档到哪一天；本地 `source/ima/YYYY/MM/DD` 必须使用报告实际发布日期。

## 前提

- 当前目录位于 Value Invest Research 仓库。
- 目标是一个 `report_scope=standalone-bom` 的 BOM 项目。
- IMA 凭据只从 `IMA_OPENAPI_CLIENTID`、`IMA_OPENAPI_APIKEY`、`IMA_KNOWLEDGE_BASE_ID` 或用户主目录私密配置读取，绝不写入 Git。
- 默认知识库名称为 `环球研报直通车`。

## 工作流

1. 确认目标 BOM 项目和唯一扫描日期 `YYYY-MM-DD`。
2. 阅读该项目 `project.json` 的 `material_relevance_profile`，理解核心术语、相关公司、上下文、供应环节和排除项。
3. 运行 `scripts/scan_ima_day.py`。脚本强制 `start_date=end_date`，不会扩展为多日扫描。
4. 检查 `material_intake/directory_candidates.jsonl`：
   - `relevant` 进入材料账本并下载；
   - `needs_review` 由 GPT 根据当前 BOM 边界复核；
   - 明显与 BOM 无关的材料保持 `not_relevant`。
5. 若复核改变相关性，使用项目 CLI 写入 relevance review，再重跑同一天。重复扫描会重试尚未成功下载的原文。
6. 下载后读取 PDF 前三页：
   - 原文明确日期：标记 `verified`，用该日期归档；
   - 原文不可提取但标题带 `YYMMDD`：保留 `inferred_from_title`，按标题日期归档并在结果中披露；
   - 两者都没有：保留在 `source/ima/unmapped/<source_id>/`，不得进入研究时间线。
7. 汇报候选数、相关数、待复核数、下载成功数、PDF 核验日期数、标题推断日期数和日期缺口。

## 日期约束

- `directory_date`：IMA 归档目录日，只用于来源追溯。
- `published_at`：报告实际发布日期，用于本地目录、时间线和回测可见性。
- `discovered_at`：系统扫描日。
- 不得用 `directory_date`、IMA 创建时间或下载时间填充 `published_at`。

## 执行

```bash
python3 skills/value_invest_research/specialty_skills/ima-single-day-bom-scan/scripts/scan_ima_day.py \
  research/bom/<bom-project> \
  --date YYYY-MM-DD
```

若项目 Python 环境不是当前解释器，使用安装了仓库依赖的 Python 执行脚本。

## 完成标准

- 扫描事件的开始和结束日期完全相同。
- 所有下载文件位于目标 BOM 项目内部。
- 日期目录不使用 IMA 归档日冒充报告发布日期。
- 每份相关材料均产生窄化到当前 BOM 问题的待解析任务。
- API 配额、下载失败或日期不可核验时明确报告，不伪造完成。
