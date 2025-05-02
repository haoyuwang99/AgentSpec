objtypes = []

state_keys = [ 
"isToggled",
"isBroken",
"isFilledWithLiquid",
"isDirty",
"isUsedUp",
"isCooked",
"isHeatSource",
"isColdSource",
"isSliced",
"isOpen",
"isPickedUp",
"isMoving"
]    

# def encode_obj_type(ty):



def encode_state(obj):
    bit_str = 0
    for key in reversed(state_keys):
        if obj[key]: 
            bit_str = (bit_str << 1) + 1 
        else:
            bit_str = (bit_str << 1) + 0
    return bit_str

def decode_state(bit_str):
    obj_state = {}
    for i in range(0, len(state_keys)):
        key = state_keys[i]
        value = False if bit_str % 2 ==0 else True
        obj_state[key] = value
        bit_str = bit_str >> 1
    return obj_state
        