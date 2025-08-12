from datetime import datetime, timedelta, date, time
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, not_

from app.models.models import Booking, Service, WorkingHours
from app.models.schemas import BookingCreate, AvailableSlots

def get_bookings(db: Session, barber_id: int, skip: int = 0, limit: int = 100):
    return db.query(Booking).filter(Booking.barber_id == barber_id).offset(skip).limit(limit).all()

def get_customer_bookings(db: Session, customer_email: str):
    return db.query(Booking).filter(Booking.customer_email == customer_email).all()

def create_booking(db: Session, booking_data: dict):
    # Servis süresini al
    service = db.query(Service).filter(Service.id == booking_data["service_id"]).first()
    if not service:
        raise ValueError("Service not found")
    
    # Bitiş zamanını hesapla
    start_time = booking_data["start_time"]
    end_time = start_time + timedelta(minutes=service.duration)
    
    db_booking = BookingModel(
        **booking_data,
        end_time=end_time,
        status="confirmed"
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def cancel_booking(db: Session, booking_id: int):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        return None
    
    booking.status = "cancelled"
    db.commit()
    db.refresh(booking)
    return booking

def get_available_slots(db: Session, barber_id: int, service_id: int, selected_date: date):
    # Get service duration
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        return None
    
    # Get barber's working hours for the selected day
    day_of_week = selected_date.weekday()
    working_hours = db.query(WorkingHours).filter(
        WorkingHours.barber_id == barber_id,
        WorkingHours.day_of_week == day_of_week,
        WorkingHours.is_working == True
    ).first()
    
    if not working_hours:
        return AvailableSlots(date=selected_date, available_times=[])
    
    # Get all bookings for the selected date
    start_of_day = datetime.combine(selected_date, time.min)
    end_of_day = datetime.combine(selected_date, time.max)
    
    bookings = db.query(Booking).filter(
        Booking.barber_id == barber_id,
        Booking.start_time >= start_of_day,
        Booking.start_time <= end_of_day,
        Booking.status == "confirmed"
    ).all()
    
    # Generate time slots
    slot_duration = timedelta(minutes=service.duration)
    current_time = datetime.combine(selected_date, working_hours.start_time)
    end_time = datetime.combine(selected_date, working_hours.end_time)
    
    available_slots = []
    while current_time + slot_duration <= end_time:
        # Check if slot is available
        slot_available = True
        for booking in bookings:
            if (current_time < booking.end_time) and (current_time + slot_duration > booking.start_time):
                slot_available = False
                break
        
        if slot_available:
            available_slots.append(current_time)
        
        # Move to next slot (with 15 minutes interval between slots)
        current_time += timedelta(minutes=15)
    
    return AvailableSlots(date=selected_date, available_times=available_slots)