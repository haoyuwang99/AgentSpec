import os
import re 

from langchain_community.tools import ShellTool

tool_name = ShellTool().name
table = {}

def is_destructive(user_input, tool_input, intermediate_steps): 
    destructive_patterns = [r"\brm\b", r"\bdd\b", r"\bsudo\b"]
    res = any(re.search(pattern, str(tool_input)) for pattern in destructive_patterns)
    print(str(tool_input))
    print(res)
    return res

table["is_destructive"] = is_destructive
 