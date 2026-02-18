from datetime import date
from decimal import Decimal

from sqlalchemy import String, Date, ForeignKey, Column, Table, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db

ticket_mechanic = Table(
    "ticket_mechanic",
    db.metadata,
    Column("service_ticket_id", ForeignKey("service_tickets.id"), primary_key=True),
    Column("mechanic_id", ForeignKey("mechanics.id"), primary_key=True),
)


class Customer(db.Model):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(250), nullable=False)
    last_name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=False)

    service_tickets: Mapped[list["ServiceTicket"]] = relationship(
        back_populates="customer"
    )


class ServiceTicket(db.Model):
    __tablename__ = "service_tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_desc: Mapped[str] = mapped_column(Text, nullable=False)
    vin: Mapped[str] = mapped_column(String(17), nullable=False)
    service_date: Mapped[date] = mapped_column(Date, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)

    customer: Mapped["Customer"] = relationship(back_populates="service_tickets")
    mechanics: Mapped[list["Mechanic"]] = relationship(
        secondary=ticket_mechanic,
        back_populates="service_tickets",
    )


class Mechanic(db.Model):
    __tablename__ = "mechanics"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(250), nullable=False)
    last_name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    salary: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    service_tickets: Mapped[list["ServiceTicket"]] = relationship(
        secondary=ticket_mechanic,
        back_populates="mechanics",
    )
