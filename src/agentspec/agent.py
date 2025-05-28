from abc import abstractmethod
from pydantic import BaseModel 
import langchain_core.agents
from typing import Any, Union
# key component of llm agent

class Action(BaseModel):

    name: str
    input: Any
    action: Any #
    
    def is_skip(self):
        return self.name == "skip"
    
    def is_finish(self):
        return self.name=="finish"
    
    def get_finish(output, log):
        return Action(name= "finish", input=None, action= langchain_core.agents.AgentFinish({"output": output}, log)) # TODO: map from different framework here.

    def get_skip():
        return Action(name = "skip", input = None, action=None)

    def from_langchain(action: Union[langchain_core.agents.AgentAction, langchain_core.agents.AgentFinish]):
        if isinstance(action, langchain_core.agents.AgentAction):
            return Action(name = action.tool, input= action.tool_input, action = action)
        else:
            return Action(name = "finish", input=None, action = action)
    
    def from_gym():
        pass
    
    # get the original action input
    def unwrap(self):
        return self.action

class ControlledAgent():

    @abstractmethod
    def plan():
        pass

    @abstractmethod
    def invoke():
        pass
    
class Tool():
    pass