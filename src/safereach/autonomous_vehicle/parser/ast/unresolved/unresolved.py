# The file Unresolved.py defines class 
# that representing unresolved data types until we can figure it out.
from parser.ast.base.state import Node,NodeType
from typing import Union,AnyStr,NoReturn,Tuple
from parser.ast.base.motion import UniformMotion,WaypointMotion
class NameWithRealValue(Node):
	def __init__(self,value:float,name:AnyStr):
		super().__init__(NodeType.T_NRV)
		self.__class__.__name__='unresolved type'
		self._value:float=value
		self._name:AnyStr=name
	def get_value(self)->float:
		return self._value
	def get_name(self)->AnyStr:
		return self._name
	def __str__(self):
		return f'{str(self._value)}'

# class NameWithRealValueSignal(Node):
# 	def __init__(self,signal,value:float,name:AnyStr):
# 		super().__init__(NodeType.T_NRV)
# 		self.__class__.__name__='unresolved type'
# 		self._signal=signal
# 		self._value:float=value
# 		self._name:AnyStr=name
# 	def get_value(self)->float:
# 		return self._value
# 	def get_signal(self):
# 		return self._signal
# 	def get_name(self)->AnyStr:
# 		return self._name
# 	def __str__(self):
# 		return f'{str(self._signal)}{str(self._value)}'


class NameWithString(Node):
	def __init__(self,value:AnyStr,name:AnyStr):
		self.__class__.__name__ = 'unresolved type'
		super().__init__(NodeType.T_NS)
		self._value:AnyStr=value
		self._name=name
	def get_value(self)->AnyStr:
		return self._value
	def get_name(self)->AnyStr:
		return self._name
	def __str__(self):
		return 'unresolved'
		
class NameWithTwoRealValues(Node):
	def __init__(self,v1:float,v2:float,name:AnyStr) :
		self.__class__.__name__ = 'unresolved type'
		Node.__init__(self,NodeType.T_NTRV)
		self._value:Tuple[float,float]=(v1,v2)
		self._name=name
	def get_value(self)->Tuple[float,float]:
		return self._value
	def get_name(self):
		return self._name
	def __str__(self):
		# return 'lalala'
		return f'{str(self._value)}'

class NameWithMotion(Node):
	def __init__(self,motion:Union[UniformMotion,WaypointMotion],name:AnyStr=''):
		Node.__init__(self,NodeType.T_NMOTION)
		self.__class__.__name__ = 'unresolved type'
		self._name=name
		self._motion=motion
	def is_uniform_motion(self)->bool:
		return isinstance(self._motion,UniformMotion)
	def is_waypoint_motion(self)->bool:
		return isinstance(self._motion,WaypointMotion)
	def get_motion(self)->Union[UniformMotion,WaypointMotion]:
		return self._motion
	def set_name(self,name:AnyStr)->NoReturn:
		self._name=name
	def get_name(self)->AnyStr:
		return self._name
	def __str__(self):
		return 'unresolved'