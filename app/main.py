from fastapi import FastAPI
from .database import engine, Base
from .routers import trips, bookings

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CarPool API",
    version="1.0.0",
    description="API сервиса совместных поездок",
)

app.include_router(trips.router)
app.include_router(bookings.router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}