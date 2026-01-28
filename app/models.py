from sqlalchemy import String, Integer, Date, ForeignKey, Column, Table, Float, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from decimal import Decimal
from datetime import date
from flask_sqlalchemy import SQLAlchemy



class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


ticket_mechanic = Table(
    'ticket_mechanic',
    Base.metadata,
    Column('service_ticket_id', ForeignKey('service_tickets.id'), primary_key=True),
    Column('mechanic_id', ForeignKey('mechanics.id'), primary_key=True),
)
    # Relationships


class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(250), nullable=False)
    last_name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=False)

    # Relationships
    service_tickets: Mapped[list["ServiceTicket"]] = relationship(
        back_populates="customer",
    )


class ServiceTicket(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    service_desc: Mapped[str] = mapped_column(Text, nullable=False)
    vin: Mapped[str] = mapped_column(String(17), nullable=False)
    service_date: Mapped[date] = mapped_column(Date, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    # Foreign Keys
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'), nullable=False)

    # Relationships
    customer: Mapped["Customer"] = relationship(back_populates="service_tickets")
    mechanics: Mapped[list["Mechanic"]] = relationship(
        secondary=ticket_mechanic,
        back_populates="service_tickets"
    )




class Mechanic(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(250), nullable=False)
    last_name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    salary: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    # Relationships
    service_tickets: Mapped[list["ServiceTicket"]] = relationship(
        secondary=ticket_mechanic,
        back_populates="mechanics"
    )


