import sys
import os
from flask import Flask, redirect, url_for, flash

# --- DYNAMIC PATH ALIGNMENT ---
current_dir = os.path.dirname(os.path.abspath(__file__)) 
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'admin_session_secure_key'

# Import Blueprints
from Admin_app.web_app.routes.menu_routes import menu_bp
from Admin_app.web_app.routes.order_routes import order_bp
from Admin_app.web_app.routes.analytics_routes import analytics_bp

# Register Blueprints
app.register_blueprint(menu_bp)
app.register_blueprint(order_bp)
app.register_blueprint(analytics_bp)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)