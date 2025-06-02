import os
import json

def reachability_prob(dir, cur_state, steps = 1):
    model = dir + "/dtmc.prism"
    with open(dir + "/state_meta.json") as f:
        meta = json.loads(f)
        unsafe_states = meta["unsafe"]

for f in os.listdir("dtmcs"):
    if not os.path.exists(f"dtmcs/{f}/state_meta.json"):
        continue
    if not os.path.exists(f"dtmcs/{f}/dtmc.prism"):
        continue
    
    