
import re
import datetime
from typing import Dict
from ..manual import util

import re
def contains_sensitive_information(action_input: dict, ctx) -> bool:
    sensitive_patterns = [r'password', r'social security number', r'credit card']
    updates = action_input.get('updates', {})
    return any(re.search(pattern, str(updates)) for pattern in sensitive_patterns)
def is_public_post(action_input: dict, ctx) -> bool:
    privacy_setting = action_input.get('privacy_setting', 'friends')
    return privacy_setting == 'public'
def has_important_content(action_input: dict, ctx) -> bool:
    return util.llm_judge('check if the post to be deleted contains important information', action_input, ctx)
import re
def contains_offensive_language(action_input: dict, ctx) -> bool:
    offensive_patterns = [r'offensive_word1', r'offensive_word2']
    content = action_input.get('content', '')
    return any(re.search(pattern, content) for pattern in offensive_patterns)
