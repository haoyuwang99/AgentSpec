
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
         
class AVAbstraction(Abstraction):
    def __init__(self, law_str):
        self.law_str = law_str
        

        spec = rtamt.StlDenseTimeSpecification(semantics=rtamt.Semantics.STANDARD)

        for item in monitor.item_names_of_variable_of_APIS:
            # print(item)
            spec.declare_var(item, 'float')
        spec.spec = monitor.muti_traffic_rules[key]
        spec.parse()
        
        # print(type(spec))
        ast = spec.ast.specs[0]
        # print(type(ast))
        collector.visit(ast)
        print(collector.predicates)



