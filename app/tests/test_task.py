import pytest
from fastapi import status

from app.config.db import get_db
from app.main import app
from app.routers.task import get_current_user
from app.models import Tasks
from .utils import *


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_get_all_tasks(test_task):
    response = client.get("/tasks")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"id": 1, "title": "Learn Python", "complete": False,
                                "description": "Learn Python is important", "priority": 4, "owner_id": 1}]
    

def test_get_task_by_id(test_task):
    response = client.get("/tasks/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 1, "title": "Learn Python", "complete": False,
                                "description": "Learn Python is important", "priority": 4, "owner_id": 1}


def test_task_by_id_not_found():
    response = client.get("/tasks/9393")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Task with id 9393 does not exist"}


def test_create_task(test_task):
    payload = {
        "title": "New task",
        "description": "Task description",
        "priority": 3,
        "complete": False,
    }
    response = client.post("/task", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestSessionMaker()
    _created_task = db.query(Tasks).filter(Tasks.id == 2).first()
    assert _created_task.title == payload.get("title")
    assert _created_task.description == payload.get("description")
    assert _created_task.priority == payload.get("priority")
    assert _created_task.complete == payload.get("complete")


def test_update_task(test_task):
    payload = {
        "title": "Learn FastAPI",
        "description": "Learn Python is important",
        "priority": 4,
        "complete": True,
    }
    response = client.put("/task/1", json=payload)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    db = TestSessionMaker()
    model = db.query(Tasks).filter(Tasks.id == 1).first()
    assert model.title == payload.get("title")
    assert model.complete == payload.get("complete")


def test_update_task_not_found(test_task):
    payload = {
        "title": "Learn Flask",
        "description": "Flask is a good tool",
        "priority": 4,
        "complete": False,
    }
    response = client.put("/task/14", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Failed to update task, task not found"}


def test_delete_task(test_task):
    response = client.delete("/task/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestSessionMaker()
    model = db.query(Tasks).filter(Tasks.id == 1).first()
    assert model is None


def test_delete_task_not_found(test_task):
    response = client.delete("/task/1849")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error, not found or invalid task id"}
