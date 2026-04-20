# 第 11 章 · 思考题与业务实践

## 思考题

1. *Gurnee & Tegmark* 的探针实验说明 LLM 内有空间编码，但为何在 *精确距离* 任务上仍要工具？请给出至少两个层面的解释。
2. PReP 的 perceive-reflect-plan 与第 02 章的 ReAct/Reflexion 有什么本质区别？
3. 把地图/定位业务的常见算子（定位 SDK / POI / 路径 / ETA）抽象成 5-8 个 tool。请写出每个的 input/output schema。
4. MapAgent 的「分层多 agent」相对单 agent ReAct，主要在哪两个维度上有优势？

## 业务实践

5. 以下需求，哪些适合走 *LLM agent* 路径，哪些应该继续走传统 pipeline？
   - 高峰时段 ETA 预测
   - 用户用方言问「附近哪儿能停车」
   - 路网拓扑构建
   - 给老年人解释路线
   - 室内定位融合

6. 假设要做一个 *自然语言路径规划助手* 的 PoC：请给出 4 周的迭代规划（数据 / 工具 / 评测 / 上线指标）。

## 面试题

1. **(基础)** 为什么直接让 LLM 输出 lat/lng 不可靠？怎么校验？
2. **(深入)** 设计一个 reward function，使得 RL 训练后的小型路径 agent 能逼近 ReAct + 大模型的效果。
3. **(系统设计)** 设计一个支持 *打断 / 重规划* 的实时车载 agent。考虑：状态管理、上下文长度、成本、安全。
4. **(开放)** 自动驾驶里 LLM 应该处于 *cognitive layer* 还是 *control layer*？为什么？
