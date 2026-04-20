# 第 12 章 · 思考题

## 思考题

1. 直接 / 间接 prompt injection 各举一个真实业务里的具体场景。
2. *双 LLM 架构* 为什么能阻断 IPI？什么场景不适用？
3. 给出 5 条「写操作必须 HITL」的 *白名单规则*，结合地图 agent 业务。
4. 比较 LangSmith / Langfuse / OTel-only 三种可观测性方案的 *锁定风险*。

## 实操

5. 给本仓库第 03 章的 `mcp_demo` 写一个攻击 PoC：在 `add` 的 description 里塞一段 IPI，看 Cursor / Claude 怎么反应；再设计相应防御。
6. 把第 11 章 `map_agent_demo.ipynb` 的 4 个工具中标识哪个是「写操作」（提示：可以扩展加一个 *report_traffic* 写操作），并加 HITL 闸门。

## 面试题

1. **(基础)** 列出 OWASP Top 10 for LLM Applications 中前 3 项。
2. **(深入)** 解释 Spotlighting / Tagging 防御的原理与失效场景。
3. **(系统设计)** 设计一个企业级 agent 的 trace 数据 schema（PII 怎么处理？保留多久？）。
4. **(开放)** 你怎么向不懂 LLM 的安全团队解释「prompt injection 不能根本治愈」？
