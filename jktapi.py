from flask import Flask, jsonify, request, Response, g
from dbconnection import DBConnection  # Import the DBConnection class from dbconnection.py
from main import search_product

app = Flask(__name__)
app.debug = True

USERNAME = 'indra'
PASSWORD = 'indra'


# Define a function to get the database connection
def get_db():
    if 'db' not in g:
        g.db = DBConnection()  # Create a database connection if it doesn't exist in the context
    return g.db


# Close the database connection at the end of the request
@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.__exit__(None, None, None)  # Call the __exit__ method to close the connection


# Define a decorator for authentication
def requires_auth(f):
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    # Rename the decorated function to preserve the endpoint name
    decorated.__name__ = f.__name__
    return decorated


# Function to check authentication
def check_auth(username, password):
    return username == USERNAME and password == PASSWORD


# Function to request authentication
def authenticate():
    return Response('Authentication required', 401, {'WWW-Authenticate': 'Basic realm="Authentication Required"'})


# Define an API endpoint that requires authentication to retrieve the product data from the database
@app.route('/api/products', methods=['GET'])
@requires_auth
def get_products():
    db = get_db()  # Get the database connection from the context
    products = db.get_all_products()
    return jsonify(products)


@app.route('/api/search', methods=['GET'])
@requires_auth
def search_product_api():
    # Get the search key from the query parameters
    search_key = request.args.get('key')

    # Call the search_product function and store the results
    products = search_product(search_key)

    # Check if products were found
    if products:
        return jsonify(products)
    else:
        return jsonify({"message": "No products found for the given search key."}), 404


if __name__ == '__main__':
    app.run(debug=True)
