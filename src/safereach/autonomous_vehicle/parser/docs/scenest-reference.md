# API references

|类|含义|成员或函数|
|---|---|---|
|``Map``|表示一个地图对象|``get_name()->AnyStr``:获得对象的名字<br />``get_map_name()->AnyStr``:获得地图的名字|
|``CoordinateFrame``|枚举值：表示位置的参考系|``CF_IMU,CF_ENU,CF_WGS84``|
|``Coordinate``|表示由``(x,y)``或``(x,y,z)``所表示的坐标|``get_x()->float``:获得坐标``x``的值<br />``get_y()->float``:获得坐标``y``的值<br />``has_z()->bool``:是否写明``z``的值<br />``get_z()->float``:获得坐标``z``的值|
|``Lane``|表示一个车道对象|``get_name()->AnyStr``:获得对象的名字<br />``get_lane_id()->str``:获得车道的标识|
|``LaneCoordinate``|表示形如``lane->distance``所表示的位置，即想对于车道的距离所表示的坐标|``get_lane()->Lane``:获得对应的``Lane``对象<br />``get_distance()->float``:获得对应的距离信息|
|``Position``|表示地图上的一个坐标|``get_name()->AnyStr``:获得对象的名字<br />``has_frame()->bool``判断是否是默认的``CoordinateFrame``对象，如果返回为``False``的话，则默认为``ENU``<br />``get_frame()->CoordinateFrame``:获得对应的``CoordinateFrame``对象，由于在语法上是可选参数，则调用之前需判断``has_frame()``，所有的可选参数都需如此判断，下面不再重复说明<br />``is_frame_ENU()->bool``:判断是否为``ENU``<br />``is_frame_IMU()->bool``:判断是否为``IMU``<br />``is_frame_WGS84()->bool``:判断是否为``WGS84``<br />``is_normal_coordinate()->bool``:判断是否拥有一个``Coordinate``对象<br />``is_relative_coordinate()->bool``:判断是否是一个``LaneCoordinate``对象<br />``get_coordinate()->Union[Coordinate,LaneCoordinate]``:获得对应的``Coordinate``或者``LaneCoordinate``对象|
|``Unit``|枚举值：表示角度为弧度或者普通角度|``U_DEG，U_RAD``|
|``PredefinedDirection``|表示形如``90 deg related to EGO``,``90 related to ".4"->34``或者``90 related to id``形式的方向|``is_default_ego()->bool``：判断是否是``EGO``常量<br />``get_lane_reference()->Tuple[Lane,float]``：假设是以车道为参考的话的话，获得对应的``Lane``对象和距离<br />``is_lane_reference(self)->bool``:是否是以车道为参考的方向<br />``get_reference(self)->Union[EgoVehicle,Pedestrian,NPCVehicle]``:如果是表示一某个*NPC*车辆，行人或者控制车辆所表示的方向的话，获得对应的对象|
|``Heading``|表示一个朝向|``get_name()->AnyStr``:获得对象的名字<br />``get_unit()->Unit``:获得``Unit``对象<br />``get_raw_heading_angle()->float``:获得角度的值<br />``is_heading_DEG()->bool``:判断是否为``deg``表示的角度<br />``is_heading_RAD()->bool``:判断是否为``rad``表示的角度<br />``has_direction()->bool``：表示是否写明方向<br />``get_direction() -> PredefinedDirection``:获得对应的``PredefinedDirection``对象|
|``Speed``|表示速度|``get_name()->AnyStr``:获得对象的名字<br />``get_speed_value()->float``:获得速度值|
|``State``|表示状态对象|``get_name()->AnyStr``:获得对象的名字<br />``has_heading()->bool``:表示是否写明朝向<br />``has_speed()->bool``:表示是否写明速度<br />``get_position()->Position``:获得``Position``对象<br />``get_speed()->Speed``:获得``Speed``对象<br />``get_heading()->Heading``：获得``Heading``对象|
|``Type``|是``GeneralType``和``SpecificType``对象的基类|``get_name()->AnyStr``:获得对象的名字|
|``SpecificType``|表示车辆具体的类型信息|``get_value()->AnyStr``:获得描述车辆的字符串信息|
|``GeneralTypeEnum``|表示车辆具体的类型信息的枚举值|``GT_CAR，GT_BUS，GT_VAN，GT_TRUCK，GT_BICYCLE，GT_MOTORBICYCLE，GT_TRICYCLE``|
|``GeneralType``|表示车辆的具体类型信息|	``get_kind()->GeneralTypeEnum``:获得对应的``GeneralTypeEnum``对象|
|``Material``|表述车辆材料信息|为空无意义，作为保留对象|
|``ColorListEnum``|表示预置颜色枚举值|``CL_RED，CL_GREEN，CL_BLUE，CL_BLACK，CL_WHITE``|
|``ColorList``|表示预置的颜色信息|``get_kind()->ColorListEnum``：获得对应的``ColorListEnum``对象|
|``RGBColor``|表示一个*RGB*值表示的颜色|``get_r()->int``:获得*R*值<br />``get_g()->int``:获得*G*值<br />``get_b()->int``:获得*B*值<br />``get_value()->Tuple[int,int,int]``:获得*RGB*值|
|``Color``|是``ColorList``和``RGBColor``对象的基类|``get_name()->AnyStr``:获得对象的名字|
|``VehicleType``|表示一个车辆的类型|``get_name()->AnyStr``:获得对象的名字<br />``has_color()->bool``:是否写明``Color``对象<br />``get_color()->Color``:获得``Color``对象<br />``get_type()->Type``:获得``Type``对象<br />``is_specific_type()->bool``:是否拥有一个``SpecificType``对象<br />``is_general_type()->bool``:是否拥有一个``GeneralType``对<br />``is_rgb_color()->bool``:是否拥有一个``RGBColor``对象<br />``is_color_list()->bool``:是否拥有一个``ColorList``对象|
|``Height``|表示高度|``get_name()->AnyStr``:获得对象的名字<br />``get_value()->float``:获得高度值|
|``PedestrianType``|表示行人类型信息|``get_height()->Height``:获得行人的``Height``信息<br />``get_color()->Color``:获得行人的``Color``信息<br />``is_rgb_color()->bool``:是否拥有一个``RGBColor``对象<br />``is_color_list()->bool``:是否拥有一个``ColorList``对象|
|``UniformIndex``|表示*uniform*规划路径的枚举值|``UI_uniform,UI_Uniform,UI_U,UI_u``|
|``UniformMotion``|表示*uniform*规划路径|``get_uniform_index()->UniformIndex``获得对应的枚举值<br />``get_state()->State``获得规划路径的``State``对象|
|``StateList``|表示``State``对象组成的列表|``get_name()->AnyStr``:获得对象的名字<br />``get_states()->List[State]``:获得包含的``State``对象列表<br />``get_size()->int``:表示``State``对象列表大小|
|``WaypointIndex``|表示*waypoint*规划路径的枚举值|``WI_Waypoint，WI_W，WI_WP，WI_waypoint，WI_w，WI_wp``|
|``WaypointMotion``|表示*waypoint*规划路径|``get_waypoint_index()->WaypointIndex``获得对应的枚举值<br />``get_state_list()->StateList``获得规划路径的``StateList``对象|
|``Motion``|包装类型，拥有一个``UniformMotion``或者``WaypointMotion``对象|``get_name()->AnyStr``:获得对象的名字<br />``is_uniform_motion()->bool``:是否是一个``UniformMotion``对象<br />``is_waypoint_motion()->bool``:是否是一个``WaypointMotion``对象<br />``get_motion()->Union[UniformMotion,WaypointMotion]``:获得对应的``UniformMotion``或者``WaypointMotion``对象|
|``VehicleMotion``|表示车辆的规划路径|同``Motion``|
|``PedestrianMotion``|表示行人的规划路径|同``Motion``|
|``Shape``|障碍物形状的基类||
|``Sphere``|球体障碍物|``get_name()->AnyStr``:获得对象的名字<br />``get_radius()->float``:得到半径|
|``Box``|立方体障碍物|``get_name()->AnyStr``:获得对象的名字<br />``get_length()->float``:得到长度<br />``get_width()->float``:得到宽度<br />``get_height)->float``:得到高度|
|``Cone``|圆锥障碍物|``get_name()->AnyStr``:获得对象的名字<br />``get_radius()->float``:得到半径<br />``get_height)->float``:得到高度|
|``Cylinder``|圆柱障碍物|``get_name()->AnyStr``:获得对象的名字<br />``get_radius()->float``:得到半径<br />``get_height)->float``:得到高度|
|``Time``|表示时间|``get_name()->AnyStr``:获得对象的名字<br />``get_hour()->float``:得到小时<br />``get_minute()->int:获得分钟值``|
|``WeatherKind``|表示天气种类的枚举值|``WK_SUNNY，WK_RAIN，WK_SNOW，WK_FOG，WK_WETNESS``|
|``WeatherDiscreteLevelEnum``|表示描述天气程度的枚举值|``WDL_LIGHT，WDL_MIDDLE，WDL_HEAVY``|
|``WeatherDiscreteLevel``|表示描述天气的程度|``get_name()->AnyStr``:获得对象的名字<br />``get_level()->WeatherDiscreteLevelEnum``:得到对应的程度|
|``WeatherContinuousIndex``|表示描述天气的值，介于0.0-1.0之间|``get_name()->AnyStr``:获得对象的名字<br />``get_index()->float``:获得值|
|``Weather``|描述单一的天气条件|``get_name()->AnyStr``:获得对象的名字<br />``get_weather_kind()->WeatherKind``:获得描述的天气类型<br />``is_weather_continuous_index()->bool``:判断天气是否为``WeatherContinuousIndex``所描述<br />``is_weather_discrete_level()->bool``:判断天气是否为``WeatherDiscreteLevel``所描述<br />``get_weather_kind_value()->Union[WeatherContinuousIndex,WeatherDiscreteLevel]``:获得对应的``WeatherContinuousIndex``或者``WeatherDiscreteLevel``对象|
|``Weathers``|包含多个``Weather``对象|``get_name()->AnyStr``:获得对象的名字<br />``get_weathers()->List[Weather]``:获得包含的``Weather``对象列表<br />``get_size()->int``:表示``Weather``对象列表大小|
|``EgoVehicle``|表示控制车辆对象|``get_name()->AnyStr``:获得对象的名字<br />``get_first_state()->State``:获得初始状态对象<br />``get_second_state()->State``:获得目标状态对象<br />``has_vehicle_type()->bool``:是否写明了车辆类型<br />``get_vehicle_type()->VehicleType``:获得车辆类型
|``Environment``|描述环境|``get_name()->AnyStr``:获得对象的名字<br />``get_time()->Time``:获得时间<br />``get_weathers(self)->Weathers``:获得天气|
|``NPCVehicle``|描述一辆*NPC*车辆|``get_name()->AnyStr``:获得对象的名字<br />``has_second_state()->bool``:是否写明目标状态<br />``has_vehicle_motion()->bool``:是否写明车辆规划路径<br />``has_vehicle_type()->bool``:是否写明车辆类型<br />``get_first_state()->State``:得到初始状态<br />``get_second_state()->State``:得到目标状态<br />``get_vehicle_motion()->VehicleMotion``:得到规划路径<br />``get_vehicle_type()->VehicleType``:得到车辆类型|
|``NPCVehicles``|包含多个``NPCVehicle``对象|``get_name()->AnyStr``:获得对象的名字<br />``get_npc_vehicles()->List[NPCVehicle]``:获得包含的``NPCVehicle``对象列表<br />``get_size()->int``:表示``NPCVehicle``对象列表大小|
|``Obstacle``|描述一个障碍物对象|``get_name()->AnyStr``:获得对象的名字<br />``has_shape()->bool``:是否写明形状<br />``get_position()->Position``:得到障碍物的位置<br />``get_shape()->Shape``:得到障碍物形状|
|``Obstacles``|包含多个``Obstacle``对象|``get_name()->AnyStr``:获得对象的名字<br />``get_obstacles()->List[Obstacle]``:获得包含的``Obstacle``对象列表<br />``get_size()->int``:表示``Obstacle``对象列表大小|
|``Pedestrian``|描述一位行人|``get_name()->AnyStr``:获得对象的名字<br />``has_second_state()->bool``:是否写明目标状态<br />``has_pedestrian_motion()->bool``:是否写明行人规划路径<br />``has_pedestrian_type()->bool``:是否写明行人类型<br />``get_first_state()->State``:得到初始状态<br />``get_second_state()->State``:得到目标状态<br />``get_pedestrian_motion()->PedestrianMotion``:得到规划路径<br />``get_pedestrian_type()->PedestrianType``:得到行人类型|
|``Pedestrians``|包含多个``Pedestrian``对象|``get_name()->AnyStr``:获得对象的名字<br />``get_pedestrians()->List[Pedestrian]``:获得包含的``Pedestrian``对象列表<br />``get_size()->int``:表示``Pedestrian``对象列表大小|
|``IntersectionID``|表示交互路口对象|``get_name()->AnyStr``:获得对象的名字<br />``get_value()->int``:获得ID|
|``IntersectionTraffic``|表示交互路口的交通|``get_name()->AnyStr``:获得对象的名字<br />``get_id()->IntersectionID``:获得描述的路口对象<br />``get_traffic_light()->int``:获得路口交通灯有无<br />``get_stop_sign()->int``:获得路口停止信号有无<br />``get_crosswalk()->int``:获得路口人行横道有无<br />|
|``SpeedRange``|表示速度范围|``get_name()->AnyStr``:获得对象的名字<br />``get_x()->float``:获得限速最小值<br />``get_y()->float``:获得限速最大值<br />``get_value()->Tuple[float,float]``:获得限速范围
|``SpeedLimitation``|表示某一车道限速范围|``get_name()->AnyStr``:获得对象的名字<br />``get_lane()->Lane``:获得对应车道对象<br />``get_speed_range()->SpeedRange``：获得对应限速信息对象|
|``Traffic``|表示交通对象|``get_name()->AnyStr``:获得对象的名字<br />``get_intersection_traffics()->List[IntersectionTraffic]``:获得所有的交互路口交通<br />``get_speed_limitations()->List[SpeedLimitation]``:获得所有的车道限速情况|
|``Scenario``|表示一个场景对象|``get_name()->AnyStr``:获得对象的名字<br />``has_pedestrians()->bool``:是否写明行人信息<br />``has_npc_vehicles()->bool``:是否写明*NPC*车辆信息<br />``has_obstacles()->bool``:是否写明障碍物信息<br />``has_environment()->bool``:是否写明环境信息<br />``has_traffic()->bool``:是否写明交通信息<br />``get_map()->Map``::获得地图对象<br />``get_ego_vehicle()->EgoVehicle``:获得控制车辆对象<br />``get_npc_vehicles()->NPCVehicles``:获得*NPC*车辆对象<br />``get_pedestrians()->Pedestrians``:获得行人对象<br />``get_obstacles()->Obstacles``:获得障碍物对象<br />``get_environment()->Environment``:获得环境对象<br />``get_traffic()->Traffic``:获得交通对象|
|``Trace``|表示一条规划路径|``get_name()->AnyStr``:获得对象的名字<br />``get_detection_assertions()->List[DetectionAssertion]``:获得该路径上所有的检测断言<br />``get_safety_assertions()->List[SafetyAssertion]``:获得该路径上所有的安全断言<br />``get_intersection_assertions()->List[IntersectionAssertion]``:获得该路径上所有的交通断言<br />``get_speed_constraint_assertions()->List[SpeedConstraintAssertion}``:获得该路径上所有的速度约束断言<br />``get_scenario()->Scenario``:获得对应的场景对象<br />``has_assertion()->bool``:该路径上是否有断言|
|``AgentState``|表示规划路径感知到的*agent*对象信息|``get_trace()->Trace``:获得对应的``Trace``对象<br />``get_name()->AnyStr``:获得对象的名字<br />``get_agent()->Union[Pedestrian,Obstacle,NPCVehicle]``:获得描述的*agent*对象，一个*agent*对象是一个行人，障碍物或者*NPC*车辆|
|``EgoState``|描述规划路径某控制车辆信息|``get_trace()->Trace``:获得对应的``Trace``对象<br />``get_name()->AnyStr``:获得对象的名字|
|``AgentGroundTruth``|表示规划路径的*agent*的实际信息|``get_name()->AnyStr``:获得对象的名字<br />``get_trace()->Trace``:获得对应的``Trace``对象<br />``get_agent()->Union[Pedestrian,Obstacle,NPCVehicle]``:获得描述的*agent*对象，一个*agent*对象是一个行人，障碍物或者*NPC*车辆|
|``AgentGroundDistance``|属于*agent*感知断言的前一部分|``get_name()->AnyStr``:获得对象的名字<br />``get_ego_state()->EgoState``:获得对应的``EgoState``对象<br />``get_agent_ground_truth()->AgentGroundTruth``:获得对应的``AgentGroundTruth``对象|
|``AgentVisibleDetectionAssertion``|*agent*感知断言对象|``get_agent_ground_distance()->AgentGroundDistance``:获得``AgentGroundDistance``对象<br >``get_sensing_range()->float``:获得感知距离|
|``AgentError``|属于*agent*误差断言的前一部分|``get_name()->AnyStr``:获得对象的名字<br />``get_agent_state()->AgentState``:获得对应的``AgentState``对象<br />``get_agent_ground_truth()->AgentGroundTruth``:获得对应的``AgentGroundTruth``|
|``AgentErrorDetectionAssertion``|*agent*误差断言对象|``get_agent_error()->AgentError``:获得对应的``AgentError``对象<br />``get_error_threshold() -> float``:获得误差阈值|
|``TrafficDetectionAssertion``|表示感知与实际的交通检测情况|``get_left_trace()``:获得表示感知交通的``Trace``对象<br />``get_right_trace()``:获得表示实际交通的``Trace``对象
|``EgoSpeed``|表示控制车辆速度对象|``get_velocity()->Coordinate``:获得对应的``Coordinate``对象|
|``RedLightState``|表示感知到了红灯|``get_trace()->Trace``：获得对应的时刻|
|``GreenLightState``|表示感知到了绿灯|``get_trace()->Trace``：获得对应的时刻|
|``AgentSafetyAssertion``|表示关于*agent*的安全断言对象|``get_agent_state()``：获得对应的``AgentState``对象<br />``get_ego_state()``:获得对应的``EgoState``对象<br />``get_safety_radius() -> float``:获得安全距离|
|``SpeedLimitationChecking``|表示速度检查（限速）对象|``get_trace()->Trace``:获得描述的规划路径时刻<br />``get_speed_range()->SpeedRange``:获得限速内容|
|``SpeedViolation``|表示速度违反对象|``get_trace()->Trace``:获得描述的规划路径时刻<br />``get_speed()->Speed``:获得速度|
|``SpeedConstraintAssertion``|表示速度约束对象|``get_name()->AnyStr``:获得对象的名字<br />``get_left_speed_violation()->SpeedViolation``:获得对应的第一个``SpeedViolation``对象<br />``get_traffic_detection()->TrafficDetectionAssertion``:获得对应的``TrafficDetectionAssertion``对象<br />``get_right_speed_violation()->SpeedViolation``:获得对应的第二个``SpeedViolation``对象<br />``get_speed_limitation_checking()->SpeedLimitationChecking``:获得对应的``SpeedLimitationChecking``对象<br />``get_time_duration()->float``:获得时间间隔|
|``IntersectionAssertion``|表示交通断言|``get_name()->AnyStr``:获得对象的名字<br />``get_ego_speed()->EgoSpeed``:获得对应的``EgoSpeed``对象<br />``get_left_traffic_detection()->TrafficDetectionAssertion``:获得对应的第一个``TrafficDetectionAssertion``对象<br />``get_right_traffic_detection()->TrafficDetectionAssertion``:获得对应的第二个``TrafficDetectionAssertion``对象<br />``get_red_light_state()->RedLightState``:获得对应的``RedLightState``对象<br />``get_green_light_state()->GreenLightState``:获得对应的``GreenLightState``对象|
|``DetectionAssertion``|拥有多个检测断言对象|``get_name()->AnyStr``:获得对象的名字<br />``get_size(self)->int``:获得断言数目		<br /> ``get_assertions()->List[AgentVisibleDetectionAssertion,AgentErrorDetectionAssertion,TrafficDetectionAssertion]``:获得所有的断言|
|``SafetyAssertion``|拥有多个``AgentSafetyAssertion，AgentVisibleDetectionAssertion,AgentErrorDetectionAssertion``对象|``get_name()->AnyStr``:获得对象的名字<br />``get_size(self)->int``:获得断言数目		<br /> ``get_assertions()->List[Union[AgentVisibleDetectionAssertion,AgentErrorDetectionAssertion,AgentSafetyAssertion]]``:获得所有的断言|
|``AST``|储存所有的信息结构包括操作函数|``get_ast_tree()->List[Any]``:获得解析好的所有的合法对象<br />``get_scenarios()->List[Scenario]``:获得所有的解析好的场景<br />``get_traces()->List[Trace]``:获得所有解析好的规划路径|
|``ASTDumper``|打印辅助类(有待完善)|``dump(ast:AST)``:将参数``AST``类中的信息打印|


|全局函数|作用|
|---|---|
|``Parse(file_name:AnyStr)->AST``|将文件中的代码解析并返回一个``AST``对象
