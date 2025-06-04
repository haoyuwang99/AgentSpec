# This script is to enumerate all the possible state for a given object description
import json
import math

keys_map = {
    "isToggled": "toggleable",
    "isCooked":"cookable",
    "isBroken": "breakable",
    "canFillWithLiquid": "isFilledWithLiquid",
    "isDirty": "dirtyable",
    "isUsedUp" : "canBeUsedUp",
    "isSliced": "sliceable",
    "isOpen": "openable",
    "isPickedUp":"pickupable",
}

def process_type_profile():

    with open("../../../benchmarks/SafeAgentBench/dataset/meta_data.json") as f:
        
        meta_data = json.loads(f.read())
        obj_types = meta_data["obj_types"]
        keyables = [keys_map[k] for k in keys_map]

        type_profiles = {}
        for type in obj_types:
            type_profile = {}
            for k in keyables:
                type_profile[k] = obj_types[type][k]
            type_profiles[type] = type_profile
        
        with open("../../../benchmarks/SafeAgentBench/dataset/meta_data1.json", 'w') as j:
            del meta_data["obj_types"]
            meta_data["type_profiles"] = type_profiles
            j.write(json.dumps(meta_data))
        exit(0)
# process_type_profile()
        
type_profile = {}
with open("../../../benchmarks/SafeAgentBench/dataset/meta_data1.json") as f:
    meta_data = json.loads(f.read())
    type_profile = meta_data["type_profiles"]

def encode(observation, object_types, keys, parentReceptacles):
    object_types = sorted(list(object_types))
    keys = sorted(list(keys))
    parentReceptacles = sorted(list(parentReceptacles))
    
    obj_type_to_index = {type: idx+1 for idx, type in enumerate(object_types)}
    ty_bit_len = math.ceil(math.log2(len(object_types))) + 1 
    
    rec_type_to_index = {type: idx+1 for idx, type in enumerate(parentReceptacles)}
    rec_bit_len = math.ceil(math.log2(len(parentReceptacles))) + 1
    
      # object type
    type = observation["objectType"]
    type_idx = obj_type_to_index[type]
    bitstr = format(type_idx, f'0{ty_bit_len}b')
    
    for key in keys:
        val = observation.get(key, False)
        bitstr += "1" if val else "0"
    
     # parent receptacle (as list)
    receptacles = observation.get("parentReceptacles", [])
    if len(receptacles) == 0:
        bitstr += format(0, f"0{rec_bit_len}b")
    else:
        receptacle = receptacles[0]
        bitstr += format(rec_type_to_index[receptacle], f"0{rec_bit_len}b")
    
    return bitstr

    
def decode(bitstr, object_types, keys, parentReceptacles):
    object_types = sorted(list(object_types))
    keys = sorted(list(keys))
    parentReceptacles = sorted(list(parentReceptacles))
     
    ty_bit_len = math.ceil(math.log2(len(object_types))) + 1 
    rec_bit_len = math.ceil(math.log2(len(parentReceptacles))) + 1
    idx = 0
    type_bits = bitstr[idx:idx+ty_bit_len]
    idx += ty_bit_len
    type_idx = int(type_bits, 2)
    obj_type = object_types[type_idx - 1]  # directly use the list
    observation = {"objectType": obj_type}

    # key states
    for key in keys:
        observation[key] = bitstr[idx] == "1"
        idx += 1

    # receptacle
    rec_bits = bitstr[idx:idx+rec_bit_len]
    rec_idx = int(rec_bits, 2)
    if rec_idx != 0:
        observation["parentReceptacles"] = [parentReceptacles[rec_idx - 1]]
    else:
        observation["parentReceptacles"] = []
    
    return observation

def enumerate_possible_states(object_types, keys, parentReceptacles):
    assert(len(object_types)>0)
    
    # ensure encoding/decoding consistency for the same input sets. 
    object_types = sorted(list(object_types))
    keys = sorted(list(keys))
    parentReceptacles = sorted(list(parentReceptacles))
    
    prefixes = [] 
    obj_type_to_index = {type: idx+1 for idx, type in enumerate(object_types)}
    ty_bit_len = math.ceil(math.log2(len(object_types))) + 1 
    
    
    rec_type_to_index = {type: idx+1 for idx, type in enumerate(parentReceptacles)}
    rec_bit_len = math.ceil(math.log2(len(parentReceptacles))) + 1

    #enumerate all the possible
    for type in object_types:
        type_bitstr = format(obj_type_to_index[type], f'0{ty_bit_len}b')
        prefixes.append(type_bitstr)
        
    
    # for each object type, enumerate its possible configuration
    for i in range(len(keys)):
        key = keys[i]
        n = len(prefixes)
        # enumerate all the possible state prefixes
        for j in range(n):
            prefix = prefixes.pop(0)
            type_bitstr = prefix[:ty_bit_len]
            type_idx = int(type_bitstr, 2) - 1
            type = object_types[type_idx]
            
            profile = type_profile[type]
            keyable = keys_map[key]
            
            prefix_0 = prefix + "0"
            prefixes.append(prefix_0)
            if profile[keyable]: 
                prefix_1 = prefix + "1"
                prefixes.append(prefix_1)    
    
    # add description that an object is in receptacles.
    n = len(prefixes)  
    for i in range(n):
        prefix = prefixes.pop(0)
                   
        type_bitstr = prefix[:ty_bit_len]
        type_idx = int(type_bitstr, 2) - 1
        type = object_types[type_idx]

        print(type)           
        profile = type_profile[type] 
        print(profile)
        no_receptacles = format(0, f"0{rec_bit_len}b")
        prefixes.append(prefix + no_receptacles)
        if profile["pickupable"]:
            for rec in parentReceptacles:
                re_idx = format(rec_type_to_index[rec], f'0{rec_bit_len}b')
                prefixes.append(prefix + re_idx)
                
    return prefixes


obj_types = ["Apple", "Window"]
keys = ["isPickedUp", "isSliced"]
receptacles =["Sink", "Sink2"]
state_space = enumerate_possible_states(obj_types, keys, receptacles)

for state in state_space:
    print(state)
    observation = decode(state, obj_types, keys, receptacles)
    print(observation)
    state =  encode(observation, obj_types, keys, receptacles)
    print(state)
    observation = decode(state, obj_types, keys, receptacles)
    print(observation)
    