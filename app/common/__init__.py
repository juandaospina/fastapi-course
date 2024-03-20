from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.db import get_db

""" Uso de anotación de tipos para definir la dependencia a la 
inicialización de la base de datos en cada operación de ruta
"""
CommonDepends = Annotated[Session, Depends(get_db)]