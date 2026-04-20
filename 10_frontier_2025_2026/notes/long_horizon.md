# 笔记 · Long-Horizon Execution 长程执行（2025-2026）

> 关键问题：当 trajectory 长度 ≥ 数百步、跨越数小时甚至数天，agent 如何稳定地完成任务？

## 1. 失败模式

- **上下文遗忘**：context 太长，关键早期信息被压缩或淘汰。
- **错误链放大**：一步错，后面全错。
- **目标漂移**：agent 迷失初始目标。
- **重复 / 死循环**：相同步骤反复尝试。
- **资源耗尽**：成本/时间预算超限。

## 2. 应对技术

```mermaid
flowchart LR
    Plan[显式 hierarchical plan]
    Mem[长期记忆 + 总结]
    Check[周期 self-check]
    HITL[关键节点 HITL]
    Resume[Checkpoint + resume]
    Async[Async dispatch]
    Plan --> Mem --> Check --> HITL --> Resume --> Async
```

| 技术 | 作用 |
|------|------|
| 分层规划（Plan-Execute）| 把长任务切成阶段，每阶段独立 reset |
| 长期记忆 | 总结历史进 working memory，防遗忘 |
| 周期 self-check | 让 agent 自问「我是不是偏题？」 |
| HITL | 关键节点等用户确认 |
| Checkpoint | 跑挂了能恢复 |
| Async dispatch | 并行执行子任务，缩短 wall time |

## 3. 评测

- **TheAgentCompany**（CMU 2024）：模拟公司全工作流，多日任务。
- **WebArena 长程子集 / OSWorld 长程子集**。
- **Galileo Agent Leaderboard** 在 2025 加了 long-horizon 维度。

## 4. 训练角度

- **SkyRL-Agent**：把 long-horizon trajectory RL 化，async dispatch 解决 GPU 空闲。
- **Persistent Agent**（学术早期）：在 trajectory 间共享经验。
- **Memory-Augmented RL**（如 MemoryR1，2024）：把长程信息压缩到外部 memory。

## 5. 工业经验（来自 2025 Anthropic / OpenAI 多份博客）

- 90% 的失败都来自 *上下文管理*，而非「LLM 推理本身不行」。
- 复杂 agent 的实际「长任务成功率」与「单步准确率」呈非线性关系：单步 95% × 100 步 ≈ 0.6%。这就是为什么稳定性比 raw IQ 更重要。
- 把任务拆给多 agent / 多 worker 是常见缓解，但带来沟通成本。

## 6. 启示

- 不要以为「上下文窗口够大」就能解决；信息密度才是关键。
- Reference agents（一边做一边总结）+ 显式 plan 是 *最被低估* 的工程组合。
- HITL 不是耻辱，而是高 stakes 任务的最佳实践。

## 业务联想

- 在你的部门，「长期定位算法迭代」「跨季度数据飞轮」都是 long-horizon agent 的潜在落地场景。可以从「日常自动报警 + 人工 review」这种半自治起步。
