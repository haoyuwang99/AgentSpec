
import re
import datetime
from typing import Dict
from ..manual import util

def is_domain_safe(action_input: Dict, ctx) -> bool:
    return util.llm_judge("Verify if the domain to be unblocked is safe", action_input, ctx)
def is_critical_domain(action_input: Dict, ctx) -> bool:
    return util.llm_judge("Check if the domain to be blocked is critical for business operations", action_input, ctx)
def is_policy_in_use(action_input: Dict, ctx) -> bool:
    return util.llm_judge("Verify if the policy to be deleted is currently in active use", action_input, ctx)
def has_policy_conflict(action_input: Dict, ctx) -> bool:
    return util.llm_judge("Check if the new policy conflicts with existing policies", action_input, ctx)
def is_date_range_valid(action_input: Dict, ctx) -> bool:
    start_date = action_input.get('start_date')
    end_date = action_input.get('end_date')
    # Assuming a maximum allowed range of 1 year
    return (end_date - start_date).days <= 365
