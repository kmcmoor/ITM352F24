from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'simple_shop_key'

PRODUCTS = [
    {"id": 1, "name": "Chocolate chip ice cream", "price": 4.99},
    {"id": 2, "name": "Vanilla ice cream", "price": 2.99},
    {"id": 3, "name": "Cookie dough ice cream", "price": 3.99}
]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    session['username'] = username
    session['cart'] = []  # Initialize an empty cart
    return redirect(url_for('shop'))

@app.route('/shop')
def shop():
    if 'username' not in session:
        return redirect(url_for('home'))
    
    return render_template('shop.html', 
                           products=PRODUCTS, 
                           username=session['username'])

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'username' not in session:
        return redirect(url_for('home'))
    
    product_id = int(request.form['product_id'])
    # Find the product in the products list
    # next() finds the first matching product
    # None is returned if no product is found
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    
    if product:
        session['cart'] = session.get('cart', []) + [product]
        session.modified = True
    
    return redirect(url_for('shop'))

@app.route('/cart')
def cart():
    if 'username' not in session:
        return redirect(url_for('home'))
    
    # Calculate total
    total = sum(item['price'] for item in session.get('cart', []))
    
    # Pass the cart items and total to the template
    return render_template('cart.html', 
                           cart=session.get('cart', []), 
                           total=total)

if __name__ == "__main__":
    app.run(debug=True)