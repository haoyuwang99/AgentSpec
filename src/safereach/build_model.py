
import json
import math
import numpy as np
from .embodied import abstraction 
from .embodied.abstraction import EmbodiedAbstraction
from .abstraction import FINISH
from collections import defaultdict
from fractions import Fraction
import pandas as pd 
import os
from typing import List, Any, Dict
from .abstraction import Abstraction
 
# Logs should be in the form of a list of observations, 
# from the observations we can abstract and get state 
# transition
def build_model(logs: List[List[Any]], abs:Abstraction):
    states = abs.state_space
    state_idx = abs.get_state_idx()
    state_interpret = abs.get_state_interpretation()
    K = len(abs.state_space)
    
    # Initialize count matrix
    transition_counts = np.zeros((K, K), dtype=int)
    
    for observations in logs:
        
        state_trans = []
        prev_state = None
        for observation in observations: 
            state_trans.append(abs.encode(observation)) 
            # if abs.encode(observation) == "10000110":
            #     print(observation)
        state_trans.append(FINISH)
        
        prev_state = None
        for state in state_trans: 
            if state not in state_idx:
                # print(abstraction.type_profile["Window"])
                # print(abstraction.type_profile["Cabinet"])
                print(state)
                print(abs.decode(state))
                raise Exception("unexpected state in the observation")
                continue  # Ignore states not in defined state space
            if prev_state is not None and prev_state in state_idx:
                i, j = state_idx[prev_state], state_idx[state]
                transition_counts[i, j] += 1
            prev_state = state

    # Apply Laplace smoothing over reachable transitions
    transition_probs: Dict[str, Dict[str, str]] = {}
    for i, s_from in enumerate(states):
        numerators = []
        denom = 0
        reachable = []
        
        for j, s_to in enumerate(states):
            if abs.can_reach(s_from, s_to):
                
                count = transition_counts[i, j]
                numerators.append((s_to, count + 1))  # Laplace: +1
                denom += count + 1
                reachable.append(j)

        transition_probs[s_from] = {
            s_to: str(Fraction(n, denom))
            for s_to, n in numerators
        }
   
    return {
        "states": states,
        "state_index": state_idx,
        "state_interpret": state_interpret,
        "transition_probs": transition_probs
    }
  
def store_model(model, dir, abstraction) :
    if not os.path.exists(dir):
        os.mkdir(dir)
    with open(dir + "model.json","w") as f:
        f.write(json.dumps(model))
    with open(dir + "abstraction.json", "w") as f:
        f.write(abstraction.to_json())
        
    export_dtmc_to_prism(model, file_path= dir + "dtmc.prism")
    
def export_dtmc_to_prism(model, file_path="dtmc.prism", initial_state=0):
    states = model['states']
    state_index = model['state_index']
    transitions = model['transition_probs']
    K = len(states)
    with open(file_path, 'w') as f: 

       # Write PRISM DTMC model header
        f.write("dtmc\n\n")
        f.write("module dtmc_model\n\n")
        f.write(f"    s : [0..{K - 1}] init {initial_state};\n\n")

        # Write transitions for each state
        for state in states:
            i = state_index[state]
            row = transitions[state]
            transition_list = []

            for target_state, prob in row.items():
                j = state_index[target_state]
                transition_list.append(f"{prob} : (s'={j})")

            if transition_list:
                f.write(f"    [] s={i} -> {' + '.join(transition_list)};\n")

        f.write("\nendmodule\n")

def embodied_build_model(dir, model_path): 
    print(dir)
    print(model_path)
    if not os.path.exists( dir + "/spec"):
        # os.system(f"mv {dir} samples/embodied_no_final_state")
        return
    logs = []
    for f in os.listdir(dir):
        if not f.endswith("json"):
            continue
        with open( dir + "/" + f) as f:
            obj = json.loads(f.read())
            log = [o["state"] for o in obj["s_trans"]]
            logs.append(log)

    
    specs = []
    with open(dir + "/spec") as f:
        specs = json.loads(f.read()) 
    print(specs)
    try: 
        # define abstraction level
        object_types = set()
        keys = set()
        recepatacles = set()
        for spec in specs:
            object_types.add(spec.get("objectType", ""))
            for key in spec:
                keys.add(key)
            for recep in spec.get("parentReceptacles", []):
                recepatacles.add(recep)
                
        keys.remove("objectType")
        if "parentReceptacles" in keys:
            keys.remove("parentReceptacles")
            
        abstraction = EmbodiedAbstraction(object_types, keys, recepatacles)
        model = build_model(logs, abstraction)
        print(model)
        store_model(model, model_path, abstraction)
    except Exception as e:
        raise e


LOG_DIR = 'safereach/embodied/samples/'
MODEL_DIR = 'safereach/embodied/dtmcs/'
log_dirs = [f for f in os.listdir(LOG_DIR) if f.startswith('log_raw_t')]
for dir in log_dirs : 
    # dir = 'log_raw_t20'
    model = MODEL_DIR + dir + "/"
    dir = LOG_DIR + dir + "/"
    print(dir)
    try: 
        embodied_build_model(dir, model) 
        # break
    except Exception as e:
        # raise e
        # continue
        print(e) 