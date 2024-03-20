from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status

from app.common import CommonDepends
from app.models import Tasks, Users
from .auth import get_current_user


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

UserDepend = Annotated[dict, Depends(get_current_user)]


def user_unauthorized_error():
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authorized"
        )


@router.get("/tasks", status_code=status.HTTP_200_OK)
async def read_all_tasks(user: UserDepend, db: CommonDepends):
    if user is None or user.get("role") != "admin":
        user_unauthorized_error()
    tasks = db.query(Tasks).all()
    return tasks


@router.get("/users", status_code=status.HTTP_200_OK)
async def read_all_users(user: UserDepend, db: CommonDepends):
    if user is None or user.get("role") != "admin":
        user_unauthorized_error()
    users = db.query(Users).all()
    return users


@router.delete("/task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_by_admin(user: UserDepend, db: CommonDepends, task_id: int = Path(gt=0)):
    if user is None or user.get("role") != "admin":
        user_unauthorized_error()
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if task:
        db.query(Tasks).filter(Tasks.id == task_id).delete()
        db.commit()