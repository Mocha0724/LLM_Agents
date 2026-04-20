# 笔记 · tau-bench 与 TheAgentCompany

## tau-bench (Yao et al., Sierra 2024, arXiv:2406.12045)

### 任务

模拟客服多轮对话 + 工具调用。两个领域：
- *Retail*：退款、订单查询。
- *Airline*：改签、取消。

每个任务包含：
- 用户 persona + 目标。
- 一个 LLM 当用户（按 persona 与 agent 交互）。
- 验证规则：检查最终系统状态是否满足任务条件。

### 关键评估维度

- **pass^k**：连续 k 次都成功的比率（验证一致性）。
- **policy adherence**：是否违反公司政策（如未授权下单）。
- **action efficiency**：调用工具次数。

### 启示

- 多轮对话 + 工具的*组合复杂性*远超单轮 benchmark。
- pass^k 是个好指标：暴露 agent 的不确定性 / 不稳定性问题。
- *Sierra* 团队由 Bret Taylor 创立，是 2024-2025 客服 agent 商用化的代表。

## TheAgentCompany (CMU 2024, arXiv:2412.14161)

### 任务

模拟一家小型软件公司的 *完整工作流*：175 个真实工作任务，跨 PM / 工程 / 数据 / HR 多种角色，平均长程操作 30+ 步。

环境：基于 GitLab、Plane、RocketChat、ownCloud 等真实软件搭建。

### 评估

- task completion 率
- 部分完成（partial credit）
- 给出 7 类失败模式分析

### 关键发现（论文）

- 当时（2024 末）最强模型 Claude 3.5 Sonnet 完成率约 24%，部分完成 ~34%。
- 失败主要来自：上下文遗忘、错误链式扩散、长程注意力衰减。

### 与 SWE-bench / GAIA 的差异

| 维度 | SWE-bench | GAIA | TheAgentCompany |
|------|-----------|------|-----------------|
| 任务跨度 | 单 PR | 单题 | 多任务多日 |
| 环境 | 仓库 | 单回话 + 工具 | 完整公司 stack |
| 难点 | 跨文件代码 | 真实知识 | 长程 + 协作 |

### 启示

- *长程任务* 是 2025-2026 评测核心方向。
- 把多个工具/角色串成「公司」级工作流，是衡量 agent 真实经济价值的方式。

## 评注

- tau-bench 揭示「一致性」远比「单次成功率」重要——客服场景失败一次就是事故。
- TheAgentCompany 指向一个有趣的未来方向：把整个 SaaS stack 当作 *agent gym*。类比工业场景，可以把「线上 service + 监控 dashboard + on-call 工具」拼成一个 SRE-agent gym。
