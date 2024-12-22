from antlr4 import *
import unittest
from enum import Enum
from pydantic import BaseModel
from global_states import *
from spec_lang.AgentSpecListener import AgentSpecListener 
from spec_lang.AgentSpecLexer import AgentSpecLexer
from spec_lang.AgentSpecParser import AgentSpecParser  

class RuleParser(AgentSpecListener): 
    def enterEvent(self, ctx: AgentSpecParser.EventContext):
        if ctx.ACTION()!=None:
            self.event = ctx.IDENTIFIER().getText()
        else:
            self.event = "any"

    def enterRuleClause(self, ctx):
        self.id = ctx.IDENTIFIER(). getText()
            
    def getEvent(self):
        return self.event

    def getId(self):
        return self.id

class Rule(BaseModel):
    id: str
    event: str
    raw: str
    
    def triggered(self, action_name): 
        print(action_name)
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

        return Rule(raw=example_rule, event=parser.getEvent(), id=parser.getId())
     