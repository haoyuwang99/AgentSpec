from antlr4 import *
import unittest
from typing import List
from enum import Enum
from pydantic import BaseModel 
from spec_lang.AgentSpecListener import AgentSpecListener 
from spec_lang.AgentSpecLexer import AgentSpecLexer
from spec_lang.AgentSpecParser import AgentSpecParser  

class DriveRuleParser(AgentSpecListener): 
   
    predicates: List[str] = []
    enforcements: List[str] = []
    
    def enterCheckClause(self, ctx):
        for pred in ctx.predicate():
            if pred.predicate_func():
                self.predicates.append(pred.predicate_func().getText())
        return super().enterCheckClause(ctx)
    
    def enterEnforceClause(self, ctx):
        for enf in ctx.enforcement():
            if enf.config():
                self.enforcements.append(enf.config().getText())
        return super().enterEnforceClause(ctx)
            

def translate(str):
    
    input_stream = InputStream(str)
    lexer = AgentSpecLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = AgentSpecParser(token_stream)
    tree = parser.program()
    walker = ParseTreeWalker()
    
    drive_parser = DriveRuleParser()
    walker.walk(drive_parser, tree)
    
    preds = drive_parser.predicates
    preds_str = '&'.join(preds)
    enfs = drive_parser.enforcements
    enfs_str = '\n    '.join(enfs)
    
    return f"""
[{preds_str}] {{
    {enfs_str}
}}
""" 

print(translate("""
rule @s1_1
trigger
    state_change
check 
    v_f_disL(10)
enforce 
    real:obstacle:Dynamic_Obstacle_Follow_distance=10
    real:obstacle:Dynamic_Obstacle_Yield_distance=15
    real:obstacle:Dynamic_Obstacle_Overtake_distance=20
    real:obstacle:Min_stop_distance=10
    real:obstacle:Dynamic_Obstacle_Deceleration_ratio=1.0
end
"""))