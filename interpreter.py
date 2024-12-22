from antlr4 import *
from global_states import *
from evaluator import *
import unittest
from spec_lang.AgentSpecListener import AgentSpecListener 
from spec_lang.AgentSpecLexer import AgentSpecLexer
from spec_lang.AgentSpecParser import AgentSpecParser  
from antlr4.error.ErrorListener import ErrorListener
from rules.Command import Command
from state import RuleState
from enforcement import *
from rule import Rule

from langchain_core.agents import AgentAction, AgentFinish

class CustomErrorListener(ErrorListener): 
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        error_message = f"Syntax error at line {line}, column {column}: {msg}"
        raise ValueError(error_message)
 
class RuleInterpreter(AgentSpecListener):
    
    def __init__(self, rule: Rule, rule_state: RuleState) -> None:
        super().__init__() 
        self.rule  = rule
        self.check = True
        self.rule_state = rule_state
        # table for indexing the value/predicate 
        self.cond_eval_history = {}  # "ID" -> {"val": true/false, "rationale": "why this condition is evaluated as false/true"}
        
    def parse_action(self, ctx: AgentSpecParser.ActionInvokeContext):
        name = ctx.IDENTIFIER()
        arg_dict = {}
        kvs = ctx.kvPair()
        for kv in kvs: 
            arg_dict[self.eval_str(kv.STRING())] = self.eval_value(kv.value())    
        return {"name":name, "args": arg_dict}

    def eval_predicate(self, ctx: AgentSpecParser.PredicateContext) -> bool: 
        cond_str = ctx.getText()
        if ctx.TRUE() !=None: #for testing 
            self.cond_eval_history[ctx.getText()] ={"val": True, "rationale": f"JUST TRUE, WHAT CAN I SAY? :-)"} 
            return True
        elif ctx.FALSE() !=None: #for testing
            self.cond_eval_history[ctx.getText()] ={"val": False, "rationale": f"JUST TRUE, WHAT CAN I SAY? :-)"}
            return False
        elif ctx.NOT() !=None:
            if ctx.predicate().NOT()!=None:
                res = self.eval_predicate(ctx.predicate())
            else :
                res = not self.eval_predicate(ctx.predicate())
                if res == False:
                    self.cond_eval_history[ctx.getText()] ={"val": res, "rationale": f"the following condition is not satisfied: {res[ctx.condition().getText()]}"}
            return res
        elif ctx.CMD_PREDICATE() != None: 
            # cmd = Command()
            return True
        else:
            values = []
            for val_ctx in ctx.value() :
                values.append(self.eval_value(val_ctx)) 
            op = ctx.EVAL_OP().getText()
            evaluator = EVALUATOR_TO_INSTANCE[op]
            
            res =  evaluator.evaluate(cond_str,values)
            self.cond_eval_history[cond_str] = res
            return res
  
    def eval_action_invoke(self, ctx: AgentSpecParser.ActionInvokeContext):
        action = self.parse_action(ctx)
        # TODO: indexing tools, then call
        # tool = Tool(action["name"], action["args"]) 
        # tool.invoke()
        return {
            "traffic_id": "vehicle-east-west",
            "traffic_light_state": "green"
        }
    
    def eval_val_id(self, id: str):
        if not id in self.state_dict:
            raise ValueError(f"> {id}\n error: undefined value {id}")
        return self.state_dict[id]

    def eval_number(self, num: AgentSpecParser.NumberContext):
        if num.INTEGER() != None:
            return int(num.INTEGER())
        elif num.FLOAT() != None:
            return float(num.FLOAT())
        raise ValueError("unsupported type")
    
    def eval_str(self, value: AgentSpecParser.ValueContext):
        return value.getText()[1:-1]

    def eval_value(self, value: AgentSpecParser.ValueContext):  
        if value.STRING() != None and value.value() == None: # distinguish from STRING and value [STRING]
            return self.eval_str(value.STRING())
        elif value.number() != None:
            return self.eval_number(value.number()) 
        elif value.IDENTIFIER() !=None :
            return self.eval_val_id(str(value.IDENTIFIER()))
        elif value.actionInvoke() !=None :
            return self.eval_action_invoke(value.actionInvoke())
        elif value.value() != None and value.STRING()!=None:
            val = self.eval_value(value.value())
            key = self.eval_str(value.STRING())
            if not type(val) == dict:
                raise ValueError(f"> {value.getText()}\n    error: {value.value().getText()} is not a dict")
            if not key in val:
                raise ValueError(f"> {value.getText()}\n    error: {key} is not a key in {value.value().getText()}")
            return val[key] 
        raise ValueError(f"unsupported value type {value.getText()}")
    
    def enterPrepare(self, ctx: AgentSpecParser.PrepareContext): 
        self.state_dict[ctx.IDENTIFIER().getText()] = self.eval_value(ctx.value())

    def enterCheckClause(self, ctx: AgentSpecParser.CheckClauseContext):
        for cond in ctx.predicate(): 
            self.check = self.check and self.eval_predicate(cond) 
    
    def enterEnforcement(self, ctx: AgentSpecParser.EnforcementContext):
        if self.check: 
            self.enforce = ctx.getText()
        else : 
            self.enforce = "none" 
    
     
    def verify_and_enforce(self, action: AgentAction, state: RuleState) -> Union[AgentFinish, AgentAction]:  
        print(action) 
        
        self.state_dict = {
            "cur_act": action.tool_input,
            "cur_prompt": state.user_input,
            "history_trajectory": state.intermediate_steps
        }  

        input_stream = InputStream(self.rule.raw)
        lexer = AgentSpecLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = AgentSpecParser(token_stream)
        parser.removeErrorListeners()  # Remove default ConsoleErrorListener
        parser.addErrorListener(CustomErrorListener())

        # Parse the input using the top-level rule (e.g., program)
        tree = parser.program() 
        walker = ParseTreeWalker()
        
        walker.walk(self, tree)   
        return ENFORCEMENT_TO_CLASS[self.enforce](state=state).apply(action)
    
    
class TestRuleInterpreter(unittest.TestCase):
    def test_check(self):
        cur_action = {
            "name" : "ControlTrafficLight",
            "intersection_id": 123,
            "traffic_id": "pedestrain-north-west",
            "traffic_light_state" : "walk"
        }
        cur_prompt = "This is a test"
        history_trajectory = [] 
        rule = Rule.from_text(example_rule)
        rule_interpreter = RuleInterpreter(rule, None)
        rule_interpreter.verify(cur_action, cur_prompt, history_trajectory)

if __name__ == "__main__":
    unittest.main()
