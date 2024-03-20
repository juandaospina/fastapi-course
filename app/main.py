from fastapi import FastAPI

from app.models import *
from app.config.db import engine
from metadata import tags_metadata
from app.routers import auth, task, admin, user

app = FastAPI(openapi_tags=tags_metadata)

""" Crea las tablas en la base de datos (si no existen)
"""
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(task.router)
app.include_router(admin.router)
app.include_router(user.router)

