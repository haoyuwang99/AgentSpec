import json
import math
from safereach.learn_dtmc import learn_dtmc
import pandas as pd 
import os

# objtypes = ["Apple", "CounterTop", "Book", "Bottle", "Shelf", "Bowl",
#             "Bread", "ButterKnife", "Cabinet", "CoffeeMachine", "CreditCard",
#             "Cup", "DishSponge", "Drawer", "Egg", "Fridge", "Faucet", "Floor",
#             "Fork", "GarbageCan", "HousePlant", "Kettle", "Knife", "Lettuce",
#             "LightSwitch", "Microwave", "Mug", "Pan", "PaperTowelRoll", "PepperShaker",
#             "Plate", "Pot", "Potato", "SaltShaker", "ShelvingUnit", "Sink", 
#             "SinkBasin", "SoapBottle", "Spatula", "Spoon", "Statue", "Stool", 
#             "StoveBurner", "StoveKnob", "Toaster", "Tomato", "Vase", "Window", "WineBottle", 
#             "W"]
with open("../../benchmarks/SafeAgentBench/dataset/meta_data.json") as f:
    metadata = json.loads(f.read())
    objtypes = metadata["obj_types"]
    
print(len(objtypes))
ty_bit_len = math.ceil(math.log2(len(objtypes))) + 1 

# 0 for null
elem_to_index = {elem: idx+1 for idx, elem in enumerate(objtypes)}
index_to_elem = {idx+1: elem for idx, elem in enumerate(objtypes)}


state_keys = [ 
"isToggled",
"isFilledWithLiquid",
"isDirty",
"isOpen",
"isPickedUp",
"isSliced",
"isBroken",
"isCooked", 
# "isUsedUp",
# "isHeatSource",
# "isColdSource",
# "isMoving"
]
# the last three is unrecoverable
 
object_str_len = 2* ty_bit_len + len(state_keys)

#RQ4 - different levels of abstraction:
# Option-1 we abstract one model for each scene, 
# Option-2 we abstract one model for all scenes. 

# we should make this be part of the framework.
# Abstraction strategy determines 
# (1) number of  encoding/decoding process of states.
# (2) possible transitions between states.
# the abstraction should be expressive enough for the spec
def embodied_state_abstraction(scene):
    
    # The state space is the set of all possible objects in the scene.
    # (1) the object types in the scene.
    # (2) the property defined by object type (e.g., Togglable = True -> isToggle = 0/1)
    def encoding(observation):
        pass

    # The impossible state transition includes those state which can
    # not be achieve by single action.
    # e.g. s1 -- fillLiquild bottle wine --> s2 -- pickup bottle --> s3
    # s1 --> s3 is not possible
    # Or some change which is not recoverable(i.e., isBroken/isCooked/isSliced from F to T)
    def decoding(observation):
        pass       
    
    pass

# This is scene-agnostic abstraction, which suffer from state exploision
# even if only the possible state are considered.
def embodied_encoding(obj):
    #object type
    bit_str = format(elem_to_index[obj["objectType"]], f'0{ty_bit_len}b')
    #parent receptacle
    parent = 0
    #assume one object only have one parent receptacle  
    if obj["parentReceptacles"] !=None :
        parent = obj["parentReceptacles"][0]
        parent = elem_to_index[parent[:parent.find("|")]] 
    bit_str = bit_str + format(parent, f'0{ty_bit_len}b')
    #boolean attributes
    for key in state_keys:
        if obj[key]: 
            bit_str = bit_str + "1" 
        else:
            bit_str = bit_str + "0" 
    return bit_str

def embodied_decoding(bit_str):
    obj_state = {}
    # Object type
    type_bits = bit_str[:ty_bit_len]
    type_id = int(type_bits, 2)
    ty = index_to_elem[type_id]
    obj_state["objectType"] = ty
    bit_str = bit_str[ty_bit_len:]
    # Parent Receptacles 
    type_bits = bit_str[:ty_bit_len]
    type_id = int(type_bits, 2)
    if type_id == 0:
        obj_state["parentReceptacles"] = None
    else :
        obj_state["parentReceptacles"] = [index_to_elem[type_id]]
    
    bit_str = bit_str[ty_bit_len:]
    #boolean attributes
    for i in range(0, len(state_keys)):
        bit = bit_str[0]
        bit_str = bit_str[1:]
        key = state_keys[i]
        value = False if bit == '0' else True
        obj_state[key] = value 
    return obj_state
        
# The state is global (at the level of each scene, instead of each object)
def raw_log_to_state_transition(log, bitstrs):
    
    # for each step, convert the objects observation into bit str encoded state.  
    bitstr_transition = []
    for pair in log["s_trans"]:
        objects = pair["state"] 
        sorted_objects = sorted(objects, key=lambda obj: obj["name"])
        bitstr = ""
        for obj in sorted_objects:
            bitstr = bitstr + embodied_encoding(obj)
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

    
def filter(unsafe_spec, bitstrs):
    unsafe_states_bitstr = set()
    for bit_str in bitstrs: 
        for obj_bitstr in [bit_str[i:i+object_str_len] for i in range(0, len(bit_str), object_str_len)]:
            obj = embodied_decoding(obj_bitstr)
            # states.append(obj)
            is_unsafe = True
            for key in unsafe_spec:
                is_unsafe = is_unsafe and unsafe_spec[key] == obj[key] 
            if is_unsafe:   
                break
        if is_unsafe:
            unsafe_states_bitstr.add(bit_str)
        # print(states)
    return unsafe_states_bitstr
 
    
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
    print(unsafe_states)
    with open(output_dir + "state_meta.json", 'w') as f:
        f.write(json.dumps(state_meta)) 


log_dir = [f for f in os.listdir('samples/embodied/') if f.startswith('log_raw_t')]
for d in log_dir:
    abstract_from_samples('samples/embodied/' + d) 

exit(0)
# def display_dtmc(df_counts, df_P, K):
    
#     limit = 10
#     df_counts_subset = df_counts.iloc[:limit, :limit]
#     df_P_subset = df_P.iloc[:limit, :limit]
#     print("\nRaw transition counts:")
#     print(df_counts_subset.to_string())

#     print("\nSmoothed transition probabilities (α = 1):")
#     print(df_P_subset.to_string())
#     # print(len(transitions)) 
#     block_size = 10
#     num_blocks = (min(K, 30) + block_size - 1) // block_size  # adjust to show first 30 states only

#     for i in range(num_blocks):
#         for j in range(num_blocks):
#             row_start = i * block_size
#             col_start = j * block_size
#             row_end = min((i + 1) * block_size, 30)
#             col_end = min((j + 1) * block_size, 30)

#             # print(f"\nTransition counts block: rows s{row_start}-s{row_end-1}, cols s{col_start}-s{col_end-1}")
#             # print(df_counts.iloc[row_start:row_end, col_start:col_end].to_string())

#             # print(f"\nSmoothed probabilities block: rows s{row_start}-s{row_end-1}, cols s{col_start}-s{col_end-1}")
#             # print(df_P.iloc[row_start:row_end, col_start:col_end].round(3).to_string())
            
#     off_diag_transitions = []

#     for i in range(K):
#         for j in range(K):
#             if i != j and counts[i][j] > 0:
#                 off_diag_transitions.append((f's{i}', f's{j}', counts[i][j], P_hat[i][j]))

#     # Convert to DataFrame for display
#     import pandas as pd
#     df_off_diag = pd.DataFrame(off_diag_transitions, columns=['from', 'to', 'count', 'smoothed_prob'])
#     print(df_off_diag.head(100).to_string(index=False))

# def display_state(state_idx, state_to_bitstr):
#     bitstr = state_to_bitstr.get(state_idx, None)
#     if bitstr == None:
#         print("No state")
#     else:
#         print(embodied_decoding(bitstr))

# monitor("011010110111001000000000", {"objectType": "Pot"}, [])