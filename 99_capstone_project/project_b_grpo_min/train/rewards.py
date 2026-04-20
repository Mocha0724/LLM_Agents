"""GRPO reward 函数。

设计要点（见第 09 章）：
- reward_correct: 答案数值匹配 → 1.0；可解析但错 → 0.2；无法解析 → 0.0。
- reward_format: 输出含 <think>...</think><answer>...</answer> → 0.1。
- 最终 reward 是各项加和（GRPO 内部按 group 标准化）。
"""
from __future__ import annotations

import re

ANS_RE = re.compile(r"<answer>\s*(-?\d+(?:\.\d+)?)\s*</answer>")
FORMAT_RE = re.compile(r"<think>.*?</think>\s*<answer>.*?</answer>", re.S)


def reward_correct(completions, gold, **_):
    rewards = []
    for comp, g in zip(completions, gold):
        m = ANS_RE.search(comp)
        if not m:
            rewards.append(0.0)
        elif m.group(1).strip() == str(g).strip():
            rewards.append(1.0)
        else:
            rewards.append(0.2)
    return rewards


def reward_format(completions, **_):
    return [0.1 if FORMAT_RE.search(c) else 0.0 for c in completions]
