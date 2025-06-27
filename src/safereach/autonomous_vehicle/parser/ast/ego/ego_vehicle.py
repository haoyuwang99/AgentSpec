# The file EgoVehicle.py defines class representing an ego vehicle
from typing import Optional,AnyStr
from parser.ast.base.state import Node, Variable,State,NodeType
from parser.ast.base.vehicle_type import VehicleType
class EgoVehicle(Variable,Node):
    def __init__(self,name:AnyStr=''):
        Variable.__init__(self,name)
        Node.__init__(self,NodeType.T_EGO)
        self._first=None
        self._second=None
        self._type=None
    def set_first_state(self,firstState:State,):
        self._first=firstState
    def set_second_state(self,secondState:State):
        self._second=secondState
    def set_vehicle_type(self,type_:VehicleType):
        self._type=type_
    def has_vehicle_type(self)->bool:
        return self._type is not None
    def get_vehicle_type(self):
        assert self.has_vehicle_type()
        return self._type
    def get_first_state(self)->State:
        assert self._first is not None
        return self._first
    def get_second_state(self)->State:
        assert self._second is not None
        return self._second