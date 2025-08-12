from sqlalchemy.orm import Session
from typing import List

from app.models.models import Service, WorkingHours
from app.models.schemas import ServiceCreate, WorkingHoursCreate

def get_barber_services(db: Session, barber_id: int):
    return db.query(Service).filter(Service.barber_id == barber_id).all()

def create_barber_service(db: Session, service: ServiceCreate, barber_id: int):
    db_service = Service(**service.dict(), barber_id=barber_id)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

def get_barber_working_hours(db: Session, barber_id: int):
    return db.query(WorkingHours).filter(WorkingHours.barber_id == barber_id).all()

def update_barber_working_hours(db: Session, barber_id: int, working_hours: List[WorkingHoursCreate]):
    # First delete existing working hours
    db.query(WorkingHours).filter(WorkingHours.barber_id == barber_id).delete()
    
    # Add new working hours
    new_hours = []
    for wh in working_hours:
        db_wh = WorkingHours(**wh.dict(), barber_id=barber_id)
        db.add(db_wh)
        new_hours.append(db_wh)
    
    db.commit()
    return new_hours

def update_barber_profile(db: Session, barber_id: int, bio: str, shop_name: str, shop_address: str):
    barber = db.query(User).filter(User.id == barber_id).first()
    if not barber:
        return None
    
    barber.barber_bio = bio
    barber.barber_shop_name = shop_name
    barber.barber_shop_address = shop_address
    db.commit()
    db.refresh(barber)
    return barber