import logging

logging.basicConfig(level=logging.INFO)

from pydantic import BaseModel

from langchain.agents.agent import BaseMultiActionAgent, BaseSingleActionAgent
from langchain_core.agents import AgentAction, AgentFinish
from typing import Union, Optional, Any, List, Dict,Tuple
from langchain_core.callbacks.base import Callbacks
 

class RuleContext(BaseModel):
    agent: Union[BaseSingleActionAgent | BaseMultiActionAgent]
    intermediate_steps: List[Tuple[AgentAction, str]]
    user_input: Optional[Union[str, Dict[str, Any]]] = None
    run_mannager: Optional[Any] = None
    merits: List[str] = []
    critiques: List[str] = [] 
    reflection_depth:int = 0

    def add_merit(self, m: str):
        self.merits.append(m) 

    def set_critique(self, c: str):
        self.critiques.append(c) 