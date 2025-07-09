import os
import json 
import pickle
from .autonomous_vehicle.abstraction import AVAbstraction
from .runtime_monitor import runtime_monitor
from .autonomous_vehicle.TracePreprocess import raw_to_lawbreaker_API

def eval_law():
    pass

def eval_reach():
    pass

def eval_crash(observation):
    return

def load_abstraction(abstraction_desc_path):
    with open(abstraction_desc_path) as f:
        obj = json.load(f)
        predicates = obj["predicates"]

    return AVAbstraction(predicates)


# collisioncase 
abs_path = "default_av.dtmcabstraction.json"
model_path = "/Users/haoyu/SMU/AgentSpec/src/default_av.dtmcmodel.json"
dtmc_path = "/Users/haoyu/SMU/AgentSpec/src/default_av.dtmcdtmc.prism"

LOG_DIR = "safereach/autonomous_vehicle/samples/Law38_1_1/"

abs = load_abstraction(abs_path)
unsafe_states = abs.filter()
unsafe_states = [abs.get_state_idx()[state] for state in list(unsafe_states)]

print(unsafe_states)
# exit(1)
for f in os.listdir(LOG_DIR):
    if not f.endswith("pickle"):
        continue
    with open(f"{LOG_DIR}{f}", 'rb') as pic:
        trace = pickle.load(pic)["trace"]

        time_seq = sorted(list(trace.keys()))
        if len(trace.keys()) == 0:
            continue
        initial_timestamp = time_seq[0]
        enforced_trace = []

        cache = {}
        for i in range(len(time_seq)):
            if i%100 == 0:
                print(i)
            step = trace[time_seq[i]]
            observation = raw_to_lawbreaker_API(step, initial_timestamp)
            # s_idx = abs.get_state_idx()[abs.encode(observation)]

            prob = runtime_monitor(observation, dtmc_path, abs, set(unsafe_states), cache = cache)
            # # print(prob)
            # if prob < 0.05:
            #     print(i)
                # print(len(trace))
        print(cache)
        exit(0)
# with open()