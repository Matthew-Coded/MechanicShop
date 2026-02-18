from flask import jsonify, request
from app.models import Customer
from app.extensions import db
from . import customer_bp
from .schemas import customer_schema


@customer_bp.post("/")
def create_customer():
    data = request.get_json() or {}
    customer: Customer = customer_schema.load(data)

    db.session.add(customer)
    db.session.commit()

    return jsonify(customer_schema.dump(customer)), 201


@customer_bp.get("/test")
def test_customer():
    return jsonify({"message": "Customer blueprint is working!"}), 200


@customer_bp.get("/")
def get_customers():
    customers = Customer.query.all()
    return jsonify(customer_schema.dump(customers, many=True)), 200


@customer_bp.get("/<int:customer_id>")
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify(customer_schema.dump(customer)), 200


@customer_bp.put("/<int:customer_id>")
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json() or {}

    updated_customer: Customer = customer_schema.load(
        data,
        instance=customer,
        partial=False
    )

    db.session.commit()
    return jsonify(customer_schema.dump(updated_customer)), 200


@customer_bp.delete("/<int:customer_id>")
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    db.session.delete(customer)
    db.session.commit()

    return "", 204
