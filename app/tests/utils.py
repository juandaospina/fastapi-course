import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient 

from app.main import app
from app.config.db import Base
from app.models import Tasks, Users


SQLALCHEMY_BASE_URL = 'sqlite:///./tasks_app_test.db'

engine = create_engine(
    SQLALCHEMY_BASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestSessionMaker = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base.metadata.create_all(bind=engine)
client = TestClient(app)


def override_get_db():
    db = None
    try:
        db = TestSessionMaker()
        yield db
    finally:
        if db is not None:
            db.close()


def override_get_current_user():
    return {"username": "jospina", "id": 1, "role": "admin"}


@pytest.fixture
def test_task():
    task = Tasks( 
        title = "Learn Python",
        description = "Learn Python is important",
        priority = 4,
        complete = False,
        owner_id = 1
    )
    db = TestSessionMaker()
    db.add(task)
    db.commit()
    yield task
    with engine.connect() as conn:
        conn.execute(text("DELETE from tasks;"))
        conn.commit()


@pytest.fixture
def test_user():
    user = Users(
        email = "user@example.com",
        username = "userexample",
        first_name = "John",
        last_name = "Doe",
        hashed_password = "22o3-RAdAkgPkuvkjDdr0aBbm2o22uig5NlPnTy5qi4",
        is_active = True,
        role = "admin",
        phone_number = "123"
    )
    db = TestSessionMaker()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as conn:
        conn.execute(text("DELETE from users;"))
        conn.commit()
