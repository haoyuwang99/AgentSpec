
import re
import datetime
from typing import Dict
from util import llm_judge



def has_important_note(action_input: Dict, ctx) -> bool:
    return llm_judge("check if the note to be deleted contains important information", action_input, ctx)

def has_important_notebook(action_input: Dict, ctx) -> bool:
    return llm_judge("check if the notebook to be deleted contains important notes", action_input, ctx)

def is_sharing_level_can_edit(action_input: Dict, ctx) -> bool:
    return action_input.get('level') == 'can_edit'