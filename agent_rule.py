import logging

logging.basicConfig(level=logging.INFO)

from antlr4 import *
import unittest
from enum import Enum
from global_states import *
from spec_lang.AgentSpecListener import AgentSpecListener 
from spec_lang.AgentSpecLexer import AgentSpecLexer
from spec_lang.AgentSpecParser import AgentSpecParser 
from interpreter import RuleInterpreter 
from enforcement import ENFORCEMENT_TO_CLASS
from pydantic import BaseModel
from context import RuleContext

from langchain.agents.agent import BaseMultiActionAgent, BaseSingleActionAgent
from langchain_core.agents import AgentAction, AgentFinish
from typing import Union, Optional, Any, List, Dict
 

class RuleParser(AgentSpecListener): 
    def enterEvent(self, ctx: AgentSpecParser.EventContext):
        if ctx.ACTION()!=None:
            self.event = ctx.IDENTIFIER().getText()
        else:
            self.event = "any"
            
    def getEvent(self):
        return self.event

class Rule(object):
    name: str
    def __init__(self, rule_str, event) -> None:
        self.name = rule_str 
        self.event = event
        self.interpreter = RuleInterpreter(rule_str) 

    def triggered(self, action_name): 
        return self.event == "any" or action_name == self.event
    
    def from_text(rule_str):
        input_stream = InputStream(rule_str)
        lexer = AgentSpecLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = AgentSpecParser(token_stream)

        tree = parser.program()
        walker = ParseTreeWalker()
        parser = RuleParser()
        walker.walk(parser, tree) 

        return Rule(example_rule, parser.getEvent())
    
    def verify_and_enforce(self, action, ctx: RuleContext) -> Union[AgentFinish, AgentAction]: 
        enforcement = self.interpreter.verify(action, ctx.user_input, ctx.intermediate_steps) 
        return ENFORCEMENT_TO_CLASS[enforcement](ctx=ctx).apply(action)
    