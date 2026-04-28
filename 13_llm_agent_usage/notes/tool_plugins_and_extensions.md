# Agent 插件、扩展与 Slash Commands 使用指南

> 覆盖 Cursor、Claude Code、Codex CLI 三大工具的**插件/扩展体系**，包括各工具的 Slash Commands、技能扩展、第三方集成，以及 **Get Shit Done（GSD）** 插件的详细使用说明。

---

## 目录

1. [Claude Code 的 Skills / Commands / 插件](#1-claude-code-的-skills--commands--插件)
2. [Cursor 的 Marketplace 插件](#2-cursor-的-marketplace-插件)
3. [Codex CLI 的插件与扩展](#3-codex-cli-的插件与扩展)
4. [Get Shit Done（GSD） 详细使用说明](#4-get-shit-donegsd-详细使用说明)

---

## 1. Claude Code 的 Skills / Commands / 插件

### 1.1 整体架构

Claude Code 的扩展能力由以下组件构成：

| 组件 | 作用 | 触发方式 |
|------|------|----------|
| **Skills** | 封装领域知识和工作流说明书 | AI 自动匹配 或 手动引用 |
| **Slash Commands** | 快捷执行预定义工作流 | 用户输入 `/command` |
| **Hooks** | 事件前后自动执行脚本 | 事件触发（subagentStop 等） |
| **MCP Servers** | 连接外部数据源/工具 | AI 自动调用 |
| **Subagents** | 独立上下文的专家代理 | AI 自动委托 |
| **Plugins** | 打包以上组件的完整扩展 | `/plugin install` |

### 1.2 Skills（技能）

Skills 是 Claude Code 最核心的扩展方式。每个 Skill 是一个包含 `SKILL.md` 的目录，遵循 Agent Skills 开放标准。

#### 安装路径

```text
# 用户全局（所有项目可用）
~/.claude/skills/<skill-name>/SKILL.md

# 项目级（仅当前项目）
<project>/.claude/skills/<skill-name>/SKILL.md
```

#### 安装方式

```bash
# 从社区 GitHub 仓库安装
npx openskills install anthropics/skills
npx openskills install Imbad0202/academic-research-skills

# 或直接用 Claude Code 安装
/plugin install Imbad0202/academic-research-skills
```

#### 调用方式

**方式 A：AI 自动匹配**（推荐）

SKILL.md 的 `description` 写得清楚时，Claude Code 会在合适的场景自动加载使用：

```yaml
---
name: pdf
description: "Create, merge, extract text/tables from PDFs. Use when user asks: pdf 处理, 提取 PDF, merge pdf"
---
```

**方式 B：手动 Slash Command**

某些 Skill 会注册为 Slash Command，输入 `/` 即可看到：

```bash
# 在 Claude Code 终端中输入
/gsd-help
/paper-polish
```

**方式 C：在提示词中显式引用**

```bash
claude "使用 pdf skill 处理这个文件"
```

### 1.3 Slash Commands

Slash Commands 是 Claude Code 的快捷操作，输入 `/` 前缀触发。

#### 内置 Slash Commands

| 命令 | 用途 |
|------|------|
| `/help` | 显示帮助 |
| `/clear` | 清除当前会话上下文 |
| `/cost` | 查看当前会话的 token 用量和费用 |
| `/status` | 查看当前状态 |
| `/review` | 对当前分支进行代码审查 |
| `/compress` | 压缩上下文以节省 token |
| `/doctor` | 诊断并修复配置问题 |
| `/init` | 在当前目录初始化 CLAUDE.md |
| `/add` | 将文件添加到上下文 |
| `/drop` | 从上下文移除文件 |
| `/plan` | 使用规划模式 |
| `/act` | 切换到执行模式 |
| `/branch` | 创建并切换到新分支 |
| `/rewind` | 回退到之前的对话状态 |
| `/search` | 搜索整个代码库 |

#### 自定义 Slash Commands

在 `~/.claude/commands/` 目录下创建 `.md` 文件即可定义自己的命令：

```bash
mkdir -p ~/.claude/commands
```

`~/.claude/commands/paper-polish.md`：

```markdown
对论文进行学术润色：逐段检查逻辑流和语法，修复不自然的表达，保持 LaTeX 命令和引用不变。
输出格式：逐条列出修改位置、原句、修改建议。
```

之后在 Claude Code 终端中输入 `/paper-polish` 即可触发。

### 1.4 Plugins（插件）

Claude Code v2.1.88+ 推出了插件系统，使用 `/plugin` 管理。

```bash
# 安装插件
/plugin install <plugin-name>@<source>

# 列出已安装
/plugin list

# 移除
/plugin remove <plugin-name>
```

插件本质上是 **Skills + Hooks + MCP Servers + Subagents** 的打包集合。

### 1.5 推荐插件列表

| 名称 | 用途 | 安装 |
|------|------|------|
| **Get Shit Done (GSD)** | 规格驱动开发系统，上下文工程，多代理编排 | `npx get-shit-done-cc@latest` |
| **anthropics/skills** | Anthropic 官方 17 个 Office/Scientific Skills | `npx openskills install anthropics/skills` |
| **scientific-agent-skills** | 133 个跨学科科研 Skill | `npx openskills install K-Dense-AI/scientific-agent-skills` |
| **academic-research-skills** | 论文全流程：调研→写作→审稿→发表 | `npx openskills install Imbad0202/academic-research-skills` |
| **cline/tasks** | 任务系统增强 | `/plugin install tasks` |

---

## 2. Cursor 的 Marketplace 插件

### 2.1 插件体系概述

Cursor 通过 **Cursor Marketplace** 提供插件扩展。与 Claude Code 偏 CLI 的模式不同，Cursor 的插件更偏向 **IDE 集成**，通过 MCP 协议让 AI 代理获得访问外部工具的能力。

### 2.2 安装插件

**方式一：从 Marketplace 安装**

访问 [cursor.com/marketplace](https://cursor.com/marketplace) 或在 Cursor 中打开插件面板：

1. 点击左侧栏的插件图标（或 `Cmd+Shift+X`）
2. 搜索需要的插件
3. 点击安装

**方式二：配置 MCP 服务器**

Cursor 支持通过 MCP 协议连接任意外部工具。在 `.cursor/mcp.json` 中配置：

```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["@cursor/mcp-linear"],
      "env": {
        "LINEAR_API_KEY": "your-key"
      }
    },
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your-token"
      }
    }
  }
}
```

### 2.3 热门插件

| 插件 | 用途 | 效果 |
|------|------|------|
| **Datadog** | 监控和告警查询 | AI 可以直接查询服务指标和错误日志 |
| **Linear** | 项目管理 | AI 可以创建/更新/查询 Issue |
| **GitHub** | PR/Issue 管理 | AI 可以创建 PR、回复 Issue 评论 |
| **Slack** | 团队沟通 | AI 可以发送消息、搜索聊天记录 |
| **Stripe** | 支付系统 | AI 可以查询账单、管理订阅 |
| **AWS** | 云资源管理 | AI 可以操作 S3 / Lambda / ECS |
| **Figma** | 设计稿 | AI 可以读取设计组件和样式 |
| **PostgreSQL** | 数据库 | AI 可以直接查询数据库 |
| **Sentry** | 错误追踪 | AI 可以查看和分析错误堆栈 |

### 2.4 在 Cursor 中使用插件

安装插件后，Cursor 的 AI 代理会自动获得相关工具的能力。你在对话中自然描述需求即可：

```
帮我看一下最近 Sentry 上报的数据库连接错误
在 Linear 上创建一个关于优化 SQL 查询的 Task
把这个功能做成一个 Slack 公告发到 #team-dev
```

### 2.5 Cursor 的 Rules + Hooks + Skills

| 机制 | 位置 | 用途 |
|------|------|------|
| **Rules (.mdc)** | `.cursor/rules/*.mdc` | 永久生效的行为约束和编码规范 |
| **Hooks** | `.cursor/hooks.json` | 事件驱动的自动脚本 |
| **Skills** | `.cursor/skills/<name>/SKILL.md` | 按需加载的工作流说明书 |
| **Cursorrules** | `.cursorrules`（旧） | 项目级规则（已被 rules/ 替代） |

Hooks 配置示例（`hooks.json`）：

```json
{
  "version": 1,
  "hooks": {
    "subagentStop": [
      {
        "command": ".cursor/hooks/daily_literature_monitor.sh",
        "matcher": "文献追踪|daily_lit",
        "timeout": 120
      }
    ]
  }
}
```

### 2.6 Cursor 内置命令

| 快捷键/命令 | 用途 |
|-------------|------|
| `Cmd+I` | Composer：多文件编辑对话 |
| `Cmd+L` | Chat：代码对话 |
| `Cmd+K` | Inline Edit：选中代码行内编辑 |
| `Cmd+Shift+L` | 将当前文件加入 Chat 上下文 |
| `Cmd+Shift+I` | 打开 Composer Agent 模式 |

---

## 3. Codex CLI 的插件与扩展

### 3.1 概述

Codex CLI 是 OpenAI 官方的 CLI Coding Agent，扩展方式与 Claude Code 不同，依赖 OpenAI 生态。它支持 Skills（遵循 Open Skills 标准）和 Sandbox 执行环境。

### 3.2 Skills 安装

Codex CLI 使用 `~/.codex/skills/` 目录管理技能：

```bash
# 全局安装（用户级）
npx openskills install anthropics/skills --global  # 会自动安装到 ~/.codex/skills/

# 验证
ls ~/.codex/skills/
```

### 3.3 调用 Skills

Codex CLI 的命令前缀使用 `$` 而非 `/`：

```bash
# 在 Codex CLI 中
$gsd-help
$gsd-new-project

# 或直接在提示词中引用
codex "使用 pdf skill 处理这个文件"
```

### 3.4 GSD 在 Codex 中的安装

```bash
# 安装到 Codex
npx get-shit-done-cc --codex --global

# 验证（注意 Codex 使用 $ 前缀）
$gsd-help
```

### 3.5 Codex CLI 的特性

- **自动沙箱**：生成代码在隔离环境中执行，安全可控
- **看板模式**：`codex --ui` 启动图形界面
- **Git 集成**：自动创建分支和提交
- **Skills 兼容**：遵循 OpenSkills 标准

---

## 4. Get Shit Done（GSD） 详细使用说明

> **GSD（Get Shit Done）** 是一个轻量但强大的**元提示、上下文工程与规格驱动开发系统**。它解决了 Claude Code 等工具的核心痛点——随着上下文窗口填满导致输出质量逐步劣化（context rot）的问题。

> 官方仓库：[github.com/gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done)

### 4.1 安装

#### 交互式安装（推荐）

```bash
npx get-shit-done-cc@latest
```

安装器会引导你选择：
1. **运行时**：Claude Code、Cursor、Codex、Gemini CLI、OpenCode、Copilot、Windsurf 等（支持 12+ 运行时）
2. **安装位置**：全局（所有项目）或本地（仅当前项目）

#### 非交互式安装

```bash
# Claude Code
npx get-shit-done-cc --claude --global   # 全局
npx get-shit-done-cc --claude --local    # 当前项目

# Cursor
npx get-shit-done-cc --cursor --global
npx get-shit-done-cc --cursor --local

# Codex
npx get-shit-done-cc --codex --global
npx get-shit-done-cc --codex --local

# 全部
npx get-shit-done-cc --all --global
```

#### 验证安装

| 运行时 | 验证命令 |
|--------|----------|
| Claude Code / Gemini / Copilot | `/gsd-help` |
| Cursor（终端内） | `/gsd-help` |
| Codex | `$gsd-help` |

#### 推荐：跳过权限确认

GSD 依赖自动化，建议使用：

```bash
claude --dangerously-skip-permissions
```

或在 `.claude/settings.json` 中配置细粒度权限放行（详见 [官方文档](https://github.com/gsd-build/get-shit-done)）。

#### 保持更新

```bash
npx get-shit-done-cc@latest
```

#### 卸载

```bash
npx get-shit-done-cc --claude --global --uninstall
```

### 4.2 核心工作流

GSD 的核心是 **讨论 → 规划 → 执行 → 验证** 的循环。

```
/discuss ──→ /plan ──→ /execute ──→ /verify ──→ /ship
```

#### 步骤 1：新项目初始化

```bash
# 如果是已有代码库，先扫描
/gsd-map-codebase

# 初始化新项目
/gsd-new-project
```

系统会：
1. **提问**：直到彻底理解你的想法（目标、约束、技术偏好）
2. **研究**：拉起并行代理调研领域知识
3. **需求梳理**：提取 v1/v2/scope out
4. **路线图**：创建分阶段规划

生成的文件：`PROJECT.md`、`REQUIREMENTS.md`、`ROADMAP.md`、`STATE.md`

#### 步骤 2：讨论阶段

```bash
/gsd-discuss-phase 1
```

在规划前深入讨论实现决策：视觉风格、API 设计、错误处理等。

生成 `{phase_num}-CONTEXT.md`。

#### 步骤 3：规划阶段

```bash
/gsd-plan-phase 1
```

系统会结合 CONTEXT.md 的决策，进行领域调研并生成 2-3 份原子化 XML 任务计划，每份计划足够小以至于在全新的上下文窗口中执行。

生成 `{phase_num}-RESEARCH.md`、`{phase_num}-{N}-PLAN.md`。

#### 步骤 4：执行阶段

```bash
/gsd-execute-phase 1
```

系统按 **wave 依赖分析** 执行：

```
WAVE 1 (parallel)      WAVE 2 (parallel)      WAVE 3
Plan 01  Plan 02   →   Plan 03  Plan 04   →   Plan 05
(User    Product)       (Orders  Cart)         (Checkout
Model    Model)          API     API)           UI)
```

- 独立计划 → 并行执行
- 有依赖的计划 → 顺序执行
- 每个计划使用全新 20 万 token 上下文
- 每项任务生成原子 git 提交

生成 `{phase_num}-{N}-SUMMARY.md`、`{phase_num}-VERIFICATION.md`。

#### 步骤 5：验证工作

```bash
/gsd-verify-work 1
```

人工用户验收测试（UAT），系统会：
1. 提取可测试的交付项
2. 逐项带你验证
3. 自动诊断失败并生成修复计划

#### 步骤 6：发布与完成

```bash
/gsd-ship 1                  # 创建 PR
/gsd-complete-milestone      # 归档里程碑
/gsd-new-milestone            # 开启下一版本
```

#### 或者：自动推进

```bash
/gsd-next  # 自动检测当前状态并执行下一步
```

### 4.3 快速模式

适用于不需要完整规划的临时任务：

```bash
/gsd-quick "添加暗色模式开关到设置页"
```

参数组合：
```
/gsd-quick --discuss     # 先讨论再执行
/gsd-quick --research    # 先调研再执行
/gsd-quick --full        # 启用计划检查和验证
/gsd-quick --discuss --research --full  # 全流程
```

### 4.4 所有命令速览

#### 核心工作流

| 命令 | 作用 |
|------|------|
| `/gsd-new-project` | 完整初始化项目 |
| `/gsd-map-codebase` | 分析现有代码库 |
| `/gsd-discuss-phase [N]` | 讨论阶段实现决策 |
| `/gsd-plan-phase [N]` | 研究和规划 |
| `/gsd-execute-phase [N]` | 并行执行计划 |
| `/gsd-verify-work [N]` | 用户验收测试 |
| `/gsd-ship [N]` | 创建 PR |
| `/gsd-next` | 自动推进下一步 |
| `/gsd-quick` | 快速执行临时任务 |

#### 阶段管理

| 命令 | 作用 |
|------|------|
| `/gsd-add-phase` | 追加阶段 |
| `/gsd-insert-phase [N]` | 插入紧急工作 |
| `/gsd-remove-phase [N]` | 删除未来阶段 |
| `/gsd-progress` | 查看当前进度 |

#### 里程碑管理

| 命令 | 作用 |
|------|------|
| `/gsd-complete-milestone` | 归档里程碑并打 tag |
| `/gsd-new-milestone` | 开始下一版本 |
| `/gsd-audit-milestone` | 验证里程碑完成度 |

#### 会话管理

| 命令 | 作用 |
|------|------|
| `/gsd-pause-work` | 暂停并生成交接上下文 |
| `/gsd-resume-work` | 恢复上次会话 |
| `/gsd-session-report` | 生成会话摘要 |

#### 配置

| 命令 | 作用 |
|------|------|
| `/gsd-settings` | 打开配置面板 |
| `/gsd-set-profile <profile>` | 切换模型 profile（quality/balanced/budget） |
| `/gsd-help` | 显示全部命令 |

### 4.5 配置详解

#### 模型 Profile

| Profile | Planning | Execution | Verification | 适用场景 |
|---------|----------|-----------|--------------|----------|
| `quality` | Opus | Opus | Sonnet | 最关键的功能 |
| `balanced` | Opus | Sonnet | Sonnet | 默认，推荐 |
| `budget` | Sonnet | Sonnet | Haiku | 实验/原型开发 |

```bash
/gsd-set-profile budget
```

#### 工作流开关

| 设置 | 默认 | 作用 |
|------|------|------|
| `workflow.research` | true | 规划前调研领域知识 |
| `workflow.plan_check` | true | 执行前验证计划 |
| `workflow.verifier` | true | 执行后验证交付 |
| `workflow.auto_advance` | false | 自动串联各阶段 |

通过 `/gsd-settings` 修改。

#### Git 分支策略

| 策略 | 说明 |
|------|------|
| `none` | 直接提交当前分支（默认） |
| `phase` | 每个阶段一个分支 |
| `milestone` | 整个里程碑一个分支 |

### 4.6 为什么 GSD 有效

| 核心机制 | 说明 |
|----------|------|
| **上下文工程** | 每个文件严格控制大小，保证 Claude 在质量退化阈值内工作 |
| **XML 提示格式** | 结构化的任务描述，精确到具体文件、操作和验证步骤 |
| **多代理编排** | orchestrator 拉起专用研究/规划/执行/验证代理，主上下文保持清爽 |
| **原子 Git 提交** | 每项任务独立提交，`git bisect` 可精确定位问题 |
| **全新上下文每个计划** | 避免历史垃圾积累，每个计划使用干净的 20 万 token |

### 4.7 安全注意事项

```bash
# 保护敏感文件——在 .claude/settings.json 中配置
{
  "permissions": {
    "deny": [
      "Read(.env)",
      "Read(.env.*)",
      "Read(**/secrets/*)",
      "Read(**/*credential*)",
      "Read(**/*.pem)",
      "Read(**/*.key)"
    ]
  }
}
```

### 4.8 故障排查

| 问题 | 解决方法 |
|------|----------|
| 安装后找不到命令 | 重启运行时；检查 `~/.claude/commands/gsd/` 是否存在 |
| 命令行为异常 | 运行 `/gsd-help` 确认安装；重装 `npx get-shit-done-cc@latest` |
| 想更新 | `npx get-shit-done-cc@latest` |

---

## 各工具插件体系对比

| 维度 | Claude Code | Cursor | Codex CLI |
|------|-------------|--------|-----------|
| **插件类型** | Skills / Commands / Hooks / MCP | Marketplace 插件 / MCP | Skills 兼容 |
| **扩展目录** | `~/.claude/skills/` | `~/.cursor/mcp.json` | `~/.codex/skills/` |
| **命令前缀** | `/` | 自然语言 | `$` |
| **GSD 命令前缀** | `/gsd-*` | `/gsd-*`（终端内） | `$gsd-*` |
| **安装方式** | `/plugin install` / `npx` | 市场点选 / mcp.json | `npx` |
| **Skill 标准** | OpenSkills 标准 | `.cursor/skills/` | OpenSkills 标准 |
| **MCP 支持** | 原生 | 原生 | 有限 |
| **Hooks 支持** | `.claude/hooks/` | `.cursor/hooks.json` | — |
