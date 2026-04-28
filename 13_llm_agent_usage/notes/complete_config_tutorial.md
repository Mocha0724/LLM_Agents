# 完整安装配置教程：工具安装 → API 替换 → Skills 使用

> 本文是第 13 章的**核心实操手册**，覆盖从零搭建 Coding Agent 工作环境的全流程：安装工具、替换模型 API、配置 Skills、上手使用。

---

## 目录

1. [Claude Code 安装配置](#1-claude-code-安装配置)
2. [Cursor 安装配置](#2-cursor-安装配置)
3. [OpenCode 安装配置](#3-opencode-安装配置)
4. [Codex CLI 安装配置](#4-codex-cli-安装配置)
5. [VS Code 中 Claude Code 插件](#5-vs-code-中-claude-code-插件)
6. [以 DeepSeek 为例替换 API](#6-以-deepseek-为例替换-api)
7. [OpenSkill + anthropics/skills 安装配置](#7-openskill--anthropicsskills-安装配置)
8. [Skills 使用方式](#8-skills-使用方式)
9. [案例：学术 Skill 安装和使用](#9-案例学术-skill-安装和使用)
10. [案例：自定义 literature-tracker Skill](#10-案例自定义-literature-tracker-skill)

---

> **快速参考**：[官方资源与文档索引](#附录官方资源与文档索引) — 所有工具的官网、文档、GitHub 链接汇总，以及系统差异速查表。

---

## 附录：官方资源与文档索引

 **后续内容基本是AI整理。我个人也没有各种环境各种工具都配过，不保证正确**  
 **安装相关的操作尽量参考各个官网最新的指南** 

### 各工具官方资源


| #   | 工具              | 官网/下载                                                             | 官方文档                                                             | GitHub / 其他                                                                                           |
| --- | --------------- | ----------------------------------------------------------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| 1   | **Claude Code** | [code.claude.com](https://code.claude.com)                        | [docs](https://code.claude.com/docs)                             | [github.com/anthropics/claude-code](https://github.com/anthropics/claude-code)                        |
| 2   | **Cursor**      | [cursor.com](https://cursor.com)                                  | [docs.cursor.com](https://docs.cursor.com)                       | [cursor.com/shortcuts](https://cursor.com/shortcuts)                                                  |
| 3   | **OpenCode**    | [opencode-ai.github.io](https://opencode-ai.github.io)            | [opencode-ai.github.io](https://opencode-ai.github.io)           | [github.com/opencode-ai/opencode](https://github.com/opencode-ai/opencode)                            |
| 4   | **Codex CLI**   | [openai.com/index/codex-cli](https://openai.com/index/codex-cli/) | —                                                                | [github.com/openai/codex-cli](https://github.com/openai/codex-cli)                                    |
| 5   | **VS Code**     | [code.visualstudio.com](https://code.visualstudio.com)            | [code.visualstudio.com/docs](https://code.visualstudio.com/docs) | [marketplace: Claude Code](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code) |


### Skills 相关资源


| 资源                     | 链接                                                                             |
| ---------------------- | ------------------------------------------------------------------------------ |
| OpenSkills CLI（npm）    | [npmjs.com/package/openskills](https://www.npmjs.com/package/openskills)       |
| OpenSkills GitHub      | [github.com/suplant-inc/openskills](https://github.com/suplant-inc/openskills) |
| Anthropic 官方 Skills 仓库 | [github.com/anthropics/skills](https://github.com/anthropics/skills)           |


### 中国模型 API 资源


| 模型厂商           | API 文档                                                                                                                                                 | API Key 申请                                                                         |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| **DeepSeek**   | [platform.deepseek.com/api-docs](https://platform.deepseek.com/api-docs)                                                                               | [platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys)           |
|                | Anthropic 兼容网关：[api-docs.deepseek.com/zh-cn/guides/anthropic_compatible](https://api-docs.deepseek.com/zh-cn/guides/anthropic_compatible)              |                                                                                    |
|                | OpenCode 集成说明：[api-docs.deepseek.com/zh-cn/guides/agent_integrations/opencode](https://api-docs.deepseek.com/zh-cn/guides/agent_integrations/opencode) |                                                                                    |
| **通义千问（Qwen）** | [help.aliyun.com/zh/model-studio](https://help.aliyun.com/zh/model-studio)                                                                             | [bailian.console.aliyun.com](https://bailian.console.aliyun.com)                   |
| **智谱 GLM**     | [open.bigmodel.cn/dev/api](https://open.bigmodel.cn/dev/api)                                                                                           | [open.bigmodel.cn/usercenter/apikeys](https://open.bigmodel.cn/usercenter/apikeys) |


### 通用系统工具下载


| 工具                                 | 官方链接                                                                                           |
| ---------------------------------- | ---------------------------------------------------------------------------------------------- |
| **Node.js**（所有工具的前置）               | [nodejs.org/zh-cn/download](https://nodejs.org/zh-cn/download/)                                |
| **Git**（版本控制、Skills 安装依赖）          | [git-scm.com/downloads](https://git-scm.com/downloads)                                         |
| **Homebrew**（macOS 包管理器）           | [brew.sh](https://brew.sh)                                                                     |
| **nvm**（macOS/Linux Node 版本管理）     | [github.com/nvm-sh/nvm](https://github.com/nvm-sh/nvm)                                         |
| **nvm-windows**（Windows Node 版本管理） | [github.com/coreybutler/nvm-windows](https://github.com/coreybutler/nvm-windows)               |
| **Windows Terminal**（推荐终端）         | [apps.microsoft.com/detail/9n0dx20hk701](https://apps.microsoft.com/detail/9n0dx20hk701)       |
| **PowerShell 7+**（Windows 推荐）      | [github.com/PowerShell/PowerShell/releases](https://github.com/PowerShell/PowerShell/releases) |


### 系统差异快速参考


| 概念           | macOS                                           | Linux                                       | Windows                          |
| ------------ | ----------------------------------------------- | ------------------------------------------- | -------------------------------- |
| 终端           | Terminal.app / iTerm2                           | 系统终端 / Konsole / Gnome Terminal             | PowerShell 7+ / Windows Terminal |
| 包管理器         | Homebrew (`brew`)                               | apt (Debian) / dnf (Fedora) / pacman (Arch) | winget / Chocolatey / Scoop      |
| 环境变量         | `export VAR=value`                              | `export VAR=value`                          | `$env:VAR="value"` (PowerShell)  |
| 配置文件         | `~/.zshrc` / `~/.bashrc`                        | `~/.bashrc` / `~/.zshrc` / `~/.profile`     | 系统环境变量 / `$PROFILE`              |
| 全局 npm 路径    | `/usr/local/lib/node_modules` 或 `~/.npm-global` | 同 macOS                                     | `%APPDATA%\npm\node_modules`     |
| PATH 查看      | `echo $PATH`                                    | `echo $PATH`                                | `$env:Path`                      |
| Node.js 推荐安装 | brew / nvm / 官网 .pkg                            | nvm / apt / 官网 .tar.xz                      | nvm-windows / 官网 .msi            |


---

## 1. Claude Code 安装配置

### 1.1 简介

Claude Code 是 Anthropic 官方的 **CLI 原生 Coding Agent**，直接在终端中使用，支持长上下文、代码修改、Git 操作等。

### 1.2 安装

#### 前置条件


| 系统      | 前置要求                                                                                 |
| ------- | ------------------------------------------------------------------------------------ |
| macOS   | macOS 12+；Node.js ≥ 18；Git（Xcode Command Line Tools）                                 |
| Linux   | Node.js ≥ 18；Git；glibc 2.28+                                                         |
| Windows | Windows 10+；Node.js ≥ 18；**Git for Windows**（[下载](https://git-scm.com/download/win)） |


> **安装 Node.js**：从 [nodejs.org](https://nodejs.org/zh-cn/download/) 下载 LTS 版本，或通过包管理器安装：
>
> - macOS: `brew install node`
> - Linux: `curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && sudo apt-get install -y nodejs`
> - Windows: 从官网下载 `.msi` 安装包

#### 安装命令（三系统通用）

```bash
# npm 全局安装
npm install -g @anthropic-ai/claude-code

# 验证安装
claude --version
```

#### macOS 注意事项

- 如果 `claude` 命令找不到，确认 npm 全局 bin 目录在 `PATH` 中：
  ```bash
  # npm 全局安装路径通常在
  # macOS/Linux: /usr/local/bin 或 ~/.npm-global/bin
  # Windows: %APPDATA%\npm
  npm list -g @anthropic-ai/claude-code
  ```
- 首次运行可能需要授予终端「辅助功能」权限（macOS 安全提示）

#### Windows 注意事项

- 在 **PowerShell 或 Windows Terminal** 中执行安装命令
- 如果遇到执行策略限制，用管理员权限运行：
  ```powershell
  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- Claude Code 在 Windows 上依赖 **Git Bash** 运行 shell 命令，确保 Git for Windows 已安装

#### Linux 注意事项

- 如果 `npm install -g` 遇到权限错误，使用 Node 版本管理器（推荐）：
  ```bash
  # 使用 nvm 安装 Node.js（推荐 Linux 用户）
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
  nvm install 20
  # 之后安装 Claude Code 不需要 sudo
  npm install -g @anthropic-ai/claude-code
  ```

#### 官方资源


| 资源        | 链接                                                                             |
| --------- | ------------------------------------------------------------------------------ |
| 官方文档      | [code.claude.com/docs](https://code.claude.com/docs)                           |
| 下载/安装指南   | [code.claude.com/docs/en/vs-code](https://code.claude.com/docs/en/vs-code)     |
| GitHub 仓库 | [github.com/anthropics/claude-code](https://github.com/anthropics/claude-code) |
| 设置参考      | [code.claude.com/en/settings](https://code.claude.com/en/settings)             |


### 1.3 首次配置（如果要接入国产模型，跳过这一步）

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

## 2. Cursor 安装配置（Cursor可以使用IDE风格的界面，也可以使用Agent风格）

## 2.1 简介

Cursor 是基于 VS Code 的 **IDE 形态 Coding Agent**，原生支持 AI 对话、代码补全、内联编辑。适合日常开发和阅读项目。

### 2.2 安装

#### 前置条件


| 系统      | 前置要求                                                |
| ------- | --------------------------------------------------- |
| macOS   | macOS 11+（Big Sur+）；Intel 或 Apple Silicon           |
| Windows | Windows 10 20H2+；64-bit                             |
| Linux   | Ubuntu 20.04+ / Fedora 38+ / 其他主流发行版；x86_64 或 ARM64 |


#### 下载安装

从 [cursor.com](https://cursor.com) 下载对应系统的桌面版安装包：


| 系统                        | 安装包类型                         | 安装方式                   |
| ------------------------- | ----------------------------- | ---------------------- |
| **macOS (Intel)**         | `.dmg`                        | 下载后拖入 Applications 文件夹 |
| **macOS (Apple Silicon)** | `.dmg`（arm64）                 | 同上，推荐 Apple Silicon 版本 |
| **Windows**               | `.exe` 安装包                    | 双击运行，按向导安装             |
| **Linux**                 | `.AppImage` / `.deb` / `.rpm` | 参见下方 Linux 说明          |


#### macOS 安装

```bash
# 下载 .dmg → 拖入 Applications 文件夹 → 首次打开 Cursor
# 如果提示"无法验证开发者"，在系统设置 → 隐私与安全性中允许打开
```

> **macOS 特别注意**：首次打开时系统会提示安全性验证，点击"仍然打开"即可。如果使用 Apple Silicon Mac，建议下载 arm64 版本获得更好的性能。

#### Windows 安装

```bash
# 运行下载的 .exe 安装包
# 安装程序会自动添加开始菜单快捷方式和右键菜单
# 安装后可通过 Windows Terminal 或 PowerShell 使用 Cursor 命令
```

> **Windows 特别注意**：安装后可以在终端中使用 `cursor .` 命令打开当前目录（类似 VS Code 的 `code .`）。

#### Linux 安装

```bash
# 方式一：下载 .AppImage（通用，无需安装）
chmod +x cursor-*.AppImage
./cursor-*.AppImage

# 方式二：通过 .deb 包（Ubuntu/Debian）
sudo dpkg -i cursor-*.deb

# 方式三：通过 .rpm 包（Fedora/RHEL）
sudo rpm -i cursor-*.rpm

# 方式四：通过 Snap（部分发行版）
sudo snap install cursor
```

> **Linux 特别注意**：.AppImage 版本无需安装，下载后赋予执行权限即可运行。如果需要集成到应用菜单，使用 .deb 或 .rpm 版本。

#### 安装后验证

```bash
# 在终端中检查
cursor --version

# 打开当前目录
cursor .
```

#### 官方资源


| 资源             | 链接                                                       |
| -------------- | -------------------------------------------------------- |
| 官网下载           | [cursor.com](https://cursor.com)                         |
| 官方文档           | [docs.cursor.com](https://docs.cursor.com)               |
| 快捷键指南          | [cursor.com/shortcuts](https://cursor.com/shortcuts)     |
| Marketplace 插件 | [cursor.com/marketplace](https://cursor.com/marketplace) |
| 更新日志           | [cursor.com/changelog](https://cursor.com/changelog)     |


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

**OpenCode** 是一个开源的 AI 编程助手，支持终端和网页两种运行形式。它原生支持多模型供应商切换，对 DeepSeek 等国产模型有良好的开箱体验。（仿Claude Code的）

### 3.2 安装

#### 前置条件


| 系统      | 前置要求                     |
| ------- | ------------------------ |
| macOS   | macOS 11+；Node.js ≥ 18   |
| Linux   | 任意主流发行版；Node.js ≥ 18     |
| Windows | Windows 10+；Node.js ≥ 18 |


**版本要求**：OpenCode ≥ **v1.14.24**（建议升级到最新版本）

#### macOS 安装

```bash
# 方式一：Homebrew（推荐）
brew install opencode

# 方式二：npm
npm install -g @opencode-ai/cli

# 验证
opencode --version
```

#### Linux 安装

```bash
# 使用 npm（推荐）
npm install -g @opencode-ai/cli

# 验证
opencode --version

# 如果使用 Arch Linux，也可通过 AUR 安装
yay -S opencode-cli
```

#### Windows 安装

```bash
# 在 PowerShell 或 Windows Terminal 中执行
npm install -g @opencode-ai/cli

# 验证
opencode --version
```

> **Windows 特别注意**：OpenCode 在 Windows 上推荐使用 **PowerShell 7+** 或 **Windows Terminal** 运行。CMD 可能对 Unicode 支持不佳。

#### 安装后登录/配置

OpenCode 不强制登录，首次启动后通过互动界面配置模型供应商（见 [3.3 配置 DeepSeek 模型](#33-配置-deepseek-模型)章节）。

#### 官方资源


| 资源            | 链接                                                                                                                                       |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| GitHub 仓库     | [github.com/opencode-ai/opencode](https://github.com/opencode-ai/opencode)                                                               |
| 官方文档          | [opencode-ai.github.io](https://opencode-ai.github.io)                                                                                   |
| DeepSeek 集成说明 | [api-docs.deepseek.com/zh-cn/guides/agent_integrations/opencode](https://api-docs.deepseek.com/zh-cn/guides/agent_integrations/opencode) |


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


| 命令         | 作用         |
| ---------- | ---------- |
| `/connect` | 连接/切换模型供应商 |
| `/model`   | 查看或切换当前模型  |
| `/clear`   | 清除当前会话     |
| `/help`    | 查看帮助       |


---

## 4. Codex CLI 安装配置

### 4.1 简介

Codex CLI 是 OpenAI 官方的 **CLI Coding Agent**，依托 OpenAI 模型（GPT-4o / o 系列），轻量、支持 sandbox 执行。

### 4.2 安装

#### 前置条件


| 系统      | 前置要求                                     |
| ------- | ---------------------------------------- |
| macOS   | macOS 12+；Node.js ≥ 18；Git               |
| Linux   | 任意主流发行版；Node.js ≥ 18；Git                 |
| Windows | Windows 10+；Node.js ≥ 18；Git for Windows |


#### 方式一：通过 npm 安装（推荐）

```bash
# macOS / Linux / Windows 通用
npm install -g @openai/codex

# 验证
codex --version
```

#### 方式二：通过 npx 直接使用（无需安装）

```bash
npx @openai/codex --help
```

#### 方式三：从源码安装

```bash
# 克隆仓库（适用于所有系统）
git clone https://github.com/openai/codex-cli.git
cd codex-cli

# 安装
npm install -g .
```

#### macOS 注意事项

- 如果遇到 `gyp` 编译错误，确保已安装 Xcode Command Line Tools：
  ```bash
  xcode-select --install
  ```

#### Windows 注意事项

- 在 **PowerShell（管理员）** 中执行安装命令
- 如果 `codex` 命令找不到，检查 npm 全局路径是否在环境变量中：
  ```powershell
  # 将 npm 全局路径加入 PATH
  $env:Path += ";$env:APPDATA\npm"
  # 永久添加
  [Environment]::SetEnvironmentVariable("Path", $env:Path + ";$env:APPDATA\npm", [EnvironmentVariableTarget]::User)
  ```

#### Linux 注意事项

- 如果使用 `npx @openai/codex` 下载缓慢，考虑设置 npm 镜像：
  ```bash
  npm config set registry https://registry.npmmirror.com
  ```

#### 官方资源


| 资源        | 链接                                                                 |
| --------- | ------------------------------------------------------------------ |
| GitHub 仓库 | [github.com/openai/codex-cli](https://github.com/openai/codex-cli) |
| 官方文档      | [openai.com/index/codex-cli](https://openai.com/index/codex-cli/)  |


### 4.3 首次配置

```bash
# 设置 API Key
export OPENAI_API_KEY="sk-xxx"

# 验证
codex --version
```

### 4.4 基本使用

```bash
# 交互模式
codex

# 直接任务
codex "创建一个 Python 脚本，读取 CSV 并生成数据摘要"

# 指定模型
codex -m o3-mini "优化这个函数的性能"
```

### 4.5 特性

- **自动沙箱**：生成的代码在隔离环境执行，安全可控
- **看板模式**：`codex --ui` 启动图形界面
- **Git 集成**：自动创建分支、提交

---

## 5. VS Code 中 Claude Code 插件

### 5.1 简介

相比于 CLI 模式（Claude Code 终端版），插件模式更适合：

- 希望可视化查看和审阅代码变更的用户
- 习惯 IDE 内对话而非终端交互的用户
- 需要多任务并行会话的场景

### 5.2 安装

#### 前置条件


| 系统      | 前置要求                                                      |
| ------- | --------------------------------------------------------- |
| 全部      | VS Code **≥ 1.98+**（查看版本：`code --version` 或 VS Code → 关于） |
| macOS   | Node.js ≥ 18（插件内部依赖 Claude Code CLI）                      |
| Linux   | Node.js ≥ 18                                              |
| Windows | Node.js ≥ 18                                              |


> **VS Code 下载**：[code.visualstudio.com](https://code.visualstudio.com/) 选择对应系统版本。

#### 安装步骤

**方法一：VS Code 扩展市场安装（推荐）**

1. 打开 VS Code → 快捷键打开扩展面板
  - macOS: `Cmd+Shift+X`
  - Windows/Linux: `Ctrl+Shift+X`
2. 搜索 **"Claude Code"**
3. 找到 "Claude Code for VS Code"（发布者为 Anthropic），点击「安装」
4. 安装完成后侧边栏出现 Claude Code 图标

**方法二：通过 Marketplace 链接安装**

访问 [VS Code Marketplace - Claude Code](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code) 点击 Install。

**方法三：通过 Claude Code CLI 安装（如果已安装 CLI）**

```bash
claude plugin add claude-code-vscode
```

#### macOS 安装注意事项

- 确保 VS Code 命令在终端可用：`Cmd+Shift+P` → "Shell Command: Install 'code' command in PATH"
- 如果插件安装后无法激活，重载窗口：`Cmd+Shift+P` → "Developer: Reload Window"

#### Windows 安装注意事项

- 如果插件加载失败，尝试**以管理员身份运行 VS Code** 再安装一次
- 建议在 **VS Code 桌面版**（非 WSL 远程版）中安装插件，WSL 环境需要额外配置
- 确保 VS Code 终端能够运行 Node.js：`node --version`

#### Linux 安装注意事项

- 如果插件商店访问慢，可切换国内镜像源，或在环境中配置代理
- 对 Wayland 显示服务器，部分弹窗可能不完美，但不影响功能

#### 验证安装

安装后如果 Spark 图标未显示，执行：

```bash
# 命令面板 → Developer: Reload Window
# macOS: Cmd+Shift+P
# Windows/Linux: Ctrl+Shift+P
```

#### 官方资源


| 资源               | 链接                                                                                                                                                           |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| VS Code 插件市场     | [marketplace.visualstudio.com/items?itemName=anthropic.claude-code-vscode](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code-vscode) |
| Claude Code 整体文档 | [code.claude.com/docs](https://code.claude.com/docs)                                                                                                         |
| VS Code 官方下载     | [code.visualstudio.com](https://code.visualstudio.com)                                                                                                       |
| 设置参考             | [code.claude.com/en/settings](https://code.claude.com/en/settings)                                                                                           |


### 5.3 启动方式

安装并登录后，有 5 种方式打开 Claude Code：


| 方式           | 操作                                                        | 适用场景            |
| ------------ | --------------------------------------------------------- | --------------- |
| **编辑器工具栏 ✦** | 打开任意文件后，点击右上角的 Spark 图标                                   | 最快捷的方式          |
| **活动栏**      | 点击左侧边栏的 Spark 图标                                          | 始终可见            |
| **状态栏**      | 点击右下角的 "✱ Claude Code" 文字                                 | 即使没有打开文件也能用     |
| **命令面板**     | `Cmd+Shift+P`（Mac）或 `Ctrl+Shift+P`（Win）→ 搜索 "Claude Code" | 偏好键盘操作的用户       |
| **快捷键**      | `Cmd+Esc`（Mac）或 `Ctrl+Esc`（Win）切换焦点到 Claude 输入框           | 快速切换编辑器和 Claude |


### 5.4 首次登录

1. 首次打开面板会显示登录页面，点击 **Sign in** 并在浏览器中完成认证
2. 如果使用 CLI 已登录过，可直接在终端用 `code .` 启动 VS Code 以继承环境变量
3. 登录后会出现「Learn Claude Code」引导清单，可以逐一学习或关闭

### 5.5 核心功能

#### 对话交互

直接在面板中输入自然语言，Claude 会根据上下文分析或修改代码：

```
解释一下这个函数的逻辑
给这段代码加错误处理
帮我重构这个模块
```

#### @ 引用文件和文件夹

在输入框中使用 `@` 引用上下文：

```
解释 @auth.js 的逻辑
@src/components/ 里有哪些组件？
检查 @app.ts#5-10 这段代码
```

- `@文件名` — 引用单个文件
- `@目录名/` — 引用整个目录（带斜杠表示目录）
- `@文件名#行号` — 引用具体行范围（自动插入选中代码）
- `@terminal:终端名` — 引用终端输出（无需复制粘贴）

#### 审阅变更（Diff 视图）

当 Claude 修改文件时，会显示**左右对比 Diff 视图**，你可以：

- **Accept** — 接受修改
- **Reject** — 拒绝修改
- **直接编辑 Diff** — 在 Diff 视图中手动修改后再接受

#### Plan 模式

点击输入框底部的权限模式，切换到 **Plan** 模式：

1. Claude 先生成完整的执行计划（Markdown 文档）
2. 你可以添加内联评论反馈
3. 审批通过后 Claude 才开始执行
4. 适合复杂功能开发、需要提前 review 的场景

#### 多标签会话

支持同时运行多个对话：

- 命令面板 → `Open in New Tab`（`Cmd+Shift+Esc` / `Ctrl+Shift+Esc`）开新会话
- 每个会话独立维护上下文和历史
- 支持拖拽面板到侧边栏、编辑区或新窗口

### 5.6 Slash Commands（命令菜单）

在输入框中输入 `/` 调出命令菜单：


| 命令                | 用途                           |
| ----------------- | ---------------------------- |
| `/model`          | 切换模型（Claude Sonnet / Opus 等） |
| `/compact`        | 手动压缩上下文                      |
| `/usage`          | 查看用量统计                       |
| `/mcp`            | 管理 MCP 服务连接                  |
| `/plugins`        | 管理插件界面                       |
| `/remote-control` | 启动远程控制会话                     |


### 5.7 设置与配置

#### VS Code 扩展设置

打开 VS Code 设置（`Cmd+,` / `Ctrl+,`）→ Extensions → Claude Code：


| 设置                              | 默认值       | 说明                                                              |
| ------------------------------- | --------- | --------------------------------------------------------------- |
| `useTerminal`                   | `false`   | 切换到终端模式（非图形面板）                                                  |
| `initialPermissionMode`         | `default` | 默认权限模式：`default` / `plan` / `acceptEdits` / `bypassPermissions` |
| `preferredLocation`             | `panel`   | Claude 打开位置：`sidebar`（右侧）/ `panel`（新标签）                         |
| `autosave`                      | `true`    | 自动保存文件                                                          |
| `enableNewConversationShortcut` | `false`   | 启用 `Cmd/Ctrl+N` 快捷键开新会话                                         |
| `respectGitIgnore`              | `true`    | 遵守 .gitignore 规则                                                |
| `environmentVariables`          | `[]`      | 为 Claude 进程设置额外的环境变量                                            |


#### 全局 Claude Code 设置

`~/.claude/settings.json` 在插件和 CLI 间共享：

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": ["Bash(git*)"],
    "deny": ["Read(.env)"]
  },
  "hooks": {
    "subagentStop": [
      {
        "command": "echo 'done'",
        "matcher": "done",
        "timeout": 30
      }
    ]
  }
}
```

### 5.8 插件管理

VS Code 插件内置了图形化的插件管理界面：

```bash
# 在输入框中输入
/plugins
```

插件管理界面支持：

- **安装/卸载插件** — 搜索并安装社区或官方插件
- **管理插件源（Marketplaces）** — 添加 GitHub 仓库、URL 或本地路径作为来源
- **安装范围选择** — 用户级（所有项目）、项目级（共享给团队）、本地（仅当前仓库）

### 5.9 Chrome 浏览器集成

可以连接 Chrome 浏览器测试 Web 应用：

```bash
# 需要先安装 Chrome 扩展 "Claude in Chrome"
# 在 VS Code 中输入
@browser go to localhost:3000 and check console for errors
```

Claude 可以打开新标签、读取页面内容、检查控制台错误。

### 5.10 快捷键速查


| 快捷键（Mac）        | 快捷键（Windows）     | 作用                      |
| --------------- | ---------------- | ----------------------- |
| `Cmd+Esc`       | `Ctrl+Esc`       | 在编辑器和 Claude 之间切换焦点     |
| `Cmd+Shift+Esc` | `Ctrl+Shift+Esc` | 在新标签中打开 Claude          |
| `Option+K`      | `Alt+K`          | 插入 @ 引用当前文件和选中行         |
| `Cmd+N`         | `Ctrl+N`         | 新对话（需启用设置）              |
| `Shift+Enter`   | `Shift+Enter`    | 输入框换行（不发消息）             |
| `Cmd+Shift+P`   | `Ctrl+Shift+P`   | 打开命令面板 → 搜索 Claude Code |


### 5.11 VS Code 插件 vs CLI 终端模式


| 能力                | VS Code 插件（图形面板） | CLI 终端模式        |
| ----------------- | ---------------- | --------------- |
| Diff 审阅视图         | ✅ 原生支持           | ✅ 集成 IDE 时支持    |
| @ 引用文件和行          | ✅                | ✅               |
| 多标签会话             | ✅                | ❌               |
| 插件管理界面            | ✅（图形化）           | ✅（`/plugin` 命令） |
| 全部 Slash Commands | 子集               | 完整              |
| MCP 管理            | 部分（可用 `/mcp`）    | 完整              |
| `!` Bash 快捷执行     | ❌                | ✅               |
| Tab 自动补全          | ❌                | ✅               |
| 对话历史              | ✅                | ✅               |


如果某个功能只在 CLI 中可用，只需在 VS Code 集成终端中运行 `claude` 即可使用。

### 5.12 macOS / Windows 差异

插件在 macOS 和 Windows 上**功能完全一致**，差异仅在快捷键：

- macOS 使用 `Cmd`、`Option` 键
- Windows 使用 `Ctrl`、`Alt` 键

### 5.13 SSH 连接远程开发

如果你通过 VS Code Remote SSH 连接到远程 Linux 服务器：

1. VS Code 需要安装 Remote SSH 扩展
2. Claude Code 插件配置在**本地**，远程服务器无需额外设置
3. 代码编辑、文件操作都在本地的 VS Code 中完成
4. 快捷键设置与本地开发完全一致

---

## 6. 以 DeepSeek 为例替换 API

> 根据 DeepSeek 官方文档（[https://api-docs.deepseek.com/zh-cn/guides/agent_integrations），DeepSeek](https://api-docs.deepseek.com/zh-cn/guides/agent_integrations），DeepSeek) 同时提供 **OpenAI 兼容** 和 **Anthropic 兼容** 两种 API 网关，分别适用于不同的工具。
>
> 本文覆盖主流工具：**Claude Code**（Anthropic 兼容）、**Cursor**（OpenAI 兼容）、**Aider**（OpenAI 兼容）、**OpenCode**（原生支持），以及 **SSH 连接远程服务器** 的场景，并区分 **macOS / Linux / Windows** 三种系统。

### 6.1 获取 DeepSeek API Key

1. 访问 [platform.deepseek.com](https://platform.deepseek.com) 注册
2. 在 API Keys 页面创建新 Key
3. 充值（DeepSeek 价格极低，¥1 可用很久）

### 6.2 在 Claude Code 中使用 DeepSeek（Anthropic 兼容）

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

### 6.3 在 Cursor 中替换为 DeepSeek

#### 步骤 1：打开模型设置

**Cursor → Settings → Models**（或搜索 "Models"）

#### 步骤 2：添加自定义模型


| 字段               | 填写内容                                           |
| ---------------- | ---------------------------------------------- |
| **API Provider** | 选择 **OpenAI** 或自定义                             |
| **Base URL**     | `https://api.deepseek.com`                     |
| **API Key**      | 你的 DeepSeek API Key                            |
| **Model ID**     | `deepseek-chat`（通用对话）或 `deepseek-reasoner`（推理） |


#### 步骤 3：启用模型

在模型列表中勾选刚添加的 `deepseek-chat`，取消勾选其他不需要的模型。

#### 步骤 4：验证

在 Chat 中发送一条消息，如果回复正常，说明配置成功。

> **注意**：Cursor 配置在 macOS 和 Windows 上 UI 完全相同，只有快捷键差异（macOS 用 `Cmd`，Windows 用 `Ctrl`）。

#### Cursor 各模式的兼容性


| 模式                                | 替换效果                    |
| --------------------------------- | ----------------------- |
| **Chat** (`Cmd+L` / `Ctrl+L`)     | 正常使用自定义模型               |
| **Composer** (`Cmd+I` / `Ctrl+I`) | 正常使用自定义模型               |
| **Tab Autocomplete**              | 可能不支持第三方模型，仍走 Cursor 自带 |
| **Ctrl+K 内联编辑**                   | 正常使用自定义模型               |


### 6.4 在 OpenCode 中使用 DeepSeek（原生支持）

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

### 6.5 在 Aider 中替换为 DeepSeek

```bash
# 用 DeepSeek 启动 Aider
export DEEPSEEK_API_KEY="sk-xxx"
aider --model deepseek-chat --api-key deepseek=$DEEPSEEK_API_KEY

# 或用 OpenAI 兼容模式
aider --model openai/deepseek-chat \
  --openai-api-key "sk-xxx" \
  --openai-api-base "https://api.deepseek.com"
```

### 6.6 快速测试 API 是否可用

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

### 6.7 SSH 连接远程 Linux 服务器的场景

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

### 6.8 常用国产模型兼容地址速查


| 厂商               | API 类型       | Base URL                                            | 推荐模型 ID                                |
| ---------------- | ------------ | --------------------------------------------------- | -------------------------------------- |
| **DeepSeek**     | OpenAI 兼容    | `https://api.deepseek.com`                          | `deepseek-chat`, `deepseek-reasoner`   |
| **DeepSeek**     | Anthropic 兼容 | `https://api.deepseek.com/anthropic`                | `deepseek-v4-pro`, `deepseek-v4-flash` |
| **阿里通义 Qwen**    | OpenAI 兼容    | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-max`, `qwen-coder-plus`          |
| **智谱 GLM**       | OpenAI 兼容    | `https://open.bigmodel.cn/api/paas/v4`              | `glm-4-plus`, `glm-4-flash`            |
| **阶跃星辰 StepFun** | OpenAI 兼容    | `https://api.stepfun.com/v1`                        | `step-2-16k`                           |


---

## 7. OpenSkill + anthropics/skills 安装配置

### 7.1 简介

**OpenSkills CLI**（`npx openskills`）是从 GitHub 仓库自动安装和管理 Skill 的工具，最重要的来源是 Anthropic 官方技能仓库 `anthropics/skills`。

### 7.2 安装 OpenSkills CLI

#### 前置条件


| 系统      | 前置要求                              |
| ------- | --------------------------------- |
| 全部      | Node.js **≥ 20.6**；Git            |
| macOS   | 推荐通过 Homebrew 或 nvm 安装 Node.js    |
| Linux   | 推荐通过 nvm 或包管理器安装 Node.js          |
| Windows | 推荐通过 nvm-windows 或官方安装包安装 Node.js |


#### 安装命令

```bash
# 方法一：直接使用 npx（无需安装，推荐所有系统）
npx openskills@latest --help

# 方法二：全局安装（macOS / Linux / Windows 通用）
npm i -g openskills
openskills --help
```

#### macOS 注意事项

- 如果全局安装后 `openskills` 命令找不到，检查 npm 全局 bin 路径：
  ```bash
  npm list -g openskills
  which openskills
  ```

#### Windows 注意事项

- 在 **PowerShell** 中执行安装命令
- 如果 `openskills` 命令找不到，将 npm 全局路径添加到环境变量：
  ```powershell
  $env:Path += ";$env:APPDATA\npm"
  ```
- Git 需要安装并配置在 PATH 中（[git-scm.com](https://git-scm.com/download/win)）

#### Linux 注意事项

- 如果使用 `npx openskills@latest` 首次下载较慢，可配置 npm 镜像：
  ```bash
  npm config set registry https://registry.npmmirror.com
  # 下载完成后可恢复默认
  # npm config set registry https://registry.npmjs.org
  ```

#### 官方资源


| 资源               | 链接                                                                             |
| ---------------- | ------------------------------------------------------------------------------ |
| npm 包地址          | [npmjs.com/package/openskills](https://www.npmjs.com/package/openskills)       |
| GitHub 仓库        | [github.com/suplant-inc/openskills](https://github.com/suplant-inc/openskills) |
| Anthropic 官方技能仓库 | [github.com/anthropics/skills](https://github.com/anthropics/skills)           |


### 7.3 安装 anthropics/skills 全部技能

```bash
# 安装到当前项目（推荐，Skill 会放在 .claude/skills/ 或 .agent/skills/）
cd your-project
npx openskills install anthropics/skills

# 或者安装到用户全局（所有项目可用）
npx openskills install anthropics/skills --global
```

### 7.4 只安装部分技能

OpenSkills 目前不支持按需选择子目录，但可以装完再删：

```bash
npx openskills install anthropics/skills

# 删除不需要的 skill
rm -rf .claude/skills/slack-gif-creator
rm -rf .claude/skills/algorithmic-art

# 重新生成 AGENTS.md
npx openskills sync
```

### 7.5 生成 AGENTS.md

```bash
# 生成项目 AGENTS.md（汇总所有已安装 skill）
npx openskills sync

# 也可以输出到指定文件
npx openskills sync -o SKILLS_INDEX.md
```

`AGENTS.md` 的作用是让 agent（或你在 Cursor 里 @ 它）知道当前项目装了哪些 skill、每个 skill 做什么用的。

### 7.6 管理已安装的技能

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

### 7.7 多项目共享全局技能

在多个项目中想用同一套 skill：

```bash
# 全局安装
npx openskills install anthropics/skills --global

# 每个项目里只需要执行（读取全局技能列表，生成项目 AGENTS.md）
cd project-a
npx openskills sync --global
```

### 7.8 安装后的目录结构

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

## 8. Skills 使用方式

### 8.1 在 Cursor 中使用 Skill

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

### 8.2 在 Claude Code 中使用 Skill

```bash
# 方法一：依赖自动匹配（description 中的提示词）
claude "处理这个 PDF 文件"

# 方法二：手动引用 AGENTS.md
claude -r AGENTS.md "请按照汇总的技能列表处理"
```

### 8.3 在 Aider 中使用 Skill

Aider 没有原生 Skill 机制，但可以用 `--read` 预加载：

```bash
# 把 SKILL.md 当指令读入
aider --read .claude/skills/pdf/SKILL.md "处理这个 PDF"

# 或者先读出 skill 内容再管道传给 Aider
npx openskills read pdf | aider --read - "处理"
```

### 8.4 Skill 覆盖的场景速览（anthropics/skills）


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

## 9. 案例：学术 Skill 安装和使用

### 9.1 场景

你需要一个能帮你在 **Claude Code / Cursor** 中辅助论文写作、文献调研、审稿回复的学术助手 Skill。

### 9.2 安装 academic-research-skills

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

### 9.3 在 Cursor 中使用学术 Skill

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

### 9.4 在 Claude Code 中使用

```bash
claude "使用 paper-writing skill 帮我润色这段论文摘要：[粘贴摘要]"
```

### 9.5 其他推荐的学术 Skill 仓库


| 仓库                                         | 安装方式                                                              | 适用场景                               |
| ------------------------------------------ | ----------------------------------------------------------------- | ---------------------------------- |
| `Master-cai/Research-Paper-Writing-Skills` | `npx openskills install Master-cai/Research-Paper-Writing-Skills` | ML/CV/NLP 论文段落优化、逻辑检查、审稿人自评        |
| `K-Dense-AI/scientific-agent-skills`       | `npx openskills install K-Dense-AI/scientific-agent-skills`       | 跨学科 133 科研 skill（数据分析、文献综述、科学写作）   |
| `LeonChaoX/qinyan-academic-skills`         | `npx openskills install LeonChaoX/qinyan-academic-skills`         | 181 学术 skill，18 分类（论文检索、科学写作、生物信息） |
| `Orchestra-Research/AI-Research-SKILLs`    | `npx openskills install Orchestra-Research/AI-Research-SKILLs`    | AI 研究 87 工程 skill（实验管理、ML 论文写作）    |


### 9.6 学术 Skill 的典型使用提示词

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

## 10. 案例：自定义 literature-tracker Skill

### 10.1 场景

你希望有一个 **文献追踪 Skill**，能自动搜索指定领域的最新论文、分析趋势并生成结构化报告。以下参考本仓库 `[examples/literature-tracker/](../examples/literature-tracker/)` 的完整实现（该 skill 已复制到仓库中）。



实际的建立过程。就是利用Anthrophic的官方skill。利用Skill-Creator这个skill，直接向其描述上述的场景，agent可以自己建立这个skill。

在自己有个性化需求时，都可以参照这个工作流程，建立自己的skill。尽量不要自己手写skill，因为skill比较需要结构化。

下文是形成的skill的结果的简单介绍。

### 10.2 Skill 目录结构

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

### 10.3 SKILL.md 核心内容

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

### 10.4 安装自定义 Skill

```bash
# 方法一：直接放入 Cursor 项目 skill 目录
mkdir -p .cursor/skills/literature-tracker/scripts
mkdir -p .cursor/skills/literature-tracker/templates

# 把 SKILL.md、脚本、模板分别放入对应位置

# 方法二：通过 npx openskills 从本地安装
npx openskills install /path/to/literature-tracker
```

### 10.5 在 Cursor 中使用

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

### 10.6 写成 OpenSkill 格式（通用）

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

### 10.8 自定义 Skill 的最佳实践


| 要点                     | 说明                                 |
| ---------------------- | ---------------------------------- |
| **description 写清楚触发词** | 中英文都要覆盖，包含各种可能的问法                  |
| **流程拆成阶段**             | 让 agent 一步步执行，不容易遗漏关键步骤            |
| **提供快速开始模板**           | 用户看到直接可以复制的提示词，降低使用门槛              |
| **脚本放 scripts/**       | 复杂逻辑不要让 agent 现场写，预置为可执行脚本         |
| **数据 schema 另放**       | 数据结构定义放在 templates/ 中，SKILL.md 里引用 |
| **写负面约束**              | 明确"不要做什么"，比只写"要做什么"更有效             |


