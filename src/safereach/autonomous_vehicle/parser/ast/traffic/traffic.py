# The file Traffic.py defines classes that describe traffic
from parser.ast.base.state import Variable,Lane,NodeType,Node
from typing import List, Optional,AnyStr,Tuple,NoReturn
from enum import IntEnum
class IntersectionID(Variable,Node):
    def __init__(self,value:int,name:AnyStr=''):
        Variable.__init__(self,name)
        Node.__init__(self,NodeType.T_INTERID)
        self._value:int=value
    def get_value(self)->int:
        return self._value

class IntersectionTraffic(Variable,Node):
    class Sign(IntEnum):
        S_0=0
        S_1=1
        @staticmethod
        def switch(v:AnyStr)->AnyStr:
            if v=='S_0':
                return '0'
            elif v=='S_1':
                return '1'
            else:
                return ''
    def __init__(self,name:AnyStr=''):
        Variable.__init__(self,name)
        Node.__init__(self,NodeType.T_INTERTRA)
        self._id=None
        self._light=None
        self._stop=None
        self._crosswalk=None
    def set_id(self,intersection_id:IntersectionID):
        self._id=intersection_id
    def get_id(self)->IntersectionID:
        return self._id
    def set_traffic_light(self,light:Sign):
        self._light=light
    def set_stop_sign(self,stop:Sign):
        self._stop=stop
    def set_crosswalk(self,crosswalk:Sign):
        self._crosswalk=crosswalk
    def get_traffic_light(self)->int:
        return 0 if self._light==self.Sign.S_0 else 1
    def get_stop_sign(self)->int:
        return 0 if self._stop == self.Sign.S_0 else 1
    def get_crosswalk(self)->int:
        return 0 if self._crosswalk == self.Sign.S_0 else 1
class SpeedRange(Variable,Node):
    def __init__(self,name:AnyStr=''):
        Variable.__init__(self,name)
        Node.__init__(self,NodeType.T_SPEEDRANGE)
        self._x=0
        self._y=0
    def set_x(self,x:float):
        self._x=x
    def set_y(self,y:float):
        self._y=y
    def get_x(self)->float:
        return self._x
    def get_y(self)->float:
        return self._y
    def get_value(self)->Tuple[float,float]:
        return (self._x,self._y)
class SpeedLimitation(Variable,Node):
    def __init__(self,name:AnyStr=''):
        Variable.__init__(self,name)
        Node.__init__(self,NodeType.T_SPEEDLIMIT)
        self._lane=None
        self._speed_range=None
    def set_speed_range(self,speed_range:SpeedRange)->NoReturn:
        self._speed_range=speed_range
    def set_lane(self,lane:Lane):
        self._lane=lane
    def get_speed_range(self)->SpeedRange:
        return self._speed_range
    def get_lane(self)->Lane:
        return self._lane
class Traffic(Variable,Node):
    def __init__(self,name:AnyStr=''):
        Variable.__init__(self,name)
        Node.__init__(self,NodeType.T_TRAFFIC)
        self._intersection_traffics=[]
        self._speed_limitations=[]
    def add_intersection_traffic(self,value:IntersectionTraffic)->NoReturn:
        self._intersection_traffics.append(value)
    def add_speed_limitation(self,value:SpeedLimitation)->NoReturn:
        self._speed_limitations.append(value)
    def get_intersection_traffics(self)->List[IntersectionTraffic]:
        return self._intersection_traffics
    def get_speed_limitations(self)->List[SpeedLimitation]:
        return self._speed_limitations