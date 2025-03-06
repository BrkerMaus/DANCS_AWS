from config import get_products_db_connection

def get_products():
    connection = get_products_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT id, name, category, quantity, price, status FROM products")
    products = cursor.fetchall()
    
    connection.close()
    return products

def add_product(name, category, quantity, price, status):
    """Adds a new product to the database."""
    connection = get_products_db_connection()
    cursor = connection.cursor()
    
    query = """
        INSERT INTO products (name, category, quantity, price, status) 
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (name, category, quantity, price, status))
    connection.commit()
    
    connection.close()
    
def edit_product(product_id, name, category, quantity, price, status):
    try:
        connection = get_products_db_connection()
        cursor = connection.cursor()

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
    """Deletes a product from the database."""
    connection = get_products_db_connection()
    cursor = connection.cursor()
    
    query = "DELETE FROM products WHERE id = %s"
    cursor.execute(query, (product_id,))
    connection.commit()
    
    connection.close()

