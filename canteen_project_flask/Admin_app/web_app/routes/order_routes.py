from flask import Blueprint, render_template, request, redirect, url_for, flash
from Admin_app.modules.menu_manager import get_orders_by_token, mark_order_delivered

order_bp = Blueprint('orders', __name__)

@order_bp.route('/verify-token', methods=['GET', 'POST'])
def verify_token():
    found_orders = []
    if request.method == 'POST':
        token = request.form.get('token_number')
        found_orders = get_orders_by_token(token)
        if not found_orders:
            flash(f"No active order found for Token #{token} today.", "warning")
    return render_template('admin/verify_token.html', orders=found_orders)

@order_bp.route('/complete-delivery/<int:order_id>')
def complete_delivery(order_id):
    if mark_order_delivered(order_id):
        flash("Order delivered successfully!", "success")
    else:
        flash("Error: Could not update order status.", "danger")
    return redirect(url_for('orders.verify_token'))