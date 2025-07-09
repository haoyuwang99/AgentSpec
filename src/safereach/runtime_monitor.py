import os
import json
import subprocess
import re
import time
from agentspec.agent import Action
from .abstraction import Abstraction
from .embodied.abstraction import EmbodiedAbstraction
from .autonomous_vehicle.abstraction import AVAbstraction

 
#returns true if intervention needed.  
def runtime_monitor(observation, dtmc_path, abs: Abstraction, unsafe_states, cache={}):  
    # print(cache)
    state_idx = abs.get_state_idx()

    # Step 1: Abstraction
    # t = time.time()
    current_state = abs.encode(observation)
    current_state = state_idx[current_state]
    # t = time.time() - t
    # print(f"abstract: {t * 1000:.2f} ms")

    # Step 2: Cache check
    # print(cache)
    cache_hit = (current_state, str(unsafe_states)) in cache
    # print((current_state, str(unsafe_states)))
    if cache_hit:
        # print("hit")
        return cache[(current_state, str(unsafe_states))]

    # print("cache: miss")
    
    # Step 3: Rewrite DTMC init state
    # t = time.time()
    with open(dtmc_path, 'r') as f:
        model_txt = f.read()

    updated_model = re.sub(
        r's\s*:\s*\[\d+\.\.\d+\]\s+init\s+\d+;',
        lambda m: re.sub(r'init\s+\d+', f'init {current_state}', m.group(0)),
        model_txt
    )

    with open(dtmc_path, 'w') as f:
        f.write(updated_model)
    # Step 4: Run PRISM to check the prob reaching unsafe state
    states = ""
    if len(unsafe_states)==1:
        state = f"s={list(unsafe_states)[0]}"
    else :
        state = "(" +  "|".join([f"s={s}" for s in unsafe_states]) + ")"
    # print(unsafe_states)

    pctl_formula = f"P=? [ F {state} ]"
    cmd = f"../prism/bin/prism {dtmc_path} -pf \"{pctl_formula}\""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    match = re.search(r"Result:\s*([0-9.]+)", result.stdout)
    if match:
        prob = float(match.group(1))
        cache[(current_state, str(unsafe_states))] = prob  # Save to cache
        return prob
        # if prob > threshold:
        #     return True
    else:
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError("Could not parse probability from PRISM output.")
