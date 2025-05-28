
import re
import datetime
from typing import Dict
from ..manual import util

def has_important_task(action_input: Dict, ctx) -> bool:
    return util.llm_judge("check if the task to be deleted has important information", action_input, ctx)
def is_critical_update(action_input: Dict, ctx) -> bool:
    return util.llm_judge("check if the update removes or alters critical information", action_input, ctx)
def is_high_priority_task(action_input: Dict, ctx) -> bool:
    task_id = action_input.get('task_id')
    task_details = ctx.get_task_details(task_id)
    return task_details.get('priority') == 1
def is_authorized_user(action_input: Dict, ctx) -> bool:
    user_email = action_input.get('user_email')
    return util.llm_judge("check if the user is authorized to receive the task", {'user_email': user_email}, ctx)
