# 笔记 · DPO: Direct Preference Optimization（Rafailov et al., NeurIPS 2023）

- arXiv: 2305.18290
- 一句话精华：通过闭式推导，把 RLHF 转成一个「分类式」的对偶问题，*不需要 RM、不需要 RL training loop*。

## 推导直觉

RLHF 等价于：

\[
\max_\pi \mathbb E_{x, y \sim \pi}[r(x,y)] - \beta \mathrm{KL}(\pi \| \pi_{\text{ref}})
\]

闭式解：

\[
\pi^*(y|x) = \frac{1}{Z(x)} \pi_{\text{ref}}(y|x) \exp\left(\frac{r(x,y)}{\beta}\right)
\]

把 reward 反解：$r(x,y) = \beta \log \frac{\pi^*(y|x)}{\pi_{\text{ref}}(y|x)} + \beta \log Z(x)$。

代入 Bradley-Terry 偏好模型 $P(y_w \succ y_l) = \sigma(r(x,y_w) - r(x,y_l))$，$\log Z$ 项相消，得到 DPO loss。

## 工程意义

- *无需 RM*：偏好数据直接作为目标。
- *无需 PPO 调度*：标准的监督学习 loop。
- *降低基础设施门槛*：开源社区主流后训练范式之一。

## 局限

- 强假设：偏好服从 BT model；reward 平稳。
- 容易过拟合：在小数据上效果不稳定。
- 缺乏「搜索」：只能利用现有 (chosen, rejected) 对。

## 后续衍生

- **IPO** (Identity Preference Optimization)：避免 BT 模型假设。
- **KTO** (Kahneman-Tversky Optimization)：用「单边好/坏」而非成对偏好。
- **SimPO**：去掉 reference policy。

## 我的批注

- DPO 是「让后训练人人可玩」的关键工作；2024 年大量开源 chat 模型用它做对齐。
- 但对 *agentic 后训练*（多步、可验证 reward），DPO 适用面较窄；要看 GRPO/RLVR 路线。
