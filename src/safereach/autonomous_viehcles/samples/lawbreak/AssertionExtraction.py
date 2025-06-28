import copy
import warnings
from typing import Union, Any, List, Dict
from parser.ast import AST, ASTDumper, Parse
from parser.ast.assertion.assertion import AtomPredicate, KuoHaoWithGeneral, NotWithGeneral, GeneralAssertionWithTemporalOperator, GeneralAssertionWithUnitl, AndWithGeneral, OrWithGeneral, DeriveWithGeneral
from parser.ast.assertion.assertion import Traffic_Rule_Related_APIs, GeneralDistanceStatement, PerceptionDifferenceStatement, VelocityStatement, SpeedStatement, AccelerationStatement, OverallStatement
from parser.ast.base.state import Position, Coordinate, Speed
from parser.ast.assertion.assertion import EgoState, AgentState, AgentGroundTruth
from parser.ast.unresolved.unresolved import NameWithRealValue
import exception
from map_for_bridge import get_map_info

class AllAssertions:
    def __init__(self, spec_trace):
        self.spec_trace_list = spec_trace
        self.ScenarioSpec = []
        self._get_all_general_specification()

    def _get_all_general_specification(self):
        for _i in range(len(self.spec_trace_list)):
            _trace = self.spec_trace_list[_i]
            if _trace.has_assertion():
                temp = _trace.get_general_assertions()
                for _j in range(len(temp)):
                    _assertion = temp[_j].get_assertion()
                    self.ScenarioSpec.append(_assertion)

    def get_specifications_in_scenario(self, scenario_name):
        return self.ScenarioSpec


class SingleAssertion:
    def __init__(self, one_specification, current_map, ego_position=(0, 0, 0)):
        self.specification = one_specification
        self.map_info = current_map
        self.ego_position = copy.deepcopy(ego_position)
        self.dis_variables = []
        self.dis_statement = dict()
        self.diff_variables = []
        self.diff_statement = dict()
        self.vel_variables = []
        self.vel_statement = dict()
        self.spd_variables = []
        self.spd_statement = dict()
        self.acc_variables = []
        self.acc_statement = dict()
        self.atom_statement_variable_mapping = dict()  # {var1: AtomStatement, var2: AtomStatement, ...}
        self.atom_statement_No = 0
        self.predicate_variable = []
        self.predicate_statement = dict()
        self.predicate_atom_variables = dict()
        self.predicate_NO = 0
        self.translated_statement = None

        # self.sub_violations = []
        # self.current_sub_violation = dict()
        # self.sub_num = 0

        self.get_specification(self.specification)
        self.sub_violations = self.calculate_neg(one_specification)
        # print(self.calculate_neg(one_specification))
        # print(self.calculate_pos(one_specification))
        # print(len(self.calculate_neg(one_specification)))
        # print(len(self.calculate_pos(one_specification)))
        self.translate()
        # print(self.translated_statement)

    def translate(self):
        _specification = str(self.specification)
        for var in self.dis_variables:
            _specification = _specification.replace(self.atom_statement_variable_mapping[var], var)
        for var in self.diff_variables:
            _specification = _specification.replace(self.atom_statement_variable_mapping[var], var)
        for var in self.vel_variables:
            _specification = _specification.replace(self.atom_statement_variable_mapping[var], var)
        for var in self.spd_variables:
            _specification = _specification.replace(self.atom_statement_variable_mapping[var], var)
        for var in self.acc_variables:
            _specification = _specification.replace(self.atom_statement_variable_mapping[var], var)

        for var in self.predicate_variable:
            _specification = _specification.replace(self.predicate_statement[var], var)
        _specification = _specification.replace('&', 'and')
        _specification = _specification.replace('|', 'or')
        _specification = _specification.replace('~', 'not ')
        _specification = _specification.replace('G', 'always')
        _specification = _specification.replace('F', 'eventually')
        _specification = _specification.replace('X', 'next')
        _specification = _specification.replace('U', 'until')
        self.translated_statement = _specification


    def _get_ego(self):
        return "ego"

    def _get_agent(self, agent_state):
        return agent_state.get_agent().get_name()

    def _get_truth_agent(self, agent_truth_state):
        return agent_truth_state.get_agent().get_name()

    def _get_position(self, position):
        if position.is_normal_coordinate():
            coordinate = position.get_coordinate()
            _x = coordinate.get_x()
            _y = coordinate.get_y()
            if coordinate.has_z():
                _z = coordinate.get_z()
            else:
                _z = 0
            _coordinate = (_x, _y, _z)
            if position.has_frame():
                if position.is_frame_ENU():
                    _frame = "ENU"
                elif position.is_frame_IMU():
                    _frame = "ENU"
                    ego_init_position = self.ego_position
                    _coordinate = (_coordinate[0] + ego_init_position[0], _coordinate[1] + ego_init_position[1], _coordinate[2] + ego_init_position[2])
                elif position.is_frame_WGS84():
                    _frame = "WGS84"
                    exception.FrameError("The current version does not support the WGS84 frame systems.")
            else:
                _frame = "ENU"
            return [_frame, _coordinate]
        elif position.is_relative_coordinate():
            coordinate = position.get_coordinate()
            lane_id = coordinate.get_lane().get_lane_id()
            lane_offset = coordinate.get_distance()
            # lane_config = self.map_info.get_lane_config()
            # max_length = lane_config[lane_id]
            # if lane_offset > max_length:
            #     warnings.warn("The predefined position is out of the given lane, set to the end of the lane.")
            #     lane_offset = max_length
            point = self.map_info.get_position([lane_id, lane_offset])
            return ["ENU", point]

    def _get_cooridnate(self, coordinate):
        _x = coordinate.get_x()
        _y = coordinate.get_y()
        if coordinate.has_z():
            _z = coordinate.get_z()
        else:
            _z = 0
        return (_x, _y, _z)

    def _get_speed(self, speed):
        return speed.get_speed_value()

    def _get_position_element(self, position_element):
        _position = position_element
        if isinstance(_position, EgoState):
            return {'ego': "ego", 'agent': None, 'truth': None, 'position': None}
        elif isinstance(_position, AgentState):
            _agent = self._get_agent(_position)
            return {'ego': None, 'agent': _agent, 'truth': None, 'position': None}
        elif isinstance(_position, AgentGroundTruth):
            _agent = self._get_truth_agent(_position)
            return {'ego': None, 'agent': None, 'truth': _agent, 'position': None}
        elif isinstance(_position, Position):
            _final_position = self._get_position(_position)
            return {'ego': None, 'agent': None, 'truth': None, 'position': _final_position}
        else:
            position_tuple = _position.get_value()
            return {'ego': None, 'agent': None, 'truth': None, 'position': ['ENU', position_tuple]}
        # else:
        #     raise exception.DistanceTypeError("Unsupported element for distance computation!")

    def _get_speed_element(self, speed_element):
        _speed = speed_element
        if isinstance(_speed, EgoState):
            return {'ego': "ego", 'agent': None, 'truth': None, 'speed': None}
        elif isinstance(_speed, AgentState):
            _agent = self._get_agent(_speed)
            return {'ego': None, 'agent': _agent, 'truth': None, 'speed': None}
        elif isinstance(_speed, AgentGroundTruth):
            _agent = self._get_truth_agent(_speed)
            return {'ego': None, 'agent': None, 'truth': _agent, 'speed': None}
        else:
            _final_speed = _speed.get_value()
            return {'ego': None, 'agent': None, 'truth': None, 'speed': _final_speed}
        # elif isinstance(_speed, Speed):
        #     _final_speed = self._get_speed(_speed)
        #     return {'ego': None, 'agent': None, 'truth': None, 'speed': _final_speed}
        # else:
        #     raise exception.DistanceTypeError("Unsupported element for speed computation!")

    def _get_velocity_element(self, velocity_element):
        _velocity = velocity_element
        if isinstance(_velocity, EgoState):
            return {'ego': "ego", 'agent': None, 'truth': None, 'velocity': None}
        elif isinstance(_velocity, AgentState):
            _agent = self._get_agent(_velocity)
            return {'ego': None, 'agent': _agent, 'truth': None, 'velocity': None}
        elif isinstance(_velocity, AgentGroundTruth):
            _agent = self._get_truth_agent(_velocity)
            return {'ego': None, 'agent': None, 'truth': _agent, 'velocity': None}
        elif isinstance(_velocity, Coordinate):
            _final_velocity = self._get_cooridnate(_velocity) # (x, y, z)
            return {'ego': None, 'agent': None, 'truth': None, 'velocity': _final_velocity}
        else:
            _final_velocity = _velocity.get_value()
            return {'ego': None, 'agent': None, 'truth': None, 'velocity': _final_velocity}
        # else:
        #     raise exception.DistanceTypeError("Unsupported element for velocity computation!")

    def _get_acc_element(self, acc_element):
        _acc = acc_element
        if isinstance(_acc, EgoState):
            return {'ego': "ego", 'agent': None, 'truth': None, 'acceleration': None}
        elif isinstance(_acc, AgentState):
            _agent = self._get_agent(_acc)
            return {'ego': None, 'agent': _agent, 'truth': None, 'acceleration': None}
        elif isinstance(_acc, AgentGroundTruth):
            _agent = self._get_truth_agent(_acc)
            return {'ego': None, 'agent': None, 'truth': _agent, 'acceleration': None}
        elif isinstance(_acc, Coordinate):
            _final_acc = self._get_cooridnate(_acc)
            return {'ego': None, 'agent': None, 'truth': None, 'acceleration': _final_acc}
        else:
            _final_acc = _acc.get_value()
            return {'ego': None, 'agent': None, 'truth': None, 'acceleration': _final_acc}
        # else:
        #     raise exception.DistanceTypeError("Unsupported element for acceleration computation!")

    def get_predicate_statements(self, statement):
        _statement = statement
        if isinstance(_statement, Traffic_Rule_Related_APIs):
            # print('!!!!!!!!!')
            # print(_statement)
            pass
        elif isinstance(_statement, GeneralDistanceStatement):
            self.atom_statement_No += 1
            _variable = 'p' + str(self.atom_statement_No)
            self.atom_statement_variable_mapping[_variable] = _statement.__str__()
            self.dis_variables.append(_variable)
            self.dis_statement[_variable] = [{'ego': None, 'agent': None, 'truth': None, 'position': None},
                                             {'ego': None, 'agent': None, 'truth': None, 'position': None}]
            left_position = _statement.get_position_element_left()
            self.dis_statement[_variable][0] = self._get_position_element(left_position)
            right_position = _statement.get_position_element_right()
            self.dis_statement[_variable][1] = self._get_position_element(right_position)

            self.predicate_NO += 1
            _predicate_variable = 'q' + str(self.predicate_NO)
            self.predicate_variable.append(_predicate_variable)
            self.predicate_statement[_predicate_variable] = _variable
            self.predicate_atom_variables[_predicate_variable] = [_variable]
        elif isinstance(_statement, PerceptionDifferenceStatement):
            self.atom_statement_No += 1
            _variable = 'p' + str(self.atom_statement_No)
            self.diff_variables.append(_variable)
            self.atom_statement_variable_mapping[_variable] = _statement.__str__()
            agent_element = _statement.get_agent_state()
            truth_element = _statement.get_agent_ground_truth()
            _agent_name1 = self._get_agent(agent_element)
            _agent_name2 = self._get_truth_agent(truth_element)
            if _agent_name1 != _agent_name2:
                raise exception.PerceptionDiffError("Cannot compute perception errors for different agents")
            else:
                self.diff_statement[_variable] = _agent_name2

            self.predicate_NO += 1
            _predicate_variable = 'q' + str(self.predicate_NO)
            self.predicate_variable.append(_predicate_variable)
            self.predicate_statement[_predicate_variable] = _variable
            self.predicate_atom_variables[_predicate_variable] = [_variable]
        elif isinstance(_statement, VelocityStatement):
            self.atom_statement_No += 1
            _variable = 'p' + str(self.atom_statement_No)
            self.vel_variables.append(_variable)
            self.atom_statement_variable_mapping[_variable] = _statement.__str__()
            left_velocity = _statement.get_velocity_element_left()
            right_velocity = _statement.get_velocity_element_right()
            self.vel_statement[_variable] = [{'ego': None, 'agent': None, 'truth': None, 'velocity': None},
                                             {'ego': None, 'agent': None, 'truth': None, 'velocity': None}]
            self.vel_statement[_variable][0] = self._get_velocity_element(left_velocity)
            self.vel_statement[_variable][1] = self._get_velocity_element(right_velocity)

            self.predicate_NO += 1
            _predicate_variable = 'q' + str(self.predicate_NO)
            self.predicate_variable.append(_predicate_variable)
            self.predicate_statement[_predicate_variable] = _variable
            self.predicate_atom_variables[_predicate_variable] = [_variable]
        elif isinstance(_statement, SpeedStatement):
            self.atom_statement_No += 1
            _variable = 'p' + str(self.atom_statement_No)
            self.spd_variables.append(_variable)
            self.atom_statement_variable_mapping[_variable] = _statement.__str__()
            left_speed = _statement.get_speed_element_left()
            right_speed = _statement.get_speed_element_right()
            self.spd_statement[_variable] = [{'ego': None, 'agent': None, 'truth': None, 'speed': None},
                                             {'ego': None, 'agent': None, 'truth': None, 'speed': None}]
            self.spd_statement[_variable][0] = self._get_speed_element(left_speed)
            self.spd_statement[_variable][1] = self._get_speed_element(right_speed)

            self.predicate_NO += 1
            _predicate_variable = 'q' + str(self.predicate_NO)
            self.predicate_variable.append(_predicate_variable)
            self.predicate_statement[_predicate_variable] = _variable
            self.predicate_atom_variables[_predicate_variable] = [_variable]
        elif isinstance(_statement, AccelerationStatement):
            self.atom_statement_No += 1
            _variable = 'p' + str(self.atom_statement_No)
            self.acc_variables.append(_variable)
            self.atom_statement_variable_mapping[_variable] = _statement.__str__()
            left_acc = _statement.get_acceleration_element_left()
            right_acc = _statement.get_acceleration_element_right()
            self.acc_statement[_variable] = [{'ego': None, 'agent': None, 'truth': None, 'acceleration': None},
                                             {'ego': None, 'agent': None, 'truth': None, 'acceleration': None}]
            self.acc_statement[_variable][0] = self._get_acc_element(left_acc)
            self.acc_statement[_variable][1] = self._get_acc_element(right_acc)

            self.predicate_NO += 1
            _predicate_variable = 'q' + str(self.predicate_NO)
            self.predicate_variable.append(_predicate_variable)
            self.predicate_statement[_predicate_variable] = _variable
            self.predicate_atom_variables[_predicate_variable] = [_variable]
        elif isinstance(_statement, str) or isinstance(_statement, NameWithRealValue):
            pass
        elif isinstance(_statement, OverallStatement):
            self.predicate_NO += 1
            _predicate_variable = 'q' + str(self.predicate_NO)
            # self.predicate_variable.append(_predicate_variable)
            _statement_str = _statement.__str__()
            # self.predicate_statement[_predicate_variable] =
            atom_statement_variable = []
            atom_statement_variable_mapping = dict()
            statements = _statement.get_statements()
            # operators = _statement.get_operators()
            for i in range(len(statements)):
                self.get_substatements(statements[i], atom_statement_variable, atom_statement_variable_mapping)

            if len(atom_statement_variable):
                for item in atom_statement_variable:
                    _statement_str = _statement_str.replace(atom_statement_variable_mapping[item], item)
                self.predicate_variable.append(_predicate_variable)
                self.predicate_statement[_predicate_variable] = _statement_str
                self.predicate_atom_variables[_predicate_variable] = atom_statement_variable
        else:
            # print(_statement)
            raise exception.StatementTypeError("Unsupported statements in {}".format(_statement.__str__()))

    def get_substatements(self, statement, atom_statement_variable, atom_statement_variable_mapping):
        _statement = statement
        if isinstance(_statement, Traffic_Rule_Related_APIs):
            # print('!!!!!!!!!')
            # print(_statement)
            pass
            # self.atom_statement_No += 1
            # _variable = 'p' + str(self.atom_statement_No)
            # _variable = _statement.get_API()

            # atom_statement_variable.append(_variable)
            # atom_statement_variable_mapping[_variable] = _statement.__str__()

        elif isinstance(_statement, GeneralDistanceStatement):
            self.atom_statement_No += 1
            _variable = 'p' + str(self.atom_statement_No)
            self.atom_statement_variable_mapping[_variable] = _statement.__str__()
            self.dis_variables.append(_variable)
            self.dis_statement[_variable] = [{'ego': None, 'agent': None, 'truth': None, 'position': None},
                                             {'ego': None, 'agent': None, 'truth': None, 'position': None}]
            left_position = _statement.get_position_element_left()
            self.dis_statement[_variable][0] = self._get_position_element(left_position)
            right_position = _statement.get_position_element_right()
            self.dis_statement[_variable][1] = self._get_position_element(right_position)

            atom_statement_variable.append(_variable)
            atom_statement_variable_mapping[_variable] = _statement.__str__()
        elif isinstance(_statement, PerceptionDifferenceStatement):
            self.atom_statement_No += 1
            _variable = 'p' + str(self.atom_statement_No)
            self.diff_variables.append(_variable)
            self.atom_statement_variable_mapping[_variable] = _statement.__str__()
            agent_element = _statement.get_agent_state()
            truth_element = _statement.get_agent_ground_truth()
            _agent_name1 = self._get_agent(agent_element)
            _agent_name2 = self._get_truth_agent(truth_element)
            if _agent_name1 != _agent_name2:
                raise exception.PerceptionDiffError("Cannot compute perception errors for different agents")
            else:
                self.diff_statement[_variable] = _agent_name2

            atom_statement_variable.append(_variable)
            atom_statement_variable_mapping[_variable] = _statement.__str__()
        elif isinstance(_statement, VelocityStatement):
            self.atom_statement_No += 1
            _variable = 'p' + str(self.atom_statement_No)
            self.vel_variables.append(_variable)
            self.atom_statement_variable_mapping[_variable] = _statement.__str__()
            left_velocity = _statement.get_velocity_element_left()
            right_velocity = _statement.get_velocity_element_right()
            self.vel_statement[_variable] = [{'ego': None, 'agent': None, 'truth': None, 'velocity': None},
                                             {'ego': None, 'agent': None, 'truth': None, 'velocity': None}]
            self.vel_statement[_variable][0] = self._get_velocity_element(left_velocity)
            self.vel_statement[_variable][1] = self._get_velocity_element(right_velocity)

            atom_statement_variable.append(_variable)
            atom_statement_variable_mapping[_variable] = _statement.__str__()
        elif isinstance(_statement, SpeedStatement):
            self.atom_statement_No += 1
            _variable = 'p' + str(self.atom_statement_No)
            self.spd_variables.append(_variable)
            self.atom_statement_variable_mapping[_variable] = _statement.__str__()
            left_speed = _statement.get_speed_element_left()
            right_speed = _statement.get_speed_element_right()
            self.spd_statement[_variable] = [{'ego': None, 'agent': None, 'truth': None, 'speed': None},
                                             {'ego': None, 'agent': None, 'truth': None, 'speed': None}]
            self.spd_statement[_variable][0] = self._get_speed_element(left_speed)
            self.spd_statement[_variable][1] = self._get_speed_element(right_speed)

            atom_statement_variable.append(_variable)
            atom_statement_variable_mapping[_variable] = _statement.__str__()
        elif isinstance(_statement, AccelerationStatement):
            self.atom_statement_No += 1
            _variable = 'p' + str(self.atom_statement_No)
            self.acc_variables.append(_variable)
            self.atom_statement_variable_mapping[_variable] = _statement.__str__()
            left_acc = _statement.get_acceleration_element_left()
            right_acc = _statement.get_acceleration_element_right()
            self.acc_statement[_variable] = [{'ego': None, 'agent': None, 'truth': None, 'acceleration': None},
                                             {'ego': None, 'agent': None, 'truth': None, 'acceleration': None}]
            self.acc_statement[_variable][0] = self._get_acc_element(left_acc)
            self.acc_statement[_variable][1] = self._get_acc_element(right_acc)

            atom_statement_variable.append(_variable)
            atom_statement_variable_mapping[_variable] = _statement.__str__()
        elif isinstance(_statement, str) or isinstance(_statement, NameWithRealValue):
            pass
        elif isinstance(_statement, OverallStatement):
            statements = _statement.get_statements()
            # operators = _statement.get_operators()
            for i in range(len(statements)):
                self.get_substatements(statements[i], atom_statement_variable, atom_statement_variable_mapping)
        else:
            raise exception.StatementTypeError("Unsupported statements in {}".format(_statement.__str__()))

    def get_specification(self, one_specification):
        _specification = one_specification
        if isinstance(_specification, AtomPredicate):
            left_statement = _specification.get_atom_statement_left()
            right_statement = _specification.get_atom_statement_right()
            self.get_predicate_statements(left_statement)
            self.get_predicate_statements(right_statement)
        elif isinstance(_specification, KuoHaoWithGeneral):
            assertion_in_bracket = _specification.get_assertion()
            self.get_specification(assertion_in_bracket)
        elif isinstance(_specification, NotWithGeneral):
            _assertion = _specification.get_assertion()
            self.get_specification(_assertion)
        elif isinstance(_specification, GeneralAssertionWithTemporalOperator):
            assertion = _specification.get_assertion()
            self.get_specification(assertion)
        elif isinstance(_specification, GeneralAssertionWithUnitl):
            left_assertion = _specification.get_general_assertion_left()
            self.get_specification(left_assertion)
            right_assertion = _specification.get_general_assertion_right()
            self.get_specification(right_assertion)
        elif isinstance(_specification, AndWithGeneral):
            left_assertion = _specification.get_general_assertion_left()
            self.get_specification(left_assertion)
            right_assertion = _specification.get_general_assertion_right()
            self.get_specification(right_assertion)
        elif isinstance(_specification, OrWithGeneral):
            left_assertion = _specification.get_general_assertion_left()
            self.get_specification(left_assertion)
            right_assertion = _specification.get_general_assertion_right()
            self.get_specification(right_assertion)
        elif isinstance(_specification, DeriveWithGeneral):
            left_assertion = _specification.get_general_assertion_left()
            self.get_specification(left_assertion)
            right_assertion = _specification.get_general_assertion_right()
            self.get_specification(right_assertion)
        else:
            raise exception.AssertionTypeError("Wrong type of assertion!")


    def calculate_neg(self, one_specification):
        _specification = one_specification
        if isinstance(_specification, AtomPredicate):
            result = []
            left_statement = _specification.get_atom_statement_left()
            right_statement = _specification.get_atom_statement_right()
            compare_operator = _specification.get_compare_operator()
            temp = "not"+'('+str(left_statement) + str(compare_operator) + str(right_statement)+')'
            result.append(temp)
            return result

        elif isinstance(_specification, KuoHaoWithGeneral):
            assertion_in_bracket = _specification.get_assertion()
            return self.calculate_neg(assertion_in_bracket)

        elif isinstance(_specification, NotWithGeneral):
            _assertion = _specification.get_assertion()
            return self.calculate_pos(_assertion)

        elif isinstance(_specification, GeneralAssertionWithTemporalOperator):
            result = []
            assertion = _specification.get_assertion()
            temporal_operator = _specification.get_temporal_operator()
            if "G" in temporal_operator:
                temporal_operator0 = temporal_operator.replace('G', 'eventually')
            elif "F" in temporal_operator:
                temporal_operator0 = temporal_operator.replace('F', 'always')
            elif "X" in temporal_operator:
                temporal_operator0 = temporal_operator.replace('X', 'next')
            else:
                print("Bug! Something go wrong with temporal_operator: " + str(temporal_operator))
            temp = self.calculate_neg(assertion)
            for item in temp:
                a = temporal_operator0 + "(" + item + ")"
                result.append(a)
            return result


        elif isinstance(_specification, GeneralAssertionWithUnitl):
            result = []
            result0 = []
            result1 = []
            left_assertion = _specification.get_general_assertion_left()
            a1 = self.calculate_neg(left_assertion)
            b1 = self.calculate_pos(left_assertion)
            right_assertion = _specification.get_general_assertion_right()
            a2 = self.calculate_neg(right_assertion)
            for _i in a1:
                for _j in a2:
                    temp = '(' + _i + ')' + "and" + '(' + _j + ')'
                    result0.append(temp)
                    result.append(temp)
            for _i in b1:
                for _j in a2:
                    temp = '(' + _i + ')' + "and" + '(' + _j + ')'
                    result1.append(temp)
            for _i in result1:
                for _j in result0:
                    temp = '(' + _i + ')' + "until" + '(' + _j + ')'
                    result.append(temp)
            return result


        elif isinstance(_specification, AndWithGeneral):
            result = []
            left_assertion = _specification.get_general_assertion_left()
            a1 = self.calculate_neg(left_assertion)
            right_assertion = _specification.get_general_assertion_right()
            a2 = self.calculate_neg(right_assertion)
            for item in a1:
                result.append(item)
            for item in a2:
                result.append(item)
            return result


        elif isinstance(_specification, OrWithGeneral):
            result = []
            left_assertion = _specification.get_general_assertion_left()
            a1 = self.calculate_neg(left_assertion)
            right_assertion = _specification.get_general_assertion_right()
            a2 = self.calculate_neg(right_assertion)
            for _i in a1:
                for _j in a2:
                    temp = '(' + _i + ')' + "and" + '(' + _j + ')'
                    result.append(temp)
            return result


        elif isinstance(_specification, DeriveWithGeneral):
            result = []
            left_assertion = _specification.get_general_assertion_left()
            a1 = self.calculate_pos(left_assertion)
            right_assertion = _specification.get_general_assertion_right()
            a2 = self.calculate_neg(right_assertion)
            for _i in a1:
                for _j in a2:
                    temp = '(' + _i + ')' + "and" + '(' + _j + ')'
                    result.append(temp)
            return result
        else:
            raise exception.AssertionTypeError("Wrong type of assertion!")


    def calculate_pos(self, one_specification):
        _specification = one_specification
        if isinstance(_specification, AtomPredicate):
            result = []
            left_statement = _specification.get_atom_statement_left()
            right_statement = _specification.get_atom_statement_right()
            compare_operator = _specification.get_compare_operator()
            temp = str(left_statement) + str(compare_operator) + str(right_statement)
            result.append(temp)
            return result

        elif isinstance(_specification, KuoHaoWithGeneral):
            assertion_in_bracket = _specification.get_assertion()
            return self.calculate_pos(assertion_in_bracket)

        elif isinstance(_specification, NotWithGeneral):
            _assertion = _specification.get_assertion()
            return self.calculate_neg(_assertion)

        elif isinstance(_specification, GeneralAssertionWithTemporalOperator):
            result = []
            assertion = _specification.get_assertion()
            temporal_operator = _specification.get_temporal_operator()
            if "F" in temporal_operator:
                temporal_operator0 = temporal_operator.replace('F', 'eventually')
            elif "G" in temporal_operator:
                temporal_operator0 = temporal_operator.replace('G', 'always')
            elif "X" in temporal_operator:
                temporal_operator0 = temporal_operator.replace('X', 'next')
            else:
                print("Bug! Something go wrong with temporal_operator: " + str(temporal_operator))
            temp = self.calculate_pos(assertion)
            for item in temp:
                a = temporal_operator0 + "(" + item + ")"
                result.append(a)
            return result


        elif isinstance(_specification, GeneralAssertionWithUnitl):
            result = []
            result0 = []
            result1 = []
            left_assertion = _specification.get_general_assertion_left()
            a1 = self.calculate_pos(left_assertion)
            right_assertion = _specification.get_general_assertion_right()
            a2 = self.calculate_pos(right_assertion)
            for _i in a1:
                for _j in a2:
                    temp = '(' + _i + ')' + "until" + '(' + _j + ')'
                    result.append(temp)
            return result


        elif isinstance(_specification, AndWithGeneral):
            result = []
            left_assertion = _specification.get_general_assertion_left()
            a1 = self.calculate_pos(left_assertion)
            right_assertion = _specification.get_general_assertion_right()
            a2 = self.calculate_pos(right_assertion)
            for _i in a1:
                for _j in a2:
                    temp = '(' + _i + ')' + "and" + '(' + _j + ')'
                    result.append(temp)
            return result

            
        elif isinstance(_specification, OrWithGeneral):
            result = []
            left_assertion = _specification.get_general_assertion_left()
            a1 = self.calculate_pos(left_assertion)
            right_assertion = _specification.get_general_assertion_right()
            a2 = self.calculate_pos(right_assertion)
            for item in a1:
                result.append(item)
            for item in a2:
                result.append(item)
            return result


        elif isinstance(_specification, DeriveWithGeneral):
            result = []
            left_assertion = _specification.get_general_assertion_left()
            a1 = self.calculate_neg(left_assertion)
            right_assertion = _specification.get_general_assertion_right()
            a2 = self.calculate_pos(right_assertion)
            for item in a1:
                result.append(item)
            for item in a2:
                result.append(item)
            return result
        else:
            raise exception.AssertionTypeError("Wrong type of assertion!")

if __name__ == "__main__":
    input_file = 'input-test.txt'
    ast_ = Parse(input_file)
    trace_list = ast_.get_traces()
    scenario_name = 'scenario0'

    specification_obj = AllAssertions(trace_list)
    specification = specification_obj.get_specifications_in_scenario(scenario_name)
    spec_NO = len(specification)
    map_name = specification_obj.ScenarioMap[scenario_name]
    ego_position = (553090.0522572036, 4182687.8, 0)
    single_spec_class = SingleAssertion(specification[0], map_name, ego_position)
    for i in range(spec_NO):
        single_spec_class = SingleAssertion(specification[i], map_name, ego_position)
        print("Specification {}: ".format(1))
        print(single_spec_class.translated_statement)
        print(single_spec_class.atom_statement_variable_mapping)
        print(single_spec_class.specification)
    # for i in range(spec_NO):
    #     single_spec_class = SingleAssertion(specification[i])
    #     print("Specification {}: ".format(i))
    #     print(single_spec_class.translated_statement)
    #     print(single_spec_class.atom_statement_variable_mapping)







