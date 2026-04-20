"""最小 MCP Client：通过 stdio 启动 server.py 并调用其工具。

运行：
    python client.py
"""

from __future__ import annotations

import asyncio
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_PATH = os.path.join(os.path.dirname(__file__), "server.py")


async def main() -> None:
    params = StdioServerParameters(command=sys.executable, args=[SERVER_PATH])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("[tools]")
            for t in tools.tools:
                print(f"- {t.name}: {t.description}")

            r = await session.call_tool("add", {"a": 2, "b": 3})
            print(f"[call] add(2, 3) -> {r.content[0].text}")

            r = await session.call_tool("now", {"tz": "Asia/Shanghai"})
            print(f"[call] now('Asia/Shanghai') -> {r.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
