# The file Motion.py defines classes that describe vehicle
# and pedestrian motions held
# by other classes.
from enum import  IntEnum
from typing import List,Optional,AnyStr,NoReturn,Union
from parser.ast.base.state import Node, State,Variable,NodeType
class UniformIndex(IntEnum):
	UI_uniform=0
	UI_Uniform=1
	UI_U=2
	UI_u=3
	@staticmethod
	def switch(v:AnyStr)->AnyStr:
		if v=='UI_uniform':
			return 'uniform'
		elif v=='UI_Uniform':
			return 'Uniform'
		elif v=='UI_U':
			return 'U'
		elif v=='UI_u':
			return 'u'
		else:
			return ''

class UniformMotion:
	def __init__(self):
		self._state=None
		# default value
		self._index=UniformIndex.UI_uniform
	def set_uniform_index(self,index:UniformIndex)->NoReturn:
		self._index=index
	def set_state(self,state:State):
		self._state=state
	def get_uniform_index(self)->UniformIndex:
		return self._index
	def get_state(self)->State:
		return self._state
class WaypointIndex(IntEnum):
	WI_Waypoint=0
	WI_W=1
	WI_WP=2
	WI_waypoint=3
	WI_w=4
	WI_wp=5
	@staticmethod
	def switch(v:AnyStr)->AnyStr:
		if v=='WI_Waypoint':
			return 'Waypoint'
		elif v=='WI_W':
			return 'W'
		elif v=='WI_WP':
			return 'WP'
		elif v=='WI_waypoint':
			return 'waypoint'
		elif v=='WI_w':
			return 'w'
		elif v=='WI_wp':
			return 'wp'
		else:
			return ''

class StateList(Variable,Node):
	def __init__(self,name:AnyStr=''):
		Variable.__init__(self,name)
		Node.__init__(self,NodeType.T_STATELIST)
		self._states:List[State]=[]
	def add_state(self,state:State)->NoReturn:
		self._states.append(state)
	def get_size(self)->int:
		return len(self._states)
	# TODO:other helper functions
	def get_states(self)->List[State]:
		return self._states
class WaypointMotion:
	def __init__(self):
		self._statelist=None
		# default index
		self._index = WaypointIndex.WI_Waypoint
	def set_waypoint_index(self, index: WaypointIndex) -> NoReturn:
		self._index = index
	def get_waypoint_index(self) -> WaypointIndex:
		return self._index
	def set_state_list(self,statelist:StateList):
		self._statelist=statelist
	def get_state_list(self)->StateList:
		return self._statelist
class Motion(Variable):
	def __init__(self,motion:Union[UniformMotion,WaypointMotion],name:AnyStr=''):
		super().__init__(name)
		self._motion=motion
	def is_uniform_motion(self)->bool:
		return isinstance(self._motion,UniformMotion)
	def is_waypoint_motion(self)->bool:
		return isinstance(self._motion,WaypointMotion)
	def get_motion(self)->Union[UniformMotion,WaypointMotion]:
		return self._motion
class VehicleMotion(Motion,Node):
	def __init__(self, motion: Union[UniformMotion, WaypointMotion], name: AnyStr=''):
		Motion.__init__(self,motion,name)
		Node.__init__(self,NodeType.T_VEMOTION)
class PedestrianMotion(Motion,Node):
	def __init__(self, motion: Union[UniformMotion, WaypointMotion], name: AnyStr=''):
		Motion.__init__(self,motion,name)
		Node.__init__(self,NodeType.T_PEDMOTION)
