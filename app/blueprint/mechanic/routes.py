from flask import jsonify, request
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Mechanic
from . import mechanic_bp
from .schemas import mechanic_schema, mechanics_schema


@mechanic_bp.post("/")
def create_mechanic():
    data = request.get_json() or {}
    mechanic: Mechanic = mechanic_schema.load(data)

    db.session.add(mechanic)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Email already exists"}), 409

    return jsonify(mechanic_schema.dump(mechanic)), 201


@mechanic_bp.get("/")
def get_mechanics():
    mechanics = Mechanic.query.all()
    return jsonify(mechanics_schema.dump(mechanics, many=True)), 200


@mechanic_bp.put("/<int:id>")
def update_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    data = request.get_json() or {}

    updated_mechanic: Mechanic = mechanic_schema.load(
        data,
        instance=mechanic,
        partial=False
    )

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Email already exists"}), 409

    return jsonify(mechanic_schema.dump(updated_mechanic)), 200


@mechanic_bp.delete("/<int:id>")
def delete_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)

    db.session.delete(mechanic)
    db.session.commit()

    return "", 204
