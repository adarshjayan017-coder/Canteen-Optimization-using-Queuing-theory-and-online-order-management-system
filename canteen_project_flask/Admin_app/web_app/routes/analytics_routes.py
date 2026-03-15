from flask import Blueprint, render_template
from Admin_app.modules.analytics_manager import get_mrp_forecast

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics')
def analytics_dashboard():
    mrp_data, error_msg = get_mrp_forecast()
    return render_template('admin/analytics.html', 
                           data=mrp_data if mrp_data else [], 
                           error=error_msg)