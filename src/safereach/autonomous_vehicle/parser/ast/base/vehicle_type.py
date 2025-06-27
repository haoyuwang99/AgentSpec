# The file VehicleType.py defines classes that describe vehicle types held
# by other classes.
from typing import AnyStr,Optional,Tuple,NoReturn
from enum import IntEnum
from parser.ast.base.state import Node, NodeType, Variable
class Type(Variable,Node):
	def __init__(self,name:AnyStr=''):
		Variable.__init__(self,name)
		Node.__init__(self,NodeType.T_TYPE)
class SpecificType(Type):
	def __init__(self,value:AnyStr,name:AnyStr=''):
		super().__init__(name)
		self._value=value
	def get_value(self)->AnyStr:
		return self._value
class GeneralTypeEnum(IntEnum):
	GT_CAR=0
	GT_BUS=1
	GT_VAN=2
	GT_TRUCK=3
	GT_BICYCLE=4
	GT_MOTORBICYCLE=5
	GT_TRICYCLE=6
	@staticmethod
	def switch(v:AnyStr)->AnyStr:
		if v=='GT_CAR':
			return 'car'
		elif v=='GT_BUS':
			return 'bus'
		elif v=='GT_VAN':
			return 'van'
		elif v=='GT_TRUCK':
			return 'truck'
		elif v=='GT_BICYCLE':
			return 'bicycle'
		elif v=='GT_MOTORBICYCLE':
			return 'motorbicycle'
		elif v=='GT_TRICYCLE':
			return 'tricycle'
		else:
			return ''
class GeneralType(Type):
	def __init__(self,type_enum:GeneralTypeEnum,name:AnyStr=''):
		super().__init__(name)
		self._kind:GeneralTypeEnum=type_enum
	def get_kind(self)->GeneralTypeEnum:
		return self._kind


# Currently,we do not consider material
class Material:
	pass
class ColorListEnum(IntEnum):
	CL_RED=0
	CL_GREEN=1
	CL_BLUE=2
	CL_BLACK=3
	CL_WHITE=4
	@staticmethod
	def switch(v:AnyStr)->AnyStr:
		if v=='CL_RED':
			return 'red'
		elif v=='CL_GREEN':
			return 'green'
		elif v=='CL_BLUE':
			return 'blue'
		elif v=='CL_BLACK':
			return 'black'
		elif v=='CL_WHITE':
			return 'white'
		else:
			return ''
class Color(Variable,Node):
	def __init__(self,name:AnyStr=''):
		Variable.__init__(self,name)
		Node.__init__(self,NodeType.T_COLOR)
	
class ColorList(Color):
	def __init__(self,colorListEnum:ColorListEnum,name:AnyStr=''):
		super().__init__(name)
		self._kind=colorListEnum
	def get_kind(self)->ColorListEnum:
		return self._kind
	# TODO:other helper functions


class RGBColor(Color):
	def __init__(self,r:int,g:int,b:int,name:AnyStr=''):
		super().__init__(name)
		assert 0<=r<=255 and 0<=g<=255 and 0<=b<=255 
		self._value:Tuple[float,float,float]=(r,g,b)
	def get_r(self)-> float:
		return self._value[0]
	def get_g(self)-> float:
		return self._value[1]
	def get_b(self)-> float:
		return self._value[2]
	def get_value(self)-> Tuple[float, float, float]:
		return self._value



class VehicleType(Variable,Node):
	def __init__(self,name:AnyStr=''):
		Variable.__init__(self,name)
		Node.__init__(self,NodeType.T_VETYPE)
		self._type=None
		self._color=None
		self._material=None
	def set_type(self,type_:Type)->NoReturn:
		self._type=type_
	def set_color(self,color:Color)->NoReturn:
		self._color=color
	def setMaterial(self,material:Material)->NoReturn:
		self._material=material
	def has_color(self)->bool:
		return self._color is not None
	def has_material(self)->bool:
		return self._material is not None
	def get_color(self)->Color:
		assert self.has_color()
		return self._color
	def is_rgb_color(self)->bool:
		return isinstance(self._color,RGBColor)
	def is_color_list(self)->bool:
		return isinstance(self._color,ColorList)
	def get_type(self)->Type:
		return self._type
	def is_specific_type(self)->bool:
		return isinstance(self._type,SpecificType)
	def is_general_type(self)->bool:
		return isinstance(self._type,GeneralType)
	def get_material(self)->Material:
		assert self.has_material()
		return self._material
