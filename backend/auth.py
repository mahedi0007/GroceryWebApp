# backend/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from . import models, schemas, utils
from .database import get_db 
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles 


router = APIRouter(prefix="/api", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = utils.hash_password(user.password)
    new_user = models.User(name=user.name, email=user.email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"success": True, "user": schemas.UserResponse.from_orm(new_user)}

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not utils.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = utils.create_access_token({"sub": str(db_user.id)})
    return {"token": token, "user": schemas.UserResponse.from_orm(db_user)}

@router.get("/users/me", response_model=schemas.UserResponse)
def get_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = utils.decode_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
