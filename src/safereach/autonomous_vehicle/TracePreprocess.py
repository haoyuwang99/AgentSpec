import copy
import json
import pickle
import numpy as np
import math
from numpy import linalg as LA
from shapely.geometry import Polygon

ARROW_DIRECTIONS = ['forward', 'left', 'right', 'forwardOrLeft', 'forwardOrRight', 'Uturn']
_color = {
    'UNKNOWN' : 0,
    'RED' : 1,
    'YELLOW' : 2,
    'GREEN' : 3,
    'BLACK' : 4
}

def append_boolean_value(original_data, position_to_append):
    if original_data:
        position_to_append.append(1)
    else:
        position_to_append.append(0)

def convert_velocity_to_speed(velocity):
    x = velocity["x"]
    y = velocity["y"]
    z = velocity["z"]
    return math.sqrt(x*x+y*y+z*z)

def point2norm(point1, point2):
    if point1 is None or point2 is None:
        return float('inf')
    a = np.array([point1['x'], point1['y'], point1['z']])
    b = np.array([point2['x'], point2['y'], point2['z']])
    return LA.norm(a - b)


def polygon_point(polygonPointList):  # [[x,y,z], [x, y,z] ]
    polygon = []
    for i in range(len(polygonPointList)):
        point = [polygonPointList[i]['x'], polygonPointList[i]['y']]
        polygon.append(point)
    return polygon


def position_rotate(position_in_vehicle, rotation_theta):
    '''

    Args:
        position_in_vehicle: the position in the vehicle frame

    Returns: The position in the ENU frame.

    '''
    new_position = copy.deepcopy(position_in_vehicle)
    x = new_position[0]
    y = new_position[1]
    x1 = x * math.cos(rotation_theta) - y * math.sin(rotation_theta)
    y1 = x * math.sin(rotation_theta) + y * math.cos(rotation_theta)
    new_position[0] = x1
    new_position[1] = y1
    return new_position


def get_ego_polygon(ego_state):
    gps_offset = -1.348649
    ego_position = list(ego_state['pose']['position'].values())
    ego_length = ego_state['size']['length']
    ego_width = ego_state['size']['width']
    theta = ego_state['pose']['heading']
    front_left = [ego_length/2 - gps_offset, ego_width/2.0]
    front_right = [ego_length/2.0 - gps_offset, -ego_width/2.0]
    back_left = [-ego_length/2.0 - gps_offset, ego_width/2.0]
    back_right = [-ego_length/2.0 - gps_offset, -ego_width/2.0]
    poly1 = [position_rotate(front_left, theta)[0] + ego_position[0], position_rotate(front_left,theta)[1] + ego_position[1]]
    poly2 = [position_rotate(front_right, theta)[0] + ego_position[0], position_rotate(front_right,theta)[1] + ego_position[1]]
    poly3 = [position_rotate(back_right, theta)[0] + ego_position[0], position_rotate(back_right,theta)[1] + ego_position[1]]
    poly4 = [position_rotate(back_left, theta)[0] + ego_position[0], position_rotate(back_left, theta)[1] + ego_position[1]]
    ego_polygon = [poly1, poly2, poly3, poly4]
    return ego_polygon




class Trace: 
    
    def __init__(self, origin_trace):
        # origin_trac = execution trace
        self.init_trace = copy.deepcopy(origin_trace['trace'])
        self.is_groundtruth = origin_trace['groundTruthPerception']
        self.time = []
        self.trace = {}
        self.trace['time'] = [] 

        #self.trace["ego-forTrafficRule"] = {'highBeamOn':[], 'lowBeamOn':[], 'turnSignal':[], 'fogLightOn':[], 'hornOn':[], 'warningflashOn':[], 'gear':[], 'engineOn':[], 'direction':[], 'manualIntervention':[]}
        self.trace["ego-forTrafficRule"] = {'gear':[], 'engineOn':[], 'direction':[], 'manualIntervention':[]}
        self.trace["ego-driving-forTrafficRule"] = {'speed':[], 'acc':[], 'brake':[], 'isLaneChanging':[], 'isOverTaking':[], 'isTurningAround':[]}
        self.trace["currentlane-forTrafficRule"] = {'number':[], 'direction':[]}
        self.trace["speedLimit-forTrafficRule"] = {'lowerLimit':[], 'upperLimit':[]}
        self.trace["road-forTrafficRule"] = {'honkingAllowed':[], 'crosswalkAhead':[], 'junctionAhead':[], 'stopSignAhead':[], 'signalAhead':[], 'stoplineAhead':[], 'streetLightOn':[]}
        self.trace["specialLocationAhead-forTrafficRule"] = {'location':[], 'type':[]}
        self.trace["trafficLightAhead-forTrafficRule"] = {'color':[], 'blink':[]}
        self.trace["trafficLightAhead-arrow-forTrafficRule"] = dict()  #not supported yet
        self.trace["traffic-forTrafficRule"] = {'PriorityNPCAhead':[], 'PriorityPedsAhead':[],'isTrafficJam':[]}
        self.trace["NPCAhead-forTrafficRule"] = {'Ahead':[], 'speed':[]}
        self.trace["NearestNPC-forTrafficRule"] = {'Ahead':[], 'speed':[]}
        self.trace["NPCOpposite-forTrafficRule"] = {'Ahead':[], 'speed':[]}
        # self.trace["time-forTrafficRule"] = []
        self.trace["trafficLightAhead-arrow-direction-forTrafficRule"] = { 'color': [], 'blink': []} 
        self.arrow_directions = ['forward', 'left', 'right', 'forwardOrLeft', 'forwardOrRight', 'Uturn']
        for _item in self.arrow_directions:
            self.trace["trafficLightAhead-arrow-forTrafficRule"][_item] = { 'color': [], 'blink': []}        
        self.extract()

    def BUILD_single_traffic_rule_API(self, trace_state):
        ego = trace_state['ego']
        truth = trace_state['truth']
        ego_chasis = ego['Chassis']
        ego_currentLane = ego['currentLane']
        traffic_light = trace_state['traffic_lights']

 
        self.trace['ego-forTrafficRule']['gear'].append(ego_chasis['gearLocation'])
        append_boolean_value(ego_chasis['engineStarted'], self.trace['ego-forTrafficRule']['engineOn'])
        self.trace['ego-forTrafficRule']['direction'].append(ego['planning_of_turn'])
        if ego_chasis['drivingMode'] != "COMPLETE_AUTO_DRIVE":
            self.trace['ego-forTrafficRule']['manualIntervention'].append(1)
        else:
            self.trace['ego-forTrafficRule']['manualIntervention'].append(0)
       
        speed_of_ego = 3.6*ego_chasis['speedMps']
        acc_of_ego = convert_velocity_to_speed(ego['pose']['linearAcceleration'])
        self.trace["ego-driving-forTrafficRule"]['speed'].append(speed_of_ego)
        self.trace["ego-driving-forTrafficRule"]['acc'].append(acc_of_ego)
        self.trace["ego-driving-forTrafficRule"]['brake'].append(ego_chasis['brakePercentage'])
        append_boolean_value(ego['isLaneChanging'], self.trace["ego-driving-forTrafficRule"]['isLaneChanging'])
        append_boolean_value(ego['isOverTaking'], self.trace["ego-driving-forTrafficRule"]['isOverTaking'])
        append_boolean_value(ego['isTurningAround'], self.trace["ego-driving-forTrafficRule"]['isTurningAround'])

        self.trace["currentlane-forTrafficRule"]['number'].append(ego_currentLane['number'])
        if 'turn' in ego_currentLane: #hasattr(ego_currentLane, 'turn'):
            self.trace["currentlane-forTrafficRule"]['direction'].append(ego_currentLane['turn'])
        else:
            self.trace["currentlane-forTrafficRule"]['direction'].append(0)

        max_speed = 1000
        min_speed = 0
        self.trace["speedLimit-forTrafficRule"]['lowerLimit'].append(min_speed)
        self.trace["speedLimit-forTrafficRule"]['upperLimit'].append(max_speed)
        self.trace["road-forTrafficRule"]['honkingAllowed'].append(1) #not support for apollo at now stage
        self.trace["road-forTrafficRule"]['crosswalkAhead'].append(ego['crosswalkAhead'])
        self.trace["road-forTrafficRule"]['junctionAhead'].append(ego['junctionAhead'])
        self.trace["road-forTrafficRule"]['stopSignAhead'].append(ego['stopSignAhead'])
        if traffic_light == {}:
            self.trace["road-forTrafficRule"]['signalAhead'].append(0)
        else:
           append_boolean_value(True, self.trace["road-forTrafficRule"]['signalAhead'])
        self.trace["road-forTrafficRule"]['stoplineAhead'].append(ego['stoplineAhead'])
        self.trace["road-forTrafficRule"]['streetLightOn'].append(0)
        
        # self.trace["specialLocationAhead-forTrafficRule"] = {'location':[], 'type':[]}
        self.trace["specialLocationAhead-forTrafficRule"]['location'].append(0)
        self.trace["specialLocationAhead-forTrafficRule"]['type'].append(0)

        if traffic_light == {}:
            self.trace["trafficLightAhead-forTrafficRule"]['color'].append(3)
            self.trace["trafficLightAhead-forTrafficRule"]['blink'].append(0)
        else:
            _list = traffic_light['trafficLightList']
            if len(_list) == 1:
                current_signal = _list[0]
                self.trace["trafficLightAhead-forTrafficRule"]['color'].append(current_signal['color'])
                append_boolean_value(current_signal['blink'], self.trace["trafficLightAhead-forTrafficRule"]['blink'])
            else:
                # print('warning: more than one traffic light, choose the closer one')
                current_signal = _list[traffic_light['nearst']]
                self.trace["trafficLightAhead-forTrafficRule"]['color'].append(_color[current_signal['color']])
                append_boolean_value(False, self.trace["trafficLightAhead-forTrafficRule"]['blink'])


        self.trace["trafficLightAhead-arrow-direction-forTrafficRule"]['color'].append(3)
        self.trace["trafficLightAhead-arrow-direction-forTrafficRule"]['blink'].append(0)

        for _item in self.arrow_directions:
            self.trace["trafficLightAhead-arrow-forTrafficRule"][_item]['color'].append(3)
            self.trace["trafficLightAhead-arrow-forTrafficRule"][_item]['blink'].append(0)
        append_boolean_value(ego['PriorityNPCAhead'], self.trace["traffic-forTrafficRule"]['PriorityNPCAhead'])
        append_boolean_value(ego['PriorityPedsAhead'], self.trace["traffic-forTrafficRule"]['PriorityPedsAhead'])    
        append_boolean_value(ego['isTrafficJam'], self.trace["traffic-forTrafficRule"]['isTrafficJam'])

        max_dis = 1000
        min_dis = 0
        name_of_NPCAhead = truth['NPCAhead']
        name_of_NearestNPC = truth['NearestNPC']
        name_of_NPCOpposite = truth['NPCOpposite']
        for _i in truth['obsList']:
            if _i['id'] == name_of_NPCAhead:
                dist_to_NPCAhead = _i['distToEgo']
                speed_to_NPCAhead = _i['speed']
            if _i['id'] == name_of_NearestNPC:
                dist_to_NearestNPC = _i['distToEgo']
                speed_to_NearestNPC = _i['speed']
            if _i['id'] == name_of_NPCOpposite:
                dist_to_NPCOpposite = _i['distToEgo']
                speed_to_NPCOpposite = _i['speed']
        if name_of_NPCAhead != None:
            self.trace["NPCAhead-forTrafficRule"]['Ahead'].append(dist_to_NPCAhead)
            self.trace["NPCAhead-forTrafficRule"]['speed'].append(speed_to_NPCAhead)
        else:
            self.trace["NPCAhead-forTrafficRule"]['Ahead'].append(max_dis)
            self.trace["NPCAhead-forTrafficRule"]['speed'].append(min_speed)

        if name_of_NearestNPC != None:
            self.trace["NearestNPC-forTrafficRule"]['Ahead'].append(dist_to_NearestNPC)
            self.trace["NearestNPC-forTrafficRule"]['speed'].append(speed_to_NearestNPC)
        else:
            self.trace["NearestNPC-forTrafficRule"]['Ahead'].append(max_dis)
            self.trace["NearestNPC-forTrafficRule"]['speed'].append(min_speed)

        if name_of_NPCOpposite != None:
            self.trace["NPCOpposite-forTrafficRule"]['Ahead'].append(dist_to_NPCOpposite)
            self.trace["NPCOpposite-forTrafficRule"]['speed'].append(speed_to_NPCOpposite)
        else:
            self.trace["NPCOpposite-forTrafficRule"]['Ahead'].append(max_dis)
            self.trace["NPCOpposite-forTrafficRule"]['speed'].append(min_speed)


    def extract(self):
        time = sorted(self.init_trace.keys())
        initial_time = time[0]
        # initial_time = self.init_trace[0]['timestamp']
        for key, i in enumerate(time):
            trace_state = self.init_trace[i]
            _state_time = (i - initial_time) / 1000000000
            self.trace['time'].append(_state_time)
            self.time.append(_state_time)
            self.BUILD_single_traffic_rule_API(trace_state)


def raw_to_lawbreaker_API(trace_step, initial_timestamp):
    lawbreaker_step = {
        "time": (trace_step["timestamp"] - initial_timestamp)/1000000000,
    }
    
    ego = trace_step['ego']

    truth = trace_step['truth']
    ego_chasis = ego['Chassis']
    ego_currentLane = ego['currentLane']
    traffic_light = trace_step['traffic_lights']
    
    

    lawbreaker_step['gear'] = ego_chasis['gearLocation']
    lawbreaker_step['engineOn'] = 1 if ego_chasis['engineStarted'] else 0
    lawbreaker_step['direction'] = ego['planning_of_turn']
    lawbreaker_step['manualIntervention'] = 1  if ego_chasis['drivingMode'] != "COMPLETE_AUTO_DRIVE" else 0
    
    speed_of_ego = 3.6 * ego_chasis['speedMps']
    acc_of_ego = convert_velocity_to_speed(ego['pose']['linearAcceleration'])
    
    lawbreaker_step['speed'] = speed_of_ego
    lawbreaker_step['acc'] = acc_of_ego
    lawbreaker_step['brake'] = ego_chasis['brakePercentage']
    lawbreaker_step['isLaneChanging'] = 1 if ego['isLaneChanging'] else 0
    lawbreaker_step['isOverTaking'] = 1 if ego['isOverTaking'] else 0
    lawbreaker_step['isTurningAround'] = 1 if ego['isTurningAround'] else 0

    lawbreaker_step['currentLanenumber'] = ego_currentLane['number']
    if 'turn' in ego_currentLane: #hasattr(ego_currentLane, 'turn'):
        lawbreaker_step['currentLanedirection'] = ego_currentLane['turn']
    else:
        lawbreaker_step['currentLanedirection'] = 0

    max_speed = 1000
    min_speed = 0
    lawbreaker_step['speedLimitlowerLimit'] = min_speed
    lawbreaker_step['speedLimitupperLimit'] = max_speed 
    lawbreaker_step['honkingAllowed'] = 1 #not support for apollo at now stage
    lawbreaker_step['crosswalkAhead'] = ego['crosswalkAhead']
    lawbreaker_step['junctionAhead'] = ego['junctionAhead']
    lawbreaker_step['stopSignAhead'] = ego['stopSignAhead']
    if traffic_light == {}:
        lawbreaker_step['signalAhead'] = 0
    else:
        lawbreaker_step['signalAhead'] = 1
    lawbreaker_step['stoplineAhead'] = ego['stoplineAhead']
    lawbreaker_step['streetLightOn'] = 0
    
    # self.trace["specialLocationAhead-forTrafficRule"] = {'location':[], 'type':[]}
    lawbreaker_step['specialLocationAheadlocation'] = 0
    lawbreaker_step['specialLocationAheadtype'] = 0

    if traffic_light == {}:
        lawbreaker_step['trafficLightAheadcolor'] = 3
        lawbreaker_step['trafficLightAheadblink'] = 0
    else:
        _list = traffic_light['trafficLightList']
        if len(_list) == 1:
            current_signal = _list[0]
            lawbreaker_step['trafficLightAheadcolor'] = current_signal['color']
            lawbreaker_step['trafficLightAheadblink'] = 1 if current_signal['blink'] else 0
        else:
            # print('warning: more than one traffic light, choose the closest one')
            current_signal = _list[traffic_light['nearst']]
            lawbreaker_step['trafficLightAheadcolor'] = _color[current_signal['color']]
            lawbreaker_step['trafficLightAheadblink'] = 0


    # lawbreaker_step["trafficLightAhead-arrow-direction-forTrafficRule"]['trafficLightAheadArrowDirectioncolor'] = 3
    # lawbreaker_step["trafficLightAhead-arrow-direction-forTrafficRule"]['trafficLightAheadArrowDirectionblink'] = 0

    # for _item in ARROW_DIRECTIONS:
    #     lawbreaker_step[_item] = {}
    #     lawbreaker_step["trafficLightAhead-arrow-forTrafficRule"][_item]['trafficLightAheadArrowDirectioncolor'] = 3
    #     lawbreaker_step["trafficLightAhead-arrow-forTrafficRule"][_item]['trafficLightAheadArrowDirectionblink'] = 0
        
    lawbreaker_step['PriorityNPCAhead'] = 1 if ego['PriorityNPCAhead'] else 0
    lawbreaker_step['PriorityPedsAhead'] = 1 if ego['PriorityPedsAhead'] else 0
    lawbreaker_step['isTrafficJam'] = 1 if ego['isTrafficJam'] else 0
    lawbreaker_step['reach_destination'] = 1 if ego["reach_destinaton"] else 0
    lawbreaker_step['collision'] = 1 if truth["minDistToEgo"] <= 0 else 0

    max_dis = 1000
    min_dis = 0
    name_of_NPCAhead = truth['NPCAhead']
    name_of_NearestNPC = truth['NearestNPC']
    name_of_NPCOpposite = truth['NPCOpposite']
    for _i in truth['obsList']:
        if _i['id'] == name_of_NPCAhead:
            dist_to_NPCAhead = _i['distToEgo']
            speed_to_NPCAhead = _i['speed']
        if _i['id'] == name_of_NearestNPC:
            dist_to_NearestNPC = _i['distToEgo']
            speed_to_NearestNPC = _i['speed']
        if _i['id'] == name_of_NPCOpposite:
            dist_to_NPCOpposite = _i['distToEgo']
            speed_to_NPCOpposite = _i['speed']
    if name_of_NPCAhead != None:
        lawbreaker_step['NPCAheadAhead'] = dist_to_NPCAhead
        lawbreaker_step['NPCAheadspeed'] = speed_to_NPCAhead
    else:
        lawbreaker_step['NPCAheadAhead'] = max_dis
        lawbreaker_step['NPCAheadspeed'] = min_speed

    if name_of_NearestNPC != None:
        lawbreaker_step['NearestNPCAhead'] = dist_to_NearestNPC
        lawbreaker_step['NearestNPCspeed'] = speed_to_NearestNPC
    else:
        lawbreaker_step['NearestNPCAhead'] = max_dis
        lawbreaker_step['NearestNPCspeed'] = min_speed

    if name_of_NPCOpposite != None:
        lawbreaker_step['NPCOppositeAhead'] = dist_to_NPCOpposite
        lawbreaker_step['NPCOppositespeed'] = speed_to_NPCOpposite
    else:
        lawbreaker_step['NPCOppositeAhead'] = max_dis
        lawbreaker_step['NPCOppositespeed'] = min_speed
    
    return lawbreaker_step

# Helper: convert a Polygon to list-of-tuples
def polygon_to_list(obj):
    if isinstance(obj, Polygon):
        return list(obj.exterior.coords)
    return obj

# Recursive helper to traverse and convert all polygons in a structure
def convert_polygons(obj):
    if isinstance(obj, dict):
        return {k: convert_polygons(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_polygons(v) for v in obj]
    elif isinstance(obj, Polygon):
        return polygon_to_list(obj)
    else:
        return obj 