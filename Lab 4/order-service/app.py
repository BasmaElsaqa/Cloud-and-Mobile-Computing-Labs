import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Config via Environment variable (12-Factor App Principle #3) [cite: 149]
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:5001")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"service": "order-service", "status": "up"}), 200

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    # Call product-service [cite: 150]
    try:
        response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}", timeout=2)
        if response.status_code == 200:
            product = response.json()
            total_price = product["price"] * quantity
            return jsonify({
                "message": "Order created",
                "product": product["name"],
                "total_price": total_price
            }), 201
        return jsonify({"error": "Product not found"}), 404
    except requests.exceptions.RequestException:
        return jsonify({"error": "product-service unavailable"}), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
