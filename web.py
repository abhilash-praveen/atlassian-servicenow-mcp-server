import json
import os
import traceback

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from openai import AsyncOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="Jira & Confluence Assistant")
app.mount("/static", StaticFiles(directory="static"), name="static")

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()  # "openai" or "ollama"
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2" if LLM_PROVIDER == "ollama" else "gpt-4o")

if LLM_PROVIDER == "ollama":
    openai_client = AsyncOpenAI(
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
        api_key="ollama",
    )
else:
    openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SERVER_PATH = "main.py"


async def get_mcp_tools(session: ClientSession) -> list[dict]:
    tools_result = await session.list_tools()
    return [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema,
            },
        }
        for tool in tools_result.tools
    ]


async def call_mcp_tool(session: ClientSession, tool_name: str, tool_args: dict) -> str:
    result = await session.call_tool(tool_name, tool_args)
    if not result.content:
        return ""
    item = result.content[0]
    text = item.text if hasattr(item, "text") else str(item)
    if getattr(result, "isError", False):
        return f"Error: {text}"
    return text


async def run_agent(user_prompt: str) -> dict:
    server_params = StdioServerParameters(command="uv", args=["run", SERVER_PATH])
    steps = []

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await get_mcp_tools(session)
            messages = [{"role": "user", "content": user_prompt}]

            while True:
                response = await openai_client.chat.completions.create(
                    model=LLM_MODEL,
                    tools=tools,
                    messages=messages,
                )
                message = response.choices[0].message

                if not message.tool_calls:
                    return {"answer": message.content, "steps": steps}

                messages.append(message)
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    if not isinstance(tool_args, dict):
                        tool_args = {}
                    result = await call_mcp_tool(session, tool_name, tool_args)
                    steps.append({
                        "tool": tool_name,
                        "args": tool_args,
                        "result": result,
                    })
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    })


class ChatRequest(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html") as f:
        return f.read()


@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        return await run_agent(req.message)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
