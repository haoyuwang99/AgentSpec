import os
import json 

with open("ToolEmu/assets/rules.jsonl", 'r') as f:
    for l in f.readlines():
        obj = json.loads(l)
        name = obj["toolkits"].lower()
        print(name)
        prefix = f"rules/"
        os.system(f"mkdir {prefix}")
        
        with open(f"{prefix}{name}_predicates.py", 'a') as f:
            f.write("""
import re
import datetime
from typing import Dict
from util import llm_judge

""")
        for rule in obj["rules"]:
            with open(f"{prefix}{name}_rules.ar", 'a') as f:
                f.write(rule["rule"])
                f.write("\n\n")
            for pred_impl in rule["predicate_python_impl"]: 
                with open(f"{prefix}{name}_predicates.py", 'a') as f:
                    f.write("\n\n")
                    f.write(rule["predicate_python_impl"][pred_impl])
        