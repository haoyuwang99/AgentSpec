# The file Weathers.py defines classes that describe weather
from enum import IntEnum
from parser.ast.base.state import Node, Variable,NodeType
from typing import Optional,AnyStr,List,NoReturn,Union
class WeatherKind(IntEnum):
	WK_SUNNY=0
	WK_RAIN=1
	WK_SNOW=2
	WK_FOG=3
	WK_WETNESS=4
	@staticmethod
	def switch(v:AnyStr)->AnyStr:
		if v=='WK_SUNNY':
			return 'sunny'
		elif v=='WK_RAIN':
			return 'rain'
		elif v=='WK_SNOW':
			return 'snow'
		elif v=='WK_FOG':
			return 'fog'
		elif v=='WK_WETNESS':
			return 'wetness'
		else:
			return ''
class WeatherDiscreteLevelEnum(IntEnum):
	WDL_LIGHT=0
	WDL_MIDDLE=1
	WDL_HEAVY=2
	@staticmethod
	def switch(v:AnyStr)->AnyStr:
		if v=='WDL_LIGHT':
			return 'light'
		elif v=='WDL_MIDDLE':
			return 'middle'
		elif v=='WDL_HEAVY':
			return 'heavy'
		else:
			return ''
class WeatherContinuousIndex(Variable,Node):
	def __init__(self,index:float,name:AnyStr=''):
		Variable.__init__(self,name)
		Node.__init__(self,NodeType.T_WEACON)
		self._index=index
	def get_index(self)->float:
		return self._index
class WeatherDiscreteLevel(Variable,Node):
	def __init__(self,level:WeatherDiscreteLevelEnum,name:AnyStr=''):
		Variable.__init__(self,name)
		Node.__init__(self,NodeType.T_WEADIS)
		self._level=level
	def get_level(self)->WeatherDiscreteLevelEnum:
		return self._level
class Weather(Variable,Node):
	def __init__(self,name:AnyStr=''):
		Variable.__init__(self,name)
		Node.__init__(self,NodeType.T_WEA)
		self._kind=None
		self._value=None
	
	def set_weather_kind(self,kind:WeatherKind):
		self._kind=kind
	def set_weather_kind_value(self,value:Union[WeatherContinuousIndex,WeatherDiscreteLevel]):
		self._value=value
	def get_weather_kind(self)->WeatherKind:
		return self._kind
	def is_weather_continuous_index(self)->bool:
		return isinstance(self._value,WeatherContinuousIndex)
	def is_weather_discrete_level(self)->bool:
		return isinstance(self._value,WeatherDiscreteLevel)
	def get_weather_kind_value(self)->Optional[Union[WeatherContinuousIndex,WeatherDiscreteLevel]]:
		return self._value
class Weathers(Variable,Node):
	def __init__(self,name:AnyStr=''):
		Variable.__init__(self,name)
		Node.__init__(self,NodeType.T_WEAS)
		self._weathers:List[Weather]=[]
	def add_weather(self,weather:Weather)->NoReturn:
		self._weathers.append(weather)
	def get_size(self)->int:
		return len(self._weathers)
	def get_weathers(self)->List[Weather]:
		return self._weathers
