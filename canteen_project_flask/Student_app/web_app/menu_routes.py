from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request, flash
from Student_app.modules.student_manager import get_available_menu

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/menu')
def menu_page():
    # 1. Access Control: Ensure user is logged in
    if 'user_id' not in session: 
        return redirect(url_for('auth.login'))

    # 2. Fetch Data: Import only what students can actually buy
    # This replaces get_full_menu() and the manual [i for i in all_items] loop
    available_items = get_available_menu() 
    
    # 3. Cart Logic: Calculate total items currently in the session cart
    cart_count = sum(session.get('cart', {}).values())
    
    # 4. Render: Send the filtered list to the student UI
    return render_template('user/menu.html', items=available_items, cart_count=cart_count)

@menu_bp.route('/cart')
def view_cart():
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    cart = session.get('cart', {})
    all_items = get_available_menu()
    cart_display, total_bill = [], 0
    for item in all_items:
        item_id = str(item.get('item_id') or item.get('id'))
        if item_id in cart:
            item['qty'] = cart[item_id]
            item['subtotal'] = item['qty'] * item['price']
            cart_display.append(item)
            total_bill += item['subtotal']
    return render_template('user/cart.html', cart_items=cart_display, total=total_bill, cart_count=sum(cart.values()))

@menu_bp.route('/remove_from_cart/<int:item_id>')
def remove_from_cart(item_id):
    cart = session.get('cart', {})
    id_str = str(item_id)
    if id_str in cart:
        if cart[id_str] > 1:
            cart[id_str] -= 1
        else:
            cart.pop(id_str)
    session['cart'] = cart
    session.modified = True
    
    # --- HYBRID RESPONSE LOGIC ---
    # If it's an AJAX call (from your main.js), return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({"success": True, "cart_count": sum(cart.values())})
    
    # If it's a normal click (from cart.html links), reload the page
    return redirect(request.referrer or url_for('menu.view_cart'))

@menu_bp.route('/add_to_cart/<int:item_id>')
def add_to_cart(item_id):
    cart = session.get('cart', {})
    id_str = str(item_id)
    cart[id_str] = cart.get(id_str, 0) + 1
    session['cart'] = cart
    session.modified = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({"success": True, "cart_count": sum(cart.values())})
        
    return redirect(request.referrer or url_for('menu.view_cart'))


@menu_bp.route('/clear_cart')
def clear_cart():
    # Standard Operating Procedure: Check if cart exists and remove it
    if 'cart' in session:
        session.pop('cart', None)
        session.modified = True
        flash("Your tray has been cleared.", "info")
    
    return redirect(url_for('menu.view_cart'))