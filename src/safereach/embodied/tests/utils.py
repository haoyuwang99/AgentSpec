import os
import json
import argparse

def split_jsonl_to_json(jsonl_path, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    with open(jsonl_path, 'r', encoding='utf-8') as infile:
        for idx, line in enumerate(infile):
            try:
                data = json.loads(line)
                output_file = os.path.join(output_dir, f"{idx:05d}.json")
                with open(output_file, 'w', encoding='utf-8') as outfile:
                    json.dump(data, outfile, ensure_ascii=False, indent=2)
            except json.JSONDecodeError as e:
                print(f"Skipping line {idx} due to JSONDecodeError: {e}")

if __name__ == "__main__":
    import os

    # Get all files ending with .jsonl in current directory
    jsonl_files = [f for f in os.listdir('.') if f.endswith('.jsonl')]

    # Print the list
    # for file in jsonl_files:
    #     name = file[:-6] + "/"
    #     split_jsonl_to_json(file, name)

    for f in [f for f in os.listdir('.') if f.startswith('log_raw') ]:
        with open(f + "/00000.json") as log:
            log = json.load(log)
            if log["input"]["final_state"] != None:
                with open(f+"/spec", 'w') as f:
                    f.write(json.dumps( log["input"]["final_state"]))