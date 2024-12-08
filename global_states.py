import os

registered_tools = set()

example_rule = """rule @reflect
trigger 
    any
check 
    true
enforce
    user_inspection
end
""" 
