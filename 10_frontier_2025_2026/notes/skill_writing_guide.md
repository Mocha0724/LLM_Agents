# 笔记 · Skill 编写实战指南

> 承接 `skill_mechanism.md` 的原理介绍，本篇聚焦 **怎么写好一个 SKILL.md**，覆盖编码、学术、办公等常见场景的完整 skill 示例。
>
> 适用平台：Cursor Skills / Claude Code Hooks / 其它支持技能注入的 coding agent。

## 1. 编写 Skill 的核心原则

### 1.1 四条黄金法则

1. **精准触发**：`description` 决定 skill 是否被调用，要同时写清楚「干什么」和「什么时候用」。
2. **只加领域知识**：agent 已经知道通用编程，skill 只需覆盖它不知道的（团队约定、私有 API、工具链用法）。
3. **渐进披露**：SKILL.md 放核心流程，详细参考放 `reference.md`，agent 按需读取。
4. **可验证**：skill 里若有指令、模板、命令，走一遍确认无误再提交。

### 1.2 description 怎么写

```markdown
---
name: code-review-python
description: >-
  Review Python code following team's style guide (PEP 8 + internal conventions).
  Use when requested to review Python PRs or code changes.
---
```

拆解：
- **WHAT**：`Review Python code following team's style guide`
- **WHEN**：`Use when requested to review Python PRs or code changes`
- **触发词**：`Python`, `PR`, `code review`, `style guide`
- **第三人称**：不要写 "I can help you"，也不要写 "You can use this"

### 1.3 结构模板（通用）

```markdown
---
name: skill-name
description: 一句话描述
---

# Skill 标题

## 快速开始
[2-3 步说明]

## 核心指令 / 检查清单
[按步骤或 checklist 组织]

## 参考
- [reference.md](reference.md) 详细规范
- [examples.md](examples.md) 示例
```

---

## 2. Coding 场景 Skill

### 2.1 代码风格检查

**适用场景**：团队有自定义风格规范，或要统一 commit 前自动检查。

```markdown
---
name: python-style
description: >-
  Format and check Python code following the team's style rules.
  Use when writing or reviewing Python code, or when asked to check code style.
---

# Python 代码风格

## 格式工具
- 格式化：`ruff format .`
- Lint 检查：`ruff check .`
- 类型检查：`mypy src/ --strict`

## 命名规范
| 类别 | 规则 | 示例 |
|------|------|------|
| 函数/变量 | snake_case | `get_user_by_id` |
| 类名 | PascalCase | `UserService` |
| 私有方法 | _ 前缀 | `_validate_input` |
| 常量 | UPPER_SNAKE | `MAX_RETRY_COUNT` |

## Import 顺序
1. 标准库（os, sys, re）
2. 第三方（torch, numpy, anthropic）
3. 本地模块（from utils import ...）

每组之间空一行，组内按字母序。

## Docstring 格式
Google style + 类型注解：

```python
def fetch_user(user_id: int) -> dict:
    """根据 ID 获取用户信息。

    Args:
        user_id: 用户 ID。

    Returns:
        包含用户信息的 dict。

    Raises:
        ValueError: 用户不存在。
    """
```

## 不允许的模式
- 不写 `except: pass`，要指定异常类型或至少 log
- 不写 `from module import *`
- 不在函数体内修改全局变量
```

### 2.2 Code Review

```markdown
---
name: code-review-general
description: >-
  Review code changes for correctness, security, and maintainability.
  Use when reviewing PRs, examining code changes, or asked for a code review.
---

# Code Review

## 双向检视

```
review_mode: "read"    # 只看代码，不做修改
review_level: "standard"  # standard / deep
```

## 检查清单

### 正确性
- [ ] 逻辑正确，边界情况（空值、临界值、并发）有处理
- [ ] 错误路径有处理而非静默忽略
- [ ] 资源（文件句柄、网络连接、GPU 内存）正确释放

### 安全
- [ ] 无注入风险（SQL / shell / prompt injection）
- [ ] 敏感信息不硬编码
- [ ] 输入校验

### 可维护性
- [ ] 函数职责单一
- [ ] 命名表意
- [ ] 复杂度能理解（圈复杂度 < 10）

### 测试
- [ ] 有测试覆盖新逻辑
- [ ] 测试不是「快乐路径」独占

## 反馈格式
- **Critical** 🔴：必须修再合并。通常是正确性/安全问题。
- **Suggestion** 🟡：建议改进。可这次不做但值得讨论。
- **Nit** 🟢：小问题。纯风格偏好。

## 参考
详细标准见 [reference.md](reference.md)
```

### 2.3 重构 / 迁移

```markdown
---
name: code-refactor
description: >-
  Refactor or migrate code with safety guarantees.
  Use when asked to refactor, rename, restructure, or migrate code.
---

# 代码重构

## 安全步骤
1. **确认范围**：分析哪些文件和符号受影响
2. **创建分支**：`git checkout -b refactor/xxx`
3. **做改动**
4. **跑测试**：确保零失败
5. **清理**：删除废弃代码、更新 import 和引用
6. **commit**

## 重构模式

### 重命名符号
跨文件全局搜索替换，然后：
```bash
git grep "old_name"  # 确认所有引用都被覆盖
```

### 提取函数
1. 选一段独立逻辑
2. 提取为新函数，加 docstring
3. 原位置替换为调用
4. 确认参数传递正确

### 迁移接口
- 保留旧接口 + deprecation warning → 迁移调用方 → 删除旧接口
- 不做一次性断崖式迁移

## 不做的事
- 不在重构中混入功能改动
- 不修改已稳定的公共 API 签名（渐进式）
```

---

## 3. 学术代码场景 Skill

### 3.1 实验管理

```markdown
---
name: experiment-runner
description: >-
  Set up and run machine learning experiments with structured logging.
  Use when asked to write training scripts, config files, or experiment pipelines.
---

# 实验管理

## 项目结构
```
project/
├── configs/          # YAML 配置文件
│   ├── base.yaml
│   └── exp001.yaml
├── data/             # 数据（gitignore）
├── scripts/          # 训练脚本
│   ├── train.py
│   └── eval.py
├── runs/             # 实验结果（gitignore）
├── src/              # 核心代码
└── requirements.txt
```

## 训练脚本模板

```python
import argparse, yaml, random, numpy as np, torch

def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    set_seed(args.seed)
    with open(args.config) as f:
        config = yaml.safe_load(f)

    from src.model import build_model
    from src.trainer import Trainer
    model = build_model(config["model"])
    trainer = Trainer(model, config["training"])
    metrics = trainer.train()

    print(f"Done: {metrics}")

if __name__ == "__main__":
    main()
```

## 关键规范
- 固定随机种子：每个实验记录 seed
- 配置与代码分离：不改代码只改 yaml 即可跑新实验
- 自动记录：使用 wandb / tensorboard / mlflow 记录 metrics
```

### 3.2 可视化

```markdown
---
name: academic-plot
description: >-
  Create publication-quality figures using matplotlib/seaborn.
  Use when asked to generate plots, charts, or visualizations for papers.
---

# 学术论文配图

## 全局设置

```python
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams.update({
    "figure.dpi": 300,
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "legend.fontsize": 9,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "font.family": "serif",       # 论文通常用 serif
    "figure.figsize": (5, 3.5),   # 单栏
    # "figure.figsize": (7, 4),   # 双栏
})
```

## 常用图类型

### 对比柱状图（Ablation / Baseline 对比）

```python
fig, ax = plt.subplots()
bars = ax.bar(x_labels, values, color=["#4C72B0", "#DD8452", "#55A868"])
ax.set_ylabel("Accuracy (%)")
# 在柱顶标注数值
for bar, v in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f"{v:.1f}", ha="center", va="bottom", fontsize=8)
```

### 折线图（收敛曲线）

```python
fig, ax = plt.subplots()
ax.plot(steps, loss, label="Train", linewidth=1.5)
ax.plot(steps, val_loss, label="Val", linewidth=1.5, linestyle="--")
ax.set_xlabel("Step")
ax.set_ylabel("Loss")
ax.legend()
ax.grid(True, alpha=0.3)
```

### heatmap（混淆矩阵 / 注意力）

```python
sns.heatmap(matrix, annot=True, fmt=".2f", cmap="Blues",
            xticklabels=classes, yticklabels=classes)
```

## 输出格式
- 论文：保存为 PDF（`plt.savefig("fig.pdf", bbox_inches="tight")`）
- PPT 报告：保存为 PNG 300dpi
```

### 3.3 结果分析

```markdown
---
name: result-analysis
description: >-
  Analyze experiment results: compare runs, statistical tests, aggregation.
  Use when given CSV/JSONL results files from experiments.
---

# 实验结果分析

## 读取与聚合
```python
import pandas as pd
import numpy as np
df = pd.read_json("results.jsonl", lines=True)
summary = df.groupby("method").agg({
    "accuracy": ["mean", "std", "count"],
    "latency_ms": ["mean", "std"],
}).round(3)
print(summary)
```

## 统计检验
```python
from scipy import stats
# 两组独立样本，检验差异显著性
t_stat, p_val = stats.ttest_ind(
    df[df["method"] == "ours"]["accuracy"],
    df[df["method"] == "baseline"]["accuracy"],
)
print(f"t = {t_stat:.3f}, p = {p_val:.4f}")
```

## 报告模板
```
| Method | Accuracy | Δ  | p-value |
|--------|----------|----|---------|
| Baseline | {mean:.1f}±{std:.1f} | — | — |
| Ours     | {mean:.1f}±{std:.1f} | +{delta:.1f} | {p:.4f} |
```

## 可视化
详见 academic-plot skill。
```

---

## 4. 学术讨论 & 论文修改 Skill

### 4.1 论文审稿 / 结构审查

```markdown
---
name: paper-review
description: >-
  Review academic papers for structure, clarity, and argument flow.
  Use when asked to review a paper draft or provide structural feedback.
---

# 论文审稿

## 整体结构

### 检查清单
- [ ] 摘要：背景 → 问题 → 方法 → 结果 → 结论，控制 200 词内
- [ ] Intro：从大到小（领域 → 问题 → 缺口 → 贡献）
- [ ] Related Work：按主题分类，不逐篇罗列
- [ ] Method：可复现，公式/算法/架构图完整
- [ ] Experiments：消融、与 SOTA 对比、定量 + 定性
- [ ] Conclusion：只总结 + 未来工作，不引入新东西

### 常见问题
1. **缺少与最相关工作的量化对比**（审稿人最常点名）
2. **实验设置不清晰**（数据集划分、超参数、随机种子）
3. **贡献拆分太大**：一篇论文 2-3 个贡献点足够
4. **Related Work 写成流水账**：要按「不同思路」归类，不按时间线

## 语言风格
- 被动语态为主 (`is proposed`, `are evaluated`)
- 少用 `very`, `extremely`, `novel` 等空洞修饰
- 每段一句核心论点，其余是支撑

## 回复审稿人模板
1. 感谢审稿人
2. 复述问题：`We thank the reviewer for this comment. Regarding [问题]...`
3. 正面回答 + 改动：`We have [做了什么改动], as shown in [位置].`
4. 必要时引实验/文献支撑
```

### 4.2 论文润色

```markdown
---
name: paper-polish
description: >-
  Polish academic writing: grammar, clarity, and flow.
  Use when asked to proofread or improve a paper draft.
---

# 论文润色

## 操作步骤
1. **通读全文**，记录整体问题（结构、逻辑跳跃）
2. **逐段润色**：每段只保留一个核心论点
3. **逐句精简**：删冗余（`it is worth noting that` → 直接说）
4. **统一术语**：全文同一概念只用同一词

## 高频替换

| 原文（啰嗦） | 改为（简洁） |
|------|------|
| It is well known that X | X is |
| A large number of | Many |
| In order to | To |
| Due to the fact that | Because |
| We carried out experiments | We evaluate |
| It can be observed that | X shows |

## 格式检查
- [ ] 缩写首次出现标全称
- [ ] 引用格式统一
- [ ] 图和表的 caption 完整
- [ ] 公式编号正确
- [ ] 参考文献字段完整

## 不做的事
- 不改公式 / 数据的正确性（只问不修）
- 不改作者的技术判断
```

### 4.3 学术讨论 / 头脑风暴

```markdown
---
name: academic-brainstorm
description: >-
  Structure academic discussions, idea exploration, and literature gap analysis.
  Use when asked to brainstorm research ideas or explore connections.
---

# 学术头脑风暴

## 四步框架
1. **问题定义**：把模糊的想法压缩成一句具体问题
2. **现状分析**：已有工作怎么做的？有哪些共识和缺口？
3. **思路发散**：列出 3-5 个可能的切入方向，不限制
4. **收敛选择**：按「新颖度 × 可行度 × 价值度」打分筛选

## 思路启发模板

| 策略 | 举例 |
|------|------|
| 跨领域迁移 | 把 A 领域的方法迁移到 B 领域 |
| 互补整合 | 结合方法 X 的泛化性和方法 Y 的精度 |
| 问题重定义 | 换个角度定义原问题 |
| 弱监督化 | 能否去掉对 label 的依赖？ |
| 工具化 | 方法本身的瓶颈能否被最新工具突破？ |

## 输出格式
对每个潜在方向，输出：
```
## 方向：...
### 核心想法（2-3 句）
### 与已有工作的区别（1 句）
### 最大的风险 / 瓶颈（1 句）
### 最小验证实验（1 句）
```
```

---

## 5. 办公软件场景 Skill

### 5.1 Word / 文档排版

```markdown
---
name: word-doc
description: >-
  Create and format Word documents with proper structure.
  Use when asked to create .docx files, reports, or formatted documents.
---

# Word 文档操作

## 环境
```bash
pip install python-docx
```

## 常用操作

### 创建文档
```python
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# 标题
doc.add_heading("一级标题", level=1)
doc.add_heading("二级标题", level=2)

# 正文
p = doc.add_paragraph("这是一段正文。")
p.style.font.size = Pt(12)
p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

# 表格
table = doc.add_table(rows=3, cols=2, style="Light Grid Accent 1")
table.cell(0, 0).text = "header1"
```

### 模板套用
- 已有 .docx 模板 → 修改特定段落/表格 → 另存
- 用占位符 `{{name}}` 做 mail merge

## 规范
- 正文字体 12pt，行距 1.5 倍
- 标题用多级列表（非手动编号）
- 页边距：上下 2.54cm，左右 3.17cm
```

### 5.2 Excel / 数据分析

```markdown
---
name: spreadsheet-work
description: >-
  Work with Excel spreadsheets: read, analyze, chart, format.
  Use when given .xlsx, .csv files, or asked to create spreadsheets.
---

# Excel / 电子表格操作

## 环境
```bash
pip install openpyxl pandas
```

## 常用操作

### 读取与清洗
```python
import pandas as pd
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")
df = df.dropna(subset=["关键列"])
```

### 写入带格式
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border

wb = Workbook()
ws = wb.active
ws.title = "Summary"

# 标题行
header_font = Font(bold=True, color="FFFFFF")
header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
for col, name in enumerate(["Method", "Accuracy", "F1"], 1):
    cell = ws.cell(row=1, column=col, value=name)
    cell.font = header_font
    cell.fill = header_fill
```

### 公式
```python
ws["D2"] = "=B2-C2"  # 差值
ws["E2"] = "=RANK(B2,$B$2:$B$10,0)"  # 排名
```

### 图表（内置 Excel chart）
```python
from openpyxl.chart import BarChart, Reference
chart = BarChart()
data = Reference(ws, min_col=2, min_row=1, max_row=10)
cats = Reference(ws, min_col=1, min_row=2, max_row=10)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)
ws.add_chart(chart, "F1")
```

## 规范
- 第一行是 header，加粗 + 底色
- 数值保留 2-4 位小数
- 关键公式写在第一行，下拉填充
```

### 5.3 PPT / 演示文档

```markdown
---
name: ppt-deck
description: >-
  Create and format PowerPoint presentations.
  Use when asked to create slides, decks, or presentations.
---

# PPT 演示文档

## 环境
```bash
pip install python-pptx
```

## 常用操作

### 创建slides
```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# 标题 slides
slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
title = slide.shapes.title
# ... 加标题和正文
```

### 内容排版建议
| slide 类型 | 内容 |
|-----------|------|
| Title | 标题 + 作者 + 单位 |
| Outline | 1-2-3 结构 |
| Method | 架构图（左）+ 文字说明（右）|
| Result | 表格 / 柱状图 + 关键结论 |
| Summary | 3 个 bullet points |

## 规范
- 学术汇报：每页 1 个核心信息，不要堆文字
- 配色：不要超过 3 种主色
- 字体：标题 28-32pt，正文 18-24pt
- 图片：统一风格（所有 bar 图同配色）
```

### 5.4 PDF 操作

```markdown
---
name: pdf-tools
description: >-
  Manipulate PDF files: extract text, merge, split, watermark.
  Use when working with PDF files or when asked to process PDFs.
---

# PDF 操作

## 环境
```bash
pip install pypdf pdfplumber pdf2image
```

## 常用操作

### 提取文字
```python
import pdfplumber
with pdfplumber.open("paper.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        # 也可以提取表格: page.extract_tables()
```

### 提取表格
```python
with pdfplumber.open("results.pdf") as pdf:
    table = pdf.pages[0].extract_table()
    for row in table:
        print(row)
```

### 合并 PDF
```python
from pypdf import PdfWriter, PdfReader
writer = PdfWriter()
for f in ["ch1.pdf", "ch2.pdf"]:
    for page in PdfReader(f).pages:
        writer.add_page(page)
writer.write("combined.pdf")
```

### 拆分 PDF
```python
reader = PdfReader("big.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    writer.write(f"page_{i+1}.pdf")
```

## 规范
- 文本优先用 pdfplumber（比 PyPDF2 准确）
- OCR：扫描 PDF 用 `pdf2image` + `pytesseract`
- 输出路径不要覆盖源文件
```

---

## 6. 其他场景 Skill

### 6.1 Git 操作

```markdown
---
name: git-workflow
description: >-
  Automate common Git workflows: branching, commit conventions, rebase, PR.
  Use when asked about Git operations, commit messages, or repository management.
---

# Git Workflow

## Commit 规范
```
<type>(<scope>): <description>

[optional body]
```

| type | 用途 |
|------|------|
| feat | 新功能 |
| fix | 修 bug |
| docs | 文档 |
| style | 格式（空格、缩进） |
| refactor | 重构 |
| test | 测试 |
| chore | 构建、CI |

示例：`feat(trainer): add gradient accumulation support`

## 分支策略
```
main        ← 发布
  ├── dev   ← 开发
  ├── feat/xxx
  ├── fix/xxx
  └── refactor/xxx
```

## 常用自动化

### 交互式 rebase 合并
```bash
git log --oneline origin/main..HEAD
git rebase -i origin/main
```

### 自动生成 PR 描述
```bash
git log origin/main..HEAD --oneline --no-merges
```

## 规范
- feat/fix 分支从 dev checkout，PR 合入 dev
- dev 定期 rebase 到 main 保持同步
- 不直接 push main
```

### 6.2 每日日志 / 周报

```markdown
---
name: daily-log
description: >-
  Generate structured daily logs, weekly reports, and progress summaries.
  Use when asked to write daily standup, weekly report, or meeting notes.
---

# 每日日志 / 周报

## 日报模板
```markdown
## 日期：YYYY-MM-DD

### 今日完成
- [x] 任务 1：简短描述
- [x] 任务 2：简短描述

### 遇到的问题
- 问题 1 | 状态：[已解决/跟进中] | 方案/备注

### 明日计划
- [ ] 计划 1
- [ ] 计划 2
```

## 周报模板
```markdown
## 本周汇总（YYYY-MM-DD ~ YYYY-MM-DD）

### 关键进展
1. 进展 1 — 具体指标/交付物
2. 进展 2

### 问题 & 风险
| 问题 | 影响 | 缓解措施 |
|------|------|---------|
| ... | ... | ... |

### 下周计划
- [ ] 计划 1
- [ ] 计划 2
```

## 原则
- 日报：只记录「有价值」的事，不凑字数
- 周报：突出量化产出，弱化过程描述
- 写作风格：客观陈述，不写「花了很多时间」
```

### 6.3 DevOps / 部署

```markdown
---
name: devops-deploy
description: >-
  Write Dockerfiles, CI configs, and deployment scripts.
  Use when asked about containerization, CI/CD, or deployment.
---

# DevOps / 部署

## Docker

### 多阶段构建
```dockerfile
# Build stage
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY src/ .
CMD ["python", "main.py"]
```

### docker-compose 多服务
```yaml
version: '3.8'
services:
  api:
    build: .
    ports: ["8000:8000"]
    env_file: .env
  redis:
    image: redis:7-alpine
```

## CI 配置（GitHub Actions）

```yaml
name: CI
on: push
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r requirements.txt
      - run: pytest tests/
```

## 最佳实践
- 不用 root 跑应用（Dockerfile 里 `USER appuser`）
- 敏感信息用环境变量 / secrets，不写进镜像
- 健康检查：`HEALTHCHECK CMD curl -f http://localhost:8000/health`
```

### 6.4 API 文档 / README 写作

```markdown
---
name: api-docs
description: >-
  Write clear API documentation and project README files.
  Use when asked to document an API, write README, or generate docstrings.
---

# API 文档 / README

## README 结构
```markdown
# 项目名

> 一句话说明项目做什么。

## 快速开始
```bash
pip install -r requirements.txt
python main.py
```

## 使用示例
[最小可运行代码片段]

## API 文档
[接口签名 + 参数说明 + 示例]

## 项目结构
[目录树]
```

## API 文档规范

### Endpoint 模板
```
### POST /v1/predict

**描述**：...
**请求体**：
```json
{"input": "..."}
```
**响应**：
```json
{"output": "...", "latency_ms": 123}
```
**错误码**：
| code | 说明 |
|------|------|
| 400 | 参数错误 |
| 500 | 服务内部错误 |
```

## 原则
- 文档先写给「第一次使用的人」看
- 代码示例可复制即用（不要省略 import）
- 参数表说明类型、默认值、可选/必填
```
