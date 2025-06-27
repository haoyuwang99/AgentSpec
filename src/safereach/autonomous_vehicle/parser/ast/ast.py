from parser.ast.base.motion import *
from parser.ast.base.pedestrian_type import *
from parser.ast.base.vehicle_type import *
from parser.ast.base.weathers import *
from parser.ast.base.shape import *
from parser.ast.scenario.scenario import *
from parser.ast.unresolved.unresolved import *
from parser.ast.assertion.assertion import *
from typing import AnyStr, Callable, List, Mapping, TypeVar
from parser.ast.error.error import *
import sys
import copy
# forward declaration of all allowed types.
ALLOWED_TYPES = TypeVar("ALLOWED_TYPES", NameWithRealValue
, NameWithString
, NameWithTwoRealValues,Scenario,EgoVehicle
, PedestrianType,VehicleType,Position,Heading,Color
, NPCVehicle,Pedestrians,Weathers
, Traffic,Obstacle,NameWithMotion
, Speed, Height,SpeedRange,Lane, WeatherContinuousIndex
, IntersectionID, Map, SpecificType, GeneralType
, State, VehicleMotion, PedestrianMotion, StateList, Pedestrians, NPCVehicles
, Obstacles, Pedestrian, Shape, Environment
, Time, Weather, WeatherDiscreteLevel
, IntersectionTraffic, SpeedLimitation,Type
, AgentGroundDistance,AgentGroundTruth,AgentError
, DetectionAssertion,IntersectionAssertion,SafetyAssertion,SpeedConstraintAssertion
,EgoState,AgentState,Trace,AssignAssertionToTrace
,StateStateListErrorType,StateVehicleTypeStateListErrorType,StateVehicleTypePedestrianTypeStateListErrorType
,PedestriansNPCVehiclesObstaclesWeathersTrafficErrorType,
GeneralDistanceStatement,PerceptionDifferenceStatement,
SingleGeneralAssertion,VelocityStatement
)

class AST:
	def __init__(self):
		self._nodes: List[ALLOWED_TYPES] = []
		self._nodes_for_general: List[Union[SingleGeneralAssertion]]=[]
		self._scenarios:List[Scenario]=[]
		self._traces:List[Trace]=[]

	# def add_nodes_for_general_assertion(self, node_value: SingleGeneralAssertion):
	# 	self._nodes_for_general.append(node_value)#copy.deepcopy(node_value))

	def add_ast_node(self, value:ALLOWED_TYPES):
		self._nodes.append(value)
		# print('Add One')
		# print(len(self._nodes))
		# print(value.get_name())
		# print(value.get_node_kind())
	def get_ast_tree(self)->List[ALLOWED_TYPES]:
		return self._nodes
	def add_scenario(self,s:Scenario):
		self._scenarios.append(s)
	def get_scenarios(self)->List[Scenario]:
		return self._scenarios
	def add_trace(self,t:Trace):
		self._traces.append(t)
	def get_traces(self)->List[Trace]:
		return self._traces

	

	def find_node(self,name:AnyStr)->Optional[Tuple[ALLOWED_TYPES,int]]:
		''' 
			Finding function:
			call this function must call check_unique_id first to
			guarantee the unique id in the ast tree.
			:param name: The name of the node you want to find.
			:returns: If successfully finds the node,return it and its index in AST tree,
				otherwise return the none object.
		'''
		nodes:List[ALLOWED_TYPES]=self.get_ast_tree()
		for index,node in enumerate(nodes):
			
			if name==node.get_name():
				# print('find_node:')
				# print(name)
				# print(index)
				return node,index
		else:
			return None


	# def find_node_for_general(self, name:AnyStr)->Optional[Tuple[ALLOWED_TYPES,int]]:
	# 	nodes:List[SingleGeneralAssertion] = self._nodes_for_general
	# 	for index,node in enumerate(nodes):
	# 		if name==node.get_name():
	# 			return node,index
	# 	else:
	# 		return None


	def check_unique_id(self,name:AnyStr)->bool:
		''' 
			Check the name to avoiding conflict with other nodes of the AST tree.
			:param name: The name of the node you want to check.
			:returns: If the name is unique,return true
				otherwise return false.
		'''
		for val in self.get_ast_tree():
			if name == val.get_name():
				return False
		return True
class ASTDumper:
	def __init__(self,ast:AST)->NoReturn:
		self._ast=ast
		self._kv:Mapping[NodeType,Callable[...,NoReturn]]={
			NodeType.T_NRV:self.dump_name_with_real_value,
			NodeType.T_NS:self.dumpName_with_string,
			NodeType.T_NTRV:self.dump_name_with_two_real_values,
			NodeType.T_SCENARIO:self.dump_scenario,
			NodeType.T_EGO:self.dump_ego_vehicle,
			NodeType.T_PEDTYPE:self.dump_pedestrian_type,
			NodeType.T_VETYPE:self.dump_vehicle_type,
			NodeType.T_POS:self.dump_position,
			NodeType.T_HEADING:self.dump_heading,
			NodeType.T_STATE:self.dump_state,
			NodeType.T_NPC:self.dump_npc_vehicle,
			NodeType.T_PEDS:self.dump_pedestrians,
			NodeType.T_WEAS:self.dump_weathers,
			NodeType.T_TRAFFIC:self.dump_traffic,
			NodeType.T_OB:self.dump_obstacle,
			NodeType.T_NMOTION:self.dump_name_with_motion,
			NodeType.T_SPEED:self.dump_speed, 
			NodeType.T_LANE:self.dump_lane, 
			NodeType.T_WEACON:self.dump_weather_continuous_index,
			NodeType.T_INTERID:self.dump_intersection_id, 
			NodeType.T_MAP:self.dump_map, 
			NodeType.T_NPCS:self.dump_npc_vehicles,
			NodeType.T_OBS:self.dump_obstacles,
			NodeType.T_ENV:self.dump_environment,
			NodeType.T_TYPE:self.dump_type,
			NodeType.T_COLOR:self.dump_color,
			NodeType.T_VEMOTION:self.dump_vehicle_motion,
			NodeType.T_STATELIST:self.dump_state_list,
			NodeType.T_PED:self.dump_pedestrian,
			NodeType.T_PEDMOTION:self.dump_pedestrian_motion,
			NodeType.T_HEIGHT:self.dump_height,
			NodeType.T_SHAPE:self.dump_shape,
			NodeType.T_TIME:self.dump_time,
			NodeType.T_WEA:self.dump_weather,
			NodeType.T_WEADIS:self.dump_weather_discrete_level,
			NodeType.T_INTERTRA:self.dump_intersection_traffic,
			NodeType.T_SPEEDLIMIT:self.dump_speed_limitation,
			NodeType.T_SPEEDRANGE:self.dump_speed_range,
			NodeType.T_TRACE:self.dump_trace,
			NodeType.T_EGOSTATE:self.dump_ego_state,
			NodeType.T_AGENTSTATE:self.dump_agent_state,
			NodeType.T_AGENTGROUNDTRUTH:self.dump_agent_ground_truth,
			NodeType.T_AGENTGROUNDDIS:self.dump_agent_ground_distance,
			NodeType.T_AGENTERROR:self.dump_agent_error,
			NodeType.T_DETECTIONS:self.dump_detection_assertion,
			NodeType.T_SAFETYS:self.dump_safety_assertion,
			NodeType.T_INTERASSERT:self.dump_intersection_assertion,
			NodeType.T_SPEEDCA:self.dump_speed_constraint_assertion,
			NodeType.T_AASSERTIONTRACE:self.dump_assign_assertion_to_trace
		}
	def switch(self,node:ALLOWED_TYPES)->Callable[[int,ALLOWED_TYPES],NoReturn]:
		return self._kv[node.get_node_kind()]
	def dump(self):
		for node in self._ast.get_ast_tree():
			self.switch(node)(0,node)
	#TODO: dump the scenarios.
	def dump_scenarios(self)->NoReturn:
		pass
	def dump_lane(self,indent:int,lane:Lane):
		sys.stdout.write(indent*' ')
		if lane.is_anonymous():
			sys.stdout.write(f'-Lane:[anonymous][laneID:{lane._id}]\n')
		else:
			sys.stdout.write(f'-Lane:[name:{lane._name}][laneID:{lane._id}]\n')
	def dump_lane_coordinate(self,indent:int,coor:LaneCoordinate):
		if coor.get_lane().is_anonymous():
			self.dump_lane(indent,coor.get_lane())		
		else:
			sys.stdout.write(indent*' ')
			sys.stdout.write(f'-Lane:{coor.get_lane().get_name()}\n')
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-{coor.get_distance()}\n')
	def dump_coordinate(self,indent:int,coor:Coordinate):
		sys.stdout.write(indent*' ')
		if coor.has_z():
			z=coor.get_z()
			if z>0:
				sys.stdout.write(f'-({coor.get_x()},{coor.get_y()},+{coor.get_z()})\n')
			elif z<0:
				sys.stdout.write(f'-({coor.get_x()},{coor.get_y()},{coor.get_z()})\n')
			else:
				sys.stdout.write(f'-({coor.get_x()},{coor.get_y()},+0)\n')
		else:
			sys.stdout.write(f'-({coor.get_x()},{coor.get_y()})\n')
	def dump_position(self,indent:int,pos:Position):
		name=f'name:{pos.get_name()}' if not pos.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		if pos.has_frame():
			sys.stdout.write(f'-Position:[{name}][kind:{CoordinateFrame.switch(pos.get_frame().name)}]\n')
		else:
			sys.stdout.write(f'-Position:[{name}]\n')
		if pos.is_normal_coordinate():
			self.dump_coordinate(indent+2,pos.get_coordinate())
		else:
			self.dump_lane_coordinate(indent+2,pos.get_coordinate())
	def dump_predined_direction(self,indent:int,d:PredefinedDirection):	
		if d.is_default_ego():
			sys.stdout.write(indent*' ')
			sys.stdout.write(f'-direction:EGO\n')
		elif d.is_lane_reference():
			if d.get_lane_reference()[0].is_anonymous():
				self.dump_lane(indent,d.get_lane_reference()[0])
				sys.stdout.write((indent) * ' ')
				sys.stdout.write(f'-{d.get_lane_reference()[1]}\n')
			else:
				sys.stdout.write(indent*' ')
				sys.stdout.write(f'-Lane:{d.get_lane_reference()[0].get_name()}\n')
				sys.stdout.write(indent * ' ')
				sys.stdout.write(f'-{d.get_lane_reference()[1]}\n')
		else:
			sys.stdout.write(indent * ' ')
			if isinstance(d.get_reference(),EgoVehicle):
				sys.stdout.write(f'-EgoVehicle{d.get_reference().get_name()}\n')
			elif isinstance(d.get_reference(), Pedestrian):
				sys.stdout.write(f'-Pedestrian{d.get_reference().get_name()}\n')
			elif isinstance(d.get_reference(),NPCVehicle):
				sys.stdout.write(f'-NPCVehicle{d.get_reference().get_name()}\n')
	def dump_heading(self,indent:int,h:Heading):
		name=f'name:{h.get_name()}' if not h.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		pi='pi' if h.is_pi_value() else ''
		sys.stdout.write(f'-Heading:[{name}][angle:{h.get_raw_heading_angle()} {pi} {Unit.switch(h._unit.name)}]\n')
		sys.stdout.write(indent*' ')
		if h.has_direction():
			self.dump_predined_direction(indent+2,h.get_direction())
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-direction:[default]\n')
	def dump_speed(self,indent:int,s:Speed):
		name=f'name:{s.get_name()}' if not s.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-Speed:[{name}][value:{s.get_speed_value()}]\n')

	def dump_state(self,indent:int,s:State):
		name=f'name:{s.get_name()}' if not s.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-State:[{name}]\n')
		if s.get_position().is_anonymous():
			self.dump_position(indent+2,s.get_position())
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-Position:{s.get_position().get_name()}\n')
		if s.has_heading():
			if s.get_heading().is_anonymous():
				self.dump_heading(indent+2,s.get_heading())
			else:
				sys.stdout.write((indent+2)*' ')
				sys.stdout.write(f'-Heading:{s.get_heading().get_name()}\n')
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-Heading:[default]\n')
		if s.has_speed():
			if s.get_speed().is_anonymous():
				self.dump_speed(indent+2,s.get_speed())
			else:
				sys.stdout.write((indent+2)*' ')
				sys.stdout.write(f'-Speed:{s.get_speed().get_name()}\n')
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-Speed:[default]\n')
	def dump_uniform_motion(self,indent:int,m:UniformMotion):
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-{UniformIndex.switch(m.get_uniform_index().name)}\n')
		if not m.get_state().is_anonymous():
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-State:{m.get_state().get_name()}\n')
		else:
			self.dump_state(indent+2,m.get_state())
	def dump_state_list(self,indent:int,l:StateList):
		name=f'name:{l.get_name()}' if not l.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-StateList:[{name}]\n')
		for s in l.get_states():
			if s.is_anonymous():
				self.dump_state(indent+2,s)
			else:
				sys.stdout.write((indent+2)*' ')
				sys.stdout.write(f'-State:{s.get_name()}\n')
	def dump_waypoint_motion(self,indent:int,m:WaypointMotion):
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-{WaypointIndex.switch(m.get_waypoint_index().name)}\n')
		if m.get_state_list().is_anonymous():
			self.dump_state_list(indent+2,m.get_state_list())	
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-StateList:{m.get_state_list().get_name()}\n')
	def dump_vehicle_motion(self,indent:int,m:VehicleMotion):
		sys.stdout.write(indent*' ')
		name=f'name:{m.get_name()}' if not m.is_anonymous() else f'anonymous'
		sys.stdout.write(f'-VehicleMotion:[{name}]\n')
		if m.is_uniform_motion():
			self.dump_uniform_motion(indent+2,m.get_motion())
		elif m.is_waypoint_motion():
			self.dump_waypoint_motion(indent+2,m.get_motion())

	def dump_pedestrian_motion(self,indent:int,m:PedestrianMotion):
		sys.stdout.write(indent*' ')
		name=f'name:{m.get_name()}' if not m.is_anonymous() else f'anonymous'
		sys.stdout.write(f'-PedestrianMotion:[{name}]\n')
		if m.is_uniform_motion():
			self.dump_uniform_motion(indent+2,m.get_motion())
		elif m.is_waypoint_motion():
			self.dump_waypoint_motion(indent+2,m.get_motion())
	def dump_height(self,indent:int,h:Height):
		name=f'name:{h.get_name()}' if not h.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-Height:[{name}][value:{h.get_value()}]\n')
	def dump_pedestrian_type(self,indent:int,t:PedestrianType):
		name=f'name:{t.get_name()}' if not t.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-PedestrianType:[{name}]\n')
		if t.get_height().is_anonymous():
			self.dump_height(indent+2,t.get_height())
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-Height:{t.get_height().get_name()}\n')
		if t.get_color().is_anonymous():
			self.dump_color(indent+2,t.get_color())
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-Color:{t.get_color().get_name()}\n')
	def dump_sphere(self,indent:int,s:Sphere):
		name=f'name:{s.get_name()}' if not s.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-Sphere:[{name}][radius:{s.get_radius()}]\n')
	def dump_box(self,indent:int,b:Box):
		name=f'name:{b.get_name()}' if not b.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-Box:[{name}][length:{b.get_length()}][width:{b.get_width()}][height:{b.get_height()}]\n')
	def dump_cone(self,indent:int,c:Cone):
		name=f'name:{c.get_name()}' if not c.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-Cone:[{name}][radius:{c.get_radius()}][height:{c.get_height()}]\n')
	def dump_cylinder(self,indent:int,c:Cylinder):
		name=f'name:{c.get_name()}' if not c.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-Cylinder:[{name}][radius:{c.get_radius()}][height:{c.get_height()}]\n')
	def dump_shape(self,indent:int,s:Shape):
		if isinstance(s,Box):
			self.dump_box(indent,s)
		elif isinstance(s,Sphere):
			self.dump_sphere(indent,s)
		elif isinstance(s,Cone):
			self.dump_cone(indent,s)
		elif isinstance(s,Cylinder):
			self.dump_cylinder(indent,s)
	def dump_specific_type(self,indent:int,t:SpecificType):
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-{t.get_value()}\n')
	def dump_general_type(self,indent:int,t:GeneralType):
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-{GeneralTypeEnum.switch(t.get_kind().name)}\n')
	def dump_type(self,indent:int,t:Type):
		name=f'name:{t.get_name()}' if not t.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-Type:[{name}]\n')
		if isinstance(t,GeneralType):
			self.dump_general_type(indent+2,t)
		elif isinstance(t,SpecificType):
			self.dump_specific_type(indent+2,t)
	def dump_material(self,indent:int,m:Material):
		pass
	def dump_color_list(self,indent:int,c:ColorList):
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-{ColorListEnum.switch(c.get_kind().name)}\n')
	def dump_rgb_color(self,indent:int,c:RGBColor):
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-{c.get_value()}\n')
	def dump_color(self,indent:int,c:Color):
		name=f'name:{c.get_name()}' if not c.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-Color:[{name}]\n')
		if isinstance(c,ColorList):
			self.dump_color_list(indent+2,c)
		elif isinstance(c,RGBColor):
			self.dump_rgb_color(indent+2,c)
	def dump_vehicle_type(self,indent:int,t:VehicleType):
		name=f'name:{t.get_name()}' if not t.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-VehicleType:[{name}]\n')
		if t.get_type().is_anonymous():
			self.dump_type(indent+2,t.get_type())
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-Type:{t.get_type().get_name()}\n')
		if t.has_color():
			if t.get_color().is_anonymous():
				self.dump_color(indent+2,t.get_color())
			else:
				sys.stdout.write((indent+2)*' ')
				sys.stdout.write(f'-Color:{t.get_color().get_name()}\n')
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-Color:[default]\n')
		# if t.get_material() is not None:
		# 	self.dump_material(indent+2,t.get_material())

	def dump_weather_continuous_index(self,indent:int,w:WeatherContinuousIndex):
		name = f'name:{w.get_name()}' if not w.is_anonymous() else f'anonymous'
		sys.stdout.write(indent * ' ')
		sys.stdout.write(f'-Level:[{name}][value:{w.get_index()}]\n')
	def dump_weather_discrete_level(self,indent:int,w:WeatherDiscreteLevel):
		name = f'name:{w.get_name()}' if not w.is_anonymous() else f'anonymous'
		sys.stdout.write(indent * ' ')
		sys.stdout.write(f'-Level:[{name}][value:{WeatherDiscreteLevelEnum.switch(w.get_level().name)}]\n')
	def dump_weather(self,indent:int,w:Weather):
		name=f'name:{w.get_name()}' if not w.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-Weather:[{name}][kind:{WeatherKind.switch(w.get_weather_kind().name)}]\n')
		if w.is_weather_continuous_index():
			if w.get_weather_kind_value().is_anonymous():
				self.dump_weather_continuous_index(indent + 2, w.get_weather_kind_value())
			else:
				sys.stdout.write((indent + 2) * ' ')
				sys.stdout.write(f'-Level:{w.get_weather_kind_value().get_name()}\n')
		elif w.is_weather_discrete_level():
			if w.get_weather_kind_value().is_anonymous():
				self.dump_weather_discrete_level(indent+2,w.get_weather_kind_value())
			else:
				sys.stdout.write((indent + 2) * ' ')
				sys.stdout.write(f'-Level:{w.get_weather_kind_value().get_name()}\n')
	def dump_weathers(self,indent:int,w:Weathers):
		name=f'name:{w.get_name()}' if not w.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-Weathers:[{name}]\n')
		for ww in w.get_weathers():
			if ww.is_anonymous():
				self.dump_weather(indent+2,ww)
			else:
				sys.stdout.write((indent+2)*' ')
				sys.stdout.write(f'-Weather:{ww.get_name()}\n')
	def dump_time(self,indent:int,t:Time):
		name=f'name:{t.get_name()}' if not t.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-Time:[{name}][value:{t.get_hour()}::{t.get_minute()}]\n')
	def dump_ego_vehicle(self,indent:int,e:EgoVehicle):
		name=f'name:{e.get_name()}' if not e.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-EgoVehicle:[{name}]\n')
		if e.get_first_state().is_anonymous():
			self.dump_state(indent+2,e.get_first_state())
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-State:{e.get_first_state().get_name()}\n')
		if e.get_second_state().is_anonymous():	
			self.dump_state(indent+2,e.get_second_state())
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-State:{e.get_second_state().get_name()}\n')
		if e.has_vehicle_type():
			if e.get_vehicle_type().is_anonymous():
				self.dump_vehicle_type(indent+2,e.get_vehicle_type())
			else:
				sys.stdout.write((indent+2)*' ')
				sys.stdout.write(f'-VehicleType:{e.get_vehicle_type().get_name()}\n')
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-VehicleType:[default]\n')
	def dump_environment(self,indent:int,e:Environment):
		name=f'name:{e.get_name()}' if not e.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-Environment:[{name}]\n')
		if e.get_weathers().is_anonymous():
			self.dump_weathers(indent+2,e.get_weathers())
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-Weathers:{e.get_weathers().get_name()}\n')
		if e.get_time().is_anonymous():
			self.dump_time(indent+2,e.get_time())
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-Time:{e.get_time().get_name()}\n')
	def dump_map(self,indent:int,m:Map):
		name=f'name:{m.get_name()}' if not m.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-Map:[{name}][map:{m.get_map_name()}]\n')
	def dump_npc_vehicle(self,indent:int,n:NPCVehicle):
		name=f'name:{n.get_name()}' if not n.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-NPCVehicle:[{name}]\n')
		if n.get_first_state().is_anonymous():
			self.dump_state(indent+2,n.get_first_state())
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-State:{n.get_first_state().get_name()}\n')
		if n.has_vehicle_motion():
			if n.get_vehicle_motion().is_anonymous():
				self.dump_vehicle_motion(indent+2,n.get_vehicle_motion())
			else:
				sys.stdout.write((indent+2)*' ')
				sys.stdout.write(f'-VehicleMotion:{n.get_vehicle_motion().get_name()}\n')
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-VehicleMotion:[default]\n')
		if n.has_second_state():
			if n.get_second_state().is_anonymous():
				self.dump_state(indent+2,n.get_second_state())
			else:
				sys.stdout.write((indent+2)*' ')
				sys.stdout.write(f'-State:{n.get_second_state().get_name()}\n')
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-State:[default]\n')
		if n.has_vehicle_type():
			if n.get_vehicle_type().is_anonymous():
				self.dump_vehicle_type(indent+2,n.get_vehicle_type())
			else:
				sys.stdout.write((indent+2)*' ')
				sys.stdout.write(f'-VehicleType:{n.get_vehicle_type().get_name()}\n')
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-VehicleType:[default]\n')
	def dump_npc_vehicles(self,indent:int,n:NPCVehicles):
		name=f'name:{n.get_name()}' if not n.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-NPCVehicles:[{name}]\n')
		for nn in n.get_npc_vehicles():
			if nn.is_anonymous():
				self.dump_npc_vehicle(indent+2,nn)
			else:
				sys.stdout.write((indent+2)*' ')
				sys.stdout.write(f'-NPCVehicle:{nn.get_name()}\n')
	def dump_obstacle(self,indent:int,o:Obstacle):
		name=f'name:{o.get_name()}' if not o.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-Obstacle:[{name}]\n')
		if o.get_position().is_anonymous():
			self.dump_position(indent+2,o.get_position())
		else:
			sys.stdout.write((indent+2)*'')
			sys.stdout.write(f'-Position:{o.get_position().get_name()}\n')
		if o.has_shape():
			if o.get_shape().is_anonymous():
				self.dump_shape(indent+2,o.get_shape())
			else:
				sys.stdout.write((indent+2)*'')
				sys.stdout.write(f'-Shape:{o.get_shape().get_name()}\n')
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-Shape:[default]\n')
	def dump_obstacles(self,indent:int,o:Obstacles):
		name=f'name:{o.get_name()}' if not o.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-Obstacles:[{name}]\n')
		for oo in o.get_obstacles():
			if oo.is_anonymous():
				self.dump_obstacle(indent+2,oo)
			else:
				sys.stdout.write((indent+2)*' ')
				sys.stdout.write(f'-Obstacle:{oo.get_name()}\n')
	def dump_pedestrian(self,indent:int,p:Pedestrian):
		name=f'name:{p.get_name()}' if not p.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-Pedestrian:[{name}]\n')
		if p.get_first_state().is_anonymous():
			self.dump_state(indent+2,p.get_first_state())
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-State:{p.get_first_state().get_name()}\n')
		if p.has_second_state():
			if p.get_second_state().is_anonymous():
				self.dump_state(indent+2,p.get_second_state())
			else:
				sys.stdout.write((indent+2)*' ')
				sys.stdout.write(f'-State:{p.get_second_state().get_name()}\n')
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-State:[default]\n')
		if p.has_pedestrian_motion():
			if p.get_pedestrian_motion().is_anonymous():
				self.dump_pedestrian_motion(indent+2,p.get_pedestrian_motion())
			else:
				sys.stdout.write((indent+2)*' ')
				sys.stdout.write(f'-PedestrianMotion:{p.get_pedestrian_motion().get_name()}\n')
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-PedestrianMotion:[default]\n')
		if p.has_pedestrian_type():
			if p.get_pedestrian_type().is_anonymous():
				self.dump_pedestrian_type(indent+2,p.get_pedestrian_type())
			else:
				sys.stdout.write((indent+2)*' ')
				sys.stdout.write(f'-PedestrianType:{p.get_pedestrian_type().get_name()}\n')
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-PedestrianType:[default]\n')
	def dump_pedestrians(self,indent:int,p:Pedestrians):
		name=f'name:{p.get_name()}' if not p.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-Pedestrians:[{name}]\n')
		for pp in p.get_pedestrians():
			if pp.is_anonymous():
				self.dump_pedestrian(indent+2,pp)
			else:
				sys.stdout.write((indent+2)*' ')
				sys.stdout.write(f'-Pedestrian:{pp.get_name()}\n')
	def dump_intersection_id(self,indent:int,i:IntersectionID):
		name=f'name:{i.get_name()}' if not i.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-IntersectionID:[{name}][id:{i.get_value()}]\n')
	def dump_intersection_traffic(self,indent:int,i:IntersectionTraffic):
		name=f'name:{i.get_name()}' if not i.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-IntersectionTraffic:[{name}][trafficLight:{i.get_traffic_light()}][stopSign:{i.get_stop_sign()}][crosswalk:{i.get_crosswalk()}]\n')
		if i.get_id().is_anonymous():
			self.dump_intersection_id(indent+2,i.get_id())
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-IntersectionID:{i.get_id().get_name()}\n')
	def dump_speed_range(self,indent:int,s:SpeedRange):
		name=f'name:{s.get_name()}' if not s.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-SpeedRange:[{name}][value:{s.get_value()}]\n') 
	def dump_speed_limitation(self,indent:int,s:SpeedLimitation):
		name=f'name:{s.get_name()}' if not s.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-SpeedLimitation:[{name}]\n')
		if s.get_lane().is_anonymous():
			self.dump_lane(indent+2,s.get_lane())
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-Lane:{s.get_lane().get_name()}\n')
		if s.get_speed_range().is_anonymous():
			self.dump_speed_range(indent+2,s.get_speed_range())
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-SpeedRange:{s.get_speed_range().get_name()}\n')
	def dump_traffic(self,indent:int,t:Traffic):
		name=f'name:{t.get_name()}' if not t.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-Traffic:[{name}]\n')
		for i in t.get_intersection_traffics():
			if i.is_anonymous():
				self.dump_intersection_traffic(indent+2,i)
			else:
				sys.stdout.write((indent+2)*' ')
				sys.stdout.write(f'-IntersectionTraffic:{i.get_name()}\n')
		for s in t.get_speed_limitations():
			if s.is_anonymous():
				self.dump_speed_limitation(indent+2,s)
			else:
				sys.stdout.write((indent+2)*' ')
				sys.stdout.write(f'-SpeedLimitation:{s.get_name()}\n')
	def dump_name_with_real_value(self,indent:int,n:NameWithRealValue):
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-Unresolved type:{n.get_name()}={n.get_value()}\n')
	def dumpName_with_string(self,indent:int,n:NameWithString):
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-Unresolved type:{n.get_name()}={n.get_value()}\n')
	def dump_name_with_two_real_values(self,indent:int,n:NameWithTwoRealValues):
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-Unresolved type:{n.get_name()}={n.get_value()}\n')
	def dump_name_with_motion(self,indent:int,n:NameWithMotion):
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-Unresolved type:{n.get_name()}\n')
		if n.is_waypoint_motion():
			self.dump_waypoint_motion(indent+2,n.get_motion())
		elif n.is_uniform_motion():
			self.dump_uniform_motion(indent+2,n.get_motion())
	def dump_scenario(self,indent:int,s:Scenario):
		name=f'name:{s.get_name()}' if not s.is_anonymous() else f'anonymous'
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-Scenario:[{name}]\n') 
		if s.get_map().is_anonymous():
			self.dump_map(indent+2,s.get_map())
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-Map:{s.get_map().get_name()}\n')
		if s.get_ego_vehicle().is_anonymous():
			self.dump_ego_vehicle(indent+2,s.get_ego_vehicle())
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-EgoVehicle:{s.get_ego_vehicle().get_name()}\n')
		if s.has_npc_vehicles():
			if s.get_npc_vehicles().is_anonymous():
				self.dump_npc_vehicles(indent+2,s.get_npc_vehicles())
			else:
				sys.stdout.write((indent+2)*' ')
				sys.stdout.write(f'-NPCVehicles:{s.get_npc_vehicles().get_name()}\n')
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-NPCVehicles:[default]\n')
		if s.has_pedestrians():
			if s.get_pedestrians().is_anonymous():
				self.dump_pedestrians(indent+2,s.get_pedestrians())
			else:
				sys.stdout.write((indent+2)*' ')
				sys.stdout.write(f'-Pedestrians:{s.get_pedestrians().get_name()}\n')
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-Pedestrians:[default]\n')
		if s.has_obstacles():
			if s.get_obstacles().is_anonymous():
				self.dump_obstacles(indent+2,s.get_obstacles())
			else:
				sys.stdout.write((indent+2)*' ')
				sys.stdout.write(f'-Obstacles:{s.get_obstacles().get_name()}\n')
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-Obstacles:[default]\n')
		if s.has_environment():
			if s.get_environment().is_anonymous():
				self.dump_environment(indent+2,s.get_environment())
			else:
				sys.stdout.write((indent+2)*' ')
				sys.stdout.write(f'-Environment:{s.get_environment().get_name()}\n')
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-Environment:[default]\n')
		if s.has_traffic():
			if s.get_traffic().is_anonymous():
				self.dump_traffic(indent+2,s.get_traffic())
			else:
				sys.stdout.write((indent+2)*' ')
				sys.stdout.write(f'-Traffic:{s.get_traffic().get_name()}\n')
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-Traffic:[default]\n')
	## dump assertions
	def dump_trace(self,indent:int,t:Trace):
		sys.stdout.write(indent*' ')
		sys.stdout.write(f'-Trace:[name:{t.get_name()}][scenario:{t.get_scenario().get_name()}]\n')
	def dump_ego_state(self,indent:int,es:EgoState):
		sys.stdout.write(indent*' ')
		sys.stdout.write('-EgoState:')
		if es.is_anonymous():
			sys.stdout.write(str(es))
			sys.stdout.write('\n')
		else:
			sys.stdout.write(es.get_name())
			sys.stdout.write('=')
			sys.stdout.write(str(es))
			sys.stdout.write('\n')
	def dump_agent_state(self,indent:int,asp:AgentState):
		sys.stdout.write(indent*' ')
		sys.stdout.write('-AgentState:')
		if asp.is_anonymous():
			sys.stdout.write(str(asp))
			sys.stdout.write('\n')
		else:
			sys.stdout.write(asp.get_name()+'=')
			sys.stdout.write(str(asp))
			sys.stdout.write('\n')
	def dump_agent_ground_truth(self,indent:int,agt:AgentGroundTruth):
		sys.stdout.write(indent*' ')
		sys.stdout.write('-AgentGroundTruth:')
		if agt.is_anonymous():
			sys.stdout.write(str(agt))
			sys.stdout.write('\n')
		else:
			sys.stdout.write(agt.get_name()+'=')
			sys.stdout.write(str(agt))
			sys.stdout.write('\n')
	def dump_agent_ground_distance(self,indent:int,agd:AgentGroundDistance):
		name=f'{agd.get_name()}' if not agd.is_anonymous() else f''
		sys.stdout.write(indent*' ')
		sys.stdout.write('-AgentGroundDistance:')
		sys.stdout.write(f'{name}=')
		sys.stdout.write('\n')
		sys.stdout.write((indent+2)*' ')
		sys.stdout.write('-dis(')
		if agd.get_agent_ground_truth().is_anonymous():
			self.dump_agent_ground_truth(indent+2,agd.get_agent_ground_truth())
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(agd.get_agent_ground_truth().get_name())
		sys.stdout.write(',')
		if agd.get_ego_state().is_anonymous():
			self.dump_ego_state(indent+2,agd.get_ego_state())
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(agd.get_ego_state().get_name())
		sys.stdout.write(')')
		sys.stdout.write('\n')
	def dump_agent_error(self,indent:int,ae:AgentError):
		name=f'{ae.get_name()}' if not ae.is_anonymous() else f''
		sys.stdout.write(indent*' ')
		sys.stdout.write('-AgentError:')
		sys.stdout.write(f'{name}=')
		sys.stdout.write('\n')
		sys.stdout.write((indent+2)*' ')
		sys.stdout.write('-diff(')
		if ae.get_agent_state().is_anonymous():
			self.dump_agent_state(indent+2,ae.get_agent_state())
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(ae.get_agent_state().get_name())
		sys.stdout.write(',')
		if ae.get_agent_ground_truth().is_anonymous():
			self.dump_agent_ground_truth(indent+2,ae.get_agent_ground_truth())
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(ae.get_agent_ground_truth().get_name())
		sys.stdout.write(')')
		sys.stdout.write('\n')
	def dump_agent_safety_assertion(self,indent:int,asa:AgentSafetyAssertion):
		sys.stdout.write(indent*' ')
		sys.stdout.write('-AgentSafetyAssertion:')
		sys.stdout.write('\n')
		sys.stdout.write((indent+2)*' ')
		sys.stdout.write('dis(')
		if asa.get_ego_state().is_anonymous():
			self.dump_ego_state(indent+2,asa.get_ego_state())
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(asa.get_ego_state().get_name())
		sys.stdout.write(',')
		if asa.get_agent_state().is_anonymous():
			self.dump_agent_state(indent+2,asa.get_agent_state())
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(asa.get_agent_state().get_name())
		sys.stdout.write(')')
		sys.stdout.write('>=')
		sys.stdout.write(f'{asa.get_safety_radius()}')
		sys.stdout.write('\n')
	def dump_ego_speed(self,indent:int,es:EgoSpeed):
		sys.stdout.write(indent*' ')
		sys.stdout.write('-EgoSpeed:')
		sys.stdout.write(str(es))
		sys.stdout.write('\n')
	def dump_green_light_state(self,indent:int,gls:GreenLightState):
		sys.stdout.write(indent*' ')
		sys.stdout.write('-GreenLightState:')
		sys.stdout.write(str(gls))
		sys.stdout.write('\n')
	def dump_red_light_state(self,indent:int,rls:RedLightState):
		sys.stdout.write(indent*' ')
		sys.stdout.write('-RedLightState:')
		sys.stdout.write(str(rls))
		sys.stdout.write('\n')
	def dump_agent_visible_detection_assertion(self,indent:int,avda:AgentVisibleDetectionAssertion):
		sys.stdout.write(indent*' ')
		sys.stdout.write('-AgentVisibleDetectionAssertion:')
		sys.stdout.write('\n')
		if avda.get_agent_ground_distance().is_anonymous():
			self.dump_agent_ground_distance(avda.get_agent_ground_distance())
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(avda.get_agent_ground_distance().get_name())
			sys.stdout.write('\n')
		sys.stdout.write((indent+2)*' ')
		sys.stdout.write('<=')
		sys.stdout.write(f'{avda.get_sensing_range()}')
		sys.stdout.write('\n')
	def dump_traffic_detection_assertion(self,indent:int,tda:TrafficDetectionAssertion):
		sys.stdout.write(indent*' ')
		sys.stdout.write('-TrafficDetectionAssertion:')
		sys.stdout.write(str(tda))
		sys.stdout.write('\n')
	def dump_agent_error_detection_assertion(self,indent:int,aeda:AgentErrorDetectionAssertion):
		sys.stdout.write(indent*' ')
		sys.stdout.write('-AgentErrorDetectionAssertion:')
		sys.stdout.write('\n')
		if aeda.get_agent_error().is_anonymous():
			self.dump_agent_error(aeda.get_agent_error())
		else:
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(aeda.get_agent_error().get_name())
			sys.stdout.write('\n')
		sys.stdout.write((indent+2)*' ')
		sys.stdout.write('<=')
		sys.stdout.write(f'{aeda.get_error_threshold()}')
		sys.stdout.write('\n')
	def dump_intersection_assertion(self,indent:int,ia:IntersectionAssertion):
		name=f'{ia.get_name()}' if not ia.is_anonymous() else f''
		sys.stdout.write(indent*' ')
		sys.stdout.write('-IntersectionAssertion:')
		sys.stdout.write(f'{name}=')
		sys.stdout.write('\n')
		self.dump_traffic_detection_assertion(indent+2,ia.get_left_traffic_detection())
		sys.stdout.write((indent+2)*' ')
		sys.stdout.write('&')
		sys.stdout.write('\n')
		self.dump_red_light_state(indent+2,ia.get_red_light_state())
		sys.stdout.write((indent+2)*' ')
		sys.stdout.write('->')
		sys.stdout.write('\n')
		sys.stdout.write((indent+2)*' ')
		sys.stdout.write('~')
		sys.stdout.write('\n')
		self.dump_ego_speed(indent+2,ia.get_ego_speed())
		sys.stdout.write((indent+2)*' ')
		sys.stdout.write('U')
		sys.stdout.write('\n')
		self.dump_traffic_detection_assertion(indent+2,ia.get_right_traffic_detection())
		sys.stdout.write((indent+2)*' ')
		sys.stdout.write('&')
		sys.stdout.write('\n')
		self.dump_green_light_state(indent+2,ia.get_green_light_state())
	def dump_speed_violation(self,indent:int,sv:SpeedViolation):
		sys.stdout.write(indent*' ')
		sys.stdout.write('-SpeedViolation:')
		sys.stdout.write(str(sv))
		sys.stdout.write('\n')
	def dump_speed_limitation_checking(self,indent:int,slc:SpeedLimitationChecking):
		sys.stdout.write(indent*' ')
		sys.stdout.write('-SpeedLimitationChecking:')
		sys.stdout.write(str(slc))
		sys.stdout.write('\n')
	def dump_speed_constraint_assertion(self,indent:int,sca:SpeedConstraintAssertion):
		name=f'{sca.get_name()}' if not sca.is_anonymous() else f''
		sys.stdout.write(indent*' ')
		sys.stdout.write('-SpeedConstraintAssertion:')
		sys.stdout.write(f'{name}=')
		sys.stdout.write('\n')
		self.dump_traffic_detection_assertion(indent+2,sca.get_traffic_detection())
		sys.stdout.write((indent+2)*' ')
		sys.stdout.write('&')
		sys.stdout.write('\n')
		self.dump_speed_limitation_checking(indent+2,sca.get_speed_limitation_checking())
		sys.stdout.write((indent+2)*' ')
		sys.stdout.write('&')
		sys.stdout.write('\n')
		self.dump_speed_violation(indent+2,sca.get_left_speed_violation())
		sys.stdout.write((indent+2)*' ')
		sys.stdout.write('->')
		sys.stdout.write('F')
		sys.stdout.write('[0,')
		sys.stdout.write(str(sca.get_time_duration()))
		sys.stdout.write(']')
		sys.stdout.write('\n')
		sys.stdout.write((indent+2)*' ')
		sys.stdout.write('~')
		sys.stdout.write('\n')
		self.dump_speed_violation(indent+2,sca.get_right_speed_violation())
	def dump_detection_assertion(self,indent:int,da:DetectionAssertion):
		name=f'{da.get_name()}' if not da.is_anonymous() else f''
		sys.stdout.write(indent*' ')
		sys.stdout.write('-DetectionAssertion:')
		sys.stdout.write(f'{name}=')
		sys.stdout.write('\n')
		for i in da.get_assertions():
			if isinstance(i,AgentVisibleDetectionAssertion):
				self.dump_agent_visible_detection_assertion(indent+2,i)
			elif isinstance(i,AgentErrorDetectionAssertion):
				self.dump_agent_error_detection_assertion(indent+2,i)
			elif isinstance(i,TrafficDetectionAssertion):
				self.dump_traffic_detection_assertion(indent+2,i)
	def dump_safety_assertion(self,indent:int,sa:SafetyAssertion):
		name=f'{sa.get_name()}' if not sa.is_anonymous() else f''
		sys.stdout.write(indent*' ')
		sys.stdout.write('-SafetyAssertion:')
		sys.stdout.write(f'{name}=')
		sys.stdout.write('\n')
		for i in sa.get_assertions():
			if isinstance(i,AgentSafetyAssertion):
				self.dump_agent_safety_assertion(indent+2,i)
			elif isinstance(i,AgentVisibleDetectionAssertion):
				self.dump_agent_visible_detection_assertion(indent+2,i)
			elif isinstance(i,AgentErrorDetectionAssertion):
				self.dump_agent_error_detection_assertion(indent+2,i)
	def dump_assign_assertion_to_trace(self,indent:int,a:AssignAssertionToTrace):
		sys.stdout.write(indent*' ')
		sys.stdout.write('-AssignAssertionToTrace:')
		sys.stdout.write('\n')
		sys.stdout.write((indent+2)*' ')
		sys.stdout.write(f'-trace:{a.get_trace().get_name()}\n')
		assertion=a.get_assertion()
		if not assertion.is_anonymous():
			sys.stdout.write((indent+2)*' ')
			sys.stdout.write(f'-assertion:{assertion.get_name()}\n')
		elif isinstance(assertion,DetectionAssertion):
			self.dump_detection_assertion(indent+2,assertion)
		elif isinstance(assertion,SafetyAssertion):
			self.dump_safety_assertion(indent+2,assertion)
		elif isinstance(assertion,IntersectionAssertion):
			self.dump_intersection_assertion(indent+2,assertion)
		elif isinstance(assertion,SpeedConstraintAssertion):
			self.dump_speed_constraint_assertion(indent+2,assertion)
