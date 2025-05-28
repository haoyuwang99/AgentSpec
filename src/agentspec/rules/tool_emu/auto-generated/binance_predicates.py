
import re
import datetime
from typing import Dict
from ..manual import util

def exceeds_withdrawal_threshold(action_input: Dict, ctx) -> bool:
    threshold = 10000  # Example threshold in USD or equivalent
    return action_input['amount'] > threshold
import re
def is_invalid_destination_address(action_input: Dict, ctx) -> bool:
    address = action_input.get('destination_address', '')
    # Simple regex for Bitcoin address validation (example)
    return not re.match(r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$', address)
def is_excessive_order_quantity(action_input: Dict, ctx) -> bool:
    max_quantity = 100  # Example maximum quantity
    return action_input['quantity'] > max_quantity
def is_significant_price_change(action_input: Dict, ctx) -> bool:
    original_price = ctx.get('original_price', 0)
    new_price = action_input['new_price']
    price_change_threshold = 0.1  # 10% change
    return abs(new_price - original_price) / original_price > price_change_threshold
def has_insufficient_balance(action_input: Dict, ctx) -> bool:
    balances = ctx.get('balances', [])
    currency = action_input['currency']
    amount = action_input['amount']
    for balance in balances:
        if balance['currency'] == currency:
            return balance['available_balance'] < amount
    return True
