import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


def test_create_trip_ok():
    resp = client.post("/trips", json={
        "driver_id": 1,
        "origin": "Москва",
        "destination": "Тверь",
        "departure_time": "2026-01-01T10:00:00",
        "seats": 2,
        "price": 500,
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["seats_total"] == 2
    assert data["origin"] == "Москва"


def test_create_trip_zero_seats():
    resp = client.post("/trips", json={
        "driver_id": 1,
        "origin": "A",
        "destination": "B",
        "departure_time": "2026-01-01T10:00:00",
        "seats": 0,
        "price": 500,
    })
    assert resp.status_code == 422


def test_create_trip_negative_price():
    resp = client.post("/trips", json={
        "driver_id": 1,
        "origin": "A",
        "destination": "B",
        "departure_time": "2026-01-01T10:00:00",
        "seats": 2,
        "price": -100,
    })
    assert resp.status_code == 422


def test_get_trip_not_found():
    resp = client.get("/trips/9999")
    assert resp.status_code == 404


def test_booking_ok():
    trip = client.post("/trips", json={
        "driver_id": 1,
        "origin": "A",
        "destination": "B",
        "departure_time": "2026-01-01T10:00:00",
        "seats": 2,
        "price": 500,
    }).json()

    resp = client.post(f"/trips/{trip['id']}/bookings", json={"passenger_id": 2})
    assert resp.status_code == 201
    assert resp.json()["status"] == "PENDING"


def test_booking_no_seats():
    trip = client.post("/trips", json={
        "driver_id": 1,
        "origin": "A",
        "destination": "B",
        "departure_time": "2026-01-01T10:00:00",
        "seats": 1,
        "price": 500,
    }).json()

    client.post(f"/trips/{trip['id']}/bookings", json={"passenger_id": 2})
    resp = client.post(f"/trips/{trip['id']}/bookings", json={"passenger_id": 3})
    assert resp.status_code == 409


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"