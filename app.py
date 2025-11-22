from flask import Flask, render_template, request

app = Flask(__name__)

# Menu dictionary
menu = {
    1: {"name": "Burger", "price": 100},
    2: {"name": "Pizza", "price": 250},
    3: {"name": "Sandwich", "price": 120},
    
    4: {"name": "Pasta", "price": 200},
    5: {"name": "French Fries", "price": 80},
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cart = []
        for key, item in menu.items():
            qty = request.form.get(f'item_{key}')
            if qty and int(qty) > 0:
                cart.append({"item": item["name"], "price": item["price"], "quantity": int(qty)})
        if cart:
            total = sum([i['price']*i['quantity'] for i in cart])
            return render_template('bill.html', cart=cart, total=total)
    return render_template('index.html', menu=menu)

if __name__ == "__main__":
    app.run(debug=True)
