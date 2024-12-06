from langchain.agents import initialize_agent
from controlled_tool import ControlledTool
from langchain.chat_models import ChatOpenAI
from langchain_experimental.tools import  PythonREPLTool
import os

# Initialize the LLM
os.environ["OPENAI_API_KEY"] = "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"

llm = ChatOpenAI(model = "gpt-4o",temperature=0) 

python_tool = ControlledTool(
    name="PythonCodeExecutor",
    func=PythonREPLTool().run,
    description="Use this to perform code tasks.",
    rules = []
)

# Initialize the Agent
tools = [python_tool]
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# Interact with the Agent
response = agent.run("Can you help create a file named a.txt in current directory")
print(response)
