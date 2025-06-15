import os
import json
import subprocess

def load_abstration(dir, domain):
    if not os.path.exists("model.json") or \
       not os.path.exists("dtmc.prism") or \
       not os.path.exists("abstraction.json")
        raise Exception("Invalid model director")
    abs = None
    with open(dir + "abstraction.json") as f:
        obj = json.loads(f.read())
        if domain == "embodied":
            abs = EmbodiedAbstraction(obj["objectTypes"], obj["keys"], obj["parentReceptacles"])
        else :
            raise Exception("To be extended...")
    return abs


# def reachability_prob(dir, cur_state, steps = 1):
#     model = dir + "/dtmc.prism"
#     with open(dir + "/state_meta.json") as f:
#         meta = json.loads(f)
#         unsafe_states = meta["unsafe"]

for f in os.listdir("dtmcs"):
    if not os.path.exists(f"dtmcs/{f}/state_meta.json"):
        continue
    if not os.path.exists(f"dtmcs/{f}/dtmc.prism"):
        continue
    
#returns true if intervention needed.  
def runtime_monitor(observation, model_path, abs: Abstraction, unsafe_spec, threshold=0.3, k_steps = 3):  
    abs.state_idx
    current_state = abs.encode(observation)
    
    unsafe_states = abs.filter(unsafe_spec)
    for unsafe_state in unsafe_states:
        pctl_formula = f""
            

    return False
    
    