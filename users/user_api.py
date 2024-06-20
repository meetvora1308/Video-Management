from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import User
from users.controller import UserController
from users.schema import UserCreate, UserResponse

router = APIRouter()


@router.post("/create_user", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    data = UserController(db).register_user(user)
    return data


@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    data = UserController(db).login_user(user)
    return data
