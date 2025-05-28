import json
import math
import dtmc

# objtypes = ["Apple", "CounterTop", "Book", "Bottle", "Shelf", "Bowl",
#             "Bread", "ButterKnife", "Cabinet", "CoffeeMachine", "CreditCard",
#             "Cup", "DishSponge", "Drawer", "Egg", "Fridge", "Faucet", "Floor",
#             "Fork", "GarbageCan", "HousePlant", "Kettle", "Knife", "Lettuce",
#             "LightSwitch", "Microwave", "Mug", "Pan", "PaperTowelRoll", "PepperShaker",
#             "Plate", "Pot", "Potato", "SaltShaker", "ShelvingUnit", "Sink", 
#             "SinkBasin", "SoapBottle", "Spatula", "Spoon", "Statue", "Stool", 
#             "StoveBurner", "StoveKnob", "Toaster", "Tomato", "Vase", "Window", "WineBottle", 
#             "W"]
with open("../benchmarks/SafeAgentBench/dataset/meta_data.json") as f:
    metadata = json.loads(f.read())
    objtypes = metadata["obj_types"]
    
ty_bit_len = math.ceil(math.log2(len(objtypes))) + 1
# print(len(objtypes))
# print(ty_bit_len)

# 0 for null
elem_to_index = {elem: idx+1 for idx, elem in enumerate(objtypes)}
index_to_elem = {idx+1: elem for idx, elem in enumerate(objtypes)}

state_keys = [ 
"isToggled",
"isBroken",
"isFilledWithLiquid",
"isDirty",
# "isUsedUp",
"isCooked",
# "isHeatSource",
# "isColdSource",
"isSliced",
"isOpen",
"isPickedUp",
# "isMoving"
]

# print(set(state_keys) - set(metadata["attributes"].keys()) )
# exit(0)
# def encode_obj_type(ty):


def encode_bitstr(obj):
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

def decode_bitstr(bit_str):
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


bitstrs = set()
        
# The state is global (at the level of each scene, instead of each object)
def raw_log_to_state_transition(log):
    
    # scene = log[]

    # for each step, convert the objects observation into bit str encoded state. 
    global bitstrs
    bitstr_transition = []
    for pair in log["s_trans"]:
        objects = pair["state"] 
        sorted_objects = sorted(objects, key=lambda obj: obj["name"])
        bitstr = ""
        for obj in sorted_objects:
            bitstr = bitstr + encode_bitstr(obj)
        bitstrs.add(bitstr)
        bitstr_transition.append(bitstr)
    # for obj_name in objects_transition:
    #     #sort the transition according to obj name.
    #     obj_transition = objects_transition[obj_name]
    #     bitstr_tran = []
    #     for obj_state in obj_transition:
    #         bitstr = encode_bitstr(obj_state)
    #         bitstr_tran.append(bitstr)
    #         bitstrs.add(bitstr)
    #     bitstr_transitions.append(bitstr_tran) 
    return bitstr_transition


bitstr_to_state = {}
state_to_bitstr = {}
 
transitions = []
for i in range(1, 2):
    with open(f"../dtmc/embodied/log_raw_t{i}.jsonl") as f:
        for l in f:
            log = json.loads(l)
            transitions.append(raw_log_to_state_transition(log))

print(len(transitions))
K = len(bitstrs)
print(transitions[:3])


bitstr_to_state = {elem: idx for idx, elem in enumerate(bitstrs)}
state_to_bitstr = {idx: elem for idx, elem in enumerate(bitstrs)}
state_transitions = [ [bitstr_to_state[bitstr] for bitstr in transition] for transition in transitions ]

alpha = 1.0

counts, P_hat = dtmc.learn_dtmc(state_transitions, K, alpha)
print(P_hat)

import pandas as pd
# Display counts and smoothed transition matrixlimit = 30
df_counts = pd.DataFrame(counts, index=[f's{i}' for i in range(K)],
                        columns=[f's{j}' for j in range(K)])
df_P = pd.DataFrame(P_hat, index=[f's{i}' for i in range(K)],
                    columns=[f's{j}' for j in range(K)])

    
with pd.ExcelWriter("dtmc_transition_data.xlsx", engine="xlsxwriter") as writer:
# Write counts to the first sheet
    df_counts.to_excel(writer, sheet_name="Raw Counts")
    
    # Write smoothed probabilities to the second sheet
    df_P.to_excel(writer, sheet_name="Smoothed Probabilities")


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
            # print(nonzero_transitions)
            if nonzero_transitions:
                transitions = " + ".join([f"{prob} : (s'={j})" for j, prob in nonzero_transitions])
                f.write(f"    [] s={i} -> {transitions};\n")

        f.write("\nendmodule\n")

export_dtmc_to_prism(df_P, K)

exit(0)
def display_dtmc(df_counts, df_P):
    
    limit = 10
    df_counts_subset = df_counts.iloc[:limit, :limit]
    df_P_subset = df_P.iloc[:limit, :limit]
    print("\nRaw transition counts:")
    print(df_counts_subset.to_string())

    print("\nSmoothed transition probabilities (α = 1):")
    print(df_P_subset.to_string())
    # print(len(transitions)) 
    block_size = 10
    num_blocks = (min(K, 30) + block_size - 1) // block_size  # adjust to show first 30 states only

    for i in range(num_blocks):
        for j in range(num_blocks):
            row_start = i * block_size
            col_start = j * block_size
            row_end = min((i + 1) * block_size, 30)
            col_end = min((j + 1) * block_size, 30)

            print(f"\nTransition counts block: rows s{row_start}-s{row_end-1}, cols s{col_start}-s{col_end-1}")
            print(df_counts.iloc[row_start:row_end, col_start:col_end].to_string())

            print(f"\nSmoothed probabilities block: rows s{row_start}-s{row_end-1}, cols s{col_start}-s{col_end-1}")
            print(df_P.iloc[row_start:row_end, col_start:col_end].round(3).to_string())
            
    off_diag_transitions = []

    for i in range(K):
        for j in range(K):
            if i != j and counts[i][j] > 0:
                off_diag_transitions.append((f's{i}', f's{j}', counts[i][j], P_hat[i][j]))

    # Convert to DataFrame for display
    import pandas as pd
    df_off_diag = pd.DataFrame(off_diag_transitions, columns=['from', 'to', 'count', 'smoothed_prob'])
    print(df_off_diag.head(100).to_string(index=False))

def display_state(state_idx):
    bitstr = state_to_bitstr.get(state_idx, None)
    if bitstr == None:
        print("No state")
    else:
        print(decode_bitstr(bitstr))

def monitor(cur_state, unsafe_spec, P_matrix):
    unsafe_states_bitstr = set()
    for bit_str in bitstrs:
        obj = decode_bitstr(bit_str)
        is_unsafe = True
        for key in unsafe_spec:
            if unsafe_spec[key] != obj[key]:
                is_unsafe = False
                break
        if not is_unsafe:
            continue
        unsafe_states_bitstr.add(bit_str)
    for bitstr in unsafe_states_bitstr:
        print(bit_str)
        print(decode_bitstr(bitstr))
    pass
    # 1. encode the unsafe state 
    
monitor("011010110111001000000000", {"objectType": "Pot"}, [])