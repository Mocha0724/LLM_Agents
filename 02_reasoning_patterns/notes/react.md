# 笔记 · ReAct: Synergizing Reasoning and Acting in Language Models（Yao et al., 2022）

- arXiv: 2210.03629
- ICLR 2023
- 一句话精华：让 LLM 交替输出「Thought / Action / Observation」三类 token，把推理与外部工具调用编织在一起。

## 动机

- *Pure CoT* 容易产生「事实幻觉」：闭门造车。
- *Pure Action*（如 SayCan）缺乏明确推理链：动作 brittleness。
- ReAct 的洞察：**让模型显式 verbalize 它的推理**，并允许它**用 action 与外部世界对话**。

## 提示模板

```
Question: ...
Thought 1: 我需要查 X
Action 1: Search[X]
Observation 1: ...
Thought 2: 现在我知道 X 是 Y，下一步应该 ...
Action 2: ...
...
Thought N: 我可以给出答案了
Action N: Finish[answer]
```

## 关键观察

1. **推理 + 行动协同优于二者之一**：在 HotpotQA、Fever、ALFWorld、WebShop 上都更强。
2. **Few-shot prompting 即可启动**：不需要微调就能用。
3. **可解释性极强**：trace 本身就是「为什么这样做」的解释。

## 失败模式

- **死循环**：在难题上反复问相似问题。需要 step budget。
- **幻觉式 Action**：调用不存在的工具或参数错误。需要严格 schema 验证。
- **过早 Finish**：信息不充分就终止。可结合 self-critique 缓解。

## 与现代框架的关系

- **Anthropic / OpenAI tool use** 本质上就是 ReAct + 结构化 schema：模型不再生成自然语言 Action，而是直接生成 tool_use JSON，安全得多。
- 因此今天再写 agent，*几乎不需要手撸 ReAct prompt*——但理解原理是必要的，因为很多 debugging 思路（看 thought trace）来自 ReAct。

## 与本仓库

- 第 03 章会把 ReAct 升级为「函数调用 + MCP」。
- 本章 notebook 用「手撸 ReAct」对比「函数调用 ReAct」，理解二者一致性。

## 我的批注

- ReAct 是「把 reasoning 与 acting 解耦表达，再用 prompt 让它们 alternating」的优雅设计；像极了控制论里的 *观测器 + 控制器* 分离。
- 你做定位算法时也可以借这个思路：把 *特征匹配* 看成 action，把 *置信度评估* 看成 thought，让顶层调度变得可解释。
