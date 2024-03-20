from fastapi import HTTPException
from starlette import status

def user_unauthorized_error():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="User is not authorized"
    )