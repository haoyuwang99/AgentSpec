from abc import abstractmethod
from enum import Enum
from pydantic import BaseModel 
from langchain_core.agents import AgentAction ,AgentFinish
from typing import Union , Tuple, Dict
from context import RuleContext
 

class EnforceResult(Enum):
    CONTINUE =0
    FINISH = 1
    SELF_REFLECT = 2

class Enforcement(BaseModel):    

    ctx: RuleContext

    @abstractmethod
    def apply(action) -> Tuple[Union[AgentFinish, AgentAction], EnforceResult]:  
        pass

class EmptyEnforcement(Enforcement):
    def apply(self, action):
        return EnforceResult.CONTINUE, action
    
class UserInspection(Enforcement):
    def apply(self, action):
        user_auth = False
        if user_auth : 
            return EnforceResult.CONTINUE, action
        else : 
           return EnforceResult.FINISH, AgentFinish({"output": "action interrupted by user"}, "action interrupted by user")

class LLMSelfReflect(Enforcement):
 
    def apply(self, action):
        if self.ctx.reflection_depth > 3: #TODO: Magic Number
            return EnforceResult.FINISH, AgentFinish({"output": "llm self reflect exceeds max trials"}, "llm self reflect exceeds max trials")

        if isinstance(action, AgentFinish): 
            return EnforceResult.FINISH, action 

        ctx = self.ctx
        inputs_prime = ctx.user_input
        ref_str =  f"""\n\nConsider the following (output,comment) pair for better action planning:
Output action:{str(action)}
Comment: 
* merit: {str(ctx.merits)}
* critique: {str(ctx.critiques)}"""  #TODO: merit could be the passed rules
        if isinstance(inputs_prime, Dict): 
            inputs_prime["input"] = inputs_prime["input"] + ref_str
        else: 
            inputs_prime = inputs_prime + ref_str
        action_prime = ctx.agent.plan(
            ctx.intermediate_steps,
            callbacks=ctx.run_mannager.get_child() if ctx.run_mannager else None,
            **inputs_prime,
        )   
        ctx.reflection_depth = ctx.reflection_depth + 1
        return EnforceResult.SELF_REFLECT, action_prime
  

ENFORCEMENT_TO_CLASS = {
    "none" : EmptyEnforcement,
    "llm_self_reflect": LLMSelfReflect,
    "user_inspection" : UserInspection
} 