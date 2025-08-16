from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, SessionLocal
from app.models.models import Base
from app.routers import auth, user, barber, booking

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(user.router, prefix="/api/v1")
app.include_router(barber.router, prefix="/api/v1")
app.include_router(booking.router, prefix="/api/v1", tags=["bookings"])

@app.get("/")
def read_root():
    return {"message": "Barber Booking API"}

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 