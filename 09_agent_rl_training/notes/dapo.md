# 笔记 · DAPO: Decoupled Clip and Dynamic Sampling Policy Optimization（ByteDance 2025）

- arXiv: 2503.14476
- 一句话精华：在 GRPO 之上做四个工程改进，使得 RL 在长文本/数学推理上更稳更强。

## 四大改进

### 1. Clip-Higher（解耦上下界 clip）

PPO 的 clip 是对称 $[1-\epsilon, 1+\epsilon]$。**DAPO 把上界放宽**到 $1+\epsilon_{\text{high}}$（例如 0.28 vs 默认 0.2），鼓励「探索性 token」。

直觉：探索方向的更新更大，避免 entropy 过早塌缩。

### 2. Dynamic Sampling

GRPO 中 *组内全对 / 全错* 的样本 advantage 全 0，没梯度但浪费算力。
DAPO 检测此类样本并 **重新采样补够**，保证有效梯度比例。

### 3. Token-Level Loss

GRPO 默认按 sequence 算 loss；长序列里中间 token 的影响被稀释。
DAPO 改成 **token-level**：每个 token 独立计算 advantage 与 loss，长输出更平稳。

### 4. Overlong Reward Shaping

超长 sample 给 *软* 长度惩罚（不是硬截断），保留长链推理能力。

## 实验亮点

- Qwen2.5-32B + DAPO 在 AIME 2024 达到 **50 分**，超 DeepSeek-R1-Zero 同规模 base。
- 训练曲线更稳定，entropy 不塌缩。

## 工程实现

- 开源框架 **veRL** 已集成 DAPO。
- 训练脚本与 GRPO 类似，只需打开 `dapo` 配置开关。

## 评注

- DAPO 是 2025 上半年最 *实用* 的 GRPO 改进，建议在尝试 GRPO 时直接用 DAPO 配置启动。
- 四个 trick 各自独立，可拆开消融实验，体现 *工程驱动算法* 的范式。
