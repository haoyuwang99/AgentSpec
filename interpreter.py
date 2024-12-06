from antlr4 import *
import unittest
from spec_lang.AgentSpecListener import AgentSpecListener 
from spec_lang.AgentSpecLexer import AgentSpecLexer
from spec_lang.AgentSpecParser import AgentSpecParser 

class RuleInterpreter(AgentSpecListener):
    
    def __init__(self, rule_str ) -> None:
        super().__init__() 
        self.rule_str = rule_str
        self.check = False
    
    def enforce(self, ctx: AgentSpecParser.EnforcementContext):
        return  

    def parse_action(self, ctx: AgentSpecParser.ActionInvokeContext):
        name = ctx.IDENTIFIER()
        arg_dict = {}
        kvs = ctx.kvPair()
        for kv in kvs: 
            arg_dict[self.eval_str(kv.STRING())] = self.eval_value(kv.value())    
        return {"name":name, "args": arg_dict}

    def eval_condition(self, ctx: AgentSpecParser.ConditionContext) -> bool:
        arg0 = self.eval_value(ctx.value(0))
        arg1 = self.eval_value(ctx.value(1))
        op = ctx.EVAL_OP().getText()
        if op == "eq":
            return arg0 == arg1
        elif op == "lt":
            return arg0 < arg1
        elif op == "gt":
            return arg0 > arg1  
        elif op == "leq":
            return arg0 <= arg1
        elif op == "geq":
            return arg0 >= arg1 
        elif op == "llm_judge":
            #TODO: input: arg0 could be any value, 
            #             arg1: a string discribing the requirement.
            #      ouput: whether the requirement being satisfied. 
            return True
        elif op == "llm_emu":
            #TODO: input: arg0: max risky score, return true if the score is less than arg0. let's say risk score (0-5)
            #             arg1: evaluation metric descrition which map from emulation result to risky score.
            return True
        else:
            raise ValueError(f"unreachable: {op}") 
  
    def eval_action_invoke(self, ctx: AgentSpecParser.ActionInvokeContext):
        action=  self.parse_action(ctx)
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

    def enterCondition(self, ctx: AgentSpecParser.ConditionContext):
        print(self.state_dict)
        self.check = self.eval_condition(ctx)
        return super().enterCondition(ctx)
    
    def enterEnforcement(self, ctx: AgentSpecParser.EnforcementContext):
        if self.check:
            print("enforce")
            self.enforce(ctx) 

    def interpret(self, cur_action, cur_prompt, history_trajectory): 
            
        self.state_dict = {
            "cur_act" : cur_action,
            "cur_prompt" : cur_prompt,
            "history_trajectory": history_trajectory
        }  

        input_stream = InputStream(self.rule_str)
        lexer = AgentSpecLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = AgentSpecParser(token_stream)

        # Parse the input using the top-level rule (e.g., program)
        tree = parser.program() 
        walker = ParseTreeWalker()
        
        # TODO: error handling
        walker.walk(self, tree) 
        return
 
class TestRuleInterpreter(unittest.TestCase):
    def test_interpret(self):
        cur_action = {
            "name" : "ControlTrafficLight",
            "intersection_id": 123,
            "traffic_id": "pedestrain-north-west",
            "traffic_light_state" : "walk"
        }
        cur_prompt = "This is a test"
        history_trajectory = [] 
        rule = """rule @conflict_traffic_light_status
trigger 
    act ManageTrafficLightsStates
prepare  
    val light_states = invoke_action(CheckTrafficLightsStates, {"intersection_id":cur_act["intersection_id"]})
check 
    eq(light_states["traffic_id"],"vehicle-east-west")
    eq(light_states["traffic_light_state"], "green") 
    eq(cur_act["traffic_id"], "pedestrain-north-west")
    eq(cur_act["traffic_light_state"], "walk")
enforce
    llm_self_reflect
end
""" 
        rule_interpreter = RuleInterpreter(rule)
        rule_interpreter.interpret(cur_action, cur_prompt, history_trajectory)

if __name__ == "__main__":
    unittest.main()
