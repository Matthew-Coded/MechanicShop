from flask import Flask
from app.extensions import db, ma

def create_app(config_name=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    ma.init_app(app)

    from app.blueprint.customer import customer_bp
    from app.blueprint.mechanic import mechanic_bp
    from app.blueprint.service_ticket import service_ticket_bp

    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(service_ticket_bp, url_prefix="/service-tickets")

    return app
