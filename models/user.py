from config import get_users_db_connection
from datetime import datetime

def get_users():
    connection = get_users_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT id, username, password_hash FROM users")
    users = cursor.fetchall()
    
    connection.close()
    return users

def create_user(username, password_hash):
    connection = get_users_db_connection()
    cursor = connection.cursor()
    
    query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
    cursor.execute(query, (username, password_hash))
    connection.commit()
    
    log_action(username, "User Created")
    connection.close()

def log_action(username, action):
    connection = get_users_db_connection()
    cursor = connection.cursor()
    
    query = "INSERT INTO audit_logs (username, action, timestamp) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, action, datetime.now()))
    connection.commit()
    
    connection.close()
