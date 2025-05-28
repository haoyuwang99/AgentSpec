
import re
import datetime
from typing import Dict
from ..manual import util

def is_invalid_payment_info(action_input, ctx):
    payment_info = action_input['payment_method']
    card_number = payment_info.get('card_number', '')
    expiry_date = payment_info.get('expiry_date', '')
    cvv = payment_info.get('cvv', '')
    # Simple checks for length and format
    if len(card_number) < 13 or len(card_number) > 19:
        return True
    if not re.match(r'^(0[1-9]|1[0-2])/[0-9]{2}$', expiry_date):
        return True
    if len(cvv) not in [3, 4]:
        return True
    return False
def has_significant_refundable_amount(action_input, ctx):
    reservation_ids = action_input['reservation_ids']
    reservations = ctx.get('reservations', [])
    for reservation in reservations:
        if reservation['reservation_id'] in reservation_ids:
            if reservation.get('refundable_amount', 0) > 1000:  # Arbitrary threshold
                return True
    return False
def exceeds_max_results(action_input, ctx):
    max_results = action_input.get('max_results', 5)
    return max_results > 10
def exceeds_max_results(action_input, ctx):
    max_results = action_input.get('max_results', 5)
    return max_results > 10
def is_sensitive_information_access(action_input, ctx):
    information_type = action_input['information_type']
    return information_type in ['payments', 'people']
