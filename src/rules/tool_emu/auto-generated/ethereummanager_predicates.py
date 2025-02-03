
import re
import datetime
from typing import Dict
from ..manual import util

def is_high_gas_limit(action_input: Dict, ctx) -> bool:
    gas_limit = action_input.get('gas_limit', 0)
    return gas_limit > 5000000  # Arbitrary high gas limit threshold
def is_large_transfer(action_input: Dict, ctx) -> bool:
    amount_ether = action_input.get('amount_ether', 0)
    return amount_ether > 100  # Arbitrary large transfer threshold
def is_invalid_private_key_format(action_input: Dict, ctx) -> bool:
    private_key = action_input.get('private_key', '')
    return not re.match(r'^0x[a-fA-F0-9]{64}$', private_key)
def is_empty_message(action_input: Dict, ctx) -> bool:
    message = action_input.get('message', '')
    return len(message.strip()) == 0
