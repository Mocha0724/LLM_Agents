# 第 04 章 · 思考题

## 思考题

1. 用 CoALA 的 4 类记忆，分别给地图业务举一个例子。
2. Generative Agents 中的 reflection trigger 用的是「累计 importance 分」；如果用 token 量代替会有什么影响？
3. MemGPT 的 `core_memory_replace` 工具，可能引入哪些一致性问题？工程上怎么防御？
4. 给定一个客服场景：用户连续 50 轮对话，需要记住偏好与历史问题。请画出你的 memory 体系（哪些走 working / episodic / semantic / procedural）。

## 面试题

1. **(基础)** 解释 RAG 的基本流程，并指出 Naive RAG 的常见失败模式。
2. **(深入)** 对比 Self-RAG、CRAG、Agentic RAG 三者的区别与适用场景。
3. **(系统设计)** 设计一个「百万级 POI 检索 + 智能问答」系统的 RAG 架构。chunking 策略、embedding 模型、混合检索、re-ranker 都要谈到。
4. **(开放)** 现在很多模型支持 100 万+ token context，你认为 RAG 是否会被淘汰？为什么？
