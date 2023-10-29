from flask import Blueprint, render_template 

renders = Blueprint('renders', __name__)

@renders.route('/')
def index():
    return render_template('index.html')

@renders.route('/books')
def books_page():
    return render_template('books.html')

@renders.route('/loans')
def loans_page():
    return render_template('loans.html')

@renders.route('/customers')
def customers_page():
    return render_template('customers.html')

# Route to serve static image files from the 'img' dir
@renders.route('/../static/img/<image_filename>')
def serve_image(image_filename):
    return renders.send_static_file('img/' + image_filename)