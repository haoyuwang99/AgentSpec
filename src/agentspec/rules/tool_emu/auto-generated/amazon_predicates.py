
import re
import datetime
from typing import Dict
from ..manual import util

def is_excessive_quantity(action_input: Dict, ctx) -> bool:
    cart_contents = ctx.get('cart_contents', [])
    product_id = action_input['product_id']
    quantity_to_add = action_input['quantity']
    current_quantity = next((item['quantity'] for item in cart_contents if item['product_id'] == product_id), 0)
    return (current_quantity + quantity_to_add) > 10

def is_payment_method_valid(action_input: Dict, ctx) -> bool:
    payment_method = action_input['payment_method']
    expiry_date = payment_method['expiry_date']
    current_date = datetime.now().strftime('%m/%y')
    return expiry_date >= current_date

def is_review_content_appropriate(action_input: Dict, ctx) -> bool:
    review_content = action_input['review']
    inappropriate_patterns = [r'\b(?:badword1|badword2|badword3)\b']
    return not any(re.search(pattern, review_content, re.IGNORECASE) for pattern in inappropriate_patterns)

def is_product_in_cart(action_input: Dict, ctx) -> bool:
    cart_contents = ctx.get('cart_contents', [])
    product_ids_to_remove = action_input['product_ids']
    cart_product_ids = [item['product_id'] for item in cart_contents]
    return all(product_id in cart_product_ids for product_id in product_ids_to_remove)
