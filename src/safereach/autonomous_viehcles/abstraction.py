
import json
import math
from deepdiff import DeepDiff
from ..abstraction import Abstraction, FINISH
from typing import Any, Set, List, Dict
import networkx as nx
import matplotlib.pyplot as plt


class AVAbstraction(Abstraction):
    def __init__(self, law_str):
        self.law_str = 
