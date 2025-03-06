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