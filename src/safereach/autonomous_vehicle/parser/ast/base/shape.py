# The file Shape.py defines class representing npc vehicles
from parser.ast.base.state import Variable,Node,NodeType
from typing import Optional,AnyStr,Tuple
class Shape(Variable,Node):
	def __init__(self,name:AnyStr=''):
		Variable.__init__(self,name)
		Node.__init__(self,NodeType.T_SHAPE)
	def calculate_area(self):
		pass
	def calculate_volume(self):
		pass
class Sphere(Shape):
	def __init__(self,radius:float,name:AnyStr=''):
		super().__init__(name)
		self._radius=radius
	def get_radius(self)->float:
		return self._radius
	def calculate_area(self):
		pass
	# TODO:complete
	def calculate_volume(self):
		pass
class Box(Shape):
	def __init__(self,length:float,width:float,height:float,name:AnyStr=''):
		super().__init__(name)
		self._box:Tuple[float,float,float]=(length,width,height)
	def get_length(self)->float:
		return self._box[0]
	def get_width(self)->float:
		return self._box[1]
	def get_height(self)->float:
		return self._box[2]
	def calculate_area(self):
		pass
	# TODO:complete
	def calculate_volume(self):
		pass
class Cone(Shape):
	def __init__(self,radius:float,height:float,name:AnyStr=''):
		super().__init__(name)
		self._cone:Tuple[float,float]=(radius,height)
	def get_radius(self)->float:
		return self._cone[0]
	def get_height(self)->float:
		return self._cone[1]
	def calculate_area(self):
		pass
	# TODO:complete
	def calculate_volume(self):
		pass
class Cylinder(Shape):
	def __init__(self,radius:float,height:float,name:AnyStr=''):
		super().__init__(name)
		self._cone:Tuple[float,float]=(radius,height)
	def get_radius(self)->float:
		return self._cone[0]
	def get_height(self)->float:
		return self._cone[1]
	def calculate_area(self):
		pass
		# TODO:complete
	def calculate_volume(self):
		pass