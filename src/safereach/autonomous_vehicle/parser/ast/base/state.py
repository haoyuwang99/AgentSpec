# The file State.py defines classes that describe common properties held
# by other classes.
from typing import AnyStr, Optional, Tuple, Union,NoReturn, overload
from enum import IntEnum
class NodeType(IntEnum):
	"""Defines the AST node types we need

	Some types has a name when we dump it, therefore these types must
	must have relevant type attributes.
	T_UNDEFINED: undefined type, this is set in the basic Node class.
	T_SCENARIO: denotes the Scenario type.
	T_MAP: denotes the Map type.
	T_EGO: denotes the EgoVehicle type.
	T_NPCS: denotes the NPCVehicles type.
	T_PEDS: denotes the Pedestrians type.
	T_OBS: denotes the Obstacles type.
	T_ENV: denotes the Environment type.
	T_TRAFFIC: denotes the Traffic type.
	T_STATE: denotes the State type.
	T_POS: denotes the Position type.
	T_LANE: denotes the Lane type.
	T_HEADING: denotes the Heading type.
	T_SPEED: denotes the Speed type.
	T_VETYPE: denotes the VehicleType type.
	T_TYPE: denotes the Type type.
	T_COLOR: denotes the Color type
	T_NPC: denotes the NPCVehicle type.
	T_VEMOTION: denotes the VehicleMotion type.
	T_STATELIST: denotes the StateList type.
	T_PED: denotes the Pedestrian type.
	T_PEDMOTION: denotes the PedestrianMotion type.
	T_HEIGHT: denotes the Height type.
	T_PEDTYPE: denotes the PedestrianType type.
	T_OB: denotes the Obstacle type.
	T_SHAPE: denotes the Shape type.
	T_TIME: denotes the Time type.
	T_WEAS: denotes the Weathers type.
	T_WEA: denotes the Weather type.
	T_WEACON: denotes the WeatherContinuousIndex type.
	T_WEADIS: denotes the WeatherDiscreteLevel type.
	T_INTERTRA: denotes the IntersectionTraffic type.
	T_INTERID: denotes the IntersectionID type.
	T_SPEEDLIMIT: denotes the SpeedLimitation type.
	T_SPEEDRANGE: denotes the SpeedRange type.
	T_NRV: denotes the unresolved NameWithRealValue type.
	T_NTRV: denotes the unresolved NameWithTwoRealValues type.
	T_NS: denotes the unresolved NameWithString type.
	T_NMOTION: denotes the unresolved NameWithMotion type.

	T_TRACE: denotes the trace name
	T_EGOSTATE: denotes the ego state
	T_AGENTSTATE: denotes the agent state
	T_AGENTGROUNDTRUTH: denotes the agent ground truth
	T_AGENTGDROUNDDIS: denotes the agent ground distance
	T_AGENTERROR: denotes the agent error
	T_DETECTIONS: denotes the detection assertions
	T_SAFETYS: denotes the safety assertions
	T_INTERASSERT: denotes the intersection assertion
	T_SPEEDCA: denotes the speed constraint assertion
	T_AASSERTIONTRACE: denotes the intermediate form that attaches an assertion to the trace
	T_SVTSE: error type(State,VehicleType,or StateList)
	T_SSE: error type(State,StateList)
	T_SVPSE: error type(State,VehicleType,PedestrianType,or StateList)
	T_PNOWTE: error type(Pedestrians,NPCVehicles,Obstacles,Weathers,or Traffic)


	T_GeneralDistanceStatement denotes the general distance statement
	T_PerceptionDifferenceStatement denotes the general perception difference 
	T_PositionDistance denotes the position statement
	T_SINGLEGENERAL denotes the single general assertion 
	"""


	T_UNDEFINED=0
	T_SCENARIO=1
	T_MAP=2
	T_EGO=3
	T_NPCS=4
	T_PEDS=5
	T_OBS=6
	T_ENV=7
	T_TRAFFIC=8
	T_STATE=9
	T_POS=10
	T_LANE=11
	T_HEADING=12
	T_SPEED=13
	T_VETYPE=14
	T_TYPE=15
	T_COLOR=16
	T_NPC=17
	T_VEMOTION=18
	T_STATELIST=19
	T_PED=20
	T_PEDMOTION=21
	T_HEIGHT=22
	T_PEDTYPE=23
	T_OB=24
	T_SHAPE=25
	T_TIME=26
	T_WEAS=27
	T_WEA=28
	T_WEACON=29
	T_WEADIS=30
	T_INTERTRA=31
	T_INTERID=32
	T_SPEEDLIMIT=33
	T_SPEEDRANGE=34
	T_NRV=35
	T_NTRV=36
	T_NS=37
	T_NMOTION=38
	T_TRACE=39
	T_EGOSTATE=40
	T_AGENTSTATE=41
	T_AGENTGROUNDTRUTH=42
	T_AGENTGROUNDDIS=43
	T_AGENTERROR=44
	T_DETECTIONS=45
	T_SAFETYS=46
	T_INTERASSERT=47
	T_SPEEDCA=48
	T_AASSERTIONTRACE=49
	T_SVTSE=50
	T_SSE=51
	T_SVPSE=52
	T_PNOWTE=53
	T_GeneralDistanceStatement=54
	T_PerceptionDifferenceStatement=55
	T_PositionDistance=56
	T_SINGLEGENERAL=57
	T_velocity_statement=58
	T_SpeedStatement=59
	T_AccelerationStatement=60
	T_OverallStatement=61

	T_COORDINATE=62


class Node:
	"""Defines basic Node class.
	"""
	def __init__(self,t:NodeType=NodeType.T_UNDEFINED) -> None:
		self._nodeKind:NodeType=t
	def get_node_kind(self)->NodeType:
		return self._nodeKind
# Base class inherited by others which have a name or an anonymous name.
class Variable:
	"""
	"""
	def __init__(self, name:AnyStr=''):
		self._name = name
	def set_name(self,name:AnyStr)->NoReturn:
		self._name=name
	def get_name(self) -> AnyStr:
		return self._name
	def is_anonymous(self) -> bool:
		return self._name == ''
class CoordinateFrame(IntEnum):
	CF_IMU = 0
	CF_ENU = 1
	CF_WGS84 = 2
	@staticmethod
	def switch(v:AnyStr)->AnyStr:
		if v=='CF_IMU':
			return 'IMU'
		elif v=='CF_ENU':
			return 'ENU'
		elif v=='CF_WGS84':
			return 'WGS84'
		else:
			return ''

class Coordinate(Variable,Node):
	def __init__(self, x: float, y: float,z:Optional[float]=None, name: AnyStr=''):
		Variable.__init__(self,name)
		Node.__init__(self,NodeType.T_COORDINATE)
		self._x = x
		self._y = y
		self._z = z
	def get_x(self) -> float:
		return self._x
	def get_y(self) -> float:
		return self._y
	def has_z(self)->bool:
		return self._z!=None
	def get_z(self)->float:
		assert self.has_z()
		return self._z
	def __str__(self) -> str:
		if self.has_z():
			return f'({str(self._x)},{str(self._y)},{str(self._z)})'	
		else:
			return f'({str(self._x)},{str(self._y)})'	


# NOTICE: Lane is a string and as such format:
# "road_id.lane_id" or ".lane_id",
# for example: "1.5",".4"
class Lane(Variable,Node):
	def __init__(self, description: str, name: AnyStr=''):
		Variable.__init__(self,name)
		Node.__init__(self,NodeType.T_LANE)
		self._id = description
	def get_lane_id(self) -> str:
		return self._id
	def __str__(self) -> str:
		return f'{str(self._id)}'

class LaneCoordinate:
	def __init__(self, dis: float):
		self._lane = None
		self._distance = dis
	def set_lane(self,lane:Lane):
		self._lane=lane
	def get_distance(self) -> float:
		return self._distance
	def get_lane(self) -> Lane:
		return self._lane
	def __str__(self) -> str:
		return f'{str(self._lane)}->{str(self._distance)}'


class Position(Variable,Node):
	def __init__(self, name: AnyStr=''):
		self._frame=None
		Variable.__init__(self,name)
		Node.__init__(self,NodeType.T_POS)
		self._coordinate = None
	def set_frame(self,frame:CoordinateFrame)->NoReturn:
		self._frame=frame
	def has_frame(self)->bool:
		return self._frame is not None
	def get_frame(self) -> CoordinateFrame:
		assert self.has_frame()
		return self._frame
	def is_frame_ENU(self) -> bool:
		assert self.has_frame()
		return self._frame == CoordinateFrame.CF_ENU
	def is_frame_IMU(self) -> bool:
		assert self.has_frame()
		return self._frame == CoordinateFrame.CF_IMU
	def is_frame_WGS84(self) -> bool:
		assert self.has_frame()
		return self._frame == CoordinateFrame.CF_WGS84
	def set_coordinate(self,value:Union[Coordinate,LaneCoordinate]):
		self._coordinate=value
	def is_normal_coordinate(self) -> bool:
		return isinstance(self._coordinate,Coordinate)
	def is_relative_coordinate(self) -> bool:
		return isinstance(self._coordinate,LaneCoordinate)
	def get_coordinate(self) -> Union[Coordinate, LaneCoordinate]:
		assert self._coordinate is not None
		return self._coordinate
	def generate_default_frame(self)->CoordinateFrame:
		assert self._coordinate is not None
		assert self._frame is None
		return CoordinateFrame.CF_ENU
	def __str__(self) -> str:
		return f'{str(self._coordinate)}'

class Unit(IntEnum):
	U_DEG = 0
	U_RAD = 1
	@staticmethod
	def switch(v:AnyStr)->AnyStr:
		if v=='U_DEG':
			return 'deg'
		elif v=='U_RAD':
			return 'rad'
		else:
			return ''

### XXX: Forward declarations
class EgoVehicle:
	...
class NPCVehicle:
	...
class Pedestrian:
	...
## PredefinedDirection has three forms:
## 1: EGO constant
## 2: lane->distance
## 3: agent, agent is an EgoVehicle,Pedestrian or NPCVehicle
class PredefinedDirection:
	def __init__(self):
		self._reference=None
		self._dis=0
	def is_default_ego(self) -> bool:
		return self._reference is None
	def set_reference(self,ref:Union[EgoVehicle,Pedestrian,NPCVehicle]):
		self._reference=ref
	def set_lane_reference(self,lane:Lane,dis:float)->NoReturn:
		self._reference=lane
		self._dis=dis
	def is_lane_reference(self)->bool:
		return isinstance(self._reference,Lane)
	def get_lane_reference(self)->Tuple[Lane,float]:
		assert self.is_lane_reference()
		return (self._reference,self._dis)
	def get_reference(self)->Union[EgoVehicle,Pedestrian,NPCVehicle]:
		# assert not self.is_default_ego() and not self.is_lane_reference()
		return self._reference

class Heading(Variable,Node):
	def __init__(self,unit:Unit,name: AnyStr=''):
		Variable.__init__(self,name)
		Node.__init__(self,NodeType.T_HEADING)
		self._value = 0
		self._is_pi= False
		self._unit = unit
		self._direction = None
	def get_unit(self)->Unit:
		return self._unit
	def set_pi_value(self):
		self._is_pi=True
	def is_pi_value(self):
		return self._is_pi
	def set_raw_heading_angle(self,value:float)->NoReturn:
		self._value= value
	def get_raw_heading_angle(self) -> float:
		return self._value
	def is_heading_DEG(self) -> bool:
		return self._unit == Unit.U_DEG
	def is_heading_RAD(self) -> bool:
		return self._unit == Unit.U_RAD
	def has_direction(self)->bool:
		return self._direction is not None
	def set_direction(self,direction: PredefinedDirection)->NoReturn:
		self._direction=direction
	def get_direction(self) -> PredefinedDirection:
		assert self.has_direction()
		return self._direction
class Speed(Variable,Node):
	def __init__(self,value:float,name:AnyStr=''):
		Variable.__init__(self,name)
		Node.__init__(self,NodeType.T_SPEED)
		self._value=value
	def get_speed_value(self):
		return self._value
	def __str__(self) -> str:
		return f'{str(self._value)}'	

class State(Variable,Node):
	def __init__(self,name:AnyStr=''):
		Variable.__init__(self,name)
		Node.__init__(self,NodeType.T_STATE)
		self._position=None
		self._heading=None
		self._speed=None
	def set_position(self,position:Position)->NoReturn:
		self._position=position
	def get_position(self)->Position:
		assert self._position is not None
		return self._position
	def set_heading(self,heading:Heading)->NoReturn:
		self._heading=heading
	def has_heading(self)->bool:
		return self._heading is not None
	def get_heading(self)->Heading:
		assert self.has_heading()
		return self._heading
	def set_speed(self,speed:Speed)->NoReturn:
		self._speed=speed
	def has_speed(self)->bool:
		return self._speed is not None
	def get_speed(self)->Speed:
		assert self.has_speed()
		return self._speed
