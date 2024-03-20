import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette import status
from pydantic import BaseModel

from app.schemas.user_schema import UserBodySchema
from app.models import Users
from app.common import CommonDepends

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

bcrypt = CryptContext(schemes=["bcrypt"], deprecated=["auto"])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

class Token(BaseModel):
    access_token: str
    token_type: str


def validate_user(username: str, password: str, db: CommonDepends):
    user = db.query(Users).where(Users.username == username).first()
    if user is None:
        return False
    if not bcrypt.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow(timezone.utc) + timedelta(minutes=20)
    encode.update({"exp": expire})
    return jwt.encode(encode, os.environ.get("SECRET_SIGN"), algorithm="HS256")


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, os.environ.get("SECRET_SIGN"), algorithms=["HS256"])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")
        if username is None and user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user"
            ) 

        return {"username": username, "id": user_id, "role": user_role}
    except JWTError as jwt_error:
        print(jwt_error)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user"
        )


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(db: CommonDepends, user: UserBodySchema):
    try:
        user_model = Users(
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            hashed_password=bcrypt.hash(user.password),
            role=user.role,
            phone_number=user.phone_number
        )
        db.add(user_model)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Server Error")


@router.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
                                 db: CommonDepends):
    user = validate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user credentials"
        )
    
    token = create_access_token(
        data={"sub": user.username, "id": user.id, "role": user.role}, 
        expires_delta=timedelta(minutes=20)
    )
    return {"access_token": token, "token_type": "bearer"}
