from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, Text, CheckConstraint
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    rating = Column(Float, default=5.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    departure_time = Column(DateTime, nullable=False)
    seats_total = Column(Integer, nullable=False)
    price_per_seat = Column(Float, nullable=False)
    status = Column(String, default="ACTIVE")

    driver = relationship("User")
    bookings = relationship("Booking", back_populates="trip")

    __table_args__ = (
        CheckConstraint("seats_total > 0", name="check_seats_positive"),
        CheckConstraint("price_per_seat > 0", name="check_price_positive"),
    )


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    passenger_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow)

    trip = relationship("Trip", back_populates="bookings")
    passenger = relationship("User")