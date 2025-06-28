import websocket, json, copy

change_default = json.dumps(
    {
        "data":{
            "name":"",
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
)
change_pnc = json.dumps(
    {
        "data":{
            "name":"",
            "info":{
                "action":"CHANGE_MODE",
                "value":"Pnc"
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
change_module = json.dumps(
    {
        "action":"request",
        "data": {
            "info":{
                "action":"CHANGE_OPERATION",
                "value":"Scenario_Sim"
            },
            "name":"",
            "requestId":"HMIAction!",
            "source":"dreamview",
            "sourceType":"module",
            "target":"dreamview",
            "targetType":"dreamview"
        },
        "type":"HMIAction"
    }
)
reset_allmode = json.dumps(
    {
        "data":{
            "name":"",
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
setup_mode = {
        "data":{
            "name":"",
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
set_scenario = {
    "data":{
        "name":"",
        "info":{
            "action":"CHANGE_SCENARIO",
            "value":"65cdbb3ac7bbb125b913e429,65cdfb53c58396592ef9dd36"
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
        "name":"",
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

reset_sce = {
    "data":{
        "name":"",
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
        "name":"",
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
        "name":"",
        "source":"dreamview",
        "target":"dreamview",
        "sourceType":"module",
        "targetType":"dreamview",
        "requestId":"noResponse"
    },
    "type":"StartDataRecorder",
    "action":"request"
}
stop_record = {
    "data":{
        "name":"",
        "source":"dreamview",
        "target":"dreamview",
        "sourceType":"module",
        "targetType":"dreamview",
        "requestId":"noResponse"
    },
    "type":"StopDataRecorder",
    "action":"request"
}
save_record = {
    "data":{
        "name":"",
        "info":{
            "newName":"202402281450_MkzLgsvl321_Sunnyvale"
        },
        "source":"dreamview",
        "target":"dreamview",
        "sourceType":"module",
        "targetType":"dreamview",
        "requestId":"SaveDataRecorder!"
    },
    "type":"SaveDataRecorder",
    "action":"request"
}

def setup_mode_fun(mode, base_msg):
    msg = copy.deepcopy(base_msg)
    msg["data"]["info"]["value"] = mode
    return msg

def set_scenario_fun(name, base_msg):
    msg = copy.deepcopy(base_msg)
    msg["data"]["info"]["value"] = name
    return msg


ws_url = "ws://localhost:8888/websocket"
ws = websocket.create_connection(ws_url)
#ws.send(change_module)
ws.send(change_default)
ws.send(change_pnc)
ws.send(change_module)
set_name = "65cdbb3ac7bbb125b913e429"
scenario_name = ["65cdfb53c58396592ef9dd36"]
for _name in scenario_name:
    _name = set_name + "," + _name
    ws.send(json.dumps(set_scenario_fun(_name, set_scenario)))
ws.send(json.dumps(set_ego))

ws.send(reset_allmode)
mode_list = ["Planning", "Control", "Prediction"]
for _mode in mode_list:
    ws.send(json.dumps(setup_mode_fun(_mode, setup_mode)))
ws.send(json.dumps(reset_sce))
ws.send(json.dumps(start_sce))
ws.send(json.dumps(reset_sce))
ws.send(json.dumps(start_sce))
