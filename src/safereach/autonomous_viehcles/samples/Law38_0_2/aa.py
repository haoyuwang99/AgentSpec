import pickle
import json
import pickle
import json
from shapely.geometry import Polygon

def serialize(obj):
    if isinstance(obj, Polygon):
        return list(obj.exterior.coords)
    elif isinstance(obj, set):
        return list(obj)
    elif hasattr(obj, '__dict__'):
        return obj.__dict__
    else:
        return str(obj)

def pickle_to_json(pickle_path, json_path):
    # Load pickle file
    with open(pickle_path, 'rb') as f:
        data = pickle.load(f)

    # Save as JSON with custom serializer
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4, default=serialize)

    print(f"Converted pickle to JSON and saved to {json_path}")

# Example usage
pickle_file = "/Users/haoyu/SMU/AgentSpec/src/safereach/autonomous_viehcles/samples/Law38_0_2/Law38_0_2_record_1_s.00000.20250618131620.record.pickle"
json_file = "example.json"
pickle_to_json(pickle_file, json_file)
