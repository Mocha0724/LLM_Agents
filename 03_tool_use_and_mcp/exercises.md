# 第 03 章 · 思考题

## 思考题

1. JSON Function Calling 与 CodeAct 各自适合什么场景？给定一个「批量处理 1 万条数据并出报表」的任务，你会怎么选？
2. 为什么 MCP 选择 *stdio* 作为默认传输？相比 HTTP/REST 有什么优劣？
3. 一个恶意 MCP server 可以怎么攻击 host？你能想到哪些防御手段？

## 面试题

1. **(基础)** 写一个 Anthropic tool use 的最小循环伪代码，说清楚 `stop_reason == "tool_use"` 的处理。
2. **(深入)** Anthropic 支持 `parallel_tool_use=true`，并行 tool 调用相比串行有哪些挑战？
3. **(系统)** 设计一个「内部所有微服务自动转 MCP server」的方案，需要考虑鉴权、metering、错误处理。
4. **(业务)** 如果让你把部门的「定位 service」变成 MCP server，你会暴露哪些 tools？请列出 3-5 个并写 schema 草案。
