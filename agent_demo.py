import logging

logging.basicConfig(level=logging.INFO)

from controlled_agent_excector import initialize_agent 
from langchain.tools import Tool
from langchain.chat_models import ChatOpenAI
from langchain_experimental.tools import  PythonREPLTool
from agent_rule import Rule
from global_states import *
import os

# Initialize the LLM
os.environ["OPENAI_API_KEY"] = "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"

llm = ChatOpenAI(model = "gpt-4o-mini",temperature=0)  

rule = Rule.from_text(example_rule) 

python_tool = Tool(
    name="PythonCodeExecutor",
    func=PythonREPLTool().run,
    description="Use this to perform code tasks."
)

# Initialize the Agent
tools = [python_tool]
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", rules = [rule], verbose=True)

# Interact with the Agent
response = agent.invoke("Can you help create a file named a.txt in current directory")
print(response)
