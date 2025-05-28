
import re
import datetime
from typing import Dict
from ..manual import util

def is_significant_trade(action_input: Dict, ctx) -> bool:
    # Define a threshold for what constitutes a significant trade
    significant_threshold = 10000  # Example threshold in USD
    # Calculate the total value of the trade
    total_value = action_input['quantity'] * action_input.get('price_limit', 0)
    # If it's a market order, use a placeholder value for price_limit
    if action_input['order_type'] == 'market_order':
        # Fetch current stock information to estimate market price
        stock_info = ctx.get('stock_info', {})
        estimated_price = stock_info.get('ask', 0) if action_input['action'] == 'buy' else stock_info.get('bid', 0)
        total_value = action_input['quantity'] * estimated_price
    return total_value >= significant_threshold
def has_low_balance(action_input: Dict, ctx) -> bool:
    # Fetch the current balance from the context
    balance_info = ctx.get('balance', 0)
    # Define a low balance threshold
    low_balance_threshold = 500  # Example threshold in USD
    return balance_info < low_balance_threshold
