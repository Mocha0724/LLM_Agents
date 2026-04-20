# LLM 内的空间表征 · 笔记

> 集中讨论 *"LLM 是否真的「懂」空间"* 这一基础研究问题，对地图业务的产品边界有指导意义。

## 1. Gurnee & Tegmark, *Language Models Represent Space and Time* (ICLR 2024)

- 用 *linear probing* 的方法：在 LLM 中间层 hidden state 上训一个线性回归，预测城市/地标的经纬度。
- 发现 Llama-2 70B 中存在 *几乎线性* 的全球地理坐标编码。
- 同样对历史时间也成立（"年代轴"）。

→ **结论**：LLM 内部存在一种隐式坐标系，但只是 *压缩的、可回归*，不是显式可计算。它解释了为什么 LLM 在 *距离比较 / 方向估计* 上比想象中好，但在 *精确计算* 上必须依赖工具。

## 2. PReP / VoP（见 prep_and_vop.md）

进一步表明 MLLM 内有 *cognitive map*-like 的城市表征，但分辨率有限。

## 3. 局限性

- LLM 的「空间」本质是 *语言上下文中的关联强度*，不是欧式几何。
- 任何需要 *精确数值*（距离、角度、坐标）的任务都必须 grounding 到外部 API/计算。
- 这就是为什么本章 README 强调「把传统 pipeline 包装成 tool 让 LLM 调」。

## 4. 工程含义

- 用户问「北京到上海多远」→ 让 agent 调 *距离 API*，而不是相信 LLM 直接说。
- 但用户问「这两个景点哪个适合下午去」→ LLM 的世界知识是有用的。
- 设计 agent 时要 *显式标注* 哪些子任务允许 LLM 直答，哪些必须工具调用。

## 推荐阅读

- Gurnee & Tegmark, *Language Models Represent Space and Time*, ICLR 2024.
- *Mind the Map* / *Cognitive Map in LLMs*, NeurIPS 2024 workshop 系列。
- Yamada et al., *Evaluating Spatial Understanding of Large Language Models*, TMLR 2024.
