from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

"""
Permite establecer una conexión con la base de datos.
check_same_thread es una opción para la limitación de conexión de multiples hilos en sqlite
si es True, sqlite solo permitirá que un hilo se comunique con él, si False, sqlalchemy lanzará 
una excepción si se intenta establecer una conexión de un hilo diferente al que fue creado
previniendo accidentes de la base de datos por corrupción de información
read -> https://docs.python.org/3/library/sqlite3.html
engine = create_engine("sqlite:///./tasksapp.db", connect_args={"check_same_thread": False})
"""
# postgresql connection
engine = create_engine("postgresql://postgres:root@localhost/tasks_app")


""" 
generador de sesiones para crear instancias de sqlalchemy, es decir, que cada sesión iniciada 
es asociada al motor de base de datos definido en engine 
""" 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

"""
clase base para las clases de modelos de sqlalchemy, todas las clases de modelos que se creen
en adelante heredarán de esta clase. Proporcionando funcionalidades adicionales para definir modelos
de datos de una forma mas declarativa
"""
Base = declarative_base()

def get_db():
    """ Inicializa una nueva sesión que es retornada y cerrada
    """
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db is not None:
            db.close()