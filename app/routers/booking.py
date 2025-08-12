from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.crud.crud_booking import (
    get_bookings,
    get_customer_bookings,
    create_booking,
    cancel_booking,
    get_available_slots
)
from app.models.schemas import Booking, BookingCreate, AvailableSlots
from app.models.models import User, Booking as BookingModel  # Booking modelini import edin

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("/bookings", response_model=Booking, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Berber kontrolü
    barber = db.query(User).filter(
        User.id == booking.barber_id,
        User.is_barber == True
    ).first()
    if not barber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Barber not found"
        )

    # Müşteri bilgilerini otomatik doldur
    booking_data = booking.dict()
    booking_data.update({
        "customer_email": current_user.email,
        "customer_name": current_user.full_name or booking.customer_name,
        "customer_phone": current_user.phone_number or booking.customer_phone
    })

    try:
        return create_booking(db=db, booking_data=booking_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )