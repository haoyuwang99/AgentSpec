
import re
import datetime
from typing import Dict
from ..manual import util

def is_search_term_specific(action_input: Dict, ctx) -> bool:
    search_term = action_input['search_term']
    # Check if the search term is overly broad, e.g., too short or too common
    return len(search_term) > 3 and not search_term.lower() in ['john', 'doe', 'smith']
def is_valid_unique_id(action_input: Dict, ctx) -> bool:
    unique_id = action_input['unique_id']
    # Assume a valid unique_id follows a specific pattern or length
    return len(unique_id) == 10 and unique_id.isalnum()
def is_provided_data_format_correct(action_input: Dict, ctx) -> bool:
    provided_data = action_input['provided_data']
    # Check if provided_data contains expected keys
    expected_keys = {'name', 'location', 'age_range', 'contact_info', 'social_profiles', 'public_records'}
    return expected_keys.issubset(provided_data.keys())
import re
def is_valid_phone_number(action_input: Dict, ctx) -> bool:
    phone_number = action_input['phone_number']
    # Validate phone number format (e.g., E.164 format)
    return re.match(r'^\+?[1-9]\d{1,14}$', phone_number) is not None
import os
def is_valid_file_path(action_input: Dict, ctx) -> bool:
    local_file_path = action_input['local_file_path']
    # Check if the file path is absolute and does not contain dangerous patterns
    return os.path.isabs(local_file_path) and '..' not in local_file_path
