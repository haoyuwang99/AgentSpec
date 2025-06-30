
import json
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
        print(pre_str)
        print(op)
        lhs = pre_str[1:pre_str.find(op)-1]
        rhs = pre_str[pre_str.find(op)+len(op)+1:-1]
        self.predicates.append((lhs, op, rhs))
        # super().visit_predicate( node, args, kwargs)
    
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

    def encode(self, observations):
        if observations == FINISH:
            return FINISH
        
        # for predicate in self.predicates:
        
            
        
        return super().encode(observations)
    
    def decode(self, state):
        if state== FINISH:
            return FINISH
        return super().decode(state)

