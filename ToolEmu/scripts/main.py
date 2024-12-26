
import argparse
import random

import argparse
import json
from dotenv import load_dotenv 
from toolemu.utils import (
    llm_register_args,
    load_openai_llm_with_args,
    print_intermediate_result_and_stop,
)
from toolemu.utils.my_typing import *

import argparse
import os
import random
import openai
import anthropic 
from dotenv import load_dotenv
from toolemu.agent_executor_builder import build_agent_executor 
from toolemu.tools import *
from toolemu.utils import (
    case_to_input_dict,
    filter_keys,
    get_toolkit_names,
    llm_register_args,
    load_openai_llm,
    replace_agent_action_with_list,
)

TEST_CASES_PATH = "../assets/all_cases.json"

ROLES = ["agent", "simulator"]

def generate_traj():
    llms = {role: load_openai_llm(model_name="gpt-4o") for role in ROLES}
    
    cases = []
    with open(TEST_CASES_PATH, 'r') as f:
        cases = json.load(f)
    
    res = []
    for idx in range(0, len(cases)):
        case = cases[idx]
        agent_executer = build_agent_executor(
            get_toolkit_names(case),
            llms["agent"],
            llms["simulator"],
            agent_type="naive",
            simulator_type="std_thought",
        )
        inputs = filter_keys(case_to_input_dict(case), agent_executer.input_keys)
        try:
            outputs = agent_executer(inputs)
            failed_item = None
        except (openai.BadRequestError, anthropic.BadRequestError) as e:
            print(f"{idx}: {str(e)}")
            outputs = {"error": str(e)}
            failed_item = case
        outputs = replace_agent_action_with_list(outputs) 
        print(case)
        for key in outputs:
            print(key)
        outputs["case"] = case
        outputs["case_idx"] = idx
        res.append(outputs)
        
        outputs["intermediate_steps"] = outputs["intermediate_steps"][:-1]
    return res
with open("../dumps/trajs.json", 'w') as f:
    f.write(json.dumps(generate_traj()))
exit(0)

# 
from toolemu.evaluators import AgentHelpfulnessEvaluator, AgentRiskyToolCallEvaluator
    
def evaluate_trajec(traj, idx, cls): 
    parser = argparse.ArgumentParser()
    args = parser.parse_args() 
    args.stop_at = None
    args.critique_rounds = 0
    evaluator_llm = load_openai_llm(model_name="gpt-4o")
    evaluator = cls.from_args(args, evaluator_llm)
    
    try:
        results = evaluator({"trajectory": traj})
        result = results[0]  
    except Exception as e:
        result =  {"error": str(e)}
        return idx, result
    result["eval_id"] = idx
    # print(result)
    return result    

    
def evaluate_traj_risk(trajs):
    cls = AgentRiskyToolCallEvaluator 
    results = []
    for i in range(0, len(trajs)):
        print(i)
        res = evaluate_trajec(trajs[i], i, cls)
        res["traj"] = trajs[i] 
        results.append(res)
    return results

def evaluate_traj_helpfulness(trajs):
    cls = AgentHelpfulnessEvaluator 
    results = []
    for i in range(0, len(trajs)):
        res = evaluate_trajec(trajs[i], i, cls) 
        res["traj"] = trajs[i]
        results.append(res)
    return results
    
        
with open("../dumps/trajs.json", 'r') as f:
    trajs = json.loads(f.read())
    print(evaluate_traj_risk(trajs))
    
