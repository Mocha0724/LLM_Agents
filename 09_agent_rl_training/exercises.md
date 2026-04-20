# 第 09 章 · 思考题与面试题

## 思考题

1. RLHF / DPO / RLVR 三者，各自适用什么任务？给一个不能用 RLVR 的任务例子。
2. GRPO 为什么不需要 value model？这种取舍有什么代价？
3. DAPO 的 4 个改进里，哪一个对「长 CoT 数学题」最关键？为什么？
4. SkyRL-Agent 的 async dispatch 解决了什么瓶颈？类比到你的 RL 训练任务，是否有同样问题？
5. Argos 的 *agentic verifier* 与传统 RM 相比，从 reward hacking 角度看优势是什么？

## 面试题

1. **(基础)** 写出 PPO 与 GRPO 的目标函数，并指出唯一区别。
2. **(深入)** DeepSeek-R1-Zero 用纯 RL（无 SFT）训出强推理能力，这违反了 RLHF 三步式 dogma 吗？请解释。
3. **(系统)** 你要在公司内部从零搭一个 GRPO 训练 stack，需要哪些组件（rollout / reward / inference / optimizer / 监控）？
4. **(开放)** RLVR 在「reward 难以验证」的任务（开放对话、创意写作）上失效，那么 *RLAIF* / *Argos-style verifier* 是出路吗？
5. **(业务)** 在你的部门，*重定位成功率* 算可验证 reward 吗？设计一个把 LLM agent 接入「定位 pipeline」并用 RLVR 训练的方案。
