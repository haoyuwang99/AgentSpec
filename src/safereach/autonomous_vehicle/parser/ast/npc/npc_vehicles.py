# The file NPCVehicles.py defines class representing npc vehicles
from parser.ast.base.state import Variable,State,Node,NodeType
from parser.ast.base.motion import VehicleMotion
from parser.ast.base.vehicle_type import VehicleType
from typing import NoReturn, Optional,AnyStr,List
class NPCVehicle(Variable,Node):
    def __init__(self,name:AnyStr=''):
        Variable.__init__(self,name)
        Node.__init__(self,NodeType.T_NPC)
        self._first=None
        self._motion=None
        self._second=None
        self._type=None
    def set_first_state(self,first:State)->NoReturn:
        self._first=first
    def set_second_state(self,second:State)->NoReturn:
        self._second=second
    def set_vehicle_motion(self,motion:VehicleMotion)->NoReturn:
        self._motion=motion
    def set_vehicle_type(self,type_:VehicleType)->NoReturn:
        self._type=type_
    def has_second_state(self)->bool:
        return self._second is not None
    def has_vehicle_motion(self)->bool:
        return self._motion is not None
    def has_vehicle_type(self)->bool:
        return self._type is not None
    def get_first_state(self)->State:
        assert self._first is not None
        return self._first
    def get_second_state(self)->State:
        assert self.has_second_state()
        return self._second
    def get_vehicle_motion(self)->VehicleMotion:
        assert self.has_vehicle_motion()
        return self._motion
    def get_vehicle_type(self)->VehicleType:
        assert self.has_vehicle_type()
        return self._type
class NPCVehicles(Variable,Node):
    def __init__(self,name:AnyStr=''):
        Variable.__init__(self,name)
        Node.__init__(self,NodeType.T_NPCS)
        self._vehicles:List[NPCVehicle]=[]
    def add_npc_vehicle(self,vehicle:NPCVehicle):
        self._vehicles.append(vehicle)
    def get_size(self):
        return len(self._vehicles)
    def get_npc_vehicles(self)->List[NPCVehicle]:
        return self._vehicles

