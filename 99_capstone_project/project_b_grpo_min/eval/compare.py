"""训练前/后对比：随机采 50 题，分别用 base 模型和 finetuned 模型生成，
计算 (格式合规率, 答案准确率, 平均长度) 三项指标。
"""
from __future__ import annotations

import json
import random
from pathlib import Path

from transformers import AutoModelForCausalLM, AutoTokenizer

from train.rewards import ANS_RE, FORMAT_RE

BASE = "Qwen/Qwen2.5-0.5B-Instruct"
FT = "runs/grpo_arith/final"
DATA = "data/arith_1k.jsonl"
N = 50


def gen(model_id: str, prompts: list[str]) -> list[str]:
    tok = AutoTokenizer.from_pretrained(model_id)
    mdl = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype="auto")
    outs = []
    for p in prompts:
        msg = tok.apply_chat_template(
            [{"role": "user", "content": p}],
            tokenize=False, add_generation_prompt=True,
        )
        ids = tok(msg, return_tensors="pt").to(mdl.device)
        gen_ids = mdl.generate(**ids, max_new_tokens=128, do_sample=False)
        outs.append(tok.decode(gen_ids[0][ids.input_ids.shape[1]:], skip_special_tokens=True))
    return outs


def metrics(outs: list[str], gold: list[str]) -> dict:
    fmt = sum(bool(FORMAT_RE.search(o)) for o in outs) / len(outs)
    correct = 0
    for o, g in zip(outs, gold):
        m = ANS_RE.search(o)
        if m and m.group(1).strip() == g.strip():
            correct += 1
    return {
        "format_rate": round(fmt, 3),
        "accuracy": round(correct / len(outs), 3),
        "avg_len": round(sum(len(o) for o in outs) / len(outs), 1),
    }


def main() -> None:
    rows = [json.loads(l) for l in Path(DATA).read_text(encoding="utf-8").splitlines()]
    random.Random(0).shuffle(rows)
    sample = rows[:N]
    prompts = [r["prompt"] for r in sample]
    gold = [r["gold"] for r in sample]

    print("[base]")
    print(metrics(gen(BASE, prompts), gold))
    if Path(FT).exists():
        print("[finetuned]")
        print(metrics(gen(FT, prompts), gold))
    else:
        print(f"finetuned model not found at {FT}; run grpo_train.py first")


if __name__ == "__main__":
    main()
