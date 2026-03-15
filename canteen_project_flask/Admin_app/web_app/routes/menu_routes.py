from flask import Blueprint, render_template, request, redirect, url_for
from Admin_app.modules.menu_manager import get_full_menu, add_menu_item, toggle_availability, alter_menu_item

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/')
def dashboard():
    menu_items = get_full_menu()
    return render_template('admin/dashboard.html', items=menu_items)

@menu_bp.route('/add_item', methods=['POST'])
def add_item():
    name = request.form.get('name')
    price = request.form.get('price')
    category = request.form.get('category')
    if name and price:
        add_menu_item(name, price, category)
    return redirect(url_for('menu.dashboard'))

@menu_bp.route('/toggle/<int:item_id>/<int:status>')
def toggle_status(item_id, status):
    toggle_availability(item_id, status)
    return redirect(url_for('menu.dashboard'))

@menu_bp.route('/edit_item/<int:item_id>', methods=['POST'])
def edit_item(item_id):
    name = request.form.get('new_name')
    price = request.form.get('new_price')
    category = request.form.get('new_cat')
    status = request.form.get('new_status') 
    if name and price:
        alter_menu_item(item_id, name, float(price), category, int(status))
    return redirect(url_for('menu.dashboard'))