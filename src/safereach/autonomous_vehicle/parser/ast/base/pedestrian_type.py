# The file PedestrianType.py defines class representing pedestrian type
from typing import NoReturn, Optional,AnyStr
from parser.ast.base.state import Variable,Node,NodeType
from parser.ast.base.vehicle_type import Color,RGBColor,ColorList
class Height(Variable,Node):
	def __init__(self,height:float,name:AnyStr=''):
		Variable.__init__(self,name)
		Node.__init__(self,NodeType.T_HEIGHT)
		self._value=height
	def get_value(self)->float:
		return self._value
class PedestrianType(Variable,Node):
	def __init__(self,name:AnyStr=''):
		Variable.__init__(self,name)
		Node.__init__(self,NodeType.T_PEDTYPE)
		self._height=None
		self._color=None
		self._name=None
	def set_height(self,height:Height)->NoReturn:
		self._height=height
	def set_color(self,color:Color)->NoReturn:
		self._color=color
	def set_name_type(self,namee)->NoReturn:
		self._name=namee
	def get_height(self)->Height:
		return self._height
	def get_color(self)->Color:
		return self._color
	def get_type_name(self)->str:
		return self._name
	def is_rgb_color(self)->bool:
		return isinstance(self._color,RGBColor)
	def is_color_list(self)->bool:
		return isinstance(self._color,ColorList)