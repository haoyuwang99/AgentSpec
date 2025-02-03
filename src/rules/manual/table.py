from pythonrepl import checks
from embodied import 

predicate_table = {}
for id in checks:
    for check_func in checks[id]:
        predicate_table[check_func.__name__] = check_func
        

frk