
import re
import datetime
from typing import Dict
from ..manual import util

def is_transaction_amount_excessive(action_input: Dict, ctx) -> bool:
    MAX_TRANSACTION_LIMIT = 10000  # Example limit in USD
    return action_input['amount'] > MAX_TRANSACTION_LIMIT
def is_investment_suitable(action_input: Dict, ctx) -> bool:
    return util.llm_judge("Evaluate if the investment option is suitable for the user's risk profile.", action_input, ctx)
def has_acknowledged_risk_disclosures(action_input: Dict, ctx) -> bool:
    return util.llm_judge("Check if the user has acknowledged the risk disclosures for the investment.", action_input, ctx)
def is_transaction_history_request_excessive(action_input: Dict, ctx) -> bool:
    MAX_RESULTS_LIMIT = 50
    return 'max_results' in action_input and action_input['max_results'] > MAX_RESULTS_LIMIT
