# 中国模型 API 接入方案

> 目标：把 DeepSeek、Qwen、GLM、StepFun、MiniMax 等国产模型接入 coding agent、LLM agent 或自研工具。核心原则是：**优先使用 OpenAI Compatible API**。

## 1. 主流国产模型 API 速查

| 厂商 | 推荐模型 | OpenAI 兼容 base_url | 适合场景 |
|------|----------|----------------------|----------|
| **DeepSeek** | `deepseek-chat` / `deepseek-reasoner` | `https://api.deepseek.com` | 低成本对话、推理、代码 |
| **阿里 Qwen** | `qwen-max` / `qwen-plus` / `qwen-coder-plus` | `https://dashscope.aliyuncs.com/compatible-mode/v1` | 通用、代码、多模态 |
| **智谱 GLM** | `glm-4-plus` / `glm-4-flash` | `https://open.bigmodel.cn/api/paas/v4` | 中文场景、低成本 batch |
| **阶跃星辰 StepFun** | `step-2-16k` / `step-1-flash` | `https://api.stepfun.com/v1` | 轻量应用、兼容 OpenAI |
| **MiniMax** | `abab6.5s-chat` 等 | `https://api.minimax.chat/v1` | 长文本、中文应用 |
| **百度 ERNIE** | `ernie-4.0` | 以千帆文档为准 | 企业百度云生态 |
| **讯飞星火** | `spark-4.0-ultra` | 以星火文档为准 | 中文办公与教育场景 |

> 模型名更新较快，实际使用前以厂商文档为准。coding agent 场景尤其要确认该模型是否支持稳定的 tool use / function calling。

## 2. 通用 Python 调用方式

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.deepseek.com",
)

resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个严谨的编程助手。"},
        {"role": "user", "content": "写一个 Python 函数判断回文字符串。"},
    ],
)

print(resp.choices[0].message.content)
```

## 3. DeepSeek 接入

### 3.1 Python

```python
from openai import OpenAI

client = OpenAI(
    api_key="DEEPSEEK_API_KEY",
    base_url="https://api.deepseek.com",
)

resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "解释 ReAct agent。"}],
)
print(resp.choices[0].message.content)
```

### 3.2 R1 推理模型

```python
resp = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[{"role": "user", "content": "证明 1+...+n=n(n+1)/2"}],
)

msg = resp.choices[0].message
print(getattr(msg, "reasoning_content", ""))  # 推理过程，可能随 SDK 版本不同
print(msg.content)                            # 最终回答
```

### 3.3 接入 Aider

```bash
export OPENAI_API_KEY=$DEEPSEEK_API_KEY
export OPENAI_API_BASE=https://api.deepseek.com

aider --model openai/deepseek-chat
```

### 3.4 接入自研 agent

```python
client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)
```

## 4. Qwen / 通义千问接入

### 4.1 Python

```python
from openai import OpenAI

client = OpenAI(
    api_key="DASHSCOPE_API_KEY",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

resp = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "用 LangGraph 写一个三节点 agent 结构。"}],
)
print(resp.choices[0].message.content)
```

### 4.2 代码模型

Qwen Coder 系列适合：

- 自动补全。
- 代码解释。
- 单文件/多文件修改。
- 配合 Aider / Continue / Cline 做 coding agent。

使用时重点关注：

- 上下文窗口。
- diff 输出稳定性。
- function calling 支持状态。

## 5. GLM / 智谱接入

```python
from openai import OpenAI

client = OpenAI(
    api_key="ZHIPU_API_KEY",
    base_url="https://open.bigmodel.cn/api/paas/v4",
)

resp = client.chat.completions.create(
    model="glm-4-flash",
    messages=[{"role": "user", "content": "总结 AgentBench 的评测维度。"}],
)
print(resp.choices[0].message.content)
```

注意：

- 智谱的 free / flash 模型适合 batch eval、摘要、分类。
- 做 coding agent 时要先测 function calling / patch 输出能力。

## 6. StepFun / MiniMax 接入

```python
client = OpenAI(
    api_key="STEPFUN_API_KEY",
    base_url="https://api.stepfun.com/v1",
)

resp = client.chat.completions.create(
    model="step-1-flash",
    messages=[{"role": "user", "content": "写一段 agent 安全 checklist。"}],
)
```

MiniMax 类似：

```python
client = OpenAI(
    api_key="MINIMAX_API_KEY",
    base_url="https://api.minimax.chat/v1",
)
```

## 7. 在 coding agent 工具里的配置思路

### 7.1 Aider

Aider 对自定义 OpenAI compatible endpoint 支持最好：

```bash
export OPENAI_API_KEY=$DEEPSEEK_API_KEY
export OPENAI_API_BASE=https://api.deepseek.com
aider --model openai/deepseek-chat
```

### 7.2 Cursor / Continue / Cline

通常在设置里配置：

```yaml
provider: openai-compatible
base_url: https://api.deepseek.com
api_key: ${DEEPSEEK_API_KEY}
model: deepseek-chat
```

检查点：

- 是否支持 streaming。
- 是否支持 tool calling。
- 是否支持长上下文。
- 是否允许作为 agent / composer 模型，而不仅是 chat 模型。

### 7.3 OpenHands / 自研 Agent

OpenHands / 自研 agent 通常走 LiteLLM 或 OpenAI SDK：

```bash
export LLM_MODEL=deepseek/deepseek-chat
export DEEPSEEK_API_KEY=...
```

或在代码中：

```python
client = OpenAI(
    api_key=os.environ["QWEN_API_KEY"],
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
```

## 8. Tool Use / Function Calling 注意事项

国产模型做 agent 时最容易出问题的是 tool calling。建议用以下测试：

```python
tools = [{
    "type": "function",
    "function": {
        "name": "add",
        "description": "计算两个数字之和",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"},
            },
            "required": ["a", "b"],
        },
    },
}]

resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "计算 123 + 456"}],
    tools=tools,
)
print(resp.choices[0].message.tool_calls)
```

测试点：

- 是否能正确选择工具。
- 参数 JSON 是否严格合法。
- 多工具并发调用是否稳定。
- 工具结果回填后是否能继续推理。

## 9. 推荐组合

| 目标 | 推荐 |
|------|------|
| 低成本 coding agent | Aider + DeepSeek Chat |
| 复杂推理型 agent | DeepSeek Reasoner / Qwen Max |
| 中文文档、摘要、批处理 | GLM Flash / Qwen Plus |
| 国内低延迟线上服务 | Qwen / DeepSeek / StepFun |
| 多模态 agent | Qwen-VL / GLM-4V |

## 10. 常见坑

1. **模型名写错**：很多工具里不是 `deepseek-v4-pro`，而是厂商 API 文档里的正式模型名，例如 `deepseek-chat`。
2. **base_url 少 `/v1` 或多 `/v1`**：不同厂商不一致，以文档为准。
3. **工具只支持 chat，不支持 agent**：有些 IDE 允许自定义 chat 模型，但 composer/agent 模型仍有限制。
4. **function calling 格式不兼容**：先用最小工具调用测试。
5. **上下文太短**：coding agent 需要读项目，模型上下文短会明显影响体验。
