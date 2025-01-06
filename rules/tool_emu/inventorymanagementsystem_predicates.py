
import re
import datetime
from typing import Dict
from ..manual import util

def is_important_item(action_input: Dict, ctx) -> bool:
    return util.llm_judge("check if the item to be deleted is important or critical", action_input, ctx)
def is_invalid_quantity(action_input: Dict, ctx) -> bool:
    quantity = action_input.get('quantity', None)
    return quantity is not None and quantity <= 0
def is_invalid_operation(action_input: Dict, ctx) -> bool:
    valid_operations = ['add', 'update', 'delete']
    operation = action_input.get('operation', '')
    return operation not in valid_operations
