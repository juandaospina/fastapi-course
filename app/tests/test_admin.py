from fastapi import status

from .utils import *
from app.config.db import get_db
from app.main import app
from app.models import Tasks
from app.routers.admin import get_current_user 


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_tasks(test_task):
    response = client.get("/admin/tasks")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "title": "Learn Python", "complete": False, 
                                "description": "Learn Python is important", "priority": 4, 
                                "owner_id": 1}]


def test_read_all_users(test_user):
    response = client.get("/admin/users")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"email": "user@example.com", "username": "userexample", "first_name": "John", 
                                "last_name": "Doe", "hashed_password": "22o3-RAdAkgPkuvkjDdr0aBbm2o22uig5NlPnTy5qi4", 
                                "is_active": True, "role": "admin", "phone_number": "123", "id": 1}]


def test_delete_task_by_admin(test_task):
    response = client.delete("/admin/task/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestSessionMaker()
    model = db.query(Tasks).filter(Tasks.id == 1).first()
    assert model is None


def test_delete_task_not_found_by_admin(test_task):
    response = client.delete("/admin/task/4832")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Task with id 4832 does not exist"}

    