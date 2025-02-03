
import re
import datetime
from typing import Dict
from ..manual import util

def is_high_severity_incident(action_input, ctx):
    return action_input['incident_severity'] == 'High'
def is_redirection_to_new_location(action_input, ctx):
    return action_input['target_type'] == 'Location'
def is_closing_incident(action_input, ctx):
    return action_input.get('incident_status') == 'Closed'
def is_high_priority_incident(action_input, ctx):
    # Assuming context provides incident severity
    incident_severity = ctx.get('incident_severity', 'Low')
    return incident_severity == 'High'
