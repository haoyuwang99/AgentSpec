
import re
import datetime
from typing import Dict
from ..manual import util

def is_important_item(action_input: Dict, ctx) -> bool:
    return util.llm_judge("check if the item to be deleted contains important information", action_input, ctx)
def is_edit_access(action_input: Dict, ctx) -> bool:
    return action_input.get('access_level') == 'edit'
def is_edit_access_link(action_input: Dict, ctx) -> bool:
    return action_input.get('access_level') == 'edit'
