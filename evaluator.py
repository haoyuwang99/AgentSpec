from pydantic import BaseModel
from abc import abstractmethod

class EvalResult(BaseModel):
    val : bool
    rationale: str
 
class Evaluator(BaseModel):  

    eval_op:str
    
    def __init__(self, eval_op):
        self.eval_op = eval_op

    @abstractmethod
    def evaluate(self, arg0, arg1) -> EvalResult:
        pass 
class ToolEmulationJudge(Evaluator):
    def evaluate(self, arg0, arg1) -> EvalResult:
        return EvalResult(True,"")

class LLMJudge(Evaluator):
    def evaluate(self, arg0, arg1)-> EvalResult: 
        return EvalResult(True,"") 

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
     

EVALUATOR_TO_CLASS = { 
    "eq": BasicOpEvaluator,
    "lt": BasicOpEvaluator,
    "leq": BasicOpEvaluator,
    "gt": BasicOpEvaluator,
    "geq": BasicOpEvaluator, 
    "llm_judge": LLMJudge,
    "tool_emu_judge": ToolEmulationJudge,
}