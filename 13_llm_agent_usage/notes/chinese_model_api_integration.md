# 在 Cursor、Claude Code 等工具中使用中国 coding 模型

> 目标：在 **日常用的 coding 工具**（Cursor、VS Code 插件、Aider、Claude 系等）里，把 **DeepSeek、通义 Qwen、智谱 GLM** 等国内可调用、偏代码能力的模型接进来用，而不是只讲裸 HTTP / Python SDK。
>
> 核心事实：**大多数工具只认一种「大入口」**——在它们眼里，国产云厂商只要提供 **OpenAI 兼容的 Chat Completions**（`base_url` + `api_key` + `model`），就可以当作「自定义 OpenAI 端点」来配。

## 1. 为什么要接「中国 coding 模型」

| 动机 | 说明 |
|------|------|
| **成本** | 同等工作量，部分国产模型比海外旗舰便宜一个数量级。 |
| **网络** | 国内线路访问国内 API 时延往往更低。 |
| **中文与业务注释** | 对中文需求描述、国内框架栈更稳一些（非绝对）。 |
| **合规与账号** | 企业采购、发票、数据驻留时选国内云更常见。 |

**代价**：各工具对「自定义模型」的 **Tab 补全 / Chat / Agent(Composer) / 工具调用** 支持不一致，需要**实测**：同一 `base_url`，有的只能聊天，不能当 Agent 主模型。

## 2. 适合「写代码」的国产/国内可调用模型（速查）

以下名称以各厂商**当前 API 文档**为准；变更快，以控制台里的「模型 ID」为最终依据。

| 厂商 | 常用 coding/通用模型名（示例） | OpenAI 兼容 `base_url`（示例） |
|------|--------------------------------|--------------------------------|
| **DeepSeek** | `deepseek-chat`（V3 对话/代码）、`deepseek-reasoner`（R1 推理，偏慢但强） | `https://api.deepseek.com` |
| **阿里通义** | `qwen-coder-plus`、`qwen2.5-coder-32b-instruct`、`qwen-max` 等 | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| **智谱** | `glm-4-plus`、`glm-4-air`、`glm-4-flash` 等 | `https://open.bigmodel.cn/api/paas/v4` |
| **阶跃 StepFun** | `step-2-16k` / `step-1-360-chat` 等以文档为准 | `https://api.stepfun.com/v1` |
| **MiniMax** | 以官方模型列表为准 | `https://api.minimax.chat/v1` |

**选型经验（coding 场景）**：

- 要 **长上下文 + 多文件改仓库**：优先选 **Qwen Coder 系列、DeepSeek Chat** 里标明支持长上下文的款。
- 要 **强推理/数学/协议栈**：可试 `deepseek-reasoner`（时延和费用更高）。
- 要 **先跑通工具链**：**DeepSeek + Qwen 兼容端** 在「OpenAI 兼容 + function calling」上社区反馈相对多，但仍要以你本机 + 当前工具版本测为准。

## 3. 通用接法：在工具里填这三样

1. **API Key**：在云控制台创建（勿提交到 git）。
2. **Base URL**：厂商提供的 **OpenAI 兼容** 根地址（注意是否已含 `/v1`，以文档为准）。
3. **Model ID**：控制台里的**精确字符串**（如 `deepseek-chat`，不要自造 `deepseek-v4-pro` 这类未在文档出现的名字）。

在工具侧，常见标签名是：

- **OpenAI API Key** + **Override OpenAI Base URL** / **Custom OpenAI API base**
- 或 **OpenAI-compatible** provider 下的 `baseUrl` + `apiKey` + `model`

---

## 4. Cursor

### 4.1 配在哪里

打开 **Cursor → Settings（设置）→ Models**（或 **Features** 下与模型相关的页，随版本可能改名）：

- 打开 **使用自己的 API Key**（OpenAI 或 OpenAI 兼容类选项）。
- 填写 **Base URL** 为国产厂商的兼容地址，例如 `https://api.deepseek.com` 或 Qwen 的 `.../compatible-mode/v1`。
- 在模型列表中 **Add model**，把 **官方模型 ID** 填进去，例如 `deepseek-chat`。

不同 Cursor 版本 UI 有差异，若找不到项：在设置里搜索 `OpenAI`、`Base URL`、`Override`。

### 4.2 能用在哪些能力上（务必实测）

- **Chat / 对话**：一般最容易成功。
- **Composer / Agent**：是否允许选「自定义模型」、是否 **支持多步编辑 + 工具**，随版本与策略变化，**以你当前版本为准**。
- **Tab 补全**：很多产品对**补全**单独用一套模型，不一定跟 Chat 用同一个自定义端点。

### 4.3 建议的自测

1. 只开一个中小仓库，**先问一句「解释 `src/xxx` 的入口」** —— 验证能读项目。
2. 再试 **改一个小函数 + 跑测试** —— 验证多轮与编辑。
3. 若需 **MCP/工具调用**，观察是否能稳定触发；不行则换模型或把「工具重活」放终端（Aider）做。

### 4.4 与 Anthropic 官方额度的关系

在 Cursor 里，**自己填的 OpenAI 兼容 key** 与 **Claude/Anthropic 官方订阅/额度** 是不同计费体系；具体扣费以 Cursor 与厂商文档说明为准。

---

## 5. VS Code 生态：Continue / Cline 等

思路与 Cursor 类似，多在插件设置里选 **OpenAI compatible**，填：

- `apiKey`
- `baseUrl`
- `model`

部分插件用 **yaml/json** 配置，例如 Continue 的 `config.json` / `~/.continue/config`（路径随版本变）。**以插件官方文档为准**。

**优点**：可和国产模型深度绑定、偏开源。**缺点**：要自己会配、升级插件后要复查一遍。

---

## 6. Aider（终端，对国产很友好）

Aider 通过环境变量接 **OpenAI 兼容** 端，社区用它配 DeepSeek/Qwen 的教程最多。

```bash
export OPENAI_API_KEY="你的 key"
export OPENAI_API_BASE="https://api.deepseek.com"   # 或 Qwen 的 compatible-mode 地址

aider --model openai/deepseek-chat
```

- `--model` 的写法随 Aider 版本而变，若报找不到模型，用 `aider --help` 看当前**模型名规范**。

---

## 7. Claude Code / 官方 Anthropic 客户端

**重要**：**Claude Code 与官方 Claude 应用默认走 Anthropic 账号与 API**，**不是**在设置里直接填一个 `https://api.deepseek.com` 就等价于「换国产模型」。

**可行路径**只有几类，且多数偏企业/高阶：

1. **继续用官方 Claude 模型**做主力（能力、工具、合规由 Anthropic 保证）。
2. 若你司有 **LLM 网关/代理**，把国内模型接到**统一入口**，再由网关暴露成**已被 Claude Code 支持的一种协议/供应商**（视内部基建而定，个人用户很少具备）。
3. 个人日常想主力用 **国产 coding 模型**：更实际的是 **Cursor / VS Code 插件 / Aider**（上文的 OpenAI 兼容配置）。

不要混淆：**同名的「在 Cursor 里用 Claude」与「在 Claude Code 里用国产 API」** 不是同一套配置方式。

---

## 8. GitHub Copilot / OpenAI Codex CLI

- **GitHub Copilot** 以 **Microsoft/OpenAI 商业合作** 为主，**不**以「随意填国内 base_url」为常规能力；若企业有 **Azure OpenAI 或自托管** 且管理员开启，才可能有统一端点，这里不展开个人破解方案。
- **Codex CLI** 绑定 OpenAI 生态。要用国产，通常要 **能暴露 OpenAI 兼容 API 的中转**（**合规前提下**由企业 IT 配），**个人不建议**绕服务条款自行转发。

---

## 9. 接进来以后仍要自测的 4 件事

| 项目 | 为什么重要 |
|------|------------|
| **模型 ID 与 base_url 完全正确** | 少 `/v1`、多拼路径是高频错误。 |
| **长上下文** | coding 要读多文件，窗口不够会乱编。 |
| **Function calling / 工具** | agent 多步任务依赖；国产模型与版本差异大。 |
| **流式输出** | 有的工具默认开 stream，有的模型要关 stream 才稳定。 |

**最小工具调用自测**（先在你本机用任意 OpenAI 兼容脚本跑通，再进 IDE，避免被 IDE 配置干扰）：

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

能稳定执行后，再到 Cursor 里配同一 `base_url` 与 `model`。

---

## 10. 常见问题

1. **填了 key 但 401/403**：检查 key、是否开余额、**是否限制地域/IP**、模型是否对该 key 开放。
2. **只有 Chat 能用，Agent 变灰**：多为**产品策略或该模型未通过 Agent 能力认证**，可换功能或换工具（如 Aider）。
3. **工具调用时灵时不灵**：换模型/降任务复杂度/减少并行工具数；仍不行就用「人审 diff + 单步跑命令」的 workflow。
4. **迷信「某某-pro」非官方名**：**以云控制台/文档里的 `model` 为准**。

---

## 11. 与第 07 章「API 速查」的关系

- 本章：**IDE / 终端 / coding agent 工具**里**怎么接、怎么测、各工具策略差异**。
- [`07_frameworks/notes/chinese_model_apis.md`](../../07_frameworks/notes/chinese_model_apis.md)：更偏**接口表、Python 统一写法、和本仓库 `utils/llm_client` 结合**的备忘。

两章可以一起看：在 IDE 里配通后，**同一套 `base_url` + key** 也可用于自研脚本与第 3 章 notebook。
