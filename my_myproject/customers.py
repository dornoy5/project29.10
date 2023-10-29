from flask import Blueprint, jsonify, redirect, request, url_for
from my_myproject.models import Customer
from my_myproject import db

customers = Blueprint('customers', __name__)

@customers.route('/customers',methods=['GET','POST'])
def get_customers():
    customers = Customer.query.all()

    customer_list = [{'customerID': customer.customer_id,
                    'first name': customer.first_name, 
                    'last name': customer.last_name,
                    'phone num': customer.phone_num,
                    'address': customer.address} for customer in customers]

    return jsonify({'customers': customer_list})

@customers.route('/customers', methods=['GET','POST'])
def new_customer():
    data = request.get_json()
    # Validate that required fields are present in the request data
    if 'customer_id' not in data or 'first_name' not in data or 'last_name' not in data or 'phone_num' not in data or 'address' not in data:
        return jsonify({'error': 'Required fields are missing in the request data (must be: customer id, first name, last name, phone num, address)'}, 400)
    
    customer_id= data['customer_id']
    first_name = data['first_name']
    last_name = data['last_name']
    phone_num = data['phone_num']
    address = data['address']

    existing_customer = Customer.query.filter_by(customer_id=customer_id).first()
    if existing_customer:
        return jsonify({'error': 'customer id is already in use'}), 400


    new_customer = Customer(customer_id=customer_id,
                            first_name=first_name,
                            last_name=last_name,
                            phone_num=phone_num,
                            address=address)
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer created successfully!'})
    
@customers.route('/customers/<int:customer_id>', methods=['GET', 'PUT'])
def update_customer(customer_id):
    data = request.get_json()
    customer = Customer.query.get_or_404(customer_id)
    
    if 'customer_id' in data:
        customer.customer_id = data['customer_id']
    if 'first_name' in data:
        customer.first_name = data['first_name']
    if 'last_name' in data:
        customer.last_name = data['last_name']
    if 'phone_num' in data:
        customer.phone_num = data['phone_num']
    if 'address' in data:
        customer.address = data['address']

    db.session.commit()
    
    return jsonify({'message': 'Customer updated successfully'})

@customers.route('/customers/<int:customer_id>', methods=['delete'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for('customers.index'))