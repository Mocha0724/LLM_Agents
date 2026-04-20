"""TRL GRPO 最小训练脚本。

用法：
    python data/gen_arith.py
    python train/grpo_train.py
"""
from __future__ import annotations

import json
from pathlib import Path

from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import GRPOConfig, GRPOTrainer

from .rewards import reward_correct, reward_format

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
DATA_PATH = "data/arith_1k.jsonl"


def load_dataset(path: str) -> Dataset:
    rows = [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines()]
    return Dataset.from_list(rows)


def main() -> None:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype="auto")
    ds = load_dataset(DATA_PATH)

    cfg = GRPOConfig(
        output_dir="runs/grpo_arith",
        learning_rate=2e-6,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        num_generations=8,
        max_prompt_length=128,
        max_completion_length=128,
        beta=0.01,
        num_train_epochs=1,
        logging_steps=10,
        save_strategy="epoch",
        report_to=[],
    )

    trainer = GRPOTrainer(
        model=model,
        processing_class=tokenizer,
        reward_funcs=[reward_correct, reward_format],
        args=cfg,
        train_dataset=ds,
    )
    trainer.train()
    trainer.save_model("runs/grpo_arith/final")


if __name__ == "__main__":
    main()
