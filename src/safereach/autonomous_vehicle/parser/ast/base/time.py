# The file Time.py defines class representing the time
from parser.ast.base.state import Variable,NodeType,Node
from typing import Optional,AnyStr
class Time(Variable,Node):
	def __init__(self,h:int,m:int,name:AnyStr=''):
		Variable.__init__(self,name)
		Node.__init__(self,NodeType.T_TIME)
		assert (0<=h<=23 and 0<=m<=59) or (h==24 and m==0)
		self._hour=h
		self._minute=m
	def get_hour(self)->int:
		return self._hour
	def get_minute(self)->int:
		return self._minute
