# 笔记 · 中国产模型 API 使用指南

> OpenAI 兼容 API 是事实标准。国内主流模型厂商几乎全部实现了 OpenAI SDK 兼容接口，切换只需改 `base_url` + `api_key`。

## 1. 主流模型与 API 入口

| 厂商 | 模型 | API base_url | 特点 |
|------|------|-------------|------|
| **DeepSeek** | deepseek-chat (V3 / R1) | `https://api.deepseek.com` | 性价比极高，R1 推理强 |
| **智谱 GLM** | glm-4-plus / glm-4-flash | `https://open.bigmodel.cn/api/paas/v4` | 调用方式略有不同 |
| **阿里 Qwen** | qwen-max / qwen-plus / qwen-turbo | `https://dashscope.aliyuncs.com/compatible-mode/v1` | 兼容 OpenAI |
| **阶跃星辰 StepFun** | step-2-16k / step-1-flash | `https://api.stepfun.com/v1` | 全兼容 OpenAI |
| **百度 ERNIE** | ernie-4.0 / ernie-3.5 | `https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions` | 特殊 endpoint |
| **讯飞星火** | spark-4.0 / spark-3.5 | `https://spark-api-open.xf-yun.com/v1` | 兼容 OpenAI |
| **MiniMax** | abab-6.5 / abab-5.5 | `https://api.minimax.chat/v1` | 全兼容 |

## 2. 统一调用示例

由于大多兼容 OpenAI SDK，代码高度一致：

```python
from openai import OpenAI

# === DeepSeek ===
client = OpenAI(api_key="sk-deepseek-xxx", base_url="https://api.deepseek.com")

# === Qwen ===
# client = OpenAI(api_key="sk-qwen-xxx", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

# === StepFun ===
# client = OpenAI(api_key="sk-step-xxx", base_url="https://api.stepfun.com/v1")

# === MiniMax ===
# client = OpenAI(api_key="sk-minimax-xxx", base_url="https://api.minimax.chat/v1")

resp = client.chat.completions.create(
    model="指定模型名",
    messages=[{"role": "user", "content": "你好"}],
    stream=False,
)
print(resp.choices[0].message.content)
```

## 3. 各厂商的注意事项

### 3.1 DeepSeek

- `deepseek-chat` = V3 聊天模型；`deepseek-reasoner` = R1 推理模型。
- R1 模型的 `content` 会返回推理过程（reasoning_content），注意解析：
  ```python
  resp = client.chat.completions.create(model="deepseek-reasoner", ...)
  print(resp.choices[0].message.reasoning_content)  # 推理链
  print(resp.choices[0].message.content)             # 最终回答
  ```
- DeepSeek 的 tool use / function calling 与 OpenAI 完全兼容。
- 价格约为 GPT-4o 的 1/20 - 1/10，对 token 敏感场景非常友好。
- FIM 补全：`https://api.deepseek.com/beta/completions`（用于 Code Infill）。

### 3.2 阿里 Qwen（DashScope）

- 推荐使用 `compatible-mode` endpoint，完全兼容 OpenAI SDK。
- 旧版 DashScope SDK 使用 `dashscope` 包，不建议新项目使用。
- Tool use / streaming / FIM 均支持。
- 提供 **VL（视觉）模型** `qwen-vl-max`，调用方式一样，message 里加 `image_url`。
- 参考文档：<https://help.aliyun.com/zh/model-studio/developer-reference/use-qwen-by-openai-compatible-api>

### 3.3 智谱 GLM

- OpenAI 兼容 endpoint：需要查最新文档确认。早期使用 `zhipuai` 包，新版已逐步兼容。
- 在 agent / tool use 场景下，注意 GLM 的 function calling 实现在某些边缘情况可能不如 DeepSeek/Qwen 稳定。
- 智谱的 GLM-4-Flash 有相当大的免费额度，适合做 eval / 批量打分。

### 3.4 阶跃星辰 StepFun

- 完全兼容 OpenAI SDK，切换成本极低。
- step-2-16k 是高端模型；step-1-flash 适合快速打样。
- 与 utils/llm_client.py 配合：`LLMClient(provider="stepfun")` 只需在 client 里加一个 `provider` 分支。

### 3.5 百度 ERNIE

- API 结构相对特殊，建议用百度官方的 `qianfan` SDK 或请求转换代理。
- 在 agent 代码中需要单独写一个 adapter。

## 4. 在 agent 代码中统一管理

本仓库已有 `utils/llm_client.py`，可以直接扩展支持国内厂商：

```python
class LLMClient:
    PROVIDERS = {
        "openai": {"base_url": None},                                    # 默认
        "deepseek": {"base_url": "https://api.deepseek.com"},
        "qwen": {"base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1"},
        "stepfun": {"base_url": "https://api.stepfun.com/v1"},
        "minimax": {"base_url": "https://api.minimax.chat/v1"},
    }

    def __init__(self, provider="openai", model=None, api_key=None, **kwargs):
        self.provider = provider
        config = self.PROVIDERS.get(provider, {})
        client_kwargs = {"api_key": api_key or os.getenv(f"{provider.upper()}_API_KEY")}
        if config.get("base_url"):
            client_kwargs["base_url"] = config["base_url"]
        self.client = OpenAI(**client_kwargs)
        ...
```

对应的 `.env` 配置：

```bash
# 国产模型 API Key（任选其一）
DEEPSEEK_API_KEY=sk-deepseek-xxxxxxxxx
QWEN_API_KEY=sk-qwen-xxxxxxxxx
STEPFUN_API_KEY=sk-step-xxxxxxxxx
```

## 5. 在国内使用 agent 的注意事项

| 问题 | 说明 | 对策 |
|------|------|------|
| **网络访问第三方 LLM** | 海外模型（Anthropic / OpenAI）在国内直连可能不稳定 | 使用国内中转代理或模型厂商的内地节点 |
| **Tool use 一致性** | 不同厂商的 function calling 实现细节有别 | 选 DeepSeek / Qwen，它们是兼容性最好的两家 |
| **Streaming 时延** | 国产模型的首 token 时延普遍低于海外（内地网络优势） | 对实时交互场景是利好 |
| **MCP 支持** | 国产模型对 MCP 没有原生支持 | 客户端侧实现 tool use 解析逻辑即可（见第 03 章） |
| **并发与限流** | 国产厂商的免费/低价套餐往往有较低 QPS 限制 | 检查套餐文档，必要时加排队/退避 |

## 6. 推荐组合方案

| 场景 | 推荐 |
|------|------|
| 日常开发 / 写代码 | DeepSeek (V3) — 性价比极高 |
| 复杂推理 / 数学 | DeepSeek (R1) — 推理链可解释 |
| 大规模 batch eval | Qwen-Plus 或 GLM-4-Flash — 稳定、有免费额度 |
| 国内部署的 agent 服务 | Qwen-Max 或 DeepSeek — 网络最低延迟 |
| 多模态（图片理解） | Qwen-VL-Max — 兼容 OpenAI SDK，切换成本低 |

## 7. 参考文档

- DeepSeek API docs：<https://platform.deepseek.com/api-docs>
- 阿里 DashScope 文档：<https://help.aliyun.com/zh/model-studio/>
- 智谱开放平台：<https://open.bigmodel.cn/>
- 阶跃星辰 StepFun 文档：<https://platform.stepfun.com/>
- 百度千帆：<https://cloud.baidu.com/product/wenxinworkshop>
- 讯飞星火：<https://www.xfyun.cn/doc/spark/HTTP%E8%B0%83%E7%94%A8%E6%96%87%E6%A1%A3.html>
- MiniMax 开放平台：<https://platform.minimax.chat/>
