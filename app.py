from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

# Correct MONGO_URI includes the database name "Stock_Db"
app.config["MONGO_URI"] = ""
mongo = PyMongo(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    stocks = list(mongo.db.stocks.find())
    total_cost = None
    selected_company = None
    shares = None

    if request.method == 'POST':
        selected_company = request.form.get('company')
        shares = int(request.form.get('shares', 0))
        stock = mongo.db.stocks.find_one({'name': selected_company})

        if stock:
            total_cost = shares * stock['price']

    return render_template("index.html", stocks=stocks,
                           total_cost=total_cost,
                           selected_company=selected_company,
                           shares=shares)

# API to insert a new company and price
@app.route('/add_stock', methods=['POST'])
def add_stock():
    data = request.get_json()

    name = data.get('name')
    price = data.get('price')

    if not name or price is None:
        return jsonify({"error": "Name and price are required"}), 400

    try:
        price = float(price)
    except ValueError:
        return jsonify({"error": "Invalid price format"}), 400

    # Insert into MongoDB
    mongo.db.stocks.insert_one({"name": name, "price": price})
    return jsonify({"message": "Stock added successfully!"}), 201

# API to fetch all stock prices
@app.route('/fetch_stock', methods=['GET'])
def fetch_stock():
    stocks = list(mongo.db.stocks.find({}, {'_id': 0}))  # exclude MongoDB _id field if not needed
    return jsonify({"stocks": stocks}), 200  # 200 OK for successful GET


if __name__ == '__main__':
    app.run(debug=True)
