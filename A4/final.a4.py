from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Important for session management

# File paths for data storage
USERS_FILE = 'data/users.json'
PRODUCTS_FILE = 'data/products.json'

def load_users():
    """Load users from JSON file."""
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        
        # Check if file exists and is not empty
        if not os.path.exists(USERS_FILE) or os.path.getsize(USERS_FILE) == 0:
            # Create an empty list if file doesn't exist or is empty
            return []
        
        # Try to load the file
        with open(USERS_FILE, 'r') as f:
            content = f.read().strip()
            # If content is empty string, return empty list
            if not content:
                return []
            
            # Load JSON
            return json.loads(content)
    
    except json.JSONDecodeError:
        # If there's a JSON decoding error, return empty list
        return []
    except Exception as e:
        # Log any unexpected errors
        print(f"Error loading users: {e}")
        return []

def save_users(users):
    """Save users to JSON file."""
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        
        # Write users to file
        with open(USERS_FILE, 'w') as f:
            # Ensure we always write a valid JSON list, even if empty
            json.dump(users, f, indent=4)
    except Exception as e:
        print(f"Error saving users: {e}")

def load_products():
    """Load products from JSON file."""
    try:
        with open(PRODUCTS_FILE, 'r') as f:
            products = json.load(f)
            # Ensure each product has the required keys
            for product in products:
                if not all(key in product for key in ['id', 'name', 'price', 'quantity']):
                    raise ValueError("Incomplete product data")
            return products
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        # Default products if file doesn't exist or is malformed
        default_products = [
            {"id": 1, "name": "Vanilla Scoop", "price": 3.50, "quantity": 50},
            {"id": 2, "name": "Chocolate Delight", "price": 4.00, "quantity": 40},
            {"id": 3, "name": "Strawberry Swirl", "price": 4.50, "quantity": 30},
            {"id": 4, "name": "Mint Chocolate Chip", "price": 4.25, "quantity": 35}
        ]
        save_products(default_products)
        return default_products

def save_products(products):
    """Save products to JSON file."""
    os.makedirs(os.path.dirname(PRODUCTS_FILE), exist_ok=True)
    with open(PRODUCTS_FILE, 'w') as f:
        json.dump(products, f, indent=4)

@app.route('/')
def home():
    """Home page with product listing."""
    products = load_products()
    return render_template('home.html', products=products, username=session.get('username'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = load_users()
        
        # Check if username already exists
        if any(user['username'] == username for user in users):
            return render_template('register.html', error='Username already exists')
        
        # Add new user
        users.append({
            'username': username,
            'password': password  # Note: In a real app, you'd hash passwords
        })
        
        save_users(users)
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = load_users()
        
        # Check credentials
        for user in users:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                session['cart'] = []  # Initialize empty cart
                return redirect(url_for('home'))
        
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout route."""
    session.clear()
    return redirect(url_for('home'))

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Add product to cart."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    quantity = int(request.form['quantity'])
    products = load_products()
    
    # Find the product
    product = next((p for p in products if p['id'] == product_id), None)
    
    if product and product['quantity'] >= quantity:
        # Update product inventory
        product['quantity'] -= quantity
        save_products(products)
        
        # Add to cart
        cart_item = {
            'id': product_id,
            'name': product['name'],
            'price': product['price'],
            'quantity': quantity
        }
        
        if 'cart' not in session:
            session['cart'] = []
        
        session['cart'].append(cart_item)
        session.modified = True
    
    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    """View cart contents."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    
    return render_template('cart.html', cart=cart, total=total)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Checkout process."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    
    if request.method == 'POST':
        # Generate receipt
        receipt = {
            'username': session['username'],
            'items': cart,
            'total': total,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Clear cart after checkout
        session['cart'] = []
        session.modified = True
        
        return render_template('checkout.html', receipt=receipt)
    
    return render_template('checkout.html', cart=cart, total=total)

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    """Change user password route."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        
        users = load_users()
        
        for user in users:
            if user['username'] == session['username']:
                # Verify current password
                if user['password'] == current_password:
                    user['password'] = new_password
                    save_users(users)
                    return render_template('change_password.html', success=True)
                else:
                    return render_template('change_password.html', error='Incorrect current password')
    
    return render_template('change_password.html')

if __name__ == "__main__":
    app.run(debug=True)