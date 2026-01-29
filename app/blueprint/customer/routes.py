from flask import jsonify, request
from app.models import Customer
from app.extensions import db
from . import customer_bp
from .schemas import customer_schema, customer_schema


# Create Customer
def create_customer():
    data = request.get_json()
    customer: Customer = customer_schema.load(data)

    db.session.add(customer)
    db.session.commit()
    
    return customer_schema.jsonify(customer), 201


# Read Customer
def test_customer():
    return jsonify(
        {
            'message': 'Customer bluepront is working!'
        }
    )

# Read All Customers
def get_customer():
    customers = Customer.query.all()
    return customer_schema.jsonify(customers)

# Read One Customer
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return customer_schema.jsonify(customer)

# Update Customer
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer.id)
    data = request.get_json()

    updated_customer: Customer = customer_schema.load(
        data,
        instance=customer,
        partial=False
    )

    db.session.commit()

    return customer_schema.jsonify(updated_customer), 201

# Delete Customer
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    db.session.delete(customer)
    db.session.commit()

    return '', 204