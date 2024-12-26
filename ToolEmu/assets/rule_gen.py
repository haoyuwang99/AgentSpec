from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
import json
from typing import List, Dict
    
def load_json(file_path):
    """Loads JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)

import json
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate

from langchain.output_parsers import PydanticOutputParser


class Tool(BaseModel):
    name : str = ""
    summary : str = ""
    parameters : List[Dict] = []
    returns : List[Dict] = [] 

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            summary=data["summary"],
            parameters=data.get("parameters", []),
            returns=data.get("returns", []), 
        )

class Toolkit(BaseModel): 
    name:str = ""
    description_for_model : str = ""
    tools: List[Tool] = []

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["toolkit"],
            tools= [Tool.from_dict(tool) for tool in data.get("tools", [])],
            description_for_model = data.get("description_for_model", "")
        )

class Case(BaseModel):
    name : str = ""
    toolkits :List[Toolkit]= [] 
    user_instruction:str = ""
    underspecifications: Dict = {}
    expected_achievements :List[str] = []
    potential_risks : List[str]= []

    @classmethod
    def from_dict(cls, data, toolkits_map):
        return cls(
            name=data["name"],
            toolkits=[toolkits_map[toolkit] for toolkit in data.get("Toolkits", [])],
            user_instruction=data.get("User Instruction", ""),
            underspecifications=data.get("Underspecifications", {}),
            expected_achievements=data.get("Expected Achievements", []),
            potential_risks=data.get("Potential Risky Actions", [])
        )


cases_file = "all_cases.json"
toolkits_file = "all_toolkits.json"

case_data = load_json(cases_file)
toolkit_data = load_json(toolkits_file)
   
# Create Case and Toolkit objects
toolkits = { toolkit["toolkit"]: Toolkit.from_dict(toolkit) for toolkit in toolkit_data}
cases = [Case.from_dict(case, toolkits) for case in case_data]


class LLMGeneratedRule(BaseModel):
    rule_desc : str  = Field(description="the description of the rule")
    rule: str = Field(description="the rule")
    predicate_python_impl: Dict = Field(description="python implementation of the check predicates in rule")

class RuleList(BaseModel):
    toolkits: str = Field(description="toolkit name")
    rules: List[LLMGeneratedRule] = Field(description="List of rules")

# generate rule for case risky actions.
def generate_rules(toolkit):
    # for risky_action in case.underspecifications["Safety & Security Constraints"]:
    #     print(risky_action)
    
    parser = PydanticOutputParser(pydantic_object=RuleList)
    messages = [
        SystemMessage(content=f"You are an assistant tasked with generating a Python rule to ensure safety and security for given toolkit."),
        HumanMessage(content=f"""
Chain of Thought
1. Identify Potential Risky Outcomes and Associate with Tools
* Examine the provided toolkits.
* For each tool, identify potential risky outcomes or misuse.
* Document the risks and associated actions/tools.
2. Write Rules for Each Tool and Risk
* Translate each identified risk into a safety rule.
Specify:
    * The trigger (tool).
    * The condition (predicate function).
    * The enforcement mechanism (say user_inspection).
3. Implement Predicate Functions
* Create Python functions to evaluate the risks.
* Use schemas, regex patterns, llm_judge, or logical conditions to detect potential issues. You have the access to call function 
def llm_judge(requirements, action, ctx) -> True:
    \"\"\"
    Uses an LLM to evaluate the requirements for a given action within its context.

    Parameters:
    - requirements: A string prompt specifying the evaluation criteria.
    - action: The action being performed.
    - ctx: Context containing intermediate steps and previous action-observation pairs.

    Returns:
    - The result from the LLM as a boolean. 
    \"\"\"
    # Initialize LangChain's LLM with your preferred model (e.g., OpenAI GPT-4)
    llm = ChatOpenAI(temperature=0.0, model_name="gpt-4")
    
    # Constructing the context messages
    messages = [
        SystemMessage(content="You are an assistant evaluating task importance for risk management."),
        HumanMessage(content=f"Context of previous actions: {{ctx.intermediate_steps}}\n"),
        HumanMessage(content=f"Action being evaluated: {{action}}\nNote: the output should ONLY be 'true' or 'false', indicating the requiement is satisfied"),
        HumanMessage(content=requirements)
    ]
    
    # Query the LLM and parse the response
    response = llm.invoke(messages) 
    return response.content.strip().lower() == \"true\"
* Ensure predicate functions are modular, reusable, and context-aware.                     
"""),
        HumanMessage(content=f"""
You can refer to the following example
Example Rule for Toolkit Terminal:

Toolkit Description:

Example case1: CMD check
{toolkits["Terminal"]}
```
rule @inspect_dangerous_cmd
trigger Execute
check
    is_destructive_command
enforce
    user_inspection
end
```
Note: trigger action must be one of the tool in the current Toolkit(e.g., Execute in Terminal)
Predicate Function examples:
```
import re
def is_destructive_command(action_input: Dict, ctx) -> bool :
    destructive_patterns = [r"\brm\b", r"\bdd\b", r"\bsudo\b"]
    cmd = action["command"] #NOTE: action_input is a dict act as the parameter of the current tool call, check the schema.
    return any(re.search(pattern, cmd) for pattern in destructive_patterns)
```

Example case2: DeleteTodoistTask check
{toolkits["Todoist"]}

Example case1: Todoist check
```
rule @check_before_delete_task
trigger TodoistDeleteTask
check
    has_important_task
enforce
    user_inspection
end
```
Note: trigger action must be one of the tool in the current Toolkit(e.g., Execute in Terminal)
Predicate Function examples:
```
import re
def has_important_task(action_input: Dict, ctx) -> bool :
    return llm_judge("check the task to be deleted has important information", action_input, ctx)
```
""")
        ,
        HumanMessage(content=f"Generate rules for this toolkit: {dict(toolkit)}\n"),
        HumanMessage(content=parser.get_format_instructions())
    ]
    
    prompt = ChatPromptTemplate(messages=messages)  
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
     
    chain = prompt | llm | parser
    toolkit = dict(toolkit)

    res = chain.invoke({"input": "",
    "format_instructions": parser.get_format_instructions()})
    with open("rules.json", 'a') as f: 
        f.write(res.json() + "\n")
        
for name in toolkits:
    generate_rules(toolkits[name])
    