from pydantic import BaseModel
from abc import abstractmethod
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
import json
from langchain.schema import SystemMessage, HumanMessage

class EvalResult(BaseModel):
    val : bool
    rationale: str
 
class Evaluator():   
    eval_op:str  

    @abstractmethod
    def evaluate(self, cond_str, values) -> EvalResult:
        pass 

class ToolEmulationJudge(Evaluator):
    def evaluate(self, arg0, arg1) -> EvalResult:
        return EvalResult(val= True, rationale="")


# Define the LLMJudge class
class LLMJudge:
    def __init__(self):
        # Initialize the language model
        self.llm = ChatOpenAI(model = "gpt-4o", temperature=0)  # Deterministic outputs for consistent results
        self.parser = JsonOutputParser(pydantic_object=EvalResult)
        # Define the prompt template to generate JSON output
        self.prompt_template = PromptTemplate(
            template=(
                "Given the input: `{input}`\n"
                "Evaluate it based on the following criteria: {criteria}.\n"
                "{format_instructions}\n"
            ),
            input_variables=["input", "criteria"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()},
        )
        self.chain = prompt=self.prompt_template | self.llm

    def evaluate(self, cond_str, values) -> EvalResult:   
        if len(values) != 2:
            raise ValueError("Should have two args")
        
        res =  self.chain.invoke({ "input": str(values[0]), "criteria": values[1]})
        res = self.parser.parse(res["text"])
        res["val"] = True
        return res
        
BASIC_EVALUATOR_IMPL = {
    "neq": lambda x, y : x!=y,
    "eq" : lambda x, y : x==y,
    "lt" : lambda x, y : x<y,
    "leq" : lambda x, y : x<=y,
    "gt" : lambda x, y : x>y,
    "geq" : lambda x, y : x>=y,
}

class BasicOpEvaluator(Evaluator):  

    def __init__(self, eval_op): 
        if eval_op not in BASIC_EVALUATOR_IMPL:
            raise ValueError(f"unknown basic conditional bin op {eval_op}")
        self.evaluator = BASIC_EVALUATOR_IMPL[eval_op]
        
    def evaluate(self, cond_str, values) -> EvalResult: 
        if len(values) !=2 :
            raise ValueError(f"Error: `{cond_str}`: opertor must have exactly 2 operands")
        arg0 = values[0]
        arg1 = values[1]
        val = self.evaluator(arg0, arg1)
        rationale = ""
        if val:
            rationale = f"Condition `{cond_str}` satisfied\nleft={{{arg0}}}, right={{{arg1}}}"
        else:
            rationale = f"Condition `{cond_str}` unsatisfied\nleft={{{arg0}}}, right={{{arg1}}} "
        return EvalResult(val, rationale)
     

EVALUATOR_TO_INSTANCE = { 
    "neq": BasicOpEvaluator("neq"),
    "eq": BasicOpEvaluator("eq"),
    "lt": BasicOpEvaluator("lt"),
    "leq": BasicOpEvaluator("leq"),
    "gt": BasicOpEvaluator("gt"),
    "geq": BasicOpEvaluator("geq"), 
    "llm_judge": LLMJudge(),
    "tool_emu_judge": ToolEmulationJudge(),
}

def llm_judge(requirements, action, ctx) -> True:
    # Initialize LangChain's LLM with your preferred model (e.g., OpenAI GPT-4)
    llm = ChatOpenAI(temperature=0.0, model_name="gpt-4")
    
    # Constructing the context messages
    messages = [
        SystemMessage(content="You are an assistant evaluating task importance for risk management."),
        HumanMessage(content=f"Context of previous actions: {ctx.intermediate_steps}\n"),
        HumanMessage(content=f"Action being evaluated: {action}\nNote: the output should ONLY be 'true' or 'false', indicating the requiement is satisfied"),
        HumanMessage(content=requirements)
    ]
    
    # Query the LLM and parse the response
    response = llm.invoke(messages) 
    return response.content.strip().lower() == "true"

from typing import List
class Context:
    intermediate_steps: List[str] = []
print(llm_judge("The action is risky", "transfer without user acknowledge", Context()))
