from core.db_config import get_db_connection

# --- 1. VIEW MENU ---
def get_full_menu():
    conn = get_db_connection()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True)
        # We fetch all items, including inactive ones for the Admin
        cursor.execute("SELECT * FROM menu ORDER BY is_available DESC, item_id ASC")
        return cursor.fetchall()
    finally:
        conn.close()

# --- 2. ADD MENU ITEM ---
def add_menu_item(name, price, category):
    if not name.strip(): return False
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = "INSERT INTO menu (item_name, price, category, is_available) VALUES (%s, %s, %s, 1)"
        cursor.execute(query, (name.strip(), price, category.strip()))
        conn.commit()
        print(f"✅ '{name}' added successfully.")
    finally:
        conn.close()

# --- 3. ALTER MENU ITEM (Includes Status Update) ---
def alter_menu_item(item_id, new_name, new_price, new_cat, new_status=None):
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM menu WHERE item_id = %s", (item_id,))
        current = cursor.fetchone()
        
        if not current:
            print("❌ Item not found.")
            return

        # Logic: Use new input if provided, otherwise keep database current value
        final_name = new_name.strip() if new_name and new_name.strip() else current['item_name']
        final_price = new_price if new_price is not None else current['price']
        final_cat = new_cat.strip() if new_cat and new_cat.strip() else current['category']
        
        # Status logic: 1 (Active), 0 (Stock Out), -1 (Inactive)
        final_status = int(new_status) if new_status is not None else current['is_available']

        query = "UPDATE menu SET item_name = %s, price = %s, category = %s, is_available = %s WHERE item_id = %s"
        cursor.execute(query, (final_name, final_price, final_cat, final_status, item_id))
        conn.commit()
        print(f"✅ Item ID {item_id} updated successfully.")
    finally:
        conn.close()

# --- 4. TOGGLE AVAILABILITY (Quick Switch) ---
def toggle_availability(item_id, is_available):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = "UPDATE menu SET is_available = %s WHERE item_id = %s"
        cursor.execute(query, (is_available, item_id))
        conn.commit()
        status_map = {1: "AVAILABLE", 0: "STOCK OUT", -1: "INACTIVE"}
        print(f"✅ Item ID {item_id} status set to {status_map.get(is_available, 'UNKNOWN')}.")
    finally:
        conn.close()