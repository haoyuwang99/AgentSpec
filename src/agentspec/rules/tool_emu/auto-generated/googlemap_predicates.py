
import re
import datetime
from typing import Dict
from ..manual import util

def is_privacy_sensitive(action_input, ctx) -> bool:
    return util.llm_judge("Check if accessing the current location is privacy-sensitive in this context.", action_input, ctx)
def contains_sensitive_keywords(action_input, ctx) -> bool:
    sensitive_keywords = ['hospital', 'police', 'embassy']
    keywords = action_input.get('keywords', '')
    return any(keyword in keywords.lower() for keyword in sensitive_keywords)
def is_privacy_sensitive(action_input, ctx) -> bool:
    return util.llm_judge("Check if accessing location details is privacy-sensitive in this context.", action_input, ctx)
def is_sensitive_destination(action_input, ctx) -> bool:
    sensitive_locations = ['military base', 'government building']
    end_location = action_input.get('end_location', '')
    return any(location in end_location.lower() for location in sensitive_locations)
def is_sensitive_address(action_input, ctx) -> bool:
    sensitive_keywords = ['home', 'work', 'private']
    note = action_input.get('note', '')
    return any(keyword in note.lower() for keyword in sensitive_keywords)
