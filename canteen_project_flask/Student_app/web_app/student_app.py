import sys
import os
from flask import Flask, session, redirect, url_for

# --- 1. PATH ALIGNMENT ---
current_file = os.path.abspath(__file__)
# Go up 2 levels: web_app -> Student_app -> canteen_project_flask
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

# --- 2. EXPLICIT IMPORTS ---
try:
    # We reference the full path from the project root
    from Student_app.web_app.auth_routes import auth_bp
    from Student_app.web_app.menu_routes import menu_bp
    from Student_app.web_app.profile_routes import profile_bp
    from Student_app.web_app.order_routes import order_bp
except ImportError as e:
    print(f"CRITICAL: Failed to load routes. Error: {e}")
    sys.exit(1)

# --- 3. FLASK SETUP ---
# Pointing to folders inside Student_app
app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')
app.secret_key = 'student_session_secret'

app.register_blueprint(auth_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(order_bp)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('menu.menu_page')) # Note the 'menu.' prefix
    return redirect(url_for('auth.login'))         # Note the 'auth.' prefix

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)