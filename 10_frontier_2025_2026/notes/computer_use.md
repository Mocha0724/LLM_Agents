# 笔记 · Computer Use / Browser Use（2024-2026）

## 代表

- **Anthropic Claude Computer Use**（2024-10 beta，2025 正式）：Claude 直接看屏幕截图、输出键鼠操作。
- **OpenAI Operator / CUA**（2025-01）：基于 *Computer-Using Agent* 模型，先沙盒浏览器后扩展。
- **ChatGPT Atlas**、**Perplexity Comet**（2025）：浏览器作为 agent host，让 LLM 嵌入日常网页流。
- **Microsoft Magentic-One** / **OmniParser**：Windows 桌面 + UI parser。
- **Google Gemini 2 + Browser Use**：浏览器自动化 + 推理模型。
- **OpenInterpreter / Self-Operating Computer**：开源工具集。

## 核心架构

```mermaid
flowchart LR
    Screenshot[屏幕截图] --> VLM[多模态 LLM]
    State[DOM/可访问性树] --> VLM
    VLM --> Action[输出: click(x,y) / type(text) / scroll(dy)]
    Action --> OS[执行: pyautogui / selenium / WinAppDriver]
    OS --> Screenshot
```

## 关键挑战

1. **Grounding**：把语义意图落到正确像素坐标。误差几像素可能点错。
2. **状态理解**：弹窗、加载动画、异步刷新让单步决策困难。
3. **长 trajectory**：30-100 步任务对 context 与 reasoning 是巨大压力。
4. **安全**：模型一旦执行 *破坏性* 操作（删文件、点支付）很难回滚。
5. **延迟**：每步需要截图 + LLM 推理，端到端慢。

## 评测

- **OSWorld**（跨 OS 桌面任务）：当前最严肃的 benchmark。
- **WebArena / VisualWebArena**：Web 任务。
- **Mind2Web**：静态网页元素预测。
- **WindowsAgentArena**：Windows 应用场景。

2026 年顶级模型在 OSWorld 总分约 30-50%；离实用还有差距。

## 落地启示

- 不要追求「全自动 *任意* 任务」；先选 *狭窄场景 + HITL*（如「填表 + 检查」）。
- 必须有 sandbox + dry-run。
- 做好 audit log + 撤销机制。
- 与传统 RPA（UIPath）的对比：LLM agent 在 *未见过的 UI* 上更强，但稳定性弱；混合架构（LLM 当 fallback）正在兴起。

## 业务联想

- 在地图业务里：Computer Use 不直接相关，但 *Browser Use* 与 *agentic search* 是相邻领域；未来「行程规划 agent」很可能是 Browser Use 的杀手级场景之一。
