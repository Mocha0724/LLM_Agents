# 文献报告数据 Schema

`generate_report.py` 脚本接收 JSON 格式的输入数据，结构如下：

## JSON Schema

```json
{
  "topic": "世界模型",
  "topic_en": "World Models",
  "timeframe": "2026-04-21 ~ 2026-04-28",
  "report_date": "2026-04-28",
  "summary_zh": "本周世界模型领域共有 X 篇值得关注的新论文...",
  "trends": {
    "hot_directions": [
      "方向1：...（简要说明）",
      "方向2：...（简要说明）"
    ],
    "method_trends": [
      "趋势1：...",
      "趋势2：..."
    ],
    "key_breakthroughs": [
      "突破1：...",
      "突破2：..."
    ],
    "open_questions": [
      "问题1：...",
      "问题2：..."
    ]
  },
  "papers": [
    {
      "id": 1,
      "title": "Learning World Models with Action-Conditioned Transformers",
      "authors": "Author A, Author B, et al.",
      "venue": "arXiv preprint arXiv:2604.xxxxx",
      "date": "2026-04-22",
      "abstract": "This paper proposes...",
      "contribution_zh": "提出了基于动作条件Transformer的世界模型，解决了长期时序预测中的误差累积问题。",
      "method_zh": "使用因果Transformer架构，在潜在空间中进行自回归预测，并引入对比损失确保表征一致性。",
      "relevance_zh": "改进了世界模型在长时域预测中的实用性，对规划任务意义重大。"
    },
    {
      "id": 2,
      "title": "...",
      "authors": "...",
      "venue": "...",
      "date": "...",
      "abstract": "...",
      "contribution_zh": "...",
      "method_zh": "...",
      "relevance_zh": "..."
    }
  ],
  "outlook_zh": "整体来看，本周世界模型领域在...方面取得了进展。下周值得关注的子方向包括..."
}
```

## 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `topic` | string | 中文主题名 |
| `topic_en` | string | 英文主题名 |
| `timeframe` | string | 时间范围描述 |
| `report_date` | string | 报告生成日期 |
| `summary_zh` | string | 执行摘要（200-300字中文） |
| `trends.hot_directions` | string[] | 热门研究方向列表 |
| `trends.method_trends` | string[] | 方法范式趋势列表 |
| `trends.key_breakthroughs` | string[] | 关键突破列表 |
| `trends.open_questions` | string[] | 开放问题列表 |
| `papers[].id` | int | 论文序号 |
| `papers[].title` | string | 论文英文标题 |
| `papers[].authors` | string | 作者列表 |
| `papers[].venue` | string | 发布渠道（arXiv/会议/期刊） |
| `papers[].date` | string | 发表日期 |
| `papers[].abstract` | string | 英文摘要 |
| `papers[].contribution_zh` | string | 核心贡献（中文） |
| `papers[].method_zh` | string | 方法亮点（中文） |
| `papers[].relevance_zh` | string | 与主题的关系（中文） |
| `outlook_zh` | string | 总结与展望（中文） |

## 使用流程

1. 通过 WebSearch 收集文献信息
2. 按上述 Schema 组织为 JSON 文件
3. 调用 `generate_report.py` 生成 PDF
