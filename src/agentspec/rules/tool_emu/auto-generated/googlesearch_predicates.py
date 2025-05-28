
import re
import datetime
from typing import Dict
from ..manual import util

import re

def contains_sensitive_keywords(action_input: dict, ctx) -> bool:
    sensitive_keywords = [r'password', r'credit card', r'social security number', r'confidential']
    keyword = action_input['keyword']
    return any(re.search(pattern, keyword, re.IGNORECASE) for pattern in sensitive_keywords)
import re

def contains_inappropriate_keywords(action_input: dict, ctx) -> bool:
    inappropriate_keywords = [r'nude', r'explicit', r'xxx', r'porn']
    keyword = action_input['keyword']
    return any(re.search(pattern, keyword, re.IGNORECASE) for pattern in inappropriate_keywords)
import re

def contains_inappropriate_keywords(action_input: dict, ctx) -> bool:
    inappropriate_keywords = [r'nude', r'explicit', r'xxx', r'porn']
    keyword = action_input['keyword']
    return any(re.search(pattern, keyword, re.IGNORECASE) for pattern in inappropriate_keywords)
import re

def contains_sensitive_news_keywords(action_input: dict, ctx) -> bool:
    sensitive_news_keywords = [r'political scandal', r'terrorism', r'extremism', r'propaganda']
    keyword = action_input['keyword']
    return any(re.search(pattern, keyword, re.IGNORECASE) for pattern in sensitive_news_keywords)
def has_user_consent(action_input: dict, ctx) -> bool:
    # Assuming ctx contains a field 'user_consent' that indicates if the user has given consent
    return ctx.get('user_consent', False)
