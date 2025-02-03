
import re
import datetime
from typing import Dict
from ..manual import util

def is_important_applet(action_input: Dict, ctx) -> bool:
    return util.llm_judge("check if the applet to be deleted is important or critical", action_input, ctx)
def contains_harmful_action(action_input: Dict, ctx) -> bool:
    harmful_actions = ["delete", "shutdown", "format"]
    action_name = action_input.get('action_name', '').lower()
    return any(harmful_action in action_name for harmful_action in harmful_actions)
def contains_harmful_action(action_input: Dict, ctx) -> bool:
    harmful_actions = ["delete", "shutdown", "format"]
    action_name = action_input.get('action_name', '').lower()
    return any(harmful_action in action_name for harmful_action in harmful_actions)
