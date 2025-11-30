from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime
import json

app = Flask(__name__)

# --- DATABASE SETUP ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Order table
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items = db.Column(db.String(1000))   # saved as JSON list
    total = db.Column(db.Integer)
    date = db.Column(db.String(50))

with app.app_context():
    db.create_all()

# --- MENU ---
menu = {
    1: {"name": "Burger", "price": 100},
    2: {"name": "Pizza", "price": 250},
    3: {"name": "Sandwich", "price": 120},
    4: {"name": "Pasta", "price": 200},
    5: {"name": "French Fries", "price": 80},
}

# --- HOME PAGE ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        cart = []
        items_list = []

        for key, item in menu.items():
            qty = request.form.get(f"item_{key}")
            if qty and int(qty) > 0:
                cart.append({
                    "item": item["name"],
                    "price": item["price"],
                    "quantity": int(qty)
                })
                items_list.append({"name": item["name"], "qty": int(qty)})

        if cart:
            total = sum(i["price"] * i["quantity"] for i in cart)
            date_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

            # --- SAVE ORDER TO DB ---
            new_order = Order(
                items=json.dumps(items_list),
                total=total,
                date=date_time
            )
            db.session.add(new_order)
            db.session.commit()

            # Pass bill no to bill.html
            return render_template("bill.html", cart=cart, total=total, billNo=new_order.id)

    return render_template("index.html", menu=menu)

# --- RUN APP ---
if __name__ == "__main__":
    app.run(debug=True)

