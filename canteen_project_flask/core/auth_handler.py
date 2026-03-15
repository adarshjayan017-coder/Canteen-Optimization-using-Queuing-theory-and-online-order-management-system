import bcrypt
from core.db_config import get_db_connection

# --- YOUR ESTABLISHED HASHING LOGIC ---
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(provided_password, stored_hash):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash.encode('utf-8'))

# --- UPDATED REGISTRATION FUNCTION ---
def register_user(username, email, password):
    """SOP: Validates, Hashes, and Stores user data."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # 1. Check if user already exists
        cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return False, "Username already taken."

        # 2. Hash the password
        hashed_val = hash_password(password)

        # 3. Insert using the correct column name: 'password_hash'
        query = """
            INSERT INTO users (username, email, password_hash) 
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (username, email, hashed_val))
        
        conn.commit()
        return True, "Registration successful!"

    except Exception as e:
        return False, f"Database Error: {str(e)}"
    finally:
        cursor.close()
        conn.close()

def login_user(username, password):
    """Generic login that returns user data for role-checking."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        # Using password_hash column
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and verify_password(password, user['password_hash']):
            return user
        return None
    finally:
        conn.close()