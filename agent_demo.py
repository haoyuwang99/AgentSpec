from controlled_agent_excector import initialize_controlled_agent 
from langchain.tools import Tool
from langchain.chat_models import ChatOpenAI
from langchain_experimental.tools import  PythonREPLTool
from agent_rule import Rule
from global_states import *
import os

# Initialize the LLM
llm = ChatOpenAI(model = "gpt-4o-mini", temperature=0)  

def demo1():
 
    rule = Rule.from_text(example_rule) 

    python_tool = Tool(
        name="PythonCodeExecutor",
        func=PythonREPLTool().run,
        description="Use this to perform code tasks."
    )

    # Initialize the Agent
    tools = [python_tool]
    # instead of use initialize agent from langchain, 
    # add rule for initialize controlled agent, where rules are list of rule strings. 
    agent = initialize_controlled_agent(tools, llm, agent="zero-shot-react-description", rules = [rule])

    # Interact with the Agent
    response = agent.invoke("Can you help create a file named a.txt in current directory")
    print(response)

from langchain_community.tools.playwright.utils import (
    create_async_playwright_browser,  # A synchronous browser is available, though it isn't compatible with jupyter.\n",	  },
)
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain.agents import AgentType, initialize_agent
 
import asyncio
from playwright.async_api import async_playwright

# Ensure this import is correct in your environment
# from your_project import PlayWrightBrowserToolkit

async def playwright_demo():
    async with async_playwright() as playwright:
        # Launch the browser
        browser = await playwright.chromium.launch()
        # Initialize the toolkit with the correct browser instance
        toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
        tools = toolkit.get_tools()

        # Map tools by their names
        tools_by_name = {tool.name: tool for tool in tools}

        try:
            # Retrieve specific tools by name
            navigate_tool = tools_by_name.get("navigate_browser")
            get_elements_tool = tools_by_name.get("get_elements")

            if not navigate_tool or not get_elements_tool:
                raise ValueError("Required tools are not available in the toolkit")
            print("before navigate")
            # Use the navigate tool to visit the URL
            await navigate_tool.arun(
                {"url": "https://google.com"}
            )
            print("Navigation completed successfully.")
        
        except Exception as e:
            print(f"Error during tool execution: {e}")
        
        finally:
            # Clean up the browser
            await browser.close()

async def main():
    # Use the async context manager for Playwright
    async with async_playwright() as playwright:
        # Launch the browser
        browser = await playwright.chromium.launch(headless=True)

        # Initialize PlaywrightBrowserToolkit
        toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
        tools = toolkit.get_tools()

        # Initialize the agent
        agent_chain = initialize_agent(
            tools,
            llm,  # Ensure this is a properly initialized language model
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            max_iterations=100, 
        )

        # Run the agent's task
        result = await agent_chain.arun("Gather the latest research papers on llm agent safety" )
        with open("list.txt", 'w') as f:
            f.write(str(result))
 

# Run the asynchronous function
asyncio.run(main())