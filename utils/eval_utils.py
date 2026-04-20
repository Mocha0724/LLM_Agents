"""共享的评测/比对小工具。"""

from __future__ import annotations

import re
from dataclasses import dataclass


def normalize_answer(text: str) -> str:
    """GSM8K 等数值题答案归一化。"""
    text = text.strip().lower()
    text = text.replace(",", "")
    m = re.findall(r"-?\d+(?:\.\d+)?", text)
    return m[-1] if m else text


@dataclass
class RunResult:
    name: str
    correct: int
    total: int
    tokens_in: int = 0
    tokens_out: int = 0

    @property
    def acc(self) -> float:
        return self.correct / self.total if self.total else 0.0

    def __str__(self) -> str:
        return (
            f"[{self.name}] acc={self.acc:.2%} "
            f"({self.correct}/{self.total})  tok_in={self.tokens_in} tok_out={self.tokens_out}"
        )


def compare_runs(*runs: RunResult) -> str:
    header = f"{'Run':<25}{'Acc':>10}{'TokIn':>10}{'TokOut':>10}"
    lines = [header, "-" * len(header)]
    for r in runs:
        lines.append(f"{r.name:<25}{r.acc:>10.2%}{r.tokens_in:>10}{r.tokens_out:>10}")
    return "\n".join(lines)
