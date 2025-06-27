/***************************AVScenarios.g4*************************************
 * 
 * This is the grammar coming from BNF rules written within antlr4.
 * Please see https://antlr.org for detail description about antlr4.
 * See detailed and clean description about the grammar:docs/scenest-grammar.md
 *
 *****************************************************************************/



// TODO:Under development.(2020.10.8)
// NOTICE: Due to that we want to generate python3 target, we must avoid parsing rules names
// same as the python3 keyword and antlr4 builtin variables, so we add a '_' 
// in every world conflict with python3 keyword,
// for example: map->map_,state->state_

grammar AVScenarios;

// start rule.
scenarios:assignment_statements EOF?    # entry
		 ;

string_expression: String 											#string_for_string_expression
				| string_expression '+' string_expression 			#string_expression_for_string_expression
				| identifier 										#string_id
				;

real_value_expression: real_value       														#real_value_of_real_value_expression
					| '(' real_value_expression ')'                       						#kuohao_of_real_value_expression  
					| real_value_expression '^' real_value_expression   						#cifang_of_real_value_expression              
					| real_value_expression op=('*'|'/') real_value_expression 					#Multi_of_real_value_expression
					| real_value_expression op=('+'|'-') real_value_expression 					#Plus_of_real_value_expression
					| identifier 																#real_value_expression_id
					;

coordinate_expression: coordinate 																#coordinate_of_coordinate_expression
					| '(' coordinate_expression ')'                       						#kuohao_of_coordinate_expression
					| coordinate_expression op=('*'|'/') coordinate_expression 					#Muti_of_coordinate_expression
					| coordinate_expression op=('+'|'-') coordinate_expression 					#Plus_of_coordinate_expression
					| identifier 																#coordinate_expression_id
					;

scenario:'CreateScenario' '{' map_parameter ';'
		   ego_parameter';'
		   npc_vehicles_parameter';'
		   pedestrians_parameter';'
		   obstacles_parameter';'
		   env_parameter';'
		   '}'                          #create_scenario
		   ;
npc_vehicles_parameter:identifier    #npc_var
					   |npc_vehicles     #npc_npc
					   |'{''}'           #npc_empty
					   ;
pedestrians_parameter:identifier     #pedestrians_var
					 |pedestrians       #pedestrians_ped
					 |'{''}'            #pedestrians_empty
					 ;
obstacles_parameter:identifier        #obstacles_var
				   |obstacles            #obstacles_obs
				   |'{''}'               #obstacles_empty
				   ;

map_parameter:'load''(' map_name')'       #map_load_name
			 ;
map_name:string_expression                        #map_name_str
		;
/* parameter_list_ego:describe the parameters explicitly
 * or all parameters are generated randomly.
 * */
ego_parameter:ego_vehicle               #ego_ego_vehicle
			 |identifier            #ego_ego_var
			 ;
ego_vehicle:'AV''('parameter_list_ego')' #ego_av
			;
/* first <state> is the initial state of the ego vehicle;
 * second <state> is the target state of the ego vehicle;
 * without <vehicle_type>, use the default one.
 * */
parameter_list_ego:state_parameter','state_parameter(','vehicle_type_parameter)? #par_list_ego_
				  ;
state_parameter:state_                 #state_state
				|identifier     #state_state_var
				;
state_:'('position_parameter')'                                         #state_position
	 | '('position_parameter','heading_parameter?(','speed_parameter)?')'   #state_position_heading_speed
	 ;
position:coordinate_frame? coordinate   #pos_coor_coor
			| coordinate_frame coordinate_expression #pos_coor_coor2
			| coordinate_frame? coordinate_expression 'range' '(' real_value_expression ',' real_value_expression ')' '&' '(' real_value_expression ',' real_value_expression ')' #pos_coor_range1
		;
/* IMU:vehicle coordinate system, right-forward-up, origin is the
 * position of the vehicle.
 * ENU:east-north-up, map origin is the origin of the coordinate;
 * WGS84:world geodetic system;
 * default coordinate frame:ENU.
 * */
coordinate_frame:'IMU'                     #coor_imu
				|'ENU'                     #coor_enu
				|'WGS84'                   #coor_wgs84
				;
position_parameter:position            #pos_pos
				  |identifier        #pos_pos_var
				  ;
speed_parameter:speed                  #speed_speed
			   |identifier            #speed_speed_var
			   ;
speed:real_value_expression                        							#speed_rv
		| 'range' '(' real_value_expression',' real_value_expression')' 	#speed_range_for_state
	 ;
real_value:op=('+'|'-')? non_negative_real_value     #rv
		  ;
non_negative_real_value:(float_value|number_value)    #non_negative_rv
					   ;
float_value:Non_negative_value                        #non_negative_float
		   ;
/// XXX: add extra 0 and 1 to avoid conflict lexer.
number_value:Non_negative_number                      #non_negative_number
			| '0'                                     #non_negative_conflict_0
			| '1'                                     #non_negative_conflict_1
			;
/* <laneID>-><real_value>:the distance of the point to the start point
 * of <laneID> is <real_value>.
 * */
coordinate:'('real_value_expression','real_value_expression(',' op=('+'|'-') real_value_expression)?')'      #coor_rv_rv
			| laneID_parameter'->'real_value_expression  							#coor_laneID_rv
			| laneID_parameter'->' 'range' '(' real_value_expression ',' real_value_expression ')' #coor_laneID_range
			;

laneID_parameter:identifier         #laneID_laneID_var
				|laneID                #laneID_laneID
				;
/* Lane is a string of such format:
 * "road_id.lane_id" or ".lane_id",
 * road_id and lane_id must be integers
 * for example: "1.5",".4"
 * */
laneID:string_expression                    #laneID_str
	  ;
heading_parameter:identifier          #head_var
				 |heading                #head_heading
				 ;
/* default value: the direction to the lane where the position is on.
 * */
heading:	real_value_expression unit('related to' direction)?     	#head_value
       	|real_value_expression 'pi' unit('related to' direction)?            #head_pi_value
	   	|'pi' unit ('related to' direction)?                 #head_only_pi_value

	   	|'range' '(' real_value_expression  ','real_value_expression ')' unit ('related to' direction)?     	#head_value_range
	   	|'range' '(' real_value_expression 'pi' ','real_value_expression 'pi' ')' unit('related to' direction)?            #head_pi_value_range
	   ;

unit:'deg'                                           #unit_deg
	|'rad'                                           #unit_rad
	;
direction:predefined_direction                       #direction_pre
		 ;
/* <identifier> must be a npc or a pedestrian and the ego,
 * note: In one scenario, the ego is unique.
 * */
predefined_direction:laneID_parameter'->'real_value_expression          #pre_lane
					 |'EGO'                          #pre_ego
					 |identifier					#pre_id
					 ;


vehicle_type_parameter:identifier            #vehicle_vehicle_type_var
				 |vehicle_type                            #vehicle_vehicle_type
				 ;
/* currently,we do not consider <material>.
 * */
vehicle_type:'('type_parameter')'                                     #vehicle_type_
			|'('type_parameter','color_parameter?/*(','material)?*/')'  #vehicle_type_color
			;
type_parameter:identifier    #type_var
			  |type_            #type_type_
			  ;
type_:specific_type        #type_specific
	 |general_type         #type_general
	 ;
specific_type:string_expression                     #specific_str
			 ;
/* model of the vehicle.
 * */
general_type:'car'    #general_car
			|'bus'    #general_bus
			|'Van'    #general_van
			|'truck'  #general_truck
			|'bicycle' #general_bicycle
			|'motorbicycle' #general_motorbicycle
			|'tricycle'     #general_tricycle
			;
color_parameter:identifier        #color_var
			   |color                #color_color
			   ;
color:color_list            #color_color_list
	 |rgb_color             #color_rgb_color
	 ;
color_list:'red'            #color_red
		  |'green'          #color_green
		  |'blue'           #color_blue
		  |'black'          #color_black
		  |'white'          #color_white
		  ;
/// rgb_color must be a value rgb value.
rgb_color:Rgb_color         #rgb_rgb
		 ;
npc_vehicles:'{'multi_npc_vehicles'}'       #npc
			;
multi_npc_vehicles:npc_vehicle_parameter     #multi_npc
				 |multi_npc_vehicles','npc_vehicle_parameter     #multi_multi_npc
				 ;
npc_vehicle:'Vehicle''('parameter_list_npc')'     #npc_vehicle_par
		   ;
npc_vehicle_parameter:npc_vehicle                   #npc_npc_vehicle
					 |identifier        #npc_npc_vehicle_var
					 ;
/* first <state> is the initial state of a vehicle;
 * second <state> is the target state of a vehicle;
 * default motion:uniform form motion along paths.
 * */
parameter_list_npc:state_parameter                                #par_npc_state
				   |state_parameter ','vehicle_motion_parameter   #par_npc_state_vehicle
				   |state_parameter','vehicle_motion_parameter?','state_parameter?(','vehicle_type_parameter)?  #par_npc_state_vehicle_state
				   ;
vehicle_motion_parameter:vehicle_motion                 #vehicle_vehicle_motion
						|identifier      #vehicle_vehicle_motion_var
						;
vehicle_motion:uniform_motion               #vehicle_motion_uniform
			  |waypoint_motion              #vehicle_motion_waypoint
			  ;
/* move with the given speed in <state>.
 * */
uniform_motion:uniform_index'('state_parameter')'        #uniform
			  ;
uniform_index:'uniform'      #uniform_uniform
			 |'Uniform'      #uniform_Uniform
			 ;
waypoint_motion:waypoint_index'('state_list_parameter')'      #waypoint
			   ;
state_list_parameter:identifier      #state_state_list_var
					|state_list         #state_state_list
					;
state_list:'('multi_states')' #state_list_multi
		  ;
multi_states:multi_states','state_parameter    #multi_states_par_state
			|state_parameter                   #multi_states_par
			;
waypoint_index:'Waypoint'   #waypoint_Waypoint
			  |'W'          #waypoint_W
			  |'WP'         #waypoint_WP
			  |'waypoint'   #waypoint_waypoint
			  |'w'          #waypoint_w
			  |'wp'         #waypoint_wp
			  ;
pedestrians:'{'multiple_pedestrians'}'   #pedestrians_multi
		   ;
multiple_pedestrians:pedestrian_parameter   #multi_pedestrian
					|multiple_pedestrians','pedestrian_parameter   #multi_multi_pedestrian
					;
pedestrian_parameter:pedestrian                 #pedestrian_pedestrian
					|identifier      #pedestrian_pedestrian_var
					;
pedestrian:'Pedestrian''('parameter_list_ped')'   #pedestrian_par
		  ;
/* default motion:uniform motion along the crosswalk with the same direction
 * of the nearest lane parallel with the crosswalk.
 * */
parameter_list_ped:state_parameter                                       #par_ped_state
				   |state_parameter','pedestrian_motion_parameter        #par_ped_state_ped
				   |state_parameter','pedestrian_motion_parameter?','state_parameter?(','pedestrian_type_parameter)?   #par_ped_state_ped_state
				   ;
pedestrian_motion_parameter:pedestrian_motion            #pedestrian_motion_pedestrian
						   |identifier                #pedestrian_motion_pedestrian_var
						   ;
pedestrian_motion:uniform_motion    #pedestrian_uniform
				 |waypoint_motion   #pedestrian_waypoint
				 ;
pedestrian_type_parameter:pedestrian_type             #pedestrian_pedestrian_type
						 |identifier  								#pedestrian_pedestrian_type_var
						 |String 			           			#pedestrian_type_name
						 ;
pedestrian_type:'('height_parameter','color_parameter')'    #pedestrian_type_height_color
				;

height_parameter:identifier  #height_var
				|height         #height_height
				;
height:real_value_expression                 #height_rv
	  ;
obstacles:'{'multiple_obstacles'}'      #obstacles_multi
		 ;
multiple_obstacles:obstacle_parameter                            #obstacles_obstacle
				  |multiple_obstacles','obstacle_parameter       #obstacles_multi_obstacle
				  ;
obstacle_parameter:obstacle                                      #obstacle_obstacle
				  |identifier                           #obstacle_obstacle_var
				  ;
obstacle:'Obstacle''('parameter_list_obs')'                      #obstacle_para
		;
parameter_list_obs:position_parameter(','shape_parameter)?       #par_position_shape
				  ;
shape_parameter:identifier                                 #shape_shape_var
				|shape                                           #shape_shape
				;
shape:sphere              #shape_sphere
	 |box                 #shape_box
	 |cone                #shape_cone
	 |cylinder            #shape_cylinder
	 ;
sphere:'(''sphere'','real_value_expression')'     #sphere_sphere
	  ;
box:'(''box'','real_value_expression','real_value_expression','real_value_expression')'  #box_box
   ;
cone:'(''cone'','real_value_expression','real_value_expression','real_value_expression')'  #cone_cone
	;
cylinder:'(''cylinder'','real_value_expression','real_value_expression','real_value_expression')'  #cylinder_cylinder
		;
env_parameter:identifier                              #env_var
			 |env                                         #env_env
			 // NOTICE:add a default empty environment.
			 |'{''}'                                      #env_empty
			 ;
env:'Environment''('parameter_list_env')'                 #env_par
   ;
parameter_list_env:time_parameter','weather_parameter               #par_time_weather
				  ;
weather_parameter:identifier            #weather_var
				 |weather                 #weather_wtr
				 ;
time_parameter:time                         #time_time
			  |identifier              #time_time_var
			  ;
time:Time                                  #time_Time
	;
weather:'{'multi_weathers'}'            #weathers
	   ;
multi_weathers:weather_statement_parameter                       #weathers_weather
			  |multi_weathers','weather_statement_parameter      #weathers_multi_weather
			  ;
weather_statement_parameter:identifier                #weather_weather_var
						   |weather_statement            #weather_weather
						   ;
weather_statement:kind':'weather_continuous_index_parameter       #weather_continuous
				 |kind':'weather_discrete_level_parameter        #weather_discrete
				 ;
kind:'sunny'                             #kind_sunny
	|'rain'                              #kind_rain
	|'snow'                              #kind_snow
	|'fog'                               #kind_fog
	|'wetness'                           #kind_wetness
	;
/// float_value must 0.0-0.9 or 1.0
weather_continuous_index_parameter:float_value                   #weather_continuous_value
								  |identifier                     #weather_continuous_var
								  ;
weather_discrete_level_parameter:weather_discrete_level                #weather_discrete_level_par
								|identifier                            #weather_discrete_var
								;
weather_discrete_level:'light'                 #weather_discrete_light
					  |'middle'                #weather_discrete_middle
					  |'heavy'                 #weather_discrete_heavy
					  ;
traffic:'{'traffic_statement'}'                          #traffic_traffic
	   ;
traffic_statement:intersection_traffic','lane_traffic     #traffic_stmt
				 ;
intersection_traffic:meta_intersection_traffic_parameter(','meta_intersection_traffic_parameter)* #intersection
					;
meta_intersection_traffic_parameter:identifier         #meta_intersection_meta_var
									|meta_intersection_traffic        #meta_intersection_meta
									;
meta_intersection_traffic:'Intersection''('intersection_ID_parameter','
						  ('0'|'1')','('0'|'1')','('0'|'1')')'   #meta_intersection_intersection
						 ;
intersection_ID_parameter:intersection_ID                #intersection_intersection
						 |identifier     #intersection_intersection_var
						 ;
intersection_ID:op=('+'|'-')? number_value              #intersection_signal
			   ;
lane_traffic:speed_limitation_parameter                  #lane_speed_limit
			|lane_traffic','speed_limitation_parameter   #lane_lane_speed_limit
			;
speed_limitation_parameter:speed_limitation        #speed_limit
						  |identifier           #speed_limit_var
						  ;
speed_limitation:'SpeedLimit''('laneID_parameter','speed_range_parameter')'  #speed_limit_speed_limit
				;
speed_range_parameter:identifier         #speed_range_var
					 |speed_range           #speed_range_speed
					 ;
speed_range:'('real_value_expression','real_value_expression')'   #speed_range_value
		   ;

// assertions.
/// the second identifier denotes the scenario.
trace_assignment:'Trace' identifier'=''EXE''('identifier')'          #trace_scenario
				;
trace_identifier:identifier									#trace_id
				;

//general assertions
compare_operator: '==' | '<' | '<=' | '>' | '>=' | '!='
				; 	
temporal_operator: 'G' | 'F'  | 'X' 
				| 'G''['a','b']'|'F''['a','b']'|'X' '['a','b']'
				; 
temporal_operator1:	'U' |                              
					'U''['a','b']' 
						;

a:real_value                        #a_rv
 ;
b:real_value                        #b_rv
 ;


atom_statement_overall: atom_statement                                        			#atom_statement_overall_atom_statement
				| '(' atom_statement_overall ')'										#atom_statement_overall_with_kuohao
				| atom_statement_overall arithmetic_operator atom_statement_overall    	#atom_statement_overall_combination
				| identifier                       										#atom_statement_id       
				;


atom_statement: distance_statement					#distance_statement_for_general_statement
				|perception_difference_statement 	#perception_difference_statement_for_general_statement
				|velocity_statement					#velocity_statement_for_general_statement
				|speed_statement					#speed_statement_for_general_statement
				|acceleration_statement 			#acceleration_statement_for_general_statement
				|real_value 						#real_value_for_general_statement
				|value_related_APIs 							#traffic_rule_value_related_APIs
				;


boolean_related_APIs: 'highBeamOn'			#traffic_rule_highBeamOn
						|'lowBeamOn'				#traffic_rule_lowBeamOn						
						|'fogLightOn'				#traffic_rule_fogLightOn
						|'hornOn'					#traffic_rule_hornOn
						|'warningFlashOn'			#traffic_rule_warningFlashOn
						|'engineOn'					#traffic_rule_engineOn		
						|'isLaneChanging'			#traffic_rule_isLaneChanging
						|'isOverTaking'			#traffic_rule_isOverTaking
						|'isTurningAround'		#traffic_rule_isTurningAround
						|'manualIntervention'	#traffic_rule_manualIntervention
						//road
						|'honkingAllowed'			#traffic_rule_honkingAllowed
						|'crosswalkAhead'	'('real_value_expression')'		#traffic_rule_crosswalkAhead
						|'junctionAhead' '('real_value_expression')'			#traffic_rule_junctionAhead
						|'stopSignAhead'	'('real_value_expression')'		#traffic_rule_stopSignAhead
						|'stoplineAhead''('real_value_expression')'			#traffic_rule_stoplineAhead
						|'streetLightOn'												#traffic_rule_streetLightOn
						//
						|'specialLocationAhead''('real_value_expression')' #traffic_rule_specialLocationAhead
						//
						|'trafficLightAhead.isBlinking'									#traffic_rule_trafficLightAhead_blink
						//traffic
						|'PriorityNPCAhead'		#traffic_rule_PriorityNPCAhead
						|'PriorityPedsAhead'		#traffic_rule_PriorityPedsAhead
						|'isTrafficJam'			#traffic_rule_isTrafficJam
						//NPCs
						|'NPCAhead''('real_value_expression')'				#traffic_rule_NPCAhead
						|'NearestNPC''('real_value_expression')'			#traffic_rule_NearestNPC
						|'NPCOpposite''('real_value_expression')'			#traffic_rule_NPCOpposite
						//Arrow
						|'trafficLightAhead.direction.isBlinking'				#traffic_rule_trafficLightAhead_arrow_blink
						//Time
						|'Time' compare_operator time_parameter 				#traffic_rule_Time
						;

value_related_APIs:	'turnSignal'			#traffic_rule_turnSignal
					|'gear'							#traffic_rule_gear
					|'direction'					#traffic_rule_direction
					|'speed'							#traffic_rule_speed
					|'acc'							#traffic_rule_acc
					|'brake'							#traffic_rule_brake
					//current lane
					|'currentLane.number'		#traffic_rule_currentlane_number
					|'currentLane.direction'	#traffic_rule_currentlane_direction
					//speed limit
					|'speedLimit.upperLimit'	#traffic_rule_speedLimit_upperLimit
					|'speedLimit.lowerLimit'	#traffic_rule_speedLimit_lowerLimit
					//
					|'specialLocationAhead.type' #traffic_rule_speedLimit_specialLocationAhead_type
					//
					|'trafficLightAhead.color'	#traffic_rule_trafficLightAhead_color
					//
					|'signalAhead'					#traffic_rule_signalAhead
					//NPCs
					|'NPCAhead.speed'				#traffic_rule_NPCAhead_speed
					|'NearestNPC.speed'			#traffic_rule_NearestNPC_speed
					|'NPCOpposite.speed'			#traffic_rule_NPCOpposite_speed
					//Arrow
					|'trafficLightAhead.direction.color'				#traffic_rule_trafficLightAhead_arrow_color
					//color values
					|'green'							#traffic_rule_green
					|'red'							#traffic_rule_red
					|'yellow'						#traffic_rule_yellow
					//directions
					|'off'							#traffic_rule_off
					|'forward'						#traffic_rule_forward
					|'left'							#traffic_rule_left
					|'right'							#traffic_rule_right
					//weather
					|'fog'							#traffic_rule_fog
					|'rain'							#traffic_rule_rain
					|'snow'							#traffic_rule_snow
					|'visibility'					#traffic_rule_visibility
					;

distance_statement: 'dis' '(' position_element ',' position_element ')'    
					;

position_element: ego_state             #ego_state_parameter_for_distance
				| agent_state       	 #agent_state_parameter_for_distance
				| agent_ground_truth	#agent_ground_truth_parameter_for_distance
				| position          	#position_parameter_for_general
				| identifier            #position_element_id
				;


ego_state_parameter:identifier		#ego_state_id
                   |ego_state		#ego_state_par
                   ;

ego_state:trace_identifier'[''ego'']'			#ego_state_for_general
		 ;
agent_state_parameter:identifier			#agent_state_id
                     |agent_state			#agent_state_par
                     ;
agent_state:trace_identifier'[''perception'']''['identifier']'		#agent_state_for_general
		   ;


agent_ground_truth_parameter:identifier		#agent_ground_truth_id
                            |agent_ground_truth	#agent_ground_truth_par
                            ;
/// identifier must be a npc vehicle,a pedestrian,or an obstacle
agent_ground_truth:trace_identifier'[' 'truth' ']''[' identifier ']'		#agent_ground_truth_for_general
				  ;



perception_difference_statement: 'diff' '(' agent_state_parameter ',' agent_ground_truth_parameter ')' 
							;


velocity_statement : 'vel' '('velocity_parameter_for_statement ',' velocity_parameter_for_statement ')'
					;

velocity_parameter_for_statement:  identifier              #velocity_element_id
									|ego_state 				  #velocity_element_ego_state
									| agent_state 			  #velocity_element_agent_state
									| agent_ground_truth      #velocity_element_agent_ground_truth
									| velocity 				  #velocity_element_velocity									
									;

velocity_parameter: identifier
					| velocity
					;
velocity:coordinate_expression		#velocity_value
		;


speed_statement: 'spd' '('speed_parameter_for_statement ',' speed_parameter_for_statement ')'
				;

speed_parameter_for_statement:  identifier 			#speed_element_id
									| ego_state 					#speed_element_ego_state
									| agent_state 			#speed_element_agent_state
									| agent_ground_truth 	#speed_element_agent_ground_truth
									| speed 				#speed_element_speed								
									;

acceleration_statement: 'acc' '(' acceleration_parameter_for_statement ',' acceleration_parameter_for_statement ')' 
						;


acceleration_parameter_for_statement: identifier        #acceleration_element_id 
									|ego_state 		#acceleration_element_ego_state
									| agent_state 		#acceleration_element_agent_state
									| agent_ground_truth 		#acceleration_element_agent_ground
									| acceleration 		#acceleration_element_acc								
									;



acceleration: coordinate_expression
			;


atom_statement_parameter:  atom_statement_overall 			#atom_statement_var
						;

atom_predicate: atom_statement_parameter compare_operator atom_statement_parameter  
				;

general_assertion: boolean_related_APIs 										#traffic_rule_boolean_related_APIs
					| atom_predicate 											#general_assertion0
					|'(' general_assertion ')'									#general_assertion0_0
					|'~' general_assertion 										#general_assertion1
					| temporal_operator general_assertion						#general_assertion2
					| general_assertion temporal_operator1 general_assertion  	#general_assertion3
					| general_assertion '&' general_assertion 					#general_assertion4
					| general_assertion '|' general_assertion 					#general_assertion5				
					| general_assertion '->' general_assertion 					#general_assertion6	
					| identifier 												#general_assertion_id											
					;



operator_related_assignments: string_expression
							| real_value_expression
							| coordinate_expression
							| atom_statement_overall
							;

// statements.
assignment_statements:(assignment_statement';')*          #assigns
					 ;
assignment_statement:identifier'='scenario             #assign_scenario
					/// this rule may refer to <Variable>::= '='<height>
					/// <Variable>::= '='<speed>
					/// <Variable>::= '='<weather_continuous_index>
					/// <Variable>::= '='<intersection_ID>.
					/// this rule may refer to <map_name>::= '='<string>
					/// <type_>::= '='<specific_type>
					/// <Variable>::= '='<laneID>

					|identifier'='ego_vehicle          #assign_ego
					/// this rule may refer to
					/// <state>::= '=''('<position>')'
					/// <vehicle_type>::= '='<type_>
					/// <state_list>::='('<state>')'
					|identifier'=''('identifier')'     #assign_variable
					|identifier '=''('identifier','identifier')'       #assign_name_two_variables
					/// this rule may refer to
					/// <state>::= '=''('<position>','<heading>','<speed>')'
					/// <state_list>::='('<state>','<state>','<state>')'
					|identifier'=''('identifier','identifier','identifier')'            #assign_name_three_variables
					|identifier'='state_								#assign_state
					|identifier'='vehicle_type						#assign_vehicle_type
					|identifier'='state_list				#assign_state_list
					|identifier'='pedestrian_type			#assign_pedestrian_type
					/// this rule may refer to
					/// <position>::= '='coordinate_frame?'('real_value_expression','real_value_expression')'
					/// <Variable>::= '='<speed_range>

					|identifier'='coordinate_frame coordinate_expression 							#assign_case_of_position
					|identifier'='coordinate_frame?'('real_value_expression','real_value_expression(','op=('+'|'-') real_value_expression)?')'       #assign_rv_rv


					|identifier'='coordinate_frame?laneID_parameter'->'real_value_expression      	#assign_lane_rv
					| identifier'='coordinate_frame?laneID_parameter'->''range' '(' real_value_expression ',' real_value_expression ')'      	#assign_lane_range

					|identifier'='coordinate_frame identifier  										#assign_special_case_of_coordinate


					|identifier'='heading                     #assign_heading
					|identifier'='general_type                #assign_general_type
					|identifier'='color                       #assign_color
					|identifier'='npc_vehicle                 #assign_npc
					/// the next two rules may refer to
					/// <Variable>::= '='<vehicle_motion>
					/// <Variable>::= '='<pedestrian_motion>
					|identifier'='uniform_motion         #assign_uniform_motion
					|identifier'='waypoint_motion        #assign_waypoint_motion
					|identifier'='state_list             #assign_state_list
					/// XXX: notice the next rule may refer to
					/// multiple <pedestrian>s
					/// multiple <npc_vehicle>s
					/// multiple <obstacle>s
					/// <weather>
					/// <traffic>
					/// therefore of many variable will not fall 
					/// into next five rules.
					|identifier'=''{'identifier(','identifier)*'}'   #assign_variables
					|identifier'='pedestrians                #assign_pedestrians
					|identifier'='npc_vehicles               #assign_npcs
					|identifier'='obstacles                  #assign_obstacles
					|identifier'='weather                    #assign_weather
					|identifier'='traffic                    #assign_traffic
					|identifier'='pedestrian                 #assign_ped
					|identifier'='obstacle                   #assign_obs
					|identifier'='shape                      #assign_shape
					|identifier'='env                        #assign_env
					|identifier'='time                       #assign_time
					|identifier'='weather_statement          #assign_weather_stmt
					|identifier'='weather_discrete_level     #assign_weather_discrete
					|identifier'='meta_intersection_traffic  #assign_intersection
					|identifier'='speed_limitation           #assign_speed_limit
					|trace_assignment                        #assign_trace


					/// The identifier may be the atom assertion
					|identifier'='distance_statement           #assign_distance_statement
					|identifier'='perception_difference_statement  #assignperception_difference_statement
					|identifier'='velocity_statement           #assign_velocity_statement
					|identifier'='speed_statement              #assign_speed_statement
					|identifier'='acceleration_statement       #assign_acceleration_statement
					//|identifier'='atom_statement_overall 	   #assign_atom_statement_overall
					|identifier'='operator_related_assignments               #assign_operator_related_assignments 

					/// The identifer may be parameters related to atom assertion 
					|identifier'='general_assertion              #assign_general_assertion_to_var
					|trace_identifier'|=' general_assertion		 #assign_general_assertion


					|identifier'='agent_ground_truth         #assign_agent_ground
					|identifier'='ego_state                  #assign_ego_state
					|identifier'='agent_state                #assign_agent_state
					|identifier'='speed							 #assign_speed
					//|identifier'='coordinate					 #assign_coordinate

					/// The general assertion

					|identifier'=' position #assign_position_range_extension					

					;




/// XXX: The following rule allows keywords as identifiers.
identifier:Variable_name
		  |'CreateScenario'|'load'|'AV'|'IMU'|'ENU'|'WGS84'
		  |'deg'|'rad'|'EGO'|'car'|'bus'|'Van'|'truck'|'pi'
		  |'bicycle'|'motorbicycle'|'tricycle'|'Vehicle'|'uniform'|'Uniform'
		  |'Waypoint'|'w'|'wp'|'W'|'WP'|'waypoint'|'Pedestrian'
		  |'Obstacle'|'Environment'|'Intersection'|'SpeedLimit'|'EXE'|'dis'|'diff'
		  |'truth'|'perception'|'traffic'|'norm'
		  ;




// lexer.


String:'"'Input_character+?'"'
	  ;

fragment Input_character:[a-zA-Z0-9]
						 |Symbol
						 ;
fragment Symbol :'`'|'~'|'!'|'@'|'#'|'$'|'%'|'^'|'&'|'*'|'('|')'
				|'_'|'-'|'+'|'='|'\\'|'|'|'['|']'|'{'|'}'|';'
				|':'|'\''|'"'|'/'|'?'|'<'|'>'|','|'.'|' '
				;

arithmetic_operator: '.*' | './' | '.+' | '.-' 
					;


Variable_name:[a-zA-Z_]([a-zA-Z0-9_])*
			 ;
Time:Hour':'Minute
	;
fragment Hour:[0-9]
			 |'1'[0-9]
			 |'2'[0-3]
			 ;
fragment Minute:[0-5][0-9]
			   ;
/// XXX:<Rgb_color> must match as many as whitespaces.
Rgb_color:'('' '*Rgb' '*','' '*Rgb' '*','' '*Rgb' '*')'
		 ;
fragment Rgb:Rgb1
			|Rgb2
			|Rgb3
			;
fragment Rgb1:[0-9]
			 ;
fragment Rgb2:[1-9][0-9]
			 ;
fragment Rgb3:'1'[0-9][0-9]
			  |'2'[0-4][0-9]
			  |'25'[0-5]
			  ;
Non_negative_value:Non_negative_number'.'Non_negative_number
				  ;
Non_negative_number:[0-9]+
				   ;


// skipping tokens.
WS:[ \t\n\r]+->skip
  ;


// comments.
LINE_COMMENT:'//'(~[\n])*->skip
			;
BLOCK_COMMENT:'/*'.*?'*/'->skip
			 ;
