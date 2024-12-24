from abc import abstractmethod
from enum import Enum
from pydantic import BaseModel 
from agent import Action
from typing import Union, Tuple, Dict
from state import RuleState

class EnforceResult(Enum):
    CONTINUE =0
    FINISH = 1
    SELF_REFLECT = 2

class Enforcement(BaseModel): 
    state: RuleState

    @abstractmethod
    def apply(action) -> Tuple[EnforceResult, Action]:  
        pass

class EmptyEnforcement(Enforcement):
    def apply(self, action: Action) -> Tuple[EnforceResult, Action]:
        return EnforceResult.CONTINUE, action
    
class UserInspection(Enforcement): 
    def apply(self, action: Action) -> Tuple[EnforceResult, Action]: 
        """
        Prompt the user to decide whether to take an action.
        """
        user_auth = False

        while True:
            user_input = input(f"{str(action)}\n Do you want to perform the above action? (yes/no)\n").strip().lower()
            if user_input in {"yes", "y"}:
                print("Action confirmed. Proceeding...")
                user_auth = True
                break
            elif user_input in {"no", "n"}:
                print("Action declined. Exiting...")
                user_auth = False
                break          
            else:
                print("Invalid input. Please type 'yes' or 'no'.")

        if user_auth : 
            return EnforceResult.CONTINUE, action
        else : 
           return EnforceResult.FINISH, Action.get_finish("" ,f"action {action.name}({action.input}) interrupted by user")

class LLMSelfReflect(Enforcement):
 
    def apply(self, action: Action):
        if self.state.reflection_depth > 3: #TODO: Magic Number
            return EnforceResult.FINISH, Action.get_finish("", "llm self reflect exceeds max trials")

        if action.is_finish(): 
            return EnforceResult.FINISH, action 

        ctx = self.state
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