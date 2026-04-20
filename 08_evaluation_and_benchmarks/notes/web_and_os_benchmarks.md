# 笔记 · WebArena / VisualWebArena / Mind2Web / OSWorld

## WebArena（Zhou et al., 2023, arXiv:2307.13854）

- 在 *本地复刻* 4 个真实网站（OneStopShop / Reddit / GitLab / Magento / Wikipedia / map），让 agent 完成 812 个任务。
- 优势：可重复、可调试、可作为训练环境。
- 评价：基于最终页面状态，task success 0/1。
- 2023 SOTA：GPT-4 ~14%；2024-2025：Claude/Operator 等达到 50-70%+。

## VisualWebArena (Koh et al., 2024)

- WebArena 的视觉版：要求 agent 看截图操作，不能依赖 DOM 文本。
- 更贴近 *Computer Use* 场景。

## Mind2Web (Deng et al., NeurIPS 2023)

- 真实网页操作集合：跨 137 个真实网站、2350 个任务。
- 静态采集（不可重复执行），适合 *element selection* / 行为预测的离线评测。
- 与 WebArena 互补：一个是 *动态环境*，一个是 *静态数据集*。

## OSWorld (Xie et al., 2024)

- 提供 369 个跨 Ubuntu / Windows / macOS 的桌面任务。
- 涉及浏览器、Office、终端、文件管理器等。
- 是 *Computer Use* / 跨应用 agent 的关键评测。
- Anthropic Computer Use、OpenAI Operator 都在 OSWorld 上报数。

## 共同设计哲学

| 维度 | 做法 |
|------|------|
| 真实性 | 来自真实站点 / OS，而非合成 |
| 可重复 | 容器化环境，可一键 reset |
| 可解释 | trace 完整保留，便于错误分析 |
| 自动评测 | 基于状态 / 文件 / DOM，避免人工 |

## 2026 视角

- WebArena 已大致饱和；研究焦点转向 *long-horizon*（TheAgentCompany）与 *adversarial*（恶意网页 / prompt injection）。
- 业务实战提示：自建 *小型 webarena* 环境是 web agent 研发的标配。

## 我的批注

- Web/OS benchmark 的真实贡献不仅是分数，而是 *提供可重复实验环境*。
- 在你的工作里，地图/导航产品的 *自动化测试环境* 是否可以参考 WebArena 的设计？
