import json
import math
from .abstraction import *
from safereach.learn_dtmc import learn_dtmc
import pandas as pd 
import os
 
# The state is global (at the level of each scene, instead of each object)
def raw_log_to_state_transition(log, bitstrs):
    
    # for each step, convert the objects observation into bit str encoded state.  
    bitstr_transition = []
    for pair in log["s_trans"]:
        objects = pair["state"] 
        sorted_objects = sorted(objects, key=lambda obj: obj["name"])
        bitstr = encode()
            
        bitstrs.add(bitstr)
        bitstr_transition.append(bitstr) 
    return bitstr_transition, bitstrs

def export_dtmc_to_prism(df_P, K,  initial_state=0, file_path="learned_dtmc.prism"):
    with open(file_path, 'w') as f:
        K = len(df_P)

        # Write PRISM DTMC model header
        f.write("dtmc\n\n")
        f.write("module dtmc_model\n\n")
        f.write(f"    s : [0..{K-1}] init {initial_state};\n\n")

        # Write transitions for each state
        for i in range(K):
            row = df_P.iloc[i]
            nonzero_transitions = [(j, prob) for j, prob in enumerate(row)]

            if nonzero_transitions:
                transitions = " + ".join([f"{prob} : (s'={j})" for j, prob in nonzero_transitions])
                f.write(f"    [] s={i} -> {transitions};\n")

        f.write("\nendmodule\n")

def abstract_from_samples(dir): 
    # process input: spec to filter unsafe states 
    if not os.path.exists(dir + "/spec"):
        # os.system(f"mv {dir} samples/embodied_no_final_state")
        return
    specs = []
    with open(dir + "/spec") as f:
        specs = json.loads(f.read()) 
        
    #abstract state transition from logs
    bitstrs = set()
    bitstr_transitions = []
    for file in [f for f in os.listdir(dir) if f.endswith('json')]:
        with open(dir + "/" + file) as f:
            log = json.loads(f.read())
            bitstr_transition, bitstrs = raw_log_to_state_transition(log, bitstrs)
            bitstr_transitions.append(bitstr_transition)
        
    bitstrs = list(bitstrs)
    K = len(bitstrs) 
    
    bitstr_to_state = {elem: idx for idx, elem in enumerate(bitstrs)}
    state_to_bitstr = {idx: elem for idx, elem in enumerate(bitstrs)}
    state_transitions = [ [bitstr_to_state[bitstr] for bitstr in transition] for transition in bitstr_transitions ]
        
    # filter unsafe state by spec
    unsafe_bitstrs = set()
    init = True
    for spec in specs: 
        unsafe_bitstrs = filter(spec, bitstrs)
        states = map(lambda bitstr : bitstr_to_state[bitstr] ,unsafe_bitstrs) 
        if init: 
            unsafe_states = set(states)
            init = False
        else:
            unsafe_states = unsafe_states & set(states)
    spec_state = {
        "specs": specs,
        "states" : list(unsafe_states) 
    }
    # with open("spec_state.jsonl",'a') as f:
    #     f.write(json.dumps(spec_state )+"\n") 
    
    # when the sample do not reach state, 
    # assume an unsafe state = K, 
    # and assign prob to reach that state.
    if len(unsafe_states)==0:
        unsafe_states.add(K)
        K = K + 1
        
        
    # before smoothing, we need to filter out impossible transitions between states.
    
    
    alpha = 1.0
    counts, P_hat = learn_dtmc(state_transitions, K, alpha)
        
    

     
    df_counts = pd.DataFrame(counts, index=[f's{i}' for i in range(K)],
                            columns=[f's{j}' for j in range(K)])
    df_P = pd.DataFrame(P_hat, index=[f's{i}' for i in range(K)],
                        columns=[f's{j}' for j in range(K)])
  
    output_dir = "dtmcs/embodied/" + dir[dir.rfind("/"):] + "/"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        
    export_dtmc_to_prism(df_P, K, file_path=output_dir + "/dmtc.prism")
    
    state_meta = {
        "bitstr_to_state_idx" : bitstr_to_state,
        "specs": specs,
        "unsafe_states": list(unsafe_states)
    }

    with open(output_dir + "state_meta.json", 'w') as f:
        f.write(json.dumps(state_meta)) 


log_dir = [f for f in os.listdir('samples/embodied/') if f.startswith('log_raw_t')]
for d in log_dir:
    abstract_from_samples('samples/embodied/' + d) 
 