from typing import Annotated

from fastapi import Depends, HTTPException, Path, APIRouter
from starlette import status

from app.models import Tasks
from app.schemas.task_schema import TaskBodySchema
from app.common import CommonDepends
from app.common.functions import user_unauthorized_error
from .auth import get_current_user


router = APIRouter(tags=["Tasks"])
UserDepend = Annotated[dict, Depends(get_current_user)]


def find_task_by_id_and_owner(db: CommonDepends, user: UserDepend, task_id: int):
    task_model = db.query(Tasks).where(Tasks.id == task_id).filter(
        Tasks.owner_id == user.get("id")
    ).first()
    return task_model


@router.get("/tasks", status_code=status.HTTP_200_OK)
async def get_all_tasks(db: CommonDepends, user: UserDepend):
    """ Método que permite la recuperación de todos los
    registros de tareas por usuario autenticado
    """
    if user is None: user_unauthorized_error()

    try:
        tasks = db.query(Tasks).where(Tasks.owner_id == user.get("id")).all() 
        return tasks
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        ) 


@router.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def get_task_by_id(task_id: int, db: CommonDepends, user: UserDepend):
    """ Permite recuperar una registro de tarea por su ID 
    """
    if user is None: user_unauthorized_error()
    
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} does not exist"
        )
    
    if task.owner_id == user.get("id"):
        return task
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not find searched task"
        )


@router.post("/task", status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskBodySchema, user: UserDepend, db: CommonDepends):
    try:
        if user is not None:
            task = Tasks(**task.model_dump(), owner_id=user.get("id"))
            db.add(task)
            db.commit()
    except Exception as e: 
        print("[POST/task]", e)
        # Revierte cambios no confirmados (no commited)
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating task")


@router.put("/task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_task(db: CommonDepends, user: UserDepend, 
                      task_request: TaskBodySchema, task_id: int = Path(gt=0)):
    if user is None: user_unauthorized_error()    

    task = find_task_by_id_and_owner(db, user, task_id)
    if task:
        for key, value in task_request.model_dump().items():
            setattr(task, key, value)
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Failed to update task, task not found"
        )


@router.delete("/task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(db: CommonDepends, user: UserDepend, task_id: int = Path(gt=0)):
    if user is None: user_unauthorized_error()

    task = find_task_by_id_and_owner(db, user, task_id)
    if task:
        db.query(Tasks).where(Tasks.id == task_id).delete()
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Error, not found or invalid task id"
        )
