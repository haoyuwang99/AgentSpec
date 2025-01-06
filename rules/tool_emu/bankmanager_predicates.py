
import re
import datetime
from typing import Dict
from ..manual import util

def is_large_transfer(action_input: Dict, ctx) -> bool:
    threshold = 10000  # Example threshold amount
    return action_input['amount'] > threshold
def is_download_requested(action_input: Dict, ctx) -> bool:
    return action_input.get('download', False)
from datetime import datetime

def is_payment_date_valid(action_input: Dict, ctx) -> bool:
    payment_date = datetime.strptime(action_input['payment_date'], '%Y-%m-%d')
    return payment_date >= datetime.now()
def is_valid_account_type(action_input: Dict, ctx) -> bool:
    valid_account_types = ['checking', 'savings', 'mutual fund TFSA', 'mutual fund non-registered', 'self-directed TFSA', 'self-directed non-registered', 'mortgage', 'credit_card']
    return action_input['account_type'] in valid_account_types
