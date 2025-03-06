from config import get_users_db_connection

def get_users():
    connection = get_users_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT id, username, password_hash FROM users")
    users = cursor.fetchall()
    
    connection.close()
    return users