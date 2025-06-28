import os
import pickle
from cyber_record.record import Record
from lawbreak_sample import Mutation,_map # assuming your large script is saved as Mutation.py
from map_for_bridge import get_map_info
import json

# === Configuration ===
record_path = "/home/sunsun/Desktop/UserIntercation/Lawbreak/records/Law38_1_1_record_11.00000.20250617153237.record"
testcase_json = "/home/sunsun/Desktop/UserIntercation/Lawbreak/scenario_sets/65fbd4b2ec034cc74fa7728c/65fff1894d4e92f55da709c2.json"  # you must provide this
output_pickle = "Law38_2_2.pickle"

# === Setup ===
map_name = "sunnyvale"  # or infer from JSON
with open(testcase_json) as f:
    data = json.load(f)

map_info = get_map_info(map_name)
mutation = Mutation(data, map_name, map_info, set_name="Law38")

# === Inject the record ===
mutation.record = {}  # make sure record dict is initialized

# === Save messages from the record ===
for key in  _map:
    print(f"Processing topic: {key}")
    mutation.save_message(record_path, key)

# === Process all pose + chassis data ===
pose_list = sorted(mutation.record['pose'].keys())
chassis_list = sorted(mutation.record['chassis'].keys())

from tqdm import tqdm
for pose_key, chassis_key in tqdm(zip(pose_list, chassis_list), total=len(pose_list), desc="Processing trace"):
    mutation.process_pose(pose_key, chassis_key)

# === Process trace metadata (stuck, overtaking, etc.) ===
mutation.trace_time = sorted(mutation.trace.keys())
for i, key in enumerate(mutation.trace_time):
    mutation.check_stuck(key)
    mutation.check_is_lane_changing(i, key)
    mutation.check_is_overtaking(key)
    mutation.check_is_TurningAround(i, key)
    mutation.Find_Priority_NPCs_and_Peds(i, key)

# === Store result to pickle ===
mutation.result = {
    "testFailures": [],
    "trace": mutation.trace,
    "completed": True,
    "destinationReached": True,
    "groundTruthPerception": mutation.is_groundtruth,
    "AgentNames": mutation.agent
}

with open(output_pickle, 'wb') as f:
    pickle.dump(mutation.result, f)

print(f"Saved trace to {output_pickle}")

# === Run Lawbreak analysis ===
mutation.name = os.path.basename(record_path).replace(".record", "")
mutation.lawbreak()
