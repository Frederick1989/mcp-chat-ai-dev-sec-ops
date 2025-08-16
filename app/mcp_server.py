import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from transformers import pipeline
import os

MODEL = os.getenv("MODEL_NAME", "microsoft/DialoGPT-small")
pipe = pipeline("conversational", model=MODEL)

server = Server("ai-chatbot-mcp")

@server.call_tool()
async def chat_tool(arguments: dict) -> str:
    prompt = arguments["prompt"]
    return str(pipe(prompt))

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write)

if __name__ == "__main__":
    asyncio.run(main())