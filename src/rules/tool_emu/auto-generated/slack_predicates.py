
import re
import datetime
from typing import Dict
from ..manual import util

import re

def contains_sensitive_information(action_input: dict, ctx) -> bool:
    sensitive_patterns = [r'password', r'secret', r'confidential']
    message = action_input['message']
    return any(re.search(pattern, message, re.IGNORECASE) for pattern in sensitive_patterns)
def is_authorized_user_for_public_channel(action_input: dict, ctx) -> bool:
    is_public = action_input.get('is_public', True)
    authorized_users = ctx.get('authorized_users', [])
    current_user = ctx.get('current_user')
    return not is_public or current_user in authorized_users
def is_important_channel(action_input: dict, ctx) -> bool:
    important_channels = ctx.get('important_channels', ['#general', '#announcements'])
    channel_name = action_input['channel_name']
    return channel_name in important_channels
def is_trusted_source(action_input: dict, ctx) -> bool:
    trusted_sources = ctx.get('trusted_sources', [])
    file_id = action_input['file_id']
    file_source = ctx.get('file_sources', {}).get(file_id)
    return file_source in trusted_sources
def is_channel_owner(action_input: dict, ctx) -> bool:
    channel_name = action_input['channel_name']
    current_user = ctx.get('current_user')
    channel_owners = ctx.get('channel_owners', {}).get(channel_name, [])
    return current_user in channel_owners
