from flask import Blueprint, jsonify, request, redirect, url_for, flash
from my_myproject.models import Loan, Book, Customer
from datetime import datetime
from my_myproject import db

loans = Blueprint('loans', __name__)

@loans.route('/loans', methods=['GET', 'POST'])
def new_loan():
    if request.method == 'POST':
        data = request.get_json()
        customer_id = data.get('customer_id')
        book_id = data.get('book_id')
        loan_type = data.get('loan_type')

        if not customer_id or not book_id or not loan_type:
            return jsonify({'error': 'All fields are required!'}), 400
        
        # Validate if the book is available
        book = Book.query.get(book_id)
        if book.available_quantity <= 0:
            return jsonify({'error': 'The book is not available for loan!'}), 400

        new_loan = Loan(customer_id=customer_id, book_id=book_id, loan_type=loan_type)
        new_loan.set_return_date()
        db.session.add(new_loan)
        
        # Decrease the available quantity of the book
        book.available_quantity -= 1
        db.session.commit()
        
        return jsonify({'message': 'Loan created successfully!'}), 201

    # If it's a GET request, we return the available books and customers for the frontend (if needed)
    books = Book.query.all()
    customers = Customer.query.all()

    books_list = [{'id': book.id, 'name': book.name} for book in books]
    customers_list = [{'id': customer.customer_id, 'name': f"{customer.first_name} {customer.last_name}"} for customer in customers]

    return jsonify({'books': books_list, 'customers': customers_list})


@loans.route('/loans/<int:loan_id>/update', methods=['GET', 'POST'])
def update_loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    
    if request.method == 'POST':
        data = request.get_json()
        loan.customer_id = data.get('customer_id')
        loan.book_id = data.get('book_id')
        loan.loan_type = data.get('loan_type')
        loan.date_of_loan = datetime.strptime(data.get('date_of_loan'), '%Y-%m-%d %H:%M:%S')
        loan.set_return_date()
        db.session.commit()
        return jsonify({"message": "Loan updated successfully!", "loan": {
            "loan_id": loan.id,
            "customer_id": loan.customer_id,
            "book_id": loan.book_id,
            "loan_type": loan.loan_type,
            "date_of_loan": loan.date_of_loan.strftime('%Y-%m-%d %H:%M:%S')
        }})

    books = Book.query.all()
    customers = Customer.query.all()

    books_list = [{'id': book.id, 'name': book.name} for book in books]
    customers_list = [{'id': customer.customer_id, 'name': f"{customer.first_name} {customer.last_name}"} for customer in customers]

    return jsonify({'loan': {
        "loan_id": loan.id,
        "customer_id": loan.customer_id,
        "book_id": loan.book_id,
        "loan_type": loan.loan_type,
        "date_of_loan": loan.date_of_loan.strftime('%Y-%m-%d %H:%M:%S')
    }, 'books': books_list, 'customers': customers_list})


@loans.route('/loans/<int:loan_id>/finish', methods=['POST'])
def finish_loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    if not loan.is_finished:
        loan.is_finished = True

        # Increase the available quantity of the book when the loan is finished
        book = Book.query.get(loan.book_id)
        book.available_quantity += 1

        db.session.commit()
        flash("Loan finished successfully!", "success")
    else:
        flash("This loan is already finished!", "warning")
    return redirect(url_for('loans.index'))
