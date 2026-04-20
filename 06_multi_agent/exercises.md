# 第 06 章 · 思考题

## 思考题

1. AutoGen 的 GroupChat 与 LangGraph 的 StateGraph，分别更适合哪类任务？
2. MetaGPT 用 SOP 固化协作流程，优缺点分别是什么？什么任务最适合 SOP？
3. 多 agent debate 真的能减少幻觉吗？请举一个 *它无法解决* 的场景。
4. 给定 100 万 token / 月预算，让你设计一个客服系统：单 agent 还是多 agent？阐述权衡。

## 面试题

1. **(基础)** 列出 3 种多 agent 拓扑（pipeline / orchestrator-worker / debate）并各举一例。
2. **(深入)** Anthropic 在 2025 多 agent 研究博客中提到，多 agent token 消耗约为单 agent 的 15 倍。这个 gap 主要来自哪？
3. **(系统设计)** 为「自动复现一篇 ML 论文」任务设计多 agent 流水线。每个 agent 的输入 / 输出是什么？
4. **(开放)** 一个典型的 *算法迭代* 流程是：调研 → 写代码 → 跑实验 → 写报告。能否抽象为多 agent？哪些步骤适合自动化？
