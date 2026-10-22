from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/trips/{trip_id}/bookings", tags=["bookings"])


@router.post("", response_model=schemas.BookingOut, status_code=201)
def create_booking(
    trip_id: int,
    booking: schemas.BookingCreate,
    db: Session = Depends(get_db),
):
    trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    active_bookings = (
        db.query(models.Booking)
        .filter(
            models.Booking.trip_id == trip_id,
            models.Booking.status.in_(["PENDING", "CONFIRMED"]),
        )
        .count()
    )
    if active_bookings >= trip.seats_total:
        raise HTTPException(status_code=409, detail="No seats available")

    db_booking = models.Booking(
        trip_id=trip_id,
        passenger_id=booking.passenger_id,
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking