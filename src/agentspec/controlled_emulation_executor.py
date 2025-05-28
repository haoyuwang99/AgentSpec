from toolemu.agents.virtual_agent_executor import StandardVirtualAgentExecutorWithToolkit
from .rule import Rule
from typing import List, Dict, Tuple, Optional, Union
 
from langchain_core.agents import AgentFinish
from toolemu.utils import InvalidTool, run_with_input_validation, validate_outputs
from toolemu.utils.my_typing import SimulatedObservation
from agent import Action
from .interpreter import RuleInterpreter
from .enforcement import EnforceResult
from .state import RuleState

from langchain_core.agents import AgentAction 
from langchain_core.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForChainRun

class ControlledVirtualAgentExecutor(StandardVirtualAgentExecutorWithToolkit):
    rules: List[Rule] = []
    
    def set_rules(self, rules):
        self.rules = self.rules + rules 
    
    def validate_and_enforce(self, action: Action, state: RuleState) -> Tuple[Action, Rule]: 
        if self.rules==None:
            raise ValueError("rules should not be none")
        if action.is_finish():
            return (action, None)
        for rule in self.rules: 
            if rule.triggered(action.name, action.input): 
                print(f"triggered rule {rule.raw}")
                interpreter = RuleInterpreter(rule, state)
                res, action = interpreter.verify_and_enforce(action)
                if res == EnforceResult.CONTINUE:
                    break
                elif res == EnforceResult.SKIP:
                    return (Action.get_skip(), rule)
                elif res == EnforceResult.SELF_REFLECT: 
                    return self.validate_and_enforce(action, state)
                else:
                    raise ValueError("Unreachable")
        return (action, None)
    
    def _take_next_step(self,
                        name_to_tool_map: Dict[str, BaseTool], 
                        color_mapping: Dict[str, str],
                        inputs: Dict[str, str],
                        intermediate_steps: List[Tuple[AgentAction, str]],
                        run_manager: Optional[CallbackManagerForChainRun] = None) -> Union[AgentFinish, List[Tuple[AgentAction, str]]]:
        """Override to use virtual tool execution and custom InvalidTool."""
        # Call the LLM to see what to do.
        output = self.agent.plan(intermediate_steps, **inputs)
        # If the tool chosen is the finishing tool, then we end and return.
        if isinstance(output, AgentFinish):
            return output
        actions: List[AgentAction]
        if isinstance(output, AgentAction):
            actions = [output]
        else:
            actions = output
        result = []
        for agent_action in actions:
            if run_manager:
                run_manager.on_agent_action(
                    agent_action, verbose=self.verbose, color="green"
                )
            # Otherwise we lookup the tool
            if agent_action.tool in name_to_tool_map: 
                # implementation 
                action = Action.from_langchain(agent_action)
                state = RuleState(
                    action = action,
                    agent =self._action_agent,
                    intermediate_steps=intermediate_steps,
                    user_input=inputs
                ) 
                action, rule = self.validate_and_enforce(action, state)
                if action.is_skip():
                    observation_text = f"action is skipped due to the enforcement of {rule.raw}"
                    observation = SimulatedObservation(
                        observation=observation_text,
                        thought_summary="",
                        log=observation_text,
                    )
                    result.append((agent_action, observation))
                    continue
                
                tool = name_to_tool_map[agent_action.tool]
                return_direct = tool.return_direct
                color = color_mapping[agent_action.tool]
                tool_run_kwargs = self.agent.tool_run_logging_kwargs()


                # We then call the llm to simulate the execution of the tool
                empty_observation = ""  # for the current step
                simulator_scratchpad = self._construct_simulator_scratchpad(
                    intermediate_steps + result + [(agent_action, empty_observation)]
                )
                #TODO- add validate and enforce here.
                  
                full_inputs = {
                    "simulator_scratchpad": simulator_scratchpad,
                    "current_tool": agent_action.tool,
                    "current_tool_description": tool.description,
                    "toolkit_descriptions": self._get_current_toolkit_descriptions(
                        agent_action.tool
                    ),
                    **inputs,
                }
                 
                observation = run_with_input_validation(
                    self.llm_simulator_tool.run,
                    full_inputs,
                    tool,
                    agent_action.tool_input,
                    verbose=self.verbose,
                    color=color,
                    **tool_run_kwargs,
                )
                if isinstance(observation, str):
                    observation = SimulatedObservation(
                        observation=observation, thought_summary="", log=observation
                    )
                    
            else:
                tool_run_kwargs = self.agent.tool_run_logging_kwargs()
                observation_text = InvalidTool(available_tools=self.tool_names).run(
                    agent_action.tool,
                    verbose=self.verbose,
                    color=None,
                    **tool_run_kwargs,
                )
                observation = SimulatedObservation(
                    observation=observation_text,
                    thought_summary="",
                    log=observation_text,
                )
            result.append((agent_action, observation))
        if isinstance(result, AgentFinish):
            print(inputs)
            print(intermediate_steps)
        return result