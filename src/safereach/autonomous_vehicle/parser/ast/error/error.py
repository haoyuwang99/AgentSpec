from parser.ast.base.state import Variable, Node, NodeType
from typing import AnyStr, NoReturn, Tuple, List


class BasicError:
	def __init__(self) -> NoReturn:
		pass


# TODO: Raise Trace time exception
# Some assertions defines the same trace time if they have.

class TraceTimeError(BasicError):
	pass


class IllegalTypeError(BasicError):
	def __init__(self, var_name: AnyStr, line: int, column: int, index_of_color_start: int, index_of_color_end: int,
				 display_text: AnyStr, origin_type: AnyStr, *expected_type: Tuple[AnyStr]) -> NoReturn:
		super().__init__()
		self.display_text = display_text
		self.line = line
		self.column = column
		self.index_of_color_start = index_of_color_start
		self.index_of_color_end = index_of_color_end
		self.var_name = var_name
		size = len(expected_type)
		expect = ''
		if size == 1:
			expect+=f'<class {expected_type[size - 1]}>'
		for v in range(0, size - 1):
			expect+=f'<class {expected_type[v]}> '
		else:
			expect+=f'or <class {expected_type[size - 1]}>'
		self.msg = f'Illegal type of  \'{var_name}\'' \
				   f':<class {origin_type}> ,expect type:{expect}'

	def __str__(self) -> AnyStr:
		return f'{self.line}:{self.column}:error:{self.msg}' \
			   f'\n\t{self.display_text}'


# TODO: maybe add previous definition here.
class RedefinitionVariableError(BasicError):
	def __init__(self, var_name: AnyStr, line: int, column: int, index_of_color_start: int, index_of_color_end: int,
				 display_text: AnyStr) -> NoReturn:
		super().__init__()
		self.var_name = var_name
		self.line = line
		self.column = column
		self.index_of_color_start = index_of_color_start
		self.index_of_color_end = index_of_color_end
		self.display_text = display_text

	def error(self) -> NoReturn:
		pass

	def __str__(self) -> AnyStr:
		return f'{self.line}:{self.column}:error:redefinition of variable \'{self.var_name}\'' \
			   f'\n\t{self.display_text}'


class UndefinedVariableError(BasicError):
	def __init__(self, var_name: AnyStr, line: int, column: int, index_of_color_start: int, index_of_color_end: int,
				 display_text: AnyStr) -> NoReturn:
		super().__init__()
		self.var_name = var_name
		self.line = line
		self.column = column
		self.index_of_color_end = index_of_color_end
		self.index_of_color_start = index_of_color_start
		self.display_text = display_text

	def __str__(self) -> AnyStr:
		return f'{self.line}:{self.column}:error:use of undeclared identifier \'{self.var_name}\'' \
			   f'\n\t{self.display_text}'


class LaneFormatError(BasicError):
	def __init__(self,lane_id:AnyStr,line: int, column: int, index_of_color_start: int, index_of_color_end: int,
				 display_text: AnyStr) -> NoReturn:
		super().__init__()
		self.lane_id = lane_id
		self.line = line
		self.column = column
		self.index_of_color_end = index_of_color_end
		self.index_of_color_start = index_of_color_start
		self.display_text = display_text

	def __str__(self) -> AnyStr:
		return f'{self.line}:{self.column}:error:\"{self.lane_id}\" illegal lane id format,lane id string must be consisting real number' \
			   f'\n\t{self.display_text}'


class IntersectionIDFormatError(BasicError):
	def __init__(self, id: float, line: int, column: int, index_of_color_start: int, index_of_color_end: int,
				 display_text: AnyStr) -> NoReturn:
		super().__init__()
		self.id=id
		self.line = line
		self.column = column
		self.index_of_color_end = index_of_color_end
		self.index_of_color_start = index_of_color_start
		self.display_text = display_text

	def __str__(self) -> AnyStr:
		return f'{self.line}:{self.column}:error:\"{self.id}\" illegal intersection id format,intersection id must be integer' \
			   f'\n\t{self.display_text}'


class WeatherContinuousIndexFormatError(BasicError):
	def __init__(self, id: float, line: int, column: int, index_of_color_start: int, index_of_color_end: int,
				 display_text: AnyStr) -> NoReturn:
		super().__init__()
		self.id = id
		self.line = line
		self.column = column
		self.index_of_color_end = index_of_color_end
		self.index_of_color_start = index_of_color_start
		self.display_text = display_text

	def __str__(self) -> AnyStr:
		return f'{self.line}:{self.column}:error:\"{self.id}\" illegal weather continuous index format,weather continuous index must be 0.0-1.0' \
			   f'\n\t{self.display_text}'


# The following classes define the error types:
# When we meet some error,it is important to resume
# (transit to error type) and continue parsing,
# Therefore, these error types are also designed to represent
# for some types caused of errors
## TODO:If taking them as correct types,then we can do something normal
class StateVehicleTypeStateListErrorType(Node, Variable):
	def __init__(self, name: AnyStr, value: AnyStr):
		self.__class__.__name__ = 'error type'
		Variable.__init__(self, name)
		Node.__init__(self, NodeType.T_SVTSE)
		self._value_name = value

	def get_value_name(self) -> AnyStr:
		return self._value_name


class StateStateListErrorType(Node, Variable):
	def __init__(self, name: AnyStr, first: AnyStr, second: AnyStr, third: AnyStr):
		self.__class__.__name__ = 'error type'
		Variable.__init__(self, name)
		self._first_value_name = first
		self._second_value_name = second
		self._third_value_name = third
		Node.__init__(self, NodeType.T_SSE)

	def get_first_value_name(self) -> AnyStr:
		return self._first_value_name

	def get_second_value_name(self) -> AnyStr:
		return self._second_value_name

	def get_third_value_name(self) -> AnyStr:
		return self._third_value_name


class StateVehicleTypePedestrianTypeStateListErrorType(Node, Variable):
	def __init__(self, name: AnyStr, first: AnyStr, second: AnyStr):
		self.__class__.__name__ = 'error type'
		Variable.__init__(self, name)
		self._first_value_name = first
		self._second_value_name = second
		Node.__init__(self, NodeType.T_SVPSE)

	def get_first_value_name(self) -> AnyStr:
		return self._first_value_name

	def get_second_value_name(self) -> AnyStr:
		return self._second_value_name


class PedestriansNPCVehiclesObstaclesWeathersTrafficErrorType(Node, Variable):
	def __init__(self, name: AnyStr):
		self.__class__.__name__ = 'error type'
		Variable.__init__(self, name)
		self._values = []
		Node.__init__(self, NodeType.T_PNOWTE)

	def add_value(self, value: AnyStr) -> NoReturn:
		return self._values.append(value)

	def get_values(self) -> List[AnyStr]:
		return self._values
