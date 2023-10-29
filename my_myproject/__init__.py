from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder="../../frontend/html", static_folder='../../frontend/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)

###Register blueprints###

# Import and register blueprints for different parts of the project
from my_myproject.books import books
from my_myproject.customers import customers
from my_myproject.loans import loans
from my_myproject.views import renders

# Register the blueprints with the Flask app
app.register_blueprint(books)
app.register_blueprint(customers)
app.register_blueprint(loans)
app.register_blueprint(renders)
