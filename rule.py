from antlr4 import *
import unittest
from enum import Enum
from pydantic import BaseModel 
from spec_lang.AgentSpecListener import AgentSpecListener 
from spec_lang.AgentSpecLexer import AgentSpecLexer
from spec_lang.AgentSpecParser import AgentSpecParser  

class RuleParser(AgentSpecListener): 
    tool:str
    toolkit:str
    
    def enterToolkit(self, ctx: AgentSpecParser.ToolkitContext): 
        if ctx.IDENTIFIER()!=None:
            self.toolkit = ctx.IDENTIFIER().getText()
        else:
            self.toolkit = "any"
    
    def enterTool(self, ctx: AgentSpecParser.ToolContext): 
        if ctx.IDENTIFIER()!=None:
            self.tool = ctx.IDENTIFIER().getText()
        else:
            self.tool = "any"

    def enterRuleClause(self, ctx):
        self.id = ctx.IDENTIFIER(). getText()
            

    def getId(self):
        return self.id

class Rule(BaseModel):
    id: str
    tool: str
    toolkit: str
    raw: str
    
    # TODO- make it a tool
    def triggered(self, action_name): 
        print(action_name)
        return self.tool == "any" or action_name == self.tool
    
    def from_text(rule_str):
        input_stream = InputStream(rule_str)
        lexer = AgentSpecLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = AgentSpecParser(token_stream)

        tree = parser.program()
        walker = ParseTreeWalker()
        parser = RuleParser()
        walker.walk(parser, tree)  

        return Rule(raw=rule_str, tool=parser.tool, toolkit=parser.toolkit, id=parser.getId())
     