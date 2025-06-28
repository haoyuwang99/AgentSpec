import json, copy, random, math, json, time, subprocess, os, websocket, logging, pickle
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from cyber_record.record import Record
from shapely.geometry import Polygon
from tqdm import tqdm
import concurrent.futures
import numpy as np

from map_for_bridge import get_map_info
from shapely.geometry import LineString, Point
from google.protobuf.json_format import MessageToDict

from EXtraction import ExtractAll
from AssertionExtraction import SingleAssertion
from GeneticAlgorithm import EncodedTestCase

_map = {
    'planning' : '/apollo/planning',
    'traffic_light': '/apollo/perception/traffic_light',
    'obstacles' : '/apollo/perception/obstacles',
    'pose' : '/apollo/localization/pose',
    'chassis' : '/apollo/canbus/chassis'
}

_turn = {
    'TURN_NONE' : 0,
    'TURN_LEFT' : 1,
    'TURN_RIGHT' : 2
}

_gear = {
    'GEAR_NEUTRAL' : 0,
    'GEAR_DRIVE' : 1,
    'GEAR_REVERSE' : 2,
    'GEAR_PARKING' : 3,
    'GEAR_LOW' : 4,
    'GEAR_INVALID' : 5,
    'GEAR_NONE' : 6
}


def find_time(time_list, target):
    filtered_array = np.array(list(time_list))[np.array(list(time_list)) < target]
    return None if len(filtered_array) == 0 else np.max(filtered_array)


class Mutation:
    def __init__(self, data, map_name, map_info, set_name) -> None:
        self.testFailures = []
        self.trace = {}
        self.is_groundtruth = True
        self.start_position = (data['scenario']['start']['x'], data['scenario']['start']['y'], 0)
        self.destination = [data['scenario']['end']['x'], data['scenario']['end']['y']]
        self.position_for_check = {}
        self.Check_The_vehicle_is_stuck_or_not = None
        self.result = {}
        self.name = ""
        self.agent = []
        self.weather = {'rain' : 0.0,  'snow': 0.0, 'fog' : 0.0}

        self.original_data_ = copy.deepcopy(data)
        self.map_name = map_name
        self.map_info = map_info
        self.testcase = []
        self.num = 0
        self.change_default = {
            "data":{
                "id":"",
                "info":{
                    "action":"CHANGE_MODE",
                    "value":"Default"
                },
                "source":"dreamview",
                "target":"dreamview",
                "sourceType":"module",
                "targetType":"dreamview",
                "requestId":"noResponse"
            },
            "type":"HMIAction",
            "action":"request"
        }
        self.change_module = {
            "action":"request",
            "data": {
                "info":{
                    "action":"CHANGE_OPERATION",
                    "value":"Scenario_Sim"
                },
                "id":"",
                "requestId":"HMIAction!",
                "source":"dreamview",
                "sourceType":"module",
                "target":"dreamview",
                "targetType":"dreamview"
            },
            "type":"HMIAction"
        }
        self.set_name = set_name
        self.scenario_name = []
        self.set_scenario = {
            "data":{
                "id":"",
                "info":{
                    "action":"CHANGE_SCENARIO",
                    "value":"65e0308b6f0ae871927b3bce,65e02fa86f0ae81e257b3bcd"
                },
                "source":"dreamview",
                "target":"dreamview",
                "sourceType":"module",
                "targetType":"dreamview",
                "requestId":"noResponse"
            },
            "type":"HMIAction",
            "action":"request"
        }
        self.set_ego = {
            "data":{
                "id":"",
                "info":{
                    "action":"CHANGE_VEHICLE",
                    "value":"Mkz Eample"
                },
                "source":"dreamview",
                "target":"dreamview",
                "sourceType":"module",
                "targetType":"dreamview",
                "requestId":"noResponse"
            },
            "type":"HMIAction",
            "action":"request"
        }
        self.reset_allmode = json.dumps(
            {
                "data":{
                    "id":"",
                    "info":{
                        "action":"RESET_MODE"
                    },
                    "source":"dreamview",
                    "target":"dreamview",
                    "sourceType":"module",
                    "targetType":"dreamview",
                    "requestId":"noResponse"
                },
                "type":"HMIAction",
                "action":"request"
            }
        )
        self.mode_list = ["Planning", "Control", "Prediction"]
        self.setup_mode = {
            "data":{
                "id":"",
                "info":{
                    "action":"START_MODULE",
                    "value":"Planning"
                },
                "source":"dreamview",
                "target":"dreamview",
                "sourceType":"module",
                "targetType":"dreamview",
                "requestId":"noResponse"
            },
            "type":"HMIAction",
            "action":"request"
        }
        self.reset_sce = {
            "data":{
                "id":"",
                "info":"",
                "source":"dreamview",
                "target":"dreamview",
                "sourceType":"module",
                "targetType":"dreamview",
                "requestId":"noResponse"
            },
            "type":"ResetScenarioSimulation",
            "action":"request"
        }
        self.start_sce = {
            "data":{
                "id":"",
                "info":{
                    "fromScenario":True
                },
                "source":"dreamview",
                "target":"dreamview",
                "sourceType":"module",
                "targetType":"dreamview",
                "requestId":"SendScenarioSimulationRequest!"
            },
            "type":"SendScenarioSimulationRequest",
            "action":"request"
        }
        self.start_record = {
            "data":{
                "id":"",
                "source":"dreamview",
                "target":"dreamview",
                "sourceType":"module",
                "targetType":"dreamview",
                "requestId":"noResponse"
            },
            "type":"StartDataRecorder",
            "action":"request"
        }
        # self.dr = webdriver.Firefox()
        # self.dr = webdriver.Chrome()
        # self.dr.get('http://localhost:8888')
        # self.dr.find_element(By.XPATH, "//div[@class='dreamview-tabs-tab']/div[contains(text(), 'PNC Mode')]").click()
        # self.dr.find_element(By.CSS_SELECTOR, "div#rc-tabs-0-panel-Pnc input.dreamview-check-box-input").click()
        # self.dr.find_element(By.XPATH, "//div[@id='rc-tabs-0-panel-Pnc']//button[contains(@class, 'css-8vdc0a-enter-this-mode-btn')]").click()
        # self.dr.refresh()
        # time.sleep(10)

    # generate one test case
    def testcase_random(self, idx = 0,dir_prefix = "sample/"):
        if not os.path.exists(dir_prefix):
            os.mkdir(dir_prefix) 
        testcase = copy.deepcopy(self.original_data_)
        self.ego_random(testcase)
        self.npc_random(testcase)
        self.traffic_light_random(testcase)
        self.testcase.append(testcase)
        self.scenario_name.append(testcase["id"])
        directory = f"{dir_prefix}case_{idx}/"
        # if os.path.exists(directory):
        #     os.rmdir(directory)
        os.mkdir(directory)
        with open(directory + "testcase.json", 'w') as f:
            f.write(json.dumps(testcase))

    def ego_random(self, testcase):
        ego_start = testcase['scenario']['start']
        delta_offset = random.gauss(0.0, 1.0)
        ego_start_angle = ego_start['heading']
        ego_start_angle_jd = ego_start_angle * 180 / math.pi
        delta_offset_angle = random.gauss(ego_start_angle_jd, 30)
        delta_offset_angle = float(np.clip(delta_offset_angle, ego_start_angle_jd - 45, ego_start_angle_jd + 45))
        ego_start['heading'] = delta_offset_angle * math.pi / 180
        new_x = delta_offset * math.cos(ego_start_angle) * delta_offset
        new_y = delta_offset * math.sin(ego_start_angle) * delta_offset
        ego_start['x'] += new_x
        ego_start['y'] += new_y

    def npc_random(self, testcase):
        if 'agent' not in testcase['scenario'].keys(): 
            return
        npc = testcase['scenario']['agent']
        _speed_max = 20
        _speed_min = 0.5
        for _npc in npc:
            start_Position = _npc['startPosition']
            speed = start_Position['speed']
            heading = start_Position['heading']
            delta_offset = random.gauss(0.0, 1.0)
            delta_speed = random.gauss(speed, 1.0)
            delta_speed = float(np.clip(delta_speed, _speed_min, _speed_max))
            start_Position['speed'] = delta_speed
            new_x = delta_offset * math.cos(heading) * delta_offset + start_Position['x']
            new_y = delta_offset * math.sin(heading) * delta_offset + start_Position['y']
            
            start_Position['x'] = new_x
            start_Position['y'] = new_y
            start_angle_jd = heading * 180 / math.pi
            delta_offset_angle = random.gauss(start_angle_jd, 30)
            delta_offset_angle = float(np.clip(delta_offset_angle, start_angle_jd - 30, start_angle_jd + 30))
            start_Position['heading'] = delta_offset_angle * math.pi / 180

            try:
                start_time = _npc['startTime']
                delta_time = random.gauss(start_time, 3.0)
                _npc['startTime'] = delta_time
            except:
                pass
            
            try:
                start_dis = _npc['startDistance']
                delta_dis = random.gauss(start_dis, 3.0)
                delta_dis = float(np.clip(delta_dis, 3, delta_dis+3))
                _npc['stratDistance'] = delta_dis
            except:
                pass

            wp = _npc['trackedPoint']
            for _wp in wp:
                _x = _wp['x']
                _y = _wp['y']
                _speed = _wp['speed']
                delta_speed = random.gauss(_speed, 1.0)
                delta_speed = float(np.clip(delta_speed, _speed_min, _speed_max))
                _wp['speed'] = delta_speed
                _x += float(np.clip(random.gauss(0.0, 1.0), -1, 1))
                _y += float(np.clip(random.gauss(0.0, 1.0), -1, 1))
                _wp['x'] = _x
                _wp['y'] = _y

    def weather_random(self):
        for _w in self.weather.keys():
            self.weather[_w] = random.random()

    def traffic_light_random(self, testcase):
        if 'trafficLights' not in testcase['scenario'].keys():
            return
        tl = testcase['scenario']['trafficLights']
        for _tl in tl:
            _tl['triggerValue'] = random.gauss(_tl['triggerValue'], 10.0)
            for _sg in _tl['stateGroup']:
                _sg['keepTime'] = random.gauss(_sg['keepTime'], 10.0)

    def prepare_dreamviewer_input(self):
        data = self.testcase[0] 
        with open('record/' + self.original_data_['id'] +'.json' , "w") as json_file:
            json.dump(data, json_file) 
        cmd = "docker cp " + self.original_data_['id']+'.json apollo_neo_dev_core:/home/sunsun/.apollo/resources/scenario_sets/65e0308b6f0ae871927b3bce/scenarios/'
        subprocess.run(cmd, shell=True, capture_output=True, text=True) 

    def run(self ):
        cmd = "docker exec apollo_neo_dev_core rm -rf /home/sunsun/.apollo/resources/records/*"
        subprocess.run(cmd, shell=True, capture_output=True, text=True)
        ws_url = "ws://localhost:8888/websocket"
        ws = websocket.create_connection(ws_url)
        ws.send(json.dumps(self.change_mode_fun("Default")))
        time.sleep(1)
        ws.send(json.dumps(self.change_mode_fun("Pnc")))
        time.sleep(1)
        ws.send(json.dumps(self.change_module_fun("Scenario_Sim")))
        time.sleep(1)
        for _name  in self.scenario_name:
             _name = self.set_name + "," + _name
             ws.send(json.dumps(self.set_scenario_fun(_name)))
             time.sleep(1)
        ws.send(json.dumps(self.set_ego_fun("Mkz Eample")))
        time.sleep(1)
        ws.send(self.reset_allmode)
        time.sleep(1)
        for _mode in self.mode_list:
            ws.send(json.dumps(self.setup_mode_fun(_mode)))
            time.sleep(1)
        ws.send(json.dumps(self.reset_sce))
        time.sleep(1)
        ws.send(json.dumps(self.start_sce))
        time.sleep(1)
        ws.send(json.dumps(self.reset_sce))
        time.sleep(1)
        ws.send(json.dumps(self.start_record))
        ws.send(json.dumps(self.start_sce))
        time.sleep(90)
        self.dr.find_element(By.CLASS_NAME, "css-ixukix-player-record-btn").click()
        name = self.dr.find_element(By.CLASS_NAME, "css-1hknsu3-record-modal-input")
        name.clear()
        name.send_keys('sample')

        self.dr.find_element(By.CLASS_NAME, "ant-btn-primary").click()

    def change_mode_fun(self, mode_name):
        msg = copy.deepcopy(self.change_default)
        msg["data"]["info"]["value"] = mode_name
        return msg

    def change_module_fun(self, module_name):
        msg = copy.deepcopy(self.change_module)
        msg["data"]["info"]["value"] = module_name
        return msg     

    def set_scenario_fun(self, name):
        msg = copy.deepcopy(self.set_scenario)
        msg["data"]["info"]["value"] = name
        return msg

    def set_ego_fun(self, name):
        msg = copy.deepcopy(self.set_ego)
        msg["data"]["info"]["value"] = name
        return msg

    def setup_mode_fun(self, name):
        msg = copy.deepcopy(self.setup_mode)
        msg["data"]["info"]["value"] = name
        return msg

    def save_message(self, file_name, item):
        if item not in self.record:
            self.record[item] = {}
        record = Record(file_name)
        time_list = sorted([t for topic, message, t in record.read_messages(_map[item])])
     
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.process_message, item, MessageToDict(message), t) for topic, message, t in record.read_messages(_map[item]) if t in time_list]

            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc=f"Processing {item}:"):
                result = future.result()
                if result is not None:
                    t, processed_message = result
                    if processed_message != {}:
                        self.record[item][t] = copy.deepcopy(processed_message)
        record.close()
        
    def process_message(self, item, message, t):
        if item == 'planning':
            return t, self.process_planning(message)
        elif item == 'traffic_light':
            return t, self.process_traffic_light(message, t)
        elif item == 'obstacles':
            return t, self.process_obstacles(message, t)
        elif item == 'chassis':
            return t, self.process_chassis(message)
        elif item == 'pose':
            message['size'] = { "length": 4.7, "width": 2.06 }
            self._process_pose(message)
            return t, message
        
    def process_chassis(self, chassis):
        truth = copy.deepcopy(chassis)
        truth["gearLocation"] = _gear[chassis['gearLocation']]
        return truth

    def process_planning(self, recoder):
        recoder = copy.deepcopy(recoder)
        decisions = recoder['decision']['objectDecision']
        planning_turn_signal = _turn[recoder['decision']['vehicleSignal']['turnSignal']]
        is_overtaking = False
        for item in decisions['decision']:
            item0 = item['objectDecision'][0]
            if 'overtake' in item0 and item0['overtake']['distanceS']!= 0:
                is_overtaking = True
            if 'nudge' in item0 and item0['nudge']['distanceL']!= 0:
                is_overtaking = True			
            if 'stop' in item0 and item0['stop']['distanceS']!= 0:
                pass
        recoder = {'is_overtaking' : is_overtaking, 'planning_turn_signal' : planning_turn_signal}
        return recoder

    def process_obstacles(self, obstacles, t):
        time_use = find_time(self.record['pose'].keys(), t)
        truth = {}
        if time_use != None:
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                executor.map(self._process_obstacles, obstacles['perceptionObstacle'], [time_use] * len(obstacles['perceptionObstacle']))
            if len(obstacles['perceptionObstacle']) > 0:
                nearestGtObs = obstacles['perceptionObstacle'][0]["id"]
                minDistToEgo = obstacles['perceptionObstacle'][0]["distToEgo"]
                NearestNPC = None
                for _ii in obstacles['perceptionObstacle']:
                    if _ii["id"] not in self.agent:
                        self.agent.append(_ii["id"])
                    if _ii["distToEgo"] <= minDistToEgo:
                        minDistToEgo = _ii["distToEgo"]
                        nearestGtObs = _ii["id"]
                        if _ii['type'] == 'VEHICLE':
                            NearestNPC = _ii["id"]
                truth["minDistToEgo"] = minDistToEgo
                truth["nearestGtObs"] = nearestGtObs
                truth["NearestNPC"] = NearestNPC
                truth["obsList"] =  obstacles['perceptionObstacle']
            else:
                truth["minDistToEgo"] = 200
                truth["nearestGtObs"] = None
                truth["NearestNPC"] = None
                truth["obsList"] =  obstacles['perceptionObstacle']
        else:
            pass
        return truth
    
    def _process_obstacles(self, msg, time_use):
        speed = self.convert_velocity_to_speed(msg['velocity'])
        msg['speed'] = speed
        msg["distToEgo"] = self.calculate_distToEgo(time_use, msg)
        points = []
        for _p in msg["polygonPoint"]:
            x = _p["x"]
            y = _p["y"]
            points.append((x,y))
        the_area = Polygon(points)
        result = self.map_info.find_which_area_the_ego_is_in(the_area)
        msg["currentLane"]= {}
        if result != None:
            if result[0].__contains__("lane_id"):
                lane_id = result[0]["lane_id"]
                msg["currentLane"]["currentLaneId"] = lane_id
                msg["currentLane"]['type'] = 'lane'
                msg['currentLane']['turn'] = result[0]["turn"]
            if result[0].__contains__("junction_id"):
                lane_id = result[0]["junction_id"]
                msg["currentLane"]["currentLaneId"] = lane_id
                msg["currentLane"]["type"] = 'junction'
        else:
            msg["currentLane"]["currentLaneId"] = None
            msg["currentLane"]["type"] = None
        msg["currentLane"]["area"] = the_area

    def process_traffic_light(self, msg, t):
        result = {}
        time_use = find_time(self.record['pose'].keys(), t)
        if time_use != None:
            result["trafficLightList"] = msg["trafficLight"]
            id_light = None
            distance_min = None
            for k in range(len(msg["trafficLight"])):
                item = msg["trafficLight"][k]
                distance = self.calculate_distance_to_traffic_light_stop_line(time_use, item['id'])
                if distance_min == None:
                    distance_min = distance
                    id_light = k
                elif distance < distance_min:
                    distance_min = distance
                    id_light = k
            result["nearst"] = id_light            
            result["trafficLightStopLine"] = distance_min
        else:
            pass
        return result

    def _process_pose(self, pose):
        original_point = []
        original_point.append(pose["pose"]["position"]["x"])
        original_point.append(pose["pose"]["position"]["y"])
        heading_of_ego = pose["pose"]["heading"]
        lengthen_of_ego = pose["size"]["length"]
        width_of_ego = pose["size"]["width"]
        ego_polygonPointList = []
        ego_polygonPointList = self.get_four_polygon_point_list_of_ego(original_point,heading_of_ego,lengthen_of_ego,width_of_ego)
        ego = Polygon(ego_polygonPointList)
        pose['area'] = ego

    def process_pose(self, pose_key, chassis_key):
        time_use = find_time(self.record['obstacles'].keys(), pose_key)
        if time_use != None:
            obs = copy.deepcopy(self.record['obstacles'][time_use])
            pose = self.record['pose'][pose_key]
            single_trace = {}
            single_trace["timestamp"] = pose_key
            pose['Chassis'] = copy.deepcopy(self.record['chassis'][chassis_key])
            original_point = []
            original_point.append(pose['pose']['position']['x'])
            original_point.append(pose['pose']['position']['y'])
            heading_of_ego = pose['pose']['heading']
            length_of_ego = pose["size"]["length"]
            width_of_ego = pose["size"]["width"]
            ego_position_area = pose['area']
            head_middle_point = self.get_the_head_middle_point_of_ego(original_point,heading_of_ego,length_of_ego,width_of_ego)
            back_middle_point = self.get_the_back_middle_point_of_ego(original_point,heading_of_ego,length_of_ego,width_of_ego)
            currentLane = self.check_current_lane(ego_position_area)
            pose["currentLane"] = currentLane
            ahead_area_polygon = self.calculate_area_of_ahead(head_middle_point, heading_of_ego, width_of_ego)
            back_area_polygon = self.calculate_area_of_ahead(back_middle_point, heading_of_ego, width_of_ego)
            ahead_area_polygon_for_opposite = self.calculate_area_of_ahead(head_middle_point, heading_of_ego, width_of_ego, dist=30)
            crosswalkAhead = self.calculate_distance_to_crosswalk_ahead(ahead_area_polygon, ego_position_area)
            pose['crosswalkAhead'] = crosswalkAhead
            junctionAhead = self.calculate_distance_to_junction_ahead(ahead_area_polygon, ego_position_area, pose)
            pose["junctionAhead"] = junctionAhead
            stopSignAhead = self.calculate_distance_to_stopline_of_sign_ahead(ahead_area_polygon, ego_position_area) #the stopSignAhead API
            pose["stopSignAhead"] = stopSignAhead
            stoplineAhead = self.calculate_distance_to_stopline_of_ahead(back_area_polygon, ego_position_area, stopSignAhead) #the stoplineAhead API
            pose["stoplineAhead"] = stoplineAhead
            planning_time = find_time(self.record['planning'].keys(), pose_key)
            if planning_time == None:
                pose['planning_of_turn'] = 0
            else:
                pose['planning_of_turn'] = self.record['planning'][planning_time]['planning_turn_signal']
            obs['NPCAhead'] = self.find_npc_ahead(obs['obsList'], ahead_area_polygon, ego_position_area, pose["currentLane"], pose['junction_ahead'])
            obs['PedAhead'] = self.find_ped_ahead(obs["obsList"], ahead_area_polygon, ego_position_area)
            obs["NPCOpposite"] = self.find_npc_opposite(obs["obsList"], ahead_area_polygon_for_opposite, ego_position_area, heading_of_ego)
            obs['npcClassification'] = self.classify_oblist(obs["obsList"], pose)
            pose["isTrafficJam"] = self.check_is_traffic_jam(obs["obsList"], pose)
            single_trace["ego"] = pose
            if self.is_groundtruth:
                single_trace["truth"] = obs
            else:
                single_trace["perception"] = obs
            traffic_light_time = find_time(self.record['traffic_light'].keys(), pose_key)
            # if currentLane['type'] == 'junction':
            #     single_trace["traffic_lights"] = {}
            # else:
            single_trace["traffic_lights"] = self.record['traffic_light'][traffic_light_time] if traffic_light_time != None else {}
            distance = self.calculate_distToDEstination(ego_position_area)
            #threshold = 0.01
            if distance < 2:
                pose['reach_destinaton'] = True
            else:
                pose['reach_destinaton'] = False
            if planning_time == None:
                pose['isOverTaking'] = False
            else:
                pose["isOverTaking"] = self.record['planning'][planning_time]['is_overtaking']
            self.trace[pose_key] = copy.deepcopy(single_trace)
        else:
            pass

    def check_record(self, case_id=0, repeat_id=0, file="sample/"): 
        # directory = f"{dir_prefix}case_{case_id}/record_{repeat_id}/"
        # cmd = f"docker cp apollo_neo_dev_core:/home/sunsun/.apollo/resources/records/ {directory}"
        # subprocess.run(cmd, shell=True, capture_output=True, text=True)
        # # return
        # files = os.listdir(directory+"default_record_name/")  
        # sorted_files = sorted(files)

        sorted_files = [file]
        self.record = {}

        for file_name in sorted_files:
            # file_name = f"{directory}default_record_name/{file_name}" 
            
            self.save_message(file_name, 'pose')
            key_list = list(_map.keys())
            key_list.remove('pose')
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
               executor.map(self.save_message, [file_name] * (len( _map.keys()) - 1), key_list)
            
        pose_list = sorted(list(self.record['pose'].keys()))
        chassis_list = sorted(list(self.record['chassis'].keys()))
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for _ in tqdm(executor.map(self.process_pose, pose_list, chassis_list), total=len(pose_list), desc=f"Processing truth:"):
                pass

        self.trace_time = sorted(self.trace.keys())
        for key, value in tqdm(enumerate(self.trace_time), desc = f"Processing trace:", total=len(self.trace_time)):
            self.check_stuck(value)
            self.check_is_lane_changing(key, value)
            self.check_is_overtaking(value)
            self.check_is_TurningAround(key, value)
            self.Find_Priority_NPCs_and_Peds(key, value)


        minEgoObsDist = None
        reach = False
        for time, _ii in self.trace.items():
            if reach == False and _ii["ego"]["reach_destinaton"] == True:
                reach = True
            truth = _ii["truth"]
            if truth.__contains__("minDistToEgo"):
                if minEgoObsDist == None or minEgoObsDist > truth["minDistToEgo"]:
                    minEgoObsDist = truth["minDistToEgo"]
            else:
                minEgoObsDist = 200
        if minEgoObsDist != None and minEgoObsDist <= 0:
            testFailures = ['Accident']
        else:
            testFailures = []
        
        self.result["testFailures"] = testFailures
        self.result["trace"] = self.trace
        self.result["completed"] = reach
        self.result["destinationReached"] = reach
        self.result["groundTruthPerception"] = self.is_groundtruth
        self.result["AgentNames"] = self.agent

        with open(f'{file}.pickle', 'wb') as file:
            pickle.dump(self.result, file)


    def get_four_polygon_point_list_of_ego(self, original_point,heading_of_ego,lengthen_of_ego,width_of_ego):
        zhouju = 2.697298
        result = []
        point0 = []
        point0.append(original_point[0] + (lengthen_of_ego - zhouju)/2 + zhouju)
        point0.append(original_point[1] + width_of_ego/2)  
        x = point0[0] 
        y = point0[1]
        point0 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        result.append(point0)
        point1 = []
        point1.append(original_point[0] + (lengthen_of_ego - zhouju)/2 + zhouju)
        point1.append(original_point[1] - width_of_ego/2)
        x = point1[0] 
        y = point1[1]
        point1 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        result.append(point1)
        point2 = []
        point2.append(original_point[0] - (lengthen_of_ego - zhouju)/2 )
        point2.append(original_point[1] - width_of_ego/2)
        x = point2[0] 
        y = point2[1]
        point2 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        result.append(point2)
        point3 = []
        point3.append(original_point[0] - (lengthen_of_ego - zhouju)/2 )
        point3.append(original_point[1] + width_of_ego/2)
        x = point3[0] 
        y = point3[1]
        point3 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        result.append(point3)
        return result

    def add_heading_to_ego(self, angle, x, y, pointx, pointy):
        angle = -angle
        srx = (x-pointx)*math.cos(angle) + (y-pointy)*math.sin(angle)+pointx
        sry = (y-pointy)*math.cos(angle) - (x-pointx)*math.sin(angle)+pointy
        point = [srx , sry]
        return point

    def get_the_head_middle_point_of_ego(self, original_point,heading_of_ego,lengthen_of_ego,width_of_ego):
        zhouju = 2.697298
        result = []
        point0 = []
        point0.append(original_point[0] + (lengthen_of_ego - zhouju)/2 + zhouju)
        point0.append(original_point[1] + width_of_ego/2)  
        x = point0[0] 
        y = point0[1]
        point0 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        point1 = []
        point1.append(original_point[0] + (lengthen_of_ego - zhouju)/2 + zhouju)
        point1.append(original_point[1] - width_of_ego/2)
        x = point1[0] 
        y = point1[1]
        point1 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        result.append((point0[0] + point1[0])/2) 
        result.append((point0[1] + point1[1])/2) 
        return result

    def get_the_back_middle_point_of_ego(self,original_point,heading_of_ego,lengthen_of_ego,width_of_ego):
        zhouju = 2.697298
        result = []
        point0 = []
        point0.append(original_point[0] - (lengthen_of_ego - zhouju)/2 )
        point0.append(original_point[1] - width_of_ego/2)  
        x = point0[0] 
        y = point0[1]
        point0 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        point1 = []
        point1.append(original_point[0] - (lengthen_of_ego - zhouju)/2 )
        point1.append(original_point[1] + width_of_ego/2)
        x = point1[0] 
        y = point1[1]
        point1 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        result.append((point0[0] + point1[0])/2) 
        result.append((point0[1] + point1[1])/2) 
        return result

    def check_current_lane(self, ego_position_area):
        value = {}
        assert ego_position_area is not None
        ego = ego_position_area
        result = self.map_info.find_which_area_the_ego_is_in(ego)

        if result != None:
            if result[0].__contains__("lane_id"):
                ego_lane_id = result[0]["lane_id"]
                value["currentLaneId"] = ego_lane_id
                value['type'] = 'lane'
                forward = 0
                left = 0
                right = 0
                U = 0
                number = 0
                for _i in result:
                    number += _i["laneNumber"] 
                    if _i["turn"] == 'NO_TURN':
                        forward = 1
                    elif _i["turn"] == 'LEFT_TURN':
                        left = 1
                    elif _i["turn"] == 'RIGHT_TURN':
                        right = 1
                    elif _i["turn"] == 'U_TURN':
                        U = 1
                if forward == 1:
                    if left == 1:
                        if right == 1:
                            value["turn"] = 6
                        else:
                            value["turn"] = 4
                    else:
                        if right == 1:
                            value["turn"] = 5
                        else:
                            value["turn"] = 0
                else:
                    if left == 1:
                        if right == 1:
                            value["turn"] = 7
                        else:
                            value["turn"] = 1
                    else:
                        if right == 1:
                            value["turn"] = 2
                        else:
                            if U == 1:
                                value["turn"] = 3
                            else:
                                print("Unexpected!!!")
                value["number"] = number
            if result[0].__contains__("junction_id"):
                ego_lane_id = result[0]["junction_id"]
                value["currentLaneId"] = ego_lane_id
                value["type"] = 'junction'
                value["number"] = 0 
        else:
            ego_lane_id = None
            value["currentLaneId"] = ego_lane_id
            value["number"] = -1

        return value

    def convert_velocity_to_speed(self, velocity):
        x = velocity["x"]
        y = velocity["y"]
        z = velocity["z"] if ('z' in velocity) else 0
        return math.sqrt(x*x+y*y+z*z)
    
    def calculate_distToEgo(self, time_use, obstacle):
        original_point = []
        original_point.append(self.record['pose'][time_use]["pose"]["position"]["x"])
        original_point.append(self.record['pose'][time_use]["pose"]["position"]["y"])
        heading_of_ego = self.record['pose'][time_use]["pose"]["heading"]
        lengthen_of_ego = self.record['pose'][time_use]["size"]["length"]
        width_of_ego = self.record['pose'][time_use]["size"]["width"]
        ego_polygonPointList = []
        ego_polygonPointList = self.get_four_polygon_point_list_of_ego(original_point,heading_of_ego,lengthen_of_ego,width_of_ego)
        obstacles_polygonPointList = []
        for _i in obstacle["polygonPoint"]:
            temp = []
            temp.append(_i["x"])
            temp.append(_i["y"])
            obstacles_polygonPointList.append(temp)
        ego = Polygon(ego_polygonPointList)
        obstacle = Polygon(obstacles_polygonPointList)
        Mindis = ego.distance(obstacle)
        return Mindis

    def calculate_area_of_ahead(self, original_point, heading_of_ego,width_of_ego, dist=200):
        ahead_area = []
        point0 = []
        point0.append(original_point[0] + dist)
        point0.append(original_point[1] + dist)  
        x = point0[0] 
        y = point0[1]
        point0 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        ahead_area.append(point0)

        point1 = []
        point1.append(original_point[0] + dist)
        point1.append(original_point[1] - dist)
        x = point1[0] 
        y = point1[1]
        point1 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        ahead_area.append(point1)

        point2 = []
        point2.append(original_point[0] - 0 )
        point2.append(original_point[1] - width_of_ego/2)
        x = point2[0] 
        y = point2[1]
        point2 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        ahead_area.append(point2)

        point3 = []
        point3.append(original_point[0] - 0 )
        point3.append(original_point[1] + width_of_ego/2)
        x = point3[0] 
        y = point3[1]
        point3 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        ahead_area.append(point3)

        ahead_area_polygon = Polygon(ahead_area)
        return ahead_area_polygon

    def calculate_area_of_ahead2(self, original_point, heading_of_ego):
		 # calculate the Ahead area
        ahead_area = []
        point0 = []
        point0.append(original_point[0] + 200)
        point0.append(original_point[1] + 200)  
        x = point0[0] 
        y = point0[1]
        point0 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        ahead_area.append(point0)
        point1 = []
        point1.append(original_point[0] + 200)
        point1.append(original_point[1] - 200)
        x = point1[0] 
        y = point1[1]
        point1 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        ahead_area.append(point1)
        point2 = []
        point2.append(original_point[0] - 0 )
        point2.append(original_point[1] - 200)
        x = point2[0] 
        y = point2[1]
        point2 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        ahead_area.append(point2)
        point3 = []
        point3.append(original_point[0] - 0 )
        point3.append(original_point[1] + 200)
        x = point3[0] 
        y = point3[1]
        point3 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        ahead_area.append(point3)
        ahead_area_polygon = Polygon(ahead_area)
        return ahead_area_polygon

    def calculate_area_of_ahead_left(self, original_point, heading_of_ego):
		 # calculate the Ahead area
        ahead_area = []
        point0 = []
        point0.append(original_point[0] + 30)
        point0.append(original_point[1] + 0)  
        x = point0[0] 
        y = point0[1]
        point0 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        ahead_area.append(point0)

        point1 = []
        point1.append(original_point[0] + 30)
        point1.append(original_point[1] - 30)
        x = point1[0] 
        y = point1[1]
        point1 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        ahead_area.append(point1)

        point2 = []
        point2.append(original_point[0] - 0 )
        point2.append(original_point[1] - 30)
        x = point2[0] 
        y = point2[1]
        point2 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        ahead_area.append(point2)

        point3 = []
        point3.append(original_point[0] - 0 )
        point3.append(original_point[1] + 0)
        x = point3[0] 
        y = point3[1]
        point3 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        ahead_area.append(point3)

        ahead_area_polygon = Polygon(ahead_area)
        return ahead_area_polygon

    def calculate_area_of_ahead_right(self, original_point, heading_of_ego):
            # calculate the Ahead area
        ahead_area = []
        point0 = []
        point0.append(original_point[0] + 30)
        point0.append(original_point[1] + 30)  
        x = point0[0] 
        y = point0[1]
        point0 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        ahead_area.append(point0)

        point1 = []
        point1.append(original_point[0] + 30)
        point1.append(original_point[1] - 0)
        x = point1[0] 
        y = point1[1]
        point1 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        ahead_area.append(point1)

        point2 = []
        point2.append(original_point[0] - 0 )
        point2.append(original_point[1] - 0)
        x = point2[0] 
        y = point2[1]
        point2 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        ahead_area.append(point2)

        point3 = []
        point3.append(original_point[0] - 0 )
        point3.append(original_point[1] + 30)
        x = point3[0] 
        y = point3[1]
        point3 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        ahead_area.append(point3)

        ahead_area_polygon = Polygon(ahead_area)
        return ahead_area_polygon

    def calculate_area_of_back_left(self, original_point, heading_of_ego, width_of_ego):
		 # calculate the Ahead area
        ahead_area = []
        point0 = []
        point0.append(original_point[0] + 0)
        point0.append(original_point[1] - width_of_ego/2-0.3)  
        x = point0[0] 
        y = point0[1]
        point0 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        ahead_area.append(point0)

        point1 = []
        point1.append(original_point[0] + 0)
        point1.append(original_point[1] - width_of_ego/2-0.3-3)
        x = point1[0] 
        y = point1[1]
        point1 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        ahead_area.append(point1)

        point2 = []
        point2.append(original_point[0] - 30 )
        point2.append(original_point[1] - width_of_ego/2-0.3-3)
        x = point2[0] 
        y = point2[1]
        point2 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        ahead_area.append(point2)

        point3 = []
        point3.append(original_point[0] - 30 )
        point3.append(original_point[1] - width_of_ego/2-0.3)
        x = point3[0] 
        y = point3[1]
        point3 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        ahead_area.append(point3)

        ahead_area_polygon = Polygon(ahead_area)
        return ahead_area_polygon

    def calculate_area_of_back_right(self, original_point, heading_of_ego,width_of_ego):
            # calculate the Ahead area
        ahead_area = []
        point0 = []
        point0.append(original_point[0] + 0)
        point0.append(original_point[1] + width_of_ego/2+0.3+3)  
        x = point0[0] 
        y = point0[1]
        point0 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        ahead_area.append(point0)

        point1 = []
        point1.append(original_point[0] + 0)
        point1.append(original_point[1] + width_of_ego/2+0.3)
        x = point1[0] 
        y = point1[1]
        point1 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        ahead_area.append(point1)

        point2 = []
        point2.append(original_point[0] - 30 )
        point2.append(original_point[1] + width_of_ego/2+0.3)
        x = point2[0] 
        y = point2[1]
        point2 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        ahead_area.append(point2)

        point3 = []
        point3.append(original_point[0] - 30 )
        point3.append(original_point[1] + width_of_ego/2+0.3+3)
        x = point3[0] 
        y = point3[1]
        point3 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
        ahead_area.append(point3)

        ahead_area_polygon = Polygon(ahead_area)
        return ahead_area_polygon

    def calculate_distance_to_crosswalk_ahead(self, ahead_area_polygon, ego_position_area):
        result = []
        crosswalk_list = self.map_info.get_crosswalk_config()
        assert ego_position_area is not None
        ego = ego_position_area
        for key in crosswalk_list:
            the_area = crosswalk_list[key]  
            if ahead_area_polygon.distance(the_area) == 0:     
                result.append(ego.distance(the_area))
        if result != []:
            _min = min(result)
        else:
            _min = 200
        return _min

    def calculate_distance_to_junction_ahead(self, ahead_area_polygon, ego_position_area, pose):
        result = {}
        junction_list = self.map_info.areas["junction_areas"]
        assert ego_position_area is not None
        ego = ego_position_area
        for key in junction_list:
            the_area = junction_list[key]  
            if ahead_area_polygon.distance(the_area) == 0:          
                dist = ego.distance(the_area)
                result[key] = dist
        if result!= {}:
            pose['junction_ahead'] = min(result, key = result.get)
            _min = result[pose['junction_ahead']]
        else:
            pose['junction_ahead'] = None
            _min = 200
        return _min

    def calculate_distance_to_stopline_of_ahead(self, ahead_area_polygon, ego_position_area, stopSignAhead):
        min1 = stopSignAhead
        result = []
        traffic_signal_list = self.map_info.get_traffic_signals()
        assert ego_position_area is not None
        ego = ego_position_area
        for _i in traffic_signal_list:
            the_line = _i["stop_line"]
            if ahead_area_polygon.distance(the_line) == 0:              
                result.append(ego.distance(the_line))
        if result != []:
            _min = min(result)
        else:
            _min = 200
        return min(_min, min1)
    
    def calculate_distance_to_stopline_of_sign_ahead(self, ahead_area_polygon, ego_position_area):
        result = []
        traffic_sign_list = self.map_info.get_traffic_sign()
        assert ego_position_area is not None
        ego = ego_position_area
        for _i in traffic_sign_list:
            the_line = _i["stop_line"]
            if ahead_area_polygon.distance(the_line) == 0:              
                result.append(ego.distance(the_line))
        if result != []:
            _min = min(result)
        else:
            _min = 200
        return _min

    def find_npc_ahead(self, oblist, ahead_area_polygon, ego_position_area, pose_area, junctionAhead):
        assert ego_position_area is not None
        ego = ego_position_area
        return_value = None
        _temp = {}
        if pose_area != None:
            if 'type' not in pose_area:
                return return_value
            if pose_area['type'] == 'lane':
                for _i in oblist:
                    area = _i['currentLane']['area']
                    if ahead_area_polygon.distance(area) == 0 and _i["type"] == 'VEHICLE' and \
                        pose_area['type'] == _i['currentLane']['type'] and pose_area['currentLaneId'] == _i['currentLane']['currentLaneId']:
                         _temp[_i["id"]] = ego.distance(area)
                         return_value = _i["id"]
                    # elif _i['currentLane']['type'] == 'junction' and _i['currentLane']['currentLaneId'] == junctionAhead:
                    #     _temp[_i["id"]] = ego.distance(area)
                    #     return_value = _i["id"]
                for key in _temp:
                    if _temp[key] < _temp[return_value]:
                        return_value = key
            elif pose_area['type'] == 'junction':
                for _i in oblist:
                    area = _i['currentLane']['area']
                    if ahead_area_polygon.distance(area) == 0 and _i["type"] == 'VEHICLE':
                        _temp[_i["id"]] = ego.distance(area)
                        return_value = _i["id"]
                for key in _temp:
                    if _temp[key] < _temp[return_value]:
                        return_value = key
        else:
            print("!bug of localization of ego")     
        return return_value

    def find_ped_ahead(self, oblist, ahead_area_polygon, ego_position_area):
        assert ego_position_area is not None
        ego = ego_position_area
        return_value = None
        _temp = {}
        for _i in oblist:
            the_area = _i['currentLane']['area'] 
            if ahead_area_polygon.distance(the_area) == 0 and _i["type"] == 'PEDESTRIAN':
                _temp[_i["id"]] = ego.distance(the_area)
                return_value = _i["id"]             
        for key in _temp:
            if _temp[key] < _temp[return_value]:
                return_value = key 
        return return_value

    def find_npc_opposite(self, oblist, ahead_area_polygon, ego_position_area, heading_of_ego):
        assert ego_position_area is not None
        ego = ego_position_area
        return_value = None
        _temp = {}
        for _i in oblist:
            the_area = _i['currentLane']['area']
            if ahead_area_polygon.distance(the_area) == 0 and _i["type"] == 'VEHICLE':
                heading_of_npc = _i["theta"]
                heading_of_npc = self.process_with_angle_pi(heading_of_npc)
                if abs(heading_of_npc- heading_of_ego)> 3*math.pi/4 and abs(heading_of_npc- heading_of_ego)< 5*math.pi/4:					
                    _temp[_i["id"]] = ego.distance(the_area)
                    return_value = _i["id"]             
        for key in _temp:
            if _temp[key] < _temp[return_value]:
                return_value = key 
        return return_value

    def classify_oblist(self, oblist, pose):
        the_result_after_classification = dict()
        same_list = []
        different_list = []
        junction_list = []
        fourth_list = []
        fivth_list = []
        unknown_list = []
        result_ego = pose['currentLane']
        for ob in oblist:
            temp = dict()
            result_obs = ob['currentLane']
            if result_ego != None and result_ego != {} and result_obs != None and result_obs != {}:
                if 'type' not in result_ego:
                    continue
                if result_ego['type'] == 'lane':
                    if result_obs['type'] == 'lane':
                        temp["name"] = ob["id"]
                        temp["laneId"] = result_obs["currentLaneId"]
                        temp["turn"] = result_obs["turn"]
                        temp['type'] = result_obs['type']
                        if self.map_info.check_whether_two_lanes_are_in_the_same_road(result_ego["currentLaneId"], result_obs["currentLaneId"]):
                            same_list.append(temp)
                        else:
                            different_list.append(temp)
                    elif result_obs['type'] == 'junction':
                        temp["name"] = ob["id"]
                        temp["junctionId"] = result_obs["currentLaneId"]
                        temp['type'] = result_obs['type']
                        junction_list.append(temp)
                elif result_ego['type'] == 'junction':
                    if result_obs['type'] == 'lane':
                        temp["name"] = ob["id"]
                        temp["laneId"] = result_obs["currentLaneId"]
                        temp["turn"] = result_obs["turn"]
                        temp['type'] = result_obs['type']
                        fourth_list.append(temp)
                    elif result_obs['type'] == 'junction':
                        temp["name"] = ob["id"]
                        temp["junctionId"] = result_obs["currentLaneId"]
                        temp['type'] = result_obs['type']
                        fivth_list.append(temp)
            else:
                temp["name"] = ob["id"]
                unknown_list.append(temp)

        #When ego on lane
        the_result_after_classification["NextToEgo"] = same_list
        the_result_after_classification["OntheDifferentRoad"] = different_list
        the_result_after_classification["IntheJunction"] = junction_list

        #when ego on junction
        the_result_after_classification["EgoInjunction_Lane"] = fourth_list
        the_result_after_classification["EgoInjunction_junction"] = fivth_list
        return the_result_after_classification

    def check_is_traffic_jam(self, oblist, pose):
        number = 0
        for _i in oblist:
            if _i["speed"] < 1 and _i["type"] == 'VEHICLE':
                if _i['currentLane']['type'] == 'junction':
                    if _i['currentLane']["currentLaneId"] == pose['junction_ahead']:
                        number = number + 1

        if number >=6:
            return True
        else:
            return False

    def calculate_distToDEstination(self, ego_position_area):
        point = Point(self.destination[0],self.destination[1])
        distance = point.distance(ego_position_area)
        return distance

    def check_is_lane_changing(self, key, value):
        num_of_track = -10 	#check the value of 5 states before
        if key >= -num_of_track:
            if self.trace[self.trace_time[key + num_of_track]]["ego"]["isLaneChanging"] == False:
                previous_trace = self.trace[self.trace_time[key + num_of_track]]
                orig = previous_trace["ego"]["currentLane"]["currentLaneId"]
                if previous_trace["ego"]["planning_of_turn"] != 0:
                    for num in range(key + num_of_track + 1, key+1):
                        dest = self.trace[self.trace_time[num]]["ego"]["currentLane"]["currentLaneId"]
                        In_the_same_road = self.map_info.check_whether_two_lanes_are_in_the_same_road(orig, dest)
                        if dest != orig and dest != None and In_the_same_road == True:
                            self.trace[self.trace_time[key + num_of_track]]["ego"]["isLaneChanging"] = True

    def check_is_overtaking(self, value):	
        if self.trace[value]["ego"]["isOverTaking"]:
            self.trace[value]["ego"]["isLaneChanging"] = True		
        else:
            self.trace[value]["ego"]["isLaneChanging"] = False	

    def check_is_TurningAround(self, key, value):
        self.trace[value]["ego"]["isTurningAround"] = False
        num_of_track = -20 	
        if key >= -num_of_track: 
            # self.trace[self.trace_time[key + num_of_track]]["ego"]["isTurningAround"] = False
            previous_trace = self.trace[self.trace_time[key + num_of_track]]
            orig = previous_trace["ego"]["pose"]["heading"]
            orig = self.process_with_angle_pi(orig)
            if previous_trace["ego"]["planning_of_turn"] != 0:
                for num in range(key + num_of_track + 1, key+1):
                    dest = self.trace[self.trace_time[num]]["ego"]["pose"]["heading"]
                    dest = self.process_with_angle_pi(dest)
                    if abs(dest - orig) > 3*math.pi/4:
                        self.trace[self.trace_time[key + num_of_track]]["ego"]["isTurningAround"] = True

        # if self.trace[value]['ego']["reach_destinaton"] or self.Check_The_vehicle_is_stuck_or_not == "Stuck!":
        #     if key >= -num_of_track: 
        #         for num in range(key + num_of_track + 1, key):
        #             self.trace[self.trace_time[num]]["ego"]["isTurningAround"] = False
        #     else:
        #         for num in range(0, key):
        #             self.trace[self.trace_time[num]]["ego"]["isTurningAround"] = False

    def check_stuck(self, value):
        threshold = 0.01
        if self.position_for_check == {}:
            self.position_for_check = self.trace[value]["ego"]["pose"]["position"]
            self.position_check_num = 0
        elif abs(self.position_for_check["x"] - self.trace[value]["ego"]["pose"]["position"]["x"]) <= threshold and \
             abs(self.position_for_check["y"]- self.trace[value]["ego"]["pose"]["position"]["y"]) <= threshold and \
             abs(self.position_for_check["z"]- self.trace[value]["ego"]["pose"]["position"]["z"]) <= threshold:
            self.position_check_num += 1
            if self.position_check_num >= 150:
                self.Check_The_vehicle_is_stuck_or_not = "Stuck!"
            else:
                self.Check_The_vehicle_is_stuck_or_not = None
        else:
            self.position_check_num = 0
            self.position_for_check = self.trace[value]["ego"]["pose"]["position"]

    def process_with_angle_pi(self, angle_pi):
        if angle_pi<0:
            return angle_pi + 2*math.pi
        else:
            return angle_pi

    def Find_Priority_NPCs_and_Peds(self, key, value):
        num_of_track = -20
        self.trace[value]['ego']['PriorityNPCAhead'] = False
        self.trace[value]['ego']['PriorityPedsAhead'] = False
        if key >= -num_of_track or self.trace[value]['ego']["reach_destinaton"] or self.Check_The_vehicle_is_stuck_or_not == "Stuck!":
            ego = self.trace[value]["ego"]
            original_point = []
            original_point.append(ego["pose"]["position"]["x"])
            original_point.append(ego["pose"]["position"]["y"])
            heading_of_ego = ego["pose"]["heading"]
            lengthen_of_ego = ego["size"]["length"]
            width_of_ego = ego["size"]["width"]
            back_middle_point = self.get_the_back_middle_point_of_ego(original_point, heading_of_ego, lengthen_of_ego, width_of_ego)
            ahead_square_area = self.calculate_area_of_ahead2(back_middle_point, heading_of_ego)
            left_area_polygon = self.calculate_area_of_ahead_left(back_middle_point, heading_of_ego)
            right_area_polygon = self.calculate_area_of_ahead_right(back_middle_point, heading_of_ego)
            backward_area_left = self.calculate_area_of_back_left(back_middle_point, heading_of_ego, width_of_ego)
            backward_area_right = self.calculate_area_of_back_right(back_middle_point, heading_of_ego, width_of_ego)
        if key >= -num_of_track: 
            self._sub_Find_Priority_NPCs_and_Peds(ahead_square_area , left_area_polygon, right_area_polygon, key + num_of_track, backward_area_left, backward_area_right)
        if self.trace[value]['ego']["reach_destinaton"] or self.Check_The_vehicle_is_stuck_or_not == "Stuck!":
            if key >= -num_of_track: 
                for num in range(key + num_of_track + 1, key+1):
                    self._sub_Find_Priority_NPCs_and_Peds(ahead_square_area , left_area_polygon, right_area_polygon, num, backward_area_left, backward_area_right)
            else:				
                for num in range(0, key+1):
                    self._sub_Find_Priority_NPCs_and_Peds(ahead_square_area , left_area_polygon, right_area_polygon, num, backward_area_left, backward_area_right)

    def _sub_Find_Priority_NPCs_and_Peds(self, ahead_square_area , left_area_polygon, right_area_polygon, num_of_track, backward_area_left, backward_area_right):
        previous_trace = self.trace[self.trace_time[num_of_track]]
        if self.is_groundtruth:
            obstacles = previous_trace["truth"]["obsList"]
            _road =  previous_trace["truth"]
        else:
            obstacles = previous_trace["perception"]["obsList"]
            _road =  previous_trace["perception"]

        heading_of_ego = previous_trace["ego"]["pose"]["heading"]
        heading_of_ego = self.process_with_angle_pi(heading_of_ego)

        # if we are turning, we should give way to the cars in the direct way
        for obstacle in obstacles:
            the_area = obstacle['currentLane']['area']
            # Find priority NPC of ahead
            if _road['NPCAhead'] == obstacle['id'] and obstacle['distToEgo'] < 3:
                previous_trace["ego"]["PriorityNPCAhead"] = True
            if obstacle["type"] == 'VEHICLE':
                # Find priority NPC when turning
                heading_of_npc = obstacle["theta"]
                heading_of_npc = self.process_with_angle_pi(heading_of_npc)
                if previous_trace["ego"]["planning_of_turn"] != 0 and previous_trace["ego"]["isLaneChanging"] == False:
                    if abs(heading_of_npc- heading_of_ego)>math.pi/4 and abs(heading_of_npc- heading_of_ego)< 3*math.pi/4:
                        if obstacle["distToEgo"] < 30 and ahead_square_area.distance(the_area) == 0:
                            previous_trace["ego"]["PriorityNPCAhead"] = True
                # Find priority NPC when lane changing
                if previous_trace["ego"]["isLaneChanging"] == True:
                    if abs(heading_of_npc- heading_of_ego)<math.pi/4 :
                        ego_speed = self.convert_velocity_to_speed(previous_trace["ego"]["pose"]["linearVelocity"])
                        if previous_trace["ego"]["planning_of_turn"] == 1 and backward_area_left.distance(the_area) == 0: #left lane changing
                            if obstacle["distToEgo"] < 10 and obstacle["speed"] > ego_speed:
                                previous_trace["ego"]["PriorityNPCAhead"] = True
                                print("Find priority NPC for left lane changing!")
                        if previous_trace["ego"]["planning_of_turn"] == 2 and backward_area_right.distance(the_area) == 0: #right lane changing
                            if obstacle["distToEgo"] < 10 and obstacle["speed"] > ego_speed:
                                previous_trace["ego"]["PriorityNPCAhead"] = True
                                print("Find priority NPC for right lane changing!")

            elif obstacle["type"] == 'PEDESTRIAN':
                if previous_trace["ego"]["planning_of_turn"] == 0:						
                    if obstacle["distToEgo"] < 3 and ahead_square_area.distance(the_area) == 0: 
                        previous_trace["ego"]["PriorityPedsAhead"] = True
                        print("Find priority Ped for direct!")
                if previous_trace["ego"]["planning_of_turn"] == 1:						
                    if obstacle["distToEgo"] < 10 and left_area_polygon.distance(the_area) == 0: 
                        previous_trace["ego"]["PriorityPedsAhead"] = True
                        print("Find priority Ped for turning left!")
                if previous_trace["ego"]["planning_of_turn"] == 2:						
                    if obstacle["distToEgo"] < 10 and right_area_polygon.distance(the_area) == 0: 
                        previous_trace["ego"]["PriorityPedsAhead"] = True
                        print("Find priority Ped for turning right!")

    def calculate_distance_to_traffic_light_stop_line(self, time_use, ID):
        traffic_signal_list = self.map_info.get_traffic_signals()
        ego = self.record['pose'][time_use]['area']

        _distance = 10000000
        single_result = {}
        for _i in traffic_signal_list:

            if _i["id"] == ID:             
                single_result["id"] = _i["id"]
                single_result["types"] = _i["sub_signal_type_list"]
                the_line = _i["stop_line"]
                single_result["distance"] = ego.distance(the_line)
            else:
                the_line = _i["stop_line"]
                distance_of_temp = ego.distance(the_line)
                if distance_of_temp < _distance:
                    _distance = distance_of_temp

                if hasattr(single_result, 'distance'):
                    if single_result['distance'] > _distance:
                        print('Traffic Light Error: wrong traffic light perception!')
                        self.testFailures.append("Traffic Light Error: wrong traffic light perception! ")
                    else:
                        pass
        return single_result["distance"]

    def lawbreak(self):
        extracted_data = ExtractAll('law.txt', self.is_groundtruth)
        specifications_in_scenario = extracted_data.Get_Specifications()
        for spec_index in range(len(specifications_in_scenario)):
                first_specification = specifications_in_scenario[spec_index]
                single_specification = SingleAssertion(first_specification, self.map_info, self.start_position)
                self._lawbreak(single_specification)

    def _lawbreak(self, single_spec):
        directory = 'analysis/'
        maxnum = len(single_spec.sub_violations)
        remaining_sub_violations = single_spec.sub_violations
        mapping = dict()
        seed = dict()
        for item in remaining_sub_violations:
            mapping[item] = -1000
            seed[item] = None


        output_trace = copy.deepcopy(self.result)
        if not output_trace["destinationReached"]:
            logging.info("Not reach the destination")
            with open(directory + '/Incompleted.txt', 'a') as f:
                 f.write(self.name)
                 f.write('\n')
        if len(output_trace['trace']) > 1:
            encoded_testcase = EncodedTestCase(output_trace, single_spec, self.weather)
            if encoded_testcase.muti_fitness == {}:
                encoded_testcase.compute_muti_fitness()
                if 'Accident!' in output_trace["testFailures"]:
                    with open(directory + '/AccidentTestCase.txt', 'a') as bug_file:
                        bug_file.write(self.name + '\n')
                        bug_file.write("The detailed fitness values:" + str(encoded_testcase.muti_fitness) + '\n')
                        bug_file.write('\n')
                if encoded_testcase.fitness <= 0.0:
                    with open(directory + '/improvedTestCase.txt', 'a') as bug_file:
                        bug_file.write(self.name + '\n')
                        string_index2 = "The detailed fitness values:" + str(encoded_testcase.muti_fitness) + '\n'
                        bug_file.write(string_index2)
                        bug_file.write('\n')
        else:
            pass

def parse_record():

    SAMPLE_DATA = "/data/sample/" 
    SCENARIO_DIR =  "/home/sunsun/Desktop/UserIntercation/Lawbreak/scenario_sets/65fbd4b2ec034cc74fa7728c/scenarios"
    for f in os.listdir(SCENARIO_DIR):
        with open(f"{SCENARIO_DIR}/{f}", 'r') as js_file:
            data = json.loads(js_file.read())
        scenario_id = data["descriptionEnTokens"][0]
        if scenario_id in ["Law38_2_2", "Law38_0_2", "Law38_1_1","Law38_2_1", "Law44_2", "Law_53_0_1"]:
            continue
 
        RECORDS_DIR = f"records/{scenario_id}_records"
        if not os.path.exists(RECORDS_DIR):
            continue
        print(RECORDS_DIR) 
 
        map_Dir = data['scenario']['mapDir']
        # map_name = map_Dir.split("/")[-1]
        map_name = 'sunnyvale'
        # map_name = 'san'
        map_info = get_map_info(map_name)
      
        for f in os.listdir(RECORDS_DIR):  
            path = f"{RECORDS_DIR}/{f}" 
            print(path) 
            mutation = Mutation(data, map_name, map_info, "65e0308b6f0ae871927b3bce")
            mutation.check_record(file = path)  


parse_record()
# if __name__ == "__main__":  
