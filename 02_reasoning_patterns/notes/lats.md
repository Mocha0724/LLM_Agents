# 笔记 · LATS: Language Agent Tree Search（Zhou et al., 2024）

- arXiv: 2310.04406
- ICML 2024
- 一句话精华：把 *MCTS* 拿来跑 *ReAct + Reflexion*，得到一个能「搜索 + 行动 + 反思」的统一 agent。

## 公式

LATS 用 UCT 选节点：

\[
\text{UCT}(s) = V(s) + c \cdot \sqrt{\frac{\ln N(\text{parent}(s))}{N(s)}}
\]

- $V(s)$：节点估值（LLM 打分 + 历史回报）。
- 选中后展开 $k$ 个子节点（每个子节点是一次 ReAct step）。
- 模拟到终态，回传 reward；失败 trajectory 用 Reflexion 写反思，下次绕开。

## 与前作对比

| 方法 | 搜索 | 工具 | 反思 | 备注 |
|------|------|------|------|------|
| CoT | × | × | × | 线性思考 |
| ReAct | × | √ | × | 工具调用 |
| Reflexion | × | √ | √ | 多 episode 反思 |
| ToT | √ | × | × | 树搜索 |
| **LATS** | **√** | **√** | **√** | 三者融合 |

## 实验亮点

- HotpotQA、HumanEval、WebShop 上同时领先各前作。
- HumanEval pass@1：LATS GPT-4 达 94.4%。

## 工程代价

- 调用次数巨大（MCTS rollout × 工具调用），延迟与成本极高。
- 适合「评估代价低、决策代价高」的任务，且要严格的 budget 控制。

## 我的批注

- 类比经典 RL：LATS 之于 ReAct，犹如 AlphaGo 之于 policy network。
- 在生产环境，LATS 适合做 *离线优化*（如自动 prompt 优化、数据生成），不适合在线服务。
- 与定位算法的桥梁：MCTS + LLM 也可以用在「多假设位姿评估」上——但要小心成本。
