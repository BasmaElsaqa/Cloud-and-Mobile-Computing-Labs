from flask import Flask, jsonify

app = Flask(__name__)

# In-memory product catalog [cite: 105]
PRODUCTS = {
    1: {"id": 1, "name": "Laptop", "price": 1200},
    2: {"id": 2, "name": "Phone", "price": 650},
    3: {"id": 3, "name": "Headphones", "price": 120}
}

@app.route("/health", methods=["GET"])
def health():
    # Cloud-native health check endpoint [cite: 110]
    return jsonify({"service": "product-service", "status": "up"}), 200

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    # Product lookup API [cite: 113]
    product = PRODUCTS.get(product_id)
    if product:
        return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404

if __name__ == "__main__":
    # Container listens on all interfaces (0.0.0.0) [cite: 100]
    app.run(host="0.0.0.0", port=5001)
