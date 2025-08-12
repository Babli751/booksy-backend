from sqlalchemy.orm import Session
from typing import Optional

from app.models.models import User
from app.models.schemas import UserCreate
from app.core.security import get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        phone_number=user.phone_number,
        is_barber=user.is_barber
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_barbers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).filter(User.is_barber == True).offset(skip).limit(limit).all()