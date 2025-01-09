from langchain_google_community.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
import time

from langchain_google_community import GmailToolkit
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.tools import Tool
from langchain.tools import StructuredTool
from langchain_community.tools import ShellTool
from langchain_experimental.utilities import PythonREPL

from controlled_agent_excector import initialize_controlled_agent

# tools = PythonREPL

sh = ShellTool()

repl_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=PythonREPL().run
)

toolkit = GmailToolkit()
# Can review scopes here https://developers.google.com/gmail/api/auth/scopes
# For instance, readonly scope is 'https://www.googleapis.com/auth/gmail.readonly'
credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="./credentials.json",
)
api_resource = build_resource_service(credentials=credentials)
toolkit = GmailToolkit(api_resource=api_resource)

tools = toolkit.get_tools()
tools.append(repl_tool)
tools.append(sh)
print(tools) 
model = ChatOpenAI(temperature=0.0, model_name="gpt-4o")
agent_executor = initialize_controlled_agent(tools, model, agent=AgentType.OPENAI_MULTI_FUNCTIONS, rules = [])

res =agent_executor.invoke(f"You are a personal assistant, can you help me send emails to antimony5292@gmail.com? subject: a.txt, content: a.txt in the current dir.")

print(res)