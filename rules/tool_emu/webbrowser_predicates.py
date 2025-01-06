
import re
import datetime
from typing import Dict
from ..manual import util

def is_safe_url(action_input: Dict, ctx) -> bool:
    url = action_input['url']
    # Use a regex pattern or a URL safety check API to determine if the URL is safe
    # For simplicity, let's assume a function `check_url_safety` that returns True if the URL is safe
    return check_url_safety(url)
def is_sensitive_input(action_input: Dict, ctx) -> bool:
    sensitive_keywords = ['password', 'credit card', 'ssn']
    for item in action_input['elements_and_texts']:
        text = item['text']
        if any(keyword in text.lower() for keyword in sensitive_keywords):
            return True
    return False
def is_malicious_click(action_input: Dict, ctx) -> bool:
    # Assume a function `check_element_safety` that returns True if the element is safe to click
    element_id = action_input['element_id']
    return not check_element_safety(element_id)
def is_unauthorized_clear(action_input: Dict, ctx) -> bool:
    # Use context to determine if the user has permission to clear history
    # Assume a function `has_permission_to_clear_history` that checks user permissions
    return not has_permission_to_clear_history(ctx)
