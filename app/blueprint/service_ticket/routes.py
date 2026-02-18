from flask import jsonify, request
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import ServiceTicket, Mechanic
from . import service_ticket_bp
from .schemas import service_ticket_schema, service_tickets_schema


@service_ticket_bp.post("/")
def create_service_ticket():
    data = request.get_json() or {}
    ticket: ServiceTicket = service_ticket_schema.load(data)

    db.session.add(ticket)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Invalid data (check required fields / foreign keys)"}), 400

    return jsonify(service_ticket_schema.dump(ticket)), 201


@service_ticket_bp.put("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>")
def assign_mechanic(ticket_id, mechanic_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)
        db.session.commit()

    return jsonify(service_ticket_schema.dump(ticket)), 200


@service_ticket_bp.put("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>")
def remove_mechanic(ticket_id, mechanic_id):
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    if mechanic in ticket.mechanics:
        ticket.mechanics.remove(mechanic)
        db.session.commit()

    return jsonify(service_ticket_schema.dump(ticket)), 200


@service_ticket_bp.get("/")
def get_service_tickets():
    tickets = ServiceTicket.query.all()
    return jsonify(service_tickets_schema.dump(tickets, many=True)), 200
