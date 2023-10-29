from flask import Blueprint, request, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from my_myproject.models import Book
db=SQLAlchemy()


books = Blueprint('books', __name__)

# Route to retrieve all books
@books.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()

    book_list = [{'bookID': book.id, 'title': book.title, 'author': book.author, 'publication year': book.publishedYear, 'status': book.status, 'book Type': book.bookType, 'quantity': book.quantity, 'available_quantity': book.available_quantity} for book in books]

    return jsonify({'books': book_list})

@books.route('/books', methods=['POST'])
def new_books():
    data = request.get_json()

    # Validate that required fields are present in the request data
    if 'title' not in data or 'author' not in data or 'publishedYear' not in data or 'bookType' not in data:
        return jsonify({'error': 'Required fields are missing in the request data (must be: title, author, publishedYear, and bookType)'}, 400)
    
    title = data['title']
    author = data['author']
    publishedYear = data['publishedYear']
    bookType = data['bookType']
    
    # Validate that the title is not an empty string
    if not title:
        return jsonify({'error': 'Title cannot be empty.'}), 400

    #Validation for bookType
    if bookType not in [1, 2, 3]:
        return jsonify({'error': 'Invalid bookType. It must be 1, 2, or 3'}, 400)
    quantity = data.get('quantity', 1)
    new_book = Book(title=title, author=author, publishedYear=publishedYear, bookType=bookType, quantity=quantity, available_quantity=quantity)
    db.session.add(new_book)
    db.session.commit()

    return jsonify({'message': 'Book created successfully!'})

@books.route('/books/<int:book_id>/update', methods=['GET', 'POST'])
def update_book(bookID):
    data = request.get_json()
    new_title = data.get('title')
    new_author = data.get('author')
    new_publishedYear = data.get('publishedYear')
    new_bookType = data.get('bookType')
    new_quantity = data.get('quantity')
    new_available_quantity = data.get('available_quantity')

    # validate that this book exists
    book = Book.query.get(bookID)
    if book:
        #check for each object if exists, to allow edit just some of the book objects
        if new_title is not None:
            book.title = new_title
        if new_author is not None:
            book.author = new_author
        if new_publishedYear is not None:
            book.publishedYear = new_publishedYear
        if new_bookType is not None:
            book.bookType = new_bookType
        if new_quantity is not None:
            book.quantity = new_quantity
        if new_available_quantity is not None:
            book.available_quantity = new_available_quantity

        db.session.commit()

        return jsonify({'message': 'Book updated successfully'})
    else:
        return jsonify({'error': 'Book not found'}, 404)

@books.route('/books/<int:bookID>', methods=['DELETE'])
def delete_book(bookID):
    #check if the book exists
    book = Book.query.get(bookID)
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully'})
    else:
        return jsonify({'error': 'Book not found'}, 404)