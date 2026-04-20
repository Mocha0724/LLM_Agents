# 笔记 · Toolformer: Language Models Can Teach Themselves to Use Tools（Schick et al., 2023）

- arXiv: 2302.04761
- Meta AI
- 一句话精华：用 *self-supervised* 的方式让 LM 自己生成训练数据，学会在合适位置插入 API 调用。

## 关键流程

1. **采样候选位置**：在普通文本里，让 LM 提出「这里如果插入一个 API 调用，能否让后续 token 更准确」。
2. **API 执行**：实际调用 API（计算器、QA、翻译、日历），拿到结果。
3. **过滤**：保留「插入 API 后下游 perplexity 显著降低」的样本。
4. **微调**：用筛选后的样本继续训练 LM。

得到的模型在 zero-shot 数学、QA、翻译上显著提升，且不损害原 LM 能力。

## 关键贡献

- 第一篇系统证明 *LM 能 self-supervised 学会使用工具* 的工作。
- 思路简洁：用「下游困惑度」当 reward，避免人工标注。
- 启发后续 *Toolken*、*Granite-Function-Calling*、*Hermes-Tool-Use* 系列。

## 局限

- 只能学「单步」工具调用，不能交互多轮。
- 训练时仍用静态 corpus，与实际 agent loop 差距大。
- 工具集合是写死的，不易扩展。

## 与 MCP / Function Calling 的关系

Toolformer 探索了「能否学会调」，而 OpenAI/Anthropic 的 Function Calling 把问题变成了「教模型按 schema 输出」。
两条路线殊途同归，目前主流走 schema 路线（更可控），但 Toolformer 的思想在 *agentic post-training*（09 章）中复活：用执行结果作 reward 训练模型。

## 我的批注

- 把 Toolformer 看作「Tool Use 的预训练原型」非常合适。
- 对你算法岗工作的启发：在「带置信度的混合 pipeline」中，*用下游指标做软监督* 是很可借鉴的范式。
