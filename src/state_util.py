import json
import math
import demo

objtypes = []
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
        
# with open("embodied_log.jsonl", 'r') as f:
#     for l in f:
#         obj = json.loads(l)
#         initial_states = obj["s0"]
#         for obj in initial_states:
#             # print(type(obj))
#             # print(obj) 
#             print(decode_bitstr(encode_bitstr(obj)))
            
#         break

def raw_log_to_state_transition(log):
    # 1. seperate state transition for each object
    objects_transition = {}
    init = True
    i = 0
    for pair in log["trans"]:
        i = i+1
        state_prime = pair["state_prime"]
        try: 
            if init: 
                for obj in state_prime:
                    objects_transition[obj["name"]] = [obj]
                init = False
            else:
                for obj in state_prime:
                    objects_transition[obj["name"]].append(obj)
        except Exception as e:
            continue
    
    # 2. for each object, convert to a bitstr transition. 
    global bitstrs
    bitstr_transitions = []
    for obj_name in objects_transition:
        obj_transition = objects_transition[obj_name]
        bitstr_tran = []
        for obj_state in obj_transition:
            bitstr = encode_bitstr(obj_state)
            bitstr_tran.append(bitstr)
            bitstrs.add(bitstr)
        bitstr_transitions.append(bitstr_tran)

     
    return bitstr_transitions
    
bitstr_to_state = {}
state_to_bitstr = {}

with open("embodied_log_raw.jsonl") as f:
    transitions = []
    print("!!!!")
    for l in f:
        log = json.loads(l)
        for transition in raw_log_to_state_transition(log):
            transitions.append(transition)
    # print("!!")
    print(len(transitions))
    K = len(bitstrs)
    print(transitions[:3])
    
    bitstr_to_state = {elem: idx for idx, elem in enumerate(bitstrs)}
    state_to_bitstr = {idx: elem for idx, elem in enumerate(bitstrs)}
    state_transitions = [ [bitstr_to_state[bitstr] for bitstr in transition] for transition in transitions ]
    # print(state_transitions[:5])
    # exit(0)
    alpha = 1.0

    counts, P_hat =  demo.learn_dtmc(state_transitions, K, alpha)
    
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

    # limit = 10
    # df_counts_subset = df_counts.iloc[:limit, :limit]
    # df_P_subset = df_P.iloc[:limit, :limit]
    # print("\nRaw transition counts:")
    # print(df_counts_subset.to_string())

    # print("\nSmoothed transition probabilities (α = 1):")
    # print(df_P_subset.round(3).to_string())
    # # print(len(transitions)) 
    # block_size = 10
    # num_blocks = (min(K, 30) + block_size - 1) // block_size  # adjust to show first 30 states only

    # for i in range(num_blocks):
    #     for j in range(num_blocks):
    #         row_start = i * block_size
    #         col_start = j * block_size
    #         row_end = min((i + 1) * block_size, 30)
    #         col_end = min((j + 1) * block_size, 30)

    #         print(f"\nTransition counts block: rows s{row_start}-s{row_end-1}, cols s{col_start}-s{col_end-1}")
    #         print(df_counts.iloc[row_start:row_end, col_start:col_end].to_string())

    #         print(f"\nSmoothed probabilities block: rows s{row_start}-s{row_end-1}, cols s{col_start}-s{col_end-1}")
    #         print(df_P.iloc[row_start:row_end, col_start:col_end].round(3).to_string())
            
    # off_diag_transitions = []

    # for i in range(K):
    #     for j in range(K):
    #         if i != j and counts[i][j] > 0:
    #             off_diag_transitions.append((f's{i}', f's{j}', counts[i][j], P_hat[i][j]))

    # # Convert to DataFrame for display
    # import pandas as pd
    # df_off_diag = pd.DataFrame(off_diag_transitions, columns=['from', 'to', 'count', 'smoothed_prob'])
    # print(df_off_diag.head(100).to_string(index=False))


