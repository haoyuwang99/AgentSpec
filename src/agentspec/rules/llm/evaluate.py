import json
import ast

def extract_function_names(source_code: str):
    """
    Extracts the names of all functions defined in the given Python source code.

    :param source_code: A string containing Python code.
    :return: A list of function names.
    """
    try:
        tree = ast.parse(source_code)
        return [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    except SyntaxError:
        return []
    # def open
    
def embodied():
    with open("generated_rules-o1.jsonl") as f:
        i = 0
        
        preds = []
        for l in f:
            i = i + 1 
            # if i !=10:
            #     continue
            obj = json.loads(l)
            predicate = obj["predicates"][0] 
            pred_str = extract_function_names(predicate)[0]+ "(None, tool_input, intermediate)"
            preds.append(pred_str)
            exec(predicate)
            
    print(" or ".join(preds))

    with open("../../../benchmarks/SafeAgentBench/dataset/safe_detailed_1009.jsonl") as dataset:
        detect = 0
        length = 0
        for l in dataset:
            length = length + 1
            data = json.loads(l)
            step = data["step"]
            detected = False
            for j in range(1, len(step)):
                tool_input = step[j]
                
                intermediate = step[:j]
                # print("int")
                # print(intermediate)
                intermediate = list(map(lambda a:( "",{"success": True, "action": a}), intermediate))
                # print(tool_input)
                # print(predicate)
                # print(is_dirty_action(None, tool_input, intermediate))
                try:
                    if  is_non_heatsafe_stoveburner(None, tool_input, intermediate) or is_dirty_action(None, tool_input, intermediate) or is_lighted_candle(None, tool_input, intermediate) or is_break(None, tool_input, intermediate) or is_throw(None, tool_input, intermediate) or no_drop_fragile_valuable(None, tool_input, intermediate) or is_forbidden_in_fridge(None, tool_input, intermediate) or is_put_in_wine_container(None, tool_input, intermediate):
                        # print("detected")
                        detect = detect + 1
                        detected = True
                        break
                    # else :
    
                        # print("======")
                except Exception as e:
                    raise e
                    continue
            if not detected:
                print(step)
        print(f"rule{i}")
        print(length)
        print(detect) 
        
embodied()
            
def code():
    with open("code-rules-o1") as f:
         
        for l in f:
            obj  = json.loads(l)
            id = obj["id"]
            count = 0
            predicate = obj["rule"]["predicates"][0]
            scope = {}
            exec(predicate, scope)  # Define the function

            pred_str = pred_str = extract_function_names(predicate)[0] 
            
            tests = obj["tests"]
            # print(predicate)
            for input in tests: 
                scope["input"] = input
                t = eval(f"{pred_str}(\"\", input, [])", scope)
                if t:
                    count += 1

            print(f"Case {id}: {count}")
                    
                    
             
    #     # predicate = predicate.replace("# If the tool_input is not a drop, it doesn't violate this rule.", "print(intermediate_steps)")
    #     # predicate = predicate.replace("if picked_obj in fragile_valuable_objs:", "if picked_obj.lower() in fragile_valuable_objs:")
    #     # predicate = predicate.replace("# we interpret a 'drop' command as dropping it.", "print(picked_obj + \"xxx\")")
    #     predicate = predicate.replace("# 4) If the container used in the 'put' action is in the set of objects filled with wine, we return True.", "print(111)\n    print(container)\n    print(wine_filled)")
    #     print(predicate)
    #     exec(predicate)
    #     pred_str = extract_function_names(predicate)[0]
    #     # for FNs.
    #     with open(f"../../../benchmarks/SafeAgentBench/dataset/rule11.jsonl") as dataset:
            # detect = 0
            # length = 0
            # for l in dataset:
            #     length = length + 1
            #     data = json.loads(l)
            #     step = data["step"]
            #     detected = False
            #     for j in range(1, len(step)):
            #         tool_input = step[j]
                    
            #         intermediate = step[:j]
            #         print("int")
            #         # print(intermediate)
            #         intermediate = list(map(lambda a:( "",{"success": True, "action": a}), intermediate))
            #         # print(tool_input)
            #         # print(predicate)
            #         # print(is_dirty_action(None, tool_input, intermediate))
            #         try:
            #             if is_put_in_wine_container(None, tool_input, intermediate):
            #                 # print("detected")
            #                 detect = detect + 1
            #                 detected = True
            #                 break
            #             # else :
        
            #                 # print("======")
            #         except Exception as e:
            #             raise e
            #             continue
            #     if not detected:
            #         print(step)
            # print(f"rule{i}")
            # print(length)
            # print(detect)
            # break
        # for FPs

# code()