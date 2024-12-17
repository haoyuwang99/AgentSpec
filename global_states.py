import os

registered_tools = set()

example_rule = """rule @check_python_code
trigger 
    act PythonCodeExecutor
check 
    llm_judge(cur_act, "return true if this is a risky python code")
enforce
    user_inspection
end
"""  
 