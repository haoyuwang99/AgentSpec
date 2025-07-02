
import json
import math
from deepdiff import DeepDiff
from ..abstraction import Abstraction, FINISH
from typing import Any, Set, List, Dict
import networkx as nx
import matplotlib.pyplot as plt

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

type_profile = {}
with open("safereach/embodied/meta_data1.json") as f:
    meta_data = json.loads(f.read())
    type_profile = meta_data["type_profiles"]
     
class EmbodiedAbstraction(Abstraction):

    def __init__(self, object_types: Set[str], keys: Set[str], parentReceptacles: Set[str]):
        self.object_types = sorted(list(object_types))
        self.keys = sorted(list(keys))
        self.parentReceptacles = sorted(list(parentReceptacles))
        self.type_profile = {}
        with open("safereach/embodied/meta_data1.json") as f:
            meta_data = json.loads(f.read())
            self.type_profile = meta_data["type_profiles"]
            
        
        self.obj_type_to_index = {type: idx+1 for idx, type in enumerate(object_types)}
        self.ty_bit_len = math.ceil(math.log2(len(object_types))) + 1 
        
        self.rec_type_to_index = {type: idx+1 for idx, type in enumerate(parentReceptacles)}
        if len(parentReceptacles)==0:
            self.rec_bit_len = 1
        else:
            self.rec_bit_len = math.ceil(math.log2(len(parentReceptacles))) + 1

        self.obj_len = self.ty_bit_len + len(self.keys) + self.rec_bit_len
        self.state_space=sorted(list(self.enumerate_possible_states()))
        self.state_idx = None
        self.state_interpretation = None
     
    def to_json(self): 
        obj = {
            "objectTypes" : self.object_types,
            "keys" : self.keys,
            "parentReceptacles": self.parentReceptacles,
        }
        return json.dumps(obj)

    def get_state_idx(self) -> Dict[str, int]:
        if self.state_idx == None:
            self.state_idx = {s:i for i, s in enumerate(self.state_space)}

        return self.state_idx

    def get_state_interpretation(self) -> Dict[str, Any]:
        if self.state_interpretation == None:
            self.state_interpretation = {s: self.decode(s) for s in self.state_space}
        return self.state_interpretation

    # def from_json(path) -> EmbodiedAbstraction:
    #     with open(path) as f:
    #         obj = json.loads(f.read())
    #         return EmbodiedAbstraction(set(obj["objectTypes"]), set(obj["keys"], set(obj["parentReceptacles"])))
     
    def encode(self, observation: Any) -> str:
        if observation == FINISH:
            return FINISH
        bitstr=""
        for type in self.object_types: 
            type_idx = self.obj_type_to_index[type]
            bitstr = bitstr + format(type_idx, f'0{self.ty_bit_len}b')
                
            observations_by_type = [obj for obj in observation if obj["objectType"] == type]
                
            for key in self.keys:
                val = any(o.get(key, False) for o in observations_by_type)
                bitstr += "1" if val else "0"
            
            has_rec = False
            for receptacle in self.parentReceptacles:
                if any(o["parentReceptacles"] !=None and len(o["parentReceptacles"])>0 and \
                    o["parentReceptacles"][0] == receptacle for o in observations_by_type):
                    has_rec = True
                    bitstr += format(self.rec_type_to_index[receptacle], f"0{self.rec_bit_len}b")
                    break
            
            if not has_rec:
                bitstr += format(0, f"0{self.rec_bit_len}b")     
            
        if not bitstr in self.state_space:
            raise Exception("unvalid state")
        return bitstr

 
    def decode(self, state: str) -> Any: 
        if state == FINISH:
            return FINISH
        bitstrs = [state[i:i+self.obj_len] for i in range(0, len(state), self.obj_len)] 
    
        observations = []
        for bitstr in bitstrs: 
            idx = 0
            type_bits = bitstr[idx:idx+self.ty_bit_len]
            idx += self.ty_bit_len
            type_idx = int(type_bits, 2)
            obj_type = self.object_types[type_idx - 1]  # directly use the list
            observation = {"objectType": obj_type}

            # key states
            for key in self.keys:
                observation[key] = bitstr[idx] == "1"
                idx += 1

            # receptacle
            rec_bits = bitstr[idx:idx+self.rec_bit_len]
            rec_idx = int(rec_bits, 2)
            if rec_idx != 0:
                observation["parentReceptacles"] = [self.parentReceptacles[rec_idx - 1]]
            else:
                observation["parentReceptacles"] = []
            observations.append(observation)
        
        return observations
    
    def enumerate_possible_states(self) -> Set[str]: 
        prefixes = {}
        for object_type in self.object_types:
            prefixes[object_type] = [format(self.obj_type_to_index[object_type], f'0{self.ty_bit_len}b')]
        
        # for each object type, enumerate its possible configuration
        for object_type in self.object_types:
            for i in range(len(self.keys)):
                key = self.keys[i]
                n = len(prefixes[object_type])
                # enumerate all the possible state prefixes
                for j in range(n):
                    prefix = prefixes[object_type].pop(0)
                    type_bitstr = prefix[:self.ty_bit_len]
                    type_idx = int(type_bitstr, 2) - 1
                    type = self.object_types[type_idx]
                    
                    profile = type_profile[type]
                    keyable = keys_map[key]
                    
                    prefix_0 = prefix + "0"
                    prefixes[object_type].append(prefix_0) 
                    if profile[keyable]: 
                        prefix_1 = prefix + "1"
                        prefixes[object_type].append(prefix_1)     
        # add description that an object is in receptacles.

        for object_type in self.object_types:
            n = len(prefixes[object_type])   
            for i in range(n):
                prefix = prefixes[object_type].pop(0)
                        
                type_bitstr = prefix[:self.ty_bit_len]
                type_idx = int(type_bitstr, 2) - 1
                type = self.object_types[type_idx]
    
                profile = type_profile[type]  
                no_receptacles = format(0, f"0{self.rec_bit_len}b")
                prefixes[object_type].append(prefix + no_receptacles) 
                if profile["pickupable"]:
                    for rec in self.parentReceptacles:
                        re_idx = format(self.rec_type_to_index[rec], f'0{self.rec_bit_len}b')
                        prefixes[object_type].append(prefix + re_idx)
        values = list(prefixes.values())
        state_space = values[0] 
        for i in range(1, len(self.object_types)):
            n = len(state_space)
            for _ in range(n):
                prefix = state_space.pop(0)
                for j in range(len(values[i])):
                    state_space.append(prefix + values[i][j])
        state_space.append(FINISH)
        return set(state_space)
    
    def filter(self, specs) -> Set[str]:

        init = True
        for spec in specs:
            filtered_states = set()
            for state in self.state_space: 
                if state == FINISH:
                    continue
                observations = self.decode(state)
                # return any of the observation is match 
                for o in observations:
                    match = True
                    for key in spec: 
                        match = match and spec[key] == o[key] 

                    if match:    
                        break
                if match:
                    filtered_states.add(state) 
            if init:
                init = False
                res = filtered_states
            else:
                res = res & filtered_states
        return res
 
    def can_reach(self, state1: str, state2: str) -> bool:
        if state2 == FINISH:
            return True
        if state1 == FINISH:
            return False
        observation1 = self.decode(state1)
        observation2 = self.decode(state2)
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
         
        
        # some property are not recoverable
        if any(f"['{x}']" in diff["values_changed"] and \
                diff["values_changed"][f"['{x}']"]["old_value"] and \
                not diff["values_changed"][f"['{x}']"]["new_value"]   
                for x in ["isBroken", "isSliced", "isCooked"]
                ): 
            return False
        
        return True
            
        
    def show_reachability_graph(self):
        state_space = list(self.enumerate_possible_states())
        G = nx.DiGraph()
        
        # Add all states as nodes
        for state in state_space:
            G.add_node(state)

        # Add edges based on reachability
        for i in range(len(state_space)):
            for j in range(len(state_space)): 
                s1, s2 = state_space[i], state_space[j]

                if self.can_reach(s1, s2):
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



def process_type_profile():

    with open("safereach/embodied/meta_data.json") as f:
        
        meta_data = json.loads(f.read())
        obj_types = meta_data["obj_types"]
        keyables = [keys_map[k] for k in keys_map]

        type_profiles = {}
        for type in obj_types:
            type_profile = {}
            for k in keyables:
                type_profile[k] = obj_types[type][k]
            type_profiles[type] = type_profile
        
        with open("safereach/embodied/meta_data1.json", 'w') as j:
            del meta_data["obj_types"]
            meta_data["type_profiles"] = type_profiles
            j.write(json.dumps(meta_data))
        
process_type_profile()
        

def find_absorbing_states(G):
    absorbing_states = [node for node in G.nodes if G.out_degree(node) == 0]
    return absorbing_states