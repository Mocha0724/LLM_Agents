"""最小 MCP Server：暴露 add / now 两个工具。

启动：
    python server.py     # stdio 模式（被 host 通过子进程方式启动）
"""

from __future__ import annotations

import asyncio
import datetime
from zoneinfo import ZoneInfo

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

server = Server("agents-guide-demo")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="add",
            description="加法：返回 a + b",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"},
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="now",
            description="返回指定 IANA 时区当前时间（ISO 8601）",
            inputSchema={
                "type": "object",
                "properties": {"tz": {"type": "string", "description": "如 Asia/Shanghai"}},
                "required": ["tz"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "add":
        return [TextContent(type="text", text=str(arguments["a"] + arguments["b"]))]
    if name == "now":
        try:
            t = datetime.datetime.now(ZoneInfo(arguments["tz"])).isoformat(timespec="seconds")
        except Exception as e:
            t = f"Error: {e}"
        return [TextContent(type="text", text=t)]
    raise ValueError(f"unknown tool: {name}")


async def main() -> None:
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
