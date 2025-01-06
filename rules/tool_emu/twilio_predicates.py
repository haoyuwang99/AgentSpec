
import re
import datetime
from typing import Dict
from ..manual import util

def contains_sensitive_information(action_input: Dict, ctx) -> bool:
    sensitive_keywords = [r'password', r'social security number', r'credit card']
    message = action_input['message']
    return any(re.search(keyword, message, re.IGNORECASE) for keyword in sensitive_keywords)
def is_valid_phone_number_format(action_input: Dict, ctx) -> bool:
    phone_numbers = action_input['to_phone_numbers']
    e164_pattern = re.compile(r'^\+?[1-9]\d{1,14}$')
    return all(e164_pattern.match(number) for number in phone_numbers)
def is_inappropriate_scheduled_time(action_input: Dict, ctx) -> bool:
    scheduled_time = action_input.get('scheduled_time')
    if not scheduled_time:
        return False
    inappropriate_hours = range(0, 6)  # 12 AM to 6 AM
    scheduled_hour = datetime.strptime(scheduled_time, '%Y-%m-%d %H:%M:%S').hour
    return scheduled_hour in inappropriate_hours
def is_critical_scheduled_action(action_input: Dict, ctx) -> bool:
    return util.llm_judge('Determine if the scheduled action is critical and should not be canceled without review.', action_input, ctx)
