import asyncio
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SERVER_PATH = "main.py"

async def get_mcp_tools(session: ClientSession) -> list[dict]:
    """Fetch tools from the MCP server and convert to OpenAI tool format."""
    tools_result = await session.list_tools()
    tools = []
    for tool in tools_result.tools:
        tools.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema,
            }
        })
    return tools


async def call_mcp_tool(session: ClientSession, tool_name: str, tool_args: dict) -> str:
    """Call a tool on the MCP server and return the result as a string."""
    result = await session.call_tool(tool_name, tool_args)
    return str(result.content[0].text)


async def run(user_prompt: str):
    """Main loop — sends prompt to OpenAI, handles tool calls, prints final answer."""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", SERVER_PATH]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Get tools from MCP server
            tools = await get_mcp_tools(session)
            print(f"Loaded {len(tools)} tools from MCP server ✓")

            messages = [{"role": "user", "content": user_prompt}]

            # Agentic loop
            while True:
                response = openai_client.chat.completions.create(
                    model="gpt-4o",
                    tools=tools,
                    messages=messages,
                )

                message = response.choices[0].message

                # No tool calls — we have our final answer
                if not message.tool_calls:
                    print("\nAssistant:", message.content)
                    break

                # Handle tool calls
                messages.append(message)
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)

                    print(f"\nCalling tool: {tool_name} with args: {tool_args}")
                    result = await call_mcp_tool(session, tool_name, tool_args)
                    print(f"Tool result: {result}")

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    })


if __name__ == "__main__":
    import sys
    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "What tools do you have available?"
    asyncio.run(run(prompt))