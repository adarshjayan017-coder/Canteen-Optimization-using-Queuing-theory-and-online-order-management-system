from flask import Blueprint, render_template, session, redirect, url_for
from Student_app.modules.student_manager import get_student_profile, get_user_order_history

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile')
def profile():
    if 'user_id' not in session: 
        return redirect(url_for('auth.login'))
    
    # Fetches real username, email, and created_at
    user_data = get_student_profile(session['user_id'])
    cart_count = sum(session.get('cart', {}).values())
    
    return render_template('user/profile.html', 
                           user=user_data, 
                           cart_count=cart_count)

@profile_bp.route('/profile/history')
def order_history():
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    
    # 1. Fetch History with item names
    history = get_user_order_history(session['user_id'])
    
    # 2. Calculate Total Spend metric
    total_spend = sum(order['total_amount'] for order in history)
    
    return render_template('user/order_history.html', 
                           orders=history, 
                           total_spend=total_spend)