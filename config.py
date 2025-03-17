import mysql.connector

DB_CONFIG_PRODUCTS = {
    "host": "inventorydb.cz8w80wacvpb.ap-southeast-1.rds.amazonaws.com",
    "user": "admin",
    "password": "rootadmin",
    "database": "inventorydb"
}

DB_CONFIG_USERS = {
    "host": "inventorydb.cz8w80wacvpb.ap-southeast-1.rds.amazonaws.com",
    "user": "admin",
    "password": "rootadmin",
    "database": "userdb"
}

def get_products_db_connection():
    return mysql.connector.connect(**DB_CONFIG_PRODUCTS)

def get_users_db_connection():
    return mysql.connector.connect(**DB_CONFIG_USERS)

def setup_audit_logs():
    connection = get_users_db_connection() 
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255),
            action TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    connection.close()

setup_audit_logs()
