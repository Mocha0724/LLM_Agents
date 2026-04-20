# 最小 MCP Server Demo

本目录提供一个最小可运行的本地 MCP Server，暴露两个工具：

- `add(a, b)` — 加法
- `now(tz)` — 返回指定时区的 ISO 时间

## 安装

```bash
pip install "mcp>=1.0.0"
```

## 启动 Server（stdio 模式）

```bash
python server.py
```

它会用 stdio 通信，不会输出任何东西到 stdout —— 这是设计如此（stdio 用于协议通信，日志请打到 stderr）。

## 用 Python Client 调用

```bash
python client.py
```

预期输出（示例）：

```text
[tools]
- add: 加法
- now: 返回时区当前时间
[call] add(2, 3) -> 5
[call] now('Asia/Shanghai') -> 2026-04-20T...
```

## 接入 Claude Desktop

把以下加入 `~/Library/Application Support/Claude/claude_desktop_config.json`：

```json
{
  "mcpServers": {
    "agents-guide-demo": {
      "command": "python",
      "args": ["/绝对路径/Agents_Guide/03_tool_use_and_mcp/mcp_demo/server.py"]
    }
  }
}
```

重启 Claude Desktop 即可在工具列表看到 `add` / `now`。

## 接入 Cursor

在 Cursor 的 *Settings → MCP* 添加同样配置。

## 接下来

- 把 `add` / `now` 替换成你自己的算法 API（如 `relocalize`、`map_match`），就得到一个「定位算法 MCP server」。
- 和第 11 章的「地图 Agent」结合，让 LLM 通过 MCP 调用真实地图 / 定位服务。
