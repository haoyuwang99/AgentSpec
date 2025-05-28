
import re
import datetime
from typing import Dict
from ..manual import util

def has_pending_or_open_orders(action_input: Dict, ctx) -> bool:
    product_id = action_input['product_id']
    orders = ctx.get('orders', [])
    for order in orders:
        if any(item['product_id'] == product_id for item in order['items']) and order['status'] in ['open', 'pending']:
            return True
    return False
def is_price_unreasonable(action_input: Dict, ctx) -> bool:
    price = action_input['price']
    return price > 10000  # Assuming $10,000 is an unreasonably high price for a product
def is_price_unreasonable(action_input: Dict, ctx) -> bool:
    price = action_input.get('price')
    if price is not None:
        return price > 10000  # Assuming $10,000 is an unreasonably high price for a product
    return False
def is_order_fulfilled(action_input: Dict, ctx) -> bool:
    order_id = action_input['order_id']
    action = action_input['action']
    if action == 'cancel':
        order_details = ctx.get('order_details', {})
        return order_details.get('status') == 'fulfilled'
    return False
def is_order_not_fulfilled(action_input: Dict, ctx) -> bool:
    order_id = action_input['order_id']
    action = action_input['action']
    if action == 'refund':
        order_details = ctx.get('order_details', {})
        return order_details.get('status') != 'fulfilled'
    return False
