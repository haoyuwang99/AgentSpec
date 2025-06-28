# import gc
# import math

import numpy as np
# import json
import copy

# import numpy.random

# from EXtraction import ExtractAll
from monitor import Monitor
# from TestCaseRandom import TestCaseRandom
# from TracePreprocess import Trace
import random
import ast
from itertools import chain, islice
from random import gauss
# import operator
# from map_for_bridge import get_map_info
# from pedestrian_motion_checking import pedestrian_in_crosswalk
# from config import get_npc_list, get_pedestrian_list, get_weather_list

# file = 'map_lane_config.txt'
# with open(file) as f:
#     lane_config = json.load(f)

# vehicle_list = get_npc_list()
# pedestrian_list = get_pedestrian_list()
# weather_list = get_weather_list()
# offset_offset = 5.0


# def get_testcase(trace_scneario):
#     testcase_ = {}
#     # testcase_['ScenarioName'] = trace_scneario['ScenarioName']
#     # testcase_['MapVariable'] = trace_scneario['MapVariable']
#     # testcase_['map'] = trace_scneario['map']
#     # testcase_['time'] = trace_scneario['time']
#     # testcase_['weather'] = trace_scneario['weather']
#     testcase_['ego'] = trace_scneario['ego']
#     testcase_['npcList'] = trace_scneario['npcList']
#     testcase_['pedestrianList'] = trace_scneario['pedestrianList']
#     testcase_['obstacleList'] = trace_scneario['obstacleList']
#     # testcase_['AgentNames'] = trace_scneario['AgentNames']
#     # remove the vector positions in ego's start and destination states
#     testcase_['ego']['start'].pop('position', None)
#     testcase_['ego']['start']['heading'].pop('ref_point', None)
#     testcase_['ego']['destination'].pop('position', None)
#     testcase_['ego']['destination']['heading'].pop('ref_point', None)

#     map_info = get_map_info(trace_scneario['map'])
#     lane_config = map_info.get_lane_config()
#     crosswalk_config = map_info.get_crosswalk_config()

#     for _i in range(len(testcase_['npcList'])):
#         testcase_['npcList'][_i]['start'].pop('position', None)
#         testcase_['npcList'][_i]['start']['heading'].pop('ref_point', None)
#         _offset_s = testcase_['npcList'][_i]['start']['lane_position']['offset']
#         _lane_name_s = testcase_['npcList'][_i]['start']['lane_position']['lane']
#         testcase_['npcList'][_i]['start']['lane_position']['offset'] = float(np.clip(_offset_s, offset_offset, lane_config[_lane_name_s] - offset_offset))
#         testcase_['npcList'][_i]['start']['heading']['ref_lane_point'] = testcase_['npcList'][_i]['start']['lane_position']
#         if testcase_['npcList'][_i]['destination'] is not None:
#             testcase_['npcList'][_i]['destination'].pop('position', None)
#             testcase_['npcList'][_i]['destination']['heading'].pop('ref_point', None)
#             _offset_s = testcase_['npcList'][_i]['destination']['lane_position']['offset']
#             _lane_name_s = testcase_['npcList'][_i]['destination']['lane_position']['lane']
#             testcase_['npcList'][_i]['destination']['lane_position']['offset'] = float(np.clip(_offset_s, offset_offset, lane_config[_lane_name_s] - offset_offset))
#             testcase_['npcList'][_i]['destination']['heading']['ref_lane_point'] = testcase_['npcList'][_i]['destination']['lane_position']
#         for _j in range(len(testcase_['npcList'][_i]['motion'])):
#             testcase_['npcList'][_i]['motion'][_j].pop('position', None)
#             testcase_['npcList'][_i]['motion'][_j]['heading'].pop('ref_point', None)
#             _offset_s = testcase_['npcList'][_i]['motion'][_j]['lane_position']['offset']
#             _lane_name_s = testcase_['npcList'][_i]['motion'][_j]['lane_position']['lane']
#             testcase_['npcList'][_i]['motion'][_j]['lane_position']['offset'] = float(np.clip(_offset_s, offset_offset, lane_config[_lane_name_s] - offset_offset))
#             testcase_['npcList'][_i]['motion'][_j]['heading']['ref_lane_point'] = testcase_['npcList'][_i]['motion'][_j]['lane_position']

#     return testcase_


'''
{'ScenarioName': 'scenario0', 
'MapVariable': 'map', 
'map': 'san_francisco_roadonly', 
'ego': {'ID': 'ego_vehicle', 'name': 'lidar_only', 'color': [0, 0, 0], 
        'start': {'heading': {'ref_point': {'x': 553090.0522572036, 'y': 4182687.8, 'z': 10.1246}, 'ref_angle': 0, 'ref_lane_point': {'lane': 'lane_780', 'offset': 50.659846368510046}}, 
                    'speed': 0.9746172672711946, 
                    'lane_position': {'lane': 'lane_780', 'offset': 101.7363211004984}}, 
        'destination': {'heading': {'ref_point': {'x': 552898.9957, 'y': 4182687.8989561526, 'z': 10.124655723571777}, 'ref_angle': 0, 'ref_lane_point': {'lane': 'lane_40', 'offset': 55.667100099773435}}, 
                    'speed': 0, 
                    'lane_position': {'lane': 'lane_40', 'offset': 55.667100099773435}}}, 
        'npcList': [
                    {'ID': 'npc1', 'name': 'Sedan', 'color': None, 
                            'start': {'lane_position': {'lane': 'lane_39', 'offset': 50, 'roadID': None}, 'heading': {'ref_point': {'x': 553090.0522572036, 'y': 4182687.8, 'z': 10.1246}, 'ref_angle': 10, 'ref_lane_point': {'lane': 'lane_780', 'offset': 50.659846368510046}}, 'speed': 1}, 
                            'motion': [], 
                            'destination': None}, 
                     {'ID': 'npc2', 'name': 'SUV', 'color': None, 
                            'start': {'lane_position': {'lane': 'lane_38', 'offset': 0, 'roadID': None}, 'heading': {'ref_point': {'x': 553090.0522572036, 'y': 4182687.8, 'z': 10.1246}, 'ref_angle': 50, 'ref_lane_point': {'lane': 'lane_780', 'offset': 50.659846368510046}}, 'speed': 2}, 
                            'motion': [{'lane_position': {'lane': 'lane_755', 'offset': 0, 'roadID': None}, 'heading': {'ref_lane_point': {'lane': 'lane_755', 'offset': 0, 'roadID': None}, 'ref_angle': 0, 'ref_point': {'x': 553013.5759388442, 'y': 4182683.829345557, 'z': 0}}, 'speed': 0}, 
                                        {'lane_position': {'lane': 'lane_41', 'offset': 0, 'roadID': None}, 'heading': {'ref_lane_point': {'lane': 'lane_41', 'offset': 0, 'roadID': None}, 'ref_angle': 0, 'ref_point': {'x': 552949.4718281265, 'y': 4182683.7929838626, 'z': 0}}, 'speed': 0}], 
                            'destination': {'lane_position': {'lane': 'lane_41', 'offset': 50, 'roadID': None}, 'heading': {'ref_lane_point': {'lane': 'lane_41', 'offset': 50, 'roadID': None}, 'ref_angle': 0, 'ref_point': {'x': 552899.4718530587, 'y': 4182683.7430518474, 'z': 0}}, 'speed': 0}}, 
                    {'ID': 'npc3', 'name': 'Sedan', 'color': None, 
                            'start': {'lane_position': {'lane': 'lane_779', 'offset': 0, 'roadID': None}, 'heading': {'ref_point': {'x': 553090.0522572036, 'y': 4182687.8, 'z': 10.1246}, 'ref_angle': 140, 'ref_lane_point': {'lane': 'lane_780', 'offset': 50.659846368510046}}, 'speed': 0}, 
                            'motion': [], 
                            'destination': None}
                    ], 
        'pedestrianList': [
                            {'name': 'Bob', 'ID': 'people', 
                            'start': {'position': {(x, y, z), 'heading': {'ref_point': {'x': 2, 'y': 3, 'z': 4}, 'ref_angle': 0, 'ref_lane_point': {'lane': 356, 'offset': 0}}, 'speed': 0},  
                            'motion': [], 
                            'destination': {}, 'height': None, 'color': None}, 
                            {'name': 'Bob', 'ID': 'people1', 
                            'start': {'lane_position': {'lane': 'lane_780', 'offset': 50}, 'heading': {'ref_point': {'x': 2, 'y': 3, 'z': 4}, 'ref_angle': 0}, 'speed': 0}, 
                            'motion': [], 
                            'destination': {'heading': {'ref_point': {'x': 1, 'y': 2, 'z': 3}, 'ref_angle': 0, 'ref_lane_point': {'lane': 23, 'offset': 0}}, 'speed': 0, 'lane_position': {'lane': 'lane_12', 'offset': 12}}, 
                            'height': None, 'color': None}
                            ], 
        'obstacleList': [], 'AgentNames': ['npc1', 'npc2', 'npc3']}
'''


'''
  {'speed': 
            [400.0, 55.667100099773435, 
             [11.012682245003893], 
             [20.0, 6.444461414542243, 2.215821721182575, 8.342062632705845], 
             [13.216840566429106], 
             [0], 
             [0, 0]], 
    'offset': [0.0, 0, 
               [400.0], 
               [4.170922361416934, 4.889163357483504, 9.72207030083321, 400.0], 
               [17.176542855666547], 
               [50], 
               [50, 12]]}  
'''


def testcase_encode(testcase):
    chrm_time = [testcase['time']['hour'], testcase['time']['minute']]
    chrm_weather = []
    for key in weather_list:
        chrm_weather.append((testcase['weather'][key]))
    chrm_v_type = []
    chrm_p_type = []
    chrm = {'speed': [], 'offset': []}
    ego_config = testcase['ego']
    chrm['offset'] = [[ego_config['start']['lane_position']['offset']]]
    chrm_ped = {'position': [], 'speed': []}

    # npc list config encode
    _npc_number = len(testcase['npcList'])
    for _i in range(_npc_number):
        _npc_chrm_offset, _npc_chrm_speed = [], []
        _npc_i = testcase['npcList'][_i]
        _npc_chrm_offset.append(_npc_i['start']['lane_position']['offset'])
        _npc_chrm_speed.append(_npc_i['start']['speed'])
        for _j in range(len(_npc_i['motion'])):
            wp_j = _npc_i['motion'][_j]
            _offset = wp_j['lane_position']['offset']
            _speed = wp_j['speed']
            _npc_chrm_offset.append(_offset)
            _npc_chrm_speed.append(_speed)
        if _npc_i['destination'] is not None:
            _npc_chrm_offset.append(_npc_i['destination']['lane_position']['offset'])
        chrm['speed'].append(_npc_chrm_speed)
        chrm['offset'].append(_npc_chrm_offset)
        chrm_v_type.append(_npc_i['name'])

    # pedestrian list config encode
    for _i in range(len(testcase['pedestrianList'])):
        _ped_i = testcase['pedestrianList'][_i]
        _ped_init_position = _ped_i['start']['position']
        _ped_init_speed = _ped_i['start']['speed']
        chrm_ped['position'].append((_ped_init_position['x'], _ped_init_position['y']))
        chrm_ped['speed'].append(_ped_init_speed)
        for _j in range(len(_ped_i['motion'])):
            wp_j = _ped_i['motion'][_j]
            chrm_ped['position'].append((wp_j['position']['x'], wp_j['position']['y']))
            chrm_ped['speed'].append(wp_j['speed'])
        if _ped_i['destination'] is not None:
            chrm_ped['position'].append(_ped_i['destination']['position']['x'], _ped_i['destination']['position']['y'])
        chrm_p_type.append(_ped_i['name'])

    return [chrm, chrm_time, chrm_weather, chrm_v_type, chrm_p_type, chrm_ped]


class EncodedTestCase:
    def __init__(self, trace, spec, weather):
        # self.trace = trace.pop('trace')
        # _result = copy.deepcopy(trace)
        # self.trace = Trace(_result)
        # _result.pop('trace')
        self.trace = copy.deepcopy(trace)
        # trace.pop('trace')
        # self.testcase = get_testcase(trace)
        # self.chromosome = testcase_encode(self.testcase)
        self.spec = spec
        self.robustness = []
        self.fitness = float('inf')
        self.muti_fitness = dict()
        self.weather = weather
        self.compute_fitness()

    def compute_fitness(self):
        # agents = self.testcase['AgentNames']
        # # agents = ['npc1']
        # processed_trace = Trace(self.trace, agents)
        if self.spec != {}:
            monitor = Monitor(self.trace, self.spec, self.weather)
            self.fitness = monitor.continuous_monitor()

    def compute_muti_fitness(self):
            monitor = Monitor(self.trace, self.spec, self.weather)
            self.muti_fitness = monitor.continuous_monitor_for_muti_traffic_rules()
            print(self.muti_fitness)
            
            # self.fitness = monitor.continuous_monitor()
            # self.fitness = monitor.discrete_monitor()

    # def to_json(self):
    #     return json.dumps(self, indent=4, default=lambda o: o.__dict__)


class list2d_convert:
    def __init__(self, list_2d):
        self.list2d = list_2d
        self.list1d = []
        self.len_list = []
        self.len = 0
        self.to_1d()
        self.len_compute()

    def to_1d(self):
        self.list1d = list(chain.from_iterable(self.list2d))
        self.len = len(self.list1d)

    def len_compute(self):
        for _i in range(len(self.list2d)):
            element_len = len(self.list2d[_i])
            self.len_list.append(element_len)

    def to_2d(self):
        _it = iter(self.list1d)
        return [list(islice(_it, i)) for i in self.len_list]


# class GAGeneration:
#     def __init__(self, population_para, crossover_prob=1.0, mutation_prob=1.0):
#         self.population = copy.deepcopy(population_para) # a list of EncodedTestCase
#         self.p_cross = crossover_prob
#         self.p_mutation = mutation_prob
#         self.population_size = len(self.population)

#     def selection(self, pop_size):
#         selected_population = []
#         sorted_pop = sorted(self.population, key=operator.attrgetter('fitness'), reverse=False)
#         for i in range(pop_size):
#             first_int = random.sample(range(0, math.ceil(self.population_size/2)), 1)[0]
#             second_int = random.sample(range(0, self.population_size), 1)[0]
#             # two_int = random.sample(range(0, self.population_size), 2)
#             # p1 = copy.deepcopy(self.population[two_int[0]])
#             # p2 = copy.deepcopy(self.population[two_int[1]])
#             p1 = copy.deepcopy(sorted_pop[first_int])
#             p2 = copy.deepcopy(sorted_pop[second_int])
#             if p1.fitness < p2.fitness:
#                 selected_population.append(p1)
#             else:
#                 selected_population.append(p2)
#             del p1, p2
#             gc.collect()
#         return selected_population


#     def selection2(self, pop_size):
#         selected_population = []
#         sorted_pop = sorted(self.population, key=operator.attrgetter('fitness'), reverse=True)
#         for i in range(pop_size):
#             first_int = random.sample(range(0, math.ceil(self.population_size/2)), 1)[0]
#             second_int = random.sample(range(0, self.population_size), 1)[0]
#             # two_int = random.sample(range(0, self.population_size), 2)
#             # p1 = copy.deepcopy(self.population[two_int[0]])
#             # p2 = copy.deepcopy(self.population[two_int[1]])
#             p1 = copy.deepcopy(sorted_pop[first_int])
#             p2 = copy.deepcopy(sorted_pop[second_int])
#             if p1.fitness > p2.fitness:
#                 selected_population.append(p1)
#             else:
#                 selected_population.append(p2)
#             del p1, p2
#             gc.collect()
#         return selected_population

#     def crossover(self, p1, p2):
#         # crossover is only performed on speed for vehicles
#         new_p1 = copy.deepcopy(p1)
#         new_p2 = copy.deepcopy(p2)
#         chm1 = new_p1.chromosome[0]['speed']
#         chm2 = new_p2.chromosome[0]['speed']
#         if len(chm1):
#             chm1_convert = list2d_convert(chm1)
#             chm2_convert = list2d_convert(chm2)
#             cross_point = random.randint(1, chm1_convert.len)
#             temp = chm1_convert.list1d[0:cross_point]
#             chm1_convert.list1d[0:cross_point] = chm2_convert.list1d[0:cross_point]
#             chm2_convert.list1d[0:cross_point] = temp
#             new_p1.chromosome[0]['speed'] = chm1_convert.to_2d()
#             new_p2.chromosome[0]['speed'] = chm2_convert.to_2d()

#         # crossover is performed on speed
#         # chm1_p_x = new_p1.chromosome[5]['x']
#         # chm1_p_y = new_p1.chromosome[5]['y']
#         # chm2_p_x = new_p1.chromosome[5]['x']
#         # chm2_p_y = new_p1.chromosome[5]['y']
#         # cross_ped_position_point = random.randint(1, len(chm1_p_x))
#         # temp_x = chm1_p_x[0: cross_ped_position_point]
#         # chm1_p_x[0:cross_ped_position_point] = chm2_p_x[0: cross_ped_position_point]
#         # chm2_p_x[0:cross_ped_position_point] = temp_x
#         # temp_y = chm1_p_y[0: cross_ped_position_point]
#         # chm1_p_y[0:cross_ped_position_point] = chm2_p_y[0: cross_ped_position_point]
#         # chm2_p_y[0:cross_ped_position_point] = temp_y
#         try:
#             chm1_p_speed = new_p1.chromosome[5]['speed']
#             if len(chm1_p_speed):
#                 chm2_p_speed = new_p2.chromosome[5]['speed']
#                 cross_ped_speed_point = random.randint(1, len(chm1_p_speed))
#                 temp_speed = chm1_p_speed[0:cross_ped_speed_point]
#                 chm1_p_speed[0:cross_ped_speed_point] = chm2_p_speed[0:cross_ped_speed_point]
#                 chm2_p_speed[0:cross_ped_speed_point] = temp_speed
#                 new_p1.chromosome[5]['speed'] = chm1_p_speed
#                 new_p2.chromosome[5]['speed'] = chm2_p_speed
#         except ValueError:
#             print('checking')

#         # if not new_p1.testcase['ego']['groundTruthPerception']:
#         if True:
#             # time crossover
#             _chrm_time1 = new_p1.chromosome[1]
#             _chrm_time2 = new_p2.chromosome[1]
#             _time_point = random.randint(1, len(_chrm_time1))
#             _temp = _chrm_time1[0:_time_point]
#             _chrm_time1[0:_time_point] = _chrm_time2[0:_time_point]
#             _chrm_time2[0:_time_point] = _temp
#             new_p1.chromosome[1] = _chrm_time1
#             new_p2.chromosome[1] = _chrm_time2

#             # weather crossover
#             _chrm_weather1 = new_p1.chromosome[2]
#             _chrm_weather2 = new_p2.chromosome[2]
#             _weather_point = random.randint(1, len(_chrm_weather1))
#             _temp = _chrm_weather1[0:_weather_point]
#             _chrm_weather1[0:_weather_point] = _chrm_weather2[0:_weather_point]
#             _chrm_weather2[0:_weather_point] = _temp
#             new_p1.chromosome[2] = _chrm_weather1
#             new_p2.chromosome[2] = _chrm_weather2

#             # vehicle type
#             _chrm_v_type1 = new_p1.chromosome[3]
#             _chrm_v_type2 = new_p2.chromosome[3]
#             if len(_chrm_v_type1):
#                 _v_type_point = random.randint(1, len(_chrm_v_type1))
#                 _temp = _chrm_v_type1[0:_v_type_point]
#                 _chrm_v_type1[0:_v_type_point] = _chrm_v_type2[0:_v_type_point]
#                 _chrm_v_type2[0:_v_type_point] = _temp
#                 new_p1.chromosome[3] = _chrm_v_type1
#                 new_p2.chromosome[3] = _chrm_v_type2

#             # pedestrian type
#             _chrm_p_type1 = new_p1.chromosome[4]
#             _chrm_p_type2 = new_p2.chromosome[4]
#             if len(_chrm_p_type1):
#                 _p_type_point = random.randint(1, len(_chrm_p_type1))
#                 _temp = _chrm_p_type1[0:_p_type_point]
#                 _chrm_p_type1[0:_p_type_point] = _chrm_p_type2[0:_p_type_point]
#                 _chrm_p_type2[0:_p_type_point] = _temp
#                 new_p1.chromosome[4] = _chrm_p_type1
#                 new_p2.chromosome[4] = _chrm_p_type2
#         return new_p1, new_p2

#     def mutation(self, p, lane_config, crosswalk_config):
#         v_max = 20
#         v_min = 0.5
#         pv_max = 5
#         pv_min = 0.05
#         new_p = copy.deepcopy(p)
#         speed_element = list2d_convert(new_p.chromosome[0]['speed'])
#         offset_element = list2d_convert(new_p.chromosome[0]['offset'])
#         # mutate speed
#         for i in range(speed_element.len):
#             mutated_speed = gauss(speed_element.list1d[i], 1)
#             speed_element.list1d[i] = float(np.clip(mutated_speed, v_min, v_max))

#         #ego vehicle offset
#         _offset_count = 0
#         _ego_offsets = offset_element.list2d[0]
#         _ego = new_p.testcase['ego']
#         _ego_start_lane = _ego['start']['lane_position']['lane']
#         _ego_start_length = lane_config[_ego_start_lane]
#         mutated_start_offset = float(np.clip(gauss(_ego_offsets[0], 1), offset_offset, _ego_start_length - offset_offset))
#         offset_element.list1d[0] = mutated_start_offset
#         _offset_count += 1
#         # _ego_destination_lane = _ego['destination']['lane_position']['lane']
#         # if _ego_start_lane == _ego_destination_lane:
#         #     mutated_destination_offset = float(np.clip(gauss(_ego_offsets[1], 1), mutated_start_offset, _ego_start_length - offset_offset))
#         # else:
#         #     _ego_destination_length = lane_config[_ego_destination_lane]
#         #     mutated_destination_offset = float(np.clip(gauss(_ego_offsets[1], 1), offset_offset, _ego_destination_length - offset_offset))
#         # offset_element.list1d[_offset_count] = mutated_destination_offset
#         # _offset_count += 1

#         # npc offsets
#         no_npc = len(new_p.testcase['npcList'])
#         for index_npc in range(no_npc):
#             npc_offset = offset_element.list2d[index_npc+1]
#             npc = copy.deepcopy(new_p.testcase['npcList'][index_npc])
#             _npc_start_lane = npc['start']['lane_position']['lane']
#             _npc_start_length = lane_config[_npc_start_lane]
#             mutated_npc_started_offset = gauss(npc_offset[0], 1)
#             if _ego_start_lane == _npc_start_lane:
#                 _diff_dis = mutated_npc_started_offset - offset_element.list1d[0]
#                 if -8 <= _diff_dis <= 0:
#                     mutated_npc_started_offset = offset_element.list1d[0] - 8
#                 elif 0 <= _diff_dis <= 8:
#                     mutated_npc_started_offset = offset_element.list1d[0] + 8
#             # mutated_npc_started_offset = float(np.clip(mutated_npc_started_offset, offset_offset, _npc_start_length - offset_offset))
#             offset_element.list1d[_offset_count] = float(np.clip(mutated_npc_started_offset, offset_offset, _npc_start_length - offset_offset))
#             if _ego_start_lane == _npc_start_lane and np.abs(offset_element.list1d[_offset_count]-offset_element.list1d[0]) < 7.9:
#                 print("something is wrong.")
#             _offset_count += 1

#             current_lane = _npc_start_lane
#             current_length = _npc_start_length
#             for wp in range(len(npc['motion'])):
#                 wp_i = npc['motion'][wp]
#                 wp_lane = wp_i['lane_position']['lane']
#                 mutated_offset = gauss(npc_offset[1+wp], 1)
#                 if wp_lane == current_lane:
#                     mutated_offset = float(np.clip(mutated_offset, offset_element.list1d[_offset_count-1], current_length - offset_offset))
#                     offset_element.list1d[_offset_count] = mutated_offset
#                     _offset_count += 1
#                 else:
#                     current_lane = wp_lane
#                     current_length = lane_config[wp_lane]
#                     mutated_offset = float(np.clip(mutated_offset, offset_offset, current_length - offset_offset))
#                     offset_element.list1d[_offset_count] = mutated_offset
#                     _offset_count += 1
#             if npc['destination'] is not None:
#                 npc_destination_lane = npc['destination']['lane_position']['lane']
#                 mutated_offset = gauss(npc_offset[-1], 1)
#                 if npc_destination_lane == current_lane:
#                     mutated_offset = float(np.clip(mutated_offset, offset_element.list1d[_offset_count-1], current_length - offset_offset))
#                     offset_element.list1d[_offset_count] = mutated_offset
#                 else:
#                     npc_destination_length = lane_config[npc_destination_lane]
#                     mutated_offset = float(np.clip(mutated_offset, offset_offset, npc_destination_length - offset_offset))
#                     offset_element.list1d[_offset_count] = mutated_offset
#                 _offset_count += 1

#         new_p.chromosome[0]['speed'] = speed_element.to_2d()
#         new_p.chromosome[0]['offset'] = offset_element.to_2d()


#          # pedestrian
#         no_ped = len(new_p.testcase['pedestrianList'])
#         if no_ped:
#             _chrm_ped = new_p.chromosome[5]
#             position_value = _chrm_ped['position']
#             speed_value = _chrm_ped['speed']
#             new_chrm_ped = {'position': [], 'speed': []}
#             for _i in range(len(position_value)):
#                 _position = position_value[_i]
#                 _new_position = (gauss(_position[0], 1), gauss(_position[1], 1))
#                 new_chrm_ped['position'].append(_new_position)
#                 _mutated_speed = gauss(speed_value[_i], 1)
#                 new_chrm_ped['speed'].append(float(np.clip(_mutated_speed, pv_min, pv_max)))
#             _, new_chrm_ped['position'] = pedestrian_in_crosswalk(new_chrm_ped['position'], crosswalk_config)
#             new_p.chromosome[5] = copy.deepcopy(new_chrm_ped)

#         # if not new_p.testcase['ego']['groundTruthPerception']:
#         if True:
#             # mutate time
#             new_p.chromosome[1] = [random.randint(0, 23), random.randint(0, 59)]
#             # mutate weather
#             if len(new_p.chromosome[2]) != 3:
#                 print("wrong weather features.")
#             new_p.chromosome[2] = list(np.random.uniform(0, 1, len(new_p.chromosome[2])))
#             # mutate vehicle type
#             if no_npc:
#                 new_p.chromosome[3] = [vehicle_list[item] for item in np.random.randint(0, len(vehicle_list), len(new_p.chromosome[3]))]
#             # mutate pedestrian type
#             if no_ped:
#                 new_p.chromosome[4] = [pedestrian_list[item] for item in np.random.randint(0, len(pedestrian_list), len(new_p.chromosome[4]))]
#         return new_p

#     def one_generation(self):
#         # always keep the individual with the minimal fitness
#         map_name = self.population[0].testcase['map']
#         map_info = get_map_info(map_name)
#         lane_info = map_info.get_lane_config()
#         crosswalk_info = map_info.get_crosswalk_config()
#         sorted_pop = sorted(self.population, key=operator.attrgetter('fitness'), reverse=True)
#         try:
#             _top1_pop = copy.deepcopy(sorted_pop[-1])
#         except IndexError:
#             print(len(sorted_pop))
#         _new_population = [_top1_pop]
#         selected_pop = self.selection(self.population_size-1)  # only need to select n-1 individual and perform mutation.
#         for i in range(0, self.population_size - 1, 2):  # i = 0,2,4,...,n-3
#             if i + 1 <= self.population_size - 2:
#                 p1 = copy.deepcopy(selected_pop[i])
#                 p2 = copy.deepcopy(selected_pop[i+1])
#                 if random.random() < self.p_cross:
#                     p1, p2 = self.crossover(p1, p2)
#                 if random.random() < self.p_mutation:
#                     p1 = self.mutation(p1, lane_info, crosswalk_info)
#                 if random.random() < self.p_mutation:
#                     p2 = self.mutation(p2, lane_info, crosswalk_info)
#                 _new_population.append(p1)
#                 _new_population.append(p2)
#             else:
#                 new_p = copy.deepcopy(selected_pop[i])
#                 _new_population.append(new_p)

#         return _new_population


#     def one_generation_law_breaking(self, population_size):
#         # always keep the individual with the minimal fitness
#         map_name = self.population[0].testcase['map']
#         map_info = get_map_info(map_name)
#         lane_info = map_info.get_lane_config()
#         crosswalk_info = map_info.get_crosswalk_config()
#         sorted_pop = sorted(self.population, key=operator.attrgetter('fitness'), reverse=True)
#         try:
#             _top1_pop = copy.deepcopy(sorted_pop[-1])
#         except IndexError:
#             print(len(sorted_pop))
#         _new_population = [_top1_pop]
#         selected_pop = self.selection2(population_size-1)  # only need to select n-1 individual and perform mutation.
#         for i in range(0, population_size - 1, 2):  # i = 0,2,4,...,n-3
#             if i + 1 <= population_size - 2:
#                 p1 = copy.deepcopy(selected_pop[i])
#                 p2 = copy.deepcopy(selected_pop[i+1])
#                 if random.random() < self.p_cross:
#                     p1, p2 = self.crossover(p1, p2)
#                 if random.random() < self.p_mutation:
#                     p1 = self.mutation(p1, lane_info, crosswalk_info)
#                 if random.random() < self.p_mutation:
#                     p2 = self.mutation(p2, lane_info, crosswalk_info)
#                 _new_population.append(p1)
#                 _new_population.append(p2)
#             else:
#                 new_p = copy.deepcopy(selected_pop[i])
#                 _new_population.append(new_p)

#         return _new_population



#     def coverage_one_generation(self, coverage_population):
#         _new_population = []
#         map_name = self.population[0].testcase['map']
#         map_info = get_map_info(map_name)
#         lane_info = map_info.get_lane_config()
#         crosswalk_info = map_info.get_crosswalk_config()
#         for i in range(0, len(coverage_population), 2):
#             if i + 1 <= self.population_size - 2:
#                 p1 = copy.deepcopy(coverage_population[i])
#                 p2 = copy.deepcopy(coverage_population[i + 1])
#                 if random.random() < self.p_cross:
#                     p1, p2 = self.crossover(p1, p2)
#                 if random.random() < self.p_mutation:
#                     p1 = self.mutation(p1, lane_info, crosswalk_info)
#                 if random.random() < self.p_mutation:
#                     p2 = self.mutation(p2, lane_info, crosswalk_info)
#                 _new_population.append(p1)
#                 _new_population.append(p2)
#             else:
#                 new_p = copy.deepcopy(coverage_population[i])
#                 _new_population.append(new_p)

#         return _new_population

# class DecodedTestCase:
#     def __init__(self, population_para):
#         self.population = copy.deepcopy(population_para)

#     def Decode_POP(self, p):
#         new_testcase = copy.deepcopy(p.testcase)

#         try:
#             new_testcase['time']['hour'] = p.chromosome[1][0]
#             new_testcase['time']['minute'] = p.chromosome[1][1]
#             _weather_index = 0
#             for key in weather_list:
#                 new_testcase['weather'][key] = p.chromosome[2][_weather_index]
#                 _weather_index += 1
#             # new_testcase['weather']['rain'] = p.chromosome[2][0]
#             # new_testcase['weather']['fog'] = p.chromosome[2][1]
#             # new_testcase['weather']['wetness'] = p.chromosome[2][2]
#         except IndexError:
#             print('Error!')

#         speed = p.chromosome[0]['speed']
#         offset = p.chromosome[0]['offset']
#         new_testcase['ego']['start']['lane_position']['offset'] = offset[0][0]
#         new_testcase['ego']['start']['heading']['ref_lane_point'] = new_testcase['ego']['start']['lane_position']
#         new_testcase['ego']['start']['heading']['ref_angle'] = 0.0

#         # decode NPCs
#         npc_no = len(new_testcase['npcList'])
#         ped_no = len(new_testcase['pedestrianList'])
#         v_type = copy.deepcopy(p.chromosome[3])
#         for i in range(npc_no):
#             try:
#                 new_testcase['npcList'][i]['name'] = copy.deepcopy(v_type.pop(0))
#             except IndexError:
#                 print("wrong vehicle type.")
#             agent_speed = speed[i]
#             agent_offset = offset[i+1]
#             new_testcase['npcList'][i]['start']['speed'] = agent_speed[0]
#             new_testcase['npcList'][i]['start']['lane_position']['offset'] = agent_offset[0]
#             new_testcase['npcList'][i]['start']['heading']['ref_lane_point'] = new_testcase['npcList'][i]['start']['lane_position']
#             new_testcase['npcList'][i]['start']['heading']['ref_angle'] = 0.0

#             for k in range(len(new_testcase['npcList'][i]['motion'])):
#                 new_testcase['npcList'][i]['motion'][k]['speed'] = agent_speed[1+k]
#                 new_testcase['npcList'][i]['motion'][k]['lane_position']['offset'] = agent_offset[1+k]
#                 new_testcase['npcList'][i]['motion'][k]['heading']['ref_lane_point'] = new_testcase['npcList'][i]['motion'][k]['lane_position']
#                 new_testcase['npcList'][i]['motion'][k]['heading']['ref_angle'] = 0.0
#             if new_testcase['npcList'][i]['destination'] is not None:
#                 new_testcase['npcList'][i]['destination']['speed'] = 0.0
#                 new_testcase['npcList'][i]['destination']['lane_position']['offset'] = agent_offset[-1]
#                 new_testcase['npcList'][i]['destination']['heading']['ref_lane_point'] = new_testcase['npcList'][i]['destination']['lane_position']
#                 new_testcase['npcList'][i]['destination']['heading']['ref_angle'] = 0.0

#         p_type = copy.deepcopy(p.chromosome[4])
#         ped_count = 0
#         position_value = copy.deepcopy(p.chromosome[5]['position'])
#         speed_value = copy.deepcopy(p.chromosome[5]['speed'])
#         for j in range(ped_no):
#             new_testcase['pedestrianList'][j]['name'] = p_type.pop(0)
#             new_testcase['pedestrianList'][j]['start']['position']['x'] = position_value[ped_count][0]
#             new_testcase['pedestrianList'][j]['start']['position']['y'] = position_value[ped_count][1]
#             new_testcase['pedestrianList'][j]['start']['speed'] = speed_value[ped_count]
#             ped_count += 1
#             for k in range(len(new_testcase['pedestrianList'][j]['motion'])):
#                 new_testcase['pedestrianList'][j]['motion'][k]['speed'] = speed_value[ped_count]
#                 new_testcase['pedestrianList'][j]['motion'][k]['position']['x'] = position_value[ped_count][0]
#                 new_testcase['pedestrianList'][j]['motion'][k]['position']['y'] = position_value[ped_count][1]
#                 ped_count += 1
#             if new_testcase['pedestrianList'][j]['destination'] is not None:
#                 new_testcase['pedestrianList'][j]['destination']['position']['x'] = position_value[ped_count][0]
#                 new_testcase['pedestrianList'][j]['destination']['position']['y'] = position_value[ped_count][1]
#                 new_testcase['pedestrianList'][j]['destination']['speed'] = 0.0
#                 ped_count += 1
#         return new_testcase

#     def decoding(self):
#         newTestCases = []
#         for i in range(len(self.population)):
#             _testcase = self.Decode_POP(self.population[i])
#             newTestCases.append(_testcase)
#         return newTestCases


# if __name__ == "__main__":

#     results = ['result1.json', 'result1.json','result1.json','result1.json']
#     population = []
#     for result in results:
#         with open(result) as f:
#             data = json.load(f)
#             scenario_in_trace = data['ScenarioName']
#             encoded_testcase = EncodedTestCase(data, {})
#             del encoded_testcase.trace
#             population.append(encoded_testcase)
#     new_population_obj = GAGeneration(population)
#     new_population = new_population_obj.one_generation()
#     decoder = DecodedTestCase(new_population)
#     new_testcases = decoder.decoding()
#     print(new_testcases)







