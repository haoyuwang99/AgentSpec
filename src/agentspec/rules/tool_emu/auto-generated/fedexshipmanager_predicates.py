
import re
import datetime
from typing import Dict
from ..manual import util

def is_valid_package_details(action_input, ctx):
    package_details = action_input.get('package_details', {})
    required_keys = ['description', 'weight', 'dimensions']
    return all(key in package_details and package_details[key] for key in required_keys)
def is_valid_sender_recipient_info(action_input, ctx):
    sender_info = action_input.get('sender_information', {})
    recipient_info = action_input.get('recipient_information', {})
    required_keys = ['full_name', 'address', 'contact_number']
    return all(key in sender_info and sender_info[key] for key in required_keys) and all(key in recipient_info and recipient_info[key] for key in required_keys)
def is_valid_shipment_operation(action_input, ctx):
    shipment_id = action_input.get('shipment_id')
    operation = action_input.get('operation')
    shipment_status = ctx.get('shipment_status', {}).get(shipment_id, 'unknown')
    if operation in ['cancel', 'reschedule_pickup']:
        return shipment_status == 'pending'
    elif operation in ['redirect', 'return_to_sender']:
        return shipment_status == 'in_transit'
    return False
def is_valid_special_handling(action_input, ctx):
    special_handling = action_input.get('special_handling', [])
    valid_options = {'signature_required', 'fragile', 'oversized', 'dangerous_goods', 'temperature_sensitive'}
    return all(option in valid_options for option in special_handling)
