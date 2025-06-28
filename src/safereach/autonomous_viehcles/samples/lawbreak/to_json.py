from modules.common_msgs.map_msgs import map_pb2
from google.protobuf.json_format import MessageToDict
import json

with open("maps/sim_map.bin", 'rb') as f:
            binary_data = f.read()
            map_config = map_pb2.Map()
            map_config.ParseFromString(binary_data)
            json_str = MessageToDict(map_config)
            with open("maps/san.json", 'w') as f1:
                json.dump(json_str, f1)
