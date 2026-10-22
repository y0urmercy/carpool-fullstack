from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TripCreate(BaseModel):
    driver_id: int
    origin: str = Field(..., min_length=1)
    destination: str = Field(..., min_length=1)
    departure_time: datetime
    seats: int = Field(..., ge=1, le=4)
    price: float = Field(..., gt=0)


class TripOut(BaseModel):
    id: int
    origin: str
    destination: str
    departure_time: datetime
    seats_total: int
    price_per_seat: float
    status: str

    class Config:
        from_attributes = True


class BookingCreate(BaseModel):
    passenger_id: int


class BookingOut(BaseModel):
    id: int
    trip_id: int
    passenger_id: int
    status: str

    class Config:
        from_attributes = True