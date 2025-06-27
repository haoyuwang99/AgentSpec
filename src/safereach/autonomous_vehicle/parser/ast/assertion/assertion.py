# The file defines assertions needed to meet with the trace
from parser.ast.scenario.scenario import Scenario
from parser.ast.npc.npc_vehicles import NPCVehicle
from parser.ast.pedestrian.pedestrians import Pedestrian
from parser.ast.obstacle.obstacles import Obstacle
from parser.ast.base.state import Coordinate,Speed,Variable,NodeType,Node,CoordinateFrame, Position
from parser.ast.traffic.traffic import SpeedRange
from typing import Union,AnyStr,Optional,List
from parser.ast.unresolved.unresolved import *
## TODO: __str__ for pretty dumping?
class Trace:
    ...
class EgoState(Variable,Node):
    def __init__(self,trace:Trace,name:AnyStr=''):
        Variable.__init__(self,name)
        Node.__init__(self,NodeType.T_EGOSTATE)
        self._trace:Trace=trace
    def get_trace(self)-> Trace:
        return self._trace
    def __str__(self):
        return f'{self._trace.get_name()}[ego]'
class RedLightState:
    def __init__(self,trace:Trace):
        self._trace:Trace=trace
    def get_trace(self)->Trace:
        return self._trace
    def __str__(self):
        return f'{self._trace.get_name()}[traffic]==red'
class EgoSpeed:
    def __init__(self):
        self._velocity=None
    def set_velocity(self,coordinate:Coordinate):
        self._velocity=coordinate
    def get_velocity(self)->Coordinate:
        return self._velocity
    def __str__(self) -> str:
        return f'norm({self._velocity.get_x(),self._velocity.get_y()})'
class GreenLightState:
    def __init__(self,trace:Trace):
        self._trace:Trace=trace
    def get_trace(self)->Trace:
        return self._trace
    def __str__(self):
        return f'{self._trace.get_name()}[traffic]==green'
class AgentState(Variable,Node):
    def __init__(self,trace:Trace,name:AnyStr=''):
        Variable.__init__(self, name)
        Node.__init__(self, NodeType.T_AGENTSTATE)
        self._agent=None
        self._trace:Trace=trace
    def set_agent(self,agent:Union[Pedestrian,Obstacle,NPCVehicle]):
        self._agent=agent
    def get_agent(self)->Union[Pedestrian,Obstacle,NPCVehicle]:
        return self._agent
    def get_trace(self)->Trace:
        return self._trace
    def __str__(self) -> str:
        return f'{self._trace.get_name()}[perception][{self._agent.get_name()}]'
class AgentGroundTruth(Variable,Node):
    def __init__(self,trace:Trace,name:AnyStr=''):
        Variable.__init__(self, name)
        Node.__init__(self, NodeType.T_AGENTGROUNDTRUTH)
        self._agent=None
        self._trace: Trace = trace
    def set_agent(self,agent:Union[Pedestrian,Obstacle,NPCVehicle]):
        self._agent=agent
    def get_agent(self)->Union[Pedestrian,Obstacle,NPCVehicle]:
        return self._agent
    def get_trace(self)->Trace:
        return self._trace
    def __str__(self) -> str:
        return f'{self._trace.get_name()}[truth][{self._agent.get_name()}]'


class AgentGroundDistance(Variable,Node):
    def __init__(self,name:AnyStr=''):
        Variable.__init__(self,name)
        Node.__init__(self,NodeType.T_AGENTGROUNDDIS)
        self._ego_state=None
        self._agent_ground_truth=None
    def set_ego_state(self,ego_state:EgoState):
        self._ego_state=ego_state
    def set_agent_ground_truth(self,agent_ground_truth:AgentGroundTruth):
        self._agent_ground_truth=agent_ground_truth
    def get_ego_state(self)->EgoState:
        return self._ego_state
    def get_agent_ground_truth(self)->AgentGroundTruth:
        return self._agent_ground_truth
    def __str__(self) -> str:
        return f'dis({str(self._ego_state)},{str(self._agent_ground_truth)})'


class AgentError(Variable,Node):
    def __init__(self,name:AnyStr=''):
        Variable.__init__(self, name)
        Node.__init__(self, NodeType.T_AGENTERROR)
        self._agent_state = None
        self._agent_ground_truth = None

    def set_agent_state(self, agent_state: AgentState):
        self._agent_state = agent_state

    def set_agent_ground_truth(self, agent_ground_truth: AgentGroundTruth):
        self._agent_ground_truth = agent_ground_truth

    def get_agent_state(self)->AgentState:
        return self._agent_state

    def get_agent_ground_truth(self)->AgentGroundTruth:
        return self._agent_ground_truth
    def __str__(self) -> str:
        return f'diff({str(self._agent_state)},{str(self._agent_ground_truth)})'


class AgentSafetyAssertion:
    def __init__(self, safety_radius: float):
        self._safety_radius = safety_radius
        self._agent_state = None
        self._ego_state=None
    def set_agent_state(self, agent_state: AgentState):
        self._agent_state = agent_state
    def set_ego_state(self,ego_state:EgoState):
        self._ego_state=ego_state
    def get_agent_state(self)->AgentState:
        return self._agent_state
    def get_ego_state(self)->EgoState:
        return self._ego_state
    def get_safety_radius(self) -> float:
        return self._safety_radius
    def __str__(self):
        return f'dis({self._ego_state,self._agent_state})>={self._safety_radius}'


# trace[traffic]==trace[ground][traffic]
class TrafficDetectionAssertion:
    def __init__(self):
        super().__init__()
        self._left_trace=None
        self._right_trace=None
    def set_left_trace(self,trace:Trace):
        self._left_trace=trace
    def get_left_trace(self)->Trace:
        return self._left_trace
    def set_right_trace(self,trace:Trace):
        self._right_trace=trace
    def get_right_trace(self)->Trace:
        return self._right_trace
    def __str__(self) -> str:
        return f'{self._left_trace.get_name()}[perception][traffic]=={self._right_trace.get_name()}[truth][traffic]'


class IntersectionAssertion(Node,Variable):
    def __init__(self,name:AnyStr=''):
        Node.__init__(self,NodeType.T_INTERASSERT)
        Variable.__init__(self,name)
        self._left_traffic_detection=None
        self._right_traffic_detection=None
        self._red_light=None
        self._green_light=None
        self._ego_speed=None
    def set_ego_speed(self,ego_speed:EgoSpeed):
        self._ego_speed=ego_speed
    def get_ego_speed(self)->EgoSpeed:
        return self._ego_speed

    def set_left_traffic_detection(self,traffic_detection:TrafficDetectionAssertion):
        self._left_traffic_detection=traffic_detection

    def get_left_traffic_detection(self)->TrafficDetectionAssertion:
        return self._left_traffic_detection
    def set_right_traffic_detection(self,traffic_detection:TrafficDetectionAssertion):
        self._right_traffic_detection=traffic_detection

    def get_right_traffic_detection(self)->TrafficDetectionAssertion:
        return self._right_traffic_detection
    def set_red_light_state(self,red_light:RedLightState):
        self._red_light=red_light
    def get_red_light_state(self)->RedLightState:
        return self._red_light
    def set_green_light_state(self,green_light:GreenLightState):
        self._green_light=green_light
    def get_green_light_state(self)->GreenLightState:
        return self._green_light
    def __str__(self) -> str:
        return f'({str(self._left_traffic_detection)}&{str(self._red_light)})->(~{str(self._ego_speed)}U({str(self._right_traffic_detection)}&{str(self._green_light)}))'
class SpeedLimitationChecking:
    def __init__(self,trace:Trace):
        self._trace:Trace=trace
        self._speed_range=None
    def get_trace(self)->Trace:
        return self._trace
    def set_speed_range(self,speed_range:SpeedRange):
        self._speed_range=speed_range
    def get_speed_range(self)->SpeedRange:
        return self._speed_range
    def __str__(self) -> str:
        return f'{self._trace.get_name()}[traffic]=={self._speed_range.get_value()}'
class SpeedViolation:
    def __init__(self,trace:Trace,index0:bool):
        self._trace:Trace=trace
        self._speed=None
        self._index0=index0
    def get_trace(self)->Trace:
        return self._trace
    def set_speed(self,speed:Speed):
        self._speed=speed
    def get_speed(self)->Speed:
        return self._speed
    def isMinimumSpeedViolation(self)->bool:
        return self._index0
    def isMaximumSpeedViolation(self)->bool:
        return not self._index0
    def __str__(self) -> str:
        return f'{self._speed.get_speed_value()}<{self._trace.get_name()}[traffic][{0 if self._index0 else 1}]'

class SpeedConstraintAssertion(Node,Variable):
    def __init__(self,name:AnyStr=''):
        Node.__init__(self,NodeType.T_SPEEDCA)
        Variable.__init__(self,name)
        self._traffic_detection=None
        self._speed_limitation_checking=None
        self._left_speed_violation=None
        self._right_speed_violation=None
        self._time_duration:float=0
    def set_left_speed_violation(self,speed_violation:SpeedViolation):
        self._left_speed_violation=speed_violation
    def get_left_speed_violation(self)->SpeedViolation:
        return self._left_speed_violation
    def set_right_speed_violation(self,speed_violation:SpeedViolation):
        self._right_speed_violation=speed_violation
    def set_traffic_detection(self,traffic_detection:TrafficDetectionAssertion):
        self._traffic_detection=traffic_detection
    def get_traffic_detection(self)->TrafficDetectionAssertion:
        return self._traffic_detection
    def get_right_speed_violation(self)->SpeedViolation:
        return self._right_speed_violation
    def set_speed_limitation_checking(self,speed_limitation_checking:SpeedLimitationChecking):
        self._speed_limitation_checking=speed_limitation_checking
    def get_speed_limitation_checking(self)->SpeedLimitationChecking:
        return self._speed_limitation_checking
    def set_time_duration(self,duration:float):
        self._time_duration=duration
    def get_time_duration(self)->float:
        return self._time_duration
    def __str__(self) -> str:
        return f'({str(self._traffic_detection)}&{str(self._speed_limitation_checking)}&{str(self._left_speed_violation)}) \
            ->F[0,{self._time_duration}]~{str(self._right_speed_violation)}'

class AgentVisibleDetectionAssertion:
    def __init__(self, sensing_range: float):
        super().__init__()
        self._sensing_range=sensing_range
        self._agent_ground_distance=None
    def set_agent_ground_distance(self,agent_ground_distance:AgentGroundDistance):
        self._agent_ground_distance=agent_ground_distance
    def get_agent_ground_distance(self)->AgentGroundDistance:
        return self._agent_ground_distance
    def get_sensing_range(self)->float:
        return self._sensing_range
    def __str__(self) -> str:
        return f'{str(self._agent_ground_distance)}<={self._sensing_range}'
class AgentErrorDetectionAssertion:
    def __init__(self, error_threshold: float):
        super().__init__()
        self._error_threshold = error_threshold
        self._agent_error = None

    def set_agent_error(self, agent_error: AgentError):
        self._agent_error = agent_error

    def get_agent_error(self)->AgentError:
        return self._agent_error

    def get_error_threshold(self) -> float:
        return self._error_threshold
    def __str__(self) -> str:
        return f'{str(self._agent_error)}<={self._error_threshold}'
class DetectionAssertion(Node,Variable):
    def __init__(self,name:AnyStr=''):
        Variable.__init__(self,name)
        Node.__init__(self,NodeType.T_DETECTIONS)
        self._assertions:List[Union[AgentVisibleDetectionAssertion,AgentErrorDetectionAssertion,TrafficDetectionAssertion]]=[]
    def add_assertion(self,detection:Union[AgentVisibleDetectionAssertion,AgentErrorDetectionAssertion,TrafficDetectionAssertion]):
        self._assertions.append(detection)
    def get_size(self):
        return len(self._assertions)
    def get_assertions(self)->List[Union[AgentVisibleDetectionAssertion,AgentErrorDetectionAssertion,TrafficDetectionAssertion]]:
        return self._assertions
    def __str__(self) -> str:
        pass
class SafetyAssertion(Variable,Node):
    def __init__(self,name:AnyStr=''):
        Variable.__init__(self,name)
        Node.__init__(self,NodeType.T_SAFETYS)
        self._assertions:List[Union[AgentVisibleDetectionAssertion,AgentErrorDetectionAssertion,AgentSafetyAssertion]]=[]
    def add_assertion(self,assertion:Union[AgentVisibleDetectionAssertion,AgentErrorDetectionAssertion,AgentSafetyAssertion]):
        self._assertions.append(assertion)
    def get_size(self)->int:
        return len(self._assertions)
    def get_assertions(self)->List[Union[AgentVisibleDetectionAssertion,AgentErrorDetectionAssertion,AgentSafetyAssertion]]:
        return self._assertions
    def __str__(self) -> str:
        pass





#########################################

class Traffic_Rule_Related_APIs(Variable,Node):
    def __init__(self,name:AnyStr=''):
        Variable.__init__(self,name)
        Node.__init__(self,NodeType.T_GeneralDistanceStatement)
        self.API = None
        self.API_value = '1'
        self.API_operator = '=='

    def set_API(self, API):
        self.API = API

    def set_API_value(self, API_value):
        self.API_value = API_value

    def set_API_operator(self, API_operator):
        self.API_operator = API_operator

    def get_API(self):
        return self.API

    def get_API_value(self):
        return self.API_value

    def get_API_operator(self):
        return self.API_operator

    def __str__(self) -> str:
        return f'{self.API}'


# The general distance statement
class GeneralDistanceStatement(Variable,Node):
    def __init__(self,name:AnyStr=''):
        Variable.__init__(self,name)
        Node.__init__(self,NodeType.T_GeneralDistanceStatement)
        self._position_element_left=None
        self._position_element_right=None
        self._frame_left = ""
        self._frame_right = ""
    def set_position_element_left(self,left:Union[EgoState,AgentState,AgentGroundTruth,Position,NameWithTwoRealValues]):
        self._position_element_left=left
        if isinstance(left, Position):
            if left.has_frame():
                if left.is_frame_IMU():
                    self._frame_left = "IMU"
                elif left.is_frame_WGS84():
                    self._frame_left = "WGS84"
    def set_position_element_right(self,right:Union[EgoState,AgentState,AgentGroundTruth,Position,NameWithTwoRealValues]):
        self._position_element_right=right
        if isinstance(right, Position):
            if right.has_frame():
                if right.is_frame_IMU():
                    self._frame_right = "IMU"
                elif right.is_frame_WGS84():
                    self._frame_right = "WGS84"
    def get_position_element_left(self)->Union[EgoState,AgentState,AgentGroundTruth,Position,NameWithTwoRealValues]:
        return self._position_element_left
    def get_position_element_right(self)->Union[EgoState,AgentState,AgentGroundTruth,Position,NameWithTwoRealValues]:
        return self._position_element_right
    def __str__(self) -> str:
        return f'dis({self._frame_left + str(self._position_element_left)},{self._frame_right+str(self._position_element_right)})'


class PerceptionDifferenceStatement(Variable,Node):
    def __init__(self,name:AnyStr=''):
        Variable.__init__(self,name)
        Node.__init__(self,NodeType.T_PerceptionDifferenceStatement)
        self._agent_state = None
        self._agent_ground_truth = None
    def set_agent_state(self, agent_state: AgentState):
        self._agent_state = agent_state
    def set_agent_ground_truth(self, agent_ground_truth: AgentGroundTruth):
        self._agent_ground_truth = agent_ground_truth
    def get_agent_state(self)->AgentState:
        return self._agent_state
    def get_agent_ground_truth(self)->AgentGroundTruth:
        return self._agent_ground_truth
    def __str__(self) -> str:
        return f'diff({str(self._agent_state)},{str(self._agent_ground_truth)})'


class VelocityStatement(Variable,Node):
    def __init__(self,name:AnyStr=''):
        Variable.__init__(self,name)
        Node.__init__(self,NodeType.T_velocity_statement)
        self._velocity_element_left=None
        self._velocity_element_right=None
    def set_velocity_element_left(self,left:Union[EgoState,AgentState,AgentGroundTruth,Coordinate,NameWithTwoRealValues,Position]):
        self._velocity_element_left=left
    def set_velocity_element_right(self,right:Union[EgoState,AgentState,AgentGroundTruth,Coordinate,NameWithTwoRealValues,Position]):
        self._velocity_element_right=right
    def get_velocity_element_left(self)->Union[EgoState,AgentState,AgentGroundTruth,Coordinate,NameWithTwoRealValues,Position]:
        if isinstance(self._velocity_element_left, Position):
            return self._velocity_element_left.get_coordinate()
        else:
            return self._velocity_element_left
        # return self._velocity_element_left
    def get_velocity_element_right(self)->Union[EgoState,AgentState,AgentGroundTruth,Coordinate,NameWithTwoRealValues,Position]:
        if isinstance(self._velocity_element_right, Position):
            return self._velocity_element_right.get_coordinate()
        else:
            return self._velocity_element_right
        # return self._velocity_element_right
    def __str__(self) -> str:
        return f'vel({str(self._velocity_element_left)},{str(self._velocity_element_right)})'


class SpeedStatement(Variable,Node):
    def __init__(self,name:AnyStr=''):
        Variable.__init__(self,name)
        Node.__init__(self,NodeType.T_SpeedStatement)
        self._speed_element_left=None
        self._speed_element_right=None
    def set_speed_element_left(self,left:Union[EgoState,AgentState,AgentGroundTruth,Speed,NameWithRealValue]):
        self._speed_element_left=left
    def set_speed_element_right(self,right:Union[EgoState,AgentState,AgentGroundTruth,Speed,NameWithRealValue]):
        self._speed_element_right=right
    def get_speed_element_left(self)->Union[EgoState,AgentState,AgentGroundTruth,Speed,NameWithRealValue]:
        return self._speed_element_left
    def get_speed_element_right(self)->Union[EgoState,AgentState,AgentGroundTruth,Speed,NameWithRealValue]:
        return self._speed_element_right
    def __str__(self) -> str:
        return f'spd({str(self._speed_element_left)},{str(self._speed_element_right)})'


class AccelerationStatement(Variable,Node):
    def __init__(self,name:AnyStr=''):
        Variable.__init__(self,name)
        Node.__init__(self,NodeType.T_AccelerationStatement)
        self._acceleration_element_left=None
        self._acceleration_element_right=None

    def set_acceleration_element_left(self,left:Union[EgoState,AgentState,AgentGroundTruth,Coordinate,NameWithTwoRealValues,Position]):
        self._acceleration_element_left=left

    def set_acceleration_element_right(self,right:Union[EgoState,AgentState,AgentGroundTruth,Coordinate,NameWithTwoRealValues,Position]):
        self._acceleration_element_right=right

    def get_acceleration_element_left(self)->Union[EgoState,AgentState,AgentGroundTruth,Coordinate,NameWithTwoRealValues,Position]:
        if isinstance(self._acceleration_element_left, Position):
            return self._acceleration_element_left.get_coordinate()
        else:
            return self._acceleration_element_left
        # return self._acceleration_element_left

    def get_acceleration_element_right(self)->Union[EgoState,AgentState,AgentGroundTruth,Coordinate,NameWithTwoRealValues,Position]:
        if isinstance(self._acceleration_element_right, Position):
            return self._acceleration_element_right.get_coordinate()
        else:
            return self._acceleration_element_right
        # return self._acceleration_element_right

    def __str__(self) -> str:
        return f'acc({str(self._acceleration_element_left)},{str(self._acceleration_element_right)})'


class OverallStatement(Variable,Node):
    def __init__(self,name:AnyStr=''):
        Variable.__init__(self,name)
        Node.__init__(self,NodeType.T_OverallStatement)
        self._statements=[]#:List[Union[GeneralDistanceStatement,PerceptionDifferenceStatement,VelocityStatement,SpeedStatement,AccelerationStatement,float,int,OverallStatement]]=[]
        self._operators=[]
    def add_statement(self,statement):#Union[GeneralDistanceStatement,PerceptionDifferenceStatement,VelocityStatement,SpeedStatement,AccelerationStatement,float,int,OverallStatement]):
        self._statements.append(statement)
    def add_operator(self,operator):
        self._operators.append(operator)
    def get_statements(self):#-> List[Union[GeneralDistanceStatement,PerceptionDifferenceStatement,VelocityStatement,SpeedStatement,AccelerationStatement,float,int,OverallStatement]]:
        return self._statements
    def get_operators(self):
        return self._operators
    def get_size_of_statements(self)->int:
        return len(self._statements)
    def get_size_of_operators(self)->int:
        return len(self._operators)
    def __str__(self) -> str:
        if len(self._statements)> 0:
            returnstr = '('+str(self._statements[0])
            for _i in range(len(self._operators)):
                returnstr = returnstr + str(self._operators[_i])+str(self._statements[_i+1])
            returnstr = returnstr + ')'
            return returnstr

# class PositionDistanceStatement(Variable,Node):
#     def __init__(self,name:AnyStr=''):
#         Variable.__init__(self, name)
#         Node.__init__(self, NodeType.T_PositionDistance)
#         self._state = None
#         self._position = None
#     def set_state(self, state: Union[AgentState,EgoState]):
#         self._state = state
#     def set_position(self, positiona):
#         self._position = positiona
#     def get_state(self)->Union[AgentState,EgoState]:
#         return self._state
#     def get_position(self):
#         return self._position
#     def __str__(self) -> str:
#         return f'dis({str(self._state)},{str(self._position)})'


###general_assertion0
class AtomPredicate():         
    def __init__(self):
        super().__init__()
        self._atom_statement_left = None
        self._compare_operator = None
        self._atom_statement_right = None
    def set_atom_statement_left(self, statement):
        self._atom_statement_left = statement
    def set_compare_operator(self, statement):
        self._compare_operator = statement
    def set_atom_statement_right(self, statement):
        self._atom_statement_right = statement

    def get_atom_statement_left(self):#->List[Union[GeneralAssertionComponent,]]:
        return self._atom_statement_left
    def get_compare_operator(self):
        return self._compare_operator
    def get_atom_statement_right(self):#->List[Union[GeneralAssertionComponent,]]:
        return self._atom_statement_right
    def __str__(self) -> str:
        return f'{str(self._atom_statement_left)}{str(self._compare_operator)}{str(self._atom_statement_right)}'

class KuoHaoWithGeneral():         
    def __init__(self):
        super().__init__()
        self._left_kuohao = '('
        self._gneral_assertion = None
        self._right_kuohao = ')'
    def set_gneral_assertion(self, statement):
        self._gneral_assertion = statement
    # def get_not_symbol(self):#->List[Union[GeneralAssertionComponent,]]:
    #     return self._not_symbol
    def get_assertion(self):
        return self._gneral_assertion
    def __str__(self) -> str:
        return f'{str(self._left_kuohao)}{str(self._gneral_assertion)}{str(self._right_kuohao)}'

###general_assertion1
class NotWithGeneral():         
    def __init__(self):
        super().__init__()
        self._not_symbol = '~'
        self._gneral_assertion = None
    def set_gneral_assertion(self, statement):
        self._gneral_assertion = statement

    def get_not_symbol(self):#->List[Union[GeneralAssertionComponent,]]:
        return self._not_symbol
    def get_assertion(self):
        return self._gneral_assertion
    def __str__(self) -> str:
        return f'({str(self._not_symbol)}{str(self._gneral_assertion)})'

###general_assertion2
class GeneralAssertionWithTemporalOperator():
    def __init__(self):
        super().__init__()
        self._temporal_operator = None
        self._statement = None
    def set_assertion(self, statement):
        self._statement = statement
    def set_temporal_operator(self, operator):
        self._temporal_operator = operator

    def get_assertion(self):#->List[Union[GeneralAssertionComponent,]]:
        return self._statement
    def get_temporal_operator(self):
        return self._temporal_operator
    # def get_assertion(self):
    #   return f'{str(self._temporal_operator)}[{str(self._statement)}]'
    def __str__(self) -> str:
        return f'({str(self._temporal_operator)} {str(self._statement)})'

###general_assertion3
class GeneralAssertionWithUnitl():
    def __init__(self):
        super().__init__()
        self._statement_left =None
        self._temporal_operator = None
        self._statement_right = None
    def set_general_assertion_left(self, statement):
        self._statement_left = statement
    def set_general_assertion_right(self, statement):
        self._statement_right = statement
    def set_temporal_operator(self, operator):
        self._temporal_operator = operator

    def get_general_assertion_left(self):#->List[Union[GeneralAssertionComponent,]]:
        return self._statement_left
    def get_general_assertion_right(self):#->List[Union[GeneralAssertionComponent,]]:
        return self._statement_right
    def get_temporal_operator(self):
        return self._temporal_operator
    # def get_assertion(self):
    #   return f'{str(self._temporal_operator)}[{str(self._statement)}]'
    def __str__(self) -> str:
        return f'({str(self._statement_left)} {str(self._temporal_operator)} {str(self._statement_right)})'

###general_assertion4
class AndWithGeneral():        
    def __init__(self):
        super().__init__()
        self._general_assertion_left = None
        self._and_symbol = '&'
        self._general_assertion_right = None
    def set_general_assertion_left(self, statement):
        self._general_assertion_left = statement
    def set_general_assertion_right(self, statement):
        self._general_assertion_right = statement

    def get_general_assertion_left(self):#->List[Union[GeneralAssertionComponent,]]:
        return self._general_assertion_left
    def get_general_assertion_right(self):
        return self._general_assertion_right
    def get_and_symbol(self):
        return self._and_symbol
    def __str__(self) -> str:
        return f'({str(self._general_assertion_left)} {str(self._and_symbol)} {str(self._general_assertion_right)})'

###general_assertion5
class OrWithGeneral():        
    def __init__(self):
        super().__init__()
        self._general_assertion_left = None
        self._and_symbol = '|'
        self._general_assertion_right = None
    def set_general_assertion_left(self, statement):
        self._general_assertion_left = statement
    def set_general_assertion_right(self, statement):
        self._general_assertion_right = statement

    def get_general_assertion_left(self):#->List[Union[GeneralAssertionComponent,]]:
        return self._general_assertion_left
    def get_general_assertion_right(self):
        return self._general_assertion_right
    def get_and_symbol(self):
        return self._and_symbol
    def __str__(self) -> str:
        return f'({str(self._general_assertion_left)} {str(self._and_symbol)} {str(self._general_assertion_right)})'



###general_assertion6   
class DeriveWithGeneral():        
    def __init__(self):
        super().__init__()
        self._general_assertion_left = None
        self._derive_symbol = '->'
        self._general_assertion_right = None
    def set_general_assertion_left(self, statement):
        self._general_assertion_left = statement
    def set_general_assertion_right(self, statement):
        self._general_assertion_right = statement

    def get_general_assertion_left(self):
        return self._general_assertion_left
    def get_general_assertion_right(self):
        return self._general_assertion_right
    def get_and_symbol(self):
        return self._derive_symbol
    def __str__(self) -> str:
        return f'({str(self._general_assertion_left)} {str(self._derive_symbol)} {str(self._general_assertion_right)})'



class SingleGeneralAssertion(Variable,Node):
    def __init__(self,name:AnyStr=''):
        Variable.__init__(self, name)
        Node.__init__(self, NodeType.T_SINGLEGENERAL)
        self._assertion:Union[AtomPredicate,NotWithGeneral]=None
    def add_assertion(self,assertion:Union[AtomPredicate,NotWithGeneral,AndWithGeneral,OrWithGeneral,GeneralAssertionWithTemporalOperator,DeriveWithGeneral,GeneralAssertionWithUnitl]):
        self._assertion=assertion
    # def get_size(self)->int:
    #   return len(self._assertions)
    def get_assertion(self)->Union[AtomPredicate,NotWithGeneral,AndWithGeneral,OrWithGeneral,GeneralAssertionWithTemporalOperator,DeriveWithGeneral,GeneralAssertionWithUnitl]:
        return self._assertion
    def __str__(self) -> str:
        return str(self._assertion)


class Trace(Node,Variable):
    def __init__(self,name:AnyStr,scenario:Scenario):
        Node.__init__(self,NodeType.T_TRACE)
        Variable.__init__(self,name)
        self._scenario=scenario
        self._detection_assertions:List[DetectionAssertion]=[]
        self._safety_assertions:List[SafetyAssertion]=[]
        self._intersection_assertions:List[IntersectionAssertion]=[]
        self._speed_constraint_assertions:List[SpeedConstraintAssertion]=[]

        self._general_assertions:List[SingleGeneralAssertion]=[]

    def add_general_assertion(self,general_assertion:SingleGeneralAssertion):
        self._general_assertions.append(general_assertion)
    def get_general_assertions(self)->List[SingleGeneralAssertion]:
        return self._general_assertions

    def add_detection_assertion(self,detection_assertion:DetectionAssertion):
        self._detection_assertions.append(detection_assertion)
    def add_safety_assertion(self,safety_assertion:SafetyAssertion):
        self._safety_assertions.append(safety_assertion)
    def add_intersection_assertion(self,intersection_assertion:IntersectionAssertion):
        self._intersection_assertions.append(intersection_assertion)
    def add_speed_constraint_assertion(self,speed_constraint_assertion:SpeedConstraintAssertion):
        self._speed_constraint_assertions.append(speed_constraint_assertion)
    def get_detection_assertions(self)->List[DetectionAssertion]:
        return self._detection_assertions
    def get_safety_assertions(self)->List[SafetyAssertion]:
        return self._safety_assertions
    def get_intersection_assertions(self)->List[IntersectionAssertion]:
        return self._intersection_assertions
    def get_speed_constraint_assertions(self)->List[SpeedConstraintAssertion]:
        return self._speed_constraint_assertions
    def get_scenario(self)->Scenario:
        return self._scenario
    def has_assertion(self)->bool:
        if len(self._detection_assertions)!=0 or len(self._safety_assertions)!=0 \
            or len(self._intersection_assertions)!=0 or len(self._speed_constraint_assertions)!=0\
            or len(self._general_assertions)!=0:
            return True
        return False
    def __str__(self) -> str:
        pass
class AssignAssertionToTrace(Node,Variable):
    def __init__(self):
        # Empty Name
        Variable.__init__(self)
        Node.__init__(self,NodeType.T_AASSERTIONTRACE)
        self._trace=None
        self._assertion=None
    def set_trace(self,t:Trace):
        self._trace=t
    def set_assertion(self,assertion:Union[DetectionAssertion,SafetyAssertion,IntersectionAssertion,SpeedConstraintAssertion,SingleGeneralAssertion]):
        self._assertion=assertion
    def get_trace(self)->Trace:
        return self._trace
    def get_assertion(self)->Union[DetectionAssertion,SafetyAssertion,IntersectionAssertion,SpeedConstraintAssertion]:
        return self._assertion
    def __str__(self) -> str:
        pass
