# IMA 每日研报资料流

## 目标

把 IMA 知识库 `环球研报直通车` 中每日新增的报告，转成可审计的研究更新：

```text
逐层枚举年度 / 月份 / 日期目录
-> 记录当天全部 PDF 候选
-> 判断与哪个 BOM 相关
-> 下载相关原文并核验 PDF 实际发布日期
-> 按 source/ima/<published_at>/ 归档
-> 对该项目的每个候选问题分别解析
-> GPT 复核原子观点
-> 追加时间账本
-> 重建 Markdown 问题时间线与最新结论
```

发现报告不等于获得证据。未经问题化解析和复核的材料只停留在 inbox。

## 访问配置

IMA 凭证只允许放在环境变量或本机配置目录：

```text
IMA_OPENAPI_CLIENTID
IMA_OPENAPI_APIKEY
IMA_KNOWLEDGE_BASE_ID        # 可选；系统也可按名称解析
```

也支持 IMA 官方技能使用的本机文件：

```text
~/.config/ima/client_id
~/.config/ima/api_key
```

凭证、原始知识库 ID 和短期签名下载链接不得进入 Git。

## 活跃项目

`config/active_research_feeds.json` 只登记需要每天更新的实时项目。每个项目
在自己的 `project.json` 中定义：

- `bom_node_id`
- `question_labels`
- `material_relevance_profile`
- `refresh_cadence`

历史回测项目不得进入该列表。需要持续跟踪时，先建立 `live_prediction` 后继项目。

每个 BOM 项目必须自包含：

```text
research/bom/<bom_project_id>/
  project.json
  professional_report.md
  source/ima/YYYY/MM/DD/
  material_intake/
  inbox/
  ledger/
```

原文只保存在该 BOM 的 `source/` 下。`material_intake/` 只保存候选、扫描、
路由和去重元数据，不再保存另一份 `raw` 原文。

## 每日发现

```bash
PYTHONPATH=src python3 -m value_invest_research \
  scan-active-ima-materials
```

系统会：

1. 按名称定位知识库；
2. 用 `get_knowledge_list` 逐层枚举年度、月份和日期文件夹，并完整翻页；
3. 把每个 PDF 记录到 `material_intake/directory_candidates.jsonl`；
4. 使用项目的 BOM 相关性 profile 形成 `relevant`、`not_relevant` 或
   `needs_review` 决策，模糊项允许 GPT 写入 `relevance_reviews.jsonl`；
5. 按 IMA `media_id` 去重，只下载 `relevant` 原文；
6. 从 PDF 首页核验报告实际发布日期；
7. 将原文保存到项目的 `source/ima/<published_at>/`；
8. 为该项目的每个候选问题生成一个独立解析任务。

日常任务默认回看最近三天，以覆盖延迟上传；首次回填使用：

```bash
PYTHONPATH=src python3 -m value_invest_research \
  scan-active-ima-materials \
  --full-backfill
```

目录日期是 IMA 的归档位置，`published_at` 是报告真正发布时间；二者分别保存，
不能用目录日期、IMA 上传时间、更新时间或扫描时间覆盖报告日期。发布日期的
取值顺序是：原文封面/页眉核验、明确的 provider publication 字段、标题日期；
同时保存 `publication_date_status`、`publication_date_source` 和页码/章节。
日期尚未核验时，`published_at` 留空，材料只能用于日期核验，不能进入公开时间线
或历史回测证据。

关键词搜索命中只证明“知识库里存在这份材料”，不证明材料属于哪一个日目录，
因此仍标记为 `pending_directory_reconciliation`。但本地目录不按 IMA 归档日
组织：只要 `published_at` 可用，就保存到对应发布日期目录；只有发布日期未知时
才暂存于 `source/ima/unmapped/<source_id>/`。

独立 BOM 五问项目的任务位于：

```text
inbox/materials.jsonl
inbox/parse_tasks.jsonl
```

## 问题化解析

每个 `source x lens` 任务单独回答当前问题。研报使用
`industry-report-analysis`，长材料可用 DeepSeek 做第一轮字段提取，GPT 负责：

1. 核对原文位置与数字；
2. 区分报告事实、分析师预测和分析师观点；
3. 判断该信息支持、反驳还是仅提示当前问题；
4. 保存 `published_at`、`effective_period`、`target_period`、`ingested_at`；
5. 不相关的问题写任务审阅结果，但不生成公共时间线行。

通过复核的观点写入待应用 claims JSONL；每行至少包含：

```json
{
  "lens_id": "demand",
  "source_id": "SRC-...",
  "published_at": "2026-07-24",
  "material_class": "sell_side_research",
  "ingestion_channel": "knowledge_base_scan",
  "source_title": "报告标题",
  "source_url": "可审计来源链接",
  "source_location": "第 12 页 / 图 8",
  "statement": "只回答当前问题的具体数据、预测或观点",
  "claim_type": "forecast",
  "stance": "support",
  "effective_period": "2026Q2",
  "target_period": "2027"
}
```

结论更新单独写入 conclusions JSONL，不能用报告摘要直接覆盖原结论。

公共 Markdown 的每个问题使用：

```text
| 时间 | 信息类型 | Source | 观点列表 |
```

同一份报告在同一问题中只占一行；该报告针对当前问题的所有原子观点组成列表，
每条观点保留页码或章节定位。`Source` 优先链接项目内已下载的 PDF。

## 应用更新

```bash
PYTHONPATH=src python3 -m value_invest_research \
  apply-standalone-bom-updates \
  research/bom/gpu_asic_bom_live \
  --claims <reviewed_claims.jsonl> \
  --conclusions <reviewed_conclusions.jsonl>
```

该命令验证并合并账本，再重建 `professional_report.md`。时间线由近及远，
公开报告不显示 IMA 查询词、API 信息、解析提示词或内部任务状态。
