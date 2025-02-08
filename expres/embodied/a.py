import json
with open("safe_controlled_records_1.jsonl") as f:
    for l in f:
        obj = json.loads(l)
        if obj["output"].find("action stopped by") == -1:
            with open("safe_controlled_records.jsonl",'a') as w:
                w.write(l)
        else:
            with open("rule_interferred_a.jsonl",'a') as w:
                w.write(l)