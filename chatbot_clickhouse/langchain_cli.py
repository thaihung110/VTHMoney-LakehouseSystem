import os

from dotenv import load_dotenv
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Đảm bảo đã cài các package: mcp, langchain-mcp-adapters, langgraph, langchain[anthropic]

load_dotenv()

# Lấy API key từ environment
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")


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
