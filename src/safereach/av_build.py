import os
import pickle
import json
from .autonomous_vehicle.TracePreprocess import Trace, raw_to_lawbreaker_API
from .build_model import *
from .autonomous_vehicle.abstraction import AVAbstraction, traffic_rules

def av_build_model(abs, logs, model_path = "default_av.dtmc"): 
    model = build_model(logs, abs)
    store_model(model, model_path, abs)

LOG_F = 'safereach/autonomous_vehicle/Law38_0_2_record_1.00000.20250618131620.record.pickle'

law42 = traffic_rules["rule42"]
abs = AVAbstraction(law42)
with open(LOG_F, 'rb') as f:
    trace = pickle.load(f)["trace"] 
    time_seq = sorted(list(trace.keys()))
    initial_timestamp = time_seq[0]
       
    if len(trace.keys()) == 0:
        exit(0)
    logs = [[raw_to_lawbreaker_API(trace[t], initial_timestamp) for t in trace]]
    av_build_model(abs, logs)
    
    