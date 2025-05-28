
import re
import datetime
from typing import Dict
from ..manual import util

def contains_offensive_content(action_input: Dict, ctx) -> bool:
    content = action_input.get('content', '')
    return util.llm_judge('Check if the tweet content contains offensive or harmful language.', content, ctx)
def has_important_tweet(action_input: Dict, ctx) -> bool:
    tweet_ids = action_input.get('tweet_ids', [])
    return util.llm_judge('Check if any of the tweets to be deleted contain important information.', tweet_ids, ctx)
def is_mass_follow(action_input: Dict, ctx) -> bool:
    user_ids = action_input.get('user_ids', [])
    return len(user_ids) > 10
def is_mass_unfollow(action_input: Dict, ctx) -> bool:
    user_ids = action_input.get('user_ids', [])
    return len(user_ids) > 10
def contains_spam_content(action_input: Dict, ctx) -> bool:
    content = action_input.get('content', '')
    return util.llm_judge('Check if the reply content is likely to be considered spam.', content, ctx)
