from .pythonrepl import checks
from .embodied import predicates

#python
predicate_table = {}
for id in checks:
    for check_func in checks[id]:
        predicate_table[check_func.__name__] = check_func
        
#embodied
for predicate in predicates:
    predicate_table[predicate.__name__] = predicate
    
# print( "' | '".join(predicate_table.keys()))