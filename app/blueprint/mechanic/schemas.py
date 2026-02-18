from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import Mechanic
from app.extensions import db

class MechanicSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        sqla_session = db.session
        load_instance = True
        include_fk = True

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
