from langchain.agents.agent import AgentExecutor
from typing import Optional
from typing import List

from langchain_core.exceptions import OutputParserException
from langchain_core.agents import AgentAction, AgentFinish, AgentStep
from langchain.agents.agent import ExceptionTool
from agent_rule import *

class ControlledAgentExecutor(AgentExecutor) : 
   rules: Optional[List[Rule]]
   user_input: Optional[str] = None
   
   def invoke(self, user_input, config = None, **kwargs):
       self.user_input = input 
       return super().invoke(user_input, config, **kwargs)


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
         **kwargs,
      ) 
   
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
         if isinstance(output, AgentAction): 
            for rule in self.rules:
               #1. check if the rule is triggered.
               if not rule.triggered(output.tool): 
                  continue
                
               #2. interpret the following prepare/condition/enforce of the rule.
               enforcement = rule.check(output, self.user_input, intermediate_steps)
 

               #3. check the enforcement of the rule:
               #   for USER_INSPECT, we either 1)continue if user authorized or 2) return an empty dict if not
               #   for SELF_REFLECT, we exit the execution to let the agent execute an new option.
               res = enforcement.apply()

               if res == EnforceResult.FINISH:
                     output = AgentFinish({"output": "AA"}, "the action is stopped due to the enforcement of rule")
                     yield output
                     return
               
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

      # If the tool chosen is the finishing tool, then we end and return.
      if isinstance(output, AgentFinish):
         yield output
         return

      actions: List[AgentAction]
      if isinstance(output, AgentAction):
         actions = [output]
      else:
         raise ValueError("not implemented for this type")
         actions = output
      for agent_action in actions:
         yield agent_action
      for agent_action in actions:
         yield self._perform_agent_action(
               name_to_tool_map, color_mapping, agent_action, run_manager
         )