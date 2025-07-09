import rtamt
import sys
import numpy as np
from TracePreprocess import Trace
import json
import copy 
from antlr4 import *
from antlr4.InputStream import InputStream
from AssertionExtraction import SingleAssertion, ExtractAll
from shapely.geometry import Polygon, Point 

inf_value = 1000

def polygon2polygon_distance(polygon_list1, polygon_list2):
    distance = []
    n = np.min(len(polygon_list1), len(polygon_list2))
    for i in range(n):
        if polygon_list1[i] == [] or polygon_list2 == []:
            distance.append(inf_value)
        else:
            polygon1 = Polygon(polygon_list1[i])
            polygon2 = Polygon(polygon_list2[i])
            distance.append(polygon1.distance(polygon2))
    return np.array(distance)


def polygon2point_distance(polygon_list, point):
    '''

    Args:
        p: [x, y]
        polygon_list: [p1, p2, p3]
        point: [x, y]
    Returns:

    '''
    distance = []
    p = Point(point)
    for i in range(len(polygon_list)):
        polygon = Polygon(polygon_list[i])
        distance.append(polygon.distance(p))
    return np.array(distance)


def velocitylist_distance(list1, list2):
    n = min(len(list1), len(list2))
    v1 = np.array(list1)[0:n, 0:2]
    v2 = np.array(list2)[0:n, 0:2]
    vel_dis = np.linalg.norm(v1 - v2, axis=1)
    return vel_dis


def velocitylist2point_distance(list1, velocity_point):
    v1 = np.array(list1)[:, 0:2]
    v_point = np.array(velocity_point)[0:2]
    vel_dis = np.linalg.norm(v1 - v_point, axis=1)
    return vel_dis


def acclist_distance(list1, list2):
    n = min(len(list1), len(list2))
    acc1 = np.array(list1)[0:n, 0:2]
    acc2 = np.array(list2)[0:n, 0:2]
    acc_dis = np.linalg.norm(acc1 - acc2, axis=1)
    return acc_dis


def acclist2point_distance(list1, acc_point):
    acc1 = np.array(list1)[:, 0:2]
    acc_point = np.array(acc_point)[0:2]
    acc_dis = np.linalg.norm(acc1 - acc_point, axis=1)
    return acc_dis


def speed_value(velocity_list):
    velocity_array = np.array(velocity_list)[:, 0:2]
    speed_array = np.linalg.norm(velocity_array, axis=1)
    return speed_array


def speedlist_distance(velocity_list1, velocity_list2):
    speed1 = speed_value(velocity_list1)
    speed2 = speed_value(velocity_list2)
    spd_dis = speed1 - speed2
    return spd_dis


def speedlist2point_distance(velocity_list, speed_point):
    speed = speed_value(velocity_list)
    spd_dis = speed - speed_point
    return spd_dis

class Monitor:
    def __init__(self, returned_msg, specification, weather):
        self.specification = copy.deepcopy(specification)
        self.isGroundTruth = returned_msg['groundTruthPerception']
        self.original_data = copy.deepcopy(returned_msg['trace'])
        self.atom_data = dict()
        self.data = dict()
        self.c_data = dict()
        self.robustness_list = {}
        self.weather_raw = weather
        # self.time_raw = returned_msg["time"]

        self.item_names_of_variable_of_APIS = []
        self.traffic_rules = None
        self.muti_traffic_rules = dict()

        self.preprocessed_data = Trace(returned_msg)
        self.prepare_data()

    def prepare_data(self): 
        self.prepare_for_rules()
        # print("direction")
        # print(self.c_data["direction"])
        # print("isTurningAround")
        # print(self.c_data["isTurningAround"])

    def prepare_traffic_rule_related_APIs(self, _time ,state_len , _var_data, name_of_vaiable):

        self.c_data[name_of_vaiable] = [[_time[i], _var_data[i]] for i in range(state_len)]
        self.data[name_of_vaiable] = _var_data[:state_len]

    def prepare_for_rules(self):
        state_len = len(self.original_data)

        _time = self.preprocessed_data.trace['time']
        self.c_data['time'] = [[i, _time[i]] for i in range(state_len)]

        self.data['time'] = [i for i in range(state_len)]
        self.data['t'] = self.preprocessed_data.trace['time'][:state_len]
        TRACE = self.preprocessed_data.trace

        for key in TRACE["ego-forTrafficRule"]:
            name_of_vaiable = str(key)
            self.prepare_traffic_rule_related_APIs( _time ,state_len , TRACE["ego-forTrafficRule"][key], name_of_vaiable)
            self.item_names_of_variable_of_APIS.append(name_of_vaiable)

        for key in TRACE["ego-driving-forTrafficRule"]:
            name_of_vaiable = str(key)
            self.prepare_traffic_rule_related_APIs( _time ,state_len , TRACE["ego-driving-forTrafficRule"][key], name_of_vaiable)
            self.item_names_of_variable_of_APIS.append(name_of_vaiable)
        
        for key in TRACE["currentlane-forTrafficRule"]:
            name_of_vaiable = 'currentLane' + str(key)
            self.prepare_traffic_rule_related_APIs( _time ,state_len , TRACE["currentlane-forTrafficRule"][key], name_of_vaiable)
            self.item_names_of_variable_of_APIS.append(name_of_vaiable)

        for key in TRACE["speedLimit-forTrafficRule"]:
            name_of_vaiable = 'speedLimit' + str(key)
            self.prepare_traffic_rule_related_APIs( _time ,state_len , TRACE["speedLimit-forTrafficRule"][key], name_of_vaiable)
            self.item_names_of_variable_of_APIS.append(name_of_vaiable)

        for key in TRACE["road-forTrafficRule"]:
            name_of_vaiable = str(key)
            self.prepare_traffic_rule_related_APIs( _time ,state_len ,  TRACE["road-forTrafficRule"][key], name_of_vaiable)
            self.item_names_of_variable_of_APIS.append(name_of_vaiable)

        for key in TRACE["specialLocationAhead-forTrafficRule"]:
            name_of_vaiable = 'specialLocationAhead' + str(key)
            self.prepare_traffic_rule_related_APIs( _time ,state_len , TRACE["specialLocationAhead-forTrafficRule"][key], name_of_vaiable)
            self.item_names_of_variable_of_APIS.append(name_of_vaiable)

        for key in TRACE["trafficLightAhead-forTrafficRule"]:
            name_of_vaiable = 'trafficLightAhead' + str(key)
            # print(name_of_vaiable)
            self.prepare_traffic_rule_related_APIs( _time ,state_len , TRACE["trafficLightAhead-forTrafficRule"][key], name_of_vaiable)
            self.item_names_of_variable_of_APIS.append(name_of_vaiable)


        for key in TRACE["traffic-forTrafficRule"]:
            name_of_vaiable = str(key)
            self.prepare_traffic_rule_related_APIs( _time ,state_len , TRACE["traffic-forTrafficRule"][key], name_of_vaiable)
            self.item_names_of_variable_of_APIS.append(name_of_vaiable)

        for key in TRACE["NPCAhead-forTrafficRule"]:
            name_of_vaiable = 'NPCAhead' + str(key)
            self.prepare_traffic_rule_related_APIs( _time ,state_len , TRACE["NPCAhead-forTrafficRule"][key], name_of_vaiable)
            self.item_names_of_variable_of_APIS.append(name_of_vaiable)

        for key in TRACE["NearestNPC-forTrafficRule"]:
            name_of_vaiable = 'NearestNPC' + str(key)
            self.prepare_traffic_rule_related_APIs( _time ,state_len , TRACE["NearestNPC-forTrafficRule"][key], name_of_vaiable)
            self.item_names_of_variable_of_APIS.append(name_of_vaiable)

        for key in TRACE["NPCOpposite-forTrafficRule"]:
            name_of_vaiable = 'NPCOpposite' + str(key)
            self.prepare_traffic_rule_related_APIs( _time ,state_len , TRACE["NPCOpposite-forTrafficRule"][key], name_of_vaiable)
            self.item_names_of_variable_of_APIS.append(name_of_vaiable)

        for key in self.weather_raw:
            name_of_vaiable = str(key)
            data = [self.weather_raw[key]] * state_len
            self.prepare_traffic_rule_related_APIs( _time ,state_len , data, name_of_vaiable)
            self.item_names_of_variable_of_APIS.append(name_of_vaiable)

        for key in TRACE["trafficLightAhead-arrow-direction-forTrafficRule"]:
            name_of_vaiable = 'trafficLightAheadArrowDirection' + str(key)
            self.prepare_traffic_rule_related_APIs( _time ,state_len , TRACE["trafficLightAhead-arrow-direction-forTrafficRule"][key], name_of_vaiable)
            self.item_names_of_variable_of_APIS.append(name_of_vaiable)

        name_of_vaiable = 'snow'
        data = [0] * state_len
        self.prepare_traffic_rule_related_APIs( _time ,state_len , data, name_of_vaiable)
        self.item_names_of_variable_of_APIS.append(name_of_vaiable)

        name_of_vaiable = 'visibility'
        data = [100] * state_len
        self.prepare_traffic_rule_related_APIs( _time ,state_len , data, name_of_vaiable)
        self.item_names_of_variable_of_APIS.append(name_of_vaiable)


        # name_of_vaiable = 'Time'
        # data = [int(self.time_raw['hour']) + int(self.time_raw['minute'])/60 ] * state_len
        # self.prepare_traffic_rule_related_APIs( _time ,state_len , data, name_of_vaiable)
        # self.item_names_of_variable_of_APIS.append(name_of_vaiable)
 
        rule38_1 = self.prepare_for_rule38_1()
        rule38_2 = self.prepare_for_rule38_2()
        rule38_3 = self.prepare_for_rule38_3() #for the normal red,yelow,green traffic lights
        rule42 = self.prepare_for_rule42()     #for the blink yellow light
        rule44 = self.prepare_for_rule44()     #for the lane change and speed limit
        rule45 = self.prepare_for_rule45()     #for pure speed limit
        rule46_2 = self.prepare_for_rule46_2()
        rule46_3 = self.prepare_for_rule46_3()
        # rule47 = self.prepare_for_rule47()
        rule50 = self.prepare_for_rule50()
        # rule51_3 = self.prepare_for_rule51_3()
        rule51_4 = self.prepare_for_rule51_4()
        rule51_5 = self.prepare_for_rule51_5()
        rule51_6 = self.prepare_for_rule51_6()
        rule51_7 = self.prepare_for_rule51_7()
        rule52 = self.prepare_for_rule52()
        rule53 = self.prepare_for_rule53()
        # rule57 = self.prepare_for_rule57()
        # rule58 = self.prepare_for_rule58()
        # rule59 = self.prepare_for_rule59()
        # rule62 = self.prepare_for_rule62()

        

        self.muti_traffic_rules["rule38_1"] = rule38_1
        self.muti_traffic_rules["rule38_2"] = rule38_2
        self.muti_traffic_rules["rule38_3"] = rule38_3
        self.muti_traffic_rules["rule42"] = rule42
        self.muti_traffic_rules["rule44"] = rule44
        self.muti_traffic_rules["rule45"] = rule45
        self.muti_traffic_rules["rule46_2"] = rule46_2
        self.muti_traffic_rules["rule46_3"] = rule46_3
        # self.muti_traffic_rules["rule47"] = rule47
        self.muti_traffic_rules["rule50"] = rule50
        # self.muti_traffic_rules["rule51_3"] = rule51_3
        self.muti_traffic_rules["rule51_4"] = rule51_4
        self.muti_traffic_rules["rule51_5"] = rule51_5
        self.muti_traffic_rules["rule51_6"] = rule51_6
        self.muti_traffic_rules["rule51_7"] = rule51_7
        self.muti_traffic_rules["rule52"] = rule52
        self.muti_traffic_rules["rule53"] = rule53
        
    def prepare_for_rule38_1(self):              
        #GREEN = 3; 
        traffic_rule = '(\
                                always( (   (   (trafficLightAheadcolor == 3) and \
                                                (PriorityNPCAhead == 0) and (PriorityPedsAhead == 0)    ) \
                                    implies (eventually[0,100](speed > 0.5)) ) \
                                )\
                        )'
        return traffic_rule

    def prepare_for_rule38_2(self):              
        #YELLOW = 2;
        traffic_rule = '(\
                                always(\
                                        ( \
                                            (\
                                                (trafficLightAheadcolor == 2) and ((currentLanenumber == 0))\
                                            ) implies ( eventually[0,100](speed > 0.5) )\
                                        ) and \
                                        ( \
                                            (\
                                                (trafficLightAheadcolor == 2) and ((currentLanenumber > 0))\
                                            ) implies ( eventually[0,100](speed < 0.5) )\
                                        ) \
                                ) \
                            )'
        return traffic_rule

    def prepare_for_rule38_3(self):              
        #RED = 1;   
        traffic_rule = '(\
                                always((((trafficLightAheadcolor == 1) and \
                                    ((stoplineAhead <= 2) or (junctionAhead <= 2)) and\
                                    (currentLanenumber > 0) and \
                                    (direction <= 1)) \
                                    implies ( eventually[0,100](speed < 0.5) )) and \
                                    (((trafficLightAheadcolor == 1) and \
                                    ((stoplineAhead <= 2) or (junctionAhead <= 2)) and \
                                    (direction == 2) and (PriorityNPCAhead == 0) and \
                                    (currentLanenumber > 0) and \
                                    (PriorityPedsAhead == 0) ) \
                                    implies ( eventually[0,100](speed > 0.5) )) ) \
                                )'
        return traffic_rule

    def prepare_for_rule38(self):              
        # message TrafficLight {
        #   enum Color {
        #     UNKNOWN = 0;
        #     RED = 1;
        #     YELLOW = 2;
        #     GREEN = 3;
        #     BLACK = 4;
        #   };       
        # we should put different weight on different variables!
        traffic_rule = '(always(((trafficLightAheadcolor == 3) and ((stoplineAhead <= 2) or (junctionAhead <= 2)) and (PriorityNPCAhead == 0) and (PriorityPedsAhead == 0)) implies ( speed >= 0.1 ))   and \
                                always((((trafficLightAheadcolor == 2) and ((stoplineAhead == 0) or (stoplineAhead > 50))) implies ( speed > 0.1 )) and \
                                        (((trafficLightAheadcolor == 2) and (stoplineAhead <= 2)) implies (speed < 0.1)) ) and \
                                always((((trafficLightAheadcolor == 1) and ((stoplineAhead <= 2) or (junctionAhead <= 2)) and (direction <= 1)) implies ( speed < 0.1 )) and \
                                        (((trafficLightAheadcolor == 1) and ((stoplineAhead <= 2) or (junctionAhead <= 2)) and (direction == 2) and (PriorityNPCAhead == 0) and (PriorityPedsAhead == 0) ) implies ( speed >= 0.1 )) ) \
                                )'
        return traffic_rule

    def prepare_for_rule42(self):
        # \begin{aligned}
        #     & G(((trafficLightAhead.color = yellow \land \\
        #     & trafficLightAhead.blink) \lor \\
        #     & (trafficLightAhead.direction.color = yellow \land \\
        #     & trafficLightAhead.direction.blink)) \land \\
        #     & ( stoplineAhead(realvalue) \lor junctionAhead(realvalue) )\\
        #     & \implies    speed < realvalue )
        # \end{aligned}          
        traffic_rule = '(always(((trafficLightAheadcolor == 2) and \
                                (trafficLightAheadblink == 1) and \
                                ((stoplineAhead <= 1) or (junctionAhead <= 1)))\
                                implies (speed < 5))\
                                )'
        return traffic_rule

    def prepare_for_rule44(self):
        # \begin{aligned}
        #     & G(currentLane.number \geq 2  \implies \\
        #     & (speed \geq speedLimit.lowerLimit \land  \\
        #     & speed \leq speedLimit.upperLimit)) \land \\
        #     & G(isLaneChanging \land   currentLane.number \geq 2 \\
        #     & \implies  \lnot PriorityNPCAhead)
        # \end{aligned}          
        traffic_rule = '(   always( (currentLanenumber >= 201) \
                                    implies ((eventually[0,6000](currentLanenumber >= 201 implies speed >= 20)) and (speed <= speedLimitupperLimit))))'
        return traffic_rule

    def prepare_for_rule45(self):
        # \begin{aligned}
        #     & G(speed \geq speedLimit.lowerLimit  \land \\
        #     & speed \leq speedLimit.upperLimit )
        # \end{aligned}    
        traffic_rule = '(always((speed >= speedLimitlowerLimit) and (speed <= speedLimitupperLimit)))'
        return traffic_rule

    def prepare_for_rule46_2(self):
        # \begin{aligned}
        #     & G( (direction \neq forward) \lor isTurningAround) \\
        #     & \implies   speed \leq 30 )
        # \end{aligned}
        traffic_rule = '(always(((direction == 1) or (direction == 2) or (isTurningAround == 1))\
                                implies (speed <= 30)))'
        return traffic_rule

    def prepare_for_rule46_3(self):
        # \begin{aligned}
        #     & G((Weather.rain \geq 0.5 \lor Weather.fog \geq 0.5 \\
        #     & \lor  Weather.snow \geq 0.5) \land Weather.visibility \leq 50 \\
        #     & \implies speed \leq 30)
        # \end{aligned}
        traffic_rule = '(always(((rain >= 0.5) or (fog >= 0.5) or (snow >= 0.5))\
                                implies (speed <= 30)))'

        return traffic_rule

    def prepare_for_rule47(self):
        # $$
        # \begin{aligned}
            # & G(isOverTaking \implies  turnSignal = left \land \\
            # & (F[-realvalue,\ realvalue](hornOn) \lor \\
            # & ( highBeamOn \land (highBeamOn \\
            # & \implies   F[0,\ realvalue](lowBeamOn) )) \lor \\
            # & ( lowBeamOn \land (lowBeamOn \\
            # & \implies   F[0,\ realvalue](highBeamOn) )))  \land  \\
            # & F[0,\ realvalue]( (turnSignal = right \land \\
            # & isLaneChanging \implies NearestNPC(realvalue) \\
            # & \land isLaneChanging) )
        # \end{aligned}
        # $$
        traffic_rule = '(always((isOverTaking == 1)\
                                implies ( (turnSignal == 1) and \
                                    ((eventually[-1, 2](hornOn == 1)) or \
                                        ( \
                                        ((highBeamOn == 1 ) and \
                                            ((highBeamOn == 1) implies (eventually[0, 2](lowBeamOn == 1))) ) or \
                                        ((lowBeamOn == 1 ) and \
                                            ((lowBeamOn == 1) implies (eventually[0, 2](highBeamOn == 1))) ) \
                                        )\
                                    ) and \
                                    F[0, 10]( (turnSignal == 2) and \
                                        (((isLaneChanging == 1) implies (NearestNPCAhead >= 5)) and (isLaneChanging == 1) ) ) ))\
                        )'

        return traffic_rule

    def prepare_for_rule50(self):
        # \begin{aligned}
        #     & G(speed \geq speedLimit.lowerLimit  \land \\
        #     & speed \leq speedLimit.upperLimit )
        # \end{aligned}    
        traffic_rule = '(always ((not (gear==2))))'
        return traffic_rule

    def prepare_for_rule51_3(self):
        traffic_rule = "(always ((((((((trafficLightAheadcolor==3) and (direction==1)) and (Time<=20.0)) and (Time>=7.0))) -> ((turnSignal==1))) and (((((trafficLightAheadcolor==3) and (direction==1)) and (((Time>=20.0) or (Time<=7.0))))) -> (((turnSignal==1) and (lowBeamOn==1)))))))"
        return traffic_rule

    def prepare_for_rule51_4(self):
        traffic_rule = "(always ((((trafficLightAheadcolor==3) and (((not (NPCAheadAhead<=8.0)) or (((((NPCAheadAhead<=8.0) -> (eventually[0,2] ((NPCAheadspeed>0.5))))) and (NPCAheadAhead<=8.0)))))) -> (((eventually[0,3] ((speed>0.5)))) and (not (NPCAheadAhead<=0.5))))))"
        return traffic_rule

    def prepare_for_rule51_5(self):
        traffic_rule = "(always ((((trafficLightAheadcolor==1) and ((((stoplineAhead<=2.0) or (junctionAhead<=2.0)) or (NPCAheadAhead<=0.5)))) -> (eventually[0,2] ((speed<0.5))))))"
        return traffic_rule

    def prepare_for_rule51_6(self):
        traffic_rule = "(always ((((((direction==2) and (NPCAheadAhead<=2.0)) and ((eventually[0,2] ((NPCAheadspeed<0.5)))))) -> (eventually[0,3] ((speed<0.5))))))"
        return traffic_rule

    def prepare_for_rule51_7(self):
        traffic_rule = "(always (((((((direction==2) or (direction==1))) and (((PriorityNPCAhead==1) or (PriorityPedsAhead==1))))) -> (eventually[0,2] ((speed<0.5))))))"
        return traffic_rule

    def prepare_for_rule52(self):
        traffic_rule = "(\
                        always (\
                                    ((signalAhead==0 and (NPCAheadAhead<=1)) and junctionAhead<=1.0) \
                                    -> (eventually[0,300] (speed<0.5))\
                                ) \
                        )"
        # traffic_rule = "(always (((((signalAhead==0 and ((NPCAheadAhead<=1 or PriorityPedsAhead<=1))) and junctionAhead<=1.0)) -> (eventually[0,200] (speed<0.5)))))"
        return traffic_rule

    def prepare_for_rule53(self):
        traffic_rule = "(always ((((isTrafficJam==1 and (((NPCAheadspeed<0.5 or NPCAheadAhead<=0.5) or junctionAhead<=1.0)))) -> (eventually[0,200] (speed<0.5)))))"
        return traffic_rule

    def prepare_for_rule57(self):
        traffic_rule = "((always ((direction==1 -> turnSignal==1))) and (always ((direction==2 -> turnSignal==2))))"
        return traffic_rule

    def prepare_for_rule58(self):
        traffic_rule = "(always ((((((((((not streetLightOn==1) and ((Time>=20.0 or Time<=7.0)))) or (((rain>=0.5 or fog>=0.5) or snow>=0.5))) and (not NPCAheadAhead<=10.0))) -> highBeamOn==1) and (NPCAheadAhead<=10.0 -> (not highBeamOn==1))) and (fog>=0.5 -> ((fogLightOn==1 and warningflashOn==1))))))"
        return traffic_rule

    def prepare_for_rule59(self):
        traffic_rule = "(always (((((crosswalkAhead<=5.0 or ((signalAhead==0 and junctionAhead<=1.0)))) and ((Time>=20.0 or Time<=7.0))) -> ((eventually[0,3] ((highBeamOn==1 and ((highBeamOn==1 -> (eventually[0,3] (lowBeamOn==1))))))) or (eventually[0,3] ((lowBeamOn==1 and ((lowBeamOn==1 -> (eventually[0,3] (highBeamOn==1)))))))))))"
        return traffic_rule

    def prepare_for_rule62(self):
        traffic_rule = "(always (((not honkingAllowed==1) -> (not hornOn==1))))"
        return traffic_rule

    def continuous_monitor_for_muti_traffic_rules(self):
            # print(item)
        result = dict()
        for key in self.muti_traffic_rules:

            # print()
            spec = rtamt.StlDenseTimeSpecification(semantics=rtamt.Semantics.STANDARD)
            for item in self.item_names_of_variable_of_APIS:
                # print(item)
                spec.declare_var(item, 'float')
            spec.spec = self.muti_traffic_rules[key]
            # print(spec.spec)
            try:
                spec.parse()
                # spec.pastify()

            except Exception as err:
                raise err
                print('STL Parse Exception: {}'.format(err))
                sys.exit()
            _data = [[var, self.c_data[var]] for var in self.item_names_of_variable_of_APIS]

            rob = spec.evaluate(*_data)
            result[key] = rob[0][1]
            del spec
        return result


from rtamt.syntax.node.ltl.predicate import Predicate
# from rtamt.syntax.node.ltl.binary_node import BinaryNode
from rtamt.syntax.ast.visitor.stl.ast_visitor import StlAstVisitor

class PredicateCollector(StlAstVisitor):
    def __init__(self):
        self.predicates = []

        
    def visit(self, node, *args, **kwargs):
        if isinstance(node, Predicate):
            self.visit_predicate(node, args, kwargs)
        else:
            super().visit(node, *args, **kwargs)
        
    def visit_predicate(self, node, *args, **kwargs):
        op = str(node.operator)
        pre_str = node.name
        print(pre_str)
        print(op)
        lhs = pre_str[1:pre_str.find(op)-1]
        rhs = pre_str[pre_str.find(op)+len(op)+1:-1]
        self.predicates.append((lhs, op, rhs))
        # super().visit_predicate( node, args, kwargs)
        
if __name__ == "__main__": 
    import os
    from TracePreprocess import raw_to_lawbreaker_API
    import pickle
    input_file = 'law.txt'
    weather = {'rain' : 0.0,  'snow': 0.0, 'fog' : 0.0}
    isGroundTruth = True
    extracted_script = ExtractAll(input_file,isGroundTruth)
    specification = extracted_script.Get_Specifications()[0]
    # print(specification.dis_variables)
    # print(specification.dis_statement)
    # extracted_data = ExtractAll('law.txt', True)
    # output_file = 'Law38_0_2_record_1.00000.20250618131620.record.pickle'
    SAMPLE_DIR = "samples/"
    for scenario in os.listdir(SAMPLE_DIR):
        scenario = "Law44_2"
        for filename in os.listdir(f"{SAMPLE_DIR}{scenario}"):
            if not filename.endswith("pickle"):
                continue
            path = f"{SAMPLE_DIR}{scenario}/{filename}"
            with open(path, 'rb') as f:
                print(path)
                msg = pickle.load(f)
                trace = msg["trace"]
                monitor = Monitor(msg, specification, weather)
                print(monitor.continuous_monitor_for_muti_traffic_rules())
                continue
        
                time_seq = sorted(list(trace.keys()))
                if len(trace.keys()) == 0:
                    exit(0)
                initial_timestamp = time_seq[0]
                trajectory = []
                for key in trace:
                    trajectory.append(raw_to_lawbreaker_API(trace[key], initial_timestamp))

                log = {"trajectory": trajectory}
                with open(f"{path}.json", 'w') as w:
                    w.write(json.dumps(log))
        break