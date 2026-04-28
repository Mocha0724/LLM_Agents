---
name: literature-tracker
description: "Track latest research progress in specific fields (e.g., world models, foundation models, multi-agent systems) and generate periodic literature progress reports (PDF format). Use when the user wants to: track research frontiers, generate weekly/monthly literature updates, survey recent papers, monitor specific research areas, or produce a PDF literature progress report for a given time window. Triggers on: 文献追踪, 研究进展, 最新论文, research tracking, literature update, paper survey, weekly report, 周报, 文献报告, literature report, research monitoring, frontier tracking, track papers, paper monitoring."
---

# Literature Tracker — 研究领域文献追踪与周报生成

自动化追踪特定研究领域的最新文献进展，生成结构化的 PDF 格式文献进展报告。

## 快速开始

**基本用法（最短提示词）：**

```
追踪上周世界模型的文献进展
```

```
为我生成一篇关于多智能体系统的近两周文献报告
```

```
文献周报：主题 = 推理时扩展（inference-time scaling），时间 = 近一周
```

## 工作流程

### Phase 1: 解析需求（用户只需提供少量信息）

用户提供：
- **研究主题**：如"世界模型"、"多智能体系统"、"推理时扩展"
- **时间范围**：如"近一周"、"上周"、"近两周"、"2026年4月"
- **可选：深度级别**：标准（默认）/ 深入

### Phase 2: 执行文献检索

使用 WebSearch 工具执行系统化的文献搜索。

**搜索策略分为三轮：**

**第一轮：arXiv 主搜索**

使用以下查询模板搜索 arXiv（每个主题使用 2-3 组不同关键词）：

```
[research topic] arxiv 2026 recent papers
[research topic] arxiv latest research advances
[research topic] survey advances 2026
```

**第二轮：会议论文搜索**

搜索顶级会议（NeurIPS, ICML, ICLR, CVPR, ICRA, AAAI 等）的最新论文：

```
[research topic] NeurIPS ICML ICLR 2026
[research topic] CVPR ICRA AAAI 2026
```

**第三轮：补充搜索**

搜索特定子方向、知名研究组、或热门工作：

```
[research subtopic 1] 2026 [research topic]
[research subtopic 2] 2026 [research topic]
```

### Phase 3: 信息提取与验证

对每篇找到的论文，提取以下信息：
- **标题**（英文原文）
- **作者**（第一作者 + 通讯作者）
- **发表信息**（arXiv/会议/期刊 + 时间）
- **摘要**（英文原文）
- **核心贡献**（1-3句话，中文总结）
- **方法亮点**（1-2句话）
- **与 Topic 的关系/意义**（1句话）

初步结果验证标准：
- 确认论文确实发表于指定时间窗口内
- 排除不相关的结果
- 确保覆盖主要子方向

### Phase 4: 趋势分析

基于找到的文献进行分析：

1. **热门方向**：哪些子方向论文最多、引用最高？
2. **方法趋势**：主流方法范式是什么？
3. **关键突破**：是否有显著进展或新范式出现？
4. **开放问题**：哪些问题仍未解决？

### Phase 5: 生成 PDF 报告

使用 `scripts/generate_report.py` 脚本生成 PDF 文件。

**脚本依赖：**

```bash
pip install reportlab
```

**字体说明：**

PDF 中文显示依赖 macOS 系统字体 **STHeiti**。
- 如果运行环境不是 macOS（如 Linux 服务器），脚本需要下载并配置中文字体（如 Noto Sans CJK SC）。可以通过修改 `scripts/generate_report.py` 开头的字体注册部分来适配其他操作系统。

**使用方法：**

```python
python scripts/generate_report.py \
    --topic "世界模型" \
    --timeframe "2026-04-21 ~ 2026-04-28" \
    --input research_data.json \
    --output "文献进展报告_世界模型_20260428.pdf"
```

JSON 输入文件格式参见 [templates/report_data_schema.md](templates/report_data_schema.md)。

生成的 PDF 包含以下结构：

1. **封面** — 主题、时间范围、生成日期
2. **执行摘要** — 一周进展概览（中文，200-300字）
3. **趋势洞察** — 热门方向、方法趋势、关键突破
4. **论文详情** — 每篇论文的结构化展示（英文标题、中文核心贡献、英文摘要）
5. **总结与展望** — 整体评述和下周关注点

## 输入数据格式

参见 [templates/report_data_schema.md](templates/report_data_schema.md) 获取完整的数据结构和示例。

## 配置文件（可选）

在 `templates/config.json` 中可预设常用的跟踪主题列表，无需每次输入完整描述。

## 常见提示词模板

```
# 简洁版
文献周报：{主题}

# 标准版
为我生成一篇关于{主题}的近{时间}文献进展报告（PDF格式）

# 详细版
文献追踪。主题：{主题}。时间范围：{时间}。
请搜索arXiv和顶级会议论文，做趋势分析，然后生成PDF报告。
```

## 注意事项

- 使用 WebSearch 进行搜索时，**优先搜索 arXiv**，因为 arXiv 的论文更新最及时
- 对于中文提示词的响应，报告中的分析部分使用中文，论文标题和摘要保留英文原文
- 如果搜索到的论文数量太少（<5篇），扩大搜索关键词或时间范围
- 如果搜索到的论文太多（>20篇），优先选择引用量高、来自知名机构/作者的论文
- 报告生成前必须验证所有论文信息的准确性

## 相关资源

- 如需进行更深入的文献调研，参见 `deep-research` skill
- 如需撰写学术论文，参见 `academic-paper` skill
- PDF 生成脚本的参数说明参见 [scripts/README.md](scripts/README.md)
- 报告数据 schema 参见 [templates/report_data_schema.md](templates/report_data_schema.md)
