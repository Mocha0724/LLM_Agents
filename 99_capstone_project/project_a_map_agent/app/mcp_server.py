"""把地图工具暴露成 MCP server。

启动：
    python -m app.mcp_server
然后在 Cursor / Claude Desktop 的 MCP 配置里指向本进程即可。
"""
from __future__ import annotations

import asyncio
import json

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from .tools import READ_TOOLS

server = Server("map-agent")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="geocode",
            description="把中文地址转成经纬度。",
            inputSchema={
                "type": "object",
                "properties": {"address": {"type": "string"}},
                "required": ["address"],
            },
        ),
        Tool(
            name="poi_search",
            description="在指定中心点周围搜索 POI。",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {"type": "string"},
                    "near": {"type": "object", "properties": {"lat": {"type": "number"}, "lng": {"type": "number"}}, "required": ["lat", "lng"]},
                    "radius_m": {"type": "integer", "default": 2000},
                },
                "required": ["keyword", "near"],
            },
        ),
        Tool(
            name="route",
            description="计算两点之间路径的距离与时长。",
            inputSchema={
                "type": "object",
                "properties": {
                    "origin": {"type": "object", "properties": {"lat": {"type": "number"}, "lng": {"type": "number"}}, "required": ["lat", "lng"]},
                    "destination": {"type": "object", "properties": {"lat": {"type": "number"}, "lng": {"type": "number"}}, "required": ["lat", "lng"]},
                    "mode": {"type": "string", "enum": ["walking", "cycling", "driving"], "default": "walking"},
                },
                "required": ["origin", "destination"],
            },
        ),
        Tool(
            name="explain_route",
            description="把 route 结果转成中文话术。",
            inputSchema={
                "type": "object",
                "properties": {"route": {"type": "object"}},
                "required": ["route"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    fn = READ_TOOLS.get(name)
    if not fn:
        return [TextContent(type="text", text=json.dumps({"error": f"unknown tool: {name}"}))]
    try:
        result = fn(**arguments)
    except Exception as e:
        result = {"error": str(e)}
    return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]


async def main() -> None:
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
