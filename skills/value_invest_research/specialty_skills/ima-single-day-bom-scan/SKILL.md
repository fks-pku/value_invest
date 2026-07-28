---
name: ima-single-day-bom-scan
description: 通过已登录的 IMA 可见界面逐层进入指定年月日目录，完整枚举当天全部 PDF，并逐项点击页面下载按钮，将原文登记到仓库级 source/ima/YYYY/MM/DD。用户提到“扫描某天 IMA”“鼠标下载 IMA”“下载当天全部研报”“补齐 IMA 中央归档”时必须使用；不要调用 IMA OpenAPI 或 API 下载命令。
---

# IMA 单日 UI 点击归档

## 目标

只处理一个 IMA `directory_date`。通过浏览器中可见的 IMA 页面逐项点击下载，
再把下载完成的 PDF 导入仓库级 `source/ima/YYYY/MM/DD`，同时维护
`archive_manifest.jsonl` 和 `archive_events.jsonl`。

这个技能只负责中央原始资料归档，不做 BOM 相关性筛选、项目复制、解析任务或
研究账本更新。

## 下载边界

- 使用用户已登录的 IMA 网页会话和浏览器控制能力。优先复用现有 IMA 标签页；
  没有现成标签页时打开 `https://ima.qq.com/`。
- 如果页面要求登录，停在登录页并请用户完成登录；不要读取 Cookie、令牌或本地
  登录数据。
- 每一份原文都必须由页面上可见的下载按钮触发。可以用唯一 DOM 定位器点击，
  DOM 不可靠时使用屏幕坐标点击。
- 不得调用 IMA OpenAPI、IMA MCP 下载技能、`archive-ima-day`、
  `archive-ima-daily`、`ImaKnowledgeBaseFeed`、`get_media_info`，也不得提取
  隐藏下载 URL 后直接请求文件。
- 不需要 IMA API 凭据。不要读取或输出 `IMA_OPENAPI_CLIENTID`、
  `IMA_OPENAPI_APIKEY`、`IMA_KNOWLEDGE_BASE_ID`。

## UI 枚举

1. 确认唯一日期 `YYYY-MM-DD` 和中央归档根目录。
2. 在 IMA 中进入 `环球研报直通车 -> 年 -> 月 -> 日`。
3. 从可见页面记录全部 PDF 标题。分页时逐页前进；无限滚动时持续滚动，直到
   连续两次到底后标题集合不再增长。
4. 返回上一页或翻页后重新观察页面状态再点击，不能复用已经失效的坐标。
5. 不做关键词搜索，不做 BOM 过滤。目录页出现的每一份 PDF 都进入候选清单。
6. 候选清单写入临时 JSON，格式如下：

```json
{
  "directory_date": "2026-07-27",
  "directory_path": "2026年国际顶级投行研报/7月/7.27",
  "candidates": [
    {"title": "报告标题.pdf"}
  ]
}
```

## 点击下载

1. 在开始点击前创建一个临时 marker 文件，并记录浏览器下载目录；默认使用
   `~/Downloads`。
2. 读取中央 `archive_manifest.jsonl`。同一 `directory_date + title` 已有
   `status=available` 且文件仍存在时计为复用，不重复点击。
3. 对其余候选逐项操作：
   - 定位该报告所在行或卡片；
   - 点击可见的“下载”按钮；若需要先打开详情或 PDF 预览，则进入后再点击预览
     页的可见下载按钮；
   - 观察浏览器下载事件或下载目录，确认 PDF 已完成写入；`.crdownload`、
     `.download`、`.part` 不算完成；
   - 返回目录页，重新获取页面状态，再处理下一份。
4. 同名下载产生 `文件名 (1).pdf` 时保留即可，导入步骤会与原标题匹配。
5. 登录失效、验证码、页面权限或 UI 限制出现时明确暂停；不要改用 API 绕过。

## 导入中央归档

页面点击结束后运行：

```bash
python3 skills/value_invest_research/specialty_skills/ima-single-day-bom-scan/scripts/register_ui_downloads.py \
  --date YYYY-MM-DD \
  --candidate-list /tmp/ima-ui-YYYY-MM-DD/candidates.json \
  --download-dir ~/Downloads \
  --download-marker /tmp/ima-ui-YYYY-MM-DD/download-start.marker
```

导入器只接受 marker 之后出现的匹配 PDF，校验 `%PDF` 文件头，复制原文，计算
SHA-256，并按 `directory_date + title` 与旧 API 失败记录对账。找不到的候选保留
为 `unavailable`，不能伪造成已归档。

最后运行：

```bash
PYTHONPATH=src python3 -m value_invest_research validate-ima-archive
```

## 完成标准

- 目标年月日与 IMA 可见目录完全一致。
- 已跨全部分页或完整滚动，候选数量来自 UI 全量枚举。
- 每个缺失候选都经过一次可见下载按钮点击。
- 所有完成文件位于 `source/ima/YYYY/MM/DD/`，且清单的路径、哈希、大小通过
  `validate-ima-archive`。
- 汇报候选数、UI 新下载数、复用数和失败数。
- `partial` 必须保留真实失败原因；不得因局部下载成功而报告完整完成。
