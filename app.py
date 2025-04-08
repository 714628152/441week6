# I'm Friday
# Import necessary modules from Flask and Flask-SQLAlchemy
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

# Create a Flask application instance
app = Flask(__name__)

# Import the os module to work with the operating system
import os

# Get the absolute path of the directory where the current file is located
basedir = os.path.abspath(os.path.dirname(__file__))

# Configure the SQLAlchemy database URI to use a SQLite database file named 'items.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'items.db')

# Disable SQLAlchemy's modification tracking to reduce memory usage
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy database instance
db = SQLAlchemy(app)

# Define the Item model, which represents a table in the database
class Item(db.Model):
    # Define the columns of the Item table
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    name = db.Column(db.String(100), nullable=False)  # Name column, cannot be null
    description = db.Column(db.String(200), nullable=False)  # Description column, cannot be null
    price = db.Column(db.Float, nullable=False)  # Price column, cannot be null
    quantity = db.Column(db.Integer, nullable=False)  # Quantity column, cannot be null

# Create the database tables within the application context
with app.app_context():
    db.create_all()

# Define the route for the home page, which renders the 'index.html' template
@app.route('/')
def home():
    return render_template('index.html')

# Define the route for adding a new item via a POST request to '/api/items'
@app.route('/api/items', methods=['POST'])
def add_item():
    # Get the JSON data from the request
    data = request.get_json()
    
    # Create a new Item instance with the data from the request
    new_item = Item(name=data['name'], description=data['description'], price=data['price'], quantity=data['quantity'])
    
    # Add the new item to the database session
    db.session.add(new_item)
    
    # Commit the changes to the database
    db.session.commit()
    
    # Return a JSON response with a success message and the details of the added item
    return jsonify({'message': 'Item added successfully', 'item': {
        'id': new_item.id,
        'name': new_item.name,
        'description': new_item.description,
        'price': new_item.price,
        'quantity': new_item.quantity
    }}), 201  # HTTP status code 201 indicates resource creation

# Define the route for retrieving the list of items via a GET request to '/api/items'
@app.route('/api/items', methods=['GET'])
def list_items():
    # Query all items from the Item table
    items = Item.query.all()
    
    # Create a list of dictionaries representing the items
    items_list = [{'id': item.id, 'name': item.name, 'description': item.description, 'price': item.price, 'quantity': item.quantity} for item in items]
    
    # Return a JSON response with the list of items
    return jsonify(items_list), 200  # HTTP status code 200 indicates a successful request

# Check if the script is executed directly (not imported as a module)
if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)