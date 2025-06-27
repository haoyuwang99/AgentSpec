# The file Pedestrians.py defines class representing pedestrians
from parser.ast.base.state import Node, NodeType, Variable,State
from parser.ast.base.motion import PedestrianMotion
from parser.ast.base.pedestrian_type import PedestrianType
from typing import Optional,AnyStr,List,NoReturn
class Pedestrian(Variable,Node):
    def __init__(self,name:AnyStr=''):
        Variable.__init__(self,name)
        Node.__init__(self,NodeType.T_PED)
        self._first=None
        self._motion=None
        self._second=None
        self._type=None
    def set_first_state(self,first:State):
        self._first=first
    def set_second_state(self,second:State):
        self._second=second
    def set_pedestrian_motion(self,motion:PedestrianMotion):
        self._motion=motion
    def set_vehicle_type(self,type_:PedestrianType):
        self._type=type_
    def has_second_state(self)->bool:
        return self._second is not None
    def has_pedestrian_motion(self)->bool:
        return self._motion is not None
    def has_pedestrian_type(self)->bool:
        return self._type is not None
    def get_first_state(self)->State:
        assert self._first is not None
        return self._first
    def get_second_state(self)->State:
        assert self.has_second_state()
        return self._second
    def get_pedestrian_motion(self)->PedestrianMotion:
        assert self.has_pedestrian_motion()
        return self._motion
    def get_pedestrian_type(self)->PedestrianType:
        assert self.has_pedestrian_type()
        return self._type
class Pedestrians(Variable,Node):
    def __init__(self,name:AnyStr=''):
        super().__init__(name)
        Node.__init__(self,NodeType.T_PEDS)
        self._pedestrians:List[Pedestrian]=[]
    def add_pedestrian(self,pedestrian:Pedestrian)->NoReturn:
        self._pedestrians.append(pedestrian)
    def get_size(self)->int:
        return len(self._pedestrians)
    def get_pedestrians(self)->List[Pedestrian]:
        return self._pedestrians
