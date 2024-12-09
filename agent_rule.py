from antlr4 import *
import unittest
from enum import Enum
from global_states import *
from spec_lang.AgentSpecListener import AgentSpecListener 
from spec_lang.AgentSpecLexer import AgentSpecLexer
from spec_lang.AgentSpecParser import AgentSpecParser 
from interpreter import RuleInterpreter 
from enforcement import Enforcement

class RuleParser(AgentSpecListener): 
    def enterEvent(self, ctx: AgentSpecParser.EventContext):
        if ctx.ACTION()!=None:
            self.event = ctx.IDENTIFIER().getText()
        else:
            self.event = "any"

    def getEvent(self):
        return self.event

class Rule(object):
    def __init__(self, rule_str, event) -> None:
        self.rule_str = rule_str 
        self.event = event
        self.interpreter = RuleInterpreter(rule_str)
        print(event)

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
        
    def check(self, action, input, traj):
        enforcement = self.interpreter.interpret(action, input, traj) 
        return Enforcement(enforcement)
     