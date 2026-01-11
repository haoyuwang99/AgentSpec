from rules.manual.table import predicate_table
from rule import Rule

def is_destructive(_, tool_input, interm):
    print(tool_input)
    return True

rule_before_tool_execution = Rule.from_text("""
rule @stop_before_tool
trigger
    python_repl
check
    is_destructive
enforce
    user_inspection
end
""")
# customizing event: this require instrumentation different stage of the agent

# customizing predicate: this require defining context of the agent. 

# customizing enforcement: this take over the control of the agent.
from langchain.tools import Tool
from controlled_agent_excector import initialize_controlled_agent 
from langchain_experimental.utilities import PythonREPL
from langchain_openai import ChatOpenAI
from rules.manual.table import predicate_table

with open("../key.txt") as f:
    key = f.read()

# Initialize the LLM
llm = ChatOpenAI(model = "gpt-4o", api_key=key)


def check_weather(city):
    print(f"The weather of {city} is sunny!")
    
weather_tool = Tool(
    name="weather",
    description="Check the weather of a city",
    func=check_weather
)


repl_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=PythonREPL().run
)

tools = [repl_tool, weather_tool]

# customizing predicates using pattern matching
def is_destructive(_, tool_input, interm):
    print("checking!!!!!!!")
    if tool_input.find("os.remove") != -1:
        return True
    return False

# or using llm as a judge
def is_destructive(_, tool_input, interm):
    # specify the compilance requirement in natural language:
    safety_requirement = "check whether the code is not doing math calculation" # not doing math calculation
    prompt= f"""You are a experienced python, check whether the code satify the requirement:
    code: {tool_input}
    requirement: {safety_requirement}
    intermediate steps,
    return true the requirement is violated, only output true or false.
"""
    res = llm.invoke(prompt)
    print(prompt) 
    print(res.content)
    return res.content.lower() == "true"


predicate_table["is_destructive"] = is_destructive

# The event is customized to monitor before the execution of the python interpreter.
# The check here is customized to what we defined above.
# The enforce here can be seclected from stop, user_inspection, llm_self_reflect
rule_python_destructive = Rule.from_text("""
rule @stop_before_tool
trigger
    python_repl
check
    is_destructive
enforce
    llm_self_reflect
end
""")

python_controlled_agent = initialize_controlled_agent(tools, llm, agent="zero-shot-react-description", rules = [rule_python_destructive])

res = python_controlled_agent.invoke("what is 1.32454+1.453234")
print(res)