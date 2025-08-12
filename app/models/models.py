from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Time, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import time

from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
    phone_number = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    is_barber = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Barber-specific fields (nullable for regular users)
    barber_bio = Column(Text, nullable=True)
    barber_shop_name = Column(String, nullable=True)
    barber_shop_address = Column(String, nullable=True)
    
    services = relationship("Service", back_populates="barber")
    working_hours = relationship("WorkingHours", back_populates="barber")
    bookings = relationship("Booking", back_populates="barber")

class Service(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    duration = Column(Integer)  # in minutes
    price = Column(Float)
    barber_id = Column(Integer, ForeignKey("users.id"))
    
    barber = relationship("User", back_populates="services")
    bookings = relationship("Booking", back_populates="service")

class WorkingHours(Base):
    __tablename__ = "working_hours"
    
    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(Integer)  # 0-6 (Monday-Sunday)
    start_time = Column(Time)
    end_time = Column(Time)
    is_working = Column(Boolean, default=True)
    barber_id = Column(Integer, ForeignKey("users.id"))
    
    barber = relationship("User", back_populates="working_hours")

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    customer_email = Column(String)
    customer_phone = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    notes = Column(Text, nullable=True)
    status = Column(String, default="confirmed")  # confirmed, cancelled, completed
    barber_id = Column(Integer, ForeignKey("users.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    barber = relationship("User", back_populates="bookings")
    service = relationship("Service", back_populates="bookings")