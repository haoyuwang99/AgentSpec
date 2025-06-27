# This file Scenarios.py is aim to represent the scenario we create.
from parser.ast.base.state import *
from parser.ast.map.map import *
from parser.ast.ego.ego_vehicle import *
from parser.ast.npc.npc_vehicles import *
from parser.ast.pedestrian.pedestrians import *
from parser.ast.obstacle.obstacles import *
from parser.ast.environment.environment import *
from parser.ast.traffic.traffic import *
from typing import Any, Optional,AnyStr,NoReturn
class Scenario(Variable,Node):
    def __init__(self,name:AnyStr=''):
        Variable.__init__(self,name)
        Node.__init__(self,NodeType.T_SCENARIO)
        self._map=None
        self._ego=None
        self._npc=None
        self._ped=None
        self._obs=None
        self._env=None
        # self._tra=None
    def add_map(self,map:Map):
        self._map=map
    def add_ego_vehicle(self,ego:EgoVehicle)->NoReturn:
        self._ego=ego
    def add_npc_vehicles(self,npc:NPCVehicles)->NoReturn:
        self._npc=npc
    def add_pedestrians(self,ped:Pedestrians)->NoReturn:
        self._ped=ped
    def add_obstacles(self,obs:Obstacles)->NoReturn:
        self._obs=obs
    def add_environment(self,env:Environment)->NoReturn:
        self._env=env
    # def add_traffic(self,tra:Traffic)->NoReturn:
    #     self._tra=tra
    # TODO: other helper functions
    def has_pedestrians(self)->bool:
        return self._ped is not None
    def has_npc_vehicles(self)->bool:
        return self._npc is not None
    def has_obstacles(self)->bool:
        return self._obs is not None
    def has_environment(self)->bool:
        return self._env is not None
    def has_traffic(self)->bool:
        return self._tra is not None
    def get_map(self)->Map:
        assert self._map is not None
        return self._map
    def get_ego_vehicle(self)->EgoVehicle:
        assert self._ego is not None
        return self._ego
    def get_npc_vehicles(self)->NPCVehicles:
        assert self.has_npc_vehicles()
        return self._npc
    def get_pedestrians(self)->Pedestrians:
        assert self.has_pedestrians()
        return self._ped
    def get_obstacles(self)->Obstacles:
        assert self.has_obstacles()
        return self._obs
    def get_environment(self)->Environment:
        assert self.has_environment()
        return self._env
    # def get_traffic(self)->Traffic:
    #     assert self.has_traffic()
    #     return self._tra
