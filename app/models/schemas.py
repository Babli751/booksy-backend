from datetime import datetime, time, date
from typing import Optional, List
from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    phone_number: Optional[str] = None

class UserCreate(UserBase):
    password: str
    is_barber: bool = False

class User(UserBase):
    id: int
    is_active: bool
    is_barber: bool
    
    class Config:
        from_attributes = True

class Barber(User):
    barber_bio: Optional[str] = None
    barber_shop_name: Optional[str] = None
    barber_shop_address: Optional[str] = None
    
    class Config:
        from_attributes = True

class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    duration: int
    price: float

class ServiceCreate(ServiceBase):
    pass

class Service(ServiceBase):
    id: int
    barber_id: int
    
    class Config:
        from_attributes = True

class WorkingHoursBase(BaseModel):
    day_of_week: int
    start_time: time
    end_time: time
    is_working: bool = True

class WorkingHoursCreate(WorkingHoursBase):
    pass

class WorkingHours(WorkingHoursBase):
    id: int
    barber_id: int
    
    class Config:
        from_attributes = True

class BookingBase(BaseModel):
    customer_name: str
    customer_email: EmailStr
    customer_phone: str
    start_time: datetime
    service_id: int
    notes: Optional[str] = None

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    barber_id: int
    end_time: datetime
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class BarberWithServicesAndHours(Barber):
    services: List[Service] = []
    working_hours: List[WorkingHours] = []
    
    class Config:
        from_attributes = True

class AvailableSlots(BaseModel):
    date: date
    available_times: List[datetime]