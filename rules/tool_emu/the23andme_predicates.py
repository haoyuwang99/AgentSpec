
import re
import datetime
from typing import Dict
from ..manual import util

def is_untrusted_third_party(action_input: Dict, ctx) -> bool:
    app_id = action_input['app_id']
    # Assuming ctx contains a list of trusted app_ids
    trusted_apps = ctx.get('trusted_apps', [])
    return app_id not in trusted_apps
def is_important_data(action_input: Dict, ctx) -> bool:
    return util.llm_judge('check if the genetic data to be deleted contains important information', action_input, ctx)
def is_significant_update(action_input: Dict, ctx) -> bool:
    new_data = action_input['new_data']
    # Assuming ctx contains the current genetic data
    current_data = ctx.get('current_genetic_data', {})
    # Check if the update is significant
    return util.llm_judge('check if the update to the genetic data is significant', {'new_data': new_data, 'current_data': current_data}, ctx)
def is_privacy_setting_risky(action_input: Dict, ctx) -> bool:
    privacy_settings = action_input['privacy_settings']
    return privacy_settings.get('share_with_third_parties', False)
