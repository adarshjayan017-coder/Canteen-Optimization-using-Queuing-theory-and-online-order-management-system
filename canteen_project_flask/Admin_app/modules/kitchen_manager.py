from core.db_config import get_db_connection

def get_active_queue():
    """
    Fetches all orders that are 'pending', 'preparing', or 'ready'.
    Orders are sorted by time (FIFO - First In, First Out).
    """
    conn = get_db_connection()
    if not conn: return []
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT o.order_id, o.status, o.created_at, u.username,
                   GROUP_CONCAT(CONCAT(m.item_name, ' (x', oi.quantity, ')') SEPARATOR ', ') as items
            FROM orders o
            JOIN users u ON o.user_id = u.user_id
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN menu m ON oi.item_id = m.item_id
            WHERE o.status IN ('pending', 'preparing', 'ready')
            GROUP BY o.order_id
            ORDER BY o.created_at ASC
        """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        conn.close()

def update_order_status(order_id, new_status):
    """
    Updates the status and sets the appropriate timestamp for analytics.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Determine which timestamp column to update based on the status
        timestamp_col = ""
        if new_status == 'preparing': timestamp_col = ", preparing_at = NOW()"
        elif new_status == 'ready': timestamp_col = ", ready_at = NOW()"
        elif new_status == 'completed': timestamp_col = ", completed_at = NOW()"

        query = f"UPDATE orders SET status = %s {timestamp_col} WHERE order_id = %s"
        cursor.execute(query, (new_status, order_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conn.close()