import os
import pickle
import json
from .autonomous_vehicle.TracePreprocess import Trace, raw_to_lawbreaker_API
from .build_model import *
from .autonomous_vehicle.abstraction import AVAbstraction, traffic_rules, parse_law

def av_build_model(abs, logs, model_path = "default_av.dtmc"): 
    model = build_model(logs, abs)
    store_model(model, model_path, abs)
    
rules_map = {
    "Law38_0_2": "rule38_1",
    "Law38_1_1": "rule38_1",
    
    "Law53_0_1" : "rule53"
}

LOG_F = 'safereach/autonomous_vehicle/Law38_0_2_record_1.00000.20250618131620.record.pickle'
SAMPLES = "safereach/autonomous_vehicle/samples/"
# SCENEARIO = "safereach/autonomous_vehicle/samples/Law38_1_1/"
for s in os.listdir(SAMPLES):
    SCENEARIO = f"{SAMPLES}{s}/" 
    
    law = traffic_rules[rules_map[s]]
    predicates = parse_law(law)
    abs = AVAbstraction(predicates)
    logs = []
    for f in os.listdir(SCENEARIO):
        if not f.endswith("pickle"):
            continue
        with open(f"{SCENEARIO}{f}", 'rb') as pic:
            trace = pickle.load(pic)["trace"] 
            time_seq = sorted(list(trace.keys()))
            initial_timestamp = time_seq[0]
            
            if len(trace.keys()) == 0:
                exit(0)
            logs.append([raw_to_lawbreaker_API(trace[t], initial_timestamp) for t in trace])
    av_build_model(abs, logs, model_path=f"safereach/autonomous_vehicle/dtmcs/{s}")

    