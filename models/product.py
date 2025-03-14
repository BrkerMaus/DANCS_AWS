from config import get_products_db_connection

def get_products():
    connection = get_products_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT id, name, category, quantity, price FROM products")
    products = cursor.fetchall()
    
    for product in products:
        quantity = product["quantity"]
        if quantity > 20:
            product["status"] = "Available"
        elif 0 < quantity <= 20:
            product["status"] = "Low Stock"
        else:
            product["status"] = "Out of Stock"
    
    connection.close()
    return products

def add_product(name, category, quantity, price, status):
    connection = get_products_db_connection()
    cursor = connection.cursor()
    
    query = """
        INSERT INTO products (name, category, quantity, price, status) 
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (name, category, quantity, price, status))
    connection.commit()
    
    connection.close()
    
def edit_product(product_id, name, category, quantity, price):
    try:
        connection = get_products_db_connection()
        cursor = connection.cursor()
        if quantity > 20:
            status = "Available"
        elif 0 < quantity <= 20:
            status = "Low Stock"
        else:
            status = "Out of Stock"

        query = """
            UPDATE products 
            SET name = %s, category = %s, quantity = %s, price = %s, status = %s 
            WHERE id = %s
        """
        cursor.execute(query, (name, category, quantity, price, status, product_id))
        connection.commit()
        print("Product updated successfully")
    except Exception as e:
        print("Error updating product:", str(e))
    finally:
        connection.close()

def delete_product(product_id):
    connection = get_products_db_connection()
    cursor = connection.cursor()
    
    query = "DELETE FROM products WHERE id = %s"
    cursor.execute(query, (product_id,))
    connection.commit()
    
    connection.close()
