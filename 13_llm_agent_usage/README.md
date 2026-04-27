# 13 · LLM Agent 使用实战

> 本目录聚焦 **怎么选择、配置、使用 LLM Agent 工具**。前面章节偏理论、论文与框架，本目录偏实用教程：选哪个 coding agent、怎么接国内模型 API、Skill/OpenSkill 怎么写、Hook 与 Skill 有什么区别。

## 1. 本目录适合解决的问题

- 想用 Cursor / Claude Code / Codex / Aider / OpenHands 等 coding agent，但不知道选哪个。
- 想在 agent 工具里接入 DeepSeek、Qwen、GLM 等国产模型 API。
- 想理解 Skill、OpenSkill、Hook、Rule、MCP Tool 等概念的区别。
- 想给常见工作流写可复用 skill：编码、学术代码、论文修改、Word/Excel/PPT/PDF、Git/DevOps。

## 2. 阅读顺序

```mermaid
flowchart TD
    A[1. Coding Agent 选型] --> B[2. 国产模型 API 接入]
    B --> C[3. Skill / OpenSkill 编写与配置]
    C --> D[4. Hook vs Skill vs Rule vs Tool]
    D --> E[5. 实战模板与清单]
```

## 3. 文件导览

| 文件 | 内容 |
|------|------|
| [`notes/coding_agent_selection.md`](./notes/coding_agent_selection.md) | Coding Agent 选择指南：Cursor、Claude Code、Codex、Aider、OpenHands、Devin、国产工具等 |
| [`notes/chinese_model_api_integration.md`](./notes/chinese_model_api_integration.md) | 中国模型 API 接入方案：DeepSeek / Qwen / GLM / StepFun / MiniMax 等 |
| [`notes/skill_openskill_guide.md`](./notes/skill_openskill_guide.md) | Skill / OpenSkill 的原理、安装、编写、配置与迁移 |
| [`notes/hooks_vs_skills.md`](./notes/hooks_vs_skills.md) | Hook、Skill、Rule、Command、MCP Tool、Function Calling 的理解与比较 |
| [`examples/`](./examples/) | 可复制的 Skill / Hook / 配置片段 |

## 4. 快速结论

### Coding Agent 怎么选

| 场景 | 推荐 |
|------|------|
| 日常开发、阅读项目、改中小 feature | **Cursor** |
| 终端重度用户、脚本/后端项目、长上下文 | **Claude Code** |
| OpenAI 生态、轻量 CLI coding | **Codex CLI** |
| 想用国产/开源模型 + git 友好 | **Aider** |
| 想自托管云端 agent / 做 SWE-bench 研究 | **OpenHands / SWE-agent** |
| 想委托长任务、让 agent 自己开 PR | **Devin / 云端 coding agent** |

### 国内模型怎么接

优先选择 **OpenAI 兼容 API**。大多数国产模型可以统一这样调用：

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.deepseek.com",  # 或 Qwen / GLM / StepFun 的 base_url
)

resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "你好"}],
)
print(resp.choices[0].message.content)
```

### Skill 和 Hook 怎么理解

- **Skill**：给 agent 的「可按需加载的知识/流程说明」。
- **Hook**：在某个事件发生前后自动执行的脚本或命令。
- **Rule**：长期生效的行为约束。
- **MCP Tool**：真正可执行的外部工具。
- **Function Calling**：模型调用工具的 schema 协议。

一句话：**Skill 告诉 agent 怎么做，Hook 在事件发生时自动做，Tool 让 agent 能做。**

## 5. 与其它章节的关系

- 第 03 章讲 Tool Use / MCP 的原理，本目录讲实际工具怎么配。
- 第 07 章讲框架选型，本目录讲开发者日常怎么用。
- 第 10 章讲 frontier coding agent，本目录整理成实操教程。
- 第 12 章讲安全，本目录在每个工具使用方案里补充权限、沙箱、HITL 建议。
