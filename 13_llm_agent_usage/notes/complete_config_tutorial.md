# 完整安装配置教程：工具安装 → API 替换 → Skills 使用

> 本文是第 13 章的**核心实操手册**，覆盖从零搭建 Coding Agent 工作环境的全流程：安装工具、替换模型 API、配置 Skills、上手使用。

---

## 目录

1. [Claude Code 安装配置](#1-claude-code-安装配置)
2. [Cursor 安装配置](#2-cursor-安装配置)
3. [OpenCode 安装配置](#3-opencode-安装配置)
4. [Codex CLI 安装配置](#4-codex-cli-安装配置)
5. [以 DeepSeek 为例替换 API](#5-以-deepseek-为例替换-api)
6. [OpenSkill + anthropics/skills 安装配置](#6-openskill--anthropicsskills-安装配置)
7. [Skills 使用方式](#7-skills-使用方式)
8. [案例：学术 Skill 安装和使用](#8-案例学术-skill-安装和使用)
9. [案例：自定义 literature-tracker Skill](#9-案例自定义-literature-tracker-skill)

---

## 1. Claude Code 安装配置

### 1.1 简介

Claude Code 是 Anthropic 官方的 **CLI 原生 Coding Agent**，直接在终端中使用，支持长上下文、代码修改、Git 操作等。

### 1.2 安装

```bash
# 使用 npm 全局安装
npm install -g @anthropic-ai/claude-code

# 验证安装
claude --version
```

### 1.3 首次配置

```bash
# 登录你的 Anthropic 账号
claude login

# 浏览器会自动打开授权页面，允许后终端会显示登录成功
```

### 1.4 基本使用

```bash
# 在当前目录启动交互模式
claude

# 直接提问
claude "解释一下这个项目的主要架构"

# 指定文件上下文的单次使用
claude -p "给 src/main.py 增加错误处理" --print

# 从 stdin 读取问题
cat bug_report.txt | claude
```

### 1.5 关键配置文件


| 文件                | 作用                 | 位置     |
| ----------------- | ------------------ | ------ |
| `CLAUDE.md`       | 项目级长期指令（行为规则、编码规范） | 项目根目录  |
| `.claude/skills/` | Skill 目录           | 项目根目录下 |
| `.claude/hooks/`  | 事件钩子（自动脚本）         | 项目根目录下 |


创建 `CLAUDE.md` 示例：

```markdown
# CLAUDE.md — 项目指令

## 编码规范
- Python 使用 type hints
- 优先使用 `pathlib` 而非 `os.path`
- 测试用 pytest，放在 `tests/` 目录

## Git 规范
- commit message 使用 conventional commits
- 提交前运行 `pytest` 确保测试通过
```

### 1.6 常用命令

```bash
claude          # 启动交互模式
claude -p "..." # 单次提问（非交互）
claude --help   # 查看全部选项
```

---

## 2. Cursor 安装配置

### 2.1 简介

Cursor 是基于 VS Code 的 **IDE 形态 Coding Agent**，原生支持 AI 对话、代码补全、内联编辑。适合日常开发和阅读项目。

### 2.2 安装

1. 从 [cursor.com](https://cursor.com) 下载桌面版安装包
2. 安装后打开，按提示登录（支持 GitHub / Google 账号）
3. 初始会提示选择模型（默认 Claude / GPT，也可以后续在设置中修改）

### 2.3 关键设置

#### 2.3.1 功能开关

打开 **Cursor → Settings → Features** 或 `Cmd+Shift+P` 搜索 "Cursor Settings"：


| 功能                   | 说明                 | 默认  |
| -------------------- | ------------------ | --- |
| **Composer**         | 多文件编辑对话（`Cmd+I`）   | 开启  |
| **Chat**             | 单文件/代码块对话（`Cmd+L`） | 开启  |
| **Inline Edit**      | 行内代码编辑（`Cmd+K`）    | 开启  |
| **Tab Autocomplete** | AI 代码补全            | 开启  |


#### 2.3.2 配置目录

```text
~/.cursor/                      # 用户级全局配置
  ├── settings.json             # 用户设置
  └── skills/                   # 用户级 Skill（所有项目可用）

<项目>/.cursor/                 # 项目级配置
  ├── rules/                    # Rules（.mdc 文件）
  ├── skills/                   # 项目级 Skill
  └── .cursorrules              # （旧版规则文件，现渐被 rules/ 替代）
```

### 2.4 基本使用快捷键


| 快捷键           | 功能                 |
| ------------- | ------------------ |
| `Cmd+I`       | 打开 Composer（多文件编辑） |
| `Cmd+L`       | 打开 Chat（对话）        |
| `Cmd+K`       | 行内编辑（选中代码后按）       |
| `Cmd+Shift+L` | 在 Chat 中添加当前文件上下文  |


### 2.5 Rules 配置（.mdc 文件）

Cursor 的 Rules 是永久生效的行为约束，位于 `.cursor/rules/*.mdc`：

```markdown
---
description: Python 编码规范。Use when working with Python files.
glob: "**/*.py"
---
- 所有函数必须有 type hints
- 使用 snake_case 命名
- 导入顺序：标准库 → 第三方 → 本地
```

---

## 3. OpenCode 安装配置

### 3.1 简介

**OpenCode** 是一个开源的 AI 编程助手，支持终端和网页两种运行形式。它原生支持多模型供应商切换，对 DeepSeek 等国产模型有良好的开箱体验。

### 3.2 安装

#### macOS

```bash
# 推荐使用 Homebrew
brew install opencode

# 或使用 npm
npm install -g @opencode-ai/cli

# 验证
opencode --version
```

#### Linux

```bash
# 使用 npm
npm install -g @opencode-ai/cli

# 验证
opencode --version
```

#### Windows

```bash
# 使用 npm（Windows 推荐在 PowerShell 或 CMD 中执行）
npm install -g @opencode-ai/cli

# 验证
opencode --version
```

**环境要求**：
- **OpenCode 版本 ≥ v1.14.24**（建议升级到最新版本以避免兼容性问题）
- Node.js 18+

### 3.3 配置 DeepSeek 模型

第一步：启动 OpenCode

```bash
cd /path/to/my-project
opencode
```

第二步：在互动界面中配置

1. 在输入框中输入 `/connect`
2. 选择 `deepseek` 供应商
3. 填入你的 [DeepSeek API Key](https://platform.deepseek.com/api_keys)
4. 选择 `DeepSeek-V4-Pro` 模型

### 3.4 验证

配置成功后，在 OpenCode 中输入一个问题测试：

```
解释当前项目的目录结构
```

如果回复正常，说明配置成功。

### 3.5 常用命令

| 命令 | 作用 |
|------|------|
| `/connect` | 连接/切换模型供应商 |
| `/model` | 查看或切换当前模型 |
| `/clear` | 清除当前会话 |
| `/help` | 查看帮助 |

---

## 4. Codex CLI 安装配置

### 3.1 简介

Codex CLI 是 OpenAI 官方的 **CLI Coding Agent**，依托 OpenAI 模型（GPT-4o / o 系列），轻量、支持 sandbox 执行。

### 3.2 安装

```bash
# 克隆仓库
git clone https://github.com/openai/codex-cli.git
cd codex-cli

# 安装
npm install -g .

# 或者直接用 npx（推荐）
npx @openai/codex --help
```

### 3.3 首次配置

```bash
# 设置 API Key
export OPENAI_API_KEY="sk-xxx"

# 验证
codex --version
```

### 3.4 基本使用

```bash
# 交互模式
codex

# 直接任务
codex "创建一个 Python 脚本，读取 CSV 并生成数据摘要"

# 指定模型
codex -m o3-mini "优化这个函数的性能"
```

### 3.5 特性

- **自动沙箱**：生成的代码在隔离环境执行，安全可控
- **看板模式**：`codex --ui` 启动图形界面
- **Git 集成**：自动创建分支、提交

---

## 5. 以 DeepSeek 为例替换 API

> 根据 DeepSeek 官方文档（https://api-docs.deepseek.com/zh-cn/guides/agent_integrations），DeepSeek 同时提供 **OpenAI 兼容** 和 **Anthropic 兼容** 两种 API 网关，分别适用于不同的工具。
>
> 本文覆盖主流工具：**Claude Code**（Anthropic 兼容）、**Cursor**（OpenAI 兼容）、**Aider**（OpenAI 兼容）、**OpenCode**（原生支持），以及 **SSH 连接远程服务器** 的场景，并区分 **macOS / Linux / Windows** 三种系统。

### 5.1 获取 DeepSeek API Key

1. 访问 [platform.deepseek.com](https://platform.deepseek.com) 注册
2. 在 API Keys 页面创建新 Key
3. 充值（DeepSeek 价格极低，¥1 可用很久）

### 5.2 在 Claude Code 中使用 DeepSeek（Anthropic 兼容）

> DeepSeek 官方提供 `https://api.deepseek.com/anthropic` 作为 Anthropic 兼容 API 网关，Claude Code 可通过环境变量直接接入。

#### macOS / Linux

```bash
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN="<你的 DeepSeek API Key>"
export ANTHROPIC_MODEL=deepseek-v4-pro
export ANTHROPIC_DEFAULT_OPUS_MODEL=deepseek-v4-pro
export ANTHROPIC_DEFAULT_SONNET_MODEL=deepseek-v4-pro
export ANTHROPIC_DEFAULT_HAIKU_MODEL=deepseek-v4-flash
export CLAUDE_CODE_SUBAGENT_MODEL=deepseek-v4-flash
export CLAUDE_CODE_EFFORT_LEVEL=max
```

#### Windows（PowerShell）

```powershell
$env:ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
$env:ANTHROPIC_AUTH_TOKEN="<你的 DeepSeek API Key>"
$env:ANTHROPIC_MODEL="deepseek-v4-pro"
$env:ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro"
$env:ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-pro"
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_SUBAGENT_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_EFFORT_LEVEL="max"
```

#### 持久化配置

```bash
# macOS / Linux（zsh）—— 写入 ~/.zshrc
echo 'export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic' >> ~/.zshrc
echo 'export ANTHROPIC_AUTH_TOKEN="sk-xxxx"' >> ~/.zshrc
# ...（其余变量同理）

# 然后重新加载
source ~/.zshrc
```

```powershell
# Windows（PowerShell）—— 写入 $PROFILE
Add-Content $PROFILE '$env:ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"'
# 重新加载
. $PROFILE
```

#### 使用

```bash
cd /path/to/my-project
claude
```

### 5.3 在 Cursor 中替换为 DeepSeek

#### 步骤 1：打开模型设置

**Cursor → Settings → Models**（或搜索 "Models"）

#### 步骤 2：添加自定义模型

| 字段 | 填写内容 |
|------|----------|
| **API Provider** | 选择 **OpenAI** 或自定义 |
| **Base URL** | `https://api.deepseek.com` |
| **API Key** | 你的 DeepSeek API Key |
| **Model ID** | `deepseek-chat`（通用对话）或 `deepseek-reasoner`（推理） |

#### 步骤 3：启用模型

在模型列表中勾选刚添加的 `deepseek-chat`，取消勾选其他不需要的模型。

#### 步骤 4：验证

在 Chat 中发送一条消息，如果回复正常，说明配置成功。

> **注意**：Cursor 配置在 macOS 和 Windows 上 UI 完全相同，只有快捷键差异（macOS 用 `Cmd`，Windows 用 `Ctrl`）。

#### Cursor 各模式的兼容性

| 模式 | 替换效果 |
|------|----------|
| **Chat** (`Cmd+L` / `Ctrl+L`) | 正常使用自定义模型 |
| **Composer** (`Cmd+I` / `Ctrl+I`) | 正常使用自定义模型 |
| **Tab Autocomplete** | 可能不支持第三方模型，仍走 Cursor 自带 |
| **Ctrl+K 内联编辑** | 正常使用自定义模型 |

### 5.4 在 OpenCode 中使用 DeepSeek（原生支持）

OpenCode 原生支持 DeepSeek 模型供应商，无需手动配置 base_url：

```bash
# 启动 OpenCode
cd /path/to/my-project
opencode

# 在互动界面中输入
/connect

# 选择 deepseek 供应商
# 填入 API Key
# 选择 DeepSeek-V4-Pro 模型
```

详情见第 3 章「OpenCode 安装配置」。

### 5.5 在 Aider 中替换为 DeepSeek

```bash
# 用 DeepSeek 启动 Aider
export DEEPSEEK_API_KEY="sk-xxx"
aider --model deepseek-chat --api-key deepseek=$DEEPSEEK_API_KEY

# 或用 OpenAI 兼容模式
aider --model openai/deepseek-chat \
  --openai-api-key "sk-xxx" \
  --openai-api-base "https://api.deepseek.com"
```

### 5.6 快速测试 API 是否可用

```bash
# macOS / Linux
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -d '{"model": "deepseek-chat", "messages": [{"role": "user", "content": "Hello"}]}'

# Windows（PowerShell）
$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer $env:DEEPSEEK_API_KEY"
}
$body = '{"model":"deepseek-chat","messages":[{"role":"user","content":"Hello"}]}'
Invoke-RestMethod -Uri "https://api.deepseek.com/chat/completions" -Method Post -Headers $headers -Body $body
```

### 5.7 SSH 连接远程 Linux 服务器的场景

#### 场景一：本地 Cursor + 远程服务器代码

**推荐方式**：Cursor 的 Remote SSH 功能

1. 本地安装 Cursor（模型配置在本地完成）
2. 安装 Remote SSH 扩展
3. 通过 `Cmd+Shift+P` 或 `Ctrl+Shift+P` → `Remote-SSH: Connect to Host` 连接
4. **模型 API 配置在本地**，远程服务器无需任何 API 配置

#### 场景二：在远程服务器直接使用 CLI 工具

```bash
# SSH 连接到远程 Linux 服务器
ssh user@remote-server

# 安装 Node.js（如果还没有）
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# 安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 设置 DeepSeek 环境变量
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN=sk-xxxxxxxxxx
export ANTHROPIC_MODEL=deepseek-v4-pro

# 启动
claude
```

#### 场景三：通过 SSH 使用 OpenCode

```bash
# SSH 到远程服务器
ssh user@remote-server

# 安装 OpenCode
npm install -g @opencode-ai/cli

# 启动并配置
cd /path/to/project
opencode
# 输入 /connect → 选择 deepseek
```

#### SSH 场景的网络注意事项

- 确保远程服务器能访问 API 端点（`api.deepseek.com`）
- 如果服务器在内网无法直连外网，需要配置 HTTP 代理：
  ```bash
  export HTTP_PROXY=http://proxy-server:port
  export HTTPS_PROXY=http://proxy-server:port
  ```
- 如果使用 Cursor Remote SSH，**只有本地机器需要能访问 API**，远程服务器不需要

### 5.8 常用国产模型兼容地址速查

| 厂商 | API 类型 | Base URL | 推荐模型 ID |
|------|----------|----------|-------------|
| **DeepSeek** | OpenAI 兼容 | `https://api.deepseek.com` | `deepseek-chat`, `deepseek-reasoner` |
| **DeepSeek** | Anthropic 兼容 | `https://api.deepseek.com/anthropic` | `deepseek-v4-pro`, `deepseek-v4-flash` |
| **阿里通义 Qwen** | OpenAI 兼容 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-max`, `qwen-coder-plus` |
| **智谱 GLM** | OpenAI 兼容 | `https://open.bigmodel.cn/api/paas/v4` | `glm-4-plus`, `glm-4-flash` |
| **阶跃星辰 StepFun** | OpenAI 兼容 | `https://api.stepfun.com/v1` | `step-2-16k` |


---

## 6. OpenSkill + anthropics/skills 安装配置

### 6.1 简介

**OpenSkills CLI**（`npx openskills`）是从 GitHub 仓库自动安装和管理 Skill 的工具，最重要的来源是 Anthropic 官方技能仓库 `anthropics/skills`。

### 6.2 安装 OpenSkills CLI

```bash
# 方法一：直接使用 npx（无需安装，推荐）
npx openskills@latest --help

# 方法二：全局安装
npm i -g openskills
openskills --help
```

环境要求：**Node.js ≥ 20.6**、Git。

### 6.3 安装 anthropics/skills 全部技能

```bash
# 安装到当前项目（推荐，Skill 会放在 .claude/skills/ 或 .agent/skills/）
cd your-project
npx openskills install anthropics/skills

# 或者安装到用户全局（所有项目可用）
npx openskills install anthropics/skills --global
```

### 5.4 只安装部分技能

OpenSkills 目前不支持按需选择子目录，但可以装完再删：

```bash
npx openskills install anthropics/skills

# 删除不需要的 skill
rm -rf .claude/skills/slack-gif-creator
rm -rf .claude/skills/algorithmic-art

# 重新生成 AGENTS.md
npx openskills sync
```

### 6.5 生成 AGENTS.md

```bash
# 生成项目 AGENTS.md（汇总所有已安装 skill）
npx openskills sync

# 也可以输出到指定文件
npx openskills sync -o SKILLS_INDEX.md
```

`AGENTS.md` 的作用是让 agent（或你在 Cursor 里 @ 它）知道当前项目装了哪些 skill、每个 skill 做什么用的。

### 6.6 管理已安装的技能

```bash
# 列出已安装
npx openskills list
npx openskills list --global

# 读取某个 skill 的内容（快速查看）
npx openskills read pdf

# 更新技能（从来源拉取最新）
npx openskills update

# 删除技能
npx openskills remove pdf
# 或交互式管理
npx openskills manage
```

### 6.7 多项目共享全局技能

在多个项目中想用同一套 skill：

```bash
# 全局安装
npx openskills install anthropics/skills --global

# 每个项目里只需要执行（读取全局技能列表，生成项目 AGENTS.md）
cd project-a
npx openskills sync --global
```

### 6.8 安装后的目录结构

```
your-project/
├── .claude/
│   └── skills/                    # 项目级 skill
│       ├── pdf/
│       │   └── SKILL.md
│       ├── docx/
│       │   └── SKILL.md
│       └── ...
└── AGENTS.md                      # 技能索引
```

---

## 7. Skills 使用方式

### 7.1 在 Cursor 中使用 Skill

Cursor 通过 **Composer / Chat 对话** 触发 Skill。有两种触发方式：

#### 方式 A：由 agent 自动匹配（推荐）

只要 SKILL.md 的 `description` 写得清楚，agent 会在合适的场景自动加载：

```yaml
---
name: pdf
description: "Create, merge, extract text/tables from PDFs. Use when user asks: pdf 处理, 提取 PDF, pdf合并, extract pdf, merge pdf"
---
```

当你对 Cursor 说"帮我提取这个 PDF 中的表格"时，agent 会自动匹配 pdf skill。

#### 方式 B：手动指定

在对话中明确引用 Skill 文件：

```
请按照 @AGENTS.md 中的 pdf skill 流程来处理这个 PDF
```

或直接 `@` 指定文件：在 Composer 中输入 `@.claude/skills/pdf/SKILL.md`。

### 6.2 在 Claude Code 中使用 Skill

```bash
# 方法一：依赖自动匹配（description 中的提示词）
claude "处理这个 PDF 文件"

# 方法二：手动引用 AGENTS.md
claude -r AGENTS.md "请按照汇总的技能列表处理"
```

### 6.3 在 Aider 中使用 Skill

Aider 没有原生 Skill 机制，但可以用 `--read` 预加载：

```bash
# 把 SKILL.md 当指令读入
aider --read .claude/skills/pdf/SKILL.md "处理这个 PDF"

# 或者先读出 skill 内容再管道传给 Aider
npx openskills read pdf | aider --read - "处理"
```

### 6.4 Skill 覆盖的场景速览（anthropics/skills）


| Skill             | 核心用途                                 |
| ----------------- | ------------------------------------ |
| `pdf`             | PDF 读、拆、合、表格提取、OCR                   |
| `docx`            | Word 文档创建、排版、目录、页眉页脚                 |
| `pptx`            | PowerPoint 创建、编辑、版式                  |
| `xlsx`            | 电子表格公式、图表、数据清洗                       |
| `canvas-design`   | 静态视觉设计（海报、信息图）                       |
| `frontend-design` | 前端界面设计（产品级 UI）                       |
| `claude-api`      | Claude/Anthropic API 开发（SDK、缓存、工具调用） |
| `mcp-builder`     | MCP Server 开发指南                      |
| `webapp-testing`  | Playwright Web 测试                    |
| `skill-creator`   | 创建和优化 Agent Skill 本身                 |
| `doc-coauthoring` | 文档协作编写工作流                            |
| `internal-comms`  | 内部沟通文案（状态汇报等）                        |


---

## 8. 案例：学术 Skill 安装和使用

### 8.1 场景

你需要一个能帮你在 **Claude Code / Cursor** 中辅助论文写作、文献调研、审稿回复的学术助手 Skill。

### 7.2 安装 academic-research-skills

```bash
# 从 GitHub 安装社区学术 Skill 包
npx openskills install Imbad0202/academic-research-skills

# 或手动放到 skills 目录
git clone https://github.com/Imbad0202/academic-research-skills.git
cp -r academic-research-skills/* .claude/skills/
```

该 Skill 包的结构（部分）：

```
.claude/skills/
├── deep-research/
│   ├── SKILL.md
│   ├── agents/
│   │   ├── research_question_agent.md
│   │   ├── synthesis_agent.md
│   │   └── ...
│   └── references/
│       ├── systematic_review_protocol.md
│       └── socratic_questioning_framework.md
├── paper-writing/
│   └── SKILL.md
└── peer-review/
    └── SKILL.md
```

### 7.3 在 Cursor 中使用学术 Skill

安装后，直接在 Cursor 中输入：

```
使用 deep-research skill 帮我调研一下「世界模型」领域的最新研究进展
```

Agent 会自动匹配 `description` 中的关键词，按照 SKILL.md 中定义的分阶段流程执行：

1. 解析需求
2. 多轮搜索（arXiv → 会议 → 补充）
3. 信息提取与验证
4. 趋势分析
5. 输出结构化报告

### 7.4 在 Claude Code 中使用

```bash
claude "使用 paper-writing skill 帮我润色这段论文摘要：[粘贴摘要]"
```

### 7.5 其他推荐的学术 Skill 仓库


| 仓库                                         | 安装方式                                                              | 适用场景                               |
| ------------------------------------------ | ----------------------------------------------------------------- | ---------------------------------- |
| `Master-cai/Research-Paper-Writing-Skills` | `npx openskills install Master-cai/Research-Paper-Writing-Skills` | ML/CV/NLP 论文段落优化、逻辑检查、审稿人自评        |
| `K-Dense-AI/scientific-agent-skills`       | `npx openskills install K-Dense-AI/scientific-agent-skills`       | 跨学科 133 科研 skill（数据分析、文献综述、科学写作）   |
| `LeonChaoX/qinyan-academic-skills`         | `npx openskills install LeonChaoX/qinyan-academic-skills`         | 181 学术 skill，18 分类（论文检索、科学写作、生物信息） |
| `Orchestra-Research/AI-Research-SKILLs`    | `npx openskills install Orchestra-Research/AI-Research-SKILLs`    | AI 研究 87 工程 skill（实验管理、ML 论文写作）    |


### 7.6 学术 Skill 的典型使用提示词

```
# 文献调研
"帮我做一份关于[主题]的系统文献综述，时间范围近3个月"

# 论文写作
"用 academic-writing skill 写一段 introduction，主题是..."

# 论文润色
"润色这段文字，目标是学术会议论文风格：[文本]"

# 审稿回复
"模拟审稿人视角，对这段论文给出改进建议：[文本]"
```

---

## 9. 案例：自定义 literature-tracker Skill

### 9.1 场景

你希望有一个 **文献追踪 Skill**，能自动搜索指定领域的最新论文、分析趋势并生成结构化报告。以下参考 `/Users/joeyzhang/workspace/Agent_Sample/.cursor/skills/literature-tracker/` 的完整实现。

### 8.2 Skill 目录结构

```
literature-tracker/
├── SKILL.md                     # 主 skill 定义（核心文件）
├── scripts/
│   ├── generate_report.py       # PDF 报告生成脚本
│   └── README.md                # 脚本使用说明
└── templates/
    ├── report_data_schema.md    # JSON 数据格式定义
    └── test_data.json           # 示例数据
```

### 8.3 SKILL.md 核心内容

```markdown
---
name: literature-tracker
description: "Track latest research progress in specific fields and generate
periodic literature progress reports (PDF format). Use when user wants:
文献追踪, 研究进展, 最新论文, research tracking, literature update,
paper survey, 文献报告, research monitoring, frontier tracking"
---

# Literature Tracker — 研究领域文献追踪与周报生成

## 快速开始
```

追踪上周[研究主题]的文献进展
为我生成一篇关于[主题]的近两周文献报告

```

## 工作流程

### Phase 1: 解析需求
用户需提供：研究主题、时间范围、可选深度级别。

### Phase 2: 执行文献检索（三轮）
- 第一轮：arXiv 主搜索
- 第二轮：会议论文搜索（NeurIPS, ICML, ICLR 等）
- 第三轮：补充搜索

### Phase 3: 信息提取与验证
每篇论文提取：标题、作者、发表信息、摘要、核心贡献等。

### Phase 4: 趋势分析
热门方向、方法趋势、关键突破、开放问题。

### Phase 5: 生成 PDF 报告
```bash
pip install reportlab
python scripts/generate_report.py \
    --topic "世界模型" \
    --timeframe "2026-04-21 ~ 2026-04-28" \
    --input research_data.json \
    --output "文献进展报告.pdf"
```

## JSON 数据格式

参见 templates/report_data_schema.md。

```

### 8.4 安装自定义 Skill

```bash
# 方法一：直接放入 Cursor 项目 skill 目录
mkdir -p .cursor/skills/literature-tracker/scripts
mkdir -p .cursor/skills/literature-tracker/templates

# 把 SKILL.md、脚本、模板分别放入对应位置

# 方法二：通过 npx openskills 从本地安装
npx openskills install /path/to/literature-tracker
```

### 8.5 在 Cursor 中使用

安装后，在 Cursor 中直接输入：

```
文献周报：世界模型，近一周
```

Agent 自动执行：

1. 使用 `literature-tracker` skill 的流程
2. 用 WebSearch 搜索 arXiv 和会议论文
3. 提取结构化信息
4. 分析趋势
5. 调用 `scripts/generate_report.py` 生成 PDF

### 8.6 进阶：配合 Cursor Hooks 实现自动化

你还可以添加 Hooks，让文献追踪在 Agent 对话结束后自动触发：

`.cursor/hooks.json`：

```json
{
  "version": 1,
  "hooks": {
    "subagentStop": [
      {
        "command": ".cursor/hooks/daily_literature_monitor.sh",
        "matcher": "文献追踪|daily_lit|research_monitor",
        "timeout": 120
      }
    ]
  }
}
```

对应的 shell 脚本 `/Users/joeyzhang/workspace/Agent_Sample/.cursor/hooks/daily_literature_monitor.sh` 封装了文献扫描器，从 `research_topics.json` 读取研究主题，自动搜索 arXiv 和 Semantic Scholar，生成 Markdown 报告。

详情参考 `Agent_Sample` 目录下的完整实现。

### 8.7 写成 OpenSkill 格式（通用）

如果你想把这个 skill 分享给团队或发布到 GitHub，保持标准格式：

```
literature-tracker/
├── SKILL.md                     # YAML front matter + markdown 正文
├── scripts/
│   └── generate_report.py
└── templates/
    ├── report_data_schema.md
    └── test_data.json
```

其他团队成员可以通过 OpenSkills 安装：

```bash
# 从 GitHub
npx openskills install your-org/your-skills-repo

# 从本地
npx openskills install ./literature-tracker
```

### 8.8 自定义 Skill 的最佳实践


| 要点                     | 说明                                 |
| ---------------------- | ---------------------------------- |
| **description 写清楚触发词** | 中英文都要覆盖，包含各种可能的问法                  |
| **流程拆成阶段**             | 让 agent 一步步执行，不容易遗漏关键步骤            |
| **提供快速开始模板**           | 用户看到直接可以复制的提示词，降低使用门槛              |
| **脚本放 scripts/**       | 复杂逻辑不要让 agent 现场写，预置为可执行脚本         |
| **数据 schema 另放**       | 数据结构定义放在 templates/ 中，SKILL.md 里引用 |
| **写负面约束**              | 明确"不要做什么"，比只写"要做什么"更有效             |


