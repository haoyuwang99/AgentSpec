# This script is to enumerate all the possible state for a given object description
import json
import math
from deepdiff import DeepDiff
from ..abstraction import Abstraction

keys_map = {
    "isToggled": "toggleable",
    "isCooked":"cookable",
    "isBroken": "breakable",
    "isFilledWithLiquid": "canFillWithLiquid",
    "isDirty": "dirtyable",
    "isUsedUp" : "canBeUsedUp",
    "isSliced": "sliceable",
    "isOpen": "openable",
    "isPickedUp":"pickupable",
}

class EmbodiedAbstraction():

    def __init__(self):
        pass

def process_type_profile():

    with open("meta_data.json") as f:
        
        meta_data = json.loads(f.read())
        obj_types = meta_data["obj_types"]
        keyables = [keys_map[k] for k in keys_map]

        type_profiles = {}
        for type in obj_types:
            type_profile = {}
            for k in keyables:
                type_profile[k] = obj_types[type][k]
            type_profiles[type] = type_profile
        
        with open("meta_data1.json", 'w') as j:
            del meta_data["obj_types"]
            meta_data["type_profiles"] = type_profiles
            j.write(json.dumps(meta_data))
        exit(0)
# process_type_profile()
        
type_profile = {}
with open("meta_data1.json") as f:
    meta_data = json.loads(f.read())
    type_profile = meta_data["type_profiles"]


def encode(observations, object_types, keys, parentReceptacles):
    # assert
    object_types = sorted(list(object_types))
    keys = sorted(list(keys))
    parentReceptacles = sorted(list(parentReceptacles))
    
    obj_type_to_index = {type: idx+1 for idx, type in enumerate(object_types)}
    ty_bit_len = math.ceil(math.log2(len(object_types))) + 1 
    
    rec_type_to_index = {type: idx+1 for idx, type in enumerate(parentReceptacles)}
    rec_bit_len = math.ceil(math.log2(len(parentReceptacles))) + 1
    bitstr=""
    for type in object_types: 
        type_idx = obj_type_to_index[type]
        bitstr = bitstr + format(type_idx, f'0{ty_bit_len}b')
            
        observations_by_type = [o for o in observations if o["objectType"] == type]
            
        for key in keys:
            val = any(o.get(key, False) for o in observations_by_type)
            bitstr += "1" if val else "0"
        
        has_rec = False
        for receptacle in parentReceptacles:
            if any(len(o["parentReceptacles"])>0 and \
                o["parentReceptacles"][0] == receptacle for o in observations_by_type):
                has_rec = True
                bitstr += format(rec_type_to_index[receptacle], f"0{rec_bit_len}b")
                break
        
        if not has_rec:
            bitstr += format(0, f"0{rec_bit_len}b")     
        
    return bitstr

    
def decode(bitstr, object_types, keys, parentReceptacles):
    object_types = sorted(list(object_types))
    keys = sorted(list(keys))
    parentReceptacles = sorted(list(parentReceptacles))
     
    ty_bit_len = math.ceil(math.log2(len(object_types))) + 1 
    rec_bit_len = math.ceil(math.log2(len(parentReceptacles))) + 1
    
    obj_len = ty_bit_len + len(keys) + rec_bit_len
    
    bitstrs = [bitstr[i:i+obj_len] for i in range(0, len(bitstr), obj_len)]

    
    observations = []
    for bitstr in bitstrs: 
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
        observations.append(observation)
    
    return observations

def enumerate_possible_states( object_types, keys, parentReceptacles):
    assert(len(object_types)>0)
    
    # ensure encoding/decoding consistency for the same input sets. 
    object_types = sorted(list(object_types))
    keys = sorted(list(keys))
    parentReceptacles = sorted(list(parentReceptacles))
    
    obj_type_to_index = {type: idx+1 for idx, type in enumerate(object_types)}
    ty_bit_len = math.ceil(math.log2(len(object_types))) + 1 
    
    prefixes = {}
    for object_type in object_types:
        prefixes[object_type] = [format(obj_type_to_index[object_type], f'0{ty_bit_len}b')]
    
    rec_type_to_index = {type: idx+1 for idx, type in enumerate(parentReceptacles)}
    rec_bit_len = math.ceil(math.log2(len(parentReceptacles))) + 1
    
    len_obj_state = ty_bit_len + rec_bit_len + len(keys)
    
    # for each object type, enumerate its possible configuration
    for object_type in object_types:
        for i in range(len(keys)):
            key = keys[i]
            n = len(prefixes[object_type])
            # enumerate all the possible state prefixes
            for j in range(n):
                prefix = prefixes[object_type].pop(0)
                type_bitstr = prefix[:ty_bit_len]
                type_idx = int(type_bitstr, 2) - 1
                type = object_types[type_idx]
                
                profile = type_profile[type]
                keyable = keys_map[key]
                
                prefix_0 = prefix + "0"
                prefixes[object_type].append(prefix_0)
                if profile[keyable]: 
                    prefix_1 = prefix + "1"
                    prefixes[object_type].append(prefix_1)     
    # add description that an object is in receptacles.
    for object_type in object_types:
        n = len(prefixes[object_type])   
        for i in range(n):
            prefix = prefixes[object_type].pop(0)
                    
            type_bitstr = prefix[:ty_bit_len]
            type_idx = int(type_bitstr, 2) - 1
            type = object_types[type_idx]
   
            profile = type_profile[type]  
            no_receptacles = format(0, f"0{rec_bit_len}b")
            prefixes[object_type].append(prefix + no_receptacles)
            if profile["pickupable"]:
                for rec in parentReceptacles:
                    re_idx = format(rec_type_to_index[rec], f'0{rec_bit_len}b')
                    prefixes[object_type].append(prefix + re_idx)

    values = list(prefixes.values())
    state_space = values[0] 
    for i in range(1, len(object_types)):
        n = len(state_space)
        for j in range(n):
            prefix = state_space.pop(0)
            for k in range(len(values[i])):
                state_space.append(prefix + values[i][k])
        
    return len_obj_state, prefixes, state_space

# check whether can reach from state 1 to state 2
def can_reach(bitstr1, bitstr2, object_types, keys, parentReceptacles):
    
    observation1 = decode(bitstr1, object_types, keys, parentReceptacles)
    observation2 = decode(bitstr2, object_types, keys, parentReceptacles)
    # observations are list of object state
    
    diff = DeepDiff(observation1, observation2, ignore_order=True)
    
     
    # we assume transitions are atomic, (i.e., the )
    if len(diff.keys()) > 1:
        return False
    
    # same state
    if len(diff) == 0 :
        return True
    
    # only one item can be added removed at a time
    if "iterable_item_added" in diff:
        return len(diff["iterable_item_added"]) == 1
    if "iterable_item_removed" in diff:
        return len(diff["iterable_item_removed"]) == 1
    
    if "values_changed" in diff and "['parentReceptacles'][0]" in diff["values_changed"]:
        return False
        
    if len(diff["values_changed"]) >1:
        return False
    
    key_o = list(diff["values_changed"].keys())[0]
    key = key_o[key_o.find("]")+1:] 
    diff["values_changed"][key] =  diff["values_changed"][key_o]
    del diff["values_changed"][key_o]
     
    if "['parentReceptacles'][0]" in diff["values_changed"]: 
        return False
    
    print(diff)
    
    # some property are not recoverable
    if any(f"['{x}']" in diff["values_changed"] and \
            diff["values_changed"][f"['{x}']"]["old_value"] and \
            not diff["values_changed"][f"['{x}']"]["new_value"]   
            for x in ["isBroken", "isSliced", "isCooked"]
            ): 
        return False
    
    return True
    

## below are tests

obj_types = ["Apple", "Window"]
keys = ["isPickedUp", "isSliced"]
receptacles =["Sink", "Sink2"]
len_obj_state, prefixes, state_space = enumerate_possible_states(obj_types, keys, receptacles)
# print(state_space)

can_reach(state_space[5], state_space[4], obj_types, keys, receptacles)

# for type in obj_types:
#     state_space = prefixes[type]
#     for state in state_space:
#         print("!!!!")
#         print(state)
#         observation = decode(state, obj_types, keys, receptacles)
#         print(observation)
#         state = encode(observation, obj_types, keys, receptacles)
#         print(state)
#         observation = decode(state, obj_types, keys, receptacles)
#         print(observation)
        
        
## for visuallization
import networkx as nx
import matplotlib.pyplot as plt

def find_absorbing_states(G):
    absorbing_states = [node for node in G.nodes if G.out_degree(node) == 0]
    return absorbing_states

def show_reachability_graph(state_space, object_types, keys, receptacles):
    G = nx.DiGraph()
    
    # Add all states as nodes
    for state in state_space:
        G.add_node(state)

    # Add edges based on reachability
    for i in range(len(state_space)):
        for j in range(len(state_space)): 
            s1, s2 = state_space[i], state_space[j]

            if can_reach(s1, s2, object_types, keys, receptacles):
                G.add_edge(s1, s2)
 
    print(f"Absorbing states: {find_absorbing_states(G)}")
    # Optional: Print summary
    print(f"Total states: {len(G.nodes)}")
    print(f"Reachable transitions: {len(G.edges)}")

    # Optional: Draw the graph (only for small graphs!)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=False, node_size=100, arrows=True)
    plt.title("State Transition Graph")
    plt.show()

show_reachability_graph(state_space, obj_types, keys, receptacles)