import os
import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
from dotenv import load_dotenv, find_dotenv
from tavily import AsyncTavilyClient


#Loading Gemini API
load_dotenv(find_dotenv())
set_tracing_disabled(disabled=True)

gemini_api_key = os.environ.get("GEMINI_API_KEY")
tavily_api_key = os.environ.get("TAVILY_API_KEY")


# Loading Tavily API
tavily_client = AsyncTavilyClient(api_key = tavily_api_key)


# 1. Provider
provider = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/",
)

# 2. Model
llm_model = OpenAIChatCompletionsModel(
    openai_client = provider,
    model = "gemini-2.5-flash",
)

# 3. Function Tool --> Decorator
@function_tool()
async def search(query: str) -> str:
    print("Searching for:", query)
    response = await tavily_client.search(query)
    # print("Search response:", response)
    return response

#3 Agent
agent: Agent = Agent (
    name = "SearchAgent",
    model = llm_model,
    tools = [search],
)

# print("agent tools:", agent.tools)
async def main():
    runner = await Runner.run(agent, "Who is the CM of Sindh Pakistan?")
    print("BOT:", runner.final_output)

asyncio.run(main())