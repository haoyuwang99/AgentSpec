
import re
import datetime
from typing import Dict
from ..manual import util

def exceeds_max_grabbed_objects(action_input, ctx):
    max_objects = 5
    current_state = ctx['current_state']
    grabbed_objects = current_state.get('grabbed_objects', [])
    return len(grabbed_objects) > max_objects
def allowed_operations_retrieved(action_input, ctx):
    last_operation = ctx.get('last_operation')
    return last_operation == 'GetAllowedOperations'
def person_identified(action_input, ctx):
    person_id = action_input.get('person_id')
    found_people = ctx.get('found_people', [])
    for person in found_people:
        if person['person_id'] == person_id and person['person_name'] != 'unknown':
            return True
    return False
def is_high_risk_operation(action_input, ctx):
    operation_id = action_input.get('operation_id')
    allowed_operations = ctx.get('allowed_operations', [])
    for operation in allowed_operations:
        if operation['operation_id'] == operation_id:
            for side_effect in operation.get('potential_side_effects', []):
                if side_effect['probability'] > 0.7:
                    return True
    return False
