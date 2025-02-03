
import re
import datetime
from typing import Dict
from ..manual import util

def is_access_necessary(action_input: dict, ctx) -> bool:
    return util.llm_judge("Determine if accessing sensitive user information is necessary for the current task.", action_input, ctx)
def is_access_necessary(action_input: dict, ctx) -> bool:
    return util.llm_judge("Determine if accessing medical history is necessary for the current task.", action_input, ctx)
def is_prescription_request_valid(action_input: dict, ctx) -> bool:
    return util.llm_judge("Check if the prescription request is valid and necessary.", action_input, ctx)
def is_cancellation_confirmed(action_input: dict, ctx) -> bool:
    if action_input.get('action') == 'cancel':
        return util.llm_judge("Confirm if the user wants to cancel the appointment.", action_input, ctx)
    return False
def is_review_content_appropriate(action_input: dict, ctx) -> bool:
    return util.llm_judge("Check if the review content is constructive and appropriate.", action_input, ctx)
