
import json
import itertools
import operator
import math
from deepdiff import DeepDiff
from ..abstraction import Abstraction, FINISH
from typing import Any, Set, List, Dict
import networkx as nx
import matplotlib.pyplot as plt
import rtamt

from rtamt.syntax.node.ltl.predicate import Predicate
# from rtamt.syntax.node.ltl.binary_node import BinaryNode
from rtamt.syntax.ast.visitor.stl.ast_visitor import StlAstVisitor

        
def prepare_for_rule38_1():              
    #GREEN = 3; 
    traffic_rule = '(\
                            always( (   (   (trafficLightAheadcolor == 3) and \
                                            (PriorityNPCAhead == 0) and (PriorityPedsAhead == 0)    ) \
                                implies (eventually[0,100](speed > 0.5)) ) \
                            )\
                    )'
    return traffic_rule

def prepare_for_rule38_2():              
    #YELLOW = 2;
    traffic_rule = '(\
                            always(\
                                    ( \
                                        (\
                                            (trafficLightAheadcolor == 2) and ((currentLanenumber == 0))\
                                        ) implies ( eventually[0,100](speed > 0.5) )\
                                    ) and \
                                    ( \
                                        (\
                                            (trafficLightAheadcolor == 2) and ((currentLanenumber > 0))\
                                        ) implies ( eventually[0,100](speed < 0.5) )\
                                    ) \
                            ) \
                        )'
    return traffic_rule

def prepare_for_rule38_3():              
    #RED = 1;   
    traffic_rule = '(\
                            always((((trafficLightAheadcolor == 1) and \
                                ((stoplineAhead <= 2) or (junctionAhead <= 2)) and\
                                (currentLanenumber > 0) and \
                                (direction <= 1)) \
                                implies ( eventually[0,100](speed < 0.5) )) and \
                                (((trafficLightAheadcolor == 1) and \
                                ((stoplineAhead <= 2) or (junctionAhead <= 2)) and \
                                (direction == 2) and (PriorityNPCAhead == 0) and \
                                (currentLanenumber > 0) and \
                                (PriorityPedsAhead == 0) ) \
                                implies ( eventually[0,100](speed > 0.5) )) ) \
                            )'
    return traffic_rule

def prepare_for_rule38():              
    # message TrafficLight {
    #   enum Color {
    #     UNKNOWN = 0;
    #     RED = 1;
    #     YELLOW = 2;
    #     GREEN = 3;
    #     BLACK = 4;
    #   };       
    # we should put different weight on different variables!
    traffic_rule = '(always(((trafficLightAheadcolor == 3) and ((stoplineAhead <= 2) or (junctionAhead <= 2)) and (PriorityNPCAhead == 0) and (PriorityPedsAhead == 0)) implies ( speed >= 0.1 ))   and \
                            always((((trafficLightAheadcolor == 2) and ((stoplineAhead == 0) or (stoplineAhead > 50))) implies ( speed > 0.1 )) and \
                                    (((trafficLightAheadcolor == 2) and (stoplineAhead <= 2)) implies (speed < 0.1)) ) and \
                            always((((trafficLightAheadcolor == 1) and ((stoplineAhead <= 2) or (junctionAhead <= 2)) and (direction <= 1)) implies ( speed < 0.1 )) and \
                                    (((trafficLightAheadcolor == 1) and ((stoplineAhead <= 2) or (junctionAhead <= 2)) and (direction == 2) and (PriorityNPCAhead == 0) and (PriorityPedsAhead == 0) ) implies ( speed >= 0.1 )) ) \
                            )'
    return traffic_rule

def prepare_for_rule42():
    # \begin{aligned}
    #     & G(((trafficLightAhead.color = yellow \land \\
    #     & trafficLightAhead.blink) \lor \\
    #     & (trafficLightAhead.direction.color = yellow \land \\
    #     & trafficLightAhead.direction.blink)) \land \\
    #     & ( stoplineAhead(realvalue) \lor junctionAhead(realvalue) )\\
    #     & \implies    speed < realvalue )
    # \end{aligned}          
    traffic_rule = '(always(((trafficLightAheadcolor == 2) and \
                            (trafficLightAheadblink == 1) and \
                            ((stoplineAhead <= 1) or (junctionAhead <= 1)))\
                            implies (speed < 5))\
                            )'
    return traffic_rule

def prepare_for_rule44():
    # \begin{aligned}
    #     & G(currentLane.number \geq 2  \implies \\
    #     & (speed \geq speedLimit.lowerLimit \land  \\
    #     & speed \leq speedLimit.upperLimit)) \land \\
    #     & G(isLaneChanging \land   currentLane.number \geq 2 \\
    #     & \implies  \lnot PriorityNPCAhead)
    # \end{aligned}          
    traffic_rule = '(   always( (currentLanenumber >= 201) \
                                implies ((eventually[0,6000](currentLanenumber >= 201 implies speed >= 20)) and (speed <= speedLimitupperLimit))))'
    return traffic_rule

def prepare_for_rule45():
    # \begin{aligned}
    #     & G(speed \geq speedLimit.lowerLimit  \land \\
    #     & speed \leq speedLimit.upperLimit )
    # \end{aligned}    
    traffic_rule = '(always((speed >= speedLimitlowerLimit) and (speed <= speedLimitupperLimit)))'
    return traffic_rule

def prepare_for_rule46_2():
    # \begin{aligned}
    #     & G( (direction \neq forward) \lor isTurningAround) \\
    #     & \implies   speed \leq 30 )
    # \end{aligned}
    traffic_rule = '(always(((direction == 1) or (direction == 2) or (isTurningAround == 1))\
                            implies (speed <= 30)))'
    return traffic_rule

def prepare_for_rule46_3():
    # \begin{aligned}
    #     & G((Weather.rain \geq 0.5 \lor Weather.fog \geq 0.5 \\
    #     & \lor  Weather.snow \geq 0.5) \land Weather.visibility \leq 50 \\
    #     & \implies speed \leq 30)
    # \end{aligned}
    traffic_rule = '(always(((rain >= 0.5) or (fog >= 0.5) or (snow >= 0.5))\
                            implies (speed <= 30)))'

    return traffic_rule

def prepare_for_rule47():
    # $$
    # \begin{aligned}
        # & G(isOverTaking \implies  turnSignal = left \land \\
        # & (F[-realvalue,\ realvalue](hornOn) \lor \\
        # & ( highBeamOn \land (highBeamOn \\
        # & \implies   F[0,\ realvalue](lowBeamOn) )) \lor \\
        # & ( lowBeamOn \land (lowBeamOn \\
        # & \implies   F[0,\ realvalue](highBeamOn) )))  \land  \\
        # & F[0,\ realvalue]( (turnSignal = right \land \\
        # & isLaneChanging \implies NearestNPC(realvalue) \\
        # & \land isLaneChanging) )
    # \end{aligned}
    # $$
    traffic_rule = '(always((isOverTaking == 1)\
                            implies ( (turnSignal == 1) and \
                                ((eventually[-1, 2](hornOn == 1)) or \
                                    ( \
                                    ((highBeamOn == 1 ) and \
                                        ((highBeamOn == 1) implies (eventually[0, 2](lowBeamOn == 1))) ) or \
                                    ((lowBeamOn == 1 ) and \
                                        ((lowBeamOn == 1) implies (eventually[0, 2](highBeamOn == 1))) ) \
                                    )\
                                ) and \
                                F[0, 10]( (turnSignal == 2) and \
                                    (((isLaneChanging == 1) implies (NearestNPCAhead >= 5)) and (isLaneChanging == 1) ) ) ))\
                    )'

    return traffic_rule

def prepare_for_rule50():
    # \begin{aligned}
    #     & G(speed \geq speedLimit.lowerLimit  \land \\
    #     & speed \leq speedLimit.upperLimit )
    # \end{aligned}    
    traffic_rule = '(always ((not (gear==2))))'
    return traffic_rule

def prepare_for_rule51_3():
    traffic_rule = "(always ((((((((trafficLightAheadcolor==3) and (direction==1)) and (Time<=20.0)) and (Time>=7.0))) -> ((turnSignal==1))) and (((((trafficLightAheadcolor==3) and (direction==1)) and (((Time>=20.0) or (Time<=7.0))))) -> (((turnSignal==1) and (lowBeamOn==1)))))))"
    return traffic_rule

def prepare_for_rule51_4():
    traffic_rule = "(always ((((trafficLightAheadcolor==3) and (((not (NPCAheadAhead<=8.0)) or (((((NPCAheadAhead<=8.0) -> (eventually[0,2] ((NPCAheadspeed>0.5))))) and (NPCAheadAhead<=8.0)))))) -> (((eventually[0,3] ((speed>0.5)))) and (not (NPCAheadAhead<=0.5))))))"
    return traffic_rule

def prepare_for_rule51_5():
    traffic_rule = "(always ((((trafficLightAheadcolor==1) and ((((stoplineAhead<=2.0) or (junctionAhead<=2.0)) or (NPCAheadAhead<=0.5)))) -> (eventually[0,2] ((speed<0.5))))))"
    return traffic_rule

def prepare_for_rule51_6():
    traffic_rule = "(always ((((((direction==2) and (NPCAheadAhead<=2.0)) and ((eventually[0,2] ((NPCAheadspeed<0.5)))))) -> (eventually[0,3] ((speed<0.5))))))"
    return traffic_rule

def prepare_for_rule51_7():
    traffic_rule = "(always (((((((direction==2) or (direction==1))) and (((PriorityNPCAhead==1) or (PriorityPedsAhead==1))))) -> (eventually[0,2] ((speed<0.5))))))"
    return traffic_rule

def prepare_for_rule52():
    traffic_rule = "(\
                    always (\
                                ((signalAhead==0 and (NPCAheadAhead<=1)) and junctionAhead<=1.0) \
                                -> (eventually[0,300] (speed<0.5))\
                            ) \
                    )"
    # traffic_rule = "(always (((((signalAhead==0 and ((NPCAheadAhead<=1 or PriorityPedsAhead<=1))) and junctionAhead<=1.0)) -> (eventually[0,200] (speed<0.5)))))"
    return traffic_rule

def prepare_for_rule53():
    traffic_rule = "(always ((((isTrafficJam==1 and (((NPCAheadspeed<0.5 or NPCAheadAhead<=0.5) or junctionAhead<=1.0)))) -> (eventually[0,200] (speed<0.5)))))"
    return traffic_rule


class PredicateCollector(StlAstVisitor):
    def __init__(self):
        self.predicates = []

        
    def visit(self, node, *args, **kwargs):
        if isinstance(node, Predicate):
            self.visit_predicate(node, args, kwargs)
        else:
            super().visit(node, *args, **kwargs)
        
    def visit_predicate(self, node, *args, **kwargs):
        op = str(node.operator)
        pre_str = node.name 
        lhs = pre_str[1:pre_str.find(op)-1]
        rhs = pre_str[pre_str.find(op)+len(op)+1:-1]
        self.predicates.append((lhs, op, rhs))
        # super().visit_predicate( node, args, kwargs)
    

traffic_rules = {
    "rule38_1" : prepare_for_rule38_1(),
    "rule38_2" : prepare_for_rule38_2(),
    "rule38_3" : prepare_for_rule38_3(),
    "rule42" : prepare_for_rule42(),
    # "rule45" : prepare_for_rule45(),
    "rule46_2" : prepare_for_rule46_2(),
    "rule46_3" : prepare_for_rule46_3(),
    "rule50" : prepare_for_rule50(),
    "rule51_4" : prepare_for_rule51_4(),
    "rule51_5" : prepare_for_rule51_5(),
    "rule51_6" : prepare_for_rule51_6(),
    "rule51_7" : prepare_for_rule51_7(),
    "rule52" : prepare_for_rule52(),
    "rule53" : prepare_for_rule53(),

}

VARIABLE_APIS = ['gear', 'engineOn', 'direction', 'manualIntervention', \
    'speed', 'acc', 'brake', 'isLaneChanging', 'isOverTaking',\
    'isTurningAround', 'currentLanenumber', 'currentLanedirection', \
    'speedLimitlowerLimit', 'speedLimitupperLimit', 'honkingAllowed',\
    'crosswalkAhead', 'junctionAhead', 'stopSignAhead', 'signalAhead',\
    'stoplineAhead', 'streetLightOn', 'specialLocationAheadlocation', \
    'specialLocationAheadtype', 'trafficLightAheadcolor', 'trafficLightAheadblink', \
    'PriorityNPCAhead', 'PriorityPedsAhead', 'isTrafficJam', 'NPCAheadAhead', 'NPCAheadspeed',\
    'NearestNPCAhead', 'NearestNPCspeed', 'NPCOppositeAhead', 'NPCOppositespeed', 'rain', 'snow',\
    'fog', 'trafficLightAheadArrowDirectioncolor', 'trafficLightAheadArrowDirectionblink', 'visibility']
    
    
REACH_PREDICATE = ("reach_destination", "==", '1')
COLLISION_PREDICATE = ("collision", "==", "1")

STR_TO_BINOP = {
    "==": operator.eq,
    ">=": operator.ge,
    "<=": operator.le,
    ">": operator.gt,
    "<": operator.lt
}

#predicate is a tuple (lhs, op, rhs)
def eval_pred(observation, predicate):
    lvalue = eval_expr(observation, predicate[0])
    op = predicate[1]
    rvalue = eval_expr(observation, predicate[2])
    return eval_bin_op(lvalue, op, rvalue)

def eval_expr(observation, expr):
    # print(observation)
    try:
        float(expr)
        return float(expr)
    except ValueError:
        # print(observation.keys())
        return float(observation[expr])


def eval_bin_op(lvalue, op, rvalue):
    if not op in STR_TO_BINOP.keys():
        print("currently unsupported bin op")
    if type(lvalue) != float or type(rvalue) != float:
        raise Exception("Expected lvalue and rvalue to be float")
    binop = STR_TO_BINOP[op]
    return binop(lvalue, rvalue)    

        
class AVAbstraction(Abstraction):
    
    #law_str example:
    # '(  always( (   (   (trafficLightAheadcolor == 3) and \
    #     (PriorityNPCAhead == 0) and (PriorityPedsAhead == 0)    ) \
    #     implies (eventually[0,100](speed > 0.5)) ) \
    #   )\
    #  )'
    def __init__(self, law_str):
        self.law_str = law_str
        

        spec = rtamt.StlDenseTimeSpecification(semantics=rtamt.Semantics.STANDARD)

        for item in VARIABLE_APIS:
            spec.declare_var(item, 'float')
        spec.spec = law_str
        spec.parse()
        
        ast = spec.ast.specs[0]

        collector = PredicateCollector()
        collector.visit(ast)
        self.predicates = collector.predicates
        
        self.predicates = sorted(self.predicates)
        
        self.state_space=sorted(list(self.enumerate_possible_states()))
        self.state_idx = None
        self.state_interpretation = None

    def encode(self, observation):
        bitstr = ""
        collision = eval_pred(observation, COLLISION_PREDICATE)
        reach = eval_pred(observation, REACH_PREDICATE)
        # if already reach or collision, then we do not care about other variables.
        if collision or reach:
            bitstr = "0" * len(self.predicates)
            bitstr = bitstr + "1" if reach else bitstr + "0"
            bitstr = bitstr + "1" if collision else bitstr + "0"
            return bitstr
            

        for predicate in self.predicates: 
            pvalue = eval_pred(observation, predicate)
            bitstr = bitstr + "1" if pvalue else bitstr + "0"
        bitstr = bitstr + "00"
        
        if not bitstr in self.state_space:
            raise Exception("unvalid state")
            
        return bitstr
    
    def decode(self, state):
        observation = {}
        for i in range(len(self.predicates)):
            cur_bit = state[i]
            predicate = self.predicates[i]
            var_name = predicate[0]
            op = predicate[1]
            # currently only support float value as rhs
            rvalue = float(predicate[2])
            if op == "==":
                observation[var_name] = rvalue if cur_bit=='1' else rvalue + 1
            elif op == ">=" or op == ">":
                observation[var_name] = rvalue + 1 if cur_bit=='1' else rvalue - 1 
            elif op == '<='or op == "<":
                observation[var_name] = rvalue - 1 if cur_bit=='1' else rvalue + 1
            else: 
                raise Exception(f"unsupported bin op {op}")
        observation["reach_destination"] = float(state[len(self.predicates)])
        observation["collision"] = float(state[len(self.predicates)+1])
                
        return observation

    def enumerate_possible_states(self) -> Set[str]: 
        enums = [''.join(bits) + "00" for bits in itertools.product('01', repeat=len(self.predicates))]
        enums.append("0" * len(self.predicates) + "00")
        enums.append("0" * len(self.predicates) + "10")
        enums.append("0" * len(self.predicates) + "01")
        return set(enums)
        # for a in self.predicates:

    # last two bits: reach then collision
    def can_reach(self, state1: str, state2: str) -> bool:
        if (state1.endswith("10") or state1.endswith("01") or state1.endswith("01")) and state2.endswith("00"):
            return False
        # we do not consider the crashes after reaching destination
        if state1.endswith("10") and state2.endswith("01"):
            return False
        return True

    #currently, we only support collision and finish journey
    def filter(self, specs) -> Set[str]:
        pass

    def get_state_idx(self) -> Dict[str, int]:  
        if self.state_idx == None:
            self.state_idx = {s:i for i, s in enumerate(self.state_space)}
        return self.state_idx


    def get_state_interpretation(self) -> Dict[str, Any]:
        if self.state_interpretation == None:
            self.state_interpretation = {s: list(zip([f"{p[0]} {p[1]} {p[2]}" for p in self.predicates],\
                [ True if bit == '1' else False for bit in s])) for s in self.state_space}
            print(self.state_interpretation)
        return self.state_interpretation
    
    def to_json(self) -> str:
        obj = {
            "predicates":  self.predicates,
            "reach" : REACH_PREDICATE, 
            "collision": COLLISION_PREDICATE 
        }
        return json.dumps(obj)
    
