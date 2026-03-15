from flask import Blueprint, session, redirect, url_for, render_template, request
# Import your backend logic with an alias to avoid NameError/TypeError
from Student_app.modules.student_manager import place_order as record_order

order_bp = Blueprint('order', __name__)

# Student_app/web_app/order_routes.py

from datetime import datetime, timedelta
from Student_app.modules.student_manager import generate_unique_token, get_item_details, place_order as record_order

@order_bp.route('/place_order', methods=['POST'])
def place_order():
    if 'user_id' not in session: return redirect(url_for('auth.login'))

    user_id = session['user_id']
    session_cart = session.get('cart', {})

    if not session_cart: return redirect(url_for('menu.view_cart'))

    # 1. Prepare the cart as usual
    prepared_cart = []
    for item_id, qty in session_cart.items():
        details = get_item_details(item_id)
        if details:
            prepared_cart.append({
                'item_id': int(item_id),
                'qty': int(qty),
                'price': float(details['price'])
            })

    # --- THE FIX STARTS HERE ---
    
    # 2. Generate the 4-digit token
    new_token = generate_unique_token() 
    
    # 3. Set the 3-hour expiry time
    expiry = datetime.now() + timedelta(hours=3) 

    # 4. Pass ALL FOUR required arguments to your solid manager
    success, result = record_order(user_id, prepared_cart, new_token, expiry)

    # --- THE FIX ENDS HERE ---

    if success:
        session['cart'] = {}
        # Redirect to your new open tokens page
        return redirect(url_for('order.view_open_tokens'))
    
    return redirect(url_for('menu.view_cart', error=result))

@order_bp.route('/order_success/<int:order_id>')
def order_success(order_id):
    """Displays the final confirmation and Token Number to the student"""
    return render_template('user/order_success.html', order_id=order_id)

# Student_app/web_app/order_routes.py

@order_bp.route('/my_tokens')
def view_open_tokens(): # This MUST match the name in your url_for
    """Displays non-expired 4-digit tokens for student pickup"""
    if 'user_id' not in session: 
        return redirect(url_for('auth.login'))
    
    from Student_app.modules.student_manager import get_open_tokens
    # Fetches tokens valid for 3 hours from ordering
    active_tokens = get_open_tokens(session['user_id'])
    
    return render_template('user/open_tokens.html', tokens=active_tokens)