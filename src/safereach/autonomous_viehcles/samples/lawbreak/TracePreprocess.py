import copy
import json
import numpy as np
import math
from numpy import linalg as LA
from shapely.geometry import Polygon

_color = {
    'UNKNOWN' : 0,
    'RED' : 1,
    'YELLOW' : 2,
    'GREEN' : 3,
    'BLACK' : 4
}


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
    '''
    Main attributes in Trace class:
    1. list of npc, pedestrian and static obstacle
    agent: ['npc1', 'npc2', 'pedestrian1', 'pedestrian2',...]
    2. distance dict
    distance:
        'perception':
            'npc1': [10.3, 10.2, 10.1, ...]
            'npc2': [10.3, 10.2, 10.1, ...]
        'truth':
            'npc1': [10.3, 10.2, 10.1, ...]
            'npc2': [10.3, 10.2, 10.1, ...]
    3. trace dict
    trace:
        'time': [0, 0.1, 0.2, 0.3,...]
        'ego':
        [(array(x,y,z), array(qx,qy,qz,qw), array(vx,vy,vz), array(ax, ay,az))]
        'perception':
            'npc1': [(array(x,y,z), array(vx,vy,vz), theta, [[x,y,z], [x,y,z])] position, velocity, heading, polygon
            'pedestrian1': [(array(x,y,z), array(vx,vy,vz)), (array(x,y,z), array(vx,vy,vz)), (array(x,y,z), array(vx,vy,vz))]
        'truth':
            'npc1': [(array(x,y,z), array(vx,vy,vz)), (array(x,y,z), array(vx,vy,vz)), (array(x,y,z), array(vx,vy,vz))]
            'pedestrian1': [(array(x,y,z), array(vx,vy,vz)), (array(x,y,z), array(vx,vy,vz)), (array(x,y,z), array(vx,vy,vz))]
    '''

    def __init__(self, origin_trace):
        # origin_trac = execution trace
        self.init_trace = copy.deepcopy(origin_trace['trace'])
        self.is_groundtruth = origin_trace['groundTruthPerception']
        self.time = []
        self.trace = {}
        self.distance = {}
        self.perception_diff = {}
        self.agent = origin_trace['AgentNames']
        self.trace['time'] = []
        self.trace['ego'] = {'position': [], 'velocity': [], 'heading': [], 'acceleration': [], 'shape': []}
        self.trace['perception'] = dict()
        self.trace['truth'] = dict()
        for _item in self.agent:
            self.perception_diff[_item] = {'type': [0.0]*len(self.init_trace),
                                           'position': [0.0]*len(self.init_trace),
                                           'velocity': [0.0]*len(self.init_trace),
                                           'heading': [0.0]*len(self.init_trace),
                                           'shape': [0.0]*len(self.init_trace)}
            self.trace['perception'][_item] = {'position': [], 'velocity': [], 'heading': [], 'acceleration': [], 'shape': []}
            self.trace['truth'][_item] = {'position': [], 'velocity': [], 'heading': [], 'acceleration': [], 'shape': []}
        _distance = {}
        perception_dis = {}
        truth_dist = {}
        for _item in self.agent:
            perception_dis[_item] = []
            truth_dist[_item] = []
        self.distance['perception'] = perception_dis
        self.distance['truth'] = truth_dist

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


    def convert_velocity_to_speed(self, velocity):
        x = velocity["x"]
        y = velocity["y"]
        z = velocity["z"]
        return math.sqrt(x*x+y*y+z*z)

    def append_boolean_value(self, original_data, position_to_append):
        if original_data:
            position_to_append.append(1)
        else:
            position_to_append.append(0)


    def BUILD_single_traffic_rule_API(self, trace_state):
        ego = trace_state['ego']
        truth = trace_state['truth']
        ego_chasis = ego['Chassis']
        ego_currentLane = ego['currentLane']
        traffic_light = trace_state['traffic_lights']


        # self.append_boolean_value(ego_chasis['highBeamOn'], self.trace['ego-forTrafficRule']['highBeamOn'])
        # self.append_boolean_value(ego_chasis['lowBeamOn'], self.trace['ego-forTrafficRule']['lowBeamOn'])
        # self.append_boolean_value(ego_chasis['turnSignal'], self.trace['ego-forTrafficRule']['turnSignal'])
        # self.trace['ego-forTrafficRule']['fogLightOn'].append(0) #not support for apollo at now stage
        # self.append_boolean_value(ego_chasis['hornOn'], self.trace['ego-forTrafficRule']['hornOn'])
        # self.trace['ego-forTrafficRule']['warningflashOn'].append(0) #not support for apollo at now stage
        self.trace['ego-forTrafficRule']['gear'].append(ego_chasis['gearLocation'])
        self.append_boolean_value(ego_chasis['engineStarted'], self.trace['ego-forTrafficRule']['engineOn'])
        self.trace['ego-forTrafficRule']['direction'].append(ego['planning_of_turn'])
        if ego_chasis['drivingMode'] != "COMPLETE_AUTO_DRIVE":
            self.trace['ego-forTrafficRule']['manualIntervention'].append(1)
        else:
            self.trace['ego-forTrafficRule']['manualIntervention'].append(0)
       
        speed_of_ego = 3.6*ego_chasis['speedMps']
        acc_of_ego = self.convert_velocity_to_speed(ego['pose']['linearAcceleration'])
        self.trace["ego-driving-forTrafficRule"]['speed'].append(speed_of_ego)
        self.trace["ego-driving-forTrafficRule"]['acc'].append(acc_of_ego)
        self.trace["ego-driving-forTrafficRule"]['brake'].append(ego_chasis['brakePercentage'])
        self.append_boolean_value(ego['isLaneChanging'], self.trace["ego-driving-forTrafficRule"]['isLaneChanging'])
        self.append_boolean_value(ego['isOverTaking'], self.trace["ego-driving-forTrafficRule"]['isOverTaking'])
        self.append_boolean_value(ego['isTurningAround'], self.trace["ego-driving-forTrafficRule"]['isTurningAround'])

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
            self.append_boolean_value(True, self.trace["road-forTrafficRule"]['signalAhead'])
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
                self.append_boolean_value(current_signal['blink'], self.trace["trafficLightAhead-forTrafficRule"]['blink'])
            else:
                # print('warning: more than one traffic light, choose the closer one')
                current_signal = _list[traffic_light['nearst']]
                self.trace["trafficLightAhead-forTrafficRule"]['color'].append(_color[current_signal['color']])
                self.append_boolean_value(False, self.trace["trafficLightAhead-forTrafficRule"]['blink'])


        self.trace["trafficLightAhead-arrow-direction-forTrafficRule"]['color'].append(3)
        self.trace["trafficLightAhead-arrow-direction-forTrafficRule"]['blink'].append(0)

        for _item in self.arrow_directions:
            self.trace["trafficLightAhead-arrow-forTrafficRule"][_item]['color'].append(3)
            self.trace["trafficLightAhead-arrow-forTrafficRule"][_item]['blink'].append(0)
        self.append_boolean_value(ego['PriorityNPCAhead'], self.trace["traffic-forTrafficRule"]['PriorityNPCAhead'])
        self.append_boolean_value(ego['PriorityPedsAhead'], self.trace["traffic-forTrafficRule"]['PriorityPedsAhead'])    
        self.append_boolean_value(ego['isTrafficJam'], self.trace["traffic-forTrafficRule"]['isTrafficJam'])

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


    def extract(self, sensing_range=100.0):
        inf_dis = 1000.0
        _trace_len = len(self.init_trace)
        time = sorted(self.init_trace.keys())
        initial_time = time[0]
        # initial_time = self.init_trace[0]['timestamp']
        for key, i in enumerate(time):
            trace_state = self.init_trace[i]
            _state_time = (i - initial_time) / 1000000000
            self.trace['time'].append(_state_time)
            self.time.append(_state_time)
            self.BUILD_single_traffic_rule_API(trace_state)
            ego_state = trace_state['ego']['pose']
            ego_state_position = np.array(list(ego_state['position'].values()))
            ego_state_heading = ego_state['heading']
            ego_state_velocity = np.array(list(ego_state['linearVelocity'].values()))
            ego_state_acceleration = np.array(list(ego_state['linearAcceleration'].values()))
            ego_state_polygon = get_ego_polygon(trace_state['ego'])
            self.trace['ego']['position'].append(ego_state_position)
            self.trace['ego']['velocity'].append(ego_state_velocity)
            self.trace['ego']['heading'].append(ego_state_heading)
            self.trace['ego']['acceleration'].append(ego_state_acceleration)
            self.trace['ego']['shape'].append(ego_state_polygon)

            truth_state = trace_state['truth']['obsList']
            truth_remaining_agent = self.agent.copy()
            for k in range(len(truth_state)):
                obs_k = truth_state[k]
                if obs_k['id'] in self.agent:
                    truth_remaining_agent.remove(obs_k['id'])
                    obs_position = np.array(list(obs_k['position'].values()))  # vector
                    obs_velocity = np.array(list(obs_k['velocity'].values())) # vector
                    obs_heading = obs_k['theta']  # float
                    # obs_acceleration = np.array(list(obs_k['acceleration'].values()))
                    obs_polygon = polygon_point(obs_k['polygonPoint'])
                    dis2ego = obs_k['distToEgo']
                    self.trace['truth'][obs_k['id']]['position'].append(obs_position)
                    self.trace['truth'][obs_k['id']]['velocity'].append(obs_velocity)
                    self.trace['truth'][obs_k['id']]['heading'].append(obs_heading)
                    # self.trace['truth'][obs_k['name']]['acceleration'].append(obs_acceleration)
                    self.trace['truth'][obs_k['id']]['shape'].append(obs_polygon)
                    self.distance['truth'][obs_k['id']].append(dis2ego)
            if len(truth_remaining_agent):
                for item in truth_remaining_agent:
                    self.trace['truth'][item]['position'].append(np.array([0, 0, 0]))
                    self.trace['truth'][item]['velocity'].append(np.array([0, 0, 0]))
                    self.trace['truth'][item]['heading'].append(0)
                    self.trace['truth'][item]['acceleration'].append(np.array([0, 0, 0]))
                    self.trace['truth'][item]['shape'].append([])
                    self.distance['truth'][item].append(inf_dis)

            # extract perception state
            if not self.is_groundtruth:
                perception_state = trace_state['perception']['obsList']
                remaining_agent = self.agent.copy()
                for j in range(len(perception_state)):
                    obs_j = perception_state[j]
                    if obs_j['matchedGT'] in self.agent:
                        remaining_agent.remove(obs_j['matchedGT'])
                        obs_position_p = np.array(list(obs_j['position'].values()))
                        obs_velocity_p = np.array(list(obs_j['velocity'].values()))
                        obs_heading_p = obs_j['theta']
                        obs_acceleration_p = np.array(list(obs_j['acceleration'].values()))
                        obs_polygon_p = polygon_point(obs_j['polygonPointList'])
                        dis2ego_p = obs_j['distToEgo']
                        self.trace['perception'][obs_j['matchedGT']]['position'].append(obs_position_p)
                        self.trace['perception'][obs_j['matchedGT']]['velocity'].append(obs_velocity_p)
                        self.trace['perception'][obs_j['matchedGT']]['heading'].append(obs_heading_p)
                        self.trace['perception'][obs_j['matchedGT']]['acceleration'].append(obs_acceleration_p)
                        self.trace['perception'][obs_j['matchedGT']]['shape'].append(obs_polygon_p)

                        # self.trace['perception'][obs_j['matchedGT']].append({'position': obs_position_p,
                        #                                                      'velocity': obs_velocity_p,
                        #                                                      'heading': obs_heading_p,
                        #                                                      'acceleration': obs_acceleration_p,
                        #                                                      'shape': obs_polygon_p})
                        self.distance['perception'][obs_j['matchedGT']].append(dis2ego_p)
                # For other objects not in perception results
                if len(remaining_agent):
                    for item in remaining_agent:
                        if self.distance['truth'][item][i] <= sensing_range:
                            self.trace['perception'][item]['position'].append(None)
                            self.trace['perception'][item]['velocity'].append(None)
                            self.trace['perception'][item]['heading'].append(None)
                            self.trace['perception'][item]['acceleration'].append(None)
                            self.trace['perception'][item]['shape'].append([])
                            # self.trace['perception'][item].append((np.zeros(3), np.zeros(3), 0, [[0, 0, 0]]))
                            self.distance['perception'][item].append(self.distance['truth'][item][i])  # todo: determine a more suitable distance
                        else:
                            self.trace['perception'][item]['position'].append(np.array([inf_dis, inf_dis, inf_dis]))
                            self.trace['perception'][item]['velocity'].append(np.array([0, 0, 0]))
                            self.trace['perception'][item]['heading'].append(0)
                            self.trace['perception'][item]['acceleration'].append(np.array([0, 0, 0]))
                            self.trace['perception'][item]['shape'].append([])
                            self.distance['perception'][item].append(inf_dis)

                # compute perception difference for each agent
                for item in self.agent:
                    if self.distance['truth'][item][i] <= sensing_range:
                        jj = 0
                        perception_result = dict()
                        for jj in range(len(perception_state)): # for each detected obstacle obs_jj
                            obs_jj = perception_state[jj]
                            if obs_jj['matchedGT'] == item:
                                perception_result = obs_jj
                                break
                        if jj == len(perception_state): # the obstacle item is not detected in the sensing range
                            self.perception_diff[item]['type'][i] = 1.0
                            self.perception_diff[item]['position'][i] = inf_dis
                            self.perception_diff[item]['velocity'][i] = inf_dis
                            self.perception_diff[item]['heading'][i] = inf_dis
                            self.perception_diff[item]['shape'][i] = 0
                            continue
                        for k in range(len(truth_state)): # obtain the ground truth of item
                            obs_k = truth_state[k]
                            if obs_k['name'] == item:
                                truth_result = obs_k
                                break
                        # type check
                        if perception_result['typeName'] == truth_result['typeName']:
                            type_error = 0.0
                        else:
                            type_error = 1.0
                        # position check
                        position_error = point2norm(perception_result['position'], truth_result['position'])
                        velocity_error = point2norm(perception_result['velocity'], truth_result['velocity'])
                        heading_error = np.abs(perception_result['theta'] - truth_result['theta'])
                        polygon1 = Polygon(polygon_point(perception_result['polygonPointList']))
                        polygon2 = Polygon(polygon_point(truth_result['polygonPointList']))
                        shape_error = polygon1.intersection(polygon2).area / polygon2.area
                        self.perception_diff[item]['type'][i] = type_error
                        self.perception_diff[item]['position'][i] = position_error
                        self.perception_diff[item]['velocity'][i] = velocity_error
                        self.perception_diff[item]['heading'][i] = heading_error
                        self.perception_diff[item]['shape'][i] = shape_error
            else:
                for item in self.agent:
                    self.distance['perception'][item].append(self.distance['truth'][item][key])
                    # self.trace['perception'][item].append(self.trace['truth'][item][i])
                    self.trace['perception'][item]['position'].append(self.trace['truth'][item]['position'][key])
                    self.trace['perception'][item]['velocity'].append(self.trace['truth'][item]['velocity'][key])
                    self.trace['perception'][item]['heading'].append(self.trace['truth'][item]['heading'][key])
                    # self.trace['perception'][item]['acceleration'].append(self.trace['truth'][item]['acceleration'][key])
                    self.trace['perception'][item]['shape'].append(self.trace['truth'][item]['shape'][key])





if __name__ == "__main__":
    output_file = 'data/result01.json'
    with open(output_file) as f:
        data = json.load(f)  # read as a msg from apollo via websocket
        trace = Trace(data)

        # print(len(trace.trace['ego-forTrafficRule']['highBeamOn']))
        print(trace.trace['time'])
        print()
        print(trace.trace['ego-forTrafficRule'])
        print()
        print(trace.trace['ego-driving-forTrafficRule'])
        print()
        print(trace.trace['currentlane-forTrafficRule'])
        print()
        print(trace.trace['speedLimit-forTrafficRule'])
        print()
        print(trace.trace['road-forTrafficRule'])
        print()
        print(trace.trace['specialLocationAhead-forTrafficRule'])
        print()
        print(trace.trace['trafficLightAhead-forTrafficRule'])
        print()
        print(trace.trace['traffic-forTrafficRule'])
        print()
        print(trace.trace['NPCAhead-forTrafficRule'])
        print()
        print(trace.trace['NearestNPC-forTrafficRule'])
        print()
        # print(trace.trace['perception']['npc1'][34])
        # print(trace.trace['truth']['npc1'][34])
        # print(trace.distance['perception']['npc1'][34])
        # print(trace.distance['truth']['npc1'][34])
        # print(len(trace.trace['perception']['npc1']))




    # p1 = {'x': 1.0, 'y': 2.0, 'z': 3.0}
    # p2 = {'x': 2.0, 'y': 3.0, 'z': 4.0}
    # print(point2norm(p1, p2))

    # ego_state = { "size": {
    #       "length": 4.7,
    #       "width": 2.06
    #     },
    #     "pose": {
    #       "position": {
    #         "x": 552829.3482471938,
    #         "y": 4183198.3280027835,
    #         "z": 10.124656677246094
    #       },
    #       "orientation": {
    #         "qx": -5.909786864322086e-07,
    #         "qy": -4.6492385052943064e-08,
    #         "qz": 0.4581255614757538,
    #         "qw": 0.8888875842094421
    #       },
    #       "linearVelocity": {
    #         "x": 1.073107159754727e-05,
    #         "y": -8.155493560479954e-06,
    #         "z": -2.4668872356414795e-05
    #       },
    #       "linearAcceleration": {
    #         "x": -4.7755669017582286e-05,
    #         "y": -2.7896752591041223e-05,
    #         "z": 9.809666633611167
    #       },
    #       "angularVelocity": {
    #         "x": -3.4123785269863597e-06,
    #         "y": -4.314480573963567e-06,
    #         "z": 1.2359062541833489e-09
    #       },
    #       "heading": 2.522566710369909,
    #       "linearAccelerationVrf": {
    #         "x": -5.493117350852117e-05,
    #         "y": 1.198328027385287e-05,
    #         "z": 9.809666633605957
    #       },
    #       "angularVelocityVrf": {
    #         "x": -5.493908247444779e-06,
    #         "y": 2.7574944283514924e-07,
    #         "z": 1.2336869303908315e-09
    #       },
    #       "eulerAngles": {
    #         "x": -1.0080285838030164e-06,
    #         "y": -6.241378660286242e-07,
    #         "z": 0.9517705564328693
    #       },
    #       "lane_position": {
    #         "lane": "lane_231",
    #         "offset": 94.80424083205679
    #       }
    #     },
    #     "lane": "lane_231",
    #     "laneOffset": 94.80424083205679,
    #     "road": "road_230_231",
    #     "junction": None
    #   }

    # ego_polygon = get_ego_polygon(ego_state)
    # print(ego_polygon)

    # file_name = 'result-trace.json'
    # agent_name = ['npc1']
    # with open(file_name) as f:
    #     data = json.load(f)
    # # trace_data = data['trace']
    # trace = Trace(data)
    # print('distance sequence to the ego vehicle: {}'.format(trace.distance))
    # print('perception difference: {}'.format(trace.perception_diff))



    # print(len(trace.trace['truth']['npc1']))
    # print(trace.trace['ego'][34])
    # print(trace.trace['perception']['npc1'][34])
    # print(trace.trace['truth']['npc1'][34])
    # print(trace.distance['perception']['npc1'][34])
    # print(trace.distance['truth']['npc1'][34])
    # print(len(trace.trace['perception']['npc1']))
