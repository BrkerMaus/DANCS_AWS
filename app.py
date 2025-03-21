from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from models.product import get_products, add_product, edit_product, delete_product
from models.user import get_users, create_user, log_action
from track import generate_charts
import platform
import requests
import hashlib
import math

app = Flask(__name__)

app.secret_key = "bitte arbeiten, danke"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        existing_users = get_users()
        if any(user['username'].lower() == username.lower() for user in existing_users):
            flash('Username already exists. Please choose another one.', 'error')
            return redirect(url_for('register'))

        create_user(username, hashed_password)
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        users = get_users()
        user_dict = {user['username']: user['password_hash'] for user in users}

        if username in user_dict and user_dict[username] == hashed_password:
            session['logged_in'] = True
            session['username'] = username
            log_action(username, "Login")
            flash('You were successfully logged in')
            return redirect(url_for('inventory'))
        else:
            error = 'Invalid credentials. Please try again.'

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    username = session.get('username', 'Unknown')
    session.pop('logged_in', None)
    session.pop('username', None)
    log_action(username, "Logout")
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
    if not session.get("logged_in"):
        return jsonify({"error": "Unauthorized"}), 403
    
    try:
        data = request.json
        name = data.get("name", "").strip()
        category = data.get("category", "").strip()
        quantity = int(data.get("quantity", 0))
        price = float(data.get("price", 0))

        if not name or not category or quantity < 0 or price < 0:
            return jsonify({"success": False, "message": "Invalid input values"}), 400

        username = session.get("username", "Unknown")
        add_product(username, name, category, quantity, price, "Auto")

        return jsonify({"success": True, "message": "Product added successfully"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    
@app.route("/edit-product", methods=["POST"])
def edit_product_route():
    if not session.get("logged_in"):
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    username = session.get("username", "Unknown")

    edit_product(username, data["id"], data["name"], data["category"], data["quantity"], data["price"])
    return jsonify({"message": "Product updated successfully"})

@app.route('/delete-product', methods=['POST'])
def delete_product_route():
    if not session.get("logged_in"):
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    username = session.get("username", "Unknown")
    
    delete_product(username, data["id"])
    return jsonify({"message": "Product deleted successfully!"})

@app.route('/track')
def track():
    if 'logged_in' not in session or not session['logged_in']:
        flash("Please log in to access this page.")
        return redirect(url_for('login'))
    
    generate_charts() 
    return render_template('track.html')

@app.route('/user-info')
def user_info():
    try:
        ip_data = requests.get("https://ipinfo.io/json").json()
        ip = ip_data.get("ip", "Unknown")
        location = f"{ip_data.get('city', 'Unknown')}, {ip_data.get('country', 'Unknown')}"

        processor_info = platform.processor() or "Unknown Processor"
        os_info = platform.system() + " " + platform.release()

        return jsonify({
            "ip": ip,
            "location": location,
            "processor": processor_info,
            "os": os_info
        })
    except Exception as e:
        return jsonify({"error": str(e)})
    
if __name__ == '__main__':
    app.run(debug=True)
