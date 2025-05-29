from pydantic import BaseModel

from .agent import Action
from langchain.agents.agent import BaseMultiActionAgent, BaseSingleActionAgent
from typing import Union, Optional, Any, List, Dict, Tuple
from langchain_core.callbacks.base import Callbacks
 
class RuleState(BaseModel):
    toolkit: str = ""
    action: Optional[Action] = None
    agent: Optional[Union[BaseSingleActionAgent, BaseMultiActionAgent]] = None
    intermediate_steps: Any #todo: List[Tuple[AgentAction, str]]
    user_input: Optional[Union[str, Dict[str, Any]]] = None # task_prompt
    run_mannager: Optional[Any] = None
    merits: List[str] = []
    critiques: List[str] = [] 
    reflection_depth:int = 0

    def add_merit(self, m: str):
        self.merits.append(m) 

    def set_critique(self, c: str):
        self.critiques.append(c) 