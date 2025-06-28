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


change_default = {
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
change_module = {
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
set_scenario = {
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
set_ego = {
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
reset_allmode = json.dumps(
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
mode_list = ["Planning", "Control", "Prediction"]
setup_mode = {
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
reset_sce = {
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
start_sce = {
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
start_record = {
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
dr = webdriver.Chrome()
dr.get('http://localhost:8888')
dr.find_element(By.XPATH, "//div[@class='dreamview-tabs-tab']/div[contains(text(), 'PNC Mode')]").click()
dr.find_element(By.CSS_SELECTOR, "div#rc-tabs-0-panel-Pnc input.dreamview-check-box-input").click()
dr.find_element(By.XPATH, "//div[@id='rc-tabs-0-panel-Pnc']//button[contains(@class, 'css-8vdc0a-enter-this-mode-btn')]").click()
dr.refresh()
  

def change_mode_fun( mode_name):
    msg = copy.deepcopy(change_default)
    msg["data"]["info"]["value"] = mode_name
    return msg

def change_module_fun(module_name):
    msg = copy.deepcopy(change_module)
    msg["data"]["info"]["value"] = module_name
    return msg     

def set_scenario_fun( name):
    msg = copy.deepcopy(set_scenario)
    msg["data"]["info"]["value"] = name
    return msg

def set_ego_fun(name):
    msg = copy.deepcopy(set_ego)
    msg["data"]["info"]["value"] = name
    return msg

def setup_mode_fun( name):
    msg = copy.deepcopy(setup_mode)
    msg["data"]["info"]["value"] = name
    return msg

def run(self, sce = "default", i = 0):
    cmd = "docker exec apollo_neo_dev_core rm -rf /home/sunsun/.apollo/resources/records/*"
    subprocess.run(cmd, shell=True, capture_output=True, text=True)
    ws_url = "ws://localhost:8888/websocket"
    ws = websocket.create_connection(ws_url)
    ws.send(json.dumps(change_mode_fun("Default")))
    time.sleep(1)
    ws.send(json.dumps(change_mode_fun("Pnc")))
    time.sleep(1)
    ws.send(json.dumps(change_module_fun("Scenario_Sim")))
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
    name.send_keys(f'sample_scene_{sce}_{i}')

    self.dr.find_element(By.CLASS_NAME, "ant-btn-primary").click()

def simulate():

    pass