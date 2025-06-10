import asyncio
import os
import warnings

from dotenv import load_dotenv
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Hướng dẫn sử dụng:
# 1. Đảm bảo đã cài các package: mcp, langchain-mcp-adapters, langgraph, langchain[anthropic]
# 2. Chạy: python langchain_cli.py
#


load_dotenv()

# Lấy API key từ environment
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")


class UltraCleanStreamHandler:
    def __init__(self):
        self.buffer = ""
        self.in_text_generation = False
        self.last_was_tool = False

    def handle_chunk(self, chunk):
        event = chunk.get("event", "")
        if event == "on_chat_model_stream":
            data = chunk.get("data", {})
            chunk_data = data.get("chunk", {})
            if hasattr(chunk_data, "content"):
                content = chunk_data.content
                if isinstance(content, str) and not content.startswith('{"'):
                    if self.last_was_tool:
                        print(" ", end="", flush=True)
                        self.last_was_tool = False
                    print(content, end="", flush=True)
                    self.in_text_generation = True
                elif isinstance(content, list):
                    for item in content:
                        if (
                            isinstance(item, dict)
                            and item.get("type") == "text"
                            and "partial_json" not in str(item)
                        ):
                            text = item.get("text", "")
                            if text and not text.startswith('{"'):
                                if self.last_was_tool:
                                    print(" ", end="", flush=True)
                                    self.last_was_tool = False
                                print(text, end="", flush=True)
                                self.in_text_generation = True
        elif event == "on_tool_start":
            if self.in_text_generation:
                print(f"\n🔧 {chunk.get('name', 'tool')}", end="", flush=True)
                self.in_text_generation = False
        elif event == "on_tool_end":
            print(" ✅", end="", flush=True)
            self.last_was_tool = True


# async def main():
#     server_params = StdioServerParameters(
#         command="uv",
#         args=[
#             "run",
#             "--with",
#             "mcp-clickhouse",
#             "--python",
#             "3.13",
#             "mcp-clickhouse",
#         ],
#         env={
#             "CLICKHOUSE_HOST": "localhost",
#             "CLICKHOUSE_PORT": "8123",
#             "CLICKHOUSE_USER": "admin",
#             "CLICKHOUSE_PASSWORD": "password",
#             "CLICKHOUSE_SECURE": "false",
#         },
#     )
#     async with stdio_client(server_params) as (read, write):
#         async with ClientSession(read, write) as session:
#             await session.initialize()
#             tools = await load_mcp_tools(session)
#             agent = create_react_agent("anthropic:claude-sonnet-4-0", tools)
#             handler = UltraCleanStreamHandler()
#             async for chunk in agent.astream_events(
#                 {
#                     "messages": [
#                         {
#                             "role": "user",
#                             "content": "Draw a simple chart of total transactions",
#                         }
#                     ]
#                 },
#                 version="v1",
#             ):
#                 handler.handle_chunk(chunk)
#             print("\n")


# if __name__ == "__main__":
#     asyncio.run(main())


async def run_agent_stream(prompt: str):
    server_params = StdioServerParameters(
        command="uv",
        args=[
            "run",
            "--with",
            "mcp-clickhouse",
            "--python",
            "3.13",
            "mcp-clickhouse",
        ],
        env={
            "CLICKHOUSE_HOST": "localhost",
            "CLICKHOUSE_PORT": "8123",
            "CLICKHOUSE_USER": "admin",
            "CLICKHOUSE_PASSWORD": "password",
            "CLICKHOUSE_SECURE": "false",
        },
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent = create_react_agent("anthropic:claude-sonnet-4-0", tools)

            async for chunk in agent.astream_events(
                {"messages": [{"role": "user", "content": prompt}]},
                version="v1",
            ):
                yield chunk  # Stream từng chunk cho UI xử lý
