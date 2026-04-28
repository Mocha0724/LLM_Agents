# 在 Cursor、Claude Code 等工具中使用中国 coding 模型

> 目标：在 **日常用的 coding 工具**（Cursor、Claude Code、Aider、OpenCode、VS Code 插件）里，把 **DeepSeek、通义 Qwen、智谱 GLM** 等国内可调用、偏代码能力的模型接进来用。
>
> **2026 年重要更新**：DeepSeek 官方已提供 **Anthropic 兼容 API 网关**（`https://api.deepseek.com/anthropic`），Claude Code 可以通过设置环境变量直接接入 DeepSeek 模型，无需通过其他中转。

---

## 1. 为什么要接「中国 coding 模型」


| 动机          | 说明                       |
| ----------- | ------------------------ |
| **成本**      | 同等工作量，部分国产模型比海外旗舰便宜一个数量级 |
| **网络**      | 国内线路访问国内 API 时延往往更低      |
| **中文与业务注释** | 对中文需求描述、国内框架栈更稳一些（非绝对）   |
| **合规与账号**   | 企业采购、发票、数据驻留时选国内云更常见     |


**代价**：各工具对「自定义模型」的 **Tab 补全 / Chat / Agent(Composer) / 工具调用** 支持不一致，需要**实测**。

---

## 2. 适合「写代码」的国产/国内可调用模型（速查）


| 厂商                         | 常用 coding/通用模型名                                           | OpenAI 兼容 `base_url`（示例）                            |
| -------------------------- | --------------------------------------------------------- | --------------------------------------------------- |
| **DeepSeek**               | `deepseek-chat`（对话/代码）、`deepseek-reasoner`（推理）            | `https://api.deepseek.com`                          |
| **DeepSeek**（Anthropic 兼容） | `deepseek-v4-pro`、`deepseek-v4-flash`                     | `https://api.deepseek.com/anthropic`                |
| **阿里通义**                   | `qwen-coder-plus`、`qwen2.5-coder-32b-instruct`、`qwen-max` | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| **智谱**                     | `glm-4-plus`、`glm-4-air`、`glm-4-flash`                    | `https://open.bigmodel.cn/api/paas/v4`              |
| **阶跃 StepFun**             | `step-2-16k` / `step-1-360-chat` 等                        | `https://api.stepfun.com/v1`                        |
| **MiniMax**                | 以官方模型列表为准                                                 | `https://api.minimax.chat/v1`                       |


---

## 3. Claude Code 中接入 DeepSeek

> DeepSeek 官方提供了 **Anthropic 兼容 API**，Claude Code 可以通过环境变量直接使用 DeepSeek 模型，无需通过第三方中转。
>
> 参考官方文档：[https://api-docs.deepseek.com/zh-cn/guides/agent_integrations/claude_code](https://api-docs.deepseek.com/zh-cn/guides/agent_integrations/claude_code)



同样注意，尽量参考官网的最新指南，这里的不一定准确。

### 3.1 前置条件

- 安装 [Node.js](https://nodejs.org/zh-cn/download/) **18+**
- 已全局安装 Claude Code：`npm install -g @anthropic-ai/claude-code`
- 在 [DeepSeek Platform](https://platform.deepseek.com/api_keys) 获取 API Key

### 3.2 macOS / Linux 配置

```bash
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN=<你的 DeepSeek API Key>
export ANTHROPIC_MODEL=deepseek-v4-pro
export ANTHROPIC_DEFAULT_OPUS_MODEL=deepseek-v4-pro
export ANTHROPIC_DEFAULT_SONNET_MODEL=deepseek-v4-pro
export ANTHROPIC_DEFAULT_HAIKU_MODEL=deepseek-v4-flash
export CLAUDE_CODE_SUBAGENT_MODEL=deepseek-v4-flash
export CLAUDE_CODE_EFFORT_LEVEL=max
```

### 3.3 Windows 配置（PowerShell）

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

### 3.4 持久化配置

为了避免每次打开终端都重设环境变量，建议写入 shell 配置文件：

**macOS / Linux（zsh）**——`~/.zshrc`：

```bash
# DeepSeek for Claude Code
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN="sk-xxxxxxxxxxxxxxxx"
export ANTHROPIC_MODEL=deepseek-v4-pro
export ANTHROPIC_DEFAULT_OPUS_MODEL=deepseek-v4-pro
export ANTHROPIC_DEFAULT_SONNET_MODEL=deepseek-v4-pro
export ANTHROPIC_DEFAULT_HAIKU_MODEL=deepseek-v4-flash
export CLAUDE_CODE_SUBAGENT_MODEL=deepseek-v4-flash
export CLAUDE_CODE_EFFORT_LEVEL=max
```

**macOS / Linux（bash）**——`~/.bashrc` 或 `~/.bash_profile`：

```bash
# 同上内容
```

**Windows（PowerShell）**——`$PROFILE` 文件：

```powershell
# 查找并编辑 PowerShell profile
notepad $PROFILE

# 添加以下内容
$env:ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
$env:ANTHROPIC_AUTH_TOKEN="sk-xxxxxxxxxxxxxxxx"
$env:ANTHROPIC_MODEL="deepseek-v4-pro"
$env:ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro"
$env:ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-pro"
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_SUBAGENT_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_EFFORT_LEVEL="max"
```

### 3.5 使用

```bash
# 进入项目目录
cd /path/to/my-project

# 启动 Claude Code（已自动使用 DeepSeek 模型）
claude
```

### 3.6 环境变量说明


| 环境变量                             | 作用           | 推荐值                                  |
| -------------------------------- | ------------ | ------------------------------------ |
| `ANTHROPIC_BASE_URL`             | API 端点地址     | `https://api.deepseek.com/anthropic` |
| `ANTHROPIC_AUTH_TOKEN`           | API 认证 Token | 你的 DeepSeek API Key                  |
| `ANTHROPIC_MODEL`                | 主模型          | `deepseek-v4-pro`                    |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`   | 最优模型（规划/执行）  | `deepseek-v4-pro`                    |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | 平衡模型（执行/验证）  | `deepseek-v4-pro`                    |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`  | 轻量模型（快速任务）   | `deepseek-v4-flash`                  |
| `CLAUDE_CODE_SUBAGENT_MODEL`     | 子代理模型        | `deepseek-v4-flash`                  |
| `CLAUDE_CODE_EFFORT_LEVEL`       | 推理努力级别       | `max`                                |


> **注意**：`deepseek-v4-pro` 和 `deepseek-v4-flash` 是 DeepSeek Anthropic 兼容网关下的模型 ID，与 OpenAI 兼容端点的 `deepseek-chat` / `deepseek-reasoner` 不同。请以 DeepSeek 官方文档为准。

### 3.7 排错


| 问题             | 检查点                                        |
| -------------- | ------------------------------------------ |
| `claude` 报连接错误 | 确认 `ANTHROPIC_BASE_URL` 拼写正确，末尾无 `/`       |
| 认证失败 401       | 确认 `ANTHROPIC_AUTH_TOKEN` 是有效 DeepSeek Key |
| 模型不存在          | 确认 DeepSeek 官方文档中 Anthropic 兼容的模型 ID 列表    |
| Windows 下变量不生效 | 使用 `$env:` 前缀设置，或重启终端                      |


---

## 4. Cursor

### 4.1 配在哪里

打开 **Cursor → Settings（设置）→ Models**（或 Features 下与模型相关的页，随版本可能改名）：

- 打开 **使用自己的 API Key**（OpenAI 或 OpenAI 兼容类选项）。
- 填写 **Base URL** 为国产厂商的兼容地址，例如 `https://api.deepseek.com` 或 Qwen 的 `.../compatible-mode/v1`。
- 在模型列表中 **Add model**，把 **官方模型 ID** 填进去，例如 `deepseek-chat`。

不同 Cursor 版本 UI 有差异，若找不到项：在设置里搜索 `OpenAI`、`Base URL`、`Override`。

### 4.2 能用在哪些能力上（务必实测）


| 模式                     | 替换效果                          |
| ---------------------- | ----------------------------- |
| **Chat** (`Cmd+L`)     | 一般最容易成功                       |
| **Composer** (`Cmd+I`) | 随版本与策略变化，**以你当前版本为准**         |
| **Tab 补全**             | 可能单独用一套模型，不一定跟 Chat 用同一个自定义端点 |


### 4.3 与 Anthropic 官方额度的关系

在 Cursor 里，**自己填的 OpenAI 兼容 key** 与 **Claude/Anthropic 官方订阅/额度** 是不同计费体系；具体扣费以 Cursor 与厂商文档说明为准。

### 4.4 macOS / Windows 差异

Cursor 是跨平台桌面应用，**设置界面在 macOS 和 Windows 上完全一致**（UI 位置相同）。唯一的差异是：

- **macOS**：快捷键使用 `Cmd`（如 `Cmd+I`、`Cmd+L`）
- **Windows**：快捷键使用 `Ctrl`（如 `Ctrl+I`、`Ctrl+L`）

### 4.5 SSH 连接 Linux 服务器场景

如果你在本地 macOS/Windows 上通过 SSH 连接到远程 Linux 开发服务器：

1. **本地 Cursor 安装**：Cursor 是桌面应用，安装在本地机器上。
2. **远程开发**：使用 Cursor 的 **Remote SSH** 插件（与 VS Code Remote SSH 类似）连接到远程 Linux 服务器。
3. **模型配置**：API Key 和 Base URL 的配置在**本地的 Cursor 设置**中完成，与远程服务器无关。
4. **网络注意**：远程服务器不需要访问 DeepSeek API，但本地机器需要。如果本地无法直连国内 API，可以在本地配置代理。

---

## 5. VS Code 生态：Continue / Cline 等

思路与 Cursor 类似，多在插件设置里选 **OpenAI compatible**，填 `apiKey` + `baseUrl` + `model`。

部分插件用 **yaml/json** 配置，例如 Continue 的 `config.json` / `~/.continue/config`（路径随版本变）。**以插件官方文档为准**。

---

## 6. Aider（终端，对国产很友好）

```bash
export OPENAI_API_KEY="你的 key"
export OPENAI_API_BASE="https://api.deepseek.com"

aider --model openai/deepseek-chat
```

`--model` 的写法随 Aider 版本而变，若报找不到模型，用 `aider --help` 看当前**模型名规范**。

---

## 7. OpenCode

### 7.1 简介

**OpenCode** 是一个开源的 AI 编程助手，支持终端和网页两种运行形式。它原生支持多模型供应商切换，对 DeepSeek 等国产模型有良好的开箱体验。

> 参考官方文档：[https://api-docs.deepseek.com/zh-cn/guides/agent_integrations/opencode](https://api-docs.deepseek.com/zh-cn/guides/agent_integrations/opencode)

### 7.2 安装

**macOS / Linux**：

```bash
# 推荐使用 brew 安装（macOS）
brew install opencode

# 或使用 npm
npm install -g @opencode-ai/cli

# 验证
opencode --version
```

**Windows**：

```bash
# Windows 使用 npm 安装
npm install -g @opencode-ai/cli

# 验证
opencode --version
```

**环境要求**：

- **OpenCode 版本 ≥ v1.14.24**（建议升级到最新版本以避免兼容性问题）
- Node.js 18+

### 7.3 配置 DeepSeek 模型

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

配置完成后，OpenCode 会自动使用 DeepSeek 模型进行代码生成和对话。

### 7.4 配置其他国产模型

OpenCode 的 `/connect` 命令支持多种供应商，包括 Qwen、GLM 等。如果列表中没有，可以选择「自定义 OpenAI 兼容」选项，手动填写 `base_url` 和 `api_key`。

### 7.5 macOS / Windows 差异


| 维度   | macOS                           | Windows                           |
| ---- | ------------------------------- | --------------------------------- |
| 安装方式 | `brew install opencode` 或 `npm` | `npm install -g @opencode-ai/cli` |
| 终端   | Terminal / iTerm2               | PowerShell / CMD                  |
| 使用方式 | 完全相同 — OpenCode 是跨平台 CLI 工具     |                                   |


### 7.6 SSH 连接 Linux 服务器场景

如果你通过 SSH 连接到远程 Linux 服务器：

1. **远程服务器安装 OpenCode**：
  ```bash
   # 在远程 Linux 服务器上
   npm install -g @opencode-ai/cli
  ```
2. **在 SSH 会话中配置**：
  ```bash
   # 通过 SSH 连接到远程
   ssh user@remote-server

   # 启动 OpenCode 并配置模型
   cd /path/to/project
   opencode
   # 输入 /connect → 选择 deepseek
  ```
3. **网络注意**：确保远程服务器能访问 DeepSeek API（`https://api.deepseek.com`）。如果服务器在内网（无公网访问），需要配置代理或使用内部 API 网关。

---

## 8. GitHub Copilot / OpenAI Codex CLI

- **GitHub Copilot** 以 Microsoft/OpenAI 商业合作为主，不开放随意填国内 `base_url`。
- **Codex CLI** 绑定 OpenAI 生态，要用国产通常需要中转。

---

## 9. 接进来以后仍要自测的 4 件事


| 项目                        | 为什么重要                            |
| ------------------------- | -------------------------------- |
| **模型 ID 与 base_url 完全正确** | 少 `/v1`、多拼路径是高频错误                |
| **长上下文**                  | coding 要读多文件，窗口不够会乱编             |
| **Function calling / 工具** | agent 多步任务依赖；国产模型与版本差异大          |
| **流式输出**                  | 有的工具默认开 stream，有的模型要关 stream 才稳定 |


**最小工具调用自测**（先在你本机用任意 OpenAI 兼容脚本跑通，再进 IDE）：

```python
from openai import OpenAI

client = OpenAI(
    api_key="KEY",
    base_url="https://api.deepseek.com",
)

r = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "用 JSON 只返回：{\"a\":1}"}],
)
print(r.choices[0].message.content)
```

---

## 10. SSH 连接远程 Linux 开发环境通用指南

如果你在本地使用 macOS/Windows，通过 SSH 连接到远程 Linux 服务器进行开发：

### 10.1 场景判断


| 你的情况                   | 推荐方式                                    |
| ---------------------- | --------------------------------------- |
| 本地 Cursor + 远程服务器代码    | Cursor Remote SSH（模型配置在本地）              |
| 本地终端 SSH 到服务器，用 CLI 工具 | 在远程服务器安装 Claude Code / OpenCode / Aider |
| 纯远程开发（服务器是主力机）         | 直接在服务器上安装 CLI 工具                        |


### 10.2 Cursor Remote SSH 方式

Cursor 支持 VS Code 的 Remote SSH 插件：

1. 本地安装 Cursor
2. 安装 Remote SSH 扩展（`Cmd+Shift+X` → 搜索 "Remote SSH"）
3. 通过 `Cmd+Shift+P` → `Remote-SSH: Connect to Host` 连接远程服务器
4. **模型配置在本地 Cursor 设置中完成**，远程服务器不需要任何 API 配置
5. 代码编辑、文件操作都在本地完成，通过 SSH 同步到远程

### 10.3 远程服务器 CLI 方式

如果直接在远程服务器上使用 CLI 工具：

```bash
# 在远程服务器上安装 Node.js（如果还没有）
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# 安装 Claude Code（如果需要）
npm install -g @anthropic-ai/claude-code

# 设置环境变量
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN=sk-xxxxxxxxxx
export ANTHROPIC_MODEL=deepseek-v4-pro

# 或者安装 OpenCode
npm install -g @opencode-ai/cli
```

**网络注意事项**：

- 确保远程服务器能访问 DeepSeek API
- 如果服务器在内网，需要配置 HTTP 代理：
  ```bash
  export HTTP_PROXY=http://proxy-server:port
  export HTTPS_PROXY=http://proxy-server:port
  ```

### 10.4 Windows SSH 客户端推荐


| 工具                     | 特点                                   |
| ---------------------- | ------------------------------------ |
| **Windows Terminal**   | 微软官方，支持多标签页，推荐                       |
| **PowerShell 7+**      | 内置 SSH 客户端                           |
| **WSL 2**              | 在 Windows 上运行 Linux 子系统，体验与 Linux 一致 |
| **VS Code Remote SSH** | 与 Cursor Remote SSH 同一技术，纯 GUI 操作    |


---

## 11. 常见问题

1. **填了 key 但 401/403**：检查 key、是否开余额、**是否限制地域/IP**、模型是否对该 key 开放。
2. **只有 Chat 能用，Agent 变灰**：多为**产品策略或该模型未通过 Agent 能力认证**，可换功能或换工具（如 Aider）。
3. **工具调用时灵时不灵**：换模型/降任务复杂度/减少并行工具数；仍不行就用「人审 diff + 单步跑命令」的 workflow。
4. **迷信「某某-pro」非官方名**：**以云控制台/文档里的 `model` 为准**。
5. **Claude Code 配了 DeepSeek 但启动报错**：确认所有 8 个环境变量都设置正确，特别是 `ANTHROPIC_BASE_URL` 末尾不能有空格或斜杠。

