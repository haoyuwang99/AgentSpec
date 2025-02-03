
import re
import datetime
from typing import Dict
from ..manual import util

def has_important_event(action_input: Dict, ctx) -> bool:
    return util.llm_judge("check if any of the events to be deleted contain important information", action_input, ctx)
def is_event_verified(action_input: Dict, ctx) -> bool:
    return util.llm_judge("verify the event details before sending invitations", action_input, ctx)
from datetime import datetime

def is_reminder_time_valid(action_input: Dict, ctx) -> bool:
    reminder_time = action_input.get('reminder_time')
    if reminder_time:
        reminder_datetime = datetime.fromisoformat(reminder_time)
        return reminder_datetime > datetime.now()
    return False
from datetime import datetime

def is_event_time_range_valid(action_input: Dict, ctx) -> bool:
    start_time = action_input.get('start_time')
    end_time = action_input.get('end_time')
    if start_time and end_time:
        start_datetime = datetime.fromisoformat(start_time)
        end_datetime = datetime.fromisoformat(end_time)
        return start_datetime < end_datetime
    return True
