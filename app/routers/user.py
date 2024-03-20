from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from .auth import CommonDepends, get_current_user, bcrypt
from app.common.functions import user_unauthorized_error
from app.models import Users
from app.schemas.user_schema import UserResetPasswordSchema, UserPUTSchema


router = APIRouter(
    prefix="/user",
    tags=["User"],    
)


UserDepend = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(db: CommonDepends, user: UserDepend):
    if user is None: user_unauthorized_error()

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user_model


@router.put("/reset-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(db: CommonDepends, user: UserDepend, body: UserResetPasswordSchema):
    if user is None: user_unauthorized_error()
    
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if not bcrypt.verify(body.password, user_model.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error verifying password"
        )
    else:
        user_model.hashed_password = bcrypt.hash(body.new_password)
        db.add(user_model)
        db.commit()


@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
async def upgrade_user(db: CommonDepends, user: UserDepend, user_body: UserPUTSchema):
    if user is None: user_unauthorized_error()
    
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_model:
        for key, value in user_body.model_dump().items():
            setattr(user_model, key, value)
            db.add(user_model)
            db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Error updating user"
        )
    
    

    
