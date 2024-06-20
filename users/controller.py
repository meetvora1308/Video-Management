from fastapi import HTTPException, status

from database.models import User
from users.auth import authenticate_user, create_access_token, get_password_hash
from users.schema import Token, UserCreate


class UserController:
    def __init__(self, db):
        self.db = db

    def register_user(self, user: UserCreate):
        hashed_password = get_password_hash(user.password)
        db_user = User(username=user.username, hashed_password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def login_user(self, user: UserCreate):
        user = authenticate_user(self.db, user.username, user.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": user.username})
        return Token(access_token=access_token, token_type="bearer")
