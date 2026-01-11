from controlled_agent_excector import initialize_controlled_agent 
from langchain_experimental.utilities import PythonREPL
from langchain_openai import ChatOpenAI

from langchain_core.agents import AgentAction, AgentFinish, AgentStep
from langchain.agents import initialize_agent, types
# from langchain.agents.agent_types import AgentType
from langchain.tools import tool, Tool

with open("../key.txt") as f:
    key = f.read()

# Initialize the LLM
llm = ChatOpenAI(model = "gpt-4o", api_key=key)



repl_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=PythonREPL().run
)

tools = [repl_tool]

from rule import Rule
# rules for inspection before every tool call

rule_before_tool_execution = """
rule @stop_before_tool
trigger
    before_action
check
    true
enforce
    user_inspection
end
"""

rule_before_tool_execution = Rule.from_text(rule_before_tool_execution)
print(rule_before_tool_execution.event)

agent = initialize_controlled_agent(tools, llm, agent="zero-shot-react-description", rules =[rule_before_tool_execution])

res = agent.invoke("what is 1.123+1.432?")
print(res)

