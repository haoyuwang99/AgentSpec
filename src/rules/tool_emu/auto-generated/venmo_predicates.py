
import re
import datetime
from typing import Dict
from ..manual import util

def is_amount_within_balance(action_input: Dict, ctx) -> bool:
    balance = ctx['balance']  # Assume balance is fetched from context
    amount = action_input['amount']
    return amount <= balance
def is_positive_amount(action_input: Dict, ctx) -> bool:
    amount = action_input['amount']
    return amount > 0
def is_valid_action(action_input: Dict, ctx) -> bool:
    action = action_input['action']
    return action in ['confirm', 'decline']
def is_positive_amount(action_input: Dict, ctx) -> bool:
    amount = action_input['amount']
    return amount > 0
def is_amount_within_balance(action_input: Dict, ctx) -> bool:
    balance = ctx['balance']  # Assume balance is fetched from context
    amount = action_input['amount']
    return amount <= balance
