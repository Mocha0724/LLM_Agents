# 笔记 · LLM+P: Empowering LLMs with Optimal Planning Proficiency（Liu et al., 2023）

- arXiv: 2304.11477
- 一句话精华：LLM 不擅长 *最优*规划，但可以把自然语言转成 PDDL，让经典 planner 算最优解，再翻回自然语言。

## 流程

```mermaid
flowchart LR
    NL[自然语言任务] --> LLM1[LLM: 翻译成 PDDL]
    LLM1 --> PDDL[PDDL Domain + Problem]
    PDDL --> Planner["经典 planner (Fast Downward)"]
    Planner --> Plan[最优 plan]
    Plan --> LLM2[LLM: 翻译回自然语言]
    LLM2 --> User
```

## 关键洞察

- LLM 擅长 *形式转换*（NL ↔ formal），不擅长 *组合搜索* 与 *最优性保证*。
- 经典 planner（Fast Downward, OPTIC, ENHSP）几十年的算法积累不应被忽视。
- *神经符号结合*：LLM 当前端编译器，符号求解器当后端引擎。

## 实验

- 在 BlocksWorld 等经典 benchmark 上，LLM+P 几乎 100% 最优；纯 LLM 经常给出非法或次优 plan。
- 但要求 LLM 能写出正确 PDDL，对 prompt + few-shot 例子很敏感。

## 局限

- PDDL 域必须预定义。
- 现实任务很难形式化；用于「打开文件、打开浏览器」类 agent 任务困难。
- 适合：物流、调度、机器人任务规划。

## 我的批注

- 把 LLM 看成「自然语言到形式语言的编译器」是一个被 *持续低估* 的视角；很多场景比让 LLM 直接「思考」更可靠。
- 业务联想：地图导航本身就是一类形式化规划，*把用户口语 query 转成路径搜索约束* 是 LLM+P 思路的天然落地。
