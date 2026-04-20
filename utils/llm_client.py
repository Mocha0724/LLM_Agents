"""统一的 LLM 客户端封装。

设计目标：
- 让所有章节的 notebook 用同一行 `from utils.llm_client import chat` 即可工作。
- 默认走 Anthropic（Claude），找不到 key 时自动 fallback 到 OpenAI。
- 内置重试与简单的 token 计费日志，方便后续 09/12 章引用。
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Iterable

from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0

    @property
    def total(self) -> int:
        return self.input_tokens + self.output_tokens


@dataclass
class LLMClient:
    """轻量统一封装：Anthropic 优先，OpenAI fallback。"""

    provider: str = "auto"  # "auto" | "anthropic" | "openai"
    model: str | None = None
    temperature: float = 0.0
    max_tokens: int = 1024
    usage: Usage = field(default_factory=Usage)

    def __post_init__(self) -> None:
        if self.provider == "auto":
            if os.getenv("ANTHROPIC_API_KEY"):
                self.provider = "anthropic"
            elif os.getenv("OPENAI_API_KEY"):
                self.provider = "openai"
            else:
                raise RuntimeError(
                    "未检测到 ANTHROPIC_API_KEY 或 OPENAI_API_KEY，请配置 .env"
                )

        if self.model is None:
            self.model = (
                "claude-sonnet-4-5" if self.provider == "anthropic" else "gpt-4o-mini"
            )

        if self.provider == "anthropic":
            from anthropic import Anthropic

            self._client: Any = Anthropic()
        else:
            from openai import OpenAI

            self._client = OpenAI()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        system: str | None = None,
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """统一接口：返回 ``{"text": str, "raw": <provider response>}``。

        - ``messages`` 形如 ``[{"role": "user", "content": "hi"}, ...]``。
        - ``tools`` 为可选 tool schema。具体格式按 provider 原生约定。
        """
        if self.provider == "anthropic":
            req: dict[str, Any] = dict(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=messages,
                **kwargs,
            )
            if system:
                req["system"] = system
            if tools:
                req["tools"] = tools
            resp = self._client.messages.create(**req)
            self.usage.input_tokens += resp.usage.input_tokens
            self.usage.output_tokens += resp.usage.output_tokens
            text = "".join(
                block.text for block in resp.content if getattr(block, "type", None) == "text"
            )
            return {"text": text, "raw": resp}

        # openai
        msgs = list(messages)
        if system:
            msgs = [{"role": "system", "content": system}, *msgs]
        req = dict(
            model=self.model,
            messages=msgs,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            **kwargs,
        )
        if tools:
            req["tools"] = tools
        resp = self._client.chat.completions.create(**req)
        if resp.usage is not None:
            self.usage.input_tokens += resp.usage.prompt_tokens
            self.usage.output_tokens += resp.usage.completion_tokens
        text = resp.choices[0].message.content or ""
        return {"text": text, "raw": resp}


_default: LLMClient | None = None


def chat(
    user: str,
    *,
    system: str | None = None,
    history: Iterable[dict[str, Any]] | None = None,
    **kwargs: Any,
) -> str:
    """便捷函数：单轮/带历史聊天，直接返回文本。"""
    global _default
    if _default is None:
        _default = LLMClient()
    messages: list[dict[str, Any]] = list(history or [])
    messages.append({"role": "user", "content": user})
    return _default.chat(messages, system=system, **kwargs)["text"]
