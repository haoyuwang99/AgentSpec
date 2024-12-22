import os

registered_tools = set()

example_rule = """rule @check_python_code
trigger 
    act terminalAA
check 
    is_destructive
enforce
    user_inspection
end
"""  
 