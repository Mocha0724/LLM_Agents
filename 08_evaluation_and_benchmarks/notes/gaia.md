# 笔记 · GAIA: A Benchmark for General AI Assistants（Mialon et al., Meta 2023）

- arXiv: 2311.12983
- 一句话精华：466 道真实世界问题，需要多步推理 + 多模态理解 + 工具使用，人类 92% 解决，GPT-4 直接做仅 ~15%。

## 题目特点

- 来自真实生活：旅行规划、文献查找、电子表格分析等。
- 需要 *多步*（平均 8-9 步）。
- 答案 *exact match*：通常是数字 / 短文本，便于自动评测。
- 三级难度：Level 1（短链条）→ Level 2（多步）→ Level 3（开放搜索）。

## 例子

> Q: *What's the population (2023) of the city where the 2024 Summer Olympics opening ceremony was held, expressed in millions to 2 decimal places?*

需要：(1) 找到 2024 奥运城市；(2) 查 2023 人口；(3) 转单位 + 四舍五入。

## 关键意义

- 把「真实世界 agent 能力」与刷题/学术 benchmark 区分开来。
- 暴露当时 SOTA 的能力差距：人 92% vs GPT-4 ~15%。
- 推动 web 搜索 / 多模态 agent 研究。

## 2025-2026 进展

- 顶级 agent（如 H2O Multi-Agent、Trase Agent）已达 70-80%。
- 但 Level 3 仍未饱和；下一代 GAIA 在筹划。

## 评注

- GAIA 是检验「LLM agent 是否真能干活」的最佳真实 benchmark 之一。
- 业务联想：在垂直业务（如出行/导航）里，可以仿 GAIA 风格自建一组 *真实用户问题*（如 "帮我查一下从 X 到 Y 工作日早上的最佳路线"），作为定位 / 出行 agent 的金标准评测集。
