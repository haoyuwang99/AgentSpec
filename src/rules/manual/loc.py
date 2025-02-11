import re

def count_function_loc(code):
    function_pattern = re.compile(r"def (\w+)\(.*\):(.*\)")
    matches = function_pattern.finditer(code)

    function_lines = {}
    lines = code.split("\n")
    current_function = None
    start_line = None

    for i, line in enumerate(lines):
        match = function_pattern.match(line)
        if match:
            if current_function:
                function_lines[current_function] = i - start_line
            current_function = match.group(1)
            start_line = i

    if current_function:
        function_lines[current_function] = len(lines) - start_line

    return function_lines

with open("pythonrepl.py", "r") as file:
    code = file.read()

loc_results = count_function_loc(code)
for func, loc in loc_results.items():
    print(f"{func}: {loc} LoC")
