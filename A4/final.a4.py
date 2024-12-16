#final.a4.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
import time
from datetime import datetime  # Add this new import

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# File paths for data storage
USERS_FILE = 'data/users.json'
PRODUCTS_FILE = 'data/products.json'
RECEIPTS_FILE = 'data/receipts.json'  # Add this new constant

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
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        
        # Path to products file
        products_path = os.path.join('data', 'products.json')
        
        # If file doesn't exist or is empty, create default products
        if not os.path.exists(products_path) or os.path.getsize(products_path) == 0:
            default_products = [
                {"id": 1, "name": "Vanilla Scoop", "price": 3.50, "quantity": 50},
                {"id": 2, "name": "Chocolate Delight", "price": 4.00, "quantity": 40},
                {"id": 3, "name": "Strawberry Swirl", "price": 4.50, "quantity": 30},
                {"id": 4, "name": "Mint Chocolate Chip", "price": 4.25, "quantity": 35}
            ]
            
            # Write default products to file
            with open(products_path, 'w') as f:
                json.dump(default_products, f, indent=4)
            
            return default_products
        
        # Load products from file
        with open(products_path, 'r') as f:
            products = json.load(f)
            
            # Validate products have required keys
            for product in products:
                if not all(key in product for key in ['id', 'name', 'price', 'quantity']):
                    raise ValueError("Incomplete product data")
            
            return products
    
    except Exception as e:
        print(f"Error loading products: {e}")
        # Fallback to default products if loading fails
        default_products = [
            {"id": 1, "name": "Vanilla Scoop", "price": 3.50, "quantity": 50},
            {"id": 2, "name": "Chocolate Delight", "price": 4.00, "quantity": 40},
            {"id": 3, "name": "Strawberry Swirl", "price": 4.50, "quantity": 30},
            {"id": 4, "name": "Mint Chocolate Chip", "price": 4.25, "quantity": 35}
        ]
        
        # Write default products to file
        products_path = os.path.join('data', 'products.json')
        with open(products_path, 'w') as f:
            json.dump(default_products, f, indent=4)
        
        return default_products

def save_products(products):
    """Save products to JSON file."""
    os.makedirs(os.path.dirname(PRODUCTS_FILE), exist_ok=True)
    with open(PRODUCTS_FILE, 'w') as f:
        json.dump(products, f, indent=4)

def load_receipts():
    """Load receipts from JSON file."""
    try:
        os.makedirs(os.path.dirname(RECEIPTS_FILE), exist_ok=True)
        if not os.path.exists(RECEIPTS_FILE) or os.path.getsize(RECEIPTS_FILE) == 0:
            return []
        with open(RECEIPTS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading receipts: {e}")
        return []

def save_receipt(receipt):
    """Save a new receipt to the receipts file."""
    try:
        receipts = load_receipts()
        receipts.append(receipt)
        os.makedirs(os.path.dirname(RECEIPTS_FILE), exist_ok=True)
        with open(RECEIPTS_FILE, 'w') as f:
            json.dump(receipts, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving receipt: {e}")
        return False

def update_product_quantities(cart):
    """Update product quantities after successful purchase."""
    try:
        products = load_products()
        for cart_item in cart:
            for product in products:
                if product['id'] == cart_item['id']:
                    # Quantity was already decremented when adding to cart,
                    # so we don't need to decrement it again
                    pass
        save_products(products)
        return True
    except Exception as e:
        print(f"Error updating product quantities: {e}")
        return False

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
                session['cart'] = []  # Explicitly initialize as an empty list
                session.modified = True  # Ensure the session is marked as modified
                return redirect(url_for('home'))
        
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/debug_session')
def debug_session():
    """Debug route to print session contents"""
    print("Debug Session:")
    print("Username:", session.get('username'))
    print("Cart:", session.get('cart'))
    return "Check your console"

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
        
        # Ensure cart exists and is a list
        if 'cart' not in session or not isinstance(session['cart'], list):
            session['cart'] = []
        
        session['cart'].append(cart_item)
        session.modified = True
        
        # Add a flash message
        flash(f'{quantity} {product["name"]} added to cart!', 'success')
    
    return redirect(url_for('home'))

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
    if 'username' not in session:
        flash('Please log in to checkout', 'error')
        return redirect(url_for('login'))
    
    cart = session.get('cart', [])
    if not cart:
        flash('Your cart is empty', 'error')
        return redirect(url_for('home'))
    
    total = sum(item['price'] * item['quantity'] for item in cart)
    
    if request.method == 'POST':
        receipt = {
            'receipt_id': f"REC-{int(time.time())}",
            'username': session['username'],
            'items': cart,  # Make sure this is a list
            'total': total,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        print("Generated Receipt:", receipt)  # Debug print
        
        # Save receipt
        save_receipt(receipt)
        
        # Update product quantities
        update_product_quantities(cart)
        
        # Clear the cart
        session['cart'] = []
        session.modified = True
        
        # Explicitly pass items to the template
        return render_template('checkout.html', 
                               receipt_id=receipt['receipt_id'], 
                               username=receipt['username'], 
                               items=cart,  # Pass cart items directly 
                               total=total, 
                               timestamp=receipt['timestamp'])
    
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