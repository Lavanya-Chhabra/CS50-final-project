import sqlite3
import re
from flask import Flask, render_template, request, redirect, flash, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import rs, get_hex_color

app = Flask(__name__)
app.jinja_env.globals.update(rs=rs)
app.jinja_env.filters["colorhex"] = get_hex_color

# Secret key for session
app.secret_key = "super_secret_key_123"

# Database Connection Function
def get_db_connection():
    conn = sqlite3.connect("app.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "")
        password = request.form.get("password", "")
        confirmation = request.form.get("confirmation", "")

        if not email:
            flash("Email is required.", "error")
            return redirect("/signup")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Enter a valid email address.", "error")
            return redirect("/signup")
        
        if len(password) < 8:
            flash("Password must be at least 8 characters.", "error")
            return redirect("/signup")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            flash("Password must contain at least one special character.", "error")
            return redirect("/signup")
        
        if password != confirmation:
            flash("Passwords do not match.", "error")
            return redirect("/signup")
        
        else:
            try:
                with get_db_connection() as conn:

                    conn.execute("INSERT INTO users (email, hash, phone, name) VALUES (?, ?, ?, ?)",(email, generate_password_hash(password), phone, name))

                    conn.commit()

                    user = conn.execute("SELECT id FROM users WHERE email = ?",(email,)).fetchone()

                session["user_id"] = user["id"]
                flash("Successfully signed up!", "success")
                return redirect("/")

            except sqlite3.IntegrityError:
                flash("Email already registered.", "error")
                return redirect("/signup")

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        identifier = request.form.get("identifier", "").strip()
        password = request.form.get("password", "")

        if not identifier:
            flash("Email or phone is required.", "error")
            return redirect("/login")

        elif not password:
            flash("Password is required.", "error")
            return redirect("/login")
        
        else:
            with get_db_connection() as conn:

                user = conn.execute("SELECT id, hash FROM users WHERE email = ? OR phone = ?",(identifier, identifier)).fetchone()

            if user is None:
                flash("User not found.", "error")
                return redirect("/login")

            if not check_password_hash(user["hash"], password):
                flash("Incorrect password.", "error")
                return redirect("/login")

            session.clear()
            session["user_id"] = user["id"]

            flash("Logged in successfully!", "success")
            return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def logout():

    session.clear() 

    flash("Logged out successfully.", "success")
    return redirect("/")

@app.route("/")
def home():
    with get_db_connection() as conn:
        collection = conn.execute("SELECT p.id, p.name, p.price, p.sale_price, pi.image_url FROM products AS p JOIN product_images AS pi ON pi.product_id = p.id WHERE p.is_featured = 1 AND pi.type = 'f' ORDER BY RANDOM() LIMIT 3").fetchall()
        
        sale = conn.execute("SELECT p.id, p.name, p.price, p.sale_price, pi.image_url FROM products AS p JOIN product_images AS pi ON pi.product_id = p.id WHERE p.sale_price IS NOT NULL AND pi.type = 'f' ORDER BY RANDOM() LIMIT 3").fetchall()

        wishlist_ids = []
        if 'user_id' in session:
            rows = conn.execute("SELECT product_id FROM wishlist WHERE user_id = ?",(session['user_id'],)).fetchall()
            wishlist_ids = [row['product_id'] for row in rows]

        cart_ids = []
        if 'user_id' in session:
            rows = conn.execute("SELECT product_id FROM cart WHERE user_id = ?",(session['user_id'],)).fetchall()
            cart_ids = [row['product_id'] for row in rows]

    return render_template("index.html", coll=collection, sale=sale, wishlist_ids=wishlist_ids, cart_ids=cart_ids)

@app.route("/shop")
def shop():
    with get_db_connection() as conn:
        products = conn.execute("SELECT p.id, p.name, p.price, p.sale_price, pi.image_url FROM products AS p JOIN product_images AS pi ON pi.product_id = p.id WHERE pi.type = 'f' ORDER BY RANDOM() LIMIT 27").fetchall()

        wishlist_ids = []
        if 'user_id' in session:
            rows = conn.execute("SELECT product_id FROM wishlist WHERE user_id = ?",(session['user_id'],)).fetchall()
            wishlist_ids = [row['product_id'] for row in rows]

        cart_ids = []
        if 'user_id' in session:
            rows = conn.execute("SELECT product_id FROM cart WHERE user_id = ?",(session['user_id'],)).fetchall()
            cart_ids = [row['product_id'] for row in rows]

    return render_template("shop.html", products=products, wishlist_ids=wishlist_ids, cart_ids=cart_ids)

@app.route("/dresses")
def dresses():
    with get_db_connection() as conn:
        products = conn.execute("SELECT p.id, p.name, p.price, p.sale_price, pi.image_url FROM products AS p JOIN product_images AS pi ON pi.product_id = p.id WHERE pi.type = 'f' AND p.category_id = 1 ORDER BY RANDOM() LIMIT 9").fetchall()
        wishlist_ids = []
        if 'user_id' in session:
            rows = conn.execute("SELECT product_id FROM wishlist WHERE user_id = ?",(session['user_id'],)).fetchall()
            wishlist_ids = [row['product_id'] for row in rows]

        cart_ids = []
        if 'user_id' in session:
            rows = conn.execute("SELECT product_id FROM cart WHERE user_id = ?",(session['user_id'],)).fetchall()
            cart_ids = [row['product_id'] for row in rows]

    return render_template("dresses.html", products=products, wishlist_ids=wishlist_ids, cart_ids=cart_ids)

@app.route("/coord-sets")
def coord():
    with get_db_connection() as conn:
        products = conn.execute("SELECT p.id, p.name, p.price, p.sale_price, pi.image_url FROM products AS p JOIN product_images AS pi ON pi.product_id = p.id WHERE pi.type = 'f' AND p.category_id = 2 ORDER BY RANDOM() LIMIT 6").fetchall()

        wishlist_ids = []
        if 'user_id' in session:
            rows = conn.execute("SELECT product_id FROM wishlist WHERE user_id = ?",(session['user_id'],)).fetchall()
            wishlist_ids = [row['product_id'] for row in rows]

        cart_ids = []
        if 'user_id' in session:
            rows = conn.execute("SELECT product_id FROM cart WHERE user_id = ?",(session['user_id'],)).fetchall()
            cart_ids = [row['product_id'] for row in rows]

    return render_template("coord-sets.html", products=products, wishlist_ids=wishlist_ids, cart_ids=cart_ids)

@app.route("/jeans")
def jeans():
    with get_db_connection() as conn:
        products = conn.execute("SELECT p.id, p.name, p.price, p.sale_price, pi.image_url FROM products AS p JOIN product_images AS pi ON pi.product_id = p.id WHERE pi.type = 'f' AND p.category_id = 3 ORDER BY RANDOM() LIMIT 6").fetchall()

        wishlist_ids = []
        if 'user_id' in session:
            rows = conn.execute("SELECT product_id FROM wishlist WHERE user_id = ?",(session['user_id'],)).fetchall()
            wishlist_ids = [row['product_id'] for row in rows]

        cart_ids = []
        if 'user_id' in session:
            rows = conn.execute("SELECT product_id FROM cart WHERE user_id = ?",(session['user_id'],)).fetchall()
            cart_ids = [row['product_id'] for row in rows]

    return render_template("jeans.html", products=products, wishlist_ids=wishlist_ids, cart_ids=cart_ids)

@app.route("/tops")
def tops():
    with get_db_connection() as conn:
        products = conn.execute("SELECT p.id, p.name, p.price, p.sale_price, pi.image_url FROM products AS p JOIN product_images AS pi ON pi.product_id = p.id WHERE pi.type = 'f' AND p.category_id = 4 ORDER BY RANDOM() LIMIT 6").fetchall()

        wishlist_ids = []
        if 'user_id' in session:
            rows = conn.execute("SELECT product_id FROM wishlist WHERE user_id = ?",(session['user_id'],)).fetchall()
            wishlist_ids = [row['product_id'] for row in rows]

        cart_ids = []
        if 'user_id' in session:
            rows = conn.execute("SELECT product_id FROM cart WHERE user_id = ?",(session['user_id'],)).fetchall()
            cart_ids = [row['product_id'] for row in rows]

    return render_template("tops.html", products=products, wishlist_ids=wishlist_ids, cart_ids=cart_ids)

@app.route('/product/<int:id>')
def product_detail(id):
    with get_db_connection() as conn:
        product = conn.execute("SELECT p.id, p.name, p.description, p.price, p.sale_price, pd.style, pd.fit, pd.color, pd.fabric, pd.strechability, pd.fabric, pd.length, pd.ratings FROM products AS p JOIN product_details AS pd ON pd.product_id = p.id WHERE p.id = ? LIMIT 1", (id,)).fetchall()
        images = conn.execute("SELECT image_url FROM product_images WHERE product_id = ? ORDER BY id", (id,)).fetchall()
        sizes = ['XS', 'S', 'M', 'L', 'XL']

        wishlist_ids = []
        if 'user_id' in session:
            rows = conn.execute("SELECT product_id FROM wishlist WHERE user_id = ?",(session['user_id'],)).fetchall()
            wishlist_ids = [row['product_id'] for row in rows]

        cart_ids = []
        if 'user_id' in session:
            rows = conn.execute("SELECT product_id FROM cart WHERE user_id = ?",(session['user_id'],)).fetchall()
            cart_ids = [row['product_id'] for row in rows]

    return render_template("product.html", product=product, images=images, sizes=sizes, wishlist_ids=wishlist_ids, cart_ids=cart_ids)

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    with get_db_connection() as conn:
        user = conn.execute("SELECT * FROM users WHERE id=?",(session["user_id"],)).fetchone()

    return render_template("dashboard.html", user=user)

@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/login")
    
    with get_db_connection() as conn:
        user = conn.execute("SELECT * FROM users WHERE id=?",(session["user_id"],)).fetchone()

    return render_template("profile.html", user=user)

@app.route("/orders")
def orders():

    if "user_id" not in session:
        return redirect("/login")

    with get_db_connection() as conn:
        orders = conn.execute("SELECT * FROM orders WHERE user_id=? ORDER BY id DESC",(session["user_id"],)).fetchall()

    return render_template("orders.html", orders=orders)

@app.route("/order/<int:order_id>")
def order_detail(order_id):

    if "user_id" not in session:
        return redirect("/login")

    with get_db_connection() as conn:
        items = conn.execute("SELECT p.id, p.name, p.price, p.sale_price, pi.image_url, oi.order_id, oi.quantity FROM order_items AS oi JOIN products AS P ON p.id = oi.product_id JOIN product_images AS pi ON pi.product_id = p.id WHERE oi.order_id = ? AND pi.type='f'",(order_id,)).fetchall()

    grand_total = sum(item["price"] * item["quantity"] for item in items)

    return render_template("order_detail.html", items=items, order_id=order_id, grand_total=grand_total)

@app.route("/edit-profile", methods=["GET","POST"])
def edit_profile():

    if "user_id" not in session:
        return redirect("/login")

    with get_db_connection() as conn:
        if request.method == "POST":

            name = request.form["name"]
            email = request.form["email"]
            phone = request.form["phone"]

            conn.execute("UPDATE users SET name=?, email=?, phone=? WHERE id=?",(name,email,phone,session["user_id"]))

            conn.commit()

            return redirect(url_for("profile"))

        user = conn.execute("SELECT * FROM users WHERE id=?",(session["user_id"],)).fetchone()

    return render_template("edit_profile.html", user=user)

@app.route('/wishlist')
def wishlist():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    with get_db_connection() as conn:
        products = conn.execute("SELECT * FROM products JOIN product_images ON product_images.product_id = products.id JOIN wishlist ON products.id = wishlist.product_id WHERE product_images.type = 'f' AND wishlist.user_id = ?", (session['user_id'],)).fetchall()

        cart_ids = []
        if 'user_id' in session:
            rows = conn.execute("SELECT product_id FROM cart WHERE user_id = ?",(session['user_id'],)).fetchall()
            cart_ids = [row['product_id'] for row in rows]

    return render_template("wishlist.html", products=products, cart_ids=cart_ids)


@app.route('/toggle_wishlist/<int:product_id>', methods=['POST'])
def toggle_wishlist(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    with get_db_connection() as conn:

        existing = conn.execute("SELECT * FROM wishlist WHERE user_id = ? AND product_id = ?",(user_id, product_id)).fetchone()

        if existing:
            conn.execute("DELETE FROM wishlist WHERE user_id = ? AND product_id = ?",(user_id, product_id))
        else:
            conn.execute("INSERT INTO wishlist (user_id, product_id) VALUES (?, ?)",(user_id, product_id))

        conn.commit()

    return redirect(request.referrer)

@app.route("/cart")
def cart():

    if 'user_id' not in session:
        return redirect(url_for('login'))

    with get_db_connection() as conn:

        products = conn.execute("SELECT cart.id as cart_id, p.id as product_id, p.name, COALESCE(p.sale_price, p.price) AS final_price, pi.image_url, cart.quantity, cart.size FROM cart JOIN products AS p ON p.id = cart.product_id JOIN product_images AS pi ON pi.product_id = p.id WHERE pi.type = 'f' AND cart.user_id = ? ORDER BY cart.id DESC", (session['user_id'],)).fetchall()
        
        subtotal = sum(item['final_price'] * item['quantity'] for item in products)

    return render_template(
        "cart.html", products=products, subtotal=subtotal)

@app.route('/toggle_cart/<int:product_id>', methods=['POST'])
def toggle_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    with get_db_connection() as conn:
        existing = conn.execute(
            "SELECT * FROM cart WHERE user_id = ? AND product_id = ?",
            (user_id, product_id)
        ).fetchone()

        if existing:
            conn.execute("DELETE FROM cart WHERE user_id = ? AND product_id = ?",(user_id, product_id))
        else:
            conn.execute("INSERT INTO cart (user_id, product_id) VALUES (?, ?)",(user_id, product_id))

        conn.commit()

    return redirect(request.referrer)

@app.route("/update_cart/<int:cart_id>", methods=["POST"])
def update_cart(cart_id):

    if 'user_id' not in session:
        return redirect(url_for('login'))

    quantity = int(request.form.get("quantity", 1))
    size = request.form.get("size", "XS")

    if quantity < 1:
        quantity = 1

    with get_db_connection() as conn:

        conn.execute("UPDATE cart SET quantity = ?, size = ? WHERE id = ? AND user_id = ?", (quantity, size, cart_id, session['user_id']))

        conn.commit()

    return redirect(url_for('cart'))

@app.route("/remove_from_cart/<int:cart_id>", methods=["POST"])
def remove_from_cart(cart_id):

    if 'user_id' not in session:
        return redirect(url_for('login'))

    with get_db_connection() as conn:

        conn.execute("DELETE FROM cart WHERE id = ? AND user_id = ?", (cart_id, session['user_id']))

        conn.commit()

    return redirect(url_for('cart'))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    conn = get_db_connection()

    # SAVE NEW ADDRESS

    if request.method == "POST":

        full_name = request.form.get("full_name")
        phone = request.form.get("phone")
        address = request.form.get("address")
        city = request.form.get("city")
        pincode = request.form.get("pincode")

        if full_name and phone and address and city and pincode:

            conn.execute("INSERT INTO addresses (user_id, full_name, phone, address, city, pincode) VALUES (?,?,?,?,?,?)",(user_id, full_name, phone, address, city, pincode))

            conn.commit()

            flash("Address added successfully", "success")

            return redirect(url_for("checkout"))

        else:
            flash("Please fill complete address", "error")

    # CART ITEMS

    cart_items = conn.execute("SELECT cart.*, products.name, products.price FROM cart JOIN products ON cart.product_id = products.id WHERE cart.user_id = ?",(user_id,)).fetchall()


    if not cart_items:
        conn.close()
        return redirect(url_for("cart"))


    subtotal = sum(item["price"] * item["quantity"] for item in cart_items)

    # GET ADDRESSES

    addresses = conn.execute("SELECT * FROM addresses WHERE user_id = ? ORDER BY id DESC",(user_id,)).fetchall()

    conn.close()

    return render_template("checkout.html", cart_items=cart_items, subtotal=subtotal, addresses=addresses)

@app.route("/place_order", methods=["POST"])
def place_order():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    address_id = request.form.get("address_id")

    if not address_id:
        flash("Please select an address", "error")
        return redirect(url_for("checkout"))

    conn = get_db_connection()

    cart_items = conn.execute("SELECT cart.*, products.price FROM cart JOIN products ON cart.product_id = products.id WHERE cart.user_id = ?",(user_id,)).fetchall()

    if not cart_items:
        conn.close()
        return redirect(url_for("cart"))

    subtotal = sum(item["price"] * item["quantity"] for item in cart_items)

    # CREATE ORDER

    cursor = conn.execute("INSERT INTO orders (user_id, address_id, total_amount) VALUES (?,?,?)",(user_id, address_id, subtotal))

    order_id = cursor.lastrowid

    # INSERT ORDER ITEMS

    for item in cart_items:

        conn.execute("INSERT INTO order_items (order_id, product_id, size, quantity, price) VALUES (?,?,?,?,?)",(order_id, item["product_id"], item["size"], item["quantity"], item["price"]))

    # CLEAR CART

    conn.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("order_success", order_id=order_id))

@app.route("/order_success/<int:order_id>")
def order_success(order_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("order_success.html", order_id=order_id)

if __name__ == "__main__":
    app.run(debug=True)
