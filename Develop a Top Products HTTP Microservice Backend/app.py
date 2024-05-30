from flask import Flask, request, jsonify
import requests
import uuid

app = Flask(__name__)

# Mock data store for products
products_store = {}

# Function to generate unique product ID
def generate_product_id():
    return str(uuid.uuid4())

# Function to add product to the mock data store
def add_product(company, category, product):
    if company not in products_store:
        products_store[company] = {}
    if category not in products_store[company]:
        products_store[company][category] = []
    products_store[company][category].append(product)

# Function to fetch top products from a specific company and category
def fetch_top_products(company, category, n):
    # Mock API URL for fetching products
    api_url = f"http://20.244.56.144/test/companies/{company}/categories/{category}/products?top={n}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

@app.route('/categories/<string:categoryname>/products', methods=['GET'])
def get_top_products(categoryname):
    n = int(request.args.get('n', 10))  # Get number of products (default: 10)
    page = int(request.args.get('page', 1))  # Get page number (default: 1)
    sort_by = request.args.get('sort_by', 'rating')  # Get sorting parameter (default: rating)
    sort_order = request.args.get('sort_order', 'desc')  # Get sorting order (default: descending)
    min_price = float(request.args.get('min_price', 0))  # Get minimum price (default: 0)
    max_price = float(request.args.get('max_price', float('inf')))  # Get maximum price (default: infinity)

    # Provided product data
    products = [
        {"productName": "Laptop 1", "price": 2236, "rating": 4.7, "discount": 63, "availability": "yes"},
        {"productName": "Laptop 13", "price": 1244, "rating": 4.5, "discount": 45, "availability": "out-of-stock"},
        {"productName": "Laptop 3", "price": 9102, "rating": 4.44, "discount": 98, "availability": "out-of-stock"},
        {"productName": "Laptop 11", "price": 2652, "rating": 4.12, "discount": 70, "availability": "yes"},
        {"productName": "Laptop 4", "price": 1258, "rating": 3.8, "discount": 33, "availability": "yes"},
        {"productName": "Laptop 13", "price": 8686, "rating": 3.22, "discount": 24, "availability": "out-of-stock"},
        {"productName": "Laptop 14", "price": 9254, "rating": 3, "discount": 56, "availability": "yes"},
        {"productName": "Laptop 1", "price": 1059, "rating": 2.77, "discount": 21, "availability": "yes"},
        {"productName": "Laptop 10", "price": 7145, "rating": 2.74, "discount": 15, "availability": "yes"},
        {"productName": "Laptop 10", "price": 4101, "rating": 2.67, "discount": 37, "availability": "out-of-stock"}
    ]

    # Filter products based on price range
    filtered_products = [product for product in products if min_price <= product['price'] <= max_price]

    # Sort products based on sorting parameters
    filtered_products.sort(key=lambda x: x[sort_by], reverse=(sort_order == 'desc'))

    # Paginate the results
    start_index = (page - 1) * n
    end_index = start_index + n
    paginated_products = filtered_products[start_index:end_index]

    return jsonify(paginated_products)

@app.route('/categories/<string:categoryname>/products/<string:productid>', methods=['GET'])
def get_product_details(categoryname, productid):
    # Find product with the given ID
    for company, categories in products_store.items():
        for category, products in categories.items():
            for product in products:
                if product['id'] == productid:
                    return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
