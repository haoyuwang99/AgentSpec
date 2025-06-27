// Generated from /home/sunsun/Desktop/UserIntercation/Lawbreak/parser/grammar/AVScenarios.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link AVScenariosParser}.
 */
public interface AVScenariosListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by the {@code entry}
	 * labeled alternative in {@link AVScenariosParser#scenarios}.
	 * @param ctx the parse tree
	 */
	void enterEntry(AVScenariosParser.EntryContext ctx);
	/**
	 * Exit a parse tree produced by the {@code entry}
	 * labeled alternative in {@link AVScenariosParser#scenarios}.
	 * @param ctx the parse tree
	 */
	void exitEntry(AVScenariosParser.EntryContext ctx);
	/**
	 * Enter a parse tree produced by the {@code string_expression_for_string_expression}
	 * labeled alternative in {@link AVScenariosParser#string_expression}.
	 * @param ctx the parse tree
	 */
	void enterString_expression_for_string_expression(AVScenariosParser.String_expression_for_string_expressionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code string_expression_for_string_expression}
	 * labeled alternative in {@link AVScenariosParser#string_expression}.
	 * @param ctx the parse tree
	 */
	void exitString_expression_for_string_expression(AVScenariosParser.String_expression_for_string_expressionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code string_id}
	 * labeled alternative in {@link AVScenariosParser#string_expression}.
	 * @param ctx the parse tree
	 */
	void enterString_id(AVScenariosParser.String_idContext ctx);
	/**
	 * Exit a parse tree produced by the {@code string_id}
	 * labeled alternative in {@link AVScenariosParser#string_expression}.
	 * @param ctx the parse tree
	 */
	void exitString_id(AVScenariosParser.String_idContext ctx);
	/**
	 * Enter a parse tree produced by the {@code string_for_string_expression}
	 * labeled alternative in {@link AVScenariosParser#string_expression}.
	 * @param ctx the parse tree
	 */
	void enterString_for_string_expression(AVScenariosParser.String_for_string_expressionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code string_for_string_expression}
	 * labeled alternative in {@link AVScenariosParser#string_expression}.
	 * @param ctx the parse tree
	 */
	void exitString_for_string_expression(AVScenariosParser.String_for_string_expressionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code real_value_expression_id}
	 * labeled alternative in {@link AVScenariosParser#real_value_expression}.
	 * @param ctx the parse tree
	 */
	void enterReal_value_expression_id(AVScenariosParser.Real_value_expression_idContext ctx);
	/**
	 * Exit a parse tree produced by the {@code real_value_expression_id}
	 * labeled alternative in {@link AVScenariosParser#real_value_expression}.
	 * @param ctx the parse tree
	 */
	void exitReal_value_expression_id(AVScenariosParser.Real_value_expression_idContext ctx);
	/**
	 * Enter a parse tree produced by the {@code cifang_of_real_value_expression}
	 * labeled alternative in {@link AVScenariosParser#real_value_expression}.
	 * @param ctx the parse tree
	 */
	void enterCifang_of_real_value_expression(AVScenariosParser.Cifang_of_real_value_expressionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code cifang_of_real_value_expression}
	 * labeled alternative in {@link AVScenariosParser#real_value_expression}.
	 * @param ctx the parse tree
	 */
	void exitCifang_of_real_value_expression(AVScenariosParser.Cifang_of_real_value_expressionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code real_value_of_real_value_expression}
	 * labeled alternative in {@link AVScenariosParser#real_value_expression}.
	 * @param ctx the parse tree
	 */
	void enterReal_value_of_real_value_expression(AVScenariosParser.Real_value_of_real_value_expressionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code real_value_of_real_value_expression}
	 * labeled alternative in {@link AVScenariosParser#real_value_expression}.
	 * @param ctx the parse tree
	 */
	void exitReal_value_of_real_value_expression(AVScenariosParser.Real_value_of_real_value_expressionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Plus_of_real_value_expression}
	 * labeled alternative in {@link AVScenariosParser#real_value_expression}.
	 * @param ctx the parse tree
	 */
	void enterPlus_of_real_value_expression(AVScenariosParser.Plus_of_real_value_expressionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Plus_of_real_value_expression}
	 * labeled alternative in {@link AVScenariosParser#real_value_expression}.
	 * @param ctx the parse tree
	 */
	void exitPlus_of_real_value_expression(AVScenariosParser.Plus_of_real_value_expressionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code kuohao_of_real_value_expression}
	 * labeled alternative in {@link AVScenariosParser#real_value_expression}.
	 * @param ctx the parse tree
	 */
	void enterKuohao_of_real_value_expression(AVScenariosParser.Kuohao_of_real_value_expressionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code kuohao_of_real_value_expression}
	 * labeled alternative in {@link AVScenariosParser#real_value_expression}.
	 * @param ctx the parse tree
	 */
	void exitKuohao_of_real_value_expression(AVScenariosParser.Kuohao_of_real_value_expressionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Multi_of_real_value_expression}
	 * labeled alternative in {@link AVScenariosParser#real_value_expression}.
	 * @param ctx the parse tree
	 */
	void enterMulti_of_real_value_expression(AVScenariosParser.Multi_of_real_value_expressionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Multi_of_real_value_expression}
	 * labeled alternative in {@link AVScenariosParser#real_value_expression}.
	 * @param ctx the parse tree
	 */
	void exitMulti_of_real_value_expression(AVScenariosParser.Multi_of_real_value_expressionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Plus_of_coordinate_expression}
	 * labeled alternative in {@link AVScenariosParser#coordinate_expression}.
	 * @param ctx the parse tree
	 */
	void enterPlus_of_coordinate_expression(AVScenariosParser.Plus_of_coordinate_expressionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Plus_of_coordinate_expression}
	 * labeled alternative in {@link AVScenariosParser#coordinate_expression}.
	 * @param ctx the parse tree
	 */
	void exitPlus_of_coordinate_expression(AVScenariosParser.Plus_of_coordinate_expressionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code coordinate_expression_id}
	 * labeled alternative in {@link AVScenariosParser#coordinate_expression}.
	 * @param ctx the parse tree
	 */
	void enterCoordinate_expression_id(AVScenariosParser.Coordinate_expression_idContext ctx);
	/**
	 * Exit a parse tree produced by the {@code coordinate_expression_id}
	 * labeled alternative in {@link AVScenariosParser#coordinate_expression}.
	 * @param ctx the parse tree
	 */
	void exitCoordinate_expression_id(AVScenariosParser.Coordinate_expression_idContext ctx);
	/**
	 * Enter a parse tree produced by the {@code coordinate_of_coordinate_expression}
	 * labeled alternative in {@link AVScenariosParser#coordinate_expression}.
	 * @param ctx the parse tree
	 */
	void enterCoordinate_of_coordinate_expression(AVScenariosParser.Coordinate_of_coordinate_expressionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code coordinate_of_coordinate_expression}
	 * labeled alternative in {@link AVScenariosParser#coordinate_expression}.
	 * @param ctx the parse tree
	 */
	void exitCoordinate_of_coordinate_expression(AVScenariosParser.Coordinate_of_coordinate_expressionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code kuohao_of_coordinate_expression}
	 * labeled alternative in {@link AVScenariosParser#coordinate_expression}.
	 * @param ctx the parse tree
	 */
	void enterKuohao_of_coordinate_expression(AVScenariosParser.Kuohao_of_coordinate_expressionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code kuohao_of_coordinate_expression}
	 * labeled alternative in {@link AVScenariosParser#coordinate_expression}.
	 * @param ctx the parse tree
	 */
	void exitKuohao_of_coordinate_expression(AVScenariosParser.Kuohao_of_coordinate_expressionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Muti_of_coordinate_expression}
	 * labeled alternative in {@link AVScenariosParser#coordinate_expression}.
	 * @param ctx the parse tree
	 */
	void enterMuti_of_coordinate_expression(AVScenariosParser.Muti_of_coordinate_expressionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Muti_of_coordinate_expression}
	 * labeled alternative in {@link AVScenariosParser#coordinate_expression}.
	 * @param ctx the parse tree
	 */
	void exitMuti_of_coordinate_expression(AVScenariosParser.Muti_of_coordinate_expressionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code create_scenario}
	 * labeled alternative in {@link AVScenariosParser#scenario}.
	 * @param ctx the parse tree
	 */
	void enterCreate_scenario(AVScenariosParser.Create_scenarioContext ctx);
	/**
	 * Exit a parse tree produced by the {@code create_scenario}
	 * labeled alternative in {@link AVScenariosParser#scenario}.
	 * @param ctx the parse tree
	 */
	void exitCreate_scenario(AVScenariosParser.Create_scenarioContext ctx);
	/**
	 * Enter a parse tree produced by the {@code npc_var}
	 * labeled alternative in {@link AVScenariosParser#npc_vehicles_parameter}.
	 * @param ctx the parse tree
	 */
	void enterNpc_var(AVScenariosParser.Npc_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code npc_var}
	 * labeled alternative in {@link AVScenariosParser#npc_vehicles_parameter}.
	 * @param ctx the parse tree
	 */
	void exitNpc_var(AVScenariosParser.Npc_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code npc_npc}
	 * labeled alternative in {@link AVScenariosParser#npc_vehicles_parameter}.
	 * @param ctx the parse tree
	 */
	void enterNpc_npc(AVScenariosParser.Npc_npcContext ctx);
	/**
	 * Exit a parse tree produced by the {@code npc_npc}
	 * labeled alternative in {@link AVScenariosParser#npc_vehicles_parameter}.
	 * @param ctx the parse tree
	 */
	void exitNpc_npc(AVScenariosParser.Npc_npcContext ctx);
	/**
	 * Enter a parse tree produced by the {@code npc_empty}
	 * labeled alternative in {@link AVScenariosParser#npc_vehicles_parameter}.
	 * @param ctx the parse tree
	 */
	void enterNpc_empty(AVScenariosParser.Npc_emptyContext ctx);
	/**
	 * Exit a parse tree produced by the {@code npc_empty}
	 * labeled alternative in {@link AVScenariosParser#npc_vehicles_parameter}.
	 * @param ctx the parse tree
	 */
	void exitNpc_empty(AVScenariosParser.Npc_emptyContext ctx);
	/**
	 * Enter a parse tree produced by the {@code pedestrians_var}
	 * labeled alternative in {@link AVScenariosParser#pedestrians_parameter}.
	 * @param ctx the parse tree
	 */
	void enterPedestrians_var(AVScenariosParser.Pedestrians_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code pedestrians_var}
	 * labeled alternative in {@link AVScenariosParser#pedestrians_parameter}.
	 * @param ctx the parse tree
	 */
	void exitPedestrians_var(AVScenariosParser.Pedestrians_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code pedestrians_ped}
	 * labeled alternative in {@link AVScenariosParser#pedestrians_parameter}.
	 * @param ctx the parse tree
	 */
	void enterPedestrians_ped(AVScenariosParser.Pedestrians_pedContext ctx);
	/**
	 * Exit a parse tree produced by the {@code pedestrians_ped}
	 * labeled alternative in {@link AVScenariosParser#pedestrians_parameter}.
	 * @param ctx the parse tree
	 */
	void exitPedestrians_ped(AVScenariosParser.Pedestrians_pedContext ctx);
	/**
	 * Enter a parse tree produced by the {@code pedestrians_empty}
	 * labeled alternative in {@link AVScenariosParser#pedestrians_parameter}.
	 * @param ctx the parse tree
	 */
	void enterPedestrians_empty(AVScenariosParser.Pedestrians_emptyContext ctx);
	/**
	 * Exit a parse tree produced by the {@code pedestrians_empty}
	 * labeled alternative in {@link AVScenariosParser#pedestrians_parameter}.
	 * @param ctx the parse tree
	 */
	void exitPedestrians_empty(AVScenariosParser.Pedestrians_emptyContext ctx);
	/**
	 * Enter a parse tree produced by the {@code obstacles_var}
	 * labeled alternative in {@link AVScenariosParser#obstacles_parameter}.
	 * @param ctx the parse tree
	 */
	void enterObstacles_var(AVScenariosParser.Obstacles_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code obstacles_var}
	 * labeled alternative in {@link AVScenariosParser#obstacles_parameter}.
	 * @param ctx the parse tree
	 */
	void exitObstacles_var(AVScenariosParser.Obstacles_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code obstacles_obs}
	 * labeled alternative in {@link AVScenariosParser#obstacles_parameter}.
	 * @param ctx the parse tree
	 */
	void enterObstacles_obs(AVScenariosParser.Obstacles_obsContext ctx);
	/**
	 * Exit a parse tree produced by the {@code obstacles_obs}
	 * labeled alternative in {@link AVScenariosParser#obstacles_parameter}.
	 * @param ctx the parse tree
	 */
	void exitObstacles_obs(AVScenariosParser.Obstacles_obsContext ctx);
	/**
	 * Enter a parse tree produced by the {@code obstacles_empty}
	 * labeled alternative in {@link AVScenariosParser#obstacles_parameter}.
	 * @param ctx the parse tree
	 */
	void enterObstacles_empty(AVScenariosParser.Obstacles_emptyContext ctx);
	/**
	 * Exit a parse tree produced by the {@code obstacles_empty}
	 * labeled alternative in {@link AVScenariosParser#obstacles_parameter}.
	 * @param ctx the parse tree
	 */
	void exitObstacles_empty(AVScenariosParser.Obstacles_emptyContext ctx);
	/**
	 * Enter a parse tree produced by the {@code map_load_name}
	 * labeled alternative in {@link AVScenariosParser#map_parameter}.
	 * @param ctx the parse tree
	 */
	void enterMap_load_name(AVScenariosParser.Map_load_nameContext ctx);
	/**
	 * Exit a parse tree produced by the {@code map_load_name}
	 * labeled alternative in {@link AVScenariosParser#map_parameter}.
	 * @param ctx the parse tree
	 */
	void exitMap_load_name(AVScenariosParser.Map_load_nameContext ctx);
	/**
	 * Enter a parse tree produced by the {@code map_name_str}
	 * labeled alternative in {@link AVScenariosParser#map_name}.
	 * @param ctx the parse tree
	 */
	void enterMap_name_str(AVScenariosParser.Map_name_strContext ctx);
	/**
	 * Exit a parse tree produced by the {@code map_name_str}
	 * labeled alternative in {@link AVScenariosParser#map_name}.
	 * @param ctx the parse tree
	 */
	void exitMap_name_str(AVScenariosParser.Map_name_strContext ctx);
	/**
	 * Enter a parse tree produced by the {@code ego_ego_vehicle}
	 * labeled alternative in {@link AVScenariosParser#ego_parameter}.
	 * @param ctx the parse tree
	 */
	void enterEgo_ego_vehicle(AVScenariosParser.Ego_ego_vehicleContext ctx);
	/**
	 * Exit a parse tree produced by the {@code ego_ego_vehicle}
	 * labeled alternative in {@link AVScenariosParser#ego_parameter}.
	 * @param ctx the parse tree
	 */
	void exitEgo_ego_vehicle(AVScenariosParser.Ego_ego_vehicleContext ctx);
	/**
	 * Enter a parse tree produced by the {@code ego_ego_var}
	 * labeled alternative in {@link AVScenariosParser#ego_parameter}.
	 * @param ctx the parse tree
	 */
	void enterEgo_ego_var(AVScenariosParser.Ego_ego_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code ego_ego_var}
	 * labeled alternative in {@link AVScenariosParser#ego_parameter}.
	 * @param ctx the parse tree
	 */
	void exitEgo_ego_var(AVScenariosParser.Ego_ego_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code ego_av}
	 * labeled alternative in {@link AVScenariosParser#ego_vehicle}.
	 * @param ctx the parse tree
	 */
	void enterEgo_av(AVScenariosParser.Ego_avContext ctx);
	/**
	 * Exit a parse tree produced by the {@code ego_av}
	 * labeled alternative in {@link AVScenariosParser#ego_vehicle}.
	 * @param ctx the parse tree
	 */
	void exitEgo_av(AVScenariosParser.Ego_avContext ctx);
	/**
	 * Enter a parse tree produced by the {@code par_list_ego_}
	 * labeled alternative in {@link AVScenariosParser#parameter_list_ego}.
	 * @param ctx the parse tree
	 */
	void enterPar_list_ego_(AVScenariosParser.Par_list_ego_Context ctx);
	/**
	 * Exit a parse tree produced by the {@code par_list_ego_}
	 * labeled alternative in {@link AVScenariosParser#parameter_list_ego}.
	 * @param ctx the parse tree
	 */
	void exitPar_list_ego_(AVScenariosParser.Par_list_ego_Context ctx);
	/**
	 * Enter a parse tree produced by the {@code state_state}
	 * labeled alternative in {@link AVScenariosParser#state_parameter}.
	 * @param ctx the parse tree
	 */
	void enterState_state(AVScenariosParser.State_stateContext ctx);
	/**
	 * Exit a parse tree produced by the {@code state_state}
	 * labeled alternative in {@link AVScenariosParser#state_parameter}.
	 * @param ctx the parse tree
	 */
	void exitState_state(AVScenariosParser.State_stateContext ctx);
	/**
	 * Enter a parse tree produced by the {@code state_state_var}
	 * labeled alternative in {@link AVScenariosParser#state_parameter}.
	 * @param ctx the parse tree
	 */
	void enterState_state_var(AVScenariosParser.State_state_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code state_state_var}
	 * labeled alternative in {@link AVScenariosParser#state_parameter}.
	 * @param ctx the parse tree
	 */
	void exitState_state_var(AVScenariosParser.State_state_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code state_position}
	 * labeled alternative in {@link AVScenariosParser#state_}.
	 * @param ctx the parse tree
	 */
	void enterState_position(AVScenariosParser.State_positionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code state_position}
	 * labeled alternative in {@link AVScenariosParser#state_}.
	 * @param ctx the parse tree
	 */
	void exitState_position(AVScenariosParser.State_positionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code state_position_heading_speed}
	 * labeled alternative in {@link AVScenariosParser#state_}.
	 * @param ctx the parse tree
	 */
	void enterState_position_heading_speed(AVScenariosParser.State_position_heading_speedContext ctx);
	/**
	 * Exit a parse tree produced by the {@code state_position_heading_speed}
	 * labeled alternative in {@link AVScenariosParser#state_}.
	 * @param ctx the parse tree
	 */
	void exitState_position_heading_speed(AVScenariosParser.State_position_heading_speedContext ctx);
	/**
	 * Enter a parse tree produced by the {@code pos_coor_coor}
	 * labeled alternative in {@link AVScenariosParser#position}.
	 * @param ctx the parse tree
	 */
	void enterPos_coor_coor(AVScenariosParser.Pos_coor_coorContext ctx);
	/**
	 * Exit a parse tree produced by the {@code pos_coor_coor}
	 * labeled alternative in {@link AVScenariosParser#position}.
	 * @param ctx the parse tree
	 */
	void exitPos_coor_coor(AVScenariosParser.Pos_coor_coorContext ctx);
	/**
	 * Enter a parse tree produced by the {@code pos_coor_coor2}
	 * labeled alternative in {@link AVScenariosParser#position}.
	 * @param ctx the parse tree
	 */
	void enterPos_coor_coor2(AVScenariosParser.Pos_coor_coor2Context ctx);
	/**
	 * Exit a parse tree produced by the {@code pos_coor_coor2}
	 * labeled alternative in {@link AVScenariosParser#position}.
	 * @param ctx the parse tree
	 */
	void exitPos_coor_coor2(AVScenariosParser.Pos_coor_coor2Context ctx);
	/**
	 * Enter a parse tree produced by the {@code pos_coor_range1}
	 * labeled alternative in {@link AVScenariosParser#position}.
	 * @param ctx the parse tree
	 */
	void enterPos_coor_range1(AVScenariosParser.Pos_coor_range1Context ctx);
	/**
	 * Exit a parse tree produced by the {@code pos_coor_range1}
	 * labeled alternative in {@link AVScenariosParser#position}.
	 * @param ctx the parse tree
	 */
	void exitPos_coor_range1(AVScenariosParser.Pos_coor_range1Context ctx);
	/**
	 * Enter a parse tree produced by the {@code coor_imu}
	 * labeled alternative in {@link AVScenariosParser#coordinate_frame}.
	 * @param ctx the parse tree
	 */
	void enterCoor_imu(AVScenariosParser.Coor_imuContext ctx);
	/**
	 * Exit a parse tree produced by the {@code coor_imu}
	 * labeled alternative in {@link AVScenariosParser#coordinate_frame}.
	 * @param ctx the parse tree
	 */
	void exitCoor_imu(AVScenariosParser.Coor_imuContext ctx);
	/**
	 * Enter a parse tree produced by the {@code coor_enu}
	 * labeled alternative in {@link AVScenariosParser#coordinate_frame}.
	 * @param ctx the parse tree
	 */
	void enterCoor_enu(AVScenariosParser.Coor_enuContext ctx);
	/**
	 * Exit a parse tree produced by the {@code coor_enu}
	 * labeled alternative in {@link AVScenariosParser#coordinate_frame}.
	 * @param ctx the parse tree
	 */
	void exitCoor_enu(AVScenariosParser.Coor_enuContext ctx);
	/**
	 * Enter a parse tree produced by the {@code coor_wgs84}
	 * labeled alternative in {@link AVScenariosParser#coordinate_frame}.
	 * @param ctx the parse tree
	 */
	void enterCoor_wgs84(AVScenariosParser.Coor_wgs84Context ctx);
	/**
	 * Exit a parse tree produced by the {@code coor_wgs84}
	 * labeled alternative in {@link AVScenariosParser#coordinate_frame}.
	 * @param ctx the parse tree
	 */
	void exitCoor_wgs84(AVScenariosParser.Coor_wgs84Context ctx);
	/**
	 * Enter a parse tree produced by the {@code pos_pos}
	 * labeled alternative in {@link AVScenariosParser#position_parameter}.
	 * @param ctx the parse tree
	 */
	void enterPos_pos(AVScenariosParser.Pos_posContext ctx);
	/**
	 * Exit a parse tree produced by the {@code pos_pos}
	 * labeled alternative in {@link AVScenariosParser#position_parameter}.
	 * @param ctx the parse tree
	 */
	void exitPos_pos(AVScenariosParser.Pos_posContext ctx);
	/**
	 * Enter a parse tree produced by the {@code pos_pos_var}
	 * labeled alternative in {@link AVScenariosParser#position_parameter}.
	 * @param ctx the parse tree
	 */
	void enterPos_pos_var(AVScenariosParser.Pos_pos_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code pos_pos_var}
	 * labeled alternative in {@link AVScenariosParser#position_parameter}.
	 * @param ctx the parse tree
	 */
	void exitPos_pos_var(AVScenariosParser.Pos_pos_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code speed_speed}
	 * labeled alternative in {@link AVScenariosParser#speed_parameter}.
	 * @param ctx the parse tree
	 */
	void enterSpeed_speed(AVScenariosParser.Speed_speedContext ctx);
	/**
	 * Exit a parse tree produced by the {@code speed_speed}
	 * labeled alternative in {@link AVScenariosParser#speed_parameter}.
	 * @param ctx the parse tree
	 */
	void exitSpeed_speed(AVScenariosParser.Speed_speedContext ctx);
	/**
	 * Enter a parse tree produced by the {@code speed_speed_var}
	 * labeled alternative in {@link AVScenariosParser#speed_parameter}.
	 * @param ctx the parse tree
	 */
	void enterSpeed_speed_var(AVScenariosParser.Speed_speed_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code speed_speed_var}
	 * labeled alternative in {@link AVScenariosParser#speed_parameter}.
	 * @param ctx the parse tree
	 */
	void exitSpeed_speed_var(AVScenariosParser.Speed_speed_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code speed_rv}
	 * labeled alternative in {@link AVScenariosParser#speed}.
	 * @param ctx the parse tree
	 */
	void enterSpeed_rv(AVScenariosParser.Speed_rvContext ctx);
	/**
	 * Exit a parse tree produced by the {@code speed_rv}
	 * labeled alternative in {@link AVScenariosParser#speed}.
	 * @param ctx the parse tree
	 */
	void exitSpeed_rv(AVScenariosParser.Speed_rvContext ctx);
	/**
	 * Enter a parse tree produced by the {@code speed_range_for_state}
	 * labeled alternative in {@link AVScenariosParser#speed}.
	 * @param ctx the parse tree
	 */
	void enterSpeed_range_for_state(AVScenariosParser.Speed_range_for_stateContext ctx);
	/**
	 * Exit a parse tree produced by the {@code speed_range_for_state}
	 * labeled alternative in {@link AVScenariosParser#speed}.
	 * @param ctx the parse tree
	 */
	void exitSpeed_range_for_state(AVScenariosParser.Speed_range_for_stateContext ctx);
	/**
	 * Enter a parse tree produced by the {@code rv}
	 * labeled alternative in {@link AVScenariosParser#real_value}.
	 * @param ctx the parse tree
	 */
	void enterRv(AVScenariosParser.RvContext ctx);
	/**
	 * Exit a parse tree produced by the {@code rv}
	 * labeled alternative in {@link AVScenariosParser#real_value}.
	 * @param ctx the parse tree
	 */
	void exitRv(AVScenariosParser.RvContext ctx);
	/**
	 * Enter a parse tree produced by the {@code non_negative_rv}
	 * labeled alternative in {@link AVScenariosParser#non_negative_real_value}.
	 * @param ctx the parse tree
	 */
	void enterNon_negative_rv(AVScenariosParser.Non_negative_rvContext ctx);
	/**
	 * Exit a parse tree produced by the {@code non_negative_rv}
	 * labeled alternative in {@link AVScenariosParser#non_negative_real_value}.
	 * @param ctx the parse tree
	 */
	void exitNon_negative_rv(AVScenariosParser.Non_negative_rvContext ctx);
	/**
	 * Enter a parse tree produced by the {@code non_negative_float}
	 * labeled alternative in {@link AVScenariosParser#float_value}.
	 * @param ctx the parse tree
	 */
	void enterNon_negative_float(AVScenariosParser.Non_negative_floatContext ctx);
	/**
	 * Exit a parse tree produced by the {@code non_negative_float}
	 * labeled alternative in {@link AVScenariosParser#float_value}.
	 * @param ctx the parse tree
	 */
	void exitNon_negative_float(AVScenariosParser.Non_negative_floatContext ctx);
	/**
	 * Enter a parse tree produced by the {@code non_negative_number}
	 * labeled alternative in {@link AVScenariosParser#number_value}.
	 * @param ctx the parse tree
	 */
	void enterNon_negative_number(AVScenariosParser.Non_negative_numberContext ctx);
	/**
	 * Exit a parse tree produced by the {@code non_negative_number}
	 * labeled alternative in {@link AVScenariosParser#number_value}.
	 * @param ctx the parse tree
	 */
	void exitNon_negative_number(AVScenariosParser.Non_negative_numberContext ctx);
	/**
	 * Enter a parse tree produced by the {@code non_negative_conflict_0}
	 * labeled alternative in {@link AVScenariosParser#number_value}.
	 * @param ctx the parse tree
	 */
	void enterNon_negative_conflict_0(AVScenariosParser.Non_negative_conflict_0Context ctx);
	/**
	 * Exit a parse tree produced by the {@code non_negative_conflict_0}
	 * labeled alternative in {@link AVScenariosParser#number_value}.
	 * @param ctx the parse tree
	 */
	void exitNon_negative_conflict_0(AVScenariosParser.Non_negative_conflict_0Context ctx);
	/**
	 * Enter a parse tree produced by the {@code non_negative_conflict_1}
	 * labeled alternative in {@link AVScenariosParser#number_value}.
	 * @param ctx the parse tree
	 */
	void enterNon_negative_conflict_1(AVScenariosParser.Non_negative_conflict_1Context ctx);
	/**
	 * Exit a parse tree produced by the {@code non_negative_conflict_1}
	 * labeled alternative in {@link AVScenariosParser#number_value}.
	 * @param ctx the parse tree
	 */
	void exitNon_negative_conflict_1(AVScenariosParser.Non_negative_conflict_1Context ctx);
	/**
	 * Enter a parse tree produced by the {@code coor_rv_rv}
	 * labeled alternative in {@link AVScenariosParser#coordinate}.
	 * @param ctx the parse tree
	 */
	void enterCoor_rv_rv(AVScenariosParser.Coor_rv_rvContext ctx);
	/**
	 * Exit a parse tree produced by the {@code coor_rv_rv}
	 * labeled alternative in {@link AVScenariosParser#coordinate}.
	 * @param ctx the parse tree
	 */
	void exitCoor_rv_rv(AVScenariosParser.Coor_rv_rvContext ctx);
	/**
	 * Enter a parse tree produced by the {@code coor_laneID_rv}
	 * labeled alternative in {@link AVScenariosParser#coordinate}.
	 * @param ctx the parse tree
	 */
	void enterCoor_laneID_rv(AVScenariosParser.Coor_laneID_rvContext ctx);
	/**
	 * Exit a parse tree produced by the {@code coor_laneID_rv}
	 * labeled alternative in {@link AVScenariosParser#coordinate}.
	 * @param ctx the parse tree
	 */
	void exitCoor_laneID_rv(AVScenariosParser.Coor_laneID_rvContext ctx);
	/**
	 * Enter a parse tree produced by the {@code coor_laneID_range}
	 * labeled alternative in {@link AVScenariosParser#coordinate}.
	 * @param ctx the parse tree
	 */
	void enterCoor_laneID_range(AVScenariosParser.Coor_laneID_rangeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code coor_laneID_range}
	 * labeled alternative in {@link AVScenariosParser#coordinate}.
	 * @param ctx the parse tree
	 */
	void exitCoor_laneID_range(AVScenariosParser.Coor_laneID_rangeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code laneID_laneID_var}
	 * labeled alternative in {@link AVScenariosParser#laneID_parameter}.
	 * @param ctx the parse tree
	 */
	void enterLaneID_laneID_var(AVScenariosParser.LaneID_laneID_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code laneID_laneID_var}
	 * labeled alternative in {@link AVScenariosParser#laneID_parameter}.
	 * @param ctx the parse tree
	 */
	void exitLaneID_laneID_var(AVScenariosParser.LaneID_laneID_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code laneID_laneID}
	 * labeled alternative in {@link AVScenariosParser#laneID_parameter}.
	 * @param ctx the parse tree
	 */
	void enterLaneID_laneID(AVScenariosParser.LaneID_laneIDContext ctx);
	/**
	 * Exit a parse tree produced by the {@code laneID_laneID}
	 * labeled alternative in {@link AVScenariosParser#laneID_parameter}.
	 * @param ctx the parse tree
	 */
	void exitLaneID_laneID(AVScenariosParser.LaneID_laneIDContext ctx);
	/**
	 * Enter a parse tree produced by the {@code laneID_str}
	 * labeled alternative in {@link AVScenariosParser#laneID}.
	 * @param ctx the parse tree
	 */
	void enterLaneID_str(AVScenariosParser.LaneID_strContext ctx);
	/**
	 * Exit a parse tree produced by the {@code laneID_str}
	 * labeled alternative in {@link AVScenariosParser#laneID}.
	 * @param ctx the parse tree
	 */
	void exitLaneID_str(AVScenariosParser.LaneID_strContext ctx);
	/**
	 * Enter a parse tree produced by the {@code head_var}
	 * labeled alternative in {@link AVScenariosParser#heading_parameter}.
	 * @param ctx the parse tree
	 */
	void enterHead_var(AVScenariosParser.Head_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code head_var}
	 * labeled alternative in {@link AVScenariosParser#heading_parameter}.
	 * @param ctx the parse tree
	 */
	void exitHead_var(AVScenariosParser.Head_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code head_heading}
	 * labeled alternative in {@link AVScenariosParser#heading_parameter}.
	 * @param ctx the parse tree
	 */
	void enterHead_heading(AVScenariosParser.Head_headingContext ctx);
	/**
	 * Exit a parse tree produced by the {@code head_heading}
	 * labeled alternative in {@link AVScenariosParser#heading_parameter}.
	 * @param ctx the parse tree
	 */
	void exitHead_heading(AVScenariosParser.Head_headingContext ctx);
	/**
	 * Enter a parse tree produced by the {@code head_value}
	 * labeled alternative in {@link AVScenariosParser#heading}.
	 * @param ctx the parse tree
	 */
	void enterHead_value(AVScenariosParser.Head_valueContext ctx);
	/**
	 * Exit a parse tree produced by the {@code head_value}
	 * labeled alternative in {@link AVScenariosParser#heading}.
	 * @param ctx the parse tree
	 */
	void exitHead_value(AVScenariosParser.Head_valueContext ctx);
	/**
	 * Enter a parse tree produced by the {@code head_pi_value}
	 * labeled alternative in {@link AVScenariosParser#heading}.
	 * @param ctx the parse tree
	 */
	void enterHead_pi_value(AVScenariosParser.Head_pi_valueContext ctx);
	/**
	 * Exit a parse tree produced by the {@code head_pi_value}
	 * labeled alternative in {@link AVScenariosParser#heading}.
	 * @param ctx the parse tree
	 */
	void exitHead_pi_value(AVScenariosParser.Head_pi_valueContext ctx);
	/**
	 * Enter a parse tree produced by the {@code head_only_pi_value}
	 * labeled alternative in {@link AVScenariosParser#heading}.
	 * @param ctx the parse tree
	 */
	void enterHead_only_pi_value(AVScenariosParser.Head_only_pi_valueContext ctx);
	/**
	 * Exit a parse tree produced by the {@code head_only_pi_value}
	 * labeled alternative in {@link AVScenariosParser#heading}.
	 * @param ctx the parse tree
	 */
	void exitHead_only_pi_value(AVScenariosParser.Head_only_pi_valueContext ctx);
	/**
	 * Enter a parse tree produced by the {@code head_value_range}
	 * labeled alternative in {@link AVScenariosParser#heading}.
	 * @param ctx the parse tree
	 */
	void enterHead_value_range(AVScenariosParser.Head_value_rangeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code head_value_range}
	 * labeled alternative in {@link AVScenariosParser#heading}.
	 * @param ctx the parse tree
	 */
	void exitHead_value_range(AVScenariosParser.Head_value_rangeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code head_pi_value_range}
	 * labeled alternative in {@link AVScenariosParser#heading}.
	 * @param ctx the parse tree
	 */
	void enterHead_pi_value_range(AVScenariosParser.Head_pi_value_rangeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code head_pi_value_range}
	 * labeled alternative in {@link AVScenariosParser#heading}.
	 * @param ctx the parse tree
	 */
	void exitHead_pi_value_range(AVScenariosParser.Head_pi_value_rangeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code unit_deg}
	 * labeled alternative in {@link AVScenariosParser#unit}.
	 * @param ctx the parse tree
	 */
	void enterUnit_deg(AVScenariosParser.Unit_degContext ctx);
	/**
	 * Exit a parse tree produced by the {@code unit_deg}
	 * labeled alternative in {@link AVScenariosParser#unit}.
	 * @param ctx the parse tree
	 */
	void exitUnit_deg(AVScenariosParser.Unit_degContext ctx);
	/**
	 * Enter a parse tree produced by the {@code unit_rad}
	 * labeled alternative in {@link AVScenariosParser#unit}.
	 * @param ctx the parse tree
	 */
	void enterUnit_rad(AVScenariosParser.Unit_radContext ctx);
	/**
	 * Exit a parse tree produced by the {@code unit_rad}
	 * labeled alternative in {@link AVScenariosParser#unit}.
	 * @param ctx the parse tree
	 */
	void exitUnit_rad(AVScenariosParser.Unit_radContext ctx);
	/**
	 * Enter a parse tree produced by the {@code direction_pre}
	 * labeled alternative in {@link AVScenariosParser#direction}.
	 * @param ctx the parse tree
	 */
	void enterDirection_pre(AVScenariosParser.Direction_preContext ctx);
	/**
	 * Exit a parse tree produced by the {@code direction_pre}
	 * labeled alternative in {@link AVScenariosParser#direction}.
	 * @param ctx the parse tree
	 */
	void exitDirection_pre(AVScenariosParser.Direction_preContext ctx);
	/**
	 * Enter a parse tree produced by the {@code pre_lane}
	 * labeled alternative in {@link AVScenariosParser#predefined_direction}.
	 * @param ctx the parse tree
	 */
	void enterPre_lane(AVScenariosParser.Pre_laneContext ctx);
	/**
	 * Exit a parse tree produced by the {@code pre_lane}
	 * labeled alternative in {@link AVScenariosParser#predefined_direction}.
	 * @param ctx the parse tree
	 */
	void exitPre_lane(AVScenariosParser.Pre_laneContext ctx);
	/**
	 * Enter a parse tree produced by the {@code pre_ego}
	 * labeled alternative in {@link AVScenariosParser#predefined_direction}.
	 * @param ctx the parse tree
	 */
	void enterPre_ego(AVScenariosParser.Pre_egoContext ctx);
	/**
	 * Exit a parse tree produced by the {@code pre_ego}
	 * labeled alternative in {@link AVScenariosParser#predefined_direction}.
	 * @param ctx the parse tree
	 */
	void exitPre_ego(AVScenariosParser.Pre_egoContext ctx);
	/**
	 * Enter a parse tree produced by the {@code pre_id}
	 * labeled alternative in {@link AVScenariosParser#predefined_direction}.
	 * @param ctx the parse tree
	 */
	void enterPre_id(AVScenariosParser.Pre_idContext ctx);
	/**
	 * Exit a parse tree produced by the {@code pre_id}
	 * labeled alternative in {@link AVScenariosParser#predefined_direction}.
	 * @param ctx the parse tree
	 */
	void exitPre_id(AVScenariosParser.Pre_idContext ctx);
	/**
	 * Enter a parse tree produced by the {@code vehicle_vehicle_type_var}
	 * labeled alternative in {@link AVScenariosParser#vehicle_type_parameter}.
	 * @param ctx the parse tree
	 */
	void enterVehicle_vehicle_type_var(AVScenariosParser.Vehicle_vehicle_type_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code vehicle_vehicle_type_var}
	 * labeled alternative in {@link AVScenariosParser#vehicle_type_parameter}.
	 * @param ctx the parse tree
	 */
	void exitVehicle_vehicle_type_var(AVScenariosParser.Vehicle_vehicle_type_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code vehicle_vehicle_type}
	 * labeled alternative in {@link AVScenariosParser#vehicle_type_parameter}.
	 * @param ctx the parse tree
	 */
	void enterVehicle_vehicle_type(AVScenariosParser.Vehicle_vehicle_typeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code vehicle_vehicle_type}
	 * labeled alternative in {@link AVScenariosParser#vehicle_type_parameter}.
	 * @param ctx the parse tree
	 */
	void exitVehicle_vehicle_type(AVScenariosParser.Vehicle_vehicle_typeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code vehicle_type_}
	 * labeled alternative in {@link AVScenariosParser#vehicle_type}.
	 * @param ctx the parse tree
	 */
	void enterVehicle_type_(AVScenariosParser.Vehicle_type_Context ctx);
	/**
	 * Exit a parse tree produced by the {@code vehicle_type_}
	 * labeled alternative in {@link AVScenariosParser#vehicle_type}.
	 * @param ctx the parse tree
	 */
	void exitVehicle_type_(AVScenariosParser.Vehicle_type_Context ctx);
	/**
	 * Enter a parse tree produced by the {@code vehicle_type_color}
	 * labeled alternative in {@link AVScenariosParser#vehicle_type}.
	 * @param ctx the parse tree
	 */
	void enterVehicle_type_color(AVScenariosParser.Vehicle_type_colorContext ctx);
	/**
	 * Exit a parse tree produced by the {@code vehicle_type_color}
	 * labeled alternative in {@link AVScenariosParser#vehicle_type}.
	 * @param ctx the parse tree
	 */
	void exitVehicle_type_color(AVScenariosParser.Vehicle_type_colorContext ctx);
	/**
	 * Enter a parse tree produced by the {@code type_var}
	 * labeled alternative in {@link AVScenariosParser#type_parameter}.
	 * @param ctx the parse tree
	 */
	void enterType_var(AVScenariosParser.Type_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code type_var}
	 * labeled alternative in {@link AVScenariosParser#type_parameter}.
	 * @param ctx the parse tree
	 */
	void exitType_var(AVScenariosParser.Type_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code type_type_}
	 * labeled alternative in {@link AVScenariosParser#type_parameter}.
	 * @param ctx the parse tree
	 */
	void enterType_type_(AVScenariosParser.Type_type_Context ctx);
	/**
	 * Exit a parse tree produced by the {@code type_type_}
	 * labeled alternative in {@link AVScenariosParser#type_parameter}.
	 * @param ctx the parse tree
	 */
	void exitType_type_(AVScenariosParser.Type_type_Context ctx);
	/**
	 * Enter a parse tree produced by the {@code type_specific}
	 * labeled alternative in {@link AVScenariosParser#type_}.
	 * @param ctx the parse tree
	 */
	void enterType_specific(AVScenariosParser.Type_specificContext ctx);
	/**
	 * Exit a parse tree produced by the {@code type_specific}
	 * labeled alternative in {@link AVScenariosParser#type_}.
	 * @param ctx the parse tree
	 */
	void exitType_specific(AVScenariosParser.Type_specificContext ctx);
	/**
	 * Enter a parse tree produced by the {@code type_general}
	 * labeled alternative in {@link AVScenariosParser#type_}.
	 * @param ctx the parse tree
	 */
	void enterType_general(AVScenariosParser.Type_generalContext ctx);
	/**
	 * Exit a parse tree produced by the {@code type_general}
	 * labeled alternative in {@link AVScenariosParser#type_}.
	 * @param ctx the parse tree
	 */
	void exitType_general(AVScenariosParser.Type_generalContext ctx);
	/**
	 * Enter a parse tree produced by the {@code specific_str}
	 * labeled alternative in {@link AVScenariosParser#specific_type}.
	 * @param ctx the parse tree
	 */
	void enterSpecific_str(AVScenariosParser.Specific_strContext ctx);
	/**
	 * Exit a parse tree produced by the {@code specific_str}
	 * labeled alternative in {@link AVScenariosParser#specific_type}.
	 * @param ctx the parse tree
	 */
	void exitSpecific_str(AVScenariosParser.Specific_strContext ctx);
	/**
	 * Enter a parse tree produced by the {@code general_car}
	 * labeled alternative in {@link AVScenariosParser#general_type}.
	 * @param ctx the parse tree
	 */
	void enterGeneral_car(AVScenariosParser.General_carContext ctx);
	/**
	 * Exit a parse tree produced by the {@code general_car}
	 * labeled alternative in {@link AVScenariosParser#general_type}.
	 * @param ctx the parse tree
	 */
	void exitGeneral_car(AVScenariosParser.General_carContext ctx);
	/**
	 * Enter a parse tree produced by the {@code general_bus}
	 * labeled alternative in {@link AVScenariosParser#general_type}.
	 * @param ctx the parse tree
	 */
	void enterGeneral_bus(AVScenariosParser.General_busContext ctx);
	/**
	 * Exit a parse tree produced by the {@code general_bus}
	 * labeled alternative in {@link AVScenariosParser#general_type}.
	 * @param ctx the parse tree
	 */
	void exitGeneral_bus(AVScenariosParser.General_busContext ctx);
	/**
	 * Enter a parse tree produced by the {@code general_van}
	 * labeled alternative in {@link AVScenariosParser#general_type}.
	 * @param ctx the parse tree
	 */
	void enterGeneral_van(AVScenariosParser.General_vanContext ctx);
	/**
	 * Exit a parse tree produced by the {@code general_van}
	 * labeled alternative in {@link AVScenariosParser#general_type}.
	 * @param ctx the parse tree
	 */
	void exitGeneral_van(AVScenariosParser.General_vanContext ctx);
	/**
	 * Enter a parse tree produced by the {@code general_truck}
	 * labeled alternative in {@link AVScenariosParser#general_type}.
	 * @param ctx the parse tree
	 */
	void enterGeneral_truck(AVScenariosParser.General_truckContext ctx);
	/**
	 * Exit a parse tree produced by the {@code general_truck}
	 * labeled alternative in {@link AVScenariosParser#general_type}.
	 * @param ctx the parse tree
	 */
	void exitGeneral_truck(AVScenariosParser.General_truckContext ctx);
	/**
	 * Enter a parse tree produced by the {@code general_bicycle}
	 * labeled alternative in {@link AVScenariosParser#general_type}.
	 * @param ctx the parse tree
	 */
	void enterGeneral_bicycle(AVScenariosParser.General_bicycleContext ctx);
	/**
	 * Exit a parse tree produced by the {@code general_bicycle}
	 * labeled alternative in {@link AVScenariosParser#general_type}.
	 * @param ctx the parse tree
	 */
	void exitGeneral_bicycle(AVScenariosParser.General_bicycleContext ctx);
	/**
	 * Enter a parse tree produced by the {@code general_motorbicycle}
	 * labeled alternative in {@link AVScenariosParser#general_type}.
	 * @param ctx the parse tree
	 */
	void enterGeneral_motorbicycle(AVScenariosParser.General_motorbicycleContext ctx);
	/**
	 * Exit a parse tree produced by the {@code general_motorbicycle}
	 * labeled alternative in {@link AVScenariosParser#general_type}.
	 * @param ctx the parse tree
	 */
	void exitGeneral_motorbicycle(AVScenariosParser.General_motorbicycleContext ctx);
	/**
	 * Enter a parse tree produced by the {@code general_tricycle}
	 * labeled alternative in {@link AVScenariosParser#general_type}.
	 * @param ctx the parse tree
	 */
	void enterGeneral_tricycle(AVScenariosParser.General_tricycleContext ctx);
	/**
	 * Exit a parse tree produced by the {@code general_tricycle}
	 * labeled alternative in {@link AVScenariosParser#general_type}.
	 * @param ctx the parse tree
	 */
	void exitGeneral_tricycle(AVScenariosParser.General_tricycleContext ctx);
	/**
	 * Enter a parse tree produced by the {@code color_var}
	 * labeled alternative in {@link AVScenariosParser#color_parameter}.
	 * @param ctx the parse tree
	 */
	void enterColor_var(AVScenariosParser.Color_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code color_var}
	 * labeled alternative in {@link AVScenariosParser#color_parameter}.
	 * @param ctx the parse tree
	 */
	void exitColor_var(AVScenariosParser.Color_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code color_color}
	 * labeled alternative in {@link AVScenariosParser#color_parameter}.
	 * @param ctx the parse tree
	 */
	void enterColor_color(AVScenariosParser.Color_colorContext ctx);
	/**
	 * Exit a parse tree produced by the {@code color_color}
	 * labeled alternative in {@link AVScenariosParser#color_parameter}.
	 * @param ctx the parse tree
	 */
	void exitColor_color(AVScenariosParser.Color_colorContext ctx);
	/**
	 * Enter a parse tree produced by the {@code color_color_list}
	 * labeled alternative in {@link AVScenariosParser#color}.
	 * @param ctx the parse tree
	 */
	void enterColor_color_list(AVScenariosParser.Color_color_listContext ctx);
	/**
	 * Exit a parse tree produced by the {@code color_color_list}
	 * labeled alternative in {@link AVScenariosParser#color}.
	 * @param ctx the parse tree
	 */
	void exitColor_color_list(AVScenariosParser.Color_color_listContext ctx);
	/**
	 * Enter a parse tree produced by the {@code color_rgb_color}
	 * labeled alternative in {@link AVScenariosParser#color}.
	 * @param ctx the parse tree
	 */
	void enterColor_rgb_color(AVScenariosParser.Color_rgb_colorContext ctx);
	/**
	 * Exit a parse tree produced by the {@code color_rgb_color}
	 * labeled alternative in {@link AVScenariosParser#color}.
	 * @param ctx the parse tree
	 */
	void exitColor_rgb_color(AVScenariosParser.Color_rgb_colorContext ctx);
	/**
	 * Enter a parse tree produced by the {@code color_red}
	 * labeled alternative in {@link AVScenariosParser#color_list}.
	 * @param ctx the parse tree
	 */
	void enterColor_red(AVScenariosParser.Color_redContext ctx);
	/**
	 * Exit a parse tree produced by the {@code color_red}
	 * labeled alternative in {@link AVScenariosParser#color_list}.
	 * @param ctx the parse tree
	 */
	void exitColor_red(AVScenariosParser.Color_redContext ctx);
	/**
	 * Enter a parse tree produced by the {@code color_green}
	 * labeled alternative in {@link AVScenariosParser#color_list}.
	 * @param ctx the parse tree
	 */
	void enterColor_green(AVScenariosParser.Color_greenContext ctx);
	/**
	 * Exit a parse tree produced by the {@code color_green}
	 * labeled alternative in {@link AVScenariosParser#color_list}.
	 * @param ctx the parse tree
	 */
	void exitColor_green(AVScenariosParser.Color_greenContext ctx);
	/**
	 * Enter a parse tree produced by the {@code color_blue}
	 * labeled alternative in {@link AVScenariosParser#color_list}.
	 * @param ctx the parse tree
	 */
	void enterColor_blue(AVScenariosParser.Color_blueContext ctx);
	/**
	 * Exit a parse tree produced by the {@code color_blue}
	 * labeled alternative in {@link AVScenariosParser#color_list}.
	 * @param ctx the parse tree
	 */
	void exitColor_blue(AVScenariosParser.Color_blueContext ctx);
	/**
	 * Enter a parse tree produced by the {@code color_black}
	 * labeled alternative in {@link AVScenariosParser#color_list}.
	 * @param ctx the parse tree
	 */
	void enterColor_black(AVScenariosParser.Color_blackContext ctx);
	/**
	 * Exit a parse tree produced by the {@code color_black}
	 * labeled alternative in {@link AVScenariosParser#color_list}.
	 * @param ctx the parse tree
	 */
	void exitColor_black(AVScenariosParser.Color_blackContext ctx);
	/**
	 * Enter a parse tree produced by the {@code color_white}
	 * labeled alternative in {@link AVScenariosParser#color_list}.
	 * @param ctx the parse tree
	 */
	void enterColor_white(AVScenariosParser.Color_whiteContext ctx);
	/**
	 * Exit a parse tree produced by the {@code color_white}
	 * labeled alternative in {@link AVScenariosParser#color_list}.
	 * @param ctx the parse tree
	 */
	void exitColor_white(AVScenariosParser.Color_whiteContext ctx);
	/**
	 * Enter a parse tree produced by the {@code rgb_rgb}
	 * labeled alternative in {@link AVScenariosParser#rgb_color}.
	 * @param ctx the parse tree
	 */
	void enterRgb_rgb(AVScenariosParser.Rgb_rgbContext ctx);
	/**
	 * Exit a parse tree produced by the {@code rgb_rgb}
	 * labeled alternative in {@link AVScenariosParser#rgb_color}.
	 * @param ctx the parse tree
	 */
	void exitRgb_rgb(AVScenariosParser.Rgb_rgbContext ctx);
	/**
	 * Enter a parse tree produced by the {@code npc}
	 * labeled alternative in {@link AVScenariosParser#npc_vehicles}.
	 * @param ctx the parse tree
	 */
	void enterNpc(AVScenariosParser.NpcContext ctx);
	/**
	 * Exit a parse tree produced by the {@code npc}
	 * labeled alternative in {@link AVScenariosParser#npc_vehicles}.
	 * @param ctx the parse tree
	 */
	void exitNpc(AVScenariosParser.NpcContext ctx);
	/**
	 * Enter a parse tree produced by the {@code multi_multi_npc}
	 * labeled alternative in {@link AVScenariosParser#multi_npc_vehicles}.
	 * @param ctx the parse tree
	 */
	void enterMulti_multi_npc(AVScenariosParser.Multi_multi_npcContext ctx);
	/**
	 * Exit a parse tree produced by the {@code multi_multi_npc}
	 * labeled alternative in {@link AVScenariosParser#multi_npc_vehicles}.
	 * @param ctx the parse tree
	 */
	void exitMulti_multi_npc(AVScenariosParser.Multi_multi_npcContext ctx);
	/**
	 * Enter a parse tree produced by the {@code multi_npc}
	 * labeled alternative in {@link AVScenariosParser#multi_npc_vehicles}.
	 * @param ctx the parse tree
	 */
	void enterMulti_npc(AVScenariosParser.Multi_npcContext ctx);
	/**
	 * Exit a parse tree produced by the {@code multi_npc}
	 * labeled alternative in {@link AVScenariosParser#multi_npc_vehicles}.
	 * @param ctx the parse tree
	 */
	void exitMulti_npc(AVScenariosParser.Multi_npcContext ctx);
	/**
	 * Enter a parse tree produced by the {@code npc_vehicle_par}
	 * labeled alternative in {@link AVScenariosParser#npc_vehicle}.
	 * @param ctx the parse tree
	 */
	void enterNpc_vehicle_par(AVScenariosParser.Npc_vehicle_parContext ctx);
	/**
	 * Exit a parse tree produced by the {@code npc_vehicle_par}
	 * labeled alternative in {@link AVScenariosParser#npc_vehicle}.
	 * @param ctx the parse tree
	 */
	void exitNpc_vehicle_par(AVScenariosParser.Npc_vehicle_parContext ctx);
	/**
	 * Enter a parse tree produced by the {@code npc_npc_vehicle}
	 * labeled alternative in {@link AVScenariosParser#npc_vehicle_parameter}.
	 * @param ctx the parse tree
	 */
	void enterNpc_npc_vehicle(AVScenariosParser.Npc_npc_vehicleContext ctx);
	/**
	 * Exit a parse tree produced by the {@code npc_npc_vehicle}
	 * labeled alternative in {@link AVScenariosParser#npc_vehicle_parameter}.
	 * @param ctx the parse tree
	 */
	void exitNpc_npc_vehicle(AVScenariosParser.Npc_npc_vehicleContext ctx);
	/**
	 * Enter a parse tree produced by the {@code npc_npc_vehicle_var}
	 * labeled alternative in {@link AVScenariosParser#npc_vehicle_parameter}.
	 * @param ctx the parse tree
	 */
	void enterNpc_npc_vehicle_var(AVScenariosParser.Npc_npc_vehicle_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code npc_npc_vehicle_var}
	 * labeled alternative in {@link AVScenariosParser#npc_vehicle_parameter}.
	 * @param ctx the parse tree
	 */
	void exitNpc_npc_vehicle_var(AVScenariosParser.Npc_npc_vehicle_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code par_npc_state}
	 * labeled alternative in {@link AVScenariosParser#parameter_list_npc}.
	 * @param ctx the parse tree
	 */
	void enterPar_npc_state(AVScenariosParser.Par_npc_stateContext ctx);
	/**
	 * Exit a parse tree produced by the {@code par_npc_state}
	 * labeled alternative in {@link AVScenariosParser#parameter_list_npc}.
	 * @param ctx the parse tree
	 */
	void exitPar_npc_state(AVScenariosParser.Par_npc_stateContext ctx);
	/**
	 * Enter a parse tree produced by the {@code par_npc_state_vehicle}
	 * labeled alternative in {@link AVScenariosParser#parameter_list_npc}.
	 * @param ctx the parse tree
	 */
	void enterPar_npc_state_vehicle(AVScenariosParser.Par_npc_state_vehicleContext ctx);
	/**
	 * Exit a parse tree produced by the {@code par_npc_state_vehicle}
	 * labeled alternative in {@link AVScenariosParser#parameter_list_npc}.
	 * @param ctx the parse tree
	 */
	void exitPar_npc_state_vehicle(AVScenariosParser.Par_npc_state_vehicleContext ctx);
	/**
	 * Enter a parse tree produced by the {@code par_npc_state_vehicle_state}
	 * labeled alternative in {@link AVScenariosParser#parameter_list_npc}.
	 * @param ctx the parse tree
	 */
	void enterPar_npc_state_vehicle_state(AVScenariosParser.Par_npc_state_vehicle_stateContext ctx);
	/**
	 * Exit a parse tree produced by the {@code par_npc_state_vehicle_state}
	 * labeled alternative in {@link AVScenariosParser#parameter_list_npc}.
	 * @param ctx the parse tree
	 */
	void exitPar_npc_state_vehicle_state(AVScenariosParser.Par_npc_state_vehicle_stateContext ctx);
	/**
	 * Enter a parse tree produced by the {@code vehicle_vehicle_motion}
	 * labeled alternative in {@link AVScenariosParser#vehicle_motion_parameter}.
	 * @param ctx the parse tree
	 */
	void enterVehicle_vehicle_motion(AVScenariosParser.Vehicle_vehicle_motionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code vehicle_vehicle_motion}
	 * labeled alternative in {@link AVScenariosParser#vehicle_motion_parameter}.
	 * @param ctx the parse tree
	 */
	void exitVehicle_vehicle_motion(AVScenariosParser.Vehicle_vehicle_motionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code vehicle_vehicle_motion_var}
	 * labeled alternative in {@link AVScenariosParser#vehicle_motion_parameter}.
	 * @param ctx the parse tree
	 */
	void enterVehicle_vehicle_motion_var(AVScenariosParser.Vehicle_vehicle_motion_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code vehicle_vehicle_motion_var}
	 * labeled alternative in {@link AVScenariosParser#vehicle_motion_parameter}.
	 * @param ctx the parse tree
	 */
	void exitVehicle_vehicle_motion_var(AVScenariosParser.Vehicle_vehicle_motion_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code vehicle_motion_uniform}
	 * labeled alternative in {@link AVScenariosParser#vehicle_motion}.
	 * @param ctx the parse tree
	 */
	void enterVehicle_motion_uniform(AVScenariosParser.Vehicle_motion_uniformContext ctx);
	/**
	 * Exit a parse tree produced by the {@code vehicle_motion_uniform}
	 * labeled alternative in {@link AVScenariosParser#vehicle_motion}.
	 * @param ctx the parse tree
	 */
	void exitVehicle_motion_uniform(AVScenariosParser.Vehicle_motion_uniformContext ctx);
	/**
	 * Enter a parse tree produced by the {@code vehicle_motion_waypoint}
	 * labeled alternative in {@link AVScenariosParser#vehicle_motion}.
	 * @param ctx the parse tree
	 */
	void enterVehicle_motion_waypoint(AVScenariosParser.Vehicle_motion_waypointContext ctx);
	/**
	 * Exit a parse tree produced by the {@code vehicle_motion_waypoint}
	 * labeled alternative in {@link AVScenariosParser#vehicle_motion}.
	 * @param ctx the parse tree
	 */
	void exitVehicle_motion_waypoint(AVScenariosParser.Vehicle_motion_waypointContext ctx);
	/**
	 * Enter a parse tree produced by the {@code uniform}
	 * labeled alternative in {@link AVScenariosParser#uniform_motion}.
	 * @param ctx the parse tree
	 */
	void enterUniform(AVScenariosParser.UniformContext ctx);
	/**
	 * Exit a parse tree produced by the {@code uniform}
	 * labeled alternative in {@link AVScenariosParser#uniform_motion}.
	 * @param ctx the parse tree
	 */
	void exitUniform(AVScenariosParser.UniformContext ctx);
	/**
	 * Enter a parse tree produced by the {@code uniform_uniform}
	 * labeled alternative in {@link AVScenariosParser#uniform_index}.
	 * @param ctx the parse tree
	 */
	void enterUniform_uniform(AVScenariosParser.Uniform_uniformContext ctx);
	/**
	 * Exit a parse tree produced by the {@code uniform_uniform}
	 * labeled alternative in {@link AVScenariosParser#uniform_index}.
	 * @param ctx the parse tree
	 */
	void exitUniform_uniform(AVScenariosParser.Uniform_uniformContext ctx);
	/**
	 * Enter a parse tree produced by the {@code uniform_Uniform}
	 * labeled alternative in {@link AVScenariosParser#uniform_index}.
	 * @param ctx the parse tree
	 */
	void enterUniform_Uniform(AVScenariosParser.Uniform_UniformContext ctx);
	/**
	 * Exit a parse tree produced by the {@code uniform_Uniform}
	 * labeled alternative in {@link AVScenariosParser#uniform_index}.
	 * @param ctx the parse tree
	 */
	void exitUniform_Uniform(AVScenariosParser.Uniform_UniformContext ctx);
	/**
	 * Enter a parse tree produced by the {@code waypoint}
	 * labeled alternative in {@link AVScenariosParser#waypoint_motion}.
	 * @param ctx the parse tree
	 */
	void enterWaypoint(AVScenariosParser.WaypointContext ctx);
	/**
	 * Exit a parse tree produced by the {@code waypoint}
	 * labeled alternative in {@link AVScenariosParser#waypoint_motion}.
	 * @param ctx the parse tree
	 */
	void exitWaypoint(AVScenariosParser.WaypointContext ctx);
	/**
	 * Enter a parse tree produced by the {@code state_state_list_var}
	 * labeled alternative in {@link AVScenariosParser#state_list_parameter}.
	 * @param ctx the parse tree
	 */
	void enterState_state_list_var(AVScenariosParser.State_state_list_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code state_state_list_var}
	 * labeled alternative in {@link AVScenariosParser#state_list_parameter}.
	 * @param ctx the parse tree
	 */
	void exitState_state_list_var(AVScenariosParser.State_state_list_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code state_state_list}
	 * labeled alternative in {@link AVScenariosParser#state_list_parameter}.
	 * @param ctx the parse tree
	 */
	void enterState_state_list(AVScenariosParser.State_state_listContext ctx);
	/**
	 * Exit a parse tree produced by the {@code state_state_list}
	 * labeled alternative in {@link AVScenariosParser#state_list_parameter}.
	 * @param ctx the parse tree
	 */
	void exitState_state_list(AVScenariosParser.State_state_listContext ctx);
	/**
	 * Enter a parse tree produced by the {@code state_list_multi}
	 * labeled alternative in {@link AVScenariosParser#state_list}.
	 * @param ctx the parse tree
	 */
	void enterState_list_multi(AVScenariosParser.State_list_multiContext ctx);
	/**
	 * Exit a parse tree produced by the {@code state_list_multi}
	 * labeled alternative in {@link AVScenariosParser#state_list}.
	 * @param ctx the parse tree
	 */
	void exitState_list_multi(AVScenariosParser.State_list_multiContext ctx);
	/**
	 * Enter a parse tree produced by the {@code multi_states_par}
	 * labeled alternative in {@link AVScenariosParser#multi_states}.
	 * @param ctx the parse tree
	 */
	void enterMulti_states_par(AVScenariosParser.Multi_states_parContext ctx);
	/**
	 * Exit a parse tree produced by the {@code multi_states_par}
	 * labeled alternative in {@link AVScenariosParser#multi_states}.
	 * @param ctx the parse tree
	 */
	void exitMulti_states_par(AVScenariosParser.Multi_states_parContext ctx);
	/**
	 * Enter a parse tree produced by the {@code multi_states_par_state}
	 * labeled alternative in {@link AVScenariosParser#multi_states}.
	 * @param ctx the parse tree
	 */
	void enterMulti_states_par_state(AVScenariosParser.Multi_states_par_stateContext ctx);
	/**
	 * Exit a parse tree produced by the {@code multi_states_par_state}
	 * labeled alternative in {@link AVScenariosParser#multi_states}.
	 * @param ctx the parse tree
	 */
	void exitMulti_states_par_state(AVScenariosParser.Multi_states_par_stateContext ctx);
	/**
	 * Enter a parse tree produced by the {@code waypoint_Waypoint}
	 * labeled alternative in {@link AVScenariosParser#waypoint_index}.
	 * @param ctx the parse tree
	 */
	void enterWaypoint_Waypoint(AVScenariosParser.Waypoint_WaypointContext ctx);
	/**
	 * Exit a parse tree produced by the {@code waypoint_Waypoint}
	 * labeled alternative in {@link AVScenariosParser#waypoint_index}.
	 * @param ctx the parse tree
	 */
	void exitWaypoint_Waypoint(AVScenariosParser.Waypoint_WaypointContext ctx);
	/**
	 * Enter a parse tree produced by the {@code waypoint_W}
	 * labeled alternative in {@link AVScenariosParser#waypoint_index}.
	 * @param ctx the parse tree
	 */
	void enterWaypoint_W(AVScenariosParser.Waypoint_WContext ctx);
	/**
	 * Exit a parse tree produced by the {@code waypoint_W}
	 * labeled alternative in {@link AVScenariosParser#waypoint_index}.
	 * @param ctx the parse tree
	 */
	void exitWaypoint_W(AVScenariosParser.Waypoint_WContext ctx);
	/**
	 * Enter a parse tree produced by the {@code waypoint_WP}
	 * labeled alternative in {@link AVScenariosParser#waypoint_index}.
	 * @param ctx the parse tree
	 */
	void enterWaypoint_WP(AVScenariosParser.Waypoint_WPContext ctx);
	/**
	 * Exit a parse tree produced by the {@code waypoint_WP}
	 * labeled alternative in {@link AVScenariosParser#waypoint_index}.
	 * @param ctx the parse tree
	 */
	void exitWaypoint_WP(AVScenariosParser.Waypoint_WPContext ctx);
	/**
	 * Enter a parse tree produced by the {@code waypoint_waypoint}
	 * labeled alternative in {@link AVScenariosParser#waypoint_index}.
	 * @param ctx the parse tree
	 */
	void enterWaypoint_waypoint(AVScenariosParser.Waypoint_waypointContext ctx);
	/**
	 * Exit a parse tree produced by the {@code waypoint_waypoint}
	 * labeled alternative in {@link AVScenariosParser#waypoint_index}.
	 * @param ctx the parse tree
	 */
	void exitWaypoint_waypoint(AVScenariosParser.Waypoint_waypointContext ctx);
	/**
	 * Enter a parse tree produced by the {@code waypoint_w}
	 * labeled alternative in {@link AVScenariosParser#waypoint_index}.
	 * @param ctx the parse tree
	 */
	void enterWaypoint_w(AVScenariosParser.Waypoint_wContext ctx);
	/**
	 * Exit a parse tree produced by the {@code waypoint_w}
	 * labeled alternative in {@link AVScenariosParser#waypoint_index}.
	 * @param ctx the parse tree
	 */
	void exitWaypoint_w(AVScenariosParser.Waypoint_wContext ctx);
	/**
	 * Enter a parse tree produced by the {@code waypoint_wp}
	 * labeled alternative in {@link AVScenariosParser#waypoint_index}.
	 * @param ctx the parse tree
	 */
	void enterWaypoint_wp(AVScenariosParser.Waypoint_wpContext ctx);
	/**
	 * Exit a parse tree produced by the {@code waypoint_wp}
	 * labeled alternative in {@link AVScenariosParser#waypoint_index}.
	 * @param ctx the parse tree
	 */
	void exitWaypoint_wp(AVScenariosParser.Waypoint_wpContext ctx);
	/**
	 * Enter a parse tree produced by the {@code pedestrians_multi}
	 * labeled alternative in {@link AVScenariosParser#pedestrians}.
	 * @param ctx the parse tree
	 */
	void enterPedestrians_multi(AVScenariosParser.Pedestrians_multiContext ctx);
	/**
	 * Exit a parse tree produced by the {@code pedestrians_multi}
	 * labeled alternative in {@link AVScenariosParser#pedestrians}.
	 * @param ctx the parse tree
	 */
	void exitPedestrians_multi(AVScenariosParser.Pedestrians_multiContext ctx);
	/**
	 * Enter a parse tree produced by the {@code multi_multi_pedestrian}
	 * labeled alternative in {@link AVScenariosParser#multiple_pedestrians}.
	 * @param ctx the parse tree
	 */
	void enterMulti_multi_pedestrian(AVScenariosParser.Multi_multi_pedestrianContext ctx);
	/**
	 * Exit a parse tree produced by the {@code multi_multi_pedestrian}
	 * labeled alternative in {@link AVScenariosParser#multiple_pedestrians}.
	 * @param ctx the parse tree
	 */
	void exitMulti_multi_pedestrian(AVScenariosParser.Multi_multi_pedestrianContext ctx);
	/**
	 * Enter a parse tree produced by the {@code multi_pedestrian}
	 * labeled alternative in {@link AVScenariosParser#multiple_pedestrians}.
	 * @param ctx the parse tree
	 */
	void enterMulti_pedestrian(AVScenariosParser.Multi_pedestrianContext ctx);
	/**
	 * Exit a parse tree produced by the {@code multi_pedestrian}
	 * labeled alternative in {@link AVScenariosParser#multiple_pedestrians}.
	 * @param ctx the parse tree
	 */
	void exitMulti_pedestrian(AVScenariosParser.Multi_pedestrianContext ctx);
	/**
	 * Enter a parse tree produced by the {@code pedestrian_pedestrian}
	 * labeled alternative in {@link AVScenariosParser#pedestrian_parameter}.
	 * @param ctx the parse tree
	 */
	void enterPedestrian_pedestrian(AVScenariosParser.Pedestrian_pedestrianContext ctx);
	/**
	 * Exit a parse tree produced by the {@code pedestrian_pedestrian}
	 * labeled alternative in {@link AVScenariosParser#pedestrian_parameter}.
	 * @param ctx the parse tree
	 */
	void exitPedestrian_pedestrian(AVScenariosParser.Pedestrian_pedestrianContext ctx);
	/**
	 * Enter a parse tree produced by the {@code pedestrian_pedestrian_var}
	 * labeled alternative in {@link AVScenariosParser#pedestrian_parameter}.
	 * @param ctx the parse tree
	 */
	void enterPedestrian_pedestrian_var(AVScenariosParser.Pedestrian_pedestrian_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code pedestrian_pedestrian_var}
	 * labeled alternative in {@link AVScenariosParser#pedestrian_parameter}.
	 * @param ctx the parse tree
	 */
	void exitPedestrian_pedestrian_var(AVScenariosParser.Pedestrian_pedestrian_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code pedestrian_par}
	 * labeled alternative in {@link AVScenariosParser#pedestrian}.
	 * @param ctx the parse tree
	 */
	void enterPedestrian_par(AVScenariosParser.Pedestrian_parContext ctx);
	/**
	 * Exit a parse tree produced by the {@code pedestrian_par}
	 * labeled alternative in {@link AVScenariosParser#pedestrian}.
	 * @param ctx the parse tree
	 */
	void exitPedestrian_par(AVScenariosParser.Pedestrian_parContext ctx);
	/**
	 * Enter a parse tree produced by the {@code par_ped_state}
	 * labeled alternative in {@link AVScenariosParser#parameter_list_ped}.
	 * @param ctx the parse tree
	 */
	void enterPar_ped_state(AVScenariosParser.Par_ped_stateContext ctx);
	/**
	 * Exit a parse tree produced by the {@code par_ped_state}
	 * labeled alternative in {@link AVScenariosParser#parameter_list_ped}.
	 * @param ctx the parse tree
	 */
	void exitPar_ped_state(AVScenariosParser.Par_ped_stateContext ctx);
	/**
	 * Enter a parse tree produced by the {@code par_ped_state_ped}
	 * labeled alternative in {@link AVScenariosParser#parameter_list_ped}.
	 * @param ctx the parse tree
	 */
	void enterPar_ped_state_ped(AVScenariosParser.Par_ped_state_pedContext ctx);
	/**
	 * Exit a parse tree produced by the {@code par_ped_state_ped}
	 * labeled alternative in {@link AVScenariosParser#parameter_list_ped}.
	 * @param ctx the parse tree
	 */
	void exitPar_ped_state_ped(AVScenariosParser.Par_ped_state_pedContext ctx);
	/**
	 * Enter a parse tree produced by the {@code par_ped_state_ped_state}
	 * labeled alternative in {@link AVScenariosParser#parameter_list_ped}.
	 * @param ctx the parse tree
	 */
	void enterPar_ped_state_ped_state(AVScenariosParser.Par_ped_state_ped_stateContext ctx);
	/**
	 * Exit a parse tree produced by the {@code par_ped_state_ped_state}
	 * labeled alternative in {@link AVScenariosParser#parameter_list_ped}.
	 * @param ctx the parse tree
	 */
	void exitPar_ped_state_ped_state(AVScenariosParser.Par_ped_state_ped_stateContext ctx);
	/**
	 * Enter a parse tree produced by the {@code pedestrian_motion_pedestrian}
	 * labeled alternative in {@link AVScenariosParser#pedestrian_motion_parameter}.
	 * @param ctx the parse tree
	 */
	void enterPedestrian_motion_pedestrian(AVScenariosParser.Pedestrian_motion_pedestrianContext ctx);
	/**
	 * Exit a parse tree produced by the {@code pedestrian_motion_pedestrian}
	 * labeled alternative in {@link AVScenariosParser#pedestrian_motion_parameter}.
	 * @param ctx the parse tree
	 */
	void exitPedestrian_motion_pedestrian(AVScenariosParser.Pedestrian_motion_pedestrianContext ctx);
	/**
	 * Enter a parse tree produced by the {@code pedestrian_motion_pedestrian_var}
	 * labeled alternative in {@link AVScenariosParser#pedestrian_motion_parameter}.
	 * @param ctx the parse tree
	 */
	void enterPedestrian_motion_pedestrian_var(AVScenariosParser.Pedestrian_motion_pedestrian_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code pedestrian_motion_pedestrian_var}
	 * labeled alternative in {@link AVScenariosParser#pedestrian_motion_parameter}.
	 * @param ctx the parse tree
	 */
	void exitPedestrian_motion_pedestrian_var(AVScenariosParser.Pedestrian_motion_pedestrian_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code pedestrian_uniform}
	 * labeled alternative in {@link AVScenariosParser#pedestrian_motion}.
	 * @param ctx the parse tree
	 */
	void enterPedestrian_uniform(AVScenariosParser.Pedestrian_uniformContext ctx);
	/**
	 * Exit a parse tree produced by the {@code pedestrian_uniform}
	 * labeled alternative in {@link AVScenariosParser#pedestrian_motion}.
	 * @param ctx the parse tree
	 */
	void exitPedestrian_uniform(AVScenariosParser.Pedestrian_uniformContext ctx);
	/**
	 * Enter a parse tree produced by the {@code pedestrian_waypoint}
	 * labeled alternative in {@link AVScenariosParser#pedestrian_motion}.
	 * @param ctx the parse tree
	 */
	void enterPedestrian_waypoint(AVScenariosParser.Pedestrian_waypointContext ctx);
	/**
	 * Exit a parse tree produced by the {@code pedestrian_waypoint}
	 * labeled alternative in {@link AVScenariosParser#pedestrian_motion}.
	 * @param ctx the parse tree
	 */
	void exitPedestrian_waypoint(AVScenariosParser.Pedestrian_waypointContext ctx);
	/**
	 * Enter a parse tree produced by the {@code pedestrian_pedestrian_type}
	 * labeled alternative in {@link AVScenariosParser#pedestrian_type_parameter}.
	 * @param ctx the parse tree
	 */
	void enterPedestrian_pedestrian_type(AVScenariosParser.Pedestrian_pedestrian_typeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code pedestrian_pedestrian_type}
	 * labeled alternative in {@link AVScenariosParser#pedestrian_type_parameter}.
	 * @param ctx the parse tree
	 */
	void exitPedestrian_pedestrian_type(AVScenariosParser.Pedestrian_pedestrian_typeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code pedestrian_pedestrian_type_var}
	 * labeled alternative in {@link AVScenariosParser#pedestrian_type_parameter}.
	 * @param ctx the parse tree
	 */
	void enterPedestrian_pedestrian_type_var(AVScenariosParser.Pedestrian_pedestrian_type_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code pedestrian_pedestrian_type_var}
	 * labeled alternative in {@link AVScenariosParser#pedestrian_type_parameter}.
	 * @param ctx the parse tree
	 */
	void exitPedestrian_pedestrian_type_var(AVScenariosParser.Pedestrian_pedestrian_type_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code pedestrian_type_name}
	 * labeled alternative in {@link AVScenariosParser#pedestrian_type_parameter}.
	 * @param ctx the parse tree
	 */
	void enterPedestrian_type_name(AVScenariosParser.Pedestrian_type_nameContext ctx);
	/**
	 * Exit a parse tree produced by the {@code pedestrian_type_name}
	 * labeled alternative in {@link AVScenariosParser#pedestrian_type_parameter}.
	 * @param ctx the parse tree
	 */
	void exitPedestrian_type_name(AVScenariosParser.Pedestrian_type_nameContext ctx);
	/**
	 * Enter a parse tree produced by the {@code pedestrian_type_height_color}
	 * labeled alternative in {@link AVScenariosParser#pedestrian_type}.
	 * @param ctx the parse tree
	 */
	void enterPedestrian_type_height_color(AVScenariosParser.Pedestrian_type_height_colorContext ctx);
	/**
	 * Exit a parse tree produced by the {@code pedestrian_type_height_color}
	 * labeled alternative in {@link AVScenariosParser#pedestrian_type}.
	 * @param ctx the parse tree
	 */
	void exitPedestrian_type_height_color(AVScenariosParser.Pedestrian_type_height_colorContext ctx);
	/**
	 * Enter a parse tree produced by the {@code height_var}
	 * labeled alternative in {@link AVScenariosParser#height_parameter}.
	 * @param ctx the parse tree
	 */
	void enterHeight_var(AVScenariosParser.Height_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code height_var}
	 * labeled alternative in {@link AVScenariosParser#height_parameter}.
	 * @param ctx the parse tree
	 */
	void exitHeight_var(AVScenariosParser.Height_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code height_height}
	 * labeled alternative in {@link AVScenariosParser#height_parameter}.
	 * @param ctx the parse tree
	 */
	void enterHeight_height(AVScenariosParser.Height_heightContext ctx);
	/**
	 * Exit a parse tree produced by the {@code height_height}
	 * labeled alternative in {@link AVScenariosParser#height_parameter}.
	 * @param ctx the parse tree
	 */
	void exitHeight_height(AVScenariosParser.Height_heightContext ctx);
	/**
	 * Enter a parse tree produced by the {@code height_rv}
	 * labeled alternative in {@link AVScenariosParser#height}.
	 * @param ctx the parse tree
	 */
	void enterHeight_rv(AVScenariosParser.Height_rvContext ctx);
	/**
	 * Exit a parse tree produced by the {@code height_rv}
	 * labeled alternative in {@link AVScenariosParser#height}.
	 * @param ctx the parse tree
	 */
	void exitHeight_rv(AVScenariosParser.Height_rvContext ctx);
	/**
	 * Enter a parse tree produced by the {@code obstacles_multi}
	 * labeled alternative in {@link AVScenariosParser#obstacles}.
	 * @param ctx the parse tree
	 */
	void enterObstacles_multi(AVScenariosParser.Obstacles_multiContext ctx);
	/**
	 * Exit a parse tree produced by the {@code obstacles_multi}
	 * labeled alternative in {@link AVScenariosParser#obstacles}.
	 * @param ctx the parse tree
	 */
	void exitObstacles_multi(AVScenariosParser.Obstacles_multiContext ctx);
	/**
	 * Enter a parse tree produced by the {@code obstacles_obstacle}
	 * labeled alternative in {@link AVScenariosParser#multiple_obstacles}.
	 * @param ctx the parse tree
	 */
	void enterObstacles_obstacle(AVScenariosParser.Obstacles_obstacleContext ctx);
	/**
	 * Exit a parse tree produced by the {@code obstacles_obstacle}
	 * labeled alternative in {@link AVScenariosParser#multiple_obstacles}.
	 * @param ctx the parse tree
	 */
	void exitObstacles_obstacle(AVScenariosParser.Obstacles_obstacleContext ctx);
	/**
	 * Enter a parse tree produced by the {@code obstacles_multi_obstacle}
	 * labeled alternative in {@link AVScenariosParser#multiple_obstacles}.
	 * @param ctx the parse tree
	 */
	void enterObstacles_multi_obstacle(AVScenariosParser.Obstacles_multi_obstacleContext ctx);
	/**
	 * Exit a parse tree produced by the {@code obstacles_multi_obstacle}
	 * labeled alternative in {@link AVScenariosParser#multiple_obstacles}.
	 * @param ctx the parse tree
	 */
	void exitObstacles_multi_obstacle(AVScenariosParser.Obstacles_multi_obstacleContext ctx);
	/**
	 * Enter a parse tree produced by the {@code obstacle_obstacle}
	 * labeled alternative in {@link AVScenariosParser#obstacle_parameter}.
	 * @param ctx the parse tree
	 */
	void enterObstacle_obstacle(AVScenariosParser.Obstacle_obstacleContext ctx);
	/**
	 * Exit a parse tree produced by the {@code obstacle_obstacle}
	 * labeled alternative in {@link AVScenariosParser#obstacle_parameter}.
	 * @param ctx the parse tree
	 */
	void exitObstacle_obstacle(AVScenariosParser.Obstacle_obstacleContext ctx);
	/**
	 * Enter a parse tree produced by the {@code obstacle_obstacle_var}
	 * labeled alternative in {@link AVScenariosParser#obstacle_parameter}.
	 * @param ctx the parse tree
	 */
	void enterObstacle_obstacle_var(AVScenariosParser.Obstacle_obstacle_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code obstacle_obstacle_var}
	 * labeled alternative in {@link AVScenariosParser#obstacle_parameter}.
	 * @param ctx the parse tree
	 */
	void exitObstacle_obstacle_var(AVScenariosParser.Obstacle_obstacle_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code obstacle_para}
	 * labeled alternative in {@link AVScenariosParser#obstacle}.
	 * @param ctx the parse tree
	 */
	void enterObstacle_para(AVScenariosParser.Obstacle_paraContext ctx);
	/**
	 * Exit a parse tree produced by the {@code obstacle_para}
	 * labeled alternative in {@link AVScenariosParser#obstacle}.
	 * @param ctx the parse tree
	 */
	void exitObstacle_para(AVScenariosParser.Obstacle_paraContext ctx);
	/**
	 * Enter a parse tree produced by the {@code par_position_shape}
	 * labeled alternative in {@link AVScenariosParser#parameter_list_obs}.
	 * @param ctx the parse tree
	 */
	void enterPar_position_shape(AVScenariosParser.Par_position_shapeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code par_position_shape}
	 * labeled alternative in {@link AVScenariosParser#parameter_list_obs}.
	 * @param ctx the parse tree
	 */
	void exitPar_position_shape(AVScenariosParser.Par_position_shapeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code shape_shape_var}
	 * labeled alternative in {@link AVScenariosParser#shape_parameter}.
	 * @param ctx the parse tree
	 */
	void enterShape_shape_var(AVScenariosParser.Shape_shape_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code shape_shape_var}
	 * labeled alternative in {@link AVScenariosParser#shape_parameter}.
	 * @param ctx the parse tree
	 */
	void exitShape_shape_var(AVScenariosParser.Shape_shape_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code shape_shape}
	 * labeled alternative in {@link AVScenariosParser#shape_parameter}.
	 * @param ctx the parse tree
	 */
	void enterShape_shape(AVScenariosParser.Shape_shapeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code shape_shape}
	 * labeled alternative in {@link AVScenariosParser#shape_parameter}.
	 * @param ctx the parse tree
	 */
	void exitShape_shape(AVScenariosParser.Shape_shapeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code shape_sphere}
	 * labeled alternative in {@link AVScenariosParser#shape}.
	 * @param ctx the parse tree
	 */
	void enterShape_sphere(AVScenariosParser.Shape_sphereContext ctx);
	/**
	 * Exit a parse tree produced by the {@code shape_sphere}
	 * labeled alternative in {@link AVScenariosParser#shape}.
	 * @param ctx the parse tree
	 */
	void exitShape_sphere(AVScenariosParser.Shape_sphereContext ctx);
	/**
	 * Enter a parse tree produced by the {@code shape_box}
	 * labeled alternative in {@link AVScenariosParser#shape}.
	 * @param ctx the parse tree
	 */
	void enterShape_box(AVScenariosParser.Shape_boxContext ctx);
	/**
	 * Exit a parse tree produced by the {@code shape_box}
	 * labeled alternative in {@link AVScenariosParser#shape}.
	 * @param ctx the parse tree
	 */
	void exitShape_box(AVScenariosParser.Shape_boxContext ctx);
	/**
	 * Enter a parse tree produced by the {@code shape_cone}
	 * labeled alternative in {@link AVScenariosParser#shape}.
	 * @param ctx the parse tree
	 */
	void enterShape_cone(AVScenariosParser.Shape_coneContext ctx);
	/**
	 * Exit a parse tree produced by the {@code shape_cone}
	 * labeled alternative in {@link AVScenariosParser#shape}.
	 * @param ctx the parse tree
	 */
	void exitShape_cone(AVScenariosParser.Shape_coneContext ctx);
	/**
	 * Enter a parse tree produced by the {@code shape_cylinder}
	 * labeled alternative in {@link AVScenariosParser#shape}.
	 * @param ctx the parse tree
	 */
	void enterShape_cylinder(AVScenariosParser.Shape_cylinderContext ctx);
	/**
	 * Exit a parse tree produced by the {@code shape_cylinder}
	 * labeled alternative in {@link AVScenariosParser#shape}.
	 * @param ctx the parse tree
	 */
	void exitShape_cylinder(AVScenariosParser.Shape_cylinderContext ctx);
	/**
	 * Enter a parse tree produced by the {@code sphere_sphere}
	 * labeled alternative in {@link AVScenariosParser#sphere}.
	 * @param ctx the parse tree
	 */
	void enterSphere_sphere(AVScenariosParser.Sphere_sphereContext ctx);
	/**
	 * Exit a parse tree produced by the {@code sphere_sphere}
	 * labeled alternative in {@link AVScenariosParser#sphere}.
	 * @param ctx the parse tree
	 */
	void exitSphere_sphere(AVScenariosParser.Sphere_sphereContext ctx);
	/**
	 * Enter a parse tree produced by the {@code box_box}
	 * labeled alternative in {@link AVScenariosParser#box}.
	 * @param ctx the parse tree
	 */
	void enterBox_box(AVScenariosParser.Box_boxContext ctx);
	/**
	 * Exit a parse tree produced by the {@code box_box}
	 * labeled alternative in {@link AVScenariosParser#box}.
	 * @param ctx the parse tree
	 */
	void exitBox_box(AVScenariosParser.Box_boxContext ctx);
	/**
	 * Enter a parse tree produced by the {@code cone_cone}
	 * labeled alternative in {@link AVScenariosParser#cone}.
	 * @param ctx the parse tree
	 */
	void enterCone_cone(AVScenariosParser.Cone_coneContext ctx);
	/**
	 * Exit a parse tree produced by the {@code cone_cone}
	 * labeled alternative in {@link AVScenariosParser#cone}.
	 * @param ctx the parse tree
	 */
	void exitCone_cone(AVScenariosParser.Cone_coneContext ctx);
	/**
	 * Enter a parse tree produced by the {@code cylinder_cylinder}
	 * labeled alternative in {@link AVScenariosParser#cylinder}.
	 * @param ctx the parse tree
	 */
	void enterCylinder_cylinder(AVScenariosParser.Cylinder_cylinderContext ctx);
	/**
	 * Exit a parse tree produced by the {@code cylinder_cylinder}
	 * labeled alternative in {@link AVScenariosParser#cylinder}.
	 * @param ctx the parse tree
	 */
	void exitCylinder_cylinder(AVScenariosParser.Cylinder_cylinderContext ctx);
	/**
	 * Enter a parse tree produced by the {@code env_var}
	 * labeled alternative in {@link AVScenariosParser#env_parameter}.
	 * @param ctx the parse tree
	 */
	void enterEnv_var(AVScenariosParser.Env_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code env_var}
	 * labeled alternative in {@link AVScenariosParser#env_parameter}.
	 * @param ctx the parse tree
	 */
	void exitEnv_var(AVScenariosParser.Env_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code env_env}
	 * labeled alternative in {@link AVScenariosParser#env_parameter}.
	 * @param ctx the parse tree
	 */
	void enterEnv_env(AVScenariosParser.Env_envContext ctx);
	/**
	 * Exit a parse tree produced by the {@code env_env}
	 * labeled alternative in {@link AVScenariosParser#env_parameter}.
	 * @param ctx the parse tree
	 */
	void exitEnv_env(AVScenariosParser.Env_envContext ctx);
	/**
	 * Enter a parse tree produced by the {@code env_empty}
	 * labeled alternative in {@link AVScenariosParser#env_parameter}.
	 * @param ctx the parse tree
	 */
	void enterEnv_empty(AVScenariosParser.Env_emptyContext ctx);
	/**
	 * Exit a parse tree produced by the {@code env_empty}
	 * labeled alternative in {@link AVScenariosParser#env_parameter}.
	 * @param ctx the parse tree
	 */
	void exitEnv_empty(AVScenariosParser.Env_emptyContext ctx);
	/**
	 * Enter a parse tree produced by the {@code env_par}
	 * labeled alternative in {@link AVScenariosParser#env}.
	 * @param ctx the parse tree
	 */
	void enterEnv_par(AVScenariosParser.Env_parContext ctx);
	/**
	 * Exit a parse tree produced by the {@code env_par}
	 * labeled alternative in {@link AVScenariosParser#env}.
	 * @param ctx the parse tree
	 */
	void exitEnv_par(AVScenariosParser.Env_parContext ctx);
	/**
	 * Enter a parse tree produced by the {@code par_time_weather}
	 * labeled alternative in {@link AVScenariosParser#parameter_list_env}.
	 * @param ctx the parse tree
	 */
	void enterPar_time_weather(AVScenariosParser.Par_time_weatherContext ctx);
	/**
	 * Exit a parse tree produced by the {@code par_time_weather}
	 * labeled alternative in {@link AVScenariosParser#parameter_list_env}.
	 * @param ctx the parse tree
	 */
	void exitPar_time_weather(AVScenariosParser.Par_time_weatherContext ctx);
	/**
	 * Enter a parse tree produced by the {@code weather_var}
	 * labeled alternative in {@link AVScenariosParser#weather_parameter}.
	 * @param ctx the parse tree
	 */
	void enterWeather_var(AVScenariosParser.Weather_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code weather_var}
	 * labeled alternative in {@link AVScenariosParser#weather_parameter}.
	 * @param ctx the parse tree
	 */
	void exitWeather_var(AVScenariosParser.Weather_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code weather_wtr}
	 * labeled alternative in {@link AVScenariosParser#weather_parameter}.
	 * @param ctx the parse tree
	 */
	void enterWeather_wtr(AVScenariosParser.Weather_wtrContext ctx);
	/**
	 * Exit a parse tree produced by the {@code weather_wtr}
	 * labeled alternative in {@link AVScenariosParser#weather_parameter}.
	 * @param ctx the parse tree
	 */
	void exitWeather_wtr(AVScenariosParser.Weather_wtrContext ctx);
	/**
	 * Enter a parse tree produced by the {@code time_time}
	 * labeled alternative in {@link AVScenariosParser#time_parameter}.
	 * @param ctx the parse tree
	 */
	void enterTime_time(AVScenariosParser.Time_timeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code time_time}
	 * labeled alternative in {@link AVScenariosParser#time_parameter}.
	 * @param ctx the parse tree
	 */
	void exitTime_time(AVScenariosParser.Time_timeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code time_time_var}
	 * labeled alternative in {@link AVScenariosParser#time_parameter}.
	 * @param ctx the parse tree
	 */
	void enterTime_time_var(AVScenariosParser.Time_time_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code time_time_var}
	 * labeled alternative in {@link AVScenariosParser#time_parameter}.
	 * @param ctx the parse tree
	 */
	void exitTime_time_var(AVScenariosParser.Time_time_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code time_Time}
	 * labeled alternative in {@link AVScenariosParser#time}.
	 * @param ctx the parse tree
	 */
	void enterTime_Time(AVScenariosParser.Time_TimeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code time_Time}
	 * labeled alternative in {@link AVScenariosParser#time}.
	 * @param ctx the parse tree
	 */
	void exitTime_Time(AVScenariosParser.Time_TimeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code weathers}
	 * labeled alternative in {@link AVScenariosParser#weather}.
	 * @param ctx the parse tree
	 */
	void enterWeathers(AVScenariosParser.WeathersContext ctx);
	/**
	 * Exit a parse tree produced by the {@code weathers}
	 * labeled alternative in {@link AVScenariosParser#weather}.
	 * @param ctx the parse tree
	 */
	void exitWeathers(AVScenariosParser.WeathersContext ctx);
	/**
	 * Enter a parse tree produced by the {@code weathers_multi_weather}
	 * labeled alternative in {@link AVScenariosParser#multi_weathers}.
	 * @param ctx the parse tree
	 */
	void enterWeathers_multi_weather(AVScenariosParser.Weathers_multi_weatherContext ctx);
	/**
	 * Exit a parse tree produced by the {@code weathers_multi_weather}
	 * labeled alternative in {@link AVScenariosParser#multi_weathers}.
	 * @param ctx the parse tree
	 */
	void exitWeathers_multi_weather(AVScenariosParser.Weathers_multi_weatherContext ctx);
	/**
	 * Enter a parse tree produced by the {@code weathers_weather}
	 * labeled alternative in {@link AVScenariosParser#multi_weathers}.
	 * @param ctx the parse tree
	 */
	void enterWeathers_weather(AVScenariosParser.Weathers_weatherContext ctx);
	/**
	 * Exit a parse tree produced by the {@code weathers_weather}
	 * labeled alternative in {@link AVScenariosParser#multi_weathers}.
	 * @param ctx the parse tree
	 */
	void exitWeathers_weather(AVScenariosParser.Weathers_weatherContext ctx);
	/**
	 * Enter a parse tree produced by the {@code weather_weather_var}
	 * labeled alternative in {@link AVScenariosParser#weather_statement_parameter}.
	 * @param ctx the parse tree
	 */
	void enterWeather_weather_var(AVScenariosParser.Weather_weather_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code weather_weather_var}
	 * labeled alternative in {@link AVScenariosParser#weather_statement_parameter}.
	 * @param ctx the parse tree
	 */
	void exitWeather_weather_var(AVScenariosParser.Weather_weather_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code weather_weather}
	 * labeled alternative in {@link AVScenariosParser#weather_statement_parameter}.
	 * @param ctx the parse tree
	 */
	void enterWeather_weather(AVScenariosParser.Weather_weatherContext ctx);
	/**
	 * Exit a parse tree produced by the {@code weather_weather}
	 * labeled alternative in {@link AVScenariosParser#weather_statement_parameter}.
	 * @param ctx the parse tree
	 */
	void exitWeather_weather(AVScenariosParser.Weather_weatherContext ctx);
	/**
	 * Enter a parse tree produced by the {@code weather_continuous}
	 * labeled alternative in {@link AVScenariosParser#weather_statement}.
	 * @param ctx the parse tree
	 */
	void enterWeather_continuous(AVScenariosParser.Weather_continuousContext ctx);
	/**
	 * Exit a parse tree produced by the {@code weather_continuous}
	 * labeled alternative in {@link AVScenariosParser#weather_statement}.
	 * @param ctx the parse tree
	 */
	void exitWeather_continuous(AVScenariosParser.Weather_continuousContext ctx);
	/**
	 * Enter a parse tree produced by the {@code weather_discrete}
	 * labeled alternative in {@link AVScenariosParser#weather_statement}.
	 * @param ctx the parse tree
	 */
	void enterWeather_discrete(AVScenariosParser.Weather_discreteContext ctx);
	/**
	 * Exit a parse tree produced by the {@code weather_discrete}
	 * labeled alternative in {@link AVScenariosParser#weather_statement}.
	 * @param ctx the parse tree
	 */
	void exitWeather_discrete(AVScenariosParser.Weather_discreteContext ctx);
	/**
	 * Enter a parse tree produced by the {@code kind_sunny}
	 * labeled alternative in {@link AVScenariosParser#kind}.
	 * @param ctx the parse tree
	 */
	void enterKind_sunny(AVScenariosParser.Kind_sunnyContext ctx);
	/**
	 * Exit a parse tree produced by the {@code kind_sunny}
	 * labeled alternative in {@link AVScenariosParser#kind}.
	 * @param ctx the parse tree
	 */
	void exitKind_sunny(AVScenariosParser.Kind_sunnyContext ctx);
	/**
	 * Enter a parse tree produced by the {@code kind_rain}
	 * labeled alternative in {@link AVScenariosParser#kind}.
	 * @param ctx the parse tree
	 */
	void enterKind_rain(AVScenariosParser.Kind_rainContext ctx);
	/**
	 * Exit a parse tree produced by the {@code kind_rain}
	 * labeled alternative in {@link AVScenariosParser#kind}.
	 * @param ctx the parse tree
	 */
	void exitKind_rain(AVScenariosParser.Kind_rainContext ctx);
	/**
	 * Enter a parse tree produced by the {@code kind_snow}
	 * labeled alternative in {@link AVScenariosParser#kind}.
	 * @param ctx the parse tree
	 */
	void enterKind_snow(AVScenariosParser.Kind_snowContext ctx);
	/**
	 * Exit a parse tree produced by the {@code kind_snow}
	 * labeled alternative in {@link AVScenariosParser#kind}.
	 * @param ctx the parse tree
	 */
	void exitKind_snow(AVScenariosParser.Kind_snowContext ctx);
	/**
	 * Enter a parse tree produced by the {@code kind_fog}
	 * labeled alternative in {@link AVScenariosParser#kind}.
	 * @param ctx the parse tree
	 */
	void enterKind_fog(AVScenariosParser.Kind_fogContext ctx);
	/**
	 * Exit a parse tree produced by the {@code kind_fog}
	 * labeled alternative in {@link AVScenariosParser#kind}.
	 * @param ctx the parse tree
	 */
	void exitKind_fog(AVScenariosParser.Kind_fogContext ctx);
	/**
	 * Enter a parse tree produced by the {@code kind_wetness}
	 * labeled alternative in {@link AVScenariosParser#kind}.
	 * @param ctx the parse tree
	 */
	void enterKind_wetness(AVScenariosParser.Kind_wetnessContext ctx);
	/**
	 * Exit a parse tree produced by the {@code kind_wetness}
	 * labeled alternative in {@link AVScenariosParser#kind}.
	 * @param ctx the parse tree
	 */
	void exitKind_wetness(AVScenariosParser.Kind_wetnessContext ctx);
	/**
	 * Enter a parse tree produced by the {@code weather_continuous_value}
	 * labeled alternative in {@link AVScenariosParser#weather_continuous_index_parameter}.
	 * @param ctx the parse tree
	 */
	void enterWeather_continuous_value(AVScenariosParser.Weather_continuous_valueContext ctx);
	/**
	 * Exit a parse tree produced by the {@code weather_continuous_value}
	 * labeled alternative in {@link AVScenariosParser#weather_continuous_index_parameter}.
	 * @param ctx the parse tree
	 */
	void exitWeather_continuous_value(AVScenariosParser.Weather_continuous_valueContext ctx);
	/**
	 * Enter a parse tree produced by the {@code weather_continuous_var}
	 * labeled alternative in {@link AVScenariosParser#weather_continuous_index_parameter}.
	 * @param ctx the parse tree
	 */
	void enterWeather_continuous_var(AVScenariosParser.Weather_continuous_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code weather_continuous_var}
	 * labeled alternative in {@link AVScenariosParser#weather_continuous_index_parameter}.
	 * @param ctx the parse tree
	 */
	void exitWeather_continuous_var(AVScenariosParser.Weather_continuous_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code weather_discrete_level_par}
	 * labeled alternative in {@link AVScenariosParser#weather_discrete_level_parameter}.
	 * @param ctx the parse tree
	 */
	void enterWeather_discrete_level_par(AVScenariosParser.Weather_discrete_level_parContext ctx);
	/**
	 * Exit a parse tree produced by the {@code weather_discrete_level_par}
	 * labeled alternative in {@link AVScenariosParser#weather_discrete_level_parameter}.
	 * @param ctx the parse tree
	 */
	void exitWeather_discrete_level_par(AVScenariosParser.Weather_discrete_level_parContext ctx);
	/**
	 * Enter a parse tree produced by the {@code weather_discrete_var}
	 * labeled alternative in {@link AVScenariosParser#weather_discrete_level_parameter}.
	 * @param ctx the parse tree
	 */
	void enterWeather_discrete_var(AVScenariosParser.Weather_discrete_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code weather_discrete_var}
	 * labeled alternative in {@link AVScenariosParser#weather_discrete_level_parameter}.
	 * @param ctx the parse tree
	 */
	void exitWeather_discrete_var(AVScenariosParser.Weather_discrete_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code weather_discrete_light}
	 * labeled alternative in {@link AVScenariosParser#weather_discrete_level}.
	 * @param ctx the parse tree
	 */
	void enterWeather_discrete_light(AVScenariosParser.Weather_discrete_lightContext ctx);
	/**
	 * Exit a parse tree produced by the {@code weather_discrete_light}
	 * labeled alternative in {@link AVScenariosParser#weather_discrete_level}.
	 * @param ctx the parse tree
	 */
	void exitWeather_discrete_light(AVScenariosParser.Weather_discrete_lightContext ctx);
	/**
	 * Enter a parse tree produced by the {@code weather_discrete_middle}
	 * labeled alternative in {@link AVScenariosParser#weather_discrete_level}.
	 * @param ctx the parse tree
	 */
	void enterWeather_discrete_middle(AVScenariosParser.Weather_discrete_middleContext ctx);
	/**
	 * Exit a parse tree produced by the {@code weather_discrete_middle}
	 * labeled alternative in {@link AVScenariosParser#weather_discrete_level}.
	 * @param ctx the parse tree
	 */
	void exitWeather_discrete_middle(AVScenariosParser.Weather_discrete_middleContext ctx);
	/**
	 * Enter a parse tree produced by the {@code weather_discrete_heavy}
	 * labeled alternative in {@link AVScenariosParser#weather_discrete_level}.
	 * @param ctx the parse tree
	 */
	void enterWeather_discrete_heavy(AVScenariosParser.Weather_discrete_heavyContext ctx);
	/**
	 * Exit a parse tree produced by the {@code weather_discrete_heavy}
	 * labeled alternative in {@link AVScenariosParser#weather_discrete_level}.
	 * @param ctx the parse tree
	 */
	void exitWeather_discrete_heavy(AVScenariosParser.Weather_discrete_heavyContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_traffic}
	 * labeled alternative in {@link AVScenariosParser#traffic}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_traffic(AVScenariosParser.Traffic_trafficContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_traffic}
	 * labeled alternative in {@link AVScenariosParser#traffic}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_traffic(AVScenariosParser.Traffic_trafficContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_stmt}
	 * labeled alternative in {@link AVScenariosParser#traffic_statement}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_stmt(AVScenariosParser.Traffic_stmtContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_stmt}
	 * labeled alternative in {@link AVScenariosParser#traffic_statement}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_stmt(AVScenariosParser.Traffic_stmtContext ctx);
	/**
	 * Enter a parse tree produced by the {@code intersection}
	 * labeled alternative in {@link AVScenariosParser#intersection_traffic}.
	 * @param ctx the parse tree
	 */
	void enterIntersection(AVScenariosParser.IntersectionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code intersection}
	 * labeled alternative in {@link AVScenariosParser#intersection_traffic}.
	 * @param ctx the parse tree
	 */
	void exitIntersection(AVScenariosParser.IntersectionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code meta_intersection_meta_var}
	 * labeled alternative in {@link AVScenariosParser#meta_intersection_traffic_parameter}.
	 * @param ctx the parse tree
	 */
	void enterMeta_intersection_meta_var(AVScenariosParser.Meta_intersection_meta_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code meta_intersection_meta_var}
	 * labeled alternative in {@link AVScenariosParser#meta_intersection_traffic_parameter}.
	 * @param ctx the parse tree
	 */
	void exitMeta_intersection_meta_var(AVScenariosParser.Meta_intersection_meta_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code meta_intersection_meta}
	 * labeled alternative in {@link AVScenariosParser#meta_intersection_traffic_parameter}.
	 * @param ctx the parse tree
	 */
	void enterMeta_intersection_meta(AVScenariosParser.Meta_intersection_metaContext ctx);
	/**
	 * Exit a parse tree produced by the {@code meta_intersection_meta}
	 * labeled alternative in {@link AVScenariosParser#meta_intersection_traffic_parameter}.
	 * @param ctx the parse tree
	 */
	void exitMeta_intersection_meta(AVScenariosParser.Meta_intersection_metaContext ctx);
	/**
	 * Enter a parse tree produced by the {@code meta_intersection_intersection}
	 * labeled alternative in {@link AVScenariosParser#meta_intersection_traffic}.
	 * @param ctx the parse tree
	 */
	void enterMeta_intersection_intersection(AVScenariosParser.Meta_intersection_intersectionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code meta_intersection_intersection}
	 * labeled alternative in {@link AVScenariosParser#meta_intersection_traffic}.
	 * @param ctx the parse tree
	 */
	void exitMeta_intersection_intersection(AVScenariosParser.Meta_intersection_intersectionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code intersection_intersection}
	 * labeled alternative in {@link AVScenariosParser#intersection_ID_parameter}.
	 * @param ctx the parse tree
	 */
	void enterIntersection_intersection(AVScenariosParser.Intersection_intersectionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code intersection_intersection}
	 * labeled alternative in {@link AVScenariosParser#intersection_ID_parameter}.
	 * @param ctx the parse tree
	 */
	void exitIntersection_intersection(AVScenariosParser.Intersection_intersectionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code intersection_intersection_var}
	 * labeled alternative in {@link AVScenariosParser#intersection_ID_parameter}.
	 * @param ctx the parse tree
	 */
	void enterIntersection_intersection_var(AVScenariosParser.Intersection_intersection_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code intersection_intersection_var}
	 * labeled alternative in {@link AVScenariosParser#intersection_ID_parameter}.
	 * @param ctx the parse tree
	 */
	void exitIntersection_intersection_var(AVScenariosParser.Intersection_intersection_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code intersection_signal}
	 * labeled alternative in {@link AVScenariosParser#intersection_ID}.
	 * @param ctx the parse tree
	 */
	void enterIntersection_signal(AVScenariosParser.Intersection_signalContext ctx);
	/**
	 * Exit a parse tree produced by the {@code intersection_signal}
	 * labeled alternative in {@link AVScenariosParser#intersection_ID}.
	 * @param ctx the parse tree
	 */
	void exitIntersection_signal(AVScenariosParser.Intersection_signalContext ctx);
	/**
	 * Enter a parse tree produced by the {@code lane_lane_speed_limit}
	 * labeled alternative in {@link AVScenariosParser#lane_traffic}.
	 * @param ctx the parse tree
	 */
	void enterLane_lane_speed_limit(AVScenariosParser.Lane_lane_speed_limitContext ctx);
	/**
	 * Exit a parse tree produced by the {@code lane_lane_speed_limit}
	 * labeled alternative in {@link AVScenariosParser#lane_traffic}.
	 * @param ctx the parse tree
	 */
	void exitLane_lane_speed_limit(AVScenariosParser.Lane_lane_speed_limitContext ctx);
	/**
	 * Enter a parse tree produced by the {@code lane_speed_limit}
	 * labeled alternative in {@link AVScenariosParser#lane_traffic}.
	 * @param ctx the parse tree
	 */
	void enterLane_speed_limit(AVScenariosParser.Lane_speed_limitContext ctx);
	/**
	 * Exit a parse tree produced by the {@code lane_speed_limit}
	 * labeled alternative in {@link AVScenariosParser#lane_traffic}.
	 * @param ctx the parse tree
	 */
	void exitLane_speed_limit(AVScenariosParser.Lane_speed_limitContext ctx);
	/**
	 * Enter a parse tree produced by the {@code speed_limit}
	 * labeled alternative in {@link AVScenariosParser#speed_limitation_parameter}.
	 * @param ctx the parse tree
	 */
	void enterSpeed_limit(AVScenariosParser.Speed_limitContext ctx);
	/**
	 * Exit a parse tree produced by the {@code speed_limit}
	 * labeled alternative in {@link AVScenariosParser#speed_limitation_parameter}.
	 * @param ctx the parse tree
	 */
	void exitSpeed_limit(AVScenariosParser.Speed_limitContext ctx);
	/**
	 * Enter a parse tree produced by the {@code speed_limit_var}
	 * labeled alternative in {@link AVScenariosParser#speed_limitation_parameter}.
	 * @param ctx the parse tree
	 */
	void enterSpeed_limit_var(AVScenariosParser.Speed_limit_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code speed_limit_var}
	 * labeled alternative in {@link AVScenariosParser#speed_limitation_parameter}.
	 * @param ctx the parse tree
	 */
	void exitSpeed_limit_var(AVScenariosParser.Speed_limit_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code speed_limit_speed_limit}
	 * labeled alternative in {@link AVScenariosParser#speed_limitation}.
	 * @param ctx the parse tree
	 */
	void enterSpeed_limit_speed_limit(AVScenariosParser.Speed_limit_speed_limitContext ctx);
	/**
	 * Exit a parse tree produced by the {@code speed_limit_speed_limit}
	 * labeled alternative in {@link AVScenariosParser#speed_limitation}.
	 * @param ctx the parse tree
	 */
	void exitSpeed_limit_speed_limit(AVScenariosParser.Speed_limit_speed_limitContext ctx);
	/**
	 * Enter a parse tree produced by the {@code speed_range_var}
	 * labeled alternative in {@link AVScenariosParser#speed_range_parameter}.
	 * @param ctx the parse tree
	 */
	void enterSpeed_range_var(AVScenariosParser.Speed_range_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code speed_range_var}
	 * labeled alternative in {@link AVScenariosParser#speed_range_parameter}.
	 * @param ctx the parse tree
	 */
	void exitSpeed_range_var(AVScenariosParser.Speed_range_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code speed_range_speed}
	 * labeled alternative in {@link AVScenariosParser#speed_range_parameter}.
	 * @param ctx the parse tree
	 */
	void enterSpeed_range_speed(AVScenariosParser.Speed_range_speedContext ctx);
	/**
	 * Exit a parse tree produced by the {@code speed_range_speed}
	 * labeled alternative in {@link AVScenariosParser#speed_range_parameter}.
	 * @param ctx the parse tree
	 */
	void exitSpeed_range_speed(AVScenariosParser.Speed_range_speedContext ctx);
	/**
	 * Enter a parse tree produced by the {@code speed_range_value}
	 * labeled alternative in {@link AVScenariosParser#speed_range}.
	 * @param ctx the parse tree
	 */
	void enterSpeed_range_value(AVScenariosParser.Speed_range_valueContext ctx);
	/**
	 * Exit a parse tree produced by the {@code speed_range_value}
	 * labeled alternative in {@link AVScenariosParser#speed_range}.
	 * @param ctx the parse tree
	 */
	void exitSpeed_range_value(AVScenariosParser.Speed_range_valueContext ctx);
	/**
	 * Enter a parse tree produced by the {@code trace_scenario}
	 * labeled alternative in {@link AVScenariosParser#trace_assignment}.
	 * @param ctx the parse tree
	 */
	void enterTrace_scenario(AVScenariosParser.Trace_scenarioContext ctx);
	/**
	 * Exit a parse tree produced by the {@code trace_scenario}
	 * labeled alternative in {@link AVScenariosParser#trace_assignment}.
	 * @param ctx the parse tree
	 */
	void exitTrace_scenario(AVScenariosParser.Trace_scenarioContext ctx);
	/**
	 * Enter a parse tree produced by the {@code trace_id}
	 * labeled alternative in {@link AVScenariosParser#trace_identifier}.
	 * @param ctx the parse tree
	 */
	void enterTrace_id(AVScenariosParser.Trace_idContext ctx);
	/**
	 * Exit a parse tree produced by the {@code trace_id}
	 * labeled alternative in {@link AVScenariosParser#trace_identifier}.
	 * @param ctx the parse tree
	 */
	void exitTrace_id(AVScenariosParser.Trace_idContext ctx);
	/**
	 * Enter a parse tree produced by {@link AVScenariosParser#compare_operator}.
	 * @param ctx the parse tree
	 */
	void enterCompare_operator(AVScenariosParser.Compare_operatorContext ctx);
	/**
	 * Exit a parse tree produced by {@link AVScenariosParser#compare_operator}.
	 * @param ctx the parse tree
	 */
	void exitCompare_operator(AVScenariosParser.Compare_operatorContext ctx);
	/**
	 * Enter a parse tree produced by {@link AVScenariosParser#temporal_operator}.
	 * @param ctx the parse tree
	 */
	void enterTemporal_operator(AVScenariosParser.Temporal_operatorContext ctx);
	/**
	 * Exit a parse tree produced by {@link AVScenariosParser#temporal_operator}.
	 * @param ctx the parse tree
	 */
	void exitTemporal_operator(AVScenariosParser.Temporal_operatorContext ctx);
	/**
	 * Enter a parse tree produced by {@link AVScenariosParser#temporal_operator1}.
	 * @param ctx the parse tree
	 */
	void enterTemporal_operator1(AVScenariosParser.Temporal_operator1Context ctx);
	/**
	 * Exit a parse tree produced by {@link AVScenariosParser#temporal_operator1}.
	 * @param ctx the parse tree
	 */
	void exitTemporal_operator1(AVScenariosParser.Temporal_operator1Context ctx);
	/**
	 * Enter a parse tree produced by the {@code a_rv}
	 * labeled alternative in {@link AVScenariosParser#a}.
	 * @param ctx the parse tree
	 */
	void enterA_rv(AVScenariosParser.A_rvContext ctx);
	/**
	 * Exit a parse tree produced by the {@code a_rv}
	 * labeled alternative in {@link AVScenariosParser#a}.
	 * @param ctx the parse tree
	 */
	void exitA_rv(AVScenariosParser.A_rvContext ctx);
	/**
	 * Enter a parse tree produced by the {@code b_rv}
	 * labeled alternative in {@link AVScenariosParser#b}.
	 * @param ctx the parse tree
	 */
	void enterB_rv(AVScenariosParser.B_rvContext ctx);
	/**
	 * Exit a parse tree produced by the {@code b_rv}
	 * labeled alternative in {@link AVScenariosParser#b}.
	 * @param ctx the parse tree
	 */
	void exitB_rv(AVScenariosParser.B_rvContext ctx);
	/**
	 * Enter a parse tree produced by the {@code atom_statement_overall_atom_statement}
	 * labeled alternative in {@link AVScenariosParser#atom_statement_overall}.
	 * @param ctx the parse tree
	 */
	void enterAtom_statement_overall_atom_statement(AVScenariosParser.Atom_statement_overall_atom_statementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code atom_statement_overall_atom_statement}
	 * labeled alternative in {@link AVScenariosParser#atom_statement_overall}.
	 * @param ctx the parse tree
	 */
	void exitAtom_statement_overall_atom_statement(AVScenariosParser.Atom_statement_overall_atom_statementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code atom_statement_overall_with_kuohao}
	 * labeled alternative in {@link AVScenariosParser#atom_statement_overall}.
	 * @param ctx the parse tree
	 */
	void enterAtom_statement_overall_with_kuohao(AVScenariosParser.Atom_statement_overall_with_kuohaoContext ctx);
	/**
	 * Exit a parse tree produced by the {@code atom_statement_overall_with_kuohao}
	 * labeled alternative in {@link AVScenariosParser#atom_statement_overall}.
	 * @param ctx the parse tree
	 */
	void exitAtom_statement_overall_with_kuohao(AVScenariosParser.Atom_statement_overall_with_kuohaoContext ctx);
	/**
	 * Enter a parse tree produced by the {@code atom_statement_id}
	 * labeled alternative in {@link AVScenariosParser#atom_statement_overall}.
	 * @param ctx the parse tree
	 */
	void enterAtom_statement_id(AVScenariosParser.Atom_statement_idContext ctx);
	/**
	 * Exit a parse tree produced by the {@code atom_statement_id}
	 * labeled alternative in {@link AVScenariosParser#atom_statement_overall}.
	 * @param ctx the parse tree
	 */
	void exitAtom_statement_id(AVScenariosParser.Atom_statement_idContext ctx);
	/**
	 * Enter a parse tree produced by the {@code atom_statement_overall_combination}
	 * labeled alternative in {@link AVScenariosParser#atom_statement_overall}.
	 * @param ctx the parse tree
	 */
	void enterAtom_statement_overall_combination(AVScenariosParser.Atom_statement_overall_combinationContext ctx);
	/**
	 * Exit a parse tree produced by the {@code atom_statement_overall_combination}
	 * labeled alternative in {@link AVScenariosParser#atom_statement_overall}.
	 * @param ctx the parse tree
	 */
	void exitAtom_statement_overall_combination(AVScenariosParser.Atom_statement_overall_combinationContext ctx);
	/**
	 * Enter a parse tree produced by the {@code distance_statement_for_general_statement}
	 * labeled alternative in {@link AVScenariosParser#atom_statement}.
	 * @param ctx the parse tree
	 */
	void enterDistance_statement_for_general_statement(AVScenariosParser.Distance_statement_for_general_statementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code distance_statement_for_general_statement}
	 * labeled alternative in {@link AVScenariosParser#atom_statement}.
	 * @param ctx the parse tree
	 */
	void exitDistance_statement_for_general_statement(AVScenariosParser.Distance_statement_for_general_statementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code perception_difference_statement_for_general_statement}
	 * labeled alternative in {@link AVScenariosParser#atom_statement}.
	 * @param ctx the parse tree
	 */
	void enterPerception_difference_statement_for_general_statement(AVScenariosParser.Perception_difference_statement_for_general_statementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code perception_difference_statement_for_general_statement}
	 * labeled alternative in {@link AVScenariosParser#atom_statement}.
	 * @param ctx the parse tree
	 */
	void exitPerception_difference_statement_for_general_statement(AVScenariosParser.Perception_difference_statement_for_general_statementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code velocity_statement_for_general_statement}
	 * labeled alternative in {@link AVScenariosParser#atom_statement}.
	 * @param ctx the parse tree
	 */
	void enterVelocity_statement_for_general_statement(AVScenariosParser.Velocity_statement_for_general_statementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code velocity_statement_for_general_statement}
	 * labeled alternative in {@link AVScenariosParser#atom_statement}.
	 * @param ctx the parse tree
	 */
	void exitVelocity_statement_for_general_statement(AVScenariosParser.Velocity_statement_for_general_statementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code speed_statement_for_general_statement}
	 * labeled alternative in {@link AVScenariosParser#atom_statement}.
	 * @param ctx the parse tree
	 */
	void enterSpeed_statement_for_general_statement(AVScenariosParser.Speed_statement_for_general_statementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code speed_statement_for_general_statement}
	 * labeled alternative in {@link AVScenariosParser#atom_statement}.
	 * @param ctx the parse tree
	 */
	void exitSpeed_statement_for_general_statement(AVScenariosParser.Speed_statement_for_general_statementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code acceleration_statement_for_general_statement}
	 * labeled alternative in {@link AVScenariosParser#atom_statement}.
	 * @param ctx the parse tree
	 */
	void enterAcceleration_statement_for_general_statement(AVScenariosParser.Acceleration_statement_for_general_statementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code acceleration_statement_for_general_statement}
	 * labeled alternative in {@link AVScenariosParser#atom_statement}.
	 * @param ctx the parse tree
	 */
	void exitAcceleration_statement_for_general_statement(AVScenariosParser.Acceleration_statement_for_general_statementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code real_value_for_general_statement}
	 * labeled alternative in {@link AVScenariosParser#atom_statement}.
	 * @param ctx the parse tree
	 */
	void enterReal_value_for_general_statement(AVScenariosParser.Real_value_for_general_statementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code real_value_for_general_statement}
	 * labeled alternative in {@link AVScenariosParser#atom_statement}.
	 * @param ctx the parse tree
	 */
	void exitReal_value_for_general_statement(AVScenariosParser.Real_value_for_general_statementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_value_related_APIs}
	 * labeled alternative in {@link AVScenariosParser#atom_statement}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_value_related_APIs(AVScenariosParser.Traffic_rule_value_related_APIsContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_value_related_APIs}
	 * labeled alternative in {@link AVScenariosParser#atom_statement}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_value_related_APIs(AVScenariosParser.Traffic_rule_value_related_APIsContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_highBeamOn}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_highBeamOn(AVScenariosParser.Traffic_rule_highBeamOnContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_highBeamOn}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_highBeamOn(AVScenariosParser.Traffic_rule_highBeamOnContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_lowBeamOn}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_lowBeamOn(AVScenariosParser.Traffic_rule_lowBeamOnContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_lowBeamOn}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_lowBeamOn(AVScenariosParser.Traffic_rule_lowBeamOnContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_fogLightOn}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_fogLightOn(AVScenariosParser.Traffic_rule_fogLightOnContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_fogLightOn}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_fogLightOn(AVScenariosParser.Traffic_rule_fogLightOnContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_hornOn}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_hornOn(AVScenariosParser.Traffic_rule_hornOnContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_hornOn}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_hornOn(AVScenariosParser.Traffic_rule_hornOnContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_warningFlashOn}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_warningFlashOn(AVScenariosParser.Traffic_rule_warningFlashOnContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_warningFlashOn}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_warningFlashOn(AVScenariosParser.Traffic_rule_warningFlashOnContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_engineOn}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_engineOn(AVScenariosParser.Traffic_rule_engineOnContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_engineOn}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_engineOn(AVScenariosParser.Traffic_rule_engineOnContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_isLaneChanging}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_isLaneChanging(AVScenariosParser.Traffic_rule_isLaneChangingContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_isLaneChanging}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_isLaneChanging(AVScenariosParser.Traffic_rule_isLaneChangingContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_isOverTaking}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_isOverTaking(AVScenariosParser.Traffic_rule_isOverTakingContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_isOverTaking}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_isOverTaking(AVScenariosParser.Traffic_rule_isOverTakingContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_isTurningAround}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_isTurningAround(AVScenariosParser.Traffic_rule_isTurningAroundContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_isTurningAround}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_isTurningAround(AVScenariosParser.Traffic_rule_isTurningAroundContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_manualIntervention}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_manualIntervention(AVScenariosParser.Traffic_rule_manualInterventionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_manualIntervention}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_manualIntervention(AVScenariosParser.Traffic_rule_manualInterventionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_honkingAllowed}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_honkingAllowed(AVScenariosParser.Traffic_rule_honkingAllowedContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_honkingAllowed}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_honkingAllowed(AVScenariosParser.Traffic_rule_honkingAllowedContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_crosswalkAhead}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_crosswalkAhead(AVScenariosParser.Traffic_rule_crosswalkAheadContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_crosswalkAhead}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_crosswalkAhead(AVScenariosParser.Traffic_rule_crosswalkAheadContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_junctionAhead}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_junctionAhead(AVScenariosParser.Traffic_rule_junctionAheadContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_junctionAhead}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_junctionAhead(AVScenariosParser.Traffic_rule_junctionAheadContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_stopSignAhead}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_stopSignAhead(AVScenariosParser.Traffic_rule_stopSignAheadContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_stopSignAhead}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_stopSignAhead(AVScenariosParser.Traffic_rule_stopSignAheadContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_stoplineAhead}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_stoplineAhead(AVScenariosParser.Traffic_rule_stoplineAheadContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_stoplineAhead}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_stoplineAhead(AVScenariosParser.Traffic_rule_stoplineAheadContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_streetLightOn}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_streetLightOn(AVScenariosParser.Traffic_rule_streetLightOnContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_streetLightOn}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_streetLightOn(AVScenariosParser.Traffic_rule_streetLightOnContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_specialLocationAhead}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_specialLocationAhead(AVScenariosParser.Traffic_rule_specialLocationAheadContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_specialLocationAhead}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_specialLocationAhead(AVScenariosParser.Traffic_rule_specialLocationAheadContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_trafficLightAhead_blink}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_trafficLightAhead_blink(AVScenariosParser.Traffic_rule_trafficLightAhead_blinkContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_trafficLightAhead_blink}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_trafficLightAhead_blink(AVScenariosParser.Traffic_rule_trafficLightAhead_blinkContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_PriorityNPCAhead}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_PriorityNPCAhead(AVScenariosParser.Traffic_rule_PriorityNPCAheadContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_PriorityNPCAhead}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_PriorityNPCAhead(AVScenariosParser.Traffic_rule_PriorityNPCAheadContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_PriorityPedsAhead}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_PriorityPedsAhead(AVScenariosParser.Traffic_rule_PriorityPedsAheadContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_PriorityPedsAhead}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_PriorityPedsAhead(AVScenariosParser.Traffic_rule_PriorityPedsAheadContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_isTrafficJam}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_isTrafficJam(AVScenariosParser.Traffic_rule_isTrafficJamContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_isTrafficJam}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_isTrafficJam(AVScenariosParser.Traffic_rule_isTrafficJamContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_NPCAhead}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_NPCAhead(AVScenariosParser.Traffic_rule_NPCAheadContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_NPCAhead}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_NPCAhead(AVScenariosParser.Traffic_rule_NPCAheadContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_NearestNPC}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_NearestNPC(AVScenariosParser.Traffic_rule_NearestNPCContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_NearestNPC}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_NearestNPC(AVScenariosParser.Traffic_rule_NearestNPCContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_NPCOpposite}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_NPCOpposite(AVScenariosParser.Traffic_rule_NPCOppositeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_NPCOpposite}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_NPCOpposite(AVScenariosParser.Traffic_rule_NPCOppositeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_trafficLightAhead_arrow_blink}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_trafficLightAhead_arrow_blink(AVScenariosParser.Traffic_rule_trafficLightAhead_arrow_blinkContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_trafficLightAhead_arrow_blink}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_trafficLightAhead_arrow_blink(AVScenariosParser.Traffic_rule_trafficLightAhead_arrow_blinkContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_Time}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_Time(AVScenariosParser.Traffic_rule_TimeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_Time}
	 * labeled alternative in {@link AVScenariosParser#boolean_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_Time(AVScenariosParser.Traffic_rule_TimeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_turnSignal}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_turnSignal(AVScenariosParser.Traffic_rule_turnSignalContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_turnSignal}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_turnSignal(AVScenariosParser.Traffic_rule_turnSignalContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_gear}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_gear(AVScenariosParser.Traffic_rule_gearContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_gear}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_gear(AVScenariosParser.Traffic_rule_gearContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_direction}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_direction(AVScenariosParser.Traffic_rule_directionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_direction}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_direction(AVScenariosParser.Traffic_rule_directionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_speed}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_speed(AVScenariosParser.Traffic_rule_speedContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_speed}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_speed(AVScenariosParser.Traffic_rule_speedContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_acc}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_acc(AVScenariosParser.Traffic_rule_accContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_acc}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_acc(AVScenariosParser.Traffic_rule_accContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_brake}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_brake(AVScenariosParser.Traffic_rule_brakeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_brake}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_brake(AVScenariosParser.Traffic_rule_brakeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_currentlane_number}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_currentlane_number(AVScenariosParser.Traffic_rule_currentlane_numberContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_currentlane_number}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_currentlane_number(AVScenariosParser.Traffic_rule_currentlane_numberContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_currentlane_direction}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_currentlane_direction(AVScenariosParser.Traffic_rule_currentlane_directionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_currentlane_direction}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_currentlane_direction(AVScenariosParser.Traffic_rule_currentlane_directionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_speedLimit_upperLimit}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_speedLimit_upperLimit(AVScenariosParser.Traffic_rule_speedLimit_upperLimitContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_speedLimit_upperLimit}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_speedLimit_upperLimit(AVScenariosParser.Traffic_rule_speedLimit_upperLimitContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_speedLimit_lowerLimit}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_speedLimit_lowerLimit(AVScenariosParser.Traffic_rule_speedLimit_lowerLimitContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_speedLimit_lowerLimit}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_speedLimit_lowerLimit(AVScenariosParser.Traffic_rule_speedLimit_lowerLimitContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_speedLimit_specialLocationAhead_type}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_speedLimit_specialLocationAhead_type(AVScenariosParser.Traffic_rule_speedLimit_specialLocationAhead_typeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_speedLimit_specialLocationAhead_type}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_speedLimit_specialLocationAhead_type(AVScenariosParser.Traffic_rule_speedLimit_specialLocationAhead_typeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_trafficLightAhead_color}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_trafficLightAhead_color(AVScenariosParser.Traffic_rule_trafficLightAhead_colorContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_trafficLightAhead_color}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_trafficLightAhead_color(AVScenariosParser.Traffic_rule_trafficLightAhead_colorContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_signalAhead}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_signalAhead(AVScenariosParser.Traffic_rule_signalAheadContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_signalAhead}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_signalAhead(AVScenariosParser.Traffic_rule_signalAheadContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_NPCAhead_speed}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_NPCAhead_speed(AVScenariosParser.Traffic_rule_NPCAhead_speedContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_NPCAhead_speed}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_NPCAhead_speed(AVScenariosParser.Traffic_rule_NPCAhead_speedContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_NearestNPC_speed}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_NearestNPC_speed(AVScenariosParser.Traffic_rule_NearestNPC_speedContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_NearestNPC_speed}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_NearestNPC_speed(AVScenariosParser.Traffic_rule_NearestNPC_speedContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_NPCOpposite_speed}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_NPCOpposite_speed(AVScenariosParser.Traffic_rule_NPCOpposite_speedContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_NPCOpposite_speed}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_NPCOpposite_speed(AVScenariosParser.Traffic_rule_NPCOpposite_speedContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_trafficLightAhead_arrow_color}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_trafficLightAhead_arrow_color(AVScenariosParser.Traffic_rule_trafficLightAhead_arrow_colorContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_trafficLightAhead_arrow_color}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_trafficLightAhead_arrow_color(AVScenariosParser.Traffic_rule_trafficLightAhead_arrow_colorContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_green}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_green(AVScenariosParser.Traffic_rule_greenContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_green}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_green(AVScenariosParser.Traffic_rule_greenContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_red}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_red(AVScenariosParser.Traffic_rule_redContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_red}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_red(AVScenariosParser.Traffic_rule_redContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_yellow}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_yellow(AVScenariosParser.Traffic_rule_yellowContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_yellow}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_yellow(AVScenariosParser.Traffic_rule_yellowContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_off}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_off(AVScenariosParser.Traffic_rule_offContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_off}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_off(AVScenariosParser.Traffic_rule_offContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_forward}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_forward(AVScenariosParser.Traffic_rule_forwardContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_forward}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_forward(AVScenariosParser.Traffic_rule_forwardContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_left}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_left(AVScenariosParser.Traffic_rule_leftContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_left}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_left(AVScenariosParser.Traffic_rule_leftContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_right}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_right(AVScenariosParser.Traffic_rule_rightContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_right}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_right(AVScenariosParser.Traffic_rule_rightContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_fog}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_fog(AVScenariosParser.Traffic_rule_fogContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_fog}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_fog(AVScenariosParser.Traffic_rule_fogContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_rain}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_rain(AVScenariosParser.Traffic_rule_rainContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_rain}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_rain(AVScenariosParser.Traffic_rule_rainContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_snow}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_snow(AVScenariosParser.Traffic_rule_snowContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_snow}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_snow(AVScenariosParser.Traffic_rule_snowContext ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_visibility}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_visibility(AVScenariosParser.Traffic_rule_visibilityContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_visibility}
	 * labeled alternative in {@link AVScenariosParser#value_related_APIs}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_visibility(AVScenariosParser.Traffic_rule_visibilityContext ctx);
	/**
	 * Enter a parse tree produced by {@link AVScenariosParser#distance_statement}.
	 * @param ctx the parse tree
	 */
	void enterDistance_statement(AVScenariosParser.Distance_statementContext ctx);
	/**
	 * Exit a parse tree produced by {@link AVScenariosParser#distance_statement}.
	 * @param ctx the parse tree
	 */
	void exitDistance_statement(AVScenariosParser.Distance_statementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code ego_state_parameter_for_distance}
	 * labeled alternative in {@link AVScenariosParser#position_element}.
	 * @param ctx the parse tree
	 */
	void enterEgo_state_parameter_for_distance(AVScenariosParser.Ego_state_parameter_for_distanceContext ctx);
	/**
	 * Exit a parse tree produced by the {@code ego_state_parameter_for_distance}
	 * labeled alternative in {@link AVScenariosParser#position_element}.
	 * @param ctx the parse tree
	 */
	void exitEgo_state_parameter_for_distance(AVScenariosParser.Ego_state_parameter_for_distanceContext ctx);
	/**
	 * Enter a parse tree produced by the {@code agent_state_parameter_for_distance}
	 * labeled alternative in {@link AVScenariosParser#position_element}.
	 * @param ctx the parse tree
	 */
	void enterAgent_state_parameter_for_distance(AVScenariosParser.Agent_state_parameter_for_distanceContext ctx);
	/**
	 * Exit a parse tree produced by the {@code agent_state_parameter_for_distance}
	 * labeled alternative in {@link AVScenariosParser#position_element}.
	 * @param ctx the parse tree
	 */
	void exitAgent_state_parameter_for_distance(AVScenariosParser.Agent_state_parameter_for_distanceContext ctx);
	/**
	 * Enter a parse tree produced by the {@code agent_ground_truth_parameter_for_distance}
	 * labeled alternative in {@link AVScenariosParser#position_element}.
	 * @param ctx the parse tree
	 */
	void enterAgent_ground_truth_parameter_for_distance(AVScenariosParser.Agent_ground_truth_parameter_for_distanceContext ctx);
	/**
	 * Exit a parse tree produced by the {@code agent_ground_truth_parameter_for_distance}
	 * labeled alternative in {@link AVScenariosParser#position_element}.
	 * @param ctx the parse tree
	 */
	void exitAgent_ground_truth_parameter_for_distance(AVScenariosParser.Agent_ground_truth_parameter_for_distanceContext ctx);
	/**
	 * Enter a parse tree produced by the {@code position_parameter_for_general}
	 * labeled alternative in {@link AVScenariosParser#position_element}.
	 * @param ctx the parse tree
	 */
	void enterPosition_parameter_for_general(AVScenariosParser.Position_parameter_for_generalContext ctx);
	/**
	 * Exit a parse tree produced by the {@code position_parameter_for_general}
	 * labeled alternative in {@link AVScenariosParser#position_element}.
	 * @param ctx the parse tree
	 */
	void exitPosition_parameter_for_general(AVScenariosParser.Position_parameter_for_generalContext ctx);
	/**
	 * Enter a parse tree produced by the {@code position_element_id}
	 * labeled alternative in {@link AVScenariosParser#position_element}.
	 * @param ctx the parse tree
	 */
	void enterPosition_element_id(AVScenariosParser.Position_element_idContext ctx);
	/**
	 * Exit a parse tree produced by the {@code position_element_id}
	 * labeled alternative in {@link AVScenariosParser#position_element}.
	 * @param ctx the parse tree
	 */
	void exitPosition_element_id(AVScenariosParser.Position_element_idContext ctx);
	/**
	 * Enter a parse tree produced by the {@code ego_state_id}
	 * labeled alternative in {@link AVScenariosParser#ego_state_parameter}.
	 * @param ctx the parse tree
	 */
	void enterEgo_state_id(AVScenariosParser.Ego_state_idContext ctx);
	/**
	 * Exit a parse tree produced by the {@code ego_state_id}
	 * labeled alternative in {@link AVScenariosParser#ego_state_parameter}.
	 * @param ctx the parse tree
	 */
	void exitEgo_state_id(AVScenariosParser.Ego_state_idContext ctx);
	/**
	 * Enter a parse tree produced by the {@code ego_state_par}
	 * labeled alternative in {@link AVScenariosParser#ego_state_parameter}.
	 * @param ctx the parse tree
	 */
	void enterEgo_state_par(AVScenariosParser.Ego_state_parContext ctx);
	/**
	 * Exit a parse tree produced by the {@code ego_state_par}
	 * labeled alternative in {@link AVScenariosParser#ego_state_parameter}.
	 * @param ctx the parse tree
	 */
	void exitEgo_state_par(AVScenariosParser.Ego_state_parContext ctx);
	/**
	 * Enter a parse tree produced by the {@code ego_state_for_general}
	 * labeled alternative in {@link AVScenariosParser#ego_state}.
	 * @param ctx the parse tree
	 */
	void enterEgo_state_for_general(AVScenariosParser.Ego_state_for_generalContext ctx);
	/**
	 * Exit a parse tree produced by the {@code ego_state_for_general}
	 * labeled alternative in {@link AVScenariosParser#ego_state}.
	 * @param ctx the parse tree
	 */
	void exitEgo_state_for_general(AVScenariosParser.Ego_state_for_generalContext ctx);
	/**
	 * Enter a parse tree produced by the {@code agent_state_id}
	 * labeled alternative in {@link AVScenariosParser#agent_state_parameter}.
	 * @param ctx the parse tree
	 */
	void enterAgent_state_id(AVScenariosParser.Agent_state_idContext ctx);
	/**
	 * Exit a parse tree produced by the {@code agent_state_id}
	 * labeled alternative in {@link AVScenariosParser#agent_state_parameter}.
	 * @param ctx the parse tree
	 */
	void exitAgent_state_id(AVScenariosParser.Agent_state_idContext ctx);
	/**
	 * Enter a parse tree produced by the {@code agent_state_par}
	 * labeled alternative in {@link AVScenariosParser#agent_state_parameter}.
	 * @param ctx the parse tree
	 */
	void enterAgent_state_par(AVScenariosParser.Agent_state_parContext ctx);
	/**
	 * Exit a parse tree produced by the {@code agent_state_par}
	 * labeled alternative in {@link AVScenariosParser#agent_state_parameter}.
	 * @param ctx the parse tree
	 */
	void exitAgent_state_par(AVScenariosParser.Agent_state_parContext ctx);
	/**
	 * Enter a parse tree produced by the {@code agent_state_for_general}
	 * labeled alternative in {@link AVScenariosParser#agent_state}.
	 * @param ctx the parse tree
	 */
	void enterAgent_state_for_general(AVScenariosParser.Agent_state_for_generalContext ctx);
	/**
	 * Exit a parse tree produced by the {@code agent_state_for_general}
	 * labeled alternative in {@link AVScenariosParser#agent_state}.
	 * @param ctx the parse tree
	 */
	void exitAgent_state_for_general(AVScenariosParser.Agent_state_for_generalContext ctx);
	/**
	 * Enter a parse tree produced by the {@code agent_ground_truth_id}
	 * labeled alternative in {@link AVScenariosParser#agent_ground_truth_parameter}.
	 * @param ctx the parse tree
	 */
	void enterAgent_ground_truth_id(AVScenariosParser.Agent_ground_truth_idContext ctx);
	/**
	 * Exit a parse tree produced by the {@code agent_ground_truth_id}
	 * labeled alternative in {@link AVScenariosParser#agent_ground_truth_parameter}.
	 * @param ctx the parse tree
	 */
	void exitAgent_ground_truth_id(AVScenariosParser.Agent_ground_truth_idContext ctx);
	/**
	 * Enter a parse tree produced by the {@code agent_ground_truth_par}
	 * labeled alternative in {@link AVScenariosParser#agent_ground_truth_parameter}.
	 * @param ctx the parse tree
	 */
	void enterAgent_ground_truth_par(AVScenariosParser.Agent_ground_truth_parContext ctx);
	/**
	 * Exit a parse tree produced by the {@code agent_ground_truth_par}
	 * labeled alternative in {@link AVScenariosParser#agent_ground_truth_parameter}.
	 * @param ctx the parse tree
	 */
	void exitAgent_ground_truth_par(AVScenariosParser.Agent_ground_truth_parContext ctx);
	/**
	 * Enter a parse tree produced by the {@code agent_ground_truth_for_general}
	 * labeled alternative in {@link AVScenariosParser#agent_ground_truth}.
	 * @param ctx the parse tree
	 */
	void enterAgent_ground_truth_for_general(AVScenariosParser.Agent_ground_truth_for_generalContext ctx);
	/**
	 * Exit a parse tree produced by the {@code agent_ground_truth_for_general}
	 * labeled alternative in {@link AVScenariosParser#agent_ground_truth}.
	 * @param ctx the parse tree
	 */
	void exitAgent_ground_truth_for_general(AVScenariosParser.Agent_ground_truth_for_generalContext ctx);
	/**
	 * Enter a parse tree produced by {@link AVScenariosParser#perception_difference_statement}.
	 * @param ctx the parse tree
	 */
	void enterPerception_difference_statement(AVScenariosParser.Perception_difference_statementContext ctx);
	/**
	 * Exit a parse tree produced by {@link AVScenariosParser#perception_difference_statement}.
	 * @param ctx the parse tree
	 */
	void exitPerception_difference_statement(AVScenariosParser.Perception_difference_statementContext ctx);
	/**
	 * Enter a parse tree produced by {@link AVScenariosParser#velocity_statement}.
	 * @param ctx the parse tree
	 */
	void enterVelocity_statement(AVScenariosParser.Velocity_statementContext ctx);
	/**
	 * Exit a parse tree produced by {@link AVScenariosParser#velocity_statement}.
	 * @param ctx the parse tree
	 */
	void exitVelocity_statement(AVScenariosParser.Velocity_statementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code velocity_element_id}
	 * labeled alternative in {@link AVScenariosParser#velocity_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void enterVelocity_element_id(AVScenariosParser.Velocity_element_idContext ctx);
	/**
	 * Exit a parse tree produced by the {@code velocity_element_id}
	 * labeled alternative in {@link AVScenariosParser#velocity_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void exitVelocity_element_id(AVScenariosParser.Velocity_element_idContext ctx);
	/**
	 * Enter a parse tree produced by the {@code velocity_element_ego_state}
	 * labeled alternative in {@link AVScenariosParser#velocity_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void enterVelocity_element_ego_state(AVScenariosParser.Velocity_element_ego_stateContext ctx);
	/**
	 * Exit a parse tree produced by the {@code velocity_element_ego_state}
	 * labeled alternative in {@link AVScenariosParser#velocity_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void exitVelocity_element_ego_state(AVScenariosParser.Velocity_element_ego_stateContext ctx);
	/**
	 * Enter a parse tree produced by the {@code velocity_element_agent_state}
	 * labeled alternative in {@link AVScenariosParser#velocity_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void enterVelocity_element_agent_state(AVScenariosParser.Velocity_element_agent_stateContext ctx);
	/**
	 * Exit a parse tree produced by the {@code velocity_element_agent_state}
	 * labeled alternative in {@link AVScenariosParser#velocity_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void exitVelocity_element_agent_state(AVScenariosParser.Velocity_element_agent_stateContext ctx);
	/**
	 * Enter a parse tree produced by the {@code velocity_element_agent_ground_truth}
	 * labeled alternative in {@link AVScenariosParser#velocity_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void enterVelocity_element_agent_ground_truth(AVScenariosParser.Velocity_element_agent_ground_truthContext ctx);
	/**
	 * Exit a parse tree produced by the {@code velocity_element_agent_ground_truth}
	 * labeled alternative in {@link AVScenariosParser#velocity_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void exitVelocity_element_agent_ground_truth(AVScenariosParser.Velocity_element_agent_ground_truthContext ctx);
	/**
	 * Enter a parse tree produced by the {@code velocity_element_velocity}
	 * labeled alternative in {@link AVScenariosParser#velocity_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void enterVelocity_element_velocity(AVScenariosParser.Velocity_element_velocityContext ctx);
	/**
	 * Exit a parse tree produced by the {@code velocity_element_velocity}
	 * labeled alternative in {@link AVScenariosParser#velocity_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void exitVelocity_element_velocity(AVScenariosParser.Velocity_element_velocityContext ctx);
	/**
	 * Enter a parse tree produced by {@link AVScenariosParser#velocity_parameter}.
	 * @param ctx the parse tree
	 */
	void enterVelocity_parameter(AVScenariosParser.Velocity_parameterContext ctx);
	/**
	 * Exit a parse tree produced by {@link AVScenariosParser#velocity_parameter}.
	 * @param ctx the parse tree
	 */
	void exitVelocity_parameter(AVScenariosParser.Velocity_parameterContext ctx);
	/**
	 * Enter a parse tree produced by the {@code velocity_value}
	 * labeled alternative in {@link AVScenariosParser#velocity}.
	 * @param ctx the parse tree
	 */
	void enterVelocity_value(AVScenariosParser.Velocity_valueContext ctx);
	/**
	 * Exit a parse tree produced by the {@code velocity_value}
	 * labeled alternative in {@link AVScenariosParser#velocity}.
	 * @param ctx the parse tree
	 */
	void exitVelocity_value(AVScenariosParser.Velocity_valueContext ctx);
	/**
	 * Enter a parse tree produced by {@link AVScenariosParser#speed_statement}.
	 * @param ctx the parse tree
	 */
	void enterSpeed_statement(AVScenariosParser.Speed_statementContext ctx);
	/**
	 * Exit a parse tree produced by {@link AVScenariosParser#speed_statement}.
	 * @param ctx the parse tree
	 */
	void exitSpeed_statement(AVScenariosParser.Speed_statementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code speed_element_id}
	 * labeled alternative in {@link AVScenariosParser#speed_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void enterSpeed_element_id(AVScenariosParser.Speed_element_idContext ctx);
	/**
	 * Exit a parse tree produced by the {@code speed_element_id}
	 * labeled alternative in {@link AVScenariosParser#speed_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void exitSpeed_element_id(AVScenariosParser.Speed_element_idContext ctx);
	/**
	 * Enter a parse tree produced by the {@code speed_element_ego_state}
	 * labeled alternative in {@link AVScenariosParser#speed_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void enterSpeed_element_ego_state(AVScenariosParser.Speed_element_ego_stateContext ctx);
	/**
	 * Exit a parse tree produced by the {@code speed_element_ego_state}
	 * labeled alternative in {@link AVScenariosParser#speed_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void exitSpeed_element_ego_state(AVScenariosParser.Speed_element_ego_stateContext ctx);
	/**
	 * Enter a parse tree produced by the {@code speed_element_agent_state}
	 * labeled alternative in {@link AVScenariosParser#speed_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void enterSpeed_element_agent_state(AVScenariosParser.Speed_element_agent_stateContext ctx);
	/**
	 * Exit a parse tree produced by the {@code speed_element_agent_state}
	 * labeled alternative in {@link AVScenariosParser#speed_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void exitSpeed_element_agent_state(AVScenariosParser.Speed_element_agent_stateContext ctx);
	/**
	 * Enter a parse tree produced by the {@code speed_element_agent_ground_truth}
	 * labeled alternative in {@link AVScenariosParser#speed_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void enterSpeed_element_agent_ground_truth(AVScenariosParser.Speed_element_agent_ground_truthContext ctx);
	/**
	 * Exit a parse tree produced by the {@code speed_element_agent_ground_truth}
	 * labeled alternative in {@link AVScenariosParser#speed_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void exitSpeed_element_agent_ground_truth(AVScenariosParser.Speed_element_agent_ground_truthContext ctx);
	/**
	 * Enter a parse tree produced by the {@code speed_element_speed}
	 * labeled alternative in {@link AVScenariosParser#speed_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void enterSpeed_element_speed(AVScenariosParser.Speed_element_speedContext ctx);
	/**
	 * Exit a parse tree produced by the {@code speed_element_speed}
	 * labeled alternative in {@link AVScenariosParser#speed_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void exitSpeed_element_speed(AVScenariosParser.Speed_element_speedContext ctx);
	/**
	 * Enter a parse tree produced by {@link AVScenariosParser#acceleration_statement}.
	 * @param ctx the parse tree
	 */
	void enterAcceleration_statement(AVScenariosParser.Acceleration_statementContext ctx);
	/**
	 * Exit a parse tree produced by {@link AVScenariosParser#acceleration_statement}.
	 * @param ctx the parse tree
	 */
	void exitAcceleration_statement(AVScenariosParser.Acceleration_statementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code acceleration_element_id}
	 * labeled alternative in {@link AVScenariosParser#acceleration_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void enterAcceleration_element_id(AVScenariosParser.Acceleration_element_idContext ctx);
	/**
	 * Exit a parse tree produced by the {@code acceleration_element_id}
	 * labeled alternative in {@link AVScenariosParser#acceleration_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void exitAcceleration_element_id(AVScenariosParser.Acceleration_element_idContext ctx);
	/**
	 * Enter a parse tree produced by the {@code acceleration_element_ego_state}
	 * labeled alternative in {@link AVScenariosParser#acceleration_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void enterAcceleration_element_ego_state(AVScenariosParser.Acceleration_element_ego_stateContext ctx);
	/**
	 * Exit a parse tree produced by the {@code acceleration_element_ego_state}
	 * labeled alternative in {@link AVScenariosParser#acceleration_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void exitAcceleration_element_ego_state(AVScenariosParser.Acceleration_element_ego_stateContext ctx);
	/**
	 * Enter a parse tree produced by the {@code acceleration_element_agent_state}
	 * labeled alternative in {@link AVScenariosParser#acceleration_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void enterAcceleration_element_agent_state(AVScenariosParser.Acceleration_element_agent_stateContext ctx);
	/**
	 * Exit a parse tree produced by the {@code acceleration_element_agent_state}
	 * labeled alternative in {@link AVScenariosParser#acceleration_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void exitAcceleration_element_agent_state(AVScenariosParser.Acceleration_element_agent_stateContext ctx);
	/**
	 * Enter a parse tree produced by the {@code acceleration_element_agent_ground}
	 * labeled alternative in {@link AVScenariosParser#acceleration_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void enterAcceleration_element_agent_ground(AVScenariosParser.Acceleration_element_agent_groundContext ctx);
	/**
	 * Exit a parse tree produced by the {@code acceleration_element_agent_ground}
	 * labeled alternative in {@link AVScenariosParser#acceleration_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void exitAcceleration_element_agent_ground(AVScenariosParser.Acceleration_element_agent_groundContext ctx);
	/**
	 * Enter a parse tree produced by the {@code acceleration_element_acc}
	 * labeled alternative in {@link AVScenariosParser#acceleration_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void enterAcceleration_element_acc(AVScenariosParser.Acceleration_element_accContext ctx);
	/**
	 * Exit a parse tree produced by the {@code acceleration_element_acc}
	 * labeled alternative in {@link AVScenariosParser#acceleration_parameter_for_statement}.
	 * @param ctx the parse tree
	 */
	void exitAcceleration_element_acc(AVScenariosParser.Acceleration_element_accContext ctx);
	/**
	 * Enter a parse tree produced by {@link AVScenariosParser#acceleration}.
	 * @param ctx the parse tree
	 */
	void enterAcceleration(AVScenariosParser.AccelerationContext ctx);
	/**
	 * Exit a parse tree produced by {@link AVScenariosParser#acceleration}.
	 * @param ctx the parse tree
	 */
	void exitAcceleration(AVScenariosParser.AccelerationContext ctx);
	/**
	 * Enter a parse tree produced by the {@code atom_statement_var}
	 * labeled alternative in {@link AVScenariosParser#atom_statement_parameter}.
	 * @param ctx the parse tree
	 */
	void enterAtom_statement_var(AVScenariosParser.Atom_statement_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code atom_statement_var}
	 * labeled alternative in {@link AVScenariosParser#atom_statement_parameter}.
	 * @param ctx the parse tree
	 */
	void exitAtom_statement_var(AVScenariosParser.Atom_statement_varContext ctx);
	/**
	 * Enter a parse tree produced by {@link AVScenariosParser#atom_predicate}.
	 * @param ctx the parse tree
	 */
	void enterAtom_predicate(AVScenariosParser.Atom_predicateContext ctx);
	/**
	 * Exit a parse tree produced by {@link AVScenariosParser#atom_predicate}.
	 * @param ctx the parse tree
	 */
	void exitAtom_predicate(AVScenariosParser.Atom_predicateContext ctx);
	/**
	 * Enter a parse tree produced by the {@code general_assertion3}
	 * labeled alternative in {@link AVScenariosParser#general_assertion}.
	 * @param ctx the parse tree
	 */
	void enterGeneral_assertion3(AVScenariosParser.General_assertion3Context ctx);
	/**
	 * Exit a parse tree produced by the {@code general_assertion3}
	 * labeled alternative in {@link AVScenariosParser#general_assertion}.
	 * @param ctx the parse tree
	 */
	void exitGeneral_assertion3(AVScenariosParser.General_assertion3Context ctx);
	/**
	 * Enter a parse tree produced by the {@code general_assertion4}
	 * labeled alternative in {@link AVScenariosParser#general_assertion}.
	 * @param ctx the parse tree
	 */
	void enterGeneral_assertion4(AVScenariosParser.General_assertion4Context ctx);
	/**
	 * Exit a parse tree produced by the {@code general_assertion4}
	 * labeled alternative in {@link AVScenariosParser#general_assertion}.
	 * @param ctx the parse tree
	 */
	void exitGeneral_assertion4(AVScenariosParser.General_assertion4Context ctx);
	/**
	 * Enter a parse tree produced by the {@code general_assertion5}
	 * labeled alternative in {@link AVScenariosParser#general_assertion}.
	 * @param ctx the parse tree
	 */
	void enterGeneral_assertion5(AVScenariosParser.General_assertion5Context ctx);
	/**
	 * Exit a parse tree produced by the {@code general_assertion5}
	 * labeled alternative in {@link AVScenariosParser#general_assertion}.
	 * @param ctx the parse tree
	 */
	void exitGeneral_assertion5(AVScenariosParser.General_assertion5Context ctx);
	/**
	 * Enter a parse tree produced by the {@code general_assertion6}
	 * labeled alternative in {@link AVScenariosParser#general_assertion}.
	 * @param ctx the parse tree
	 */
	void enterGeneral_assertion6(AVScenariosParser.General_assertion6Context ctx);
	/**
	 * Exit a parse tree produced by the {@code general_assertion6}
	 * labeled alternative in {@link AVScenariosParser#general_assertion}.
	 * @param ctx the parse tree
	 */
	void exitGeneral_assertion6(AVScenariosParser.General_assertion6Context ctx);
	/**
	 * Enter a parse tree produced by the {@code traffic_rule_boolean_related_APIs}
	 * labeled alternative in {@link AVScenariosParser#general_assertion}.
	 * @param ctx the parse tree
	 */
	void enterTraffic_rule_boolean_related_APIs(AVScenariosParser.Traffic_rule_boolean_related_APIsContext ctx);
	/**
	 * Exit a parse tree produced by the {@code traffic_rule_boolean_related_APIs}
	 * labeled alternative in {@link AVScenariosParser#general_assertion}.
	 * @param ctx the parse tree
	 */
	void exitTraffic_rule_boolean_related_APIs(AVScenariosParser.Traffic_rule_boolean_related_APIsContext ctx);
	/**
	 * Enter a parse tree produced by the {@code general_assertion0_0}
	 * labeled alternative in {@link AVScenariosParser#general_assertion}.
	 * @param ctx the parse tree
	 */
	void enterGeneral_assertion0_0(AVScenariosParser.General_assertion0_0Context ctx);
	/**
	 * Exit a parse tree produced by the {@code general_assertion0_0}
	 * labeled alternative in {@link AVScenariosParser#general_assertion}.
	 * @param ctx the parse tree
	 */
	void exitGeneral_assertion0_0(AVScenariosParser.General_assertion0_0Context ctx);
	/**
	 * Enter a parse tree produced by the {@code general_assertion0}
	 * labeled alternative in {@link AVScenariosParser#general_assertion}.
	 * @param ctx the parse tree
	 */
	void enterGeneral_assertion0(AVScenariosParser.General_assertion0Context ctx);
	/**
	 * Exit a parse tree produced by the {@code general_assertion0}
	 * labeled alternative in {@link AVScenariosParser#general_assertion}.
	 * @param ctx the parse tree
	 */
	void exitGeneral_assertion0(AVScenariosParser.General_assertion0Context ctx);
	/**
	 * Enter a parse tree produced by the {@code general_assertion1}
	 * labeled alternative in {@link AVScenariosParser#general_assertion}.
	 * @param ctx the parse tree
	 */
	void enterGeneral_assertion1(AVScenariosParser.General_assertion1Context ctx);
	/**
	 * Exit a parse tree produced by the {@code general_assertion1}
	 * labeled alternative in {@link AVScenariosParser#general_assertion}.
	 * @param ctx the parse tree
	 */
	void exitGeneral_assertion1(AVScenariosParser.General_assertion1Context ctx);
	/**
	 * Enter a parse tree produced by the {@code general_assertion2}
	 * labeled alternative in {@link AVScenariosParser#general_assertion}.
	 * @param ctx the parse tree
	 */
	void enterGeneral_assertion2(AVScenariosParser.General_assertion2Context ctx);
	/**
	 * Exit a parse tree produced by the {@code general_assertion2}
	 * labeled alternative in {@link AVScenariosParser#general_assertion}.
	 * @param ctx the parse tree
	 */
	void exitGeneral_assertion2(AVScenariosParser.General_assertion2Context ctx);
	/**
	 * Enter a parse tree produced by the {@code general_assertion_id}
	 * labeled alternative in {@link AVScenariosParser#general_assertion}.
	 * @param ctx the parse tree
	 */
	void enterGeneral_assertion_id(AVScenariosParser.General_assertion_idContext ctx);
	/**
	 * Exit a parse tree produced by the {@code general_assertion_id}
	 * labeled alternative in {@link AVScenariosParser#general_assertion}.
	 * @param ctx the parse tree
	 */
	void exitGeneral_assertion_id(AVScenariosParser.General_assertion_idContext ctx);
	/**
	 * Enter a parse tree produced by {@link AVScenariosParser#operator_related_assignments}.
	 * @param ctx the parse tree
	 */
	void enterOperator_related_assignments(AVScenariosParser.Operator_related_assignmentsContext ctx);
	/**
	 * Exit a parse tree produced by {@link AVScenariosParser#operator_related_assignments}.
	 * @param ctx the parse tree
	 */
	void exitOperator_related_assignments(AVScenariosParser.Operator_related_assignmentsContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assigns}
	 * labeled alternative in {@link AVScenariosParser#assignment_statements}.
	 * @param ctx the parse tree
	 */
	void enterAssigns(AVScenariosParser.AssignsContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assigns}
	 * labeled alternative in {@link AVScenariosParser#assignment_statements}.
	 * @param ctx the parse tree
	 */
	void exitAssigns(AVScenariosParser.AssignsContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_scenario}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_scenario(AVScenariosParser.Assign_scenarioContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_scenario}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_scenario(AVScenariosParser.Assign_scenarioContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_ego}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_ego(AVScenariosParser.Assign_egoContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_ego}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_ego(AVScenariosParser.Assign_egoContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_variable}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_variable(AVScenariosParser.Assign_variableContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_variable}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_variable(AVScenariosParser.Assign_variableContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_name_two_variables}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_name_two_variables(AVScenariosParser.Assign_name_two_variablesContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_name_two_variables}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_name_two_variables(AVScenariosParser.Assign_name_two_variablesContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_name_three_variables}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_name_three_variables(AVScenariosParser.Assign_name_three_variablesContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_name_three_variables}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_name_three_variables(AVScenariosParser.Assign_name_three_variablesContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_state}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_state(AVScenariosParser.Assign_stateContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_state}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_state(AVScenariosParser.Assign_stateContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_vehicle_type}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_vehicle_type(AVScenariosParser.Assign_vehicle_typeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_vehicle_type}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_vehicle_type(AVScenariosParser.Assign_vehicle_typeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_state_list}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_state_list(AVScenariosParser.Assign_state_listContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_state_list}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_state_list(AVScenariosParser.Assign_state_listContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_pedestrian_type}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_pedestrian_type(AVScenariosParser.Assign_pedestrian_typeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_pedestrian_type}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_pedestrian_type(AVScenariosParser.Assign_pedestrian_typeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_case_of_position}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_case_of_position(AVScenariosParser.Assign_case_of_positionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_case_of_position}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_case_of_position(AVScenariosParser.Assign_case_of_positionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_rv_rv}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_rv_rv(AVScenariosParser.Assign_rv_rvContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_rv_rv}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_rv_rv(AVScenariosParser.Assign_rv_rvContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_lane_rv}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_lane_rv(AVScenariosParser.Assign_lane_rvContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_lane_rv}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_lane_rv(AVScenariosParser.Assign_lane_rvContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_lane_range}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_lane_range(AVScenariosParser.Assign_lane_rangeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_lane_range}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_lane_range(AVScenariosParser.Assign_lane_rangeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_special_case_of_coordinate}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_special_case_of_coordinate(AVScenariosParser.Assign_special_case_of_coordinateContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_special_case_of_coordinate}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_special_case_of_coordinate(AVScenariosParser.Assign_special_case_of_coordinateContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_heading}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_heading(AVScenariosParser.Assign_headingContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_heading}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_heading(AVScenariosParser.Assign_headingContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_general_type}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_general_type(AVScenariosParser.Assign_general_typeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_general_type}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_general_type(AVScenariosParser.Assign_general_typeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_color}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_color(AVScenariosParser.Assign_colorContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_color}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_color(AVScenariosParser.Assign_colorContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_npc}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_npc(AVScenariosParser.Assign_npcContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_npc}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_npc(AVScenariosParser.Assign_npcContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_uniform_motion}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_uniform_motion(AVScenariosParser.Assign_uniform_motionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_uniform_motion}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_uniform_motion(AVScenariosParser.Assign_uniform_motionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_waypoint_motion}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_waypoint_motion(AVScenariosParser.Assign_waypoint_motionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_waypoint_motion}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_waypoint_motion(AVScenariosParser.Assign_waypoint_motionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_variables}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_variables(AVScenariosParser.Assign_variablesContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_variables}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_variables(AVScenariosParser.Assign_variablesContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_pedestrians}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_pedestrians(AVScenariosParser.Assign_pedestriansContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_pedestrians}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_pedestrians(AVScenariosParser.Assign_pedestriansContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_npcs}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_npcs(AVScenariosParser.Assign_npcsContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_npcs}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_npcs(AVScenariosParser.Assign_npcsContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_obstacles}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_obstacles(AVScenariosParser.Assign_obstaclesContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_obstacles}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_obstacles(AVScenariosParser.Assign_obstaclesContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_weather}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_weather(AVScenariosParser.Assign_weatherContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_weather}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_weather(AVScenariosParser.Assign_weatherContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_traffic}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_traffic(AVScenariosParser.Assign_trafficContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_traffic}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_traffic(AVScenariosParser.Assign_trafficContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_ped}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_ped(AVScenariosParser.Assign_pedContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_ped}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_ped(AVScenariosParser.Assign_pedContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_obs}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_obs(AVScenariosParser.Assign_obsContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_obs}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_obs(AVScenariosParser.Assign_obsContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_shape}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_shape(AVScenariosParser.Assign_shapeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_shape}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_shape(AVScenariosParser.Assign_shapeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_env}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_env(AVScenariosParser.Assign_envContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_env}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_env(AVScenariosParser.Assign_envContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_time}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_time(AVScenariosParser.Assign_timeContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_time}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_time(AVScenariosParser.Assign_timeContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_weather_stmt}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_weather_stmt(AVScenariosParser.Assign_weather_stmtContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_weather_stmt}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_weather_stmt(AVScenariosParser.Assign_weather_stmtContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_weather_discrete}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_weather_discrete(AVScenariosParser.Assign_weather_discreteContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_weather_discrete}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_weather_discrete(AVScenariosParser.Assign_weather_discreteContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_intersection}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_intersection(AVScenariosParser.Assign_intersectionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_intersection}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_intersection(AVScenariosParser.Assign_intersectionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_speed_limit}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_speed_limit(AVScenariosParser.Assign_speed_limitContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_speed_limit}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_speed_limit(AVScenariosParser.Assign_speed_limitContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_trace}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_trace(AVScenariosParser.Assign_traceContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_trace}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_trace(AVScenariosParser.Assign_traceContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_distance_statement}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_distance_statement(AVScenariosParser.Assign_distance_statementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_distance_statement}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_distance_statement(AVScenariosParser.Assign_distance_statementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assignperception_difference_statement}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssignperception_difference_statement(AVScenariosParser.Assignperception_difference_statementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assignperception_difference_statement}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssignperception_difference_statement(AVScenariosParser.Assignperception_difference_statementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_velocity_statement}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_velocity_statement(AVScenariosParser.Assign_velocity_statementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_velocity_statement}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_velocity_statement(AVScenariosParser.Assign_velocity_statementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_speed_statement}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_speed_statement(AVScenariosParser.Assign_speed_statementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_speed_statement}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_speed_statement(AVScenariosParser.Assign_speed_statementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_acceleration_statement}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_acceleration_statement(AVScenariosParser.Assign_acceleration_statementContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_acceleration_statement}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_acceleration_statement(AVScenariosParser.Assign_acceleration_statementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_operator_related_assignments}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_operator_related_assignments(AVScenariosParser.Assign_operator_related_assignmentsContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_operator_related_assignments}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_operator_related_assignments(AVScenariosParser.Assign_operator_related_assignmentsContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_general_assertion_to_var}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_general_assertion_to_var(AVScenariosParser.Assign_general_assertion_to_varContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_general_assertion_to_var}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_general_assertion_to_var(AVScenariosParser.Assign_general_assertion_to_varContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_general_assertion}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_general_assertion(AVScenariosParser.Assign_general_assertionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_general_assertion}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_general_assertion(AVScenariosParser.Assign_general_assertionContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_agent_ground}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_agent_ground(AVScenariosParser.Assign_agent_groundContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_agent_ground}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_agent_ground(AVScenariosParser.Assign_agent_groundContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_ego_state}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_ego_state(AVScenariosParser.Assign_ego_stateContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_ego_state}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_ego_state(AVScenariosParser.Assign_ego_stateContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_agent_state}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_agent_state(AVScenariosParser.Assign_agent_stateContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_agent_state}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_agent_state(AVScenariosParser.Assign_agent_stateContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_speed}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_speed(AVScenariosParser.Assign_speedContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_speed}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_speed(AVScenariosParser.Assign_speedContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assign_position_range_extension}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void enterAssign_position_range_extension(AVScenariosParser.Assign_position_range_extensionContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assign_position_range_extension}
	 * labeled alternative in {@link AVScenariosParser#assignment_statement}.
	 * @param ctx the parse tree
	 */
	void exitAssign_position_range_extension(AVScenariosParser.Assign_position_range_extensionContext ctx);
	/**
	 * Enter a parse tree produced by {@link AVScenariosParser#identifier}.
	 * @param ctx the parse tree
	 */
	void enterIdentifier(AVScenariosParser.IdentifierContext ctx);
	/**
	 * Exit a parse tree produced by {@link AVScenariosParser#identifier}.
	 * @param ctx the parse tree
	 */
	void exitIdentifier(AVScenariosParser.IdentifierContext ctx);
	/**
	 * Enter a parse tree produced by {@link AVScenariosParser#arithmetic_operator}.
	 * @param ctx the parse tree
	 */
	void enterArithmetic_operator(AVScenariosParser.Arithmetic_operatorContext ctx);
	/**
	 * Exit a parse tree produced by {@link AVScenariosParser#arithmetic_operator}.
	 * @param ctx the parse tree
	 */
	void exitArithmetic_operator(AVScenariosParser.Arithmetic_operatorContext ctx);
}