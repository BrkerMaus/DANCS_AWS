from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from models.product import get_products, add_product, edit_product, delete_product
from models.user import get_users
import hashlib
import math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = get_users()
        user_dict = {user['username']: user['password_hash'] for user in users}

        if username in user_dict and user_dict[username] == hashlib.sha256(password.encode()).hexdigest():
            session['logged_in'] = True
            session['username'] = username
            flash('You were successfully logged in')
            return redirect(url_for('inventory'))
        else:
            error = 'Invalid credentials. Please try again.'

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You were logged out')
    return redirect(url_for('index'))

@app.route('/inventory')
def inventory():
    if 'logged_in' not in session or not session['logged_in']:
        flash('Please log in to access the inventory.')
        return redirect(url_for('login'))
    
    page = request.args.get('page', 1, type=int)
    items_per_page = 10

    products = get_products()
    
    total_items = len(products)
    total_pages = math.ceil(total_items / items_per_page) 
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page

    inventory_items = products[start_index:end_index]

    return render_template(
        'inventory.html',
        inventory_items=inventory_items,
        current_page=page,
        total_pages=total_pages
    )
    
@app.route('/add-product', methods=['POST'])
def add_product_route():
    data = request.json
    name = data.get('name')
    category = data.get('category')
    quantity = data.get('quantity')
    price = data.get('price')
    status = data.get('status')

    if not all([name, category, quantity, price, status]):
        return jsonify({"error": "Missing required fields"}), 400

    add_product(name, category, quantity, price, status)
    return jsonify({"message": "Product added successfully!"}), 201
    
@app.route("/edit-product", methods=["POST"])
def edit_product_route():
    data = request.json
    edit_product(data["id"], data["name"], data["category"], data["quantity"], data["price"], data["status"])
    return jsonify({"message": "Product updated successfully"})


@app.route('/delete-product', methods=['POST'])
def delete_product_route():
    data = request.json
    product_id = data['id']
    
    delete_product(product_id)
    return jsonify({"message": "Product deleted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
