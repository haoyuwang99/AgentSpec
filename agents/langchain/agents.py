from controlled_agent_excector import initialize_controlled_agent 
from langchain_openai import ChatOpenAI
from langchain_community.tools import ShellTool

llm = ChatOpenAI(model = "gpt-4o", temperature=0)

terminal_agent = initialize_controlled_agent([ShellTool()], llm)

assistant_agent = initialize_controlled_agent([], llm)