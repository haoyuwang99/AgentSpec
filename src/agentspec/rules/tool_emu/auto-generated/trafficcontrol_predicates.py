
import re
import datetime
from typing import Dict
from ..manual import util

def is_unsafe_traffic_light_change(action_input, ctx):
    # Check if the traffic light state change is to 'hazard' or if it conflicts with current traffic patterns
    unsafe_states = ['hazard']
    return action_input['traffic_light_state'] in unsafe_states
def is_invalid_priority_time(action_input, ctx):
    # Check if the priority time is outside of normal emergency response hours
    from datetime import datetime
    start_time = datetime.strptime(action_input['start_time'], '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(action_input['end_time'], '%Y-%m-%d %H:%M:%S')
    # Assuming normal emergency response hours are between 6 AM and 10 PM
    return not (6 <= start_time.hour <= 22 and 6 <= end_time.hour <= 22)
def is_during_peak_hours(action_input, ctx):
    # Check if the maintenance is scheduled during peak traffic hours
    from datetime import datetime
    start_time = datetime.strptime(action_input['start_time'], '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(action_input['end_time'], '%Y-%m-%d %H:%M:%S')
    # Assuming peak hours are between 7 AM - 9 AM and 4 PM - 6 PM
    peak_hours = [(7, 9), (16, 18)]
    return any(start_time.hour in range(start, end) or end_time.hour in range(start, end) for start, end in peak_hours)
