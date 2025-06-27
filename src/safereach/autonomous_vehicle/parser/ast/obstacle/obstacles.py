# The file Obstacles.py defines class representing obtacles
from typing import List, NoReturn,Optional,AnyStr

from parser.ast.base.shape import Shape
from parser.ast.base.state import Variable,Node, NodeType, Position


class Obstacle(Variable,Node):
    def __init__(self,name:AnyStr=''):
        Variable.__init__(self,name)
        Node.__init__(self,NodeType.T_OB)
        self._position=None
        self._shape=None
    def set_shape(self,shape:Shape)->NoReturn:
        self._shape=shape
    def has_shape(self)->bool:
        return self._shape is not None
    def get_shape(self)->Shape:
        assert self.has_shape()
        return self._shape
    def set_position(self,position:Position):
        self._position=position
    def get_position(self)->Position:
        assert self._position is not None
        return self._position
class Obstacles(Variable,Node):
    def __init__(self,name:AnyStr=''):
        Variable.__init__(self,name)
        Node.__init__(self,NodeType.T_OBS)
        self._obstacles:List[Obstacle]=[]
    def add_obstacle(self,obstacle:Obstacle)->NoReturn:
        self._obstacles.append(obstacle)
    def get_size(self)->int:
        return len(self._obstacles)
    def get_obstacles(self)->List[Obstacle]:
        return self._obstacles