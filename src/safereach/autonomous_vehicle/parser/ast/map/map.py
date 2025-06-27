# this file Map.py defines the map
from parser.ast.base.state import Variable,NodeType,Node
from typing import Optional, AnyStr


class Map(Variable,Node):
    def __init__(self, map_name: AnyStr, name: AnyStr=''):
        Variable.__init__(self,name)
        Node.__init__(self,NodeType.T_MAP)
        self._map: AnyStr = map_name

    def get_map_name(self) -> AnyStr:
        return self._map
