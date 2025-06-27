import re
from parser.ast.assertion.assertion import DetectionAssertion, SafetyAssertion

from antlr4.CommonTokenStream import CommonTokenStream
from antlr4.tree.Tree import ParseTreeWalker
from antlr4.FileStream import FileStream
from parser.ast.base.motion import Motion, StateList, UniformIndex, WaypointIndex
from parser.ast.base.pedestrian_type import Height
from parser.ast.base.vehicle_type import (Color, ColorList, ColorListEnum, GeneralType,
													  GeneralTypeEnum, RGBColor, SpecificType,
													  Type)
from parser.ast.base.weathers import (Weather, WeatherContinuousIndex,
												  WeatherDiscreteLevel, WeatherDiscreteLevelEnum,
												  WeatherKind)
from parser.ast.error.error import *
from parser.ast.error.error_handler import *
from parser.ast.scenario.scenario import *
from parser.ast.unresolved.unresolved import *
from parser.ast.assertion.assertion import *
from parser.ast.ast import *
from parser import AVScenariosListener
from parser import AVScenariosLexer
from parser import AVScenariosParser
import math
from numpy import *

import random

class Sema:
	'''
	Sema: Semantic analysis for source code, hold a long-lived AST tree,
		also contains some utility functions,and error handling functions.
	1. Error resuming strategy:
		UndefinedVariableError: add an new empty object to continue parsing
		RedefinitionVariableError: ignore this node
		IllegalTypeError: add an new empty object to continue parsing
	'''

	# TODO: remove the Current class to ASTListener in the future.
	class Current:
		'''
		This class represents the current parsing point
		'''

		# XXX: _states stores the State objects we created.
		# Due to the fact that we cannot use one State object
		# to figure out which object it belongs to.
		# e.g., EgoVehicle has two States,
		# NPCVehicle has two States and one VehicleMotion,while
		# VehicleMotion has one State or a StateList consisting
		# of State elements.
		class TemporaryStates:
			def __init__(self):
				# _first and _second denote the Pedestrian and NPCVehicle
				# initial and target State.
				# _value denotes other State.
				self._first: Optional[State] = None
				self._second: Optional[State] = None
				self._value: Optional[State] = None
				self._flag = 0

		def __init__(self):
			self._scenario = None
			self._map = None
			self._ego_vehicle = None
			self._pedestrians = None
			self._npc_vehicles = None
			self._obstacles = None
			self._traffic = None
			self._vehicle_type = None
			self._coordinate = None
			self._lane = None
			self._lane_coordinate = None
			# self._lane_coordinate1 = None
			self._direction = None
			self._pedestrian_motion = None
			self._pedestrian_type = None
			self._name_with_motion = None
			self._position = None
			self._heading = None
			self._type = None
			self._height = None
			self._color = None
			self._name_of_ped_type = None
			self._npc_vehicle = None
			self._state_list = None
			self._pedestrian = None
			self._obstacle = None
			self._shape = None
			self._env = None
			self._time = None
			self._weathers = None
			self._weather = None
			self._weather_continuous = None
			self._weather_discrete = None
			self._intersection_traffic = None
			self._intersection_id = None
			self._speed_limit = None
			self._speed_range = None
			self._speed = None
			self._states = self.TemporaryStates()
			self._ego_speed = None
			self._agent_state = None
			self._string_expression = []
			self._real_value_expression = []
			self._coordinate_expression = []

			#self._perception_distance = None
			#self._truth_distance = None
			self._distance_statement = None
			self._distance_statement_temp = None
			self._perception_difference_statement = None
			self._perception_difference_statement_temp = None
			self._velocity_statement = None
			self._velocity_statement_temp = None
			self._speed_statement = None
			self._speed_statement_temp = None
			self._acceleration_statement = None
			self._acceleration_statement_temp = None
			self._real_value_of_atom_statement = None
			self._real_value_of_atom_statement_temp = None
			self._overall_statement = None
			self._overall_statement0 = None
			self._overall_statement1 = None
			self._sequence_of_statement0 = None
			self._sequence_of_statement1 = None
			self._kuohao_of_statement = None
			self._one_or_two = None
			self._temp_for_statement = None


			self._agent_ground_truth = None
			self._agent_ground_distance = None
			self._agent_visible_assert = None
			self._agent_error_assert = None
			self._agent_error = None
			self._agent_safety_assertion = None
			self._intersection_assertion = None
			self._speed_limitation_checking = None
			self._speed_violation = None
			self._speed_constraint_assertion = None
			self._trace = None
			self._ego_state = None
			self._traffic_detection_assert = None
			self._ego_speed = None
			self._red_light = None
			self._green_light = None
			self._detection_assertion = None
			self._safety_assertion = None

			self._general_assertion = None
			self._general_assertion1 = None

			self._general_assertion_list:Union[SingleGeneralAssertion]=[]
			self._general_atom_statements_list=[]

			self._traffic_rule_boolean_API = None

			# self._general_assertion2_left = None
			# self._general_assertion2_right = None

			# self._general_assertion3_left = None
			# self._general_assertion3_right = None

			# self._general_assertion4_left = None
			# self._general_assertion4_right = None

			# self._general_assertion5_left = None
			# self._general_assertion5_right = None

			# self._general_assertion6_left = None
			# self._general_assertion6_right = None

			self._atom_statement = None
			self._atom_statement_left = None
			self._atom_statement_right = None

			#XXX: These context are recorded just for error processing.
			self._lane_id_contexts:List[AVScenariosParser.Assign_strContext]=[]
			self._intersection_id_or_weather_continuous_index_contexts:List[AVScenariosParser.Assign_rv_rvContext]=[]

	def __init__(self,file_name:AnyStr):
		self._ast = AST()
		self._file_name=file_name
		self._current = self.Current()
		# statistics of errors
		self._errors = []

	def get_ast(self) -> AST:
		return self._ast

	def add_error(self, error: BasicError) -> NoReturn:
		self._errors.append(error)

	def set_error_handler(self) -> NoReturn:
		for error in self._errors:
			set_error_handler(error,self._file_name)

	def finish_sema(self) -> NoReturn:
		# If occurring errors ,then output them and exiting the parsing.
		size=len(self._errors)
		if size>0:
			self.set_error_handler()
			sys.stderr.write(f'{size} error(s) generated.\n')
			exit(0)

	def set(self, index, node: ALLOWED_TYPES) -> NoReturn:
		self._ast._nodes[index] = node

	def check_unique_id(self, name: AnyStr) -> bool:
		return self._ast.check_unique_id(name)

	def find_node(self, name: AnyStr) -> Optional[Tuple[ALLOWED_TYPES, int]]:
		return self._ast.find_node(name)

	# The following functions are helper functions that dealing with
	# different AST nodes during parsing.

	def begin_scenario(self, s: Scenario):
		pass

	def end_scenario(self, s: Scenario):
		# NOTICE:Scenarios can have a default(empty)
		# NPCVehicles,Obstacles,Environment and Traffic
		assert self._current._map is not None
		s.add_map(self._current._map)
		assert self._current._ego_vehicle is not None
		s.add_ego_vehicle(self._current._ego_vehicle)
		if self._current._npc_vehicles is not None:
			s.add_npc_vehicles(self._current._npc_vehicles)
		if self._current._pedestrians is not None:
			s.add_pedestrians(self._current._pedestrians)
		if self._current._obstacles is not None:
			s.add_obstacles(self._current._obstacles)
		if self._current._env is not None:
			s.add_environment(self._current._env)
		# if self._current._traffic is not None:
		# 	s.add_traffic(self._current._traffic)

	# we have already construct a scenario.
	def finish_scenario(self, s: Scenario):
		self._ast.add_scenario(s)
		self._ast.add_ast_node(s)

	def act_on_name_with_real_value(self, name: AnyStr, rv: float):
		v = NameWithRealValue(rv, name)
		# self._ast.addNRV(v)
		self._ast.add_ast_node(v)

	def act_on_name_with_real_value_and_signal(self, name: AnyStr, signal ,rv: float):
		v = NameWithRealValueSignal(signal, rv, name)
		# self._ast.addNRV(v)
		self._ast.add_ast_node(v)



	def act_on_name_with_string(self, name: AnyStr, str_: AnyStr):
		v = NameWithString(str_, name)
		# self._ast.addNS(v)
		self._ast.add_ast_node(v)

	def act_on_scenario(self, name: AnyStr):
		assert self._current._scenario is not None
		self._current._scenario.set_name(name)
		self.finish_scenario(self._current._scenario)

	def act_on_ego_vehicle(self, name: AnyStr):
		assert self._current._ego_vehicle is not None
		self._current._ego_vehicle.set_name(name)
		self.finish_ego_vehicle(self._current._ego_vehicle)

	def finish_ego_vehicle(self, e: EgoVehicle):
		self._ast.add_ast_node(e)

	# we must find the real context about this rule may stands for.
	# var may be <position>
	# or <type_>
	# or <state>
	def act_on_name_with_one_variable(self, name: AnyStr, var: Union[Tuple[ALLOWED_TYPES, int], AnyStr]):
		if isinstance(var, str):
			self._ast.add_ast_node(StateVehicleTypeStateListErrorType(name,var))
			return
		v, index = var
		if isinstance(v, Position):
			# print(name)
			s = State(name)
			# state=(position) no heading no speed
			s.set_position(v)
			self._ast.add_ast_node(s)
		elif isinstance(v, NameWithTwoRealValues):
			s = State(name)
			p = self.cast_to_position(v)
			s.set_position(p)
			self._ast.add_ast_node(s)
			self.set(index, p)
		elif isinstance(v, Type):
			vt = VehicleType(name)
			vt.set_type(v)
			self._ast.add_ast_node(vt)
		elif isinstance(v, NameWithString):
			vt = VehicleType(name)
			t = self.cast_to_type(v)
			vt.set_type(t)
			self._ast.add_ast_node(vt)
			self.set(index, t)
		elif isinstance(v, State):
			sl = StateList(name)
			sl.add_state(v)
			self._ast.add_ast_node(sl)
		elif isinstance(v,StateStateListErrorType) or isinstance(v,StateVehicleTypeStateListErrorType) \
				or isinstance(v,StateVehicleTypePedestrianTypeStateListErrorType):
			# cast the error type to StateList
			sl=StateList(name)
			s=self.cast_to_state(v)
			sl.add_state(s)
			self.set(index,s)
			self._ast.add_ast_node(sl)


	def act_on_state(self, name: AnyStr):
		assert self._current._states._value is not None
		self._current._states._value.set_name(name)
		self.finish_state(self._current._states._value)

	def begin_state(self, s: State):
		pass

	def end_state(self, s: State):
		assert self._current._position is not None
		s.set_position(self._current._position)
		if self._current._heading is not None:
			s.set_heading(self._current._heading)
		if self._current._speed is not None:
			s.set_speed(self._current._speed)

	def finish_state(self, s: State):
		self._ast.add_ast_node(s)

	def act_on_vehicle_type(self, name: AnyStr):
		assert self._current._vehicle_type is not None
		self._current._vehicle_type.set_name(name)
		self.finish_vehicle_type(self._current._vehicle_type)

	def begin_vehicle_type(self, vt: VehicleType):
		pass

	def end_vehicle_type(self, vt: VehicleType):
		assert self._current._type is not None
		vt.set_type(self._current._type)
		if self._current._color is not None:
			vt.set_color(self._current._color)

	# TODO: material?
	def finish_vehicle_type(self, vt: VehicleType):
		self._ast.add_ast_node(vt)

	# we already check the unique id of name
	# we must find the real context about this rule may stands for.
	# n1 and n2 may be <position> <heading>
	# or <type_> <color>
	# or <height> <color>
	# or <state> <state>
	def act_on_name_with_two_variables(self, name: AnyStr, v1: Union[Tuple[ALLOWED_TYPES, int],AnyStr],
									   v2: Union[Tuple[ALLOWED_TYPES, int],AnyStr]):
		if isinstance(v1,str):
			if isinstance(v2, str):
				self._ast.add_ast_node(StateVehicleTypePedestrianTypeStateListErrorType(name,v1,v2))
			return
		n1, index1 = v1
		# forward declaration
		index2=-1
		if isinstance(v2,str):
			n2=None
		else:
			n2, index2 = v2
		if isinstance(n1, Position):
			s = State(name)
			s.set_position(n1)
			if n2 is None:
				# Construct an empty Heading
				n2=Heading(Unit.U_DEG,v2)
				s.set_heading(n2)
			elif isinstance(n2, Heading):
				s.set_heading(n2)
			self._ast.add_ast_node(s)
		elif isinstance(n1, NameWithTwoRealValues):
			p = self.cast_to_position(n1)
			self.set(index1, p)
			s = State(name)
			s.set_position(p)
			if n2 is None:
				# Construct an empty Heading
				n2=Heading(Unit.U_DEG,v2)
				s.set_heading(n2)
			elif isinstance(n2, Heading):
				s.set_heading(n2)
			self._ast.add_ast_node(s)
		elif isinstance(n1, Type):
			vt = VehicleType(name)
			vt.set_type(n1)
			if n2 is None:
				# Construct an empty Color
				n2=RGBColor(0,0,0,v2)
				vt.set_color(n2)
			elif isinstance(n2, Color):
				vt.set_color(n2)
			self._ast.add_ast_node(vt)
		elif isinstance(n1, NameWithString):
			vt = VehicleType(name)
			t = self.cast_to_type(n1)
			self.set(index1, t)
			vt.set_type(t)
			if n2 is None:
				# Construct an empty Color
				n2=RGBColor(0,0,0,v2)
				vt.set_color(n2)
			elif isinstance(n2, Color):
				vt.set_color(n2)
			self._ast.add_ast_node(vt)
		elif isinstance(n1, Height):
			pt = PedestrianType(name)
			pt.set_height(n1)
			if n2 is None:
				# Construct an empty Color
				n2=RGBColor(0,0,0,v2)
				pt.set_color(n2)
			elif isinstance(n2, Color):
				pt.set_color(n2)
			self._ast.add_ast_node(pt)
		elif isinstance(n1, NameWithRealValue):
			pt = PedestrianType(name)
			h = self.cast_to_height(n1)
			self.set(index1, h)
			pt.set_height(h)
			if n2 is None:
				# Construct an empty Color
				n2=RGBColor(0,0,0,v2)
				pt.set_color(n2)
			elif isinstance(n2, Color):
				pt.set_color(n2)
			self._ast.add_ast_node(pt)
		elif isinstance(n1, State) or isinstance(n1,StateVehicleTypeStateListErrorType) or isinstance(n1,StateVehicleTypePedestrianTypeStateListErrorType) \
			or isinstance(n1,StateStateListErrorType):
			sl = StateList(name)
			if not isinstance(n1,State):
				n1=self.cast_to_state(n1)
				self.set(index1,n1)
			sl.add_state(n1)
			if n2 is None:
				n2=State(v2)
				sl.add_state(n2)
			elif isinstance(n2, State) or isinstance(n2,StateVehicleTypeStateListErrorType) or isinstance(n2,StateVehicleTypePedestrianTypeStateListErrorType) \
				or isinstance(n2,StateStateListErrorType):
				if not isinstance(n2, State):
					n2 = self.cast_to_state(n2)
					self.set(index2, n2)
				sl.add_state(n2)
			self._ast.add_ast_node(sl)

	def act_on_pedestrian_type(self, name: AnyStr):
		assert self._current._pedestrian_type is not None
		self._current._pedestrian_type.set_name(name)
		self.finish_pedestrian_type(self._current._pedestrian_type)

	def begin_pedestrian_type(self, pt: PedestrianType):
		pass

	def end_pedestrian_type(self, pt: PedestrianType):
		if self._current._height is not None:
			pt.set_height(self._current._height)
			assert self._current._color is not None
			pt.set_color(self._current._color)
		else:
			# print('????????????????///')
			assert self._current._name_of_ped_type is not None 
			pt.set_name_type(self._current._name_of_ped_type)

	def finish_pedestrian_type(self, pt: PedestrianType):
		self._ast.add_ast_node(pt)

	def finish_position(self, p: Position):
		self._ast.add_ast_node(p)
		self._current._lane = None

	def act_on_coordinate_position(self, name: AnyStr, coor: AnyStr, x: float, y: float, z: Optional[float] = None):
		# print('!!!!!!!!!!!!!!!!!!!!!!')
		# print('x: '+str(x)+'y: '+str(y)+'z: '+str(z))
		cf = Coordinate(x, y, z)
		p = Position(name)
		p.set_coordinate(cf)
		if coor == 'IMU':
			p.set_frame(CoordinateFrame.CF_IMU)
		elif coor == 'ENU':
			p.set_frame(CoordinateFrame.CF_ENU)
		elif coor == 'WGS84':
			p.set_frame(CoordinateFrame.CF_WGS84)
		self.finish_position(p)

	def act_on_lane_coordinate_position(self, name: AnyStr, coor: AnyStr, rv: float):
		assert self._current._lane is not None
		lc = LaneCoordinate(rv)
		lc.set_lane(self._current._lane)
		p = Position(name)
		p.set_coordinate(lc)
		if coor == 'IMU':
			p.set_frame(CoordinateFrame.CF_IMU)
		elif coor == 'ENU':
			p.set_frame(CoordinateFrame.CF_ENU)
		elif coor == 'WGS84':
			p.set_frame(CoordinateFrame.CF_WGS84)
		self.finish_position(p)

	def act_on_name_with_two_real_values(self, name: AnyStr, v1: float, v2: float):
		v = NameWithTwoRealValues(v1, v2, name)
		self._ast.add_ast_node(v)

	# we must find the real context about this rule may stands for.
	# n1 n2, and n3 may be <position> <heading> <speed>
	# or <state> <state> <state>
	def act_on_name_with_three_variables(self, name: AnyStr, v1: Union[Tuple[ALLOWED_TYPES, int],AnyStr],
										 v2: Union[Tuple[ALLOWED_TYPES, int],AnyStr], v3: Union[Tuple[ALLOWED_TYPES, int],AnyStr]):
		if isinstance(v1,str):
			if isinstance(v2,str) and isinstance(v3,str):
				self._ast.add_ast_node(StateStateListErrorType(name,v1,v2,v3))
			return
		n1, index1 = v1
		index2=-1
		if isinstance(v2,str):
			n2=None
		else:
			n2, index2 = v2
		# XXX: The index3 value [here -1] is not useless,
		# this statement is only to declare a local variable index3
		index3=-1
		if isinstance(v3,str):
			n3=None
		else:
			n3, index3 = v3
		isPos = isinstance(n1, Position)
		isNTRV = isinstance(n1, NameWithTwoRealValues)
		isState = isinstance(n1, State) or isinstance(n1,StateVehicleTypeStateListErrorType) or isinstance(n1,StateVehicleTypePedestrianTypeStateListErrorType) \
			or isinstance(n1,StateStateListErrorType)
		if isNTRV or isPos:
			if isNTRV:
				n1 = self.cast_to_position(n1)
				self.set(index1, n1)
			s = State(name)
			s.set_position(n1)
			if n2 is None:
				# Construct an empty Heading
				n2=Heading(Unit.U_DEG,v2)
				s.set_heading(n2)
			elif isinstance(n2, Heading):
				s.set_heading(n2)
			if n3 is None:
				# Construct an empty Speed
				n3=Speed(0,v3)
				s.set_speed(n3)
			elif isinstance(n3, NameWithRealValue):
				n3 = self.cast_to_speed(n3)
				# XXX:This guarantee index3 is already defined
				self.set(index3, n3)
				s.set_speed(n3)
			elif isinstance(n3, Speed):
				s.set_speed(n3)
			self._ast.add_ast_node(s)
		elif isState:  # n1 is State
			if not isinstance(n1,State):
				n1=self.cast_to_state(n1)
				self.set(index1,n1)
			sl = StateList(name)
			sl.add_state(n1)
			if n2 is None:
				# Construct an empty State
				n2=State(v2)
				sl.add_state(n2)
			elif isinstance(n2, State) or isinstance(n2,StateVehicleTypeStateListErrorType) or isinstance(n2,StateVehicleTypePedestrianTypeStateListErrorType) \
				or isinstance(n2,StateStateListErrorType):
				if not isinstance(n2,State):
					n2 = self.cast_to_state(n2)
					self.set(index2, n2)
				sl.add_state(n2)
			if n3 is None:
				# Construct an empty State
				n3=State(v3)
				sl.add_state(n3)
			elif isinstance(n3, State) or isinstance(n3,StateVehicleTypeStateListErrorType) or isinstance(n3,StateVehicleTypePedestrianTypeStateListErrorType) \
				or isinstance(n3,StateStateListErrorType):
				if not isinstance(n3,State):
					n3 = self.cast_to_state(n3)
					self.set(index3, n3)
				sl.add_state(n3)
			self._ast.add_ast_node(sl)

	def finish_heading(self, h: Heading):
		self._ast.add_ast_node(h)

	def act_on_heading(self, name: AnyStr):
		assert self._current._heading is not None
		self._current._heading.set_name(name)
		self.finish_heading(self._current._heading)

	def finish_type(self, t: Type):
		self._ast.add_ast_node(t)

	def act_on_type(self, name: AnyStr):
		assert self._current._type is not None
		self._current._type.set_name(name)
		self.finish_type(self._current._type)

	def finish_color(self, c: Color):
		self._ast.add_ast_node(c)

	def act_on_color(self, name: AnyStr):
		assert self._current._color is not None
		self._current._color.set_name(name)
		self.finish_color(self._current._color)

	def finish_npc_vehicle(self, n: NPCVehicle):
		self._ast.add_ast_node(n)

	def act_on_npc_vehicle(self, name: AnyStr):
		assert self._current._npc_vehicle is not None
		self._current._npc_vehicle.set_name(name)
		self.finish_npc_vehicle(self._current._npc_vehicle)

	def finish_state_list(self, sl: StateList):
		self._ast.add_ast_node(sl)

	def act_on_stateList(self, name: AnyStr):
		assert self._current._state_list is not None
		self._current._state_list.set_name(name)
		self.finish_state_list(self._current._state_list)

	def finish_pedestrians(self, ps: Pedestrians):
		self._ast.add_ast_node(ps)

	def act_on_pedestrians(self, name: AnyStr):
		assert self._current._pedestrians is not None
		self._current._pedestrians.set_name(name)
		self.finish_pedestrians(self._current._pedestrians)

	def finish_npc_vehicles(self, npcs: NPCVehicles):
		self._ast.add_ast_node(npcs)

	def act_on_npc_vehicles(self, name: AnyStr):
		assert self._current._npc_vehicles is not None
		self._current._npc_vehicles.set_name(name)
		self.finish_npc_vehicles(self._current._npc_vehicles)

	def finish_obstacles(self, obs: Obstacles):
		self._ast.add_ast_node(obs)

	def act_on_obstacles(self, name: AnyStr):
		assert self._current._obstacles is not None
		self._current._obstacles.set_name(name)
		self.finish_obstacles(self._current._obstacles)

	def finish_weathers(self, ws: Weathers):
		self._ast.add_ast_node(ws)

	def act_on_weathers(self, name: AnyStr):
		assert self._current._weathers is not None
		self._current._weathers.set_name(name)
		self.finish_weathers(self._current._weathers)

	def finish_traffic(self, t: Traffic):
		self._ast.add_ast_node(t)

	def act_on_traffic(self, name: AnyStr):
		assert self._current._traffic is not None
		self._current._traffic.set_name(name)
		self.finish_traffic(self._current._traffic)

	def finish_pedestrian(self, p: Pedestrian):
		self._ast.add_ast_node(p)

	def act_on_pedestrian(self, name: AnyStr):
		assert self._current._pedestrian is not None
		self._current._pedestrian.set_name(name)
		self.finish_pedestrian(self._current._pedestrian)

	def finish_obstacle(self, o: Obstacle):
		self._ast.add_ast_node(o)

	def act_on_obstacle(self, name: AnyStr):
		assert self._current._obstacle is not None
		self._current._obstacle.set_name(name)
		self.finish_obstacle(self._current._obstacle)

	def finish_environment(self, e: Environment):
		self._ast.add_ast_node(e)

	def act_on_environment(self, name: AnyStr):
		assert self._current._env is not None
		self._current._env.set_name(name)
		self.finish_environment(self._current._env)

	def finish_shape(self, s: Shape):
		self._ast.add_ast_node(s)

	def act_on_shape(self, name: AnyStr):
		assert self._current._shape is not None
		self._current._shape.set_name(name)
		self.finish_shape(self._current._shape)

	def finish_time(self, t: Time):
		self._ast.add_ast_node(t)

	def act_on_time(self, name: AnyStr):
		assert self._current._time is not None
		self._current._time.set_name(name)
		self.finish_time(self._current._time)

	def finish_weather(self, w: Weather):
		self._ast.add_ast_node(w)

	def act_on_weather(self, name: AnyStr):
		assert self._current._weather is not None
		self._current._weather.set_name(name)
		self.finish_weather(self._current._weather)

	def act_on_weather_discrete_level(self, name: AnyStr, value: AnyStr):
		if value == 'light':
			self._ast.add_ast_node(WeatherDiscreteLevel(
				WeatherDiscreteLevelEnum.WDL_LIGHT, name))
		elif value == 'middle':
			self._ast.add_ast_node(WeatherDiscreteLevel(
				WeatherDiscreteLevelEnum.WDL_MIDDLE, name))
		elif value == 'heavy':
			self._ast.add_ast_node(WeatherDiscreteLevel(
				WeatherDiscreteLevelEnum.WDL_HEAVY, name))

	def finish_intersection_traffic(self, it: IntersectionTraffic):
		self._ast.add_ast_node(it)

	def act_on_intersecion_traffic(self, name: AnyStr):
		assert self._current._intersection_traffic is not None
		self._current._intersection_traffic.set_name(name)
		self.finish_intersection_traffic(self._current._intersection_traffic)

	def finish_speed_limitation(self, sl: SpeedLimitation):
		self._ast.add_ast_node(sl)

	def act_on_speed_limitation(self, name: AnyStr):
		assert self._current._speed_limit is not None
		self._current._speed_limit.set_name(name)
		self.finish_speed_limitation(self._current._speed_limit)

	def finish_name_with_motion(self, nm: NameWithMotion):
		self._ast.add_ast_node(nm)

	def act_on_name_with_motion(self, name: AnyStr):
		assert self._current._name_with_motion is not None
		self._current._name_with_motion.set_name(name)
		self.finish_name_with_motion(self._current._name_with_motion)

	def begin_ego_vehicle(self, e: EgoVehicle):
		# do not check unique because
		# e is anonymous
		pass

	def end_ego_vehicle(self, e: EgoVehicle):
		assert self._current._states._first is not None \
			   and self._current._states._second is not None
		e.set_first_state(self._current._states._first)
		e.set_second_state(self._current._states._second)
		if self._current._vehicle_type is not None:
			e.set_vehicle_type(self._current._vehicle_type)

	def begin_position(self, p: Position):
		# do not call check_unique_id
		pass

	def end_position(self, p: Position, coor: AnyStr = ''):
		if coor == 'IMU':
			p.set_frame(CoordinateFrame.CF_IMU)
		elif coor == 'ENU':
			p.set_frame(CoordinateFrame.CF_ENU)
		elif coor == 'WGS84':
			p.set_frame(CoordinateFrame.CF_WGS84)
		assert not (self._current._lane_coordinate is None and
					len(self._current._coordinate_expression) ==0)
		if self._current._lane_coordinate is not None:
			p.set_coordinate(self._current._lane_coordinate)
		# elif self._current._lane_coordinate is not None:
		#   p.set_coordinate(self._current._lane_coordinate)
		elif len(self._current._coordinate_expression)>0:
			p.set_coordinate(self._current._coordinate_expression[-1])
			self._current._coordinate_expression.pop()

	def begin_lane_coordinate(self, lc: LaneCoordinate):
		pass

	def end_lane_coordinate(self, lc: LaneCoordinate):
		assert self._current._lane is not None
		lc.set_lane(self._current._lane)

	def begin_heading(self, value: float, h: Heading):
		h.set_raw_heading_angle(value)

	def end_heading(self, h: Heading):
		if self._current._direction is not None:
			h.set_direction(self._current._direction)

	def begin_direction(self, pd: PredefinedDirection):
		pass

	def end_direction(self, pd:PredefinedDirection):
		if self._current._lane is not None:
			# print('????')
			pd._reference=self._current._lane

	def begin_npc_vehicle(self, nv: NPCVehicle):
		pass

	def end_npc_vehicle(self, nv: NPCVehicle):
		assert self._current._states._first is not None
		nv.set_first_state(self._current._states._first)
		if self._current._states._second is not None:
			nv.set_second_state(self._current._states._second)
		if self._current._name_with_motion is not None:
			# motion is either waypointmotion or uniformmotion.
			# so we must build vehicle motion
			vm = VehicleMotion(self._current._name_with_motion.get_motion()
							   , self._current._name_with_motion.get_name())
			nv.set_vehicle_motion(vm)
		if self._current._vehicle_type is not None:
			nv.set_vehicle_type(self._current._vehicle_type)

	def begin_motion(self, m: NameWithMotion, isUniform: bool):
		pass

	def end_motion(self, m: NameWithMotion, isUniform: bool, ):
		if isUniform:
			# here we do not need set index.
			assert self._current._states._value is not None
			m.get_motion().set_state(self._current._states._value)
		else:
			assert self._current._state_list is not None
			m.get_motion().set_state_list(self._current._state_list)

	def begin_pedestrian(self, p: Pedestrian):
		pass

	def end_pedestrian(self, p: Pedestrian):
		assert self._current._states._first is not None
		p.set_first_state(self._current._states._first)
		if self._current._states._second is not None:
			p.set_second_state(self._current._states._second)
		if self._current._name_with_motion is not None:
			# motion is either waypointmotion or uniformmotion.
			# so we must build pedestrian motion
			pm = PedestrianMotion(self._current._name_with_motion.get_motion()
								  , self._current._name_with_motion.get_name())
			p.set_pedestrian_motion(pm)
		if self._current._pedestrian_type is not None:
			p.set_vehicle_type(self._current._pedestrian_type)

	def begin_obstacle(self, o: Obstacle):
		pass

	def end_obstacle(self, o: Obstacle):
		assert self._current._position is not None
		o.set_position(self._current._position)
		if self._current._shape is not None:
			o.set_shape(self._current._shape)

	def begin_env(self, e: Environment):
		pass

	def end_env(self, e: Environment):
		assert self._current._time is not None and self._current._weathers is not None
		e.set_time(self._current._time)
		e.set_weathers(self._current._weathers)

	def begin_weather(self, w: Weather):
		pass

	def end_weather(self, w: Weather):
		assert self._current._weather_continuous is not None \
			   or self._current._weather_discrete is not None
		if self._current._weather_continuous is not None:
			w.set_weather_kind_value(self._current._weather_continuous)
		elif self._current._weather_discrete is not None:
			w.set_weather_kind_value(self._current._weather_discrete)

	def begin_intersection_traffic(self, it: IntersectionTraffic, traffic_light: int
								   , stop_sign: int, crosswalk: int):
		it.set_traffic_light(IntersectionTraffic.Sign.S_0
							 if traffic_light == 0 else IntersectionTraffic.Sign.S_1)
		it.set_traffic_light(IntersectionTraffic.Sign.S_0
							 if stop_sign == 0 else IntersectionTraffic.Sign.S_1)
		it.set_crosswalk(IntersectionTraffic.Sign.S_0
						 if crosswalk == 0 else IntersectionTraffic.Sign.S_1)

	def end_intersection_traffic(self, it: IntersectionTraffic):
		assert self._current._intersection_id is not None
		it.set_id(self._current._intersection_id)

	def begin_speed_limitation(self, sl: SpeedLimitation):
		pass

	def end_speed_limitation(self, sl: SpeedLimitation):
		assert self._current._lane is not None
		sl.set_lane(self._current._lane)
		assert self._current._speed_range is not None
		sl.set_speed_range(self._current._speed_range)

	def cast_to_height(self, n: NameWithRealValue) -> Height:
		return Height(n.get_value(), n.get_name())

	def cast_to_speed(self, n: NameWithRealValue) -> Speed:
		return Speed(n.get_value(), n.get_name())

	def cast_to_state(self,n:Union[StateVehicleTypePedestrianTypeStateListErrorType,StateVehicleTypeStateListErrorType,StateStateListErrorType]):
		if isinstance(n,StateVehicleTypePedestrianTypeStateListErrorType):
			s=State(n.get_name())
			s.set_position(Position(n.get_first_value_name()))
			s.set_heading(Heading(n.get_second_value_name()))
		elif isinstance(n,StateVehicleTypeStateListErrorType):
			s=State(n.get_name())
			s.set_position(n.get_value_name())
			return s
		elif isinstance(n,StateStateListErrorType):
			s=State(n.get_name())
			s.set_position(n.get_first_value_name())
			s.set_heading(n.get_second_value_name())
			s.set_speed(n.get_third_value_name())
			return s
	def cast_to_state_list(self,n:Union[StateVehicleTypePedestrianTypeStateListErrorType,StateVehicleTypeStateListErrorType,StateStateListErrorType]):
		if isinstance(n,StateVehicleTypePedestrianTypeStateListErrorType):
			sl=StateList(n.get_name())
			sl.add_state(State(n.get_first_value_name()))
			sl.add_state(State(n.get_second_value_name()))
			return sl
		elif isinstance(n,StateVehicleTypeStateListErrorType):
			sl = StateList(n.get_name())
			sl.add_state(State(n.get_value_name()))
			return sl
		elif isinstance(n,StateStateListErrorType):
			sl = StateList(n.get_name())
			sl.add_state(State(n.get_first_value_name()))
			sl.add_state(State(n.get_second_value_name()))
			sl.add_state(State(n.get_third_value_name()))
			return sl
	def cast_to_vehicle_type(self,n:Union[StateVehicleTypePedestrianTypeStateListErrorType,StateVehicleTypeStateListErrorType]):
		if isinstance(n,StateVehicleTypeStateListErrorType):
			vh=VehicleType(n.get_name())
			vh.set_type(SpecificType("Error Type",n.get_value_name()))
			return vh
		if isinstance(n,StateVehicleTypePedestrianTypeStateListErrorType):
			vh = VehicleType(n.get_name())
			vh.set_type(SpecificType("Error Type", n.get_first_value_name()))
			vh.set_color(RGBColor(0,0,0,n.get_second_value_name()))
			return vh
	def cast_to_pedestrian_type(self,n:StateVehicleTypePedestrianTypeStateListErrorType):
		if isinstance(n,StateVehicleTypePedestrianTypeStateListErrorType):
			pt=PedestrianType(n.get_name())
			pt.set_height(Height(0,n.get_first_value_name()))
			pt.set_color(RGBColor(0,0,0,n.get_second_value_name()))
			return pt
	def cast_to_pedestrians(self,n:PedestriansNPCVehiclesObstaclesWeathersTrafficErrorType):
		ps=Pedestrians(n.get_name())
		for ele in n.get_values():
			ps.add_pedestrian(Pedestrian(ele))
		return ps
	def cast_to_npc_vehicles(self,n:PedestriansNPCVehiclesObstaclesWeathersTrafficErrorType):
		npcs=NPCVehicles(n.get_name())
		for ele in n.get_values():
			npcs.add_npc_vehicle(NPCVehicle(ele))
		return npcs
	def cast_to_obstacles(self,n:PedestriansNPCVehiclesObstaclesWeathersTrafficErrorType):
		os=Obstacles(n.get_name())
		for ele in n.get_values():
			os.add_obstacle(Obstacle(ele))
		return os
	def cast_to_weathers(self,n:PedestriansNPCVehiclesObstaclesWeathersTrafficErrorType):
		ws=Weathers(n.get_name())
		for ele in n.get_values():
			ws.add_weather(Weather(ele))
		return ws
	def cast_to_traffic(self,n:PedestriansNPCVehiclesObstaclesWeathersTrafficErrorType):
		t=Traffic(n.get_name())
		for ele in n.get_values():
			t.add_intersection_traffic(IntersectionTraffic(ele))
		return t
	def cast_to_lane(self, n: NameWithString) -> Lane:
		return Lane(n.get_value(), n.get_name())
	def check_lane_id_validity(self,description:AnyStr):
		split=description.split('.')
		if len(split) != 2:
			return False
		else:
			if split[1] == '':
				return False
			for Ele in split[0]:
				if not ('0' <= Ele <= '9' or Ele == '-' or Ele == '+'):
					return False
			for Ele in split[1]:
				if not ('0' <= Ele <= '9' or Ele == '-' or Ele == '+'):
					return False
		return True
	def cast_to_weather_continuous_index(self, n: NameWithRealValue) -> WeatherContinuousIndex:
		return WeatherContinuousIndex(n.get_value(), n.get_name())

	def cast_to_intersection_id(self, n: NameWithRealValue) -> IntersectionID:
		return IntersectionID(int(n.get_value()), n.get_name())
	# guarantee the unique id
	def find_context_for_error(self,name):
		for ctx in self._current._lane_id_contexts:
			if ctx.children[0].getText()==name:
				return ctx
		for ctx in self._current._intersection_id_or_weather_continuous_index_contexts:
			if ctx.children[0].getText()==name:
				return ctx

	def cast_to_map(self, n: NameWithString) -> Map:
		return Map(n.get_value(), n.get_name())

	def cast_to_type(self, n: NameWithString) -> Type:
		t = SpecificType(n.get_value(), n.get_name())
		return t

	def cast_to_position(self, n: NameWithTwoRealValues) -> Position:
		p = Position(n.get_name())
		p.set_coordinate(Coordinate(n.get_value()[0], n.get_value()[1]))
		return p

	def cast_to_speed_range(self, n: NameWithTwoRealValues) -> SpeedRange:
		sr = SpeedRange(n.get_name())
		sr.set_x(n.get_value()[0])
		sr.set_y(n.get_value()[1])
		return sr

	def cast_to_motion(self, n: Union[PedestrianMotion, VehicleMotion]):
		return NameWithMotion(n.get_motion(), n.get_name())

	def finish_trace(self, trace: Trace):
		self._ast.add_ast_node(trace)
		self._ast.add_trace(trace)

	def act_on_agent_ground_truth(self, name: AnyStr):
		assert self._current._agent_ground_truth is not None
		self._current._agent_ground_truth.set_name(name)
		self.finish_agent_ground_truth(self._current._agent_ground_truth)

	def finish_agent_ground_truth(self, agt: AgentGroundTruth):
		self._ast.add_ast_node(agt)

	def act_on_agent_ground_distance(self, name: AnyStr):
		assert self._current._agent_ground_distance is not None
		self._current._agent_ground_distance.set_name(name)
		self.finish_agent_ground_distance(self._current._agent_ground_distance)

	def finish_agent_ground_distance(self, agd: AgentGroundDistance):
		self._ast.add_ast_node(agd)

	def act_on_ego_state(self, name: AnyStr):
		assert self._current._ego_state is not None
		self._current._ego_state.set_name(name)
		self.finish_ego_state(self._current._ego_state)

	def finish_ego_state(self, es: EgoState):
		self._ast.add_ast_node(es)

	def act_on_agent_error(self, name: AnyStr):
		assert self._current._agent_error is not None
		self._current._agent_error.set_name(name)
		self.finish_agent_error(self._current._agent_error)


	def finish_agent_error(self, ae: AgentError):
		self._ast.add_ast_node(ae)

	def act_on_agent_state(self, name: AnyStr):
		assert self._current._agent_state is not None
		self._current._agent_state.set_name(name)
		self.finish_agent_state(self._current._agent_state)


	def finish_agent_state(self, as_: AgentState):
		self._ast.add_ast_node(as_)

	def begin_agent_visible_detection_assertion(self, avda: AgentVisibleDetectionAssertion):
		pass

	def end_agent_visible_detection_assertion(self, avda: AgentVisibleDetectionAssertion):
		assert self._current._agent_ground_distance is not None

		avda.set_agent_ground_distance(self._current._agent_ground_distance)


	def begin_agent_ground_distance(self, agd: AgentGroundDistance):
		pass

	def end_agent_ground_distance(self, agd: AgentGroundDistance):
		assert self._current._ego_state is not None
		assert self._current._agent_ground_truth is not None
		agd.set_ego_state(self._current._ego_state)
		agd.set_agent_ground_truth(self._current._agent_ground_truth)


	def begin_distance_statement(self, agd: GeneralDistanceStatement):
		pass

	def end_distance_statement(self, agd: GeneralDistanceStatement):
		if self._current._ego_state is not None and self._current._agent_state is not None:
			assert self._current._position is None
			assert self._current._agent_ground_truth is None
			agd.set_position_element_left(self._current._ego_state)
			agd.set_position_element_right(self._current._agent_state)
		elif self._current._ego_state is not None and self._current._agent_ground_truth is not None:
			assert self._current._position is None
			assert self._current._agent_state is None
			agd.set_position_element_left(self._current._ego_state)
			agd.set_position_element_right(self._current._agent_ground_truth)
		elif self._current._ego_state is not None and self._current._position is not None:
			assert self._current._agent_ground_truth is None
			assert self._current._agent_state is None
			agd.set_position_element_left(self._current._ego_state)
			agd.set_position_element_right(self._current._position)
		elif self._current._agent_state is not None and self._current._agent_ground_truth is not None:
			assert self._current._position is None
			assert self._current._ego_state is None
			agd.set_position_element_left(self._current._agent_state)
			agd.set_position_element_right(self._current._agent_ground_truth)
		elif self._current._agent_state is not None and self._current._position is not None:
			assert self._current._agent_ground_truth is None
			assert self._current._ego_state is None
			agd.set_position_element_left(self._current._agent_state)
			agd.set_position_element_right(self._current._position)
		elif self._current._agent_ground_truth is not None and self._current._position is not None:
			assert self._current._agent_state is None
			assert self._current._ego_state is None
			agd.set_position_element_left(self._current._agent_ground_truth)
			agd.set_position_element_right(self._current._position)
		elif self._current._temp_for_statement is not None:
			if isinstance(self._current._temp_for_statement, AgentGroundTruth):
				assert self._current._agent_ground_truth is not None 
				agd.set_position_element_left(self._current._agent_ground_truth)
				agd.set_position_element_right(self._current._temp_for_statement)
			if isinstance(self._current._temp_for_statement, EgoState):
				assert self._current._ego_state is not None 
				agd.set_position_element_left(self._current._ego_state)
				agd.set_position_element_right(self._current._temp_for_statement)
			if isinstance(self._current._temp_for_statement, AgentState):
				assert self._current._agent_state is not None 
				agd.set_position_element_left(self._current._agent_state)
				agd.set_position_element_right(self._current._temp_for_statement)
			if isinstance(self._current._temp_for_statement, Position) or isinstance(self._current._temp_for_statement, NameWithTwoRealValues):
				assert self._current._position is not None 
				agd.set_position_element_left(self._current._position)
				agd.set_position_element_right(self._current._temp_for_statement)
		else:
			print('Something get wrong with distance_statement! Check it!')
		self._current._ego_state = None
		self._current._agent_state = None
		self._current._agent_ground_truth = None
		self._current._position = None
		self._current._temp_for_statement = None


	def begin_perception_difference_statement(self, agd: PerceptionDifferenceStatement):
		pass


	def end_perception_difference_statement(self, agd: PerceptionDifferenceStatement):
		assert self._current._agent_state is not None
		assert self._current._agent_ground_truth is not None
		agd.set_agent_state(self._current._agent_state)
		agd.set_agent_ground_truth(self._current._agent_ground_truth)



	def begin_velocity_statement(self, agd: VelocityStatement):
		pass


	def end_velocity_statement(self, agd: VelocityStatement):
		if self._current._ego_state is not None and self._current._agent_state is not None:
			assert len(self._current._coordinate_expression) ==0
			assert self._current._agent_ground_truth is None
			agd.set_velocity_element_left(self._current._ego_state)
			agd.set_velocity_element_right(self._current._agent_state)
		elif self._current._ego_state is not None and self._current._agent_ground_truth is not None:
			assert len(self._current._coordinate_expression) ==0
			assert self._current._agent_state is None
			agd.set_velocity_element_left(self._current._ego_state)
			agd.set_velocity_element_right(self._current._agent_ground_truth)
		elif self._current._ego_state is not None and len(self._current._coordinate_expression)==1:
			assert self._current._agent_ground_truth is None
			assert self._current._agent_state is None
			agd.set_velocity_element_left(self._current._ego_state)
			agd.set_velocity_element_right(self._current._coordinate_expression[-1])
			self._current._coordinate_expression.pop()
		elif self._current._agent_state is not None and self._current._agent_ground_truth is not None:
			assert len(self._current._coordinate_expression) ==0
			assert self._current._ego_state is None
			agd.set_velocity_element_left(self._current._agent_state)
			agd.set_velocity_element_right(self._current._agent_ground_truth)
		elif self._current._agent_state is not None and len(self._current._coordinate_expression)==1:
			assert self._current._agent_ground_truth is None
			assert self._current._ego_state is None
			agd.set_velocity_element_left(self._current._agent_state)
			agd.set_velocity_element_right(self._current._coordinate_expression[-1])
			self._current._coordinate_expression.pop()
		elif self._current._agent_ground_truth is not None and len(self._current._coordinate_expression)==1:
			assert self._current._agent_state is None
			assert self._current._ego_state is None
			agd.set_velocity_element_left(self._current._agent_ground_truth)
			agd.set_velocity_element_right(self._current._coordinate_expression[-1])
			self._current._coordinate_expression.pop()
		elif len(self._current._coordinate_expression)==2:
			assert self._current._agent_ground_truth is None
			assert self._current._agent_state is None
			assert self._current._ego_state is None
			agd.set_velocity_element_left(self._current._coordinate_expression[-2])
			agd.set_velocity_element_right(self._current._coordinate_expression[-1])
			self._current._coordinate_expression.pop()
			self._current._coordinate_expression.pop()
		elif self._current._temp_for_statement is not None:
			if isinstance(self._current._temp_for_statement, AgentGroundTruth):
				assert self._current._agent_ground_truth is not None 
				agd.set_velocity_element_left(self._current._agent_ground_truth)
				agd.set_velocity_element_right(self._current._temp_for_statement)
			if isinstance(self._current._temp_for_statement, EgoState):
				assert self._current._ego_state is not None 
				agd.set_velocity_element_left(self._current._ego_state)
				agd.set_velocity_element_right(self._current._temp_for_statement)
			if isinstance(self._current._temp_for_statement, AgentState):
				assert self._current._agent_state is not None 
				agd.set_velocity_element_left(self._current._agent_state)
				agd.set_velocity_element_right(self._current._temp_for_statement)
			# if isinstance(self._current._temp_for_statement, Position) or isinstance(self._current._temp_for_statement, NameWithTwoRealValues) or isinstance(self._current._temp_for_statement, Coordinate):
			#   assert self._current._coordinate is not None 
			#   agd.set_velocity_element_left(self._current._coordinate)
			#   agd.set_velocity_element_right(self._current._temp_for_statement)
		else:
			print('Something get wrong with velocity_statement! Check it!')
		self._current._ego_state = None
		self._current._agent_state = None
		self._current._agent_ground_truth = None
		# self._current._coordinate = None
		# self._current._temp_for_statement = None


	def begin_speed_statement(self, agd: SpeedStatement):
		pass

	def end_speed_statement(self, agd: SpeedStatement):
		if self._current._ego_state is not None and self._current._agent_state is not None:
			assert self._current._speed is None
			assert self._current._agent_ground_truth is None
			agd.set_speed_element_left(self._current._ego_state)
			agd.set_speed_element_right(self._current._agent_state)
		elif self._current._ego_state is not None and self._current._agent_ground_truth is not None:
			assert self._current._speed is None
			assert self._current._agent_state is None
			agd.set_speed_element_left(self._current._ego_state)
			agd.set_speed_element_right(self._current._agent_ground_truth)
		elif self._current._ego_state is not None and self._current._speed is not None:
			assert self._current._agent_ground_truth is None
			assert self._current._agent_state is None
			agd.set_speed_element_left(self._current._ego_state)
			agd.set_speed_element_right(self._current._speed)
		elif self._current._agent_state is not None and self._current._agent_ground_truth is not None:
			assert self._current._speed is None
			assert self._current._ego_state is None
			agd.set_speed_element_left(self._current._agent_state)
			agd.set_speed_element_right(self._current._agent_ground_truth)
		elif self._current._agent_state is not None and self._current._speed is not None:
			assert self._current._agent_ground_truth is None
			assert self._current._ego_state is None
			agd.set_speed_element_left(self._current._agent_state)
			agd.set_speed_element_right(self._current._speed)
		elif self._current._agent_ground_truth is not None and self._current._speed is not None:
			assert self._current._agent_state is None
			assert self._current._ego_state is None
			agd.set_speed_element_left(self._current._agent_ground_truth)
			agd.set_speed_element_right(self._current._speed)
		elif self._current._temp_for_statement is not None:
			if isinstance(self._current._temp_for_statement, AgentGroundTruth):
				assert self._current._agent_ground_truth is not None 
				agd.set_speed_element_left(self._current._agent_ground_truth)
				agd.set_speed_element_right(self._current._temp_for_statement)
			if isinstance(self._current._temp_for_statement, EgoState):
				assert self._current._ego_state is not None 
				agd.set_speed_element_left(self._current._ego_state)
				agd.set_speed_element_right(self._current._temp_for_statement)
			if isinstance(self._current._temp_for_statement, AgentState):
				assert self._current._agent_state is not None 
				agd.set_speed_element_left(self._current._agent_state)
				agd.set_speed_element_right(self._current._temp_for_statement)
			if isinstance(self._current._temp_for_statement, Speed) or isinstance(self._current._temp_for_statement, NameWithRealValue):
				assert self._current._speed is not None 
				agd.set_speed_element_left(self._current._speed)
				agd.set_speed_element_right(self._current._temp_for_statement)
		else:
			print('Something get wrong with speed_statement! Check it!')
		self._current._ego_state = None
		self._current._agent_state = None
		self._current._agent_ground_truth = None
		self._current._speed = None
		self._current._temp_for_statement = None


	def begin_acceration_statement(self, agd: AccelerationStatement):
		pass

	def end_acceration_statement(self, agd: AccelerationStatement):
		if self._current._ego_state is not None and self._current._agent_state is not None:
			assert len(self._current._coordinate_expression) ==0
			assert self._current._agent_ground_truth is None
			agd.set_acceleration_element_left(self._current._ego_state)
			agd.set_acceleration_element_right(self._current._agent_state)
		elif self._current._ego_state is not None and self._current._agent_ground_truth is not None:
			assert len(self._current._coordinate_expression) ==0
			assert self._current._agent_state is None
			agd.set_acceleration_element_left(self._current._ego_state)
			agd.set_acceleration_element_right(self._current._agent_ground_truth)
		elif self._current._ego_state is not None and len(self._current._coordinate_expression)==1:
			assert self._current._agent_ground_truth is None
			assert self._current._agent_state is None
			agd.set_acceleration_element_left(self._current._ego_state)
			agd.set_acceleration_element_right(self._current._coordinate_expression[-1])
			self._current._coordinate_expression.pop()
		elif self._current._agent_state is not None and self._current._agent_ground_truth is not None:
			assert len(self._current._coordinate_expression) ==0
			assert self._current._ego_state is None
			agd.set_acceleration_element_left(self._current._agent_state)
			agd.set_acceleration_element_right(self._current._agent_ground_truth)
		elif self._current._agent_state is not None and len(self._current._coordinate_expression)==1:
			assert self._current._agent_ground_truth is None
			assert self._current._ego_state is None
			agd.set_acceleration_element_left(self._current._agent_state)
			agd.set_acceleration_element_right(self._current._coordinate_expression[-1])
			self._current._coordinate_expression.pop()
		elif self._current._agent_ground_truth is not None and len(self._current._coordinate_expression)==1:
			assert self._current._agent_state is None
			assert self._current._ego_state is None
			agd.set_acceleration_element_left(self._current._agent_ground_truth)
			agd.set_acceleration_element_right(self._current._coordinate_expression[-1])
			self._current._coordinate_expression.pop()
		elif len(self._current._coordinate_expression)==2:
			assert self._current._agent_ground_truth is None
			assert self._current._agent_state is None
			assert self._current._ego_state is None
			agd.set_acceleration_element_left(self._current._coordinate_expression[-2])
			agd.set_acceleration_element_right(self._current._coordinate_expression[-1])
			self._current._coordinate_expression.pop()
			self._current._coordinate_expression.pop()
		elif self._current._temp_for_statement is not None:
			if isinstance(self._current._temp_for_statement, AgentGroundTruth):
				assert self._current._agent_ground_truth is not None 
				agd.set_acceleration_element_left(self._current._agent_ground_truth)
				agd.set_acceleration_element_right(self._current._temp_for_statement)
			if isinstance(self._current._temp_for_statement, EgoState):
				assert self._current._ego_state is not None 
				agd.set_acceleration_element_left(self._current._ego_state)
				agd.set_acceleration_element_right(self._current._temp_for_statement)
			if isinstance(self._current._temp_for_statement, AgentState):
				assert self._current._agent_state is not None 
				agd.set_acceleration_element_left(self._current._agent_state)
				agd.set_acceleration_element_right(self._current._temp_for_statement)
			# if isinstance(self._current._temp_for_statement, Position) or isinstance(self._current._temp_for_statement, NameWithTwoRealValues) or isinstance(self._current._temp_for_statement, Coordinate):
			#   assert self._current._coordinate is not None 
			#   agd.set_velocity_element_left(self._current._coordinate)
			#   agd.set_velocity_element_right(self._current._temp_for_statement)
		else:
			print('Something get wrong with acceration_statement! Check it!')
		self._current._ego_state = None
		self._current._agent_state = None
		self._current._agent_ground_truth = None
	

	def act_on_distance_statement(self, name: AnyStr):
		#assert self._current._distance_statement is not None
		assert len(self._current._general_atom_statements_list)==1
		self._current._general_atom_statements_list[-1].set_name(name)
		self.finish_distance_statement(self._current._general_atom_statements_list[-1])

	def finish_distance_statement(self, agd: GeneralDistanceStatement):
		self._ast.add_ast_node(agd)





	def act_on_perception_difference_statement(self, name: AnyStr):
		# assert self._current._perception_difference_statement is not None
		# self._current._perception_difference_statement.set_name(name)
		# self.finish_perception_difference_statement(self._current._perception_difference_statement)
		assert len(self._current._general_atom_statements_list)==1
		self._current._general_atom_statements_list[-1].set_name(name)
		self.finish_perception_difference_statement(self._current._general_atom_statements_list[-1])

	def finish_perception_difference_statement(self, agd: PerceptionDifferenceStatement):
		self._ast.add_ast_node(agd)



	def act_on_velocity_statement(self, name: AnyStr):
		# assert self._current._velocity_statement is not None
		# self._current._velocity_statement.set_name(name)
		# #print(name)
		# self.finish_velocity_statement(self._current._velocity_statement)
		assert len(self._current._general_atom_statements_list)==1
		self._current._general_atom_statements_list[-1].set_name(name)
		self.finish_velocity_statement(self._current._general_atom_statements_list[-1])

	def finish_velocity_statement(self, agd: VelocityStatement):
		self._ast.add_ast_node(agd)




	def act_on_speed_statement(self, name: AnyStr):
		# assert self._current._speed_statement is not None
		# self._current._speed_statement.set_name(name)
		# #print(name)
		# self.finish_speed_statement(self._current._speed_statement)
		assert len(self._current._general_atom_statements_list)==1
		self._current._general_atom_statements_list[-1].set_name(name)
		self.finish_speed_statement(self._current._general_atom_statements_list[-1])

	def finish_speed_statement(self, agd: SpeedStatement):
		self._ast.add_ast_node(agd)

	def act_on_acceleration_statement(self, name: AnyStr):
		# assert self._current._acceleration_statement is not None
		# self._current._acceleration_statement.set_name(name)
		# #print(name)
		# self.finish_acceleration_statement(self._current._acceleration_statement)
		assert len(self._current._general_atom_statements_list)==1
		self._current._general_atom_statements_list[-1].set_name(name)
		self.finish_acceleration_statement(self._current._general_atom_statements_list[-1])

	def finish_acceleration_statement(self, agd: AccelerationStatement):
		self._ast.add_ast_node(agd)




	def act_on_speed(self, name: AnyStr):
		assert self._current._speed is not None
		self._current._speed.set_name(name)
		#print(name)
		self.finish_speed(self._current._speed)

	def finish_speed(self, agd: Speed):
		#temp = copy.deepcopy(agd)
		self._ast.add_ast_node(agd)



	def act_on_coordinate(self, name: AnyStr):
		assert self._current._coordinate is not None
		self._current._coordinate.set_name(name)
		#print(name)
		self.finish_coordinate(self._current._coordinate)

	def finish_coordinate(self, agd: Coordinate):
		#temp = copy.deepcopy(agd)
		self._ast.add_ast_node(agd)


	def act_on_overall_statement(self, name: AnyStr):
		assert self._current._overall_statement is not None
		self._current._overall_statement.set_name(name)
		#print(name)
		self.finish_overall_statement(self._current._overall_statement)

	def finish_overall_statement(self, agd: OverallStatement):
		self._ast.add_ast_node(agd)


























	def begin_agent_error(self, ae: AgentError):
		pass

	def end_agent_error(self, ae: AgentError):
		assert self._current._agent_state is not None
		assert self._current._agent_ground_truth is not None
		ae.set_agent_state(self._current._agent_state)
		ae.set_agent_ground_truth(self._current._agent_ground_truth)

	def begin_agent_error_detection_assertion(self, eda: AgentErrorDetectionAssertion):
		pass

	def end_agent_error_detection_assertion(self, aeda: AgentErrorDetectionAssertion):
		assert self._current._agent_error is not None
		aeda.set_agent_error(self._current._agent_error)

	def begin_agent_safety_assertion(self, asa: AgentSafetyAssertion):
		pass

	def end_agent_safety_assertion(self, asa: AgentSafetyAssertion):
		assert self._current._ego_state is not None
		assert self._current._agent_state is not None
		asa.set_ego_state(self._current._ego_state)
		asa.set_agent_state(self._current._agent_state)

	def begin_ego_speed(self, es: EgoSpeed):
		pass

	def end_ego_speed(self, es: EgoSpeed):
		assert self._current._coordinate is not None
		es.set_velocity(self._current._coordinate)

	def begin_detection_assertion(self, ds: DetectionAssertion):
		pass

	def end_detection_assertion(self, ds: DetectionAssertion):
		# Do not add detection assertion here,
		# because they will auto be added.
		pass

	def begin_safety_assertion(self, sa: SafetyAssertion):
		pass

	def end_safety_assertion(self, sa: SafetyAssertion):
		# Do not add detection assertion here,
		# because they will auto be added.
		pass



	def act_on_detection_assertion(self, name: AnyStr):
		assert self._current._detection_assertion is not None
		self._current._detection_assertion.set_name(name)
		self.finish_detection_assertion(self._current._detection_assertion)
		#print("This  is a test for detection")
		#print(name)

	def finish_detection_assertion(self, da: DetectionAssertion):
		self._ast.add_ast_node(da)

	def act_on_safety_assertion(self, name: AnyStr):
		assert self._current._safety_assertion is not None
		self._current._safety_assertion.set_name(name)
		self.finish_safety_assertion(self._current._safety_assertion)
		#print("This  is a test for safety")
		#print(name)

	def finish_safety_assertion(self, sa: SafetyAssertion):
		self._ast.add_ast_node(sa)

	def act_on_intersection_assertion(self, name: AnyStr):
		assert self._current._intersection_assertion is not None
		self._current._intersection_assertion.set_name(name)
		self.finish_intersection_assertion(self._current._intersection_assertion)

	def finish_intersection_assertion(self, ia: IntersectionAssertion):
		self._ast.add_ast_node(ia)

	def act_on_speed_constraint_assertion(self, name: AnyStr):
		assert self._current._speed_constraint_assertion is not None
		self._current._speed_constraint_assertion.set_name(name)
		self.finish_speed_constraint_assertion(self._current._speed_constraint_assertion)

	def finish_speed_constraint_assertion(self, sca: SpeedConstraintAssertion):
		self._ast.add_ast_node(sca)

	def handle_assertion(self, trace: Trace, assertion: Union[
		DetectionAssertion, SafetyAssertion, IntersectionAssertion, SpeedConstraintAssertion]):
		if isinstance(assertion, DetectionAssertion):
			trace.add_detection_assertion(assertion)
		elif isinstance(assertion, SafetyAssertion):
			trace.add_safety_assertion(assertion)
		elif isinstance(assertion, IntersectionAssertion):
			trace.add_intersection_assertion(assertion)
		elif isinstance(assertion, SpeedConstraintAssertion):
			trace.add_speed_constraint_assertion(assertion)
		self.finish_assign_assertion_to_trace(trace, assertion)

	def finish_assign_assertion_to_trace(self, t: Trace, a: Union[DetectionAssertion, SafetyAssertion
	, IntersectionAssertion, SpeedConstraintAssertion]):
		# Construct a temporary AssignAssertionToTrace just for dumping
		tmp = AssignAssertionToTrace()
		tmp.set_trace(t)
		tmp.set_assertion(a)
		self._ast.add_ast_node(tmp)

	# other functions
	# v:'(R,G,B)'
	# grammar syntax guarantees that we can match this successfully.
	def parse_rgb_color_internal(self, v: AnyStr) -> RGBColor:
		pattern = re.compile(r'^\( *([0-9]+) *, *([0-9]+) *, *([0-9]+) *\)$')
		result = re.match(pattern, v)
		assert result is not None
		assert len(result.groups()) == 3
		return RGBColor(int(result.group(1)), int(result.group(2)), int(result.group(3)))

	def parse_time_from_internal(self, v: AnyStr) -> Time:
		# print(v)
		pattern = re.compile(r'^([0-9][0-9]):([0-9][0-9])$')
		result = re.match(pattern, v)
		if result is None:
			pattern = re.compile(r'^([0-9]):([0-9][0-9])$')
			result = re.match(pattern, v)
		assert len(result.groups()) == 2
		return Time(int(result.group(1)), int(result.group(2)))



# This is the main entry.
class ASTListener(AVScenariosListener):

	def __init__(self, sema: Sema):
		self._sema = sema
		self._current = sema._current

	def enterEntry(self, ctx: AVScenariosParser.EntryContext):
		pass

	def exitEntry(self, ctx: AVScenariosParser.EntryContext):
		# complete the whole grammar parsing
		self._sema.finish_sema()

	def enterAssigns(self, ctx: AVScenariosParser.AssignsContext):
		pass

	def exitAssigns(self, ctx: AVScenariosParser.AssignsContext):
		pass

	# Enter a parse tree produced by AVScenariosParser#rv.
	def enterRv(self, ctx:AVScenariosParser.RvContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#rv.
	def exitRv(self, ctx:AVScenariosParser.RvContext):
		print('Exit Rv: '+ctx.getText())
		pass


	# Real value related operations
	def enterReal_value_of_real_value_expression(self, ctx:AVScenariosParser.Real_value_of_real_value_expressionContext):
		pass

	def exitReal_value_of_real_value_expression(self, ctx:AVScenariosParser.Real_value_of_real_value_expressionContext):
		# print('Exit Real_value_of_real_value_expression: '+ctx.getText()+'  length'+str(len(ctx.children)))
		self._current._real_value_expression.append(float(ctx.getText()))
		# print(self._current._real_value_expression)


	def enterCifang_of_real_value_expression(self, ctx:AVScenariosParser.Cifang_of_real_value_expressionContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#cifang_of_real_value_expression.
	def exitCifang_of_real_value_expression(self, ctx:AVScenariosParser.Cifang_of_real_value_expressionContext):
		# print('Exit Cifang_of_real_value_expression:  '+ctx.getText())
		assert len(self._current._real_value_expression)>=2
		if ctx.children[1].getText()=='^':
			self._current._real_value_expression[-2]=math.pow(self._current._real_value_expression[-2],self._current._real_value_expression[-1])
			self._current._real_value_expression.pop()
		else:
			print('Fatal: Wrong with Plus or ^ of real value expression!')
		# print(self._current._real_value_expression)

	# Enter a parse tree produced by AVScenariosParser#Multi_of_real_value_expression.
	def enterMulti_of_real_value_expression(self, ctx:AVScenariosParser.Multi_of_real_value_expressionContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#Multi_of_real_value_expression.
	def exitMulti_of_real_value_expression(self, ctx:AVScenariosParser.Multi_of_real_value_expressionContext):
		# print('Exit Multi_of_real_value_expression:  '+ctx.getText())
		if len(self._current._real_value_expression)>=2:
			if ctx.children[1].getText()=='*':
				self._current._real_value_expression[-2]=self._current._real_value_expression[-2]*self._current._real_value_expression[-1]
				self._current._real_value_expression.pop()
			elif ctx.children[1].getText()=='/':
				self._current._real_value_expression[-2]=self._current._real_value_expression[-2]/self._current._real_value_expression[-1]
				self._current._real_value_expression.pop()
			else:
				print('Fatal: Wrong with + or - of real value expression!')
		elif len(self._current._coordinate_expression)>=2:
			assert len(self._current._coordinate_expression)>1
			temp_left = []
			temp_right = []
			if isinstance(self._current._coordinate_expression[-1] , Coordinate):
				if self._current._coordinate_expression[-1].has_z():
					temp_right.append(self._current._coordinate_expression[-1].get_x())
					temp_right.append(self._current._coordinate_expression[-1].get_y())
					temp_right.append(self._current._coordinate_expression[-1].get_z())
				else:
					temp_right.append(self._current._coordinate_expression[-1].get_x())
					temp_right.append(self._current._coordinate_expression[-1].get_y())
				self._current._coordinate_expression.pop()
			elif isinstance(self._current._coordinate_expression[-1] , NameWithTwoRealValues):
				temp_right.append(self._current._coordinate_expression[-1].get_value()[0])
				temp_right.append(self._current._coordinate_expression[-1].get_value()[1])
				self._current._coordinate_expression.pop()
			elif isinstance(self._current._coordinate_expression[-1]  , Position):
				self._current._coordinate_expression[-1] = self._current._coordinate_expression[-1].get_coordinate()
				if self._current._coordinate_expression[-1].has_z():
					temp_right.append(self._current._coordinate_expression[-1].get_x())
					temp_right.append(self._current._coordinate_expression[-1].get_y())
					temp_right.append(self._current._coordinate_expression[-1].get_z())
				else:
					temp_right.append(self._current._coordinate_expression[-1].get_x())
					temp_right.append(self._current._coordinate_expression[-1].get_y())
				self._current._coordinate_expression.pop()

			if isinstance(self._current._coordinate_expression[-1] , Coordinate):
				if self._current._coordinate_expression[-1].has_z():
					temp_left.append(self._current._coordinate_expression[-1].get_x())
					temp_left.append(self._current._coordinate_expression[-1].get_y())
					temp_left.append(self._current._coordinate_expression[-1].get_z())
				else:
					temp_left.append(self._current._coordinate_expression[-1].get_x())
					temp_left.append(self._current._coordinate_expression[-1].get_y())
				self._current._coordinate_expression.pop()
			elif isinstance(self._current._coordinate_expression[-1] , NameWithTwoRealValues):
				temp_left.append(self._current._coordinate_expression[-1].get_value()[0])
				temp_left.append(self._current._coordinate_expression[-1].get_value()[1])
				self._current._coordinate_expression.pop()
			elif isinstance(self._current._coordinate_expression[-1]  , Position):
				self._current._coordinate_expression[-1] = self._current._coordinate_expression[-1].get_coordinate()
				if self._current._coordinate_expression[-1].has_z():
					temp_left.append(self._current._coordinate_expression[-1].get_x())
					temp_left.append(self._current._coordinate_expression[-1].get_y())
					temp_left.append(self._current._coordinate_expression[-1].get_z())
				else:
					temp_left.append(self._current._coordinate_expression[-1].get_x())
					temp_left.append(self._current._coordinate_expression[-1].get_y())
				self._current._coordinate_expression.pop()  
			
			assert len(temp_left) == len(temp_right)
			temp_left = array(temp_left)
			temp_right = array(temp_right)
			if ctx.children[1].getText()=='*':
				result = temp_left *  temp_right
			elif ctx.children[1].getText()=='/':
				result = temp_left /  temp_right
			if len(result)==3:
				self._current._coordinate_expression.append(Coordinate(result[0]
															   , result[1]
															   , result[2]))
			elif len(result)==2:
				self._current._coordinate_expression.append(Coordinate(result[0]
															   , result[1]))
			else:
				print('Length of result not fit!!!!')
		else:
			print('Something go wrong with exitMulti_of_real_value_expression')
		# print(self._current._real_value_expression)

	# Enter a parse tree produced by AVScenariosParser#Plus_of_real_value_expression.
	def enterPlus_of_real_value_expression(self, ctx:AVScenariosParser.Plus_of_real_value_expressionContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#Plus_of_real_value_expression.
	def exitPlus_of_real_value_expression(self, ctx:AVScenariosParser.Plus_of_real_value_expressionContext):
		# print('Exit Plus_of_real_value_expression:  '+ctx.getText())
		# print(self._current._real_value_expression)
		if len(self._current._real_value_expression)>=2:
			if ctx.children[1].getText()=='+':
				self._current._real_value_expression[-2]=self._current._real_value_expression[-2]+self._current._real_value_expression[-1]
				self._current._real_value_expression.pop()
			elif ctx.children[1].getText()=='-':
				self._current._real_value_expression[-2]=self._current._real_value_expression[-2]-self._current._real_value_expression[-1]
				self._current._real_value_expression.pop()
			else:
				print('Fatal: Wrong with Plus or Minus of real value expression!')
		elif len(self._current._general_atom_statements_list)>0:
			if self._current._overall_statement is None:
				self._current._overall_statement = OverallStatement()

				len_before = len(self._current._overall_statement.get_statements())


				for _i in range(len(self._current._general_atom_statements_list)):
					self._current._overall_statement.add_statement(self._current._general_atom_statements_list[_i])
				self._current._general_atom_statements_list=[]

				len_after = len(self._current._overall_statement.get_statements())
				if len_after > len_before:
					# print(ctx.children[1].getText())
					self._current._overall_statement.add_operator(ctx.children[1].getText())

				assert len_after-len_before>= 0

				if self._current._kuohao_of_statement is not None and len(self._current._kuohao_of_statement)>0: #and len_after-len_before!=0:
					# print('!!!!!!!!!111')
					self._current._kuohao_of_statement[-1].add_operator(self._current._overall_statement._operators[-1])
					self._current._overall_statement._operators.pop()
					if len_after-len_before>=2 or len(self._current._kuohao_of_statement[-1].get_statements())==0:#isinstance(ctx.parentCtx, AVScenariosParser.Atom_statement_overall_with_kuohaoContext):
						# print('???2')
						self._current._kuohao_of_statement[-1].add_statement(self._current._overall_statement._statements[-2])
						self._current._kuohao_of_statement[-1].add_statement(self._current._overall_statement._statements[-1])
						self._current._overall_statement._statements.pop() 
						self._current._overall_statement._statements.pop() 
					else:
						# print('???1')
						self._current._kuohao_of_statement[-1].add_statement(self._current._overall_statement._statements[-1])
						self._current._overall_statement._statements.pop()
					#print(self._current._kuohao_of_statement[-1])
					#print(self._current._kuohao_of_statement[-1]) 


				if isinstance(ctx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
					#print('233333333333333333333333333333333333333333333333333333333333333333')
					if ctx.parentCtx.parentCtx.children[2]==ctx.parentCtx:
						assert self._current._atom_statement_right is None
						self._current._atom_statement_right=self._current._overall_statement
						# print('Right')
						# print(self._current._overall_statement)
						self._current._overall_statement = None
					if ctx.parentCtx.parentCtx.children[0]==ctx.parentCtx:
						assert self._current._atom_statement_left is None
						self._current._atom_statement_left=self._current._overall_statement
						# print('Left')
						# print(self._current._overall_statement)
						self._current._overall_statement = None
		elif len(self._current._coordinate_expression)>0:
			assert len(self._current._coordinate_expression)>1
			temp_left = []
			temp_right = []
			if isinstance(self._current._coordinate_expression[-1] , Coordinate):
				if self._current._coordinate_expression[-1].has_z():
					temp_right.append(self._current._coordinate_expression[-1].get_x())
					temp_right.append(self._current._coordinate_expression[-1].get_y())
					temp_right.append(self._current._coordinate_expression[-1].get_z())
				else:
					temp_right.append(self._current._coordinate_expression[-1].get_x())
					temp_right.append(self._current._coordinate_expression[-1].get_y())
				self._current._coordinate_expression.pop()
			elif isinstance(self._current._coordinate_expression[-1] , NameWithTwoRealValues):
				temp_right.append(self._current._coordinate_expression[-1].get_value()[0])
				temp_right.append(self._current._coordinate_expression[-1].get_value()[1])
				self._current._coordinate_expression.pop()
			elif isinstance(self._current._coordinate_expression[-1]  , Position):
				self._current._coordinate_expression[-1] = self._current._coordinate_expression[-1].get_coordinate()
				if self._current._coordinate_expression[-1].has_z():
					temp_right.append(self._current._coordinate_expression[-1].get_x())
					temp_right.append(self._current._coordinate_expression[-1].get_y())
					temp_right.append(self._current._coordinate_expression[-1].get_z())
				else:
					temp_right.append(self._current._coordinate_expression[-1].get_x())
					temp_right.append(self._current._coordinate_expression[-1].get_y())
				self._current._coordinate_expression.pop()

			if isinstance(self._current._coordinate_expression[-1] , Coordinate):
				if self._current._coordinate_expression[-1].has_z():
					temp_left.append(self._current._coordinate_expression[-1].get_x())
					temp_left.append(self._current._coordinate_expression[-1].get_y())
					temp_left.append(self._current._coordinate_expression[-1].get_z())
				else:
					temp_left.append(self._current._coordinate_expression[-1].get_x())
					temp_left.append(self._current._coordinate_expression[-1].get_y())
				self._current._coordinate_expression.pop()
			elif isinstance(self._current._coordinate_expression[-1] , NameWithTwoRealValues):
				temp_left.append(self._current._coordinate_expression[-1].get_value()[0])
				temp_left.append(self._current._coordinate_expression[-1].get_value()[1])
				self._current._coordinate_expression.pop()
			elif isinstance(self._current._coordinate_expression[-1]  , Position):
				self._current._coordinate_expression[-1] = self._current._coordinate_expression[-1].get_coordinate()
				if self._current._coordinate_expression[-1].has_z():
					temp_left.append(self._current._coordinate_expression[-1].get_x())
					temp_left.append(self._current._coordinate_expression[-1].get_y())
					temp_left.append(self._current._coordinate_expression[-1].get_z())
				else:
					temp_left.append(self._current._coordinate_expression[-1].get_x())
					temp_left.append(self._current._coordinate_expression[-1].get_y())
				self._current._coordinate_expression.pop()  
			
			assert len(temp_left) == len(temp_right)
			temp_left = array(temp_left)
			temp_right = array(temp_right)
			if ctx.children[1].getText()=='+':
				result = temp_left +  temp_right
			elif ctx.children[1].getText()=='-':
				result = temp_left -  temp_right
			if len(result)==3:
				self._current._coordinate_expression.append(Coordinate(result[0]
															   , result[1]
															   , result[2]))
			elif len(result)==2:
				self._current._coordinate_expression.append(Coordinate(result[0]
															   , result[1]))
			else:
				print('Length of result not fit!!!!')

		# print(self._current._real_value_expression)







	# Enter a parse tree produced by AVScenariosParser#real_value_expression_id.
	def enterReal_value_expression_id(self, ctx:AVScenariosParser.Real_value_expression_idContext):
		# print('Enter Real_value_expression_id:  '+ ctx.getText())
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)


		#   name = ctx.getText()
		# ret = self._sema._ast.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[2].start.line, ctx.children[2].start.column
														, ctx.children[2].start.start - ctx.start.start,
														ctx.children[2].stop.stop - ctx.start.start
														, ctx.getText()))
			self._current._real_value_expression.append(None)
		else:
			n, index = ret
			if isinstance(n, NameWithRealValue):
				self._current._real_value_expression.append(n._value)
			elif isinstance(n, Coordinate):
				self._current._coordinate_expression.append(n)
				#   self._current._temp_for_statement = n
			elif isinstance(n, NameWithTwoRealValues):
				self._current._coordinate_expression.append(n)
				#   self._current._temp_for_statement = n
			elif isinstance(n , Position):
				self._current._coordinate_expression.append(n)

			elif isinstance(n, SingleGeneralAssertion):
				temp=SingleGeneralAssertion()
				temp.set_name(n.get_name())
				temp.add_assertion(n.get_assertion()) 
				self._current._general_assertion_list.append(temp)
				# print(self._current._general_assertion_list[-2].get_assertion())
				# print(self._current._general_assertion_list[-1].get_assertion())
				# print(len(self._current._general_assertion_list))
			elif isinstance(n, Speed):
				self._current._speed = n
				
			else:
				print('Wrong with Real_value_expression_id')

	# Exit a parse tree produced by AVScenariosParser#real_value_expression_id.
	def exitReal_value_expression_id(self, ctx:AVScenariosParser.Real_value_expression_idContext):
		pass





	# Enter a parse tree produced by AVScenariosParser#Plus_of_coordinate_expression.
	def enterPlus_of_coordinate_expression(self, ctx:AVScenariosParser.Plus_of_coordinate_expressionContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#Plus_of_coordinate_expression.
	def exitPlus_of_coordinate_expression(self, ctx:AVScenariosParser.Plus_of_coordinate_expressionContext):
		# print('Exit Plus_of_coordinate_expression:  '+ ctx.getText())
		assert len(self._current._coordinate_expression)>1
		temp_left = []
		temp_right = []
		if isinstance(self._current._coordinate_expression[-1] , Coordinate):
			if self._current._coordinate_expression[-1].has_z():
				temp_right.append(self._current._coordinate_expression[-1].get_x())
				temp_right.append(self._current._coordinate_expression[-1].get_y())
				temp_right.append(self._current._coordinate_expression[-1].get_z())
			else:
				temp_right.append(self._current._coordinate_expression[-1].get_x())
				temp_right.append(self._current._coordinate_expression[-1].get_y())
			self._current._coordinate_expression.pop()
		elif isinstance(self._current._coordinate_expression[-1] , NameWithTwoRealValues):
			temp_right.append(self._current._coordinate_expression[-1].get_value()[0])
			temp_right.append(self._current._coordinate_expression[-1].get_value()[1])
			self._current._coordinate_expression.pop()
		elif isinstance(self._current._coordinate_expression[-1]  , Position):
			self._current._coordinate_expression[-1] = self._current._coordinate_expression[-1].get_coordinate()
			if self._current._coordinate_expression[-1].has_z():
				temp_right.append(self._current._coordinate_expression[-1].get_x())
				temp_right.append(self._current._coordinate_expression[-1].get_y())
				temp_right.append(self._current._coordinate_expression[-1].get_z())
			else:
				temp_right.append(self._current._coordinate_expression[-1].get_x())
				temp_right.append(self._current._coordinate_expression[-1].get_y())
			self._current._coordinate_expression.pop()

		if isinstance(self._current._coordinate_expression[-1] , Coordinate):
			if self._current._coordinate_expression[-1].has_z():
				temp_left.append(self._current._coordinate_expression[-1].get_x())
				temp_left.append(self._current._coordinate_expression[-1].get_y())
				temp_left.append(self._current._coordinate_expression[-1].get_z())
			else:
				temp_left.append(self._current._coordinate_expression[-1].get_x())
				temp_left.append(self._current._coordinate_expression[-1].get_y())
			self._current._coordinate_expression.pop()
		elif isinstance(self._current._coordinate_expression[-1] , NameWithTwoRealValues):
			temp_left.append(self._current._coordinate_expression[-1].get_value()[0])
			temp_left.append(self._current._coordinate_expression[-1].get_value()[1])
			self._current._coordinate_expression.pop()
		elif isinstance(self._current._coordinate_expression[-1]  , Position):
			self._current._coordinate_expression[-1] = self._current._coordinate_expression[-1].get_coordinate()
			if self._current._coordinate_expression[-1].has_z():
				temp_left.append(self._current._coordinate_expression[-1].get_x())
				temp_left.append(self._current._coordinate_expression[-1].get_y())
				temp_left.append(self._current._coordinate_expression[-1].get_z())
			else:
				temp_left.append(self._current._coordinate_expression[-1].get_x())
				temp_left.append(self._current._coordinate_expression[-1].get_y())
			self._current._coordinate_expression.pop()  
		
		assert len(temp_left) == len(temp_right)
		temp_left = array(temp_left)
		temp_right = array(temp_right)
		if ctx.children[1].getText()=='+':
			result = temp_left +  temp_right
		elif ctx.children[1].getText()=='-':
			result = temp_left -  temp_right
		if len(result)==3:
			self._current._coordinate_expression.append(Coordinate(result[0]
														   , result[1]
														   , result[2]))
		elif len(result)==2:
			self._current._coordinate_expression.append(Coordinate(result[0]
														   , result[1]))
		else:
			print('Length of result not fit!!!!')


			



	# Enter a parse tree produced by AVScenariosParser#coordinate_expression_id.
	def enterCoordinate_expression_id(self, ctx:AVScenariosParser.Coordinate_expression_idContext):
		# print('Enter Coordinate_expression_id:  '+ctx.getText())
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)


		#   name = ctx.getText()
		# ret = self._sema._ast.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[2].start.line, ctx.children[2].start.column
														, ctx.children[2].start.start - ctx.start.start,
														ctx.children[2].stop.stop - ctx.start.start
														, ctx.getText()))
			self._current._real_value_expression.append(None)
		else:
			n, index = ret
			if isinstance(n, Coordinate):
				self._current._coordinate_expression.append(n)
				#   self._current._temp_for_statement = n
			elif isinstance(n, NameWithTwoRealValues):
				self._current._coordinate_expression.append(n)
				#   self._current._temp_for_statement = n
			elif isinstance(n , Position):
				self._current._coordinate_expression.append(n)

			elif isinstance(n, SingleGeneralAssertion):
				temp=SingleGeneralAssertion()
				temp.set_name(n.get_name())
				temp.add_assertion(n.get_assertion()) 
				self._current._general_assertion_list.append(temp)
				# print(self._current._general_assertion_list[-2].get_assertion())
				# print(self._current._general_assertion_list[-1].get_assertion())
				# print(len(self._current._general_assertion_list))

			else:
				print('Wrong with Real_value_expression_id')

	# Exit a parse tree produced by AVScenariosParser#coordinate_expression_id.
	def exitCoordinate_expression_id(self, ctx:AVScenariosParser.Coordinate_expression_idContext):
		pass


	# Enter a parse tree produced by AVScenariosParser#coordinate_of_coordinate_expression.
	def enterCoordinate_of_coordinate_expression(self, ctx:AVScenariosParser.Coordinate_of_coordinate_expressionContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#coordinate_of_coordinate_expression.
	def exitCoordinate_of_coordinate_expression(self, ctx:AVScenariosParser.Coordinate_of_coordinate_expressionContext):
		pass


	# Enter a parse tree produced by AVScenariosParser#kuohao_of_coordinate_expression.
	def enterKuohao_of_coordinate_expression(self, ctx:AVScenariosParser.Kuohao_of_coordinate_expressionContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#kuohao_of_coordinate_expression.
	def exitKuohao_of_coordinate_expression(self, ctx:AVScenariosParser.Kuohao_of_coordinate_expressionContext):
		pass


	# Enter a parse tree produced by AVScenariosParser#Muti_of_coordinate_expression.
	def enterMuti_of_coordinate_expression(self, ctx:AVScenariosParser.Muti_of_coordinate_expressionContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#Muti_of_coordinate_expression.
	def exitMuti_of_coordinate_expression(self, ctx:AVScenariosParser.Muti_of_coordinate_expressionContext):
		# print('Exit Muti_of_coordinate_expression:  '+ ctx.getText())
		assert len(self._current._coordinate_expression)>1
		temp_left = []
		temp_right = []
		if isinstance(self._current._coordinate_expression[-1] , Coordinate):
			if self._current._coordinate_expression[-1].has_z():
				temp_right.append(self._current._coordinate_expression[-1].get_x())
				temp_right.append(self._current._coordinate_expression[-1].get_y())
				temp_right.append(self._current._coordinate_expression[-1].get_z())
			else:
				temp_right.append(self._current._coordinate_expression[-1].get_x())
				temp_right.append(self._current._coordinate_expression[-1].get_y())
			self._current._coordinate_expression.pop()
		elif isinstance(self._current._coordinate_expression[-1] , NameWithTwoRealValues):
			temp_right.append(self._current._coordinate_expression[-1].get_value()[0])
			temp_right.append(self._current._coordinate_expression[-1].get_value()[1])
			self._current._coordinate_expression.pop()
		elif isinstance(self._current._coordinate_expression[-1]  , Position):
			self._current._coordinate_expression[-1] = self._current._coordinate_expression[-1].get_coordinate()
			if self._current._coordinate_expression[-1].has_z():
				temp_right.append(self._current._coordinate_expression[-1].get_x())
				temp_right.append(self._current._coordinate_expression[-1].get_y())
				temp_right.append(self._current._coordinate_expression[-1].get_z())
			else:
				temp_right.append(self._current._coordinate_expression[-1].get_x())
				temp_right.append(self._current._coordinate_expression[-1].get_y())
			self._current._coordinate_expression.pop()

		if isinstance(self._current._coordinate_expression[-1] , Coordinate):
			if self._current._coordinate_expression[-1].has_z():
				temp_left.append(self._current._coordinate_expression[-1].get_x())
				temp_left.append(self._current._coordinate_expression[-1].get_y())
				temp_left.append(self._current._coordinate_expression[-1].get_z())
			else:
				temp_left.append(self._current._coordinate_expression[-1].get_x())
				temp_left.append(self._current._coordinate_expression[-1].get_y())
			self._current._coordinate_expression.pop()
		elif isinstance(self._current._coordinate_expression[-1] , NameWithTwoRealValues):
			temp_left.append(self._current._coordinate_expression[-1].get_value()[0])
			temp_left.append(self._current._coordinate_expression[-1].get_value()[1])
			self._current._coordinate_expression.pop()
		elif isinstance(self._current._coordinate_expression[-1]  , Position):
			self._current._coordinate_expression[-1] = self._current._coordinate_expression[-1].get_coordinate()
			if self._current._coordinate_expression[-1].has_z():
				temp_left.append(self._current._coordinate_expression[-1].get_x())
				temp_left.append(self._current._coordinate_expression[-1].get_y())
				temp_left.append(self._current._coordinate_expression[-1].get_z())
			else:
				temp_left.append(self._current._coordinate_expression[-1].get_x())
				temp_left.append(self._current._coordinate_expression[-1].get_y())
			self._current._coordinate_expression.pop()  
		
		assert len(temp_left) == len(temp_right)
		temp_left = array(temp_left)
		temp_right = array(temp_right)
		if ctx.children[1].getText()=='*':
			result = temp_left *  temp_right
		elif ctx.children[1].getText()=='/':
			result = temp_left /  temp_right
		if len(result)==3:
			self._current._coordinate_expression.append(Coordinate(result[0]
														   , result[1]
														   , result[2]))
		elif len(result)==2:
			self._current._coordinate_expression.append(Coordinate(result[0]
														   , result[1]))
		else:
			print('Length of result not fit!!!!')












	def enterAssign_operator_related_assignments(self, ctx: AVScenariosParser.Assign_operator_related_assignmentsContext):
		pass


	#scenario = creatscenario{...}
	def exitAssign_operator_related_assignments(self, ctx: AVScenariosParser.Assign_operator_related_assignmentsContext):
		# print('Exit Assign_operator_related_assignments:   '+ctx.getText())

		# print(ctx.getText())
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.start - ctx.start.start,
														   ctx.children[0].stop.stop - ctx.start.start
														   , ctx.getText()))
		else:  # Redefinition,do not add the node
			if len(self._current._string_expression)==1:
				assert self._current._overall_statement is None

				# print('Exit Assign_str:   '+ctx.getText())
				# record it to the self._current._lane_id_contexts
				self._current._lane_id_contexts.append(ctx)
				#self._sema.act_on_name_with_string(name, ctx.children[2].getText()[1:-1])
				self._sema.act_on_name_with_string(name, self._current._string_expression[-1])
				self._current._string_expression.pop()
			elif self._current._overall_statement is not None:
				# print('Exit  Assign_atom_statement_overall: '+ ctx.getText())
				self._sema.act_on_overall_statement(name)   
				self._current._overall_statement = None 
			elif len(self._current._real_value_expression)==1:
				# record it to the self._current._intersection_id_or_weather_continuous_index_contexts
				self._current._intersection_id_or_weather_continuous_index_contexts.append(ctx)
				self._sema.act_on_name_with_real_value(name, self._current._real_value_expression[-1])
				# print(self._current._real_value_expression[-1])
				# print(ctx)
				self._current._real_value_expression.pop()
				# self._sema.act_on_name_with_real_value(name, float(ctx.children[2].getText()))
			elif len(self._current._coordinate_expression)==1:
				# print(self._current._coordinate_expression[-1])
				# print()
				temp = self._current._coordinate_expression[-1]
				temp.set_name(name)
				# print(name)
				# self._current._coordinate_expression[-1].set_name(name)
				self._sema._ast.add_ast_node(temp)

				# ret=self._sema._ast.find_node(name)
				# n1,n2=ret
				# print('######')
				# print(n1)
				# print(n2)
				# print('######')
				# print(self._current._coordinate_expression[-1])
				# print(self._current._coordinate_expression[-1].get_name())
				self._current._coordinate_expression.pop()
			else:
				print('Something go wrong with Assign_operator_related_assignments')



	# Enter a parse tree produced by AVScenariosParser#assign_special_case_of_coordinate.
	def enterAssign_special_case_of_coordinate(self, ctx:AVScenariosParser.Assign_special_case_of_coordinateContext):
		name = ctx.children[3].getText()
		# print('enterAssign_special_case_of_coordinate:  '+ctx.getText() + '      '+name)
		ret = self._sema.find_node(name)
		#   name = ctx.getText()
		# ret = self._sema._ast.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[2].start.line, ctx.children[2].start.column
														, ctx.children[2].start.start - ctx.start.start,
														ctx.children[2].stop.stop - ctx.start.start
														, ctx.getText()))
			self._current._coordinate_expression.append(None)
			# print('!!!!!!!!!!!')
		else:
			n, index = ret
			if isinstance(n, Coordinate):
				self._current._coordinate_expression.append(n)
				#   self._current._temp_for_statement = n
			elif isinstance(n, NameWithTwoRealValues):
				self._current._coordinate_expression.append(n)
				#   self._current._temp_for_statement = n
			elif isinstance(n , Position):
				self._current._coordinate_expression.append(n)
				# print(self._current._general_assertion_list[-2].get_assertion())
				# print(self._current._general_assertion_list[-1].get_assertion())
				# print(len(self._current._general_assertion_list))

			else:
				print('Wrong with Real_value_expression_id')




	# Exit a parse tree produced by AVScenariosParser#assign_special_case_of_coordinate.
	def exitAssign_special_case_of_coordinate(self, ctx:AVScenariosParser.Assign_special_case_of_coordinateContext):
		name = ctx.children[0].getText()
		# print('exitAssign_special_case_of_coordinate: '+ctx.getText())
		# print(self._current._coordinate_expression)
		assert len(self._current._coordinate_expression)==1
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start,
														   ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			# we meet a position
			if isinstance(self._current._coordinate_expression[-1], Coordinate):
				if self._current._coordinate_expression[-1].has_z():
					self._sema.act_on_coordinate_position(name
														  , ctx.children[2].getText()
														  , self._current._coordinate_expression[-1].get_x
														  , self._current._coordinate_expression[-1].get_y
														  , self._current._coordinate_expression[-1].get_z)
				else:
					self._sema.act_on_coordinate_position(name
														  , ctx.children[2].getText()
														  , self._current._coordinate_expression[-1].get_x
														  , self._current._coordinate_expression[-1].get_y)
				self._current._coordinate_expression.pop()
			elif isinstance(self._current._coordinate_expression[-1], NameWithTwoRealValues):
				self._sema.act_on_coordinate_position(name
														  , ctx.children[2].getText()
														  , self._current._coordinate_expression[-1].get_value()[0]
														  , self._current._coordinate_expression[-1].get_value()[1])
				self._current._coordinate_expression.pop()
			elif isinstance(self._current._coordinate_expression[-1], Position):
				self._current._coordinate_expression[-1] = self._current._coordinate_expression[-1].get_coordinate()
				if self._current._coordinate_expression[-1].has_z():
					self._sema.act_on_coordinate_position(name
														  , ctx.children[2].getText()
														  , self._current._coordinate_expression[-1].get_x
														  , self._current._coordinate_expression[-1].get_y
														  , self._current._coordinate_expression[-1].get_z)
				else:
					self._sema.act_on_coordinate_position(name
														  , ctx.children[2].getText()
														  , self._current._coordinate_expression[-1].get_x
														  , self._current._coordinate_expression[-1].get_y)
				self._current._coordinate_expression.pop()
			else:
				print('Something wrong with exitAssign_special_case_of_coordinate')





	# strat dealing with the assignment_statements related to scenario creation
	def enterAssign_scenario(self, ctx: AVScenariosParser.Assign_scenarioContext):
		pass

	#scenario = creatscenario{...}
	def exitAssign_scenario(self, ctx: AVScenariosParser.Assign_scenarioContext):
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.start - ctx.start.start,
														   ctx.children[0].stop.stop - ctx.start.start
														   , ctx.getText()))
		else:  # Redefinition,do not add the node
			self._sema.act_on_scenario(name)
		self._current._scenario = None





	def enterAssign_ego(self, ctx: AVScenariosParser.Assign_egoContext):
		pass

	def exitAssign_ego(self, ctx: AVScenariosParser.Assign_egoContext):
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.start  - ctx.start.start,
														   ctx.children[0].stop.stop - ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_ego_vehicle(name)
		self._current._ego_vehicle = None

	def enterAssign_variable(self, ctx: AVScenariosParser.Assign_variableContext):
		# print('Assign_variable:  '+ctx.getText())
		#  ctx.children[1].getText()=='='
		#  ctx.children[2].getText()=='('
		name = ctx.children[0].getText()
		var = ctx.children[3].getText()
		ret = self._sema.find_node(var)
		if not ret:
			self._sema.add_error(UndefinedVariableError(var, ctx.children[3].start.line, ctx.children[3].start.column
														, ctx.children[3].start.start  - ctx.start.start,
														ctx.children[3].stop.stop - ctx.start.start
														, ctx.getText()))
			# For error
			ret = var
		else:
			v, index = ret
			if isinstance(v, Coordinate):
				p = Position(v.get_name())
				p.set_coordinate(v)
				v = p
				ret = v, index

				# print('name of coordinate: '+ name)
				# print(p)
			if not isinstance(v, Position) and not isinstance(v, NameWithTwoRealValues) \
					and not isinstance(v, Type) and not isinstance(v, NameWithString) \
					and not isinstance(v, State) and not isinstance(v,StateVehicleTypeStateListErrorType)\
					and not isinstance(v,StateStateListErrorType) and not isinstance(v,StateVehicleTypePedestrianTypeStateListErrorType):
				self._sema.add_error(IllegalTypeError(var, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.start  - ctx.start.start,
													  ctx.children[0].stop.stop - ctx.start.start
													  , ctx.getText(), v.__class__.__name__,
													  'State', 'Position', 'SpecificType', 'GeneralType'))
				# For error
				ret = var
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.start - ctx.start.start,
														   ctx.children[0].stop.stop - ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_name_with_one_variable(ctx.children[0].getText()
													 , ret)

	def exitAssign_variable(self, ctx: AVScenariosParser.Assign_variableContext):
		# print('exitAssign_variable')
		# print(len(self._current._coordinate_expression)>0)
		pass

	def enterAssign_name_two_variables(self, ctx: AVScenariosParser.Assign_name_two_variablesContext):
		# ctx.children[1].getText()=='='
		# ctx.children[2].getText()=='('
		# ctx.children[6].getText()==')'
		# print('Enter Assign_name_two_variables:  '+ctx.getText())
		flag = 0;
		name = ctx.children[0].getText()
		v1 = ctx.children[3].getText()
		v2 = ctx.children[5].getText()
		ret1 = self._sema.find_node(v1)
		ret2 = self._sema.find_node(v2)
		if not ret1:
			self._sema.add_error(UndefinedVariableError(v1, ctx.children[3].start.line
														, ctx.children[3].start.column
														, ctx.children[3].start.start - ctx.start.start
														, ctx.children[3].stop.stop - ctx.start.start
														, ctx.getText()))
			ret1=v1
			ret2=v2
		else:
			n1, index1 = ret1
			if not ret2:
				self._sema.add_error(UndefinedVariableError(v2, ctx.children[5].start.line
															, ctx.children[5].start.column
															, ctx.children[5].start.start  - ctx.start.start
															, ctx.children[5].stop.stop - ctx.start.start
															, ctx.getText()))
				ret2=v2
			else:
				n2, _ = ret2
				if isinstance(n1, NameWithRealValue) or isinstance(n1, NameWithRealValue):
					flag = 1
				elif isinstance(n1, Position) or isinstance(n1, NameWithTwoRealValues):
					if not isinstance(n2, Heading):
						self._sema.add_error(IllegalTypeError(v2, ctx.children[5].start.line
															  , ctx.children[5].start.column
															  , ctx.children[5].start.start - ctx.start.start
															  , ctx.children[5].stop.stop - ctx.start.start
															  , ctx.getText(), n2.__class__.__name__, 'Heading'))
						ret2=v2
				elif isinstance(n1, Type) or isinstance(n1, NameWithString):
					if not isinstance(n2, Color):
						self._sema.add_error(IllegalTypeError(v2, ctx.children[5].start.line
															  , ctx.children[5].start.column
															  , ctx.children[5].start.start - ctx.start.start
															  , ctx.children[5].stop.stop - ctx.start.start
															  , ctx.getText(), n2.__class__.__name__, 'RGBColor', 'ColorList'))
					ret2 = v2
				elif isinstance(n1, Height) or isinstance(n1,NameWithRealValue):
					if not isinstance(n2, Color):
						self._sema.add_error(IllegalTypeError(v2, ctx.children[5].start.line
															  , ctx.children[5].start.column
															  , ctx.children[5].start.start - ctx.start.start
															  , ctx.children[5].stop.stop - ctx.start.start
															  , ctx.getText(), n2.__class__.__name__, 'RGBColor', 'ColorList'))
					ret2 = v2
				elif isinstance(n1, State) or isinstance(n1,StateVehicleTypePedestrianTypeStateListErrorType)\
						or isinstance(n1,StateStateListErrorType) or isinstance(n1,StateVehicleTypeStateListErrorType):
					if not isinstance(n2, State) and not isinstance(n2,StateVehicleTypePedestrianTypeStateListErrorType)\
						and not isinstance(n2,StateStateListErrorType) and not isinstance(n2,StateVehicleTypeStateListErrorType):
						self._sema.add_error(IllegalTypeError(v2, ctx.children[5].start.line
															  , ctx.children[5].start.column
															  , ctx.children[5].start.start - ctx.start.start
															  , ctx.children[5].stop.stop - ctx.start.start
															  , ctx.getText(), n2.__class__.__name__, 'State'))
					ret2 = v2
				else:
					self._sema.add_error(IllegalTypeError(v1, ctx.children[3].start.line
														  , ctx.children[3].start.column
														  , ctx.children[3].start.start - ctx.start.start
														  , ctx.children[3].stop.stop - ctx.start.start
														  , ctx.getText(), n1.__class__.__name__
														  , 'Position', 'Type', 'Height', 'State'))
					ret1 = v1
					ret2 = v2
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line
														   , ctx.children[0].start.column
														   , ctx.children[0].start.start  - ctx.start.start
														   , ctx.children[0].stop.stop - ctx.start.start
														   , ctx.getText()))
		else:
			if flag ==0 :
				self._sema.act_on_name_with_two_variables(name, ret1, ret2)
			else:
				self._sema.act_on_name_with_two_real_values(name
														, n1.get_value()
														, n2.get_value())
				# self._current._real_value_expression.pop()
				# self._current._real_value_expression.pop()

	def exitAssign_name_two_variables(self, ctx: AVScenariosParser.Assign_name_two_variablesContext):
		pass

	def enterAssign_name_three_variables(self, ctx: AVScenariosParser.Assign_name_three_variablesContext):
		# ctx.children[1].getText()=='='
		# ctx.children[2].getText()=='('
		# ctx.children[4].getText()==','
		# ctx.children[6].getText()==','
		# ctx.children[8].getText()==')'
		name = ctx.children[0].getText()
		v1 = ctx.children[3].getText()
		v2 = ctx.children[5].getText()
		v3 = ctx.children[7].getText()
		ret1 = self._sema.find_node(v1)
		ret2 = self._sema.find_node(v2)
		ret3 = self._sema.find_node(v3)
		if not ret1:
			self._sema.add_error(UndefinedVariableError(v1, ctx.children[3].start.line, ctx.children[3].start.column
														, ctx.children[3].start.start  - ctx.start.start,
														ctx.children[3].stop.stop - ctx.start.start
														, ctx.getText()))
			ret1=v1
			ret2=v2
			ret3=v3
		else:
			n1, index1 = ret1
			if not ret2:
				self._sema.add_error(UndefinedVariableError(v2, ctx.children[5].start.line, ctx.children[5].start.column
															, ctx.children[5].start.start  - ctx.start.start,
															ctx.children[5].stop.stop - ctx.start.start
															, ctx.getText()))
				ret2=v2
			else:
				n2, _ = ret2
				if not ret3:
					self._sema.add_error(UndefinedVariableError(v3, ctx.children[7].start.line, ctx.children[7].start.column
																, ctx.children[7].start.start - ctx.start.start,
																ctx.children[7].stop.stop - ctx.start.start
																, ctx.getText()))
					ret3=v3
				else:
					n3, index3 = ret3
					isPos = isinstance(n1, Position)
					isNTRV = isinstance(n1, NameWithTwoRealValues)
					isState = isinstance(n1, State) or isinstance(n1,StateVehicleTypePedestrianTypeStateListErrorType) \
						or isinstance(n1,StateStateListErrorType) or isinstance(n1,StateVehicleTypeStateListErrorType)
					if not isPos and not isNTRV and not isState:
						self._sema.add_error(IllegalTypeError(v1, ctx.children[3].start.line, ctx.children[3].start.column
															  , ctx.children[3].start.start - ctx.start.start, ctx.children[3].stop.stop - ctx.start.start
															  , ctx.getText(), n1.__class__.__name__,
															  'Position', 'State'))
						ret1 = v1
						ret2 = v2
						ret3 = v3
					if isNTRV or isPos:
						isHead = isinstance(n2, Heading)
						if not isHead:
							self._sema.add_error(IllegalTypeError(v2, ctx.children[5].start.line, ctx.children[5].start.column
																  , ctx.children[5].start.start  - ctx.start.start,
																  ctx.children[5].stop.stop - ctx.start.start
																  , ctx.getText(), n2.__class__.__name__,
																  'Heading'))
							ret2=v2
					else:  # n1 is State
						if isinstance(n2, State) or isinstance(n2,StateVehicleTypePedestrianTypeStateListErrorType)\
						or isinstance(n2,StateStateListErrorType) or isinstance(n2,StateVehicleTypeStateListErrorType):
							if not isinstance(n3, State) or isinstance(n3,StateVehicleTypePedestrianTypeStateListErrorType)\
						or isinstance(n3,StateStateListErrorType) or isinstance(n3,StateVehicleTypeStateListErrorType):
								self._sema.add_error(IllegalTypeError(v3, ctx.children[7].start.line, ctx.children[7].start.column
																	  , ctx.children[7].start.start - ctx.start.start,
																	  ctx.children[7].stop.stop - ctx.start.start
																	  , ctx.getText(), n3.__class__.__name__,
																	  'State'))
								ret3=v3
						else:
							self._sema.add_error(IllegalTypeError(v2, ctx.children[5].start.line, ctx.children[5].start.column
																  , ctx.children[5].start.start - ctx.start.start,
																  ctx.children[5].stop.stop - ctx.start.start
																  , ctx.getText(), n2.__class__.__name__,
																  'State'))
							ret2=v2
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.start - ctx.start.start,
														   ctx.children[0].stop.stop - ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_name_with_three_variables(name, ret1, ret2, ret3)


	def exitAssign_name_three_variables(self, ctx: AVScenariosParser.Assign_name_three_variablesContext):
		pass

	def enterAssign_state(self, ctx: AVScenariosParser.Assign_stateContext):
		self._current._states._flag = 0

	def exitAssign_state(self, ctx: AVScenariosParser.Assign_stateContext):
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.start - ctx.start.start,
														   ctx.children[0].stop.stop - ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_state(name)
		self._current._states._value = None

	def enterAssign_vehicle_type(self, ctx: AVScenariosParser.Assign_vehicle_typeContext):
		pass

	def exitAssign_vehicle_type(self, ctx: AVScenariosParser.Assign_vehicle_typeContext):
		name = ctx.chilren[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.start - ctx.start.start,
														   ctx.children[0].stop.stop - ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_vehicle_type(name)
		self._current._vehicle_type = None

	def enterAssign_state_list(self, ctx: AVScenariosParser.Assign_state_listContext):
		self._current._states._flag = 0

	def exitAssign_state_list(self, ctx: AVScenariosParser.Assign_state_listContext):
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.start - ctx.start.start,
														   ctx.children[0].stop.stop - ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_stateList(name)
		self._current._state_list = None
		self._current._states._flag = 0

	def enterAssign_pedestrian_type(self, ctx: AVScenariosParser.Assign_pedestrian_typeContext):
		pass

	def exitAssign_pedestrian_type(self, ctx: AVScenariosParser.Assign_pedestrian_typeContext):
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start,
														   ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_pedestrian_type(name)
		self._current._pedestrian_type = None


	def enterAssign_rv_rv(self, ctx: AVScenariosParser.Assign_rv_rvContext):
		pass
		# print('Enter Assign_rv_rv:   '+ctx.getText())
		# print(self._current._real_value_expression)


	def exitAssign_rv_rv(self, ctx: AVScenariosParser.Assign_rv_rvContext):
		# print('Exit Assign_rv_rv:   '+ctx.getText())
		# print(self._current._real_value_expression)
		name = ctx.children[0].getText()
		# print('Enter Assign_rv_rv: '+ctx.getText())
		assert len(self._current._real_value_expression)>0
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start,
														   ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		elif len(ctx.children) == 8:
			# we meet a position
			self._sema.act_on_coordinate_position(name
												  , ctx.children[2].getText()
												  , self._current._real_value_expression[-2]
												  , self._current._real_value_expression[-1])
			self._current._real_value_expression.pop()
			self._current._real_value_expression.pop()
		elif len(ctx.children) == 10:
			# we meet a position
			if ctx.children[7].getText() == '+':
				self._sema.act_on_coordinate_position(name
													  , ""
													  ,  self._current._real_value_expression[-3]
													  ,  self._current._real_value_expression[-2]
													  ,  self._current._real_value_expression[-1])
				self._current._real_value_expression.pop()
				self._current._real_value_expression.pop()
				self._current._real_value_expression.pop()
			else:  # ctx.children[7].getText()=='-'
				self._sema.act_on_coordinate_position(name
													  , ""
													  ,  self._current._real_value_expression[-3]
													  ,  self._current._real_value_expression[-2]
													  ,  -self._current._real_value_expression[-1])
				self._current._real_value_expression.pop()
				self._current._real_value_expression.pop()
				self._current._real_value_expression.pop()              
		elif len(ctx.children) == 11:
			# we meet a position
			if ctx.children[8].getText() == '+':
				self._sema.act_on_coordinate_position(name
													  , ctx.children[2].getText()
													  ,  self._current._real_value_expression[-3]
													  ,  self._current._real_value_expression[-2]
													  ,  self._current._real_value_expression[-1])
				self._current._real_value_expression.pop()
				self._current._real_value_expression.pop()
				self._current._real_value_expression.pop()
			else:  # ctx.children[8].getText()=='-'
				self._sema.act_on_coordinate_position(name
													  , ctx.children[2].getText()
													  ,  self._current._real_value_expression[-3]
													  ,  self._current._real_value_expression[-2]
													  ,  -self._current._real_value_expression[-1])
				self._current._real_value_expression.pop()
				self._current._real_value_expression.pop()
				self._current._real_value_expression.pop()
		elif len(ctx.children)==7:
			# print('????????')
			self._sema.act_on_name_with_two_real_values(name
														, self._current._real_value_expression[-2]
														, self._current._real_value_expression[-1])
			self._current._real_value_expression.pop()
			self._current._real_value_expression.pop()
		else:
			print('Something wrong with exitAssign_rv_rv')








	# Enter a parse tree produced by AVScenariosParser#assign_case_of_position.
	def enterAssign_case_of_position(self, ctx:AVScenariosParser.Assign_case_of_positionContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#assign_case_of_position.
	def exitAssign_case_of_position(self, ctx:AVScenariosParser.Assign_case_of_positionContext):
		# print('Exit Assign_case_of_position:   '+ctx.getText())
		# pass
		assert len(self._current._coordinate_expression)==1
		# print(self._current._coordinate_expression[0])
		name = ctx.children[0].getText()
		cf = self._current._coordinate_expression[-1]
		self._current._coordinate_expression.pop()
		p = Position(name)
		p.set_coordinate(cf)
		coor = ctx.children[2].getText()
		if coor == 'IMU':
			p.set_frame(CoordinateFrame.CF_IMU)
		elif coor == 'ENU':
			p.set_frame(CoordinateFrame.CF_ENU)
		elif coor == 'WGS84':
			p.set_frame(CoordinateFrame.CF_WGS84)
		# self.finish_position(p)
		self._sema._ast.add_ast_node(p)
		self._current._lane = None

















	def enterAssign_lane_rv(self, ctx: AVScenariosParser.Assign_lane_rvContext):
		pass


		

	def exitAssign_lane_rv(self, ctx: AVScenariosParser.Assign_lane_rvContext):
		# print('Exit Assign_lane_rv:  '+ctx.getText())
		# print(len(self._current._general_assertion_list))
		if len(self._current._general_assertion_list) >0:
			if len(self._current._general_assertion_list)>=2:
			# print('general_assertion5:'+ctx.getText())
				temp = DeriveWithGeneral()
				temp.set_general_assertion_left(self._current._general_assertion_list[-2].get_assertion())
				temp.set_general_assertion_right(self._current._general_assertion_list[-1].get_assertion())
				self._current._general_assertion_list.pop()
				self._current._general_assertion_list[-1].add_assertion(temp)
			# print(len(self._current._general_assertion_list))
			# for i in self._current._general_assertion_list:
			#   print(i.get_assertion())
			name = ctx.children[0].getText()
			temp = SingleGeneralAssertion()
			temp.set_name(name)
				# temp.add_assertion(self._current._general_assertion.get_assertion())#copy.deepcopy(self._current._general_assertion)
			temp.add_assertion(self._current._general_assertion_list[-1].get_assertion())
			if not self._sema.check_unique_id(name):
				self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line
																		, ctx.children[0].start.column
																		, ctx.children[0].start.stop- ctx.start.start
																		, ctx.children[0].stop.stop- ctx.start.start
																		, ctx.getText()))
			else:
				temp.set_name(name)
				if isinstance(temp, SingleGeneralAssertion):
					self._sema._ast.add_ast_node(temp)
					# print('success in add node: '+ name)
				else:
					print('Something unexpected happen with Assign_general_assertion_to_var: ' +name+' is Not SingleGeneralAssertion')
				# self._current._general_assertion = None
			self._current._general_assertion_list.pop()
			# print(len(self._current._general_assertion_list))
		elif self._current._lane_coordinate is not None:
			name = ctx.children[0].getText()
			if not self._sema.check_unique_id(name):
				self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
															   , ctx.children[0].start.stop- ctx.start.start,
															   ctx.children[0].stop.stop- ctx.start.start
															   , ctx.getText()))
			elif len(ctx.children) == 5:
				self._current._lane = self._current._lane_coordinate.get_lane()
				self._sema.act_on_lane_coordinate_position(name, '',self._current._lane_coordinate.get_distance())
				# self._current._real_value_expression.pop()
				# print('success in add node: '+ name)
			else:  # len(...)==6
				self._current._lane = self._current._lane_coordinate.get_lane()
				self._sema.act_on_lane_coordinate_position(name, ctx.children[2].getText()
														   , self._current._lane_coordinate.get_distance())
				# self._current._real_value_expression.pop()
			self._current._lane = None
			self._current._lane_coordinate = None
		elif len(self._current._real_value_expression)>0: #and len(self._current._string_expression)>0:
			name = ctx.children[0].getText()
			if not self._sema.check_unique_id(name):
				self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
															   , ctx.children[0].start.stop- ctx.start.start,
															   ctx.children[0].stop.stop- ctx.start.start
															   , ctx.getText()))
			elif len(ctx.children) == 5:
				# self._current._lane = self._current._string_expression[-1]
				self._sema.act_on_lane_coordinate_position(name, '',self._current._real_value_expression[-1])
				self._current._real_value_expression.pop()
				# print('success in add node: '+ name)
			else:  # len(...)==6
				# self._current._lane = self._current._string_expression[-1]
				self._sema.act_on_lane_coordinate_position(name, ctx.children[2].getText()
														   , self._current._real_value_expression[-1])
				self._current._real_value_expression.pop()
			self._current._lane = None
			self._current._lane_coordinate = None
		else:
			print('Something go wrong with exitAssign_lane_rv')



	def enterAssign_lane_range(self, ctx:AVScenariosParser.Assign_lane_rangeContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#assign_lane_range.
	def exitAssign_lane_range(self, ctx:AVScenariosParser.Assign_lane_rangeContext):
		if self._current._lane_coordinate is not None:
			name = ctx.children[0].getText()
			if not self._sema.check_unique_id(name):
				self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
															   , ctx.children[0].start.stop- ctx.start.start,
															   ctx.children[0].stop.stop- ctx.start.start
															   , ctx.getText()))
			elif len(ctx.children) == 9:
				self._current._lane = self._current._lane_coordinate.get_lane()
				self._sema.act_on_lane_coordinate_position(name, '',self._current._lane_coordinate.get_distance())
				# self._current._real_value_expression.pop()
				# print('success in add node: '+ name)
			else:  # len(...)==6
				self._current._lane = self._current._lane_coordinate.get_lane()
				self._sema.act_on_lane_coordinate_position(name, ctx.children[2].getText()
														   , self._current._lane_coordinate.get_distance())
				# self._current._real_value_expression.pop()
			self._current._lane = None
			self._current._lane_coordinate = None
		elif len(self._current._real_value_expression) == 2: #and len(self._current._string_expression)>0:
			name = ctx.children[0].getText()
			if not self._sema.check_unique_id(name):
				self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
															   , ctx.children[0].start.stop- ctx.start.start,
															   ctx.children[0].stop.stop- ctx.start.start
															   , ctx.getText()))
			elif len(ctx.children) == 10:
				# self._current._lane = self._current._string_expression[-1]
				rv_right = self._current._real_value_expression[-1]
				self._current._real_value_expression.pop()
				rv_left = self._current._real_value_expression[-1]
				self._current._real_value_expression.pop()
				rv = random.randint(rv_left*10000, rv_right*10000)
				rv = rv/10000
				self._sema.act_on_lane_coordinate_position(name, '',rv)
				# print('success in add node: '+ name)
			else:  # len(...)==6
				# self._current._lane = self._current._string_expression[-1]
				self._sema.act_on_lane_coordinate_position(name, ctx.children[2].getText()
														   , self._current._real_value_expression[-1])
				self._current._real_value_expression.pop()
			self._current._lane = None
			self._current._lane_coordinate = None
		else:
			print('Something go wrong with exitAssign_lane_rv')



	def enterAssign_heading(self, ctx: AVScenariosParser.Assign_headingContext):
		pass

	def exitAssign_heading(self, ctx: AVScenariosParser.Assign_headingContext):
		# print('Exit Assign_heading:  '+ ctx.getText())
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start,
														   ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_heading(name)
		self._current._heading = None

	def enterAssign_general_type(self, ctx: AVScenariosParser.Assign_general_typeContext):
		pass

	def exitAssign_general_type(self, ctx: AVScenariosParser.Assign_general_typeContext):
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start,
														   ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_type(name)
		self._current._type = None

	def enterAssign_color(self, ctx: AVScenariosParser.Assign_colorContext):
		pass

	def exitAssign_color(self, ctx: AVScenariosParser.Assign_colorContext):
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start,
														   ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_color(name)
		self._current._color = None

	def enterAssign_npc(self, ctx: AVScenariosParser.Assign_npcContext):
		pass

	def exitAssign_npc(self, ctx: AVScenariosParser.Assign_npcContext):
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start,
														   ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_npc_vehicle(name)
		self._current._npc_vehicle = None

	def enterAssign_uniform_motion(self, ctx: AVScenariosParser.Assign_uniform_motionContext):
		self._current._states._flag = 0

	def exitAssign_uniform_motion(self, ctx: AVScenariosParser.Assign_uniform_motionContext):
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start,
														   ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_name_with_motion(name)
		self._current._name_with_motion = None
		self._current._states._flag = 0

	def enterAssign_waypoint_motion(self, ctx: AVScenariosParser.Assign_waypoint_motionContext):
		self._current._states._flag = 0

	def exitAssign_waypoint_motion(self, ctx: AVScenariosParser.Assign_waypoint_motionContext):
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start,
														   ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_name_with_motion(name)
		self._current._name_with_motion = None
		self._current._states._flag = 0

	def enterAssign_variables(self, ctx: AVScenariosParser.Assign_variablesContext):
		size = len(ctx.children)
		# size>=5
		name = ctx.children[0].getText()
		redefinition=False
		if not self._sema.check_unique_id(name):
			redifinition=True
			self._sema.add_error(
				RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
										  , ctx.children[0].start.stop - ctx.start.start,
										  ctx.children[0].stop.stop - ctx.start.start
										  , ctx.getText()))
		first_ele = ctx.children[3].getText()
		ret = self._sema.find_node(first_ele)
		if not ret:
			self._sema.add_error(UndefinedVariableError(first_ele, ctx.children[3].start.line, ctx.children[3].start.column
														, ctx.children[3].start.start- ctx.start.start,
														ctx.children[3].stop.stop- ctx.start.start
														, ctx.getText()))
			ET=PedestriansNPCVehiclesObstaclesWeathersTrafficErrorType(name)
			ET.add_value(first_ele)
			for i in range(5, size - 1, 2):
				ET.add_value(ctx.children[i].getText())
			self._sema._ast.add_ast_node(ET)
			return
		n, _ = ret
		if isinstance(n, Pedestrian):
			p = Pedestrians(name)
			p.add_pedestrian(n)
			for i in range(5, size - 1, 2):
				pret = self._sema.find_node(ctx.children[i].getText())
				if not pret:
					self._sema.add_error(
						UndefinedVariableError(ctx.children[i].getText(), ctx.children[i].start.line, ctx.children[i].start.column
											   , ctx.children[i].start.start - ctx.start.start,
											   ctx.children[i].stop.stop - ctx.start.start
											   , ctx.getText()))
					p.add_pedestrian(Pedestrian(ctx.children[i].getText()))
					continue
				pp, _ = pret
				if not isinstance(pp, Pedestrian):
					self._sema.add_error(IllegalTypeError(pp.get_name(), ctx.children[i].start.line, ctx.children[i].start.column
														  , ctx.children[i].start.start - ctx.start.start,
														  ctx.children[i].stop.stop - ctx.start.start
														  , ctx.getText(), pp.__class__.__name__
														  , 'Pedestrian'))
					p.add_pedestrian(Pedestrian(ctx.children[i].getText()))
					continue
				p.add_pedestrian(n)
			if not redefinition:
				self._sema.finish_pedestrians(p)
		elif isinstance(n, NPCVehicle):
			npc = NPCVehicles(name)
			npc.add_npc_vehicle(n)
			for i in range(5, size - 1, 2):
				nret = self._sema.find_node(ctx.children[i].getText())
				if not nret:
					self._sema.add_error(
						UndefinedVariableError(ctx.children[i].getText(), ctx.children[i].start.line, ctx.children[i].start.column
											   , ctx.children[i].start.start - ctx.start.start,
											   ctx.children[i].stop.stop - ctx.start.start
											   , ctx.getText()))
					npc.add_npc_vehicle(NPCVehicle(ctx.children[i].getText()))
					continue
				nn, _ = nret
				if not isinstance(nn, NPCVehicle):
					self._sema.add_error(IllegalTypeError(nn.get_name(), ctx.children[i].start.line, ctx.children[i].start.column
														  , ctx.children[i].start.start - ctx.start.start,
														  ctx.children[i].stop.stop - ctx.start.start
														  , ctx.getText(), nn.__class__.__name__
														  , 'NPCVehicle'))
					npc.add_npc_vehicle(NPCVehicle(ctx.children[i].getText()))
					continue
				npc.add_npc_vehicle(nn)
			if not redefinition:
				self._sema.finish_npc_vehicles(npc)
		elif isinstance(n, Obstacle):
			o = Obstacles(name)
			o.add_obstacle(n)
			for i in range(5, size - 1, 2):
				oret = self._sema.find_node(ctx.children[i].getText())
				if not oret:
					self._sema.add_error(
						UndefinedVariableError(ctx.children[i].getText(), ctx.children[i].start.line, ctx.children[i].start.column
											   , ctx.children[i].start.start - ctx.start.start,
											   ctx.children[i].stop.stop - ctx.start.start
											   , ctx.getText()))
					o.add_obstacle(Obstacle(ctx.children[i].getText()))
					continue
				oo, _ = oret
				if not isinstance(oo, Obstacle):
					self._sema.add_error(IllegalTypeError(oo.get_name(), ctx.children[i].start.line, ctx.children[i].start.column
														  , ctx.children[i].start.start - ctx.start.start,
														  ctx.children[i].stop.stop - ctx.start.start
														  , ctx.getText(), oo.__class__.__name__
														  , 'Obstacle'))
					o.add_obstacle(Obstacle(ctx.children[i].getText()))
					continue
				o.add_obstacle(oo)
			if not redefinition:
				self._sema.finish_obstacles(o)
		elif isinstance(n, Weather):
			w = Weathers(name)
			w.add_weather(n)
			for i in range(5, size - 1, 2):
				wret = self._sema.find_node(ctx.children[i].getText())
				if not wret:
					self._sema.add_error(
						UndefinedVariableError(ctx.children[i].getText(), ctx.children[i].start.line, ctx.children[i].start.column
											   , ctx.children[i].start.start - ctx.start.start,
											   ctx.children[i].stop.stop - ctx.start.start
											   , ctx.getText()))
					w.add_weather(Weather(ctx.children[i].getText()))
					continue
				ww, _ = wret
				if not isinstance(ww, Weather):
					self._sema.add_error(IllegalTypeError(ww.get_name(), ctx.children[i].start.line, ctx.children[i].start.column
														  , ctx.children[i].start.start - ctx.start.start,
														  ctx.children[i].stop.stop - ctx.start.start
														  , ctx.getText(), ww.__class__.__name__
														  , 'Weather'))
					w.add_weather(Weather(ctx.children[i].getText()))
					continue
				w.add_weather(ww)
			if not redefinition:
				self._sema.finish_weathers(w)
		# Traffic is consisted by the consecutive intersection traffics and speed limitations
		elif isinstance(n, IntersectionTraffic):
			t = Traffic(name)
			has_seen_speed_limitation=False
			t.add_intersection_traffic(n)
			for i in range(5, size - 1, 2):
				tret = self._sema.find_node(ctx.children[i].getText())
				if not tret:
					self._sema.add_error(UndefinedVariableError(ctx.children[i].getText(), ctx.children[i].start.line, ctx.children[i].start.column
														  , ctx.children[i].start.start - ctx.start.start,
														  ctx.children[i].stop.stop - ctx.start.start
														  , ctx.getText()))
					continue
				tt, _ = tret
				if not has_seen_speed_limitation:
					if isinstance(tt,SpeedLimitation):
						t.add_speed_limitation(tt)
						has_seen_speed_limitation=True
					elif isinstance(tt,IntersectionTraffic):
						t.add_intersection_traffic(tt)
					else:
						self._sema.add_error(IllegalTypeError(tt.get_name(), ctx.children[i].start.line, ctx.children[i].start.column
															  , ctx.children[i].start.start - ctx.start.start,
															  ctx.children[i].stop .stop - ctx.start.start
															  , ctx.getText(), tt.__class__.__name__
															  , 'IntersectionTraffic','SpeedLimitation'))
						t.add_intersection_traffic(IntersectionTraffic(ctx.children[i].getText()))
						continue
				else:
					if not isinstance(tt, SpeedLimitation):
						self._sema.add_error(IllegalTypeError(tt.get_name(), ctx.children[i].start.line, ctx.children[i].start.column
															  , ctx.children[i].start.start - ctx.start.start,
															  ctx.children[i].stop.stop - ctx.start.start
															  , ctx.getText(), tt.__class__.__name__
															  , 'SpeedLimitation'))
						t.add_speed_limitation(SpeedLimitation(ctx.children[i].getText()))
						continue
					t.add_speed_limitation(tt)
			if not redefinition:
				self._sema.finish_traffic(t)
		else:
			self._sema.add_error(IllegalTypeError(first_ele, ctx.children[3].start.line, ctx.children[3].start.column
												  , ctx.children[3].start.start- ctx.start.start
												  , ctx.children[3].stop.stop- ctx.start.start
												  , ctx.getText(), n.__class__.__name__
												  , 'Pedestrian', 'NPCVehicle', 'Obstacle', 'Weather',
												  'IntersectionTraffic'))
			ET = PedestriansNPCVehiclesObstaclesWeathersTrafficErrorType(name)
			ET.add_value(first_ele)
			for i in range(5, size - 1, 2):
				ET.add_value(ctx.children[i].getText())
			self._sema._ast.add_ast_node(ET)

	def exitAssign_variables(self, ctx:AVScenariosParser.Assign_variablesContext):
		pass

	def enterAssign_pedestrians(self, ctx: AVScenariosParser.Assign_pedestriansContext):
		pass

	def exitAssign_pedestrians(self, ctx: AVScenariosParser.Assign_pedestriansContext):
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start,
														   ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_pedestrians(name)
		self._current._pedestrians = None

	def enterAssign_npcs(self, ctx: AVScenariosParser.Assign_npcsContext):
		pass

	def exitAssign_npcs(self, ctx: AVScenariosParser.Assign_npcsContext):
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start,
														   ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_npc_vehicles(name)
		self._current._npc_vehicles = None

	def enterAssign_obstacles(self, ctx: AVScenariosParser.Assign_obstaclesContext):
		pass

	def exitAssign_obstacles(self, ctx: AVScenariosParser.Assign_obstaclesContext):
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start,
														   ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_obstacles(name)
		self._current._obstacles = None

	def enterAssign_weather(self, ctx: AVScenariosParser.Assign_weatherContext):
		pass

	def exitAssign_weather(self, ctx: AVScenariosParser.Assign_weatherContext):
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start,
														   ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_weathers(name)
		self._current._weathers = None

	def enterAssign_traffic(self, ctx: AVScenariosParser.Assign_trafficContext):
		pass

	def exitAssign_traffic(self, ctx: AVScenariosParser.Assign_trafficContext):
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start,
														   ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_traffic(name)
		self._current._traffic = None

	def enterAssign_ped(self, ctx: AVScenariosParser.Assign_pedContext):
		pass

	def exitAssign_ped(self, ctx: AVScenariosParser.Assign_pedContext):
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start,
														   ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_pedestrian(name)
		self._current._pedestrian = None

	def enterAssign_obs(self, ctx: AVScenariosParser.Assign_obsContext):
		pass

	def exitAssign_obs(self, ctx: AVScenariosParser.Assign_obsContext):
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start,
														   ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_obstacle(name)
		self._current._obstacle = None

	def enterAssign_shape(self, ctx: AVScenariosParser.Assign_shapeContext):
		pass

	def exitAssign_shape(self, ctx: AVScenariosParser.Assign_shapeContext):
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start,
														   ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_shape(name)
		self._current._shape = None

	def enterAssign_env(self, ctx: AVScenariosParser.Assign_envContext):
		pass

	def exitAssign_env(self, ctx: AVScenariosParser.Assign_envContext):
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start,
														   ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_environment(name)
		self._current._env = None

	def enterAssign_time(self, ctx: AVScenariosParser.Assign_timeContext):
		pass

	def exitAssign_time(self, ctx: AVScenariosParser.Assign_timeContext):
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start,
														   ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_time(name)
		self._current._time = None

	def enterAssign_weather_stmt(self, ctx: AVScenariosParser.Assign_weather_stmtContext):
		pass

	def exitAssign_weather_stmt(self, ctx: AVScenariosParser.Assign_weather_stmtContext):
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start,
														   ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_weather(name)
		self._current._weather = None

	def enterAssign_weather_discrete(self, ctx: AVScenariosParser.Assign_weather_discreteContext):
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start,
														   ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_weather_discrete_level(name
												 , ctx.children[2].getText())

	def exitAssign_weather_discrete(self, ctx: AVScenariosParser.Assign_weather_discreteContext):
		pass

	def enterAssign_intersection(self, ctx: AVScenariosParser.Assign_intersectionContext):
		pass

	def exitAssign_intersection(self, ctx: AVScenariosParser.Assign_intersectionContext):
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start,
														   ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_intersecion_traffic(name)
		self._current._intersection_traffic = None

	def enterAssign_speed_limit(self, ctx: AVScenariosParser.Assign_speed_limitContext):
		pass

	def exitAssign_speed_limit(self, ctx: AVScenariosParser.Assign_speed_limitContext):
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start,
														   ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_speed_limitation(name)
		self._current._speed_limit = None




	# Enter a parse tree produced by AVScenariosParser#map_name_str.
	def enterMap_name_str(self, ctx:AVScenariosParser.Map_name_strContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#map_name_str.
	def exitMap_name_str(self, ctx:AVScenariosParser.Map_name_strContext):
		pass


	# Enter a parse tree produced by AVScenariosParser#string_expression_for_string_expression.
	def enterString_expression_for_string_expression(self, ctx:AVScenariosParser.String_expression_for_string_expressionContext):
		# print('Enter String_expression_for_string_expression:  '+ctx.getText())
		pass


	# Exit a parse tree produced by AVScenariosParser#string_expression_for_string_expression.
	def exitString_expression_for_string_expression(self, ctx:AVScenariosParser.String_expression_for_string_expressionContext):        
		if len(self._current._string_expression) > 0 :
			# print('Exit String_expression_for_string_expression0:  '+str(len(ctx.children)) + '   '+ ctx.getText())
			# print(self._current._string_expression)
			assert len(self._current._string_expression) == 2
			assert ctx.children[1].getText()=='+'
			# assert ctx.children[]
			self._current._string_expression[0] = self._current._string_expression[0] + self._current._string_expression[1]
			self._current._string_expression.pop()

			# print(self._current._string_expression)
		elif len(self._current._general_atom_statements_list)>0:
			# print('Exit String_expression_for_string_expression1:  '+str(len(ctx.children)) + '   '+ ctx.getText())
			if self._current._overall_statement is None:
				self._current._overall_statement = OverallStatement()
			len_before = len(self._current._overall_statement.get_statements())
			for _i in range(len(self._current._general_atom_statements_list)):
				self._current._overall_statement.add_statement(self._current._general_atom_statements_list[_i])
			self._current._general_atom_statements_list=[]

			len_after = len(self._current._overall_statement.get_statements())
			if len_after > len_before:
				# print(ctx.children[1].getText())
				self._current._overall_statement.add_operator(ctx.children[1].getText())

			# print(len_after)
			# print(len_before)
			# print(self._current._overall_statement.get_statements())
			# print(self._current._overall_statement.get_operators())
			# assert len_after-len_before<= 2
			assert len_after-len_before>0

			if self._current._kuohao_of_statement is not None and len(self._current._kuohao_of_statement)>0: #and len_after-len_before!=0:
				# print('!!!!!!!!!111')
				self._current._kuohao_of_statement[-1].add_operator(self._current._overall_statement._operators[-1])
				self._current._overall_statement._operators.pop()
				if len_after-len_before>=2 or len(self._current._kuohao_of_statement[-1].get_statements())==0:#isinstance(ctx.parentCtx, AVScenariosParser.Atom_statement_overall_with_kuohaoContext):
					# print('???2')
					self._current._kuohao_of_statement[-1].add_statement(self._current._overall_statement._statements[-2])
					self._current._kuohao_of_statement[-1].add_statement(self._current._overall_statement._statements[-1])
					self._current._overall_statement._statements.pop() 
					self._current._overall_statement._statements.pop() 
				else:
					# print('???1')
					self._current._kuohao_of_statement[-1].add_statement(self._current._overall_statement._statements[-1])
					self._current._overall_statement._statements.pop()
		elif len(self._current._coordinate_expression)>0:
			assert len(self._current._coordinate_expression)>1
			temp_left = []
			temp_right = []
			if isinstance(self._current._coordinate_expression[-1] , Coordinate):
				if self._current._coordinate_expression[-1].has_z():
					temp_right.append(self._current._coordinate_expression[-1].get_x())
					temp_right.append(self._current._coordinate_expression[-1].get_y())
					temp_right.append(self._current._coordinate_expression[-1].get_z())
				else:
					temp_right.append(self._current._coordinate_expression[-1].get_x())
					temp_right.append(self._current._coordinate_expression[-1].get_y())
				self._current._coordinate_expression.pop()
			elif isinstance(self._current._coordinate_expression[-1] , NameWithTwoRealValues):
				temp_right.append(self._current._coordinate_expression[-1].get_value()[0])
				temp_right.append(self._current._coordinate_expression[-1].get_value()[1])
				self._current._coordinate_expression.pop()
			elif isinstance(self._current._coordinate_expression[-1]  , Position):
				self._current._coordinate_expression[-1] = self._current._coordinate_expression[-1].get_coordinate()
				if self._current._coordinate_expression[-1].has_z():
					temp_right.append(self._current._coordinate_expression[-1].get_x())
					temp_right.append(self._current._coordinate_expression[-1].get_y())
					temp_right.append(self._current._coordinate_expression[-1].get_z())
				else:
					temp_right.append(self._current._coordinate_expression[-1].get_x())
					temp_right.append(self._current._coordinate_expression[-1].get_y())
				self._current._coordinate_expression.pop()

			if isinstance(self._current._coordinate_expression[-1] , Coordinate):
				if self._current._coordinate_expression[-1].has_z():
					temp_left.append(self._current._coordinate_expression[-1].get_x())
					temp_left.append(self._current._coordinate_expression[-1].get_y())
					temp_left.append(self._current._coordinate_expression[-1].get_z())
				else:
					temp_left.append(self._current._coordinate_expression[-1].get_x())
					temp_left.append(self._current._coordinate_expression[-1].get_y())
				self._current._coordinate_expression.pop()
			elif isinstance(self._current._coordinate_expression[-1] , NameWithTwoRealValues):
				temp_left.append(self._current._coordinate_expression[-1].get_value()[0])
				temp_left.append(self._current._coordinate_expression[-1].get_value()[1])
				self._current._coordinate_expression.pop()
			elif isinstance(self._current._coordinate_expression[-1]  , Position):
				self._current._coordinate_expression[-1] = self._current._coordinate_expression[-1].get_coordinate()
				if self._current._coordinate_expression[-1].has_z():
					temp_left.append(self._current._coordinate_expression[-1].get_x())
					temp_left.append(self._current._coordinate_expression[-1].get_y())
					temp_left.append(self._current._coordinate_expression[-1].get_z())
				else:
					temp_left.append(self._current._coordinate_expression[-1].get_x())
					temp_left.append(self._current._coordinate_expression[-1].get_y())
				self._current._coordinate_expression.pop()  
			
			assert len(temp_left) == len(temp_right)
			temp_left = array(temp_left)
			temp_right = array(temp_right)
			if ctx.children[1].getText()=='+':
				result = temp_left +  temp_right
			elif ctx.children[1].getText()=='-':
				result = temp_left -  temp_right
			if len(result)==3:
				self._current._coordinate_expression.append(Coordinate(result[0]
															   , result[1]
															   , result[2]))
			elif len(result)==2:
				self._current._coordinate_expression.append(Coordinate(result[0]
															   , result[1]))
			else:
				print('Length of result not fit!!!!')


		elif len(self._current._real_value_expression)>=2:
			if ctx.children[1].getText()=='+':
				self._current._real_value_expression[-2]=self._current._real_value_expression[-2]+self._current._real_value_expression[-1]
				self._current._real_value_expression.pop()
			elif ctx.children[1].getText()=='-':
				self._current._real_value_expression[-2]=self._current._real_value_expression[-2]-self._current._real_value_expression[-1]
				self._current._real_value_expression.pop()
			else:
				print('Fatal: Wrong with Plus or Minus of real value expression!')
		else:
			print('Something go wrong with exitString_expression_for_string_expression')





	# Enter a parse tree produced by AVScenariosParser#string_for_string_expression.
	def enterString_for_string_expression(self, ctx:AVScenariosParser.String_for_string_expressionContext):
		# print('String_for_string_expression: '+ ctx.children[0].getText()[1:-1])
		# print(len(ctx.children))
		#print(ctx.getText())
		self._current._string_expression.append(ctx.children[0].getText()[1:-1])
			#print(self._current._map.get_map_name() )

	# Exit a parse tree produced by AVScenariosParser#string_for_string_expression.
	def exitString_for_string_expression(self, ctx:AVScenariosParser.String_for_string_expressionContext):
		pass


	# Enter a parse tree produced by AVScenariosParser#string_id.
	def enterString_id(self, ctx:AVScenariosParser.String_idContext):
		# print('Enter String_id:  '+ ctx.children[0].getText())
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[2].start.line, ctx.children[2].start.column
														, ctx.children[2].start.start - ctx.start.start,
														ctx.children[2].stop.stop - ctx.start.start
														, ctx.getText()))
			self._current._map=Map("Error Type",name)
		else:
			n, index = ret
			# print(n)
			if isinstance(n, NameWithString):
				self._current._string_expression.append(n._value)

			# elif isinstance(n, NameWithRealValue):
			#   self._current._real_value_expression.append(n._value)


			elif isinstance(n, NameWithRealValue):
				self._current._real_value_expression.append(n._value)

			elif isinstance(n, Coordinate):
				self._current._coordinate_expression.append(n)
				#   self._current._temp_for_statement = n
			elif isinstance(n, NameWithTwoRealValues):
				self._current._coordinate_expression.append(n)
				#   self._current._temp_for_statement = n
			elif isinstance(n , Position):
				self._current._coordinate_expression.append(n)
			# elif isinstance(n, NameWithString):
			#   m = self._sema.cast_to_map(n)
			#   self._sema.set(index, m)
			#   self._current._map = m
	
			else:
				# self._current._map = Map("Error Map",name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[2].start.line, ctx.children[2].start.column
													  , ctx.children[2].start.start - ctx.start.start,
													  ctx.children[2].stop.stop - ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'Map'))


	# Exit a parse tree produced by AVScenariosParser#string_id.
	def exitString_id(self, ctx:AVScenariosParser.String_idContext):
		# print(len(self._current._coordinate_expression))
		pass


	#The end of assignment, the next is about other variable semantic
	def enterMap_load_name(self, ctx: AVScenariosParser.Map_load_nameContext):
		pass

	def exitMap_load_name(self, ctx: AVScenariosParser.Map_load_nameContext):
		#pass
		# do not delete self._current._map
		assert self._current._map is None
		assert len(self._current._string_expression)>0
		self._current._map = Map(self._current._string_expression[-1])
		self._current._string_expression.pop()


	def enterCreate_scenario(self, ctx: AVScenariosParser.Create_scenarioContext):
		assert self._current._scenario is None
		self._current._scenario = Scenario(ctx.children[0].getText())
		self._sema.begin_scenario(self._current._scenario)

	def exitCreate_scenario(self, ctx: AVScenariosParser.Create_scenarioContext):
		self._sema.end_scenario(self._current._scenario)
		# others complete added.
		self._current._map = None
		self._current._ego_vehicle = None
		self._current._npc_vehicles = None
		self._current._pedestrians = None
		self._current._obstacles = None
		self._current._env = None
		# self._current._traffic = None

	def enterNpc_npc(self, ctx: AVScenariosParser.Npc_npcContext):
		pass

	def exitNpc_npc(self, ctx: AVScenariosParser.Npc_npcContext):
		pass

	def enterNpc_var(self, ctx: AVScenariosParser.Npc_varContext):
		assert self._current._npc_vehicles is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._npc_vehicles=NPCVehicles(name)
		else:
			n, index = ret
			if isinstance(n, NPCVehicles) or isinstance(n,PedestriansNPCVehiclesObstaclesWeathersTrafficErrorType):
				if not isinstance(n,NPCVehicles):
					n=self._sema.cast_to_npc_vehicles(n)
					self._sema.set(index,n)
				self._current._npc_vehicles = n
			else:
				# Construct an empty NPCVehicles for error
				self._current._npc_vehicles=NPCVehicles(name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'NPCVehicles'))

	def exitNpc_var(self, ctx: AVScenariosParser.Npc_varContext):
		pass

	def enterNpc_empty(self, ctx: AVScenariosParser.Npc_emptyContext):
		pass

	def exitNpc_empty(self, ctx: AVScenariosParser.Npc_emptyContext):
		pass

	def enterPedestrians_ped(self, ctx: AVScenariosParser.Pedestrians_pedContext):
		pass

	def exitPedestrians_ped(self, ctx: AVScenariosParser.Pedestrians_pedContext):
		pass

	def enterPedestrians_var(self, ctx: AVScenariosParser.Pedestrians_varContext):
		assert self._current._pedestrians is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._pedestrians=Pedestrians(name)
		else:
			n, index = ret
			if isinstance(n, Pedestrians) or isinstance(n,PedestriansNPCVehiclesObstaclesWeathersTrafficErrorType):
				if not isinstance(n,Pedestrians):
					n=self._sema.cast_to_pedestrians(n)
					self._sema.set(index,n)
				self._current._pedestrians = n
			else:
				self._current._pedestrians = Pedestrians(name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'Pedestrians'))

	def exitPedestrians_var(self, ctx: AVScenariosParser.Pedestrians_varContext):
		pass

	def enterPedestrians_empty(self, ctx: AVScenariosParser.Pedestrians_emptyContext):
		pass

	def exitPedestrians_empty(self, ctx: AVScenariosParser.Pedestrians_emptyContext):
		pass

	def enterObstacles_obs(self, ctx: AVScenariosParser.Obstacles_obsContext):
		pass

	def exitObstacles_obs(self, ctx: AVScenariosParser.Obstacles_obsContext):
		pass

	def enterObstacles_var(self, ctx: AVScenariosParser.Obstacles_varContext):
		assert self._current._obstacles is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._obstacles=Obstacles(name)
		else:
			n, index = ret
			if isinstance(n, Obstacles) or isinstance(n,PedestriansNPCVehiclesObstaclesWeathersTrafficErrorType):
				if not isinstance(n,Obstacles):
					n=self._sema.cast_to_obstacles(n)
					self._sema.set(index,n)
				self._current._obstacles = n
			else:
				self._current._obstacles = Obstacles(name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'Obstacles'))

	def exitObstacles_var(self, ctx: AVScenariosParser.Obstacles_varContext):
		pass

	# def enterTraffic_tra(self, ctx: AVScenariosParser.Traffic_traContext):
	# 	pass

	# def exitTraffic_tra(self, ctx: AVScenariosParser.Traffic_traContext):
	# 	pass

	# def enterTraffic_var(self, ctx: AVScenariosParser.Traffic_varContext):
	# 	assert self._current._traffic is None
	# 	name = ctx.children[0].getText()
	# 	ret = self._sema.find_node(name)
	# 	if not ret:
	# 		self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
	# 													, ctx.children[0].start.stop- ctx.start.start,
	# 													ctx.children[0].stop.stop- ctx.start.start
	# 													, ctx.getText()))
	# 		self._current._traffic=Traffic(name)
	# 	else:
	# 		n, index = ret
	# 		if isinstance(n, Traffic) or isinstance(n,PedestriansNPCVehiclesObstaclesWeathersTrafficErrorType):
	# 			if not isinstance(n,Traffic):
	# 				n=self._sema.cast_to_traffic(n)
	# 				self._sema.set(index,n)
	# 			self._current._traffic=n
	# 		else:
	# 			self._current._traffic =Traffic(name)
	# 			self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
	# 												  , ctx.children[0].start.stop- ctx.start.start,
	# 												  ctx.children[0].stop.stop- ctx.start.start
	# 												  , ctx.getText(), n.__class__.__name__,
	# 												  'Traffic'))

	# def exitTraffic_var(self, ctx: AVScenariosParser.Traffic_varContext):
	# 	pass

	# def enterTraffic_empty(self, ctx: AVScenariosParser.Traffic_emptyContext):
	# 	pass

	# def exitTraffic_empty(self, ctx: AVScenariosParser.Traffic_emptyContext):
	# 	pass




	def enterEgo_ego_vehicle(self, ctx: AVScenariosParser.Ego_ego_vehicleContext):
		pass

	def exitEgo_ego_vehicle(self, ctx: AVScenariosParser.Ego_ego_vehicleContext):
		pass

	def enterEgo_ego_var(self, ctx: AVScenariosParser.Ego_ego_varContext):
		assert self._current._ego_vehicle is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._ego_vehicle=EgoVehicle(name)
		else:
			n, _ = ret
			if isinstance(n, EgoVehicle):
				self._current._ego_vehicle = n
			else:
				self._current._ego_vehicle = EgoVehicle(name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'EgoVehicle'))

	def exitEgo_ego_var(self, ctx: AVScenariosParser.Ego_ego_varContext):
		pass

	def enterEgo_av(self, ctx: AVScenariosParser.Ego_avContext):
		assert self._current._ego_vehicle is None
		# anonymous egoVehicle
		self._current._ego_vehicle = EgoVehicle()
		self._sema.begin_ego_vehicle(self._current._ego_vehicle)

	def exitEgo_av(self, ctx: AVScenariosParser.Ego_avContext):
		self._sema.end_ego_vehicle(self._current._ego_vehicle)
		self._current._vehicle_type = None
		self._current._states._first = None
		self._current._states._second = None

	def enterPar_list_ego_(self, ctx: AVScenariosParser.Par_list_ego_Context):
		self._current._states._flag = 1

	def exitPar_list_ego_(self, ctx: AVScenariosParser.Par_list_ego_Context):
		self._current._states._flag = 0

	def enterState_state(self, ctx: AVScenariosParser.State_stateContext):
		pass

	# do not call begin_state
	def exitState_state(self, ctx: AVScenariosParser.State_stateContext):
		pass

	def enterState_state_var(self, ctx: AVScenariosParser.State_state_varContext):
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			if self._current._states._flag == 0:
				assert self._current._states._value is None
				self._current._states._value = State(name)
			elif self._current._states._flag == 1:
				assert self._current._states._first is None
				self._current._states._first =  State(name)
			elif self._current._states._flag == 2:
				assert self._current._states._second is None
				self._current._states._second =  State(name)
		else:
			n, index = ret
			if isinstance(n, State) or isinstance(n,StateVehicleTypePedestrianTypeStateListErrorType)\
						or isinstance(n,StateStateListErrorType) or isinstance(n,StateVehicleTypeStateListErrorType):
				if not isinstance(n,State):
					n=self._sema.cast_to_state(n)
					self._sema.set(index,n)
				if self._current._states._flag == 0:
					assert self._current._states._value is None
					self._current._states._value = n
				elif self._current._states._flag == 1:
					assert self._current._states._first is None
					self._current._states._first = n
				elif self._current._states._flag == 2:
					assert self._current._states._second is None
					self._current._states._second = n
			else:
				if self._current._states._flag == 0:
					assert self._current._states._value is None
					self._current._states._value = State(name)
				elif self._current._states._flag == 1:
					assert self._current._states._first is None
					self._current._states._first = State(name)
				elif self._current._states._flag == 2:
					assert self._current._states._second is None
					self._current._states._second = State(name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'State'))

	def exitState_state_var(self, ctx: AVScenariosParser.State_state_varContext):
		if self._current._states._flag == 1:
			# NOTICE: enter VehicleMotion or PedestrianMotion will
			# set the flag=2 but these motions sometimes can be omitted.
			self._current._states._flag = 2

	def enterState_position(self, ctx: AVScenariosParser.State_positionContext):
		if self._current._states._flag == 0:
			assert self._current._states._value is None
			self._current._states._value = State()
			self._sema.begin_state(self._current._states._value)
		elif self._current._states._flag == 1:
			assert self._current._states._first is None
			self._current._states._first = State()
			self._sema.begin_state(self._current._states._first)
		elif self._current._states._flag == 2:
			assert self._current._states._second is None
			self._current._states._second = State()
			self._sema.begin_state(self._current._states._second)

	def exitState_position(self, ctx: AVScenariosParser.State_positionContext):
		if self._current._states._flag == 0:
			self._sema.end_state(self._current._states._value)
		elif self._current._states._flag == 1:
			self._sema.end_state(self._current._states._first)
			# NOTICE: enter VehicleMotion or PedestrianMotion will
			# set the flag=2 but these motions sometimes can be omitted.
			self._current._states._flag = 2
		elif self._current._states._flag == 2:
			self._sema.end_state(self._current._states._second)
		self._current._position = None
		self._current._heading = None
		self._current._speed = None

	def enterState_position_heading_speed(self, ctx: AVScenariosParser.State_position_heading_speedContext):
		if self._current._states._flag == 0:
			assert self._current._states._value is None
			self._current._states._value = State()
			self._sema.begin_state(self._current._states._value)
		elif self._current._states._flag == 1:
			assert self._current._states._first is None
			self._current._states._first = State()
			self._sema.begin_state(self._current._states._first)
		elif self._current._states._flag == 2:
			assert self._current._states._second is None
			self._current._states._second = State()
			self._sema.begin_state(self._current._states._second)

	def exitState_position_heading_speed(self, ctx: AVScenariosParser.State_position_heading_speedContext):
		if self._current._states._flag == 0:
			self._sema.end_state(self._current._states._value)
		elif self._current._states._flag == 1:
			self._sema.end_state(self._current._states._first)
			# NOTICE: enter VehicleMotion or PedestrianMotion will
			# set the flag=2 but these motions sometimes can be omitted.
			self._current._states._flag = 2
		elif self._current._states._flag == 2:
			self._sema.end_state(self._current._states._second)
		self._current._position = None
		self._current._heading = None
		self._current._speed = None

	def enterPos_coor_coor(self, ctx: AVScenariosParser.Pos_coor_coorContext):
		if self._current._position is None:
		# anonymous position
			self._current._position = Position()
			self._sema.begin_position(self._current._position)
		else:
			assert self._current._temp_for_statement is None
			self._current._temp_for_statement = Position()
			self._sema.begin_position(self._current._temp_for_statement)            

	def exitPos_coor_coor(self, ctx: AVScenariosParser.Pos_coor_coorContext):
		# print('Exit Pos_coor_coor:  '+ctx.getText())
		if self._current._temp_for_statement is None:
			if len(ctx.children) == 2:
				self._sema.end_position(self._current._position, ctx.children[0].getText())
			else:  # len(...)==1
				self._sema.end_position(self._current._position)
		else:
			if len(ctx.children) == 2:
				self._sema.end_position(self._current._temp_for_statement, ctx.children[0].getText())
			else:  # len(...)==1
				self._sema.end_position(self._current._temp_for_statement)      

		self._current._lane_coordinate = None
		# self._current._lane_coordinate1 = None
		# self._current._coordinate = None

	# Enter a parse tree produced by AVScenariosParser#pos_coor_coor2.
	def enterPos_coor_coor2(self, ctx:AVScenariosParser.Pos_coor_coor2Context):
		pass

	# Exit a parse tree produced by AVScenariosParser#pos_coor_coor2.
	def exitPos_coor_coor2(self, ctx:AVScenariosParser.Pos_coor_coor2Context):
		# print('Exit Pos_coor_coor2:  '+ctx.getText())

		assert len(self._current._coordinate_expression)==1
		# print(self._current._coordinate_expression[0])

		cf = self._current._coordinate_expression[-1]
		self._current._coordinate_expression.pop()
		p = Position()
		p.set_coordinate(cf)
		coor = ctx.children[0].getText()
		if coor == 'IMU':
			p.set_frame(CoordinateFrame.CF_IMU)
		elif coor == 'ENU':
			p.set_frame(CoordinateFrame.CF_ENU)
		elif coor == 'WGS84':
			p.set_frame(CoordinateFrame.CF_WGS84)

		if self._current._temp_for_statement is None:
			self._current._position = p
		else:
			self._current._temp_for_statement = p     



	# Enter a parse tree produced by AVScenariosParser#pos_coor_range1.
	def enterPos_coor_range1(self, ctx:AVScenariosParser.Pos_coor_range1Context):
		if self._current._position is None:
		# anonymous position
			self._current._position = Position()
			self._sema.begin_position(self._current._position)
		else:
			assert self._current._temp_for_statement is None
			self._current._temp_for_statement = Position()
			self._sema.begin_position(self._current._temp_for_statement) 

	# Exit a parse tree produced by AVScenariosParser#pos_coor_range1.
	def exitPos_coor_range1(self, ctx:AVScenariosParser.Pos_coor_range1Context):
		# print('Exit Pos_coor_coor:  '+ctx.getText())
		assert len(self._current._coordinate_expression) == 1
		assert len(self._current._real_value_expression) == 4


		y_right = self._current._real_value_expression[-1]
		self._current._real_value_expression.pop()
		y_left = self._current._real_value_expression[-1]
		self._current._real_value_expression.pop()

		assert y_right > y_left
		y_offset = random.randrange(y_left*10000,y_right*10000)
		y_offset = y_offset/10000
		# print(y_offset)

		x_right = self._current._real_value_expression[-1]
		self._current._real_value_expression.pop()
		x_left = self._current._real_value_expression[-1]
		self._current._real_value_expression.pop()


		assert x_right > x_left
		x_offset = random.randrange(x_left*10000,x_right*10000)
		x_offset = x_offset/10000
		# print(x_offset)

		# print(self._current._coordinate_expression[-1])
		if isinstance(self._current._coordinate_expression[-1], Coordinate):
			# print(self._current._coordinate_expression[-1])
			self._current._coordinate_expression[-1]._x +=  x_offset
			self._current._coordinate_expression[-1]._y +=  y_offset
			# print(self._current._coordinate_expression[-1])

			if self._current._temp_for_statement is None:
				self._current._position
				if len(ctx.children) == 13:
					self._sema.end_position(self._current._position, ctx.children[0].getText())
				else:  # len(...)==1
					self._sema.end_position(self._current._position)
			else:
				if len(ctx.children) == 13:
					self._sema.end_position(self._current._temp_for_statement, ctx.children[0].getText())
				else:  # len(...)==1
					self._sema.end_position(self._current._temp_for_statement)
		elif isinstance(self._current._coordinate_expression[-1], Position):
			temp = self._current._coordinate_expression[-1].get_coordinate()
			# print(self._current._coordinate_expression[-1].get_coordinate())
			temp._x +=  x_offset
			temp._y +=  y_offset
			# self._current._coordinate_expression[-1].set_coordinate(temp)
			# print(self._current._coordinate_expression[-1].get_coordinate())
			p = self._current._coordinate_expression[-1]
			self._current._coordinate_expression.pop()
			if len(ctx.children) == 13:
				if self._current._temp_for_statement is None:
					self._current._position = p
				else:
					self._current._temp_for_statement = p 
			else:
				name = p.get_name()
				n = p
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'Position'))	
				if self._current._temp_for_statement is None:
					self._current._position = Position()
				else:
					self._current._temp_for_statement = Position()

		else:
			print("Unexpected!!! of exitPos_coor_range1")

		# print(self._current._coordinate_expression[-1])

		# print(self._current._real_value_expression)

	# Enter a parse tree produced by AVScenariosParser#assign_position_range_extension.
	def enterAssign_position_range_extension(self, ctx:AVScenariosParser.Assign_position_range_extensionContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#assign_position_range_extension.
	def exitAssign_position_range_extension(self, ctx:AVScenariosParser.Assign_position_range_extensionContext):
		assert self._current._position is not None
		# print(self._current._coordinate_expression[0])
		name = ctx.children[0].getText()

		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start,
														   ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			self._current._position.set_name(name)
			self._sema._ast.add_ast_node(self._current._position)
			# self._sema.act_on_heading(name)
		self._current._position = None


	# def finish_heading(self, h: Heading):
	# 	self._ast.add_ast_node(h)

	# def act_on_heading(self, name: AnyStr):
	# 	assert self._current._heading is not None
	# 	self._current._heading.set_name(name)
	# 	self.finish_heading(self._current._heading)

	# # Enter a parse tree produced by AVScenariosParser#pos_coor_range2.
	# def enterPos_coor_range2(self, ctx:AVScenariosParser.Pos_coor_range2Context):
	# 	pass

	# # Exit a parse tree produced by AVScenariosParser#pos_coor_range2.
	# def exitPos_coor_range2(self, ctx:AVScenariosParser.Pos_coor_range2Context):
	# 	assert len(self._current._coordinate_expression) == 1
	# 	assert len(self._current._real_value_expression) == 4

	# 	y_right = self._current._real_value_expression[-1]
	# 	self._current._real_value_expression.pop()
	# 	y_left = self._current._real_value_expression[-1]
	# 	self._current._real_value_expression.pop()

	# 	assert y_right > y_left
	# 	y_offset = random.randrange(y_left*10000,y_right*10000)
	# 	y_offset = y_offset/10000
	# 	# print(y_offset)

	# 	x_right = self._current._real_value_expression[-1]
	# 	self._current._real_value_expression.pop()
	# 	x_left = self._current._real_value_expression[-1]
	# 	self._current._real_value_expression.pop()


	# 	assert x_right > x_left
	# 	x_offset = random.randrange(x_left*10000,x_right*10000)
	# 	x_offset = x_offset/10000

	# 	print(self._current._coordinate_expression[-1])
	# 	self._current._coordinate_expression[-1]._x +=  x_offset
	# 	self._current._coordinate_expression[-1]._y +=  y_offset
	# 	print(self._current._coordinate_expression[-1])


	# 	cf = self._current._coordinate_expression[-1]
	# 	self._current._coordinate_expression.pop()
	# 	p = Position()
	# 	p.set_coordinate(cf)
	# 	coor = ctx.children[0].getText()
	# 	if coor == 'IMU':
	# 		p.set_frame(CoordinateFrame.CF_IMU)
	# 	elif coor == 'ENU':
	# 		p.set_frame(CoordinateFrame.CF_ENU)
	# 	elif coor == 'WGS84':
	# 		p.set_frame(CoordinateFrame.CF_WGS84)

	# 	if self._current._temp_for_statement is None:
	# 		self._current._position = p
	# 	else:
	# 		self._current._temp_for_statement = p 






	def enterPos_pos_var(self, ctx: AVScenariosParser.Pos_pos_varContext):
		assert self._current._position is None
		# if self._current._position is not None:
		#   print('!!!!!!!!!!!!')
		#   print(self._current._position)
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._position=Position(name)
		else:
			n, index = ret
			if isinstance(n, Position):
				self._current._position = n
			elif isinstance(n, NameWithTwoRealValues):
				p = self._sema.cast_to_position(n)
				self._sema.set(index, p)
				self._current._position = p
			else:
				self._current._position = Position(name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'Position'))

	def exitPos_pos_var(self, ctx: AVScenariosParser.Pos_pos_varContext):
		pass

	def enterSpeed_speed(self, ctx: AVScenariosParser.Speed_speedContext):
		pass

	def exitSpeed_speed(self, ctx: AVScenariosParser.Speed_speedContext):
		pass

	def enterSpeed_speed_var(self, ctx: AVScenariosParser.Speed_speed_varContext):
		assert self._current._speed is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._speed = Speed(0, name)
		else:
			n, index = ret
			if isinstance(n, Speed):
				self._current._speed = n
			if isinstance(n, NameWithRealValue):
				sp = self._sema.cast_to_speed(n)
				self._sema.set(index, sp)
				self._current._speed = sp
			else:
				self._current._speed = Speed(0,name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'Speed'))

	def exitSpeed_speed_var(self, ctx: AVScenariosParser.Speed_speed_varContext):
		pass

	def enterSpeed_rv(self, ctx: AVScenariosParser.Speed_rvContext):
		pass

	def exitSpeed_rv(self, ctx: AVScenariosParser.Speed_rvContext):
		# print('Exit Speed_rv:  '+ctx.children[0].getText())
		# print(self._current._real_value_expression[-1])
		if len(self._current._real_value_expression) == 1:
			if self._current._speed is None:
				# self._current._speed = Speed(float(ctx.children[0].getText()))
				self._current._speed = Speed(self._current._real_value_expression[-1])
				self._current._real_value_expression.pop()
			else:
				assert self._current._temp_for_statement is  None
				# self._current._temp_for_statement = Speed(float(ctx.children[0].getText()))
				self._current._temp_for_statement = Speed(self._current._real_value_expression[-1])
				self._current._real_value_expression.pop()
		else:
			assert self._current._speed is not None
			pass



	# Enter a parse tree produced by AVScenariosParser#speed_range_for_state.
	def enterSpeed_range_for_state(self, ctx:AVScenariosParser.Speed_range_for_stateContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#speed_range_for_state.
	def exitSpeed_range_for_state(self, ctx:AVScenariosParser.Speed_range_for_stateContext):
		assert len(self._current._real_value_expression) == 2

		rv_right = self._current._real_value_expression[-1]
		self._current._real_value_expression.pop()
		rv_left = self._current._real_value_expression[-1]
		self._current._real_value_expression.pop()
		rv = random.randint(rv_left*10000, rv_right*10000)
		rv = rv/10000

		if self._current._speed is None:
			# self._current._speed = Speed(float(ctx.children[0].getText()))
			self._current._speed = Speed(rv)
			# self._current._real_value_expression.pop()
		else:
			assert self._current._temp_for_statement is  None
			# self._current._temp_for_statement = Speed(float(ctx.children[0].getText()))
			self._current._temp_for_statement = Speed(rv)
			# self._current._real_value_expression.pop()


	def enterRv(self, ctx: AVScenariosParser.RvContext):
		# print('enterRv:  '+ctx.getText())
		pass

	def exitRv(self, ctx: AVScenariosParser.RvContext):
		pass


	def enterCoor_rv_rv(self, ctx: AVScenariosParser.Coor_rv_rvContext):
		# print('Enter Coor_rv_rv:  '+ctx.getText())
		pass


	def exitCoor_rv_rv(self, ctx: AVScenariosParser.Coor_rv_rvContext):
		# print('Exit Coor_rv_rv:  '+ctx.getText())
		assert len(self._current._real_value_expression)>0
		if len(ctx.children) == 5:
			assert len(self._current._real_value_expression)>=2 
			self._current._coordinate_expression.append(Coordinate(self._current._real_value_expression[-2]
													   , self._current._real_value_expression[-1]))
			self._current._real_value_expression.pop()
			self._current._real_value_expression.pop()          
		else:  # len(ctx.children)==8:
			assert len(self._current._real_value_expression)>=3
			if ctx.children[5].getText() == '+':
				self._current._coordinate_expression.append(Coordinate(self._current._real_value_expression[-3]
														   , self._current._real_value_expression[-2]
														   , self._current._real_value_expression[-1]))             
				self._current._real_value_expression.pop()
				self._current._real_value_expression.pop()
				self._current._real_value_expression.pop()
			else:  # ctx.children[5].getText()=='-'
				self._current._coordinate_expression.append(Coordinate(self._current._real_value_expression[-3]
														   , self._current._real_value_expression[-2]
														   , -self._current._real_value_expression[-1]))
				self._current._real_value_expression.pop()
				self._current._real_value_expression.pop()
				self._current._real_value_expression.pop()

	def enterCoor_laneID_rv(self, ctx: AVScenariosParser.Coor_laneID_rvContext):
		pass
		# else:
		#   print('Enter Coor_laneID_rv：  '+ctx.getText())
		#   assert self._current._lane_coordinate1 is None
		#   self._current._lane_coordinate1 = LaneCoordinate(float(ctx.children[2].getText()))
		#   self._sema.begin_lane_coordinate(self._current._lane_coordinate1)           

	def exitCoor_laneID_rv(self, ctx: AVScenariosParser.Coor_laneID_rvContext):
		# print('Exit Coor_laneID_rv:  '+ctx.getText())
		if len(self._current._general_assertion_list)>=2:
			# print('general_assertion5:'+ctx.getText())
			temp = DeriveWithGeneral()
			temp.set_general_assertion_left(self._current._general_assertion_list[-2].get_assertion())
			temp.set_general_assertion_right(self._current._general_assertion_list[-1].get_assertion())
			self._current._general_assertion_list.pop()
			self._current._general_assertion_list[-1].add_assertion(temp)
			# print(str(self._current._general_assertion_list))
		else:
			assert self._current._lane_coordinate is None
			assert len(self._current._real_value_expression)>0
			# print('Exit Coor_laneID_rv:     '+ ctx.getText()+ '   '+ str(self._current._real_value_expression))

			self._current._lane_coordinate = LaneCoordinate(self._current._real_value_expression[-1])
			self._current._real_value_expression.pop()
			self._sema.begin_lane_coordinate(self._current._lane_coordinate)
			# if self._current._lane_coordinate1 is None:
			self._sema.end_lane_coordinate(self._current._lane_coordinate)
			self._current._lane = None

	def enterCoor_laneID_range(self, ctx:AVScenariosParser.Coor_laneID_rangeContext):
		pass


	def exitCoor_laneID_range(self, ctx:AVScenariosParser.Coor_laneID_rangeContext):
		assert self._current._lane_coordinate is None
		assert len(self._current._real_value_expression) == 2

		rv_right = self._current._real_value_expression[-1]
		self._current._real_value_expression.pop()
		rv_left = self._current._real_value_expression[-1]
		self._current._real_value_expression.pop()
		rv = random.randint(rv_left*10000, rv_right*10000)
		rv = rv/10000
		# print(rv)
		self._current._lane_coordinate = LaneCoordinate(rv)
		
		self._sema.begin_lane_coordinate(self._current._lane_coordinate)
			# if self._current._lane_coordinate1 is None:
		self._sema.end_lane_coordinate(self._current._lane_coordinate)
		self._current._lane = None

	def enterLaneID_laneID(self, ctx: AVScenariosParser.LaneID_laneIDContext):
		pass

	def exitLaneID_laneID(self, ctx: AVScenariosParser.LaneID_laneIDContext):
		pass

	def enterLaneID_laneID_var(self, ctx: AVScenariosParser.LaneID_laneID_varContext):
		# print('?????????'+ctx.getText())
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._lane = Lane("0.0", name)
		else:
			n, index = ret
			if isinstance(n, Lane):
				assert self._current._lane is None
				self._current._lane = n
				# print('Find Lane: '+str(self._current._lane))
			elif isinstance(n, NameWithString):
				assert self._current._lane is None
				context=self._sema.find_context_for_error(n.get_name())
				l = self._sema.cast_to_lane(n)
				self._sema.set(index, l)
				self._current._lane = l
				# print('Find NameWithString: '+str(self._current._lane))
			elif isinstance(n, SingleGeneralAssertion):
				# print("!!!!!!!!!!!!!!!!! "+ name)
				#self._current._general_assertion = n
				temp=SingleGeneralAssertion()
				temp.set_name(n.get_name())
				temp.add_assertion(n.get_assertion()) 
				self._current._general_assertion_list.append(temp)

			elif isinstance(n, GeneralDistanceStatement):
				if isinstance(ctx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
					#print('Atom_statement_id: ' +name+'Index: '+ str(_))
					if ctx.parentCtx.parentCtx.children[2]==ctx.parentCtx:
						assert self._current._atom_statement_right is None
						self._current._atom_statement_right = n
					elif ctx.parentCtx.parentCtx.children[0]==ctx.parentCtx:
						assert self._current._atom_statement_left is None
						self._current._atom_statement_left = n
					else:
						print('Something is wrong with id:'+ name)
				else:
					self._current._general_atom_statements_list.append(n)

			elif isinstance(n, PerceptionDifferenceStatement):
				if isinstance(ctx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
					if ctx.parentCtx.parentCtx.children[2]==ctx.parentCtx:
						assert self._current._atom_statement_right is None
						self._current._atom_statement_right = n
					elif ctx.parentCtx.parentCtx.children[0]==ctx.parentCtx:
						assert self._current._atom_statement_left is None
						self._current._atom_statement_left = n
					else:
						print('Something is wrong with id:'+ name)
				else:
					self._current._general_atom_statements_list.append(n)


			elif isinstance(n, VelocityStatement):
				if isinstance(ctx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
					if ctx.parentCtx.parentCtx.children[2]==ctx.parentCtx:
						assert self._current._atom_statement_right is None
						self._current._atom_statement_right = n
					elif ctx.parentCtx.parentCtx.children[0]==ctx.parentCtx:
						assert self._current._atom_statement_left is None
						self._current._atom_statement_left = n
					else:
						print('Something is wrong with id:'+ name)
				else:
					self._current._general_atom_statements_list.append(n)


			elif isinstance(n, SpeedStatement):
				if isinstance(ctx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
					if ctx.parentCtx.parentCtx.children[2]==ctx.parentCtx:
						assert self._current._atom_statement_right is None
						self._current._atom_statement_right = n
					elif ctx.parentCtx.parentCtx.children[0]==ctx.parentCtx:
						assert self._current._atom_statement_left is None
						self._current._atom_statement_left = n
					else:
						print('Something is wrong with id:'+ name)
				else:
					self._current._general_atom_statements_list.append(n)


			elif isinstance(n, AccelerationStatement):
				if isinstance(ctx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
					if ctx.parentCtx.parentCtx.children[2]==ctx.parentCtx:
						assert self._current._atom_statement_right is None
						self._current._atom_statement_right = n
					elif ctx.parentCtx.parentCtx.children[0]==ctx.parentCtx:
						assert self._current._atom_statement_left is None
						self._current._atom_statement_left = n
					else:
						print('Something is wrong with id:'+ name)
				else:
					self._current._general_atom_statements_list.append(n)

			elif isinstance(n, OverallStatement):
				if isinstance(ctx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
					if ctx.parentCtx.parentCtx.children[2]==ctx.parentCtx:
						assert self._current._atom_statement_right is None
						self._current._atom_statement_right = n
					elif ctx.parentCtx.parentCtx.children[0]==ctx.parentCtx:
						assert self._current._atom_statement_left is None
						self._current._atom_statement_left = n
					else:
						print('Something is wrong with id:'+ name)
				else:
					self._current._general_atom_statements_list.append(n)
			else:
				self._current._lane = Lane("0.0",name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'Lane'))

	def exitLaneID_laneID_var(self, ctx: AVScenariosParser.LaneID_laneID_varContext):
		pass

	def enterLaneID_str(self, ctx: AVScenariosParser.LaneID_strContext):
		pass
		# assert self._current._lane is None
		# assert self._current._string_expression is not None
		# context=ctx.parentCtx.parentCtx
		# # Construct an anonymous NameWithString and cast it to Lane
		# # Just for checking validity of this string
		# # strip the \"\"

		# #self._current._lane = Lane(ctx.children[0].getText()[1:-1])
		# self._current._lane = Lane(self._current._string_expression)
		# self._current._string_expression = None


	def exitLaneID_str(self, ctx: AVScenariosParser.LaneID_strContext):
		# print('Exit LaneID_str:  '+ctx.getText())
		# print(self._current._lane)
		#pass
		assert self._current._lane is None
		assert len(self._current._string_expression) >0
		# Construct an anonymous NameWithString and cast it to Lane
		# Just for checking validity of this string
		# strip the \"\"

		#self._current._lane = Lane(ctx.children[0].getText()[1:-1])
		self._current._lane = Lane(self._current._string_expression[-1])
		self._current._string_expression.pop()

	def enterHead_heading(self, ctx: AVScenariosParser.Head_headingContext):
		pass

	def exitHead_heading(self, ctx: AVScenariosParser.Head_headingContext):
		pass

	def enterHead_var(self, ctx: AVScenariosParser.Head_varContext):
		assert self._current._heading is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._heading = Heading(Unit.U_DEG, name)
		else:
			n, _ = ret
			if isinstance(n, Heading):
				self._current._heading = n
			else:
				self._current._heading = Heading(Unit.U_DEG,name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'Heading'))

	def exitHead_var(self, ctx: AVScenariosParser.Head_varContext):
		pass

	def enterHead_value(self, ctx: AVScenariosParser.Head_valueContext):
		# print('Enter Head_value:  '+ctx.getText())
		# print(self._current._real_value_expression)
		pass
		# assert self._current._heading is None
		# assert len(self._current._real_value_expression)>0
		# # anonymous heading
		# if ctx.children[1].getText() == 'deg':
		#   self._current._heading = Heading(Unit.U_DEG)
		# else:  # ctx.children[1].getText()=='rad'
		#   self._current._heading = Heading(Unit.U_RAD)
		# self._sema.begin_heading(self._current._real_value_expression[-1], self._current._heading)
		# self._current._real_value_expression.pop()

	def exitHead_value(self, ctx: AVScenariosParser.Head_valueContext):
		# print('Exit Head_value:  '+ctx.getText())
		# print(self._current._real_value_expression)
		assert self._current._heading is None
		# assert len(self._current._real_value_expression)>0
		# anonymous heading
		if ctx.children[1].getText() == 'deg':
			self._current._heading = Heading(Unit.U_DEG)
		else:  # ctx.children[1].getText()=='rad'
			self._current._heading = Heading(Unit.U_RAD)
		self._sema.begin_heading(self._current._real_value_expression[-1], self._current._heading)
		self._current._real_value_expression.pop()


		self._sema.end_heading(self._current._heading)
		self._current._direction = None




	def enterHead_pi_value(self, ctx: AVScenariosParser.Head_pi_valueContext):
		pass
		# print('Exit Head_value:  '+ctx.getText())
		# print(self._current._real_value_expression)
		# assert self._current._heading is None
		# assert len(self._current._real_value_expression)>0
		# # anonymous heading
		# if ctx.children[2].getText() == 'deg':
		#   self._current._heading = Heading(Unit.U_DEG)
		#   self._current._heading.set_pi_value()
		# else:  # ctx.children[2].getText()=='rad'
		#   self._current._heading = Heading(Unit.U_RAD)
		#   self._current._heading.set_pi_value()
		# self._sema.begin_heading(self._current._real_value_expression[-1], self._current._heading)
		# self._current._real_value_expression.pop()

	def exitHead_pi_value(self, ctx: AVScenariosParser.Head_pi_valueContext):
		# print('Exit Head_value:  '+ctx.getText())
		# print(self._current._real_value_expression)
		assert self._current._heading is None
		assert len(self._current._real_value_expression)>0
		# anonymous heading
		if ctx.children[2].getText() == 'deg':
			self._current._heading = Heading(Unit.U_DEG)
			self._current._heading.set_pi_value()
		else:  # ctx.children[2].getText()=='rad'
			self._current._heading = Heading(Unit.U_RAD)
			self._current._heading.set_pi_value()
		self._sema.begin_heading(self._current._real_value_expression[-1], self._current._heading)
		self._current._real_value_expression.pop()


		self._sema.end_heading(self._current._heading)
		self._current._direction = None











	# Enter a parse tree produced by AVScenariosParser#head_value_range.
	def enterHead_value_range(self, ctx:AVScenariosParser.Head_value_rangeContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#head_value_range.
	def exitHead_value_range(self, ctx:AVScenariosParser.Head_value_rangeContext):
		assert self._current._heading is None
		assert len(self._current._real_value_expression) == 2 
		rv_right = self._current._real_value_expression[-1]
		self._current._real_value_expression.pop()
		rv_left = self._current._real_value_expression[-1]
		self._current._real_value_expression.pop()
		rv = random.randint(rv_left*10000, rv_right*10000)
		rv = rv/10000
		# anonymous heading
		if ctx.children[6].getText() == 'deg':
			self._current._heading = Heading(Unit.U_DEG)
		else:  # ctx.children[1].getText()=='rad'
			self._current._heading = Heading(Unit.U_RAD)

		self._sema.begin_heading(rv, self._current._heading)

		self._sema.end_heading(self._current._heading)
		self._current._direction = None

	# Enter a parse tree produced by AVScenariosParser#head_pi_value_range.
	def enterHead_pi_value_range(self, ctx:AVScenariosParser.Head_pi_value_rangeContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#head_pi_value_range.
	def exitHead_pi_value_range(self, ctx:AVScenariosParser.Head_pi_value_rangeContext):
		assert self._current._heading is None
		assert len(self._current._real_value_expression) == 2
		rv_right = self._current._real_value_expression[-1]
		self._current._real_value_expression.pop()
		rv_left = self._current._real_value_expression[-1]
		self._current._real_value_expression.pop()
		rv = random.randint(rv_left*10000, rv_right*10000)
		rv = rv/10000

		# anonymous heading
		if ctx.children[8].getText() == 'deg':
			self._current._heading = Heading(Unit.U_DEG)
			self._current._heading.set_pi_value()
		else:  # ctx.children[2].getText()=='rad'
			self._current._heading = Heading(Unit.U_RAD)
			self._current._heading.set_pi_value()


		self._sema.begin_heading(rv, self._current._heading)

		self._sema.end_heading(self._current._heading)
		self._current._direction = None












	def enterHead_only_pi_value(self, ctx:AVScenariosParser.Head_only_pi_valueContext):
		assert self._current._heading is None
		# anonymous heading
		if ctx.children[1].getText() == 'deg':
			self._current._heading = Heading(Unit.U_DEG)
			self._current._heading.set_pi_value()
		else:  # ctx.children[1].getText()=='rad'
			self._current._heading = Heading(Unit.U_RAD)
			self._current._heading.set_pi_value()
		self._sema.begin_heading(1.0, self._current._heading)

	def exitHead_only_pi_value(self, ctx:AVScenariosParser.Head_only_pi_valueContext):
		self._sema.end_heading(self._current._heading)
		self._current._direction = None

	def enterUnit_deg(self, ctx: AVScenariosParser.Unit_degContext):
		pass

	def exitUnit_deg(self, ctx: AVScenariosParser.Unit_degContext):
		pass

	def enterUnit_rad(self, ctx: AVScenariosParser.Unit_radContext):
		pass

	def exitUnit_rad(self, ctx: AVScenariosParser.Unit_radContext):
		pass

	def enterDirection_pre(self, ctx: AVScenariosParser.Direction_preContext):
		pass

	def exitDirection_pre(self, ctx: AVScenariosParser.Direction_preContext):
		pass

	def enterPre_lane(self, ctx: AVScenariosParser.Pre_laneContext):
		assert self._current._direction is None
		self._current._direction = PredefinedDirection()


	def exitPre_lane(self, ctx: AVScenariosParser.Pre_laneContext):
		assert len(self._current._real_value_expression)>0
		self._current._direction._dis=self._current._real_value_expression[-1]
		self._current._real_value_expression.pop()
		self._sema.begin_direction(self._current._direction)

		self._sema.end_direction(self._current._direction)
		self._current._lane = None


	# def enterPre_lane_range(self, ctx:AVScenariosParser.Pre_lane_rangeContext):
	# 	assert self._current._direction is None
	# 	self._current._direction = PredefinedDirection()


	# def exitPre_lane_range(self, ctx:AVScenariosParser.Pre_lane_rangeContext):
	# 	assert len(self._current._real_value_expression) >= 2
	# 	rv_right = self._current._real_value_expression[-1]

	# 	print(self._current._real_value_expression)
	# 	self._current._real_value_expression.pop()
	# 	rv_left = self._current._real_value_expression[-1]
	# 	self._current._real_value_expression.pop()
	# 	rv = random.randint(rv_left*10000, rv_right*10000)
	# 	rv = rv/10000

	# 	self._current._direction._dis = rv
	# 	self._sema.begin_direction(self._current._direction)

	# 	self._sema.end_direction(self._current._direction)
	# 	self._current._lane = None


	def enterPre_ego(self, ctx: AVScenariosParser.Pre_egoContext):
		assert self._current._direction is None
		self._current._direction = PredefinedDirection()
		self._sema.begin_direction(self._current._direction)

	def exitPre_ego(self, ctx: AVScenariosParser.Pre_egoContext):
		pass

	def enterPre_id(self,ctx:AVScenariosParser.Pre_idContext):
		assert self._current._direction is None
		self._current._direction = PredefinedDirection()
		self._sema.begin_direction(self._current._direction)

	def exitPre_id(self,ctx:AVScenariosParser.Pre_idContext):
		name=ctx.children[0].getText()
		ret=self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name,ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
		else:
			n,_=ret
			if not isinstance(n,EgoVehicle) and not isinstance(n,Pedestrian) \
					and not isinstance(n,NPCVehicle):
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop - ctx.start.start,
													  ctx.children[0].stop.stop - ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'EgoVehicle','Pedestrian','NPCVehicle'))
			else:
				self._current._direction.set_reference(n)
				self._sema.end_direction(self._current._direction)
				self._current._lane = None

	def enterVehicle_vehicle_type(self, ctx: AVScenariosParser.Vehicle_vehicle_typeContext):
		pass

	def exitVehicle_vehicle_type(self, ctx: AVScenariosParser.Vehicle_vehicle_typeContext):
		pass

	def enterVehicle_vehicle_type_var(self, ctx: AVScenariosParser.Vehicle_vehicle_type_varContext):
		assert self._current._vehicle_type is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._vehicle_type = VehicleType(name)
		else:
			n, index = ret
			if isinstance(n, VehicleType) or isinstance(n,StateVehicleTypeStateListErrorType)\
					or isinstance(n,StateVehicleTypePedestrianTypeStateListErrorType):
				if not isinstance(n,VehicleType):
					n=self._sema.cast_to_vehicle_type(n)
					self._sema.set(index,n)
				self._current._vehicle_type = n
			else:
				self._current._vehicle_type = VehicleType(name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'VehicleType'))

	def exitVehicle_vehicle_type_var(self, ctx: AVScenariosParser.Vehicle_vehicle_type_varContext):
		pass

	def enterVehicle_type_(self, ctx: AVScenariosParser.Vehicle_type_Context):
		assert self._current._vehicle_type is None
		# anonymous vehicle type
		self._current._vehicle_type = VehicleType()
		self._sema.begin_vehicle_type(self._current._vehicle_type)

	# do not call:self._sema.begin_vehicle_type(self._current._vehicle_type)
	def exitVehicle_type_(self, ctx: AVScenariosParser.Vehicle_type_Context):
		self._sema.end_vehicle_type(self._current._vehicle_type)
		self._current._type = None

	def enterVehicle_type_color(self, ctx: AVScenariosParser.Vehicle_type_colorContext):
		assert self._current._vehicle_type is None
		# anonymous vehicle type
		self._current._vehicle_type = VehicleType()
		self._sema.begin_vehicle_type(self._current._vehicle_type)

	# do not call:self._sema.begin_vehicle_type(self._current._vehicle_type)
	def exitVehicle_type_color(self, ctx: AVScenariosParser.Vehicle_type_colorContext):
		self._sema.end_vehicle_type(self._current._vehicle_type)
		self._current._type = None
		self._current._color = None

	def enterType_type_(self, ctx: AVScenariosParser.Type_type_Context):
		pass

	def exitType_type_(self, ctx: AVScenariosParser.Type_type_Context):
		pass

	def enterType_var(self, ctx: AVScenariosParser.Type_varContext):
		assert self._current._type is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._type = SpecificType("Error Type", name)
		else:
			n, index = ret
			if isinstance(n, Type):
				self._current._type = n
			elif isinstance(n, NameWithString):
				t = self._sema.cast_to_type(n)
				self._sema.set(index, t)
				self._current._type = t
			else:
				self._current._type = SpecificType("Error Type",name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'GeneralType', 'SpecificType'))

	def exitType_var(self, ctx: AVScenariosParser.Type_varContext):
		pass

	def enterType_specific(self, ctx: AVScenariosParser.Type_specificContext):
		pass

	def exitType_specific(self, ctx: AVScenariosParser.Type_specificContext):
		pass

	def enterType_general(self, ctx: AVScenariosParser.Type_generalContext):
		pass

	def exitType_general(self, ctx: AVScenariosParser.Type_generalContext):
		pass

	def enterSpecific_str(self, ctx: AVScenariosParser.Specific_strContext):
		# construct an anonymous type with specific type
		pass

	def exitSpecific_str(self, ctx: AVScenariosParser.Specific_strContext):
		#pass
		assert self._current._type is None
		assert len(self._current._string_expression)>0
		self._current._type = SpecificType(self._current._string_expression[-1])
		self._current._string_expression.pop()
		#self._current._type = SpecificType(ctx.children[0].getText()[1:-1])

	def enterGeneral_car(self, ctx: AVScenariosParser.General_carContext):
		assert self._current._type is None
		self._current._type = GeneralType(GeneralTypeEnum.GT_CAR)

	def exitGeneral_car(self, ctx: AVScenariosParser.General_carContext):
		pass

	def enterGeneral_bus(self, ctx: AVScenariosParser.General_busContext):
		assert self._current._type is None
		self._current._type = GeneralType(GeneralTypeEnum.GT_BUS)

	def exitGeneral_bus(self, ctx: AVScenariosParser.General_busContext):
		pass

	def enterGeneral_van(self, ctx: AVScenariosParser.General_vanContext):
		assert self._current._type is None
		self._current._type = GeneralType(GeneralTypeEnum.GT_VAN)

	def exitGeneral_van(self, ctx: AVScenariosParser.General_vanContext):
		pass

	def enterGeneral_truck(self, ctx: AVScenariosParser.General_truckContext):
		assert self._current._type is None
		self._current._type = GeneralType(GeneralTypeEnum.GT_TRUCK)

	def exitGeneral_truck(self, ctx: AVScenariosParser.General_truckContext):
		pass

	def enterGeneral_bicycle(self, ctx: AVScenariosParser.General_bicycleContext):
		assert self._current._type is None
		self._current._type = GeneralType(GeneralTypeEnum.GT_BICYCLE)

	def exitGeneral_bicycle(self, ctx: AVScenariosParser.General_bicycleContext):
		pass

	def enterGeneral_motorbicycle(self, ctx: AVScenariosParser.General_motorbicycleContext):
		assert self._current._type is None
		self._current._type = GeneralType(GeneralTypeEnum.GT_MOTORBICYCLE)

	def exitGeneral_motorbicycle(self, ctx: AVScenariosParser.General_motorbicycleContext):
		pass

	def enterGeneral_tricycle(self, ctx: AVScenariosParser.General_tricycleContext):
		assert self._current._type is None
		self._current._typ = GeneralType(GeneralTypeEnum.GT_TRICYCLE)

	def exitGeneral_tricycle(self, ctx: AVScenariosParser.General_tricycleContext):
		pass

	def enterColor_color(self, ctx: AVScenariosParser.Color_colorContext):
		pass

	def exitColor_color(self, ctx: AVScenariosParser.Color_colorContext):
		pass

	def enterColor_var(self, ctx: AVScenariosParser.Color_varContext):
		assert self._current._color is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._color = RGBColor(0, 0, 0, name)
		else:
			n, _ = ret
			if isinstance(n, Color):
				self._current._color = n
			else:
				self._current._color = RGBColor(0,0,0,name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'RGBColor', 'ColorList'))

	def exitColor_var(self, ctx: AVScenariosParser.Color_varContext):
		pass

	def enterColor_color_list(self, ctx: AVScenariosParser.Color_color_listContext):
		pass

	def exitColor_color_list(self, ctx: AVScenariosParser.Color_color_listContext):
		pass

	def enterColor_rgb_color(self, ctx: AVScenariosParser.Color_rgb_colorContext):
		pass

	def exitColor_rgb_color(self, ctx: AVScenariosParser.Color_rgb_colorContext):
		pass

	def enterColor_red(self, ctx: AVScenariosParser.Color_redContext):
		assert self._current._color is None
		self._current._color = ColorList(ColorListEnum.CL_RED)

	def exitColor_red(self, ctx: AVScenariosParser.Color_redContext):
		pass

	def enterColor_green(self, ctx: AVScenariosParser.Color_greenContext):
		assert self._current._color is None
		self._current._color = ColorList(ColorListEnum.CL_GREEN)

	def exitColor_green(self, ctx: AVScenariosParser.Color_greenContext):
		pass

	def enterColor_blue(self, ctx: AVScenariosParser.Color_blueContext):
		assert self._current._color is None
		self._current._color = ColorList(ColorListEnum.CL_BLUE)

	def exitColor_blue(self, ctx: AVScenariosParser.Color_blueContext):
		pass

	def enterColor_black(self, ctx: AVScenariosParser.Color_blackContext):
		assert self._current._color is None
		self._current._color = ColorList(ColorListEnum.CL_BLACK)

	def exitColor_black(self, ctx: AVScenariosParser.Color_blackContext):
		pass

	def enterColor_white(self, ctx: AVScenariosParser.Color_whiteContext):
		assert self._current._color is None
		self._current._color = ColorList(ColorListEnum.CL_WHITE)

	def exitColor_white(self, ctx: AVScenariosParser.Color_whiteContext):
		pass

	def enterRgb_rgb(self, ctx: AVScenariosParser.Rgb_rgbContext):
		assert self._current._color is None
		self._current._color = self._sema.parse_rgb_color_internal(ctx.children[0].getText())

	def exitRgb_rgb(self, ctx: AVScenariosParser.Rgb_rgbContext):
		pass

	def enterNpc(self, ctx: AVScenariosParser.NpcContext):
		assert self._current._npc_vehicles is None
		self._current._npc_vehicles = NPCVehicles()

	def exitNpc(self, ctx: AVScenariosParser.NpcContext):
		# when we finish multinpc, we will add ,
		# therefore do not need to addVehicle here
		pass

	def enterMulti_npc(self, ctx: AVScenariosParser.Multi_npcContext):
		pass

	def exitMulti_npc(self, ctx: AVScenariosParser.Multi_npcContext):
		self._current._npc_vehicles.add_npc_vehicle(self._current._npc_vehicle)
		self._current._npc_vehicle = None

	def enterMulti_multi_npc(self, ctx: AVScenariosParser.Multi_multi_npcContext):
		pass

	def exitMulti_multi_npc(self, ctx: AVScenariosParser.Multi_multi_npcContext):
		self._current._npc_vehicles.add_npc_vehicle(self._current._npc_vehicle)
		self._current._npc_vehicle = None

	def enterNpc_vehicle_par(self, ctx: AVScenariosParser.Npc_vehicle_parContext):
		assert self._current._npc_vehicle is None
		self._current._states._flag = 1
		self._current._npc_vehicle = NPCVehicle()
		self._sema.begin_npc_vehicle(self._current._npc_vehicle)

	def exitNpc_vehicle_par(self, ctx: AVScenariosParser.Npc_vehicle_parContext):
		self._sema.end_npc_vehicle(self._current._npc_vehicle)
		self._current._vehicle_type = None
		self._current._name_with_motion = None
		self._current._states._first = None
		self._current._states._second = None
		self._current._states._flag = 0

	def enterNpc_npc_vehicle(self, ctx: AVScenariosParser.Npc_npc_vehicleContext):
		pass

	def exitNpc_npc_vehicle(self, ctx: AVScenariosParser.Npc_npc_vehicleContext):
		pass

	def enterNpc_npc_vehicle_var(self, ctx: AVScenariosParser.Npc_npc_vehicle_varContext):
		assert self._current._npc_vehicle is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._npc_vehicle = NPCVehicle(name)
		else:
			n, _ = ret
			if isinstance(n, NPCVehicle):
				self._current._npc_vehicle = n
			else:
				self._current._npc_vehicle =NPCVehicle(name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'NPCVehicle'))

	def exitNpc_npc_vehicle_var(self, ctx: AVScenariosParser.Npc_npc_vehicle_varContext):
		pass

	def enterPar_npc_state(self, ctx: AVScenariosParser.Par_npc_stateContext):
		pass

	def exitPar_npc_state(self, ctx: AVScenariosParser.Par_npc_stateContext):
		pass

	def enterPar_npc_state_vehicle(self, ctx: AVScenariosParser.Par_npc_state_vehicleContext):
		pass

	def exitPar_npc_state_vehicle(self, ctx: AVScenariosParser.Par_npc_state_vehicleContext):
		pass

	def enterPar_npc_state_vehicle_state(self, ctx: AVScenariosParser.Par_npc_state_vehicle_stateContext):
		pass

	def exitPar_npc_state_vehicle_state(self, ctx: AVScenariosParser.Par_npc_state_vehicle_stateContext):
		pass

	def enterVehicle_vehicle_motion(self, ctx: AVScenariosParser.Vehicle_vehicle_motionContext):
		self._current._states._flag = 0

	def exitVehicle_vehicle_motion(self, ctx: AVScenariosParser.Vehicle_vehicle_motionContext):
		self._current._states._flag = 2

	def enterVehicle_vehicle_motion_var(self, ctx: AVScenariosParser.Vehicle_vehicle_motion_varContext):
		assert self._current._name_with_motion is None
		self._current._states._flag = 0
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._name_with_motion = NameWithMotion(UniformMotion(), name)
		else:
			n, index = ret
			if isinstance(n, NameWithMotion):
				self._current._name_with_motion = n
				# cast to ast tree
				self._sema.set(index, VehicleMotion(n.get_motion(), n.get_name()))
			elif isinstance(n, VehicleMotion):
				self._current._name_with_motion = self._sema.cast_to_motion(n)
			else:
				self._current._name_with_motion = NameWithMotion(UniformMotion(),name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'VehicleMotion'))

	def exitVehicle_vehicle_motion_var(self, ctx: AVScenariosParser.Vehicle_vehicle_motion_varContext):
		self._current._states._flag = 2

	def enterVehicle_motion_uniform(self, ctx: AVScenariosParser.Vehicle_motion_uniformContext):
		pass

	def exitVehicle_motion_uniform(self, ctx: AVScenariosParser.Vehicle_motion_uniformContext):
		pass

	def enterVehicle_motion_waypoint(self, ctx: AVScenariosParser.Vehicle_motion_waypointContext):
		pass

	def exitVehicle_motion_waypoint(self, ctx: AVScenariosParser.Vehicle_motion_waypointContext):
		pass

	def enterUniform(self, ctx: AVScenariosParser.UniformContext):
		self._current._states._flag = 0
		assert self._current._name_with_motion is None
		self._current._name_with_motion = NameWithMotion(UniformMotion())
		self._sema.begin_motion(self._current._name_with_motion, True)

	def exitUniform(self, ctx: AVScenariosParser.UniformContext):
		# here we do not need set index
		self._sema.end_motion(self._current._name_with_motion, True)
		self._current._states._value = None

	def enterUniform_Uniform(self, ctx: AVScenariosParser.Uniform_UniformContext):
		self._current._name_with_motion.get_motion().set_uniform_index(UniformIndex.UI_Uniform)

	def exitUniform_Uniform(self, ctx: AVScenariosParser.Uniform_UniformContext):
		pass

	def enterUniform_uniform(self, ctx: AVScenariosParser.Uniform_uniformContext):
		self._current._name_with_motion.get_motion().set_uniform_index(UniformIndex.UI_uniform)

	def exitUniform_uniform(self, ctx: AVScenariosParser.Uniform_uniformContext):
		pass

	def enterWaypoint(self, ctx: AVScenariosParser.WaypointContext):
		self._current._states._flag = 0
		assert self._current._name_with_motion is None
		self._current._name_with_motion = NameWithMotion(WaypointMotion())
		self._sema.begin_motion(self._current._name_with_motion, False)

	def exitWaypoint(self, ctx: AVScenariosParser.WaypointContext):
		# here we do not need set index
		self._sema.end_motion(self._current._name_with_motion, False)
		self._current._state_list = None

	def enterWaypoint_Waypoint(self, ctx: AVScenariosParser.Waypoint_WaypointContext):
		self._current._name_with_motion.get_motion().set_waypoint_index(WaypointIndex.WI_Waypoint)

	def exitWaypoint_Waypoint(self, ctx: AVScenariosParser.Waypoint_WaypointContext):
		pass

	def enterWaypoint_W(self, ctx: AVScenariosParser.Waypoint_WContext):
		self._current._name_with_motion.get_motion().set_waypoint_index(WaypointIndex.WI_W)

	def exitWaypoint_W(self, ctx: AVScenariosParser.Waypoint_WContext):
		pass

	def enterWaypoint_WP(self, ctx: AVScenariosParser.Waypoint_WPContext):
		self._current._name_with_motion.get_motion().set_waypoint_index(WaypointIndex.WI_WP)

	def exitWaypoint_WP(self, ctx: AVScenariosParser.Waypoint_WPContext):
		pass

	def enterWaypoint_wp(self, ctx: AVScenariosParser.Waypoint_wpContext):
		self._current._name_with_motion.get_motion().set_waypoint_index(WaypointIndex.WI_wp)

	def exitWaypoint_wp(self, ctx: AVScenariosParser.Waypoint_wpContext):
		pass

	def enterWaypoint_waypoint(self, ctx: AVScenariosParser.Waypoint_waypointContext):
		self._current._name_with_motion.get_motion().set_waypoint_index(WaypointIndex.WI_waypoint)

	def exitWaypoint_waypoint(self, ctx: AVScenariosParser.Waypoint_waypointContext):
		pass

	def enterWaypoint_w(self, ctx: AVScenariosParser.Waypoint_wContext):
		self._current._name_with_motion.get_motion().set_waypoint_index(WaypointIndex.WI_w)

	def exitWaypoint_w(self, ctx: AVScenariosParser.Waypoint_wContext):
		pass

	def enterState_state_list(self, ctx: AVScenariosParser.State_state_listContext):
		pass

	def exitState_state_list(self, ctx: AVScenariosParser.State_state_listContext):
		pass

	def enterState_state_list_var(self, ctx: AVScenariosParser.State_state_list_varContext):
		assert self._current._state_list is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._state_list = StateList(name)
		else:
			n, index = ret
			if isinstance(n, StateList) or isinstance(n,StateStateListErrorType)\
					or isinstance(n,StateVehicleTypePedestrianTypeStateListErrorType)\
					or isinstance(n,StateVehicleTypeStateListErrorType):
				if not isinstance(n,StateList):
					n=self._sema.cast_to_state_list(n)
					self._sema.set(index,n)
				self._current._state_list = n
			else:
				self._current._state_list = StateList(name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'StateList'))

	def exitState_state_list_var(self, ctx: AVScenariosParser.State_state_list_varContext):
		pass

	def enterState_list_multi(self, ctx: AVScenariosParser.State_list_multiContext):
		self._current._states._flag = 0
		self._current._state_list = StateList()

	def exitState_list_multi(self, ctx: AVScenariosParser.State_list_multiContext):
		pass

	def enterMulti_states_par(self, ctx: AVScenariosParser.Multi_states_parContext):
		pass

	def exitMulti_states_par(self, ctx: AVScenariosParser.Multi_states_parContext):
		# NOTICE:add state to the StateList and release it
		assert self._current._states._value is not None
		self._current._state_list.add_state(self._current._states._value)
		self._current._states._value = None

	def enterMulti_states_par_state(self, ctx: AVScenariosParser.Multi_states_par_stateContext):
		pass

	def exitMulti_states_par_state(self, ctx: AVScenariosParser.Multi_states_par_stateContext):
		# NOTICE:add state to the StateList and release it
		assert self._current._states._value is not None
		self._current._state_list.add_state(self._current._states._value)
		self._current._states._value = None

	def enterPedestrians_multi(self, ctx: AVScenariosParser.Pedestrians_multiContext):
		assert self._current._pedestrians is None
		self._current._pedestrians = Pedestrians()

	def exitPedestrians_multi(self, ctx: AVScenariosParser.Pedestrians_multiContext):
		# when we finish multiped, we will add ,
		# therefore do not need to add_pedestrian here
		pass

	def enterMulti_pedestrian(self, ctx: AVScenariosParser.Multi_pedestrianContext):
		pass

	def exitMulti_pedestrian(self, ctx: AVScenariosParser.Multi_pedestrianContext):
		self._current._pedestrians.add_pedestrian(self._current._pedestrian)
		self._current._pedestrian = None

	def enterMulti_multi_pedestrian(self, ctx: AVScenariosParser.Multi_multi_pedestrianContext):
		pass

	def exitMulti_multi_pedestrian(self, ctx: AVScenariosParser.Multi_multi_pedestrianContext):
		self._current._pedestrians.add_pedestrian(self._current._pedestrian)
		self._current._pedestrian = None

	def enterPedestrian_pedestrian(self, ctx: AVScenariosParser.Pedestrian_pedestrianContext):
		pass

	def exitPedestrian_pedestrian(self, ctx: AVScenariosParser.Pedestrian_pedestrianContext):
		pass

	def enterPedestrian_pedestrian_var(self, ctx: AVScenariosParser.Pedestrian_pedestrian_varContext):
		assert self._current._pedestrian is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._pedestrian = Pedestrian(name)
		else:
			n, _ = ret
			if isinstance(n, Pedestrian):
				self._current._pedestrian = n
			else:
				self._current._pedestrian = Pedestrian(name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'Pedestrian'))

	def exitPedestrian_pedestrian_var(self, ctx: AVScenariosParser.Pedestrian_pedestrian_varContext):
		pass

	def enterPedestrian_par(self, ctx: AVScenariosParser.Pedestrian_parContext):
		assert self._current._pedestrian is None
		self._current._pedestrian = Pedestrian()
		self._current._states._flag = 1
		self._sema.begin_pedestrian(self._current._pedestrian)

	def exitPedestrian_par(self, ctx: AVScenariosParser.Pedestrian_parContext):
		self._sema.end_pedestrian(self._current._pedestrian)
		self._current._states._first = None
		self._current._states._second = None
		self._current._name_with_motion = None
		self._current._pedestrian_type = None

	def enterPar_ped_state(self, ctx: AVScenariosParser.Par_ped_stateContext):
		pass

	def exitPar_ped_state(self, ctx: AVScenariosParser.Par_ped_stateContext):
		pass

	def enterPar_ped_state_ped(self, ctx: AVScenariosParser.Par_ped_state_pedContext):
		pass

	def exitPar_ped_state_ped(self, ctx: AVScenariosParser.Par_ped_state_pedContext):
		pass

	def enterPar_ped_state_ped_state(self, ctx: AVScenariosParser.Par_ped_state_ped_stateContext):
		pass

	def exitPar_ped_state_ped_state(self, ctx: AVScenariosParser.Par_ped_state_ped_stateContext):
		pass

	def enterPedestrian_motion_pedestrian(self, ctx: AVScenariosParser.Pedestrian_motion_pedestrianContext):
		self._current._states._flag = 0

	def exitPedestrian_motion_pedestrian(self, ctx: AVScenariosParser.Pedestrian_motion_pedestrianContext):
		self._current._states._flag = 2

	def enterPedestrian_motion_pedestrian_var(self, ctx: AVScenariosParser.Pedestrian_motion_pedestrian_varContext):
		assert self._current._name_with_motion is None
		self._current._states._flag = 0
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._name_with_motion = NameWithMotion(UniformMotion(), name)
		else:
			n, index = ret
			if isinstance(n, PedestrianMotion):
				self._current._name_with_motion = self._sema.cast_to_motion(n)
			elif isinstance(n, NameWithMotion):
				self._current._name_with_motion = n
				# cast to ast tree
				self._sema.set(index, PedestrianMotion(n.get_motion(), n.get_name()))
			else:
				self._current._name_with_motion = NameWithMotion(UniformMotion(),name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'PedestrianMotion'))

	def exitPedestrian_motion_pedestrian_var(self, ctx: AVScenariosParser.Pedestrian_motion_pedestrian_varContext):
		self._current._states._flag = 2

	def enterPedestrian_uniform(self, ctx: AVScenariosParser.Pedestrian_uniformContext):
		pass

	def exitPedestrian_uniform(self, ctx: AVScenariosParser.Pedestrian_uniformContext):
		pass

	def enterPedestrian_waypoint(self, ctx: AVScenariosParser.Pedestrian_waypointContext):
		pass

	def exitPedestrian_waypoint(self, ctx: AVScenariosParser.Pedestrian_waypointContext):
		pass

	def enterPedestrian_pedestrian_type(self, ctx: AVScenariosParser.Pedestrian_pedestrian_typeContext):
		pass

	def exitPedestrian_pedestrian_type(self, ctx: AVScenariosParser.Pedestrian_pedestrian_typeContext):
		pass

	def enterPedestrian_pedestrian_type_var(self, ctx: AVScenariosParser.Pedestrian_pedestrian_type_varContext):
		assert self._current._pedestrian_type is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._pedestrian_type = PedestrianType(name)
		else:
			n, index = ret
			if isinstance(n, PedestrianType) or isinstance(n,StateVehicleTypePedestrianTypeStateListErrorType):
				if not isinstance(n,PedestrianType):
					n=self._sema.cast_to_pedestrian_type(n)
					self._sema.set(index,n)
				self._current._pedestrian_type=n
			elif isinstance(n, NameWithString):
				# assert len(self._current._string_expression)==1
				self._current._name_of_ped_type=n._value
				assert self._current._pedestrian_type is None


				self._current._pedestrian_type = PedestrianType()
				self._sema.begin_pedestrian_type(self._current._pedestrian_type)

				assert len(self._current._string_expression) == 0
				# self._current._name_of_ped_type = ctx.getText()
				# self._current._string_expression.pop()
				self._sema.end_pedestrian_type(self._current._pedestrian_type)
				self._current._name_of_ped_type = None


			else:
				self._current._pedestrian_type = PedestrianType(name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'PedestrianType'))

	def exitPedestrian_pedestrian_type_var(self, ctx: AVScenariosParser.Pedestrian_pedestrian_type_varContext):
		pass

	def enterPedestrian_type_height_color(self, ctx: AVScenariosParser.Pedestrian_type_height_colorContext):
		assert self._current._pedestrian_type is None
		self._current._pedestrian_type = PedestrianType()
		self._sema.begin_pedestrian_type(self._current._pedestrian_type)

	# do not call:self._sema.begin_pedestrian(self._current._pedestrian_type)
	def exitPedestrian_type_height_color(self, ctx: AVScenariosParser.Pedestrian_type_height_colorContext):
		self._sema.end_pedestrian_type(self._current._pedestrian_type)
		self._current._height = None
		self._current._color = None





	# Enter a parse tree produced by AVScenariosParser#pedestrian_type_name.
	def enterPedestrian_type_name(self, ctx:AVScenariosParser.Pedestrian_type_nameContext):
		assert self._current._pedestrian_type is None
		self._current._pedestrian_type = PedestrianType()
		self._sema.begin_pedestrian_type(self._current._pedestrian_type)
		pass

	# Exit a parse tree produced by AVScenariosParser#pedestrian_type_name.
	def exitPedestrian_type_name(self, ctx:AVScenariosParser.Pedestrian_type_nameContext):
		# print('exitPedestrian_type_name:  '+ ctx.getText())
		# assert len(self._current._string_expression) == 0
		name=ctx.getText()
		self._current._name_of_ped_type = name[1:-1]
		# self._current._string_expression.pop()
		self._sema.end_pedestrian_type(self._current._pedestrian_type)
		self._current._name_of_ped_type = None











	def enterHeight_height(self, ctx: AVScenariosParser.Height_heightContext):
		pass

	def exitHeight_height(self, ctx: AVScenariosParser.Height_heightContext):
		pass

	def enterHeight_var(self, ctx: AVScenariosParser.Height_varContext):
		assert self._current._height is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._height = Height(0, name)
		else:
			n, index = ret
			if isinstance(n, Height):
				self._current._height = n
			if isinstance(n, NameWithRealValue):
				h = self._sema.cast_to_height(n)
				self._sema.set(index, h)
				self._current._height = h
			else:
				self._current._height = Height(0,name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'Height'))

	def exitHeight_var(self, ctx: AVScenariosParser.Height_varContext):
		pass

	def enterHeight_rv(self, ctx: AVScenariosParser.Height_rvContext):
		pass


	def exitHeight_rv(self, ctx: AVScenariosParser.Height_rvContext):
		assert self._current._height is None
		assert len(self._current._real_value_expression)>0
		# height must be real value
		self._current._height = Height(self._current._real_value_expression[-1])
		self._current._real_value_expression.pop()


	def enterObstacles_multi(self, ctx: AVScenariosParser.Obstacles_multiContext):
		assert self._current._obstacles is None
		self._current._obstacles = Obstacles()

	def exitObstacles_multi(self, ctx: AVScenariosParser.Obstacles_multiContext):
		# when we finish multi obstacles, we will add,
		# therefore do not need to add_obstacle here
		pass

	def enterObstacles_empty(self, ctx: AVScenariosParser.Obstacles_emptyContext):
		pass

	def exitObstacles_empty(self, ctx: AVScenariosParser.Obstacles_emptyContext):
		pass

	def enterObstacles_obstacle(self, ctx: AVScenariosParser.Obstacles_obstacleContext):
		pass

	def exitObstacles_obstacle(self, ctx: AVScenariosParser.Obstacles_obstacleContext):
		self._current._obstacles.add_obstacle(self._current._obstacle)
		self._current._obstacle = None

	def enterObstacles_multi_obstacle(self, ctx: AVScenariosParser.Obstacles_multi_obstacleContext):
		pass

	def exitObstacles_multi_obstacle(self, ctx: AVScenariosParser.Obstacles_multi_obstacleContext):
		self._current._obstacles.add_obstacle(self._current._obstacle)
		self._current._obstacle = None

	def enterObstacle_obstacle(self, ctx: AVScenariosParser.Obstacle_obstacleContext):
		pass

	def exitObstacle_obstacle(self, ctx: AVScenariosParser.Obstacle_obstacleContext):
		pass

	def enterObstacle_obstacle_var(self, ctx: AVScenariosParser.Obstacle_obstacle_varContext):
		assert self._current._obstacle is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._obstacle = Obstacle(name)
		else:
			n, _ = ret
			if isinstance(n, Obstacle):
				self._current._obstacle = n
			else:
				self._current._obstacle = Obstacle(name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'Obstacle'))

	def exitObstacle_obstacle_var(self, ctx: AVScenariosParser.Obstacle_obstacle_varContext):
		pass

	def enterObstacle_para(self, ctx: AVScenariosParser.Obstacle_paraContext):
		assert self._current._obstacle is None
		self._current._obstacle = Obstacle()
		self._sema.begin_obstacle(self._current._obstacle)

	def exitObstacle_para(self, ctx: AVScenariosParser.Obstacle_paraContext):
		self._sema.end_obstacle(self._current._obstacle)
		self._current._position = None
		self._current._shape = None

	def enterPar_position_shape(self, ctx: AVScenariosParser.Par_position_shapeContext):
		pass

	def exitPar_position_shape(self, ctx: AVScenariosParser.Par_position_shapeContext):
		pass

	def enterShape_shape_var(self, ctx: AVScenariosParser.Shape_shape_varContext):
		assert self._current._shape is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._shape = Shape(name)
		else:
			n, _ = ret
			if isinstance(n, Shape):
				self._current._shape = n
			else:
				self._current._shape = Shape(name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'Shape'))

	def exitShape_shape_var(self, ctx: AVScenariosParser.Shape_shape_varContext):
		pass

	def enterShape_shape(self, ctx: AVScenariosParser.Shape_shapeContext):
		pass

	def exitShape_shape(self, ctx: AVScenariosParser.Shape_shapeContext):
		pass

	def enterShape_sphere(self, ctx: AVScenariosParser.Shape_sphereContext):
		pass

	def exitShape_sphere(self, ctx: AVScenariosParser.Shape_sphereContext):
		pass

	def enterShape_box(self, ctx: AVScenariosParser.Shape_boxContext):
		pass

	def exitShape_box(self, ctx: AVScenariosParser.Shape_boxContext):
		pass

	def enterShape_cone(self, ctx: AVScenariosParser.Shape_coneContext):
		pass

	def exitShape_cone(self, ctx: AVScenariosParser.Shape_coneContext):
		pass

	def enterShape_cylinder(self, ctx: AVScenariosParser.Shape_cylinderContext):
		pass

	def exitShape_cylinder(self, ctx: AVScenariosParser.Shape_cylinderContext):
		pass

	def enterSphere_sphere(self, ctx: AVScenariosParser.Sphere_sphereContext):
		pass

	def exitSphere_sphere(self, ctx: AVScenariosParser.Sphere_sphereContext):
		assert self._current._shape is None
		assert len(self._current._real_value_expression)>0
		self._current._shape = Sphere(self._current._real_value_expression[-1])
		self._current._real_value_expression.pop()

	def enterBox_box(self, ctx: AVScenariosParser.Box_boxContext):
		pass

	def exitBox_box(self, ctx: AVScenariosParser.Box_boxContext):
		assert self._current._shape is None
		assert len(self._current._real_value_expression)>2
		self._current._shape = Box(self._current._real_value_expression[-2], self._current._real_value_expression[-2]
								   , self._current._real_value_expression[-1])
		self._current._real_value_expression.pop()
		self._current._real_value_expression.pop()
		self._current._real_value_expression.pop()


	def enterCone_cone(self, ctx: AVScenariosParser.Cone_coneContext):
		pass

	def exitCone_cone(self, ctx: AVScenariosParser.Cone_coneContext):
		assert self._current._shape is None
		assert len(self._current._real_value_expression)>1
		self._current._shape = Cone(self._current._real_value_expression[-2], self._current._real_value_expression[-1])

	def enterCylinder_cylinder(self, ctx: AVScenariosParser.Cylinder_cylinderContext):
		pass

	def exitCylinder_cylinder(self, ctx: AVScenariosParser.Cylinder_cylinderContext):
		assert self._current._shape is None
		assert len(self._current._real_value_expression)>1
		self._current._shape = Cylinder(self._current._real_value_expression[-2], self._current._real_value_expression[-1])

	def enterEnv_var(self, ctx: AVScenariosParser.Env_varContext):
		assert self._current._env is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._env = Environment(name)
		else:
			n, _ = ret
			if isinstance(n, Environment):
				self._current._env = n
			else:
				self._current._env = Environment(name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'Environment'))

	def exitEnv_var(self, ctx: AVScenariosParser.Env_varContext):
		pass

	def enterEnv_env(self, ctx: AVScenariosParser.Env_envContext):
		pass

	def exitEnv_env(self, ctx: AVScenariosParser.Env_envContext):
		pass

	def enterEnv_empty(self, ctx: AVScenariosParser.Env_emptyContext):
		pass

	def exitEnv_empty(self, ctx: AVScenariosParser.Env_emptyContext):
		pass

	def enterEnv_par(self, ctx: AVScenariosParser.Env_parContext):
		assert self._current._env is None
		self._current._env = Environment()
		self._sema.begin_env(self._current._env)

	def exitEnv_par(self, ctx: AVScenariosParser.Env_parContext):
		self._sema.end_env(self._current._env)
		self._current._time = None
		self._current._weathers = None

	def enterPar_time_weather(self, ctx: AVScenariosParser.Par_time_weatherContext):
		pass

	def exitPar_time_weather(self, ctx: AVScenariosParser.Par_time_weatherContext):
		pass

	def enterWeather_var(self, ctx: AVScenariosParser.Weather_varContext):
		assert self._current._weathers is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._weathers = Weathers(name)
		else:
			n, index = ret
			if isinstance(n, Weathers) or isinstance(n,PedestriansNPCVehiclesObstaclesWeathersTrafficErrorType):
				if not isinstance(n,Weathers):
					n=self._sema.cast_to_weathers(n)
					self._sema.set(index,n)
				self._current._weathers = n
			else:
				self._current._weathers = Weathers(name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'Weathers'))

	def exitWeather_var(self, ctx: AVScenariosParser.Weather_varContext):
		pass

	def enterWeather_wtr(self, ctx: AVScenariosParser.Weather_wtrContext):
		pass

	def exitWeather_wtr(self, ctx: AVScenariosParser.Weather_wtrContext):
		pass

	def enterTime_time(self, ctx: AVScenariosParser.Time_timeContext):
		pass

	def exitTime_time(self, ctx: AVScenariosParser.Time_timeContext):
		pass

	def enterTime_time_var(self, ctx: AVScenariosParser.Time_time_varContext):
		assert self._current._time is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._time = Time(0, 0, name)
		else:
			n, _ = ret
			if isinstance(n, Time):
				self._current._time = n
			else:
				self._current._time = Time(0,0,name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'Time'))


	def exitTime_time_var(self, ctx: AVScenariosParser.Time_time_varContext):
		pass

	def enterTime_Time(self, ctx: AVScenariosParser.Time_TimeContext):
		assert self._current._time is None
		self._current._time = self._sema.parse_time_from_internal(ctx.children[0].getText())

	def exitTime_Time(self, ctx: AVScenariosParser.Time_TimeContext):
		pass

	def enterWeathers(self, ctx: AVScenariosParser.WeathersContext):
		assert self._current._weathers is None
		self._current._weathers = Weathers()

	def exitWeathers(self, ctx: AVScenariosParser.WeathersContext):
		# when we finish multiweather, we will add ,
		# therefore do not need to add_weather here
		pass

	def enterWeathers_weather(self, ctx: AVScenariosParser.Weathers_weatherContext):
		pass

	def exitWeathers_weather(self, ctx: AVScenariosParser.Weathers_weatherContext):
		self._current._weathers.add_weather(self._current._weather)
		self._current._weather = None

	def enterWeathers_multi_weather(self, ctx: AVScenariosParser.Weathers_multi_weatherContext):
		pass

	def exitWeathers_multi_weather(self, ctx: AVScenariosParser.Weathers_multi_weatherContext):
		self._current._weathers.add_weather(self._current._weather)
		self._current._weather = None

	def enterWeather_weather_var(self, ctx: AVScenariosParser.Weather_weather_varContext):
		assert self._current._weather is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._weather = Weather(name)
		else:
			n, _ = ret
			if isinstance(n, Weather):
				self._current._weather = n
			else:
				self._current._weather = Weather(name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'Weather'))

	def exitWeather_weather_var(self, ctx: AVScenariosParser.Weather_weather_varContext):
		pass

	def enterWeather_weather(self, ctx: AVScenariosParser.Weather_weatherContext):
		pass

	def exitWeather_weather(self, ctx: AVScenariosParser.Weather_weatherContext):
		pass

	def enterWeather_continuous(self, ctx: AVScenariosParser.Weather_continuousContext):
		assert self._current._weather is None
		self._current._weather = Weather()
		self._sema.begin_weather(self._current._weather)

	def exitWeather_continuous(self, ctx: AVScenariosParser.Weather_continuousContext):
		self._sema.end_weather(self._current._weather)
		self._current._weather_continuous = None
		self._current._weather_discrete = None

	def enterWeather_discrete(self, ctx: AVScenariosParser.Weather_discreteContext):
		assert self._current._weather is None
		self._current._weather = Weather()
		self._sema.begin_weather(self._current._weather)

	def exitWeather_discrete(self, ctx: AVScenariosParser.Weather_discreteContext):
		self._sema.end_weather(self._current._weather)
		self._current._weather_continuous = None
		self._current._weather_discrete = None

	def enterKind_sunny(self, ctx: AVScenariosParser.Kind_sunnyContext):
		self._current._weather.set_weather_kind(WeatherKind.WK_SUNNY)

	def exitKind_sunny(self, ctx: AVScenariosParser.Kind_sunnyContext):
		pass

	def enterKind_fog(self, ctx: AVScenariosParser.Kind_fogContext):
		self._current._weather.set_weather_kind(WeatherKind.WK_FOG)

	def exitKind_fog(self, ctx: AVScenariosParser.Kind_fogContext):
		pass

	def enterKind_rain(self, ctx: AVScenariosParser.Kind_rainContext):
		self._current._weather.set_weather_kind(WeatherKind.WK_RAIN)

	def exitKind_rain(self, ctx: AVScenariosParser.Kind_rainContext):
		pass

	def enterKind_snow(self, ctx: AVScenariosParser.Kind_snowContext):
		self._current._weather.set_weather_kind(WeatherKind.WK_SNOW)

	def exitKind_snow(self, ctx: AVScenariosParser.Kind_snowContext):
		pass

	def enterKind_wetness(self, ctx: AVScenariosParser.Kind_wetnessContext):
		self._current._weather.set_weather_kind(WeatherKind.WK_WETNESS)

	def exitKind_wetness(self, ctx: AVScenariosParser.Kind_wetnessContext):
		pass

	def enterWeather_continuous_value(self, ctx: AVScenariosParser.Weather_continuous_valueContext):
		assert self._current._weather_continuous is None
		v = ctx.children[0].getText()
		context=ctx.parentCtx
		vf = float(v)
		if not (0 <= vf <= 1 and len(v) == 3):
			self._sema.add_error(
				WeatherContinuousIndexFormatError(context.children[2].getText(), context.children[2].start.line,
												  context.children[2].start.column
												  , context.children[2].start.stop - context.start.start,
												  context.children[2].stop.stop - context.start.start
												  , context.getText()))
			# construct an empty WeatherContinuousIndex
			self._current._weather_continuous = WeatherContinuousIndex(0)
		else:
			self._current._weather_continuous = \
				WeatherContinuousIndex(float(ctx.children[0].getText()))


	def exitWeather_continuous_value(self, ctx: AVScenariosParser.Weather_continuous_valueContext):
		pass

	def enterWeather_continuous_var(self, ctx: AVScenariosParser.Weather_continuous_varContext):
		assert self._current._weather_continuous is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._weather_continuous = WeatherContinuousIndex(0, name)
		else:
			n, index = ret
			if isinstance(n, WeatherContinuousIndex):
				self._current._weather_continuous = n
			if isinstance(n, NameWithRealValue):
				value=n.get_value()
				context = self._sema.find_context_for_error(n.get_name())
				if not (0 <= value <= 1 and len(str(value)) == 3):
					self._sema.add_error(WeatherContinuousIndexFormatError(context.children[2].getText(), context.children[2].start.line,
														 context.children[2].start.column
														 , context.children[2].start.stop - context.start.start,
														 context.children[2].stop.stop - context.start.start
														 , context.getText()))
					# construct an empty WeatherContinuousIndex
					wi = WeatherContinuousIndex(0,name)
				else:
					wi = self._sema.cast_to_weather_continuous_index(n)
				self._sema.set(index, wi)
				self._current._weather_continuous = wi
			else:
				self._current._weather_continuous = WeatherContinuousIndex(0,name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'WeatherContinuousIndex'))

	def exitWeather_continuous_var(self, ctx: AVScenariosParser.Weather_continuous_varContext):
		pass

	def enterWeather_discrete_level_par(self, ctx: AVScenariosParser.Weather_discrete_level_parContext):
		assert self._current._weather_discrete is None
		if ctx.children[0].getText() == 'light':
			self._current._weather_discrete = WeatherDiscreteLevel(WeatherDiscreteLevelEnum.WDL_LIGHT)
		elif ctx.children[0].getText() == 'middle':
			self._current._weather_discrete = WeatherDiscreteLevel(WeatherDiscreteLevelEnum.WDL_MIDDLE)
		elif ctx.children[0].getText() == 'heavy':
			self._current._weather_discrete = WeatherDiscreteLevel(WeatherDiscreteLevelEnum.WDL_HEAVY)

	def exitWeather_discrete_level_par(self, ctx: AVScenariosParser.Weather_discrete_level_parContext):
		pass

	def enterWeather_discrete_light(self, ctx: AVScenariosParser.Weather_discrete_lightContext):
		pass

	def exitWeather_discrete_light(self, ctx: AVScenariosParser.Weather_discrete_lightContext):
		pass

	def enterWeather_discrete_middle(self, ctx: AVScenariosParser.Weather_discrete_middleContext):
		pass

	def exitWeather_discrete_middle(self, ctx: AVScenariosParser.Weather_discrete_middleContext):
		pass

	def enterWeather_discrete_heavy(self, ctx: AVScenariosParser.Weather_discrete_heavyContext):
		pass

	def exitWeather_discrete_heavy(self, ctx: AVScenariosParser.Weather_discrete_heavyContext):
		pass

	def enterWeather_discrete_var(self, ctx: AVScenariosParser.Weather_discrete_varContext):
		assert self._current._weather_discrete is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._weather_discrete = WeatherDiscreteLevel(WeatherDiscreteLevelEnum.WDL_LIGHT, name)
		else:
			n, _ = ret
			if isinstance(n, WeatherDiscreteLevel):
				self._current._weather_discrete = n
			else:
				self._current._weather_discrete = WeatherDiscreteLevel(WeatherDiscreteLevelEnum.WDL_LIGHT,name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'WeatherDiscreteLevel'))

	def exitWeather_discrete_var(self, ctx: AVScenariosParser.Weather_discrete_varContext):
		pass

	def enterTraffic_traffic(self, ctx: AVScenariosParser.Traffic_trafficContext):
		pass

	def exitTraffic_traffic(self, ctx: AVScenariosParser.Traffic_trafficContext):
		pass

	def enterTraffic_stmt(self, ctx: AVScenariosParser.Traffic_stmtContext):
		pass

	def exitTraffic_stmt(self, ctx: AVScenariosParser.Traffic_stmtContext):
		pass

	def enterIntersection(self, ctx: AVScenariosParser.IntersectionContext):
		pass

	def exitIntersection(self, ctx: AVScenariosParser.IntersectionContext):
		pass

	def enterMeta_intersection_meta_var(self, ctx: AVScenariosParser.Meta_intersection_meta_varContext):
		assert self._current._intersection_traffic is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._intersection_traffic = IntersectionTraffic(name)
		else:
			n, _ = ret
			if isinstance(n, IntersectionTraffic):
				self._current._intersection_traffic = n
			else:
				self._current._intersection_traffic = IntersectionTraffic(name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'IntersectionTraffic'))
		self._current._traffic.add_intersection_traffic(self._current._intersection_traffic)
		self._current._intersection_traffic = None

	def exitMeta_intersection_meta_var(self, ctx: AVScenariosParser.Meta_intersection_meta_varContext):
		pass

	def enterMeta_intersection_meta(self, ctx: AVScenariosParser.Meta_intersection_metaContext):
		pass

	def exitMeta_intersection_meta(self, ctx: AVScenariosParser.Meta_intersection_metaContext):
		# add to the traffic.
		self._current._traffic.add_intersection_traffic(self._current._intersection_traffic)
		self._current._intersection_traffic = None

	def enterMeta_intersection_intersection(self, ctx: AVScenariosParser.Meta_intersection_intersectionContext):
		assert self._current._intersection_traffic is None
		self._current._intersection_traffic = IntersectionTraffic()
		self._sema.begin_intersection_traffic(self._current._intersection_traffic
											  , int(ctx.children[4].getText()), int(ctx.children[6].getText())
											  , int(ctx.children[8].getText()))

	def exitMeta_intersection_intersection(self, ctx: AVScenariosParser.Meta_intersection_intersectionContext):
		self._sema.end_intersection_traffic(self._current._intersection_traffic)
		self._current._intersection_id = None

	def enterIntersection_intersection(self, ctx: AVScenariosParser.Intersection_intersectionContext):
		pass

	def exitIntersection_intersection(self, ctx: AVScenariosParser.Intersection_intersectionContext):
		pass

	def enterIntersection_intersection_var(self, ctx: AVScenariosParser.Intersection_intersection_varContext):
		assert self._current._intersection_id is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._intersection_id = IntersectionID(0, name)
		else:
			n, index = ret
			if isinstance(n, IntersectionID):
				self._current._intersection_id = n
			if isinstance(n, NameWithRealValue):
				value = n.get_value()
				context = self._sema.find_context_for_error(n.get_name())
				if not value.is_integer():
					self._sema.add_error(
						IntersectionIDFormatError(context.children[2].getText(), context.children[2].start.line,
														  context.children[2].start.column
														  , context.children[2].start.stop - context.start.start,
														  context.children[2].stop.stop - context.start.start
														  , context.getText()))
					# construct an empty IntersectionID
					iid=IntersectionID(0,name)
				else:
					iid = self._sema.cast_to_intersection_id(n)
				self._sema.set(index, iid)
				self._current._intersection_id = iid
			else:
				self._current._intersection_id = IntersectionID(0,name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'IntersectionID'))

	def exitIntersection_intersection_var(self, ctx: AVScenariosParser.Intersection_intersection_varContext):
		pass

	def enterIntersection_signal(self, ctx: AVScenariosParser.Intersection_signalContext):
		assert self._current._intersection_id is None
		# We do not need to check the intersection id validity here,
		# see the BNF rule
		value=int(ctx.getText())
		self._current._intersection_id = IntersectionID(value)

	def exitIntersection_signal(self, ctx: AVScenariosParser.Intersection_signalContext):
		pass

	def enterLane_speed_limit(self, ctx: AVScenariosParser.Lane_speed_limitContext):
		pass

	def exitLane_speed_limit(self, ctx: AVScenariosParser.Lane_speed_limitContext):
		pass

	def enterLane_lane_speed_limit(self, ctx: AVScenariosParser.Lane_lane_speed_limitContext):
		pass

	def exitLane_lane_speed_limit(self, ctx: AVScenariosParser.Lane_lane_speed_limitContext):
		pass

	def enterSpeed_limit(self, ctx: AVScenariosParser.Speed_limitContext):
		pass

	def exitSpeed_limit(self, ctx: AVScenariosParser.Speed_limitContext):
		# add to the traffic.
		self._current._traffic.add_speed_limitation(self._current._speed_limit)
		self._current._speed_limit = None

	def enterSpeed_limit_var(self, ctx: AVScenariosParser.Speed_limit_varContext):
		assert self._current._speed_limit is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._speed_limit = SpeedLimitation(name)
		else:
			n, _ = ret
			if isinstance(n, SpeedLimitation):
				self._current._speed_limit = n
			else:
				self._current._speed_limit = SpeedLimitation(name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'SpeedLimitation'))
		self._current._traffic.add_speed_limitation(self._current._speed_limit)
		self._current._speed_limit = None

	def exitSpeed_limit_var(self, ctx: AVScenariosParser.Speed_limit_varContext):
		pass

	def enterSpeed_limit_speed_limit(self, ctx: AVScenariosParser.Speed_limit_speed_limitContext):
		assert self._current._speed_limit is None
		self._current._speed_limit = SpeedLimitation()
		self._sema.begin_speed_limitation(self._current._speed_limit)

	def exitSpeed_limit_speed_limit(self, ctx: AVScenariosParser.Speed_limit_speed_limitContext):
		self._sema.end_speed_limitation(self._current._speed_limit)
		self._current._speed_range = None
		self._current._lane = None

	def enterSpeed_range_speed(self, ctx: AVScenariosParser.Speed_range_speedContext):
		pass

	def exitSpeed_range_speed(self, ctx: AVScenariosParser.Speed_range_speedContext):
		pass

	def enterSpeed_range_var(self, ctx: AVScenariosParser.Speed_range_varContext):
		assert self._current._speed_range is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start,
														ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._speed_range = SpeedRange(name)
		else:
			n, index = ret
			if isinstance(n, SpeedRange):
				self._current._speed_range = n
			if isinstance(n, NameWithTwoRealValues):
				sr = self._sema.cast_to_speed_range(n)
				self._sema.set(index, sr)
				self._current._speed_range = sr
			else:
				self._current._speed_range =SpeedRange(name)
				self._sema.add_error(IllegalTypeError(n.get_name(), ctx.children[0].start.line, ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start,
													  ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__,
													  'SpeedRange'))

	def exitSpeed_range_var(self, ctx: AVScenariosParser.Speed_range_varContext):
		pass

	def enterSpeed_range_value(self, ctx: AVScenariosParser.Speed_range_valueContext):
		pass

	def exitSpeed_range_value(self, ctx: AVScenariosParser.Speed_range_valueContext):
		assert self._current._speed_range is None
		assert len(self._current._real_value_expression)>1
		self._current._speed_range = SpeedRange()
		self._current._speed_range.set_x(self._current._real_value_expression[-2])
		self._current._speed_range.set_y(self._current._real_value_expression[-1])
		self._current._real_value_expression.pop()
		self._current._real_value_expression.pop()

	def enterIdentifier(self, ctx: AVScenariosParser.IdentifierContext):
		pass

	def exitIdentifier(self, ctx: AVScenariosParser.IdentifierContext):
		pass





























	## The following methods are designed for assertion implementation
	## Add the scenario to class Trace
	def enterTrace_scenario(self, ctx: AVScenariosParser.Trace_scenarioContext):
		name = ctx.children[5].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[5].start.line
														, ctx.children[5].start.column
														, ctx.children[5].start.start - ctx.start.start
														, ctx.children[5].stop.stop - ctx.start.start
														, ctx.getText()))
			self._current._scenario = Scenario(name)
		else:
			n, _ = ret
			if isinstance(n, Scenario):
				self._current._scenario = n
			else:
				self._current._scenario=Scenario(name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[5].start.line
													  , ctx.children[5].start.column
													  , ctx.children[5].start.start - ctx.start.start
													  , ctx.children[5].stop.stop - ctx.start.start
													  , ctx.getText(), n.__class__.__name__
													  , 'Scenario'))
		if not self._sema.check_unique_id(ctx.children[1].getText()):
			self._sema.add_error(RedefinitionVariableError(ctx.children[1].getText(), ctx.children[1].start.line
														   , ctx.children[1].start.column
														   , ctx.children[1].start.start - ctx.start.start
														   , ctx.children[1].stop.stop - ctx.start.start
														   , ctx.getText()))
		else:
			trace = Trace(ctx.children[1].getText(), self._current._scenario)
			self._sema.finish_trace(trace)

	def exitTrace_scenario(self, ctx: AVScenariosParser.Trace_scenarioContext):
		pass


	#Find the id of the current trace and add the node to the class:current
	def enterTrace_id(self, ctx: AVScenariosParser.Trace_idContext):
		pass

	def exitTrace_id(self, ctx:AVScenariosParser.Trace_idContext):
		#pass
		assert self._current._trace is None
		context=ctx.parentCtx
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, context.children[0].start.line
														, context.children[0].start.column
														, context.children[0].start.stop - context.start.start
														, context.children[0].stop.stop - context.start.start
														, context.getText()))
			self._current._trace = Trace(name,Scenario("Error Type"))
		else:
			n, _ = ret
			if isinstance(n, Trace):
				self._current._trace = n
			else:
				self._current._trace = Trace(name,Scenario("Error Type"))
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line
													  , ctx.children[0].start.column
													  , ctx.children[0].start.stop - ctx.start.start
													  , ctx.children[0].stop.stop - ctx.start.start
													  , ctx.getText(), n.__class__.__name__
													  , 'Trace'))






	def enterEgo_state_for_general(self, ctx:AVScenariosParser.Ego_state_for_generalContext):
		pass

	# If it's the direct ego_state mode, 
	#Assign the current ego state in current.trace to current._ego_state 
	def exitEgo_state_for_general(self, ctx:AVScenariosParser.Ego_state_for_generalContext):
		assert self._current._trace is not None
		# assert self._current._ego_state is None
		if self._current._ego_state is None:
			self._current._ego_state = EgoState(self._current._trace)
		else:
			assert self._current._temp_for_statement is None
			self._current._temp_for_statement = EgoState(self._current._trace)
		self._current._trace = None
		#pass


	# If the ego_state is a variable,
	# Find the id of the current.ego.state and assign it to the current class
	def enterEgo_state_id(self, ctx: AVScenariosParser.Ego_state_idContext):
		assert self._current._ego_state is None
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line
														, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start
														, ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._ego_state = EgoState(Trace("Error Type",Scenario("Error Type")),name)
		else:
			n, _ = ret
			if isinstance(n, EgoState):
				self._current._ego_state = n
			# elif isinstance(n, AgentGroundTruth):
			#   self._current._agent_ground_truth = n
			# elif isinstance(n , AgentState):
			#   self._current._agent_state = n
			else:
				self._current._ego_state = EgoState(Trace("Error Type",Scenario("Error Type")),name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line
													  , ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start
													  , ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__
													  , 'EgoState'))

	def exitEgo_state_id(self, ctx: AVScenariosParser.Ego_state_idContext):
		pass


	def enterAssign_ego_state(self, ctx: AVScenariosParser.Assign_ego_stateContext):
		pass

	def exitAssign_ego_state(self, ctx: AVScenariosParser.Assign_ego_stateContext):
		#pass
		assert self._current._ego_state is not None
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line
														   , ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start
														   , ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_ego_state(name)
		self._current._ego_state = None


	def enterAgent_state_for_general(self, ctx: AVScenariosParser.Agent_state_for_generalContext):
		pass

	def exitAgent_state_for_general(self, ctx: AVScenariosParser.Agent_state_for_generalContext):
		assert self._current._trace is not None 
		name = ctx.children[5].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[5].start.line
														, ctx.children[5].start.column
														, ctx.children[5].start.start - ctx.start.start
														, ctx.children[5].stop.stop - ctx.start.start
														, ctx.getText()))
		else:
			n, _ = ret
			if isinstance(n, NPCVehicle) or isinstance(n, Pedestrian) or isinstance(n, Obstacle):
				if self._current._agent_state is None:
					self._current._agent_state = AgentState(self._current._trace)
					self._current._agent_state.set_agent(n)
				else:
					assert self._current._temp_for_statement is None
					self._current._temp_for_statement = AgentState(self._current._trace)
					self._current._temp_for_statement.set_agent(n)
			else:
				self._current._agent_state.set_agent(Obstacle(name))
				self._sema.add_error(IllegalTypeError(name, ctx.children[5].start.line
													  , ctx.children[5].start.column
													  , ctx.children[5].start.start - ctx.start.start
													  , ctx.children[5].stop.stop - ctx.start.start
													  , ctx.getText(), n.__class__.__name__
													  , 'NPCVehicle', 'Obstacle', 'Pedestrian'))
		self._current._trace = None


	def enterAgent_state_id(self, ctx: AVScenariosParser.Agent_state_idContext):
		# print('EnterAgent_state_id:  '+ctx.getText())
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line
														, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start
														, ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._agent_state = AgentState(Trace("Error Type", Scenario("Error Type")), name)
		else:
			n, _ = ret
			if isinstance(n, AgentState):
				assert self._current._agent_state is None
				self._current._agent_state = n
			elif isinstance(n, AgentGroundTruth):
				assert self._current._agent_ground_truth is None
				self._current._agent_ground_truth = n
			elif isinstance(n , EgoState):
				assert self._current._ego_state is None
				self._current._ego_state = n
			else:
				self._current._agent_state = AgentState(Trace("Error Type",Scenario("Error Type")),name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line
													  , ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start
													  , ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__
													  , 'AgentState'))

	def exitAgent_state_id(self, ctx: AVScenariosParser.Agent_state_idContext):
		pass


	def enterAssign_agent_state(self, ctx: AVScenariosParser.Assign_agent_stateContext):
		pass

	def exitAssign_agent_state(self, ctx: AVScenariosParser.Assign_agent_stateContext):
		#pass
		assert self._current._agent_state is not None
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line
														   , ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start
														   , ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_agent_state(name)
		self._current._agent_state = None


	# Enter a parse tree produced by AVScenariosParser#agent_ground_truth_for_general.
	def enterAgent_ground_truth_for_general(self, ctx:AVScenariosParser.Agent_ground_truth_for_generalContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#agent_ground_truth_for_general.
	def exitAgent_ground_truth_for_general(self, ctx:AVScenariosParser.Agent_ground_truth_for_generalContext):
		# assert self._current._agent_ground_truth is None
		assert self._current._trace is not None 
		name = ctx.children[5].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[5].start.line
														, ctx.children[5].start.column
														, ctx.children[5].start.start - ctx.start.start
														, ctx.children[5].stop.stop - ctx.start.start
														, ctx.getText()))
		else:
			n, _ = ret
			if isinstance(n, NPCVehicle) or isinstance(n, Pedestrian) or isinstance(n, Obstacle):
				if self._current._agent_ground_truth is None:
					self._current._agent_ground_truth = AgentGroundTruth(self._current._trace)
					self._current._agent_ground_truth.set_agent(n)
				else:
					assert self._current._temp_for_statement is None
					self._current._temp_for_statement = AgentGroundTruth(self._current._trace)
					self._current._temp_for_statement.set_agent(n)
			else:
				self._current._agent_ground_truth.set_agent(Obstacle(name))
				self._sema.add_error(IllegalTypeError(name, ctx.children[5].start.line
													  , ctx.children[5].start.column
													  , ctx.children[5].start.start - ctx.start.start
													  , ctx.children[5].stop.stop - ctx.start.start
													  , ctx.getText(), n.__class__.__name__
													  , 'NPCVehicle', 'Obstacle', 'Pedestrian'))
		self._current._trace = None


	def enterAgent_ground_truth_id(self, ctx: AVScenariosParser.Agent_ground_truth_idContext):
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line
														, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start
														, ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			self._current._agent_ground_truth = AgentGroundTruth(
				Trace("Error Type", Scenario("Error Type")), name)
		else:
			n, _ = ret
			if isinstance(n, AgentGroundTruth):
				if self._current._agent_ground_truth is None:
					self._current._agent_ground_truth = n
				elif isinstance(n, AgentState):
					assert self._current._agent_state is None
					self._current._agent_state = n
			elif isinstance(n , EgoState):
				assert self._current._ego_state is None
				self._current._ego_state = n
			elif ininstance(n , AgentState):
				assert self._current._agent_state is None
				self._current._agent_state = n
			else:
				self._current._agent_ground_truth = AgentGroundTruth(Trace("Error Type",Scenario("Error Type")),name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line
													  , ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start
													  , ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__
													  , 'AgentGroundTruth'))


	def exitAgent_ground_truth_id(self, ctx: AVScenariosParser.Agent_ground_truth_idContext):
		pass

	# Enter a parse tree produced by AVScenariosParser#assign_agent_ground.
	def enterAssign_agent_ground(self, ctx:AVScenariosParser.Assign_agent_groundContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#assign_agent_ground.
	def exitAssign_agent_ground(self, ctx:AVScenariosParser.Assign_agent_groundContext):
		#pass
		assert self._current._agent_ground_truth is not None
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line
														   , ctx.children[0].start.column
														   , ctx.children[0].start.stop- ctx.start.start
														   , ctx.children[0].stop.stop- ctx.start.start
														   , ctx.getText()))
		else:
			self._sema.act_on_agent_ground_truth(name)
		self._current._agent_ground_truth = None

			# self._distance_statement = None
			# self._perception_difference_statement = None
			# self._velocity_statement = None
			# self._speed_statement = None
			# self._acceleration_statement = None




#Driver Oriented Way
#################################################################################################

#Boolean Ones
	# Enter a parse tree produced by AVScenariosParser#traffic_rule_highBeamOn.
	def enterTraffic_rule_highBeamOn(self, ctx:AVScenariosParser.Traffic_rule_highBeamOnContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_highBeamOn.
	def exitTraffic_rule_highBeamOn(self, ctx:AVScenariosParser.Traffic_rule_highBeamOnContext):
		assert self._current._traffic_rule_boolean_API is None
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('highBeamOn')
		self._current._traffic_rule_boolean_API = temp


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_lowBeamOn.
	def enterTraffic_rule_lowBeamOn(self, ctx:AVScenariosParser.Traffic_rule_lowBeamOnContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_lowBeamOn.
	def exitTraffic_rule_lowBeamOn(self, ctx:AVScenariosParser.Traffic_rule_lowBeamOnContext):
		assert self._current._traffic_rule_boolean_API is None
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('lowBeamOn')
		self._current._traffic_rule_boolean_API = temp


	def enterTraffic_rule_fogLightOn(self, ctx:AVScenariosParser.Traffic_rule_fogLightOnContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_fogLightOn.
	def exitTraffic_rule_fogLightOn(self, ctx:AVScenariosParser.Traffic_rule_fogLightOnContext):
		assert self._current._traffic_rule_boolean_API is None
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('fogLightOn')
		self._current._traffic_rule_boolean_API = temp


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_hornOn.
	def enterTraffic_rule_hornOn(self, ctx:AVScenariosParser.Traffic_rule_hornOnContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_hornOn.
	def exitTraffic_rule_hornOn(self, ctx:AVScenariosParser.Traffic_rule_hornOnContext):
		assert self._current._traffic_rule_boolean_API is None
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('hornOn')
		self._current._traffic_rule_boolean_API = temp

	# Enter a parse tree produced by AVScenariosParser#traffic_rule_warningFlashOn.
	def enterTraffic_rule_warningFlashOn(self, ctx:AVScenariosParser.Traffic_rule_warningFlashOnContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_warningFlashOn.
	def exitTraffic_rule_warningFlashOn(self, ctx:AVScenariosParser.Traffic_rule_warningFlashOnContext):
		assert self._current._traffic_rule_boolean_API is None
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('warningflashOn')
		self._current._traffic_rule_boolean_API = temp


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_engineOn.
	def enterTraffic_rule_engineOn(self, ctx:AVScenariosParser.Traffic_rule_engineOnContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_engineOn.
	def exitTraffic_rule_engineOn(self, ctx:AVScenariosParser.Traffic_rule_engineOnContext):
		assert self._current._traffic_rule_boolean_API is None
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('engineOn')
		self._current._traffic_rule_boolean_API = temp


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_isLaneChanging.
	def enterTraffic_rule_isLaneChanging(self, ctx:AVScenariosParser.Traffic_rule_isLaneChangingContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_isLaneChanging.
	def exitTraffic_rule_isLaneChanging(self, ctx:AVScenariosParser.Traffic_rule_isLaneChangingContext):
		assert self._current._traffic_rule_boolean_API is None
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('isLaneChanging')
		self._current._traffic_rule_boolean_API = temp


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_isOverTaking.
	def enterTraffic_rule_isOverTaking(self, ctx:AVScenariosParser.Traffic_rule_isOverTakingContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_isOverTaking.
	def exitTraffic_rule_isOverTaking(self, ctx:AVScenariosParser.Traffic_rule_isOverTakingContext):
		assert self._current._traffic_rule_boolean_API is None
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('isOverTaking')
		self._current._traffic_rule_boolean_API = temp


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_isTurningAround.
	def enterTraffic_rule_isTurningAround(self, ctx:AVScenariosParser.Traffic_rule_isTurningAroundContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_isTurningAround.
	def exitTraffic_rule_isTurningAround(self, ctx:AVScenariosParser.Traffic_rule_isTurningAroundContext):
		assert self._current._traffic_rule_boolean_API is None
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('isTurningAround')
		self._current._traffic_rule_boolean_API = temp




	# Enter a parse tree produced by AVScenariosParser#traffic_rule_manualIntervention.
	def enterTraffic_rule_manualIntervention(self, ctx:AVScenariosParser.Traffic_rule_manualInterventionContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_manualIntervention.
	def exitTraffic_rule_manualIntervention(self, ctx:AVScenariosParser.Traffic_rule_manualInterventionContext):
		assert self._current._traffic_rule_boolean_API is None
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('manualIntervention')
		self._current._traffic_rule_boolean_API = temp



	# Enter a parse tree produced by AVScenariosParser#traffic_rule_honkingAllowed.
	def enterTraffic_rule_honkingAllowed(self, ctx:AVScenariosParser.Traffic_rule_honkingAllowedContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_honkingAllowed.
	def exitTraffic_rule_honkingAllowed(self, ctx:AVScenariosParser.Traffic_rule_honkingAllowedContext):
		assert self._current._traffic_rule_boolean_API is None
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('honkingAllowed')
		self._current._traffic_rule_boolean_API = temp


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_crosswalkAhead.
	def enterTraffic_rule_crosswalkAhead(self, ctx:AVScenariosParser.Traffic_rule_crosswalkAheadContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_crosswalkAhead.
	def exitTraffic_rule_crosswalkAhead(self, ctx:AVScenariosParser.Traffic_rule_crosswalkAheadContext):
		assert self._current._traffic_rule_boolean_API is None
		assert len(self._current._real_value_expression) == 1
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('crosswalkAhead')
		temp.set_API_value(str(self._current._real_value_expression[-1]))
		self._current._real_value_expression.pop()
		temp.set_API_operator('<=')	
		self._current._traffic_rule_boolean_API = temp


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_junctionAhead.
	def enterTraffic_rule_junctionAhead(self, ctx:AVScenariosParser.Traffic_rule_junctionAheadContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_junctionAhead.
	def exitTraffic_rule_junctionAhead(self, ctx:AVScenariosParser.Traffic_rule_junctionAheadContext):
		assert self._current._traffic_rule_boolean_API is None
		assert len(self._current._real_value_expression) == 1
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('junctionAhead')
		temp.set_API_value(str(self._current._real_value_expression[-1]))
		self._current._real_value_expression.pop()
		temp.set_API_operator('<=')	
		self._current._traffic_rule_boolean_API = temp


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_stopSignAhead.
	def enterTraffic_rule_stopSignAhead(self, ctx:AVScenariosParser.Traffic_rule_stopSignAheadContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_stopSignAhead.
	def exitTraffic_rule_stopSignAhead(self, ctx:AVScenariosParser.Traffic_rule_stopSignAheadContext):
		assert self._current._traffic_rule_boolean_API is None
		assert len(self._current._real_value_expression) == 1
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('stopSignAhead')
		temp.set_API_value(str(self._current._real_value_expression[-1]))
		self._current._real_value_expression.pop()
		temp.set_API_operator('<=')	
		self._current._traffic_rule_boolean_API = temp


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_stoplineAhead.
	def enterTraffic_rule_stoplineAhead(self, ctx:AVScenariosParser.Traffic_rule_stoplineAheadContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_stoplineAhead.
	def exitTraffic_rule_stoplineAhead(self, ctx:AVScenariosParser.Traffic_rule_stoplineAheadContext):
		assert self._current._traffic_rule_boolean_API is None
		assert len(self._current._real_value_expression) == 1
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('stoplineAhead')
		temp.set_API_value(str(self._current._real_value_expression[-1]))
		self._current._real_value_expression.pop()
		temp.set_API_operator('<=')	
		self._current._traffic_rule_boolean_API = temp

	# Enter a parse tree produced by AVScenariosParser#traffic_rule_streetLightOn.
	def enterTraffic_rule_streetLightOn(self, ctx:AVScenariosParser.Traffic_rule_streetLightOnContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_streetLightOn.
	def exitTraffic_rule_streetLightOn(self, ctx:AVScenariosParser.Traffic_rule_streetLightOnContext):
		assert self._current._traffic_rule_boolean_API is None
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('streetLightOn')
		self._current._traffic_rule_boolean_API = temp


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_specialLocationAhead.
	def enterTraffic_rule_specialLocationAhead(self, ctx:AVScenariosParser.Traffic_rule_specialLocationAheadContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_specialLocationAhead.
	def exitTraffic_rule_specialLocationAhead(self, ctx:AVScenariosParser.Traffic_rule_specialLocationAheadContext):
		assert self._current._traffic_rule_boolean_API is None
		assert len(self._current._real_value_expression) == 1
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('specialLocationAheadlocation')
		temp.set_API_value(str(self._current._real_value_expression[-1]))
		self._current._real_value_expression.pop()
		temp.set_API_operator('<=')	
		self._current._traffic_rule_boolean_API = temp

	# Enter a parse tree produced by AVScenariosParser#traffic_rule_trafficLightAhead_blink.
	def enterTraffic_rule_trafficLightAhead_blink(self, ctx:AVScenariosParser.Traffic_rule_trafficLightAhead_blinkContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_trafficLightAhead_blink.
	def exitTraffic_rule_trafficLightAhead_blink(self, ctx:AVScenariosParser.Traffic_rule_trafficLightAhead_blinkContext):
		assert self._current._traffic_rule_boolean_API is None
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('trafficLightAheadblink')
		self._current._traffic_rule_boolean_API = temp

	# Enter a parse tree produced by AVScenariosParser#traffic_rule_PriorityNPCAhead.
	def enterTraffic_rule_PriorityNPCAhead(self, ctx:AVScenariosParser.Traffic_rule_PriorityNPCAheadContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_PriorityNPCAhead.
	def exitTraffic_rule_PriorityNPCAhead(self, ctx:AVScenariosParser.Traffic_rule_PriorityNPCAheadContext):
		assert self._current._traffic_rule_boolean_API is None
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('PriorityNPCAhead')
		self._current._traffic_rule_boolean_API = temp


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_PriorityPedsAhead.
	def enterTraffic_rule_PriorityPedsAhead(self, ctx:AVScenariosParser.Traffic_rule_PriorityPedsAheadContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_PriorityPedsAhead.
	def exitTraffic_rule_PriorityPedsAhead(self, ctx:AVScenariosParser.Traffic_rule_PriorityPedsAheadContext):
		assert self._current._traffic_rule_boolean_API is None
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('PriorityPedsAhead')
		self._current._traffic_rule_boolean_API = temp


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_isTrafficJam.
	def enterTraffic_rule_isTrafficJam(self, ctx:AVScenariosParser.Traffic_rule_isTrafficJamContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_isTrafficJam.
	def exitTraffic_rule_isTrafficJam(self, ctx:AVScenariosParser.Traffic_rule_isTrafficJamContext):
		assert self._current._traffic_rule_boolean_API is None
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('isTrafficJam')
		self._current._traffic_rule_boolean_API = temp

	# Enter a parse tree produced by AVScenariosParser#traffic_rule_NPCAhead.
	def enterTraffic_rule_NPCAhead(self, ctx:AVScenariosParser.Traffic_rule_NPCAheadContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_NPCAhead.
	def exitTraffic_rule_NPCAhead(self, ctx:AVScenariosParser.Traffic_rule_NPCAheadContext):
		assert self._current._traffic_rule_boolean_API is None
		assert len(self._current._real_value_expression) == 1
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('NPCAheadAhead')
		temp.set_API_value(str(self._current._real_value_expression[-1]))
		self._current._real_value_expression.pop()
		temp.set_API_operator('<=')	
		self._current._traffic_rule_boolean_API = temp



	# Enter a parse tree produced by AVScenariosParser#traffic_rule_NearestNPC.
	def enterTraffic_rule_NearestNPC(self, ctx:AVScenariosParser.Traffic_rule_NearestNPCContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_NearestNPC.
	def exitTraffic_rule_NearestNPC(self, ctx:AVScenariosParser.Traffic_rule_NearestNPCContext):
		assert self._current._traffic_rule_boolean_API is None
		assert len(self._current._real_value_expression) == 1
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('NearestNPCAhead')
		temp.set_API_value(str(self._current._real_value_expression[-1]))
		self._current._real_value_expression.pop()
		temp.set_API_operator('<=')	
		self._current._traffic_rule_boolean_API = temp


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_NPCOpposite.
	def enterTraffic_rule_NPCOpposite(self, ctx:AVScenariosParser.Traffic_rule_NPCOppositeContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_NPCOpposite.
	def exitTraffic_rule_NPCOpposite(self, ctx:AVScenariosParser.Traffic_rule_NPCOppositeContext):
		assert self._current._traffic_rule_boolean_API is None
		assert len(self._current._real_value_expression) == 1
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('NPCOppositeAhead')
		temp.set_API_value(str(self._current._real_value_expression[-1]))
		self._current._real_value_expression.pop()
		temp.set_API_operator('<=')	
		self._current._traffic_rule_boolean_API = temp



	# Enter a parse tree produced by AVScenariosParser#traffic_rule_trafficLightAhead_arrow_blink.
	def enterTraffic_rule_trafficLightAhead_arrow_blink(self, ctx:AVScenariosParser.Traffic_rule_trafficLightAhead_arrow_blinkContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_trafficLightAhead_arrow_blink.
	def exitTraffic_rule_trafficLightAhead_arrow_blink(self, ctx:AVScenariosParser.Traffic_rule_trafficLightAhead_arrow_blinkContext):
		assert self._current._traffic_rule_boolean_API is None
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('trafficLightAheadArrowDirectionblink')
		self._current._traffic_rule_boolean_API = temp

	# Enter a parse tree produced by AVScenariosParser#traffic_rule_Time.
	def enterTraffic_rule_Time(self, ctx:AVScenariosParser.Traffic_rule_TimeContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_Time.
	def exitTraffic_rule_Time(self, ctx:AVScenariosParser.Traffic_rule_TimeContext):
		operator = ctx.children[1].getText()
		assert self._current._traffic_rule_boolean_API is None
		assert self._current._time is not None
		temp = Traffic_Rule_Related_APIs()
		temp.set_API('Time')
		time_value = self._current._time.get_hour() + self._current._time.get_minute()/60
		temp.set_API_value(str(time_value))
		temp.set_API_operator(operator)	
		self._current._traffic_rule_boolean_API = temp
		self._current._time = None


#normal ones
	# Enter a parse tree produced by AVScenariosParser#traffic_rule_turnSignal.
	def enterTraffic_rule_turnSignal(self, ctx:AVScenariosParser.Traffic_rule_turnSignalContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_turnSignal.
	def exitTraffic_rule_turnSignal(self, ctx:AVScenariosParser.Traffic_rule_turnSignalContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('turnSignal')
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('turnSignal')
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('turnSignal')
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('turnSignal')
			self._current._general_atom_statements_list.append(temp)



	# Enter a parse tree produced by AVScenariosParser#traffic_rule_signalAhead.
	def enterTraffic_rule_signalAhead(self, ctx:AVScenariosParser.Traffic_rule_signalAheadContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_signalAhead.
	def exitTraffic_rule_signalAhead(self, ctx:AVScenariosParser.Traffic_rule_signalAheadContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('signalAhead')
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('signalAhead')
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('signalAhead')
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('turnSignal')
			self._current._general_atom_statements_list.append(temp)


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_gear.
	def enterTraffic_rule_gear(self, ctx:AVScenariosParser.Traffic_rule_gearContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_gear.
	def exitTraffic_rule_gear(self, ctx:AVScenariosParser.Traffic_rule_gearContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('gear')
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('gear')
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('gear')
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('gear')
			self._current._general_atom_statements_list.append(temp)


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_direction.
	def enterTraffic_rule_direction(self, ctx:AVScenariosParser.Traffic_rule_directionContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_direction.
	def exitTraffic_rule_direction(self, ctx:AVScenariosParser.Traffic_rule_directionContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('direction')
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('direction')
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('direction')
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('direction')
			self._current._general_atom_statements_list.append(temp)



	def enterTraffic_rule_speed(self, ctx:AVScenariosParser.Traffic_rule_speedContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_speed.
	def exitTraffic_rule_speed(self, ctx:AVScenariosParser.Traffic_rule_speedContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('speed')
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('speed')
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('speed')
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('speed')
			self._current._general_atom_statements_list.append(temp)


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_acc.
	def enterTraffic_rule_acc(self, ctx:AVScenariosParser.Traffic_rule_accContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_acc.
	def exitTraffic_rule_acc(self, ctx:AVScenariosParser.Traffic_rule_accContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('acc')
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('acc')
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('acc')
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('acc')
			self._current._general_atom_statements_list.append(temp)


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_brake.
	def enterTraffic_rule_brake(self, ctx:AVScenariosParser.Traffic_rule_brakeContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_brake.
	def exitTraffic_rule_brake(self, ctx:AVScenariosParser.Traffic_rule_brakeContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('brake')
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('brake')
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('brake')
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('brake')
			self._current._general_atom_statements_list.append(temp)

	# Enter a parse tree produced by AVScenariosParser#traffic_rule_currentlane_number.
	def enterTraffic_rule_currentlane_number(self, ctx:AVScenariosParser.Traffic_rule_currentlane_numberContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_currentlane_number.
	def exitTraffic_rule_currentlane_number(self, ctx:AVScenariosParser.Traffic_rule_currentlane_numberContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('currentLanenumber')
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('currentLanenumber')
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('currentLanenumber')
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('currentLanenumber')
			self._current._general_atom_statements_list.append(temp)


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_currentlane_direction.
	def enterTraffic_rule_currentlane_direction(self, ctx:AVScenariosParser.Traffic_rule_currentlane_directionContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_currentlane_direction.
	def exitTraffic_rule_currentlane_direction(self, ctx:AVScenariosParser.Traffic_rule_currentlane_directionContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('currentLanedirection')
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('currentLanedirection')
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('currentLanedirection')
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('currentLanedirection')
			self._current._general_atom_statements_list.append(temp)

	# Enter a parse tree produced by AVScenariosParser#traffic_rule_speedLimit_upperLimit.
	def enterTraffic_rule_speedLimit_upperLimit(self, ctx:AVScenariosParser.Traffic_rule_speedLimit_upperLimitContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_speedLimit_upperLimit.
	def exitTraffic_rule_speedLimit_upperLimit(self, ctx:AVScenariosParser.Traffic_rule_speedLimit_upperLimitContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('speedLimitupperLimit')
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('speedLimitupperLimit')
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('speedLimitupperLimit')
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('speedLimitupperLimit')
			self._current._general_atom_statements_list.append(temp)

	# Enter a parse tree produced by AVScenariosParser#traffic_rule_speedLimit_lowerLimit.
	def enterTraffic_rule_speedLimit_lowerLimit(self, ctx:AVScenariosParser.Traffic_rule_speedLimit_lowerLimitContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_speedLimit_lowerLimit.
	def exitTraffic_rule_speedLimit_lowerLimit(self, ctx:AVScenariosParser.Traffic_rule_speedLimit_lowerLimitContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('speedLimitlowerLimit')
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('speedLimitlowerLimit')
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('speedLimitlowerLimit')
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('speedLimitlowerLimit')
			self._current._general_atom_statements_list.append(temp)

	# Enter a parse tree produced by AVScenariosParser#traffic_rule_speedLimit_specialLocationAhead_type.
	def enterTraffic_rule_speedLimit_specialLocationAhead_type(self, ctx:AVScenariosParser.Traffic_rule_speedLimit_specialLocationAhead_typeContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_speedLimit_specialLocationAhead_type.
	def exitTraffic_rule_speedLimit_specialLocationAhead_type(self, ctx:AVScenariosParser.Traffic_rule_speedLimit_specialLocationAhead_typeContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('specialLocationAheadtype')
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('specialLocationAheadtype')
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('specialLocationAheadtype')
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('specialLocationAheadtype')
			self._current._general_atom_statements_list.append(temp)

	# Enter a parse tree produced by AVScenariosParser#traffic_rule_trafficLightAhead_color.
	def enterTraffic_rule_trafficLightAhead_color(self, ctx:AVScenariosParser.Traffic_rule_trafficLightAhead_colorContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_trafficLightAhead_color.
	def exitTraffic_rule_trafficLightAhead_color(self, ctx:AVScenariosParser.Traffic_rule_trafficLightAhead_colorContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('trafficLightAheadcolor')
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('trafficLightAheadcolor')
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('trafficLightAheadcolor')
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('trafficLightAheadcolor')
			self._current._general_atom_statements_list.append(temp)


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_NPCAhead_speed.
	def enterTraffic_rule_NPCAhead_speed(self, ctx:AVScenariosParser.Traffic_rule_NPCAhead_speedContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_NPCAhead_speed.
	def exitTraffic_rule_NPCAhead_speed(self, ctx:AVScenariosParser.Traffic_rule_NPCAhead_speedContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('NPCAheadspeed')
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('NPCAheadspeed')
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('NPCAheadspeed')
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('NPCAheadspeed')
			self._current._general_atom_statements_list.append(temp)


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_NearestNPC_speed.
	def enterTraffic_rule_NearestNPC_speed(self, ctx:AVScenariosParser.Traffic_rule_NearestNPC_speedContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_NearestNPC_speed.
	def exitTraffic_rule_NearestNPC_speed(self, ctx:AVScenariosParser.Traffic_rule_NearestNPC_speedContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('NearestNPCspeed')
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('NearestNPCspeed')
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('NearestNPCspeed')
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('NearestNPCspeed')
			self._current._general_atom_statements_list.append(temp)


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_NPCOpposite_speed.
	def enterTraffic_rule_NPCOpposite_speed(self, ctx:AVScenariosParser.Traffic_rule_NPCOpposite_speedContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_NPCOpposite_speed.
	def exitTraffic_rule_NPCOpposite_speed(self, ctx:AVScenariosParser.Traffic_rule_NPCOpposite_speedContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('NPCOppositespeed')
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('NPCOppositespeed')
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('NPCOppositespeed')
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('NPCOppositespeed')
			self._current._general_atom_statements_list.append(temp)

	# Enter a parse tree produced by AVScenariosParser#traffic_rule_trafficLightAhead_arrow_color.
	def enterTraffic_rule_trafficLightAhead_arrow_color(self, ctx:AVScenariosParser.Traffic_rule_trafficLightAhead_arrow_colorContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_trafficLightAhead_arrow_color.
	def exitTraffic_rule_trafficLightAhead_arrow_color(self, ctx:AVScenariosParser.Traffic_rule_trafficLightAhead_arrow_colorContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('trafficLightAheadArrowDirectioncolor')
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('trafficLightAheadArrowDirectioncolor')
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('trafficLightAheadArrowDirectioncolor')
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('trafficLightAheadArrowDirectioncolor')
			self._current._general_atom_statements_list.append(temp)


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_green.
	def enterTraffic_rule_green(self, ctx:AVScenariosParser.Traffic_rule_greenContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_green.
	def exitTraffic_rule_green(self, ctx:AVScenariosParser.Traffic_rule_greenContext):
		# print(self._current._general_atom_statements_list)
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = '3'
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = '3'
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = '3'
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = '3'
			self._current._general_atom_statements_list.append(temp)


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_red.
	def enterTraffic_rule_red(self, ctx:AVScenariosParser.Traffic_rule_redContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_red.
	def exitTraffic_rule_red(self, ctx:AVScenariosParser.Traffic_rule_redContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = '1'
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = '1'
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = '1'
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = '1'
			self._current._general_atom_statements_list.append(temp)


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_yellow.
	def enterTraffic_rule_yellow(self, ctx:AVScenariosParser.Traffic_rule_yellowContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_yellow.
	def exitTraffic_rule_yellow(self, ctx:AVScenariosParser.Traffic_rule_yellowContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = '2'
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = '2'
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = '2'
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = '2'
			self._current._general_atom_statements_list.append(temp)






	# Enter a parse tree produced by AVScenariosParser#traffic_rule_off.
	def enterTraffic_rule_off(self, ctx:AVScenariosParser.Traffic_rule_offContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_off.
	def exitTraffic_rule_off(self, ctx:AVScenariosParser.Traffic_rule_offContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = '0'
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = '0'
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = '0'
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = '0'
			self._current._general_atom_statements_list.append(temp)


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_forward.
	def enterTraffic_rule_forward(self, ctx:AVScenariosParser.Traffic_rule_forwardContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_forward.
	def exitTraffic_rule_forward(self, ctx:AVScenariosParser.Traffic_rule_forwardContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = '0'
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = '0'
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = '0'
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = '0'
			self._current._general_atom_statements_list.append(temp)


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_left.
	def enterTraffic_rule_left(self, ctx:AVScenariosParser.Traffic_rule_leftContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_left.
	def exitTraffic_rule_left(self, ctx:AVScenariosParser.Traffic_rule_leftContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = '1'
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = '1'
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = '1'
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = '1'
			self._current._general_atom_statements_list.append(temp)

	# Enter a parse tree produced by AVScenariosParser#traffic_rule_right.
	def enterTraffic_rule_right(self, ctx:AVScenariosParser.Traffic_rule_rightContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_right.
	def exitTraffic_rule_right(self, ctx:AVScenariosParser.Traffic_rule_rightContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = '2'
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = '2'
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = '2'
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = '2'
			self._current._general_atom_statements_list.append(temp)





	# Enter a parse tree produced by AVScenariosParser#traffic_rule_fog.
	def enterTraffic_rule_fog(self, ctx:AVScenariosParser.Traffic_rule_fogContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_fog.
	def exitTraffic_rule_fog(self, ctx:AVScenariosParser.Traffic_rule_fogContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('fog')
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('fog')
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('fog')
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('fog')
			self._current._general_atom_statements_list.append(temp)



	# Enter a parse tree produced by AVScenariosParser#traffic_rule_rain.
	def enterTraffic_rule_rain(self, ctx:AVScenariosParser.Traffic_rule_rainContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_rain.
	def exitTraffic_rule_rain(self, ctx:AVScenariosParser.Traffic_rule_rainContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('rain')
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('rain')
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('rain')
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('rain')
			self._current._general_atom_statements_list.append(temp)

	# Enter a parse tree produced by AVScenariosParser#traffic_rule_snow.
	def enterTraffic_rule_snow(self, ctx:AVScenariosParser.Traffic_rule_snowContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_snow.
	def exitTraffic_rule_snow(self, ctx:AVScenariosParser.Traffic_rule_snowContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('snow')
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('snow')
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('snow')
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('snow')
			self._current._general_atom_statements_list.append(temp)


	# Enter a parse tree produced by AVScenariosParser#traffic_rule_visibility.
	def enterTraffic_rule_visibility(self, ctx:AVScenariosParser.Traffic_rule_visibilityContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_visibility.
	def exitTraffic_rule_visibility(self, ctx:AVScenariosParser.Traffic_rule_visibilityContext):
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('visibility')
			self._current._general_atom_statements_list.append(temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('visibility')
				self._current._atom_statement_right = temp
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				temp = Traffic_Rule_Related_APIs()
				temp.set_API('visibility')
				self._current._atom_statement_left = temp
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			temp = Traffic_Rule_Related_APIs()
			temp.set_API('visibility')
			self._current._general_atom_statements_list.append(temp)







#God View Way
#################################################################################################
	# Enter a parse tree produced by AVScenariosParser#position_element_id.
	def enterPosition_element_id(self, ctx:AVScenariosParser.Position_element_idContext):
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line
														, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start
														, ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			# self._current._agent_ground_truth = AgentGroundTruth(
			#   Trace("Error Type", Scenario("Error Type")), name)
		else:
			n, _ = ret
			if isinstance(n, AgentGroundTruth):
				if self._current._agent_ground_truth is None:
					self._current._agent_ground_truth = n
				else:
					assert self._current._temp_for_statement is None
					self._current._temp_for_statement = n
				#print( ' This is the Position_element_id:  '+   ctx.getText() + '       agent_ground_truth')
			elif isinstance(n , EgoState):
				if self._current._ego_state is None:
					self._current._ego_state = n
				else:
					assert self._current._temp_for_statement is None
					self._current._temp_for_statement = n
				#print( ' This is the Position_element_id:  '+   ctx.getText() + '       ego_state')
			elif isinstance(n , AgentState):
				if self._current._agent_state is None:
					self._current._agent_state = n
				else:
					assert self._current._temp_for_statement is None
					self._current._temp_for_statement = n
				#print( ' This is the Position_element_id:  '+   ctx.getText() + '       agent_state')
			elif isinstance(n , Position):
				if self._current._position is None:
					self._current._position = n
				else:
					assert self._current._temp_for_statement is None
					self._current._temp_for_statement = n

			elif isinstance(n , Coordinate):
				if self._current._position is None:
					# print('a')
					p = Position(n.get_name())
					p.set_coordinate(n)
					self._current._position = p
				else:
					# print('b')
					assert self._current._temp_for_statement is None
					p = Position(n.get_name())
					p.set_coordinate(n)
					self._current._temp_for_statement = p
				# print( ' This is the Position_element_id:  '+   name + '       position')

			elif isinstance(n, NameWithTwoRealValues):
				if self._current._position is None:
					self._current._position = n
				else:
					assert self._current._temp_for_statement is None
					self._current._temp_for_statement = n

			# elif isinstance(n, Coordinate):

			#   assert self._current._position is None
			#   self._current._position = n

			#   print( ' This is the Position_element_id:  '+   name + '       Coordinate')
			else:
				print('Something Wrong with Position_element_id!')
				#self._current._agent_ground_truth = AgentGroundTruth(Trace("Error Type",Scenario("Error Type")),name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line
													  , ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start
													  , ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__
													  , 'Position_element'))

	# Exit a parse tree produced by AVScenariosParser#position_element_id.
	def exitPosition_element_id(self, ctx:AVScenariosParser.Position_element_idContext):
		pass


	def enterDistance_statement(self, ctx:AVScenariosParser.Distance_statementContext):
		# print('Enter Distance_statement:  '+ctx.getText())
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			#print('66666666666')
			self._current._general_atom_statements_list.append(GeneralDistanceStatement())
			self._sema.begin_distance_statement(self._current._general_atom_statements_list[-1])
			# if self._current._distance_statement is None:
			#   self._current._distance_statement = GeneralDistanceStatement()
			#   self._sema.begin_distance_statement(self._current._distance_statement)
			# else:
			#   assert self._current._distance_statement_temp is None
			#   self._current._distance_statement_temp = GeneralDistanceStatement()
			#   self._sema.begin_distance_statement(self._current._distance_statement_temp)

		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			# print('233333333333333333333333_6666666666666')
			# print(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx.getText())
			# print('233333333333333333333333_6666666666666')
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				self._current._atom_statement_right = GeneralDistanceStatement()
				self._sema.begin_distance_statement(self._current._atom_statement_right)
			# else:
			#   self._current._atom_statement_right = ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2].getText()
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				self._current._atom_statement_left = GeneralDistanceStatement()
				self._sema.begin_distance_statement(self._current._atom_statement_left)
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			self._current._general_atom_statements_list.append(GeneralDistanceStatement())
			self._sema.begin_distance_statement(self._current._general_atom_statements_list[-1])
			#print('66666666666')
			# if self._current._distance_statement is None:
			#   self._current._distance_statement = GeneralDistanceStatement()
			#   self._sema.begin_distance_statement(self._current._distance_statement)
			# elif self._current._distance_statement_temp is None:
			#   self._current._distance_statement_temp = GeneralDistanceStatement()
			#   self._sema.begin_distance_statement(self._current._distance_statement_temp)             
			# else:
			#   assert self._current._atom_statement_left is None
			#   self._current._atom_statement_left = ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0].getText()
		

	# Exit a parse tree produced by AVScenariosParser#distance_statement.
	def exitDistance_statement(self, ctx:AVScenariosParser.Distance_statementContext):
		# print('Exit Distance_statement:  '+ctx.getText())
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			self._sema.end_distance_statement(self._current._general_atom_statements_list[-1])
			# if self._current._distance_statement_temp is None:
			#   self._sema.end_distance_statement(self._current._distance_statement)
			# else:
			#   self._sema.end_distance_statement(self._current._distance_statement_temp)
			#print('66666666666')
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			# print('233333333333333333333333_66666666666667777777')
			# print(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx.getText())
			# print('233333333333333333333333_66666666666667777777')
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				#assert self._current._atom_statement_right is None
				self._sema.end_distance_statement(self._current._atom_statement_right)
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				#assert self._current._atom_statement_left is None
				self._sema.end_distance_statement(self._current._atom_statement_left)
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			self._sema.end_distance_statement(self._current._general_atom_statements_list[-1])
			# if self._current._distance_statement_temp is None:
			#   self._sema.end_distance_statement(self._current._distance_statement)
			# else:
			#   self._sema.end_distance_statement(self._current._distance_statement_temp)
			# if self._current._sequence_of_statement1 is None:
			#   self._current._sequence_of_statement0 = 'first'
			# else: 
			#   self._current._sequence_of_statement0 = 'second'


	# Enter a parse tree produced by AVScenariosParser#perception_difference_statement.
	def enterPerception_difference_statement(self, ctx:AVScenariosParser.Perception_difference_statementContext):
		# print('Enter Perception_difference_statement:'+ctx.getText())
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			self._current._general_atom_statements_list.append(PerceptionDifferenceStatement())
			self._sema.begin_perception_difference_statement(self._current._general_atom_statements_list[-1])
			# if self._current._perception_difference_statement is None:
			#   self._current._perception_difference_statement = PerceptionDifferenceStatement()
			#   self._sema.begin_perception_difference_statement(self._current._perception_difference_statement) 
			# else:
			#   assert self._current._perception_difference_statement_temp is None
			#   self._current._perception_difference_statement_temp = PerceptionDifferenceStatement()
			#   self._sema.begin_perception_difference_statement(self._current._perception_difference_statement_temp) 

		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			# print('233333333333333333333333_6666666666666')
			# print(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx.getText())
			# print('233333333333333333333333_6666666666666')
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				self._current._atom_statement_right = PerceptionDifferenceStatement()
				self._sema.begin_perception_difference_statement(self._current._atom_statement_right)
			# else:
			#   assert self._current._atom_statement_right is None
			#   self._current._atom_statement_right = ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2].getText()
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				self._current._atom_statement_left = PerceptionDifferenceStatement()
				self._sema.begin_perception_difference_statement(self._current._atom_statement_left)
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			self._current._general_atom_statements_list.append(PerceptionDifferenceStatement())
			self._sema.begin_perception_difference_statement(self._current._general_atom_statements_list[-1])
			# if self._current._perception_difference_statement is None:
			#   self._current._perception_difference_statement = PerceptionDifferenceStatement()
			#   self._sema.begin_perception_difference_statement(self._current._perception_difference_statement) 
			# else:
			#   assert self._current._perception_difference_statement_temp is None
			#   self._current._perception_difference_statement_temp = PerceptionDifferenceStatement()
			#   self._sema.begin_perception_difference_statement(self._current._perception_difference_statement_temp) 
		
			# else:
			#   assert self._current._atom_statement_left is None
			#   self._current._atom_statement_left = ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0].getText()


	# Exit a parse tree produced by AVScenariosParser#perception_difference_statement.
	def exitPerception_difference_statement(self, ctx:AVScenariosParser.Perception_difference_statementContext):
	# print('Exit Perception_difference_statement:'+ctx.getText())
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			self._sema.end_perception_difference_statement(self._current._general_atom_statements_list[-1])
			# if self._current._perception_difference_statement_temp is None:
			#   self._sema.end_perception_difference_statement(self._current._perception_difference_statement)
			# else:
			#   self._sema.end_perception_difference_statement(self._current._perception_difference_statement_temp)
		#print('Perception_difference_statement:'+ctx.getText())
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			# print('233333333333333333333333_6666666666666')
			# print(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx.getText())
			# print('233333333333333333333333_6666666666666')
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				#assert self._current._atom_statement_right is None
				self._sema.end_perception_difference_statement(self._current._atom_statement_right)
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				#assert self._current._atom_statement_left is None
				self._sema.end_perception_difference_statement(self._current._atom_statement_left)
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			self._sema.end_perception_difference_statement(self._current._general_atom_statements_list[-1])
			# if self._current._perception_difference_statement_temp is None:
			#   self._sema.end_perception_difference_statement(self._current._perception_difference_statement)
			# else:
			#   self._sema.end_perception_difference_statement(self._current._perception_difference_statement_temp)
			# if self._current._sequence_of_statement1 is None:
			#   self._current._sequence_of_statement0 = 'first'
			# else: 
			#   self._current._sequence_of_statement0 = 'second'                
			# self._sema.end_distance_statement(self._current._distance_statement)
		self._current._agent_state = None
		self._current._agent_ground_truth = None


	# Enter a parse tree produced by AVScenariosParser#velocity_statement.
	def enterVelocity_statement(self, ctx:AVScenariosParser.Velocity_statementContext):
		# print('Enter Velocity_statement:'+ctx.getText())
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			self._current._general_atom_statements_list.append(VelocityStatement())
			self._sema.begin_velocity_statement(self._current._general_atom_statements_list[-1])
			# if self._current._velocity_statement is None:
			#   self._current._velocity_statement = VelocityStatement()
			#   self._sema.begin_velocity_statement(self._current._velocity_statement) 
			# else:
			#   assert self._current._velocity_statement_temp is None
			#   self._current._velocity_statement_temp = VelocityStatement()
			#   self._sema.begin_velocity_statement(self._current._velocity_statement_temp) 
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			# print('233333333333333333333333_6666666666666')
			# print(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx.getText())
			# print('233333333333333333333333_6666666666666')
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				self._current._atom_statement_right = VelocityStatement()
				self._sema.begin_velocity_statement(self._current._atom_statement_right)
			# else:
			#   self._current._atom_statement_right = ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2].getText()
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				self._current._atom_statement_left = VelocityStatement()
				self._sema.begin_velocity_statement(self._current._atom_statement_left)
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			self._current._general_atom_statements_list.append(VelocityStatement())
			self._sema.begin_velocity_statement(self._current._general_atom_statements_list[-1])
			# if self._current._velocity_statement is None:
			#   self._current._velocity_statement = VelocityStatement()
			#   self._sema.begin_velocity_statement(self._current._velocity_statement) 
			# else:
			#   assert self._current._velocity_statement_temp is None
			#   self._current._velocity_statement_temp = VelocityStatement()
			#   self._sema.begin_velocity_statement(self._current._velocity_statement_temp) 
			# else:
			#   assert self._current._atom_statement_left is None
			#   self._current._atom_statement_left = ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0].getText()

			
	# Exit a parse tree produced by AVScenariosParser#velocity_statement.
	def exitVelocity_statement(self, ctx:AVScenariosParser.Velocity_statementContext):
		# print('Exit Velocity_statement:'+ctx.getText())
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			self._sema.end_velocity_statement(self._current._general_atom_statements_list[-1])
			# if self._current._velocity_statement_temp is None:
			#   self._sema.end_velocity_statement(self._current._velocity_statement)
			# else:
			#   self._sema.end_velocity_statement(self._current._velocity_statement_temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			# print('233333333333333333333333_6666666666666')
			# print(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx.getText())
			# print('233333333333333333333333_6666666666666')
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				#assert self._current._atom_statement_right is None
				self._sema.end_velocity_statement(self._current._atom_statement_right)
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				#assert self._current._atom_statement_left is None
				self._sema.end_velocity_statement(self._current._atom_statement_left)
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			self._sema.end_velocity_statement(self._current._general_atom_statements_list[-1])
			# if self._current._velocity_statement_temp is None:
			#   self._sema.end_velocity_statement(self._current._velocity_statement)
			# else:
			#   self._sema.end_velocity_statement(self._current._velocity_statement_temp)
			# if self._current._sequence_of_statement1 is None:
			#   self._current._sequence_of_statement0 = 'first'
			# else: 
			#   self._current._sequence_of_statement0 = 'second'            


	# Enter a parse tree produced by AVScenariosParser#velocity_element_id.
	def enterVelocity_element_id(self, ctx:AVScenariosParser.Velocity_element_idContext):
		# print('Enter Velocity_element_id: '+ctx.getText())
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line
														, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start
														, ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			#self._current._agent_ground_truth = AgentGroundTruth(
				#Trace("Error Type", Scenario("Error Type")), name)
		else:
			n, _ = ret
			#print('Position_element_id: ' +name+'Index: '+ str(_))
			if isinstance(n, AgentGroundTruth):
				if self._current._agent_ground_truth is None:
					self._current._agent_ground_truth = n
				else:
					assert self._current._temp_for_statement is None
					self._current._temp_for_statement = n
				#print( ' This is the Velocity_element_id:  '+   ctx.getText() + '       agent_ground_truth')
			elif isinstance(n , EgoState):
				if self._current._ego_state is None:
					self._current._ego_state = n
				else:
					assert self._current._temp_for_statement is None
					self._current._temp_for_statement = n
				#print( ' This is the Velocity_element_id:  '+   ctx.getText() + '       ego_state')
			elif isinstance(n , AgentState):
				# print('!!!!!!!!!')
				if self._current._agent_state is None:
					self._current._agent_state = n
				else:
					assert self._current._temp_for_statement is None
					self._current._temp_for_statement = n
				#print( ' This is the Velocity_element_copy.deepcopy(n):  '+   ctx.getText() + '       agent_state')
			elif isinstance(n , Coordinate):
				self._current._coordinate_expression.append(n)
				# if self._current._coordinate is None:
				#   self._current._coordinate = n
				# else:
				#   assert self._current._temp_for_statement is None
				#   self._current._temp_for_statement = n
			elif isinstance(n, NameWithTwoRealValues):
				self._current._coordinate_expression.append(n)
				# if self._current._coordinate is None:
				#   self._current._coordinate = n
				# else:
				#   assert self._current._temp_for_statement is None
				#   self._current._temp_for_statement = n
			elif isinstance(n , Position):
				self._current._coordinate_expression.append(n)
				# if self._current._coordinate is None:
				#   self._current._coordinate = n
				# else:
				#   assert self._current._temp_for_statement is None
				#   self._current._temp_for_statement = n
				#print( ' This is the Velocity_element_id:  '+   ctx.getText() + '       velocity')
			else:
				#self._current._agent_ground_truth = AgentGroundTruth(Trace("Error Type",Scenario("Error Type")),name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line
													  , ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start
													  , ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__
													  , 'Velocity_element'))

	# Exit a parse tree produced by AVScenariosParser#velocity_element_id.
	def exitVelocity_element_id(self, ctx:AVScenariosParser.Velocity_element_idContext):
		pass


	# Enter a parse tree produced by AVScenariosParser#speed_statement.
	def enterSpeed_statement(self, ctx:AVScenariosParser.Speed_statementContext):
		# print('Enter speed_statement:'+ctx.getText())
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			self._current._general_atom_statements_list.append(SpeedStatement())
			self._sema.begin_speed_statement(self._current._general_atom_statements_list[-1])
			# if self._current._speed_statement is None:
			#   self._current._speed_statement = SpeedStatement()
			#   self._sema.begin_speed_statement(self._current._speed_statement) 
			# else:
			#   assert self._current._speed_statement_temp is None
			#   self._current._speed_statement_temp = SpeedStatement()
			#   self._sema.begin_speed_statement(self._current._speed_statement_temp) 
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			# print('233333333333333333333333_6666666666666')
			# print(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx.getText())
			# print('233333333333333333333333_6666666666666')
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				self._current._atom_statement_right = SpeedStatement()
				self._sema.begin_speed_statement(self._current._atom_statement_right)
			# else:
			#   self._current._atom_statement_right = ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2].getText()
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				self._current._atom_statement_left = SpeedStatement()
				self._sema.begin_speed_statement(self._current._atom_statement_left)
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			self._current._general_atom_statements_list.append(SpeedStatement())
			self._sema.begin_speed_statement(self._current._general_atom_statements_list[-1])
			# if self._current._speed_statement is None:
			#   self._current._speed_statement = SpeedStatement()
			#   self._sema.begin_speed_statement(self._current._speed_statement) 
			# else:
			#   assert self._current._speed_statement_temp is None
			#   self._current._speed_statement_temp = SpeedStatement()
			#   self._sema.begin_speed_statement(self._current._speed_statement_temp) 
			# else:
			#   assert self._current._atom_statement_left is None
			#   self._current._atom_statement_left = ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0].getText()
	
			
	# Exit a parse tree produced by AVScenariosParser#speed_statement.
	def exitSpeed_statement(self, ctx:AVScenariosParser.Speed_statementContext):
		# print('Exit speed_statement:'+ctx.getText())
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			self._sema.end_speed_statement(self._current._general_atom_statements_list[-1])
			# if self._current._speed_statement_temp is None:
			#   self._sema.end_speed_statement(self._current._speed_statement)
			# else:
			#   self._sema.end_speed_statement(self._current._speed_statement_temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			# print('233333333333333333333333_6666666666666')
			# print(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx.getText())
			# print('233333333333333333333333_6666666666666')
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				#assert self._current._atom_statement_right is None
				self._sema.end_speed_statement(self._current._atom_statement_right)
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				#assert self._current._atom_statement_left is None
				self._sema.end_speed_statement(self._current._atom_statement_left)
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			self._sema.end_speed_statement(self._current._general_atom_statements_list[-1])
			# if self._current._speed_statement_temp is None:
			#   self._sema.end_speed_statement(self._current._speed_statement)
			# else:
			#   self._sema.end_speed_statement(self._current._speed_statement_temp)
			# if self._current._sequence_of_statement1 is None:
			#   self._current._sequence_of_statement0 = 'first'
			# else: 
			#   self._current._sequence_of_statement0 = 'second'            


	# Enter a parse tree produced by AVScenariosParser#speed_element_id.
	def enterSpeed_element_id(self, ctx:AVScenariosParser.Speed_element_idContext):
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line
														, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start
														, ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
		else:
			n, _ = ret
			#print('Position_element_id: ' +name+'Index: '+ str(_))
			if isinstance(n, AgentGroundTruth):
				if self._current._agent_ground_truth is None:
					self._current._agent_ground_truth = n
				else:
					assert self._current._temp_for_statement is None
					self._current._temp_for_statement = n
				#print( ' This is the Velocity_element_id:  '+   ctx.getText() + '       agent_ground_truth')
			elif isinstance(n , EgoState):
				if self._current._ego_state is None:
					self._current._ego_state = n
				else:
					assert self._current._temp_for_statement is None
					self._current._temp_for_statement = n
				#print( ' This is the Velocity_element_id:  '+   ctx.getText() + '       ego_state')
			elif isinstance(n , AgentState):
				if self._current._agent_state is None:
					self._current._agent_state = n
				else:
					assert self._current._temp_for_statement is None
					self._current._temp_for_statement = n
				#print( ' This is the Velocity_element_copy.deepcopy(n):  '+   ctx.getText() + '       agent_state')
			elif isinstance(n , Speed):
				if self._current._speed is None:
					self._current._speed = n
				else:
					assert self._current._temp_for_statement is None
					self._current._temp_for_statement = n
			elif isinstance(n ,NameWithRealValue):
				if self._current._speed is None:
					self._current._speed = n
				else:
					assert self._current._temp_for_statement is None
					self._current._temp_for_statement = n
			# elif isinstance(n ,NameWithRealValueSignal):
			#   assert self._current._speed is None
			#   self._current._speed = n            
				#print( ' This is the Velocity_element_id:  '+   ctx.getText() + '       velocity')
			else:
				#self._current._agent_ground_truth = AgentGroundTruth(Trace("Error Type",Scenario("Error Type")),name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line
													  , ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start
													  , ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__
													  , 'Speed_element'))

	# Exit a parse tree produced by AVScenariosParser#speed_element_id.
	def exitSpeed_element_id(self, ctx:AVScenariosParser.Speed_element_idContext):
		pass


	 # Enter a parse tree produced by AVScenariosParser#acceleration_statement.
	def enterAcceleration_statement(self, ctx:AVScenariosParser.Acceleration_statementContext):
		# print('Enter Acceleration_statement:'+ctx.getText())
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			self._current._general_atom_statements_list.append(AccelerationStatement())
			self._sema.begin_acceration_statement(self._current._general_atom_statements_list[-1])
			# if self._current._acceleration_statement is None:
			#   self._current._acceleration_statement = AccelerationStatement()
			#   self._sema.begin_acceration_statement(self._current._acceleration_statement) 
			# else:
			#   assert self._current._acceleration_statement_temp is None
			#   self._current._acceleration_statement_temp = AccelerationStatement()
			#   self._sema.begin_acceration_statement(self._current._acceleration_statement_temp) 
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			# print('233333333333333333333333_6666666666666')
			# print(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx.getText())
			# print('233333333333333333333333_6666666666666')
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_right is None
				self._current._atom_statement_right = AccelerationStatement()
				self._sema.begin_acceration_statement(self._current._atom_statement_right)
			# else:
			#   self._current._atom_statement_right = ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2].getText()
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				assert self._current._atom_statement_left is None
				self._current._atom_statement_left = AccelerationStatement()
				self._sema.begin_acceration_statement(self._current._atom_statement_left)
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			self._current._general_atom_statements_list.append(AccelerationStatement())
			self._sema.begin_acceration_statement(self._current._general_atom_statements_list[-1])
			# if self._current._acceleration_statement is None:
			#   self._current._acceleration_statement = AccelerationStatement()
			#   self._sema.begin_acceration_statement(self._current._acceleration_statement) 
			# else:
			#   assert self._current._acceleration_statement_temp is None
			#   self._current._acceleration_statement_temp = AccelerationStatement()
			#   self._sema.begin_acceration_statement(self._current._acceleration_statement_temp) 
			# if self._current._sequence_of_statement1 is None:
			#   self._current._sequence_of_statement0 = 'first'
			# else: 
			#   self._current._sequence_of_statement0 = 'second'
			# else:
			#   assert self._current._atom_statement_left is None
			#   self._current._atom_statement_left = ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0].getText()
			

	# Exit a parse tree produced by AVScenariosParser#acceleration_statement.
	def exitAcceleration_statement(self, ctx:AVScenariosParser.Acceleration_statementContext):
		# print('ExitAcceleration_statement:'+ctx.getText())
		if ctx.parentCtx.parentCtx.parentCtx.parentCtx == None:
			self._sema.end_acceration_statement(self._current._general_atom_statements_list[-1])
			# if self._current._acceleration_statement_temp is None:
			#   self._sema.end_acceration_statement(self._current._acceleration_statement)
			# else:
			#   self._sema.end_acceration_statement(self._current._acceleration_statement_temp)
		elif isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			# print('233333333333333333333333_6666666666666')
			# print(ctx.parentCtx.parentCtx.parentCtx.parentCtx.parentCtx.getText())
			# print('233333333333333333333333_6666666666666')
			if ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx.parentCtx:
				#assert self._current._atom_statement_right is None
				self._sema.end_acceration_statement(self._current._atom_statement_right)
			elif ctx.parentCtx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx.parentCtx:
				#assert self._current._atom_statement_left is None
				self._sema.end_acceration_statement(self._current._atom_statement_left)
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			self._sema.end_acceration_statement(self._current._general_atom_statements_list[-1])
			# if self._current._acceleration_statement_temp is None:
			#   self._sema.end_acceration_statement(self._current._acceleration_statement)
			# else:
			#   self._sema.end_acceration_statement(self._current._acceleration_statement_temp)
			# if self._current._sequence_of_statement1 is None:
			#   self._current._sequence_of_statement0 = 'first'
			# else: 
			#   self._current._sequence_of_statement0 = 'second'


	# Enter a parse tree produced by AVScenariosParser#acceleration_element_id.
	def enterAcceleration_element_id(self, ctx:AVScenariosParser.Acceleration_element_idContext):
		name = ctx.children[0].getText()
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line
														, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start
														, ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
		else:
			n, _ = ret
			#print('Position_element_id: ' +name+'Index: '+ str(_))
			if isinstance(n, AgentGroundTruth):
				if self._current._agent_ground_truth is None:
					self._current._agent_ground_truth = n
				else:
					assert self._current._temp_for_statement is None
					self._current._temp_for_statement = n
				#print( ' This is the Velocity_element_id:  '+   ctx.getText() + '       agent_ground_truth')
			elif isinstance(n , EgoState):
				if self._current._ego_state is None:
					self._current._ego_state = n
				else:
					assert self._current._temp_for_statement is None
					self._current._temp_for_statement = n
				#print( ' This is the Velocity_element_id:  '+   ctx.getText() + '       ego_state')
			elif isinstance(n , AgentState):
				if self._current._agent_state is None:
					self._current._agent_state = n
				else:
					assert self._current._temp_for_statement is None
					self._current._temp_for_statement = n
				#print( ' This is the Velocity_element_copy.deepcopy(n):  '+   ctx.getText() + '       agent_state')
			elif isinstance(n , Coordinate):
				self._current._coordinate_expression.append(n)
				# if self._current._coordinate is None:
				#   self._current._coordinate = n
				# else:
				#   assert self._current._temp_for_statement is None
				#   self._current._temp_for_statement = n
			elif isinstance(n, NameWithTwoRealValues):
				self._current._coordinate_expression.append(n)
				# if self._current._coordinate is None:
				#   self._current._coordinate = n
				# else:
				#   assert self._current._temp_for_statement is None
				#   self._current._temp_for_statement = n
			elif isinstance(n , Position):
				self._current._coordinate_expression.append(n)
				# if self._current._coordinate is None:
				#   self._current._coordinate = n
				# else:
				#   assert self._current._temp_for_statement is None
				#   self._current._temp_for_statement = n
				#print( ' This is the Velocity_element_id:  '+   ctx.getText() + '       velocity')
			else:
				#self._current._agent_ground_truth = AgentGroundTruth(Trace("Error Type",Scenario("Error Type")),name)
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line
													  , ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start
													  , ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__
													  , 'Acceleration_element'))

	# Exit a parse tree produced by AVScenariosParser#acceleration_element_id.
	def exitAcceleration_element_id(self, ctx:AVScenariosParser.Acceleration_element_idContext):
		pass



	# Enter a parse tree produced by AVScenariosParser#real_value_for_general_statement.
	def enterReal_value_for_general_statement(self, ctx:AVScenariosParser.Real_value_for_general_statementContext):
		# print('Enter Real_value_for_general_statement: '+ctx.getText())
		pass

	# Exit a parse tree produced by AVScenariosParser#real_value_for_general_statement.
	def exitReal_value_for_general_statement(self, ctx:AVScenariosParser.Real_value_for_general_statementContext):
		# print('Exit Real_value_for_general_statement: '+ctx.getText())
		if isinstance(ctx.parentCtx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			# print('233333333333333333333333_6666666666666')
			# print(ctx.parentCtx.parentCtx.parentCtx.parentCtx.getText())
			# print('233333333333333333333333_6666666666666')
			if ctx.parentCtx.parentCtx.parentCtx.children[2]==ctx.parentCtx.parentCtx:
				self._current._atom_statement_right = ctx.getText()
				#assert self._current._atom_statement_right is None
				#self._sema.end_atom_predicate_right_difference_statement(self._current._atom_statement_right)
			elif ctx.parentCtx.parentCtx.parentCtx.children[0]==ctx.parentCtx.parentCtx:
				self._current._atom_statement_left = ctx.getText()
				#assert self._current._atom_statement_left is None
				#self._sema.end_atom_predicate_left_difference_statement(self._current._atom_statement_left)
			else:
				print('There is something wrong with: '+ ctx.getText())
		else:
			self._current._general_atom_statements_list.append(ctx.getText())


	def enterAtom_statement_overall_with_kuohao(self, ctx:AVScenariosParser.Atom_statement_overall_with_kuohaoContext):
		# print('Enter Atom_statement_overall_with_kuohao: '+ctx.getText())
		if self._current._kuohao_of_statement is None:
			self._current._kuohao_of_statement = []
			self._current._kuohao_of_statement.append(OverallStatement())
		else:
			self._current._kuohao_of_statement.append(OverallStatement())
		#pass


	def exitAtom_statement_overall_with_kuohao(self, ctx:AVScenariosParser.Atom_statement_overall_with_kuohaoContext):
		# print('Exit Atom_statement_overall_with_kuohao: '+ctx.getText())
		# print(self._current._kuohao_of_statement[-1].get_size_of_statements())
		# for _i in range(len(self._current._kuohao_of_statement[-1]._statements)):
		#   print(str(self._current._kuohao_of_statement[-1]._statements[_i]))
		# print(self._current._kuohao_of_statement[-1].get_size_of_operators())
		# for _i in range(len(self._current._kuohao_of_statement[-1]._operators)):
		#   print(str(self._current._kuohao_of_statement[-1]._operators[_i]))
		assert self._current._kuohao_of_statement[-1].get_size_of_statements()==self._current._kuohao_of_statement[-1].get_size_of_operators()+1
		self._current._general_atom_statements_list.append(self._current._kuohao_of_statement[-1])
		# print('###')
		#print(self._current._kuohao_of_statement[-1])
		self._current._kuohao_of_statement.pop()
		if len(self._current._kuohao_of_statement)==0:
			self._current._kuohao_of_statement = None
		#print(self._current._overall_statement)        


	def enterAtom_statement_overall_combination(self, ctx:AVScenariosParser.Atom_statement_overall_combinationContext):
		self._current._sequence_of_statement0 = None
		self._current._sequence_of_statement1 = None
		if self._current._overall_statement is None:
			self._current._overall_statement = OverallStatement()
		else:
			pass

	# Exit a parse tree produced by AVScenariosParser#atom_statement_overall_combination.
	def exitAtom_statement_overall_combination(self, ctx:AVScenariosParser.Atom_statement_overall_combinationContext):
		# print()
		# print('Exit Atom_statement_overall_combination:'+ctx.getText())
		len_before = len(self._current._overall_statement.get_statements())


		for _i in range(len(self._current._general_atom_statements_list)):
			self._current._overall_statement.add_statement(self._current._general_atom_statements_list[_i])
		self._current._general_atom_statements_list=[]

		len_after = len(self._current._overall_statement.get_statements())
		if len_after > len_before:
			# print(ctx.children[1].getText())
			if ctx.children[1].getText()=='.+':
				operator='+'
			elif ctx.children[1].getText()=='.-':
				operator='-'
			elif ctx.children[1].getText()=='.*':
				operator='*'
			elif ctx.children[1].getText()=='./':
				operator='/'
			self._current._overall_statement.add_operator(operator)

		assert len_after-len_before>= 0

		if self._current._kuohao_of_statement is not None and len(self._current._kuohao_of_statement)>0: #and len_after-len_before!=0:
			# print('!!!!!!!!!111')
			self._current._kuohao_of_statement[-1].add_operator(self._current._overall_statement._operators[-1])
			self._current._overall_statement._operators.pop()
			if len_after-len_before>=2 or len(self._current._kuohao_of_statement[-1].get_statements())==0:#isinstance(ctx.parentCtx, AVScenariosParser.Atom_statement_overall_with_kuohaoContext):
				# print('???2')
				self._current._kuohao_of_statement[-1].add_statement(self._current._overall_statement._statements[-2])
				self._current._kuohao_of_statement[-1].add_statement(self._current._overall_statement._statements[-1])
				self._current._overall_statement._statements.pop() 
				self._current._overall_statement._statements.pop() 
			else:
				# print('???1')
				self._current._kuohao_of_statement[-1].add_statement(self._current._overall_statement._statements[-1])
				self._current._overall_statement._statements.pop()
			#print(self._current._kuohao_of_statement[-1])
			#print(self._current._kuohao_of_statement[-1]) 


		if isinstance(ctx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
			#print('233333333333333333333333333333333333333333333333333333333333333333')
			if ctx.parentCtx.parentCtx.children[2]==ctx.parentCtx:
				assert self._current._atom_statement_right is None
				self._current._atom_statement_right=self._current._overall_statement
				# print('Right')
				# print(self._current._overall_statement)
				self._current._overall_statement = None
			if ctx.parentCtx.parentCtx.children[0]==ctx.parentCtx:
				assert self._current._atom_statement_left is None
				self._current._atom_statement_left=self._current._overall_statement
				# print('Left')
				# print(self._current._overall_statement)
				self._current._overall_statement = None

		

		# self._current._sequence_of_statement0 = None
		# self._current._sequence_of_statement1 = None

		#print(self._current._overall_statement)


	# assignment for the single statement, all the same
	def enterAssign_distance_statement(self, ctx:AVScenariosParser.Assign_distance_statementContext):
		#print('Assign_distance_statement:'+ctx.getText())
		pass

	def exitAssign_distance_statement(self, ctx:AVScenariosParser.Assign_distance_statementContext):
		# assert self._current._distance_statement is not None
		assert len(self._current._general_atom_statements_list) == 1
		name = ctx.children[0].getText()
		#print('Assign_distance_statement:'+ctx.getText())
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line
																, ctx.children[0].start.column
																, ctx.children[0].start.stop- ctx.start.start
																, ctx.children[0].stop.stop- ctx.start.start
																, ctx.getText()))
		else:
			self._sema.act_on_distance_statement(name)  
		self._current._general_atom_statements_list.pop()   
		# self._current._distance_statement = None


	# Enter a parse tree produced by AVScenariosParser#assignperception_difference_statement.
	def enterAssignperception_difference_statement(self, ctx:AVScenariosParser.Assignperception_difference_statementContext):
		#print('No way')
		pass

	# Exit a parse tree produced by AVScenariosParser#assignperception_difference_statement.
	def exitAssignperception_difference_statement(self, ctx:AVScenariosParser.Assignperception_difference_statementContext):
		#print('Assignperception_difference_statement:'+ctx.getText())
		# assert self._current._perception_difference_statement is not None
		assert len(self._current._general_atom_statements_list) == 1
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line
																, ctx.children[0].start.column
																, ctx.children[0].start.stop- ctx.start.start
																, ctx.children[0].stop.stop- ctx.start.start
																, ctx.getText()))
		else:
			self._sema.act_on_perception_difference_statement(name) 
		self._current._general_atom_statements_list.pop()   
		# self._current._perception_difference_statement = None 


	def enterAssign_velocity_statement(self, ctx:AVScenariosParser.Assign_velocity_statementContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#assign_velocity_statement.
	def exitAssign_velocity_statement(self, ctx:AVScenariosParser.Assign_velocity_statementContext):
		#print('Assignperception_difference_statement:'+ctx.getText())
		# assert self._current._velocity_statement is not None
		assert len(self._current._general_atom_statements_list) == 1
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line
																, ctx.children[0].start.column
																, ctx.children[0].start.stop- ctx.start.start
																, ctx.children[0].stop.stop- ctx.start.start
																, ctx.getText()))
		else:
			#print('Assign_velocity_statement '+ ctx.getText())
			#print(name)
			self._sema.act_on_velocity_statement(name)  
		self._current._general_atom_statements_list.pop()   
		# self._current._velocity_statement = None  


	# Enter a parse tree produced by AVScenariosParser#assign_speed_statement.
	def enterAssign_speed_statement(self, ctx:AVScenariosParser.Assign_speed_statementContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#assign_speed_statement.
	def exitAssign_speed_statement(self, ctx:AVScenariosParser.Assign_speed_statementContext):
		# assert self._current._speed_statement is not None
		# print(ctx.getText())
		assert len(self._current._general_atom_statements_list) == 1
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line
																, ctx.children[0].start.column
																, ctx.children[0].start.stop- ctx.start.start
																, ctx.children[0].stop.stop- ctx.start.start
																, ctx.getText()))
		else:
			#print('Assign_velocity_statement '+ ctx.getText())
			#print(name)
			self._sema.act_on_speed_statement(name) 
		self._current._general_atom_statements_list.pop()
		# self._current._speed_statement = None 


	# Enter a parse tree produced by AVScenariosParser#assign_acceleration_statement.
	def enterAssign_acceleration_statement(self, ctx:AVScenariosParser.Assign_acceleration_statementContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#assign_acceleration_statement.
	def exitAssign_acceleration_statement(self, ctx:AVScenariosParser.Assign_acceleration_statementContext):
		# assert self._current._acceleration_statement is not None
		assert len(self._current._general_atom_statements_list) == 1
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line
																, ctx.children[0].start.column
																, ctx.children[0].start.stop- ctx.start.start
																, ctx.children[0].stop.stop- ctx.start.start
																, ctx.getText()))
		else:
			self._sema.act_on_acceleration_statement(name)  
		# self._current._acceleration_statement = None  
		self._current._general_atom_statements_list.pop()







	# # Enter a parse tree produced by AVScenariosParser#atom_predicate.
	# def enterAtom_predicate(self, ctx:AVScenariosParser.Atom_predicateContext):
	# 	#print('Enter Atom_predicate:  '+ctx.getText())
	# 	assert self._current._atom_statement_left is None
	# 	assert self._current._atom_statement_right is None

	# # Exit a parse tree produced by AVScenariosParser#atom_predicate.
	# def exitAtom_predicate(self, ctx:AVScenariosParser.Atom_predicateContext):
	# 	#print('Exit Atom_predicate:  '+ctx.getText())
	# 	assert self._current._atom_statement_left is not None
	# 	assert self._current._atom_statement_right is not None


	# Enter a parse tree produced by AVScenariosParser#atom_statement_var.
	# def enterAtom_statement_var(self, ctx:AVScenariosParser.Atom_statement_varContext):
	#   #pass
		

	# # Exit a parse tree produced by AVScenariosParser#atom_statement_var.
	# def exitAtom_statement_var(self, ctx:AVScenariosParser.Atom_statement_varContext):
		

	# Enter a parse tree produced by AVScenariosParser#atom_statement_id.
	def enterAtom_statement_id(self, ctx:AVScenariosParser.Atom_statement_idContext):
		#assert self._current._atom_statement is None
		name = ctx.children[0].getText()
		# print('The atom statement id:'+name)
		ret = self._sema.find_node(name)
		if not ret:
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line
														, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start
														, ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			#self._current._agent_ground_truth = GeneralAssertion(name)
		else:
			n, _ = ret
			#print('Atom_statement_id: ' +name+'Index: '+ str(_))
			if isinstance(n, GeneralDistanceStatement):
				if isinstance(ctx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
					#print('Atom_statement_id: ' +name+'Index: '+ str(_))
					if ctx.parentCtx.parentCtx.children[2]==ctx.parentCtx:
						assert self._current._atom_statement_right is None
						self._current._atom_statement_right = n
					elif ctx.parentCtx.parentCtx.children[0]==ctx.parentCtx:
						assert self._current._atom_statement_left is None
						self._current._atom_statement_left = n
					else:
						print('Something is wrong with id:'+ name)
				else:
					self._current._general_atom_statements_list.append(n)

			elif isinstance(n, PerceptionDifferenceStatement):
				if isinstance(ctx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
					if ctx.parentCtx.parentCtx.children[2]==ctx.parentCtx:
						assert self._current._atom_statement_right is None
						self._current._atom_statement_right = n
					elif ctx.parentCtx.parentCtx.children[0]==ctx.parentCtx:
						assert self._current._atom_statement_left is None
						self._current._atom_statement_left = n
					else:
						print('Something is wrong with id:'+ name)
				else:
					self._current._general_atom_statements_list.append(n)


			elif isinstance(n, VelocityStatement):
				if isinstance(ctx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
					if ctx.parentCtx.parentCtx.children[2]==ctx.parentCtx:
						assert self._current._atom_statement_right is None
						self._current._atom_statement_right = n
					elif ctx.parentCtx.parentCtx.children[0]==ctx.parentCtx:
						assert self._current._atom_statement_left is None
						self._current._atom_statement_left = n
					else:
						print('Something is wrong with id:'+ name)
				else:
					self._current._general_atom_statements_list.append(n)


			elif isinstance(n, SpeedStatement):
				if isinstance(ctx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
					if ctx.parentCtx.parentCtx.children[2]==ctx.parentCtx:
						assert self._current._atom_statement_right is None
						self._current._atom_statement_right = n
					elif ctx.parentCtx.parentCtx.children[0]==ctx.parentCtx:
						assert self._current._atom_statement_left is None
						self._current._atom_statement_left = n
					else:
						print('Something is wrong with id:'+ name)
				else:
					self._current._general_atom_statements_list.append(n)


			elif isinstance(n, AccelerationStatement):
				if isinstance(ctx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
					if ctx.parentCtx.parentCtx.children[2]==ctx.parentCtx:
						assert self._current._atom_statement_right is None
						self._current._atom_statement_right = n
					elif ctx.parentCtx.parentCtx.children[0]==ctx.parentCtx:
						assert self._current._atom_statement_left is None
						self._current._atom_statement_left = n
					else:
						print('Something is wrong with id:'+ name)
				else:
					self._current._general_atom_statements_list.append(n)

			elif isinstance(n, OverallStatement):
				if isinstance(ctx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
					if ctx.parentCtx.parentCtx.children[2]==ctx.parentCtx:
						assert self._current._atom_statement_right is None
						self._current._atom_statement_right = n
					elif ctx.parentCtx.parentCtx.children[0]==ctx.parentCtx:
						assert self._current._atom_statement_left is None
						self._current._atom_statement_left = n
					else:
						print('Something is wrong with id:'+ name)
				else:
					self._current._general_atom_statements_list.append(n)
			elif isinstance(n, NameWithRealValue):
				if isinstance(ctx.parentCtx.parentCtx.parentCtx, AVScenariosParser.General_assertion0Context):
					# print('2333333333?????????????')

					if ctx.parentCtx.parentCtx.children[2]==ctx.parentCtx:
						assert self._current._atom_statement_right is None
						self._current._atom_statement_right = n
					elif ctx.parentCtx.parentCtx.children[0]==ctx.parentCtx:
						assert self._current._atom_statement_left is None
						self._current._atom_statement_left = n
					else:
						print('Something is wrong with id:'+ name)
				else:
					# print('?????????????')
					self._current._general_atom_statements_list.append(n)       

			else:
				print('Something go wrong with enterAtom_statement_id')
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line
													  , ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start
													  , ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__
													  , 'AtomStatement'))

	# Exit a parse tree produced by AVScenariosParser#atom_statement_id.
	def exitAtom_statement_id(self, ctx:AVScenariosParser.Atom_statement_idContext):
		pass





	# Enter a parse tree produced by AVScenariosParser#assign_speed.
	def enterAssign_speed(self, ctx:AVScenariosParser.Assign_speedContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#assign_speed.
	def exitAssign_speed(self, ctx:AVScenariosParser.Assign_speedContext):
		assert self._current._speed is not None
		name = ctx.children[0].getText()
		if not self._sema.check_unique_id(name):
			self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line
																, ctx.children[0].start.column
																, ctx.children[0].start.stop- ctx.start.start
																, ctx.children[0].stop.stop- ctx.start.start
																, ctx.getText()))
		else:
			#print('Assign_velocity_statement '+ ctx.getText())
			#print(name)
			self._sema.act_on_speed(name)   
		self._current._speed = None


	# # Enter a parse tree produced by AVScenariosParser#assign_velocity.
	# def enterAssign_coordinate(self, ctx:AVScenariosParser.Assign_coordinateContext):
	#   pass

	# # Exit a parse tree produced by AVScenariosParser#assign_velocity.
	# def exitAssign_coordinate(self, ctx:AVScenariosParser.Assign_coordinateContext):
	#   print('Exit Assign_coordinate:  '+ctx.getText())
	#   assert self._current._coordinate is not None
	#   name = ctx.children[0].getText()
	#   # print('Assign_velocity_statement '+ ctx.getText())
	#   if not self._sema.check_unique_id(name):
	#       self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line
	#                                                           , ctx.children[0].start.column
	#                                                           , ctx.children[0].start.stop- ctx.start.start
	#                                                           , ctx.children[0].stop.stop- ctx.start.start
	#                                                           , ctx.getText()))
	#   else:
	#       #print('Assign_velocity_statement '+ ctx.getText())
	#       #print(name)
	#       self._sema.act_on_coordinate(name)  
	#   self._current._coordinate = None






	# Enter a parse tree produced by AVScenariosParser#general_assertion0.
	def enterGeneral_assertion0_0(self, ctx:AVScenariosParser.General_assertion0_0Context):
		# print('Enter General_assertion0: '+ctx.getText())
		pass
		# print('first')

	# Exit a parse tree produced by AVScenariosParser#general_assertion0.
	def exitGeneral_assertion0_0(self, ctx:AVScenariosParser.General_assertion0_0Context):
		# print('Exit General_assertion0: '+ctx.getText())
		# print('second')
		# print('general_assertion0:'+ctx.getText())
		assert len(self._current._general_assertion_list)>=1
		temp = KuoHaoWithGeneral()
		temp.set_gneral_assertion(self._current._general_assertion_list[-1].get_assertion())
		self._current._general_assertion_list[-1].add_assertion(temp) 



		# Enter a parse tree produced by AVScenariosParser#traffic_rule_boolean_related_APIs.
	def enterTraffic_rule_boolean_related_APIs(self, ctx:AVScenariosParser.Traffic_rule_boolean_related_APIsContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#traffic_rule_boolean_related_APIs.
	def exitTraffic_rule_boolean_related_APIs(self, ctx:AVScenariosParser.Traffic_rule_boolean_related_APIsContext):
		assert self._current._traffic_rule_boolean_API is not None
		self._current._general_assertion_list.append(SingleGeneralAssertion())

		boolean = self._current._traffic_rule_boolean_API
		atom_predicate1=AtomPredicate()
		atom_predicate1.set_atom_statement_left(boolean)
		atom_predicate1.set_atom_statement_right(boolean.get_API_value())
		atom_predicate1.set_compare_operator(boolean.get_API_operator())
		self._current._general_assertion_list[-1].add_assertion(atom_predicate1)
		self._current._traffic_rule_boolean_API = None



	# Enter a parse tree produced by AVScenariosParser#general_assertion0.
	def enterGeneral_assertion0(self, ctx:AVScenariosParser.General_assertion0Context):
		# print('Enter General_assertion0: '+ctx.getText())
		pass
		# print('first')

	# Exit a parse tree produced by AVScenariosParser#general_assertion0.
	def exitGeneral_assertion0(self, ctx:AVScenariosParser.General_assertion0Context):
		# print('Exit General_assertion0: '+ctx.getText())
		# print(self._current._atom_statement_left )
		assert self._current._atom_statement_left is not None
		assert self._current._atom_statement_right is not None      

		self._current._general_assertion_list.append(SingleGeneralAssertion())
		atom_predicate1=AtomPredicate()
		atom_predicate1.set_atom_statement_left(self._current._atom_statement_left)
		atom_predicate1.set_atom_statement_right(self._current._atom_statement_right)
		atom_predicate1.set_compare_operator(ctx.children[0].children[1].getText())
		self._current._general_assertion_list[-1].add_assertion(atom_predicate1)

			#self._current._general_assertion = None
		self._current._atom_statement_left = None
		self._current._atom_statement_right = None




	# Enter a parse tree produced by AVScenariosParser#general_assertion1.
	def enterGeneral_assertion1(self, ctx:AVScenariosParser.General_assertion1Context):
		pass
		# print('Enter General_assertion1:  '+ctx.getText())

	# Exit a parse tree produced by AVScenariosParser#general_assertion1.
	def exitGeneral_assertion1(self, ctx:AVScenariosParser.General_assertion1Context):
		# print('Exit General_assertion1:  '+ctx.getText())
		# print('second')
		# print('general_assertion1:'+ctx.getText())
		# if self._current._general_assertion1 is not None:
		#   assert self._current._general_assertion is not None
		#   temp = NotWithGeneral()
		#   temp.set_gneral_assertion(self._current._general_assertion1.get_assertion())
		#   self._current._general_assertion1.add_assertion(temp) 
		# else:
		assert len(self._current._general_assertion_list)>=1
		temp = NotWithGeneral()
		temp.set_gneral_assertion(self._current._general_assertion_list[-1].get_assertion())
		self._current._general_assertion_list[-1].add_assertion(temp) 
		# else:
		#   #print(self._current._general_assertion)
		#   #print(self._current._general_assertion1)
		#   assert self._current._general_assertion1 is not None
		#   temp = NotWithGeneral()
		#   temp.set_gneral_assertion(self._current._general_assertion1.get_assertion())
		#   self._current._general_assertion1.add_assertion(temp) 
		# if isinstance(self._current._general_assertion, SingleGeneralAssertion):
		#   print('Whywhywhy!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

		#print(self._current._general_assertion.get_assertion())
	
	# Enter a parse tree produced by AVScenariosParser#general_assertion4.
	def enterGeneral_assertion2(self, ctx:AVScenariosParser.General_assertion2Context):
		pass
		# print('Enter general_assertion2:'+ctx.getText())


	# Exit a parse tree produced by AVScenariosParser#general_assertion4.
	def exitGeneral_assertion2(self, ctx:AVScenariosParser.General_assertion2Context):
		# assert self._current._general_assertion is not None
		# assert self._current._general_assertion1 is None
		# print('Exit general_assertion2:'+ctx.getText())
		assert len(self._current._general_assertion_list)>=1
		temp = GeneralAssertionWithTemporalOperator()
		temp.set_assertion(self._current._general_assertion_list[-1].get_assertion())
		temp.set_temporal_operator(ctx.children[0].getText())
		self._current._general_assertion_list[-1].add_assertion(temp)


	# Enter a parse tree produced by AVScenariosParser#general_assertion3.
	def enterGeneral_assertion3(self, ctx:AVScenariosParser.General_assertion3Context):
		pass

	# Exit a parse tree produced by AVScenariosParser#general_assertion3.
	def exitGeneral_assertion3(self, ctx:AVScenariosParser.General_assertion3Context):
		assert len(self._current._general_assertion_list)>=2
		temp = GeneralAssertionWithUnitl()
		temp.set_general_assertion_left(self._current._general_assertion_list[-2].get_assertion())
		temp.set_general_assertion_right(self._current._general_assertion_list[-1].get_assertion()) 
		temp.set_temporal_operator(ctx.children[1].getText())
		self._current._general_assertion_list.pop()
		self._current._general_assertion_list[-1].add_assertion(temp)


	# Enter a parse tree produced by AVScenariosParser#general_assertion2.
	def enterGeneral_assertion4(self, ctx:AVScenariosParser.General_assertion4Context):
		pass
		# print('Enter General_assertion4:  ' + ctx.getText())


	# Exit a parse tree produced by AVScenariosParser#general_assertion2.
	def exitGeneral_assertion4(self, ctx:AVScenariosParser.General_assertion4Context):
		# print('Exit General_assertion4:  ' + ctx.getText())
		# print('second')
		# print('general_assertion2:'+ctx.getText())
		# assert self._current._general_assertion is not None
		# assert self._current._general_assertion1 is not None
		assert len(self._current._general_assertion_list)>=2
		temp = AndWithGeneral()
		temp.set_general_assertion_left(self._current._general_assertion_list[-2].get_assertion())
		temp.set_general_assertion_right(self._current._general_assertion_list[-1].get_assertion())
		self._current._general_assertion_list.pop()
		self._current._general_assertion_list[-1].add_assertion(temp)
		# self._current._general_assertion.add_assertion(temp)
		# self._current._general_assertion1 = None



	# Enter a parse tree produced by AVScenariosParser#general_assertion3.
	def enterGeneral_assertion5(self, ctx:AVScenariosParser.General_assertion5Context):
		pass
		# print('first')

	# Exit a parse tree produced by AVScenariosParser#general_assertion3.
	def exitGeneral_assertion5(self, ctx:AVScenariosParser.General_assertion5Context):
		# print('Exit General_assertion5: '+ctx.getText())
		assert len(self._current._general_assertion_list)>=2
		temp = OrWithGeneral()
		temp.set_general_assertion_left(self._current._general_assertion_list[-2].get_assertion())
		temp.set_general_assertion_right(self._current._general_assertion_list[-1].get_assertion())
		self._current._general_assertion_list.pop()
		self._current._general_assertion_list[-1].add_assertion(temp)






	# Enter a parse tree produced by AVScenariosParser#general_assertion5.
	def enterGeneral_assertion6(self, ctx:AVScenariosParser.General_assertion5Context):
		#print('Enter General_assertion5: '+ctx.getText())
		pass

	# Exit a parse tree produced by AVScenariosParser#general_assertion5.
	def exitGeneral_assertion6(self, ctx:AVScenariosParser.General_assertion5Context):
		# print('Exit General_assertion6: '+ctx.getText())
		# assert self._current._general_assertion is not None
		# assert self._current._general_assertion1 is not None
		if len(self._current._general_assertion_list)>=2:
		#print('general_assertion5:'+ctx.getText())
			# print('Exit Coor_laneID_rv:     '+ ctx.getText()+ '   '+ str(self._current._real_value_expression))
			temp = DeriveWithGeneral()
			temp.set_general_assertion_left(self._current._general_assertion_list[-2].get_assertion())
			temp.set_general_assertion_right(self._current._general_assertion_list[-1].get_assertion())
			self._current._general_assertion_list.pop()
			self._current._general_assertion_list[-1].add_assertion(temp)
		else:
			assert self._current._lane_coordinate is None
			assert self._current._lane is not None
			assert len(self._current._real_value_expression)>0
			# print('Exit Coor_laneID_rv:     '+ ctx.getText()+ '   '+ str(self._current._real_value_expression))

			self._current._lane_coordinate = LaneCoordinate(self._current._real_value_expression[-1])
			self._current._real_value_expression.pop()
			self._sema.begin_lane_coordinate(self._current._lane_coordinate)
			# if self._current._lane_coordinate1 is None:
			self._sema.end_lane_coordinate(self._current._lane_coordinate)
			self._current._lane = None
		# self._current._general_assertion.add_assertion(temp)
		# self._current._general_assertion1 = None




	# Enter a parse tree produced by AVScenariosParser#assign_general_assertion_to_var.
	def enterAssign_general_assertion_to_var(self, ctx:AVScenariosParser.Assign_general_assertion_to_varContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#assign_general_assertion_to_var.
	def exitAssign_general_assertion_to_var(self, ctx:AVScenariosParser.Assign_general_assertion_to_varContext):
		# print('Assign_general_assertion_to_var:'+ctx.getText())
		# assert self._current._general_assertion is not None
		# assert self._current._general_assertion1 is None
		if len(self._current._general_assertion_list) == 1:
			name = ctx.children[0].getText()
			temp = SingleGeneralAssertion()
			temp.set_name(name)
				# temp.add_assertion(self._current._general_assertion.get_assertion())#copy.deepcopy(self._current._general_assertion)
			temp.add_assertion(self._current._general_assertion_list[-1].get_assertion())
			if not self._sema.check_unique_id(name):
				# print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
				self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line
																		, ctx.children[0].start.column
																		, ctx.children[0].start.stop- ctx.start.start
																		, ctx.children[0].stop.stop- ctx.start.start
																		, ctx.getText()))
			else:
				temp.set_name(name)
				if isinstance(temp, SingleGeneralAssertion):
					self._sema._ast.add_ast_node(temp)
						#print('success in add node: '+ name)
				else:
					print('Something unexpected happen with Assign_general_assertion_to_var: ' +name+' is Not SingleGeneralAssertion')
				# self._current._general_assertion = None
			self._current._general_assertion_list.pop()
			# print(len(self._current._general_assertion_list))
		elif self._current._lane_coordinate is not None:
			name = ctx.children[0].getText()
			if not self._sema.check_unique_id(name):
				self._sema.add_error(RedefinitionVariableError(name, ctx.children[0].start.line, ctx.children[0].start.column
															   , ctx.children[0].start.stop- ctx.start.start,
															   ctx.children[0].stop.stop- ctx.start.start
															   , ctx.getText()))
			elif len(ctx.children) == 5:
				self._current._lane = self._current._lane_coordinate.get_lane()
				self._sema.act_on_lane_coordinate_position(name, '',self._current._lane_coordinate.get_distance())
				# self._current._real_value_expression.pop()
			else:  # len(...)==6
				self._current._lane = self._current._lane_coordinate.get_lane()
				self._sema.act_on_lane_coordinate_position(name, ctx.children[2].getText()
														   , self._current._lane_coordinate.get_distance())
				# self._current._real_value_expression.pop()
			self._current._lane = None
			self._current._lane_coordinate = None
		else:
			print('Something unexpected happen with Assign_general_assertion_to_var')



	# Enter when the General_assertion_id is used in expression
	# replace the variable with expression
	def enterGeneral_assertion_id(self, ctx:AVScenariosParser.General_assertion_idContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#general_assertion_id.
	def exitGeneral_assertion_id(self, ctx:AVScenariosParser.General_assertion_idContext):
		# if self._current._general_assertion is None:
		#   assert self._current._general_assertion1 is None
		# if self._current._general_assertion is not None:
		#   assert self._current._general_assertion1 is None
		# print('Exit General_assertion_id: '+ctx.getText())
		name = ctx.getText()
		ret = self._sema.find_node(name)
		if not ret:     
			# print('!!!!!!!!!!!!!!Can not find the node: '+ name)  
			self._sema.add_error(UndefinedVariableError(name, ctx.children[0].start.line
														, ctx.children[0].start.column
														, ctx.children[0].start.stop- ctx.start.start
														, ctx.children[0].stop.stop- ctx.start.start
														, ctx.getText()))
			# if self._current._general_assertion is not None:
			#   assert self._current._general_assertion1 is None
			#   self._current._general_assertion1 = SingleGeneralAssertion()
			# elif self._current._general_assertion is None:
			#   assert self._current._general_assertion is None
			#   self._current._general_assertion = SingleGeneralAssertion()
			self._current._general_assertion_list.append(SingleGeneralAssertion())
		else:
			n, index = ret
			if isinstance(n, SingleGeneralAssertion):
				#self._current._general_assertion = n
				temp=SingleGeneralAssertion()
				temp.set_name(n.get_name())
				temp.add_assertion(n.get_assertion()) 
				self._current._general_assertion_list.append(temp)
				# print(temp.get_assertion())

			elif isinstance(n, NameWithRealValue):
				self._current._real_value_expression.append(n._value)
			elif isinstance(n, Lane):
				self._current._lane = n
				# print('Lane: '+str(self._current._lane ))
			elif isinstance(n, NameWithString):
				context=self._sema.find_context_for_error(n.get_name())
				l = self._sema.cast_to_lane(n)
				self._sema.set(index, l)
				self._current._lane = l
				# print('NameWithString: '+str(self._current._lane ))

			else:
				#self._current._agent_ground_truth = SingleGeneralAssertion(name)
				print('Not the type of SingleGeneralAssertion ??????')
				self._sema.add_error(IllegalTypeError(name, ctx.children[0].start.line
													  , ctx.children[0].start.column
													  , ctx.children[0].start.stop- ctx.start.start
													  , ctx.children[0].stop.stop- ctx.start.start
													  , ctx.getText(), n.__class__.__name__
													  , 'SingleGeneralAssertion'))
		#pass








	# Enter a parse tree produced by AVScenariosParser#assign_general_assertion.
	def enterAssign_general_assertion(self, ctx:AVScenariosParser.Assign_general_assertionContext):
		pass

	# Exit a parse tree produced by AVScenariosParser#assign_general_assertion.
	def exitAssign_general_assertion(self, ctx:AVScenariosParser.Assign_general_assertionContext):
		assert self._current._trace is not None
		# assert self._current._general_assertion is not None
		# assert self._current._general_assertion1 is None
		# print(' Exit Assign_general_assertion'+ctx.getText())
		# print(str(len(self._current._general_assertion_list)))
		# for i in self._current._general_assertion_list:
		#   print(i.get_assertion())
		assert len(self._current._general_assertion_list) == 1
		self._current._trace.add_general_assertion(self._current._general_assertion_list[0])

		#self._current._trace.add_general_assertion(self._current._general_assertion)

		self._current._general_assertion_list.pop()
		assert len(self._current._general_assertion_list)==0
		self._current._trace=None



# Global parsing function:parse a file into AST.
def Parse(file_name: AnyStr) -> AST:
	file = FileStream(file_name)
	lexer = AVScenariosLexer(file)
	tokens = CommonTokenStream(lexer)
	parser = AVScenariosParser(tokens)
	sema = Sema(file.fileName)
	listener = ASTListener(sema)
	walker = ParseTreeWalker()
	walker.walk(listener, parser.scenarios())

	#print(sema.get_ast())
	return sema.get_ast()
