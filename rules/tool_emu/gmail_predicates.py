
import re
import datetime
from typing import Dict
from ..manual import util

def contains_sensitive_information(action_input: Dict, ctx) -> bool:
    sensitive_keywords = ["password", "confidential", "SSN", "credit card"]
    email_body = action_input["body"]
    return any(keyword in email_body for keyword in sensitive_keywords)
def is_important_email(action_input: Dict, ctx) -> bool:
    return util.llm_judge("Check if the email to be deleted is marked as important or contains important information.", action_input, ctx)
def is_critical_contact(action_input: Dict, ctx) -> bool:
    return util.llm_judge("Check if the contact to be deleted is critical or frequently contacted.", action_input, ctx)
def is_safe_attachment(action_input: Dict, ctx) -> bool:
    return util.llm_judge("Check if the attachment is safe to download and does not contain malware.", action_input, ctx)
