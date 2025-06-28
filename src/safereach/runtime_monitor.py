import os
import json
import subprocess
import re
import time
from agentspec.agent import Action
from .abstraction import Abstraction
from .embodied.abstraction import EmbodiedAbstraction
from agentspec.rules.manual.embodied import rules as embodied_rules
from agentspec.interpreter import RuleInterpreter, RuleState

def load_abstraction(abstraction_desc_path, domain):
    
    if not os.path.exists(abstraction_desc_path):
        raise Exception(f"Invalid model director: {abstraction_desc_path}")
    abs = None
    with open(abstraction_desc_path) as f:
        obj = json.loads(f.read())
        if domain == "embodied":
            abs = EmbodiedAbstraction(obj["objectTypes"], obj["keys"], obj["parentReceptacles"])
        else :
            raise Exception("To be extended...")
    return abs

 
#returns true if intervention needed.  
def runtime_monitor(observation, dtmc_path, abs: Abstraction, unsafe_states, threshold=0.3, cache={}):  
    # print(cache)
    state_idx = abs.get_state_idx()

    # Step 1: Abstraction
    # t = time.time()
    current_state = abs.encode(observation)
    current_state = state_idx[current_state]
    # t = time.time() - t
    # print(f"abstract: {t * 1000:.2f} ms")

    # Step 2: Cache check
    cache_hit = (current_state, str(unsafe_states)) in cache
    if cache_hit:
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
    if len(unsafe_states)==1:
        unsafe_states = f"s={list(unsafe_states)[0]}"
    else :
        unsafe_states = "(" +  "|".join([f"s={s}" for s in unsafe_states]) + ")"
    # print(unsafe_states)

    pctl_formula = f"P=? [ F {unsafe_states} ]"
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


    

LOG_DIR = "safereach/embodied/samples"
MODEL_DIR = "safereach/embodied/dtmcs"
i = 0
for f in os.listdir(MODEL_DIR):
    if not os.path.exists(f"{MODEL_DIR}/{f}/abstraction.json"):
        continue
    if not os.path.exists(f"{MODEL_DIR}/{f}/dtmc.prism"):
        continue
    if not os.path.exists(f"{LOG_DIR}/{f}/spec"):
        continue
    logs = [ l for l in os.listdir(f"{LOG_DIR}/{f}") if l.endswith(".json")]
    if len(logs)== 0:
        continue
 
    abs = load_abstraction(f"{MODEL_DIR}/{f}/abstraction.json", "embodied")

    spec = {}
    with open(f"{LOG_DIR}/{f}/spec") as spec_file:
        spec = json.loads(spec_file.read())
    unsafe_states = abs.filter(spec)
    unsafe_states = [abs.get_state_idx()[state] for state in list(unsafe_states)]
    print(unsafe_states)
  
    if len(unsafe_states) == 0:
        print(f)
        continue
        # print(spec)
        # print(abs.object_types)
        # print(abs.keys)
        # print(abs.parentReceptacles)
        raise Exception("spec must identify at least 1 unsafe state")

    print(f)
    observations = []
    times = 0
    log_files = [ f"{LOG_DIR}/{f}/{o}" for o in os.listdir(f"{LOG_DIR}/{f}") if o.endswith("json")]
    reachability_cache = {}
    for log in log_files:
        with open(log) as log_file:
            log_obj = json.loads(log_file.read())
            if len(log_obj["s_trans"]) != len(log_obj["intermediate_steps"]):
                print("wtf?")
                continue 
            # use AgentSpec.
            after_enforce = []
            enforced = False
            # print(len(log_obj["intermediate_steps"])) 
            # for i in range(len( log_obj["intermediate_steps"])):
            #     print(i)
            #     interm = log_obj["intermediate_steps"][:i]
            #     cur_step = log_obj["intermediate_steps"][i]
            #     inp = cur_step["action"]["input"]
            #     event = inp[:inp.find(" ")]
            #     print(event)
            #     interm = [(step["action"], step["observation"]) for step in interm ]
            #     state = RuleState(action=Action(name="tool_input", input=inp, action=Action.get_skip()), intermediate_steps=interm)
            #     for rule in embodied_rules:
            #         if not rule.event == event:
            #             continue
            #         inter =  RuleInterpreter(rule = rule, rule_state = state)
            #         inter.verify_and_enforce(Action.get_skip())
            #         # print(inter.check)
            #         if inter.check:
            #             enforced = True
            #             after_enforce = interm
            #             # print(len(interm))
            #             break
            #     if enforced: 
            #         break
            # if not enforced:        
            #     after_enforce = log_obj["intermediate_steps"]
            # print(len(after_enforce))
                
            observations = [trans["state"] for trans in log_obj["s_trans"]]
            # before_steps= [json.dumps(step) for step in log_obj["intermediate_steps"]]
            # before_tokens = "".join(before_steps)
            # print(f"before: {before_tokens}")
            
            print(f"before violated: {any((abs.get_state_idx()[abs.encode(o)] in unsafe_states )for o in observations)}" )

            # intermediate_steps_after = []
            # for step in log_obj["intermediate_steps"]:
            #     inp = step["action"]
            #     event = step[:step.find(" ")]
                
            
            # after_tokens = "".join([ json.dumps(step) for step in after_enforce])
            # print(f"after: {after_tokens}")
            # print(f"after violated: {any((abs.encode(o) in unsafe_states) for o in observations[:len(after_enforce)])}" )
            # print("==========")
            
            # use SafeReach.
            # i = 0
            # observations = [trans["state"] for trans in log_obj["s_trans"]]
            # obs_after_mon = []
            # for observation in observations:
            #     obs_after_mon.append(observation)
            #     prob = runtime_monitor(observation, f"{MODEL_DIR}/{f}/dtmc.prism", abs, set(unsafe_states), cache=reachability_cache)
            #     # print(f"step_{i}: {prob}")
            #     if prob >= 0.05:
            #         break
            # before_steps= [json.dumps(step) for step in log_obj["intermediate_steps"]]
            # before_tokens = "".join(before_steps)
            # print(f"before: {before_tokens}")
            # print(f"before violated: {any((abs.get_state_idx()[abs.encode(o)] in unsafe_states )for o in observations)}" )

            # after_tokens = "".join([ json.dumps(step) for step in log_obj["intermediate_steps"][:len(obs_after_mon)]])
            # print(f"after: {after_tokens}")
            # print(f"after violated: {any((abs.encode(o) in unsafe_states) for o in obs_after_mon)}" )
            # print("==========")

    # break
    # for check overhead
    # reachability_cache = {}
    # t = time.time() * 1000
    # for observation in observations[:50]:

    #     state_num = len(abs.state_space)

    #     check = runtime_monitor(observation, f"{MODEL_DIR}/{f}/dtmc.prism", abs, unsafe_states, cache=reachability_cache) 
 
    # t = time.time() * 1000 - t
    # if len(observations)==0 :
    #     continue
    # print(f"states: {len(abs.state_space)}, total_time: {t/len(observations)}")


    print(i)