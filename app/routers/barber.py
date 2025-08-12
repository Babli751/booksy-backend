from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.crud.crud_barber import (
    get_barber_services,
    create_barber_service,
    get_barber_working_hours,
    update_barber_working_hours,
    update_barber_profile
)
from app.models.schemas import (
    Service,
    ServiceCreate,
    WorkingHours,
    WorkingHoursCreate,
    Barber
)
from app.models.models import User

router = APIRouter()

@router.get("/barbers/{barber_id}", response_model=Barber)
def read_barber(barber_id: int, db: Session = Depends(get_db)):
    barber = db.query(User).filter(User.id == barber_id, User.is_barber == True).first()
    if not barber:
        raise HTTPException(status_code=404, detail="Barber not found")
    return barber

@router.get("/barbers/{barber_id}/services", response_model=List[Service])
def read_barber_services(barber_id: int, db: Session = Depends(get_db)):
    return get_barber_services(db, barber_id=barber_id)

@router.post("/barbers/{barber_id}/services", response_model=Service)
def add_barber_service(
    barber_id: int,
    service: ServiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.id != barber_id or not current_user.is_barber:
        raise HTTPException(status_code=403, detail="Only the barber can add services")
    
    return create_barber_service(db=db, service=service, barber_id=barber_id)

@router.get("/barbers/{barber_id}/working-hours", response_model=List[WorkingHours])
def read_barber_working_hours(barber_id: int, db: Session = Depends(get_db)):
    return get_barber_working_hours(db, barber_id=barber_id)

@router.put("/barbers/{barber_id}/working-hours", response_model=List[WorkingHours])
def set_barber_working_hours(
    barber_id: int,
    working_hours: List[WorkingHoursCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.id != barber_id or not current_user.is_barber:
        raise HTTPException(status_code=403, detail="Only the barber can set working hours")
    
    return update_barber_working_hours(db=db, barber_id=barber_id, working_hours=working_hours)

@router.put("/barbers/{barber_id}/profile")
def update_profile(
    barber_id: int,
    bio: str,
    shop_name: str,
    shop_address: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.id != barber_id or not current_user.is_barber:
        raise HTTPException(status_code=403, detail="Only the barber can update profile")
    
    return update_barber_profile(
        db=db,
        barber_id=barber_id,
        bio=bio,
        shop_name=shop_name,
        shop_address=shop_address
    )