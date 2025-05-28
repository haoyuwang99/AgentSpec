
import re
import datetime
from typing import Dict
from ..manual import util

import re
def is_destructive_command(action_input: Dict, ctx) -> bool:
    destructive_patterns = [r'\brm\b', r'\bdd\b', r'\bsudo\b', r'\bmkfs\b', r'\bshutdown\b', r'\breboot\b']
    cmd = action_input['command']
    return any(re.search(pattern, cmd) for pattern in destructive_patterns)
