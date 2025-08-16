from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Annotated

from app.core import security
from app.core.config import settings
from app.crud.crud_user import create_user, get_user_by_email
from app.models.schemas import UserCreate, Token, User
from app.models.models import User as DBUser
from app.core.database import get_db

router = APIRouter(tags=["auth"])

async def get_current_user(
    token: Annotated[str, Depends(security.oauth2_scheme)],
    db: Session = Depends(get_db)
) -> DBUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        email = security.verify_token(token, credentials_exception)
        user = get_user_by_email(db, email=email)
        if user is None:
            raise credentials_exception
        return user
    except Exception as e:
        raise credentials_exception

# auth.py'de register endpointi kontrolü
@router.post("/register")
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    print("Gelen veri:", user_data)  # Gelen veriyi logla
    db_user = get_user_by_email(db, email=user_data.email)
    if db_user:
        print("Email zaten kayıtlı")  # Debug log
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = create_user(db, user_data)
    print("Oluşturulan kullanıcı:", user.id)  # Debug log
    return {"status": "success", "id": user.id}

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def read_current_user(
    current_user: Annotated[DBUser, Depends(get_current_user)]
):
    return current_user