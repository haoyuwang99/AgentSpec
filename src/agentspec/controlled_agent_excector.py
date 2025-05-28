from langchain.agents.agent import AgentExecutor
from typing import Optional
from typing import List, Union
from .agent import Action
import json

from langchain_core.exceptions import OutputParserException
from langchain_core.agents import AgentAction, AgentFinish, AgentStep
from langchain.agents.agent import ExceptionTool
from .interpreter import RuleInterpreter
from .rule import *
from .state import RuleState
from .enforcement import *

"""Load controlled agent."""

from typing import Any, Optional, Sequence

from langchain_core._api import deprecated
from langchain_core.callbacks import BaseCallbackManager
from langchain_core.language_models import BaseLanguageModel
from langchain_core.tools import BaseTool

from langchain._api.deprecation import AGENT_DEPRECATION_WARNING 
from langchain.agents.agent_types import AgentType
from langchain.agents.loading import AGENT_TO_CLASS, load_agent
from langchain_core.runnables import Runnable, RunnableConfig
from typing import Dict


NextStepOutput = List[Union[AgentFinish, AgentAction, AgentStep]]

class ControlledAgentExecutor(AgentExecutor) : 
    rules: Optional[List[Rule]]
    user_input: Optional[Dict[str, Any]] = None
   
    def invoke(
        self,
        input: Dict[str, Any],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any):
        self.user_input = input  
        return super().invoke(input, config, **kwargs) 
    
    @classmethod
    def from_agent_and_tools(cls, agent, tools, rules, callbacks = None, **kwargs):
      
        """Create from agent and tools.
 
        Args:
           agent: Agent to use.
           tools: Tools to use.
           callbacks: Callbacks to use.
           kwargs: Additional arguments.
 
        Returns:
           AgentExecutor: Agent executor object.
        """
        return cls(
           agent=agent,
           tools=tools,
           rules = rules,
           callbacks=callbacks,
           handle_parsing_errors=True, # important: other wise, skip will raise parsing error.
           return_intermediate_steps=True,
           **kwargs,
        ) 


    def _consume_next_step(
        self, values: NextStepOutput
    ) -> Union[AgentFinish, List[Tuple[AgentAction, str]]]: 
        if isinstance(values[-1], AgentFinish):
            assert len(values) == 1
            # self.validate_and_enforce(action)
            return values[-1]
        else:
            return [
                (a.action, a.observation) for a in values if isinstance(a, AgentStep)
            ]
    
    def validate_and_enforce(self, action: Action, state: RuleState): 
        if self.rules==None:
            raise ValueError("rules should not be none")
        for rule in self.rules:  
            if action.is_finish() and rule.trigger_finished() or rule.triggered(action.name, action.input): 
                interpreter = RuleInterpreter(rule, state)
                res, action = interpreter.verify_and_enforce(action)
                if res == EnforceResult.CONTINUE:
                    continue
                elif res == EnforceResult.SKIP:
                    return rule, Action.get_skip()
                elif res == EnforceResult.STOP:
                    return rule, Action.get_finish(f"action stopped by {rule.raw}", f"action stopped by {rule.raw}")
                elif res == EnforceResult.SELF_REFLECT: 
                    return self.validate_and_enforce(action, state)
                else:
                    raise ValueError("Unreachable")
        return None, action

    def _iter_next_step(self, name_to_tool_map, color_mapping, inputs, intermediate_steps, run_manager = None):
        """Take a single step in the thought-action-observation loop. 
        """
        try:
            intermediate_steps = self._prepare_intermediate_steps(intermediate_steps) 
            # Call the LLM to see what to do.
            output = self._action_agent.plan(
                intermediate_steps,
                callbacks=run_manager.get_child() if run_manager else None,
                **inputs,
            )  
            # with open("code_agent_exec", 'a') as f:
            #     o = { "prompt": inputs, "code": str(output)}
            #     f.write(json.dumps(o))

           
        except OutputParserException as e:
            if isinstance(self.handle_parsing_errors, bool):
                raise_error = not self.handle_parsing_errors
            else:
                raise_error = False
            if raise_error:
                raise ValueError(
                    "An output parsing error occurred. "
                    "In order to pass this error back to the agent and have it try "
                    "again, pass `handle_parsing_errors=True` to the AgentExecutor. "
                    f"This is the error: {str(e)}"
                )
            text = str(e)
            if isinstance(self.handle_parsing_errors, bool):
                if e.send_to_llm:
                    observation = str(e.observation)
                    text = str(e.llm_output)
                else:
                    observation = "Invalid or incomplete response"
            elif isinstance(self.handle_parsing_errors, str):
                observation = self.handle_parsing_errors
            elif callable(self.handle_parsing_errors):
                observation = self.handle_parsing_errors(e)
            else:
               raise ValueError("Got unexpected type of `handle_parsing_errors`")
            output = AgentAction("_Exception", observation, text)
            if run_manager:
                run_manager.on_agent_action(output, color="green")
            tool_run_kwargs = self._action_agent.tool_run_logging_kwargs()
            observation = ExceptionTool().run(
                output.tool_input,
                verbose=self.verbose,
                color=None,
                callbacks=run_manager.get_child() if run_manager else None,
                **tool_run_kwargs,
            )
            yield AgentStep(action=output, observation=observation)
            return

        action = Action.from_langchain(output)
        state = RuleState(
            action = action,
            agent =self._action_agent,
            intermediate_steps=intermediate_steps,
            user_input=inputs
        )
        # todo: need an adapter here.
        rule, action = self.validate_and_enforce(action, state) 
        if action.is_skip():
            observation_text = f"after the enforcement of rule:\n{rule.raw}, the action is skipped by user" 
            yield AgentStep(action=output, observation=observation_text)
            return
        output = action.unwrap()
        # If the tool chosen is the finishing tool, then we end and return.
        if isinstance(output, AgentFinish):
            yield output
            return
 
        actions: List[AgentAction]

        if output == None:
            return
        if isinstance(output, AgentAction):
            actions = [output]
        else: 
            actions = output 
        for agent_action in actions:
            yield agent_action
        for agent_action in actions:
            yield self._perform_agent_action(
                name_to_tool_map, color_mapping, agent_action, run_manager
            )
 
         
def initialize_controlled_agent(
    tools: Sequence[BaseTool],
    llm: BaseLanguageModel,
    agent: Optional[AgentType] = None,
    rules: List[Rule] = [],
    callback_manager: Optional[BaseCallbackManager] = None,
    agent_path: Optional[str] = None,
    agent_kwargs: Optional[dict] = None,
    *,
    tags: Optional[Sequence[str]] = None,
    **kwargs: Any,
) -> ControlledAgentExecutor:
    """Load an agent executor given tools and LLM.

    Args:
        tools: List of tools this agent has access to.
        llm: Language model to use as the agent.
        agent: Agent type to use. If None and agent_path is also None, will default
            to AgentType.ZERO_SHOT_REACT_DESCRIPTION. Defaults to None.
        callback_manager: CallbackManager to use. Global callback manager is used if
            not provided. Defaults to None.
        agent_path: Path to serialized agent to use. If None and agent is also None,
            will default to AgentType.ZERO_SHOT_REACT_DESCRIPTION. Defaults to None.
        agent_kwargs: Additional keyword arguments to pass to the underlying agent.
            Defaults to None.
        tags: Tags to apply to the traced runs. Defaults to None.
        kwargs: Additional keyword arguments passed to the agent executor.

    Returns:
        An agent executor.

    Raises:
        ValueError: If both `agent` and `agent_path` are specified.
        ValueError: If `agent` is not a valid agent type.
        ValueError: If both `agent` and `agent_path` are None.
    """
    tags_ = list(tags) if tags else []
    if agent is None and agent_path is None:
        agent = AgentType.ZERO_SHOT_REACT_DESCRIPTION
    if agent is not None and agent_path is not None:
        raise ValueError(
            "Both `agent` and `agent_path` are specified, "
            "but at most only one should be."
        )
    if agent is not None:
        if agent not in AGENT_TO_CLASS:
            raise ValueError(
                f"Got unknown agent type: {agent}. "
                f"Valid types are: {AGENT_TO_CLASS.keys()}."
            )
        tags_.append(agent.value if isinstance(agent, AgentType) else agent)
        agent_cls = AGENT_TO_CLASS[agent]
        agent_kwargs = agent_kwargs or {}
        agent_obj = agent_cls.from_llm_and_tools(
            llm, tools, callback_manager=callback_manager, **agent_kwargs
        )
    elif agent_path is not None:
        agent_obj = load_agent(
            agent_path, llm=llm, tools=tools, callback_manager=callback_manager
        )
        try:
            # TODO: Add tags from the serialized object directly.
            tags_.append(agent_obj._agent_type)
        except NotImplementedError:
            pass
    else:
        raise ValueError(
            "Somehow both `agent` and `agent_path` are None, "
            "this should never happen."
        )
    return ControlledAgentExecutor.from_agent_and_tools(
        agent=agent_obj,
        tools=tools,
        rules=rules,
        callback_manager=callback_manager,
        tags=tags_,
        **kwargs,
    )

