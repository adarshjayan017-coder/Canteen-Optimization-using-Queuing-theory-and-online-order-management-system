from core.db_config import get_db_connection

from datetime import datetime, timedelta
from core.db_config import get_db_connection
import random

def get_available_menu():
    """Fetches ONLY items that are 'Active' (1). Filters out -1 and 0."""
    conn = get_db_connection()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True)
        # Filter: Only show available items to the student
        query = "SELECT item_id, item_name, price, category FROM menu WHERE is_available = 1"
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        conn.close()



def place_order(user_id, cart, token_number, expiry_time):
    """
    Enhanced for Tokens: Includes Stock Validation, Transaction Rollback, 
    Unique Token, and 3-Hour Expiry.
    """
    conn = get_db_connection()
    if not conn: return False, "Database Connection Error"
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # --- UI STEP 1: VALIDATION ---
        for item in cart:
            cursor.execute("SELECT is_available, item_name FROM menu WHERE item_id = %s", (item['item_id'],))
            result = cursor.fetchone()
            if not result or result['is_available'] != 1:
                return False, f"Sorry, {result['item_name'] if result else 'Item'} just went out of stock!"

        # --- UI STEP 2: HEADER INSERT (Now with Token and Expiry) ---
        total_price = sum(item['qty'] * item['price'] for item in cart)
        # We include 'token_number' and 'expiry_time' columns here
        query_order = """
            INSERT INTO orders (user_id, total_amount, status, token_number, expiry_time) 
            VALUES (%s, %s, 'pending', %s, %s)
        """
        cursor.execute(query_order, (user_id, total_price, token_number, expiry_time))
        order_id = cursor.lastrowid
        
        # --- UI STEP 3: DETAILS INSERT ---
        query_items = """INSERT INTO order_items (order_id, item_id, quantity, price_at_sale) 
                         VALUES (%s, %s, %s, %s)"""
        
        for item in cart:
            cursor.execute(query_items, (order_id, item['item_id'], item['qty'], item['price']))
            
        conn.commit()
        return True, order_id

    except Exception as e:
        conn.rollback() # CRITICAL: Undo everything if recording fails.
        return False, str(e)
    finally:
        conn.close()

def get_item_details(item_id):
    """Fetches details for one specific item to validate it before sale"""
    from core.db_config import get_db_connection
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        # This function is built to take EXACTLY 1 argument: item_id
        cursor.execute("SELECT item_id, item_name, price, is_available FROM menu WHERE item_id = %s", (item_id,))
        return cursor.fetchone()
    finally:
        conn.close()

        

def get_user_order_history(user_id):
    """
    Fetches all previous orders for a specific student.
    Includes the items within those orders.
    """
    conn = get_db_connection()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True)
        # We fetch the order details and join with order_items and menu
        # to get the names of the items purchased.
        query = """
            SELECT o.order_id, o.total_amount, o.status, o.created_at,
                   GROUP_CONCAT(CONCAT(m.item_name, ' (x', oi.quantity, ')') SEPARATOR ', ') as items_list
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN menu m ON oi.item_id = m.item_id
            WHERE o.user_id = %s
            GROUP BY o.order_id
            ORDER BY o.created_at DESC
        """
        cursor.execute(query, (user_id,))
        return cursor.fetchall()
    finally:
        conn.close()

#single Orders Dashboard that separates your Active Orders (Pending/Preparing/Ready) from your Historical Orders (Completed/Cancelled).

def get_user_order_history(user_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT o.order_id, o.total_amount, o.status, o.created_at,
            GROUP_CONCAT(CONCAT(m.item_name, ' (x', oi.quantity, ')') SEPARATOR ', ') as items_list
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN menu m ON oi.item_id = m.item_id
            WHERE o.user_id = %s
            GROUP BY o.order_id 
            ORDER BY o.created_at DESC
        """
        cursor.execute(query, (user_id,))
        return cursor.fetchall()
    finally:
        conn.close()

def get_student_profile(user_id):
    """Fetches real data using exact columns from image_d88f25.png"""
    from core.db_config import get_db_connection
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        # We use 'AS name' so your existing HTML template doesn't need changes
        query = """
            SELECT username AS name, email, created_at 
            FROM users 
            WHERE user_id = %s
        """
        cursor.execute(query, (user_id,))
        return cursor.fetchone()
    finally:
        conn.close()





def get_open_tokens(user_id):
    """Fetches tokens that are 'pending' and haven't reached 3-hour expiry"""
    from core.db_config import get_db_connection
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        # FIX: Changed 'order_id' to 'o.order_id' to resolve ambiguity
        query = """
            SELECT o.order_id, o.token_number, o.expiry_time, 
                   GROUP_CONCAT(CONCAT(m.item_name, ' x', oi.quantity) SEPARATOR ', ') as items_summary
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN menu m ON oi.item_id = m.item_id
            WHERE o.user_id = %s 
              AND o.status = 'pending' 
              AND o.expiry_time > NOW()
            GROUP BY o.order_id
            ORDER BY o.created_at DESC
        """
        cursor.execute(query, (user_id,))
        return cursor.fetchall()
    finally:
        conn.close()

def generate_unique_token():
    """Generates a random 4-digit token unique to the current day"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        while True:
            token = random.randint(1000, 9999) # Whole number 4-digit token
            # Verify this token hasn't been used on the current date
            cursor.execute("SELECT COUNT(*) FROM orders WHERE token_number = %s AND DATE(created_at) = CURDATE()", (token,))
            if cursor.fetchone()[0] == 0:
                return token
    finally:
        conn.close()