# Crear espacio Alembic
alembic init [name_folder]
Example: alembic init migrations

# Importante: Configurar variables
alembic.init -> sqlalchemy.url = URI Database connection
migrations/env.py -> target_metadata = Base.metadata

# Crear revisión de Alembic
alembic revision -m "revision name"

# Subir upgrade
alembic upgrade [id]

# Bajar upgrade
alembic downgrade -1
