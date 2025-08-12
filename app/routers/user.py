from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.crud.crud_user import get_user, get_user_by_email, get_users, create_user,get_barbers
from app.models.schemas import User, UserCreate, Barber

router = APIRouter()

@router.post("/users", response_model=User)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)

@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/users", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.get("/barbers", response_model=List[Barber])
def read_barbers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    barbers = get_barbers(db, skip=skip, limit=limit)
    return barbers